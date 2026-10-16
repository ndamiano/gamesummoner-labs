#!/usr/bin/env bash
# sglang on JEV-9B (bf16) at :8110 plus decide.py at :8111.
set -e
JEV=/var/lib/models/jev/JEV-9B
export SGLANG_CACHE_DIR=/var/lib/models/cache/sglang
export MAX_JOBS=4
export PYTHONPATH="$(cd "$(dirname "$0")" && pwd)/patch"
cd "$(dirname "$0")"
/opt/venvs/sglang-env/bin/python -m sglang.launch_server \
  --model-path "$JEV" --served-model-name jev-9b \
  --enable-lora --max-lora-rank 32 --lora-paths jev-decision="$JEV/adapter_sglang" --lora-strict-loading --max-loras-per-batch 2 \
  --enable-return-hidden-states \
  --context-length 32768 --mem-fraction-static 0.8 --chunked-prefill-size 2048 \
  --host 127.0.0.1 --port 8110 > /tmp/claude-1000/-home-nick-Documents-ai-agent-test/8cf2e2cd-5cc8-44b9-bc4b-b906fbf9ec38/scratchpad/jev9b_sglang.log 2>&1 &
JEV_DIR="$JEV" exec /opt/venvs/sglang-env/bin/python decide.py --port 8111 --sglang http://127.0.0.1:8110
