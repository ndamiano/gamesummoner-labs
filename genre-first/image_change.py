"""The image-in-the-input arm: restore the generic game into the run, then one `change` build
whose first user message carries the same text note the text-only control got (<label>/skin.md)
plus the mockup screenshot (<label>/mockup.png) as an image_url, attached where the build seeds
its history (build_steps._seed runs in this process for the first turn). Everything else is the
prod change path. Starts the GPU runner itself. Needs run.py up.
usage: image_change.py <label> [note.md] [tag]"""
import base64
import io
import shutil
import sys
import time
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen import build_chain, build_steps, snapshots
from maestro.codegen.staging import game_dir
from maestro.state import RunState

sys.path.insert(0, str(HERE))
from build import wait_and_record

LEAD = ("Here is a screenshot of what the finished game looks like; make the game look like this. "
        "The note below names everything in it.\n\n")
LEADS = {"skin.md": LEAD}


def attach(image_path, text):
    im = Image.open(image_path).convert("RGB")
    im.thumbnail((1024, 1024))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    url = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return [{"type": "text", "text": text}, {"type": "image_url", "image_url": {"url": url}}]


def main(label, note_name="skin.md", tag="image_change"):
    source = HERE / label
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    run_dir = RunState(run).run_dir
    note = (source / note_name).read_text(encoding="utf-8")
    gd = game_dir(run_dir)
    shutil.rmtree(gd)
    shutil.copytree(source / "generic", gd)
    snapshots.take(run_dir, "generic restored for the image arm")
    content = attach(source / "mockup.png", LEADS.get(note_name, "") + note)
    original = build_steps._seed

    def seeded(tools, cursor, rd):
        if cursor.kind == "change" and cursor.history:
            cursor.history[0]["content"] = content
            tiers.log("attached the mockup to the change note")
        return original(tools, cursor, rd)

    build_steps._seed = seeded
    services = tiers.Services(source)
    services.ensure()
    if build_chain.kickoff(run, kind="change", note=note) is None:
        raise SystemExit(f"the change would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        wait_and_record(source, run, services, began, tag)
    finally:
        services.stop()


if __name__ == "__main__":
    main(*sys.argv[1:])
