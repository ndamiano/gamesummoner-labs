"""Screenshot a built game after a few inputs: shot.py <game dir> <out.png> [keys...]."""
import functools, http.server, sys, threading
from playwright.sync_api import sync_playwright
game, out, keys = sys.argv[1], sys.argv[2], sys.argv[3:]
h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=game); h.log_message = lambda *a: None
s = http.server.ThreadingHTTPServer(("127.0.0.1", 0), h); threading.Thread(target=s.serve_forever, daemon=True).start()
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 960, "height": 640}); errs = []
    p.on("pageerror", lambda e: errs.append(str(e)))
    p.goto(f"http://127.0.0.1:{s.server_port}/index.html"); p.wait_for_timeout(1500)
    for k in keys:
        if k.startswith("hold:"):
            _, key, ms = k.split(":"); p.keyboard.down(key); p.wait_for_timeout(int(ms)); p.keyboard.up(key)
        elif k.startswith("js:"):
            p.evaluate(k[3:]); p.wait_for_timeout(300)
        elif k.startswith("wait:"):
            p.wait_for_timeout(int(k[5:]))
        else:
            p.keyboard.press(k); p.wait_for_timeout(400)
    p.screenshot(path=out); b.close()
print(out, errs[:3])
