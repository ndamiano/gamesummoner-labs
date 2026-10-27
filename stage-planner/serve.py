"""The control plane with section-budget's stage arm and this lab's packed pre-read installed. Run
from the repo root in place of run.py."""

import os
import runpy
import sys

LAB = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(LAB))
sys.path[:0] = [os.path.join(REPO, "src"), LAB, os.path.join(REPO, "labs", "section-budget")]

import planned
import stage

stage.install()
print("stage-planner arm installed: planned stages, packed pre-read, turns left", flush=True)
runpy.run_path(os.path.join(REPO, "run.py"), run_name="__main__")
