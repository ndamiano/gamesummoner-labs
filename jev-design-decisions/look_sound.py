"""Make the look-and-sound decisions in look_sound.md with JEV, with the frame and kept mechanics (or the old systems) as state."""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

RUN = Path(sys.argv[1])

QUESTIONS = {
    "Art style, 2D": "Which art style should this game use?",
    "Art style, 3D": "Which art style should this game use?",
    "Palette": "Which colour palette should this game use?",
    "Lighting, 3D only": "Which lighting should this game use?",
    "Typography": "Which typography should this game's text use?",
    "Music": "Which music should this game have?",
    "Sound effects style": "Which style of sound effects should this game have?",
    "Screens": "Should this game have this screen: {item}?",
    "HUD": "Should this game's HUD show {item}?",
    "Effects": "Should this game use this visual effect: {item}?",
    "Accessibility": "Should this game offer this accessibility option: {item}?",
}


def tables():
    text = open("look_sound.md").read()
    one, many = (dict(re.findall(r"^\| ([^|]+?) \| ([^|]+) \|$", s, re.M)) for s in text.split("## Many"))
    drop = ("Decision", "---")
    one = {k: dict(o.strip().split(": ", 1) for o in v.split("; ")) for k, v in one.items() if k not in drop}
    many = {k: [i.strip() for i in v.split(",")] for k, v in many.items() if k not in drop}
    return one, many


def state_of(base, decided):
    return base + "".join(f"\n{k}: {v}" for k, v in decided.items())


def main():
    if (RUN / "mechanics_result.json").exists():
        mech = json.load(open(RUN / "mechanics_result.json"))
        base = mech["state"] + "\nmechanics: " + ", ".join(mech["kept"])
    else:
        systems = json.load(open(RUN / "systems2_result.json"))
        kept = {s: p for s, p in systems["kept"].items() if p}
        base = json.load(open(RUN / "systems_result.json"))["state"] + "\nsystems: " + "; ".join(f"{s.lower()}: {', '.join(p)}" for s, p in kept.items())
    dim = json.load(open(RUN / "frame_result.json"))["decided"]["dimension"]
    one, many = tables()
    skip = {"2d": ("Art style, 3D", "Lighting, 3D only"), "3d": ("Art style, 2D",)}[dim]
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    decided, log = {}, []
    for key, opts in one.items():
        if key in skip:
            continue
        labels = [f"{n}: {d}" for n, d in opts.items()]
        r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "choice", "state": state_of(base, decided),
                                                  "question": QUESTIONS[key], "options": labels})
        name = r["choice"].split(":")[0]
        decided[key.split(",")[0].lower()] = r["choice"]
        probs = dict(sorted(zip(opts, (round(p, 3) for p in r["probabilities"])), key=lambda x: -x[1]))
        log.append({"decision": key, "probabilities": probs})
        print(f"{key:20} {name:22} {probs}")
    for key, items in many.items():
        probs = {}
        for item in items:
            r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state_of(base, decided),
                                                      "question": QUESTIONS[key].format(item=item)})
            probs[item] = round(r["probabilities"][1], 3)
        decided[key.lower()] = ", ".join(i for i, p in probs.items() if p > 0.6) or "none"
        log.append({"decision": key, "probabilities": probs})
        print(f"{key:20} {decided[key.lower()]:40} {probs}")
    json.dump({"state": state_of(base, decided), "decided": decided, "log": log}, open(RUN / "look_sound_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
