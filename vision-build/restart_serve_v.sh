#!/usr/bin/env bash
# Restart labs/vision-build/serve_v.py so edits to look.py load. Run between jobs, when nothing builds.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
pid=$(pgrep -fx "venv/bin/python labs/vision-build/serve_v.py")
[ -n "$pid" ] && kill -TERM $pid
timeout 60 bash -c 'while pgrep -fx "venv/bin/python labs/vision-build/serve_v.py" >/dev/null; do sleep 1; done'
setsid nohup venv/bin/python labs/vision-build/serve_v.py > /tmp/maestro-local/sp-serve.log 2>&1 < /dev/null &
timeout 120 bash -c 'until curl -sf -o /dev/null http://localhost:8000/docs; do sleep 2; done' \
  && echo "[$(date -Is)] serve_v.py restarted" || { echo "[$(date -Is)] SERVE_V RESTART FAILED"; exit 1; }
