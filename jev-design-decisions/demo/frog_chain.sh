#!/usr/bin/env bash
# Frog on the current design chain (prod_design.py), then the same build path as the JEV arm.
set -u
cd "$(dirname "$0")/.."
R=/home/nick/Documents/ai-agent-test/venv/bin/python
D=/home/nick/Documents/decision-model-test/.venv/bin/python
s=$(date +%s); $D prod_design.py runs/frog || exit 1; echo "DESIGN chain done in $(( $(date +%s) - s )) s"
curl -s 127.0.0.1:5001/unload; echo
$R stack.py up || exit 1
( while sleep 60; do $R stack.py ensure; done ) > runs/demo_stack_watch.log 2>&1 &
WATCH=$!
ask=$(python3 -c "import json;print(json.load(open('runs/frog/frame_result.json'))['prompt'])")
s=$(date +%s); ./build.sh runs/frog/prod_design/design.md "$ask" frog-chain; echo "BUILD frog-chain done in $(( $(date +%s) - s )) s"
kill $WATCH
$R stack.py down
echo FROG CHAIN DONE
