"""Record the ask being typed into the local GameSummoner create page, ending on the Summon button."""
import sys
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/ai-agent-test/src")
from auth import store
from playwright.sync_api import sync_playwright

from capture import Capture

ask, out = sys.argv[1], Path(sys.argv[2])
token = store.issue_token(store.list_users()[0].id)
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": 960, "height": 640})
    ctx.add_init_script(f"localStorage.setItem('maestro_token', {token!r})")
    page = ctx.new_page()
    cap = Capture(page, out)
    page.goto("http://127.0.0.1:8000/new", wait_until="networkidle")
    cap.start()
    page.wait_for_timeout(1200)
    box = page.locator("textarea")
    box.click()
    page.wait_for_timeout(400)
    box.press_sequentially(ask, delay=55)
    page.wait_for_timeout(700)
    button = page.get_by_role("button", name="Summon it")
    button.hover()
    page.wait_for_timeout(900)
    page.wait_for_timeout(300)
    frames = cap.stop()
    browser.close()
print(out, frames, "frames")
