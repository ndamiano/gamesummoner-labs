import dataclasses
import json
import os
import shutil
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import paths
paths.bootstrap()
from lib.replay import direct
import positions
import prefix

FIX_STARTS = [
    ("1629ea1ae380", "8a22202c1e36"),
    ("632bb49dbb5b", "74264d3cf4bb"),
    ("8fc1191a0c54", "414e264d4630"),
    ("d0dc7c41c2d0", "c23286be4361"),
]
ARMS = {"ctrl": None, "seeded": prefix.seed, "read": prefix.seed_read, "list": prefix.seed_list,
        "listread": prefix.seed_list_read}

per_arm = int(sys.argv[1])
arms = sys.argv[2].split(",") if len(sys.argv) > 2 else ["ctrl", "seeded"]
start = int(sys.argv[3]) if len(sys.argv) > 3 else 0
direct.install("http://127.0.0.1:5001")

work = paths.OUTPUT / "branch-work" / f"seeded-battery-{int(time.time())}"
worlds = {run: positions.fix_start(paths.RUNS / run, build, work / f"world-{run}")
          for run, build in FIX_STARTS}
results = work / "results.jsonl"
print(f"work {work}", flush=True)

n = 0
for i in range(start, per_arm):
    run = FIX_STARTS[i % len(FIX_STARTS)][0]
    for arm in arms:
        n += 1
        target = work / f"{arm}-{run}-{i:03d}"
        out = positions.step(worlds[run], target, 5, arm, prefix=ARMS[arm])
        row = {"arm": arm, "run": run, "i": i, "direct_calls": out.direct_calls, "refused": out.refused,
               "stopped": out.stopped, "turns": [dataclasses.asdict(t) for t in out.turns]}
        with results.open("a") as f:
            f.write(json.dumps(row) + "\n")
        shutil.rmtree(target / "game", ignore_errors=True)
        print(f"== {n} {arm} {run} #{i}: direct {out.direct_calls}, refused {out.refused}, "
              f"{sum(t.seconds for t in out.turns):.0f}s", flush=True)
print("battery done", flush=True)
