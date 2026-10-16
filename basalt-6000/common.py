"""Shared helpers for the box tests: start and stop a Basalt server from a config, and stream one chat request."""
import json, os, subprocess, sys, time, urllib.request

W = "/opt/dlami/nvme/w"
BASE = "http://127.0.0.1:8210"
PACKS = {"q4": f"{W}/model/Qwen3.8-FN-UD-Q4_K_XL-bf16key.basalt",
         "q4mtp": f"{W}/model/Qwen3.8-FN-UD-Q4_K_XL-bf16key-mtptuned.basalt"}


def config(model, **engine):
    e = {"expert-cache": "auto", "prefill": "auto", "spec": 7, "spec-min-p": 0.5, "max-context": 131072, "kv": "int8",
         "vram-reserve-mib": 700, "resident-experts": True}
    e.update(engine)
    return {"server": {"model": model, "alias": "m", "host": "127.0.0.1", "port": 8210, "vision": "dynamic",
                       "parallel": 1}, "engine": e}


def start(cfg, tag):
    path = f"{W}/cfg-{tag}.json"
    json.dump(cfg, open(path, "w"))
    log = open(f"{W}/server-{tag}.log", "w")
    t0 = time.time()
    proc = subprocess.Popen([f"{W}/basalt/bin/basalt", "serve", "--config", path], stdout=log, stderr=subprocess.STDOUT,
                            start_new_session=True)
    while True:
        if proc.poll() is not None:
            sys.exit(f"basalt exited {proc.returncode}; see {W}/server-{tag}.log")
        try:
            if urllib.request.urlopen(BASE + "/health", timeout=2).status == 200: break
        except Exception: pass
        time.sleep(0.2)
    urllib.request.urlopen(urllib.request.Request(BASE + "/load", data=b"{}", headers={"Content-Type": "application/json"}),
                           timeout=1800).read()
    print(f"  up in {time.time() - t0:.1f} s", flush=True)
    return proc


def stop(proc):
    subprocess.run(["pkill", "-TERM", "-g", str(proc.pid)])
    try: proc.wait(60)
    except Exception: subprocess.run(["pkill", "-KILL", "-g", str(proc.pid)])


def post(body, timeout=3600):
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


def stream(body):
    """Returns (prompt tokens, completion tokens, time to first token, decode tok/s, text)."""
    b = dict(body, stream=True, stream_options={"include_usage": True})
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; usage = {}; text = []
    with urllib.request.urlopen(req, timeout=3600) as r:
        for line in r:
            line = line.strip()
            if not line.startswith(b"data:") or line == b"data: [DONE]":
                continue
            d = json.loads(line[5:])
            if d.get("usage"):
                usage = d["usage"]
            for c in d.get("choices") or []:
                delta = c.get("delta") or {}
                piece = delta.get("content") or delta.get("reasoning_content")
                if piece:
                    first = first or time.time()
                    if delta.get("content"): text.append(delta["content"])
    end = time.time(); first = first or end
    ct = usage.get("completion_tokens", 0)
    return usage.get("prompt_tokens", 0), ct, first - t0, ct / (end - first) if end > first else 0, "".join(text)
