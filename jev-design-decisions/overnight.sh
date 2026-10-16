#!/usr/bin/env bash
# Overnight: JEV and current-chain designs for three asks, then six builds on the local stack, then the stack down.
set -u
cd "$(dirname "$0")"
P=~/Documents/decision-model-test/.venv/bin/python
R=/home/nick/Documents/ai-agent-test/venv/bin/python
RUNS="cat salvage fridge"
ask() { python3 -c "import json;print(json.load(open('runs/$1/frame_result.json'))['prompt'])"; }
for r in $RUNS; do $P look_sound.py runs/$r > runs/$r/look_sound.log 2>&1; echo "look $r: $?"; done
for r in $RUNS; do [ -s runs/$r/design.md ] || $P write.py runs/$r; echo "write $r: $?"; done
for r in $RUNS; do [ -s runs/$r/prod_design/design.md ] || $P prod_design.py runs/$r > runs/$r/prod_design.log 2>&1; echo "prod $r: $?"; done
curl -s localhost:5001/unload; echo; sleep 10
$R stack.py up || exit 1
( while sleep 60; do $R stack.py ensure; done ) > runs/stack_watch.log 2>&1 &
WATCH=$!
for r in $RUNS; do
  [ -s runs/$r/design.md ] && ./build.sh runs/$r/design.md "$(ask $r)" $r-jev
  [ -s runs/$r/prod_design/design.md ] && ./build.sh runs/$r/prod_design/design.md "$(ask $r)" $r-chain
done
kill $WATCH
$R stack.py down
echo OVERNIGHT DONE
