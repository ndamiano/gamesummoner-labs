"""Bring the local build stack up or down, or repair it: ninfer quasar on :8090, the llm image on :8700, the llm worker."""
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

REPO = Path("/home/nick/Documents/ai-agent-test")
sys.path[:0] = [str(REPO / "src"), str(REPO / "scripts")]
os.chdir(REPO / "src")
import local_gpu

NINFER = ["/home/nick/Documents/ninfer-quasar/build/apps/ninfer-serve",
          "/var/lib/models/ninfer/qwen3_8_27b_quasar_nvfp4.ninfer", "--model-id", "qwen3.8_27b_quasar",
          "--host", "127.0.0.1", "--port", "8090", "--max-context", "131072", "--spec", "dflash2",
          "--draft-tokens", "7", "--lm-head-draft", "--presence-penalty", "0", "--cors", "--vision",
          "--kv-dtype", "int8", "--preserve-thinking"]
IMAGE = "-m local.llm.server --image-id local --engine-url http://127.0.0.1:8090 --port 8700"
WORKER = "-m gamesummoner_worker --env-file /tmp/maestro-local/llm-env.json --image http://127.0.0.1:8700"


def pids(tail):
    out = subprocess.run(["ps", "-eo", "pid=,args="], capture_output=True, text=True).stdout
    return [int(l.split(None, 1)[0]) for l in out.splitlines() if l.split(None, 1)[1:] and l.split(None, 1)[1].endswith(tail)
            and not l.split(None, 1)[1].startswith(("/bin/bash", "bash"))]


def code(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except OSError:
        return 0, b""


def kill(tail, sig=signal.SIGKILL):
    for p in pids(tail):
        try:
            os.killpg(os.getpgid(p), sig)
        except ProcessLookupError:
            pass


def wait(url, seconds, check=lambda s, b: s == 200):
    end = time.time() + seconds
    while time.time() < end:
        if check(*code(url)):
            return True
        time.sleep(3)
    return False


def ensure():
    if not wait("http://127.0.0.1:8090/v1/models", 1, lambda s, b: b"qwen3.8_27b_quasar" in b):
        kill(" ".join(NINFER[1:]))
        log = open("/tmp/maestro-local/ninfer.log", "ab")
        subprocess.Popen(NINFER, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        print("ninfer started", flush=True)
        if not wait("http://127.0.0.1:8090/v1/models", 300, lambda s, b: b"qwen3.8_27b_quasar" in b):
            sys.exit("ninfer did not come up")
        kill(WORKER)
        kill(IMAGE)
    if not pids(IMAGE) or code("http://127.0.0.1:8700/health")[0] != 200:
        kill(WORKER)
        kill(IMAGE)
        time.sleep(2)
        local_gpu._spawn_image("llm", {"port": 8090})
        if not wait("http://127.0.0.1:8700/health", 120):
            sys.exit("image did not come up")
        print("image started", flush=True)
    if not pids(WORKER):
        local_gpu._spawn_worker("llm")
        print("worker started", flush=True)


def down():
    kill(WORKER, signal.SIGTERM)
    kill(IMAGE, signal.SIGTERM)
    kill(" ".join(NINFER[1:]))
    print("stack down", flush=True)


if __name__ == "__main__":
    {"up": ensure, "ensure": ensure, "down": down}[sys.argv[1]]()
