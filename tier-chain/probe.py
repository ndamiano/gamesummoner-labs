"""Plays a built game headless through the design's debug API and reports which checks of each
tier pass, as one JSON line. Tier 1 checks are the ones verified by hand on run 26d2aeb66c16.
usage: probe.py <game dir> <highest tier to check>"""
import functools
import http.server
import json
import sys
import threading

from playwright.sync_api import sync_playwright


def serve(root):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}/index.html"


class Game:
    def __init__(self, page):
        self.page = page

    def js(self, code):
        return self.page.evaluate(code)

    def wait(self, seconds):
        self.page.wait_for_timeout(int(seconds * 1000))

    def fresh(self):
        self.js("window.debug.start()")
        self.wait(0.3)
        self.js("window.debug.setBrains(60)")

    def state(self):
        return self.js("window.debug.state()")

    def humans(self):
        return self.js("window.debug.humans()")

    def crowd(self, x, y, n=5):
        for i in range(n):
            self.js(f"window.debug.spawnHuman('local', {x + 14 * i}, {y}, 0)")

    def building(self, kind):
        return next((b for b in self.js("window.debug.buildings()") if b.get("id") == kind), None)


def tier1(g):
    out = {}
    g.fresh()
    out["starts"] = g.state()["screen"] == "playing", g.state()["screen"]
    before = g.state()["brains"]
    g.wait(1.0)
    out["meter drains"] = g.state()["brains"] < before, f"{before:.1f} -> {g.state()['brains']:.1f}"
    g.wait(6.0)
    out["humans arrive"] = len(g.humans()) >= 1, f"{len(g.humans())} on the map"
    g.fresh()
    g.js("window.debug.teleport(900, 600)")
    g.js("window.debug.spawnHuman('local', 700, 600, 0)")
    g.wait(0.7)
    seen = [h["state"] for h in g.humans() if h["y"] > 300]
    out["seen from the front"] = "alarmed" in seen, str(seen)
    g.fresh()
    g.js("window.debug.teleport(600, 600)")
    g.js("window.debug.spawnHuman('local', 630, 600, 0)")
    g.wait(0.2)
    eaten = g.state()["brainsEaten"]
    g.page.keyboard.down("Space")
    g.wait(0.15)
    g.page.keyboard.up("Space")
    g.wait(1.4)
    out["grab from behind eats"] = g.state()["brainsEaten"] == eaten + 1, f"eaten {eaten} -> {g.state()['brainsEaten']}"
    g.fresh()
    g.js("window.debug.teleport(180, 200)")
    g.wait(0.2)
    junk = sum(g.state()["junk"].values())
    g.page.keyboard.down("e")
    g.wait(1.6)
    g.page.keyboard.up("e")
    out["search gives junk"] = sum(g.state()["junk"].values()) == junk + 1, f"junk {junk} -> {sum(g.state()['junk'].values())}"
    g.fresh()
    placed = g.js("window.debug.place('box', 10, 12)")
    g.js("window.debug.teleport(1100, 650)")
    g.js("window.debug.spawnHuman('local', 420, 500, 0)")
    g.wait(0.6)
    states = [h["state"] for h in g.humans() if abs(h["x"] - 420) < 30 and abs(h["y"] - 500) < 30]
    out["box trap holds"] = bool(placed) and "trapped" in states, f"placed {placed}, {states}"
    return out


def passers(g, seconds, hit):
    """Parks the zombie out of sight and lets the game's own walkers come by; True once hit() is."""
    g.js("window.debug.teleport(1200, 690)")
    seen = set()
    for _ in range(int(seconds / 5)):
        g.wait(5.0)
        g.js("window.debug.setBrains(80)")
        seen |= {h["state"] for h in g.humans()}
        if hit(seen):
            return True, sorted(seen)
    return False, sorted(seen)


def hold(g, key, seconds):
    g.page.keyboard.down(key)
    g.wait(seconds)
    g.page.keyboard.up(key)


