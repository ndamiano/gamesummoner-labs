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

POST_COMPACTION = [
    ("1629ea1ae380", "9e9209f5d7cc", 47),
    ("22263c0d3c8b", "762550a01f00", 26),
    ("3170a8a2b4c3", "0717586acd2e", 45),
    ("524b1c3efa1c", "d46684c82196", 23),
    ("632bb49dbb5b", "c42a7d4341cd", 41),
    ("8fc1191a0c54", "d5cf4d9b2d89", 33),
    ("d0dc7c41c2d0", "dcf73de496dd", 40),
]
ARMS = {"ctrl": (None, None, None), "seeded": (prefix.seed, prefix.pin, prefix.unpin),
        "read": (prefix.seed_read, prefix.pin, prefix.unpin),
        "list": (prefix.seed_list, prefix.pin, prefix.unpin),
        "listread": (prefix.seed_list_read, prefix.pin, prefix.unpin)}

per_arm = int(sys.argv[1])
check_only = len(sys.argv) > 2 and sys.argv[2] == "check"
arms = sys.argv[2].split(",") if len(sys.argv) > 2 and not check_only else ["ctrl", "seeded"]
work = paths.OUTPUT / "branch-work" / f"seeded-pc-{int(time.time())}"
print(f"work {work}", flush=True)

worlds = {}
for run, build, position in POST_COMPACTION:
    try:
        w = positions.post_compaction(paths.RUNS / run, build, position, work / f"world-{run}")
    except Exception as e:
        print(f"skip {run}@{position}: {type(e).__name__}: {e}", flush=True)
        continue
    worlds[run] = w
    print(f"world {run}@{position}: {w.setup_seconds:.1f}s, {len(w.messages)} messages", flush=True)

if check_only:
    from lib.replay import replay
    from maestro.codegen import build_state, build_steps
    for run, w in worlds.items():
        t = work / f"pincheck-{run}"
        shutil.copytree(w.dir, t)
        tools = replay._tools_for(t, w.build, w.source_run)
        h = prefix.seed([dict(m) for m in w.messages], tools, t)
        cursor = build_state.BuildCursor(build_id="b", started=True, turn=w.turn,
                                         system=w.system, history=h, logged=len(h))
        was = prefix.pin()
        try:
            n = build_steps.compact(t, cursor, 20_000)
        finally:
            prefix.unpin(was)
        kept = [m for m in cursor.history[1:7] if prefix._is_seeded(m)]
        print(f"pin {run}: compact returned {n}, {len(cursor.history)} msgs after, "
              f"seeded at [1:7]: {len(kept)}/6, note at 7: {build_steps.is_note(cursor.history[7])}",
              flush=True)
    sys.exit(0)

direct.install("http://127.0.0.1:5001")
results = work / "results.jsonl"
runs = list(worlds)
n = 0
for i in range(per_arm):
    run = runs[i % len(runs)]
    for arm in arms:
        seed, install, restore = ARMS[arm]
        n += 1
        target = work / f"{arm}-{run}-{i:03d}"
        out = positions.step(worlds[run], target, 5, arm, prefix=seed, install=install,
                             restore=restore)
        row = {"arm": arm, "run": run, "i": i, "direct_calls": out.direct_calls,
               "refused": out.refused, "stopped": out.stopped,
               "turns": [dataclasses.asdict(t) for t in out.turns]}
        with results.open("a") as f:
            f.write(json.dumps(row) + "\n")
        shutil.rmtree(target / "game", ignore_errors=True)
        print(f"== {n} {arm} {run} #{i}: direct {out.direct_calls}, refused {out.refused}, "
              f"{sum(t.seconds for t in out.turns):.0f}s", flush=True)
print("battery done", flush=True)
