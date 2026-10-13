"""Verb feedback and motion (DESIGN.md 14.6, 14.8).

Every game event becomes a short-lived effect with a duration from the 14.6
table.  Two rules from 14.8 are enforced here and nowhere else:

* **Input outranks presentation.** ``collapse()`` ends everything except the
  newest effect when a new burst starts, and it *finishes* animations rather
  than cutting them, which is also what 15.1 asks of the audio (tails are
  ducked, never hard-cut).
* **Nothing idles.** Effects only exist because something happened.
"""

VERB_MS = {"BRACE": 150, "STEP": 120, "STRIKE": 140, "LUNGE": 160,
           "GUARD": 180, "SPRINT": 360, "PIVOT": 120, "REST": 200}
MAX_ANIM = 180          # no verb animation longer than this (14.8)


class FX:
    def __init__(self, settings=None):
        self.settings = settings
        self.items = []
        self.flash = None          # commit flash: 2 frames, 4% lift (14.5)
        self.shake = 0
        self.desaturate = 0.0      # Rest: world desaturates 40%
        self.vignette = 0.0
        self.dim = 0.0             # Brace: lantern dims 10% for 6 frames

    def reduce(self):
        return bool(self.settings and self.settings.reduced_motion)

    def handle(self, events, now_ms):
        for e in events:
            self._one(e, now_ms)

    def _add(self, kind, ms, **kw):
        if self.reduce():
            ms = min(ms, 60)
        kw.setdefault("t0", None)
        self.items.append(dict(kind=kind, ms=ms, start=self._now, **kw))
        if len(self.items) > 60:
            del self.items[:-60]

    def _one(self, e, now_ms):
        self._now = now_ms
        t = e["type"]
        if t == "verb":
            v = e["verb"]
            self._add("glyph_fire", VERB_MS.get(v, 150), x=e["x"], y=e["y"],
                      verb=v, tier=e["tier"], count=e["count"])
            if not self.reduce():
                self.flash = dict(ms=32, tier=e["tier"])
            if v in ("STRIKE", "LUNGE") and not self.reduce():
                self.shake = max(self.shake, 4)          # never more than 4 px
        elif t == "move":
            verb = e.get("verb", "STEP")
            path = e.get("path", [])
            if verb == "SPRINT":
                self._add("trail", 360, path=path, fade=True)
            elif path:
                x, y = path[-1]
                self._add("dust", 120, x=x, y=y)
        elif t == "brace":
            self._add("ring_expand", 150, x=e["x"], y=e["y"])
            self.dim = 1.0
        elif t == "guard":
            pass        # the guard ring is drawn from player state, not an effect
        elif t == "strike":
            self._add("spike", 140, x=e["x"], y=e["y"], dir=e.get("dir", 0),
                      lunge=e.get("lunge", False))
        elif t == "degrade":
            self._add("as_step", 700, x=e.get("x"), y=e.get("y"), to=e["to"], why=e["why"])
        elif t == "damage":
            self._add("hitglyph", 220, x=e["x"], y=e["y"], dmg=e.get("dmg", 0),
                      tier=e.get("tier", "normal"))
        elif t == "player_hit":
            self._add("hurt", 240, x=e["x"], y=e["y"], dmg=e.get("dmg", 1))
        elif t == "open":
            self._add("open", 260, x=e["x"], y=e["y"], kind=e["kind"])
        elif t == "switch":
            self._add("open", 260, x=e["x"], y=e["y"], kind="switch")
        elif t == "stairs":
            self._add("stairs", 400, x=e["x"], y=e["y"])
        elif t == "relic":
            self._add("grammar", 900, name=e["name"], id=e["id"])
        elif t == "rest":
            self.desaturate = 1.0
            self.vignette = 1.0
        elif t == "exit_room":
            self.clear()
        elif t == "beat":
            self._add("beat", 260, x=e["x"], y=e["y"], period=e.get("period", 700))
        elif t == "reflect":
            self._add("reflect", 200, x=e["x"], y=e["y"])
        elif t == "pivot":
            self._add("arc", 140, facing=e.get("facing", 0))

    def collapse(self, now_ms):
        """input outranks presentation: end everything, keep nothing pending."""
        for it in self.items:
            it["ms"] = 0
        self.shake = 0

    def clear(self):
        self.items = []
        self.flash = None
        self.shake = 0

    def tick(self, now_ms, dt_ms):
        if self.flash:
            self.flash["ms"] -= dt_ms
            if self.flash["ms"] <= 0:
                self.flash = None
        self.shake = max(0, self.shake - (dt_ms / 40.0))
        self.dim = max(0.0, self.dim - dt_ms / 100.0)
        if not self.any_rest():
            self.desaturate = max(0.0, self.desaturate - dt_ms / 400.0)
            self.vignette = max(0.0, self.vignette - dt_ms / 400.0)
        keep = []
        for it in self.items:
            if it.get("persist"):
                keep.append(it)
            elif now_ms - it["start"] < it["ms"]:
                keep.append(it)
        self.items = keep

    def any_rest(self):
        return self.desaturate > 0.5

    def guard_persist(self, x, y):
        for it in self.items:
            if it["kind"] == "guard_ring" and it["x"] == x and it["y"] == y:
                return True
        return False

    def clear_guard_ring(self):
        self.items = [i for i in self.items if i["kind"] != "guard_ring"]

    def live(self, kind, now_ms):
        return [i for i in self.items if i["kind"] == kind and now_ms - i["start"] < i["ms"]]

    def progress(self, item, now_ms):
        if item["ms"] <= 0:
            return 1.0
        p = (now_ms - item["start"]) / float(item["ms"])
        return max(0.0, min(1.0, p))
