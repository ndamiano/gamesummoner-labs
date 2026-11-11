"""One naked build on the prod path: the Reddit subway-FPS prompt is the ask, the build's user message
and the whole of design/design.md, built public so the build seat lands on the deepseek-4.1 entry.
Starts the GPU runner for the other queues and restarts it on a stall. Needs run.py up."""
import json
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen import build_chain
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState


def spent_usd(run):
    with sqlite3.connect(tiers.DB, uri=True, timeout=10) as conn:
        micros, = conn.execute("select sum(billed_micros) from jobs where game_id = ?", (run,)).fetchone()
    return round((micros or 0) / 1e6, 3)


def main():
    prompt = (HERE / "prompt.txt").read_text(encoding="utf-8").strip()
    run = create_run(tiers.store.list_users()[0].id, private=False)
    tiers.games.charge_game(run, 0, 3 * tiers.MICROS_PER_CREDIT)
    open_ask(run, prompt)
    spec_path(RunState(run).run_dir).write_text(prompt + "\n", encoding="utf-8")
    set_prompt(run, prompt)
    (HERE / "run.txt").write_text(run + "\n", encoding="utf-8")
    services = tiers.Services(HERE)
    services.ensure()
    tiers.log(f"run {run}: {prompt}")
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"the build would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        entry = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
                 "usd": spent_usd(run), **tiers.summary(run)}
        (HERE / "build.json").write_text(json.dumps(entry, indent=1) + "\n", encoding="utf-8")
        tiers.log(f"ended {status} after {entry['minutes']} min: {json.dumps(entry)}")
    finally:
        services.stop()


if __name__ == "__main__":
    main()
