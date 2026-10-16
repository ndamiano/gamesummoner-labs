#!/usr/bin/env bash
# One build on the production path from a design file: a new run with the ask, the design as its
# spec and the real request line, then the real build chain at its default step cap. The arms differ
# only in the design they hand over. Needs the control plane and the llm worker up.
# Usage: ./build.sh <design.md> "<ask>" <label>
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; DESIGN="$(realpath "$1")"; cd "$LAB/../.."; source venv/bin/activate; cd src
RID=$(python3 - "$DESIGN" "$2" <<'PY'
import logging, sys
from pathlib import Path
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.state import RunState
from maestro.codegen import build_chain, design
from maestro.codegen.staging import spec_path
from maestro.codegen.run import create_run, open_ask, set_prompt
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
spec, ask = Path(sys.argv[1]).read_text(), sys.argv[2]
rid = create_run(store.list_users()[0].id); games.charge_game(rid, 0, MICROS_PER_CREDIT)
open_ask(rid, ask)
spec_path(RunState(rid).run_dir).write_text(spec)
set_prompt(rid, design._request(ask))
build_chain.kickoff(rid, kind="build")
print(rid)
PY
)
echo "run: $RID $3 ($1)"
echo -e "$RID\t$3\t$1\t$(date -Iseconds)" >> "$LAB/builds.tsv"
python3 - "$RID" <<'PY'
import sys
from maestro.codegen.run import _await_build
r = _await_build(sys.argv[1])
print("result:", r.ok, r.steps, f"{r.elapsed:.0f}s", r.summary, flush=True)
PY
