"""The builder sees its game: for a stage whose stage.json has "look", or any run with a look.flag
file in its run directory, play() also captures the page as the script left it, and the turn
after a play() opens with that picture. One picture is in the conversation at a time; the one
before is replaced by a line saying it was there. With "auto" in look.flag (or "look": "auto" in
stage.json), a turn that edits files without playing gets its last play() script run again and that
picture instead. Import after stage.install(), so this wrapper is outermost and the stage arm's
turns-left line still lands on the tool result."""

import base64
import itertools
import json
import os
import signal
import subprocess
import sys
from pathlib import Path

import re

import stage
from maestro.codegen import build_chain, build_steps

WRITE = re.compile(r"\b(write_file|edit_file|write_text)\(|open\([^)]*['\"][wa]")
from maestro.codegen.staging import game_dir

LAB = Path(__file__).resolve().parent
SRC = LAB.parents[1] / "src"
SEEN = "[a picture of the page after an earlier play() was here]"
_pending: dict = {}
_last_js: dict = {}
_n = itertools.count()


def _look_play(run_dir: Path):
    root = game_dir(run_dir)
    shots = Path(run_dir) / "looks"

    def play(js: str, seconds: float = 20, **_) -> dict:
        seconds = max(1.0, min(float(seconds), 60.0))
        _last_js[str(run_dir)] = (js, seconds)
        shots.mkdir(exist_ok=True)
        shot = str(shots / f"{os.getpid()}-{next(_n)}.jpg")
        proc = subprocess.Popen([sys.executable, str(LAB / "look_play.py")],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={**os.environ, "PYTHONPATH": str(SRC)}, start_new_session=True)
        try:
            out, err = proc.communicate(json.dumps({"root": str(root), "js": js, "seconds": seconds,
                                                    "shot": shot}).encode(), timeout=seconds + 25)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
            return {"ok": False, "error": f"the page stopped responding; play was killed after "
                    f"{int(seconds)} s — a script or a game loop that never yields"}
        if proc.returncode != 0 or not out:
            return {"ok": False, "error": "play could not run: " + err.decode(errors="replace")[-400:]}
        result = json.loads(out)
        if Path(shot).exists():
            _pending[str(run_dir)] = shot
        result.pop("screenshot", None)
        return result
    return play


def _mode(run_dir) -> str:
    want = (stage.stage_of(run_dir) or {}).get("look")
    flag = Path(run_dir) / "look.flag"
    if flag.exists():
        want = flag.read_text().strip() or True
    return "auto" if want == "auto" else ("on" if want else "")


def _tools_wrapper(original):
    def build_tools(rs, build_id):
        tools = original(rs, build_id)
        if _mode(rs.run_dir):
            inner = _look_play(rs.run_dir)

            def play(**kw):
                try:
                    return inner(**kw)
                except Exception as e:
                    return {"ok": False, "error": f"{type(e).__name__}: {e}"}
            tools["play"] = play
        return tools
    return build_tools


def _apply_wrapper(original):
    def apply(tools, cursor, tc, run_dir):
        for m in cursor.history:
            if m.get("role") == "user" and isinstance(m.get("content"), list) and \
                    any(p.get("type") == "image_url" for p in m["content"]):
                m["content"] = SEEN
        finished = original(tools, cursor, tc, run_dir)
        shot = _pending.pop(str(run_dir), None)
        caption = "The page as it looked when your last play() ended:"
        if not shot and not finished and _mode(run_dir) == "auto" and str(run_dir) in _last_js:
            try:
                code = json.loads(tc["function"]["arguments"]).get("code", "")
            except (ValueError, KeyError, TypeError):
                code = ""
            if WRITE.search(code):
                js, seconds = _last_js[str(run_dir)]
                tools["play"](js=js, seconds=seconds)
                shot = _pending.pop(str(run_dir), None)
                caption = "You changed files without playing. Your last play() script, run again on the changed game, left the page like this:"
        if shot and not finished:
            data = base64.b64encode(Path(shot).read_bytes()).decode()
            cursor.history.append({"role": "user", "content": [
                {"type": "text", "text": caption},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + data}}]})
        return finished
    return apply


build_chain.build_tools = _tools_wrapper(build_chain.build_tools)
build_steps._apply = _apply_wrapper(build_steps._apply)
