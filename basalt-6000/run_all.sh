#!/bin/bash
# On the box, after the rebuilds: every test in order, one Basalt at a time.
cd /opt/dlami/nvme/w
until grep -q BOOT_DONE /var/log/basalt-boot.log; do sleep 10; done
export PATH=/opt/dlami/nvme/w/venv/bin:$PATH
python compat.py > t-compat.out 2>&1
python longturn.py q4 > t-long.out 2>&1
python longturn.py q4mtp >> t-long.out 2>&1
python interleave.py > t-interleave.out 2>&1
./boottime.sh > t-boot.out 2>&1
echo ALLDONE > t-done.out
