"""The sound of CADENCE (DESIGN.md 15).

Ten sources, three families plus the switch, built from four primitives: a
filtered noise burst, a decaying sine, a struck-metal partial set, a swept
filter (15.9).  No samples, no recorded audio - the parameter table below *is*
the 15.9 table, and this module is its renderer.

Mixing follows 15.6: six voices, a fixed never-ducked tick, the verb bus owns
the mix and everything else ducks, grammar is the loudest thing and is always
alone.  The envelope law of 15.3 applies to all of it: attack follows the
verb's urgency, decay is always longer than attack.
"""
import math
import random

SR = 22050

TABLE = {
    "tick":    dict(family="switch", prim="noise", atk=0, dec=12, band=(1200, 2500),
                    grains=1, level=0.16, bus="switch", fixed=True),
    "cloth":   dict(family="you", prim="noise", atk=5, dec=110, band=(200, 1800),
                    grains=3, level=0.30, bus="verbs"),
    "click":   dict(family="you", prim="metal", atk=0, dec=45, band=(900, 4200),
                    grains=2, level=0.40, bus="verbs"),
    "bell":    dict(family="you", prim="metal", atk=2, dec=600, band=(1400, 6000),
                    grains=1, level=0.30, bus="verbs"),
    "thud":    dict(family="room", prim="sine+noise", atk=20, dec=160, band=(40, 180),
                    grains=0, level=0.55, bus="verbs"),
    "scrape":  dict(family="you", prim="noise", atk=40, dec=0, band=(300, 1200),
                    grains=0, level=0.30, bus="verbs"),
    "page":    dict(family="you", prim="noise+sweep", atk=3, dec=180, band=(400, 3000),
                    grains=1, level=0.26, bus="verbs"),
    "roomtone": dict(family="room", prim="noise", atk=0, dec=0, band=(60, 900),
                     grains=0, level=0.05, bus="room", loop=20.0),
    "grammar": dict(family="grammar", prim="sinepair", atk=30, dec=600, band=(220, 660),
                    grains=1, level=0.50, bus="grammar"),
    # diegetic non-verb cues: room family, never the verb bus (15.2)
    "door":    dict(family="room", prim="sine+noise", atk=10, dec=220, band=(120, 700),
                    grains=1, level=0.22, bus="room"),
    "hurt":    dict(family="room", prim="sine+noise", atk=6, dec=260, band=(60, 400),
                    grains=1, level=0.60, bus="damage"),
    "beat":    dict(family="room", prim="sine", atk=2, dec=180, band=(70, 240),
                    grains=1, level=0.45, bus="room"),
    # 15.4: the pulse tick, optional and off by default in Calm mode.  It is a
    # room-family cue at a level well under the verbs: a reference, not a voice.
    "pulse":   dict(family="room", prim="noise", atk=0, dec=25, band=(700, 1500),
                    grains=1, level=0.07, bus="room"),
}

# verb -> the motif of 15.3: grains, as (source, offset ms).  None = at the
# player's own gaps, which is what makes Sprint sound like your rhythm.
MOTIF = {
    "BRACE": [("thud", 0)],
    "STEP": [("cloth", 0)],
    "STRIKE": [("click", 0), ("click", 70)],
    "LUNGE": [("click", 0), ("cloth", 120)],
    "GUARD": [("bell", 0)],
    "SPRINT": [("cloth", 0), ("cloth", None), ("cloth", None)],
    "PIVOT": [("scrape", 0)],
    "REST": [("page", 0)],
}

TIER_TREAT = {"careful": dict(lp=1800, atk_add=8, tail=0.0, gain=0.10, semis=0.0),
              "normal": dict(lp=None, atk_add=0, tail=1.0, gain=1.0, semis=0.0),
              "frantic": dict(lp=None, atk_add=0, tail=1.4, gain=1.41, semis=2.0)}

BUS_LEVEL = {"switch": 0.50, "verbs": 0.63, "room": 0.16, "damage": 0.32,
             "grammar": 0.40, "drone": 0.05}
MAX_VOICES = 6


def db(v):
    return 10 ** (v / 20.0)


