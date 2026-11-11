"""Designs from a systems list: prod's decide chain with the mechanics step's rows, question and
line swapped for a systems file, then prod's write prompt on the local Flash-Next, for control asks.
--described hands the designer each kept system with its definition; without --out it reuses the
decisions in designs/ and writes into designs-described/. --out names a folder that holds its own
decisions and designs.
usage: write.py [--systems file.json] [--described] [--out folder] <control run id> ..."""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

from systems import HERE, SWAP, read, run_chain

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import bootstrap

bootstrap()
from contract.llm import chat_body_for_engine
from llm_clients.connector import get_connector
from maestro.codegen import design

QUESTION = "Does this system make sense for this game: {item}?"
KEEP = 0.7
ENTRY = "qwen-flash-next"
OUT = HERE / "designs"
DESCRIBED = HERE / "designs-described"
BANDS = ("core mechanics", "supporting mechanics", "extra mechanics")


def decide(ask, systems):
    job = design.chain(ask)
    step = next(s for s in job["steps"] if s["key"] == "mechanics")
    step.update(question=QUESTION, keep_over=KEEP,
                items=[{"name": name, "text": f"{name}: {text}"} for name, text in systems.items()])
    return run_chain(read, job["state"], job["steps"])


def post(messages, raw):
    body = get_connector(ENTRY).build_llm_job(messages, [], design.MAX_TOKENS)[0]["body"]
    request = urllib.request.Request(f"{SWAP['url'].rstrip('/')}/v1/chat/completions",
                                     json.dumps(chat_body_for_engine(body)).encode(),
                                     {"Content-Type": "application/json"})
    started = time.time()
    result = json.load(urllib.request.urlopen(request, timeout=7200))
    raw.write_text(json.dumps({"seconds": time.time() - started, "response": result}, indent=1), encoding="utf-8")
    print(f"  {raw.name}: {time.time() - started:.0f}s, {result.get('usage')}", flush=True)
    return design._reply_text(result)


def write(ask, state, spec, raw):
    return post(design._messages(ask, state, spec), raw)


def described(state, systems):
    lines = []
    for line in state.splitlines():
        band, _, names = line.partition(": ")
        if band in BANDS and names != "none":
            lines += [f"{band}:"] + [f"- {name}: {systems[name]}" for name in names.split(", ")]
        else:
            lines.append(line)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", type=Path, default=HERE / "systems-50.json")
    parser.add_argument("--described", action="store_true")
    parser.add_argument("--out")
    parser.add_argument("runs", nargs="+")
    args = parser.parse_args()
    systems = json.loads(args.systems.read_text(encoding="utf-8"))
    root = HERE / args.out if args.out else DESCRIBED if args.described else OUT
    decided_in = root if args.out else OUT
    asks = {}
    for run in args.runs:
        decisions, out = decided_in / run / "decisions.json", root / run
        decisions.parent.mkdir(parents=True, exist_ok=True)
        out.mkdir(parents=True, exist_ok=True)
        control = json.loads((HERE / "control" / f"{run}.json").read_text(encoding="utf-8"))
        asks[run] = control["state"].splitlines()[0].removeprefix("Game prompt: ")
        if not decisions.exists():
            decided = decide(asks[run], systems)
            decisions.write_text(json.dumps(decided, indent=1, ensure_ascii=False), encoding="utf-8")
        state = design.tiered_state(json.loads(decisions.read_text(encoding="utf-8")))
        if args.described:
            state = described(state, systems)
        (out / "state.txt").write_text(state, encoding="utf-8")
        print(f"{run} decided\n{state}\n", flush=True)
    for run in args.runs:
        out = root / run
        if (out / "design.md").exists():
            continue
        state, spec = (out / "state.txt").read_text(encoding="utf-8"), ""
        print(f"{run} writing: {asks[run]}", flush=True)
        for n in range(design.CONTINUATIONS + 1):
            text = ""
            for attempt in range(design.RETRIES + 1):
                text = write(asks[run], state, spec, out / f"raw-{n}-{attempt}.json")
                if text.strip():
                    break
            if not text.strip():
                raise SystemExit(f"{run}: write came back empty")
            spec += text
            if not design.missing_sections(spec):
                break
        (out / "design.md").write_text(spec, encoding="utf-8")
        print(f"{run} design: {len(spec)} chars, missing sections {design.missing_sections(spec)}", flush=True)


if __name__ == "__main__":
    main()
