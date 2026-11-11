"""Every distinct ask JEV has decided, with the words it chose, and every catalogue word with the asks that chose it."""
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import LABS, RUNS, SRC

HERE = Path(__file__).resolve().parent
CONTROL = HERE / "control"
COVERAGE = LABS / "jev-design-decisions" / "runs" / "cov"
CATALOGUE = SRC / "maestro" / "codegen" / "prompts" / "design" / "mechanics.json"
FRAME = ["dimension", "camera", "time model", "movement model", "session shape", "failure", "tone", "size"]
LOOK = ["art style", "palette", "lighting", "typography", "music", "sound effects style"]
LISTS = ["screens", "hud", "effects", "accessibility"]
SHOWN = 300


def norm(ask):
    return " ".join(ask.lower().split()).rstrip(".")


def by_confidence(probabilities, kept):
    return sorted(kept, key=lambda name: -probabilities[name])


def chains(rows):
    newest = {}
    for path in RUNS.glob("*/design/decisions.json"):
        decided = json.loads(path.read_text(encoding="utf-8"))
        steps = {s["key"]: s for s in decided["steps"] if not s.get("skipped")}
        probabilities = steps.get("mechanics", {}).get("probabilities", {})
        if set(probabilities) != rows:
            continue
        state = dict(line.split(": ", 1) for line in decided["state"].splitlines() if ": " in line)
        ask = state["Game prompt"]
        if norm(ask) in newest and path.stat().st_mtime < newest[norm(ask)]["mtime"]:
            continue
        kept = [m for m in state.get("mechanics", "").split(", ") if m and m != "none"]
        newest[norm(ask)] = {
            "ask": ask, "run": path.parts[-3], "source": "build", "path": path,
            "mtime": path.stat().st_mtime, "state": state, "ends": state.get("win/lose", ""),
            "mechanics": by_confidence(probabilities, kept)}
    return newest


def coverage(rows, have):
    out = {}
    for path in sorted(COVERAGE.glob("*/mechanics_result.json")):
        frame = json.loads((path.parent / "frame_result.json").read_text(encoding="utf-8"))
        result = json.loads(path.read_text(encoding="utf-8"))
        ask = frame["prompt"]
        label = " — " in ask and len(ask) < 80
        if label or norm(ask) in have or norm(ask) in out or set(result["probabilities"]) != rows:
            continue
        out[norm(ask)] = {
            "ask": ask, "run": path.parent.name, "source": "coverage probe", "state": frame["decided"],
            "ends": ", ".join(frame["decided"].get("win/lose") or []),
            "mechanics": by_confidence(result["probabilities"], result["kept"])}
    return out


def section(entry):
    state = entry["state"]
    ask = entry["ask"] if len(entry["ask"]) <= SHOWN else entry["ask"][:SHOWN] + " […]"
    lines = [f"### {ask}", "", f"`{entry['run']}`, {entry['source']}", "",
             "- frame: " + ", ".join(state[k] for k in FRAME if k in state),
             "- ends: " + (entry["ends"] or "none"),
             f"- mechanics ({len(entry['mechanics'])}): " + (", ".join(entry["mechanics"]) or "none")]
    look = [state[k].split(":")[0] for k in LOOK if k in state]
    if look:
        lines.append("- look and sound: " + ", ".join(look))
    lines += [f"- {k}: {state[k]}" for k in LISTS if k in state]
    return lines + [""]


def main():
    sections = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    rows = {name for names in sections.values() for name in names}
    built = chains(rows)
    probed = coverage(rows, built)
    shutil.rmtree(CONTROL, ignore_errors=True)
    CONTROL.mkdir()
    for entry in built.values():
        shutil.copy(entry["path"], CONTROL / f"{entry['run']}.json")

    entries = sorted([*built.values(), *probed.values()], key=lambda e: (len(e["ask"]) > SHOWN, len(e["ask"])))
    n = len(entries)
    out = [f"# The words JEV chose, for each of {n} distinct asks", "",
           f"{len(built)} from the decide chain of a build (the newest chain of each ask, pinned in",
           f"`control/`), {len(probed)} from the 2026-10-15 coverage probe in `labs/jev-design-decisions`",
           "(same 157 rows and question, frame only, no look and sound). Shortest ask first; mechanics",
           f"in the order JEV was surest of them. Asks over {SHOWN} characters are cut and come last.", ""]
    for entry in entries:
        out += section(entry)
    (HERE / "asks.md").write_text("\n".join(out), encoding="utf-8")

    chosen = {name: sum(name in e["mechanics"] for e in entries) for name in rows}
    out = [f"# Catalogue words over the {n} distinct asks", "",
           "| section | word | description | asks that chose it |", "|---|---|---|---:|"]
    for name_of_section, names in sections.items():
        out += [f"| {name_of_section} | {name} | {text} | {chosen[name]} |" for name, text in names.items()]
    (HERE / "words.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"{n} distinct asks ({len(built)} build, {len(probed)} coverage probe): asks.md, words.md")


main()
