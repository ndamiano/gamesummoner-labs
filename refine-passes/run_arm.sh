#!/usr/bin/env bash
# Runs one arm: each stage prompt, then its refine prompt N times, then the build; every pass is a
# fresh coding-agent process on basalt in the arm folder, committed to the labs repo when it ends.
# Usage: ./run_arm.sh <arm> <N>
set -euo pipefail
cd "$(dirname "$0")"
LAB=$PWD
ARM=$1
N=$2
SEED=d0ee945

mkdir -p "$ARM/logs"
[[ -f $ARM/DESIGN.md ]] || git show "$SEED:refine-passes/r0/DESIGN.md" > "$ARM/DESIGN.md"

pass() {
  local name=$1 log
  log="$ARM/logs/$(date +%H%M%S)_$name.log"
  (cd "$ARM" && coding-agent < "$LAB/prompts/$name.txt") > "$log" 2>&1
  git add "$ARM"
  git diff --cached --quiet -- "$ARM" || git commit -q -m "refine-passes $ARM: $name" -- "$ARM"
  echo "$ARM $name $(wc -l < "$ARM/DESIGN.md") lines"
}

refine() { for _ in $(seq 1 "$N"); do pass "$1"; done; }

refine design_refine
pass visuals
refine visuals_refine
pass sound
refine sound_refine
pass build
