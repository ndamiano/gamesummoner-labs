"""Qwen-Image 2.1 Turbo edit: each mannequin frame (image1) re-skinned as the sheet character (image2), optionally
anchored to the first output (image3), optionally sampled from the noised mannequin latent instead of an empty one.
usage: edit.py IN_DIR OUT_DIR [--seed N] [--start SIGMA] [--anchor] [--frames 0,4,6] [--ref IMG] [--prompt TXT] [--extra IMG TXT]   (comfy = mess-with-comfy on :8189)"""
import argparse, json, time, uuid
from pathlib import Path
import requests
from PIL import Image

URL = "http://localhost:8189"
HERE = Path(__file__).parent
TURBO = [1.0, 0.978453, 0.95418, 0.926626, 0.89508, 0.845148, 0.704534, 0.414568, 0.0]

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--start", type=float, default=1.0)
ap.add_argument("--anchor", action="store_true")
ap.add_argument("--frames")
ap.add_argument("--ref", default="character.jpeg")
ap.add_argument("--prompt", default="prompt.txt")
ap.add_argument("--extra", nargs=2, metavar=("IMG", "TXT"), help="fixed image3 reference and the prompt line that names it")
a = ap.parse_args()
IN, OUT = Path(a.inp), Path(a.out); OUT.mkdir(parents=True, exist_ok=True)
PROMPT = (HERE / a.prompt).read_text().strip()
ANCHOR = (HERE / "prompt_anchor.txt").read_text().strip()
WF = json.loads((Path.home() / "comfy/mess-with-comfy/user/default/workflows/qwen-2.1-turbo-edit.json").read_text())


def upload(path, name):
    r = requests.post(f"{URL}/upload/image", files={"image": (name, path.read_bytes(), "image/png")}, data={"overwrite": "true"})
    r.raise_for_status()


def run(frame, anchor=None):
    wf = json.loads(json.dumps(WF))
    wf["12"]["inputs"]["image"] = frame
    wf["13"]["inputs"]["image"] = "anim_sheet_ref.png"
    wf["4"]["inputs"]["prompt"] = PROMPT
    if anchor:
        wf["16"] = {"class_type": "LoadImage", "inputs": {"image": anchor}}
        wf["4"]["inputs"]["images.image_3"] = ["16", 0]
        wf["4"]["inputs"]["prompt"] = PROMPT + " " + ANCHOR
    if a.extra:
        wf["16"] = {"class_type": "LoadImage", "inputs": {"image": "anim_extra.png"}}
        wf["4"]["inputs"]["images.image_3"] = ["16", 0]
        wf["4"]["inputs"]["prompt"] = PROMPT + " " + (HERE / a.extra[1]).read_text().strip()
    if a.start < 1.0:
        sig = [a.start] + [s for s in TURBO if s < a.start]
        wf["6"]["inputs"]["sigmas"] = ", ".join(f"{s:g}" for s in sig)
        wf["19"] = {"class_type": "ImageScale", "inputs": {"image": ["12", 0], "upscale_method": "lanczos", "crop": "disabled",
                                                          "width": 896, "height": 1184}}
        wf["20"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["19", 0], "vae": ["3", 0]}}
        wf["7"]["inputs"]["latent_image"] = ["20", 0]
    wf["15"]["inputs"]["noise_seed"] = a.seed
    wf["9"]["inputs"]["filename_prefix"] = "anim_i2i"
    pid = requests.post(f"{URL}/prompt", json={"prompt": wf, "client_id": str(uuid.uuid4())}).json()["prompt_id"]
    while True:
        h = requests.get(f"{URL}/history/{pid}").json()
        if pid in h:
            st = h[pid]["status"]
            if st.get("status_str") == "error":
                raise RuntimeError(json.dumps(st)[:2000])
            img = h[pid]["outputs"]["9"]["images"][0]
            return requests.get(f"{URL}/view", params=img).content
        time.sleep(1)


Image.open(HERE / a.ref).convert("RGB").save(OUT / "_ref.png")
upload(OUT / "_ref.png", "anim_sheet_ref.png")
if a.extra:
    upload(HERE / a.extra[0], "anim_extra.png")
frames = sorted(IN.glob("frame_*.png"))
if a.frames:
    frames = [frames[int(i)] for i in a.frames.split(",")]
for f in frames:
    if (OUT / f.name).exists():
        continue
    t = time.time()
    upload(f, f"anim_{f.name}")
    anchor = None
    if a.anchor and f != frames[0]:
        upload(OUT / frames[0].name, "anim_anchor.png")
        anchor = "anim_anchor.png"
    (OUT / f.name).write_bytes(run(f"anim_{f.name}", anchor))
    print(f.name, f"{time.time() - t:.1f}s", flush=True)

ims = [Image.open(OUT / f.name).convert("RGB") for f in frames]
w, h = ims[0].size
strip = Image.new("RGB", (w * len(ims), h), "white")
for i, im in enumerate(ims):
    strip.paste(im, (i * w, 0))
strip.save(OUT / "strip.png")
