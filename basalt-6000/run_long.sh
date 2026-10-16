#!/bin/bash
# On the box: ~100K-context single-request decode for the rebuilt Q4 and IQ3_S.
cd /opt/dlami/nvme/w
export PATH=/opt/dlami/nvme/w/venv/bin:$PATH
for m in Qwen3.8-FN-UD-Q4_K_XL-bf16key Qwen3.8-FN-GSQ-RCO-IQ3_S; do python longctx.py model/$m.basalt >> long.out 2>&1; done
echo ALLDONE >> long.out
