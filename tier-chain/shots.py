"""Screenshots of a built zombie game in the same four states every time, so two versions of its
looks can be put side by side: the title, the first second of a run, a staged yard with every
building, civilian and lawman on it, and the build panel.
usage: shots.py <game dir> <output folder>"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from probe import serve

PLACES = [("box", 9, 6), ("wifi", 5, 7), ("banana", 20, 6), ("station", 23, 11), ("puppies", 4, 12),
          ("fridge", 14, 12), ("donuts", 24, 8), ("mailbox", 10, 9), ("gnome", 11, 13), ("door", 15, 10),
          ("pool", 16, 13), ("flamingo", 21, 13), ("sign", 13, 9), ("tombstone", 20, 14)]
WALLS = [12, 13, 14, 16, 17, 18, 19]
HUMANS = [("local", 300, 150, 0), ("jogger", 700, 140, 3.14), ("phoneGuy", 500, 270, 1.57), ("shopper", 950, 310, -1.57)]
LAW = [("cop", 880, 230, 2.4), ("police", 1040, 150, 3.1), ("guard", 1130, 430, 3.1)]


def stage(page):
    page.evaluate("""([places, walls, humans, law]) => {
        const d = window.debug;
        d.start(); d.seed(7); d.setBrains(85);
        for (const t of ['cardboard', 'rope', 'scrap', 'gizmo']) d.giveJunk(t, 4);
        d.giveBrains(2);
        for (const [id, c, r] of places) d.place(id, c, r);
        for (const c of walls) d.place('wall', c, 10);
        d.teleport(660, 560);
        for (const h of humans) d.spawnHuman(...h);
        d.setHeat(21);
        for (const l of law) d.spawnLaw(...l);
        d.setBrains(85);
    }""", [PLACES, WALLS, HUMANS, LAW])


def main():
    root, out = sys.argv[1], Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(serve(root))
        page.wait_for_function("window.debug && window.debug.start", timeout=15000)
        page.wait_for_timeout(800)
        page.screenshot(path=str(out / "1-title.png"))
        page.evaluate("window.debug.start()")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(out / "2-start.png"))
        stage(page)
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / "3-yard.png"))
        page.evaluate("window.debug.input('build', true)")
        page.wait_for_timeout(150)
        page.evaluate("window.debug.input('build', false)")
        page.wait_for_timeout(400)
        page.screenshot(path=str(out / "4-panel.png"))
        browser.close()
    print(f"{out}: 4 shots, {len(errors)} page errors {errors[:3]}")


if __name__ == "__main__":
    main()
