#!/bin/bash
# On the box: decode scaling for rebuilt Q4 and IQ3_S, speculation on and off.
cd /opt/dlami/nvme/w
export PATH=/opt/dlami/nvme/w/venv/bin:$PATH
for m in Qwen3.8-FN-UD-Q4_K_XL-bf16key Qwen3.8-FN-GSQ-RCO-IQ3_S; do
  for s in 7 0; do python conc.py model/$m.basalt $s >> conc.out 2>&1; done
done
echo ALLDONE >> conc.out
