"""The arm: programs run in realchild.py, with real file access confined to the game folder."""

import subprocess
import types

FILE_MODULES = {"os", "pathlib", "glob", "shutil", "io", "fnmatch"}
_root = {"dir": None}


def install():
    from maestro.codegen import build_steps
    from maestro.codegen.staging import game_dir
    from maestro.codegen.pyexec import runner

    saved = (build_steps._apply, runner.subprocess, runner.SAFE_IMPORTS, runner.BANNED_CALLS)
    original_apply = build_steps._apply

    def apply(tools, cursor, tc, run_dir):
        _root["dir"] = str(game_dir(run_dir).resolve())
        return original_apply(tools, cursor, tc, run_dir)

    def popen(args, **kwargs):
        args = ["realchild" if a == "maestro.codegen.pyexec.child" else a for a in args]
        kwargs["env"] = dict(kwargs["env"], PYEXEC_ROOT=_root["dir"])
        return subprocess.Popen(args, **kwargs)

    build_steps._apply = apply
    runner.subprocess = types.SimpleNamespace(Popen=popen, PIPE=subprocess.PIPE,
                                              TimeoutExpired=subprocess.TimeoutExpired)
    runner.SAFE_IMPORTS = runner.SAFE_IMPORTS | FILE_MODULES
    runner.BANNED_CALLS = runner.BANNED_CALLS - {"open"}
    return saved


def restore(saved) -> None:
    from maestro.codegen import build_steps
    from maestro.codegen.pyexec import runner
    build_steps._apply, runner.subprocess, runner.SAFE_IMPORTS, runner.BANNED_CALLS = saved
