"""Replays recorded player sessions and measures what a fixed 1.5 s settle buys: after each action,
when would an adaptive settle (no debug-state key changing beyond those an idle game changes on
its own, and frame motion within the idle game's) have stopped, and how far is its frame from the 1.5 s frame. Browser only, no model calls.

    venv/bin/python labs/vision-build/settle_probe.py > /var/tmp/vision-build/settle_probe.jsonl
"""

import io
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(REPO / "src"), str(REPO / "labs" / "vision-build"), str(REPO / "labs" / "section-budget")]

from PIL import Image, ImageChops, ImageStat

from maestro.codegen import play_gate
from maestro.codegen.error_gate import VIEWPORT, _serve
from maestro.codegen.staging import game_dir
from maestro.state import RunState
import stage_look

CAP_MS = 1500
POLL_MS = 100
FRAME_EPS = 1.0
FRAME_ONLY = '--frame-only' in sys.argv
SESSIONS = {
    "/var/tmp/playtest-refine/pv2-farm-g": ["ed92ae3ee08f", "7f29ff26e42d", "22f19e8b91ee", "db5ea5a5ff6f"],
    "/var/tmp/playtest-refine/pv2-catdefense": ["0bf97699dcd0", "31787bf9944e", "1230270af93f", "faedce8786c0"],
    "/var/tmp/playtest-refine/pv2-skatemall": ["bd5ed8523fe3", "ff2340f0be3a", "e67baf5c2d99", "ebbc5b2ff2d2"],
}


def _small(png: bytes) -> Image.Image:
    return Image.open(io.BytesIO(png)).convert("L").resize((160, 90))


def _diff(a: Image.Image, b: Image.Image) -> float:
    return ImageStat.Stat(ImageChops.difference(a, b)).mean[0]


def _ambient(page) -> tuple:
    """Keys and frame motion an idle game shows with no input."""
    keys, diffs = set(), []
    prev_state, prev_img = stage_look._state(page), _small(page.screenshot())
    for _ in range(10):
        page.wait_for_timeout(POLL_MS)
        state, img = stage_look._state(page), _small(page.screenshot())
        keys |= {c.split(":")[0] for c in stage_look._changes(prev_state, state)}
        diffs.append(_diff(img, prev_img))
        prev_state, prev_img = state, img
    return keys, max(diffs) if diffs else 0.0


def _settle(page, ambient=(set(), 0.0)) -> dict:
    keys, motion = ambient
    t0 = time.monotonic()
    prev_state, prev_img, stop = stage_look._state(page), _small(page.screenshot()), None
    stop_img = None
    while (time.monotonic() - t0) * 1000 < CAP_MS:
        page.wait_for_timeout(POLL_MS)
        state, img = stage_look._state(page), _small(page.screenshot())
        moved = {c.split(":")[0] for c in stage_look._changes(prev_state, state)} - keys
        if stop is None and (FRAME_ONLY or not moved) and _diff(img, prev_img) < max(FRAME_EPS, 1.5 * motion):
            stop, stop_img = (time.monotonic() - t0) * 1000, img
        prev_state, prev_img = state, img
    final = prev_img
    return {"stop_ms": round(stop) if stop is not None else None,
            "gap_to_final": round(_diff(stop_img, final), 2) if stop_img is not None else None,
            "has_state": prev_state is not None}


def replay(rid: str, actions: list) -> None:
    from playwright.sync_api import sync_playwright
    with _serve(game_dir(RunState(rid).run_dir)) as base_url, sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-gl=angle", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport=VIEWPORT)
        page.route("**/*", lambda route: route.continue_()
                   if route.request.url.startswith(f"{base_url}/") else route.abort())
        page.goto(f"{base_url}/index.html", timeout=15_000, wait_until="load")
        page.wait_for_timeout(CAP_MS)
        ambient = _ambient(page)
        for n, action in enumerate(actions, 1):
            act = play_gate._action_of(action)
            if act is None:
                continue
            play_gate._act(page, act)
            print(json.dumps({"run": rid, "turn": n, "action": action, **_settle(page, ambient)}), flush=True)
        browser.close()


def main() -> None:
    for root, rids in SESSIONS.items():
        for r, rid in enumerate(rids):
            session = Path(root) / f"round{r}" / "s0" / "session.json"
            if not session.exists():
                continue
            turns = json.loads(session.read_text()).get("turns") or []
            replay(rid, [t.get("action") for t in turns][:20])


if __name__ == "__main__":
    main()
