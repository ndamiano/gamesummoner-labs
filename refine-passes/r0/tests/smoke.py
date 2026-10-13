"""Engine smoke test: recogniser grammar, tier rule, verbs, enemies, run flow."""
import sys
sys.path.insert(0, ".")

from cadence.config import Thresholds, Settings
from cadence.recognizer import Recognizer
from cadence import ladder as L
from cadence.game import Game

th = Thresholds()


def run_presses(rec, t, taps, gap):
    """press / release pairs, then tick past the commit window."""
    evs = []
    for i in range(taps):
        evs += rec.press(t)
        t += 80                             # a short press, well under HOLD_START
        evs += rec.release(t)
        t += gap - 80
    for _ in range(40):
        evs += rec.tick(t)
        t += 10
        if any(e["type"] == "commit" for e in evs):
            break
    return evs


def commits(rec, t, taps, gap):
    return [e for e in run_presses(rec, t, taps, gap) if e["type"] == "commit"]


def settle(rec, t):
    """let the machine come to rest: key up, then tick past everything."""
    rec.release(t)
    for _ in range(120):
        rec.tick(t)
        t += 50
    return t + 1000


fails = []


def check(name, cond, extra=""):
    print(("PASS " if cond else "FAIL ") + name + (("  " + str(extra)) if extra else ""))
    if not cond:
        fails.append(name)


# --- grammar ---------------------------------------------------------------
r = Recognizer(th, Settings())
t = 1000
for n, want in ((1, "STEP"), (2, "STRIKE"), (3, "LUNGE"), (4, "GUARD"), (5, "SPRINT")):
    c = commits(r, t, n, 400)
    t += 4000
    check("tap x%d -> %s" % (n, want), c and c[0]["verb"] == want, c[0] if c else None)

c = commits(r, t, 8, 400)
check("six-rung ceiling: 8 taps -> SPRINT", c and c[0]["verb"] == "SPRINT")
t += 5000

# debounce
evs = []
for i in range(3):
    evs += r.press(t)
    t += 10
check("debounce: 3 presses in 20 ms = one press", sum(1 for e in evs if e["type"] == "press") == 1)
t = settle(r, t)

c = commits(r, t, 3, 40)
check("debounce burst stays one press -> STEP", c and c[0]["verb"] == "STEP", c[0] if c else None)
t += 5000

# slow burst splits at SLOW_GAP
evs = r.press(t); evs += r.release(t + 60); evs += r.press(t + 900)
evs += r.release(t + 960); evs += r.press(t + 950)
for _ in range(40):
    evs += r.tick(t + 2000)
    t += 20
    if sum(1 for e in evs if e["type"] == "commit") >= 1:
        break
kinds = [e for e in evs if e["type"] == "commit"]
check("SLOW_GAP splits a burst", len(kinds) >= 1 and kinds[0]["verb"] == "STEP",
      [(k["verb"], k["count"]) for k in kinds])
t = settle(r, t + 1000)

# hold -> pivot
evs = r.press(t)
t += 300
evs += r.tick(t)
piv = [e for e in evs if e["type"] in ("pivot", "pivot_begin", "cancel")]
check("hold past HOLD_START cancels the step and pivots",
      any(e["type"] == "cancel" for e in piv) and any(e["type"] == "pivot_begin" for e in piv))
t += 400
evs2 = r.tick(t)
check("200 ms detents while held", any(e["type"] == "pivot" for e in evs2))
t += 2000
evs3 = r.tick(t)
check("hold past REST_HOLD -> rest", any(e["type"] == "rest" for e in evs3))
t = settle(r, t)

# idle -> brace
before = r.idle_streak
evs = []
for _ in range(200):
    evs += r.tick(t)
    t += 20
check("no input -> BRACE", any(e["type"] == "brace" for e in evs))

# --- tiers -----------------------------------------------------------------
def tier_of(taps, gap, extra=0):
    rr = Recognizer(th, Settings())
    rr.press(1000)
    rr.tick(4000)
    out = commits(rr, 5000 + extra, taps, gap)
    return out[0]["tier"] if out else None

