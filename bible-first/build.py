"""The bible-first chain on the prod path for the ask in ask.txt, a private run on Flash-Next:
JEV decides, the model writes the game we want (bible.txt), then the minimum that is a game
(minimum.txt); design.md is the concept, the decisions, how it is built and the bible; the process
planner (plan_process.txt) cuts the stages; then the staged build. Each ask lives in its own
folder here with ask.txt; `plan` stops after stages.json so the bible and the minimum can be read,
`build` kicks the build off on the run in the folder's run.txt, `all` does both, and `battery`
does both for every folder named, continuing past a failure. Starts the GPU runner itself. Needs
run.py up.
usage: build.py plan|build|all <label>   |   build.py battery <label>..."""
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from config import llm_models
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from maestro.codegen import build_chain, design, stages
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState
from tools.execution_context import run_scope

MAX_TOKENS = design.MAX_TOKENS
PLAN_SYSTEM = (HERE.parent.parent / "src" / "maestro" / "codegen" / "prompts" / "stage" / "plan_system.txt").read_text(encoding="utf-8").strip()


def ask_llm(run, system, body):
    conn = get_connector(llm_models.seat("design", True))
    for _ in range(2):
        text = design._reply_text(conn.generate_with_tools(
            MessageBuilder(system).add_user(body).build(), [], max_tokens=MAX_TOKENS)).strip()
        if text:
            return text
    raise SystemExit("the model came back empty twice")


def prompt(name, **slots):
    text = (HERE / f"{name}.txt").read_text(encoding="utf-8")
    for key, value in slots.items():
        text = text.replace("{" + key + "}", value)
    return text


def plan(source):
    ask = (source / "ask.txt").read_text(encoding="utf-8").strip()
    run = create_run(tiers.store.list_users()[0].id, private=True)
    tiers.games.charge_game(run, 0, 3 * tiers.MICROS_PER_CREDIT)
    open_ask(run, ask)
    (source / "run.txt").write_text(run + "\n", encoding="utf-8")
    run_dir = RunState(run).run_dir
    tiers.log(f"run {run}: {ask}")
    services = tiers.Services(source)
    services.ensure()
    build_id = tiers.games.create_build(run, kind="design")
    tiers.games.build_started(build_id)
    try:
        with run_scope(run, build_id):
            decided = design._decide(ask)
            state = design.tiered_state(decided)
            (source / "decisions.txt").write_text(state + "\n", encoding="utf-8")
            tiers.log(f"decided:\n{state}")
            bible = ask_llm(run, design._SYSTEM, prompt("bible", ask=ask, state=state))
            (source / "bible.md").write_text(bible + "\n", encoding="utf-8")
            tiers.log(f"bible, {len(bible.split())} words:\n{bible}")
            minimum = ask_llm(run, design._SYSTEM, prompt("minimum", ask=ask, state=state, bible=bible))
            (source / "minimum.md").write_text(minimum + "\n", encoding="utf-8")
            tiers.log(f"minimum:\n{minimum}")
            concept, built = minimum.split("# 2. HOW IT IS BUILT", 1)
            spec = (f"{concept.strip()}\n\n# 1. DECISIONS\n\n{state}\n\n# 2. HOW IT IS BUILT\n{built.rstrip()}"
                    f"\n\n# 3. THE GAME WE WANT\n\n{bible}\n")
            (source / "design.md").write_text(spec, encoding="utf-8")
            asking = (HERE / "plan_process.txt").read_text(encoding="utf-8").format(
                ask=ask, budget=stages.PLAN_BUDGET, design=spec)
            for attempt in range(3):
                text = ask_llm(run, PLAN_SYSTEM, asking)
                (source / f"plan-raw-{attempt}.txt").write_text(text, encoding="utf-8")
                try:
                    parsed = stages.parse(text)
                    break
                except (ValueError, KeyError) as e:
                    tiers.log(f"plan attempt {attempt} did not parse: {e!r}")
            else:
                raise SystemExit("the plan did not parse three times")
            cut = [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
                    "reads": stages.match_reads(s.get("reads") or [], spec)} for s in parsed]
        tiers.games.build_finished(build_id, "succeeded", steps=4)
    except BaseException:
        tiers.games.build_finished(build_id, "failed", steps=4)
        services.stop()
        raise
    plan = {"stages": cut, "budgets": stages.budgets(len(cut)), "attempts": {}, "before": {}}
    (source / stages.PLAN_FILE).write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    shutil.copy2(source / "design.md", spec_path(run_dir))
    stages._save(run_dir, plan)
    set_prompt(run, design._request(ask))
    services.stop()
    tiers.log(f"{len(cut)} stages: " + " · ".join(s["name"] for s in cut))
    for i, s in enumerate(cut, 1):
        tiers.log(f"{i:2d}. {s['name']}: {s['stage']}\n    done: {s['done']}\n    reads: {s['reads']}")


def build(source):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    run_dir = RunState(run).run_dir
    services = tiers.Services(source)
    services.ensure()
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"the build would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        checks = stages.load(run_dir)["attempts"]
        entry = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
                 "stage checks": {k: [(a["attempt"], a["boots"], len(a["errors"])) for a in v] for k, v in checks.items()},
                 **tiers.summary(run)}
        (source / "build.json").write_text(json.dumps(entry, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        tiers.log(f"ended {status} after {entry['minutes']} min: {json.dumps(entry, ensure_ascii=False)}")
    finally:
        services.stop()


def all_(source):
    plan(source)
    build(source)


def battery(labels):
    for label in labels:
        try:
            all_(HERE / label)
        except BaseException as e:
            tiers.log(f"{label} failed: {e!r}")


if __name__ == "__main__":
    if sys.argv[1] == "battery":
        battery(sys.argv[2:])
    else:
        {"plan": plan, "build": build, "all": all_}[sys.argv[1]](HERE / sys.argv[2])
