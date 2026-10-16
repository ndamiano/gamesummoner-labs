#!/bin/bash
# Boot chain on this box: pull the rebuilt Q4 pack from S3 to local NVMe, then Basalt to ready.
cd /opt/dlami/nvme/w
t0=$(date +%s.%N)
aws configure set default.s3.max_concurrent_requests 64
aws s3 cp s3://gamesummoner-models-385588571625/basalt-test/packs/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt /opt/dlami/nvme/w/boot.basalt --quiet
t1=$(date +%s.%N)
echo "s3 pull $(echo "$t1-$t0" | bc) s, $(du -h boot.basalt | cut -f1)"
venv/bin/python -c "
import sys; sys.path.insert(0, '.')
from common import *
p = start(config(W + '/boot.basalt'), 'boot'); stop(p)"
echo "total $(echo "$(date +%s.%N)-$t0" | bc) s"
rm -f boot.basalt