class Synth:
    """Renders cues into lists of float samples.  Not real-time: the app plays
    the result through the OS, or a WAV is written out for checking."""

    def __init__(self, seed=1234, quiet=False):
        self.rng = random.Random(seed)
        self.quiet = quiet

    # ----------------------------------------------------------- primitives --
    def _noise(self, n):
        return [self.rng.uniform(-1.0, 1.0) for _ in range(n)]

    def _one_pole(self, xs, cutoff):
        a = math.exp(-2 * math.pi * min(cutoff, SR / 2 - 1) / SR)
        y, out = 0.0, []
        for x in xs:
            y = y * a + x * (1 - a)
            out.append(y)
        return out

    def _bandpass(self, xs, lo, hi, order=2):
        out = list(xs)
        for _ in range(order):
            out = self._one_pole(out, hi)
        slow = list(out)
        for _ in range(order):
            slow = self._one_pole(slow, lo)
        return [a - b for a, b in zip(out, slow)]

    def _env(self, n, atk_ms, dec_ms, shape="falling"):
        atk = max(1, int(atk_ms / 1000.0 * SR))
        out = []
        if shape == "sustained":
            for i in range(n):
                out.append(min(1.0, i / atk))
            fade = max(1, int(20 / 1000.0 * SR))
            for i in range(n):
                if i > n - fade:
                    out[i] *= (n - i) / fade
            return out
        if shape == "rising":
            rise = max(1, int(n * 0.45))
            for i in range(n):
                if i < rise:
                    out.append(i / rise)
                else:
                    out.append((1 - (i - rise) / max(1, n - rise)) ** 2)
            return out
        dec = max(1, int(dec_ms / 1000.0 * SR))
        for i in range(n):
            if i < atk:
                out.append(i / atk)
            else:
                out.append(math.exp(-3.2 * (i - atk) / dec))
        return out

    def _metal(self, n, f0, partials=(1.0, 2.76, 5.40, 8.93), decs=(1.0, 0.5, 0.32, 0.18)):
        out = [0.0] * n
        for k, (p, d) in enumerate(zip(partials, decs)):
            f = f0 * p
            if f > SR / 2:
                continue
            amp = 1.0 / (k + 1.5)
            ph = self.rng.uniform(0, 6.28)
            step = 2 * math.pi * f / SR
            dec = max(1, int(n * d))
            for i in range(n):
                out[i] += amp * math.sin(step * i + ph) * math.exp(-3.0 * i / dec)
        return out

    # ------------------------------------------------------------------ cue --
    def cue(self, source, tier="normal", when_ms=0, dur_ms=None, pitch_shift=0.0, gains=None):
        spec = TABLE[source]
        treat = TIER_TREAT[tier]
        atk = spec["atk"] + treat["atk_add"] + (8 if self.quiet else 0)
        tail = (spec["dec"] * treat["tail"]) if spec["dec"] else 0
        if self.quiet:
            tail *= 0.6
        total_ms = (atk + tail) if spec["dec"] else (atk + 140)
        total_ms = max(total_ms, 14)
        if dur_ms:
            total_ms = dur_ms
        n = int(total_ms / 1000.0 * SR)
        semis = treat["semis"] + pitch_shift
        lo, hi = spec["band"]
        if semis:
            k = 2 ** (semis / 12.0)
            lo, hi = lo * k, min(hi * k, SR / 2 - 200)
        prim = spec["prim"]
        sig = [0.0] * n
        if "noise" in prim:
            sig = self._bandpass(self._noise(n), lo, max(lo + 60, hi))
        if "sine" in prim:
            f = (lo + hi) / 2.0
            tone = [math.sin(2 * math.pi * min(f, SR / 2 - 100) * i / SR) for i in range(n)]
            sig = [a * 0.65 + b * 0.55 for a, b in zip(tone, sig)] if "noise" in prim else tone
        if "metal" in prim:
            m = self._metal(n, max(60.0, (lo + hi) / 2.0 * 0.42))
            sig = [a * 0.75 + b * 0.45 for a, b in zip(m, sig)] if "noise" in prim else m
        if "sinepair" in prim:
            a1 = [math.sin(2 * math.pi * lo * i / SR) for i in range(n)]
            a2 = [math.sin(2 * math.pi * lo * 1.04 * i / SR) for i in range(n)]
            sig = [(x + y) * 0.5 for x, y in zip(a1, a2)]
        if "sweep" in prim:
            out, st = [], 0.0
            for i in range(n):
                f = hi - (hi - lo) * (i / max(1, n))
                st = st * math.exp(-2 * math.pi * f / SR) + sig[i]
                out.append(st)
            sig = out
        shape = "sustained" if not spec["dec"] else ("rising" if source == "thud" else "falling")
        env = self._env(n, atk, tail or 120, shape)
        sig = [s * e for s, e in zip(sig, env)]
        if treat["lp"]:
            sig = self._one_pole(sig, treat["lp"])
        if source == "tick" and self.quiet:
            sig = self._one_pole(sig, 900)
        gain = spec["level"] * BUS_LEVEL[spec["bus"]]
        if not spec.get("fixed"):
            gain *= treat["gain"]
        if gains:
            gain *= gains.get(spec["bus"], 1.0)
        out = [0.0] * (n + int(when_ms / 1000.0 * SR))
        off = int(when_ms / 1000.0 * SR)
        for i in range(n):
            out[off + i] = sig[i] * gain
        return out

    def verb_cue(self, verb, tier, gaps=(), gains=None):
        layers = []
        for src, off in MOTIF.get(verb, []):
            if off is None:
                off = int(sum(gaps) / max(1, len(gaps))) if gaps else 180
            layers.append(self.cue(src, tier, when_ms=off, gains=gains))
        return self.mix(layers)

    def room_bed(self, aggro=0.0, seconds=6.0):
        n = int(seconds * SR)
        cut = 260 + 70 * int(min(3, aggro * 3))
        sig = self._one_pole(self._noise(n), cut)
        sig = self._one_pole(sig, cut)
        g = TABLE["roomtone"]["level"] * BUS_LEVEL["room"] * db(6 * aggro)
        return [s * g for s in sig]

    def drone(self, root=110.0, tier="normal", seconds=6.0):
        n = int(seconds * SR)
        f = root * (2 ** (TIER_TREAT[tier]["semis"] / 12.0))
        bed = self._one_pole(self._noise(n), 240 if tier != "frantic" else 700)
        tone = [math.sin(2 * math.pi * f * i / SR) * 0.5 +
                math.sin(2 * math.pi * f * 1.5 * i / SR) * 0.2 for i in range(n)]
        g = BUS_LEVEL["drone"] * (0.6 if tier == "careful" else 1.0)
        return [(b * 0.5 + t * 0.5) * g for b, t in zip(bed, tone)]

    def mix(self, layers):
        layers = layers[:MAX_VOICES]
        n = max((len(l) for l in layers), default=0)
        out = [0.0] * n
        for l in layers:
            for i, v in enumerate(l):
                out[i] += v
        peak = max((abs(v) for v in out), default=0.0)
        if peak > 0.95:
            out = [v * 0.95 / peak for v in out]
        return out

    def to_int16(self, samples):
        return [int(max(-32767, min(32767, round(v * 32767)))) for v in samples]
