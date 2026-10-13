"""The verb ladder (DESIGN.md 2.1), the tier rule (2.2) and grammar relics (6).

Six rungs is the hard ceiling on the verb set; everything else is a modifier on
these six (9, 14.7).  The meter, the poster, the ghost, the tutorial cards and
the sound motifs all read the rungs from here, so they cannot drift apart.
"""
from statistics import median

from . import theme as T

RUNGS = [
    # n taps, verb, glyph (the shape law: rung n has n sides), turn cost
    dict(n=0, name="BRACE", glyph="ring", cost=0, effect="+1 Guard on the tile you face; enemies move free"),
    dict(n=1, name="STEP", glyph="dot", cost=1, effect="move one tile along facing"),
    dict(n=2, name="STRIKE", glyph="lens", cost=1, effect="attack the tile in front"),
    dict(n=3, name="LUNGE", glyph="ngon3", cost=1, effect="attack, then hop into the vacated tile"),
    dict(n=4, name="GUARD", glyph="ngon4", cost=1, effect="full guard this turn, reflect one hit"),
    dict(n=5, name="SPRINT", glyph="ngon5", cost=3, effect="move three tiles in a line, stop on contact"),
]
BY_NAME = {r["name"]: r for r in RUNGS}
MAX_TAPS = 5

TIER_RULE = {
    "careful": dict(damage=-0.25, guard=+1, aggro=0, label="CAREFUL", colour=T.ASH),
    "normal": dict(damage=0.0, guard=0, aggro=0, label="NORMAL", colour=T.LANTERN),
    "frantic": dict(damage=+0.30, guard=0, aggro=+1, label="FRANTIC", colour=T.EMBER),
}


def glyph_for_count(n):
    return RUNGS[min(max(int(n), 0), MAX_TAPS)]["glyph"]


def tier_for(gap_ms, th, frantic_allowed=True):
    """2.2: the median gap between presses is the tier."""
    if gap_ms < th.FAST_GAP:
        return "normal" if not frantic_allowed else "frantic"
    if gap_ms > th.SLOW_GAP:
        return "careful"
    return "normal"


# -------------------------------------------------------------- grammar loot --
RELICS = [
    dict(id="metronome", name="METRONOME", glyph="ngon5",
         text="commit window +120 ms - more time to escalate, fewer misclicks"),
    dict(id="hair_trigger", name="HAIR TRIGGER", glyph="lens",
         text="commit window -90 ms, FRANTIC unreachable - fast but brittle"),
    dict(id="twin_cut", name="TWIN CUT", glyph="ngon4",
         text="Strike also hits the two tiles beside the one in front"),
    dict(id="stutter", name="STUTTER", glyph="ngon3",
         text="your 3rd press in any burst costs nothing: LUNGE is free"),
    dict(id="hollow", name="HOLLOW CADENCE", glyph="ring",
         text="CAREFUL-tier verbs deal triple damage - slow play becomes the build"),
    dict(id="drummer_relic", name="DRUMMER", glyph="dot",
         text="5-tap SPRINT costs 1 turn instead of 3"),
    dict(id="iron_rest", name="IRON REST", glyph="ring",
         text="BRACE grants Guard 2 and heals 1"),
    dict(id="offbeat", name="OFFBEAT", glyph="lens",
         text="the ladder reverses: 1 tap = STRIKE, 2 taps = STEP"),
    dict(id="fidget", name="FIDGET", glyph="dot",
         text="idle twice in a row and you automatically STEP - Bracing is gone"),
]
RELIC_BY_ID = {r["id"]: r for r in RELICS}


class Ladder:
    """the rungs as the player currently has them; relics edit this (6)."""

    def __init__(self, relics=()):
        self.relics = list(relics)

    def has(self, rid):
        return rid in self.relics

    def verb_for(self, taps):
        n = min(max(int(taps), 1), MAX_TAPS)
        if self.has("offbeat"):
            n = {1: 2, 2: 1}.get(n, n)
        return RUNGS[n]["name"]

    def rung(self, verb):
        return BY_NAME[verb]

    def cost(self, verb):
        c = BY_NAME[verb]["cost"]
        if verb == "LUNGE" and self.has("stutter"):
            return 0
        if verb == "SPRINT" and self.has("drummer_relic"):
            return 1
        return c

    def frantic_allowed(self):
        return not self.has("hair_trigger")

    def commit_window(self, base):
        c = base
        if self.has("metronome"):
            c += 120
        if self.has("hair_trigger"):
            c -= 90
        return max(80, c)

    def poster_rows(self):
        rows = []
        for r in RUNGS:
            taps = r["n"]
            if self.has("offbeat") and r["n"] in (1, 2):
                taps = {1: 2, 2: 1}[r["n"]]
            rows.append(dict(r, taps=taps))
        return rows

    def describe(self):
        return "  ".join("%d=%s" % (r["taps"], r["name"])
                         for r in self.poster_rows() if r["n"])
