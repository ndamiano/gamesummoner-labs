"""The mockup-first chain for the ask in <label>/ask.txt, a private run on Flash-Next.
`plan`: the model names the genre and lists what every game of it has, the ask's own actions kept
as plain mechanics (genre.txt); the run's ask is the genre so no stage sees the theme; the process
planner cuts the stages. `build`: the staged build of the generic game. `look`: one call writes a
short naming note and a description of a screenshot of the finished game (look.txt), and
Qwen-Image paints that screenshot, seed 0, nobody picks. `picture`: one `change` build whose first
message is note.txt plus the mockup as an image. `compare`: screenshots of the game as built are
taken and a second `change` build is shown the mockup beside them (compare.txt). `all` runs the
five. Copies of the game are kept in <label>/generic, /picture and /compare. Starts the GPU runner
itself. Needs run.py up.
usage: build.py plan|build|look|picture|compare|all <label>"""
import base64
import io
import json
import socket
import subprocess
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tier-chain"))
import tiers
from config import llm_models
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from maestro.codegen import build_chain, build_steps, design, stages
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState
from tools.execution_context import run_scope

MAX_TOKENS = design.MAX_TOKENS
PLAN_SYSTEM = (HERE.parent.parent / "src" / "maestro" / "codegen" / "prompts" / "stage" / "plan_system.txt").read_text(encoding="utf-8").strip()
LOOK = ("dimension", "camera", "tone", "art style", "palette", "typography", "music", "sound effects style")
BUILT = ("# 2. HOW IT IS BUILT\n\nThe way a person would build it with an AI: a crappy framework first, "
         "plain shapes with their generic names on them, until it plays; then every feature in the list, "
         "one at a time, each whole and working before the next; then the levels, the two ends and the "
         "balance. No theme, no art, no name: a theme is put on afterwards by someone else. Pick the "
         "numbers yourself and keep them plain.")


def ask_llm(run, system, body):
    conn = get_connector(llm_models.seat("design", True))
    for _ in range(2):
        text = design._reply_text(conn.generate_with_tools(
            MessageBuilder(system).add_user(body).build(), [], max_tokens=MAX_TOKENS)).strip()
        if text:
            return text
    raise SystemExit("the model came back empty twice")


def prompt(name, **slots):
    text = (HERE / f"{name}.txt").read_text(encoding="utf-8")
    for key, value in slots.items():
        text = text.replace("{" + key + "}", value)
    return text


def genre_of(spec):
    first = spec.split("# 0. CONCEPT", 1)[1].strip().split("\n", 1)[0]
    return first


def plan(source):
    ask = (source / "ask.txt").read_text(encoding="utf-8").strip()
    run = create_run(tiers.store.list_users()[0].id, private=True)
    tiers.games.charge_game(run, 0, 3 * tiers.MICROS_PER_CREDIT)
    open_ask(run, ask)
    (source / "run.txt").write_text(run + "\n", encoding="utf-8")
    run_dir = RunState(run).run_dir
    tiers.log(f"run {run}: {ask}")
    services = tiers.Services(source)
    services.ensure()
    build_id = tiers.games.create_build(run, kind="design")
    tiers.games.build_started(build_id)
    try:
        with run_scope(run, build_id):
            decided = design._decide(ask)
            state = design.tiered_state(decided)
            (source / "decisions.txt").write_text(state + "\n", encoding="utf-8")
            genre = ask_llm(run, design._SYSTEM, prompt("genre", ask=ask))
            (source / "genre.md").write_text(genre + "\n", encoding="utf-8")
            tiers.log(f"genre:\n{genre}")
            spec = f"{genre.strip()}\n\n{BUILT}\n"
            (source / "design.md").write_text(spec, encoding="utf-8")
            generic = f"a generic game of this genre, with no theme: {genre_of(spec)}"
            asking = (HERE / "plan_process.txt").read_text(encoding="utf-8").format(
                budget=stages.PLAN_BUDGET, design=spec)
            for attempt in range(3):
                text = ask_llm(run, PLAN_SYSTEM, asking)
                (source / f"plan-raw-{attempt}.txt").write_text(text, encoding="utf-8")
                try:
                    parsed = stages.parse(text)
                    break
                except (ValueError, KeyError) as e:
                    tiers.log(f"plan attempt {attempt} did not parse: {e!r}")
            else:
                raise SystemExit("the plan did not parse three times")
            cut = [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
                    "reads": stages.match_reads(s.get("reads") or [], spec)} for s in parsed]
        tiers.games.build_finished(build_id, "succeeded", steps=3)
    except BaseException:
        tiers.games.build_finished(build_id, "failed", steps=3)
        services.stop()
        raise
    plan = {"stages": cut, "budgets": stages.budgets(len(cut)), "attempts": {}, "before": {}}
    (source / stages.PLAN_FILE).write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    shutil.copy2(source / "design.md", spec_path(run_dir))
    stages._save(run_dir, plan)
    open_ask(run, generic)
    set_prompt(run, design._request(generic))
    services.stop()
    tiers.log(f"{len(cut)} stages: " + " · ".join(s["name"] for s in cut))
    for i, s in enumerate(cut, 1):
        tiers.log(f"{i:2d}. {s['name']}: {s['stage']}\n    done: {s['done']}\n    reads: {s['reads']}")


