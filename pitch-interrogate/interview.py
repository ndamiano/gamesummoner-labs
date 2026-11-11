"""A pitcher and an interrogator in place of the decide step, both the local Flash-Next. The pitcher
reads the ask and pitches one game. The interrogator questions it a round at a time until it ends the
interview, then writes the decisions sheet. Prod's write prompt, unchanged, writes the design from
that sheet where it would have had the decided state. With --page the pitcher first writes a page
for itself, pitches from it and answers from it; the interrogator never sees the page. With --shown
the interrogator is handed that page in place of the pitch. With --cracks it is handed the page and
asks only about where the page would leave a builder stuck, without guesses. --from takes the page
and pitch another label already wrote. With --verbs the page is written with the mechanics-curation
systems list in hand and its verbs are systems from it; a sheet line that names one carries its
definition. With --firstday the pitcher is asked, after the interview, which parts must be in on the
first day, and the interrogator has the answer when it writes the sheet. With --decided the systems
come from prod's decide step on the mechanics-curation list (JEV, as the control was decided), the
page is written with only those in hand, and the sheet bands its parts under JEV's bands.
usage: interview.py [--page | --shown | --cracks] [--verbs | --decided] [--firstday] [--from label] <label> <ask>"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "mechanics-curation"))
from lib.paths import bootstrap

bootstrap()
from config.settings_manager import settings_manager
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from llm_clients.wire import chat_body_for_wire
from maestro.codegen import design

HERE = Path(__file__).resolve().parent
SYSTEMS = HERE.parent / "mechanics-curation" / "systems-tight.json"
BANDS = ("core mechanics", "supporting mechanics", "extra mechanics")
ENTRY = "qwen-flash-next"
ROUNDS = 6
OVER = "INTERVIEW OVER"
FIRST = "Game prompt:"


def prompt(name, **slots):
    return (HERE / name).read_text(encoding="utf-8").format(**slots).strip()


def post(messages, out, name):
    body = get_connector(ENTRY).build_llm_job(messages, [], design.MAX_TOKENS)[0]["body"]
    url = settings_manager.get_settings()["local"]["llama_swap"]["url"].rstrip("/") + "/v1/chat/completions"
    for attempt in range(design.RETRIES + 1):
        request = urllib.request.Request(url, json.dumps(chat_body_for_wire(body)).encode(),
                                         {"Content-Type": "application/json"})
        started = time.time()
        result = json.load(urllib.request.urlopen(request, timeout=7200))
        (out / f"{name}-raw-{attempt}.json").write_text(
            json.dumps({"seconds": time.time() - started, "messages": messages, "response": result}, indent=1),
            encoding="utf-8")
        print(f"[{time.strftime('%H:%M:%S')}] {name}: {time.time() - started:.0f}s, {result.get('usage')}", flush=True)
        text = design._reply_text(result).strip()
        if text:
            return text
    raise SystemExit(f"{name}: came back empty")


def turn(role, text):
    return {"role": role, "content": text}


def systems():
    return json.loads(SYSTEMS.read_text(encoding="utf-8"))


def decided(ask, out, source):
    from write import decide
    kept = source / "decisions.json" if source else out / "decisions.json"
    if not kept.exists():
        kept.write_text(json.dumps(decide(ask, systems()), indent=1, ensure_ascii=False), encoding="utf-8")
    state = design.tiered_state(json.loads(kept.read_text(encoding="utf-8")))
    (out / "decided.txt").write_text(state, encoding="utf-8")
    bands = {}
    for line in state.splitlines():
        band, _, names = line.partition(": ")
        if band in BANDS:
            bands[band] = [n for n in names.split(", ") if n != "none"]
    return bands


def described(sheet):
    known, band, lines = systems(), None, []
    for line in sheet.splitlines():
        label = line.partition(":")[0].strip().lower()
        if label in BANDS:
            band = label
        elif line and not line.startswith("-"):
            band = None
        name, _, text = line.removeprefix("- ").partition(":")
        if band and line.startswith("- ") and name.strip().lower() in known and text.strip():
            text = text.strip()
            line = f"- {name.strip().lower()}: {known[name.strip().lower()]} In this game, {text[0].lower() + text[1:]}"
        lines.append(line)
    return "\n".join(lines)


def said(folder, name):
    raw = sorted(folder.glob(f"{name}-raw-*.json"))[-1]
    return design._reply_text(json.loads(raw.read_text(encoding="utf-8"))["response"]).strip()


def interview(ask, out, page, shown, cracks, source, verbs=False, firstday=False, jev=False):
    pitcher = prompt("pitcher_page.txt" if page else "pitcher.txt")
    interrogator = prompt("interrogator_cracks.txt" if cracks else "interrogator.txt")
    bands = decided(ask, out, source) if jev else {}
    if jev:
        known = systems()
        rows = "\n".join(f"- {name} ({band.split()[0]}): {known[name]}" for band, names in bands.items() for name in names)
        opening = prompt("page_decided.txt", ask=ask, systems=rows)
    elif verbs:
        rows = "\n".join(f"- {name}: {text}" for name, text in systems().items())
        opening = prompt("page_verbs.txt", ask=ask, systems=rows)
    else:
        opening = prompt("page.txt" if page else "ask.txt", ask=ask)
    theirs, held = [turn("user", opening)], ""
    if page:
        held = said(source, "page") if source else post(MessageBuilder(pitcher).extend(theirs).build(), out, "page")
        (out / "page.md").write_text(f"# The pitcher's page\n\nAsk: `{ask}`\n\n{held}\n", encoding="utf-8")
        theirs += [turn("assistant", held), turn("user", prompt("pitch_from_page.txt"))]
    pitch = said(source, "pitch") if source else post(MessageBuilder(pitcher).extend(theirs).build(), out, "pitch")
    theirs.append(turn("assistant", pitch))
    (out / "pitch.md").write_text(f"# The pitch\n\nAsk: `{ask}`\n\n{pitch}\n", encoding="utf-8")
    mine = [turn("user", prompt("paged.txt", ask=ask, page=held) if shown else prompt("pitched.txt", ask=ask, pitch=pitch))]
    if shown:
        pitcher = prompt("pitcher_cracks.txt" if cracks else "pitcher_shown.txt")
    log = ["# The interview", ""]
    for n in range(1, ROUNDS + 1):
        asked = post(MessageBuilder(interrogator).extend(mine).build(), out, f"round{n}-interrogator")
        mine.append(turn("assistant", asked))
        log += [f"## Round {n}", "", "### Interrogator", "", asked, ""]
        (out / "interview.md").write_text("\n".join(log), encoding="utf-8")
        if OVER in asked:
            break
        theirs.append(turn("user", asked))
        answered = post(MessageBuilder(pitcher).extend(theirs).build(), out, f"round{n}-pitcher")
        theirs.append(turn("assistant", answered))
        mine.append(turn("user", answered))
        log += ["### Pitcher", "", answered, ""]
        (out / "interview.md").write_text("\n".join(log), encoding="utf-8")
    asking = prompt("sheet.txt", ask=ask)
    if jev:
        said_bands = "\n".join(f"{band}: {', '.join(names) or 'none'}" for band, names in bands.items())
        asking = prompt("decided_said.txt", bands=said_bands) + "\n\n" + asking
    if firstday:
        theirs.append(turn("user", prompt("firstday.txt")))
        answer = post(MessageBuilder(pitcher).extend(theirs).build(), out, "firstday-pitcher")
        theirs.append(turn("assistant", answer))
        log += ["## First day", "", "### Pitcher", "", answer, ""]
        (out / "interview.md").write_text("\n".join(log), encoding="utf-8")
        asking = prompt("firstday_said.txt", answer=answer) + "\n\n" + asking
    mine.append(turn("user", asking))
    sheet = post(MessageBuilder(interrogator).extend(mine).build(), out, "sheet")
    lines = [line for line in sheet.splitlines() if not line.startswith("```")]
    at = next((i for i, line in enumerate(lines) if line.startswith(FIRST)), None)
    sheet = "\n".join(lines[at:] if at is not None else [f"{FIRST} {ask}"] + lines).strip()
    return described(sheet) if verbs or jev else sheet


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", action="store_true")
    parser.add_argument("--shown", action="store_true")
    parser.add_argument("--cracks", action="store_true")
    parser.add_argument("--verbs", action="store_true")
    parser.add_argument("--decided", action="store_true")
    parser.add_argument("--firstday", action="store_true")
    parser.add_argument("--from", dest="source")
    parser.add_argument("label")
    parser.add_argument("ask", nargs="+")
    args = parser.parse_args()
    ask, out = " ".join(args.ask), HERE / args.label
    out.mkdir(exist_ok=True)
    state = out / "state.txt"
    if not state.exists():
        shown = args.shown or args.cracks
        state.write_text(interview(ask, out, args.page or shown, shown, args.cracks,
                                   HERE / args.source if args.source else None, args.verbs, args.firstday,
                                   args.decided), encoding="utf-8")
    sheet, spec = state.read_text(encoding="utf-8"), ""
    for n in range(design.CONTINUATIONS + 1):
        spec += post(design._messages(ask, sheet, spec), out, f"design-{n}")
        if not design.missing_sections(spec):
            break
    (out / "design.md").write_text(spec, encoding="utf-8")
    print(f"design: {len(spec)} chars, missing sections {design.missing_sections(spec)}", flush=True)


if __name__ == "__main__":
    main()
