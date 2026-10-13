"""The renderer (DESIGN.md 14).

Polygon + ellipse + line, no bitmaps, no licensed fonts, one ten-colour palette
and the shape law: rung n is a polygon with n sides.  The world geometry rotates
so that facing reads up-right; every glyph, label and meter stays screen-aligned
(14.3).  The meter is fixed at bottom centre and is never covered; the intent
ghost sits outside it, to the left (14.4).

The shading is the one from figures/make_figures.py fig_room: unlit floor is
SLATE, floor inside the light is slate + 14% lantern, walls are always darker
than the floor beside them, and outside the light the walls are the void.
"""
import math

from PIL import Image, ImageDraw

from . import ladder as L
from . import theme as T
from . import world as W
from .config import MAX_HP, LIGHT_RADIUS

BAND_TOP = 106          # the world is only ever drawn between these two lines
BAND_BOTTOM_PAD = 104
TIER_COLOUR = T.TIER
DIRV = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
LIT_FLOOR = T.mix(T.SLATE, T.LANTERN, 0.14)


def room_rotation(room):
    """12: a room that is only corridors gains nothing from rotation."""
    straight = 0
    for y in range(room.h):
        for x in range(room.w):
            if room.solid(x, y):
                continue
            open_dirs = [(dx, dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                         if not room.solid(x + dx, y + dy)]
            if len(open_dirs) == 2 and open_dirs[0][0] == -open_dirs[1][0] and \
                    open_dirs[0][1] == -open_dirs[1][1]:
                straight += 1
    return 0 if straight >= 6 else 20


class Camera:
    def __init__(self, cx, cy, ts, angle_deg, px=0, py=0):
        self.ts = ts
        a = math.radians(angle_deg)
        self.C, self.S = math.cos(a), math.sin(a)
        self.pcx, self.pcy = (px + 0.5) * ts, (py + 0.5) * ts
        self.scx, self.scy = cx, cy

    def w2s(self, wx, wy):
        dx, dy = wx - self.pcx, wy - self.pcy
        return (self.scx + dx * self.C - dy * self.S, self.scy + dx * self.S + dy * self.C)

    def tile(self, c, r):
        return self.w2s((c + 0.5) * self.ts, (r + 0.5) * self.ts)


class Renderer:
    def __init__(self, game, fx, width=1280, height=720):
        self.game = game
        self.fx = fx
        self.w, self.h = width, height
        self.angle = room_rotation(game.room)
        self.toast = None
        self.toast_until = 0
        self._lit = {}

    # ------------------------------------------------------------------ api --
    def say(self, text, now, ms=3200):
        self.toast = text
        self.toast_until = now + ms

    def render(self, now, assist=False, screen="play"):
        g = self.game
        im = Image.new("RGB", (self.w, self.h), T.INK)
        band_bot = self.h - BAND_BOTTOM_PAD
        ts = self.tile_size(g.room, band_bot - BAND_TOP)
        cam = Camera(self.w // 2, (BAND_TOP + band_bot) // 2, ts, self.angle,
                     g.player.x, g.player.y)
        shake = self.fx.shake
        if shake:
            cam.scx += math.sin(now / 21.0) * shake
            cam.scy += math.cos(now / 17.0) * shake
        light = g.room.fov(g.player.x, g.player.y, LIGHT_RADIUS)

        layer = Image.new("RGB", (self.w, self.h), T.INK)
        d = ImageDraw.Draw(layer)
        self.draw_tiles(d, cam, light, now)
        self.draw_affordances(d, cam, now)
        self.draw_intent(d, cam, now)
        self.draw_fx_world(d, cam, now)
        self.draw_monsters(d, cam, now)
        self.draw_player(d, cam, now)
        if assist:
            self.draw_dwell(d, cam, now)
        if not g.settings.reduced_motion:
            layer = T.vignette(layer, 0.35)
        mask = Image.new("L", (self.w, self.h), 0)
        ImageDraw.Draw(mask).rectangle([0, BAND_TOP, self.w, band_bot], fill=255)
        im.paste(layer, (int(math.sin(now / 21.0) * shake),
                         int(math.cos(now / 17.0) * shake)), mask)

        d = ImageDraw.Draw(im, "RGBA")
        if self.fx.flash:
            col = TIER_COLOUR.get(self.fx.flash.get("tier", "normal"), T.LANTERN)
            d.rectangle([0, BAND_TOP, self.w, band_bot], fill=T.rgba(col, 0.04))
        if self.fx.desaturate > 0.01:
            d.rectangle([0, BAND_TOP, self.w, band_bot],
                        fill=T.rgba(T.INK, 0.35 * self.fx.desaturate))
        self.draw_hud(d, now)
        self.draw_meter(d, now)
        self.draw_ghost(d, now)
        if self.toast and now < self.toast_until:
            a = 1.0 if self.toast_until - now > 600 else max(0.0, (self.toast_until - now) / 600.0)
            T.txt(d, (self.w // 2, band_bot - 26), self.toast, 13,
                  T.mix(T.INK, T.ASH, a), "ma")
        if screen != "play":
            self.draw_screen(d, screen, now)
        if g.settings.grey:
            im = im.convert("L").convert("RGB")
        return im

    # ------------------------------------------------------------- helpers --
    def tile_size(self, room, band_h):
        """the room is scaled to the band and cropped by it (14.3)."""
        return max(26, min(48, int(band_h / float(max(8, room.h)))))

    def lit(self, c, r):
        return self._lit.get((c, r), 0.0)

    def shade(self, c, r, col):
        """an affordance is legible in the dark but never bright (14.3)."""
        return T.mix(T.INK, col, 0.30 + 0.70 * self.lit(c, r))

    # ---------------------------------------------------------------- tiles --
    def draw_tiles(self, d, cam, light, now):
        room = self.game.room
        self._lit = {}
        ts = cam.ts
        pad = ts * 0.04
        for r in range(room.h):
            for c in range(room.w):
                t = light.get((c, r), 0.0)
                self._lit[(c, r)] = t
                pts = [cam.w2s(c * ts + dx, r * ts + dy) for dx, dy in
                       ((-pad, -pad), (ts + pad, -pad), (ts + pad, ts + pad), (-pad, ts + pad))]
                ch = room.tile(c, r)
                if ch in (W.WALL, W.PILLAR):
                    wall = T.mix(T.WALL_DARK, T.STONE, t)
                    d.polygon(pts, fill=wall)
                    if t > 0.10:
                        edge = T.mix(T.INK, T.mix(T.EDGE, T.ASH, 0.55), t)
                        for i, (nx, ny) in enumerate(((0, -1), (1, 0), (0, 1), (-1, 0))):
                            if not room.solid(c + nx, r + ny):
                                d.line([pts[i], pts[(i + 1) % 4]], fill=edge, width=1)
                else:
                    floor = T.mix(T.SLATE, LIT_FLOOR, t)
                    if self.fx.dim:
                        floor = T.mix(floor, T.INK, 0.10 * self.fx.dim)
                    d.polygon(pts, fill=floor)
                    if t > 0.45 and (c + r) % 3 == 0:
                        d.point(cam.tile(c, r), fill=T.mix(floor, T.CHALK, 0.07))

    # ---------------------------------------------------------- affordances --
    def draw_affordances(self, d, cam, now):
        room = self.game.room
        for r in range(room.h):
            for c in range(room.w):
                ch = room.tile(c, r)
                if ch not in (W.DOOR, W.DOOR_OPEN, W.LOCKED, W.CHEST, W.CHEST_OPEN,
                              W.STAIRS, W.COUNTER, W.SWITCH, W.SWITCH_ON, W.PILLAR):
                    continue
                cx, cy = cam.tile(c, r)
                col = self.shade(c, r, T.TEAL)
                if ch == W.DOOR:
                    d.rounded_rectangle([cx - 15, cy - 15, cx + 15, cy + 15], 5, outline=col, width=2)
                    d.line([(cx - 15, cy), (cx + 15, cy)], fill=col, width=2)
                elif ch == W.DOOR_OPEN:
                    d.rounded_rectangle([cx - 15, cy - 15, cx + 15, cy + 15], 5,
                                        outline=T.mix(col, T.INK, 0.55), width=1)
                elif ch == W.LOCKED:
                    d.rounded_rectangle([cx - 15, cy - 15, cx + 15, cy + 15], 5, outline=col, width=2)
                    d.line([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=col, width=2)
                    d.line([(cx + 8, cy - 8), (cx - 8, cy + 8)], fill=col, width=2)
                elif ch == W.CHEST:
                    T.dashed_circle(d, cx, cy, 15, col, width=3)
                elif ch == W.CHEST_OPEN:
                    d.rounded_rectangle([cx - 12, cy - 12, cx + 12, cy + 12], 4,
                                        outline=T.mix(col, T.INK, 0.6), width=1)
                elif ch == W.STAIRS:
                    for i in range(3):
                        o = -10 + i * 8
                        d.line([(cx - 12, cy + o), (cx, cy + o + 8), (cx + 12, cy + o)],
                               fill=col, width=2)
                elif ch == W.COUNTER:
                    d.line([(cx - 16, cy - 6), (cx - 16, cy + 10), (cx + 16, cy + 10),
                            (cx + 16, cy - 6)], fill=col, width=2)
                elif ch in (W.SWITCH, W.SWITCH_ON):
                    p = T.ngon(cx, cy, 12, 4, rot=0)
                    if ch == W.SWITCH_ON:
                        d.polygon(p, fill=T.rgba(T.TEAL, 0.30))
                    d.line(p + [p[0]], fill=col, width=2)
                elif ch == W.PILLAR:
                    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=T.mix(T.INK, T.LANTERN, 0.4))
        for pk in room.pickups:
            if not pk[2]:
                continue
            c, r = pk[0], pk[1]
            cx, cy = cam.tile(c, r)
            col = self.shade(c, r, T.VIOLET)
            p = T.ngon(cx, cy, 13, 5)
            d.line(p + [p[0]], fill=col, width=2)
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=col)

    # --------------------------------------------------------------- intent --
    def draw_intent(self, d, cam, now):
        """14.5: the intent ghost is drawn on the tile the verb would affect.
        It is never bright - a ghost, not a light."""
        intent = self.game.rec.intent()
        if not intent:
            return
        p = self.game.player
        dx, dy = DIRV[p.facing]
        c, r = p.x + dx, p.y + dy
        if not self.game.room.inside(c, r):
            return
        ts = cam.ts
        quad = [cam.w2s(c * ts + 3, r * ts + 3), cam.w2s((c + 1) * ts - 3, r * ts + 3),
                cam.w2s((c + 1) * ts - 3, (r + 1) * ts - 3), cam.w2s(c * ts + 3, (r + 1) * ts - 3)]
        col = TIER_COLOUR[intent["tier"]]
        d.polygon(quad, fill=T.rgba(col, 0.10))
        d.line(quad + [quad[0]], fill=T.mix(T.INK, col, 0.8), width=2)
        cx, cy = cam.tile(c, r)
        if self.game.monster_at(c, r):
            self.monster_shape(d, cx, cy, self.game.monster_at(c, r), self.shade(c, r, col))
        T.glyph(d, intent["glyph"], cx, cy, 14, col=col, fill=T.rgba(col, 0.30), w=2)
        if self.game.ladder.has("twin_cut"):
            for ddx, ddy in ((0, -1), (0, 1)):
                if self.game.monster_at(c + ddx, r + ddy):
                    gx, gy = cam.tile(c + ddx, r + ddy)
                    T.glyph(d, intent["glyph"], gx, gy, 9, col=T.mix(T.INK, col, 0.6), w=1)

    # ------------------------------------------------------------- creatures --
    def monster_shape(self, d, cx, cy, m, eye_col):
        """14.3: a hole in the light with exactly one bright feature, the eye.
        Awareness is the eye's brightness, not its colour."""
        p = T.ngon(cx, cy, 17, m.sides)
        d.polygon(p, fill="#090c10")
        d.line(p + [p[0]], fill=T.mix(T.INK, T.CHALK, 0.22), width=1)
        d.ellipse([cx - 3, cy - 4, cx + 3, cy + 2], fill=eye_col)
        if m.max_hp != m.hp:
            for i in range(m.max_hp):
                if i < m.hp:
                    d.point((cx - 12 + i * 3, cy + 14), fill=T.mix(T.INK, T.EMBER, 0.85))

    def draw_monsters(self, d, cam, now):
        for m in self.game.monsters:
            if not m.alive:
                continue
            cx, cy = cam.tile(m.x, m.y)
            eye = self.shade(m.x, m.y, T.EMBER if m.aggro else T.ASH)
            self.monster_shape(d, cx, cy, m, eye)
            if m.aggro:
                T.dashed_arc(d, cx, cy, 21, 0, 360, T.mix(T.EMBER, T.INK, 0.55), width=1)

    def draw_player(self, d, cam, now):
        p = self.game.player
        cx, cy = cam.tile(p.x, p.y)
        ts = cam.ts
        tip = cam.w2s((p.x + 0.5) * ts + p.fx() * 0.62 * ts, (p.y + 0.5) * ts + p.fy() * 0.62 * ts)
        lft = cam.w2s((p.x + 0.5) * ts - p.fy() * 0.20 * ts, (p.y + 0.5) * ts + p.fx() * 0.20 * ts)
        rgt = cam.w2s((p.x + 0.5) * ts + p.fy() * 0.20 * ts, (p.y + 0.5) * ts - p.fx() * 0.20 * ts)
        d.ellipse([cx - 17, cy - 17, cx + 17, cy + 17], fill=T.CHALK)
        d.polygon([tip, lft, rgt], fill=T.LANTERN)
        for i in range(p.guard):
            a = math.radians(145 + i * 20)
            ex, ey = cx + 25 * math.cos(a), cy + 25 * math.sin(a)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=T.mix(T.CHALK, T.INK, 0.35))
        if p.refresh:
            T.dashed_arc(d, cx, cy, 24, 0, 360, T.ASH, width=2)
        if self.lit(p.x, p.y) > 0.25:
            T.txt(d, (cx + 24, cy - 32), "you", 11, T.mix(T.INK, T.CHALK, 0.65))

    def draw_dwell(self, d, cam, now):
        """10: the dwell wheel - the same one button with no timing."""
        intent = self.game.rec.intent()
        if not intent:
            return
        p = self.game.player
        cx, cy = cam.tile(p.x, p.y)
        for i in range(1, L.MAX_TAPS + 1):
            a = -90 + (i - 1) * 72
            x = cx + 66 * math.cos(math.radians(a))
            y = cy + 66 * math.sin(math.radians(a))
            rung = L.RUNGS[i]
            sel = (i == intent.get("count"))
            T.glyph(d, rung["glyph"], x, y, 15, col=T.CHALK if sel else T.EDGE,
                    fill=T.rgba(T.LANTERN, 0.3) if sel else None, w=2)
            if sel:
                T.txt(d, (x, y + 26), rung["name"], 11, T.LANTERN, "mm")

    # -------------------------------------------------------------------- fx --
    def draw_fx_world(self, d, cam, now):
        for it in self.fx.items:
            k = it["kind"]
            if "x" not in it:
                continue
            pr = self.fx.progress(it, now)
            cx, cy = cam.tile(it["x"], it["y"])
            if k == "glyph_fire":
                col = TIER_COLOUR[it["tier"]]
                T.glyph(d, L.glyph_for_count(it["count"]), cx, cy, 14 + 6 * pr,
                        col=T.mix(T.INK, col, 1 - pr), w=2)
            elif k == "ring_expand":
                r = 10 + 22 * pr
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          outline=T.mix(T.INK, T.ASH, 1 - pr), width=2)
            elif k == "dust":
                for i in range(3):
                    a = math.radians(200 + i * 40)
                    px, py = cx + 16 * math.cos(a) * pr, cy + 16 * math.sin(a) * pr
                    d.ellipse([px - 2, py - 2, px + 2, py + 2],
                              fill=T.mix(T.INK, T.CHALK, 0.28 * (1 - pr)))
            elif k == "spike":
                dx, dy = DIRV[it["dir"]]
                d.line([(cx, cy), (cx + dx * 40, cy + dy * 40)],
                       fill=T.mix(T.INK, T.LANTERN, 1 - pr), width=3)
            elif k == "trail":
                pts = [cam.tile(self.game.player.x, self.game.player.y)]
                pts += [cam.tile(x, y) for x, y in it["path"]]
                d.line(pts, fill=T.mix(T.INK, T.LANTERN, 0.30 * (1 - pr)), width=4, joint="curve")
            elif k == "hitglyph":
                d.line([(cx - 10, cy - 16 + 4 * pr), (cx + 10, cy - 16 + 4 * pr)],
                       fill=T.mix(T.INK, T.EMBER, 1 - pr), width=3)
                if it["dmg"]:
                    T.txt(d, (cx + 14, cy - 24), str(it["dmg"]), 12,
                          T.mix(T.INK, TIER_COLOUR.get(it["tier"], T.EMBER), 1 - pr))
            elif k == "hurt":
                r = 20 + 8 * pr
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          outline=T.mix(T.INK, T.EMBER, 1 - pr), width=3)
            elif k in ("open", "stairs"):
                r = 12 + 14 * pr
                d.rounded_rectangle([cx - r, cy - r, cx + r, cy + r], 4,
                                    outline=T.mix(T.INK, T.TEAL, 1 - pr), width=2)
            elif k == "beat":
                r = 14 + 26 * pr
                d.ellipse([cx - r, cy - r, cx + r, cy + r],
                          outline=T.mix(T.INK, T.EMBER, 0.8 * (1 - pr)), width=2)
            elif k == "reflect":
                T.dashed_arc(d, cx, cy, 18, 90 * pr, 90 * pr + 180, T.TEAL, width=2)
            elif k == "as_step":
                T.txt(d, (cx + 22, cy - 6), "-> " + it["to"], 12, T.mix(T.INK, T.ASH, 1 - pr))

    # ------------------------------------------------------------------- hud --
    def draw_hud(self, d, now):
        g = self.game
        T.txt(d, (40, 24), "F%d   ROOM %d/%d" % (g.floor + 1, g.room_index + 1,
                                                 g.total_rooms()), 15, T.CHALK, bold=True)
        T.txt(d, (40, 48), "TURN %d" % g.turns, 13, T.ASH)
        T.txt(d, (150, 48), g.room.name, 13, T.mix(T.ASH, T.INK, 0.25))
        x = 40
        for i in range(MAX_HP):
            if i < g.player.hp:
                d.rectangle([x, 72, x + 12, 84], fill=T.CHALK)
            else:
                d.rectangle([x, 72, x + 12, 84], outline=T.EDGE, width=1)
            x += 16
        T.txt(d, (x + 6, 74), "HP", 11, T.ASH)
        gx = x + 44
        for i in range(g.player.guard):
            d.ellipse([gx, 72, gx + 12, 84], fill=T.mix(T.CHALK, T.INK, 0.3))
            gx += 16
        if g.player.guard:
            T.txt(d, (gx + 4, 74), "GUARD", 11, T.ASH)
        tier = L.TIER_RULE[g.last_tier]
        T.txt(d, (self.w - 40, 24), tier["label"], 15, tier["colour"], "ra", bold=True)
        gap = ("%d ms" % g.last_gaps[-1]) if g.last_gaps else "-"
        T.txt(d, (self.w - 40, 48), "last gap %s   %d taps" % (gap, g.last_count), 12, T.ASH, "ra")
        T.txt(d, (self.w - 40, 68), "ladder: %s" % g.ladder.describe(), 11,
              T.mix(T.ASH, T.INK, 0.3), "ra")
        for i, line in enumerate(g.chat[-3:]):
            T.txt(d, (self.w - 40, 92 + i * 16), line, 11,
                  T.mix(T.INK, T.ASH, 0.8 - i * 0.2), "ra")
        hint = tutorial_hint(g)
        if hint:
            T.txt(d, (self.w // 2, 26), hint, 13, T.mix(T.INK, T.ASH, 0.95), "ma")
        for pk in g.room.pickups:
            if pk[2]:
                r = L.RELIC_BY_ID[pk[2]]
                T.txt(d, (self.w // 2, 52),
                      "%s sits on the floor: %s   (walk over it - it costs %d turns)" %
                      (r["name"], r["text"], pk[3]), 12, T.mix(T.INK, T.VIOLET, 0.95), "ma")
                break

    # ---------------------------------------------------------------- meter --
    def draw_meter(self, d, now):
        """14.4: fixed at bottom centre, never covered.  14.8: it is the last
        thing drawn and the first thing kept."""
        g = self.game
        intent = g.rec.intent()
        tier = intent["tier"] if intent else g.last_tier
        lit_rung = intent["count"] if intent else min(g.last_count, L.MAX_TAPS)
        col = TIER_COLOUR[tier]
        w = min(620, self.w - 180)
        x0 = self.w // 2 - w // 2
        y0 = self.h - 96
        h = 84
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 8, fill=T.rgba(col, 0.05),
                            outline=T.EDGE, width=1)
        if tier == "frantic" and not g.settings.reduced_motion:
            for off in (-3, 3):            # jitter, amplitude capped at 3 px
                d.rounded_rectangle([x0 + off, y0, x0 + w + off, y0 + h], 8,
                                    outline=T.mix(T.EDGE, col, 0.4), width=1)
        elif tier == "normal" and not g.settings.reduced_motion:
            pulse = 0.20 + 0.15 * math.sin(now / (1000.0 / 1.2) * math.pi * 2)
            d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 8,
                                outline=T.mix(T.EDGE, col, pulse), width=1)
        d.line([(x0 + 14, y0 + h - 24), (x0 + w - 14, y0 + h - 24)],
               fill=T.mix(T.INK, col, 0.7), width=2)
        rows = g.ladder.poster_rows()
        step = (w - 90) / 5.0
        for i, rung in enumerate(rows):
            cx, cy = x0 + 55 + i * step, y0 + 30
            if i <= lit_rung:
                T.glyph(d, rung["glyph"], cx, cy, 15, col=col, fill=T.rgba(col, 0.30), w=2)
            else:
                T.glyph(d, rung["glyph"], cx, cy, 15, col=T.mix(T.EDGE, T.INK, 0.2), w=2)
            T.txt(d, (cx, y0 + h - 19), rung["name"], 10, T.mix(T.EDGE, col, 0.6), "mm")
        if lit_rung:
            cx = x0 + 55 + (lit_rung - 1) * step
            d.line([(cx, y0 + 6), (cx, y0 + h - 24)], fill=col, width=1)
        T.txt(d, (x0, y0 - 10), "cadence meter", 10, T.mix(T.EDGE, T.ASH, 0.6))

    def draw_ghost(self, d, now):
        """the ghost is outside the meter, to the left, so it never hides the
        rung it is describing."""
        intent = self.game.rec.intent()
        if not intent:
            return
        w = min(620, self.w - 180)
        x0 = self.w // 2 - w // 2
        gx, gy = x0 - 64, self.h - 52
        col = TIER_COLOUR[intent["tier"]]
        T.glyph(d, intent["glyph"], gx, gy, 18, col=col, fill=T.rgba(col, 0.28))
        T.txt(d, (gx, gy - 34), intent["verb"], 12, col, "mb", True)
        if self.may_degrade(intent):
            T.txt(d, (gx, gy + 32), "may become STEP", 10, T.mix(T.INK, T.ASH, 0.85), "mm")

    def may_degrade(self, intent):
        """14.5: the ghost shows what the verb will degrade to when it is
        actually going to hit nothing - which is legible before you press."""
        if not self.game.settings.calm or intent.get("dwell"):
            return False
        g = self.game
        p = g.player
        dx, dy = DIRV[p.facing]
        tx, ty = p.x + dx, p.y + dy
        if intent["verb"] in ("STRIKE", "LUNGE"):
            return g.monster_at(tx, ty) is None and g.room.tile(tx, ty) not in (
                W.CHEST, W.LOCKED)
        if intent["verb"] in ("STEP", "SPRINT"):
            return bool(g.room.solid(tx, ty) or g.monster_at(tx, ty))
        return False

    # -------------------------------------------------------------- overlays --
    def draw_screen(self, d, screen, now):
        g = self.game
        d.rectangle([0, 0, self.w, self.h], fill=T.rgba(T.INK, 0.88))
        if screen in ("rest", "ladder"):
            self.ladder_poster(d, g.ladder)
            self.input_tab(d, g)
            self.profile_text(d, 70, self.h - 160)
            T.txt(d, (self.w // 2, self.h - 26),
                  "release to resume  -  one press undoes your last move (once per room)  "
                  "-  1-4 pick a threshold, [ ] tune it",
                  12, T.ASH, "ma")
        elif screen == "dead":
            T.txt(d, (self.w // 2, self.h // 2 - 90), "YOU DIE", 30, T.EMBER, "mm", bold=True)
            T.txt(d, (self.w // 2, self.h // 2 - 40),
                  "the last thing you did was %s" % (self.game.last_verb or "nothing"),
                  14, T.ASH, "mm")
            self.profile_text(d, self.w // 2 - 240, self.h // 2)
            T.txt(d, (self.w // 2, self.h // 2 + 210), "press to start a new run", 13, T.CHALK, "mm")
        elif screen == "complete":
            T.txt(d, (self.w // 2, self.h // 2 - 90), "YOU REACH THE SURFACE", 26, T.TEAL, "mm", bold=True)
            self.profile_text(d, self.w // 2 - 240, self.h // 2)
            T.txt(d, (self.w // 2, self.h // 2 + 210), "press to start a new run", 13, T.CHALK, "mm")
        elif screen == "help":
            self.help_text(d)

    def ladder_poster(self, d, ladder):
        """14.7: the whole verb set readable on one screen.  This is the pause
        menu, not a help screen bolted onto it."""
        w, h = 620, 400
        x0, y0 = self.w // 2 - w // 2 - 40, 70
        d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 10, outline=T.EDGE, width=1)
        T.txt(d, (x0 + 20, y0 + 12), "THE LADDER", 16, T.CHALK, bold=True)
        yy = y0 + 48
        for rung in ladder.poster_rows():
            tier = T.ASH if rung["n"] == 0 else (T.LANTERN if rung["n"] <= 3 else T.EMBER)
            T.glyph(d, rung["glyph"], x0 + 60, yy + 16, 18, col=T.CHALK, fill=T.rgba(tier, 0.28))
            for i in range(rung["n"]):
                d.ellipse([x0 + 108 + i * 14 - 3, yy + 13, x0 + 108 + i * 14 + 3, yy + 19], fill=T.ASH)
            T.txt(d, (x0 + 210, yy + 4), rung["name"], 16, T.CHALK, bold=True)
            T.txt(d, (x0 + 210, yy + 26), rung["effect"], 11, T.mix(T.ASH, T.INK, 0.25))
            T.txt(d, (x0 + w - 20, yy + 8),
                  ("%d turns" % rung["cost"]) if rung["cost"] > 1 else
                  ("1 turn" if rung["cost"] == 1 else "free"), 11, tier, "ra")
            yy += 58
        if ladder.relics:
            T.txt(d, (x0, y0 + h + 16),
                  "the ladder you have now: " + ", ".join(
                      L.RELIC_BY_ID[r]["name"] for r in ladder.relics), 12, T.VIOLET)

    def input_tab(self, d, g):
        """5.5: the pause menu's input tab.  The thresholds the recogniser is
        running on, in the same units the tutorial teaches them in."""
        th = g.th
        names = [("SLOW_GAP  a gap this slow is CAREFUL", th.SLOW_GAP),
                 ("FAST_GAP  a gap this fast is FRANTIC", th.FAST_GAP),
                 ("COMMIT_WINDOW  silence that ends a burst", th.COMMIT_WINDOW),
                 ("IDLE_WAIT  silence that becomes BRACE", th.IDLE_WAIT)]
        x0 = self.w - 50
        w = 260
        T.txt(d, (x0, 126), "INPUT", 15, T.CHALK, "ra", bold=True)
        for i, (name, val) in enumerate(names):
            sel = (i == g.rec_dial)
            col = T.LANTERN if sel else T.ASH
            y = 154 + i * 34
            T.txt(d, (x0, y), "%d  %s" % (i + 1, name), 11, col, "ra")
            d.line([(x0 - w, y + 22), (x0, y + 22)], fill=T.EDGE, width=2)
            frac = min(1.0, val / 2000.0)
            d.line([(x0 - w, y + 22), (x0 - w + w * frac, y + 22)], fill=col, width=3)
            T.txt(d, (x0 - w, y + 28), "%d ms" % val, 12, col)
        T.txt(d, (x0, 154 + 4 * 34 + 8), "the recogniser runs on these, live",
              11, T.mix(T.ASH, T.INK, 0.35), "ra")

    def profile_text(self, d, x, y):
        p = self.game.profile()
        rows = [
            "floor %d  room %d/%d   turns %d" % (p["floor"], p["room"], p["total_rooms"], p["turns"]),
            "median gap %d ms   tiers  careful %d  normal %d  frantic %d" %
            (p["median_gap"], p["tiers"]["careful"], p["tiers"]["normal"], p["tiers"]["frantic"]),
            "ladder: %s" % p["ladder"],
            "thresholds  slow %d  fast %d  commit %d  idle %d" %
            (p["thresholds"]["SLOW_GAP"], p["thresholds"]["FAST_GAP"],
             p["thresholds"]["COMMIT_WINDOW"], p["thresholds"]["IDLE_WAIT"]),
        ]
        for i, r in enumerate(rows):
            T.txt(d, (x, y + i * 18), r, 12, T.ASH)

    def help_text(self, d):
        lines = [
            "CADENCE - one button.  The frequency of your presses is the verb set.",
            "",
            "1 tap          STEP",
            "2 taps         STRIKE",
            "3 taps         LUNGE",
            "4 taps         GUARD",
            "5 taps         SPRINT (3 turns)",
            "hold           PIVOT - free while held, one detent per 200 ms",
            "hold 2 s       REST - the pause menu",
            "no input 1.5 s BRACE - guard up, free",
            "",
            "the gap between presses sets the tier:",
            "  over 700 ms   CAREFUL   -25% damage, +1 guard, silent",
            "  260-700 ms    NORMAL",
            "  under 260 ms  FRANTIC   +30% damage, everything hears you",
            "",
            "space / enter / click = the button",
            "h help   u undo   s save   r new run   p audio   esc quit",
            "flags: --assist (dwell wheel)  --live  --pulse  --quiet",
            "       --grey  --reduced-motion  --seed N  --resume",
        ]
        T.txt(d, (self.w // 2 - 280, 120), "\n".join(lines), 13, T.CHALK)


def tutorial_hint(g):
    """the first-contact cards of 11.1: one line, never a modal."""
    if g.room.kind == "tutorial1":
        if g.turns == 0:
            return "press once: STEP"
        if g.turns < 3:
            return "hold the press to PIVOT - free, while held"
        return "reach the stairs"
    if g.room.kind == "tutorial2":
        return "two quick presses: STRIKE"
    if g.room.kind == "tutorial3":
        return "a corridor one tile wide - pivot, then step"
    if g.room.kind == "fork":
        return "a fork: STEP takes the lit path, STRIKE the dark one, GUARD the alcove"
    if g.room.kind == "vault":
        return "a locked door: Strike it, or find the switch"
    if g.room.kind == "shop":
        return "the counter sells relics for turns - the price is on the floor label"
    if g.room.kind == "boss":
        return "the Drummer plays a period at you - break its guard on its beat"
    if g.player.hp <= 3:
        return "low: BRACE (no press) puts guard on the tile you face"
    return None
