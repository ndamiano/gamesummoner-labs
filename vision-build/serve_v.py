"""labs/stage-planner/serve.py plus look.py: the control plane with the stage arm, the packed
pre-read, the B5/B7 patches and the builder's pictures installed. Run from the repo root in place
of run.py."""

import os
import runpy
import sys

LAB = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(LAB))
sys.path[:0] = [os.path.join(REPO, "src"), LAB, os.path.join(REPO, "labs", "stage-planner"),
                os.path.join(REPO, "labs", "section-budget")]

import planned
import stage

stage.install()
import look

print("vision-build arm installed: stage arm, packed pre-read, pictures after play()", flush=True)
runpy.run_path(os.path.join(REPO, "run.py"), run_name="__main__")
