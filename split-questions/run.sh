#!/usr/bin/env bash
# Runs one arm: R rounds of two fresh-context askers (need, better) then one answerer that
# updates DESIGN.md; every pass is a fresh coding-agent process on basalt in the arm folder,
# committed to the labs repo when it ends.
# Usage: ./run.sh <arm> [rounds, default 1] [first pass to run, skipping those before it]
set -euo pipefail
cd "$(dirname "$0")"
LAB=$PWD
ARM=$1
ROUNDS=${2:-1}
FROM=${3:-}
SEED=d0ee945

mkdir -p "$ARM/logs"
[[ -f $ARM/DESIGN.md ]] || git show "$SEED:refine-passes/r0/DESIGN.md" > "$ARM/DESIGN.md"
[[ -f $ARM/ASK.md ]] || cp prompts/design.txt "$ARM/ASK.md"
git add "$ARM"
git diff --cached --quiet -- "$ARM" || git commit -q -m "split-questions $ARM: seed" -- "$ARM"

pass() {
  local name=$1 round=$2 log
  [[ -n $FROM && $name != "$FROM" ]] && return
  FROM=
  log="$ARM/logs/$(date +%H%M%S)_r${round}_$name.log"
  (cd "$ARM" && python3 "$LAB/drive.py" "$LAB/prompts/$name.txt") > "$log" 2>&1
  if [[ $name == ask_* ]] && ! git diff --quiet -- "$ARM/DESIGN.md"; then
    echo "$ARM round $round $name edited DESIGN.md; stopping, see $log"
    exit 1
  fi
  git add "$ARM"
  if git diff --cached --quiet -- "$ARM"; then
    echo "$ARM round $round $name left $ARM unchanged; stopping, see $log"
    exit 1
  fi
  git commit -q -m "split-questions $ARM: round $round $name" -- "$ARM"
  echo "$ARM round $round $name: DESIGN.md $(wc -l < "$ARM/DESIGN.md") lines"
}

for r in $(seq 1 "$ROUNDS"); do
  pass ask_need "$r"
  pass ask_better "$r"
  pass answer "$r"
done
