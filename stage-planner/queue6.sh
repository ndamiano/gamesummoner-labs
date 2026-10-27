#!/usr/bin/env bash
# After queue5.sh: restart the lab control plane so planned.py's B5 patch is loaded where the turns
# run (nothing is building then), and run B3 and B5 once each on the carts design with sp-carts' plan.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/stage-planner/queue5.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue5.sh done"

pid=$(pgrep -fx "venv/bin/python labs/stage-planner/serve.py")
[ -n "$pid" ] && kill -TERM $pid
timeout 60 bash -c 'while pgrep -fx "venv/bin/python labs/stage-planner/serve.py" >/dev/null; do sleep 1; done'
setsid nohup venv/bin/python labs/stage-planner/serve.py > /tmp/maestro-local/sp-serve.log 2>&1 < /dev/null &
timeout 120 bash -c 'until curl -sf -o /dev/null http://localhost:8000/docs; do sleep 2; done' \
  && echo "[$(date -Is)] serve.py restarted" || { echo "[$(date -Is)] SERVE RESTART FAILED"; exit 1; }

CARTS=a81bbbcec618
run() { label=$1; shift
  venv/bin/python labs/stage-planner/chain.py $CARTS "$label" "$@" < /dev/null > $OUT/$label.log 2>&1
  echo "[$(date -Is)] $label: $(grep -E '^plan has|^chain done|^gates done' $OUT/$label.log | tr '\n' ' ')"
}
run b3-carry-carts --opts '{"carry": true}'
run b5-play-done-carts --opts '{"play_before_done": true}'
echo "[$(date -Is)] queue6 done"
