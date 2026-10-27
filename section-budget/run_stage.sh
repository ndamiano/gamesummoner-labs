#!/usr/bin/env bash
# One stage of a stage chain (arm B by default, arm A with "stages": "stages_a" in STAGE_OPTS). Stage 1 is a new run with the source run's ask and design, its run directory
# on ext4 under /var/tmp/section-budget/runs (Landlock cannot list directories on the eCryptfs
# home), symlinked back into the runs folder. A later stage is a build on that run's files with
# the next stage's request. Needs labs/section-budget/serve.py (in place of run.py) and local_gpu
# auto up.
# Usage: labs/section-budget/run_stage.sh <source run id> "label"     (stage 1)
#        labs/section-budget/run_stage.sh <stage run id> next         (the next stage)
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; cd "$LAB/../.."; source venv/bin/activate; cd src
RID=$(LAB="$LAB" python3 - "$1" "$2" <<'PY'
import json, logging, os, shutil, sys
from pathlib import Path
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.state import RunState
from maestro.codegen import build_chain
from maestro.codegen.staging import spec_path
from maestro.codegen.run import create_run, open_ask, set_prompt
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s", stream=sys.stderr)
sys.path[:0] = [os.getcwd(), os.environ["LAB"]]
import stage
stage.install()
if sys.argv[2] == "next":
    rid = sys.argv[1]
    home = stage.RUNS / rid
    info = json.loads((home / "stage.json").read_text())
    info["n"] += 1
    (home / "stage.json").write_text(json.dumps(info))
    budget = info.get("budget", stage.BUDGET)
    set_prompt(rid, stage.request(RunState(rid).read_spec()["ask"], info["n"], budget, info.get("stages", "stages")))
    build_chain.kickoff(rid, kind="build", max_steps=budget,
                    designed=games.game(rid)["stage"] == "designing")
    print(rid)
    sys.exit(0)
src = RunState(sys.argv[1])
ask = src.read_spec()["ask"]
rid = create_run(store.list_users()[0].id); games.charge_game(rid, 0, MICROS_PER_CREDIT)
run_dir = RunState(rid).run_dir
home = stage.RUNS / rid
home.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(run_dir), str(home))
os.symlink(home, run_dir)
open_ask(rid, ask)
shutil.copy2(spec_path(src.run_dir), spec_path(RunState(rid).run_dir))
opts = json.loads(os.environ.get("STAGE_OPTS") or "{}")
(home / "stage.json").write_text(json.dumps({"n": 1, "budget": stage.BUDGET, "source": sys.argv[1], **opts}))
budget = opts.get("budget", stage.BUDGET)
set_prompt(rid, stage.request(ask, 1, budget, opts.get("stages", "stages")))
build_chain.kickoff(rid, kind="build", max_steps=budget,
                    designed=games.game(rid)["stage"] == "designing")
print(rid)
PY
)
echo "run: $RID $2 (from $1)"
python3 - "$RID" <<'PY'
import sys, logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")
from maestro.codegen.run import _await_build
r = _await_build(sys.argv[1])
print("result:", r.ok, r.steps, f"{r.elapsed:.0f}s", r.summary, flush=True)
PY
