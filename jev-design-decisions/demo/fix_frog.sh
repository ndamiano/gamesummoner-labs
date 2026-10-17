#!/usr/bin/env bash
set -u
cd "$(dirname "$0")/.."
R=/home/nick/Documents/ai-agent-test/venv/bin/python
$R stack.py up || exit 1
( while sleep 60; do $R stack.py ensure; done ) > runs/demo_stack_watch.log 2>&1 &
WATCH=$!
s=$(date +%s)
./fix.sh 68e135291424 "When I start a level I can't see the frog at all. The screen shows sky, clouds and the tops of some green blocks at the bottom edge, and nothing moves when I press the arrow keys. The frog seems to be below the bottom of the screen, as if the view is stuck at the top of the level and never follows the frog."
echo "FIX frog done in $(( $(date +%s) - s )) s"
kill $WATCH
$R stack.py down
echo FROG FIX DONE
