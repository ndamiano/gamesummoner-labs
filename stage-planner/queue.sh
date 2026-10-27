#!/usr/bin/env bash
# The rest of the night after sp-opus: a fresh prod design of a new ask, its chain, then the battery.
# Waits for the sp-opus chain to exit first. Needs serve.py and local_gpu auto up.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "venv/bin/python labs/stage-planner/chain.py d086d499669b sp-opus" >/dev/null; do sleep 30; done
echo "[$(date -Is)] sp-opus chain exited"

ASK="A game about a penguin climbing a pyramid"
(cd src && ../venv/bin/python -m maestro.codegen.run --new "$ASK") > $OUT/penguin-design.log 2>&1
PENGUIN=$(sed -n 's/^run: \([0-9a-f]*\).*/\1/p' $OUT/penguin-design.log | head -1)
echo "[$(date -Is)] penguin design: run $PENGUIN, $(grep '^design:' $OUT/penguin-design.log)"
[ -n "$PENGUIN" ] && venv/bin/python labs/stage-planner/chain.py "$PENGUIN" sp-penguin > $OUT/sp-penguin.log 2>&1
echo "[$(date -Is)] sp-penguin done: $(grep -E '^chain done|^gates done' $OUT/sp-penguin.log | tr '\n' ' ')"

for pair in "5870978265fe sp-hira" "33a565da9ca8 sp-frog" "9c4ac408da27 sp-bugs" "d188fbe6b5c2 sp-cat"; do
  set -- $pair
  venv/bin/python labs/stage-planner/chain.py "$1" "$2" > $OUT/$2.log 2>&1
  echo "[$(date -Is)] $2 done: $(grep -E '^chain done|^gates done' $OUT/$2.log | tr '\n' ' ')"
done
echo "[$(date -Is)] queue done"
