"""Band the kept mechanics by JEV's "first playable" probability and write the tiered state the write step reads."""
import json
import sys
from pathlib import Path

RUN = Path(sys.argv[1])
Q = "Must the first playable version of this game have this mechanic: {part}: {desc}?"
CORE, SUPPORT = 0.6, 0.3


def main():
    probs = json.load(open(RUN / "centrality_result.json"))[Q]
    state = json.load(open(RUN / "look_sound_result.json"))["state"]
    order = sorted(probs, key=lambda m: -probs[m])
    bands = {"core mechanics": [m for m in order if probs[m] >= CORE],
             "supporting mechanics": [m for m in order if SUPPORT <= probs[m] < CORE],
             "extra mechanics": [m for m in order if probs[m] < SUPPORT]}
    lines = [l for l in state.splitlines() if not l.startswith("mechanics:")]
    at = next(i for i, l in enumerate(lines) if l.startswith("art style:"))
    lines[at:at] = [f"{k}: {', '.join(v)}" for k, v in bands.items()]
    json.dump({"state": "\n".join(lines), "bands": bands}, open(RUN / "tiers_result.json", "w"), indent=1)
    for k, v in bands.items():
        print(f"{k} ({len(v)}): {', '.join(v)}")


if __name__ == "__main__":
    main()
