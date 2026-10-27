#!/usr/bin/env bash
# One full build of the arm on the production path, from an earlier run's design: a new run with
# the same ask, design.md and request line. The run directory lives on ext4 under
# /var/tmp/open-shim/runs (Landlock cannot list directories on the eCryptfs home), symlinked back
# into the runs folder. The arm is installed here too, because kickoff runs the first step in
# this process. Needs labs/open-shim/serve.py (in place of run.py) and local_gpu auto up.
# Usage: labs/open-shim/fullbuild.sh <source run id> "label"     STEPS=200 default
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; cd "$LAB/../.."; source venv/bin/activate; cd src
RID=$(LAB="$LAB" python3 - "$1" "$2" "${STEPS:-200}" <<'PY'
import json, logging, os, shutil, sys
from pathlib import Path
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.state import RunState
from maestro.codegen import build_chain, design
from maestro.codegen.staging import spec_path
from maestro.codegen.run import create_run, open_ask, set_prompt
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s", stream=sys.stderr)
lab = Path(os.environ["LAB"])
sys.path[:0] = [os.getcwd(), str(lab), str(lab.parent), str(lab.parent / "seeded-corrections")]
import arm
arm.install()
src, label, steps = RunState(sys.argv[1]), sys.argv[2], int(sys.argv[3])
ask = src.read_spec()["ask"]
rid = create_run(store.list_users()[0].id); games.charge_game(rid, 0, MICROS_PER_CREDIT)
run_dir = RunState(rid).run_dir
home = Path("/var/tmp/open-shim/runs") / rid
home.parent.mkdir(parents=True, exist_ok=True)
shutil.move(str(run_dir), str(home))
os.symlink(home, run_dir)
open_ask(rid, ask)
shutil.copy2(spec_path(src.run_dir), spec_path(RunState(rid).run_dir))
set_prompt(rid, design._request(ask))
build_chain.kickoff(rid, kind="build", max_steps=steps)
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
