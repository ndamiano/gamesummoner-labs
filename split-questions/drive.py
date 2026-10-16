"""Runs one pass: pipes a prompt into a fresh coding-agent REPL in the current folder, and while a
judge call reads the end of the turn as an announcement rather than finished work, sends the
continue prompt in the same session. The transcript goes to stdout.

    python3 drive.py <prompt file> [max continues]
"""
import json
import os
import select
import subprocess
import sys
import urllib.request
from pathlib import Path

PROMPTS = Path(__file__).resolve().parent / "prompts"
ENDPOINT = "http://127.0.0.1:5001/v1/chat/completions"
MODEL = "qwen3.8-flash-next-basalt"
TAIL = 3000


def read_turn(proc) -> str:
    buf = b""
    fd = proc.stdout.fileno()
    while True:
        chunk = os.read(fd, 65536)
        if not chunk:
            return buf.decode(errors="replace")
        sys.stdout.buffer.write(chunk)
        sys.stdout.flush()
        buf += chunk
        if buf.endswith(b"\n> ") and not select.select([fd], [], [], 2.0)[0]:
            return buf.decode(errors="replace")


def judge(turn: str) -> str:
    body = {
        "model": MODEL,
        "messages": [{"role": "user", "content": (PROMPTS / "judge.txt").read_text() + turn[-TAIL:]}],
        "max_tokens": 2000,
        "temperature": 0,
        "reasoning_effort": "none",
    }
    req = urllib.request.Request(ENDPOINT, json.dumps(body).encode(), {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        text = json.load(r)["choices"][0]["message"]["content"] or ""
    return "CONTINUE" if "CONTINUE" in text.upper() else "DONE"


def main() -> None:
    prompt = Path(sys.argv[1]).read_text().strip()
    max_continues = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    proc = subprocess.Popen(["coding-agent"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, env={**os.environ, "PYTHONUNBUFFERED": "1"})
    read_turn(proc)
    message = prompt
    for n in range(max_continues + 1):
        proc.stdin.write((message + "\n").encode())
        proc.stdin.flush()
        turn = read_turn(proc)
        verdict = judge(turn) if proc.poll() is None else "DONE"
        print(f"\n[drive] turn {n}: {verdict}", flush=True)
        if verdict == "DONE" or n == max_continues:
            break
        message = (PROMPTS / "continue.txt").read_text().strip()
    proc.stdin.close()
    proc.wait()


if __name__ == "__main__":
    main()
