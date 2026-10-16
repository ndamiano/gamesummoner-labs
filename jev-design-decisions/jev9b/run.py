"""Run a lab decision script (frame.py, flat.py, look_sound.py) against JEV-9B on :8111 instead of the 27B."""
import runpy
import sys

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
sys.path.insert(0, "/home/nick/Documents/ai-agent-test/labs/jev-design-decisions")
import ask

ask.DECIDE = "http://127.0.0.1:8111"
ask.chat = lambda *a, **k: None
script = sys.argv[1]
sys.argv = sys.argv[1:]
runpy.run_path(script, run_name="__main__")
