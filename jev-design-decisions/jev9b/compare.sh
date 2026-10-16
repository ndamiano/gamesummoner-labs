#!/usr/bin/env bash
# Frame, mechanics and look and sound on JEV-9B for the three overnight asks, into runs9b/<game>/.
set -u
cd "$(dirname "$0")/.."
PY=~/Documents/decision-model-test/.venv/bin/python
declare -A ASK=(
  [cat]="a game where you play as a cat trying to catch mice"
  [salvage]="A top-down space salvage game where you tow wrecks back to a station and the wrecks' parts upgrade your ship."
  [fridge]="A game where you are a fridge that has just gained sentience, and you're trying to escape a house."
)
for g in cat salvage fridge; do
  mkdir -p runs9b/$g
  s=$(date +%s.%N)
  $PY jev9b/run.py frame.py runs9b/$g "${ASK[$g]}" > runs9b/$g/frame.log 2>&1
  m=$(date +%s.%N)
  $PY jev9b/run.py flat.py runs9b/$g > runs9b/$g/flat.log 2>&1
  l=$(date +%s.%N)
  $PY jev9b/run.py look_sound.py runs9b/$g > runs9b/$g/look_sound.log 2>&1
  e=$(date +%s.%N)
  echo "$g frame $(echo "$m-$s"|bc) mechanics $(echo "$l-$m"|bc) look $(echo "$e-$l"|bc)" | tee -a runs9b/timing.txt
done
