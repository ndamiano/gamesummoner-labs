"""Basalt UD-Q4_K_XL on one RTX PRO 6000: startup, ~30k prompt read, decode, then N concurrent streams.

usage: bench.py PARALLEL [SPEC]
"""
import json, os, subprocess, sys, threading, time, urllib.request

W = "/opt/dlami/nvme/w"
BASALT = os.environ.get("BASALT", f"{W}/basalt")
N = int(sys.argv[1])
SPEC = int(sys.argv[2]) if len(sys.argv) > 2 else 7
BASE = "http://127.0.0.1:8210"
BODY = json.load(open(f"{W}/longctx.json"))
CFG = {"server": {"model": os.environ.get("MODEL", f"{W}/model/Qwen3.8-FN-UD-Q4_K_XL.basalt"), "alias": "fn-q4", "host": "127.0.0.1",
                  "port": 8210, "vision": "dynamic", "parallel": N},
       "engine": {"expert-cache": int(os.environ["EXPERTS"]) if os.environ.get("EXPERTS") else "auto", "prefill": "auto", "spec": SPEC, "spec-min-p": 0.5,
                  "max-context": 131072 * max(1, N // 2) if N > 1 else 131072, "kv": "int8",
                  "vram-reserve-mib": 700, "resident-experts": True}}


def post(url, body, timeout=1800):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    return json.loads(raw) if raw.strip() else {}


def state():
    v = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader"], capture_output=True, text=True).stdout.strip()
    m = subprocess.run(["free", "-g"], capture_output=True, text=True).stdout.splitlines()[1].split()
    return f"vram={v:>9s} ram_used={m[2]}G avail={m[6]}G"


def chat(body):
    b = dict(body, stream=True, stream_options={"include_usage": True})
    req = urllib.request.Request(BASE + "/v1/chat/completions", data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"})
    t0 = time.time(); first = None; usage = {}
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
                if first is None and (delta.get("content") or delta.get("reasoning_content")):
                    first = time.time()
    end = time.time(); first = first or end
    return usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0), t0, first, end


def show(label, r):
    pt, ct, t0, first, end = r
    dec = ct / (end - first) if end > first and ct else 0
    print(f"  {label:<26s} ctx {pt:>6}  first token {first - t0:6.1f} s | decode {ct:>4} tok at {dec:5.0f} tok/s"
          f" | wall {end - t0:6.1f} s  {state()}", flush=True)


def variant(i, max_tokens=500):
    b = json.loads(json.dumps(BODY))
    b["messages"].append({"role": "assistant", "content": "Done."})
    b["messages"].append({"role": "user", "content": f"Variant {i}: summarise the design above in your own words, in detail."})
    b["max_tokens"] = max_tokens
    return b


json.dump(CFG, open(f"{W}/cfg-{N}-{SPEC}.json", "w"))
print(f"parallel {N} spec {SPEC}  before {state()}", flush=True)
t0 = time.time()
log = open(f"{W}/server-{N}-{SPEC}.log", "w")
proc = subprocess.Popen([f"{BASALT}/bin/basalt", "serve", "--config", f"{W}/cfg-{N}-{SPEC}.json"], stdout=log,
                        stderr=subprocess.STDOUT, start_new_session=True)
while True:
    if proc.poll() is not None:
        sys.exit(f"basalt exited {proc.returncode}; see {W}/server-{N}-{SPEC}.log")
    try:
        if urllib.request.urlopen(BASE + "/health", timeout=2).status == 200: break
    except Exception: pass
    time.sleep(0.2)
post(BASE + "/load", {})
print(f"  up in {time.time() - t0:.1f} s  {state()}", flush=True)
try:
    show("cold 30k read", chat(BODY))
    show("same prompt (cached)", chat(BODY))
    show("next turn", chat(variant(0)))
    short = {"model": "x", "messages": [{"role": "user", "content": "Write a 600-word short story about a lighthouse keeper."}],
             "max_tokens": 800, "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}
    show("short prompt decode", chat(short))
    for k in sorted({2, N} - {1}):
        if k > N: continue
        for i in range(k): chat(variant(100 * k + i, 1))
        res = [None] * k
        ts = [threading.Thread(target=lambda i=i: res.__setitem__(i, chat(variant(100 * k + i, 800)))) for i in range(k)]
        s = time.time(); [t.start() for t in ts]; [t.join() for t in ts]; e = time.time()
        tok = sum(r[1] for r in res)
        per = [r[1] / (r[4] - r[3]) for r in res if r[4] > r[3]]
        print(f"  {k} concurrent (warm 30k ctx)  total {tok} tok in {e - s:.1f} s = {tok / (e - s):5.0f} tok/s aggregate,"
              f" per stream {min(per):.0f}-{max(per):.0f} tok/s  {state()}", flush=True)
finally:
    subprocess.run(["pkill", "-TERM", "-g", str(proc.pid)])
    try: proc.wait(60)
    except Exception: subprocess.run(["pkill", "-KILL", "-g", str(proc.pid)])
