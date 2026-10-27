"""labs/vision-build/serve_v.py with the build prompt read from this lab's prompts/ (build.txt plus
the three laws). Run from the repo root in place of serve_v.py."""

import os
import runpy
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
sys.path[:0] = [str(REPO / "src"), str(REPO / "labs" / "vision-build"), str(REPO / "labs" / "stage-planner"),
                str(REPO / "labs" / "section-budget")]

import planned
import stage

stage.install()
import look
from maestro.codegen import build_steps

build_steps._PROMPTS = LAB / "prompts"
print(f"build-prompt-laws arm installed: build prompt from {build_steps._PROMPTS}", flush=True)
runpy.run_path(os.path.join(REPO, "run.py"), run_name="__main__")
