#!/usr/bin/env bash
# Serve the llm queue from DeepSeek V4.1 Flash against the control plane already on :8000, with
# this lab's own ledger. Ctrl-C stops all of it.
set -euo pipefail
LAB=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$LAB/../.." && pwd)
FC=$REPO/labs/frontier-ceiling
IMAGES=${IMAGES_REPO_DIR:-$HOME/Documents/gamesummoner-images}
WORKERS=${WORKER_REPO_DIR:-$HOME/Documents/gamesummoner-workers}
LOGS=${MAESTRO_LOCAL_LOGS:-/tmp/maestro-local}
BUDGET=${BUDGET:-4}
mkdir -p "$LOGS"

alias=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["llm"]["model"])' \
    "$REPO/src/config/settings.json")

pids=()
trap 'kill "${pids[@]}" 2>/dev/null; wait' EXIT INT TERM

"$FC/venv/bin/python" "$FC/openai_engine.py" --alias "$alias" --budget-usd "$BUDGET" \
    --ledger "$LAB/calls.jsonl" --port 8091 >> "$LAB/engine.log" 2>&1 &
pids+=($!)

(cd "$IMAGES" && PYTHONPATH="$IMAGES" exec "$REPO/venv/bin/python" -m local.llm.server \
    --image-id model-owned-audio --engine-url http://127.0.0.1:8091 --port 8701) \
    >> "$LOGS/odd-image.log" 2>&1 &
pids+=($!)

env_file=$(cd "$REPO" && venv/bin/python -c '
import sys; sys.path.insert(0, "scripts")
import local_gpu
print(local_gpu._worker_env("llm"))')
PYTHONPATH="$WORKERS/src" "$REPO/venv/bin/python" -m gamesummoner_worker \
    --env-file "$env_file" --image http://127.0.0.1:8701 >> "$LOGS/odd-worker.log" 2>&1 &
pids+=($!)

echo "deepseek engine :8091, llm image :8701, llm worker up; logs in $LAB/engine.log and $LOGS/odd-*.log"
wait -n
echo "a process exited; stopping the stack"
