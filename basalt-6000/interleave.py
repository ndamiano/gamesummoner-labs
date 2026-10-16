"""Seven builds on one engine, one request at a time, turns round-robin: does every turn hit its parked cache?"""
import json, re
from common import *

text = json.load(open(f"{W}/longctx.json"))["messages"][0]["content"]
N, ROUNDS = 7, 3
proc = start(config(PACKS["q4"], **{"conversation-cache-mib": 32000, "conversation-cache-slots": 16}), "interleave")
try:
    base = {"model": "m", "temperature": 0, "max_tokens": 64, "chat_template_kwargs": {"enable_thinking": False}}
    convs = [[{"role": "user", "content": f"Build {i}. " + "\n\n".join([text, text]) + f"\n\nSummarise build {i}."}]
             for i in range(N)]
    for rnd in range(ROUNDS + 1):
        for i in range(N):
            pt, ct, ttft, dec, reply = stream(dict(base, messages=convs[i]))
            print(f"round {rnd} build {i}: ctx {pt}, first token {ttft:.2f} s", flush=True)
            convs[i] += [{"role": "assistant", "content": reply}, {"role": "user", "content": f"Step {rnd}: continue."}]
finally:
    stop(proc)
for line in open(f"{W}/server-interleave.log"):
    if "conversation cache" in line:
        print(line.rstrip()[:200])
