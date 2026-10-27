#!/usr/bin/env bash
# After the stage-planner bets (queue7): playtest-refine single runs on the staged penguin and the
# staged wizard cat.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/playtest-refine; mkdir -p $OUT
while pgrep -fx "bash labs/stage-planner/queue7.sh" >/dev/null || pgrep -fx "bash labs/stage-planner/queue6.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] bets done"
for pair in "eedc7205ebd3 pr-penguin" "32fa91f2477a pr-cat"; do
  set -- $pair
  venv/bin/python labs/playtest-refine/refine.py "$1" "$2" < /dev/null > $OUT/$2.log 2>&1
  echo "[$(date -Is)] $2: $(grep -E '^before:|^after:|^refine done|^change build' $OUT/$2.log | tr '\n' ' ')"
done
echo "[$(date -Is)] playtest-refine queue done"
