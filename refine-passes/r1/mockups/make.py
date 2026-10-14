"""CADENCE reference figures for DESIGN.md section 15 (Visual design).

Renders mockups/screen.png (play-screen composition) and mockups/shapes.png
(verb/entity shape language, tier badges, palette with measured WCAG contrast).
They are reference figures, not game assets. PIL only, no network, no fonts.
Run:  python3 mockups/make.py
"""
import io, math
from PIL import Image, ImageDraw, ImageFont

PAL = {
    "ink0":    "#0b0d10",   # field
    "ink1":    "#14171c",   # lit floor
    "wall":    "#1e232b",   # lit wall face
    "dust":    "#7d838c",   # secondary text, unlit entities
    "chalk":   "#e6e4df",   # player, primary text
    "careful": "#6f7883",   # tier: Careful
    "normal":  "#d8a53f",   # tier: Normal
    "frantic": "#e0553f",   # tier: Frantic
    "guard":   "#5fa8c7",   # guard / brace only
    "ghost":   "#b9c2cb",   # intent ghost, drawn at ~45% over the field
}
def C(name):
    h = PAL[name] if name in PAL else name
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def lum(name):
    r, g, b = (C(name)[i] / 255 for i in range(3))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)
def contrast(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

def F(size):
    return ImageFont.load_default(size=size)

# Vienot 1999 colour-vision-deficiency matrices, applied in linear RGB
P = [[0.152286, 1.052521, -0.204808], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048428, 1.052310]]
D = [[0.367322, 0.860381, -0.227703], [0.280085, 0.672566, 0.047349], [-0.011820, 0.042940, 0.968881]]
def rgb(name):
    return list(C(name)) if not isinstance(name, tuple) else list(name)
def lin3(name):
    r, g, b = rgb(name)
    return [_lin(r / 255), _lin(g / 255), _lin(b / 255)]
def crgb(a, b):
    def L(v):
        return 0.2126 * _lin(v[0] / 255) + 0.7152 * _lin(v[1] / 255) + 0.0722 * _lin(v[2] / 255)
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)
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

def telegraph(d, cx, cy, s, col):
    d.rectangle([cx - s * 0.4, cy - s * 0.4, cx + s * 0.4, cy + s * 0.4], outline=col, width=2)

def lunge(d, cx, cy, s, col):
    wedge(d, cx - s * 0.16, cy, s * 0.8, col)
    chevron(d, cx + s * 0.34, cy, s * 0.8, mix(C("ink0"), col, 0.6))

BREAKS = {"LUNGE", "PIVOT"}
VERBS = [
    ("BRACE",  brace,    "no input: corners on your own tile; stays until you move"),
    ("STEP",   chevron,  "1 tap: hollow chevron on the tile you would occupy"),
    ("STRIKE", wedge,    "2 taps: filled wedge, on the occupant or the wall"),
    ("LUNGE",  lunge,    "3 taps: wedge on the occupant + chevron one tile beyond"),
    ("GUARD",  ring,     "4 taps: double ring on yourself"),
    ("SPRINT", triple,   "5 taps: three fading chevrons along the line"),
    ("PIVOT",  arcarrow, "hold: arc around yourself, snapping in 90-degree steps"),
    ("BUMP",   bump,     "step into an occupant: barred chevron, you stay put"),
]

