"""The tkinter front-end (DESIGN.md 12: v0 is desktop, one key, PIL renderer).

All the app owns is the clock, the key and the frames: the recogniser is fed
``time.monotonic()`` in milliseconds and the engine never sees a device.  There
is a virtual key too (``--script`` / ``--headless``), which is how the whole
game can be driven, recorded and checked without a keyboard, a screen or a
sound card.
"""
import sys
import time

from .config import Settings, Thresholds
from .effects import FX
from .game import Game
from .render import Renderer, room_rotation
from .sound import Sound, write_wav

KEYS = ("space", "Return", "Enter", "KP_Enter")
QUIT_KEYS = ("Escape", "q")
HELP_KEYS = ("h", "H", "?")


class MutedSound(Sound):
    """the headless path: cues are still synthesised - the game behaves the
    same - and the whole mix is kept so it can be written to a WAV."""

    def __init__(self, settings):
        Sound.__init__(self, settings, find_backend=False)
        self.buffer = []

    def play(self, samples):
        self.buffer.extend(samples)

    def dump(self, path):
        return write_wav(path, self.buffer)


class App:
    FPS = 30
    STEP = int(1000.0 / FPS)

    def __init__(self, seed=None, settings=None, th=None, size=(1280, 720),
                 script=None, headless=False, record=None):
        self.settings = settings or Settings()
        self.th = th or Thresholds()
        self.game = Game(seed, self.settings, self.th)
        self.fx = FX(self.settings)
        self.sound = MutedSound(self.settings) if headless else Sound(self.settings)
        self.t0 = time.monotonic()
        self.now = 0
        self.down_at = None
        self.screen = "play"
        self.script = script or []
        self.record = record
        self.headless = headless
        self.running = True
        self._last_pulse = 0
        self.size = size
        self.root = None
        self.renderer = Renderer(self.game, self.fx, size[0], size[1])
        if not headless:
            self._build_window()

    # ------------------------------------------------------------- the window --
    def _build_window(self):
        import tkinter as tk
        self.tk = tk
        try:
            root = tk.Tk()
        except tk.TclError:
            raise SystemExit(
                "CADENCE needs a display for the window.  On a machine without one:\n"
                "  python3 main.py --headless --script 500:1:400 --record out/demo\n"
                "which drives the same game from a scripted key track.")
        root.title("CADENCE - one button")
        root.resizable(False, False)
        self.canvas = tk.Canvas(root, width=self.size[0], height=self.size[1],
                                bg="#0E1116", highlightthickness=0)
        self.canvas.pack()
        self.root = root
        self.photo = None
        self.use_imagetk = None
        try:
            from PIL import ImageTk
            self.use_imagetk = ImageTk
        except ImportError:
            self.use_imagetk = None
        root.bind("<KeyPress>", self.on_key)
        root.bind("<KeyRelease>", self.onKeyUp)
        root.bind("<Button-1>", lambda e: self.on_down())
        root.bind("<ButtonRelease-1>", lambda e: self.on_up())
        root.protocol("WM_DELETE_WINDOW", self.quit)
        if self.sound.notice:
            self.renderer.say(self.sound.notice, 0, 7000)
        hint = ("space = the button.  taps are verbs, hold turns, hold 2 s rests.  "
                "h help, u undo, s save, r restart, esc quit")
        self.renderer.say(hint, 0, 12000)

    # ----------------------------------------------------------------- clock --
    def ms(self):
        if self.headless:
            return self.now
        return int((time.monotonic() - self.t0) * 1000)

    # --------------------------------------------------------- event routing --
    def feed(self, events):
        self.fx.handle(events, self.now)
        self.sound.handle(events)
        for e in events:
            t = e["type"]
            if t == "rest" and self.screen == "play":
                self.screen = "rest"
                self.fx.desaturate = 1.0
                self.fx.vignette = 1.0
                self.renderer.say("resting - the pause menu.  release to resume, "
                                  "one press undoes the last move", self.now, 4000)
            elif t == "degrade":
                self.renderer.say("%s became %s (%s)" % (self.game.last_verb, e["to"], e["why"]),
                                  self.now, 2400)
            elif t == "relic":
                self.renderer.say("the ladder changes: %s" % e["name"], self.now, 4500)
            elif t == "stairs":
                self.fx.clear()
            elif t == "relic":
                pass
            elif t == "enter_room":
                self.game.rec.last_action = self.now
            elif t == "death":
                self.screen = "dead"
            elif t == "run_complete":
                self.screen = "complete"

    def step(self, events):
        for e in events:
            t = e["type"]
            if self.screen not in ("play", "rest") or t == "live_tick":
                continue
            if t == "commit" and self.screen == "play":
                self.game.execute(dict(verb=e["verb"], tier=e["tier"], count=e["count"],
                                       gaps=e["gaps"], dir=1))
            elif t == "brace" and self.screen == "play":
                # 2.1: nobody pressed - the turn is not free, it is a Brace
                self.game.execute(dict(verb="BRACE", tier="careful", count=0, gaps=[]))
            elif t == "pivot" and self.screen == "play":
                self.game.execute(dict(verb="PIVOT", tier="normal", count=0, gaps=[],
                                       dir=e["dir"]))

    # ---------------------------------------------------------------- the key --
    def nudge(self, delta):
        th, key = self.game.th, ("SLOW_GAP", "FAST_GAP", "COMMIT_WINDOW",
                                 "IDLE_WAIT")[self.game.rec_dial]
        val = max(60, getattr(th, key) + delta)
        setattr(th, key, val)
        self.renderer.say("%s = %d ms" % (key, val), self.now, 2000)

    def on_key(self, ev):
        k = ev.keysym
        if k in QUIT_KEYS:
            self.quit()
            return "break"
        if k in HELP_KEYS:
            self.screen = "help" if self.screen != "help" else "play"
            return "break"
        if k in ("r", "R"):
            self.restart()
            return "break"
        if k in ("s", "S"):
            self.game.save()
            self.renderer.say("run saved", self.now, 1500)
            return "break"
        if k in ("u", "U"):
            if not self.game.undo():
                self.renderer.say("no undo left this room", self.now, 1500)
            return "break"
        if self.screen == "rest" and k in ("1", "2", "3", "4"):
            self.game.rec_dial = int(k) - 1
            return "break"
        if self.screen == "rest" and k in ("minus", "bracketleft"):
            self.nudge(-20)
            return "break"
        if self.screen == "rest" and k in ("plus", "equal", "bracketright"):
            self.nudge(+20)
            return "break"
        if k in ("p", "P"):
            self.settings.audio = not self.settings.audio
            self.renderer.say("audio %s" % ("on" if self.settings.audio else "off"),
                              self.now, 1500)
            return "break"
        if k in KEYS or (ev.char or "") in (" ", "\r", "\n"):
            self.on_down()
            return "break"
        return None

    def onKeyUp(self, ev):
        if ev.keysym in KEYS or (ev.char or "") in (" ", "\r", "\n"):
            self.on_up()
        return None

    def on_down(self):
        if self.screen in ("dead", "complete"):
            self.restart()
            return
        if self.screen == "help":
            self.screen = "play"
            return
        if self.screen == "rest":
            self.game.undo()
            return
        if self.down_at is None:
            self.down_at = self.ms()
            evs = self.game.rec.press(self.down_at)
            self.sound.cue("tick", "normal")
            self.game.telemetry["presses"].append(self.down_at)
            self.fx.collapse(self.now)
            self.feed(evs)
            self.step(evs)        # a burst can also commit here (SLOW_GAP split)

    def on_up(self):
        if self.down_at is None:
            return
        evs = self.game.rec.release(self.ms())
        self.down_at = None
        if self.screen == "rest":
            # 5: the hold *is* the pause.  Releasing leaves it.
            self.screen = "play"
            self.game.rec.last_action = self.ms()
        self.feed(evs)

    # ------------------------------------------------------------ main loop --
    def tick(self):
        self.now = self.ms()
        if self.settings.pulse and self.screen == "play":
            if self.now - self._last_pulse >= 1000:      # 60 bpm
                self._last_pulse = self.now
                self.sound.pulse()
        evs = self.game.rec.tick(self.now)
        if evs:
            self.feed(evs)
            self.step(evs)
        if self.game.live_tick(self.now) and self.screen == "play":
            self.feed(self.game.drain_events())
        self.fx.tick(self.now, self.STEP)

    def draw(self):
        img = self.renderer.render(self.now, assist=self.settings.assist,
                                   screen=self.screen)
        if self.headless:
            return img
        if self.use_imagetk:
            self.photo = self.use_imagetk.PhotoImage(img)
        else:
            # no ImageTk in this PIL build: Tk 8.6 reads base64 PNG directly
            import base64, io
            buf = io.BytesIO()
            img.save(buf, "PNG", compress_level=0)
            self.photo = self.tk.PhotoImage(data=base64.b64encode(buf.getvalue()).decode("ascii"))
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        return img

    def frame(self):
        self.tick()
        self.draw()
        if self.running:
            self.root.after(self.STEP, self.frame)

    def run(self):
        if self.headless:
            return self.headless_run()
        self.root.after(self.STEP, self.frame)
        self.root.mainloop()
        self.sound.stop()
        return 0

    def capture(self, name="out/screens/capture", script=None, rest=False,
                help_screen=False, dwell=False):
        """render a frame with no window: for checking the UI and the docs.
        Same code path as the headless run."""
        import os
        os.makedirs(os.path.dirname(name) or ".", exist_ok=True)
        self.now = 0
        for (t, taps, gap) in (script or []):
            while self.now < t:
                self.now += self.STEP
                self.tick()
            for i in range(taps):
                self.on_down()
                self.advance(80)
                self.on_up()
                if i < taps - 1:
                    self.advance(max(self.STEP, gap - 80))
            self.advance(self.game.rec.commit_window() + 200)
        if rest:
            self.screen = "rest"
            self.fx.desaturate = 1.0
        if help_screen:
            self.screen = "help"
        if dwell:
            for _ in range(int(self.game.th.DWELL_START / self.STEP) + 3):
                self.now += self.STEP
                self.tick()
        self.draw().save(name + ".png")
        return name + ".png"

    def advance(self, ms):
        steps = max(1, int(round(ms / float(self.STEP))))
        for _ in range(steps):
            self.now += int(ms / steps)
            self.tick()

    def headless_run(self):
        """drive the game from a scripted key track: (start_ms, taps, gap)."""
        images = []
        if self.record:
            import os
            os.makedirs(os.path.dirname(self.record) or ".", exist_ok=True)
        for (t, taps, gap) in self.script:
            while self.now < t:
                self.now += self.STEP
                self.tick()
            # a tap: press, hold 80 ms (under HOLD_START), release, then the gap
            for i in range(taps):
                self.on_down()
                self.advance(80)
                self.on_up()
                if i < taps - 1:
                    self.advance(max(self.STEP, gap - 80))
            self.advance(self.game.rec.commit_window() + 200)
        for _ in range(int(800 / self.STEP)):
            self.now += self.STEP
            self.tick()
        images.append(self.draw())
        if self.record:
            images[0].save(self.record + ".png")
            self.sound.dump(self.record + ".wav")
            print("wrote %s.png / %s.wav" % (self.record, self.record))
        p = self.game.profile()
        print("headless run: room %d/%d  hp %d  turns %d  status %s  tiers %s" %
              (p["room"], p["total_rooms"], p["hp"], p["turns"], p["status"], p["tiers"]))
        return 0

    # ------------------------------------------------------------------ misc --
    def restart(self):
        seed = int(time.time() * 1000) % 10 ** 9
        self.game = Game(seed, self.settings, self.th)
        self.game.rec.last_action = self.ms()
        self.fx.clear()
        self.screen = "play"
        self.down_at = None
        self.renderer.game = self.game
        self.renderer.angle = room_rotation(self.game.room)

    def quit(self):
        self.running = False
        if self.root:
            try:
                self.game.save()
            except Exception:
                pass
            self.root.destroy()


