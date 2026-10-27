#!/usr/bin/env bash
# One ask through the candidate pipeline (base games for the vision swings; no control, per Nick):
#   1. prod design (local Flash-Next)
#   2. staged chain: planner, budgets 20,20,20,25,25,30,30,35,35, repair first, the builder sees its
#      page after each play() and a vision look checks each stage, with a second, longer look on
#      unclear (labs/vision-build); prod gates
#      on a copy
#   3. playtest-refine on the gated copy: three director-v3 rounds with the keep-best progress judge, change builds
#      seeing their page too
#   4. vision-ux: two paired rounds (fixed tour replayed, before/after judge) on the refined game.
#   Needs labs/vision-build/serve_v.py as the control plane.
# Usage: labs/pipeline-v2/run_ask.sh <label> "<ask>"
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
LABEL=$1; ASK=$2
OUT=/var/tmp/pipeline-v2/$LABEL; mkdir -p $OUT
ROW=$HERE/results.jsonl
stamp() { echo "[$(date -Is)] $LABEL: $*"; }
status() { (cd src && ../venv/bin/python -c "from db import games; g=games.game('$1'); print(g['status'], g['stage'])" 2>/dev/null); }

(cd src && ../venv/bin/python -m maestro.codegen.run --new "$ASK") > $OUT/design.log 2>&1
DESIGN=$(sed -n 's/^run: \([0-9a-f]*\).*/\1/p' $OUT/design.log | head -1)
stamp "design $DESIGN $(grep '^design:' $OUT/design.log)"
if [ -z "$DESIGN" ] || grep -q "the ask is the prompt" $OUT/design.log; then stamp "no design, stopping"; exit 1; fi

venv/bin/python labs/stage-planner/chain.py $DESIGN pv2-$LABEL --budgets 20,20,20,25,25,30,30,35,35 \
  --opts '{"repair_first": true, "look": true, "vision_check": true, "relook": true}' > $OUT/staged.log 2>&1
STAGED=$(sed -n 's/^chain done pv2-[^ ]* \([0-9a-f]*\)$/\1/p' $OUT/staged.log | tail -1)
GATED=$(sed -n 's/^gates done \([0-9a-f]*\) .*/\1/p' $OUT/staged.log | tail -1)
stamp "staged $STAGED gated copy $GATED"

REFINE_LOOK=auto venv/bin/python labs/playtest-refine/loop.py ${GATED:-$STAGED} pv2-$LABEL 3 director_v3.txt > $OUT/refine.log 2>&1
REFINED=$(sed -n 's/^loop done [^ ]* \([0-9a-f]*\)$/\1/p' $OUT/refine.log | tail -1)
stamp "refined $REFINED"

UX_LOOK=auto UX_PAIRED=1 venv/bin/python labs/vision-ux/ux.py ${REFINED:-${GATED:-$STAGED}} pv2-$LABEL-ux 2 > $OUT/ux.log 2>&1
POLISHED=$(sed -n 's/^ux done [^ ]* \([0-9a-f]*\)$/\1/p' $OUT/ux.log | tail -1)
stamp "polished $POLISHED"

python3 - "$ROW" "$LABEL" "$ASK" "$DESIGN" "$STAGED" "$GATED" "$REFINED" "$POLISHED" <<'PY'
import json, sys, time
path, label, ask, design, staged, gated, refined, polished = sys.argv[1:]
with open(path, "a") as f:
    f.write(json.dumps({"label": label, "ask": ask, "design": design, "staged": staged,
                        "staged_gated": gated, "refined": refined, "polished": polished,
                        "finished": time.strftime("%Y-%m-%dT%H:%M:%S")}) + "\n")
PY
stamp "done"
