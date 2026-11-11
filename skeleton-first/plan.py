"""The process planner once on <label>/design.md: Flash-Next writes the build steps in the order a
person builds with an AI (framework, replacements, UI, game), and the result lands as the label's
stages.json in prod's plan shape. Needs llama-swap up.
usage: plan.py <label>"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "pitch-interrogate"))
from interview import post
from llm_clients.message_builder import MessageBuilder
from maestro.codegen import stages

SYSTEM = (HERE.parent.parent / "src" / "maestro" / "codegen" / "prompts" / "stage" / "plan_system.txt").read_text(encoding="utf-8").strip()


def main():
    source = HERE / sys.argv[1]
    spec = (source / "design.md").read_text(encoding="utf-8")
    ask = (source / "state.txt").read_text(encoding="utf-8").splitlines()[0].removeprefix("Game prompt: ")
    asking = (HERE / "plan_process.txt").read_text(encoding="utf-8").format(ask=ask, budget=stages.PLAN_BUDGET, design=spec)
    text = post(MessageBuilder(SYSTEM).add_user(asking).build(), source, "plan")
    cut = [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
            "reads": stages.match_reads(s.get("reads") or [], spec)} for s in stages.parse(text)]
    plan = {"stages": cut, "budgets": stages.budgets(len(cut)), "attempts": {}, "before": {}}
    (source / stages.PLAN_FILE).write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    for i, s in enumerate(cut, 1):
        print(f"{i:2d}. {s['name']}: {s['stage']}\n    done: {s['done']}\n    reads: {s['reads']}")


if __name__ == "__main__":
    main()
