"""The control plane with arm.py installed. Run from the repo root in place of run.py."""

import os
import runpy
import sys

LAB = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(LAB)
REPO = os.path.dirname(LABS)
sys.path[:0] = [os.path.join(REPO, "src"), LAB, LABS, os.path.join(LABS, "seeded-corrections")]

import arm

arm.install()
print("open-shim arm installed: real files, seeded rounds, nudge, compaction pin", flush=True)
runpy.run_path(os.path.join(REPO, "run.py"), run_name="__main__")