def tier2(g):
    out = {}
    g.fresh()
    placed = g.js("window.debug.place('wifi', 16, 5)")
    ok, seen = passers(g, 45, lambda s: s & {"lured", "using"})
    out["wifi lures"] = bool(placed) and ok, f"placed {placed}, states seen {seen}"
    g.fresh()
    placed = g.js("window.debug.place('fridge', 14, 12)")
    g.js("window.debug.giveBrains(1)")
    g.js("window.debug.teleport(580, 536)")
    g.wait(0.2)
    hold(g, "e", 0.4)
    g.wait(0.4)
    stored = (g.building("fridge") or {}).get("stored")
    eaten = g.state()["brainsEaten"]
    hold(g, "Space", 0.2)
    g.wait(1.0)
    out["fridge stores and feeds"] = bool(placed) and stored == 1 and g.state()["brainsEaten"] == eaten + 1, \
        f"placed {placed}, stored {stored}, eaten {eaten} -> {g.state()['brainsEaten']}"
    g.fresh()
    placed = g.js("window.debug.place('banana', 14, 5)")
    ok, seen = passers(g, 60, lambda s: "trapped" in s or (g.building("banana") or {}).get("holding"))
    out["banana stand pits one"] = bool(placed) and ok, f"placed {placed}, states seen {seen}, {g.building('banana')}"
    g.fresh()
    placed = g.js("window.debug.place('station', 10, 5)")
    ok, seen = passers(g, 60, lambda s: "husk" in s or ((g.building("station") or {}).get("stored") or 0) >= 1)
    out["station leaves a husk"] = bool(placed) and ok, f"placed {placed}, states seen {seen}, {g.building('station')}"
    g.fresh()
    fridge = g.js("window.debug.place('fridge', 14, 12)")
    placed = g.js("window.debug.place('puppies', 20, 6)")
    ok, seen = passers(g, 90, lambda s: "dragged" in s or ((g.building("fridge") or {}).get("stored") or 0) >= 1)
    out["puppies deliver"] = bool(placed and fridge) and ok, f"placed {placed}, states seen {seen}, {g.building('fridge')}"
    return out


def tier3(g):
    out = {}
    g.fresh()
    g.js("window.debug.teleport(1200, 680)")
    g.js("window.debug.setHeat(6)")
    level = g.state().get("heatLevel")
    g.wait(26.0)
    g.js("window.debug.setBrains(60)")
    law = g.js("window.debug.law ? window.debug.law() : []")
    out["heat brings a cop"] = level == 1 and len(law) >= 1, f"level {level}, law {[l.get('kind') for l in law]}"
    g.fresh()
    g.js("window.debug.teleport(800, 600)")
    g.js("window.debug.spawnLaw('cop', 600, 600, 0)")
    before = g.state()["brains"]
    g.wait(4.0)
    drop = before - g.state()["brains"]
    out["cop shoots on sight"] = drop >= 10, f"brains fell {drop:.1f} in 4 s"
    return out


def tier4(g):
    out = {}
    g.fresh()
    placed = g.js("window.debug.place('wall', 17, 15)")
    g.js("window.debug.teleport(780, 620)")
    g.js("window.debug.spawnHuman('local', 620, 620, 0)")
    g.wait(0.7)
    states = [h["state"] for h in g.humans() if abs(h["x"] - 620) < 30 and abs(h["y"] - 620) < 30]
    out["wall blocks sight"] = bool(placed) and states and "alarmed" not in states, f"placed {placed}, {states}"
    g.fresh()
    placed = [g.js(f"window.debug.place('{kind}', {col}, 13)") for kind, col in (("pool", 2), ("flamingo", 6), ("sign", 8), ("tombstone", 10))]
    out["decor places"] = all(placed), str(placed)
    return out


def main():
    root, top = sys.argv[1], int(sys.argv[2])
    report = {}
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(serve(root))
        page.wait_for_timeout(2000)
        game = Game(page)
        for n, checks in ((1, tier1), (2, tier2), (3, tier3), (4, tier4)):
            if n > top:
                break
            try:
                report[f"tier {n}"] = {name: {"ok": bool(ok), "detail": detail} for name, (ok, detail) in checks(game).items()}
            except Exception as e:
                report[f"tier {n}"] = {"probe failed": {"ok": False, "detail": str(e)[:300]}}
        report["page errors"] = errors[:5]
        browser.close()
    print(json.dumps(report))


if __name__ == "__main__":
    main()
