"""Shows Flash-Next screenshots of a built game, one at a time, and asks what looks wrong (look.txt).
Screenshots land in the output folder; the model's answers land beside this file.
usage: look.py <run id> [label]"""
import base64
import json
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import OUTPUT, bootstrap

bootstrap()
from config.settings_manager import settings_manager
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from llm_clients.wire import chat_body_for_wire
from maestro.codegen import design
from maestro.codegen.error_gate import VIEWPORT, _serve
from maestro.codegen.staging import game_dir
from maestro.state import RunState

HERE = Path(__file__).resolve().parent
ENTRY = "qwen-flash-next"
MAX_TOKENS = 16000
PLACES = [("box", 9, 6), ("wifi", 5, 7), ("banana", 20, 6), ("station", 23, 11), ("puppies", 4, 12),
          ("fridge", 14, 12), ("donuts", 24, 8), ("mailbox", 10, 9), ("gnome", 11, 13), ("door", 15, 10),
          ("pool", 16, 13), ("flamingo", 21, 13), ("sign", 13, 9), ("tombstone", 20, 14)]
WALLS = [12, 13, 14, 16, 17, 18, 19]
HUMANS = [("local", 300, 150, 0), ("jogger", 700, 140, 3.14), ("phoneGuy", 500, 270, 1.57), ("shopper", 950, 310, -1.57)]
LAW = [("cop", 880, 230, 2.4), ("police", 1040, 150, 3.1), ("guard", 1130, 430, 3.1)]
YARD = """([places, walls, humans, law]) => {
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
}"""
MENU = """() => {
    const d = window.debug;
    d.start();
    for (const t of ['cardboard', 'rope', 'scrap', 'gizmo']) d.giveJunk(t, 5);
    d.input('build', true);
}"""
STATES = {
    "title": "The title screen, before a run starts.",
    "start": "One second into a run. The player is the zombie. Nothing has been built yet.",
    "yard": ("A yard set up to show everything at once. The player is the zombie. Placed in the yard: Box on a Stick, "
             "Free WiFi Sign, Banana Stand, Brain Rot Cleaning Station, Free Puppies, Fridge, Free Donuts, Mailbox, "
             "Garden Gnome, a row of Walls with a Door, Fetid Pool, Dead Flamingo, Crooked Sign and Tombstone. On screen "
             "too: four passers-by (a Local, a Jogger, a Phone Guy and a Shopper), a Cop, a Police officer and a Guard, "
             "and the junk spots the player searches."),
    "menu": "A run with the build menu open on the right. The player has 5 of each kind of junk.",
}


def shots(root, out):
    out.mkdir(parents=True, exist_ok=True)
    with _serve(root) as base, sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT)
        page.goto(f"{base}/index.html")
        page.wait_for_timeout(2500)
        page.screenshot(path=str(out / "title.png"))
        page.evaluate("window.debug.start()")
        page.wait_for_timeout(1200)
        page.screenshot(path=str(out / "start.png"))
        page.evaluate(YARD, [PLACES, WALLS, HUMANS, LAW])
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / "yard.png"))
        page.evaluate(MENU)
        page.wait_for_timeout(200)
        page.evaluate("window.debug.input('build', false)")
        page.wait_for_timeout(500)
        page.screenshot(path=str(out / "menu.png"))
        browser.close()


def ask(system, state, png):
    image = "data:image/png;base64," + base64.b64encode(png.read_bytes()).decode()
    turn = {"role": "user", "content": [{"type": "text", "text": f"The game now: {state}"},
                                        {"type": "image_url", "image_url": {"url": image}}]}
    body = get_connector(ENTRY).build_llm_job(MessageBuilder(system).extend([turn]).build(), [], MAX_TOKENS)[0]["body"]
    url = settings_manager.get_settings()["local"]["llama_swap"]["url"].rstrip("/") + "/v1/chat/completions"
    request = urllib.request.Request(url, json.dumps(chat_body_for_wire(body)).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(request, timeout=3600))


def main():
    run = sys.argv[1]
    state = RunState(run)
    label = sys.argv[2] if len(sys.argv) > 2 else ""
    folder = OUTPUT / "builder-eyes" / run / label
    shots(game_dir(state.run_dir), folder)
    system = (HERE / "look.txt").read_text(encoding="utf-8").format(ask=state.read_spec()["ask"], **VIEWPORT)
    out = HERE / run / label
    out.mkdir(parents=True, exist_ok=True)
    found = {}
    for name, line in STATES.items():
        started = time.time()
        result = ask(system, line, folder / f"{name}.png")
        (out / f"{name}-raw.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
        text = design._reply_text(result)
        try:
            found[name] = json.loads(text[text.index("{"):text.rindex("}") + 1])
        except ValueError:
            found[name] = {"unparsed": text}
        print(f"{name}: {time.time() - started:.0f}s, {result.get('usage')}, "
              f"{len(found[name].get('problems', []))} problems", flush=True)
    (out / "found.json").write_text(json.dumps(found, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"shots in {folder}, answers in {out}")


if __name__ == "__main__":
    main()
