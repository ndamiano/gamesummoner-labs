"""Record a built game being played from a JSON plan of inputs: [["wait", ms], ["tap", key], ["hold", key, ms], ["down", key], ["up", key], ["click", x, y], ["js", code]]."""
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

from capture import Capture

game, plan, out = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3])
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(game))
handler.log_message = lambda *a: None
server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--use-gl=angle", "--use-angle=swiftshader", "--autoplay-policy=no-user-gesture-required"])
    ctx = browser.new_context(viewport={"width": 960, "height": 640})
    page = ctx.new_page()
    cap = Capture(page, out)
    cap.start()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(f"http://127.0.0.1:{server.server_port}/index.html", wait_until="load")
    for step in plan:
        op = step[0]
        if op == "wait":
            page.wait_for_timeout(step[1])
        elif op == "tap":
            page.keyboard.press(step[1])
        elif op == "hold":
            page.keyboard.down(step[1]); page.wait_for_timeout(step[2]); page.keyboard.up(step[1])
        elif op == "down":
            page.keyboard.down(step[1])
        elif op == "up":
            page.keyboard.up(step[1])
        elif op == "move":
            page.mouse.move(step[1], step[2], steps=step[3] if len(step) > 3 else 12)
        elif op == "mdown":
            page.mouse.down()
        elif op == "mup":
            page.mouse.up()
        elif op == "click":
            page.mouse.click(step[1], step[2])
        elif op == "js":
            page.evaluate(step[1])
    frames = cap.stop()
    browser.close()
server.shutdown()
print(out, frames, "frames, page errors:", errors[:5])
