#!/usr/bin/env python3
"""Generate the figures referenced by DESIGN.md section 14 (Visual design).

    python3 figures/make_figures.py

Written with the same primitives, palette and shape law the game renderer is
meant to use, so this file is the seed of the renderer rather than a throwaway:
no bitmaps, no external fonts, everything drawn from polygon + ellipse + line.
"""
import math
from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------- palette --
INK = "#0E1116"        # void, outside the light
SLATE = "#1B2129"      # unlit floor
STONE = "#2C343F"      # walls
EDGE = "#39424E"       # inactive UI lines, unlit rungs
ASH = "#8C93A0"        # careful tier, secondary text
CHALK = "#E8E4DA"      # the player, primary text
LANTERN = "#E8A33D"    # normal tier, light, intent ghost
EMBER = "#D4483B"      # frantic tier, damage, aggro
TEAL = "#4FA3A5"       # room affordances: doors, chests, stairs
VIOLET = "#7C6BD1"     # the grammar itself: relics, ladder changes

FLOOR_NEAR = "#28313C"
TIER = {"careful": ASH, "normal": LANTERN, "frantic": EMBER}

VERBS = [  # name, taps, glyph shape, cost
    ("BRACE", 0, "ring", "free"),
    ("STEP", 1, "dot", "1 turn"),
    ("STRIKE", 2, "lens", "1 turn"),
    ("LUNGE", 3, "ngon3", "1 turn"),
    ("GUARD", 4, "ngon4", "1 turn"),
    ("SPRINT", 5, "ngon5", "3 turns"),
]

# ------------------------------------------------------------------ helper --
_fc = {}


def F(sz):
    if sz not in _fc:
        _fc[sz] = ImageFont.load_default(sz)
    return _fc[sz]


def canvas(w, h, bg=INK):
    im = Image.new("RGB", (w, h), bg)
    return im, ImageDraw.Draw(im)


def txt(d, xy, s, sz=15, fill=CHALK, anchor="lt", bold=False):
    if bold:
        for dx, dy in ((0, 0), (1, 0), (0, 1)):
            d.text((xy[0] + dx, xy[1] + dy), s, font=F(sz), fill=fill, anchor=anchor)
    else:
        d.text(xy, s, font=F(sz), fill=fill, anchor=anchor)


def mix(a, b, t):
    """fake alpha: mix hex a (background) toward hex b by t"""
    pa, pb = a.lstrip("#"), b.lstrip("#")
    return "#" + "".join("%02x" % int(round(int(pa[i:i + 2], 16) * (1 - t) + int(pb[i:i + 2], 16) * t))
                         for i in (0, 2, 4))


def ngon(cx, cy, r, n, rot=None):
    if rot is None:
        rot = -90 + (180.0 / n if n % 2 == 0 else 0)
    return [(cx + r * math.cos(math.radians(rot + i * 360.0 / n)),
             cy + r * math.sin(math.radians(rot + i * 360.0 / n))) for i in range(n)]


def vesica(cx, cy, r):
    """a 2-sided lens: intersection of two circles of radius r offset by r/2"""
    dd, pts = r / 2.0, []
    for i in range(13):
        a = math.radians(-60 + 120 * i / 12)
        pts.append((cx - dd + r * math.cos(a), cy + r * math.sin(a)))
    for i in range(13):
        a = math.radians(120 + 120 * i / 12)
        pts.append((cx + dd + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def glyph(d, shape, cx, cy, r, col=CHALK, fill=None, w=2):
    """the shape law: rung n is a polygon with n sides (0 = open ring, 1 = dot)"""
    if shape == "ring":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=w)
    elif shape == "dot":
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill or col)
    elif shape == "lens":
        p = vesica(cx, cy, r)
        if fill:
            d.polygon(p, fill=fill)
        d.line(p + [p[0]], fill=col, width=w)
    else:
        n = int(shape[-1])
        p = ngon(cx, cy, r, n)
        if fill:
            d.polygon(p, fill=fill)
        d.line(p + [p[0]], fill=col, width=w)


