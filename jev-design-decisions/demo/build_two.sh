#!/usr/bin/env bash
# Build the two demo designs on the local stack, keeping the stack alive between checks, then bring it down.
set -u
cd "$(dirname "$0")/.."
R=/home/nick/Documents/ai-agent-test/venv/bin/python
ask() { python3 -c "import json;print(json.load(open('runs/$1/frame_result.json'))['prompt'])"; }
$R stack.py up || exit 1
( while sleep 60; do $R stack.py ensure; done ) > runs/demo_stack_watch.log 2>&1 &
WATCH=$!
for r in frog shooter; do
  s=$(date +%s); ./build.sh runs/$r/design.md "$(ask $r)" $r-demo; echo "BUILD $r done in $(( $(date +%s) - s )) s"
done
kill $WATCH
$R stack.py down
echo DEMO BUILDS DONE
