"""Frame plus the flat mechanics list for every distinct prompt in rows.json, in one process, results under runs/cov/."""
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.argv = ["coverage.py", "runs/cov"]
sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from frame import MANY, ONE, state_of
from flat import QUESTION, mechanics

TABLE = mechanics()
POOL = ThreadPoolExecutor(8)
MAX_CHARS = 4000


def decide(body):
    try:
        return ask.post(f"{ask.DECIDE}/v1/decide", body)
    except OSError:
        warm()
        return ask.post(f"{ask.DECIDE}/v1/decide", body)


def warm():
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()


def keep_alive():
    while True:
        time.sleep(60)
        ask.chat(ask.JEV, "hi", 1, think=False)


def frame(prompt):
    decided, log = {}, []
    for key, question, options in ONE:
        opts = options(decided)
        r = decide({"kind": "choice", "state": state_of(prompt, decided), "question": question, "options": opts})
        decided[key] = r["choice"]
        log.append({"decision": key, "question": question,
                    "probabilities": dict(zip(opts, (round(p, 3) for p in r["probabilities"])))})
    for key, question, opts in MANY:
        st = state_of(prompt, decided)
        probs = {o: round(decide({"kind": "noul", "state": st, "question": f"{question} {o}"})["probabilities"][1], 3) for o in opts}
        decided[key] = [o for o, p in probs.items() if p > 0.6]
        log.append({"decision": key, "question": question, "probabilities": probs})
    return {"prompt": prompt, "decided": decided, "log": log}


def framed(row):
    run = Path("runs/cov") / row["run"]
    run.mkdir(parents=True, exist_ok=True)
    if not (run / "frame_result.json").exists():
        json.dump(frame(row["prompt"]), open(run / "frame_result.json", "w"), indent=1)


def one(row):
    run = Path("runs/cov") / row["run"]
    if (run / "mechanics_result.json").exists() or not (run / "frame_result.json").exists():
        return
    f = json.load(open(run / "frame_result.json"))
    state = state_of(f["prompt"], f["decided"])
    names = list(TABLE)
    ps = POOL.map(lambda m: decide({"kind": "noul", "state": state, "question": QUESTION.format(part=m, desc=TABLE[m])})["probabilities"][1], names)
    probs = {n: round(p, 3) for n, p in zip(names, ps)}
    kept = sorted((n for n, p in probs.items() if p > 0.6), key=lambda n: -probs[n])
    json.dump({"state": state, "question": QUESTION, "probabilities": probs, "kept": kept},
              open(run / "mechanics_result.json", "w"), indent=1)
    print(row["run"], len(kept), flush=True)


def safe(fn, row):
    try:
        fn(row)
    except OSError as e:
        print(row["run"], "FAILED", len(row["prompt"]), e, flush=True)


def main():
    seen = {}
    for r in json.load(open("rows.json")):
        if len(r["prompt"]) <= MAX_CHARS:
            seen.setdefault(r["prompt"], r)
    seen = dict(sorted(seen.items(), key=lambda kv: len(kv[0])))
    warm()
    threading.Thread(target=keep_alive, daemon=True).start()
    with ThreadPoolExecutor(2) as ex:
        list(ex.map(lambda r: safe(framed, r), seen.values()))
    print("frames done", flush=True)
    for row in seen.values():
        try:
            one(row)
        except OSError as e:
            print(row["run"], "FAILED", len(row["prompt"]), e, flush=True)


if __name__ == "__main__":
    main()