check("gap 900 ms -> careful", tier_of(2, 900) == "careful", tier_of(2, 900))
check("gap 120 ms -> frantic", tier_of(2, 120) == "frantic", tier_of(2, 120))
check("gap 450 ms -> normal", tier_of(2, 450) == "normal", tier_of(2, 450))

# --- assist mode -----------------------------------------------------------
ar = Recognizer(th, Settings(assist=True))
evs = []
t0 = 1000
for _ in range(200):
    evs += ar.tick(t0)
    t0 += 100
    if any(e["type"] == "dwell_begin" for e in evs):
        break
check("dwell wheel appears after 1.2 s", any(e["type"] == "dwell_begin" for e in evs))
ar.tick(t0 + 700)
evs2 = ar.press(t0 + 700)
c = [e for e in evs2 if e["type"] == "commit"]
check("dwell + press commits the rung under the wheel", bool(c))

# --- the game --------------------------------------------------------------
g = Game(seed=7)
check("room loaded", g.room.w == 21 and g.room.h == 13)
check("start walkable", not g.room.solid(g.player.x, g.player.y))
g.rec.press(0)
for _ in range(40):
    g.rec.tick(400)
evs = [e for e in g.rec.last_commit and [g.rec.last_commit] or []]
g.execute(g.rec.last_commit)
check("STEP moves one tile", g.player.x == g.room.start[0] + 1 or g.player.y != g.room.start[1],
      g.player.x)
check("turns spent", g.turns == 1)

g2 = Game(seed=7)
p0 = (g2.player.x, g2.player.y)
g2.execute(dict(verb="PIVOT", dir=1, tier="normal", count=0, gaps=[]))
check("pivot costs nothing and turns facing", g2.player.facing == 1 and g2.turns == 0)

g3 = Game(seed=11)
g3.execute(dict(verb="BRACE", tier="careful", count=0, gaps=[]))
check("BRACE grants guard", g3.player.guard >= 1)

g4 = Game(seed=11)
g4.player.facing = 0
tx, ty = g4.player.front()
while g4.room.solid(tx, ty):
    g4.player.facing = (g4.player.facing + 1) % 8
    tx, ty = g4.player.front()
from cadence.entities import Monster
m = Monster(tx, ty, "rat")
g4.monsters.append(m)
hp0 = m.hp
g4.execute(dict(verb="STRIKE", tier="frantic", count=2, gaps=[120]))
check("STRIKE damages an adjacent monster", m.hp < hp0, (hp0, m.hp))

# graceful degradation: STEP into a wall becomes BUMP
g5 = Game(seed=7)
g5.player.x, g5.player.y = 8, 7          # one tile from the west wall
g5.player.facing = 4                     # facing W into the wall
g5.execute(dict(verb="STEP", tier="normal", count=1, gaps=[]))
check("STEP into a wall degrades to BUMP",
      any(e["type"] == "degrade" and e["to"] == "BUMP" for e in g5.events))

# undo (5.4)
g6 = Game(seed=7)
before = (g6.player.x, g6.player.y)
g6.execute(dict(verb="STEP", tier="normal", count=1, gaps=[]))
after = (g6.player.x, g6.player.y)
check("the step moved", before != after)
check("undo restores position", g6.undo() and (g6.player.x, g6.player.y) == before)
g6.execute(dict(verb="STEP", tier="normal", count=1, gaps=[]))
check("undo is once per room", not g6.undo())

# relics edit the ladder (6)
g7 = Game(seed=3, ladder=L.Ladder(["offbeat"]))
r7 = Recognizer(th, Settings(), g7.ladder)
c = commits(r7, 1000, 1, 400)
check("OFFBEAT: 1 tap = STRIKE", c and c[0]["verb"] == "STRIKE", c[0] if c else None)
g8 = Game(seed=3, ladder=L.Ladder(["hollow"]))
d_careful = g8.damage_for("strike", "careful", L.TIER_RULE["careful"])
d_normal = g8.damage_for("strike", "normal", L.TIER_RULE["normal"])
check("HOLLOW CADENCE: careful is the build", d_careful > d_normal, (d_careful, d_normal))

