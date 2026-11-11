"""Each design written from the systems list beside the control design for the same ask: the
decided frame and list, and the gameplay sections the designer wrote. For a folder other than
designs, the names-only design in designs is shown as well.
usage: sections.py [folder]"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import RUNS

HERE = Path(__file__).resolve().parent
NAMES = HERE / "designs"
OUT = HERE / (sys.argv[1] if len(sys.argv) > 1 else "designs")
BANDS = ("core mechanics", "supporting mechanics", "extra mechanics")
FRAME = ["dimension", "camera", "time model", "movement model", "session shape", "failure", "tone", "size", "win/lose"]


def gameplay(text):
    body = re.search(r"^# 4\. .*?(?=^# 5\. )", text, re.S | re.M)
    return re.findall(r"^## 4\.\d+ (.*)$", body.group(0) if body else "", re.M)


def fields(state):
    found, band = {}, None
    for line in state.splitlines():
        if line.rstrip(":") in BANDS and line.endswith(":"):
            band = line.rstrip(":")
            found[band] = []
        elif line.startswith("- ") and band:
            found[band].append(line[2:].split(": ", 1)[0])
        elif ": " in line:
            key, value = line.split(": ", 1)
            found[key], band = value, None
    return {key: ", ".join(value) if isinstance(value, list) else value for key, value in found.items()}


def main():
    out = ["# Designs from the systems list beside the control designs", ""]
    for folder in sorted(p for p in OUT.iterdir() if (p / "design.md").exists()):
        new = fields((folder / "state.txt").read_text(encoding="utf-8"))
        old = fields(json.loads((HERE / "control" / f"{folder.name}.json").read_text(encoding="utf-8"))["state"])
        design, control = (folder / "design.md").read_text(encoding="utf-8"), RUNS / folder.name / "design.md"
        out += [f"## {new['Game prompt']}", "",
                "- frame changed from the control: "
                + (", ".join(f"{k} {old.get(k)} -> {new.get(k)}" for k in FRAME if old.get(k) != new.get(k)) or "nothing"),
                f"- systems, core: {new['core mechanics']}", f"- systems, supporting: {new['supporting mechanics']}",
                f"- systems, extra: {new['extra mechanics']}",
                f"- new design: {len(design)} chars, {len(gameplay(design))} gameplay sections: " + "; ".join(gameplay(design))]
        names = NAMES / folder.name / "design.md"
        if OUT != NAMES and names.exists():
            text = names.read_text(encoding="utf-8")
            out += [f"- names-only design: {len(text)} chars, {len(gameplay(text))} gameplay sections: "
                    + "; ".join(gameplay(text))]
        if control.exists():
            text = control.read_text(encoding="utf-8")
            out += [f"- control design: {len(text)} chars, {len(old['mechanics'].split(', '))} words, "
                    f"{len(gameplay(text))} gameplay sections: " + "; ".join(gameplay(text))]
        else:
            out += [f"- control: {len(old['mechanics'].split(', '))} words, no design was written"]
        out += [""]
    (OUT / "sections.md").write_text("\n".join(out), encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
