"""Full-build battery: for each source design, one control build (tests-in-files/build.sh, stock
path) and one arm build (fullbuild.sh) side by side on serve.py's control plane, fix builds
included; the next pair starts once both games have settled.

Run from the repo root with serve.py and local_gpu auto up:
    venv/bin/python labs/open-shim/battery_full.py <source run> ...
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parent.parent
OUT = Path("/var/tmp/open-shim/battery")
SETTLED_POLLS = 3

sys.path.insert(0, str(REPO / "src"))
from db import games


def settled(rid: str) -> bool:
    g = games.game(rid)
    return bool(g) and g.get("status") != "building"


def launch(script, source, label, log):
    return subprocess.Popen([str(script), source, label], stdout=log, stderr=subprocess.STDOUT,
                            cwd=REPO)


def run_id(log_path: Path) -> str:
    for _ in range(120):
        for line in log_path.read_text().splitlines():
            if line.startswith("run: "):
                return line.split()[1]
        time.sleep(2)
    raise RuntimeError(f"no run id in {log_path}")


def main(sources):
    OUT.mkdir(parents=True, exist_ok=True)
    index = OUT / "pairs.jsonl"
    for source in sources:
        logs = {arm: OUT / f"{source}-{arm}.log" for arm in ("ctrl", "arm")}
        procs = {
            "ctrl": launch(REPO / "labs/tests-in-files/build.sh", source, f"open-shim ctrl {source}",
                           logs["ctrl"].open("w")),
            "arm": launch(LAB / "fullbuild.sh", source, f"open-shim arm {source}",
                          logs["arm"].open("w")),
        }
        rids = {arm: run_id(log) for arm, log in logs.items()}
        print(f"{time.strftime('%H:%M')} pair {source}: ctrl {rids['ctrl']} arm {rids['arm']}",
              flush=True)
        for p in procs.values():
            p.wait()
        streak = 0
        while streak < SETTLED_POLLS:
            time.sleep(60)
            streak = streak + 1 if all(settled(r) for r in rids.values()) else 0
        with index.open("a") as f:
            f.write(json.dumps({"source": source, **rids, "settled_at": time.time()}) + "\n")
        print(f"{time.strftime('%H:%M')} pair {source} settled", flush=True)
    print("battery done", flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
