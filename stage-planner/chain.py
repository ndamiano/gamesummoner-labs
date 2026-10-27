"""One stage-planner game: plan the source run's design, build it stage by stage on the same files,
our check after each, then the prod gates on a copy. A stage whose game will not boot or throws on
the page is run again from the snapshot before it (stage 1: from the design) up to RETRIES times, and the chain goes on from
the best attempt (boots, then fewest page errors, then not missing, then the share of look inputs the
screen answered, then the latest). One JSON line per stage in
chains.jsonl.

    venv/bin/python labs/stage-planner/chain.py <source run id> <label> [--prompt plan_x.txt] [--budgets 20,20,...] [--opts '{"carry": true}']
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
SB = REPO / "labs" / "section-budget"
sys.path[:0] = [str(REPO / "src"), str(LAB), str(SB)]

import battery
import branch
import check
import gates
import plan
import stage

OUT = LAB / "chains.jsonl"
RETRIES = 2
RELOOK = False
TRACE = False
TELEPORT = False
EXTRA_READS = ["# 2. CONTRACTS", "# 8. DEBUG API", "# 9. TESTS"]


def latest(rid: str) -> str:
    return subprocess.run(["git", f"--git-dir={stage.RUNS / rid / 'game.git'}", "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()


def broken(c: dict) -> bool:
    return not c.get("boots") or bool(c.get("errors"))


def failed(row: dict) -> bool:
    """Broken, or a vision look (V3) went to where the stage should show and it was not there."""
    return broken(row["check"]) or (row.get("vision") or {}).get("verdict") == "missing"


def rank(row: dict) -> tuple:
    c = row["check"]
    vision = row.get("vision") or {}
    return (bool(c.get("boots")), -len(c.get("errors") or []),
            vision.get("verdict") != "missing", vision.get("responsive", 0.0), row["attempt"])


def record(label, n, rid, attempt, t0, vision_arm=None):
    row = {"label": label, "stage": n, "run": rid, "attempt": attempt,
           "seconds": round(time.time() - t0), **battery.shape(rid), "check": check.check(rid, 8891)}
    if vision_arm and not broken(row["check"]):
        import stage_look
        row["vision"] = stage_look.look(rid, stage_look.done_line(vision_arm, n),
                                        Path("/var/tmp/vision-build/looks") / label / f"{rid}-stage{n}",
                                        trace=TRACE, teleport=TELEPORT)
        if RELOOK and row["vision"].get("verdict") == "unclear":
            again = stage_look.look(rid, stage_look.done_line(vision_arm, n),
                                    Path("/var/tmp/vision-build/looks") / label / f"{rid}-stage{n}-relook",
                                    turns=2 * stage_look.TURNS, trace=TRACE, teleport=TELEPORT)
            row["vision"] = again if again.get("verdict") != "unclear" else \
                {**again, "verdict": "missing", "relooked": True}
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps({k: row[k] for k in ("label", "stage", "run", "attempt", "turns", "done",
                                          "first_write", "lost")}
                     | {"boots": row["check"].get("boots"), "errors": len(row["check"].get("errors") or [])}
                     | ({"vision": row["vision"]} if row.get("vision") else {})),
          flush=True)
    return row


def set_repair(rid: str, errors, key: str = "repair") -> None:
    p = stage.RUNS / rid / "stage.json"
    info = json.loads(p.read_text())
    info.pop(key, None)
    if errors:
        info[key] = errors
    p.write_text(json.dumps(info))


def run_stage(rid: str, arg: str, log: Path, script: str = "run_stage_b.sh") -> str:
    with log.open("w") as f:
        out = subprocess.run([str(LAB / script), rid, arg], cwd=REPO, stdout=subprocess.PIPE,
                             stderr=f, text=True).stdout
    log.open("a").write(out)
    return out


def main(source: str, label: str, prompt_file: str = "plan.txt", budgets=None, extra=None) -> None:
    arm = str(plan.PLANS / label)
    if not (Path(arm) / "1.txt").exists():
        plan.main(source, label, prompt_file)
    last = len([p for p in Path(arm).glob("*.txt") if p.stem.isdigit()])
    if budgets and len(budgets) != last:
        budgets = [budgets[min(i * len(budgets) // last, len(budgets) - 1)] for i in range(last)]
    os.environ["STAGE_OPTS"] = json.dumps({"stages": arm, "last": last, "extra_reads": EXTRA_READS,
                                           "files_cap": 100_000, **({"budgets": budgets} if budgets else {}),
                                           **(extra or {})})
    logs = LAB / "logs" / label
    logs.mkdir(parents=True, exist_ok=True)
    script = ("../vision-build/run_stage_v.sh" if (extra or {}).get("look") or (extra or {}).get("vision_check")
              else "run_stage_c.sh" if (extra or {}).get("repair_first") else "run_stage_b.sh")
    vision_arm = arm if (extra or {}).get("vision_check") else None
    global RELOOK, TRACE, TELEPORT
    RELOOK = bool((extra or {}).get("relook"))
    TELEPORT = bool((extra or {}).get("teleport"))
    TRACE = bool((extra or {}).get("trace"))
    if TRACE:
        script = "../vision-build/run_stage_vt.sh"
    if vision_arm:
        sys.path.insert(0, str(REPO / "labs" / "vision-build"))
    rows = []
    for attempt in range(RETRIES + 1):
        t0 = time.time()
        out = run_stage(source, label, logs / f"stage1.{attempt}.log", script)
        cur = next(l.split()[1] for l in out.splitlines() if l.startswith("run: "))
        rows.append(record(label, 1, cur, attempt, t0, vision_arm))
        if not failed(rows[-1]):
            break
    rid = max(rows, key=rank)["run"]
    repair_first = (extra or {}).get("repair_first")
    for n in range(2, last + 1):
        before = latest(rid)
        prev = rid
        base = max(rows, key=rank)["check"]
        errors = (base.get("errors") or ["the page does not boot"]) if repair_first and broken(base) else None
        kept = max(rows, key=rank)
        carried = [r["vision"]["why"] for r in rows if (r.get("vision") or {}).get("verdict") == "missing"] \
            if vision_arm and (kept.get("vision") or {}).get("verdict") != "shown" else []
        rows = []
        for attempt in range(RETRIES + 1):
            cur = rid if attempt == 0 else branch.branch(prev, before, n - 1, json.loads(os.environ["STAGE_OPTS"]))
            t0 = time.time()
            if repair_first:
                set_repair(cur, errors)
            if vision_arm:
                missed = [r["vision"]["why"] for r in rows if (r.get("vision") or {}).get("verdict") == "missing"]
                set_repair(cur, missed[-1:] or None, "seen_missing")
                import stage_look
                traced = [r["vision"] for r in rows if (r.get("vision") or {}).get("verdict") == "missing"
                          and r["vision"].get("trace")]
                set_repair(cur, [stage_look.trace_text(traced[-1]["trace"])] if traced else None, "seen_trace")
                set_repair(cur, carried[-1:] or None, "carry_missing")
            run_stage(cur, "next", logs / f"stage{n}.{attempt}.log", script)
            rows.append(record(label, n, cur, attempt, t0, vision_arm))
            if not failed(rows[-1]):
                break
        rid = max(rows, key=rank)["run"]
    print(f"chain done {label} {rid}", flush=True)
    gates.main(rid)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("label")
    ap.add_argument("--prompt", default="plan.txt")
    ap.add_argument("--budgets", type=lambda s: [int(x) for x in s.split(",")])
    ap.add_argument("--opts", type=json.loads)
    a = ap.parse_args()
    main(a.source, a.label, a.prompt, a.budgets, a.opts)
