#!/usr/bin/env bash
# One build on the production path from a design an earlier run's design chain produced: a new run
# with the same ask, the same design.md and the same request line, so the only difference from the
# source run is build.txt: this lab's prompts/ copy drops the lib/audio.js rule (patched in at kickoff).
# Needs the control plane (venv/bin/python run.py) and serve.sh up.
# Usage: ./build.sh <source run id> "label"     STEPS=200 default
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; cd "$LAB/../.."; source venv/bin/activate; cd src
RID=$(LAB="$LAB" python3 - "$1" "$2" "${STEPS:-200}" <<'PY'
import json, logging, os, shutil, sys
sys.path.insert(0, os.getcwd())
from pathlib import Path
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.state import RunState
from maestro.codegen import build_chain, build_steps, design
build_steps._PROMPTS = Path(os.environ["LAB"]) / "prompts"
from maestro.codegen.staging import spec_path
from maestro.codegen.run import create_run, open_ask, set_prompt
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s", stream=sys.stderr)
src, label, steps = RunState(sys.argv[1]), sys.argv[2], int(sys.argv[3])
ask = src.read_spec()["ask"]
rid = create_run(store.list_users()[0].id); games.charge_game(rid, 0, MICROS_PER_CREDIT)
open_ask(rid, ask)
shutil.copy2(spec_path(src.run_dir), spec_path(RunState(rid).run_dir))
set_prompt(rid, design._request(ask))
build_chain.kickoff(rid, kind="build", max_steps=steps, designed=True)
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
