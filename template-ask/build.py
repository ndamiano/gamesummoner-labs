"""One run on the prod path with the design stage replaced by a single llm call: the ask in ask.txt
goes through concrete_ask.txt on the design seat, the paragraph that comes back is the request and
the whole of design/design.md, and the build runs naked from it. Public run so both seats land on
the deepseek-4.1 entry. Starts the GPU runner for the other queues and restarts it on a stall.
Needs run.py up."""
import json
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from config import llm_models
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from maestro.codegen import build_chain, design
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import spec_path
from maestro.state import RunState
from tools.execution_context import run_scope

MAX_TOKENS = 16000


def spent_usd(run):
    with sqlite3.connect(tiers.DB, uri=True, timeout=10) as conn:
        micros, = conn.execute("select sum(billed_micros) from jobs where game_id = ?", (run,)).fetchone()
    return round((micros or 0) / 1e6, 3)


def concrete(run, ask):
    body = (HERE / "concrete_ask.txt").read_text(encoding="utf-8").replace("{ask}", ask)
    conn = get_connector(llm_models.seat("design", False))
    build_id = tiers.games.create_build(run, kind="design")
    tiers.games.build_started(build_id)
    with run_scope(run, build_id):
        reply = conn.generate_with_tools(MessageBuilder(design._SYSTEM).add_user(body).build(), [],
                                         max_tokens=MAX_TOKENS)
    text = design._reply_text(reply).strip()
    tiers.games.build_finished(build_id, "succeeded" if text else "failed", steps=1)
    if not text:
        raise SystemExit(f"the concrete ask came back empty: {reply.get('error')}")
    return text


def main():
    ask = (HERE / "ask.txt").read_text(encoding="utf-8").strip()
    run = create_run(tiers.store.list_users()[0].id, private=False)
    tiers.games.charge_game(run, 0, 3 * tiers.MICROS_PER_CREDIT)
    open_ask(run, ask)
    (HERE / "run.txt").write_text(run + "\n", encoding="utf-8")
    tiers.log(f"run {run}: {ask}")
    paragraph = concrete(run, ask)
    (HERE / "concrete.txt").write_text(paragraph + "\n", encoding="utf-8")
    tiers.log(f"concrete ask ({len(paragraph.split())} words, ${spent_usd(run)}):\n{paragraph}")
    spec_path(RunState(run).run_dir).write_text(paragraph + "\n", encoding="utf-8")
    set_prompt(run, paragraph)
    services = tiers.Services(HERE)
    services.ensure()
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"the build would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        entry = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
                 "usd": spent_usd(run), "concrete_words": len(paragraph.split()), **tiers.summary(run)}
        (HERE / "build.json").write_text(json.dumps(entry, indent=1) + "\n", encoding="utf-8")
        tiers.log(f"ended {status} after {entry['minutes']} min: {json.dumps(entry)}")
    finally:
        services.stop()


if __name__ == "__main__":
    main()
