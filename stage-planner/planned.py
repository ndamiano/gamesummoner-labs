"""section-budget's stage pre-read, with the design sections packed into programs that fit the
runner's stdout cap. A prod Flash-Next design's §2 alone can pass 20,000 chars, and one program
printing every named section was cut off mid-section. Import before stage.install().

Two bets ride on stage.json flags: "carry" opens every stage after the first on the previous
stage's whole conversation instead of a fresh agent and a pre-read (B3), and "play_before_done"
refuses done() until the game was played after its last edit, twice at most per stage (B5)."""

import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path[:0] = [str(LAB.parents[1] / "labs" / "section-budget")]

import stage

SECTION = """design = open("design/design.md").read()
for start, end in {ranges}:
    print(design[start:end].rstrip())
    print()
"""


def section_range(design: str, start: str) -> tuple:
    i = design.index(start)
    if start.startswith("#"):
        level = len(start) - len(start.lstrip("#"))
        ends = [design.find("\n" + "#" * n + " ", i + 1) for n in range(1, level + 1)]
    else:
        ends = [design.find("\n**", i + 1), design.find("\n#", i + 1)]
    ends = [e for e in ends if e > 0]
    return i, min(ends) if ends else len(design)


def packed(design: str, starts: list, room: int = stage.ROOM) -> list:
    ranges = []
    for s in starts:
        if s in design:
            a, b = section_range(design, s)
            while a < b:
                ranges.append((a, min(b, a + room - 200)))
                a += room - 200
    out, cur, used = [], [], 0
    for a, b in ranges:
        if cur and used + (b - a) + 2 > room:
            out.append(cur)
            cur, used = [], 0
        cur.append((a, b))
        used += b - a + 2
    return out + ([cur] if cur else [])


def preread(tools, cursor, run_dir, n: int) -> None:
    from maestro.codegen import build_steps, code_map
    from maestro.codegen.build_state import BuildCursor
    from maestro.codegen.staging import game_dir, spec_path

    opts = stage.stage_of(run_dir) or {}
    arm = opts.get("stages", "stages")
    if opts.get("carry") and n > 1:
        before = previous_history(Path(run_dir).name, cursor.build_id)
        if before is not None:
            cursor.history = before + cursor.history
            return
    reads = stage.LAB / arm / f"{n}.reads"
    if not reads.exists():
        return
    starts = [s for s in reads.read_text(encoding="utf-8").splitlines() if s.strip()]
    starts += [s for s in opts.get("extra_reads", []) if s not in starts]
    design = spec_path(run_dir).read_text(encoding="utf-8")
    programs = [SECTION.format(ranges=repr(r)) for r in packed(design, starts)]
    if opts.get("files", True):
        programs += [stage._text("preread_files.txt", arm).format(pieces=repr(p))
                     for p in stage.pieces(run_dir, stage.source_files(run_dir, n, opts.get("files_cap"), arm))]
    nudge = cursor.history.pop()
    for i, code in enumerate(programs):
        tc = {"id": f"{build_steps._SEEDED}stage_{n}_{i}", "type": "function",
              "function": {"name": "python", "arguments": json.dumps({"code": code})}}
        scratch = BuildCursor(build_id=cursor.build_id, started=True)
        build_steps._apply(tools, scratch, tc, run_dir)
        if stage.CODE_MAP and i == len(programs) - 1:
            scratch.history[-1]["content"] += ("\n\n" + stage._text("codemap_head.txt", arm) + "\n"
                                               + code_map.render(game_dir(run_dir)))
        cursor.history += [{"role": "assistant", "content": "", "tool_calls": [tc]}] + scratch.history
    cursor.history.append(nudge)


def previous_history(run_id: str, build_id: str):
    from db.connection import platform_db
    with platform_db() as conn:
        row = conn.execute("SELECT cursor FROM builds WHERE game_id = ? AND id != ? AND cursor IS NOT NULL "
                           "ORDER BY queued_at DESC LIMIT 1", (run_id, build_id)).fetchone()
    return json.loads(row["cursor"]).get("history") if row else None


REFUSED = ("[done() was not accepted: the game has not been played since your last edit. Play "
           "this stage's done line, then call done().]")
_plays: dict = {}


def _apply_wrapper(original):
    def apply(tools, cursor, tc, run_dir):
        finished = original(tools, cursor, tc, run_dir)
        if not (stage.stage_of(run_dir) or {}).get("play_before_done"):
            return finished
        try:
            code = json.loads(tc["function"]["arguments"]).get("code", "")
        except (ValueError, KeyError, TypeError):
            code = ""
        s = _plays.setdefault(cursor.build_id, {"dirty": False, "refused": 0})
        writes = [m.end() for m in battery.WRITE.finditer(code)]
        if writes:
            s["dirty"] = code.rfind("play(") < writes[-1]
        elif "play(" in code:
            s["dirty"] = False
        if finished and s["dirty"] and s["refused"] < 2:
            s["refused"] += 1
            cursor.finished = False
            cursor.summary = None
            cursor.history[-1]["content"] = str(cursor.history[-1].get("content") or "") + "\n\n" + REFUSED
            return False
        return finished
    return apply


import battery
from maestro.codegen import build_steps

stage.preread = preread
build_steps._apply = _apply_wrapper(build_steps._apply)
