#!/usr/bin/env bash
# One Quality build on the mainline staged chain from an earlier run's design and stage plan: a new
# run with the same ask, design.md and stages.json, so only the builder differs from the source.
# Needs the control plane (venv/bin/python run.py) with seats naming the builder first.
# Usage: ./staged.sh <source run id> "label"
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; cd "$LAB/../.."; source venv/bin/activate; cd src
RID=$(python3 - "$1" <<'PY'
import json, logging, os, shutil, sys
sys.path.insert(0, os.getcwd())
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.state import RunState
from maestro.codegen import build_chain, design, stages
from maestro.codegen.staging import spec_path
from maestro.codegen.run import create_run, open_ask, set_prompt
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s", stream=sys.stderr)
src = RunState(sys.argv[1])
ask = src.read_spec()["ask"]
rid = create_run(store.list_users()[0].id, private=False)
games.charge_game(rid, 0, MICROS_PER_CREDIT)
open_ask(rid, ask)
run_dir = RunState(rid).run_dir
shutil.copy2(spec_path(src.run_dir), spec_path(run_dir))
plan = json.loads((src.run_dir / "design" / "stages.json").read_text(encoding="utf-8"))
plan.update(attempts={}, before={})
(run_dir / "design").mkdir(exist_ok=True)
stages._save(run_dir, plan)
set_prompt(rid, design._request(ask))
build_chain.kickoff(rid, kind="build", designed=True)
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
