from __future__ import annotations

import os
import pathlib
import sys
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


if sys.platform == "win32":
    _PathBase = pathlib.WindowsPath
else:
    _PathBase = pathlib.PosixPath


disk_sync = os.fsync
# https://mjtsai.com/blog/2022/02/17/apple-ssd-benchmarks-and-f_fullsync/
# https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fsync.2.html
if sys.platform == "darwin":
    import fcntl

    if hasattr(fcntl, "F_FULLFSYNC"):

        def disk_sync(fd) -> None:
            fcntl.fcntl(fd, fcntl.F_FULLFSYNC)


class Path(_PathBase):
    def ensure_dir_exists(self) -> None:
        self.mkdir(parents=True, exist_ok=True)

    def ensure_parent_dir_exists(self) -> None:
        self.parent.mkdir(parents=True, exist_ok=True)

    def expand(self) -> Path:
        return Path(os.path.expanduser(os.path.expandvars(self)))

    def resolve(self, strict: bool = False) -> Path:  # noqa: FBT001, FBT002
        # https://bugs.python.org/issue38671
        return Path(os.path.realpath(self))

    def remove(self) -> None:
        if self.is_file():
            os.remove(self)
        elif self.is_dir():
            import shutil

            shutil.rmtree(self, ignore_errors=False)

    def write_atomic(self, data: str | bytes, *args: Any, **kwargs: Any) -> None:
        from tempfile import mkstemp

        fd, path = mkstemp(dir=self.parent)
        with os.fdopen(fd, *args, **kwargs) as f:
            f.write(data)
            f.flush()
            disk_sync(fd)

        os.replace(path, self)


def load_toml_data(data: str) -> dict[str, Any]:
    return tomllib.loads(data)


def load_toml_file(path: str) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return tomllib.loads(f.read())
