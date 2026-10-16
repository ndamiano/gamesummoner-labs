"""Ninfer's 27B lists candidate mechanics for the frame; JEV triages each and picks the core loop."""
import json
import re
import time
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from frame import state_of

RUN = Path(sys.argv[1])

GEN = "qwen3.8-27b-quasar"

TIERS = ["core: the game does not work without it", "nice-to-have: makes the game better",
         "cut: not worth building"]


def mechanics(state):
    prompt = open("prompts/mechanics.txt").read().format(state=state)
    r = ask.chat(GEN, prompt, 16000, think=True)
    json.dump(r, open(RUN / "mechanics_raw.json", "w"), indent=1)
    text = r["choices"][0]["message"]["content"].split("</think>")[-1]
    return json.loads(re.search(r"\[.*\]", text, re.S).group(0))


def main():
    frame = json.load(open(RUN / "frame_result.json"))
    state = state_of(frame["prompt"], frame["decided"])
    t = time.time()
    mechs = mechanics(state)
    print(f"generated in {time.time() - t:.0f}s")
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    listing = "\n".join(f"- {m['name']}: {m['what']}" for m in mechs)
    full = f"{state}\n\nCandidate mechanics:\n{listing}"
    print(f"{len(mechs)} candidates\n")
    out = []
    for m in mechs:
        r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "choice", "state": full, "options": TIERS,
                                                  "question": f"How important is the mechanic '{m['name']}' to this game?"})
        tier = r["choice"].split(":")[0]
        out.append({**m, "tier": tier, "p": [round(p, 3) for p in r["probabilities"]]})
    for t in ("core", "nice-to-have", "cut"):
        print(f"== {t}")
        for m in sorted((m for m in out if m["tier"] == t), key=lambda m: -max(m["p"])):
            print(f"  {max(m['p']):.2f}  {m['name']}: {m['what']}")
    names = [m["name"] for m in out if m["tier"] == "core"] or [m["name"] for m in out]
    r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "choice", "state": full, "options": names,
                                              "question": "Which one mechanic is the core loop of this game?"})
    core = dict(sorted(zip(names, (round(p, 3) for p in r["probabilities"])), key=lambda x: -x[1]))
    print("\ncore loop:", core)
    json.dump({"state": state, "mechanics": out, "core_loop": core}, open(RUN / "gameplay_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
