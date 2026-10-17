#!/usr/bin/env bash
# One fix pass on a built run, the way a player reports a problem: ./fix.sh <run id> "<what the player saw>"
set -u
LAB="$(cd "$(dirname "$0")" && pwd)"; cd "$LAB/../.."; source venv/bin/activate; cd src
python3 - "$1" "$2" <<'PY'
import logging, sys
from maestro.codegen import build_chain
from maestro.codegen.run import _await_build
logging.basicConfig(level=logging.WARNING, stream=sys.stderr)
build_chain.kickoff(sys.argv[1], kind="fix", note=sys.argv[2])
r = _await_build(sys.argv[1])
print("fix result:", r.ok, r.steps, f"{r.elapsed:.0f}s", r.summary, flush=True)
PY
