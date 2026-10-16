"""Make the frame-of-the-game decisions for one prompt with JEV, each answer carried into the next question."""
import json
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

RUN = Path(sys.argv[1])

CAMERAS = {"2d": ["top-down", "side-on", "isometric"],
           "3d": ["first-person", "third-person", "top-down", "isometric"]}
ONE = [
    ("dimension", "Should this game be 2d or 3d?", lambda d: ["2d", "3d"]),
    ("camera", "Which camera view should this game use?", lambda d: CAMERAS[d["dimension"]]),
    ("time model", "How does time pass in this game?", lambda d: ["real-time", "turn-based", "real-time with pause"]),
    ("movement model", "How does the player move?", lambda d: ["free movement", "grid-based", "lanes", "on rails", "no movement, cursor only"]),
    ("session shape", "What is the shape of a play session?", lambda d: ["single screen", "a sequence of levels", "endless", "open world", "connected rooms"]),
    ("failure", "What happens when the player fails?", lambda d: ["restart the level", "lose a life", "return to a checkpoint", "permadeath, start a new run", "no failure"]),
    ("tone", "What tone should this game have?", lambda d: ["cozy", "tense", "silly", "epic", "eerie"]),
    ("size", "How big should this game be?", lambda d: ["one screen, a few minutes", "a handful of levels, under 30 minutes", "many levels, a few hours"]),
]
MANY = [
    ("win/lose", "Should this game end this way?", ["survive as long as possible", "reach the exit", "beat a score", "defeat a final boss", "no ending, play forever"]),
]


def state_of(prompt, decided):
    lines = [f"Game prompt: {prompt}"] + [f"{k}: {v}" for k, v in decided.items()]
    return "\n".join(lines)


def main():
    prompt = sys.argv[2]
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    decided, log = {}, []
    for key, question, options in ONE:
        opts = options(decided)
        r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "choice", "state": state_of(prompt, decided),
                                                  "question": question, "options": opts})
        decided[key] = r["choice"]
        probs = dict(sorted(zip(opts, (round(p, 3) for p in r["probabilities"])), key=lambda x: -x[1]))
        log.append({"decision": key, "question": question, "probabilities": probs})
        print(f"{key:15} {r['choice']:40} {probs}")
    for key, question, opts in MANY:
        probs = {}
        for o in opts:
            r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state_of(prompt, decided),
                                                      "question": f"{question} {o}"})
            probs[o] = round(r["probabilities"][1], 3)
        decided[key] = [o for o, p in probs.items() if p > 0.6]
        log.append({"decision": key, "question": question, "probabilities": probs})
        print(f"{key:15} {decided[key]}  {probs}")
    json.dump({"prompt": prompt, "decided": decided, "log": log}, open(RUN / "frame_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
