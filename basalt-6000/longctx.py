"""One request at ~100K context: prompt read time and decode speed over 2048 tokens.

usage: longctx.py MODEL
"""
import json, os, subprocess, sys, time, urllib.request

W = "/opt/dlami/nvme/w"
MODEL = sys.argv[1]
BASE = "http://127.0.0.1:8210"
body = json.load(open(f"{W}/longctx.json"))
text = body["messages"][0]["content"]
body["messages"][0]["content"] = "\n\n".join(f"Part {i + 1}:\n{text}" for i in range(3)) + "\n\nNow write a detailed review of all three parts."
body["max_tokens"] = 2048
CFG = {"server": {"model": MODEL, "alias": "m", "host": "127.0.0.1", "port": 8210, "vision": "dynamic", "parallel": 1},
       "engine": {"expert-cache": "auto", "prefill": "auto", "spec": 7, "spec-min-p": 0.5, "max-context": 131072,
                  "kv": "int8", "vram-reserve-mib": 700, "resident-experts": True}}


def chat(b):
    b = dict(b, stream=True, stream_options={"include_usage": True})
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
                if first is None and ((c.get("delta") or {}).get("content") or (c.get("delta") or {}).get("reasoning_content")):
                    first = time.time()
    end = time.time()
    ct = usage.get("completion_tokens", 0)
    print(f"  ctx {usage.get('prompt_tokens')}  first token {first - t0:.1f} s  decode {ct} tok at {ct / (end - first):.0f} tok/s",
          flush=True)


json.dump(CFG, open(f"{W}/cfg-long.json", "w"))
log = open(f"{W}/server-long.log", "w")
proc = subprocess.Popen([f"{W}/basalt-patch/bin/basalt", "serve", "--config", f"{W}/cfg-long.json"], stdout=log,
                        stderr=subprocess.STDOUT, start_new_session=True)
while True:
    if proc.poll() is not None:
        sys.exit(f"basalt exited {proc.returncode}")
    try:
        if urllib.request.urlopen(BASE + "/health", timeout=2).status == 200: break
    except Exception: pass
    time.sleep(0.2)
urllib.request.urlopen(urllib.request.Request(BASE + "/load", data=b"{}", headers={"Content-Type": "application/json"}), timeout=1800).read()
print(os.path.basename(MODEL), flush=True)
try:
    chat(body)
    chat(body)
finally:
    subprocess.run(["pkill", "-TERM", "-g", str(proc.pid)])
    try: proc.wait(60)
    except Exception: subprocess.run(["pkill", "-KILL", "-g", str(proc.pid)])
