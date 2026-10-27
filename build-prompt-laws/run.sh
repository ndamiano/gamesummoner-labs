#!/usr/bin/env bash
# One run of the laws arm on an existing design: the staged chain exactly as pipeline-v2's run_ask.sh
# runs it, then three refine rounds on the gated copy (no UX rounds). The control plane is swapped
# to serve_laws.py for the run and back to serve_v.py after, each swap only with no game building.
# Usage: labs/build-prompt-laws/run.sh <label> <design run id> [HH:MM to start at]
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
LABEL=$1; DESIGN=$2; AT=${3:-}
OUT=/var/tmp/build-prompt-laws/$LABEL; mkdir -p $OUT
ROW=$HERE/results.jsonl
CP_LOG=/tmp/maestro-local/sp-serve.log
stamp() { echo "[$(date -Is)] $LABEL: $*"; }

if [ -n "$AT" ]; then
  target=$(date -d "$AT" +%s); [ $target -le $(date +%s) ] && target=$(date -d "tomorrow $AT" +%s)
  stamp "waiting for $AT"; sleep $(( target - $(date +%s) ))
fi

idle() {
  until [ "$(sqlite3 data/platform.db "select count(*) from games where status='running'")" = 0 ] \
     && [ "$(sqlite3 data/platform.db "select count(*) from jobs where status in ('pending','claimed')")" = 0 ]; do
    sleep 30
  done
}

swap() {
  local from=$1 to=$2
  idle
  pkill -fx "venv/bin/python $from"
  while pgrep -fx "venv/bin/python $from" >/dev/null; do sleep 1; done
  local n=$(wc -l < $CP_LOG)
  setsid nohup venv/bin/python $to >> $CP_LOG 2>&1 < /dev/null &
  until tail -n +$((n + 1)) $CP_LOG | grep -q 'startup complete\|startup failed'; do sleep 1; done
  if ! tail -n +$((n + 1)) $CP_LOG | grep -q 'startup complete'; then
    stamp "control plane $to failed to start, back to $from"
    setsid nohup venv/bin/python $from >> $CP_LOG 2>&1 < /dev/null &
    exit 1
  fi
  stamp "control plane now $to"
}

GPU="venv/bin/python scripts/local_gpu.py auto --ready-timeout 600"
( while sleep 60; do
    pgrep -fx "$GPU" >/dev/null || { stamp "local_gpu gone, restarting"; setsid nohup $GPU >> /tmp/maestro-local/sp-auto.log 2>&1 < /dev/null & }
  done ) &
KEEPER=$!
trap 'kill $KEEPER 2>/dev/null' EXIT

swap labs/vision-build/serve_v.py labs/build-prompt-laws/serve_laws.py

venv/bin/python labs/stage-planner/chain.py $DESIGN bpl-$LABEL --budgets 20,20,20,25,25,30,30,35,35 \
  --opts '{"repair_first": true, "look": true, "vision_check": true, "relook": true}' > $OUT/staged.log 2>&1
STAGED=$(sed -n 's/^chain done bpl-[^ ]* \([0-9a-f]*\)$/\1/p' $OUT/staged.log | tail -1)
GATED=$(sed -n 's/^gates done \([0-9a-f]*\) .*/\1/p' $OUT/staged.log | tail -1)
stamp "staged $STAGED gated copy $GATED"

REFINE_LOOK=auto venv/bin/python labs/playtest-refine/loop.py ${GATED:-$STAGED} bpl-$LABEL 3 director_v3.txt > $OUT/refine.log 2>&1
REFINED=$(sed -n 's/^loop done [^ ]* \([0-9a-f]*\)$/\1/p' $OUT/refine.log | tail -1)
stamp "refined $REFINED"

swap labs/build-prompt-laws/serve_laws.py labs/vision-build/serve_v.py

python3 - "$ROW" "$LABEL" "$DESIGN" "$STAGED" "$GATED" "$REFINED" <<'PY'
import json, sys, time
path, label, design, staged, gated, refined = sys.argv[1:]
with open(path, "a") as f:
    f.write(json.dumps({"label": label, "design": design, "staged": staged, "staged_gated": gated,
                        "refined": refined, "finished": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
PY
stamp "done"
