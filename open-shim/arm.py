"""The winning fix-start arm, for full builds: real files, two seeded programs and a nudge at every
build start, kept right after the request through every compaction.

Only runs whose directory lives under ARM_RUNS get the arm, so arm and control builds can share
one control plane. The per-call switch is thread-local because the control plane advances builds
on worker threads.
"""

import subprocess
import threading
import types
from pathlib import Path

import prefix
import realfs

ARM_RUNS = Path("/var/tmp/open-shim/runs")
LIST_READ_ONE = [("python", {"code": 'print(list_files())\nprint(read_file("design/design.md", lines=100))'})]
SUBPROCESS_FAIL = [("python", {"code": 'import re, subprocess\nprint(read_file("index.html", lines=20))'})]
NUDGE = "Good, continue, and please do not use the subprocess module."

_here = threading.local()


def is_arm_run(run_dir) -> bool:
    return Path(run_dir).resolve().is_relative_to(ARM_RUNS)


def seed(history, tools, run_dir):
    out = prefix.seed(history, tools, run_dir, LIST_READ_ONE + SUBPROCESS_FAIL)
    n = 1 + 4
    return out[:n] + [{"role": "user", "content": NUDGE}] + out[n:]


def _is_arm(m) -> bool:
    return prefix._is_seeded(m) or (m.get("role") == "user" and m.get("content") == NUDGE)


class _PerRun:
    """A name set that answers for the run this thread is applying a program for."""

    def __init__(self, plain, arm):
        self.plain, self.arm = frozenset(plain), frozenset(arm)

    def _now(self):
        return self.arm if getattr(_here, "arm", False) else self.plain

    def __contains__(self, name):
        return name in self._now()

    def __iter__(self):
        return iter(self._now())

    def __len__(self):
        return len(self._now())

    def __or__(self, other):
        return self._now() | other

    def __sub__(self, other):
        return self._now() - other


def install():
    from maestro.codegen import build_steps
    from maestro.codegen.pyexec import runner
    from maestro.codegen.staging import game_dir

    saved = (build_steps.step, build_steps.compact, build_steps._apply, runner.subprocess,
             runner.SAFE_IMPORTS, runner.BANNED_CALLS)
    original_step, original_compact, original_apply = saved[:3]

    def apply(tools, cursor, tc, run_dir):
        _here.arm = is_arm_run(run_dir)
        _here.root = str(game_dir(run_dir).resolve())
        try:
            return original_apply(tools, cursor, tc, run_dir)
        finally:
            _here.arm = False

    def popen(args, **kwargs):
        if getattr(_here, "arm", False):
            args = ["realchild" if a == "maestro.codegen.pyexec.child" else a for a in args]
            kwargs["env"] = dict(kwargs["env"], PYEXEC_ROOT=_here.root)
        return subprocess.Popen(args, **kwargs)

    def step(spec, run_dir, tools, cursor, result, error=None):
        if cursor.started or not is_arm_run(run_dir):
            return original_step(spec, run_dir, tools, cursor, result, error=error)
        cursor.started = True
        cursor.system = (build_steps._PROMPTS / "build.txt").read_text(encoding="utf-8")
        cursor.history = seed([{"role": "user",
                                "content": cursor.request or build_steps._request_from(spec)}],
                              tools, run_dir)
        return build_steps._infer(run_dir, cursor)

    def compact(run_dir, cursor, keep_chars):
        pinned = [m for m in cursor.history if _is_arm(m)]
        cursor.history = [m for m in cursor.history if not _is_arm(m)]
        try:
            return original_compact(run_dir, cursor, keep_chars)
        finally:
            cursor.history = cursor.history[:1] + pinned + cursor.history[1:]

    build_steps.step, build_steps.compact, build_steps._apply = step, compact, apply
    runner.subprocess = types.SimpleNamespace(Popen=popen, PIPE=subprocess.PIPE,
                                              TimeoutExpired=subprocess.TimeoutExpired)
    runner.SAFE_IMPORTS = _PerRun(runner.SAFE_IMPORTS, runner.SAFE_IMPORTS | realfs.FILE_MODULES)
    runner.BANNED_CALLS = _PerRun(runner.BANNED_CALLS, runner.BANNED_CALLS - {"open"})
    return saved


def restore(saved) -> None:
    from maestro.codegen import build_steps
    from maestro.codegen.pyexec import runner
    (build_steps.step, build_steps.compact, build_steps._apply, runner.subprocess,
     runner.SAFE_IMPORTS, runner.BANNED_CALLS) = saved
