"""Decode scaling only: K simultaneous short-prompt requests (K = 1, 2, 4, 8) on one --parallel 8 server.

usage: conc.py MODEL SPEC
"""
import json, os, subprocess, sys, threading, time, urllib.request

W = "/opt/dlami/nvme/w"
MODEL, SPEC = sys.argv[1], int(sys.argv[2])
BASALT = os.environ.get("BASALT", f"{W}/basalt-patch")
BASE = "http://127.0.0.1:8210"
TOPICS = ["a lighthouse keeper", "a desert caravan", "a robot gardener", "a deep-sea diver", "a mountain village",
          "a clockmaker's apprentice", "a lost spaceship", "a jazz musician"]
CFG = {"server": {"model": MODEL, "alias": "m", "host": "127.0.0.1", "port": 8210, "vision": "dynamic", "parallel": 8},
       "engine": {"expert-cache": "auto", "prefill": "auto", "spec": SPEC, "spec-min-p": 0.5, "max-context": 131072,
                  "kv": "int8", "vram-reserve-mib": 700, "resident-experts": True}}


def post(url, body, timeout=1800):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    raw = urllib.request.urlopen(req, timeout=timeout).read()
    return json.loads(raw) if raw.strip() else {}


def chat(i, max_tokens=600):
    b = {"model": "m", "messages": [{"role": "user", "content": f"Write a long, detailed story about {TOPICS[i % 8]}. "
                                                                 f"Keep going for at least 1500 words."}],
         "max_tokens": max_tokens, "temperature": 0, "chat_template_kwargs": {"enable_thinking": False},
         "stream": True, "stream_options": {"include_usage": True}}
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
                if first is None and (c.get("delta") or {}).get("content"):
                    first = time.time()
    return usage.get("completion_tokens", 0), first or time.time(), time.time()


tag = f"{os.path.basename(MODEL).split('.basalt')[0]}-spec{SPEC}"
json.dump(CFG, open(f"{W}/cfg-conc.json", "w"))
log = open(f"{W}/server-conc-{tag}.log", "w")
proc = subprocess.Popen([f"{BASALT}/bin/basalt", "serve", "--config", f"{W}/cfg-conc.json"], stdout=log,
                        stderr=subprocess.STDOUT, start_new_session=True)
while True:
    if proc.poll() is not None:
        sys.exit(f"basalt exited {proc.returncode}")
    try:
        if urllib.request.urlopen(BASE + "/health", timeout=2).status == 200: break
    except Exception: pass
    time.sleep(0.2)
post(BASE + "/load", {})
print(tag, flush=True)
try:
    chat(0, 50)
    for k in (1, 2, 4, 8):
        res = [None] * k
        ts = [threading.Thread(target=lambda i=i: res.__setitem__(i, chat(i))) for i in range(k)]
        [t.start() for t in ts]; [t.join() for t in ts]
        start = max(r[1] for r in res); end = min(r[2] for r in res)
        overlap_tok = 0
        tok = sum(r[0] for r in res)
        per = [r[0] / (r[2] - r[1]) for r in res if r[2] > r[1]]
        span = max(r[2] for r in res) - min(r[1] for r in res)
        print(f"  {k} at once: {tok} tok, aggregate {tok / span:5.0f} tok/s, per stream {min(per):.0f}-{max(per):.0f}",
              flush=True)
finally:
    subprocess.run(["pkill", "-TERM", "-g", str(proc.pid)])
    try: proc.wait(60)
    except Exception: subprocess.run(["pkill", "-KILL", "-g", str(proc.pid)])
