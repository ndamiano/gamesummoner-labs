"""The 157-row catalogue as prod asks it against the candidate systems at a tighter line, on the
known games (same frame state for both) and on the control asks.
usage: compare.py [--ask-old]   --ask-old runs prod's mechanics step on the known games' states"""
import json
import re
import statistics
import sys
from pathlib import Path

from systems import HERE, read, run_chain

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import bootstrap

bootstrap()
from maestro.codegen import design

OLD_LINE, NEW_LINE = 0.6, 0.7
OUT = HERE / "systems"
OLD_ROWS_FOR = {
    "combat": ["enemies", "weapons", "player health", "bosses", "shoot", "melee attack"],
    "procedural generation": [],
    "roguelike": ["upgrades between runs"],
    "cards": ["cards", "deck building", "hand", "draw / discard"],
    "story": ["plot", "cutscenes", "lore"],
    "progression": ["experience and levels", "skill tree", "stats"],
    "companions": ["companions", "allies"],
    "equipment": ["equipment", "armour / defence"],
    "world map": ["map / world", "fast travel"],
    "dialogue": ["conversations", "choices"],
    "abilities": ["abilities / special moves"],
    "inventory": ["consumables", "key items", "inventory limit"],
    "economy": ["currency", "shops", "prices", "selling", "trading"],
    "quests": ["main quests", "side quests"],
    "survival": ["hunger", "thirst", "temperature", "shelter"],
    "crafting": ["materials", "recipes", "crafting stations"],
    "gathering": ["resource types", "gathering spots", "tools needed"],
    "building": ["buildable pieces", "placement", "rooms / structures"],
    "creatures": ["collectible creatures", "taming", "evolution"],
    "opponents": ["opponents", "rivals"],
}


def lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def ask_old(known):
    step = next(s for s in design.chain("")["steps"] if s["key"] == "mechanics")
    with (OUT / "known-old.jsonl").open("a", encoding="utf-8") as log:
        for row in known:
            state = "\n".join(line for line in row["state"].splitlines() if not line.startswith("systems:"))
            p = run_chain(read, state, [dict(step)])["steps"][0]["probabilities"]
            log.write(json.dumps({"game": row["game"], "ask": row["ask"], "state": state,
                                  "probabilities": p}, ensure_ascii=False) + "\n")


def kept(p, line):
    return sorted((name for name in p if p[name] > line), key=lambda name: -p[name])


def generic_words():
    rows = re.findall(r"^\| [^|]+ \| ([^|]+) \| [^|]+ \| (\d+) \|$", (HERE / "words.md").read_text(), re.M)
    asks = int(re.search(r"over the (\d+) distinct asks", (HERE / "words.md").read_text()).group(1))
    return {name for name, n in rows if int(n) >= asks / 2}


def main():
    known = lines(OUT / "known.jsonl")[-6:]
    if "--ask-old" in sys.argv:
        ask_old(known)
    old_known = {row["game"]: row["probabilities"] for row in lines(OUT / "known-old.jsonl")[-6:]}
    predictions = json.loads((HERE / "predictions.json").read_text(encoding="utf-8"))
    generic = generic_words()
    out = [f"# The 157-row catalogue at {OLD_LINE} against {len(known[0]['systems'])} systems at {NEW_LINE}", ""]

    print(f"KNOWN GAMES: old = 157 rows kept over {OLD_LINE}, new = systems kept over {NEW_LINE}")
    print("| game | old words | of them generic | old core covered | new systems | new core kept | new not predicted |")
    print("|---|---:|---:|---|---:|---|---|")
    totals = [0, 0, 0]
    for row in known:
        game, new, old = row["game"], row["probabilities"], old_known[row["game"]]
        core, fine = predictions[game]["core"], predictions[game]["fine"]
        old_kept, new_kept = kept(old, OLD_LINE), kept(new, NEW_LINE)
        covered = [c for c in core if any(w in old_kept for w in OLD_ROWS_FOR[c])]
        hit = [c for c in core if c in new_kept]
        extra = [m for m in new_kept if m not in core and m not in fine]
        totals = [totals[0] + len(core), totals[1] + len(covered), totals[2] + len(hit)]
        print(f"| {game} | {len(old_kept)} | {sum(w in generic for w in old_kept)} | {len(covered)} of {len(core)}"
              f"{', no ' + ', '.join(c for c in core if c not in covered) if len(covered) < len(core) else ''} | "
              f"{len(new_kept)} | {len(hit)} of {len(core)}"
              f"{', no ' + ', '.join(f'{c} {new[c]:.2f}' for c in core if c not in hit) if len(hit) < len(core) else ''} | "
              f"{', '.join(extra) or 'none'} |")
        out += [f"### {row['ask']}", "", f"- old ({len(old_kept)}): " + ", ".join(old_kept),
                f"- old at {NEW_LINE} ({len(kept(old, NEW_LINE))}): " + ", ".join(kept(old, NEW_LINE)),
                f"- new ({len(new_kept)}): " + ", ".join(f"{m} {new[m]:.2f}" for m in new_kept),
                "- new, 0.60 to 0.70: " + (", ".join(f"{m} {new[m]:.2f}" for m in kept(new, 0.6) if m not in new_kept) or "none"), ""]
    print(f"core: {totals[0]} predicted, old covers {totals[1]}, new keeps {totals[2]}\n")

    control = {path.stem: json.loads(path.read_text(encoding="utf-8")) for path in (HERE / "control").glob("*.json")}
    sizes = []
    for row in lines(OUT / "across-candidates.jsonl")[-len(control):]:
        steps = {s["key"]: s for s in control[row["run"]]["steps"] if not s.get("skipped")}
        old, new = steps["mechanics"]["probabilities"], row["probabilities"]
        old_kept, new_kept = kept(old, OLD_LINE), kept(new, NEW_LINE)
        sizes.append((row["ask"], len(old_kept), sum(w in generic for w in old_kept), len(kept(old, NEW_LINE)), len(new_kept), new_kept))
        out += [f"### {row['ask']}", "", f"- old ({len(old_kept)}): " + ", ".join(old_kept),
                f"- new ({len(new_kept)}): " + (", ".join(f"{m} {new[m]:.2f}" for m in new_kept) or "none"),
                "- new, 0.60 to 0.70: " + (", ".join(f"{m} {new[m]:.2f}" for m in kept(new, 0.6) if m not in new_kept) or "none"), ""]
    print(f"{len(sizes)} BUILD ASKS: words handed to the designer")
    for label, i in (("old, 157 rows over 0.6", 1), ("  of them generic", 2), ("old over 0.7", 3), ("new, systems over 0.7", 4)):
        values = [s[i] for s in sizes]
        print(f"  {label}: min {min(values)}, median {statistics.median(values):.0f}, max {max(values)}")
    print("  new keeps none:", [s[0][:40] for s in sizes if not s[4]])
    for ask, o, g, o7, n, names in sorted(sizes, key=lambda s: s[1]):
        print(f"  {o:3d} -> {n:2d} | {ask[:42]:42s} | {', '.join(names) or 'none'}")
    (OUT / "compare.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
