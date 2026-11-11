"""Builds the tiers of a design one after another on a copy of a built game. For each tier: one
plan call with the code map in hand (plan_tier.txt), prod's staged chain on that plan, the headless
probe, one fix build if a tier 1 check has broken, and a kept copy of the game. It starts the GPU
runner itself and restarts it when it dies or stalls. Needs run.py up.
usage: tiers.py <source run id> <first tier> <last tier>"""
import json
import shutil
import sqlite3
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import OUTPUT, REPO, bootstrap

bootstrap()
from auth import store
from billing.packages import MICROS_PER_CREDIT
from config.settings_manager import settings_manager
from db import games
from llm_clients.connector import get_connector
from llm_clients.message_builder import MessageBuilder
from llm_clients.wire import chat_body_for_wire
from maestro.codegen import build_chain, code_map, design, snapshots, stages
from maestro.codegen.run import create_run, open_ask, set_prompt
from maestro.codegen.staging import game_dir, spec_path
from maestro.state import RunState

HERE = Path(__file__).resolve().parent
ENTRY = "qwen-flash-next"
BUDGET = 35
FIX_STEPS = 60
STALL = 20 * 60
PYTHON = str(REPO / "venv" / "bin" / "python")
RUNNER = [PYTHON, "scripts/local_gpu.py", "auto", "--idle-exit", "86400", "--ready-timeout", "600"]
DB = f"file:{REPO / 'data' / 'platform.db'}?mode=ro"


def log(text):
    print(f"[{time.strftime('%H:%M:%S')}] {text}", flush=True)


def fork(source):
    src = RunState(source)
    ask = src.read_spec()["ask"]
    run = create_run(store.list_users()[0].id, private=True)
    games.charge_game(run, 0, MICROS_PER_CREDIT)
    open_ask(run, ask)
    dst = RunState(run).run_dir
    shutil.copy2(spec_path(src.run_dir), spec_path(dst))
    shutil.copytree(game_dir(src.run_dir), game_dir(dst), dirs_exist_ok=True)
    shutil.copytree(src.run_dir / snapshots.REPO_DIR, dst / snapshots.REPO_DIR, dirs_exist_ok=True)
    set_prompt(run, design._request(ask))
    return run


def plan_tier(run_dir, tier, out):
    return plan(run_dir, f"tier {tier}", out, "plan_tier.txt", done=tier - 1, tier=tier)


