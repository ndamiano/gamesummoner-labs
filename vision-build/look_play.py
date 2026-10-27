"""maestro.codegen.play with a picture: the same run, and before the browser closes a 640x360 JPEG
of the page as the script left it, written to the path the request names."""

from __future__ import annotations

import io
import json
import sys
import time
from pathlib import Path

from maestro.codegen import error_gate
from maestro.codegen.play import _BOOT_MS, _START, _TURN, _late


def _shot(page, path: str) -> None:
    from PIL import Image
    img = Image.open(io.BytesIO(page.screenshot(type="png"))).convert("RGB")
    img.thumbnail((640, 360))
    img.save(path, "JPEG", quality=60)


def run(root: Path, js: str, seconds: float, shot: str) -> dict:
    from playwright.sync_api import sync_playwright
    deadline = time.monotonic() + seconds
    errors, blocked, console = [], [], []
    done = None
    with error_gate._serve(root) as base_url, sync_playwright() as pw:
        browser = error_gate._browser(pw)
        try:
            page = error_gate._open(browser, base_url, errors, blocked, settle=False)
            if page is None:
                return {"ok": False, "error": "the page did not load: " + errors[0]["message"]}
            page.on("console", lambda m: console.append(m.text))
            try:
                page.wait_for_function("window.__game", timeout=_BOOT_MS)
            except Exception:
                _shot(page, shot)
                return {"ok": False, "error": "window.__game never appeared within 10 s of load "
                        "— install it in the page before play() can drive the game",
                        "errors": errors, "console": console[-50:], "screenshot": shot}
            page.evaluate(_START, js)
            while True:
                left = deadline - time.monotonic()
                if left <= 0:
                    _shot(page, shot)
                    return {**_late(seconds, errors, console), "screenshot": shot}
                try:
                    page.wait_for_function(_TURN, timeout=left * 1000)
                except Exception:
                    _shot(page, shot)
                    return {**_late(seconds, errors, console), "screenshot": shot}
                done = page.evaluate("window.__play_done")
                if done is not None:
                    break
                req = page.evaluate("window.__press_q[0]")
                page.keyboard.down(req["key"])
                page.wait_for_timeout(float(req["ms"]))
                page.keyboard.up(req["key"])
                page.evaluate("window.__press_q.shift().res(true)")
            _shot(page, shot)
        finally:
            browser.close()
    if "error" in done:
        return {"ok": False, "error": "the script threw: " + done["error"],
                "errors": errors, "console": console[-50:], "screenshot": shot}
    out = {"ok": True, "result": done["value"], "errors": errors, "console": console[-50:],
           "screenshot": shot}
    if blocked:
        out["blocked"] = sorted(set(blocked))[:10]
    return out


def main() -> int:
    req = json.load(sys.stdin)
    try:
        out = run(Path(req["root"]), req["js"], float(req["seconds"]), req["shot"])
    except Exception as e:
        out = {"ok": False, "error": f"{type(e).__name__}: {e}"}
    json.dump(out, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
