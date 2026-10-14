"""CADENCE - a headless screenshot of the real renderer.

src/render.js is canvas-only, so a browser is the only way to see it normally. This runs the
renderer under Node against a recording canvas (tools/canvas.js), then paints the recorded
ops into a PNG. It is not part of the game; it exists so the composition, the light model
and the HUD anchoring can be looked at, and so a change to the renderer leaves an image
behind instead of an argument.

  node tools/canvas.js 5 4242 3 > tools/out/ops.json      # room 5, seed, taps pending
  python3 tools/shot.py tools/out/ops.json tools/out/shot.png
"""
import json, re, sys
from PIL import Image, ImageDraw


def col8(c, a=1):
    """PIL takes #rrggbbaa; the renderer emits css, which may be rgba(...). One place to
    translate, so the recorder can pass through whatever src/color.js produces."""
    m = re.match(r"rgba\((\d+),(\d+),(\d+),([0-9.]+)\)", c)
    if m:
        r, g, b, al = m.groups()
        c = "#%02x%02x%02x" % (int(r), int(g), int(b))
        a = min(a, float(al))
    if a not in (1, None):
        c += "%02x" % max(0, min(255, int(round(a * 255))))
    return c

def arc_points(cx, cy, r, a0, a1, seg=48):
    if a1 is None:
        a1 = a0 + 2 * 3.141592653589793
    pts = []
    for i in range(seg + 1):
        a = a0 + (a1 - a0) * i / seg
        pts.append((cx + r * __import__("math").cos(a), cy + r * __import__("math").sin(a)))
    return pts

def paint(ops, W, H):
    img = Image.new("RGB", (W, H), "#000000")
    d = ImageDraw.Draw(img, "RGBA")
    for o in ops:
        col = col8(o.get("c") or "#000", o.get("a", 1))
        if o["op"] == "rect":
            d.rectangle([o["x"], o["y"], o["x"] + o["w"], o["y"] + o["h"]], fill=col)
        elif o["op"] == "srect":
            d.rectangle([o["x"], o["y"], o["x"] + o["w"] - 1, o["y"] + o["h"] - 1],
                        outline=col, width=max(1, int(o.get("lw", 1))))
        elif o["op"] in ("path", "fill"):
            pts, polys, cur = o.get("p", []), [], []
            for p in pts:
                if len(p) >= 4:                      # an arc: cx, cy, r, a0[, a1]
                    if cur: polys.append(cur); cur = []
                    a1 = p[4] if len(p) > 4 and p[4] is not None else p[3] + 6.283185307
                    polys.append(arc_points(p[0], p[1], p[2], p[3], a1))
                else:
                    cur.append(tuple(p[:2]))
            if cur: polys.append(cur)
            for poly in polys:
                if len(poly) < 2:
                    continue
                if o["op"] == "fill":
                    d.polygon(poly, fill=col)
                else:
                    d.line(poly, fill=col, width=max(1, int(o.get("lw", 1))))
        elif o["op"] == "text":
            d.text((o["x"], o["y"]), o["t"], fill=col, anchor="mm")
    return img

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    img = paint(spec["ops"], spec["w"], spec["h"])
    img.save(sys.argv[2])
    print("wrote", sys.argv[2], img.size)
