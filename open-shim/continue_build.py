"""Continue a build that ended only because the server refused its turns (Basalt's RAM guard).

Drops the refused turns' "server could not read" messages and gives their steps back, reopens the
build and the game, then re-drives it from its last real turn. Needs local_gpu auto up.

    python3 continue_build.py <run id> ...
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from db import games
from db.connection import platform_db
from maestro.codegen import build_chain, build_state
from maestro.state import RunState

REFUSED = "The inference server could not read your last reply"


def reopen(run_id: str) -> None:
    rs = RunState(run_id)
    cursor = build_state.load(rs.run_dir)
    refused = 0
    while cursor.history and cursor.history[-1].get("role") == "user" \
            and str(cursor.history[-1].get("content")).startswith(REFUSED):
        cursor.history.pop()
        refused += 1
    cursor.step -= refused
    cursor.turn -= refused
    cursor.logged = min(cursor.logged, len(cursor.history))
    cursor.no_call_streak = 0
    cursor.phase = "build"
    cursor.ok = None
    build_state.save(rs.run_dir, cursor)
    with platform_db() as conn:
        conn.execute("UPDATE builds SET status = 'running', finished_at = NULL WHERE id = ?",
                     (cursor.build_id,))
    games.set_status(run_id, "building")
    print(f"{run_id}: dropped {refused} refused turns, back at step {cursor.step}", flush=True)
    build_chain.resume(run_id)


if __name__ == "__main__":
    for rid in sys.argv[1:]:
        reopen(rid)
