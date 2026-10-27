#!/usr/bin/env bash
# After the combined stage-planner run: playtest-refine v2 (goal + what was seen + how to reproduce,
# no guessed cause) on the staged penguin, where v1's guessed fix missed the camera occlusion.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/playtest-refine
while pgrep -fx 'venv/bin/python labs/stage-planner/chain\.py a81bbbcec618 b467-combined-carts .*' >/dev/null; do sleep 30; done
echo "[$(date -Is)] combined chain done"
venv/bin/python labs/playtest-refine/refine.py eedc7205ebd3 pr-penguin-v2 v2 < /dev/null > $OUT/pr-penguin-v2.log 2>&1
echo "[$(date -Is)] pr-penguin-v2: $(grep -E '^before:|^after:|^refine done|^change build' $OUT/pr-penguin-v2.log | tr '\n' ' ')"
