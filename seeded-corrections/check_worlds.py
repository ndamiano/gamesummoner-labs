import os
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path

from lib import paths
paths.bootstrap()
import positions

work = Path(tempfile.mkdtemp(dir=paths.OUTPUT / "branch-work", prefix="seeded-check-"))
run = paths.RUNS / "8fc1191a0c54"

world = positions.post_compaction(run, "414e264d4630", 0, work / "stubbed-build1")
print(f"stubbed replay of build 1: {world.setup_seconds:.0f}s, {len(world.messages)} messages")

snap = work / "snapshot"
snap.mkdir()
subprocess.run(f"git --git-dir={run / 'game.git'} archive 0937a2a | tar -x -C {snap}",
               shell=True, check=True)
diff = subprocess.run(["diff", "-rq", str(snap), str(world.dir / "game")],
                      capture_output=True, text=True).stdout
print("diff vs built snapshot 0937a2a:", diff.strip() or "identical")

fix = positions.fix_start(run, "414e264d4630", work / "fixstart")
print(f"fix start setup: {fix.setup_seconds:.1f}s, request: {fix.messages[0]['content'][:160]!r}")
print("workdir", work)
