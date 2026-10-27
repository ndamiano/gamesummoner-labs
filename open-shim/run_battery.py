import dataclasses
import json
import os
import shutil
import sys
import time
from pathlib import Path

LABS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, LABS)
sys.path.insert(0, os.path.join(LABS, "seeded-corrections"))
from lib import paths
paths.bootstrap()
from lib.replay import direct
import openshim
import realfs
import positions
import prefix

FIX_STARTS = [
    ("1629ea1ae380", "8a22202c1e36"),
    ("632bb49dbb5b", "74264d3cf4bb"),
    ("8fc1191a0c54", "414e264d4630"),
    ("d0dc7c41c2d0", "c23286be4361"),
]
LIST_READ_ONE = [("python", {"code": 'print(list_files())\nprint(read_file("design/design.md", lines=100))'})]


def seed_list_read_one(history, tools, run_dir):
    return prefix.seed(history, tools, run_dir, LIST_READ_ONE)


NUDGE = "Good, continue, and please do not use the subprocess module."


def seed_list_read_one_nudge(history, tools, run_dir):
    out = seed_list_read_one(history, tools, run_dir)
    n = 1 + 2
    return out[:n] + [{"role": "user", "content": NUDGE}] + out[n:]


SUBPROCESS_FAIL = [("python", {"code": 'import re, subprocess\nprint(read_file("index.html", lines=20))'})]


def seed_list_read_subfail_nudge(history, tools, run_dir):
    was = realfs.install()
    try:
        out = prefix.seed(history, tools, run_dir, LIST_READ_ONE + SUBPROCESS_FAIL)
    finally:
        realfs.restore(was)
    n = 1 + 4
    return out[:n] + [{"role": "user", "content": NUDGE}] + out[n:]


ARMS = {"shim": (None, openshim.install, openshim.restore),
        "shim+read": (prefix.seed_read, openshim.install, openshim.restore),
        "real": (None, realfs.install, realfs.restore),
        "real+listread1": (seed_list_read_one, realfs.install, realfs.restore),
        "real+listread1+nudge": (seed_list_read_one_nudge, realfs.install, realfs.restore),
        "real+listread1+subfail+nudge": (seed_list_read_subfail_nudge, realfs.install,
                                         realfs.restore)}
ECRYPTFS_SAFE = Path("/var/tmp/open-shim")

per_arm = int(sys.argv[1])
arms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["shim", "shim+read"]
direct.install("http://127.0.0.1:5001")

base = ECRYPTFS_SAFE if any(a.startswith("real") for a in arms) else paths.OUTPUT / "branch-work"
work = base / f"open-shim-{int(time.time())}"
worlds = {run: positions.fix_start(paths.RUNS / run, build, work / f"world-{run}")
          for run, build in FIX_STARTS}
results = work / "results.jsonl"
print(f"work {work}", flush=True)

n = 0
for i in range(per_arm):
    run = FIX_STARTS[i % len(FIX_STARTS)][0]
    for arm in arms:
        n += 1
        target = work / f"{arm}-{run}-{i:03d}"
        seed, install, restore = ARMS[arm]
        out = positions.step(worlds[run], target, 5, arm, prefix=seed, install=install,
                             restore=restore)
        row = {"arm": arm, "run": run, "i": i, "direct_calls": out.direct_calls, "refused": out.refused,
               "stopped": out.stopped, "turns": [dataclasses.asdict(t) for t in out.turns]}
        with results.open("a") as f:
            f.write(json.dumps(row) + "\n")
        shutil.rmtree(target / "game", ignore_errors=True)
        print(f"== {n} {arm} {run} #{i}: direct {out.direct_calls}, refused {out.refused}, "
              f"{sum(t.seconds for t in out.turns):.0f}s", flush=True)
print("battery done", flush=True)
