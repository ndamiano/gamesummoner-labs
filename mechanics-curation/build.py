"""One staged build on the prod path from a design and stage plan in <folder>/<run> (folder
defaults to designs): a new private run with the control run's ask, so Flash-Next builds it as it
built the control. Needs run.py and scripts/local_gpu.py auto up.
usage: build.py <control run id> [folder]"""
import json
import logging
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import bootstrap

bootstrap()
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.codegen import build_chain, design, stages
from maestro.codegen.run import _await_build, create_run, open_ask, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState

HERE = Path(__file__).resolve().parent


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")
    source = HERE / (sys.argv[2] if len(sys.argv) > 2 else "designs") / sys.argv[1]
    ask = (source / "state.txt").read_text(encoding="utf-8").splitlines()[0].removeprefix("Game prompt: ")
    run = create_run(store.list_users()[0].id, private=True)
    games.charge_game(run, 0, MICROS_PER_CREDIT)
    open_ask(run, ask)
    run_dir = RunState(run).run_dir
    shutil.copy2(source / "design.md", spec_path(run_dir))
    (run_dir / design.DESIGN_DIR).mkdir(exist_ok=True)
    if (source / "decisions.json").exists():
        shutil.copy2(source / "decisions.json", run_dir / design.DESIGN_DIR / design.DECISIONS)
    stages._save(run_dir, json.loads((source / stages.PLAN_FILE).read_text(encoding="utf-8")))
    set_prompt(run, design._request(ask))
    build_chain.kickoff(run, kind="build", designed=True)
    (source / "build.txt").write_text(run + "\n", encoding="utf-8")
    print(f"run: {run} from {sys.argv[1]}: {ask}", flush=True)
    result = _await_build(run)
    print("result:", result.ok, result.steps, f"{result.elapsed:.0f}s", result.summary, flush=True)


if __name__ == "__main__":
    main()
