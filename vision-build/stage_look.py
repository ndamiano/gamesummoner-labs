"""V3, a look per stage: a vision player gets TURNS turns to reach and see what the finished stage
promised (its done line), then says shown, missing or unclear. After each action it sees a strip
of three frames, during the action, just after it and once it settles, so a jump or a hit that is
over within a second is still on screen; it can hold two keys at once (a chord)."""

import base64
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
sys.path[:0] = [str(REPO / "src"), str(REPO / "labs" / "section-budget")]

import stage
from maestro.codegen import play_gate
from maestro.codegen.error_gate import VIEWPORT, _serve
from maestro.codegen.staging import game_dir
from maestro.state import RunState

TURNS = 16
SETTLE_MS = 1500
FAST = os.environ.get("LAB_SETTLE") == "fast"
FAST_FLOOR_MS, FAST_CAP_MS, FAST_POLL_MS, STILL = 200, 600, 100, 1.0


def _thumb(png: bytes):
    from PIL import Image
    return Image.open(io.BytesIO(png)).convert("L").resize((160, 90))


def settle(page) -> None:
    """SETTLE_MS, or with LAB_SETTLE=fast a 200 ms floor that runs on to 600 ms only while the
    frame is still visibly changing (labs/vision-build/settle_probe.py measured the split)."""
    if not FAST:
        page.wait_for_timeout(SETTLE_MS)
        return
    from PIL import ImageChops, ImageStat
    page.wait_for_timeout(FAST_FLOOR_MS)
    prev, waited = _thumb(page.screenshot()), FAST_FLOOR_MS
    while waited < FAST_CAP_MS:
        page.wait_for_timeout(FAST_POLL_MS)
        waited += FAST_POLL_MS
        img = _thumb(page.screenshot())
        if ImageStat.Stat(ImageChops.difference(img, prev)).mean[0] < STILL:
            return
        prev = img


def _prompt(name: str) -> str:
    return (LAB / "prompts" / name).read_text(encoding="utf-8")


def done_line(arm: str, n: int) -> str:
    text = (Path(stage.LAB) / arm / f"{n}.txt").read_text(encoding="utf-8")
    return text.split("\n---\n")[1].strip() if "\n---\n" in text else text.strip()


def _strip(frames: List[bytes]) -> bytes:
    from PIL import Image
    imgs = [Image.open(io.BytesIO(f)).convert("RGB") for f in frames]
    for im in imgs:
        im.thumbnail((640, 360))
    w, h = imgs[0].size
    sheet = Image.new("RGB", (w * len(imgs) + 8 * (len(imgs) - 1), h), (0, 0, 0))
    for i, im in enumerate(imgs):
        sheet.paste(im, (i * (w + 8), 0))
    buf = io.BytesIO()
    sheet.save(buf, "PNG")
    return buf.getvalue()


def _key(name) -> str:
    k = play_gate._KEY_NAMES.get(str(name).strip().lower(), str(name).strip())
    return k.lower() if len(k) == 1 and k.isalpha() else k


def _pressable(page, key: str) -> bool:
    try:
        page.keyboard.down(key)
        return True
    except Exception:
        return False


def _act_watching(page, action) -> bytes:
    """Do the action and return the three-frame strip: during, just after, settled. A key the
    browser does not know is skipped, as the play gate skips it."""
    frames = []
    debug = _debug_call(action)
    if debug:
        try:
            page.evaluate("([m, a]) => { const g = window.__game; if (g && typeof g[m] === 'function') g[m](...a); }",
                          [debug[0], debug[1]])
        except Exception:
            pass
        frames.append(page.screenshot())
    elif isinstance(action, dict) and isinstance(action.get("chord"), dict):
        keys = [_key(k) for k in (action["chord"].get("keys") or [])][:3]
        seconds = min(3.0, max(0.5, float(action["chord"].get("seconds", 1) or 1)))
        held = [k for k in keys if _pressable(page, k)]
        page.wait_for_timeout(seconds * 500)
        frames.append(page.screenshot())
        page.wait_for_timeout(seconds * 500)
        for k in reversed(held):
            page.keyboard.up(k)
    else:
        kind, what = play_gate._action_of(action)
        if kind == "click":
            page.mouse.click(*what)
            page.wait_for_timeout(150)
            frames.append(page.screenshot())
        elif kind == "hold":
            name, seconds = what
            down = _pressable(page, name)
            page.wait_for_timeout(seconds * 500)
            frames.append(page.screenshot())
            page.wait_for_timeout(seconds * 500)
            if down:
                page.keyboard.up(name)
        else:
            down = _pressable(page, what)
            page.wait_for_timeout(120)
            frames.append(page.screenshot())
            if down:
                page.keyboard.up(what)
    page.wait_for_timeout(100 if FAST else 250)
    frames.append(page.screenshot())
    if FAST:
        settle(page)
    else:
        page.wait_for_timeout(SETTLE_MS - 250)
    frames.append(page.screenshot())
    return _strip(frames)


def _debug_call(action):
    if isinstance(action, dict) and isinstance(action.get("debug"), dict):
        call = action["debug"].get("call")
        args = action["debug"].get("args") or []
        if isinstance(call, str) and call.isidentifier() and isinstance(args, list):
            return call, args
    return None


def _valid(action) -> bool:
    if _debug_call(action):
        return True
    if isinstance(action, dict) and isinstance(action.get("chord"), dict):
        return bool(action["chord"].get("keys"))
    return play_gate._action_of(action) is not None


