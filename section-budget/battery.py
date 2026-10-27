"""Run one stage again and again from one snapshot under several pre-read arms, interleaved, and
record each run's turn shape and our check. One JSON line per run in results.jsonl.

    venv/bin/python labs/section-budget/battery.py <source run> <snapshot ref> <stage it ended> <reps> <arm> ...

Arms: codemap (sections + §2 + code map), files (+ every source file), files89 (+ §8, §9).
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
sys.path[:0] = [str(REPO / "src"), str(LAB)]

import branch
import check
import stage

ARMS = {
    "codemap": {"files": False},
    "files": {"files": True},
    "files89": {"files": True, "extra_reads": ["# 8. DEBUG API", "# 9. TESTS"]},
}
OUT = LAB / "results.jsonl"
WRITE = re.compile(r"\b(write_file|edit_file|write_text)\(|open\([^)]*['\"][wa]")


def shape(rid: str) -> dict:
    recs = [json.loads(l) for l in (stage.RUNS / rid / "turns.jsonl").open()]
    last = max(i for i, r in enumerate(recs) if r["kind"] == "meta")
    turns = [r for r in recs[last:] if r["kind"] == "turn"]
    first_write = first_play = None
    lost = 0
    for t in turns:
        code = ""
        for c in (t.get("response") or {}).get("tool_calls") or []:
            try:
                code += json.loads(c["function"]["arguments"]).get("code", "")
            except (ValueError, AttributeError):
                pass
        if first_write is None and WRITE.search(code):
            first_write = t["turn"]
        if first_play is None and "play(" in code:
            first_play = t["turn"]
    for r in recs[last:]:
        for m in r.get("added") or []:
            if m.get("role") == "tool" and not str(m.get("tool_call_id", "")).startswith("call_seeded"):
                c = str(m.get("content"))
                if "Nothing ran" in c or "nothing in the program ran" in c or "carried no `code`" in c:
                    lost += 1
    from maestro.codegen import build_state
    cursor = build_state.load(rid)
    return {"turns": cursor.turn, "done": bool(cursor.finished), "first_write": first_write,
            "first_play": first_play, "lost": lost, "summary": (cursor.summary or "")[:300]}


def run(source: str, ref: str, n: int, arm: str, port: int) -> dict:
    rid = branch.branch(source, ref, n, ARMS[arm])
    t0 = time.time()
    subprocess.run([str(LAB / "run_stage.sh"), rid, "next"], cwd=REPO,
                   stdout=(stage.RUNS / rid / "stage.log").open("w"), stderr=subprocess.STDOUT)
    row = {"arm": arm, "stage": n + 1, "from": [source, ref], "seconds": round(time.time() - t0),
           **shape(rid), "check": check.check(rid, port)}
    with OUT.open("a") as f:
        f.write(json.dumps(row) + "\n")
    print(json.dumps({k: row[k] for k in ("arm", "turns", "done", "first_write", "first_play",
                                          "lost")} | {"run": rid, "sprite": row["check"].get("sprite")}),
          flush=True)
    return row


if __name__ == "__main__":
    source, ref, n, reps, arms = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5:]
    for i in range(reps):
        for arm in arms:
            run(source, ref, n, arm, 8890)
    print("battery done", flush=True)
