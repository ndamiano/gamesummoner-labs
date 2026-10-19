#!/usr/bin/env bash
# Serve the llm queue from several hosted models at once: Claude on :8092, DeepSeek on :8093, Gemini on :8094, the
# router on :8091 picking per ask (routes.json), and WORKERS workers so games build in parallel.
set -euo pipefail
LAB=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$LAB/../.." && pwd)
IMAGES=${IMAGES_REPO_DIR:-$HOME/Documents/gamesummoner-images}
WORKERS_REPO=${WORKER_REPO_DIR:-$HOME/Documents/gamesummoner-workers}
LOGS=${MAESTRO_LOCAL_LOGS:-/tmp/maestro-local}
CLAUDE_MODEL=${CLAUDE_MODEL:-claude-sonnet-5-5}
CLAUDE_BUDGET=${CLAUDE_BUDGET:-25}
DEEPSEEK_BUDGET=${DEEPSEEK_BUDGET:-6}
WORKERS=${WORKERS:-6}
mkdir -p "$LOGS"

alias=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["llm"]["model"])' \
    "$REPO/src/config/settings.json")

pids=()
trap 'kill "${pids[@]}" 2>/dev/null; wait' EXIT INT TERM

"$LAB/venv/bin/python" "$LAB/anthropic_engine.py" --model "$CLAUDE_MODEL" --alias "$alias" \
    --budget-usd "$CLAUDE_BUDGET" --port 8092 --ledger "${CLAUDE_MODEL}_calls.jsonl" \
    --thinking-store "${CLAUDE_MODEL}_thinking.json" \
    --agentic-write "$LAB/write_agentic.txt" --write-budget 60000 ${TURN_BUDGET:+--turn-budget "$TURN_BUDGET"} >> "$LAB/${CLAUDE_MODEL}_engine.log" 2>&1 &
pids+=($!)

"$LAB/venv/bin/python" "$LAB/openai_engine.py" --alias "$alias" --budget-usd "$DEEPSEEK_BUDGET" \
    --port 8093 >> "$LAB/deepseek_engine.log" 2>&1 &
pids+=($!)

"$LAB/venv/bin/python" "$LAB/openai_engine.py" --alias "$alias" --budget-usd "${GEMINI_BUDGET:-15}" \
    --base-url https://generativelanguage.googleapis.com/v1beta/openai --model gemini-4-argon \
    --key-file ~/api_keys/gemini-api.key --ledger gemini_calls.jsonl \
    --port 8094 >> "$LAB/gemini_engine.log" 2>&1 &
pids+=($!)

"$LAB/venv/bin/python" "$LAB/router_engine.py" --routes "$LAB/routes.json" --alias "$alias" \
    --port 8091 >> "$LAB/router.log" 2>&1 &
pids+=($!)

(cd "$IMAGES" && PYTHONPATH="$IMAGES" exec "$REPO/venv/bin/python" -m local.llm.server \
    --image-id frontier-ceiling-multi --engine-url http://127.0.0.1:8091 --port 8701) \
    >> "$LOGS/frontier-image.log" 2>&1 &
pids+=($!)

for i in $(seq 1 "$WORKERS"); do
    env_file=$(cd "$REPO" && MAESTRO_LOCAL_LOGS="$LOGS/multi-$i" venv/bin/python -c '
import sys; sys.path.insert(0, "scripts")
import local_gpu
print(local_gpu._worker_env("llm"))')
    PYTHONPATH="$WORKERS_REPO/src" "$REPO/venv/bin/python" -m gamesummoner_worker \
        --env-file "$env_file" --image http://127.0.0.1:8701 >> "$LOGS/frontier-worker-$i.log" 2>&1 &
    pids+=($!)
done

echo "claude ($CLAUDE_MODEL) :8092, deepseek :8093, router :8091, image :8701, $WORKERS workers up"
wait -n
echo "a process exited; stopping the stack"
