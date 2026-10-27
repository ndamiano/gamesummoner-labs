import collections
import glob
import json
import re

READ = re.compile(r"\bread_file\(")
OPEN_R = re.compile(r"""\bopen\((?![^)\n]*['"][wax])""")
WRITE = re.compile(r"\b(?:write_file|edit_file)\(|\bopen\([^)\n]*['\"][wax]")
CALLED = re.compile(r"\[what the program called:\n(.*?)\]", re.S)


def scan(pattern):
    out = []
    for f in sorted(glob.glob(pattern + "/transcript.json")):
        h = json.load(open(f))
        h = h.get("history", h) if isinstance(h, dict) else h
        reads = writes = landed = 0
        for i, m in enumerate(h):
            if not m.get("tool_calls") or m["tool_calls"][0]["id"].startswith("call_seeded"):
                continue
            reply = str(h[i + 1].get("content")) if i + 1 < len(h) else ""
            if re.search(r"nothing ran|nothing in the program ran", reply, re.I):
                continue
            code = json.loads(m["tool_calls"][0]["function"]["arguments"]).get("code") or ""
            reads += len(READ.findall(code)) + len(OPEN_R.findall(code))
            writes += len(WRITE.findall(code))
            for block in CALLED.findall(reply):
                landed += sum(1 for line in block.splitlines()
                              if re.match(r"\s*(write_file|edit_file)\b", line) and "failed" not in line)
        out.append((reads, writes, landed))
    return out
