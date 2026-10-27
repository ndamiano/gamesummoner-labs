#!/usr/bin/env bash
# After queue.sh: the penguin ask again (its first design fell back to the bare ask when the decide
# model would not start), its chain, then the same design built the stock way, one conversation on
# the prod build path with its gates, as the control for sp-penguin. If decide fails again, the
# decide container is started by hand once so its own error is on disk.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE/../.."
OUT=/var/tmp/stage-planner
while pgrep -fx "bash labs/stage-planner/queue.sh" >/dev/null; do sleep 30; done
echo "[$(date -Is)] queue.sh done"

ASK="A game about a penguin climbing a pyramid"
(cd src && ../venv/bin/python -m maestro.codegen.run --new "$ASK") > $OUT/penguin-design2.log 2>&1
PENGUIN=$(sed -n 's/^run: \([0-9a-f]*\).*/\1/p' $OUT/penguin-design2.log | head -1)
echo "[$(date -Is)] penguin design: run $PENGUIN, $(grep '^design:' $OUT/penguin-design2.log)"
if grep -q "the ask is the prompt" $OUT/penguin-design2.log; then
  curl -s localhost:5001/unload >/dev/null; sleep 20
  timeout 600 docker run --rm --name decide-debug --gpus all --ipc host \
    -v /var/lib/models:/var/lib/models:ro \
    vllm/vllm-openai@sha256:befccf0e7e4089aa23926bb6f887a85c0d46c2a99e6de5c5ffdf5cb7957c5b34 \
    --model /var/lib/models/llm/Qwen3.8-27B-NVFP4 --tokenizer /var/lib/models/jev/JEV-27B-VL \
    --served-model-name jev-base --enable-lora --max-lora-rank 32 \
    --lora-modules jev-decision=/var/lib/models/jev/JEV-27B-VL/adapter_vllm \
    --logprobs-mode processed_logprobs --max-logprobs 32 --max-model-len 32768 --max-num-seqs 8 \
    --gpu-memory-utilization 0.90 --enforce-eager --limit-mm-per-prompt '{"image":0,"video":0}' \
    --load-format runai_streamer > $OUT/decide-debug.log 2>&1
  echo "[$(date -Is)] DECIDE BROKEN, debug run ended: $(tail -3 $OUT/decide-debug.log | tr '\n' ' ')"
  exit 1
fi

venv/bin/python labs/stage-planner/chain.py "$PENGUIN" sp-penguin > $OUT/sp-penguin.log 2>&1
echo "[$(date -Is)] sp-penguin done: $(grep -E '^chain done|^gates done' $OUT/sp-penguin.log | tr '\n' ' ')"

(cd src && ../venv/bin/python -m maestro.codegen.run --build "$PENGUIN") > $OUT/penguin-control.log 2>&1
echo "[$(date -Is)] control build ended: $(grep -E 'succeeded|failed' $OUT/penguin-control.log | tail -1)"
until [ "$(cd src && ../venv/bin/python -c "from db import games; print(games.game('$PENGUIN')['status'])" 2>/dev/null)" != "running" ]; do sleep 30; done
echo "[$(date -Is)] control gates done: $(cd src && ../venv/bin/python -c "from db import games; g=games.game('$PENGUIN'); print(g['status'], g['stage'])")"
