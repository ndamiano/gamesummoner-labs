"""One playtest-refine pass on a finished stage-chain game: a first-time player session on it, a
director turning what the player ran into into at most three changes, one change build on a copy
with those changes as its note (prod path, prod gates after), then the same player session on the
result. One JSON line per pass in results.jsonl; the sessions, screenshots and notes under
/var/tmp/playtest-refine/<label>/.

    venv/bin/python labs/playtest-refine/refine.py <stage run id> <label> [v2]

v2: the director names goals, what the player saw and how to reproduce it, never a cause, and
the note asks the builder to reproduce each problem and find its cause before changing code.
"""

import base64
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
SB = REPO / "labs" / "section-budget"
sys.path[:0] = [str(REPO / "src"), str(SB), str(REPO / "labs" / "vision-build")]

import branch
import stage
import stage_look
from db import games
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from maestro.codegen import build_chain, play_gate
from maestro.codegen.error_gate import VIEWPORT, _serve
from maestro.codegen.run import _await_build
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState

OUT = Path("/var/tmp/playtest-refine")
RESULTS = LAB / "results.jsonl"
TURNS = 30
SETTLE_MS = 1500
REQUEST_CHARS = 8000
CHANGE_STEPS = 40


def _prompt(name: str) -> str:
    return (LAB / "prompts" / name).read_text(encoding="utf-8")


def _section(design: str, start: str) -> str:
    i = design.find(start)
    if i < 0:
        return ""
    j = design.find("\n# ", i + 1)
    return design[i:j if j > 0 else len(design)]


def request_for(rid: str) -> str:
    design = spec_path(RunState(rid).run_dir).read_text(encoding="utf-8")
    ask = (RunState(rid).read_spec() or {}).get("ask") or ""
    return (f"Asked for: {ask}\n\n" + _section(design, "# 7. UX"))[:REQUEST_CHARS]


def _parse(text: str) -> Optional[Dict]:
    data = play_gate._parse_json(text)
    if data is None or not stage_look._valid(data.get("action")):
        return None
    return data


def session(gdir: Path, request: str, out: Path) -> Dict:
    """TURNS turns of free play, then the player's report."""
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    system = _prompt("player_turn.txt").format(request=request, **VIEWPORT)
    history: List[Dict] = []
    turns: List[Dict] = []
    errors: List[str] = []
    with _serve(gdir) as base_url, sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-gl=angle", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport=VIEWPORT)
        page.route("**/*", lambda route: route.continue_()
                   if route.request.url.startswith(f"{base_url}/") else route.abort())
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(f"{base_url}/index.html", timeout=15_000, wait_until="load")
        page.wait_for_timeout(SETTLE_MS)
        png = page.screenshot()
        for n in range(1, TURNS + 1):
            (out / f"turn{n:02d}.png").write_bytes(png)
            history.append({"role": "user", "content": [
                {"type": "text", "text": f"Turn {n}, the game now:" if n == 1 else
                 f"Turn {n}: three frames left to right, during your last action, just after it, and settled:"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,"
                                                    + base64.b64encode(png).decode()}}]})
            turn = answer = None
            for _ in range(3):
                answer = play_gate._ask(system, history, max_tokens=4000)
                turn = _parse(answer) if answer else None
                if turn is not None:
                    break
            if turn is None:
                break
            history.append({"role": "assistant", "content": answer})
            turns.append(turn)
            png = stage_look._act_watching(page, turn["action"])
        browser.close()
    history.append({"role": "user", "content": _prompt("player_report.txt")})
    report = {}
    for _ in range(3):
        report = play_gate._parse_json(play_gate._ask(system, history, max_tokens=6000) or "") or {}
        if report.get("observations") or report.get("reached"):
            break
    result = {"turns": turns, "page_errors": sorted(set(errors))[:10],
              "observations": report.get("observations") or [], "reached": report.get("reached")}
    (out / "session.json").write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result


