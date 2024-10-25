from __future__ import annotations

import os
import sys
import sysconfig


def find_deno_bin() -> str:
    """Return the deno binary path."""

    deno_exe = "deno" + sysconfig.get_config_var("EXE")

    path = os.path.join(sysconfig.get_path("scripts"), deno_exe)
    if os.path.isfile(path):
        return path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    path = os.path.join(sysconfig.get_path("scripts", scheme=user_scheme), deno_exe)
    if os.path.isfile(path):
        return path

    # Search in `bin` adjacent to package root (as created by `pip install --target`).
    pkg_root = os.path.dirname(os.path.dirname(__file__))
    target_path = os.path.join(pkg_root, "bin", deno_exe)
    if os.path.isfile(target_path):
        return target_path

    raise FileNotFoundError(path)
