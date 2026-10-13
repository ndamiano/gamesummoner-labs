"""Tunables: the thresholds of DESIGN.md 2.3, the dials of 3 / 9 / 10.

Every number the design calls tunable lives here and nowhere else, so the
pause > input diagram (5.5) and the sliders (10) can read and edit the same
table the recogniser runs on.
"""
from dataclasses import dataclass, field, asdict


@dataclass
class Thresholds:
    """section 2.3 - starting values, all tunable, all shown to the player."""
    DEBOUNCE: int = 40        # below this, a second press is the same press
    HOLD_START: int = 240     # press held past this -> pivot begins, step cancelled
    COMMIT_WINDOW: int = 260  # silence after the last press, then the burst executes
    SLOW_GAP: int = 700       # a gap this long inside a burst splits it in two
    FAST_GAP: int = 260       # median gap under this -> FRANTIC
    IDLE_WAIT: int = 1500     # no input -> Brace
    REST_HOLD: int = 2000     # hold this long -> Rest (menu)
    PIVOT_STEP: int = 200     # ms of hold per detent while pivoting
    DWELL_START: int = 1200   # assist mode (10): dwell wheel appears
    DWELL_STEP: int = 650     # assist mode: auto-scan per rung


@dataclass
class Settings:
    """difficulty and accessibility dials."""
    calm: bool = True          # graceful degradation (2.5) + one undo per room (5.4)
    live: bool = False         # Live mode (3): enemies also move on a clock
    live_period: int = 900     # ms of real time per enemy move in Live mode
    assist: bool = False       # dwell wheel (10): the same one button, no timing
    reduced_motion: bool = False
    grey: bool = False         # the greyscale test of 14, as a setting
    audio: bool = True
    quiet: bool = False        # 15.7 quiet mode: soft attacks, short tails
    pulse: bool = False        # 15.4 the pulse tick; off by default in Calm mode
    volume: dict = field(default_factory=lambda: {
        "switch": 0.5, "verbs": 0.7, "room": 0.4, "drone": 0.35})

    def copy(self):
        return Settings(**asdict(self))


# ------------------------------------------------------------------- world --
MAX_HP = 10
GUARD_CAP = 4
BASE_DAMAGE = {"bump": 1, "strike": 3, "lunge": 4, "guard": 0}
LIGHT_RADIUS = 7.0            # tiles (14.3 one light, radius ~7)
TIER_ORDER = ("careful", "normal", "frantic")
