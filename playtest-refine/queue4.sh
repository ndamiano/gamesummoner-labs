#!/usr/bin/env bash
# After queue3.sh: two director-v3 rounds on loop-penguin's last build (2c272a1e92fe), where v2
# stalled because the design names the climb key but never shows it on screen.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/playtest-refine
while pgrep -fx "bash labs/playtest-refine/queue3.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue3 done"
venv/bin/python labs/playtest-refine/loop.py 2c272a1e92fe loop3-penguin 2 director_v3.txt < /dev/null > $OUT/loop3-penguin.log 2>&1
echo "[$(date -Is)] loop3-penguin: $(grep -E '^round|^loop done' $OUT/loop3-penguin.log | tr '\n' ' ')"
