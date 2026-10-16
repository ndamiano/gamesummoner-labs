"""Ask JEV a yes/no question (default "Is this design sufficient?") of every finished local design, plus controls."""
import glob
import json
import os
import re
import sys

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

RUNS = "/home/nick/output/runs"


def design_of(run):
    for p in (f"{RUNS}/{run}/game/design/design.md", f"{RUNS}/{run}/design.md"):
        if os.path.exists(p):
            return open(p).read()


def ask_yes(state, question):
    r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "noul", "state": state, "question": question})
    return round(r["probabilities"][1], 4)


def main():
    question = sys.argv[1] if len(sys.argv) > 1 else "Is this design sufficient?"
    runs = sorted({p[len(RUNS) + 1:].split("/")[0]
                   for p in glob.glob(f"{RUNS}/*/game/design/design.md") + glob.glob(f"{RUNS}/*/design.md")})
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    out = []
    for run in runs:
        spec = json.load(open(f"{RUNS}/{run}/spec.json"))
        row = {"run": run, "prompt": spec.get("ask") or spec.get("request", ""), "p_yes": ask_yes(design_of(run), question)}
        out.append(row)
        print(f"{row['p_yes']:.3f}  {run}  {row['prompt'][:80]}", flush=True)
    d = design_of("e9d964fc34c7")
    controls = {"empty": "(no design)", "bare prompt": json.load(open(f"{RUNS}/e9d964fc34c7/spec.json"))["ask"],
                "first 5%": d[: len(d) // 20], "full": d}
    controls = {k: ask_yes(v, question) for k, v in controls.items()}
    print("controls (cozy fishing):", controls)
    name = "sufficiency_results.json" if len(sys.argv) == 1 else "sufficiency_" + re.sub(r"[^a-z]+", "_", question.lower()).strip("_")[:40] + ".json"
    json.dump({"question": question, "designs": out, "controls": controls}, open(name, "w"), indent=1)


if __name__ == "__main__":
    main()
