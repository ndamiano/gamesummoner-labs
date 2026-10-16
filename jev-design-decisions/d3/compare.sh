#!/usr/bin/env bash
# Frame, mechanics and look and sound on a Decision 3.0 model for the three overnight asks, into runs-<model>/<game>/.
set -u
M=$1
cd "$(dirname "$0")/.."
PY=~/Documents/decision-model-test/.venv/bin/python
/var/lib/models/d3/venv/bin/python d3/shim.py /var/lib/models/d3/$M 8121 > d3/shim-$M.log 2>&1 &
SHIM=$!
until curl -sf http://127.0.0.1:8121/ > /dev/null; do sleep 1; done
export DECIDE_URL=http://127.0.0.1:8121
declare -A ASK=(
  [cat]="a game where you play as a cat trying to catch mice"
  [salvage]="A top-down space salvage game where you tow wrecks back to a station and the wrecks' parts upgrade your ship."
  [fridge]="A game where you are a fridge that has just gained sentience, and you're trying to escape a house."
)
for g in cat salvage fridge; do
  mkdir -p runs-$M/$g
  s=$(date +%s.%N)
  $PY d3/run.py frame.py runs-$M/$g "${ASK[$g]}" > runs-$M/$g/frame.log 2>&1
  $PY d3/run.py flat.py runs-$M/$g > runs-$M/$g/flat.log 2>&1
  $PY d3/run.py look_sound.py runs-$M/$g > runs-$M/$g/look_sound.log 2>&1
  echo "$g $(echo "$(date +%s.%N)-$s" | bc) s" | tee -a runs-$M/timing.txt
done
kill $SHIM
