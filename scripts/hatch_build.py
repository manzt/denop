import urllib.request
import zipfile
import platform
import os
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface


SELF_DIR = Path(__file__).parent

# these are the binaries provided by deno, mapped to a python tag
binary_to_tag = {
    "deno-x86_64-apple-darwin.zip": "py3-none-macosx_10_12_x86_64",
    "deno-aarch64-apple-darwin.zip": "py3-none-macosx_11_0_arm64",
    "deno-aarch64-unknown-linux-gnu.zip": "py3-none-manylinux_2_17_aarch64",
    "deno-x86_64-pc-windows-msvc.zip": "py3-none-win_amd64",
    "deno-x86_64-unknown-linux-gnu.zip": "py3-none-manylinux_2_17_x86_64",
}


def detect_platform() -> tuple[str, str]:
    """Detect the platform and architecture."""
    system = platform.system().lower()
    os_name = {
        "darwin": "apple-darwin",
        "linux": "unknown-linux-gnu",
        "windows": "pc-windows-msvc",
    }.get(system)
    if not os_name:
        raise RuntimeError(f"Unsupported OS: {system}")

    arch = platform.machine().lower()
    if arch in {"x86_64", "amd64"}:
        arch = "x86_64"
    elif arch in {"aarch64", "arm64"}:
        arch = "aarch64"
    else:
        raise RuntimeError(f"Unsupported architecture: {arch}")

    return os_name, arch


def download_deno_bin(dir: Path, version: str, zname: str) -> Path:
    assert zname in binary_to_tag, f"Unsupported binary: {zname}"
    url = f"https://github.com/denoland/deno/releases/download/v{version}/{zname}"

    with urllib.request.urlopen(url) as resp, (dir / zname).open("wb") as out_file:
        out_file.write(resp.read())

    with zipfile.ZipFile(dir / zname, "r") as zf:
        for fname in zf.namelist():
            if fname in ("deno", "deno.exe"):
                with (dir / fname).open("wb") as out_file:
                    out_file.write(zf.read(fname))
            return dir / fname

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
