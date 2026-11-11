"""One staged build on the prod path from the design in <label>/: prod's stage plan if the label has
none yet, then a new private run with the label's ask, built by Flash-Next on the local card. Starts
the GPU runner itself and restarts it on a stall. Needs run.py up.
usage: build.py <label>"""
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen import build_chain, design, stages
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState

from interview import post


def plan(source):
    spec = (source / "design.md").read_text(encoding="utf-8")
    for _ in range(design.RETRIES + 1):
        text = post(stages.plan_messages(spec), source, "plan")
        try:
            cut = [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
                    "reads": stages.match_reads(s.get("reads") or [], spec)} for s in stages.parse(text)]
            return {"stages": cut, "budgets": stages.budgets(len(cut)), "attempts": {}, "before": {}}
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            tiers.log(f"plan did not parse: {e}")
    raise SystemExit(f"{source.name}: no stage plan")


def main():
    source = HERE / sys.argv[1]
    landed = source / stages.PLAN_FILE
    if not landed.exists():
        landed.write_text(json.dumps(plan(source), indent=1, ensure_ascii=False), encoding="utf-8")
    cut = json.loads(landed.read_text(encoding="utf-8"))
    tiers.log(f"{len(cut['stages'])} stages: " + " · ".join(s["name"] for s in cut["stages"]))
    ask = (source / "state.txt").read_text(encoding="utf-8").splitlines()[0].removeprefix("Game prompt: ")
    run = create_run(tiers.store.list_users()[0].id, private=True)
    tiers.games.charge_game(run, 0, tiers.MICROS_PER_CREDIT)
    open_ask(run, ask)
    run_dir = RunState(run).run_dir
    shutil.copy2(source / "design.md", spec_path(run_dir))
    stages._save(run_dir, cut)
    set_prompt(run, design._request(ask))
    (source / "build.txt").write_text(run + "\n", encoding="utf-8")
    services = tiers.Services(source)
    services.ensure()
    tiers.log(f"run {run}: {ask}")
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"the build would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        checks = stages.load(run_dir)["attempts"]
        entry = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
                 "stage checks": {k: [(a["attempt"], a["boots"], len(a["errors"])) for a in v] for k, v in checks.items()},
                 **tiers.summary(run)}
        (source / "build.json").write_text(json.dumps(entry, indent=1, ensure_ascii=False), encoding="utf-8")
        tiers.log(f"ended {status} after {entry['minutes']} min: {json.dumps(entry, ensure_ascii=False)}")
    finally:
        services.stop()


if __name__ == "__main__":
    main()