def plan(run_dir, label, out, prompt_file, most=12, **slots):
    spec = spec_path(run_dir).read_text(encoding="utf-8")
    prompt = (HERE / prompt_file).read_text(encoding="utf-8").format(
        budget=BUDGET, design=spec, codemap=code_map.render(game_dir(run_dir)), **slots)
    name = label.replace(" ", "")
    messages = MessageBuilder(stages._text("plan_system.txt")).add_user(prompt).build()
    body = get_connector(ENTRY).build_llm_job(messages, [], design.MAX_TOKENS)[0]["body"]
    url = settings_manager.get_settings()["local"]["llama_swap"]["url"].rstrip("/") + "/v1/chat/completions"
    for attempt in range(3):
        request = urllib.request.Request(url, json.dumps(chat_body_for_wire(body)).encode(),
                                         {"Content-Type": "application/json"})
        started = time.time()
        result = json.load(urllib.request.urlopen(request, timeout=7200))
        (out / f"{name}-plan-raw-{attempt}.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
        log(f"{label} plan call: {time.time() - started:.0f}s, {result.get('usage')}")
        try:
            cut = [{"name": s["name"].strip().lower(), "stage": s["stage"].strip(), "done": s["done"].strip(),
                    "reads": stages.match_reads(s.get("reads") or [], spec)}
                   for s in stages.parse(design._reply_text(result))]
            if 1 <= len(cut) <= most:
                return cut
            log(f"{label} plan has {len(cut)} stages, asking again")
        except (ValueError, KeyError, TypeError, AttributeError) as e:
            log(f"{label} plan did not parse: {e}")
    raise SystemExit(f"{label}: no stage plan")


def last_activity(run):
    with sqlite3.connect(DB, uri=True, timeout=10) as conn:
        row = conn.execute("select max(coalesce(finished_at, started_at, created_at)) from jobs where game_id = ?",
                           (run,)).fetchone()
    return row[0] or time.time()


def up(url):
    try:
        urllib.request.urlopen(url, timeout=3)
        return True
    except Exception:
        return False


class Services:
    def __init__(self, out):
        self.out, self.runner, self.plane = out, None, None

    def ensure(self):
        if not up("http://localhost:8000/docs"):
            log("control plane is down, starting it")
            self.plane = subprocess.Popen([PYTHON, "run.py"], cwd=REPO, stdout=open(self.out / "control-plane.log", "a"),
                                          stderr=subprocess.STDOUT)
            for _ in range(60):
                if up("http://localhost:8000/docs"):
                    break
                time.sleep(1)
        if self.runner is None or self.runner.poll() is not None:
            log("starting the GPU runner")
            self.runner = subprocess.Popen(RUNNER, cwd=REPO, stdout=open(self.out / "runner.log", "a"),
                                           stderr=subprocess.STDOUT)

    def restart_runner(self):
        if self.runner is not None and self.runner.poll() is None:
            self.runner.terminate()
            try:
                self.runner.wait(timeout=60)
            except subprocess.TimeoutExpired:
                self.runner.kill()
        self.runner = None
        self.ensure()

    def stop(self):
        if self.runner is not None and self.runner.poll() is None:
            self.runner.terminate()
            try:
                self.runner.wait(timeout=90)
            except subprocess.TimeoutExpired:
                self.runner.kill()
                self.runner.wait()


def wait(run, services):
    restarts, since = 0, time.time()
    while True:
        status = (games.game(run) or {}).get("status")
        if status != "running":
            return status
        services.ensure()
        idle = time.time() - max(last_activity(run), since)
        if idle > STALL:
            if restarts >= 2:
                log(f"stalled {idle:.0f}s after {restarts} runner restarts, pausing the run")
                build_chain.pause(run)
                return "stalled"
            restarts, since = restarts + 1, time.time()
            log(f"STALL: no job for {idle:.0f}s, restarting the GPU runner ({restarts})")
            services.restart_runner()
        time.sleep(15)


def probe(run_dir, tier):
    done = subprocess.run([PYTHON, str(HERE / "probe.py"), str(game_dir(run_dir)), str(tier)],
                          capture_output=True, text=True, timeout=900)
    try:
        return json.loads(done.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return {"probe failed": {"crashed": {"ok": False, "detail": (done.stderr or done.stdout)[-400:]}}}


def failed(report, tier):
    return [f"{name}: {check['detail']}" for name, check in report.get(f"tier {tier}", {}).items() if not check["ok"]]


def summary(run):
    with sqlite3.connect(DB, uri=True, timeout=10) as conn:
        builds = conn.execute("select kind, status, steps from builds where game_id = ? order by rowid", (run,)).fetchall()
        jobs = conn.execute("select count(*), sum(status = 'failed') from jobs where game_id = ?", (run,)).fetchone()
    return {"builds": builds, "jobs": jobs[0], "failed jobs": jobs[1] or 0}


def keep(run_dir, label):
    target = OUTPUT / "tier-chain" / run_dir.name / label
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(game_dir(run_dir), target)
    return str(target)


def main():
    source, first, last = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    run = fork(source)
    run_dir = RunState(run).run_dir
    out = HERE / run
    out.mkdir(parents=True, exist_ok=True)
    (HERE / "run.txt").write_text(run + "\n", encoding="utf-8")
    log(f"run {run} forked from {source}, snapshot head {snapshots.head(run_dir)}")
    ask = RunState(run).read_spec()["ask"]
    services, results = Services(out), {}
    try:
        for tier in range(first, last + 1):
            services.ensure()
            cut = plan_tier(run_dir, tier, out)
            plan = {"stages": cut, "budgets": [BUDGET] * len(cut), "attempts": {}, "before": {}}
            stages._save(run_dir, plan)
            (out / f"tier{tier}-stages.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
            log(f"tier {tier}: {len(cut)} stages: " + " · ".join(s["name"] for s in cut))
            start = dict(kind="build", stage=1, request=stages.request(ask, plan, 1))
            if build_chain.kickoff(run, designed=True, **start) is None and build_chain.kickoff(run, **start) is None:
                raise SystemExit(f"tier {tier}: the chain would not start, game is {games.game(run)}")
            began = time.time()
            status = wait(run, services)
            checks = stages.load(run_dir)["attempts"]
            (out / f"tier{tier}-stages.json").write_text(json.dumps(stages.load(run_dir), indent=1, ensure_ascii=False),
                                                         encoding="utf-8")
            log(f"tier {tier} chain ended {status} after {(time.time() - began) / 60:.0f} min; stage checks "
                + json.dumps({k: [(a["attempt"], a["boots"], len(a["errors"])) for a in v] for k, v in checks.items()}))
            if status == "stalled":
                results[f"tier {tier}"] = {"status": status, **summary(run)}
                break
            report = probe(run_dir, tier)
            entry = {"status": status, "probe": report, "minutes": round((time.time() - began) / 60), **summary(run)}
            broke = failed(report, 1)
            if broke and status in ("succeeded", "failed"):
                note = ("These things worked before the last change and no longer do, checked through window.debug: "
                        + "; ".join(broke))
                log(f"tier {tier}: tier 1 checks broke, one fix build: {note[:300]}")
                if build_chain.kickoff(run, kind="fix", note=note, max_steps=FIX_STEPS) is not None:
                    entry["fix status"] = wait(run, services)
                    entry["probe after fix"] = probe(run_dir, tier)
                    entry.update(summary(run))
            entry["kept"] = keep(run_dir, f"tier{tier}")
            entry["snapshot"] = snapshots.head(run_dir)
            results[f"tier {tier}"] = entry
            (out / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
            final = entry.get("probe after fix", report)
            for name in sorted(k for k in final if k.startswith("tier ")):
                log(f"tier {tier} probe, {name}: " + ", ".join(
                    f"{'PASS' if c['ok'] else 'FAIL'} {check}" for check, c in final[name].items()))
    finally:
        (out / "results.json").write_text(json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8")
        services.stop()
    log(f"done: run {run}")


if __name__ == "__main__":
    main()
