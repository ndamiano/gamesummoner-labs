"""Answer a game's pending decide job with a finished game's JEV result, through the worker API.

JEV is deterministic for a given ask (three runs of the wizard-cat ask returned byte-identical
results), so replaying one stands in for booting the decide box when the card is busy.
"""

import argparse
import json
import sqlite3
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))


def post(path: str, token: str, body: dict) -> dict:
    req = urllib.request.Request(f"http://localhost:8000/worker/{path}", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {token}"})
    return json.load(urllib.request.urlopen(req, timeout=60))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("game", help="game whose decide job is pending")
    parser.add_argument("source", help="finished game whose decide result is replayed")
    args = parser.parse_args()

    db = sqlite3.connect(REPO / "data" / "platform.db")
    row = db.execute("select result from jobs where queue='decide' and status='done' and game_id=?",
                     (args.source,)).fetchone()
    if row is None:
        raise SystemExit(f"no finished decide job for {args.source}")
    pending = db.execute("select id from jobs where queue='decide' and status='pending' and game_id=?",
                         (args.game,)).fetchone()
    if pending is None:
        raise SystemExit(f"no pending decide job for {args.game}")
    if db.execute("select count(*) from jobs where queue='decide' and status in ('pending','claimed')"
                  ).fetchone()[0] != 1:
        raise SystemExit("other decide jobs are waiting; the claim could take the wrong one")

    import local_gpu
    env = json.loads(local_gpu._worker_env("decide").read_text())
    token, worker = env["WORKER_TOKEN"], env["WORKER_ID"]
    job = post("claim", token, {"queue": "decide", "worker_id": worker, "source": "replay"}).get("job")
    if not job or job["id"] != pending[0]:
        raise SystemExit(f"claimed {job and job['id']}, expected {pending[0]}")
    out = post("complete", token, {"job_id": job["id"], "worker_id": worker,
                                   "result": json.loads(row[0]), "exec_seconds": 0.0})
    print(f"replayed {args.source}'s decide result into {args.game} job {job['id']}: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
