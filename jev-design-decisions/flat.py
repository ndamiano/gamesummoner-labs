"""Ask JEV yes/no on every mechanic in mechanics.md on its own, with its description and the frame as state."""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from frame import state_of

RUN = Path(sys.argv[1])

QUESTION = "Does this mechanic make sense for this game: {part}: {desc}?"


def mechanics():
    rows = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", open("mechanics.md").read(), re.M)
    return {m: d for m, d in rows if m not in ("Mechanic", "---")}


def main():
    frame = json.load(open(RUN / "frame_result.json"))
    state = state_of(frame["prompt"], frame["decided"])
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    table = mechanics()
    ask_one = lambda m: ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state,
                                                             "question": QUESTION.format(part=m, desc=table[m])})["probabilities"][1]
    names = list(table)
    with ThreadPoolExecutor(16) as ex:
        probs = {n: round(p, 3) for n, p in zip(names, ex.map(ask_one, names))}
    kept = sorted((n for n, p in probs.items() if p > 0.6), key=lambda n: -probs[n])
    print(", ".join(f"{n} {probs[n]:.2f}" for n in kept))
    json.dump({"state": state, "question": QUESTION, "probabilities": probs, "kept": kept},
              open(RUN / "mechanics_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
