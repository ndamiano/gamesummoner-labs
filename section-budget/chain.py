"""A whole arm B game: stage 1 from the source design, then every later stage on the same files,
our check after each. A stage whose game will not boot, or throws on the page, is run again from
the snapshot before it (a new branched run) up to RETRIES times. One JSON line per stage in
chains.jsonl.

    STAGE_OPTS='{"files": true}' venv/bin/python labs/section-budget/chain.py <source run> <label> [first] [last]
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
sys.path[:0] = [str(REPO / "src"), str(LAB)]

import battery
import branch
import check
import stage

OUT = LAB / "chains.jsonl"
RETRIES = 2
LAST = 9


def latest(rid: str) -> str:
    return subprocess.run(["git", f"--git-dir={stage.RUNS / rid / 'game.git'}", "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()


def broken(c: dict, n: int, opts=None) -> bool:
    """Will not boot, throws on the page (after Enter on a title screen too), shows no Mittens
    from his stage on (a blank floor throws nothing), or E does not end the turn from the turn
    loop's stage on: arm B's stages 2 and 3 unless STAGE_OPTS names others."""
    opts = opts or {}
    if not c.get("boots") or c.get("errors"):
        return True
    if n >= opts.get("mittens_from", 2) and (c.get("sprite") or {}).get("orange", 0) < 100:
        return True
    turns = c.get("end_turn") or []
    return n >= opts.get("turns_from", 3) and len(turns) == 2 and turns[0] is not None and turns[1] == turns[0]


def record(label, n, rid, attempt, t0):
    row = {"label": label, "stage": n, "run": rid, "attempt": attempt,
           "seconds": round(time.time() - t0), **battery.shape(rid), "check": check.check(rid, 8891)}
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps({k: row[k] for k in ("label", "stage", "run", "attempt", "turns", "done",
                                          "first_write", "lost")} | {"check": row["check"]}),
          flush=True)
    return row


def main(source, label, first=1, last=None):
    opts = json.loads(os.environ.get("STAGE_OPTS") or "{}")
    last = last or opts.get("last", LAST)
    if first == 1:
        t0 = time.time()
        log = subprocess.run([str(LAB / "run_stage.sh"), source, label], cwd=REPO,
                             capture_output=True, text=True).stdout
        rid = next(l.split()[1] for l in log.splitlines() if l.startswith("run: "))
        record(label, 1, rid, 0, t0)
        first = 2
    else:
        rid = source
    for n in range(first, last + 1):
        before = latest(rid)
        prev = rid
        for attempt in range(RETRIES + 1):
            cur = rid if attempt == 0 else branch.branch(prev, before, n - 1, opts)
            t0 = time.time()
            subprocess.run([str(LAB / "run_stage.sh"), cur, "next"], cwd=REPO,
                           stdout=(stage.RUNS / cur / f"stage{n}.log").open("w"),
                           stderr=subprocess.STDOUT)
            row = record(label, n, cur, attempt, t0)
            if not broken(row["check"], n, opts) or attempt == RETRIES:
                rid = cur
                break
    print(f"chain done {label} {rid}", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(a[0], a[1], int(a[2]) if len(a) > 2 else 1, int(a[3]) if len(a) > 3 else None)