_STATE_JS = """() => {
  const g = window.__game;
  if (!g) return null;
  const f = typeof g.state === "function" ? g.state : typeof g.getState === "function" ? g.getState : null;
  try { return JSON.parse(JSON.stringify(f ? f.call(g) : g, (k, v) => typeof v === "function" ? undefined : v)); }
  catch (e) { return null; }
}"""
_NOISE = re.compile(r"time|frame|step|tick|elapsed|clock|fps|seed|events|log|ms$|dt$", re.I)


def _flat(value, path: str = "", out: Dict = None) -> Dict:
    out = {} if out is None else out
    if len(out) > 600:
        return out
    if isinstance(value, dict):
        for k, v in value.items():
            _flat(v, f"{path}.{k}" if path else str(k), out)
    elif isinstance(value, list):
        if all(not isinstance(v, (dict, list)) for v in value) and len(value) <= 4:
            out[path] = value
        else:
            out[path + ".length"] = len(value)
            for i, v in enumerate(value[:6]):
                _flat(v, f"{path}[{i}]", out)
    else:
        out[path] = value
    return out


def _changes(before: Dict, after: Dict) -> List[str]:
    if before is None or after is None:
        return []
    a, b = _flat(before), _flat(after)
    changed = []
    for k in sorted(set(a) | set(b)):
        if _NOISE.search(k) or a.get(k) == b.get(k):
            continue
        x, y = a.get(k), b.get(k)
        if isinstance(x, float) and isinstance(y, float) and abs(x - y) < 1e-3:
            continue
        changed.append(f"{k}: {json.dumps(x)[:40]} -> {json.dumps(y)[:40]}")
    return changed


def _state(page):
    try:
        return page.evaluate(_STATE_JS)
    except Exception:
        return None


def trace_text(trace: List[Dict]) -> str:
    """The inputs of a look and what the game's debug state did after each, for a builder to replay."""
    lines = []
    for t in trace:
        if t["changed"]:
            what = "; ".join(t["changed"][:6])
        elif t.get("screen"):
            what = "the screen changed but nothing in window.__game's state did (the debug state does not expose it)"
        elif "screen" in t:
            what = "neither the screen nor window.__game's state changed"
        else:
            what = "nothing in window.__game's state changed"
        lines.append(f"turn {t['turn']}, {json.dumps(t['action'])}: {what}")
    return "\n".join(lines)


def look(rid: str, done: str, out: Path, turns: int = TURNS, trace: bool = False,
         teleport: bool = False) -> Dict:
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    system = None if teleport else _prompt("stage_look_turn.txt").format(done=done, **VIEWPORT)
    history: List[Dict] = []
    steps: List[Dict] = []
    answered: List[bool] = []
    with _serve(game_dir(RunState(rid).run_dir)) as base_url, sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-gl=angle", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport=VIEWPORT)
        page.route("**/*", lambda route: route.continue_()
                   if route.request.url.startswith(f"{base_url}/") else route.abort())
        page.goto(f"{base_url}/index.html", timeout=15_000, wait_until="load")
        page.wait_for_timeout(SETTLE_MS)
        if teleport:
            api = page.evaluate("() => window.__game ? Object.keys(window.__game).filter(k => "
                                "typeof window.__game[k] === 'function') : []")
            system = _prompt("stage_look_turn_teleport.txt").format(
                done=done, api=", ".join(api[:120]) or "(none)", **VIEWPORT)
        png = page.screenshot()
        for n in range(1, turns + 1):
            (out / f"turn{n:02d}.png").write_bytes(png)
            history.append({"role": "user", "content": [
                {"type": "text", "text": f"Turn {n}, the game now:" if n == 1 else
                 f"Turn {n}: three frames left to right, during your last action, just after it, and settled:"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,"
                                                    + base64.b64encode(png).decode()}}]})
            turn = answer = None
            for _ in range(3):
                answer = play_gate._ask(system, history, max_tokens=4000)
                turn = play_gate._parse_json(answer or "")
                if turn and _valid(turn.get("action")):
                    break
                turn = None
            if turn is None:
                break
            history.append({"role": "assistant", "content": answer})
            before = _state(page) if trace else None
            shot = _thumb(page.screenshot())
            png = _act_watching(page, turn["action"])
            from PIL import ImageChops, ImageStat
            moved = ImageStat.Stat(ImageChops.difference(shot, _thumb(page.screenshot()))).mean[0] >= STILL
            answered.append(moved)
            if trace:
                steps.append({"turn": n, "action": turn["action"], "changed": _changes(before, _state(page)),
                              "screen": moved})
        png = page.screenshot()
        history.append({"role": "user", "content": [
            {"type": "text", "text": "The game at the end of the look:"},
            {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(png).decode()}},
            {"type": "text", "text": _prompt("stage_look_verdict.txt")}]})
        browser.close()
    verdict = {}
    for _ in range(3):
        verdict = play_gate._parse_json(play_gate._ask(system, history, max_tokens=6000) or "") or {}
        if verdict.get("verdict") in ("shown", "missing", "unclear"):
            break
    result = {"verdict": verdict.get("verdict") if verdict.get("verdict") in ("shown", "missing", "unclear")
              else "unclear", "why": str(verdict.get("why") or "")}
    result["responsive"] = round(sum(answered) / len(answered), 2) if answered else 0.0
    if trace:
        result["trace"] = steps[-10:]
    (out / "verdict.json").write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result
