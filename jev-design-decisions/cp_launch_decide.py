"""Launch one decide box on EC2 from the local control plane through scaler.ec2_client, then create
a game whose design stage sends its decide job to that box; the build runs on whatever llm worker
is local. Mirrors labs/ec2-g7e/cp_launch.py.

Run from the repo root: venv/bin/python labs/jev-design-decisions/cp_launch_decide.py "<ask>" [--on-demand]
"""

import configparser
import json
import sys
import time
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from auth import store  # noqa: E402
from config.settings_manager import settings_manager  # noqa: E402
from db import workers  # noqa: E402
from db.connection import platform_db  # noqa: E402
from scaler.ec2_client import Ec2Client, Ec2Error  # noqa: E402

CP_URL = "https://nick-ms-7e70.taild62b23.ts.net"
AMIS = {"us-east-1": "ami-04366b4063158fcfe"}
INSTANCE_TYPE = "g7e.2xlarge"
NAME_PREFIX = "gstest-decide-"
T0 = time.time()


def say(msg: str) -> None:
    print(f"[{time.time() - T0:6.0f}s] {msg}", flush=True)


def main() -> int:
    ask = sys.argv[1]
    markets = ["spot", "on-demand"] if "--on-demand" in sys.argv else ["spot"]
    creds = configparser.ConfigParser()
    creds.read(Path.home() / ".aws" / "credentials")
    client = Ec2Client(creds["default"]["aws_access_key_id"],
                       creds["default"]["aws_secret_access_key"])
    settings = settings_manager.get_settings()

    running = client.list_instances(AMIS, NAME_PREFIX)
    if running:
        say(f"already running, not launching: {running}")
        return 1

    worker_id = uuid.uuid4().hex
    env = {
        "CP_URL": CP_URL,
        "WORKER_TOKEN": settings["workqueue"]["token"],
        "WORKER_QUEUE": "decide",
        "WORKER_ID": worker_id,
        "WORKER_SOURCE": "aws",
        "WORKER_SLOTS": "1",
        "IDLE_EXIT_SECONDS": "120",
        "JOB_TIMEOUT_SECONDS": "600",
        "SGLANG_ARGS_EXTRA": "",
    }
    launched = None
    for offer in client.offers(AMIS, [INSTANCE_TYPE], markets):
        try:
            instance_id = client.launch(offer, f"{NAME_PREFIX}{worker_id[:8]}", AMIS[offer.region],
                                        env, "gs-gpu-worker", "gs-gpu-worker")
        except Ec2Error as e:
            say(f"{offer.zone} {offer.market} refused: {e}")
            if not e.stock:
                break
            continue
        launched = (offer, instance_id)
        break
    if not launched:
        say("nothing launched")
        return 2
    offer, instance_id = launched
    workers.worker_created(worker_id, f"{offer.region}/{instance_id}", "decide",
                           offer.instance_type, offer.usd_per_hour)
    say(f"launched {instance_id} in {offer.zone} ({offer.market} ${offer.usd_per_hour:.4f}/hr), "
        f"worker {worker_id}")

    token = store.issue_token(store.list_users()[0].id)
    req = urllib.request.Request("http://127.0.0.1:8000/api/games",
                                 json.dumps({"prompt": ask}).encode(),
                                 {"Content-Type": "application/json",
                                  "Authorization": f"Bearer {token}"})
    game = json.loads(urllib.request.urlopen(req).read())
    say(f"game {game}")

    registered, status = False, None
    while time.time() - T0 < 1500:
        time.sleep(5)
        with platform_db() as conn:
            if not registered:
                row = conn.execute("SELECT registered_at FROM workers WHERE id = ?",
                                   (worker_id,)).fetchone()
                if row["registered_at"]:
                    registered = True
                    say("worker registered")
            job = conn.execute("SELECT id, status, error, exec_seconds FROM jobs WHERE queue = 'decide' "
                               "AND game_id = ? ORDER BY created_at DESC LIMIT 1",
                               (game["run_id"],)).fetchone()
        if job and job["status"] != status:
            status = job["status"]
            say(f"decide job {job['id']} {status} exec {job['exec_seconds']} {job['error'] or ''}")
        if status in ("done", "failed"):
            break
    while time.time() - T0 < 1800:
        if not client.list_instances([offer.region], NAME_PREFIX):
            say("instance gone")
            return 0 if status == "done" else 1
        time.sleep(10)
    say(f"instance {instance_id} still up; terminating")
    client.terminate(offer.region, instance_id)
    return 1


if __name__ == "__main__":
    sys.exit(main())
