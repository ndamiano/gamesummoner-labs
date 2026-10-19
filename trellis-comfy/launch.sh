#!/bin/bash
# ComfyUI 0.34.4 with native TRELLIS.2, capped at 45G host RAM, on port 8288.
SAFE="$(dirname "$(readlink -f "$0")")/../rig-lab/safe"
cd ~/comfy/ComfyUI-0.34
exec "$SAFE" -m 45G \
    ~/comfy/comfy-env-034/bin/python main.py --port 8288 \
    --use-pytorch-cross-attention --disable-dynamic-vram