def wait_and_record(source, run, services, began, name):
    run_dir = RunState(run).run_dir
    status = tiers.wait(run, services)
    checks = stages.load(run_dir)["attempts"] if name == "build" else {}
    entry = {"run": run, "status": status, "minutes": round((time.time() - began) / 60),
             "stage checks": {k: [(a["attempt"], a["boots"], len(a["errors"])) for a in v] for k, v in checks.items()},
             **tiers.summary(run)}
    (source / f"{name}.json").write_text(json.dumps(entry, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tiers.log(f"{name} ended {status} after {entry['minutes']} min: {json.dumps(entry, ensure_ascii=False)}")


def build(source):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    services = tiers.Services(source)
    services.ensure()
    if build_chain.kickoff(run, kind="build", designed=True) is None:
        raise SystemExit(f"the build would not start, game is {tiers.games.game(run)}")
    began = time.time()
    try:
        wait_and_record(source, run, services, began, "build")
    finally:
        services.stop()


def keep(run, source, name):
    shutil.copytree(game_dir(RunState(run).run_dir), source / name, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git"))


def picture_part(path):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    im.thumbnail((1024, 1024))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=80)
    return {"type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()}}


def shots(run, source, tag):
    from playwright.sync_api import sync_playwright
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1"],
                              cwd=game_dir(RunState(run).run_dir), stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    title, play = source / f"{tag}_title.png", source / f"{tag}_play.png"
    try:
        time.sleep(1)
        with sync_playwright() as p:
            browser = p.chromium.launch(args=["--use-gl=swiftshader"])
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            page.goto(f"http://127.0.0.1:{port}/index.html")
            page.wait_for_timeout(3000)
            page.screenshot(path=str(title))
            for _ in range(3):
                page.keyboard.press("Enter")
                page.wait_for_timeout(1000)
            page.mouse.click(640, 400)
            page.wait_for_timeout(8000)
            page.screenshot(path=str(play))
            browser.close()
    finally:
        server.terminate()
    return [title, play]


def change(source, note, images, tag):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    (source / f"{tag}_note.md").write_text(note, encoding="utf-8")
    content = [{"type": "text", "text": note}] + [picture_part(p) for p in images]
    original = build_steps._seed

    def seeded(tools, cursor, rd):
        if cursor.kind == "change" and cursor.history:
            cursor.history[0]["content"] = content
            tiers.log(f"attached {len(images)} picture(s) to the change note")
        return original(tools, cursor, rd)

    build_steps._seed = seeded
    services = tiers.Services(source)
    services.ensure()
    try:
        if build_chain.kickoff(run, kind="change", note=note) is None:
            raise SystemExit(f"the change would not start, game is {tiers.games.game(run)}")
        wait_and_record(source, run, services, time.time(), tag)
    finally:
        build_steps._seed = original
        services.stop()
    keep(run, source, tag)


def look(source):
    ask = (source / "ask.txt").read_text(encoding="utf-8").strip()
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    spec = (source / "design.md").read_text(encoding="utf-8")
    state = "\n".join(line for line in (source / "decisions.txt").read_text(encoding="utf-8").splitlines()
                      if line.split(":")[0] in LOOK)
    keep(run, source, "generic")
    services = tiers.Services(source)
    services.ensure()
    build_id = tiers.games.create_build(run, kind="design")
    tiers.games.build_started(build_id)
    try:
        with run_scope(run, build_id):
            text = ask_llm(run, design._SYSTEM, prompt("look", ask=ask, spec=spec, state=state))
        tiers.games.build_finished(build_id, "succeeded", steps=1)
    except BaseException:
        tiers.games.build_finished(build_id, "failed", steps=1)
        raise
    finally:
        services.stop()
    (source / "look.md").write_text(text + "\n", encoding="utf-8")
    names, mockup = text.split("# MOCKUP", 1)
    names = names.split("# NOTE", 1)[1].strip()
    (source / "names.md").write_text(names + "\n", encoding="utf-8")
    (source / "mockup_prompt.txt").write_text(mockup.strip() + "\n", encoding="utf-8")
    tiers.log(f"look:\n{text}")
    sys.path.insert(0, str(HERE.parent / "worldclaw"))
    from worldclaw.backends.images import ImageModel
    began = time.time()
    ImageModel("http://localhost:5001/upstream/comfyui_auto").generate(
        mockup.strip(), source / "mockup.png", width=1280, height=720, steps=30, seed=100,
        negative="photo, 3d render, blurry, watermark, realistic, dark, cluttered, tiny text")
    tiers.log(f"mockup painted in {time.time() - began:.0f}s")
    open_ask(run, ask)
    set_prompt(run, design._request(ask))


def picture(source):
    names = (source / "names.md").read_text(encoding="utf-8").strip()
    change(source, prompt("note", names=names), [source / "mockup.png"], "picture")


def compare(source):
    run = (source / "run.txt").read_text(encoding="utf-8").strip()
    now = shots(run, source, "picture")
    change(source, prompt("compare"), [source / "mockup.png", *now], "compare")
    shots(run, source, "compare")


STEPS = {"plan": plan, "build": build, "look": look, "picture": picture, "compare": compare}

if __name__ == "__main__":
    for name in (STEPS if sys.argv[1] == "all" else [sys.argv[1]]):
        tiers.log(f"== {name}")
        STEPS[name](HERE / sys.argv[2])