def direct(rid: str, observations: List[Dict], turns: List[Dict], v2: bool = False) -> List[Dict]:
    design = spec_path(RunState(rid).run_dir).read_text(encoding="utf-8")
    if v2:
        prompt_file = v2 if isinstance(v2, str) else "director_v2.txt"
        pressed = "\n".join(f"{i}. {play_gate._describe_action(t.get('action'))}: {t.get('noticed', '')}"
                            for i, t in enumerate(turns, 1))
        prompt = _prompt(prompt_file).format(
            observations=json.dumps(observations, indent=1, ensure_ascii=False), turns=pressed,
            design=design)
    else:
        prompt = _prompt("director.txt").format(
            observations=json.dumps(observations, indent=1, ensure_ascii=False), design=design)
    reply = get_connector("qwen-flash-next").generate_with_tools(
        MessageBuilder("You are the lead developer on a game team.").add_user(prompt).build(), [])
    text = ((reply.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    return (play_gate._parse_json(text) or {}).get("changes") or []


def note_of(changes: List[Dict], v2: bool = False) -> str:
    if v2:
        return ("A first-time player hit these problems. For each one, first make it happen yourself "
                "with the steps given and find its cause in the code; then change the game so it does "
                "what the goal says.\n\n" + "\n\n".join(
                    f"{i}. Goal: {c.get('goal', '').strip()} (design {c.get('section', '').strip()})\n"
                    f"   What the player saw: {c.get('seen', '').strip()}\n"
                    f"   To make it happen: {c.get('repro', '').strip()}"
                    for i, c in enumerate(changes, 1)))
    return "\n".join(f"{i}. {c.get('change', '').strip()} (design {c.get('section', '').strip()})"
                     for i, c in enumerate(changes, 1))


def copy_of(source: str) -> str:
    head = subprocess.run(["git", f"--git-dir={stage.RUNS / source / 'game.git'}", "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True).stdout.strip()
    n = json.loads((stage.RUNS / source / "stage.json").read_text())["n"]
    rid = branch.branch(source, head, n)
    (stage.RUNS / rid / "stage.json").unlink()
    return rid


def main(source: str, label: str, version: str = "") -> None:
    v2 = version == "v2"
    out = OUT / label
    t0 = time.time()
    request = request_for(source)
    before = session(game_dir(RunState(source).run_dir), request, out / "before")
    print(f"before: {len(before['turns'])} turns, {len(before['observations'])} observations, "
          f"reached: {before['reached']}", flush=True)
    for o in before["observations"]:
        print("  -", o.get("problem"), flush=True)
    changes = direct(source, before["observations"], before["turns"], v2)
    note = note_of(changes, v2)
    (out / "note.txt").write_text(note, encoding="utf-8")
    print("changes:\n" + note, flush=True)
    rid = copy_of(source)
    build_chain.kickoff(rid, kind="change", note=note, max_steps=CHANGE_STEPS,
                        designed=games.game(rid)["stage"] == "designing")
    built = _await_build(rid)
    print(f"change build {rid}: ok={built.ok} steps={built.steps}", flush=True)
    while (games.game(rid) or {}).get("status") == "running":
        time.sleep(30)
    gates = {name: json.loads((RunState(rid).run_dir / name).read_text())
             for name in ("error_gate.json", "play_gate.json") if (RunState(rid).run_dir / name).exists()}
    after = session(game_dir(RunState(rid).run_dir), request, out / "after")
    print(f"after: {len(after['turns'])} turns, {len(after['observations'])} observations, "
          f"reached: {after['reached']}", flush=True)
    for o in after["observations"]:
        print("  -", o.get("problem"), flush=True)
    row = {"label": label, "version": version or "v1", "source": source, "refined": rid, "seconds": round(time.time() - t0),
           "change_steps": built.steps, "gates": {k: v.get("rounds") for k, v in gates.items()},
           "before": {"observations": before["observations"], "reached": before["reached"],
                      "page_errors": before["page_errors"]},
           "changes": changes,
           "after": {"observations": after["observations"], "reached": after["reached"],
                     "page_errors": after["page_errors"]}}
    with RESULTS.open("a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"refine done {label} {rid}", flush=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
