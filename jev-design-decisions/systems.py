"""Ask JEV yes/no for each level-1 system in systems.md, with the frame decisions as state."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from frame import state_of

RUN = Path(sys.argv[1])

QUESTION = "Does this game contain {system}?"


def level1():
    rows = re.findall(r"^\| ([^|]+?) \| [^|]+ \|$", open("systems.md").read(), re.M)
    return [r for r in rows if r not in ("System", "---")]


def main():
    frame = json.load(open(RUN / "frame_result.json"))
    state = state_of(frame["prompt"], frame["decided"])
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    probs = {}
    for s in level1():
        r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state,
                                                  "question": QUESTION.format(system=s.lower())})
        probs[s] = round(r["probabilities"][1], 3)
    for s, p in sorted(probs.items(), key=lambda x: -x[1]):
        print(f"{p:.3f}  {'KEEP' if p > 0.6 else '    '}  {s}")
    json.dump({"state": state, "question": QUESTION, "probabilities": probs,
               "kept": [s for s, p in probs.items() if p > 0.6]}, open(RUN / "systems_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
