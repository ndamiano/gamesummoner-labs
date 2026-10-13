"""The input recogniser - the state machine of DESIGN.md 2.4.

Pure logic, no drawing and no clock of its own: the caller feeds press /
release / tick with a monotonic millisecond clock and receives events.  That is
what makes the latency budget analysable (2.3: worst case HOLD_START +
COMMIT_WINDOW ~ 500 ms, ~260 ms for the common single step) and what lets the
whole input design be tested without a window.

Events are dicts:
  {"type":"press"}                                the switch registered (15.2 TICK)
  {"type":"escalate",count,verb,glyph}            the intent climbed a rung (14.5)
  {"type":"cancel"}                               the burst was abandoned
  {"type":"commit",verb,count,tier,gaps,median}   a verb is ready to execute
  {"type":"pivot_begin"} / {"type":"pivot",dir} / {"type":"pivot_end"}
  {"type":"brace",idle_ms,streak}                 nobody pressed (2.1)
  {"type":"rest"}                                 held past REST_HOLD
  {"type":"dwell_begin"/"dwell",rung}             assist mode (10)
"""
from statistics import median

from . import ladder as L
from .config import Thresholds, Settings


class Recognizer:
    IDLE, PENDING, PIVOTING = "IDLE", "PENDING", "PIVOTING"

    def __init__(self, th=None, settings=None, gameladder=None):
        self.th = th or Thresholds()
        self.settings = settings or Settings()
        self.ladder = gameladder or L.Ladder()
        self.state = self.IDLE
        self.burst = []            # press timestamps of the current burst
        self.prev_press = None     # last press before this burst (single-tap rate)
        self.last_press = None     # last press of any kind
        self.last_action = 0       # last committed verb or pivot -> IDLE_WAIT
        self.idle_streak = 0
        self.holding = False
        self.press_down = None
        self.pivot_next = None
        self.rest_fired = False
        self.dwell = None
        self.dwell_next = None
        self.last_tier = "careful"
        self.last_count = 0
        self.last_commit = None
        self.t = 0

    # ------------------------------------------------------------------ in --
    def _now(self, t):
        self.t = max(self.t, int(t))
        return self.t

    def press(self, t):
        t = self._now(t)
        if self.dwell is not None:                       # assist mode (10)
            rung = self.dwell
            self._reset_dwell()
            return [{"type": "press"}, self._commit_at(t, rung, assist=True)]
        if self.last_press is not None and t - self.last_press < self.th.DEBOUNCE:
            return []                                    # 2.3: same press
        prev = self.last_press
        self.last_press = t
        self.holding = True
        self.press_down = t
        self.idle_streak = 0
        out = [{"type": "press"}]

        if self.state == self.PIVOTING:
            return out                                   # the press belongs to the pivot
        if self.state == self.PENDING and self.burst and t - self.burst[-1] > self.th.SLOW_GAP:
            out.append(self._commit_at(t, len(self.burst)))   # SLOW_GAP splits the burst
            self.prev_press, self.burst = prev, [t]
            self.state = self.PENDING
        elif not self.burst:
            self.prev_press = prev
            self.burst = [t]
            self.state = self.PENDING
        else:
            self.burst.append(t)
        out.extend(self._escalate())
        return out

    def release(self, t):
        t = self._now(t)
        self.holding = False
        self.press_down = None
        self.rest_fired = False
        if self.state == self.PIVOTING:
            self.state = self.IDLE
            self.pivot_next = None
            self.last_action = t        # a pivot is free, and it does not arm a Brace
            return [{"type": "pivot_end"}]
        return []

    def tick(self, t):
        t = self._now(t)
        out = []
        if self.holding and self.press_down is not None:
            held = t - self.press_down
            if self.state == self.PENDING and held > self.th.HOLD_START:
                self.state = self.PIVOTING
                self.burst = []
                self.pivot_next = t + self.th.PIVOT_STEP
                out.append({"type": "cancel"})
                out.append({"type": "pivot_begin"})
            if self.state == self.PIVOTING:
                if held > self.th.REST_HOLD:
                    if not self.rest_fired:
                        self.rest_fired = True
                        out.append({"type": "rest"})
                else:
                    self.rest_fired = False
                    while self.pivot_next is not None and t >= self.pivot_next:
                        out.append({"type": "pivot", "dir": 1})
                        self.pivot_next += self.th.PIVOT_STEP
                return out
        if self.state == self.PENDING and self.burst and \
                t - self.burst[-1] > self.commit_window():
            out.append(self._commit_at(t, len(self.burst)))
            return out
        if self.state == self.IDLE:
            out.extend(self._dwell(t))
            if t - self.last_action > self.th.IDLE_WAIT:
                self.last_action = t
                self.idle_streak += 1
                out.append({"type": "brace", "idle_ms": self.th.IDLE_WAIT,
                            "streak": self.idle_streak})
        return out

    # --------------------------------------------------------------- parts --
    def commit_window(self):
        return self.ladder.commit_window(self.th.COMMIT_WINDOW)

    def apply_settings(self):
        """the pause menu's input tab edits the Thresholds object directly, so
        the recogniser reads them live."""
        return self

    def _escalate(self):
        n = min(len(self.burst), L.MAX_TAPS)
        verb = self.ladder.verb_for(n)
        return [{"type": "escalate", "count": n, "verb": verb, "glyph": L.glyph_for_count(n)}]

    def _gaps(self):
        return [self.burst[i + 1] - self.burst[i] for i in range(len(self.burst) - 1)]

    def _intent_gap(self, at=None):
        gaps = self._gaps()
        if gaps:
            return median(gaps)
        if self.prev_press is None:
            return self.th.SLOW_GAP + 1
        start = self.burst[0] if self.burst else at
        return max(0, start - self.prev_press)

    def _commit_at(self, t, count, assist=False):
        gap = self._intent_gap(t)
        tier = L.tier_for(gap, self.th, frantic_allowed=self.ladder.frantic_allowed()) \
            if not assist else "normal"
        n = min(max(int(count), 1), L.MAX_TAPS)
        verb = self.ladder.verb_for(n)
        self.last_tier, self.last_count = tier, n
        self.state = self.IDLE
        ev = {"type": "commit", "verb": verb, "count": n, "tier": tier,
              "gaps": self._gaps(), "median": gap, "glyph": L.glyph_for_count(n),
              "assist": assist}
        self.last_commit = ev
        self.burst = []
        self.last_action = t
        self.idle_streak = 0
        return ev

    def _dwell(self, t):
        if not self.settings.assist:
            return []
        out = []
        if self.dwell is None:
            if t - self.last_action > self.th.DWELL_START:
                self.dwell = 1
                self.dwell_next = t + self.th.DWELL_STEP
                out.append({"type": "dwell_begin", "rung": 1})
        elif t >= self.dwell_next:
            self.dwell = self.dwell % L.MAX_TAPS + 1
            self.dwell_next = t + self.th.DWELL_STEP
            out.append({"type": "dwell", "rung": self.dwell})
        return out

    def _reset_dwell(self):
        self.dwell = self.dwell_next = None

    # ---------------------------------------------------------- readouts --
    def intent(self):
        """what the ghost must show right now (14.5), or None."""
        if self.state == self.PENDING and self.burst:
            n = min(len(self.burst), L.MAX_TAPS)
            return dict(count=n, verb=self.ladder.verb_for(n), glyph=L.glyph_for_count(n),
                        tier=L.tier_for(self._intent_gap(), self.th,
                                        frantic_allowed=self.ladder.frantic_allowed()))
        if self.dwell is not None:
            n = self.dwell
            return dict(count=n, verb=self.ladder.verb_for(n), glyph=L.glyph_for_count(n),
                        tier="normal", dwell=True)
        return None

    def pending_count(self):
        return len(self.burst)
