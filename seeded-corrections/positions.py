"""Build a branch's starting world once, then step copies of it forward k turns."""

import json
import shutil
import sqlite3
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional

from lib import paths
from lib.replay import branch, replay

DB = paths.REPO / "data" / "platform.db"

NO_CODE = "carried no `code`"
NOTHING_RAN = "Nothing ran"


@dataclass
class World:
    dir: Path
    source_run: Path
    build: str
    system: str
    messages: List[Dict]
    turn: int
    setup_seconds: float


def _records(run: Path) -> List[Dict]:
    return [json.loads(line) for line in (run / "turns.jsonl").open(errors="replace")]


def _build_started(build: str) -> float:
    with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as db:
        return db.execute("SELECT queued_at FROM builds WHERE id = ?", (build,)).fetchone()[0]


def fix_start(run: Path, build: str, target: Path) -> World:
    """A fix build's turn 0: the `built` snapshot taken just before it, and its request."""
    t0 = time.time()
    started = _build_started(build)
    log = subprocess.run(["git", "--git-dir", str(run / "game.git"), "log", "--format=%H %ct"],
                         capture_output=True, text=True, check=True).stdout.split()
    commits = [(log[i], int(log[i + 1])) for i in range(0, len(log), 2)]
    commit = next(h for h, ct in commits if ct <= started)
    game = target / "game"
    game.mkdir(parents=True)
    replay._seed_vendor_as_it_was(run, target)
    subprocess.run(f"git --git-dir={run / 'game.git'} archive {commit} | tar -x -C {game}",
                   shell=True, check=True)
    shutil.copy2(run / "spec.json", target / "spec.json")
    records = _records(run)
    i = next(i for i, r in enumerate(records) if r.get("kind") == "meta" and r["build_id"] == build)
    first = next(r for r in records[i + 1:] if r.get("kind") == "turn")
    request = [m for m in first["added"] if m.get("role") == "user"][:1]
    return World(target, run, build, records[i]["system"], request, 0, time.time() - t0)


def _stubbed_tools(original: Callable) -> Callable:
    def tools_for(target, build_id, source_run):
        tools = original(target, build_id, source_run)
        tools["play"] = lambda *a, **k: {"ok": True, "result": None, "errors": [], "console": []}
        tools["check_syntax"] = lambda *a, **k: {"checked": {}}
        return tools
    return tools_for


def _seed_with_design(original: Callable) -> Callable:
    def seed(source_run, target):
        original(source_run, target)
        game = target / "game"
        (game / "design").mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_run / "design.md", game / "design" / "design.md")
        shutil.copytree(source_run / "game" / "docs", game / "docs", dirs_exist_ok=True)
    return seed


def post_compaction(run: Path, build: str, position: int, target: Path) -> World:
    """The transcript a compaction at `position` was about to act on, with the files as they stood.

    play and check_syntax answer instantly during the replay: neither writes a game file."""
    t0 = time.time()
    original, seed = replay._tools_for, replay._seed_vendor_as_it_was
    replay._tools_for = _stubbed_tools(original)
    replay._seed_vendor_as_it_was = _seed_with_design(seed)
    try:
        world = replay.run_to_position(run, position, target, before_compaction=True, build=build)
    finally:
        replay._tools_for, replay._seed_vendor_as_it_was = original, seed
    if world.gaps:
        raise ValueError(f"{run.name}@{position} sits after unarchived compactions {world.gaps}")
    return World(target, run, build, world.system, world.messages, position, time.time() - t0)


@dataclass
class Result:
    world: World
    arm: str
    turns: List[branch.TurnRecord] = field(default_factory=list)
    direct_calls: int = 0
    refused: int = 0
    stopped: str = ""


def step(world: World, workdir: Path, k: int, arm: str,
         prefix: Optional[Callable] = None, reasoning: Optional[str] = None,
         install: Optional[Callable] = None, restore: Optional[Callable] = None) -> Result:
    """Copy the world, then take k real turns through build_steps.step."""
    from maestro.codegen import build_state, build_steps

    target = workdir
    shutil.copytree(world.dir, target)
    spec = json.loads((target / "spec.json").read_text(encoding="utf-8"))
    tools = replay._tools_for(target, world.build, world.source_run)
    history = [dict(m) for m in world.messages]
    if prefix is not None:
        history = prefix(history, tools, target)
    cursor = build_state.BuildCursor(build_id="branch", started=True, turn=world.turn,
                                     system=world.system, history=history, logged=len(history))
    out = Result(world, arm)
    was = install() if install else None
    try:
        _turns(out, spec, target, tools, cursor, k, world, arm, reasoning)
    finally:
        if restore:
            restore(was)
    (target / "transcript.json").write_text(json.dumps(cursor.history, indent=1), encoding="utf-8")
    return out


def _turns(out, spec, target, tools, cursor, k, world, arm, reasoning) -> None:
    from maestro.codegen import build_steps

    outcome = build_steps.step(spec, target, tools, cursor, None)
    for _ in range(k):
        if isinstance(outcome, build_steps.Done):
            out.stopped = outcome.report
            break
        t0 = time.time()
        result = branch._infer_once(outcome, world.system, reasoning)
        before = len(cursor.history)
        outcome = build_steps.step(spec, target, tools, cursor, result)
        program = branch._program_of(cursor, cursor.turn)
        direct = sum(1 for m in cursor.history[before:]
                     if m.get("role") == "tool" and NO_CODE in str(m.get("content")))
        out.direct_calls += direct
        out.refused += sum(1 for m in cursor.history[before:]
                           if m.get("role") == "tool" and NOTHING_RAN in str(m.get("content")))
        usage = (result or {}).get("usage") or {}
        out.turns.append(branch.TurnRecord(
            turn=cursor.turn, reads=branch.READ.findall(program), repeat_reads=[],
            tools_called=branch._tools_of(program) + (["DIRECT"] if direct else []),
            generated=usage.get("completion_tokens") or 0,
            prompt_tokens=usage.get("prompt_tokens") or 0,
            compacted=cursor.compacted, seconds=time.time() - t0,
            error=(result or {}).get("error")))
        t = out.turns[-1]
        print(f"  {arm} turn {t.turn:3} gen={t.generated:6} prompt={t.prompt_tokens:6} "
              f"cuts={t.compacted} {t.seconds:5.1f}s {','.join(t.tools_called)}"
              + (f"  ERROR {t.error}" if t.error else ""), flush=True)
