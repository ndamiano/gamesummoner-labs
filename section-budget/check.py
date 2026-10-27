"""Our own look at a stage's game, outside the build: does it boot clean, what does the screen
show, is Mittens drawn in his colours, and do the stage's mechanics answer. Prints one JSON line
and saves a screenshot next to the run.

    python3 check.py <run id> <port>
"""

import json
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

RUNS = Path("/var/tmp/section-budget/runs")
SHOTS = Path("/var/tmp/section-budget/shots")
COLOURS = {"orange": (0xE6, 0x9F, 0x00), "purple": (0x8F, 0x3F, 0xD1), "outline": (0x14, 0x10, 0x1E)}

PLAYER = """(() => { const g = window.__game; if (!g) return null;
  const apis = [g.DBG, window.DBG, g].filter(Boolean);
  let p = null;
  for (const a of apis) for (const k of ["playerState", "player", "playerPos"])
    if (!p && typeof a[k] === "function") { try { p = a[k](); } catch (e) {} }
  if (!p || p.x == null) p = (g.G || {}).player || null;
  if ((!p || p.x == null)) for (const a of apis) if (typeof a.state === "function") {
    try { const s = a.state(); if (s && s.player) p = s.player; } catch (e) {} }
  if (!p || p.x == null) return null;
  let hp = p.hp;
  if (hp == null) for (const a of apis) if (typeof a.state === "function") {
    try { hp = ((a.state() || {}).run || {}).hp; } catch (e) {} if (hp != null) break; }
  if (hp == null) hp = ((g.G || {}).run || {}).hp;
  return {x: p.x, y: p.y, state: p.state, hp}; })()"""
MODE = """(() => { const g = window.__game; if (!g) return null; if (g.G && g.G.mode) return g.G.mode;
  for (const a of [g.DBG, window.DBG, g].filter(Boolean)) if (typeof a.state === "function") {
    try { const s = a.state(); if (s && s.mode) return s.mode; } catch (e) {} }
  return null; })()"""
TURN = """(() => { const g = window.__game; if (!g) return null; if (g.G && g.G.run) return g.G.run.turn;
  for (const a of [g.DBG, window.DBG, g].filter(Boolean)) if (typeof a.state === "function") {
    try { const s = a.state(); if (s && s.run) return s.run.turn; } catch (e) {} }
  return null; })()"""
HUD = "(document.body.innerText.match(/HP \\d+\\/\\d+/) || [null])[0]"
VIEW = "(() => { const v = window.__game.view; return {offX: v.offX, offY: v.offY, scale: v.scale, dpr: v.dpr || 1}; })()"


def sprite_colours(page, p):
    """Design colours in the player's tile, or on the whole canvas when the game keeps no view."""
    v = page.evaluate(f"(() => {{ try {{ return {VIEW}; }} catch (e) {{ return null; }} }})()")
    if v and v.get("scale"):
        s, d = v["scale"], v["dpr"]
        x0, y0 = (v["offX"] + p["x"] * 16 * s) * d, (v["offY"] + (p["y"] - 1) * 16 * s) * d
        w, h = 16 * s * d, 32 * s * d
    else:
        x0, y0 = 0, 0
        w, h = page.evaluate("[document.querySelector('canvas').width, document.querySelector('canvas').height]")
    data = page.evaluate(f"""(() => {{ const c = document.querySelector('canvas');
      const img = c.getContext('2d').getImageData({int(x0)}, {int(y0)}, {int(w)}, {int(h)}).data;
      return Array.from(img); }})()""")
    counts = {k: 0 for k in COLOURS}
    for i in range(0, len(data), 4):
        px = tuple(data[i:i + 3])
        for k, c in COLOURS.items():
            if all(abs(a - b) <= 12 for a, b in zip(px, c)):
                counts[k] += 1
    return counts


def probe(page, out) -> None:
    mode = page.evaluate(MODE)
    out["mode"] = mode
    if mode and mode != "play":
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        out["mode_after_enter"] = page.evaluate(MODE)
    p = page.evaluate(PLAYER) if out["boots"] else None
    out["player"] = p
    if not p:
        return
    out["sprite"] = sprite_colours(page, p)
    start = p["x"]
    for _ in range(3):
        page.keyboard.press("ArrowRight", delay=80)
        page.wait_for_timeout(450)
    out["taps_right"] = (page.evaluate(PLAYER) or {}).get("x", start) - start
    turn = TURN
    before = page.evaluate(turn)
    page.keyboard.press("e")
    page.wait_for_timeout(2500)
    out["end_turn"] = [before, page.evaluate(turn)]
    dbg = "(window.DBG || window.__game.DBG || {})"
    if "setPlayer" in page.evaluate(f"Object.keys({dbg})"):
        page.evaluate(f"{dbg}.setPlayer(9,3)")
        page.wait_for_timeout(3000)
        after = page.evaluate(PLAYER) or {}
        out["drop"] = {"hp": after.get("hp"), "hud": page.evaluate(HUD)}


def check(rid: str, port: int) -> dict:
    game = RUNS / rid / "game"
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                               "--directory", str(game)], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    time.sleep(1)
    out = {"run": rid}
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            page = b.new_page(viewport={"width": 1280, "height": 720})
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)[:200]))
            page.goto(f"http://127.0.0.1:{port}/")
            page.wait_for_timeout(2500)
            out["boots"] = page.evaluate("!!window.__game")
            SHOTS.mkdir(parents=True, exist_ok=True)
            n = json.loads((RUNS / rid / "stage.json").read_text())["n"]
            page.screenshot(path=str(SHOTS / f"{rid}-stage{n}.png"))
            try:
                probe(page, out)
            except Exception as e:
                out["probe_error"] = str(e)[:200]
            out["errors"] = errors
            b.close()
    finally:
        server.terminate()
    return out


if __name__ == "__main__":
    print(json.dumps(check(sys.argv[1], int(sys.argv[2]))))
