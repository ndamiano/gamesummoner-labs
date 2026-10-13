"""The visual language of CADENCE - DESIGN.md section 14.

Palette, the shape law, and the drawing primitives.  Deliberately the same code
as ``figures/make_figures.py`` (14.10: "this file is the seed of the renderer
rather than a throwaway"): polygon + ellipse + line, no bitmaps, no licensed
fonts.  If something cannot be drawn here it is not finished, it is decorated.
"""
import math

from PIL import Image, ImageDraw, ImageFont

# ----------------------------------------------------------------- palette --
INK = "#0E1116"        # void, outside the light
SLATE = "#1B2129"      # unlit floor
STONE = "#2C343F"      # walls (always darker than the floor beside them)
EDGE = "#39424E"       # inactive UI lines, unlit rungs
ASH = "#8C93A0"       # careful tier, secondary text, unaware enemies
CHALK = "#E8E4DA"      # the player, primary text
LANTERN = "#E8A33D"    # normal tier, light, intent ghost
EMBER = "#D4483B"      # frantic tier, damage, aggro
TEAL = "#4FA3A5"       # room affordances: doors, chests, stairs, switches
VIOLET = "#7C6BD1"     # the grammar itself: relics, ladder edits

FLOOR_NEAR = "#28313C"  # slate + 14% lantern: floor inside the light
WALL_DARK = "#151A21"

TIER = {"careful": ASH, "normal": LANTERN, "frantic": EMBER}

_fc = {}


def F(sz):
    if sz not in _fc:
        _fc[sz] = ImageFont.load_default(sz)
    return _fc[sz]


def txt(d, xy, s, sz=13, fill=CHALK, anchor="lt", bold=False):
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


def rgba(hexcol, a):
    """(r,g,b,a) tuple for real alpha drawing."""
    p = hexcol.lstrip("#")
    return (int(p[0:2], 16), int(p[2:4], 16), int(p[4:6], 16), int(round(255 * a)))


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
    """14.2 the shape law: rung n is a polygon with n sides (0 = ring, 1 = dot).

    Screen-aligned, never rotated with the world, never scaled per encounter.
    """
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


def glyph_points(shape, cx, cy, r):
    if shape == "ring":
        return ngon(cx, cy, r, 24)
    if shape == "dot":
        return [(cx + r * 0.6 * math.cos(math.radians(a)), cy + r * 0.6 * math.sin(math.radians(a)))
                for a in range(0, 360, 30)]
    if shape == "lens":
        return vesica(cx, cy, r)
    return ngon(cx, cy, r, int(shape[-1]))


def tapdots(d, x, y, n, col=ASH, r=4, gap=16):
    """tap-count dots, used on the ladder poster and the tutorial cards."""
    for i in range(n):
        d.ellipse([x + i * gap - r, y - r, x + i * gap + r, y + r], fill=col)


def dashed_circle(d, cx, cy, r, col, width=3, arc=25, step=45):
    for a in range(0, 360, step):
        p0 = (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        p1 = (cx + r * math.cos(math.radians(a + arc)), cy + r * math.sin(math.radians(a + arc)))
        d.line([p0, p1], fill=col, width=width)


def dashed_arc(d, cx, cy, r, a0, a1, col, width=2, step=14):
    a = a0
    while a < a1:
        b = min(a + step, a1)
        p0 = (cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
        p1 = (cx + r * math.cos(math.radians(b)), cy + r * math.sin(math.radians(b)))
        d.line([p0, p1], fill=col, width=width)
        a = b + step


def vignette(im, strength=0.5):
    """the one asset the design allows itself (14.10): a vignette."""
    w, h = im.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([-w * 0.25, -h * 0.35, w * 1.25, h * 1.35], fill=255)
    shade = Image.new("RGB", (w, h), INK)
    return Image.composite(im, shade, mask.point(lambda v: int(v * (1 - strength) + 255 * strength)))
