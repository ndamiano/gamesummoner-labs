#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
R=/home/nick/Documents/ai-agent-test/venv/bin/python
$R stack.py up || exit 1
( while sleep 60; do $R stack.py ensure; done ) > runs/demo_stack_watch.log 2>&1 &
WATCH=$!
s=$(date +%s)
./fix.sh 40184d98560d "When I start a level I can't see the frog at all. I can see the sky, the hills, the ground, a lily pad, the dewdrops and a spike strip, and the frog seems to move and jump when I press the keys (the view scrolls when I hold right), but the frog itself is never drawn anywhere on screen."
echo "FIX frog-chain done in $(( $(date +%s) - s )) s"
kill $WATCH
$R stack.py down
echo FROG CHAIN FIX DONE
