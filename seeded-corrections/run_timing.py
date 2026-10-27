import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import paths
paths.bootstrap()
from lib.replay import direct
import positions

direct.install("http://127.0.0.1:5001")

work = paths.OUTPUT / "branch-work" / f"seeded-timing-{int(time.time())}"
worlds = [
    ("fixstart", positions.fix_start(paths.RUNS / "8fc1191a0c54", "414e264d4630",
                                     work / "world-fixstart")),
    ("postcompact", positions.post_compaction(paths.RUNS / "524b1c3efa1c", "d46684c82196", 23,
                                              work / "world-postcompact")),
]
for name, world in worlds:
    print(f"== {name}: setup {world.setup_seconds:.1f}s, {len(world.messages)} messages", flush=True)
    t0 = time.time()
    out = positions.step(world, work / f"ctrl-{name}", 5, f"ctrl-{name}")
    infer = sum(t.seconds for t in out.turns)
    print(f"== {name}: 5 turns {infer:.0f}s ({infer / max(1, len(out.turns)):.0f}s/turn), "
          f"wall {time.time() - t0:.0f}s, direct calls {out.direct_calls}"
          + (f", stopped: {out.stopped}" if out.stopped else ""), flush=True)