def head(d, w, title, sub):
    txt(d, (40, 34), title, 26, CHALK, bold=True)
    txt(d, (40, 70), sub, 14, ASH)
    d.line([(40, 96), (w - 40, 96)], fill=EDGE, width=1)


def caption(d, w, h, s):
    txt(d, (40, h - 34), s, 13, ASH)


def taps(d, x, y, n, col=CHALK, r=4, gap=16):
    for i in range(n):
        d.ellipse([x + i * gap - r, y - r, x + i * gap + r, y + r], fill=col)


# ------------------------------------------------------- 01 shapes+palette --
def fig_shapes(path):
    W, H = 1200, 680
    im, d = canvas(W, H)
    head(d, W, "14.2  The shape law", "rung n is a polygon with n sides - tap count reads with colour removed and audio off")

    y, x = 210, 120
    for name, n, shape, cost in VERBS:
        d.ellipse([x - 46, y - 46, x + 46, y + 46], outline=EDGE, width=1)
        glyph(d, shape, x, y, 26, col=CHALK, fill=mix(INK, CHALK, 0.12))
        txt(d, (x, y + 66), name, 15, CHALK, "mm", bold=True)
        txt(d, (x, y + 88), ("%d taps" % n) if n else "no input", 13, ASH, "mm")
        x += 190

    txt(d, (40, 330), "PALETTE - ten colours, three hue families, never more than five lit at once", 14, CHALK, bold=True)
    sw = [("INK", INK, "void"), ("SLATE", SLATE, "floor"), ("STONE", STONE, "walls"),
          ("EDGE", EDGE, "inactive"), ("ASH", ASH, "careful"), ("CHALK", CHALK, "player"),
          ("LANTERN", LANTERN, "normal / intent"), ("EMBER", EMBER, "frantic / damage"),
          ("TEAL", TEAL, "affordance"), ("VIOLET", VIOLET, "grammar")]
    x, y = 40, 366
    for i, (n, c, role) in enumerate(sw):
        d.rectangle([x, y, x + 92, y + 46], fill=c, outline=EDGE, width=1)
        txt(d, (x, y + 56), n, 13, CHALK, "lt", True)
        txt(d, (x, y + 74), c.upper(), 12, ASH)
        txt(d, (x, y + 92), role, 12, mix(ASH, INK, 0.25))
        x += 116
        if i == 4:
            x, y = 40, y + 118
    caption(d, W, H, "warm = you and your rhythm | cool = the room's affordances | violet = the grammar itself")
    im.save(path)


# --------------------------------------------------- 02 cadence meter states --
def meter(d, x, y, w, h, lit, tier, jitter=False):
    col = TIER[tier]
    d.rounded_rectangle([x, y, x + w, y + h], 8, fill=mix(INK, col, 0.05), outline=EDGE, width=1)
    if jitter:  # frantic: the frame itself vibrates - the tier is legible in motion
        for off in (-3, 3):
            d.rounded_rectangle([x + off, y, x + w + off, y + h], 8, outline=mix(INK, col, 0.35), width=1)
    d.line([(x + 12, y + h - 9), (x + w - 12, y + h - 9)], fill=mix(INK, col, 0.65), width=2)
    step = (w - 80) / 5.0
    for i, (name, n, shape, cost) in enumerate(VERBS):
        cx, cy = x + 50 + i * step, y + h / 2 - 4
        if i < lit:
            glyph(d, shape, cx, cy, 14, col=col, fill=mix(INK, col, 0.45), w=2)
        else:
            glyph(d, shape, cx, cy, 14, col=mix(EDGE, INK, 0.15), w=2)
    if lit:
        cx = x + 50 + (lit - 1) * step
        d.line([(cx, y + 6), (cx, y + h - 6)], fill=col, width=1)


