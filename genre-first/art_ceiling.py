"""The art at the ceiling of what is on this box: Qwen-Image 2512 paints one key art, then
Qwen-Image-Edit 2511 draws every asset with that key art as its style reference (a white canvas
seeds the latent, the key art conditions the text encoder), BiRefNet cuts the sprites out, tiles
are quilted seamless. Uses worldclaw's ImageModel client against the llama-swap ComfyUI. Writes
<label>/assets_ceiling/ and, with --install, the run's game/assets.
usage: art_ceiling.py <label> [--install]"""
import json
import shutil
import sys
import time
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
sys.path.insert(0, str(HERE.parent / "worldclaw"))
import tiers
from maestro.codegen.assets import autocrop_image, save_image
from maestro.codegen.staging import game_dir
from maestro.state import RunState
from tools.quilting import quilt_tile
from worldclaw.backends.images import ImageModel

COMFY = "http://localhost:5001/upstream/comfyui_auto"
NEGATIVE = "photo, realistic, 3d render, blurry, text, watermark, signature, gradient background, shadow on background, multiple subjects"
SPRITE = ("Using the exact art style, line weight, palette and shading of the reference illustration, draw {subject}. "
          "One subject only, whole and centered, large in the frame, {view} view, on a plain pure white background with nothing else.")
TILE = ("Using the exact art style and palette of the reference illustration, paint {subject}. "
        "The texture fills the whole frame edge to edge, flat and even, no objects, no border, no vignette.")


def main(label, install):
    source = HERE / label
    order = json.loads((HERE / "art.json").read_text(encoding="utf-8"))
    out = source / "assets_ceiling"
    out.mkdir(exist_ok=True)
    model = ImageModel(COMFY)
    key = out / "title_art.png"
    began = time.time()
    if not key.exists():
        art = next(a for a in order["assets"] if a["id"] == "title_art")
        model.generate(order["style"] + ". " + art["subject"] + ". Wide illustration, one consistent cartoon style, "
                       "every character and object drawn with the same line weight and flat shading.",
                       key, negative=NEGATIVE, width=1344, height=768, steps=30, seed=7)
        tiers.log(f"key art in {time.time() - began:.0f}s")
    canvas = out / "_canvas.png"
    Image.new("RGB", (1024, 1024), "white").save(canvas)
    for a in order["assets"]:
        if a["id"] == "title_art":
            continue
        dst = out / f"{a['id']}.png"
        if dst.exists():
            continue
        t0 = time.time()
        if a["kind"] == "tile":
            model.edit(TILE.format(subject=a["subject"]), [canvas, key], dst, negative=NEGATIVE, seed=3)
            im = quilt_tile(Image.open(dst).convert("RGB"))
        else:
            model.edit(SPRITE.format(subject=a["subject"], view=a.get("view", "three-quarter")), [canvas, key], dst,
                       negative=NEGATIVE, seed=3, cutout=True)
            im = autocrop_image(Image.open(dst).convert("RGBA"))
        im.save(dst)
        tiers.log(f"{a['id']} ({a['kind']}): {im.size} in {time.time() - t0:.0f}s")
    tiers.log(f"all in {(time.time() - began) / 60:.0f} min")
    if install:
        run = (source / "run.txt").read_text(encoding="utf-8").strip()
        assets_dir = game_dir(RunState(run).run_dir) / "assets"
        assets_dir.mkdir(exist_ok=True)
        for a in order["assets"]:
            im = Image.open(out / f"{a['id']}.png")
            save_image(im, assets_dir / f"{a['id']}.webp")
        tiers.log(f"installed {len(order['assets'])} into {assets_dir}")


if __name__ == "__main__":
    main(sys.argv[1], "--install" in sys.argv)
