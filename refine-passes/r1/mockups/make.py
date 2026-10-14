"""CADENCE reference figures for DESIGN.md section 15 (Visual design).

Renders:
  mockups/screen.png       the play screen at the reference surface (960x600, TILE 30)
  mockups/screen_small.png the same screen at the TILE-20 fallback (640x400) - this is
                           what 15.2's small-surface rule actually looks like
  mockups/shapes.png       verb/entity shape language, tier badges (incl. the no-data
                           state), the ghost-over-an-occupant rule, palette + contrast

Reference figures, not game assets. It also prints every number section 15 quotes,
including the measurements behind the 15.11 decisions. PIL only, no network, no fonts.
Run:  python3 mockups/make.py
"""
import io, math, re
from PIL import Image, ImageDraw, ImageFont

PAL = {
    "ink0":    "#0b0d10",   # field, void, unlit floor, HUD text plates (15.11-v7)
    "ink1":    "#14171c",   # pause / end-screen scrim (15.11-v10)
    "wall":    "#1e232b",   # unlit wall face, hairlines, frame, door slab
    "dust":    "#7d838c",   # all secondary text, entities, doors, no-data badge
    "chalk":   "#e6e4df",   # primary text, the player, HP pips, active-rung outline
    "careful": "#6f7883",   # tier: Careful (shapes only, never text)
    "normal":  "#d8a53f",   # tier: Normal (shapes only, never text)
    "frantic": "#e0553f",   # tier: Frantic (shapes only, never text)
    "guard":   "#5fa8c7",   # guard pips, Brace corners, Guard glyph - never on the meter
    "ghost":   "#b9c2cb",   # intent ghost, lit wall lips
}
# derived ceilings: formulas, not tokens (15.3) - the palette stays at ten
# lit_edge 0.70 is the weakest mix that clears 3:1 against lit_wall (0.55 measured 2.15:1)
DERIVED = {"lit_floor": ("dust", 0.27), "lit_wall": ("dust", 0.42), "lit_edge": ("ghost", 0.70)}
PLATE = 0.72          # glyph / telegraph plate strength (15.7)
LIGHT_GAMMA = 1.25    # 15.11-v3: the exponent the 15.3 formula omitted
def C(name):
    h = PAL[name] if name in PAL else name
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def ceil_(name):
    tok, t = DERIVED[name]
    return mix(C("ink0"), C(tok), t)
def plate(surface, t=PLATE):
    return mix(surface, C("ink0"), t)

def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _lumv(v):
    r, g, b = (v[i] / 255 for i in range(3))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
def lum(name):
    return _lumv(C(name))
def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
def crgb(a, b):
    la, lb = _lumv(a), _lumv(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def F(size):
    assert size >= 11, "15.11-v6: nothing in this game is drawn below 11 px"
    return ImageFont.load_default(size=size)

# Vienot 1999 colour-vision-deficiency matrices, applied in linear RGB
P = [[0.152286, 1.052521, -0.204808], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048428, 1.052310]]
D = [[0.367322, 0.860381, -0.227703], [0.280085, 0.672566, 0.047349], [-0.011820, 0.042940, 0.968881]]
def rgb(name):
    return list(C(name)) if not isinstance(name, tuple) else list(name)
def lin3(name):
    r, g, b = rgb(name)
    return [_lin(r / 255), _lin(g / 255), _lin(b / 255)]
def cvd(name, m):
    v = lin3(name)
    out = [max(0.0, min(1.0, sum(m[i][j] * v[j] for j in range(3)))) for i in range(3)]
    inv = lambda c: 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return "#%02x%02x%02x" % tuple(round(inv(c) * 255) for c in out)
def sep(a, b, m=None):
    u = lin3(a); v = lin3(b)
    if m:
        u = [sum(m[i][j] * u[j] for j in range(3)) for i in range(3)]
        v = [sum(m[i][j] * v[j] for j in range(3)) for i in range(3)]
    return sum((x - y) ** 2 for x, y in zip(u, v)) ** 0.5

# ---------------------------------------------------------------- shape language
def brace(d, cx, cy, s, col):
    a, b = s * 0.16, s * 0.42
    w = max(1, round(s / 15))
    for sx in (-1, 1):
        for sy in (-1, 1):
            d.line([(cx + sx * b, cy + sy * a), (cx + sx * b, cy + sy * b),
                    (cx + sx * a, cy + sy * b)], fill=col, width=w)

