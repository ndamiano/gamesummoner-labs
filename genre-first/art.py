"""Phase 2 by hand at the ceiling: the art direction is written by a person (art.json: one prompt
per asset, one style line; wire.txt: the HUD layout and how each asset is used), the pictures are
rendered through prod's comfy path (request_media, the same routing and matte the builder would
get), and the local model only wires them in with one `change` build that may change no rule.
`art` renders and waits, copying the pictures to <label>/assets/; `wire` runs the change build.
usage: art.py art|wire|all <label>"""
import json
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen import assets, build_chain
from maestro.codegen.staging import game_dir
from maestro.state import RunState
from tools.execution_context import run_scope

sys.path.insert(0, str(HERE))
from build import wait_and_record


def art(source):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    run_dir = RunState(run).run_dir
    order = json.loads((HERE / "art.json").read_text(encoding="utf-8"))
    services = tiers.Services(source)
    services.ensure()
    build_id = tiers.games.create_build(run, kind="design")
    tiers.games.build_started(build_id)
    began = time.time()
    try:
        with run_scope(run, build_id):
            for a in order["assets"]:
                details = {"view": a["view"]} if a.get("view") else None
                out = assets.request_media(run, run_dir, build_id, a["id"], a["subject"], order["style"],
                                           a["kind"], details)
                tiers.log(f"{a['id']}: {out}")
        while True:
            entries = {e["id"]: e for e in assets.read_manifest(run_dir)}
            waiting = [a["id"] for a in order["assets"] if a["id"] not in entries or not assets.landed(run, entries[a["id"]])]
            if not waiting:
                break
            if time.time() - began > 1800:
                raise SystemExit(f"still waiting on {waiting} after 30 min")
            services.ensure()
            time.sleep(15)
        tiers.games.build_finished(build_id, "succeeded", steps=len(order["assets"]))
    except BaseException:
        tiers.games.build_finished(build_id, "failed", steps=len(order["assets"]))
        raise
    finally:
        services.stop()
    dst = source / "assets"
    dst.mkdir(exist_ok=True)
    for a in order["assets"]:
        for f in (game_dir(run_dir) / "assets").glob(f"{a['id']}.*"):
            shutil.copy2(f, dst / f.name)
    tiers.log(f"{len(order['assets'])} assets landed in {round((time.time() - began) / 60)} min: {sorted(p.name for p in dst.iterdir())}")


def wire(source):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    order = json.loads((HERE / "art.json").read_text(encoding="utf-8"))
    listing = "\n".join(f"- assets/{a['id']}.webp: {a['subject']}" for a in order["assets"])
    note = (HERE / "wire.txt").read_text(encoding="utf-8").replace("{assets}", listing)
    (source / "wire.md").write_text(note, encoding="utf-8")
    shutil.copytree(game_dir(RunState(run).run_dir), source / "skinned", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git"))
    services = tiers.Services(source)
    services.ensure()
    if build_chain.kickoff(run, kind="change", note=note) is None:
        raise SystemExit(f"the change would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        wait_and_record(source, run, services, began, "wire")
    finally:
        services.stop()


if __name__ == "__main__":
    source = HERE / sys.argv[2]
    if sys.argv[1] in ("art", "all"):
        art(source)
    if sys.argv[1] in ("wire", "all"):
        wire(source)
