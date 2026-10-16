"""Remove the style JEV picked for one prompt, offer "something else" in its place, and see where the probability goes."""
import json
import sys

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from style import STYLES, decide

PROMPT_START, REMOVED = sys.argv[1], sys.argv[2]
row = next(r for r in json.load(open("style_results.json")) if r["prompt"].startswith(PROMPT_START))
q = f"Given a {row['dim']} game with the prompt '{row['prompt']}', what art style would you choose?"
ask.chat(ask.JEV, "hi", 1, think=False)
ask.wait_decide()
styles = {k: v for k, v in STYLES.items() if k != REMOVED}
styles["something else"] = "a style not listed above"
for name, opts in (("all nine", STYLES), (f"without {REMOVED}, plus something else", styles)):
    r = decide(q, opts)
    print(f"\n{name}:")
    for k, p in sorted(r["p"].items(), key=lambda x: -x[1]):
        print(f"  {p:6.1%}  {k}")
