#!/usr/bin/env bash
# After the B6 battery (stage-planner queue8): three playtest-refine v2 rounds each on the staged
# penguin and the staged wizard cat.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/playtest-refine
while pgrep -fx "bash labs/stage-planner/queue8.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] B6 battery done"
for pair in "eedc7205ebd3 loop-penguin" "32fa91f2477a loop-cat"; do
  set -- $pair
  venv/bin/python labs/playtest-refine/loop.py "$1" "$2" 3 < /dev/null > $OUT/$2.log 2>&1
  echo "[$(date -Is)] $2: $(grep -E '^round|^loop done' $OUT/$2.log | tr '\n' ' ')"
done
echo "[$(date -Is)] queue3 done"
