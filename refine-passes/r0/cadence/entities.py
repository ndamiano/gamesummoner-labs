"""The player and the enemies (DESIGN.md 4.2, 7).

Enemies are telegraphed and deterministic.  Several archetypes are keyed to the
player's cadence - that is the whole point of section 7: the encounter reads
your rhythm back at you.  Each one's telegraph is its shape and its eye
brightness (14.3: enemies are holes in the light with one bright feature).
"""
import random

DIRS = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]


def towards(fx, fy, tx, ty, allow_diagonal=True):
    """greedy steps, 8-way (4-way when the room is a corridor)."""
    dx, dy = tx - fx, ty - fy
    cands = []
    for d in DIRS:
        if not allow_diagonal and (d[0] and d[1]):
            continue
        if (d[0] and (d[0] > 0) == (dx > 0)) or (d[1] and (d[1] > 0) == (dy > 0)):
            if d[0] and d[1] and not (dx and dy):
                continue
            cands.append((abs(dx if d[0] else 0) + abs(dy if d[1] else 0), d))
    cands.sort(key=lambda c: -c[0])
    return [d for _, d in cands]


class Monster:
    hp, dmg, eye_off = 2, 1, "ash"

    def __init__(self, x, y, kind="rat", elite=False):
        self.kind = kind
        self.x, self.y = x, y
        self.elite = elite
        spec = SPEC[kind]
        self.hp = self.max_hp = spec["hp"] * (2 if elite else 1)
        self.dmg = spec["dmg"]
        self.name = ("ELITE " if elite else "") + spec["name"]
        self.telegraph = spec["telegraph"]
        self.glyph = spec["glyph"]
        self.aggro = False
        self.alive = True
        self.struck_tier = None
        self.struck_same = 0
        self.guard_broken = False
        self.sides = spec["sides"]

    # ---------------------------------------------------------------- hit --
    def hurt(self, game, dmg, from_tier=None):
        spec = SPEC[self.kind]
        if self.kind == "drummer":
            if not self.guard_broken:
                game.log("%s: guard up - you played off the beat" % self.name)
                return False
            self.guard_broken = False       # one hit per beat, then it is up again
        if self.kind == "priestess" and self.struck_same < 3:
            game.log("%s: immune (%d/3 same-tier strikes)" % (self.name, self.struck_same))
            return False
        self.hp -= dmg
        game.events.append({"type": "damage", "x": self.x, "y": self.y, "dmg": dmg,
                            "tier": from_tier})
        if self.hp <= 0:
            self.alive = False
            game.log("%s dies" % self.name)
            return True
        return False

    def note_strike(self, tier):
        if self.kind == "priestess":
            if self.struck_tier == tier:
                self.struck_same += 1
            else:
                self.struck_tier, self.struck_same = tier, 1

    def notice(self, game, loud=True):
        if not self.aggro:
            self.aggro = True
            game.log("%s turns to you" % self.name)
            game.room_aware += 1

    # ------------------------------------------------------------- moving --
    def step_to(self, game, dx, dy):
        nx, ny = self.x + dx, self.y + dy
        if game.room.walkable(nx, ny, game.monsters):
            self.x, self.y = nx, ny
            game.events.append({"type": "monster_step", "x": nx, "y": ny})
            return True
        return False

    def step_towards(self, game, allow_diag=True):
        p = game.player
        for d in towards(self.x, self.y, p.x, p.y, allow_diag):
            if self.step_to(game, *d):
                return True
        return False

    def step_away(self, game, allow_diag=True):
        p = game.player
        for d in towards(p.x, p.y, self.x, self.y, allow_diag):
            if self.step_to(game, *d):
                return True
        return False

    def adjacent(self, game):
        p = game.player
        return abs(p.x - self.x) <= 1 and abs(p.y - self.y) <= 1

    def attack(self, game):
        game.hurt_player(self.dmg, source=self)

    # ------------------------------------------------------------ the turn --
    def act(self, game):
        spec = SPEC[self.kind]
        if self.adjacent(game):
            self.attack(game)
            return
        if not spec["moves"]:
            return
        behavior = spec["behavior"]
        if behavior == "rat":
            if self.aggro:
                self.step_towards(game)
            elif game.rng.random() < 0.35:
                self.step_towards(game)
        elif behavior == "sentinel":
            if game.last_tier == "careful":
                game.events.append({"type": "telegraph", "x": self.x, "y": self.y,
                                    "text": "FROZEN"})
                return                      # freezes while you are Careful
            if game.last_tier == "frantic":
                self.step_away(game)        # flinches at Frantic
                return
            self.step_towards(game)
        elif behavior == "mirror":
            n = max(0, min(3, game.last_count))
            for _ in range(n):
                if not self.step_towards(game):
                    break
            game.events.append({"type": "telegraph", "x": self.x, "y": self.y,
                                "text": "x%d" % n})
        elif behavior == "tic":
            self.step_towards(game)         # you are its clock
        elif behavior == "swarm":
            if game.presses_recent(1000) >= 6:
                self.notice(game)
                self.step_towards(game)
            elif game.rng.random() < 0.4:
                self.step_to(game, *game.rng.choice(DIRS))
        elif behavior == "priestess":
            if game.rng.random() < 0.3:
                self.hp = min(self.max_hp, self.hp + 1)
            self.step_towards(game)
        elif behavior == "drummer":
            # 7: it keeps a period at you and its guard is up except for the
            # one verb after each beat.  Three quarters of what you do to it
            # lands off the beat and does nothing - the fight is about finding
            # the one that does not.
            game.drummer_beat = 0 if game.drummer_beat is None else (game.drummer_beat + 1) % 4
            self.guard_broken = (game.drummer_beat == 0)
            if self.guard_broken:
                game.events.append({"type": "beat", "x": self.x, "y": self.y,
                                    "period": game.drummer_period()})
            self.step_towards(game, allow_diag=False)


SPEC = {
    "rat": dict(name="RAT", hp=2, dmg=1, behavior="rat", moves=True, sides=6,
                glyph="ngon6", telegraph="still until it sees you"),
    "sentinel": dict(name="SENTINEL", hp=4, dmg=2, behavior="sentinel", moves=True, sides=7,
                     glyph="ngon7", telegraph="freezes while you are Careful"),
    "mirror": dict(name="MIRROR", hp=5, dmg=2, behavior="mirror", moves=True, sides=8,
                   glyph="ngon8", telegraph="copies your last burst"),
    "tic": dict(name="TIC", hp=3, dmg=1, behavior="tic", moves=True, sides=5,
                glyph="ngon5", telegraph="one tile per press of yours"),
    "priestess": dict(name="PRIESTESS", hp=6, dmg=2, behavior="priestess", moves=True,
                      sides=3, glyph="ngon3", telegraph="immune until 3 strikes at one tier"),
    "swarm": dict(name="SWARM", hp=3, dmg=1, behavior="swarm", moves=True, sides=4,
                  glyph="ngon4", telegraph="wakes when you press too much"),
    "drummer": dict(name="THE DRUMMER", hp=14, dmg=3, behavior="drummer", moves=True,
                    sides=12, glyph="ngon12", telegraph="guard breaks only on its beat",
                    immune=True),
}
