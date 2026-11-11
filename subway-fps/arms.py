"""Two public runs on the deepseek-4.1 entry, waited on together under one GPU runner: a naked build
of the ask in <naked prompt file> (ask = user message = design.md, as build.py) and the full prod
chain (design write, JEV, stage plan, staged build) for the ask in <chain prompt file>.
usage: arms.py <naked prompt file> <chain prompt file>; writes arms.json here. Needs run.py up."""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from build import spent_usd
from maestro.codegen import build_chain
from maestro.codegen.run import create_run, open_ask, propose_prompt, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState


def new_run():
    run = create_run(tiers.store.list_users()[0].id, private=False)
    tiers.games.charge_game(run, 0, 3 * tiers.MICROS_PER_CREDIT)
    return run


def naked(prompt):
    run = new_run()
    open_ask(run, prompt)
    spec_path(RunState(run).run_dir).write_text(prompt + "\n", encoding="utf-8")
    set_prompt(run, prompt)
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"naked build would not start, game is {tiers.games.game(run)}")
    return run


def chain(prompt):
    run = new_run()
    propose_prompt(prompt, run)
    return run


def main():
    arms = {"naked": naked((HERE / sys.argv[1]).read_text(encoding="utf-8").strip()),
            "chain": chain((HERE / sys.argv[2]).read_text(encoding="utf-8").strip())}
    (HERE / "arms.txt").write_text(json.dumps(arms) + "\n", encoding="utf-8")
    tiers.log(f"runs {arms}")
    services = tiers.Services(HERE)
    services.ensure()
    began, result = time.time(), {}
    try:
        for name, run in arms.items():
            status = tiers.wait(run, services)
            result[name] = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
                            "usd": spent_usd(run), **tiers.summary(run)}
            tiers.log(f"{name} ended {status}: {json.dumps(result[name])}")
        (HERE / "arms.json").write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
    finally:
        services.stop()


if __name__ == "__main__":
    main()
