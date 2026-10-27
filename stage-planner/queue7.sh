#!/usr/bin/env bash
# After queue6.sh: B7, repair first. B1's 12-stage carts plan again, and a stage that starts from a
# game that does not load is told the page errors and to make it load before building.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/stage-planner/queue6.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue6.sh done"
venv/bin/python labs/stage-planner/chain.py a81bbbcec618 b7-repair-carts --opts '{"repair_first": true}' < /dev/null > $OUT/b7-repair-carts.log 2>&1
echo "[$(date -Is)] b7-repair-carts: $(grep -E '^plan has|^chain done|^gates done' $OUT/b7-repair-carts.log | tr '\n' ' ')"
echo "[$(date -Is)] queue7 done"