def fig_meter(path):
    W, H = 1200, 720
    im, d = canvas(W, H)
    head(d, W, "14.4  The cadence meter", "bottom centre, always on: six rungs, one playhead, three tiers - the player's own rhythm mirrored back")

    rows = [
        ("no input for 1.5 s", "IDLE", 1, "careful", "BRACE - free, +1 Guard"),
        ("1 tap, gap 900 ms", "CAREFUL", 2, "careful", "STEP - silent, +1 Guard afterwards"),
        ("2 taps, gap 420 ms", "NORMAL", 3, "normal", "STRIKE - as printed"),
        ("5 taps, gap 180 ms", "FRANTIC", 6, "frantic", "SPRINT - +30% damage, +1 Aggro, no Guard"),
    ]
    y = 128
    for label, tier_name, lit, tier, outcome in rows:
        txt(d, (40, y + 26), label, 14, ASH)
        txt(d, (40, y + 50), tier_name, 13, TIER[tier], "lt", True)
        meter(d, 250, y, 560, 92, lit, tier, jitter=(tier == "frantic"))
        txt(d, (840, y + 38), outcome, 14, CHALK)
        y += 112

    txt(d, (250, y + 4), "TIER IS ENCODED THREE TIMES OVER: rung shape, rung position, and motion", 14, CHALK, "lt", True)
    txt(d, (250, y + 28), "(static / slow pulse / jitter) - hue is never the only channel; reduced-motion swaps jitter for a solid frame", 13, ASH)
    caption(d, W, H, "460 px wide at 1080p; rungs never move; the playhead only ever travels left to right")
    im.save(path)


# ------------------------------------------------------- 03 verb ladder poster --
def fig_poster(path):
    W, H = 980, 830
    im, d = canvas(W, H)
    head(d, W, "14.7  The ladder poster", "Pause > Ladder: the whole verb set on one screen, in the layout the player has been reading all run")
    EFFECT = {"BRACE": "+1 Guard on the tile you face; enemies move free",
              "STEP": "move one tile along facing",
              "STRIKE": "attack the tile in front",
              "LUNGE": "attack, then hop into the vacated tile",
              "GUARD": "full guard this turn, reflect one hit",
              "SPRINT": "move three tiles in a line, stop on contact"}
    d.rounded_rectangle([40, 116, W - 40, H - 60], 10, outline=EDGE, width=1)
    txt(d, (86, 140), "GLYPH", 11, ASH)
    txt(d, (180, 140), "TAPS", 11, ASH)
    txt(d, (400, 140), "VERB / EFFECT", 11, ASH)
    txt(d, (900, 140), "COST", 11, ASH, "rm")
    d.line([(60, 162), (W - 60, 162)], fill=EDGE, width=1)
    y = 176
    for idx, (name, n, shape, cost) in enumerate(VERBS):
        tier = ASH if n == 0 else (LANTERN if n <= 3 else EMBER)
        if idx:
            d.line([(60, y - 8), (W - 60, y - 8)], fill=mix(EDGE, INK, 0.4), width=1)
        glyph(d, shape, 110, y + 34, 22, col=CHALK, fill=mix(INK, tier, 0.32))
        taps(d, 180, y + 34, n, col=ASH)
        txt(d, (300, y + 34), ("%d taps" % n) if n else "no input", 12, ASH, "lm")
        txt(d, (400, y + 24), name, 20, CHALK, "lm", True)
        txt(d, (400, y + 52), EFFECT[name], 13, mix(ASH, INK, 0.15), "lm")
        txt(d, (900, y + 34), cost, 14, tier, "rm")
        y += 96
    caption(d, W, H, "six rungs is the hard ceiling on the verb set; everything else is a modifier on these six")
    im.save(path)


