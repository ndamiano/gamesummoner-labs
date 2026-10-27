#!/usr/bin/env bash
# After playtest-refine's queue2: the B6 battery. Each staged baseline's own plan again (copied to
# plans/b6-<x>), with only the turn budget changed to 20,20,20,25,25,30,30,35,35.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/playtest-refine/queue2.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] playtest-refine queue2 done"
for pair in "5870978265fe b6-hira" "33a565da9ca8 b6-frog" "9c4ac408da27 b6-bugs" "d188fbe6b5c2 b6-cat" "f254f7d986a9 b6-penguin" "815570b85c6d b6-gta6"; do
  set -- $pair
  venv/bin/python labs/stage-planner/chain.py "$1" "$2" --budgets 20,20,20,25,25,30,30,35,35 < /dev/null > $OUT/$2.log 2>&1
  echo "[$(date -Is)] $2: $(grep -E '^chain done|^gates done' $OUT/$2.log | tr '\n' ' ')"
done
echo "[$(date -Is)] queue8 done"
