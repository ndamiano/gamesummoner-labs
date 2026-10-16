"""JEV System 1 decisions on top of a plain sglang server (copy of AI-Launcher/jev/decide.py; JEV_DIR picks the model).

sglang runs the backbone with the "jev-decision" LoRA and returns the final hidden state of the prompt; the decision
head is applied here: logits = h @ (W + B @ A)^T over the option tokens (readout.safetensors, from prep_adapter.py),
then JEV's per-slot bias and per-kind temperature, softmax over the options.

POST /v1/decide  {"kind": "noul"|"score"|"choice", "state": str|dict|list, "question": str, "options": [...]}
  state as a list mixes text and images: ["Photo: ", {"image": "data:...|https://...|/path.jpg"}, "\nMore text"]
  -> {"kind", "options", "probabilities", "choice_index", "choice", "elapsed_seconds"}
GET /health

Usage: python decide.py [--port 8101] [--sglang http://127.0.0.1:8100]
"""
import argparse
import json
import math
import os
import time
from pathlib import Path
from typing import Literal

import requests
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from safetensors.torch import load_file

JEV = Path(os.environ.get("JEV_DIR", "/var/lib/models/jev/JEV-27B-VL"))
LORA = "jev-decision"
IMAGE = "<|vision_start|><|image_pad|><|vision_end|>"
GROUP = 16  # the decision head was trained on choice labels A-P

HEAD = json.loads((JEV / "adapter_vllm" / "decision_head.json").read_text())
TEMPS = json.loads((JEV / "calibration.json").read_text())["per_kind"]
R = load_file(JEV / "readout.safetensors")
SLOT = {i: n for n, i in enumerate(R["ids"].tolist())}   # token id -> readout row
FIXED = {"noul": ["false", "true"], "score": [str(i) for i in range(6)]}
LABELS = "ABCDEFGHIJKLMNOP"

app = FastAPI()
SGLANG = "http://127.0.0.1:8100"


class Decide(BaseModel):
    kind: Literal["noul", "score", "choice"]
    state: str | dict | list = ""
    question: str
    options: list[str] | None = None


def render_state(state):
    """Prompt text for the state, with an image placeholder where each image goes, and the images in order."""
    if isinstance(state, str):
        return state, []
    if isinstance(state, dict):
        return json.dumps(state, ensure_ascii=False), []
    text, images = [], []
    for p in state:
        if isinstance(p, str):
            text.append(p)
        elif isinstance(p, dict) and "image" in p:
            text.append(IMAGE); images.append(p["image"])
        else:
            text.append(json.dumps(p, ensure_ascii=False))
    return "".join(text), images


def one_pass(kind, state_text, images, question, opts):
    """One System 1 read over <= 16 options; probabilities aligned with opts."""
    lo, _ = HEAD["slots"]["ranges"][kind]
    lines = opts if kind != "choice" else [f"{LABELS[i]}) {o}" for i, o in enumerate(opts)]
    prompt = (f"[kind] {kind}\n[state] {state_text}\n[question] {question}\n[options]\n" + "\n".join(lines)
              + "\n[decision]:")
    body = {"text": prompt, "lora_path": LORA, "return_hidden_states": "last",
            "sampling_params": {"max_new_tokens": 1, "temperature": 0}}
    if images:
        body["image_data"] = images
    r = requests.post(f"{SGLANG}/generate", json=body, timeout=600)
    if r.status_code != 200:
        raise HTTPException(502, f"sglang: {r.text[:500]}")
    hs = r.json()["meta_info"]["hidden_states"]
    h = torch.tensor(hs[-1] if isinstance(hs[0], list) else hs, dtype=torch.float32).reshape(-1)

    rows = [SLOT[t] for t in HEAD["verbalizer_ids"][lo: lo + len(opts)]]
    logits = R["weight"][rows] @ h + R["lora_b"][rows] @ (R["lora_a"] @ h)
    z = (logits + torch.tensor(HEAD["bias"][lo: lo + len(opts)])) / TEMPS[kind]
    return torch.softmax(z, 0).tolist()


def tournament(state_text, images, question, opts):
    """More than 16 options: score balanced groups of <= 16, then a final over the group winners plus the best
    runners-up (16 total). Finalists get their final probability scaled by how much group mass the final covers;
    the others get their in-group probability scaled by their group's share of the final. Then normalize."""
    n = len(opts)
    g = math.ceil(n / GROUP)
    groups, i = [], 0
    for j in range(g):
        size = n // g + (1 if j < n % g else 0)
        groups.append(list(range(i, i + size))); i += size
    p_group = {}
    for grp in groups:
        p_group.update(zip(grp, one_pass("choice", state_text, images, question, [opts[k] for k in grp])))
    winners = [max(grp, key=lambda k: p_group[k]) for grp in groups]
    rest = sorted((k for k in range(n) if k not in winners), key=lambda k: -p_group[k])
    final_ids = sorted(winners + rest[: GROUP - len(winners)])
    p_final = dict(zip(final_ids, one_pass("choice", state_text, images, question, [opts[k] for k in final_ids])))
    group_of = {k: gi for gi, grp in enumerate(groups) for k in grp}
    share, cover = [0.0] * g, [0.0] * g   # per group: final probability won, in-group mass of its finalists
    for k in final_ids:
        share[group_of[k]] += p_final[k]
        cover[group_of[k]] += p_group[k]
    among = sum(s * c for s, c in zip(share, cover))
    p = [p_final[k] * among if k in p_final else share[group_of[k]] * p_group[k] for k in range(n)]
    total = sum(p)
    return [x / total for x in p]


@app.post("/v1/decide")
def decide(req: Decide):
    t0 = time.time()
    if req.kind == "choice":
        opts = req.options or []
        if not 2 <= len(opts) <= 256:
            raise HTTPException(400, "choice needs 2-256 options")
    else:
        opts = FIXED[req.kind]
    state_text, images = render_state(req.state)
    if req.kind == "choice" and len(opts) > GROUP:
        probs = tournament(state_text, images, req.question, opts)
    else:
        probs = one_pass(req.kind, state_text, images, req.question, opts)
    best = max(range(len(opts)), key=lambda i: probs[i])
    return {"kind": req.kind, "options": opts, "probabilities": [round(p, 6) for p in probs],
            "choice_index": best, "choice": opts[best], "elapsed_seconds": round(time.time() - t0, 3)}


@app.get("/health")
def health():
    ok = requests.get(f"{SGLANG}/health", timeout=5).status_code == 200
    if not ok:
        raise HTTPException(503, "sglang not healthy")
    return {"status": "ok"}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8101)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--sglang", default=SGLANG)
    a = ap.parse_args()
    SGLANG = a.sglang
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")
