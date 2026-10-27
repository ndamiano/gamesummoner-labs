"""Several playtest-refine rounds in a row: each round's after-session is the next round's
before-session, so the player goes through the game once per round plus once at the start. A
round the progress judge calls worse is dropped and the next round starts again from the last
build that was not. Each build is played SESSIONS times and the furthest session stands for it,
since one session on one build can end very differently from the next. One JSON line per round in results.jsonl.

    venv/bin/python labs/playtest-refine/loop.py <run id> <label> <rounds> [director prompt file]
"""

import json
import os
import shutil
import subprocess
import sys
import time

import refine
from auth import store
from billing.packages import MICROS_PER_CREDIT
from db import games
from maestro.codegen import build_chain, snapshots
from maestro.codegen.run import _await_build, create_run, open_ask, set_prompt
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState


def copy_any(source: str) -> str:
    """A new run holding source's design and the game at its latest snapshot."""
    src = RunState(source)
    rid = create_run(store.list_users()[0].id)
    games.charge_game(rid, 0, MICROS_PER_CREDIT)
    open_ask(rid, src.read_spec()["ask"])
    shutil.copy2(spec_path(src.run_dir), spec_path(RunState(rid).run_dir))
    set_prompt(rid, src.read_spec().get("request") or src.read_spec()["ask"])
    game = game_dir(RunState(rid).run_dir)
    game.mkdir(parents=True, exist_ok=True)
    archive = subprocess.run(["git", f"--git-dir={src.run_dir / 'game.git'}", "archive", "HEAD"],
                             check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(game)], input=archive, check=True)
    snapshots.take(RunState(rid).run_dir, "copied")
    return rid


def progress(seen, after) -> dict:
    prompt = refine._prompt("progress.txt").format(
        before_reached=seen["reached"], after_reached=after["reached"],
        before_observations=json.dumps(seen["observations"], ensure_ascii=False),
        after_observations=json.dumps(after["observations"], ensure_ascii=False))
    reply = refine.get_connector("qwen-flash-next").generate_with_tools(
        refine.MessageBuilder("You judge playtests.").add_user(prompt).build(), [])
    text = ((reply.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    return refine.play_gate._parse_json(text) or {"verdict": "same", "why": "unparsed"}


SESSIONS = 2


def best_session(gdir, request, out):
    best = None
    for k in range(SESSIONS):
        s = refine.session(gdir, request, out / f"s{k}")
        if best is None or progress(best, s).get("verdict") == "further":
            best = s
    return best


def main(source: str, label: str, rounds: int, director: str = "director_v2.txt") -> None:
    out = refine.OUT / label
    request = refine.request_for(source)
    current = source
    seen = best_session(game_dir(RunState(source).run_dir), request, out / "round0")
    print(f"round 0: {len(seen['observations'])} observations, reached: {seen['reached']}", flush=True)
    for r in range(1, rounds + 1):
        t0 = time.time()
        changes = refine.direct(current, seen["observations"], seen["turns"], v2=director)
        note = refine.note_of(changes, v2=True)
        (out / f"note{r}.txt").write_text(note, encoding="utf-8")
        rid = copy_any(current) if r > 1 or not (refine.stage.RUNS / current / "stage.json").exists() else refine.copy_of(current)
        if os.environ.get("REFINE_LOOK"):
            (RunState(rid).run_dir / "look.flag").write_text(os.environ["REFINE_LOOK"])
        build_chain.kickoff(rid, kind="change", note=note, max_steps=refine.CHANGE_STEPS,
                            designed=games.game(rid)["stage"] == "designing")
        built = _await_build(rid)
        while (games.game(rid) or {}).get("status") == "running":
            time.sleep(30)
        after = best_session(game_dir(RunState(rid).run_dir), request, out / f"round{r}")
        print(f"round {r}: build {rid} steps={built.steps}; {len(after['observations'])} observations, "
              f"reached: {after['reached']}", flush=True)
        for o in after["observations"]:
            print("  -", o.get("problem"), flush=True)
        judged = progress(seen, after)
        print(f"round {r} judged {judged.get('verdict')}: {judged.get('why')}", flush=True)
        with refine.RESULTS.open("a") as f:
            f.write(json.dumps({"label": label, "version": director, "round": r, "source": current,
                                "refined": rid, "seconds": round(time.time() - t0),
                                "change_steps": built.steps, "changes": changes, "judged": judged,
                                "before": {"observations": seen["observations"], "reached": seen["reached"]},
                                "after": {"observations": after["observations"], "reached": after["reached"],
                                          "page_errors": after["page_errors"]}}, ensure_ascii=False) + "\n")
        if judged.get("verdict") != "worse":
            current, seen = rid, after
    print(f"loop done {label} {current}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]), *sys.argv[4:5])
