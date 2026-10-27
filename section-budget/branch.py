"""A new stage run that starts where another stage run's snapshot left the game, so one stage can
be run again under a different arm. The new run's stage.json names the snapshot's stage; run
`run_stage.sh <new run> next` to run the stage after it.

    python3 branch.py <stage run id> <snapshot ref> <stage the snapshot ended>
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path[:0] = [str(LAB.parents[1] / "src"), str(LAB)]

import stage
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.codegen import snapshots
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState


def branch(source: str, ref: str, n: int, opts=None) -> str:
    src = RunState(source)
    rid = create_run(store.list_users()[0].id)
    games.charge_game(rid, 0, MICROS_PER_CREDIT)
    run_dir = RunState(rid).run_dir
    home = stage.RUNS / rid
    shutil.move(str(run_dir), str(home))
    os.symlink(home, run_dir)
    ask = src.read_spec()["ask"]
    open_ask(rid, ask)
    shutil.copy2(spec_path(src.run_dir), spec_path(run_dir))
    game = game_dir(run_dir)
    game.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", f"--git-dir={src.run_dir / 'game.git'}", "archive", ref],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(game)], input=archive, check=True)
    snapshots.take(run_dir, "branched")
    info = json.loads((src.run_dir / "stage.json").read_text())
    set_prompt(rid, stage.request(ask, n, arm={**info, **(opts or {})}.get("stages", "stages")))
    (home / "stage.json").write_text(json.dumps({**info, **(opts or {}), "n": n,
                                                 "branched_from": [source, ref]}))
    return rid


if __name__ == "__main__":
    print(branch(sys.argv[1], sys.argv[2], int(sys.argv[3])))
