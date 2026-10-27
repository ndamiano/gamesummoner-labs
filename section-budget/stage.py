"""Arm B, playable stages: a stage build's system prompt asks for the stage instead of the whole
game, it is told its turns left after every program, and no gate runs between stages. Only runs whose directory lives under RUNS are touched, so lab and stock
builds can share one control plane."""

import json
from pathlib import Path

LAB = Path(__file__).resolve().parent
RUNS = Path("/var/tmp/section-budget/runs")
BUDGET = 25
LAST = 3
CODE_MAP = True
TEXT = {".js", ".mjs", ".html", ".css", ".json"}
ROOM = 18_000


def _text(name: str, arm: str = "stages") -> str:
    return (LAB / arm / name).read_text(encoding="utf-8").strip()


def stage_of(run_dir):
    if not Path(run_dir).resolve().is_relative_to(RUNS):
        return None
    p = Path(run_dir) / "stage.json"
    return json.loads(p.read_text()) if p.exists() else None


def request(ask: str, n: int, budget: int = BUDGET, arm: str = "stages") -> str:
    stage, done = [s.strip() for s in _text(f"{n}.txt", arm).split("\n---\n")]
    carry = "\n" + _text("carry.txt", arm).format(prev=n - 1) + "\n" if n > 1 else ""
    return _text("frame.txt", arm).format(ask=ask, carry=carry, n=n, stage=stage[0].upper() + stage[1:],
                                     done=done[0].upper() + done[1:], budget=budget)


def system() -> str:
    """build.txt with its opening paragraph (the whole game, by tier) swapped for the stage one."""
    from maestro.codegen import build_steps
    build = (build_steps._PROMPTS / "build.txt").read_text(encoding="utf-8")
    return _text("system_intro.txt") + "\n\n" + build.split("\n\n", 1)[1]


def source_files(run_dir, n: int, cap=None, arm: str = "stages") -> list:
    """Every text file the game wrote itself, then the platform files this stage names
    (stages/<n>.files). Past `cap` chars of the game's own files, only those the stage names."""
    from maestro.codegen.staging import game_dir, is_vendored
    root = game_dir(run_dir)
    own = sorted(str(p.relative_to(root)) for p in root.rglob("*")
                 if p.is_file() and p.suffix in TEXT and not is_vendored(p, root))
    extra = LAB / arm / f"{n}.files"
    named = [s.strip() for s in extra.read_text().splitlines() if s.strip()] if extra.exists() else []
    if cap and sum(len((root / f).read_text(encoding="utf-8")) for f in own) > cap:
        own = [f for f in own if f in named]
    return own + [f for f in named if f not in own and (root / f).exists()]


def pieces(run_dir, files, room: int = ROOM) -> list:
    """The files as (path, start, end) slices packed into programs whose output fits the runner's
    stdout cap."""
    from maestro.codegen.staging import game_dir
    root = game_dir(run_dir)
    out, cur, used = [], [], 0
    for f in files:
        size = len((root / f).read_text(encoding="utf-8"))
        start = 0
        while start < size:
            take = min(size - start, room - used - 100)
            if take <= 0:
                out.append(cur)
                cur, used = [], 0
                continue
            cur.append((f, start, start + take))
            used += take + 100
            start += take
    return out + ([cur] if cur else [])


def preread(tools, cursor, run_dir, n: int) -> None:
    """More seeded rounds before the nudge: a program that prints the design sections this stage
    names (stages/<n>.reads), then programs that print every source file of the game, run for real
    and pinned with the other seeds; the last result is followed by the code map."""
    from maestro.codegen import build_steps
    from maestro.codegen.build_state import BuildCursor

    opts = stage_of(run_dir) or {}
    arm = opts.get("stages", "stages")
    reads = LAB / arm / f"{n}.reads"
    if not reads.exists():
        return
    starts = [s for s in reads.read_text(encoding="utf-8").splitlines() if s.strip()]
    starts += [s for s in opts.get("extra_reads", []) if s not in starts]
    programs = [_text("preread.txt", arm).format(starts=repr(starts))]
    if opts.get("files", True):
        programs += [_text("preread_files.txt", arm).format(pieces=repr(p))
                     for p in pieces(run_dir, source_files(run_dir, n, opts.get("files_cap"), arm))]
    nudge = cursor.history.pop()
    for i, code in enumerate(programs):
        tc = {"id": f"{build_steps._SEEDED}stage_{n}_{i}", "type": "function",
              "function": {"name": "python", "arguments": json.dumps({"code": code})}}
        scratch = BuildCursor(build_id=cursor.build_id, started=True)
        build_steps._apply(tools, scratch, tc, run_dir)
        if CODE_MAP and i == len(programs) - 1:
            from maestro.codegen import code_map
            from maestro.codegen.staging import game_dir
            scratch.history[-1]["content"] += ("\n\n" + _text("codemap_head.txt", arm) + "\n"
                                               + code_map.render(game_dir(run_dir)))
        cursor.history += [{"role": "assistant", "content": "", "tool_calls": [tc]}] + scratch.history
    cursor.history.append(nudge)


def install():
    from maestro.codegen import build_chain, build_steps

    saved = (build_steps.step, build_steps._apply, build_chain._post_finalize)
    original_step, original_apply, original_post = saved

    def step(model, spec, run_dir, tools, cursor, result, error=None):
        fresh = not cursor.started
        out = original_step(model, spec, run_dir, tools, cursor, result, error=error)
        stage = stage_of(run_dir) if fresh else None
        if stage:
            cursor.system = system()
            preread(tools, cursor, run_dir, stage["n"])
            out = build_steps._infer(run_dir, cursor, build_steps._n_ctx(model))
        return out

    def apply(tools, cursor, tc, run_dir):
        out = original_apply(tools, cursor, tc, run_dir)
        stage = stage_of(run_dir)
        if stage and cursor.turn >= 1 and cursor.history and cursor.history[-1]["role"] == "tool":
            if stage.get("countdown", True):
                left = cursor.max_steps - cursor.turn
                line = _text("left_last.txt" if left <= LAST else "left.txt",
                             stage.get("stages", "stages")).format(
                    left=left, n=stage["n"])
                cursor.history[-1]["content"] += "\n\n" + line
        return out

    def post_finalize(run_id, build_id):
        from maestro.state import RunState
        if stage_of(RunState(run_id).run_dir):
            return build_chain._settle(run_id, build_id)
        return original_post(run_id, build_id)

    build_steps.step, build_steps._apply, build_chain._post_finalize = step, apply, post_finalize
    return saved


def restore(saved) -> None:
    from maestro.codegen import build_chain, build_steps
    build_steps.step, build_steps._apply, build_chain._post_finalize = saved
