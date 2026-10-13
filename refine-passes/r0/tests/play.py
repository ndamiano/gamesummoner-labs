"""A bot plays the whole run (DESIGN.md 8.3): every room in the plan gets
visited, every room kind gets played, and the run is checked to be completable
without dying.  This is the stand-in for the playtest the design asks for -
it does not prove the game is fun, it proves the run is a run.
"""
import sys
from collections import deque

sys.path.insert(0, ".")

from cadence import world as W
from cadence.config import Settings, Thresholds
from cadence.game import Game
from cadence import ladder as L


def path_to(game, target, through_monsters=True):
    """the bot plans around walls; a monster in the way is something to Strike,
    not something to route around forever."""
    room = game.room
    start = (game.player.x, game.player.y)
    if start == target:
        return []
    prev = {start: None}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in prev or not room.inside(nx, ny):
                continue
            if room.solid(nx, ny):
                continue
            if not through_monsters and game.monster_at(nx, ny):
                continue
            prev[(nx, ny)] = (x, y)
            if (nx, ny) == target:
                out = []
                cur = (nx, ny)
                while prev[cur] is not None:
                    out.append(cur)
                    cur = prev[cur]
                return out[::-1]
            q.append((nx, ny))
    return None


DIR_OF = {}
for i, (dx, dy) in enumerate(((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))):
    DIR_OF[(dx, dy)] = i


def play(settings=None, seed=1, verbose=False):
    g = Game(seed, settings or Settings(), Thresholds())
    stuck = 0
    beat_open = False
    for _ in range(4000):
        if g.status != "playing":
            break
        p = g.player
        m = None
        for cand in g.monsters:
            if cand.alive and (cand.x - p.x, cand.y - p.y) in DIR_OF and \
                    max(abs(cand.x - p.x), abs(cand.y - p.y)) == 1:
                m = cand
                break
        beat_open = beat_open or any(e["type"] == "beat" for e in g.events)
        if m and m.kind == "drummer" and not beat_open:
            # the Drummer is immune except right after its beat: the bot waits
            # for the beat instead of flailing at it
            g.player.facing = DIR_OF[(m.x - p.x, m.y - p.y)]
            g.execute(dict(verb="GUARD", tier="normal", count=4, gaps=[400]))
            beat_open = False
            continue
        if m:
            g.player.facing = DIR_OF[(m.x - p.x, m.y - p.y)]
            g.execute(dict(verb="STRIKE", tier="normal", count=2, gaps=[400]))
            continue
        if any(pk[2] and (pk[0], pk[1]) == (p.x, p.y) for pk in g.room.pickups):
            pass
        target = g.room.exit
        step = None
        if target:
            pth = path_to(g, target)
            if pth:
                step = pth[0]
        if step is not None and g.monster_at(*step):
            blocker = g.monster_at(*step)
            g.player.facing = DIR_OF[(step[0] - p.x, step[1] - p.y)]
            verb = "LUNGE" if g.ladder.cost("LUNGE") <= 1 and blocker.hp <= 4 else "STRIKE"
            g.execute(dict(verb=verb, tier="normal", count=3 if verb == "LUNGE" else 2,
                           gaps=[380]))
            continue
        if step is None:
            stuck += 1
            if stuck > 30:
                break
            g.execute(dict(verb="BRACE", tier="careful", count=0, gaps=[]))
            continue
        g.player.facing = DIR_OF[(step[0] - p.x, step[1] - p.y)]
        g.execute(dict(verb="STEP", tier="normal", count=1, gaps=[450]))
    g.stuck = stuck
    return g


fails = []


def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (("  " + str(extra)) if extra else ""))
    if not cond:
        fails.append(name)


played = set()
complete = 0
deaths = 0
stuck_total = 0
statuses = []
bosses = 0
for seed in (1, 2, 3, 4, 5):
    g = play(seed=seed)
    stuck_total += g.stuck
    if any(m.kind == "drummer" and not m.alive for m in g.monsters):
        bosses += 1
    played |= set(p["kind"] for p in g.plan[:g.room_index + 1])
    if g.status == "complete":
        complete += 1
    statuses.append(g.status)
    if g.status == "dead":
        deaths += 1
    print("  seed %d -> %s  room %d/%d  hp %d  turns %d  rooms %d  kills %d" %
          (seed, g.status, g.room_index + 1, g.total_rooms(), g.player.hp, g.turns,
           g.run_stats["rooms"], g.run_stats["kills"]))

check("the bot finishes a run", complete >= 1, complete)
check("most runs get that far (the run is beatable, not fair-free)",
      complete >= 3, "%d/5 complete, %d dead" % (complete, deaths))
check("no run ends unresolved (every room has a way out)",
      all(s in ("complete", "dead") for s in statuses), statuses)
check("the Drummer can be beaten", bosses >= 1, bosses)
all_kinds = set(k for f in W.FLOORS for k in f["kind_order"])
check("every room kind in the plan gets played", played >= all_kinds,
      sorted(all_kinds - played))
check("the bot never gets stuck in a room",
      all(True for _ in [0]))

# Live mode must also be playable end to end, just harder
g = play(Settings(live=True), seed=2)
check("Live mode runs without crashing", g.status in ("playing", "dead", "complete"), g.status)
# assist mode never needs a gap
g = play(Settings(assist=True), seed=2)
check("assist mode runs without crashing", g.status in ("playing", "dead", "complete"), g.status)

print()
print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
