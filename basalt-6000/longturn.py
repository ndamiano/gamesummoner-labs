"""~100K context, one request at a time: cold read, decode over 2048 tokens, next turn, and a history changed mid-way.

usage: longturn.py PACK
"""
import json
from common import *

pack = sys.argv[1]
text = json.load(open(f"{W}/longctx.json"))["messages"][0]["content"]
big = "\n\n".join(f"Part {i + 1}:\n{text}" for i in range(3))
proc = start(config(PACKS[pack]), f"long-{pack}")
try:
    msgs = [{"role": "user", "content": big + "\n\nWrite a detailed review of all three parts."}]
    base = {"model": "m", "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}
    pt, ct, ttft, dec, reply = stream(dict(base, messages=msgs, max_tokens=2048))
    print(f"{pack} cold read: ctx {pt}, first token {ttft:.1f} s, decode {ct} tok at {dec:.0f} tok/s", flush=True)
    msgs2 = msgs + [{"role": "assistant", "content": reply}, {"role": "user", "content": "Now list three weaknesses."}]
    pt, ct, ttft, dec, _ = stream(dict(base, messages=msgs2, max_tokens=512))
    print(f"{pack} next turn: ctx {pt}, first token {ttft:.2f} s, decode {dec:.0f} tok/s", flush=True)
    msgs3 = msgs + [{"role": "assistant", "content": "Done: reviewed."}, {"role": "user", "content": "Now list three weaknesses."}]
    pt, ct, ttft, dec, _ = stream(dict(base, messages=msgs3, max_tokens=512))
    print(f"{pack} history changed at the last reply: ctx {pt}, first token {ttft:.2f} s", flush=True)
finally:
    stop(proc)