def parse_args(argv):
    settings, th = Settings(), Thresholds()
    seed, size, script, record, resume = None, (1280, 720), None, None, False
    headless = "--headless" in argv
    for flag, attr in (("--assist", "assist"), ("--live", "live"), ("--grey", "grey"),
                       ("--quiet", "quiet"), ("--pulse", "pulse"),
                       ("--reduced-motion", "reduced_motion")):
        if flag in argv:
            setattr(settings, attr, True)
    if "--no-audio" in argv:
        settings.audio = False
    if "--resume" in argv:
        resume = True
    if "--seed" in argv:
        seed = int(argv[argv.index("--seed") + 1])
    if "--size" in argv:
        w, h = argv[argv.index("--size") + 1].split("x")
        size = (int(w), int(h))
    if "--script" in argv:
        script = []
        for part in argv[argv.index("--script") + 1].split(";"):
            if part.strip():
                t, taps, gap = part.split(":")
                script.append((int(t), int(taps), int(gap)))
    if "--record" in argv:
        record = argv[argv.index("--record") + 1]
    return seed, settings, th, size, script, headless, record, resume


def main(argv=None):
    (seed, settings, th, size, script, headless, record,
     resume) = parse_args(list(sys.argv[1:] if argv is None else argv))
    app = App(seed, settings, th, size, script, headless, record)
    if resume:
        loaded = Game.load()
        if loaded:
            loaded.settings, loaded.th = app.settings, app.th
            app.game = loaded
            app.fx = FX(app.settings)
            app.renderer = Renderer(app.game, app.fx, size[0], size[1])
            app.renderer.say("run resumed", app.ms(), 2500)
        else:
            app.renderer.say("no saved run", app.ms(), 2500)
    return app.run()


if __name__ == "__main__":
    raise SystemExit(main())
