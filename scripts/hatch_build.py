import contextlib
import functools
import hashlib
import re
import urllib.request
import zipfile
import platform
import os
import stat
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


SELF_DIR = Path(__file__).parent
CHUNK_SIZE = 1 << 17

# see https://github.com/denoland/deno/issues/30432
MIN_SUPPORTED_GLIBC = (2, 27)
MIN_GLIBC_STR = "_".join(map(str, MIN_SUPPORTED_GLIBC))

# these are the binaries provided by deno, mapped to a python tag
binary_to_tag = {
    "deno-x86_64-apple-darwin.zip": "py3-none-macosx_10_12_x86_64",
    "deno-aarch64-apple-darwin.zip": "py3-none-macosx_11_0_arm64",
    "deno-aarch64-unknown-linux-gnu.zip": f"py3-none-manylinux_{MIN_GLIBC_STR}_aarch64",
    "deno-x86_64-pc-windows-msvc.zip": "py3-none-win_amd64",
    "deno-x86_64-unknown-linux-gnu.zip": f"py3-none-manylinux_{MIN_GLIBC_STR}_x86_64",
}

SUPPORTED_PLATFORMS = {
    "darwin": ("apple-darwin", {"x86_64", "aarch64"}),
    "linux": ("unknown-linux-gnu", {"x86_64", "aarch64"}),
    "windows": ("pc-windows-msvc", {"x86_64"}),
}


def detect_platform() -> tuple[str, str]:
    """Detect the platform and architecture."""
    system = platform.system().lower()
    os_name, supported_arch = SUPPORTED_PLATFORMS.get(system, (None, None))
    if not os_name:
        raise RuntimeError(f"Unsupported OS: {system}")

    arch = platform.machine().lower()
    if arch in {"x86_64", "amd64"}:
        arch = "x86_64"
    elif arch in {"aarch64", "arm64"}:
        arch = "aarch64"
    if arch not in supported_arch:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    if system == "linux":
        libc_ver = None
        with contextlib.suppress(OSError):
            libc_ver = platform.libc_ver()
        if not isinstance(libc_ver, tuple) or "glibc" not in libc_ver:
            raise RuntimeError("Non-glibc Linux platforms are unsupported")
        version_tuple = tuple(map(int, libc_ver[1].split(".")[:2]))
        if version_tuple < MIN_SUPPORTED_GLIBC:
            raise RuntimeError(
                f"The minimum supported version of glibc is {MIN_GLIBC_STR}"
            )

    return os_name, arch


def download_deno_bin(dir: Path, version: str, zname: str) -> Path:
    assert zname in binary_to_tag, f"Unsupported binary: {zname}"
    url = f"https://github.com/denoland/deno/releases/download/v{version}/{zname}"

    with urllib.request.urlopen(f"{url}.sha256sum") as resp:
        sum_text = resp.read().decode()

    match = re.search(r"[0-9A-Fa-f]{64}", sum_text)
    if not match:
        raise RuntimeError(f"Unable to verify integrity of {zname}")
    expected_hash = match.group(0).lower()

    with urllib.request.urlopen(url) as resp, (dir / zname).open("wb") as out_file:
        reader = functools.partial(resp.read, CHUNK_SIZE)
        hasher = hashlib.sha256()

        for chunk in iter(reader, b""):
            out_file.write(chunk)
            hasher.update(chunk)

        hexdigest = hasher.hexdigest()
        if hexdigest != expected_hash:
            raise RuntimeError(f"{zname} hash mismatch: {hexdigest} != {expected_hash}")

    with zipfile.ZipFile(dir / zname, "r") as zf:
        for fname in zf.namelist():
            if fname in ("deno", "deno.exe"):
                out_path = dir / fname
                with out_path.open("wb") as out_file:
                    out_file.write(zf.read(fname))
                # Set executable permission bit
                out_stat = out_path.stat()
                out_path.chmod(
                    out_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                )
                return out_path

    raise FileNotFoundError("Binary 'deno' not found in archive.")


def resolve_deno_archive_name():
    if "DENO_ARCHIVE_TARGET" in os.environ:
        return os.environ["DENO_ARCHIVE_TARGET"]
    os_name, arch = detect_platform()
    return f"deno-{arch}-{os_name}.zip"


class CustomHook(BuildHookInterface):
    def initialize(self, version: str, build_data: dict) -> None:
        if self.target_name == "sdist":
            return

        zname = resolve_deno_archive_name()
        deno = download_deno_bin(
            Path(self.directory),
            os.environ.get("DENO_VERSION", self.metadata.version),
            zname,
        )
        build_data["tag"] = binary_to_tag[zname]
        build_data["shared_scripts"][str(deno.absolute())] = f"src/{deno.name}"

    def finalize(self, version: str, build_data: dict, artifact_path: str) -> None:
        if self.target_name == "sdist":
            return
        build = Path(self.directory)
        (build / "deno").unlink(missing_ok=True)
        (build / "deno.exe").unlink(missing_ok=True)
        for f in build.glob("*.zip"):
            f.unlink(missing_ok=True)
