#!/bin/bash
# On the box: once the IQ3_S pack is down, bench it at 4 concurrent with speculation on (patched Basalt).
cd /opt/dlami/nvme/w
until grep -q "iq3s download exit" rebuild.out; do sleep 5; done
export PATH=/opt/dlami/nvme/w/venv/bin:$PATH
MODEL=/opt/dlami/nvme/w/model/Qwen3.8-FN-GSQ-RCO-IQ3_S.basalt BASALT=/opt/dlami/nvme/w/basalt-patch python bench.py 4 7 > iq3s-47.out 2>&1
echo ALLDONE >> iq3s-47.out
