"""Ask JEV, for every kept mechanic, whether the game would feel wrong without it; the core set leads the design."""
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from flat import mechanics

RUN = Path(sys.argv[1])
QUESTIONS = sys.argv[2:] or ["Would this game feel broken or empty without this mechanic: {part}: {desc}?"]


def main():
    mech = json.load(open(RUN / "mechanics_result.json"))
    table = mechanics()
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    out = {}
    for q in QUESTIONS:
        one = lambda m: ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": mech["state"],
                                                             "question": q.format(part=m, desc=table[m])})["probabilities"][1]
        with ThreadPoolExecutor(16) as ex:
            probs = {n: round(p, 3) for n, p in zip(mech["kept"], ex.map(one, mech["kept"]))}
        out[q] = probs
        print(q)
        print("  " + ", ".join(f"{n} {p:.2f}" for n, p in sorted(probs.items(), key=lambda x: -x[1])))
    json.dump(out, open(RUN / "centrality_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
