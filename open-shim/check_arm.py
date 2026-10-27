import os
import shutil
import sys
import threading
from pathlib import Path

LABS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [LABS, os.path.dirname(os.path.abspath(__file__)), os.path.join(LABS, "seeded-corrections")]
from lib import paths
paths.bootstrap()
from lib.replay import replay
import arm
import positions
from maestro.codegen import build_state, build_steps

arm_world = arm.ARM_RUNS / "arm-check"
plain_world = paths.OUTPUT / "branch-work" / "arm-check-plain"
for d in (arm_world, plain_world):
    shutil.rmtree(d, ignore_errors=True)
w = positions.post_compaction(paths.RUNS / "1629ea1ae380", "9e9209f5d7cc", 47, Path("/var/tmp/open-shim/arm-check-world"))
for d in (arm_world, plain_world):
    shutil.copytree(w.dir, d)
saved = arm.install()
try:
    tools = replay._tools_for(arm_world, w.build, w.source_run)
    h = arm.seed([dict(m) for m in w.messages[:1]], tools, arm_world) + [dict(m) for m in w.messages[1:]]
    print("arm seeded head:", [(m["role"], (m.get("content") or "")[:40].replace("\n", " ")) for m in h[1:6]])
    cursor = build_state.BuildCursor(build_id="b", started=True, turn=w.turn, system=w.system,
                                     history=h, logged=len(h))
    build_steps.compact(arm_world, cursor, 20_000)
    print("pinned after compaction:", sum(arm._is_arm(m) for m in cursor.history[1:6]), "of 5")

    out = {}
    def run(name, d, code):
        tools = replay._tools_for(d, w.build, w.source_run)
        c = build_state.BuildCursor(build_id="t", started=True, history=[])
        for i in range(5):
            build_steps._apply(tools, c, {"id": f"x{i}", "type": "function", "function": {
                "name": "python", "arguments": __import__("json").dumps({"code": code})}}, d)
        out[name] = [m["content"][:70].replace("\n", " ") for m in c.history]
    code = 'import os\nprint(len(open("design/design.md").read()), len(os.listdir(".")))'
    ts = [threading.Thread(target=run, args=("arm", arm_world, code)),
          threading.Thread(target=run, args=("plain", plain_world, code))]
    [t.start() for t in ts]; [t.join() for t in ts]
    for k, v in out.items():
        print(k, "distinct replies:", sorted(set(v)))
finally:
    arm.restore(saved)
for d in (arm_world, plain_world, Path("/var/tmp/open-shim/arm-check-world")):
    shutil.rmtree(d, ignore_errors=True)
