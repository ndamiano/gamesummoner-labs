"""One subject through a ComfyUI TRELLIS.2 graph at trellis_server's prod settings, then the game's
decimate.mjs on the result. usage: run.py <subject.png> [seed]  (ComfyUI from launch.sh on :8288)"""
import json, shutil, subprocess, sys, time, urllib.request
from pathlib import Path

API = "http://localhost:8288"
HERE = Path(__file__).parent
OUT = HERE / "out"
COMFY = Path.home() / "comfy/ComfyUI-0.34"
RUNTIME = Path.home() / "Documents/ai-agent-test/runtime"
TEXTURE = 1024
DECIMATION = 50000


def graph(image, seed):
    g = {
        "u": {"class_type": "UNETLoader", "inputs": {"unet_name": "trellis_2_bf16.safetensors", "weight_dtype": "default"}},
        "cv": {"class_type": "CLIPVisionLoader", "inputs": {"clip_name": "dino_v3_vit_l.safetensors"}},
        "vs": {"class_type": "VAELoader", "inputs": {"vae_name": "trellis_2_shape_vae_bf16.safetensors"}},
        "vt": {"class_type": "VAELoader", "inputs": {"vae_name": "trellis_2_texture_vae_bf16.safetensors"}},
        "li": {"class_type": "LoadImage", "inputs": {"image": image}},
        "im": {"class_type": "InvertMask", "inputs": {"mask": ["li", 1]}},
        "crop": {"class_type": "ImageCropToMask", "inputs": {"images": ["li", 0], "masks": ["im", 0], "width": 1024, "height": 1024, "pad_factor": 1.1, "grow_mask": 0, "background": "#000000"}},
        "cond": {"class_type": "Trellis2Conditioning", "inputs": {"clip_vision_model": ["cv", 0], "image": ["crop", 0]}},
        "co1": {"class_type": "CFGOverride", "inputs": {"model": ["u", 0], "cfg": 1, "start_percent": 0.667, "end_percent": 1}},
        "rc1": {"class_type": "RescaleCFG", "inputs": {"model": ["co1", 0], "multiplier": 0.7}},
        "ms": {"class_type": "ModelSamplingSD3", "inputs": {"model": ["rc1", 0], "shift": 5}},
        "co2": {"class_type": "CFGOverride", "inputs": {"model": ["u", 0], "cfg": 1, "start_percent": 0.769, "end_percent": 1}},
        "rc2": {"class_type": "RescaleCFG", "inputs": {"model": ["co2", 0], "multiplier": 0.5}},
        "el": {"class_type": "EmptyTrellis2LatentStructure", "inputs": {"batch_size": 1}},
        "ks1": {"class_type": "KSampler", "inputs": {"model": ["ms", 0], "positive": ["cond", 0], "negative": ["cond", 1], "latent_image": ["el", 0], "seed": seed, "steps": 12, "cfg": 7.5, "sampler_name": "euler", "scheduler": "normal", "denoise": 1}},
        "ds": {"class_type": "VaeDecodeStructureTrellis2", "inputs": {"samples": ["ks1", 0], "vae": ["vs", 0], "resolution": "32"}},
        "ss": {"class_type": "Trellis2ShapeStage", "inputs": {"positive": ["cond", 0], "negative": ["cond", 1], "voxel": ["ds", 0]}},
        "ks2": {"class_type": "KSampler", "inputs": {"model": ["rc2", 0], "positive": ["ss", 0], "negative": ["ss", 1], "latent_image": ["ss", 2], "seed": seed, "steps": 20, "cfg": 7.5, "sampler_name": "euler", "scheduler": "normal", "denoise": 1}},
        "dsh": {"class_type": "VaeDecodeShapeTrellis", "inputs": {"samples": ["ks2", 0], "vae": ["vs", 0]}},
        "ts": {"class_type": "Trellis2TextureStage", "inputs": {"positive": ["ss", 0], "negative": ["ss", 1], "shape_latent": ["ks2", 0]}},
        "ks4": {"class_type": "KSampler", "inputs": {"model": ["u", 0], "positive": ["ts", 0], "negative": ["ts", 1], "latent_image": ["ts", 2], "seed": seed, "steps": 12, "cfg": 1, "sampler_name": "euler", "scheduler": "normal", "denoise": 1}},
        "dtx": {"class_type": "VaeDecodeTextureTrellis", "inputs": {"samples": ["ks4", 0], "vae": ["vt", 0], "shape_subdivides": ["dsh", 1]}},
        "fh": {"class_type": "FillHoles", "inputs": {"mesh": ["dsh", 0], "max_perimeter": 0.03, "weld_epsilon_rel": 1e-05, "max_vertices": 16, "fill_chains": False}},
        "rm": {"class_type": "RemeshMesh", "inputs": {"mesh": ["fh", 0], "resolution": 512, "sign_mode": "udf", "sign_mode.qef": False, "sign_mode.drop_inverted_components": False, "sign_mode.drop_enclosed_components": False, "band": 1.0, "project_back": 0.0, "fix_poles": False, "smooth_iters": 0, "drop_small_components": 0.01, "precluster_max_verts": 20_000_000}},
        "dec": {"class_type": "DecimateMesh", "inputs": {"mesh": ["rm", 0], "target_face_count": DECIMATION, "placement_mode": "midpoint"}},
        "uw": {"class_type": "UnwrapMesh", "inputs": {"mesh": ["dec", 0], "segmenter": "pec", "resolution": TEXTURE, "padding": 1, "weld_distance": 0.0002}},
        "sn": {"class_type": "MeshSmoothNormals", "inputs": {"mesh": ["uw", 0], "crease_angle": 180}},
        "bk": {"class_type": "BakeTextureFromVoxel", "inputs": {"mesh": ["sn", 0], "voxel_colors": ["dtx", 0], "texture_size": TEXTURE, "reference_mesh": ["dsh", 0]}},
        "ap": {"class_type": "ApplyTextureToMesh", "inputs": {"mesh": ["sn", 0], "base_color": ["bk", 0], "metallic": ["bk", 1], "roughness": ["bk", 2]}},
        "save": {"class_type": "SaveGLB", "inputs": {"mesh": ["ap", 0], "filename_prefix": "trellis-comfy/run"}},
    }
    return g


