"""Hands what look.py found to a fix build, as one note (fix_note.txt), the way a gate hands over
its findings: every problem of every screenshot, unfiltered. Waits for the build, runs the tier-chain
probe and keeps a copy of the game. Starts the GPU runner itself. Needs run.py up.
usage: fix.py <run id> <label>"""
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen import build_chain, snapshots
from maestro.state import RunState

from look import STATES


def note(found):
    blocks = []
    for shot, answer in found.items():
        lines = [f"- [{p['kind']}] {p['where']}: {p['what']}" for p in answer.get("problems", [])]
        if lines:
            blocks.append(f"Screenshot: {STATES[shot]}\n" + "\n".join(lines))
    return (HERE / "fix_note.txt").read_text(encoding="utf-8").format(findings="\n\n".join(blocks)).strip() + "\n"


def main():
    run, label = sys.argv[1], sys.argv[2]
    run_dir = RunState(run).run_dir
    out = HERE / run
    text = note(json.loads((out / "found.json").read_text(encoding="utf-8")))
    (out / f"{label}-note.txt").write_text(text, encoding="utf-8")
    services = tiers.Services(out)
    services.ensure()
    tiers.log(f"{label}: fix note on {run}, {len(text)} chars, snapshot head {snapshots.head(run_dir)}")
    if build_chain.kickoff(run, kind="fix", note=text) is None:
        raise SystemExit(f"the fix would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        report = tiers.probe(run_dir, 4)
        entry = {"status": status, "minutes": round((time.time() - began) / 60), "probe": report,
                 **tiers.summary(run), "kept": tiers.keep(run_dir, label), "snapshot": snapshots.head(run_dir)}
        (out / f"{label}.json").write_text(json.dumps(entry, indent=1, ensure_ascii=False), encoding="utf-8")
        tiers.log(f"{label}: ended {status} after {entry['minutes']} min")
        for name in sorted(k for k in report if k.startswith("tier ")):
            tiers.log(f"{label} probe, {name}: " + ", ".join(
                f"{'PASS' if c['ok'] else 'FAIL'} {check}" for check, c in report[name].items()))
    finally:
        services.stop()


if __name__ == "__main__":
    main()