def chevron(d, cx, cy, s, col):
    w, t = max(1, round(s / 12)), 0.55
    d.line([(cx - t * s * 0.4, cy - t * s * 0.5), (cx + t * s * 0.4, cy),
            (cx - t * s * 0.4, cy + t * s * 0.5)], fill=col, width=w)

def wedge(d, cx, cy, s, col):
    t = 0.5
    d.polygon([(cx - t * s * 0.42, cy - t * s * 0.62), (cx + t * s * 0.5, cy),
               (cx - t * s * 0.42, cy + t * s * 0.62)], fill=col)
    d.line([(cx - t * s * 0.62, cy - t * s * 0.62), (cx - t * s * 0.62, cy + t * s * 0.62)],
           fill=col, width=max(1, round(s / 15)))

def wedge_out(d, cx, cy, s, col):
    """15.11-v2: over an occupied tile the ghost is stroked, never filled, so the
    occupant stays readable underneath it."""
    t = 0.5
    pts = [(cx - t * s * 0.42, cy - t * s * 0.62), (cx + t * s * 0.5, cy),
           (cx - t * s * 0.42, cy + t * s * 0.62), (cx - t * s * 0.42, cy - t * s * 0.62)]
    d.line(pts, fill=col, width=2, joint="curve")
    d.line([(cx - t * s * 0.62, cy - t * s * 0.62), (cx - t * s * 0.62, cy + t * s * 0.62)],
           fill=col, width=2)

def ring(d, cx, cy, s, col):
    d.rectangle([cx - s * 0.42, cy - s * 0.42, cx + s * 0.42, cy + s * 0.42], outline=col, width=1)
    d.rectangle([cx - s * 0.28, cy - s * 0.28, cx + s * 0.28, cy + s * 0.28], outline=col, width=1)

def triple(d, cx, cy, s, col):
    for i, k in enumerate((0.34, 0.66, 1.0)):
        chevron(d, cx + (i - 1) * s * 0.3, cy, s, mix(C("ink0"), col, k))

def arcarrow(d, cx, cy, s, col):
    r = s * 0.4
    d.arc([cx - r, cy - r, cx + r, cy + r], 210, 330, fill=col, width=max(1, round(s / 14)))
    ax = cx + r * math.cos(math.radians(330)); ay = cy + r * math.sin(math.radians(330))
    d.polygon([(ax - s * 0.16, ay - s * 0.05), (ax + s * 0.1, ay - s * 0.16),
               (ax + s * 0.06, ay + s * 0.12)], fill=col)

def bump(d, cx, cy, s, col):
    chevron(d, cx, cy, s, col)
    d.line([(cx - s * 0.4, cy - s * 0.4), (cx + s * 0.4, cy + s * 0.4)],
           fill=col, width=max(1, round(s / 10)))

def telegraph(d, cx, cy, s, col, verb=None):
    """15.11-v9: the box says a thing acted; the shape inside says what it did."""
    d.rectangle([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4], outline=col, width=2)
    if verb is not None:
        verb(d, cx, cy, s * 0.5, mix(C("ink0"), col, 0.75))

def lunge(d, cx, cy, s, col):
    wedge(d, cx - s * 0.16, cy, s * 0.8, col)
    chevron(d, cx + s * 0.34, cy, s * 0.8, mix(C("ink0"), col, 0.6))