def submit(g):
    req = urllib.request.Request(API + "/prompt", json.dumps({"prompt": g}).encode(), {"Content-Type": "application/json"})
    try:
        pid = json.load(urllib.request.urlopen(req))["prompt_id"]
    except urllib.error.HTTPError as e:
        sys.exit(f"rejected: {e.read().decode()[:2000]}")
    t0 = time.time()
    while True:
        h = json.load(urllib.request.urlopen(f"{API}/history/{pid}"))
        if pid in h:
            return h[pid], round(time.time() - t0, 1)
        time.sleep(0.5)


def main():
    subject, seed = Path(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 42
    OUT.mkdir(exist_ok=True)
    if subject.resolve() != (COMFY / "input" / subject.name).resolve():
        shutil.copy(subject, COMFY / "input" / subject.name)
    row = {"subject": subject.stem, "seed": seed}
    for leg, s in (("cold", seed), ("warm", seed + 1)):
        h, secs = submit(graph(subject.name, s))
        row[f"{leg}_s"], row["status"] = secs, h["status"]["status_str"]
        if leg == "cold":
            first = h
        if row["status"] != "success":
            row["err"] = str(h["status"].get("messages"))[-1500:]
            break
    if row["status"] == "success":
        files = [f for o in first["outputs"].values() for v in o.values() if isinstance(v, list) for f in v]
        glb = next(f for f in files if isinstance(f, dict) and f.get("filename", "").endswith(".glb"))
        raw = OUT / f"{subject.stem}.comfy.glb"
        shutil.copy(COMFY / "output" / glb.get("subfolder", "") / glb["filename"], raw)
        dec = OUT / f"{subject.stem}.comfy.dec.glb"
        p = subprocess.run(["node", str(RUNTIME / "decimate.mjs"), str(raw), str(dec), "20000"],
                           capture_output=True, text=True, cwd=RUNTIME)
        row.update(glb=str(raw), raw_mb=round(raw.stat().st_size / 1e6, 2),
                   decimate_rc=p.returncode, decimate_out=(p.stdout + p.stderr).strip()[-400:])
    print(json.dumps(row, indent=1))
    (OUT / f"{subject.stem}.{seed}.json").write_text(json.dumps(row, indent=1))


if __name__ == "__main__":
    main()
