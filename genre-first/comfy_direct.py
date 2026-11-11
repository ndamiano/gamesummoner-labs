"""Render art.json straight through ComfyUI (prod's own per-kind workflow graphs, matte included)
and write the webp files into the run's game/assets and <label>/assets. No worker, no safety
verdict, no manifest: the person at the ceiling is the admission policy for this run.
usage: comfy_direct.py <label>"""
import json
import shutil
import sys
import time
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from maestro.codegen.assets import autocrop_image, compose_prompt, save_image
from maestro.codegen.staging import game_dir
from maestro.state import RunState
from tools.comfyui_tools import build_image_job
from tools.quilting import quilt_tile

COMFY = "http://localhost:5001/upstream/comfyui_auto"


def post(path, body):
    req = urllib.request.Request(COMFY + path, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())


def get(path):
    with urllib.request.urlopen(COMFY + path, timeout=600) as r:
        return r.read()


def render(prompt, kind):
    wf = build_image_job(prompt, kind)["workflow_override"]
    pid = post("/prompt", {"prompt": wf})["prompt_id"]
    began = time.time()
    while True:
        hist = json.loads(get(f"/history/{pid}")).get(pid)
        if hist and hist.get("outputs"):
            break
        if hist and hist.get("status", {}).get("status_str") == "error":
            raise RuntimeError(f"comfy error: {json.dumps(hist['status'])[:400]}")
        if time.time() - began > 600:
            raise TimeoutError(pid)
        time.sleep(2)
    img = next(o for out in hist["outputs"].values() for o in out.get("images", []))
    q = f"filename={img['filename']}&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}"
    return Image.open(BytesIO(get("/view?" + q))), round(time.time() - began, 1)


def main(label):
    source = HERE / label
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    assets_dir = game_dir(RunState(run).run_dir) / "assets"
    assets_dir.mkdir(exist_ok=True)
    keep = source / "assets"
    keep.mkdir(exist_ok=True)
    order = json.loads((HERE / "art.json").read_text(encoding="utf-8"))
    for a in order["assets"]:
        prompt = compose_prompt(a["subject"], order["style"], {"view": a["view"]} if a.get("view") else None)
        im, secs = render(prompt, a["kind"])
        if a["kind"] == "tile":
            im = quilt_tile(im)
        elif a["kind"] == "sprite":
            im = autocrop_image(im.convert("RGBA"))
        dst = assets_dir / f"{a['id']}.webp"
        save_image(im, dst)
        shutil.copy2(dst, keep / dst.name)
        tiers.log(f"{a['id']} ({a['kind']}): {im.size} in {secs}s, {dst.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1])