# --------------------------------------------------- 04 screen composition ---
def fig_screen(path):
    W, H = 1300, 860
    TOP, BOT = 106, 792          # the world is only ever drawn inside this band
    im, d = canvas(W, H)
    head(d, W, "14.3  Screen composition",
         "the world geometry rotates so facing reads up-right; every glyph, label and meter stays screen-aligned")

    layer = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(layer)

    # the map as the renderer keeps it: one character per tile
    GW, GH = 26, 20
    g = [["#"] * GW for _ in range(GH)]

    def carve(c0, r0, c1, r1):
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                g[r][c] = "."

    carve(5, 10, 16, 17)         # the room you are standing in
    carve(5, 2, 16, 6)           # the room above, mostly off the top of the view
    carve(11, 7, 11, 9)          # one-tile corridor: the bottleneck
    g[9][11] = "+"               # the door at its mouth
    for r in (12, 13):           # a pillar, so the room is not open floor
        for c in (8, 9):
            g[r][c] = "#"
    g[12][15] = "R"              # relic
    g[13][6] = "C"               # locked chest
    g[10][14] = "e"              # enemy, unaware, by the door
    g[15][15] = "e"              # enemy, waiting
    g[13][12] = "e"              # the one in front of you
    g[14][12] = "P"

    TS = 46
    ANG = math.radians(20)       # clockwise: world-up reads as up-right on screen
    C, S = math.cos(ANG), math.sin(ANG)
    pcx, pcy = 12.5 * TS, 14.5 * TS
    SCX, SCY = 640, 470          # you are always the centre of the light

    def W2S(wx, wy):
        dx, dy = wx - pcx, wy - pcy
        return (SCX + dx * C - dy * S, SCY + dx * S + dy * C)

    def tc(c, r):
        return (c + 0.5) * TS, (r + 0.5) * TS

    def lit(wx, wy):
        return min(1.0, math.hypot(wx - pcx, wy - pcy) / (TS * 7.2))

    pad = TS * 0.03
    for r in range(GH):
        for c in range(GW):
            wx, wy = tc(c, r)
            t = lit(wx, wy)
            pts = [W2S(c * TS + dx, r * TS + dy) for dx, dy in
                   ((-pad, -pad), (TS + pad, -pad), (TS + pad, TS + pad), (-pad, TS + pad))]
            if g[r][c] == "#":  # walls read as holes: always darker than the floor
                d.polygon(pts, fill=mix("#151A21", INK, t * 0.5))
                near = mix(INK, mix(EDGE, ASH, 0.55), (1 - t) * 0.85)
                d.line([pts[0], pts[1]], fill=near, width=1)      # lit lip, facing the lantern
                d.line([pts[3], pts[0]], fill=near, width=1)
            else:
                floor = mix(FLOOR_NEAR, SLATE, t)
                if t < 0.45:
                    floor = mix(floor, mix(SLATE, LANTERN, 0.14), (0.45 - t) * 0.8)  # the lantern's warmth
                d.polygon(pts, fill=floor)
                if (c + r) % 3 == 0:  # floor grain: scale without texture noise
                    d.point(W2S(*tc(c, r)), fill=mix(floor, CHALK, 0.10))

    def anchor(c, r):
        return W2S(*tc(c, r))

    def shade(c, r, col):
        return mix(INK, col, max(0.3, 1.0 - lit(*tc(c, r))))

    # affordances: teal is the room's verbs, violet is the grammar
    cx, cy = anchor(11, 9)
    col = shade(11, 9, TEAL)
    d.rounded_rectangle([cx - 15, cy - 15, cx + 15, cy + 15], 5, outline=col, width=2)
    d.line([(cx - 15, cy), (cx + 15, cy)], fill=col, width=2)

    cx, cy = anchor(6, 13)
    col = shade(6, 13, TEAL)
    for a in range(0, 360, 45):  # dashed ring = locked
        p0 = (cx + 15 * math.cos(math.radians(a)), cy + 15 * math.sin(math.radians(a)))
        p1 = (cx + 15 * math.cos(math.radians(a + 25)), cy + 15 * math.sin(math.radians(a + 25)))
        d.line([p0, p1], fill=col, width=3)

    cx, cy = anchor(15, 12)
    col = shade(15, 12, VIOLET)
    p = ngon(cx, cy, 13, 5)
    d.line(p + [p[0]], fill=col, width=2)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)

    # enemies: darker than the floor they stand on, one bright feature each
    for c, r in [(14, 10), (15, 15)]:
        cx, cy = anchor(c, r)
        p = ngon(cx, cy, 17, 6)
        d.polygon(p, fill="#090c10")
        d.line(p + [p[0]], fill=mix(INK, CHALK, 0.22), width=1)
        d.ellipse([cx - 3, cy - 4, cx + 3, cy + 2], fill=shade(c, r, EMBER))

    # the tile in front: intent ghost under the enemy, both drawn screen-aligned
    gx, gy = anchor(12, 13)
    quad = [W2S(12 * TS + 3, 13 * TS + 3), W2S(13 * TS - 3, 13 * TS + 3),
            W2S(13 * TS - 3, 14 * TS - 3), W2S(12 * TS + 3, 14 * TS - 3)]
    d.polygon(quad, fill=mix(FLOOR_NEAR, LANTERN, 0.16))
    d.line(quad + [quad[0]], fill=LANTERN, width=2)
    p = ngon(gx, gy, 17, 6)
    d.polygon(p, fill="#090c10")
    d.line(p + [p[0]], fill=mix(INK, CHALK, 0.22), width=1)
    glyph(d, "lens", gx, gy, 14, col=LANTERN, fill=mix(INK, LANTERN, 0.35))

    # you: the brightest object on screen, facing shown on your own rim
    d.ellipse([SCX - 17, SCY - 17, SCX + 17, SCY + 17], fill=CHALK)
    d.polygon([W2S(pcx, pcy - 28), W2S(pcx - 8, pcy - 15), W2S(pcx + 8, pcy - 15)], fill=LANTERN)
    pips = []
    for i in range(2):  # guard pips live on the player - there is no health bar
        a = math.radians(150 + i * 22)
        ex, ey = W2S(pcx + 25 * math.cos(a), pcy + 25 * math.sin(a))
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=mix(CHALK, INK, 0.3))
        pips.append((ex, ey))

    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle([0, TOP, W, BOT], fill=255)
    im.paste(layer, (0, 0), mask)
    d = ImageDraw.Draw(im)

    # HUD - never rotated, never over the tile in front
    txt(d, (40, 122), "F2   ROOM 14/25", 15, CHALK, "lt", True)
    txt(d, (40, 146), "TURN 128", 13, ASH)
    meter(d, W // 2 - 280, 700, 560, 74, 3, "normal")
    txt(d, (W // 2, 692), "cadence meter - bottom centre, always on, never covered", 12, ASH, "mb")

    def note(p, q, label, col=ASH, side="r"):
        d.line([p, q], fill=mix(EDGE, col, 0.55), width=1)
        d.ellipse([p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2], fill=col)
        txt(d, q, label, 12, col, "rm" if side == "r" else "lm")

    note(anchor(11, 9), (1258, 168), "door: teal, opens to a Step (the corridor is one tile wide)", TEAL)
    note(anchor(15, 12), (1258, 262), "relic: the only violet in the room", VIOLET)
    note((gx, gy), (1258, 372), "intent ghost: the verb glyph itself, 16% on the floor", LANTERN)
    note((SCX, SCY), (1258, 620), "you: brightest object, facing on your own rim", CHALK)
    note(anchor(6, 13), (42, 200), "locked chest: dashed teal, smashes to a Strike", TEAL, "l")
    note(anchor(15, 15), (1258, 480), "enemy: darker than its own tile, one bright eye", ASH)
    note(pips[0], (42, 660), "guard pips on the player - no health bar", CHALK, "l")
    caption(d, W, H, "the grid is rotated 20 degrees; no glyph, label or meter ever rotates with it")
    im.save(path)


# ------------------------------------------------------ 05 input timeline ----
def fig_timeline(path):
    W, H = 1200, 720
    im, d = canvas(W, H)
    head(d, W, "14.5  One burst, drawn",
         "the escalation window is not lag, it is a beat: you watch the intent climb, and you stop climbing by stopping")

    def row(y, bursts, axis_x, scale, span, label, col, readout, commits):
        d.line([(axis_x, y), (axis_x + span * scale, y)], fill=EDGE, width=1)
        for ms in range(0, span + 1, 100):
            x = axis_x + ms * scale
            d.line([(x, y - 4), (x, y + 4)], fill=EDGE, width=1)
            if ms % 200 == 0:
                txt(d, (x, y + 10), "%d" % ms, 11, mix(ASH, INK, 0.35), "mm")
        txt(d, (axis_x + span * scale + 14, y - 5), "ms", 11, ASH)
        txt(d, (40, y - 8), label, 14, CHALK, "lt", True)

        for ms, lab in ((260, "COMMIT_WINDOW"), (700, "SLOW_GAP")):
            x = axis_x + ms * scale
            for yy in range(int(y) - 46, int(y) + 46, 9):
                d.line([(x, yy), (x, yy + 5)], fill=mix(EDGE, INK, 0.1), width=1)
            txt(d, (x, y - 58), lab, 11, mix(ASH, INK, 0.15), "mb")

        allp = [t for b in bursts for t in b]
        for i, t in enumerate(allp):
            x = axis_x + t * scale
            d.line([(x, y - 32), (x, y + 6)], fill=CHALK, width=3)
            if i:
                prev = allp[i - 1]
                txt(d, (axis_x + (t + prev) / 2.0 * scale, y - 32), "%d ms" % (t - prev), 12, col, "mb")
        for b in bursts:
            last = axis_x + b[-1] * scale
            d.rectangle([last, y - 3, last + 260 * scale, y + 3], fill=mix(INK, col, 0.25))
            txt(d, (last + 130 * scale, y + 34), "commit window", 11, col, "mm")
        txt(d, (axis_x, y + 58), readout, 12, col)

        iy = y + 108
        for bi, b in enumerate(bursts):
            ix = axis_x + b[0] * scale + 20
            for k in range(1, len(b) + 1):
                shape = VERBS[min(k, 5)][2]
                glyph(d, shape, ix, iy, 13, col=col if k == len(b) else mix(EDGE, col, 0.4))
                txt(d, (ix, iy + 30), VERBS[min(k, 5)][0], 11,
                    mix(ASH, col, 0.5) if k == len(b) else mix(ASH, INK, 0.3), "mm")
                ix += 120
            d.line([(ix + 8, iy), (ix + 42, iy)], fill=col, width=2)
            d.polygon([(ix + 54, iy), (ix + 42, iy - 6), (ix + 42, iy + 6)], fill=col)
            verb = next(v for v in VERBS if v[0] == commits[bi])
            glyph(d, verb[2], ix + 112, iy, 17, col=col, fill=mix(INK, col, 0.35))
            txt(d, (ix + 112, iy + 34), "COMMIT: " + commits[bi], 13, col, "mm", True)

    row(210, [[0, 210, 430]], 230, 0.7, 700, "3 taps, 210 ms apart", EMBER,
        "median gap 210 ms -> FRANTIC tier: +30% damage, +1 Aggro, no Guard", ["LUNGE"])
    row(490, [[0], [900]], 230, 0.5, 1200, "2 taps, 900 ms apart", ASH,
        "gap over SLOW_GAP: not one burst of two, it is two bursts of one", ["STEP", "STEP"])
    caption(d, W, H,
            "worst case input-to-effect is HOLD_START + COMMIT_WINDOW ~ 500 ms - which is why the world waits (DESIGN.md section 3)")
    im.save(path)


# ------------------------------------------------------ 06 verb motifs -----
# The audio design (DESIGN.md 15.2, 15.3) drawn with the same primitives as the
# glyphs: an envelope is a shape, a grain is a tick, a tier is a filter.
MOTIFS = [
    ("BRACE", "ring", [(0, 150, 0.40, 20)], "0 grains: one low swell", "thud + cloth"),
    ("STEP", "dot", [(0, 90, 1.00, 5)], "1 grain per tile crossed", "cloth"),
    ("STRIKE", "lens", [(0, 45, 1.00, 0), (60, 60, 0.80, 0)], "2 grains: click, then contact", "click"),
    ("LUNGE", "ngon3", [(0, 45, 1.00, 0), (120, 110, 0.70, 5)], "2 grains: click, then scuff", "click + cloth"),
    ("GUARD", "ngon4", [(0, 620, 0.90, 2)], "1 grain, long metal tail", "bell"),
    ("SPRINT", "ngon5", [(0, 90, 0.90, 5), (210, 90, 0.90, 5), (430, 90, 0.90, 5)],
     "3 grains, spaced at YOUR gaps", "cloth x3"),
]


def env(d, x0, y, grains, scale, col, h=44):
    """a grain = attack ramp + decay to the baseline; a motif = its grains."""
    for (t, dur, amp, atk) in grains:
        xa = x0 + t * scale
        xb = xa + max(atk, 1) * scale
        xc = x0 + (t + dur) * scale
        pts = [(xa, y), (xb, y - h * amp), (xc, y)]
        d.polygon(pts, fill=mix(INK, col, 0.28))
        d.line(pts, fill=col, width=2)
        d.line([(xa, y - h - 8), (xa, y + 4)], fill=col, width=2)


def axis(d, x0, y, scale, span):
    d.line([(x0, y), (x0 + span * scale, y)], fill=EDGE, width=1)
    for ms in range(0, span + 1, 100):
        x = x0 + ms * scale
        d.line([(x, y - 3), (x, y + 3)], fill=EDGE, width=1)
        if ms % 200 == 0:
            txt(d, (x, y + 9), "%d" % ms, 11, mix(ASH, INK, 0.35), "mm")
    txt(d, (x0 + span * scale + 12, y - 4), "ms", 11, ASH)


def fig_motifs(path):
    W, H = 1200, 940
    im, d = canvas(W, H)
    head(d, W, "15.3  Verb motifs, drawn",
         "family and envelope carry the verb; pitch and filter carry the tier - a Strike must still be a Strike at any tier")

    AX, SCALE, SPAN = 250, 0.60, 700
    y = 168
    for name, shape, grains, note, family in MOTIFS:
        txt(d, (40, y - 9), name, 14, CHALK, "lt", True)
        txt(d, (40, y + 10), family, 11, mix(ASH, INK, 0.25))
        glyph(d, shape, 186, y - 8, 13, col=LANTERN)
        axis(d, AX, y, SCALE, SPAN)
        env(d, AX, y, grains, SCALE, LANTERN)
        txt(d, (AX + SPAN * SCALE + 40, y - 8), note, 12, mix(ASH, LANTERN, 0.45))
        txt(d, (AX + SPAN * SCALE + 40, y + 10),
            "%d grain%s" % (len(grains), "" if len(grains) == 1 else "s"), 11, mix(ASH, INK, 0.3))
        y += 92

    d.line([(40, y - 26), (W - 40, y - 26)], fill=EDGE, width=1)
    txt(d, (40, y - 16), "the same STRIKE, three tiers", 14, CHALK, "lt", True)
    txt(d, (40, y + 4), "same source, same envelope, same two grains - only the filter, the attack and the tail move", 11, ASH)
    ty = y + 130
    tiers = [("CAREFUL", "low-passed, softened attack, no tail, -6 dB", ASH,
              [(0, 40, 0.62, 9)]),
             ("NORMAL", "as printed", LANTERN,
              [(0, 45, 1.00, 0), (60, 60, 0.80, 0)]),
             ("FRANTIC", "harder attack, longer tail, +2 semitones, +3 dB", EMBER,
              [(0, 30, 1.00, 0), (55, 150, 0.95, 0)])]
    for i, (lab, note, col, grains) in enumerate(tiers):
        cx = 90 + i * 375
        glyph(d, "lens", cx - 44, ty - 40, 11, col=col)
        txt(d, (cx - 30, ty - 48), lab, 13, col, "lt", True)
        axis(d, cx, ty, 0.24, 700)
        env(d, cx, ty, grains, 0.24, col, h=30)
        txt(d, (cx, ty + 30), note, 11, mix(ASH, col, 0.4))

    caption(d, W, H,
            "grain count = the number of things the verb does; grains under 80 ms apart merge into one (the streaming limit, not a style choice) - DESIGN.md 15.3")
    im.save(path)


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "figures"
    for name, fn in [("01_shape_law_and_palette.png", fig_shapes),
                     ("02_cadence_meter.png", fig_meter),
                     ("03_ladder_poster.png", fig_poster),
                     ("04_screen_composition.png", fig_screen),
                     ("05_burst_timeline.png", fig_timeline),
                     ("06_verb_motifs.png", fig_motifs)]:
        fn("%s/%s" % (out, name))
        print("wrote %s/%s" % (out, name))
