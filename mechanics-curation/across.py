"""Ask JEV every row of a systems file on every control ask: which asks keep which systems, which
keep none, and which systems are kept together.
usage: across.py [--systems file.json] [--question "... {item}?"]"""
import argparse
import json
from itertools import combinations
from pathlib import Path

from systems import HERE, SYSTEMS, frame_state, read, run_chain

QUESTION = "Does this system make sense for this game: {item}?"
KEEP = 0.6
OFTEN = 0.5
TOGETHER = 0.6


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--systems", type=Path, default=SYSTEMS)
    parser.add_argument("--question", default=QUESTION)
    args = parser.parse_args()
    systems = json.loads(args.systems.read_text(encoding="utf-8"))
    label = "across" if args.systems == SYSTEMS else f"across-{args.systems.stem}"
    step = {"key": "systems", "kind": "noul", "question": args.question, "keep_over": KEEP,
            "items": [{"name": name, "text": f"{name}: {text}"} for name, text in systems.items()]}
    rows = []
    with (HERE / "systems" / f"{label}.jsonl").open("a", encoding="utf-8") as log:
        for path in sorted((HERE / "control").glob("*.json")):
            state = frame_state(path.stem)
            probabilities = run_chain(read, state, [step])["steps"][0]["probabilities"]
            ask = state.splitlines()[0].removeprefix("Game prompt: ")
            rows.append((ask, probabilities))
            log.write(json.dumps({"run": path.stem, "ask": ask, "question": args.question,
                                  "systems": systems, "probabilities": probabilities},
                                 ensure_ascii=False) + "\n")

    n = len(rows)
    kept = {name: [ask for ask, p in rows if p[name] > KEEP] for name in systems}
    out = [f"# {len(systems)} systems on {n} asks", "", args.question, ""]
    for ask, p in sorted(rows, key=lambda r: sum(v > KEEP for v in r[1].values())):
        yes = sorted((name for name in systems if p[name] > KEEP), key=lambda name: -p[name])
        near = sorted((name for name in systems if 0.4 < p[name] <= KEEP), key=lambda name: -p[name])
        out += [f"### {ask}", "", f"- kept ({len(yes)}): " + (", ".join(f"{m} {p[m]:.2f}" for m in yes) or "none"),
                "- 0.40 to 0.60: " + (", ".join(f"{m} {p[m]:.2f}" for m in near) or "none"), ""]
    (HERE / "systems" / f"{label}.md").write_text("\n".join(out), encoding="utf-8")

    counts = sorted(systems, key=lambda name: -len(kept[name]))
    print(f"{len(systems)} systems, {n} asks. Kept per ask: "
          + ", ".join(str(sum(v > KEEP for v in p.values())) for _, p in rows))
    print("\nkept by:", ", ".join(f"{name} {len(kept[name])}" for name in counts))
    print(f"\nkept by {OFTEN:.0%} of asks or more:", ", ".join(m for m in counts if len(kept[m]) >= OFTEN * n) or "none")
    print("never kept:", ", ".join(m for m in counts if not kept[m]) or "none")
    print("asks with none:", " / ".join(ask[:40] for ask, p in rows if not any(v > KEEP for v in p.values())) or "none")
    print("\nkept together (both kept on at least 3 asks, and on 60% or more of the asks that kept either):")
    for a, b in combinations(systems, 2):
        both, either = len(set(kept[a]) & set(kept[b])), len(set(kept[a]) | set(kept[b]))
        if both >= 3 and both >= TOGETHER * either:
            print(f"  {a} + {b}: {both} of {either}")


if __name__ == "__main__":
    main()