# ---------------------------------------------------------------- figure 1: play screen
def screen():
    W, H, TILE = 960, 600, 30
    CW, CH = W // TILE, H // TILE
    g = [["."] * CW for _ in range(CH)]
    for x in range(CW):
        g[0][x] = g[CH - 1][x] = "#"
    for y in range(CH):
        g[y][0] = g[y][CW - 1] = "#"
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
    px, py, fx, fy = 10, 5, 1, 0
    g[py][px] = "@"
    ENT = {"r": (11, 5), "s": (20, 13), "m": (24, 16)}
    FIX = {"*": (18, 2), "<": (29, 12)}
    for k, (x, y) in list(ENT.items()) + list(FIX.items()):
        g[y][x] = k

    img = Image.new("RGB", (W, H), C("ink0"))
    d = ImageDraw.Draw(img)
    R, RC = 6.5, 10.0

    def light(x, y):
        dx, dy = x - px, y - py
        dd = math.hypot(dx, dx) * 0 + math.hypot(dx, dy)
        base = max(0.0, 1.0 - dd / R)
        if dd > 0.001:
            da = abs((math.degrees(math.atan2(dy, dx)) - math.degrees(math.atan2(fy, fx)) + 180) % 360 - 180)
            if da <= 34:
                base = max(base, min(1.0, (1.0 - dd / RC) * (1.0 + (34 - da) / 34 * 0.6)))
        return min(1.0, base) ** 1.25

    # lit ceilings, derived from tokens (15.3) - not palette tokens themselves
    floor_lit = mix(C("ink0"), C("dust"), 0.27)
    wall_lit = mix(C("ink0"), C("dust"), 0.42)
    edge_lit = mix(C("ink0"), C("ghost"), 0.55)
    for y in range(CH):
        for x in range(CW):
            ch = g[y][x]
            b = light(x, y)
            x0, y0 = x * TILE, y * TILE
            if ch == "#":
                d.rectangle([x0, y0, x0 + TILE - 1, y0 + TILE - 1], fill=mix(C("ink0"), wall_lit, b))
                if y + 1 < CH and g[y + 1][x] != "#":
                    d.line([x0, y0 + TILE - 1, x0 + TILE - 1, y0 + TILE - 1],
                           fill=mix(C("ink0"), edge_lit, b), width=2)
            else:
                d.rectangle([x0, y0, x0 + TILE - 1, y0 + TILE - 1], fill=mix(C("ink0"), floor_lit, b))
                if b > 0.08:
                    d.rectangle([x0, y0, x0 + TILE - 1, y0 + TILE - 1],
                                outline=mix(C("ink0"), (58, 66, 78), b * 0.8))

    def tcx(x): return x * TILE + TILE // 2
    def tcy(y): return y * TILE + TILE // 2

    # A ghost tile is re-rendered as a dark plate first, then the shape at full
    # token colour. Ghost contrast is therefore a constant and does not depend
    # on where the light model happens to be.
    tx, ty = px + fx, py + fy
    plate = mix(mix(C("ink0"), floor_lit, light(tx, ty)), C("ink0"), 0.72)
    d.rectangle([tx * TILE, ty * TILE, tx * TILE + TILE - 1, ty * TILE + TILE - 1], fill=plate)
    gc = C("ghost")
    d.polygon([(tx * TILE + 10, ty * TILE + 6), (tx * TILE + TILE - 5, tcy(ty)),
               (tx * TILE + 10, ty * TILE + TILE - 6)], fill=gc)
    d.line([(tx * TILE + 7, ty * TILE + 6), (tx * TILE + 7, ty * TILE + TILE - 6)], fill=gc, width=2)
    GHOST_PLATE = plate

    brace(d, tcx(px), tcy(py), TILE, mix(C("ink0"), C("guard"), 0.9))
    d.text((tcx(px) - 6, tcy(py) - 10), "@", font=F(20), fill=C("chalk"))
    d.polygon([(px * TILE + TILE - 7, tcy(py) - 4), (px * TILE + TILE - 1, tcy(py)),
               (px * TILE + TILE - 7, tcy(py) + 4)], fill=C("chalk"))
    for k, (x, y) in ENT.items():
        # an entity under the ghost is drawn in full chalk: the ghost never
        # obscures the thing it targets.
        if (x, y) == (px + fx, py + fy):
            col = C("chalk")
        else:
            col = mix(C("ink0"), C("dust"), max(0.32, light(x, y)))
        d.text((tcx(x) - 5, tcy(y) - 8), ("r" if k == "r" else k.upper()), font=F(18), fill=col)
    telegraph(d, tcx(19), tcy(13), TILE, C("frantic"))
    for k, (x, y) in FIX.items():
        col = mix(C("ink0"), C("chalk"), max(0.45, light(x, y)))
        if k == "*":
            d.polygon([(tcx(x), y * TILE + 5), (tcx(x) + 8, tcy(y)), (tcx(x), y * TILE + TILE - 5),
                       (tcx(x) - 8, tcy(y))], outline=col, width=2)
        else:
            d.polygon([(x * TILE + 8, y * TILE + 8), (x * TILE + TILE - 8, y * TILE + 8),
                       (tcx(x), y * TILE + TILE - 8)], fill=col)
    dx0, dy0 = 26 * TILE, 9 * TILE
    db = max(0.6, light(26, 9))
    d.rectangle([dx0 + 3, dy0 + 3, dx0 + TILE - 4, dy0 + TILE - 4], fill=mix(C("ink0"), (86, 74, 48), db))
    d.line([(dx0 + TILE // 2 - 4, tcy(9)), (dx0 + TILE // 2 + 4, tcy(9))],
           fill=mix(C("ink0"), C("normal"), db), width=2)

    d.text((12, 10), "ROOM 4  BOTTLENECK", font=F(13), fill=C("dust"))
    d.text((12, 28), "TURN 27", font=F(11), fill=C("dust"))
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
    for i, ln in enumerate(["23  BRACE   +1 guard", "25  STEP    ok", "26  BUMP    blocked"]):
        d.text((12, H - 48 + i * 14), ln, font=F(11), fill=C("dust"))

    mw, mh = 420, 26
    mx, my = (W - mw) // 2, H - 58
    names = ["STEP", "STRIKE", "LUNGE", "GUARD", "SPRINT"]
    rw, gap = 76, 8
    d.text((mx, my - 30), "CADENCE", font=F(11), fill=C("dust"))
    # tier band: the gap axis, 0..1200 ms, with the two threshold ticks. This is where
    # "position" carries the tier (15.5); the rungs above are the press-count axis.
    by = my - 14
    d.rectangle([mx, by, mx + mw, by + 6], outline=mix(C("ink0"), C("dust"), 0.5))
    def gx(ms):
        return round(mx + mw * ms / 1200.0)
    d.rectangle([mx, by, gx(120), by + 6], fill=C("frantic"))
    for ms in (260, 700):
        d.line([(gx(ms), by - 3), (gx(ms), by + 9)], fill=C("dust"), width=2)
    for ms, lab in ((260, "260"), (700, "700")):
        d.text((gx(ms) + 3, by - 12), lab, font=F(9), fill=C("dust"))
    for i in range(5):
        x0 = mx + i * (rw + gap)
        if i == 0:
            d.rectangle([x0, my, x0 + rw, my + mh], fill=mix(C("ink0"), C("frantic"), 0.45))
        elif i == 1:
            d.rectangle([x0, my, x0 + rw, my + mh], fill=C("frantic"))
            d.rectangle([x0 - 2, my - 2, x0 + rw + 2, my + mh + 2], outline=C("chalk"), width=2)
        else:
            d.rectangle([x0, my, x0 + rw, my + mh], outline=mix(C("ink0"), C("dust"), 0.55))
        d.text((x0 + 1, my + mh + 5), names[i], font=F(9), fill=C("dust"))
    bx = mx - 112
    d.polygon([(bx, my), (bx + 20, my), (bx + 10, my + 20)], fill=C("frantic"))
    d.text((bx + 30, my + 3), "FRANTIC", font=F(13), fill=C("chalk"))
    d.text((mx + mw + 16, my), "MED 120 ms", font=F(11), fill=C("dust"))
    d.text((mx + mw + 16, my + 15), "2 TAPS", font=F(11), fill=C("frantic"))
    print("meter: rungs at y=%d, band at y=%d, ticks at x=%d/%d, badge at x=%d"
          % (my, by, gx(260), gx(700), bx))
    d.rectangle([0, 0, W - 1, H - 1], outline=C("wall"))
    return img

# ---------------------------------------------------------------- figure 2: shape sheet
def shapes():
    W, H = 980, 800
    img = Image.new("RGB", (W, H), C("ink0"))
    d = ImageDraw.Draw(img)
    d.text((18, 14), "CADENCE - shape language", font=F(22), fill=C("chalk"))
    d.text((18, 48), "verb identity is shape and position; hue is only ever the tier scale", font=F(11), fill=C("dust"))
    y = 84
    d.text((18, y), "VERB GHOSTS   (30 / 20 / 14 px. The floor is 20 px; the 14 px column is drawn", font=F(13), fill=C("dust"))
    d.text((18, y + 16), "to show where the language breaks - crossed out is a shape that stops reading.", font=F(13), fill=C("dust"))
    y += 40
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
        y += 42
    y += 10
    d.text((18, y), "TIER BADGES   (one channel, three redundant codes: shape, position, hue)", font=F(13), fill=C("dust"))
    y += 26
    for i, (nm, col, kind) in enumerate((("CAREFUL", "careful", "circle"),
                                         ("NORMAL", "normal", "square"),
                                         ("FRANTIC", "frantic", "triangle"))):
        cx = 130 + i * 170
        for j, s in enumerate((22, 16, 12)):
            bx = cx + j * 46
            if kind == "circle":
                d.ellipse([bx - s // 2, y - s // 2, bx + s // 2, y + s // 2], outline=C(col), width=2)
            elif kind == "square":
                d.rectangle([bx - s // 2, y - s // 2, bx + s // 2, y + s // 2], outline=C(col), width=2)
            else:
                d.polygon([(bx - s // 2, y + s // 2), (bx + s // 2, y + s // 2), (bx, y - s // 2)], fill=C(col))
        d.text((cx - 6, y + 26), nm, font=F(11), fill=C("chalk"))
    y += 58
    d.text((18, y), "ENTITIES AND FURNITURE", font=F(13), fill=C("dust"))
    y += 26
    items = [("@", "player, always chalk"), ("r", "rat"), ("S", "sentinel"), ("M", "mirror"),
             ("*", "relic"), ("+", "door"), ("<", "stairs"), ("[]", "telegraph")]
    for i, (glyph, note) in enumerate(items):
        cx = 66 + i * 112
        if glyph == "*":
            d.polygon([(cx, y), (cx + 9, y + 14), (cx, y + 28), (cx - 9, y + 14)], outline=C("chalk"), width=2)
        elif glyph == "+":
            d.rectangle([cx - 10, y, cx + 10, y + 28], fill=mix(C("ink0"), (86, 74, 48), 1))
            d.line([(cx - 5, y + 14), (cx + 5, y + 14)], fill=C("normal"), width=2)
        elif glyph == "<":
            d.polygon([(cx - 9, y + 4), (cx + 9, y + 4), (cx, y + 26)], fill=C("chalk"))
        elif glyph == "[]":
            telegraph(d, cx, y + 14, 28, C("frantic"))
        else:
            d.text((cx - 6, y), glyph, font=F(20), fill=C("chalk"))
        d.text((cx - 34, y + 34), note, font=F(9), fill=C("dust"))
    y += 74
    d.text((18, y), "PALETTE   (10 tokens; contrast vs ink0 measured, WCAG relative luminance)", font=F(13), fill=C("dust"))
    y += 26
    for i, name in enumerate(PAL):
        cx = 18 + i * 96
        d.rectangle([cx, y, cx + 84, y + 26], fill=C(name), outline=C("wall"))
        d.text((cx, y + 32), name, font=F(11), fill=C("chalk"))
        d.text((cx, y + 46), PAL[name], font=F(9), fill=C("dust"))
        d.text((cx, y + 58), "%.2f:1" % contrast(name, "ink0"), font=F(9), fill=C("dust"))
    d.rectangle([0, 0, W - 1, H - 1], outline=C("wall"))
    return img

def png(img):
    buf = io.BytesIO(); img.save(buf, "PNG"); return buf.getvalue()

if __name__ == "__main__":
    for p, im in (("mockups/screen.png", screen()), ("mockups/shapes.png", shapes())):
        with open(p, "wb") as fh:
            fh.write(png(im))
        print("wrote", p)
    print("light-model ceilings (derived, not tokens):")
    for nm, t in (("lit_floor", ("dust", 0.27)), ("lit_wall", ("dust", 0.42)), ("lit_edge", ("ghost", 0.55))):
        v = mix(C("ink0"), C(t[0]), t[1])
        print("  %-10s #%02x%02x%02x" % (nm, *v))
    print("contrast vs ink0:")
    for name in PAL:
        print("  %-8s %-8s %.2f" % (name, PAL[name], contrast(name, "ink0")))
    print("separation of the three tiers, linear-RGB distance (Vienot 1999 CVD matrices):")
    for a, b in (("careful", "normal"), ("normal", "frantic"), ("careful", "frantic")):
        print("  %-8s %-8s normal %.3f  protan %.3f  deutan %.3f"
              % (a, b, sep(a, b), sep(a, b, P), sep(a, b, D)))
    for name in ("careful", "normal", "frantic"):
        print("  %-8s simulates to %s under protanopia" % (name, cvd(name, P)))
    lit = mix(C("ink0"), C("dust"), 0.27)
    over = mix(lit, C("ghost"), 0.45)
    plate = mix(lit, C("ink0"), 0.72)
    wall = mix(C("ink0"), C("dust"), 0.42)
    print("tier hues drawn on the brightest surfaces, vs the 3:1 floor for non-text:")
    for name in ("careful", "normal", "frantic", "guard", "ghost"):
        print("  %-8s on lit_floor %.2f   on lit_wall %.2f"
              % (name, crgb(C(name), lit), crgb(C(name), wall)))
    print("ghost painted straight onto the brightest lit floor: %.2f:1  (fails 3:1)" % crgb(over, lit))
    print("ghost on a dark plate (the shipped rule):          %.2f:1" % crgb(C("ghost"), plate))
