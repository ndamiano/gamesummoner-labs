"""Known games: prod's frame steps on each ask in predictions.json, then every row of a systems
file, set against the systems predicted before the run.
usage: known.py [--systems file.json] [--question "... {item}?"]"""
import argparse
import json
import sys
from pathlib import Path

from systems import HERE, read, run_chain

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import bootstrap

bootstrap()
from maestro.codegen import design

QUESTION = "Does this system make sense for this game: {item}?"
KEEP = 0.6
FRAME_ENDS = "win/lose"


def frame_steps(ask):
    steps = design.chain(ask)["steps"]
    return steps[:next(i for i, step in enumerate(steps) if step["key"] == FRAME_ENDS) + 1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", type=Path, default=HERE / "candidates.json")
    parser.add_argument("--question", default=QUESTION)
    args = parser.parse_args()
    systems = json.loads(args.systems.read_text(encoding="utf-8"))
    predictions = json.loads((HERE / "predictions.json").read_text(encoding="utf-8"))
    step = {"key": "systems", "kind": "noul", "question": args.question, "keep_over": KEEP,
            "items": [{"name": name, "text": f"{name}: {text}"} for name, text in systems.items()]}
    out = [f"# Known games on {len(systems)} systems", "", args.question, ""]
    with (HERE / "systems" / "known.jsonl").open("a", encoding="utf-8") as log:
        for game, predicted in predictions.items():
            result = run_chain(read, f"Game prompt: {predicted['ask']}", frame_steps(predicted["ask"]) + [step])
            p = result["steps"][-1]["probabilities"]
            log.write(json.dumps({"game": game, "ask": predicted["ask"], "question": args.question,
                                  "state": result["state"], "systems": systems, "probabilities": p},
                                 ensure_ascii=False) + "\n")
            kept = sorted((name for name in systems if p[name] > KEEP), key=lambda name: -p[name])
            core, fine = predicted["core"], predicted["fine"]
            show = lambda names: ", ".join(f"{name} {p[name]:.2f}" for name in names) or "none"
            frame = [line.split(": ", 1)[1] for line in result["state"].splitlines()[1:] if not line.startswith("systems:")]
            out += [f"### {game}", "", f"ask: {predicted['ask']}", "", "- frame: " + ", ".join(frame),
                    f"- core kept ({sum(name in kept for name in core)} of {len(core)}): "
                    + show([name for name in kept if name in core]),
                    "- core missed: " + show([name for name in core if name not in kept]),
                    "- fine, kept: " + show([name for name in kept if name in fine]),
                    "- kept, not predicted: " + show([name for name in kept if name not in core and name not in fine]),
                    ""]
    text = "\n".join(out)
    (HERE / "systems" / "known.md").write_text(text, encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
