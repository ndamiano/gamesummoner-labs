"""Aggregate decode throughput of Basalt at --batch N, on real build prompts through llama-swap.

For each N: set the server's `"parallel": N` in the Basalt config (none for 1; it splits
max-context between the slots, where engine `batch` gives each slot all of it), unload, then send N real build
conversations at once twice. Round 1 reads the prompts; round 2 is the measured one, each
conversation one user line longer, the way the next build turn arrives.

    python3 bench.py 1 2 4 8
"""

import concurrent.futures
import json
import shutil
import sys
import time
import urllib.request
from pathlib import Path

CONFIG = Path("/var/lib/models/basalt/basalt-iq3s.json")
BACKUP = Path("/var/tmp/open-shim/basalt-iq3s.json.bak")
SWAP = "http://127.0.0.1:5001"
MODEL = "qwen3.8-flash-next-basalt"
OUT = Path(__file__).resolve().parent / "results.jsonl"
SOURCES = ["42427fef48dd", "1629ea1ae380", "524b1c3efa1c", "d0dc7c41c2d0", "22263c0d3c8b",
           "3170a8a2b4c3", "632bb49dbb5b", "8fc1191a0c54"]
MAX_PROMPT_CHARS = 200_000
MAX_TOKENS = 2048

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from maestro.codegen.build_steps import SCHEMAS


def conversation(run: str):
    s = json.loads(Path(f"/home/nick/output/runs/{run}/build_state.json").read_text())
    history, size = [], 0
    for m in reversed(s["history"][1:]):
        size += len(json.dumps(m))
        if size > MAX_PROMPT_CHARS:
            break
        history.insert(0, m)
    while history and history[0].get("role") == "tool":
        history.pop(0)
    return [{"role": "system", "content": s["system"]}, s["history"][0]] + history


def post(path, body=None, timeout=1800):
    req = urllib.request.Request(SWAP + path, data=json.dumps(body).encode() if body else None,
                                 headers={"Content-Type": "application/json"},
                                 method="POST" if body else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read() or b"{}") if r.headers.get_content_type() == "application/json" else r.read()


def ask(messages):
    t0 = time.time()
    r = post("/v1/chat/completions", {"model": MODEL, "messages": messages, "tools": SCHEMAS,
                                      "temperature": 0.7, "max_tokens": MAX_TOKENS,
                                      "reasoning_effort": "xhigh"})
    u = r.get("usage") or {}
    return {"seconds": time.time() - t0, "completion": u.get("completion_tokens") or 0,
            "prompt": u.get("prompt_tokens") or 0}


def round_of(convs):
    t0 = time.time()
    with concurrent.futures.ThreadPoolExecutor(len(convs)) as pool:
        out = list(pool.map(ask, convs))
    return time.time() - t0, out


def configure(n: int):
    cfg = json.loads(BACKUP.read_text())
    if n > 1:
        cfg["server"]["parallel"] = n
    CONFIG.write_text(json.dumps(cfg, indent=2) + "\n")
    post("/unload")
    time.sleep(5)


def main(ns):
    convs = [conversation(r) for r in SOURCES]
    try:
        for n in ns:
            configure(n)
            t0 = time.time()
            post("/v1/chat/completions", {"model": MODEL, "messages": [{"role": "user", "content": "hi"}],
                                          "max_tokens": 1})
            load = time.time() - t0
            try:
                cache = post(f"/upstream/{MODEL}/metrics")["engine"]["expert_cache_mib"]
            except Exception:
                cache = None
            batch = convs[:max(n, 2)]
            if n == 1:
                cold = [ask(c) for c in batch]
                warm_convs = [c + [{"role": "user", "content": "Continue."}] for c in batch]
                t1 = time.time()
                warm = [ask(c) for c in warm_convs]
                wall = time.time() - t1
            else:
                _, cold = round_of(batch)
                wall, warm = round_of([c + [{"role": "user", "content": "Continue."}] for c in batch])
            gen = sum(w["completion"] for w in warm)
            row = {"parallel": n, "requests": len(batch), "load_seconds": round(load, 1), "expert_cache_mib": cache,
                   "wall_seconds": round(wall, 1), "completion_tokens": gen,
                   "aggregate_tok_s": round(gen / wall, 1),
                   "per_request_tok_s": [round(w["completion"] / w["seconds"], 1) for w in warm],
                   "prompt_tokens": [w["prompt"] for w in warm],
                   "cold_seconds": [round(c["seconds"], 1) for c in cold]}
            with OUT.open("a") as f:
                f.write(json.dumps(row) + "\n")
            print(json.dumps(row), flush=True)
    finally:
        shutil.copy2(BACKUP, CONFIG)
        post("/unload")


if __name__ == "__main__":
    main([int(a) for a in sys.argv[1:]])
