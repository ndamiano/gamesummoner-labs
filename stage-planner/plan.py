"""Ask the build model for a stage plan of a run's design, and write it as a stage set the
section-budget chain reads: <n>.txt (stage --- done), <n>.reads, and frame.txt with the stage list.
Needs the control plane and an llm worker up.

    python3 plan.py <source run id> <label> [prompt file in prompts/]
"""

import json
import re
import shutil
import sys
import time
from pathlib import Path

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
SB = REPO / "labs" / "section-budget"
sys.path[:0] = [str(REPO / "src")]

from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from maestro.codegen.staging import spec_path
from maestro.state import RunState

STAGES = 9
BUDGET = 25
SYSTEM = "You are the lead developer on a game team."
PLANS = LAB / "plans"
GENERIC = ("carry.txt", "system_intro.txt", "left.txt", "left_last.txt", "preread.txt",
           "preread_files.txt", "codemap_head.txt")


def headings(design: str) -> list:
    return [l for l in design.splitlines() if l.startswith("#")]


def match_reads(reads: list, design: str) -> list:
    """Each read as a heading line the design has: exact, else the heading its § number names."""
    heads = headings(design)
    out = []
    for r in reads:
        r = r.strip()
        hit = r if r in heads else None
        if hit is None:
            num = re.search(r"(\d+(?:\.\d+)*)", r)
            if num:
                hit = next((h for h in heads if re.match(rf"#+ {re.escape(num.group(1))}[. ]", h + " ")), None)
        if hit and hit not in out:
            out.append(hit)
    return out


def parse(text: str) -> list:
    m = re.findall(r"```(?:json)?\s*(.*?)```", text, re.S)
    body = m[-1] if m else text[text.find("["):text.rfind("]") + 1]
    return json.loads(body)


def write(label: str, stages: list, design: str) -> Path:
    out = PLANS / label
    out.mkdir(parents=True, exist_ok=True)
    for name in GENERIC:
        shutil.copy2(SB / "stages" / name, out / name)
    frame = (SB / "stages" / "frame.txt").read_text(encoding="utf-8")
    listing = " · ".join(f"{i} {s['name'].strip().lower()}" for i, s in enumerate(stages, 1))
    frame = re.sub(r"The stages: .*?\. This is stage \{n\}\.",
                   f"The stages: {listing}. This is stage {{n}}.", frame)
    (out / "frame.txt").write_text(frame, encoding="utf-8")
    for i, s in enumerate(stages, 1):
        (out / f"{i}.txt").write_text(f"{s['name'].strip().lower()}. {s['stage'].strip()}\n---\n"
                                      f"{s['done'].strip()}\n", encoding="utf-8")
        (out / f"{i}.reads").write_text("\n".join(match_reads(s.get("reads") or [], design)) + "\n",
                                        encoding="utf-8")
    return out


def main(source: str, label: str, prompt_file: str = "plan.txt") -> None:
    design = spec_path(RunState(source).run_dir).read_text(encoding="utf-8")
    prompt = (LAB / "prompts" / prompt_file).read_text(encoding="utf-8").format(
        stages=STAGES, budget=BUDGET, design=design)
    t0 = time.time()
    reply = get_connector("qwen-flash-next").generate_with_tools(MessageBuilder(SYSTEM).add_user(prompt).build(), [])
    if reply.get("error"):
        raise SystemExit(f"plan call failed: {reply['error']}")
    text = ((reply.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    out = PLANS / label
    out.mkdir(parents=True, exist_ok=True)
    (out / "reply.txt").write_text(text, encoding="utf-8")
    stages = parse(text)
    print(f"plan has {len(stages)} stages", flush=True)
    write(label, stages, design)
    (out / "plan.json").write_text(json.dumps({"source": source, "prompt": prompt_file, "seconds": round(time.time() - t0),
                                               "usage": reply.get("usage"), "stages": stages},
                                              indent=1), encoding="utf-8")
    for i, s in enumerate(stages, 1):
        reads = (out / f"{i}.reads").read_text().split("\n")
        print(f"{i}. {s['name']} | reads {len([r for r in reads if r])}/{len(s.get('reads') or [])}", flush=True)
    print(f"plan {label}: {out}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
