"""Vision UX loop: a tour of the game's screens, a vision review of how they look and read against
the design's visual spec and UX sections, a director turning the review into at most three
changes, one change build on a copy (prod path, prod gates), then the tour and review again. A
round the comparison calls worse is dropped. One JSON line per round in results.jsonl; tours,
frames and notes under /var/tmp/vision-ux/<label>/.

    venv/bin/python labs/vision-ux/ux.py <run id> <label> <rounds>

With UX_LOOK=1 or auto (under labs/vision-build/serve_v.py) the change builds see their page after
each play(), and with auto after each edit too. With UX_PAIRED=1 each round replays round 0's
tour inputs on the new build and one call judges before/after pairs of the same screens, instead
of a fresh tour and a comparison of two issue lists.
"""

import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Dict, List

LAB = Path(__file__).resolve().parent
REPO = LAB.parents[1]
sys.path[:0] = [str(REPO / "labs" / "playtest-refine")]

import loop
import refine
from db import games
from maestro.codegen import build_chain, play_gate
from maestro.codegen.error_gate import VIEWPORT, _serve
from maestro.codegen.run import _await_build
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState

OUT = Path("/var/tmp/vision-ux")
RESULTS = LAB / "results.jsonl"
TURNS = 24
FRAMES = 8
SETTLE_MS = 1500


def _prompt(name: str) -> str:
    return (LAB / "prompts" / name).read_text(encoding="utf-8")


def _ask(prompt_text: str, content=None) -> Dict:
    message = {"role": "user", "content": content + [{"type": "text", "text": prompt_text}]} \
        if content else {"role": "user", "content": prompt_text}
    reply = refine.get_connector("qwen-flash-next").generate_with_tools(
        [{"role": "system", "content": "You are the lead developer on a game team."}, message], [])
    text = ((reply.get("choices") or [{}])[0].get("message") or {}).get("content") or ""
    return play_gate._parse_json(text) or {}


def design_sections(rid: str) -> str:
    design = spec_path(RunState(rid).run_dir).read_text(encoding="utf-8")
    return refine._section(design, "# 3. VISUAL SPEC") + "\n" + refine._section(design, "# 7. UX")


def tour(gdir: Path, request: str, out: Path) -> Dict:
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    system = _prompt("tour_turn.txt").format(request=request, **VIEWPORT)
    history: List[Dict] = []
    turns: List[Dict] = []
    with _serve(gdir) as base_url, sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-gl=angle", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport=VIEWPORT)
        page.route("**/*", lambda route: route.continue_()
                   if route.request.url.startswith(f"{base_url}/") else route.abort())
        page.goto(f"{base_url}/index.html", timeout=15_000, wait_until="load")
        page.wait_for_timeout(SETTLE_MS)
        for n in range(1, TURNS + 1):
            png = page.screenshot()
            path = out / f"turn{n:02d}.png"
            path.write_bytes(png)
            history.append({"role": "user", "content": [
                {"type": "text", "text": f"Turn {n}, the game now:"},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64,"
                                                    + base64.b64encode(png).decode()}}]})
            turn = answer = None
            for _ in (1, 2):
                answer = play_gate._ask(system, history, max_tokens=4000)
                turn = refine._parse(answer) if answer else None
                if turn is not None:
                    break
            if turn is None:
                break
            turn["frame"] = str(path)
            history.append({"role": "assistant", "content": answer})
            turns.append(turn)
            play_gate._act(page, play_gate._action_of(turn["action"]))
            refine.stage_look.settle(page)
        browser.close()
    (out / "turns.json").write_text(json.dumps(turns, indent=1, ensure_ascii=False))
    return {"turns": turns}


def frames_of(turns: List[Dict]) -> List[Dict]:
    """The last frame of each distinct screen, in the order the tour first met them."""
    order, last = [], {}
    for t in turns:
        key = str(t.get("screen") or "").strip().lower()
        if key not in last:
            order.append(key)
        last[key] = t
    picked = [last[k] for k in order]
    return picked[:FRAMES] if len(picked) <= FRAMES else picked[:FRAMES - 1] + [picked[-1]]


def replay(gdir: Path, turns: List[Dict], out: Path) -> List[str]:
    """The same inputs as an earlier tour, on another build: the frame before each input, saved."""
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    frames = []
    with _serve(gdir) as base_url, sync_playwright() as pw:
        browser = pw.chromium.launch(args=["--use-gl=angle", "--enable-unsafe-swiftshader"])
        page = browser.new_page(viewport=VIEWPORT)
        page.route("**/*", lambda route: route.continue_()
                   if route.request.url.startswith(f"{base_url}/") else route.abort())
        page.goto(f"{base_url}/index.html", timeout=15_000, wait_until="load")
        page.wait_for_timeout(SETTLE_MS)
        for n, t in enumerate(turns, 1):
            path = out / f"turn{n:02d}.png"
            path.write_bytes(page.screenshot())
            frames.append(str(path))
            play_gate._act(page, play_gate._action_of(t["action"]))
            refine.stage_look.settle(page)
        browser.close()
    return frames


