#!/bin/bash
# On the box: after the Q4 rebuild, bench the rebuilt Q4 and rerun IQ3_S, both 4 concurrent with speculation on.
cd /opt/dlami/nvme/w
until grep -q REBUILD_DONE rebuild.out; do sleep 5; done
export PATH=/opt/dlami/nvme/w/venv/bin:$PATH
export BASALT=/opt/dlami/nvme/w/basalt-patch
MODEL=/opt/dlami/nvme/w/model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt python bench.py 4 7 > q4b-47.out 2>&1
MODEL=/opt/dlami/nvme/w/model/Qwen3.8-FN-GSQ-RCO-IQ3_S.basalt python bench.py 4 7 > iq3s-47b.out 2>&1
echo ALLDONE >> iq3s-47b.out
