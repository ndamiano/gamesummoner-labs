#!/usr/bin/env bash
# Serve the llm queue from a hosted API (Anthropic, or DeepSeek with ENGINE=deepseek) and every other queue from the 5090, against the
# control plane already on :8000. Ctrl-C stops all of it.
set -euo pipefail
LAB=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$LAB/../.." && pwd)
IMAGES=${IMAGES_REPO_DIR:-$HOME/Documents/gamesummoner-images}
WORKERS=${WORKER_REPO_DIR:-$HOME/Documents/gamesummoner-workers}
LOGS=${MAESTRO_LOCAL_LOGS:-/tmp/maestro-local}
MODEL=${MODEL:-claude-opus-5-5}
BUDGET=${BUDGET:-40}
mkdir -p "$LOGS"

ENTRY=${ENTRY:-qwen-flash-next}
alias=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["llm"][sys.argv[2]]["model"])' \
    "$REPO/src/config/settings.json" "$ENTRY")

pids=()
trap 'kill "${pids[@]}" 2>/dev/null; wait' EXIT INT TERM

if [ "${ENGINE:-anthropic}" = deepseek ]; then
    "$LAB/venv/bin/python" "$LAB/openai_engine.py" --alias "$alias" --budget-usd "$BUDGET" \
        --port 8091 ${LEDGER:+--ledger "$LEDGER"} >> "$LAB/deepseek_engine.log" 2>&1 &
else
    "$LAB/venv/bin/python" "$LAB/anthropic_engine.py" --model "$MODEL" --alias "$alias" \
        --budget-usd "$BUDGET" --port 8091 ${LEDGER:+--ledger "$LEDGER"} ${TOOLLESS_EFFORT:+--toolless-effort "$TOOLLESS_EFFORT"} ${TOOLLESS_NOTE:+--toolless-note "$TOOLLESS_NOTE"} ${AGENTIC_WRITE:+--agentic-write "$AGENTIC_WRITE"} ${WRITE_BUDGET:+--write-budget "$WRITE_BUDGET"} >> "$LAB/engine.log" 2>&1 &
fi
pids+=($!)

(cd "$IMAGES" && PYTHONPATH="$IMAGES" exec "$REPO/venv/bin/python" -m local.llm.server \
    --image-id frontier-ceiling --engine-url http://127.0.0.1:8091 --port 8701) \
    >> "$LOGS/frontier-image.log" 2>&1 &
pids+=($!)

env_file=$(cd "$REPO" && venv/bin/python -c '
import sys; sys.path.insert(0, "scripts")
import local_gpu
print(local_gpu._worker_env(("llm", "'"$ENTRY"'")))')
PYTHONPATH="$WORKERS/src" "$REPO/venv/bin/python" -m gamesummoner_worker \
    --env-file "$env_file" --image http://127.0.0.1:8701 >> "$LOGS/frontier-worker.log" 2>&1 &
pids+=($!)

if [ "${AUTO:-1}" != 0 ]; then
    "$LAB/auto.sh" &
    pids+=($!)
fi

echo "engine, llm image :8701, llm worker up (auto: ${AUTO:-1}); logs in $LAB/engine.log and $LOGS/frontier-*.log"
wait -n
echo "a process exited; stopping the stack"
