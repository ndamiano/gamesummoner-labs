"""Sends a built game one change note the way the site does (a `change` build with the note as
typed), waits for it, then runs the probe and keeps a copy of the game. Starts the GPU runner itself.
Needs run.py up.
usage: change.py <run id> <label> <note>"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tiers
from maestro.codegen import build_chain, snapshots
from maestro.state import RunState


def main():
    run, label, note = sys.argv[1], sys.argv[2], sys.argv[3]
    run_dir = RunState(run).run_dir
    out = tiers.HERE / run
    services = tiers.Services(out)
    services.ensure()
    tiers.log(f"{label}: change note on {run}: {note!r}, snapshot head {snapshots.head(run_dir)}")
    if build_chain.kickoff(run, kind="change", note=note) is None:
        raise SystemExit(f"the change would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        status = tiers.wait(run, services)
        report = tiers.probe(run_dir, 4)
        entry = {"note": note, "status": status, "minutes": round((time.time() - began) / 60), "probe": report,
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
