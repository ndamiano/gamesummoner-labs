#!/usr/bin/env bash
# After queue4.sh: one run of each cheap bet on the carts design (a81bbbcec618), whose staged chain
# was the roughest of the night (sp-carts) and whose one-conversation control gated clean.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/stage-planner/queue4.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue4.sh done"
CARTS=a81bbbcec618
run() { label=$1; shift
  venv/bin/python labs/stage-planner/chain.py $CARTS "$label" "$@" < /dev/null > $OUT/$label.log 2>&1
  echo "[$(date -Is)] $label: $(grep -E '^plan has|^chain done|^gates done' $OUT/$label.log | tr '\n' ' ')"
}
run b1-adaptive-carts --prompt plan_adaptive.txt
run b4-split-end-carts --prompt plan_split_end.txt
run b6-backload-carts --budgets 20,20,20,25,25,30,30,35,35
echo "[$(date -Is)] queue5 done"
