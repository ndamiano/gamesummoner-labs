"""Repeat the systems probe on one control ask: serial rounds, then rounds with several reads in
flight at once. usage: repeat.py <control run id> [rounds]"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from systems import HERE, SYSTEMS, frame_state, one, prompt

CONFIGS = [
    ("definition", "Does this mechanic make sense for this game: {item}?"),
    ("definition", "Does this system make sense for this game: {item}?"),
    ("bare name", "Does this mechanic make sense for this game: {item}?"),
    ("bare name", "Does this game contain {item}?"),
]
IN_FLIGHT = 8


def prompts(state, systems):
    out = []
    for rows, question in CONFIGS:
        for name, text in systems.items():
            item = f"{name}: {text}" if rows == "definition" else name
            out.append(((rows, question, name), prompt("noul", state, question.replace("{item}", item),
                                                       ["false", "true"])))
    return out


def main():
    run = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    asked = prompts(frame_state(run), json.loads(SYSTEMS.read_text(encoding="utf-8")))
    seen = {}
    with (HERE / "systems" / f"{run}.repeats.jsonl").open("a", encoding="utf-8") as log:
        def record(mode, n, answers):
            for (key, _), p in zip(asked, answers):
                seen.setdefault((mode, *key), []).append(p)
                log.write(json.dumps({"mode": mode, "round": n, "rows": key[0], "question": key[1],
                                      "system": key[2], "p": p}) + "\n")

        for n in range(rounds):
            record("serial", n, [one("noul", text, 2)[1] for _, text in asked])
        with ThreadPoolExecutor(IN_FLIGHT) as pool:
            for n in range(rounds):
                record("at once", n, list(pool.map(lambda a: one("noul", a[1], 2)[1], asked)))

    print("| mode | rows | question | system | n | min | max | kept |")
    print("|---|---|---|---|---:|---:|---:|---:|")
    for (mode, rows, question, name), ps in seen.items():
        print(f"| {mode} | {rows} | {question.split(':')[0].replace(' {item}?', '')} | {name} | {len(ps)} | "
              f"{min(ps):.3f} | {max(ps):.3f} | {sum(p > 0.6 for p in ps)} |")


if __name__ == "__main__":
    main()