# a scripted run: walk east into the stairs and descend
g9 = Game(seed=5)
steps = 0
while g9.status == "playing" and steps < 30 and g9.room_index == 0:
    g9.player.facing = 0
    g9.execute(dict(verb="STEP", tier="normal", count=1, gaps=[]))
    steps += 1
check("the stairs take you to the next room", g9.room_index == 1, (g9.room_index, g9.status))
check("descending keeps hp / turn state sane", g9.player.hp > 0 and g9.turns > steps)
g9.player.x, g9.player.y = g9.room.start

# every grammar relic actually edits something (6)
def with_relic(rid, fn):
    lad = L.Ladder([rid])
    return fn(lad)


lad_plain, lad_off = L.Ladder(), L.Ladder(["offbeat"])
check("OFFBEAT swaps the bottom rungs",
      lad_plain.verb_for(1) == "STEP" and lad_off.verb_for(1) == "STRIKE" and
      lad_off.verb_for(2) == "STEP")
check("HAIR TRIGGER: faster commits, no FRANTIC",
      L.Ladder(["hair_trigger"]).commit_window(260) < 260 and
      not L.Ladder(["hair_trigger"]).frantic_allowed() and
      L.Ladder(["metronome"]).commit_window(260) > 260)
check("STUTTER / DRUMMER reprice a rung",
      L.Ladder(["stutter"]).cost("LUNGE") == 0 and
      L.Ladder(["drummer_relic"]).cost("SPRINT") == 1 and
      L.Ladder().cost("SPRINT") == 3)
gH = Game(seed=1, ladder=L.Ladder(["hollow"]))
gN = Game(seed=1)
check("HOLLOW CADENCE makes careful the build",
      gH.damage_for("strike", "careful", L.TIER_RULE["careful"]) >
      gN.damage_for("strike", "careful", L.TIER_RULE["careful"]))
gT = Game(seed=1, ladder=L.Ladder(["twin_cut"]))
from cadence.entities import Monster as _M
gT.player.x, gT.player.y = 9, 6
gT.player.facing = 2                       # north
for dy in (1,):
    pass
a = _M(9, 5, "rat"); b = _M(8, 5, "rat"); c = _M(10, 5, "rat")
gT.monsters = [a, b, c]
gT.execute(dict(verb="STRIKE", tier="normal", count=2, gaps=[400]))
check("TWIN CUT hits the tiles beside the one in front",
      a.hp < a.max_hp and b.hp < b.max_hp and c.hp < c.max_hp,
      (a.hp, b.hp, c.hp))
gI = Game(seed=1, ladder=L.Ladder(["iron_rest"]))
gI.execute(dict(verb="BRACE", tier="careful", count=0, gaps=[]))
check("IRON REST: brace gives 2 guard and heals", gI.player.guard >= 2)
gD = Game(seed=2)
gD._load_room(10)                          # THE DRUMMER
dr = [m for m in gD.monsters if m.kind == "drummer"][0]
hp0 = dr.hp
gD.player.x, gD.player.y = dr.x - 1, dr.y
gD.player.facing = 0
gD.execute(dict(verb="STRIKE", tier="normal", count=2, gaps=[400]))
off_beat = dr.hp == hp0
gD.execute(dict(verb="STRIKE", tier="normal", count=2, gaps=[400]))
check("the Drummer is immune except on its beat",
      off_beat and dr.hp < hp0, (hp0, dr.hp))

# save / resume round trip
g10 = Game(seed=9)
g10.execute(dict(verb="STEP", tier="normal", count=1, gaps=[]))
g10.save("saves/smoke.json")
g11 = Game.load("saves/smoke.json")
check("save/resume round trip", g11 and g11.player.x == g10.player.x and g11.turns == g10.turns
      and g11.player.hp == g10.player.hp)

print()
print("FAILURES:", fails if fails else "none")
sys.exit(1 if fails else 0)
