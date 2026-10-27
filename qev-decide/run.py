"""Replay the prod design decide chain on a small decision model through the prod executor (contract/decide.py
run_chain), then compare every step with JEV-27B-VL's decisions.json from real runs of the same ask.

usage: <engine venv>/bin/python -I run.py CHAIN_JSON OUT_JSON JEV_DECISIONS... --engine qev|d2b [--device cpu|cuda]
  qev: /var/lib/models/qev/venv        d2b (flymy-ai/decision-2b-preview, CUDA only): /var/lib/models/decision-2b/venv
"""
import argparse
import json
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("chain")
ap.add_argument("out")
ap.add_argument("jev", nargs="+")
ap.add_argument("--engine", choices=["qev", "d2b"], required=True)
ap.add_argument("--device", default="cpu")
a = ap.parse_args()

sys.path.insert(0, "/home/nick/Documents/gamesummoner-images")
from contract.decide import run_chain

reads = []
t0 = time.time()
if a.engine == "qev":
    if a.device == "cpu":
        sys.modules["fla"] = None
    sys.path.insert(0, "/var/lib/models/qev/qev-0.8b")
    import torch
    from qev import QEV

    MODEL = QEV.from_pretrained("/var/lib/models/qev/qev-0.8b", device=a.device, dtype=torch.bfloat16,
                                backend="transformers" if a.device == "cpu" else "auto")

    def ask(kind, state, questions):
        qs = {}
        for i, (q, opts) in enumerate(questions):
            qs[str(i)] = {"type": kind, "instructions": q}
            if kind == "choice":
                qs[str(i)]["criteria"] = {o: None for o in opts}
        d = MODEL.distributions_batch([(state, qs)], per_question=True)[0]
        if kind == "noul":
            return [[d[str(i)]["False"], d[str(i)]["True"]] for i in range(len(questions))]
        return [[d[str(i)][o] for o in opts] for i, (_, opts) in enumerate(questions)]
else:
    sys.path.insert(0, "/var/lib/models/decision-2b/decision-2b-preview")
    import model as d2b

    MODEL = d2b.load("/var/lib/models/decision-2b/base")

    def ask(kind, state, questions):
        out = []
        for q, opts in questions:
            question = {"type": kind, "instructions": q}
            if kind == "choice":
                question["criteria"] = {o: None for o in opts}
            p = MODEL.decide(state, question)["probabilities"]
            out.append([p["false"], p["true"]] if kind == "noul" else [p[o] for o in opts])
        return out
load_s = time.time() - t0


def read(kind, state, questions):
    t = time.time()
    out = ask(kind, state, questions)
    reads.append((kind, len(questions), time.time() - t))
    return out


chain = json.load(open(a.chain))
t = time.time()
result = run_chain(read, chain["state"], chain["steps"])
chain_s = time.time() - t
json.dump({"result": result, "load_s": load_s, "chain_s": chain_s, "reads": reads}, open(a.out, "w"), indent=1)

jevs = [json.load(open(p)) for p in a.jev]
lists = {s["key"] for s in chain["steps"] if "keep_over" in s}
print(f"load {load_s:.1f} s, chain {chain_s:.1f} s, {sum(n for _, n, _ in reads)} questions in {len(reads)} reads")
for step in result["steps"]:
    key = step["key"]
    if step["skipped"]:
        print(f"{key:20s} model skipped | jev " + " / ".join(str(j["answers"].get(key, "skipped"))[:30] for j in jevs))
        continue
    q = result["answers"].get(key)
    js = [j["answers"].get(key) for j in jevs]
    if key in lists:
        qs = set(str(q or "").split(", ")) - {""}
        sets = [set(str(x or "").split(", ")) - {""} for x in js]
        both = [len(qs & s) for s in sets]
        print(f"{key:20s} model {len(qs)} kept | jev {[len(s) for s in sets]} kept | overlap {both}")
    elif q is None:
        p = step["probabilities"]
        jp = [next((s.get("probabilities") or {} for s in j["steps"] if s["key"] == key), {}) for j in jevs]
        top = sorted(p, key=lambda k: -p[k])[:5]
        print(f"{key:20s} qev top {[(k, round(p[k], 2)) for k in top]}")
        for x in jp:
            jt = sorted(x, key=lambda k: -x[k])[:5]
            print(f"{'':20s} jev top {[(k, round(x[k], 2)) for k in jt]}")
    else:
        mark = "=" if all(q == x for x in js) else ("~" if q in js else "x")
        p = step["probabilities"][q]
        print(f"{key:20s} {mark} model {str(q)[:40]} ({p:.2f}) | jev " + " / ".join(str(x)[:40] for x in js))
