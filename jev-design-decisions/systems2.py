"""Ask JEV yes/no for each level-2 part of the level-1 systems it kept, with frame and kept systems as state."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

RUN = Path(sys.argv[1])

QUESTION = "Does this game's {system} include {part}?"


def parts():
    rows = re.findall(r"^\| ([^|]+?) \| ([^|]+) \|$", open("systems.md").read(), re.M)
    return {s: [p.strip() for p in ps.split(",")] for s, ps in rows if s not in ("System", "---")}


def main():
    level1 = json.load(open(RUN / "systems_result.json"))
    state = level1["state"] + "\nsystems: " + ", ".join(level1["kept"]).lower()
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    table, out = parts(), {}
    for system in level1["kept"]:
        probs = {}
        for part in table[system]:
            r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state,
                                                      "question": QUESTION.format(system=system.lower(), part=part)})
            probs[part] = round(r["probabilities"][1], 3)
        out[system] = probs
        print(f"== {system} ({level1['probabilities'][system]:.2f})")
        for p, v in sorted(probs.items(), key=lambda x: -x[1]):
            print(f"  {v:.3f}  {'KEEP' if v > 0.6 else '    '}  {p}")
    json.dump({"state": state, "question": QUESTION, "probabilities": out,
               "kept": {s: [p for p, v in ps.items() if v > 0.6] for s, ps in out.items()}},
              open(RUN / "systems2_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
