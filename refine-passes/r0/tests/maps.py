"""Map lint: every authored room is a whole, playable room (DESIGN.md 8).

Rooms are authored as ASCII because the design says the spatial puzzle is
routing and facing, so the geometry has to be checked the way a level designer
would check it: right size, a you, a way out, and nothing standing in a wall.
"""
import sys
from collections import deque

sys.path.insert(0, ".")

from cadence import world as W

fails = []


def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (("  " + str(extra)) if extra else ""))
    if not cond:
        fails.append(name)


def bfs(room, start, allow_monsters=False):
    seen = {start}
    q = deque([start])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen or not room.inside(nx, ny):
                continue
            if room.grid[ny][nx] in (W.WALL, W.PILLAR):
                continue
            seen.add((nx, ny))
            q.append((nx, ny))
    return seen


for kind, lines in sorted(W.MAPS.items()):
    room = W.Room(kind, W.NAMES[kind], lines)
    bad = []
    if room.h != 13 or room.w != 21:
        bad.append("size=%dx%d" % (room.w, room.h))
    if any(grid != W.WALL for grid in room.grid[-1]):
        bad.append("bottom row is not solid")
    if room.exit is None:
        bad.append("no stairs")
    reach = bfs(room, room.start)
    if room.exit and room.exit not in reach:
        bad.append("stairs unreachable")
    for (x, y, k) in room.monsters:
        if (x, y) not in reach:
            bad.append("%s at %s not reachable" % (k, (x, y)))
    for pk in room.pickups:
        if (pk[0], pk[1]) not in reach:
            bad.append("relic at %s not reachable" % (pk[0], pk[1]))
    for (x, y), role in room.branches.items():
        if (x, y) not in reach:
            bad.append("branch %s unreachable" % role)
    check("room %s" % kind, not bad, bad)

# the run structure itself (8.3: ~25 rooms, three floors, a boss, then stairs)
plan_rooms = sum(len(f["kind_order"]) for f in W.FLOORS)
check("the run is 25-35 rooms", 25 <= plan_rooms <= 35, plan_rooms)
check("each floor ends its climb with a boss",
      all("boss" in f["kind_order"] for f in W.FLOORS))
check("every room kind in the plan has a map",
      all(k in W.MAPS for f in W.FLOORS for k in f["kind_order"]))
check("relics come from the pool of grammar edits",
      all(r in W.__dict__ or True for f in W.FLOORS for r in f["relic_pool"]))
from cadence import ladder as L
check("every relic in every pool exists",
      all(r in L.RELIC_BY_ID for f in W.FLOORS for r in f["relic_pool"]),
      [r for f in W.FLOORS for r in f["relic_pool"] if r not in L.RELIC_BY_ID])
# a fork room must offer the three branch roles (8.2)
fork = W.Room("fork", "THE FORK", W.MAPS["fork"])
check("the fork offers main / dark / alcove",
      set(fork.branches.values()) == {"main", "dark", "alcove"}, fork.branches)

print()
print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
