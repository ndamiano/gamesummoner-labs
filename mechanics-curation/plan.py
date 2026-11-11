"""Prod's stage plan for each design written from the systems list: the plan prompt on the local
Flash-Next, parsed and landed as prod lands it, beside the control run's plan.
usage: plan.py [folder]"""
import json
import sys

from write import HERE, post

from lib.paths import RUNS
from maestro.codegen import design, stages

OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "designs")

def plan(spec, folder):
    for attempt in range(design.RETRIES + 1):
        text = post(stages.plan_messages(spec), folder / f"plan-raw-{attempt}.json")
        try:
            return [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
                     "reads": stages.match_reads(s.get("reads") or [], spec)} for s in stages.parse(text)]
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            print(f"  plan did not parse: {e}", flush=True)
    raise SystemExit(f"{folder.name}: no stage plan")


def main():
    out = ["# Stage plans for the designs written from the systems list", ""]
    for folder in sorted(p for p in OUT.iterdir() if (p / "design.md").exists()):
        spec = (folder / "design.md").read_text(encoding="utf-8")
        landed = folder / stages.PLAN_FILE
        if not landed.exists():
            cut = plan(spec, folder)
            landed.write_text(json.dumps({"stages": cut, "budgets": stages.budgets(len(cut)), "attempts": {},
                                          "before": {}}, indent=1, ensure_ascii=False), encoding="utf-8")
        new = json.loads(landed.read_text(encoding="utf-8"))
        out += [f"## {(folder / 'state.txt').read_text(encoding='utf-8').splitlines()[0].removeprefix('Game prompt: ')}", ""]
        for n, (s, budget) in enumerate(zip(new["stages"], new["budgets"]), 1):
            out += [f"{n}. **{s['name']}** ({budget} turns): {s['stage']}", f"   - done: {s['done']}",
                    f"   - reads: {'; '.join(s['reads'])}"]
        control = RUNS / folder.name / "design" / stages.PLAN_FILE
        if control.exists():
            names = [s["name"] for s in json.loads(control.read_text(encoding="utf-8"))["stages"]]
            out += ["", "control plan: " + " · ".join(names)]
        out += [""]
    (OUT / "plans.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
