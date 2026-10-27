"""The control plane with stage.py installed. Run from the repo root in place of run.py."""

import os
import runpy
import sys

LAB = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(LAB))
sys.path[:0] = [os.path.join(REPO, "src"), LAB]

import stage

stage.install()
print("section-budget stage arm installed: turns left, no gates between stages", flush=True)
runpy.run_path(os.path.join(REPO, "run.py"), run_name="__main__")
