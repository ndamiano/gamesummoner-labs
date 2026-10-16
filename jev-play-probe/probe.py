"""Press a built game's start and movement inputs and ask JEV-27B-VL System 1 what each one did.

Usage: python probe.py <run_id> [<run_id> ...] [--jev http://127.0.0.1:8101]
Screens and report.json land in ~/output/jev-play-probe/<run_id>/.
"""
import argparse
import base64
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib import paths

paths.bootstrap()
from maestro.codegen.error_gate import VIEWPORT, _browser, _open, _serve

HERE = Path(__file__).parent
OUT = paths.OUTPUT / "jev-play-probe"
MOVE_KEYS = ["w", "a", "s", "d", "ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight"]
HOLD_MS = 500
SETTLE_MS = 800
START_TRIES = 3
REQUEST_CHARS = 6000


def question(name):
    text = (HERE / "questions" / f"{name}.txt").read_text(encoding="utf-8").strip()
    q, _, rest = text.partition("\n\n")
    return q, [line[2:] for line in rest.splitlines() if line.startswith("- ")]


def decide(url, kind, state, q, options=None):
    body = {"kind": kind, "state": state, "question": q}
    if options:
        body["options"] = options
    r = requests.post(f"{url}/v1/decide", json=body, timeout=300)
    r.raise_for_status()
    d = r.json()
    return {"choice": d["choice"], "probabilities": dict(zip(d["options"], d["probabilities"])),
            "seconds": d.get("elapsed_seconds")}


def shot(page, out, name):
    png = page.screenshot()
    (out / f"{name}.png").write_bytes(png)
    return {"image": "data:image/png;base64," + base64.b64encode(png).decode()}


def start_inputs(page):
    buttons = page.evaluate("""() => [...document.querySelectorAll('button, a, [role=button], [onclick]')]
      .filter(e => { const r = e.getBoundingClientRect();
                     return r.width > 0 && r.height > 0 && getComputedStyle(e).visibility !== 'hidden'; })
      .map(e => { const r = e.getBoundingClientRect();
                  return {text: (e.innerText || e.getAttribute('aria-label') || '').trim().slice(0, 60),
                          x: r.x + r.width / 2, y: r.y + r.height / 2}; })
      .filter(b => b.text)""")
    inputs = [(f'click the "{b["text"]}" button', ("click", (b["x"], b["y"]))) for b in buttons]
    return inputs + [("press Enter", ("key", "Enter")), ("press Space", ("key", "Space")),
                     ("click the middle of the screen",
                      ("click", (VIEWPORT["width"] / 2, VIEWPORT["height"] / 2)))]


def act(page, action):
    kind, what = action
    if kind == "click":
        page.mouse.click(*what)
    else:
        page.keyboard.press(what)


def probe(run_id, url):
    from playwright.sync_api import sync_playwright
    run = paths.RUNS / run_id
    request = json.loads((run / "spec.json").read_text(encoding="utf-8"))["request"]
    out = OUT / run_id
    out.mkdir(parents=True, exist_ok=True)
    report = {"run_id": run_id}
    errors, blocked = [], []
    with _serve(run / "game") as base_url, sync_playwright() as pw:
        browser = _browser(pw)
        page = _open(browser, base_url, errors, blocked)
        if page is None:
            report["load"] = errors
            (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
            return report

        inputs = start_inputs(page)
        q, _ = question("start")
        pick = decide(url, "choice", [f"The game's design:\n{request[:REQUEST_CHARS]}\n\nThe screen now:",
                                      shot(page, out, "start_0")], q, [d for d, _ in inputs])
        report["start_pick"] = pick
        order = sorted(range(len(inputs)), key=lambda i: -pick["probabilities"][inputs[i][0]])
        q, _ = question("started")
        report["start"] = []
        for n, i in enumerate(order[:START_TRIES], start=1):
            before = shot(page, out, f"start_{n}_before")
            act(page, inputs[i][1])
            page.wait_for_timeout(SETTLE_MS)
            v = decide(url, "noul", ["Before:", before, "\nAfter:", shot(page, out, f"start_{n}_after")], q)
            report["start"].append({"input": inputs[i][0], **v})
            if v["choice"] == "true":
                break

        q, options = question("moved")
        report["moves"] = []
        for key in MOVE_KEYS:
            before = shot(page, out, f"move_{key}_before")
            page.keyboard.down(key)
            page.wait_for_timeout(HOLD_MS)
            page.keyboard.up(key)
            page.wait_for_timeout(SETTLE_MS)
            v = decide(url, "choice", ["Before:", before, "\nAfter:", shot(page, out, f"move_{key}_after")],
                       q, options)
            report["moves"].append({"key": key, **v})

        q, _ = question("visible")
        report["visible"] = decide(url, "noul", [shot(page, out, "final")], q)
        report["errors"] = errors
        browser.close()
    (out / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def summary(r):
    lines = [f"== {r['run_id']}"]
    if "load" in r:
        return "\n".join(lines + [f"did not load: {r['load'][0]['message'][:120]}"])
    for t in r["start"]:
        lines.append(f"start  {t['input'][:40]:40} started={t['probabilities'].get('true', 0):.2f}")
    for m in r["moves"]:
        lines.append(f"move   {m['key']:10} {m['choice'][:40]:40} p={m['probabilities'][m['choice']]:.2f}")
    lines.append(f"visible={r['visible']['probabilities'].get('true', 0):.2f}  errors={len(r['errors'])}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run_ids", nargs="+")
    ap.add_argument("--jev", default="http://127.0.0.1:8101")
    args = ap.parse_args()
    for run_id in args.run_ids:
        print(summary(probe(run_id, args.jev)), flush=True)


if __name__ == "__main__":
    main()