def facemark(d, x, y, face, TILE, col):
    """15.11-v5: facing is a 6 px outward chevron inside the facing edge of your own
    tile - not a filled triangle, which means exit and Frantic, and not a mark that
    sits on top of the player glyph (the player glyph is offset away from that edge)."""
    cx, cy = x * TILE + TILE // 2, y * TILE + TILE // 2
    fx, fy = face
    e = TILE // 2 - 2                      # apex, just inside the tile edge
    w = max(2, TILE // 12)
    k = max(4, int(TILE * 0.20))           # wing length
    if fx:
        ax = cx + fx * e
        d.line([(ax - fx * k, cy - k), (ax, cy), (ax - fx * k, cy + k)], fill=col, width=w)
    else:
        ay = cy + fy * e
        d.line([(cx - k, ay - fy * k), (cx, ay), (cx + k, ay - fy * k)], fill=col, width=w)

def glyph_offset(face, TILE):
    fx, fy = face
    k = int(TILE * 0.12)
    return -fx * k, -fy * k

BREAKS = {"LUNGE", "PIVOT"}
VERBS = [
    ("BRACE",  brace,      "no input: corners on your own tile; stays until you move"),
    ("STEP",   chevron,    "1 tap: hollow chevron on the tile you would occupy"),
    ("STRIKE", wedge,      "2 taps: filled wedge on empty ground, stroked on an occupant"),
    ("LUNGE",  lunge,      "3 taps: wedge on the occupant + chevron one tile beyond"),
    ("GUARD",  ring,       "4 taps: double ring on yourself - the only double square"),
    ("SPRINT", triple,     "5 taps: three fading chevrons along the line"),
    ("PIVOT",  arcarrow,   "hold: arc around yourself, snapping in 90-degree steps"),
    ("BUMP",   bump,       "step into an occupant: barred chevron, you stay put"),
]

# ---------------------------------------------------------------- room fixture
def build_room():
    g = [["."] * 32 for _ in range(20)]
    for x in range(32):
        g[0][x] = g[19][x] = "#"
    for y in range(20):
        g[y][0] = g[y][31] = "#"
    for x in range(4, 28):
        if x not in (16, 17):
            g[9][x] = "#"
    g[9][26] = "+"
    for x in range(8, 13):
        g[4][x] = "#"
    for y in range(2, 5):
        g[y][22] = "#"
    for x in range(20, 25):
        g[14][x] = "#"
    player = (10, 5, 1, 0)
    # r2 is outside the light radius *and* not in the known set, so 15.11-v1 draws nothing
    ENT = {"r": (11, 5), "s": (13, 4), "m": (12, 7), "r2": (24, 16)}
    FIX = {"*": (18, 2), "<": (29, 12)}
    for k, (x, y) in list(ENT.items()) + list(FIX.items()):
        g[y][x] = k[0]
    return g, player, ENT, FIX

def light_fn(player, HALF=34, R=6.5, RC=10.0):
    px, py, fx, fy = player
    def raw(x, y):
        dx, dy = x - px, y - py
        dd = math.hypot(dx, dy)
        base = max(0.0, 1.0 - dd / R)
        if dd > 0.001:
            da = abs((math.degrees(math.atan2(dy, dx)) - math.degrees(math.atan2(fy, fx)) + 180) % 360 - 180)
            if da <= HALF:
                base = max(base, min(1.0, (1.0 - dd / RC) * (1.0 + (HALF - da) / HALF * 0.6)))
        return min(1.0, base) ** LIGHT_GAMMA
    return raw

# ---------------------------------------------------------------- the meter
def meter_geom(SW):
    """15.11-v4: the meter width is DERIVED from its rungs, and the rate band is
    exactly as wide as the rungs, so the two axes are one aligned object."""
    RW, GAP = (76, 8) if SW >= 652 else (60, 6)
    MW = 5 * RW + 4 * GAP
    return RW, GAP, MW, (SW - MW) // 2

def draw_meter(d, W, H, tier, med, taps):
    RW, GAP, MW, mx = meter_geom(W)
    MH = 26
    my = H - 58
    by = my - 14
    names = ["STEP", "STRIKE", "LUNGE", "GUARD", "SPRINT"]
    hud_plate(d, mx, my - 30, mx + MW, my + MH + 15)
    d.text((mx, my - 30), "CADENCE", font=F(11), fill=C("dust"))

    def gx(ms):
        return round(mx + MW * ms / 1200.0)
    d.rectangle([mx, by, mx + MW, by + 6], outline=mix(C("ink0"), C("dust"), 0.5))
    d.rectangle([mx, by, gx(med), by + 6], fill=C(tier))
    for ms in (260, 700):
        d.line([(gx(ms), by - 3), (gx(ms), by + 9)], fill=C("dust"), width=2)
        if RW >= 76:
            d.text((gx(ms) + 3, by - 14), str(ms), font=F(11), fill=C("dust"))
    for i in range(5):
        x0 = mx + i * (RW + GAP)
        if i == 0:
            d.rectangle([x0, my, x0 + RW, my + MH], fill=mix(C("ink0"), C(tier), 0.45))
        elif i == 1:
            d.rectangle([x0, my, x0 + RW, my + MH], fill=C(tier))
            d.rectangle([x0 - 2, my - 2, x0 + RW + 2, my + MH + 2], outline=C("chalk"), width=2)
        else:
            d.rectangle([x0, my, x0 + RW, my + MH], outline=mix(C("ink0"), C("dust"), 0.55))
        d.text((x0 + 1, my + MH + 5), names[i], font=F(11), fill=C("dust"))
    bx = mx - 112
    badge(d, bx, my, tier)
    rx = mx + MW + 16
    d.text((rx, my), "MED %d ms" % med, font=F(11), fill=C("dust"))
    d.text((rx, my + 15), "%d TAPS" % taps, font=F(11), fill=C("chalk"))
    return dict(RW=RW, GAP=GAP, MW=MW, mx=mx, rung_right=mx + MW, badge_x=bx,
                right_x=rx, right_right=rx + 10 * 7, t260=mx + round(MW * 260 / 1200),
                t700=mx + round(MW * 700 / 1200))

def badge(d, bx, my, tier):
    """15.11-v11: below CADENCE_N samples there is no tier, so the shape slot is
    left empty and only the word is drawn. A shape there would be a claim."""
    if tier == "careful":
        d.ellipse([bx, my, bx + 20, my + 20], outline=C("careful"), width=2)
    elif tier == "normal":
        d.rectangle([bx, my, bx + 20, my + 20], outline=C("normal"), width=2)
    elif tier == "frantic":
        d.polygon([(bx, my + 20), (bx + 20, my + 20), (bx + 10, my)], fill=C("frantic"))
    d.text((bx + 30, my + 3), ("READING" if tier == "nodata" else tier.upper()),
           font=F(13), fill=C("chalk"))

def dashed(d, box, col):
    x0, y0, x1, y1 = box
    for x in range(int(x0), int(x1), 6):
        d.line([(x, y0), (min(x + 3, x1), y0)], fill=col)
        d.line([(x, y1), (min(x + 3, x1), y1)], fill=col)
    for y in range(int(y0), int(y1), 6):
        d.line([(x0, y), (x0, min(y + 3, y1))], fill=col)
        d.line([(x1, y), (x1, min(y + 3, y1))], fill=col)

def hud_plate(d, x0, y0, x1, y1, pad=3):
    """15.11-v7: HUD text sits on an opaque ink0 rectangle. Constant contrast, and
    the only panel in the game."""
    d.rectangle([x0 - pad, y0 - pad, x1 + pad, y1 + pad], fill=C("ink0"))

# ---------------------------------------------------------------- figure 1/1b: play screen
def screen(W=960, H=600, TILE=30):
    g, player, ENT, FIX = build_room()
    px, py, fx, fy = player
    light = light_fn(player)
    CW, CH = len(g[0]), len(g)
    img = Image.new("RGB", (W, H), C("ink0"))
    d = ImageDraw.Draw(img)
    floor_lit, wall_lit, edge_lit = ceil_("lit_floor"), ceil_("lit_wall"), ceil_("lit_edge")
    for y in range(CH):
        for x in range(CW):
            ch = g[y][x]
            b = light(x, y)
            x0, y0 = x * TILE, y * TILE
            # 15.11-v8: the grid is geometry, not a colour - every tile is drawn 1 px
            # short and the gap is whatever is under it (ink0). No off-palette seam.
            r = [x0, y0, x0 + TILE - 2, y0 + TILE - 2]
            if ch == "#":
                d.rectangle(r, fill=mix(C("ink0"), wall_lit, b))
                if y + 1 < CH and g[y + 1][x] != "#":
                    d.line([x0, y0 + TILE - 1, x0 + TILE - 1, y0 + TILE - 1],
                           fill=mix(C("ink0"), edge_lit, b), width=2)
            else:
                d.rectangle(r, fill=mix(C("ink0"), floor_lit, b))

    def tcx(x): return x * TILE + TILE // 2
    def tcy(y): return y * TILE + TILE // 2
    def surf(x, y):
        return wall_lit if g[y][x] == "#" else floor_lit
    GF = max(13, round(TILE * 0.66))

    # draw order per 15.9: terrain -> plates -> entities -> ghost mark -> telegraph
    tx, ty = px + fx, py + fy
    occupied = g[ty][tx] in ("r", "s", "m")
    sx, sy = ENT["s"]
    d.rectangle([tx * TILE, ty * TILE, tx * TILE + TILE - 1, ty * TILE + TILE - 1],
                fill=plate(surf(tx, ty)))
    d.rectangle([sx * TILE, sy * TILE, sx * TILE + TILE - 1, sy * TILE + TILE - 1],
                fill=plate(surf(sx, sy)))

    brace(d, tcx(px), tcy(py), TILE, C("guard"))
    facemark(d, px, py, (fx, fy), TILE, C("chalk"))
    ox, oy = glyph_offset((fx, fy), TILE)
    d.text((tcx(px) - GF // 2 + ox, tcy(py) - int(GF * 0.7) + oy), "@", font=F(GF),
           fill=C("chalk"))

    # entities: drawn at full value if lit now or known; otherwise not drawn (15.11-v1)
    invisible = []
    for k, (x, y) in ENT.items():
        if light(x, y) <= 0.0:
            invisible.append((k, x, y)); continue
        col = C("chalk") if (k == "r" or (x, y) == (tx, ty)) else C("dust")
        d.text((tcx(x) - GF // 2, tcy(y) - int(GF * 0.7)), (k if k == "r" else k[0].upper()),
               font=F(GF), fill=col)

    # the intent ghost: the mark goes on top of the plate and on top of the occupant,
    # stroked when occupied so the thing stays readable (15.7, 15.11-v2)
    if occupied:
        wedge_out(d, tcx(tx), tcy(ty), TILE, C("ghost"))
    else:
        wedge(d, tcx(tx), tcy(ty), TILE, C("ghost"))
    # telegraph on the acting tile: box + the verb that is coming, in the tier hue
    # captured when it was set (15.11-v9)
    telegraph(d, tcx(sx), tcy(sy), TILE, C("frantic"), chevron)
    for k, (x, y) in FIX.items():
        if k == "*":
            d.polygon([(tcx(x), y * TILE + 5), (tcx(x) + 8, tcy(y)), (tcx(x), y * TILE + TILE - 5),
                       (tcx(x) - 8, tcy(y))], outline=C("chalk"), width=2)
        else:
            d.polygon([(x * TILE + 8, y * TILE + 8), (x * TILE + TILE - 8, y * TILE + 8),
                       (tcx(x), y * TILE + TILE - 8)], fill=C("chalk"))
    # door: wall slab + dust seam and handle (15.11-v8). No off-palette brown, no tier hue.
    dx0, dy0 = 26 * TILE, 9 * TILE
    d.rectangle([dx0, dy0, dx0 + TILE - 2, dy0 + TILE - 2], fill=C("wall"), outline=C("dust"), width=2)
    d.line([(dx0 + TILE - 9, tcy(9)), (dx0 + TILE - 4, tcy(9))], fill=C("dust"), width=2)

    # HUD text blocks get opaque plates
    hud_plate(d, 12, 10, 190, 40)
    d.text((12, 10), "ROOM 4  BOTTLENECK", font=F(13), fill=C("dust"))
    d.text((12, 28), "TURN 27", font=F(11), fill=C("dust"))
    hud_plate(d, W - 176, 10, W - 40, 36)
    d.text((W - 176, 10), "HP", font=F(11), fill=C("dust"))
    for i in range(5):
        x0 = W - 112 + i * 14
        if i < 3:
            d.rectangle([x0, 10, x0 + 10, 19], fill=C("chalk"))
        else:
            d.rectangle([x0, 10, x0 + 10, 19], outline=C("dust"))
    d.text((W - 176, 26), "GUARD", font=F(11), fill=C("dust"))
    for i in range(3):
        x0 = W - 112 + i * 14
        if i < 2:
            d.rectangle([x0, 26, x0 + 10, 35], fill=C("guard"))
        else:
            d.rectangle([x0, 26, x0 + 10, 35], outline=C("dust"))
    # 15.11-v4: at the small geometry the bottom-left log is dropped - the strip is
    # full. The record still exists on the end screen and in Pause > Input.
    if W >= 652:
        hud_plate(d, 12, H - 48, 150, H - 21)
        for i, ln in enumerate(["23  BRACE   +1 guard", "25  STEP    ok", "26  BUMP    blocked"]):
            d.text((12, H - 48 + i * 14), ln, font=F(11), fill=C("dust"))
    m = draw_meter(d, W, H, "frantic", 120, 2)
    d.rectangle([0, 0, W - 1, H - 1], outline=C("wall"))
    return img, m, invisible

# ---------------------------------------------------------------- figure 2: shape sheet
def shapes():
    W, H = 980, 1010
    img = Image.new("RGB", (W, H), C("ink0"))
    d = ImageDraw.Draw(img)
    d.text((18, 14), "CADENCE - shape language", font=F(22), fill=C("chalk"))
    d.text((18, 48), "verb identity is shape and position; hue is only ever the tier scale", font=F(11), fill=C("dust"))
    y = 84
    d.text((18, y), "VERB GHOSTS   (30 / 20 / 14 px. The floor is 20 px; the 14 px column is drawn", font=F(13), fill=C("dust"))
    d.text((18, y + 18), "to show where the language breaks - crossed out is a shape that stops reading.", font=F(13), fill=C("dust"))
    y += 46
    for name, fn, note in VERBS:
        d.text((18, y + 8), name, font=F(13), fill=C("chalk"))
        col = C("guard") if name in ("BRACE", "GUARD") else C("ghost")
        for i, s in enumerate((30, 20, 14)):
            cx = 150 + i * 62
            d.rectangle([cx - s // 2, y + 22 - s // 2, cx + s // 2, y + 22 + s // 2], outline=C("wall"))
            fn(d, cx, y + 22, s, col)
            if s == 14 and name in BREAKS:
                q = s // 2 + 3
                d.line([(cx - q, y + 22 - q), (cx + q, y + 22 + q)], fill=C("frantic"), width=2)
                d.line([(cx - q, y + 22 + q), (cx + q, y + 22 - q)], fill=C("frantic"), width=2)
        d.text((356, y + 10), note, font=F(11), fill=C("dust"))
        y += 44
    y += 6
    d.text((18, y), "GHOST OVER AN OCCUPANT", font=F(13), fill=C("chalk"))
    d.text((18, y + 18), "filled on empty ground, stroked over a thing - the occupant stays readable", font=F(11), fill=C("dust"))
    y += 26
    for i, (nm, fn) in enumerate((("empty ground", wedge), ("an occupant is there", wedge_out))):
        cx = 500 + i * 240
        d.rectangle([cx - 22, y - 22, cx + 22, y + 22], fill=plate(C("ink0")), outline=C("wall"))
        fn(d, cx, y, 44, C("ghost"))
        d.text((cx - 8, y - 12), "r", font=F(22), fill=C("chalk"))
        d.text((cx - 40, y + 30), nm, font=F(11), fill=C("dust"))
    y += 60
    d.text((18, y), "TIER BADGES   (shape + word, always both; position is carried by the band)", font=F(13), fill=C("dust"))
    y += 28
    for i, (nm, col, kind) in enumerate((("CAREFUL", "careful", "circle"),
                                         ("NORMAL", "normal", "square"),
                                         ("FRANTIC", "frantic", "triangle"),
                                         ("no data", "dust", "none"))):
        cx = 110 + i * 210
        for j, s in enumerate((22, 16, 12)):
            bx = cx + j * 46
            if kind == "circle":
                d.ellipse([bx - s // 2, y - s // 2, bx + s // 2, y + s // 2], outline=C(col), width=2)
            elif kind == "square":
                d.rectangle([bx - s // 2, y - s // 2, bx + s // 2, y + s // 2], outline=C(col), width=2)
            elif kind == "triangle":
                d.polygon([(bx - s // 2, y + s // 2), (bx + s // 2, y + s // 2), (bx, y - s // 2)], fill=C(col))
            else:
                dashed(d, (bx - s // 2, y - s // 2, bx + s // 2, y + s // 2), C("wall"))
        d.text((cx - 6, y + 26), "READING" if nm == "no data" else nm, font=F(11), fill=C("chalk"))
        if nm == "no data":
            d.text((cx - 6, y + 42), "under CADENCE_N samples:", font=F(11), fill=C("dust"))
            d.text((cx - 6, y + 56), "no shape, no hue, no band fill", font=F(11), fill=C("dust"))
    y += 76
    d.text((18, y), "ENTITIES, FURNITURE, TELEGRAPH", font=F(13), fill=C("dust"))
    y += 28
    items = [("@", "player (chalk)"), ("r", "rat"), ("S", "sentinel"), ("M", "mirror"),
             ("*", "relic"), ("+", "door"), ("<", "exit"), ("[]", "telegraph")]
    for i, (glyph, note) in enumerate(items):
        cx = 66 + i * 112
        if glyph == "*":
            d.polygon([(cx, y), (cx + 9, y + 14), (cx, y + 28), (cx - 9, y + 14)], outline=C("chalk"), width=2)
        elif glyph == "+":
            d.rectangle([cx - 10, y, cx + 10, y + 28], fill=C("wall"), outline=C("dust"), width=2)
        elif glyph == "<":
            d.polygon([(cx - 9, y + 4), (cx + 9, y + 4), (cx, y + 26)], fill=C("chalk"))
        elif glyph == "[]":
            d.rectangle([cx - 14, y, cx + 14, y + 28], fill=plate(C("ink0")))
            telegraph(d, cx, y + 14, 28, C("frantic"), wedge)
        else:
            d.text((cx - 6, y), glyph, font=F(20), fill=C("chalk"))
        d.text((cx - 44, y + 34), note, font=F(11), fill=C("dust"))
        if glyph == "@":
            d.text((cx - 44, y + 48), "always chalk, never dimmed", font=F(11), fill=C("dust"))
    d.text((18, y + 62), "15.11-v1: an entity is drawn at full value if it is lit now or already known, and",
           font=F(11), fill=C("dust"))
    d.text((18, y + 76), "is not drawn at all otherwise. Nothing in this game is drawn at a dimmed value.",
           font=F(11), fill=C("dust"))
    y += 100
    d.text((18, y), "PALETTE   (10 tokens; contrast vs ink0 measured, WCAG relative luminance)", font=F(13), fill=C("dust"))
    y += 28
    for i, name in enumerate(PAL):
        cx = 18 + i * 96
        d.rectangle([cx, y, cx + 84, y + 26], fill=C(name), outline=C("wall"))
        d.text((cx, y + 32), name, font=F(11), fill=C("chalk"))
        d.text((cx, y + 46), PAL[name], font=F(11), fill=C("dust"))
        d.text((cx, y + 60), "%.2f:1" % contrast(name, "ink0"), font=F(11), fill=C("dust"))
    d.rectangle([0, 0, W - 1, H - 1], outline=C("wall"))
    return img

def png(img):
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()

# ---------------------------------------------------------------- self-measurement
def coverage(occupied_box):
    """v2: how much of the ghost mark actually survives on the tile it is drawn on."""
    import os
    from PIL import Image
    path = os.path.join(os.path.dirname(__file__), "screen.png")
    im = Image.open(path).convert("RGB")
    x0, y0, x1, y1 = occupied_box
    n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = im.getpixel((x, y))
            if all(abs(p[i] - C("ghost")[i]) <= 28 for i in range(3)):
                n += 1
    return n


def report(mbig, msmall, invisible):
    lit, wall = ceil_("lit_floor"), ceil_("lit_wall")
    print("light-model ceilings (derived, not tokens):")
    for nm in DERIVED:
        print("  %-10s %s" % (nm, "#%02x%02x%02x" % ceil_(nm)))
    print("contrast vs ink0:")
    for name in PAL:
        print("  %-8s %-8s %.2f" % (name, PAL[name], contrast(name, "ink0")))
    print("separation of the three tiers, linear-RGB distance (Vienot 1999 CVD matrices):")
    for a, b in (("careful", "normal"), ("normal", "frantic"), ("careful", "frantic")):
        print("  %-8s %-8s normal %.3f  protan %.3f  deutan %.3f" % (a, b, sep(a, b), sep(a, b, P), sep(a, b, D)))
    for name in ("careful", "normal", "frantic"):
        print("  %-8s simulates to %s under protanopia" % (name, cvd(name, P)))
    print("tier hues drawn on the brightest surfaces, vs the 3:1 floor for marks:")
    for name in ("careful", "normal", "frantic", "guard", "ghost"):
        print("  %-8s on lit_floor %.2f   on lit_wall %.2f" % (name, crgb(C(name), lit), crgb(C(name), wall)))
    print("ghost painted straight onto the brightest lit floor: %.2f:1  (fails 3:1)" % crgb(mix(lit, C("ghost"), 0.45), lit))
    print("ghost on a dark plate (the shipped rule):          %.2f:1" % crgb(C("ghost"), plate(lit)))
    print("lit_edge lip: vs lit_wall %.2f   vs lit_floor %.2f   (15.3's wall/floor separator)"
          % (crgb(ceil_("lit_edge"), wall), crgb(ceil_("lit_edge"), lit)))
    print("wall mass vs floor mass (why terrain needs the lip, not contrast): %.2f" % crgb(wall, lit))
    print("\n-- v1: the deleted entity 'dark' clamps, against the 3:1 floor --")
    for t in (0.32, 0.45, 0.60):
        v = crgb(mix(C("ink0"), C("dust"), t), C("ink0"))
        print("   dust @ %d%% over ink0 = %.2f:1  %s" % (t * 100, v, "FAILS" if v < 3 else "ok"))
    v69 = crgb(mix(C("ink0"), C("dust"), 0.69), C("ink0"))
    print("   a 3:1-compliant dark value (dust at 69 percent) measures %.2f against %.2f lit: a %.1fx"
          " signal, so a clamp that passes the floor is too weak to mean anything"
          % (v69, crgb(C("dust"), lit), crgb(C("dust"), lit) / v69))
    print("   entities outside the light radius are not drawn: %s"
          % ", ".join("%s at (%d,%d)" % k for k in invisible))
    print("\n-- v2: ghost coverage on the tile it targets (the rat tile, 30 x 29 px) --")
    print("   ghost pixels surviving on the occupied tile: %d of %d tile pixels"
          % (coverage((330, 150, 360, 179)), 30 * 29))
    print("\n-- v3: light gamma over the 32x20 fixture (what the exponent is worth) --")
    for gam in (1.0, LIGHT_GAMMA):
        raw = light_fn((10, 5, 1, 0))
        vals = []
        for y in range(20):
            for x in range(32):
                base = raw(x, y) ** (1.0 / LIGHT_GAMMA)
                vals.append(base ** gam)
        lt = [v for v in vals if v > 0]
        print("   gamma %.2f: %d lit tiles, mean L %.3f, share L>=0.5 %.1f%%"
              % (gam, len(lt), sum(lt) / len(lt), 100 * sum(1 for v in lt if v >= 0.5) / len(lt)))
    print("\n-- v7: HUD text. unpainted = what 15.2 used to allow, painted = the plate path --")
    surfaces = (("ink0", C("ink0")), ("wall", C("wall")), ("lit_floor", lit), ("lit_wall", wall))
    for tok in ("dust", "chalk"):
        print("   %s unpainted:" % tok,
              "  ".join("%s %.2f" % (nm, crgb(C(tok), s)) for nm, s in surfaces))
        print("      opaque ink0 plate %.2f   translucent 0.72 plate worst %.2f"
              % (crgb(C(tok), C("ink0")), min(crgb(C(tok), plate(s)) for _, s in surfaces)))
    print("   the text floor is 4.5:1, so any unpainted value below it is a failure")
    print("\n-- v4: meter geometry (derived from the rungs) --")
    for nm, m, SW in (("960x600", mbig, 960), ("640x400", msmall, 640)):
        print("   %-8s rung %3d gap %d -> axis %d px | band x %d..%d | ticks %d/%d at x %d/%d"
              " | badge x %d | right col ends %d | %s"
              % (nm, m["RW"], m["GAP"], m["MW"], m["mx"], m["rung_right"], 260, 700,
                 m["t260"], m["t700"], m["badge_x"], m["right_right"],
                 "fits" if (m["badge_x"] >= 16 and m["right_right"] <= SW - 16) else "OVERFLOWS"))
        assert m["badge_x"] >= 16 and m["right_right"] <= SW - 16
    print("   rungs and band span identical pixels: %d==%d and %d==%d"
          % (mbig["rung_right"] - mbig["mx"], mbig["MW"],
             msmall["rung_right"] - msmall["mx"], msmall["MW"]))

def lint():
    try:
        src = open(__file__, encoding="utf-8").read()
    except Exception:
        return
    body = src.split("def C(name):", 1)[1]
    bad = re.findall(r"#[0-9a-fA-F]{6}", body)
    # every colour argument must come from C(), mix() or plate()
    direct = [m for m in re.findall(r"(?:fill|outline)=([^,\)]+)", body)
              if not m.strip().startswith(("C(", "mix(", "plate(", "col", "C)", "C("))]
    bad += sorted(set(direct.strip() for direct in direct if direct.strip()))
    print("\n-- v8: colour literals / non-token colour arguments outside the palette block: %d --" % len(bad))
    for b in bad:
        print("   ", b)

if __name__ == "__main__":
    big, mbig, invis = screen(960, 600, 30)
    small, msmall, _ = screen(640, 400, 20)
    for p, im in (("mockups/screen.png", big), ("mockups/screen_small.png", small),
                  ("mockups/shapes.png", shapes())):
        with open(p, "wb") as fh:
            fh.write(png(im))
        print("wrote", p)
    report(mbig, msmall, invis)
    lint()
