#!/usr/bin/env bash
# After queue2.sh: fresh asks, each a prod design, its staged chain, then the same design built the
# stock way (one conversation, prod build path, gates) as its control.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/stage-planner/queue2.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue2.sh done"

status() { (cd src && ../venv/bin/python -c "from db import games; g=games.game('$1'); print(g['status'], g['stage'])" 2>/dev/null); }

while IFS='|' read -r label ask; do
  (cd src && ../venv/bin/python -m maestro.codegen.run --new "$ask") < /dev/null > $OUT/$label-design.log 2>&1
  rid=$(sed -n 's/^run: \([0-9a-f]*\).*/\1/p' $OUT/$label-design.log | head -1)
  echo "[$(date -Is)] $label design: run $rid, $(grep '^design:' $OUT/$label-design.log)"
  if [ -z "$rid" ] || grep -q "the ask is the prompt" $OUT/$label-design.log; then continue; fi
  venv/bin/python labs/stage-planner/chain.py "$rid" "$label" < /dev/null > $OUT/$label.log 2>&1
  echo "[$(date -Is)] $label staged: $(grep -E '^chain done|^gates done' $OUT/$label.log | tr '\n' ' ')"
  (cd src && ../venv/bin/python -m maestro.codegen.run --build "$rid") < /dev/null > $OUT/$label-control.log 2>&1
  until [ "$(status $rid | cut -d' ' -f1)" != "running" ]; do sleep 30; done
  echo "[$(date -Is)] $label control: $(grep -E '^result|succeeded|failed' $OUT/$label-control.log | tail -1) | $(status $rid)"
done <<'ASKS'
sp-carts|shopping cart racing through a grocery store
sp-gears|a puzzle game about rotating gears to power a lighthouse
sp-blorp|blorp the zingle 3000
ASKS
echo "[$(date -Is)] queue3 done"
