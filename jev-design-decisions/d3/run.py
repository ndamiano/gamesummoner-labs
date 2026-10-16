"""Run a lab decision script (frame.py, flat.py, look_sound.py) against the decide endpoint at DECIDE_URL."""
import os
import runpy
import sys

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
sys.path.insert(0, "/home/nick/Documents/ai-agent-test/labs/jev-design-decisions")
import ask

ask.DECIDE = os.environ["DECIDE_URL"]
ask.chat = lambda *a, **k: None
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
