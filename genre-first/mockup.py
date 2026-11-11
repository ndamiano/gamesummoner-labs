"""Mockup screenshots of the finished game, to show the builder as the target. Qwen-Image 2512
through the llama-swap ComfyUI, N seeds; a person picks one and copies it to <label>/mockup.png.
usage: mockup.py <label> [n]"""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "worldclaw"))
from worldclaw.backends.images import ImageModel

COMFY = "http://localhost:5001/upstream/comfyui_auto"
NEGATIVE = "photo, 3d render, blurry, watermark, realistic, dark, cluttered, tiny text"


def main(label, n):
    source = HERE / label
    prompt = (source / "mockup_prompt.txt").read_text(encoding="utf-8").strip()
    out = source / "mockups"
    out.mkdir(exist_ok=True)
    model = ImageModel(COMFY)
    for seed in range(n):
        t0 = time.time()
        dst = out / f"mockup_{seed}.png"
        model.generate(prompt, dst, negative=NEGATIVE, width=1280, height=720, steps=30, seed=100 + seed)
        print(f"{dst.name} in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 4)
