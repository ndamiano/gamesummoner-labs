"""The prod gates on a finished stage chain, as prod runs them after a build: the error gate, then
the play gate, each free to start fix builds. The game is copied into a new run without
stage.json, so the gates and any fix build take the stock path.

    venv/bin/python labs/section-budget/gates.py <final stage run>
"""

import json
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path[:0] = [str(LAB.parents[1] / "src"), str(LAB)]

import branch
import stage
from db import games
from maestro.codegen import build_chain, build_state


def main(source: str) -> None:
    head = subprocess.run(["git", f"--git-dir={stage.RUNS / source / 'game.git'}", "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    n = json.loads((stage.RUNS / source / "stage.json").read_text())["n"]
    rid = branch.branch(source, head, n)
    (stage.RUNS / rid / "stage.json").unlink()
    print(f"gates on {rid} (copy of {source} @ {head[:7]})", flush=True)
    bid = games.create_build(rid, kind="build")
    games.build_started(bid)
    build_state.save(build_state.BuildCursor(build_id=bid, kind="build", started=True,
                                             finished=True, ok=True))
    games.move(rid, "running", "checking")
    build_chain._post_finalize(rid, bid)
    while (games.game(rid) or {}).get("status") == "running":
        time.sleep(30)
    rd = stage.RUNS / rid
    for name in ("error_gate.json", "play_gate.json", "play_report.json"):
        p = rd / name
        print(name, p.read_text()[:1500] if p.exists() else "-", flush=True)
    print("gates done", rid, (games.game(rid) or {}).get("status"), flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
