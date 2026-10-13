"""The room: tiles, sightlines, authored layouts (DESIGN.md 4, 8, 14.3).

Rooms are authored as ASCII maps because the design is explicit about geometry:
with one axis the spatial puzzle *is* routing and facing, so corridors,
sightlines and bottlenecks have to be placed on purpose - "wide open rooms are
boring under this scheme".  The run shuffles and re-stocks them.
"""
import math

WALL, FLOOR, DOOR, DOOR_OPEN, LOCKED = "#", ".", "+", "/", "="
CHEST, CHEST_OPEN, STAIRS, COUNTER, SWITCH, SWITCH_ON, PILLAR = "C", "c", ">", "N", "S", "s", "*"

# a locked door is solid: it opens to a Strike or to a switch (8.1)
SOLID = {WALL, DOOR, LOCKED, CHEST, COUNTER, PILLAR}
BRANCH_ROLE = {"1": "main", "2": "dark", "3": "alcove"}
ROLE_VERB = {"main": "STEP", "dark": "STRIKE", "alcove": "GUARD"}

MONSTER_CHARS = {"r": "rat", "x": "sentinel", "m": "mirror", "t": "tic",
                 "h": "priestess", "w": "swarm", "D": "drummer"}


class Room:
    def __init__(self, kind, name, lines, meta=None):
        self.kind = kind
        self.name = name
        self.meta = meta or {}
        h = len(lines)
        w = max(len(r) for r in lines)
        self.w, self.h = w, h
        self.grid = []
        self.monsters = []
        self.pickups = []            # (x, y, relic_id, price_turns)
        self.branches = {}           # (x,y) -> role
        self.exit = None
        self.pprice = self.meta.get("price", 0)
        for y in range(h):
            row = lines[y].ljust(w, "#")[:w]
            out = []
            for x, ch in enumerate(row):
                if ch in MONSTER_CHARS:
                    self.monsters.append(ch)
                    self.monsters[-1] = (x, y, MONSTER_CHARS[ch])
                    ch = FLOOR
                elif ch == "R":
                    self.pickups.append([x, y, self.meta.get("relic", "metronome"), 0])
                    ch = FLOOR
                elif ch in BRANCH_ROLE:
                    self.branches[(x, y)] = BRANCH_ROLE[ch]
                    ch = FLOOR
                elif ch == "P":
                    self.start = (x, y)
                    ch = FLOOR
                elif ch == ">":
                    self.exit = (x, y)
                out.append(ch)
            self.grid.append(out)
        self.start = getattr(self, "start", (2, self.h // 2))
        self.explored = set()
        self.lamps = [(x, y) for y, row in enumerate(self.grid) for x, ch in enumerate(row)
                      if ch == PILLAR]

    # ------------------------------------------------------------- queries --
    def inside(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def tile(self, x, y):
        return self.grid[y][x] if self.inside(x, y) else WALL

    def solid(self, x, y):
        return self.tile(x, y) in SOLID

    def walkable(self, x, y, monsters=None):
        if not self.inside(x, y) or self.solid(x, y):
            return False
        if monsters and any(m.x == x and m.y == y and m.alive for m in monsters):
            return False
        return True

    def set(self, x, y, ch):
        if self.inside(x, y):
            self.grid[y][x] = ch

    def door_state(self, x, y):
        return self.tile(x, y)

    # ------------------------------------------------------------- vision --
    def fov(self, px, py, radius):
        """soft falloff, no shadow casting in v0 (14.3): the attenuation is the
        whole trick - walls hold the light in."""
        out = {}
        r = int(math.ceil(radius)) + 1
        for y in range(max(0, py - r), min(self.h, py + r + 1)):
            for x in range(max(0, px - r), min(self.w, px + r + 1)):
                d = math.hypot(x - px, y - py)
                if d > radius:
                    continue
                att = 1.0 if self.tile(x, y) not in (WALL, PILLAR) or d < 1.5 else 0.25
                # a soft falloff that still reads as radius 7 across the floor
                t = (1.0 - (d / radius) ** 1.6) * att
                out[(x, y)] = max(0.0, min(1.0, t))
        return out


# --------------------------------------------------------------- the rooms --
# 21 x 13 authored layouts.  Legend:  # wall  . floor  + door  = locked door
# C chest  > stairs  N shop counter  S switch  * pillar   R relic
# r rat  x sentinel  m mirror  t tic  h priestess  w swarm  D drummer
# 1 main path  2 dark branch  3 safe alcove  P you
TUT1 = [
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "########.......######",
    "########.P.....>.####",
    "########.......######",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
]
TUT2 = [
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "########.......######",
    "########.P...r.>.####",
    "########.......######",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
]
# one tile wide, three corners: Step runs into the wall and becomes a Bump
# unless you Pivot first.  This is the room that teaches the pivot.
TUT3 = [
    "#####################",
    "#####################",
    "#####################",
    "###P.........########",
    "####.#######.########",
    "####.#######.########",
    "####.#######.########",
    "####.#######.########",
    "####.#######.########",
    "####.........########",
    "####.################",
    "####>################",
    "#####################",
]
CORRIDOR = [
    "#####################",
    "#####################",
    "##########+##########",
    "##########.##########",
    "##########.##########",
    "#####....r.....######",
    "#####.#######.#######",
    "#####..x..C..t.>#####",
    "#####.#######.#######",
    "#####....r.....######",
    "##########.##########",
    "#####################",
    "#####################",
]
BOTTLENECK = [
    "#####################",
    "######.......########",
    "####..r...r..########",
    "####.......+#########",
    "#####..#.#.##########",
    "######.#.############",
    "#######.#############",
    "#####..P#############",
    "#####...#############",
    "####.x..#############",
    "####....>.###########",
    "#####################",
    "#####################",
]
FORK = [
    "#####################",
    "#####################",
    "#######.2R###########",
    "#######...###########",
    "####......+##########",
    "###..#########3C#####",
    "###..P.....1>.#######",
    "###..##########.#####",
    "####......+####.#####",
    "#######...###########",
    "#######.r############",
    "#####################",
    "#####################",
]
VAULT = [
    "#####################",
    "#####################",
    "######.N.C.##########",
    "######.....##########",
    "####...=...##########",
    "####.#######.########",
    "###..P.....r.>#######",
    "###..#######.########",
    "####...S...##########",
    "####...r...##########",
    "######...x.##########",
    "#####################",
    "#####################",
]
SHRINE = [
    "#####################",
    "#####################",
    "##########.##########",
    "#########.R.#########",
    "########..+..########",
    "#####...r...#########",
    "#####..P.....>#######",
    "#####......##########",
    "########...##########",
    "#########.x.#########",
    "##########.##########",
    "#####################",
    "#####################",
]
SHOP = [
    "#####################",
    "#####################",
    "######.R.R.R.########",
    "######..N...#########",
    "#####.......#########",
    "#####..P....>.#######",
    "#####.......#########",
    "######...x..#########",
    "######.......########",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
]
NEST = [
    "#####################",
    "#####################",
    "#####.rr...rr.#######",
    "####....r.r....######",
    "####...#####...######",
    "####..#.....#..######",
    "###...#.P.#..>#######",
    "###...#...#..########",
    "####..#####...#######",
    "####...r...r..#######",
    "#####......r.########",
    "#####################",
    "#####################",
]
ARENA = [
    "#####################",
    "######.........######",
    "####....x...x..######",
    "###............######",
    "###....R....>.#######",
    "###...........#######",
    "###....P.....########",
    "###...........#######",
    "###....m.....########",
    "####..........#######",
    "######......#########",
    "#####################",
    "#####################",
]
BOSS = [
    "#####################",
    "#####.........#######",
    "####...R...D..#######",
    "###............######",
    "###................##",
    "###................##",
    "###.......P....>.####",
    "###................##",
    "###................##",
    "###............h....#",
    "####...x...x..#######",
    "#####.........#######",
    "#####################",
]
EXITHALL = [
    "#####################",
    "#####################",
    "#######.....#########",
    "######..x...>.#######",
    "#####.......#########",
    "#####.P.....#########",
    "#####....r..#########",
    "######.....##########",
    "#######.....#########",
    "#####################",
    "#####################",
    "#####################",
    "#####################",
]
DEADEND = [
    "#####################",
    "##########.##########",
    "#########.C.#########",
    "########..+..########",
    "#####.....r..########",
    "#####..P....#########",
    "#####......##########",
    "######...x.##########",
    "#######...###########",
    "#########.###########",
    "#####################",
    "#####################",
    "#####################",
]

MAPS = {
    "tutorial1": TUT1, "tutorial2": TUT2, "tutorial3": TUT3,
    "corridor": CORRIDOR, "bottleneck": BOTTLENECK, "fork": FORK,
    "vault": VAULT, "shrine": SHRINE, "shop": SHOP, "nest": NEST,
    "arena": ARENA, "boss": BOSS, "exithall": EXITHALL, "deadend": DEADEND,
}

NAMES = {
    "tutorial1": "THE FIRST STEP", "tutorial2": "THE RAT", "tutorial3": "THE TURN",
    "corridor": "CORRIDOR SKIRMISH", "bottleneck": "BOTTLENECK", "fork": "THE FORK",
    "vault": "THE VAULT", "shrine": "SHRINE", "shop": "COUNTER OF TURNS",
    "nest": "THE NEST", "arena": "OPEN GROUND", "boss": "THE DRUMMER",
    "exithall": "EXIT HALL", "deadend": "ALCOVE",
}

# run structure (8): 3 floors, ~25 rooms, floors end at a boss then stairs
FLOORS = [
    dict(kind_order=["tutorial1", "tutorial2", "tutorial3", "corridor", "bottleneck",
                     "fork", "corridor", "shop", "nest", "vault", "boss"],
         relic_pool=["metronome", "stutter", "twin_cut", "iron_rest"]),
    dict(kind_order=["corridor", "shrine", "bottleneck", "nest", "fork", "deadend",
                     "arena", "shop", "corridor", "vault", "boss"],
         relic_pool=["hollow", "offbeat", "hair_trigger", "drummer_relic", "fidget"]),
    dict(kind_order=["nest", "arena", "fork", "shrine", "corridor", "deadend",
                     "bottleneck", "arena", "shop", "vault", "exithall"],
         relic_pool=["offbeat", "hollow", "metronome", "twin_cut", "fidget"]),
]
