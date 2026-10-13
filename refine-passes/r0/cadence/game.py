"""The game itself: verbs, half-turns, rooms, the run (DESIGN.md 2.5, 4, 5, 6, 7, 8, 11, 12).

No drawing, no clock, no input device.  The app feeds recogniser events here and
gets world changes plus a list of *events* for the animator and the audio mixer
to read - the same event list is what makes the sound and the picture describe
the same verb (15.2).
"""
import json
import os
import random

from . import world as W
from . import ladder as L
from .config import MAX_HP, GUARD_CAP, BASE_DAMAGE, Settings, Thresholds
from .entities import Monster, DIRS
from .recognizer import Recognizer

SAVE_PATH = "saves/cadence.json"


class Player:
    def __init__(self, x, y, facing=0):
        self.x, self.y = x, y
        self.facing = facing          # 0=E 1=NE 2=N 3=NW 4=W 5=SW 6=S 7=SE
        self.hp = MAX_HP
        self.guard = 0
        self.refresh = False          # GUARD this turn: full guard, reflect one hit
        self.reflected = False

    def fx(self):
        return DIRS[self.facing][0]

    def fy(self):
        return DIRS[self.facing][1]

    def front(self):
        return (self.x + self.fx(), self.y + self.fy())


class Game:
    def __init__(self, seed=None, settings=None, th=None, ladder=None):
        self.settings = settings or Settings()
        self.th = th or Thresholds()
        self.rec = Recognizer(self.th, self.settings, ladder or L.Ladder())
        self.ladder = self.rec.ladder
        self.seed = seed if seed is not None else random.randrange(10 ** 9)
        self.rng = random.Random(self.seed)
        self.floor = 0
        self.room_index = 0
        self.plan = self._plan()
        self.turns = 0
        self.pressed_at = []
        self.last_tier, self.last_count, self.last_gaps = "careful", 0, []
        self.last_verb = None
        self.last_action_ms = 0
        self.events = []
        self.chat = []
        self.telemetry = {"presses": [], "bursts": [], "tier_hist": {"careful": 0, "normal": 0, "frantic": 0}}
        self.run_stats = {"rooms": 0, "kills": 0, "damage_taken": 0, "degradations": 0,
                          "relics_taken": 0, "undos": 0, "longest_gap": 0}
        self.undo_stack = []
        self.undo_available = self.settings.calm
        self.drummer_beat = None
        self.room_aware = 0
        self.rec_dial = 0
        self.status = "playing"
        self.offer = None
        self.tax_commit = None
        self._load_room(0)

    # ------------------------------------------------------------- the plan --
    def _plan(self):
        plan = []
        for fi, fl in enumerate(W.FLOORS):
            kinds = list(fl["kind_order"])
            pool = list(fl["relic_pool"])
            self.rng.shuffle(pool)
            for i, kind in enumerate(kinds):
                meta = {"relic": pool[i % len(pool)]}
                if kind == "shop":
                    meta["price"] = 25 + 5 * fi
                plan.append(dict(floor=fi, kind=kind, meta=meta))
        return plan

    def total_rooms(self):
        return len(self.plan)

    # ---------------------------------------------------------------- rooms --
    def _load_room(self, index):
        self.room_index = index
        spec = self.plan[index]
        self.floor = spec["floor"]
        self.room = W.Room(spec["kind"], W.NAMES[spec["kind"]], W.MAPS[spec["kind"]], spec["meta"])
        self.monsters = []
        elite = spec["kind"] == "boss"
        for (x, y, kind) in self.room.monsters:
            # the boss is not also an elite: its fight is the period, not the
            # hit points
            self.monsters.append(Monster(x, y, kind, elite=False))
        for p in self.room.pickups:
            if self.room.kind == "shop":
                p[3] = self.room.meta.get("price", 25)
        sx, sy = self.room.start
        facing = self.room.meta.get("facing", 0)
        self.player = Player(sx, sy, facing)
        self.undo_stack = []
        self.undo_available = self.settings.calm
        self.room_aware = 0
        self.drummer_beat = None
        self.undo_snapshot = None
        self.events.append({"type": "enter_room", "name": self.room.name, "kind": self.room.kind})
        self.run_stats["rooms"] += 1

    def descend(self):
        if self.room_index + 1 < len(self.plan):
            self._load_room(self.room_index + 1)
            return True
        self.status = "complete"
        self.events.append({"type": "run_complete"})
        return False

    # ------------------------------------------------------------- helpers --
    def monster_at(self, x, y):
        for m in self.monsters:
            if m.alive and m.x == x and m.y == y:
                return m
        return None

    def drain_events(self):
        ev, self.events = self.events, []
        return ev

    def log_line(self, s):
        self.chat.append(s)
        del self.chat[:-60]

    def log(self, s):
        self.log_line(s)

    def presses_recent(self, ms):
        now = self.last_action_ms
        return sum(1 for t in self.pressed_at if now - t <= ms)

    def drummer_period(self):
        return 620 if self.floor >= 1 else 800

    # ------------------------------------------------------------ undo (5.4) --
    def snapshot(self):
        return dict(
            px=self.player.x, py=self.player.y, facing=self.player.facing, hp=self.player.hp,
            guard=self.player.guard, turns=self.turns,
            monsters=[(m.x, m.y, m.hp, m.aggro) for m in self.monsters],
            grid=[list(r) for r in self.room.grid],
        )

    def undo(self):
        if not (self.undo_available and self.settings.calm and self.undo_snapshot):
            return False
        s = self.undo_snapshot
        self.player.x, self.player.y, self.player.facing = s["px"], s["py"], s["facing"]
        self.player.hp, self.player.guard, self.turns = s["hp"], s["guard"], s["turns"]
        self.room.grid = s["grid"]
        for m, (x, y, hp, ag) in zip(self.monsters, s["monsters"]):
            m.x, m.y, m.hp, m.aggro, m.alive = x, y, hp, ag, hp > 0
        self.undo_available = False
        self.undo_snapshot = None
        self.run_stats["undos"] += 1
        self.events.append({"type": "undo"})
        self.log_line("undo used - once per room")
        return True

    # --------------------------------------------------------------- verbs --
    def execute(self, ev):
        """run a recognised verb.  ev: {verb,tier,count,gaps}"""
        verb, tier = ev["verb"], ev["tier"]
        if self.status != "playing":
            return
        if verb == "PIVOT":
            self.player.facing = (self.player.facing + ev.get("dir", 1)) % 8
            self.events.append({"type": "pivot", "facing": self.player.facing})
            return
        self.undo_snapshot = self.snapshot()
        self.last_tier, self.last_count, self.last_gaps = tier, ev["count"], ev["gaps"]
        self.last_verb = verb
        self.last_action_ms = self.rec.t
        cost = self.ladder.cost(verb)
        self.turns += cost
        rule = L.TIER_RULE[tier]
        self.telemetry["tier_hist"][tier] += 1
        self.telemetry["bursts"].append(dict(t=self.rec.t, taps=ev["count"], verb=verb, tier=tier,
                                             median=ev.get("median"), gaps=ev["gaps"], turn=self.turns))
        del self.telemetry["bursts"][:-40]

        self.events.append({"type": "verb", "verb": verb, "tier": tier, "count": ev["count"],
                            "x": self.player.x, "y": self.player.y})
        ok = getattr(self, "verb_" + verb.lower())(tier, rule)
        if ok is False:
            self.events.append({"type": "blocked"})
        self.aggro_check(verb, tier, rule)
        if self.player.hp > 0:
            self.enemy_turn()
        self.check_state()
        return ok

    # damage maths
    def damage_for(self, verb, tier, rule):
        base = BASE_DAMAGE.get(verb, 2)
        mult = 1.0 + rule["damage"]
        if tier == "careful" and self.ladder.has("hollow"):
            mult = 3.0
        return max(1, int(round(base * mult)))

    def tile_ahead(self):
        return self.room.tile(*self.player.front())

    def degrade(self, to, why):
        """2.5 graceful degradation, and 14.5 shows it in the ghost."""
        self.run_stats["degradations"] += 1
        self.events.append({"type": "degrade", "to": to, "why": why,
                            "x": self.player.x, "y": self.player.y})
        self.log_line("%s -> %s (%s)" % (self.last_verb, to, why))

    def verb_brace(self, tier, rule):
        g = 2 if self.ladder.has("iron_rest") else 1
        self.player.guard = min(GUARD_CAP, self.player.guard + g)
        if self.ladder.has("iron_rest"):
            self.player.hp = min(MAX_HP, self.player.hp + 1)
        self.events.append({"type": "brace", "x": self.player.x, "y": self.player.y})
        self.log_line("BRACE: guard %d" % self.player.guard)
        if self.ladder.has("fidget") and self.rec.idle_streak >= 2:
            self.move(1, "STEP", "careful", rule)
        return True

    def verb_step(self, tier, rule):
        moved = self.move(1, "STEP", tier, rule)
        return moved

    def verb_strike(self, tier, rule):
        return self.strike(tier, rule, lunge=False)

    def verb_lunge(self, tier, rule):
        return self.strike(tier, rule, lunge=True)

    def verb_guard(self, tier, rule):
        p = self.player
        p.refresh = True
        p.reflected = False
        tx, ty = p.front()
        t = self.room.tile(tx, ty)
        if t == W.CHEST:
            self.events.append({"type": "examine", "x": tx, "y": ty})
            self.log_line("examine: %s" % self.chest_contents(tx, ty))
        m = self.monster_at(tx, ty)
        if m:
            m.note_strike(self.last_tier)
        self.events.append({"type": "guard", "x": p.x, "y": p.y})
        return True

    def verb_sprint(self, tier, rule):
        return self.move(3, "SPRINT", tier, rule)

    # ---------------------------------------------------------------- move --
    def move(self, tiles, verb, tier, rule):
        p = self.player
        path = []
        for i in range(tiles):
            nx, ny = p.x + p.fx(), p.y + p.fy()
            m = self.monster_at(nx, ny)
            if m:
                self.bump(m, tier, rule)
                if verb != "SPRINT" and self.settings.calm:
                    self.degrade("BUMP", "something is in the way")
                return False
            t = self.room.tile(nx, ny)
            if t == W.COUNTER:
                self.shop()
                return False
            if t == W.DOOR:
                # 8.1: a door opens when you Step into it; it costs the step
                self.open_door(nx, ny)
            if t == W.CHEST:
                if self.settings.calm:
                    self.degrade("BUMP", "a chest - Strike it")
                return False
            if self.room.solid(nx, ny):
                if t == W.LOCKED and self.settings.calm:
                    self.degrade("BUMP", "locked - Strike it or find the switch")
                elif self.settings.calm:
                    self.degrade("BUMP", "wall")
                return False
            if t == W.SWITCH:
                self.room.set(nx, ny, W.SWITCH_ON)
                self.toggle_doors()
                self.events.append({"type": "switch", "x": nx, "y": ny})
            p.x, p.y = nx, ny
            path.append((nx, ny))
            self.branch_entered(nx, ny)
            self.pick_up()
            if t == W.STAIRS:
                self.events.append({"type": "stairs", "x": nx, "y": ny})
                self.descend()
                return True
        if path:
            self.events.append({"type": "move", "path": path, "verb": verb})
            if tier != "careful":
                p.guard = min(GUARD_CAP, p.guard + 1 + rule["guard"])
        return bool(path)

    def pick_up(self):
        """6: the grammar itself is the loot.  You take it by walking onto it;
        taking it is paid in turns, and the room goes quiet for the sting."""
        p = self.player
        for pk in self.room.pickups:
            if pk[0] == p.x and pk[1] == p.y and pk[2]:
                r = L.RELIC_BY_ID[pk[2]]
                pk[2] = None
                self.turns += pk[3]
                self.ladder.relics.append(r["id"])
                self.run_stats["relics_taken"] += 1
                self.events.append({"type": "relic", "id": r["id"], "name": r["name"],
                                    "text": r["text"], "price": pk[3]})
                self.log_line("RELIC: %s - %s (%d turns)" % (r["name"], r["text"], pk[3]))

    def relic_adjacent(self):
        p = self.player
        for pk in self.room.pickups:
            if not pk[2]:
                continue
            if abs(pk[0] - p.x) <= 1 and abs(pk[1] - p.y) <= 1:
                return pk
        return None

    def branch_entered(self, x, y):
        """8.2: with one button a branch is told apart by which verb you take
        it with.  The dark branch wakes things; the alcove lets you breathe."""
        role = self.room.branches.get((x, y))
        if not role or (x, y) in getattr(self, "_branches_seen", set()):
            return
        if not hasattr(self, "_branches_seen"):
            self._branches_seen = set()
        self._branches_seen.add((x, y))
        if role == "alcove":
            self.player.guard = min(GUARD_CAP, self.player.guard + 1)
            self.events.append({"type": "alcove", "x": x, "y": y})
            self.log_line("alcove: you breathe, +1 guard")
        elif role == "dark":
            for m in self.monsters:
                if m.alive and abs(m.x - x) <= 8 and abs(m.y - y) <= 8:
                    m.notice(self)
            self.log_line("the dark branch wakes something")

    # --------------------------------------------------------------- strike --
    def strike(self, tier, rule, lunge=False):
        p = self.player
        tx, ty = p.front()
        m = self.monster_at(tx, ty)
        t = self.room.tile(tx, ty)
        hit = False
        if m:
            dmg = self.damage_for("lunge" if lunge else "strike", tier, rule)
            m.notice(self)
            self.events.append({"type": "strike", "x": tx, "y": ty,
                                "dir": p.facing, "lunge": lunge})
            killed = m.hurt(self, dmg, tier)
            self.knockback(m)
            hit = True
            if killed:
                self.run_stats["kills"] += 1
            if self.ladder.has("twin_cut"):
                for dx, dy in ((0, -1), (0, 1)):
                    m2 = self.monster_at(tx + dx, ty + dy)
                    if m2:
                        m2.hurt(self, max(1, dmg // 2), tier)
                        if not m2.alive:
                            self.run_stats["kills"] += 1
        elif t == W.CHEST:
            self.open_chest(tx, ty)
            hit = True
        elif t == W.LOCKED:
            self.room.set(tx, ty, W.DOOR_OPEN)
            self.turns += 1                      # opening a lock costs a turn
            self.events.append({"type": "open", "x": tx, "y": ty, "kind": "lock"})
            self.log_line("the lock breaks")
            hit = True
        if not hit:
            if self.settings.calm:
                self.degrade("STEP", "nothing in front")
                if lunge:
                    return self.move(1, "STEP", tier, rule)
                return self.move(1, "STEP", tier, rule)
            self.events.append({"type": "miss", "x": tx, "y": ty})
            return False
        if lunge:
            nx, ny = tx, ty
            if self.room.walkable(nx, ny, self.monsters):
                self.player.x, self.player.y = nx, ny
                self.events.append({"type": "move", "path": [(nx, ny)], "verb": "LUNGE"})
                self.pick_up()
                if self.room.tile(nx, ny) == W.STAIRS:
                    self.descend()
        return True

    def knockback(self, m):
        p = self.player
        dx, dy = (m.x - p.x) and (1 if m.x > p.x else -1), (m.y - p.y) and (1 if m.y > p.y else -1)
        for step in range(2):
            nx, ny = m.x + dx, m.y + dy
            if self.room.walkable(nx, ny, self.monsters):
                m.x, m.y = nx, ny
                self.events.append({"type": "monster_step", "x": nx, "y": ny})
                break

    def bump(self, m, tier, rule):
        dmg = 1
        m.notice(self)
        self.player.hp -= dmg
        self.run_stats["damage_taken"] += dmg
        self.events.append({"type": "player_hit", "dmg": dmg, "x": self.player.x, "y": self.player.y,
                            "why": "bump"})
        self.events.append({"type": "damage", "x": m.x, "y": m.y, "dmg": 0, "tier": tier})
        self.log_line("bump: 1 damage")

    # --------------------------------------------------------------- tiles --
    def open_door(self, x, y):
        self.room.set(x, y, W.DOOR_OPEN)
        self.events.append({"type": "open", "x": x, "y": y, "kind": "door"})
        self.log_line("door opens")

    def toggle_doors(self):
        for row in range(self.room.h):
            for col in range(self.room.w):
                if self.room.tile(col, row) in (W.DOOR, W.LOCKED):
                    self.room.set(col, row, W.DOOR_OPEN)
                    self.events.append({"type": "open", "x": col, "y": row, "kind": "door"})

    def chest_contents(self, x, y):
        return "a relic, and it is watching you" if self.monster_at(x, y) else "turns"

    def open_chest(self, x, y):
        self.room.set(x, y, W.CHEST_OPEN)
        self.events.append({"type": "open", "x": x, "y": y, "kind": "chest"})
        self.log_line("chest opens")

    def shop(self):
        self.events.append({"type": "shop"})
        self.log_line("counter of turns - GUARD a relic to buy it")

    # --------------------------------------------------------------- aggro --
    def aggro_check(self, verb, tier, rule):
        loud = verb in ("STRIKE", "LUNGE", "SPRINT") or tier == "frantic"
        if not loud and verb == "STEP" and tier == "careful":
            return
        p = self.player
        for m in self.monsters:
            if not m.alive:
                continue
            if abs(m.x - p.x) <= 6 and abs(m.y - p.y) <= 6:
                if verb in ("STRIKE", "LUNGE", "SPRINT") or tier == "frantic" or \
                        (verb == "STEP" and m.aggro):
                    m.notice(self)

    # ------------------------------------------------------------ Live mode --
    def live_tick(self, now_ms):
        """3: Live mode is a dial, not a mode war.  Enemies also move on a
        real-time clock; the player's verbs are unchanged."""
        if not self.settings.live or self.status != "playing":
            return False
        if now_ms - getattr(self, "_live_at", 0) < self.settings.live_period:
            return False
        self._live_at = now_ms
        self.events.append({"type": "live_tick"})
        self.enemy_turn()
        self.check_state()
        return True

    # ------------------------------------------------------- enemy half-turn --
    def enemy_turn(self):
        for m in self.monsters:
            if m.alive:
                m.act(self)
        self.player.refresh = False

    def hurt_player(self, dmg, source=None):
        p = self.player
        guard = max(p.guard, 3) if p.refresh else p.guard
        if p.refresh and source is not None and not p.reflected:
            p.reflected = True
            self.events.append({"type": "reflect", "x": source.x, "y": source.y})
            self.knockback(source)
            source.hurt(self, 1, self.last_tier)
            dmg = 0
        if guard:
            dmg = max(0, dmg - guard)
            p.guard = max(0, p.guard - max(1, guard if p.refresh else 1))
        if dmg:
            p.hp -= dmg
            self.run_stats["damage_taken"] += dmg
            self.events.append({"type": "player_hit", "dmg": dmg, "x": p.x, "y": p.y})
            self.log_line("you take %d" % dmg)
        else:
            self.events.append({"type": "guarded", "x": p.x, "y": p.y})

    def check_state(self):
        if self.player.hp <= 0:
            self.status = "dead"
            self.events.append({"type": "death"})
            self.log_line("you die on floor %d" % (self.floor + 1))
        if self.turns > 300:
            self.log_line("the room takes you: out of turns")

    # ------------------------------------------------------- run profile ----
    def median_gap(self):
        gaps = []
        prev = None
        for t in self.telemetry["presses"]:
            if prev is not None and t - prev < self.th.SLOW_GAP * 3:
                gaps.append(t - prev)
            prev = t
        if not gaps:
            return 0
        gaps.sort()
        return gaps[len(gaps) // 2]

    def gap_samples(self):
        out, prev = [], None
        for t in self.telemetry["presses"]:
            if prev is not None:
                out.append(t - prev)
            prev = t
        return out[-40:]

    def profile(self):
        th = self.th
        return dict(
            hp=self.player.hp, max_hp=MAX_HP, guard=self.player.guard,
            floor=self.floor + 1, room=self.room_index + 1, total_rooms=self.total_rooms(),
            turns=self.turns, relics=list(self.ladder.relics), ladder=self.ladder.describe(),
            last_bursts=self.telemetry["bursts"][-5:], tiers=dict(self.telemetry["tier_hist"]),
            median_gap=self.median_gap(), room_name=self.room.name,
            enemies=[dict(name=m.name, hp=m.hp, max_hp=m.max_hp, aggro=m.aggro,
                          telegraph=m.telegraph) for m in self.monsters if m.alive],
            stats=dict(self.run_stats), longest=self.run_stats["longest_gap"],
            thresholds=vars(th), status=self.status,
        )

    # ------------------------------------------------------------ save/resume --
    def save(self, path=SAVE_PATH):
        data = dict(seed=self.seed, floor=self.floor, room_index=self.room_index,
                    turns=self.turns, hp=self.player.hp, guard=self.player.guard,
                    facing=self.player.facing, px=self.player.x, py=self.player.y,
                    relics=list(self.ladder.relics),
                    monsters=[(m.kind, m.x, m.y, m.hp, m.elite, m.aggro) for m in self.monsters],
                    grid=[list(r) for r in self.room.grid],
                    stats=dict(self.run_stats), telemetry=self.telemetry,
                    settings=vars(self.settings), th=vars(self.th))
        write_json(path, data)
        return path

    @classmethod
    def load(cls, path=SAVE_PATH):
        data = read_json(path)
        if not data:
            return None
        st = Settings(**{k: v for k, v in data["settings"].items() if k in vars(Settings())})
        th = Thresholds(**{k: v for k, v in data["th"].items() if k in vars(Thresholds())})
        g = cls(data["seed"], st, th, L.Ladder(data["relics"]))
        g.turns = data["turns"]
        g.player.hp, g.player.guard, g.player.facing = data["hp"], data["guard"], data["facing"]
        g.player.x, g.player.y = data["px"], data["py"]
        g._load_room(data["room_index"])
        g.player.hp, g.player.guard, g.player.facing = data["hp"], data["guard"], data["facing"]
        g.player.x, g.player.y = data["px"], data["py"]
        g.room.grid = data["grid"]
        g.monsters = []
        for (kind, x, y, hp, elite, ag) in data["monsters"]:
            m = Monster(x, y, kind, elite=elite)
            m.hp, m.aggro = hp, ag
            g.monsters.append(m)
        g.run_stats.update(data["stats"])
        g.telemetry.update(data["telemetry"])
        return g


def write_json(path, data):
    try:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as fh:
            json.dump(data, fh)
        return True
    except Exception:
        return False


def read_json(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except Exception:
        return None
