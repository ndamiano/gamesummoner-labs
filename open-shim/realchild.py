"""The real-files child: pyexec's child with the game folder as the filesystem.

Landlock confines every path to the game folder (read, write, make, remove) plus Python's own
library (read only, for imports); seccomp still denies processes, network, mounts, links and
symlinks. The program runs with the game folder as its working directory.
"""

import ctypes
import fnmatch  # noqa: F401
import glob  # noqa: F401
import io
import os
import pathlib  # noqa: F401
import shutil  # noqa: F401
import socket
import struct
import sys
import sysconfig
import traceback

from maestro.codegen.pyexec import child as base
from maestro.codegen.pyexec import rpc, seccomp

SYS_CREATE, SYS_ADD, SYS_RESTRICT = 444, 445, 446
CREATE_RULESET_VERSION = 1
RULE_PATH_BENEATH = 1

WRITE_FILE, READ_FILE, READ_DIR, REMOVE_DIR, REMOVE_FILE = 1 << 1, 1 << 2, 1 << 3, 1 << 4, 1 << 5
MAKE_DIR, MAKE_REG, REFER, TRUNCATE = 1 << 7, 1 << 8, 1 << 13, 1 << 14
EVERY_FS_V1 = (1 << 13) - 1
GAME = WRITE_FILE | READ_FILE | READ_DIR | REMOVE_DIR | REMOVE_FILE | MAKE_DIR | MAKE_REG
LIBRARY = READ_FILE | READ_DIR

FS_CALLS = {"open", "openat", "openat2", "unlink", "unlinkat", "rename", "renameat", "renameat2",
            "mkdir", "mkdirat", "rmdir", "creat", "truncate"}

_libc = ctypes.CDLL(None, use_errno=True)
_libc.syscall.restype = ctypes.c_long


def _landlock(root: str) -> None:
    abi = _libc.syscall(SYS_CREATE, None, ctypes.c_size_t(0), ctypes.c_uint32(CREATE_RULESET_VERSION))
    if abi < 1:
        raise OSError(ctypes.get_errno(), "landlock unavailable")
    handled = EVERY_FS_V1
    game = GAME
    if abi >= 2:
        handled |= REFER
        game |= REFER
    if abi >= 3:
        handled |= TRUNCATE
        game |= TRUNCATE
    if abi >= 5:
        handled |= 1 << 15
    attr = struct.pack("QQQ", handled, 0b11 if abi >= 4 else 0, 0b11 if abi >= 6 else 0)
    size = 8 if abi < 4 else (16 if abi < 6 else 24)
    buf = ctypes.create_string_buffer(attr[:size], size)
    fd = _libc.syscall(SYS_CREATE, buf, ctypes.c_size_t(size), ctypes.c_uint32(0))
    if fd < 0:
        raise OSError(ctypes.get_errno(), "landlock_create_ruleset failed")
    library = {sysconfig.get_paths()[k] for k in ("stdlib", "platstdlib", "purelib", "platlib")}
    for path, access in [(root, game)] + [(p, LIBRARY) for p in library if os.path.isdir(p)]:
        dirfd = os.open(path, os.O_PATH | os.O_CLOEXEC)
        rule = ctypes.create_string_buffer(struct.pack("=Qi", access, dirfd), 12)
        if _libc.syscall(SYS_ADD, ctypes.c_int(fd), ctypes.c_int(RULE_PATH_BENEATH), rule,
                         ctypes.c_uint32(0)) != 0:
            raise OSError(ctypes.get_errno(), f"landlock_add_rule failed for {path}")
        os.close(dirfd)
    if _libc.prctl(38, 1, 0, 0, 0) != 0:
        raise OSError(ctypes.get_errno(), "PR_SET_NO_NEW_PRIVS failed")
    if _libc.syscall(SYS_RESTRICT, ctypes.c_int(fd), ctypes.c_uint32(0)) != 0:
        raise OSError(ctypes.get_errno(), "landlock_restrict_self failed")
    os.close(fd)


def main() -> int:
    sock = socket.socket(fileno=int(os.environ["PYEXEC_FD"]))
    code = sys.stdin.read()
    root = os.environ["PYEXEC_ROOT"]

    try:
        _landlock(root)
        os.chdir(root)
        seccomp.DENIED_X86_64 = {k: v for k, v in seccomp.DENIED_X86_64.items() if v not in FS_CALLS}
        seccomp.DENIED_AARCH64 = {k: v for k, v in seccomp.DENIED_AARCH64.items()
                                  if v not in FS_CALLS}
        seccomp.install()
    except Exception as e:
        print(f"pyexec: could not confine the process: {e}", file=sys.stderr)
        return 3

    for name in ("socket", "subprocess", "ctypes", "tempfile", "platform", "inspect", "pickle",
                 "webbrowser", "urllib", "http"):
        sys.modules.pop(name, None)

    out = io.StringIO()
    ns = {"__name__": "__main__", "__builtins__": __builtins__}
    ns.update({name: base._stub(sock, name) for name in base.TOOLS})

    status = 0
    sys.stdout = out
    try:
        exec(compile(code, "<program>", "exec"), ns)
    except SystemExit:
        pass
    except BaseException:
        tb = traceback.format_exc()
        keep = [line for line in tb.splitlines(keepends=True)
                if "realchild.py" not in line and "in main" not in line]
        out.write("\n" + "".join(keep))
        status = 1
    finally:
        sys.stdout = sys.__stdout__

    rpc.send(sock, {"done": True, "stdout": out.getvalue(), "status": status})
    sock.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