def paired(rid: str, turns: List[Dict], after_frames: List[str]) -> Dict:
    """One call over before/after pairs of the tour's distinct screens: verdict and the new build's issues."""
    index = {t["frame"]: i for i, t in enumerate(turns)}
    content = []
    for t in frames_of(turns):
        i = index[t["frame"]]
        if i >= len(after_frames):
            continue
        for label, path in (("before", t["frame"]), ("after", after_frames[i])):
            content += [{"type": "text", "text": f"Screen: {t.get('screen')}, {label}"},
                        {"type": "image_url", "image_url": {"url": "data:image/png;base64,"
                                                            + base64.b64encode(Path(path).read_bytes()).decode()}}]
    return _ask(_prompt("ux_paired.txt").format(design=design_sections(rid)), content)


def review(rid: str, turns: List[Dict]) -> List[Dict]:
    content = []
    for t in frames_of(turns):
        png = Path(t["frame"]).read_bytes()
        content += [{"type": "text", "text": f"Screen: {t.get('screen')}"},
                    {"type": "image_url", "image_url": {"url": "data:image/png;base64,"
                                                        + base64.b64encode(png).decode()}}]
    return _ask(_prompt("ux_review.txt").format(design=design_sections(rid)), content).get("issues") or []


def direct(rid: str, issues: List[Dict], turns: List[Dict]) -> List[Dict]:
    design = spec_path(RunState(rid).run_dir).read_text(encoding="utf-8")
    moved = "\n".join(f"{i}. on {t.get('screen')}: {play_gate._describe_action(t.get('action'))}"
                      for i, t in enumerate(turns, 1))
    return _ask(_prompt("ux_director.txt").format(
        observations=json.dumps(issues, indent=1, ensure_ascii=False), turns=moved,
        design=design)).get("changes") or []


def main(source: str, label: str, rounds: int) -> None:
    out = OUT / label
    request = refine.request_for(source)
    current = source
    seen = tour(game_dir(RunState(source).run_dir), request, out / "round0")
    issues = review(source, seen["turns"])
    (out / "round0" / "issues.json").write_text(json.dumps(issues, indent=1, ensure_ascii=False))
    print(f"round 0: {len(seen['turns'])} tour turns, {len(issues)} issues", flush=True)
    for i in issues:
        print(f"  - [{i.get('screen')}] {i.get('problem')}", flush=True)
    for r in range(1, rounds + 1):
        t0 = time.time()
        changes = direct(current, issues, seen["turns"])
        note = refine.note_of(changes, v2=True).replace(
            "A first-time player hit these problems. For each one, first make it happen yourself "
            "with the steps given and find its cause in the code;",
            "A reviewer looked at the game's screens. For each note, first reach that screen "
            "yourself with the steps given and find what draws it in the code;")
        (out / f"note{r}.txt").write_text(note, encoding="utf-8")
        rid = loop.copy_any(current) if r > 1 or not (refine.stage.RUNS / current / "stage.json").exists() \
            else refine.copy_of(current)
        if os.environ.get("UX_LOOK"):
            (RunState(rid).run_dir / "look.flag").write_text(os.environ["UX_LOOK"])
        build_chain.kickoff(rid, kind="change", note=note, max_steps=refine.CHANGE_STEPS,
                            designed=games.game(rid)["stage"] == "designing")
        built = _await_build(rid)
        while (games.game(rid) or {}).get("status") == "running":
            time.sleep(30)
        if os.environ.get("UX_PAIRED"):
            frames = replay(game_dir(RunState(rid).run_dir), seen["turns"], out / f"round{r}")
            judged = paired(rid, seen["turns"], frames)
            after_issues = judged.get("issues") or []
            after = seen
        else:
            after = tour(game_dir(RunState(rid).run_dir), request, out / f"round{r}")
            after_issues = review(rid, after["turns"])
            judged = _ask(_prompt("ux_compare.txt").format(
                before=json.dumps(issues, ensure_ascii=False), after=json.dumps(after_issues, ensure_ascii=False)))
        (out / f"round{r}" / "issues.json").write_text(json.dumps(after_issues, indent=1, ensure_ascii=False))
        print(f"round {r}: build {rid} steps={built.steps}; {len(after_issues)} issues; judged "
              f"{judged.get('verdict')}: {judged.get('why')}", flush=True)
        for i in after_issues:
            print(f"  - [{i.get('screen')}] {i.get('problem')}", flush=True)
        with RESULTS.open("a") as f:
            f.write(json.dumps({"label": label, "round": r, "source": current, "refined": rid,
                                "seconds": round(time.time() - t0), "change_steps": built.steps,
                                "changes": changes, "before": issues, "after": after_issues,
                                "judged": judged}, ensure_ascii=False) + "\n")
        if judged.get("verdict") == "better":
            current, issues = rid, after_issues
            if not os.environ.get("UX_PAIRED"):
                seen = after
    print(f"ux done {label} {current}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
