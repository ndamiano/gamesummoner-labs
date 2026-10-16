"""Ask JEV the art-style question for every local prompt, and classify the style the LLM design actually wrote."""
import json
import os
import sys
import urllib.error

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

STYLES = {
    "pixel art": "low-resolution sprites or tiles with visible square pixels and a limited palette",
    "flat vector": "clean flat shapes, solid colors, crisp edges, no texture",
    "hand-drawn / painterly": "illustrated look with brush strokes, ink lines or watercolor texture",
    "anime / cel-shaded": "bold outlines with flat banded shading, characters drawn like animation",
    "low-poly": "few large flat-shaded polygons, faceted geometric forms",
    "voxel": "everything built from cubes, blocky like Minecraft",
    "realistic": "lifelike materials, lighting and proportions",
    "neon / synthwave": "dark background with glowing saturated neon lines and bloom",
    "minimalist geometric": "abstract simple primitives, few colors, shapes stand in for things",
}
OTHER = {"something not listed": "none of the styles above fits this game"}


def decide(question, styles):
    options = [f"{k}: {v}" for k, v in styles.items()]
    try:
        r = ask.post(f"{ask.DECIDE}/v1/decide", {"kind": "choice", "question": question, "options": options})
    except urllib.error.HTTPError as e:
        if b"context length" not in e.read():
            raise
        return {"pick": "skipped: over context", "p": {}}
    names = list(styles)
    return {"pick": names[r["choice_index"]], "p": dict(zip(names, (round(x, 4) for x in r["probabilities"])))}


def main():
    other = "--other" in sys.argv
    styles = {**STYLES, **OTHER} if other else STYLES
    rows = json.load(open("dim_results.json"))
    specs = {}
    for r in rows:
        spec = json.load(open(f"/home/nick/output/runs/{r['run']}/spec.json"))
        specs.setdefault(r["prompt"], {"dim": r["jev"], "built": r["built"], "src": r["src"], "designs": []})
        run = f"/home/nick/output/runs/{r['run']}"
        doc = next((p for p in (f"{run}/game/design/design.md", f"{run}/design.md") if os.path.exists(p)), None)
        design = open(doc).read() if doc else spec.get("request")
        if r["src"] == "ask" and design:
            specs[r["prompt"]]["designs"].append((r["run"], design))
    ask.chat(ask.JEV, "hi", 1, think=False)
    ask.wait_decide()
    out = []
    for prompt, s in sorted(specs.items()):
        if " — " in prompt and len(prompt) < 90:
            continue
        row = {"prompt": prompt, "dim": s["dim"], "built": s["built"],
               "jev": decide(f"Given a {s['dim']} game with the prompt '{prompt}', what art style would you choose?", styles),
               "designs": [{"run": run, **decide(f"What art style does this game design describe?\n\n{design}", styles)}
                           for run, design in s["designs"]]}
        out.append(row)
        print(f"{row['jev']['pick']:24} {[d['pick'] for d in row['designs']]}  {prompt[:70]}", flush=True)
    json.dump(out, open("style_results_other.json" if other else "style_results.json", "w"), indent=1)


if __name__ == "__main__":
    main()
