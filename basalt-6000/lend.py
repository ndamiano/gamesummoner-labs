"""Q4 with --vram-elastic: decode at 30K with all experts on the card, then while lending 20 and 30 GB, then after
taking it back; with the give-back and take-back times."""
import json, urllib.error, urllib.request
from common import *


def vram(reserve):
    req = urllib.request.Request(BASE + "/v1/vram", data=json.dumps({"reserve_mib": reserve}).encode(),
                                 headers={"Content-Type": "application/json"})
    t = time.time()
    try:
        v = json.loads(urllib.request.urlopen(req, timeout=600).read())
    except urllib.error.HTTPError as e:
        print("  vram error:", e.code, e.read()[:400], flush=True)
        raise
    return time.time() - t, v


def gpu_used():
    return subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader"], capture_output=True,
                          text=True).stdout.strip()


body = json.load(open(f"{W}/longctx.json"))
proc = start(config(PACKS["q4"], **{"vram-elastic": True, "resident-experts": False, "mmap-experts": True}), "lend")
try:
    def run(label):
        pt, ct, ttft, dec, _ = stream(dict(body, max_tokens=500))
        print(f"  {label:<28} first token {ttft:5.2f} s  decode {dec:4.0f} tok/s  gpu {gpu_used()}", flush=True)
    run("all on the card")
    for mib in (20000, 30000):
        dt, v = vram(mib)
        print(f"  lend {mib} MiB: {dt:.1f} s, free {v.get('vram_free_mib')} MiB, cache {v.get('expert_cache_mib')}/"
              f"{v.get('expert_cache_full_mib')} MiB, gpu {gpu_used()}", flush=True)
        run(f"while lending {mib // 1000} GB")
        dt, v = vram(None)
        print(f"  take back: {dt:.1f} s, cache {v.get('expert_cache_mib')}/{v.get('expert_cache_full_mib')} MiB", flush=True)
        run("after take-back")
finally:
    stop(proc)
