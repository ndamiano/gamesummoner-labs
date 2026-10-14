"""CADENCE reference cues and measurements for DESIGN.md section 16 (Sound design).

Writes:
  mockups/cues/*.wav   one mono file per cue, the 15 tick variants, and the worst legal
                       collision twice over (mix_worst_no_plate / mix_worst_with_plate).
                       Reference audio, not game assets: this is how an ear can check
                       section 16 without a browser or a build.
  mockups/sound.png    the cue sheet: envelope, band profile and family per cue, and the
                       tier/rung ladder. Figure for 16.2-16.4.

It also prints every number section 16 quotes, including the measurements behind 16.9.
The cue table below IS the spec: cfg.js would hold the same rows. Synthesis is pure
Python - the same oscillator set the WebAudio graph in src/audio.js would use
(oscillator + biquad + gain), no samples, no network.

Run:  python3 mockups/sound.py
"""
import hashlib, io, math, struct, random
from PIL import Image, ImageDraw, ImageFont

SR = 44100

# ---------------------------------------------------------------- the three channels
# level   -> consequence only (16.1 rule 2): the loud end of the table is reserved for
#            things that happen TO the player. Nothing the player does is loud.
# pitch/timbre -> verb identity. No distinction is carried by pitch alone (16.1 rule 3).
# rhythm  -> what the game is doing (the tick chain, the enemy's scheduled move).
TICK = {                      # the metronome face: one voice, reused, never louder
    "root": 392.0,            # G4. Careful's tick.
    "tier_st": 3.0,           # semitones up per tier step: Normal +3, Frantic +6
    "lvl_db": -18.0,          # the loudest RECURRING sound in the game is -18 dBFS
    "hpf": 200.0,             # the tick's band budget: 200 Hz - 2 kHz, nothing below it
                              # (the body band is consequence's) and nothing above it
    "filt0": 900.0,           # rung 1 lowpass
    "filt_x": 1.25,           # x per rung: the ladder opens as it climbs and tops out at
                              # 2.2 kHz, still inside the tick's band (16.4)
    "n0": 0.22, "n_step": 0.10,   # the rung also raises the transient partial's share:
                              # the same voice, opening up - not a new voice
    "a_ms": 1.0, "d_ms": 26.0,
}
ATTACK_MAX_EVENT = 25.0       # 16.1 rule 5: a cue that answers your press
ATTACK_MAX_WORLD = 60.0       # a cue that announces the game
VOICES = 6                    # 16.5 voice cap
MIX_CEIL = -3.0               # dBFS ceiling for the worst legal mix
BL_LO, BL_HI = 150.0, 6500.0  # 16.4's small-speaker band-limit
MASK_FLOOR = 6.0              # 16.7: a cue must clear whatever may be under it by 6 dB
BODY_HZ = 150.0               # 16.4: reserved to consequence
AIR_HZ = 2400.0               # 16.4: reserved to the two cues that must carry over a room
WORLD_BODY = {"hurt", "die", "idlearm"}
AIR_ONLY = {"pivot", "telegraph"}
# from 2.3, as data - the audio rules are stated against the recogniser's own constants
DEBOUNCE, RESOLVE_ANIM, COMMIT_WINDOW = 40.0, 120.0, 260.0
DUCK_DB = 18.0                # the audio plate: gain pulled off the tick bus. The depth
                              # is not a taste - it is (worst no-plate margin) + 6 dB.
DUCK_PAD = 60.0               # ... for the cue's length plus this much
DUCK_REL = 80.0               # ... restored over this long
BANDS = [f for f in (60.0 * 2 ** (i / 3.0) for i in range(25)) if f <= 12000]

def semis(f0, st):
    return f0 * 2 ** (st / 12.0)

def env(n, a_ms, d_ms, s, r_ms, total_ms):
    """ADSR over the part, in samples."""
    a, d, r = int(a_ms * SR / 1000), int(d_ms * SR / 1000), int(r_ms * SR / 1000)
    out = []
    for i in range(n):
        if a and i < a:
            v = i / a
        elif i < a + d:
            k = (i - a) / max(1, d)
            v = 1.0 + (s - 1.0) * k if s > 0 else math.exp(-4.6 * k)
        elif r and i >= n - r:
            v = s * (n - i) / r
        else:
            v = s
        out.append(max(0.0, v))
    return out

def osc(kind, x):
    if kind == "sine":
        return math.sin(x)
    if kind == "saw":
        return 2 * (x / (2 * math.pi)) - 1
    if kind == "tri":
        return 4 * (x / (2 * math.pi)) - 1 if x < math.pi else 3 - 4 * (x / (2 * math.pi))
    return 1.0 if x < math.pi else -1.0     # square

def lp(sig, fc, passes=1):
    a = math.exp(-2 * math.pi * min(fc, SR / 2) / SR)
    for _ in range(passes):
        out, y = [], 0.0
        for v in sig:
            y = v * (1 - a) + y * a
            out.append(y)
        sig = out
    return sig

def hp(sig, fc):
    l = lp(sig, fc, 2)
    return [x - y for x, y in zip(sig, l)]

def bandlimit(sig, lo=BL_LO, hi=BL_HI):
    return hp(lp(sig, hi, 3), lo)

RNG = random.Random(7)

def synth(part):
    """part = {env: [a,d,sus,r,total], layers: [...]} -> float list, peak 1.0."""
    a, d, s, r, total = part["env"]
    n = int(total * SR / 1000)
    e = env(n, a, d, s, r, total)
    out = [0.0] * n
    for L in part["layers"]:
        kind, g = L[0], L[1]
        if kind == "tone":
            _, _, wv, f0, f1 = L
            ph = 0.0
            for i in range(n):
                f = f0 * (f1 / f0) ** (i / max(1, n - 1))
                out[i] += g * osc(wv, ph) * e[i]
                ph = (ph + 2 * math.pi * f / SR) % (2 * math.pi)
        elif kind == "noise":
            _, _, lpfc, hpfc = L
            raw = [RNG.uniform(-1, 1) for _ in range(n)]
            if lpfc:
                raw = lp(raw, lpfc, 2)
            if hpfc:
                raw = hp(raw, hpfc)
            pk = max(abs(v) for v in raw) or 1.0
            for i in range(n):
                out[i] += g * raw[i] / pk * e[i]
    pk = max(abs(v) for v in out) or 1.0
    return [v / pk for v in out]

def seed_for(c, v=0):
    """Noise is seeded per cue, so every figure this file prints is reproducible the way
    11's determinism promise requires. The 15 ticks share ONE seed per rung: they are the
    same voice filtered differently, and a rung-ladder comparison that also changed the
    noise draw would be measuring the draw."""
    key = c["name"] if c["fam"] != "tick" else "tick.r%d" % c["rung"]
    return int(hashlib.md5(("%s.v%d" % (key, v)).encode()).hexdigest()[:8], 16)


def cue_samples(c, v=0):
    """cue -> float list, normalised to the cue's declared peak (so the level column of
    16.2 is an achievable promise, not a coincidence of the synthesis)."""
    n = int(c["total"] * SR / 1000)
    buf = [0.0] * n
    RNG.seed(seed_for(c, v))
    for off, part in c["parts"]:
        seg = synth(part)
        for i, v in enumerate(seg):
            j = int(off * SR / 1000) + i
            if 0 <= j < n:
                buf[j] += v
    pk = max(abs(v) for v in buf) or 1.0
    tgt = 10 ** (c["lvl"] / 20.0)
    return [v / pk * tgt for v in buf]

# ---------------------------------------------------------------- the cue table
# fam  = the identity channel: plosive (move) / struck (hit) / hum (guard) /
#        sweep (turn) / chime (the game speaking) / impact (consequence) / silence.
# kind = event (answers your press) or world (the game did this).
def tick(tier_i, rung):
    f = semis(TICK["root"], TICK["tier_st"] * tier_i)
    fc = TICK["filt0"] * TICK["filt_x"] ** (rung - 1)
    total = TICK["d_ms"] + 4
    return dict(bus=3, name="tick.t%d.r%d" % (tier_i, rung), fam="tick", rung=rung,
                kind="world", lvl=TICK["lvl_db"], total=total, atk=TICK["a_ms"],
                parts=[(0, dict(env=[TICK["a_ms"], TICK["d_ms"], 0.0, 0, total],
                                layers=[["tone", 1.0, "sine", f, f],
                                        ["tone", 0.35, "sine", 2 * f, 2 * f],
                                        ["noise", TICK["n0"] + TICK["n_step"] * (rung - 1),
                                         fc, TICK["hpf"]]]))])

S_ = [["tone", 0.8, "sine", 262, 233], ["noise", 0.7, 1100, 250]]
CUES = {
    "step": dict(bus=2, name="step", fam="plosive", kind="event", lvl=-12.0, total=48, atk=1,
        parts=[(0, dict(env=[1, 44, 0.0, 0, 48], layers=S_))]),
    "strike": dict(bus=2, name="strike", fam="struck", kind="event", lvl=-10.0, total=92, atk=1,
        parts=[(0, dict(env=[1, 88, 0.0, 0, 92],
                        layers=[["tone", 1.0, "saw", 300, 170],
                                ["noise", 0.5, 2000, 900]]))]),
    "lunge": dict(bus=2, name="lunge", fam="struck", kind="event", lvl=-10.0, total=160, atk=1,
        parts=[(0, dict(env=[1, 55, 0.0, 0, 60], layers=[["tone", 1.0, "saw", 300, 420]])),
               (95, dict(env=[1, 55, 0.0, 0, 60],
                         layers=[["tone", 1.0, "tri", 420, 560],
                                 ["noise", 0.4, 1900, 900]]))]),
    "guard": dict(bus=2, name="guard", fam="hum", kind="event", lvl=-12.0, total=190, atk=20,
        parts=[(0, dict(env=[20, 120, 0.55, 40, 190],
                        layers=[["tone", 1.0, "tri", 175, 175],
                                ["tone", 0.25, "sine", 350, 350]]))]),
    "sprint": dict(bus=2, name="sprint", fam="plosive", kind="event", lvl=-12.0, total=560, atk=1,
        parts=[(o, dict(env=[1, 44, 0.0, 0, 48], layers=S_)) for o in (0, 200, 400)]),
    "pivot": dict(bus=2, name="pivot", fam="sweep", kind="event", lvl=-20.0, total=120, atk=12,
        parts=[(0, dict(env=[12, 48, 0.0, 0, 60], layers=[["noise", 1.0, 3600, 1400]])),
               (58, dict(env=[12, 48, 0.0, 0, 60], layers=[["noise", 1.0, 2400, 1000]]))]),
    "bump": dict(bus=2, name="bump", fam="silence", kind="event", lvl=-99.0, total=0, atk=0, parts=[]),
    "rest": dict(bus=2, name="rest", fam="chime", kind="event", lvl=-16.0, total=150, atk=2,
        parts=[(0, dict(env=[2, 60, 0.0, 0, 66], layers=[["tone", 1.0, "tri", 196, 196]])),
               (70, dict(env=[2, 70, 0.0, 0, 76], layers=[["tone", 1.0, "tri", 247, 247]]))]),

    "idlearm": dict(bus=1, name="idlearm", fam="hum", kind="world", lvl=-22.0, total=220, atk=45,
        parts=[(0, dict(env=[45, 120, 0.4, 50, 220],
                        layers=[["tone", 1.0, "sine", 73, 73],
                                ["tone", 0.2, "sine", 146, 146]]))]),
    "hurt": dict(bus=0, name="hurt", fam="impact", kind="world", lvl=-4.0, total=210, atk=1,
        parts=[(0, dict(env=[1, 150, 0.2, 50, 210],
                        layers=[["tone", 1.0, "sine", 90, 62],
                                ["noise", 0.9, 900, None]]))]),
    "kill": dict(bus=1, name="kill", fam="struck", kind="world", lvl=-8.0, total=170, atk=1,
        parts=[(0, dict(env=[1, 120, 0.0, 40, 170],
                        layers=[["tone", 1.0, "saw", 520, 180],
                                ["noise", 0.8, 2000, 700]]))]),
    "die": dict(bus=0, name="die", fam="chime", kind="world", lvl=-6.0, total=600, atk=8,
        parts=[(0, dict(env=[8, 520, 0.25, 60, 600],
                        layers=[["tone", 1.0, "sine", 220, 55],
                                ["tone", 0.3, "tri", 110, 55]]))]),
    "telegraph": dict(bus=1, name="telegraph", fam="chime", kind="world", lvl=-22.0, total=110, atk=10,
        parts=[(0, dict(env=[10, 40, 0.0, 0, 55], layers=[["tone", 1.0, "sine", 2600, 2600]])),
               (60, dict(env=[10, 40, 0.0, 0, 50], layers=[["tone", 0.8, "sine", 2600, 2600]]))]),
}

# ---------------------------------------------------------------- measurement
BUF, PROF = {}, {}

def dft_mag(sig, f):
    n = len(sig)
    re = im = 0.0
    for i, x in enumerate(sig):
        w = 0.5 - 0.5 * math.cos(2 * math.pi * i / max(1, n - 1))
        a = -2 * math.pi * f * i / SR
        re += x * w * math.cos(a)
        im += x * w * math.sin(a)
    return 2 * math.hypot(re, im) / n

def profile(sig):
    return [20 * math.log10(max(dft_mag(sig, f), 1e-9)) for f in BANDS] if sig else [0.0] * len(BANDS)

def peak_db(s):
    return 20 * math.log10(max(abs(v) for v in s)) if s else -160.0

def attack_ms(s):
    if not s:
        return 0.0
    pk = max(abs(v) for v in s)
    lo = next((i for i, v in enumerate(s) if abs(v) > 0.1 * pk), 0)
    hi = next((i for i, v in enumerate(s) if abs(v) > 0.9 * pk), lo)
    return 1000.0 * (hi - lo) / SR

def dur_ms(s, thr=-40.0):
    if not s:
        return 0.0
    pk = peak_db(s)
    idx = [i for i, v in enumerate(s) if 20 * math.log10(abs(v) + 1e-12) > pk + thr]
    return 1000.0 * (max(idx) - min(idx) + 1) / SR if idx else 0.0

def centroid(p):
    num = sum(f * 10 ** (db / 10.0) for f, db in zip(BANDS, p))
    den = sum(10 ** (db / 10.0) for db in p)
    return num / den if den else 0.0

def band_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)) / len(a))

def primary(p):
    k = max(range(len(p)), key=lambda i: p[i])
    return BANDS[k]

def footprint(p, ref=None, within=12.0):
    """The bands a cue has energy in, within `within` dB of its own peak: the cue's
    claimed band budget (16.3/16.4)."""
    top = ref if ref is not None else max(p)
    f = [x for x, db in zip(BANDS, p) if db > top - within]
    return (min(f), max(f)) if f else (0.0, 0.0)


def openness(p, f_fund):
    """How open the tick's transient is: mean energy above 2.5x the fundamental, minus the
    energy at the fundamental. This is the instrument for the rung channel (16.3); a
    centroid over a 26 ms click is dominated by the tone and measures nothing."""
    hi = [db for f, db in zip(BANDS, p) if f > 2.5 * f_fund]
    k = min(range(len(BANDS)), key=lambda i: abs(BANDS[i] - f_fund))
    return (sum(hi) / len(hi) - p[k]) if hi else -99.0

NOISE_VARIANTS = 3

def has_noise(c):
    return any(L[0] == "noise" for _, part in c["parts"] for L in part["layers"])

def measure():
    for k, c in list(CUES.items()):
        if not c["parts"]:
            BUF[k], PROF[k] = [], [0.0] * len(BANDS)
            continue
        BUF[k] = cue_samples(c)
        # a noisy cue's spectrum is the mean of NOISE_VARIANTS draws; a single draw moves
        # a band by a couple of dB, and section 16's floors are smaller than that
        p = [profile(cue_samples(c, v)) for v in range(NOISE_VARIANTS)] if has_noise(c) else [profile(BUF[k])]
        PROF[k] = [sum(col) / len(col) for col in zip(*p)]
    for ti in (0, 1, 2):
        for rg in (1, 2, 3, 4, 5):
            k = "tick.t%d.r%d" % (ti, rg)
            CUES[k] = tick(ti, rg)
            BUF[k] = cue_samples(CUES[k])
            PROF[k] = profile(BUF[k])
    return {k: (profile(bandlimit(BUF[k])) if BUF[k] else [0.0] * len(BANDS)) for k in BUF}

def report(BL):
    aud = [k for k in CUES if CUES[k]["parts"]]
    print("-- 16.2 the cue table, measured (levels are what the render peaks to) --")
    print("   %-12s %-8s %-6s %7s %8s %8s %9s %11s" %
          ("cue", "family", "kind", "dBFS", "dur ms", "atk ms", "centroid", "peak band"))
    for k in sorted(aud, key=lambda k: (CUES[k]["fam"], k)):
        print("   %-12s %-8s %-6s %7.1f %8.0f %8.1f %9.0f %6.0f Hz"
              % (k, CUES[k]["fam"], CUES[k]["kind"], peak_db(BUF[k]), dur_ms(BUF[k]),
                 attack_ms(BUF[k]), centroid(PROF[k]), primary(PROF[k])))
    print("   %-12s %-8s %-6s %7s %8s - the whiff is silent on purpose (15.8)"
          % ("bump", "silence", "event", "-", 0))

    print("\n-- 16.1 rule 5: attack floors (event <= %.0f ms, world <= %.0f ms) --"
          % (ATTACK_MAX_EVENT, ATTACK_MAX_WORLD))
    for kind, lim in (("event", ATTACK_MAX_EVENT), ("world", ATTACK_MAX_WORLD)):
        worst = max((attack_ms(BUF[k]), k) for k in aud if CUES[k]["kind"] == kind)
        print("   %-5s worst %7.1f ms (%s) limit %4.0f -> %s"
              % (kind, worst[0], worst[1], lim, "ok" if worst[0] <= lim else "FAIL"))
        assert worst[0] <= lim

    print("\n-- 16.4 discriminability: RMS dB difference across the %d-band profile --" % len(BANDS))
    verb = [k for k in CUES if CUES[k]["fam"] != "tick" and CUES[k]["parts"]]
    pairs = sorted((band_dist(PROF[a], PROF[b]), a, b)
                   for i, a in enumerate(verb) for b in verb[i + 1:])
    for d, a, b in pairs[:5]:
        print("   closest  %-11s vs %-11s %5.1f dB" % (a, b, d))
    for d, a, b in pairs[-2:]:
        print("   furthest %-11s vs %-11s %5.1f dB" % (a, b, d))
    floor = MASK_FLOOR
    print("   -> declared floor %.1f dB. The table clears it, but only by %.1f dB at the"
          " closest pair: if a future cue comes closer than the floor, the cue changes and"
          " the floor does not." % (floor, pairs[0][0] - floor))
    assert pairs[0][0] >= floor
    print("   after the small-speaker band-limit %.0f-%.0f Hz (16.4's CVD analogue):" % (BL_LO, BL_HI))
    bl = sorted((band_dist(BL[a], BL[b]), a, b)
                for i, a in enumerate(verb) for b in verb[i + 1:])
    for d, a, b in bl[:5]:
        print("   closest  %-11s vs %-11s %5.1f dB  (full range was %5.1f)"
              % (a, b, d, band_dist(PROF[a], PROF[b])))
    lost = [(a, b, round(d, 1)) for d, a, b in bl if d < floor]
    print("   pairs under the floor after band-limiting: %d%s"
          % (len(lost), "".join("  %s/%s %.1f" % x for x in lost)))
    assert not lost

    print("\n-- 16.7 the audio plate: a cue in its own peak band against the loudest of the "
          "15 sampled ticks (the one sound guaranteed to be playing) --")
    # the plate: measure every cue against the tick family in the cue's OWN peak band
    rows = []
    ticks = [m for m in CUES if m.startswith("tick")]
    for k in [x for x in CUES if CUES[x]["fam"] not in ("tick", "silence") and CUES[x]["parts"]]:
        bi = min(range(len(BANDS)), key=lambda i: abs(BANDS[i] - primary(PROF[k])))
        p_mask, mask_name = max((PROF[m][bi], m) for m in ticks)
        rows.append((PROF[k][bi] - p_mask, k, BANDS[bi], PROF[k][bi], p_mask, mask_name))
    # depth is DERIVED: enough to bring the worst collision to the floor, no more
    duck = round(max(0.0, MASK_FLOOR - min(r[0] for r in rows)), 1)
    print("   depth is derived: (worst collision) + the floor = %.1f dB, applied to the tick"
          " bus for the cue's length + %.0f ms, restored over %.0f ms."
          % (duck, DUCK_PAD, DUCK_REL))
    print("   %-11s %8s %8s %9s %9s %11s %s" %
          ("cue", "band Hz", "cue dB", "mask dB", "no plate", "with plate", "masked by"))
    fails = []
    for raw, k, fb, pv, pm, mn in sorted(rows):
        if raw < MASK_FLOOR:
            fails.append((raw, k, mn))
        print("   %-11s %8.0f %8.1f %9.1f %9.1f %11.1f %s"
              % (k, fb, pv, pm, raw, raw + duck,
                 ("%s" % mn) if raw < MASK_FLOOR else "ok either way"))
    print("   floor %.0f dB. without the plate %d cues fail: %s"
          % (MASK_FLOOR, len(fails),
             ", ".join("%s %.1f (by %s)" % (k, r, m) for r, k, m in fails)))
    worst = round(min(r[0] for r in rows) + duck, 1)
    print("   with the plate, worst margin %.1f dB -> %s"
          % (worst, "ok" if worst >= MASK_FLOOR - 0.05 else "FAIL"))
    assert worst >= MASK_FLOOR - 0.05
    global DUCK_DB
    DUCK_DB = duck

    print("\n-- 16.3 the tick: pitch is the tier channel, filter is the rung, level is fixed --")
    for ti, nm in ((0, "careful"), (1, "normal"), (2, "frantic")):
        print("   %-8s %6.1f Hz (%+.1f st from Careful)"
              % (nm, semis(TICK["root"], TICK["tier_st"] * ti), TICK["tier_st"] * ti))
    print("   rung lowpass ladder:", ", ".join("%.0f Hz" % (TICK["filt0"] * TICK["filt_x"] ** r)
                                              for r in range(5)))
    op = [openness(PROF["tick.t2.r%d" % r], semis(TICK["root"], TICK["tier_st"] * 2))
          for r in (1, 2, 3, 4, 5)]
    print("   rung 1..5 openness at the Frantic pitch:", " ".join("%+.1f" % o for o in op),
          "dB -> monotonic:", all(op[i] < op[i + 1] for i in range(4)))
    assert all(op[i] < op[i + 1] for i in range(4))
    print("   openness spread across the ladder: %.1f dB - the rung channel's whole width;"
          " it must stay a shading, not a second vocabulary" % (op[-1] - op[0]))
    cents = [centroid(PROF["tick.t2.r%d" % r]) for r in (1, 3, 5)]
    print("   (centroid, for the record - dominated by the tone, so NOT the rung measure):",
          ", ".join("%.0f Hz" % c for c in cents))
    lvls = set(round(peak_db(BUF["tick.t%d.r%d" % (t, r)]), 1)
               for t in (0, 1, 2) for r in (1, 3, 5))
    print("   peak level across all 15 sampled ticks:", lvls, "(declared %.1f)" % TICK["lvl_db"])

    print("\n-- 16.4 band budgets: the 1/3-octave span each cue has energy in, within 12 dB")
    print("   of its own peak. This is what the mix bus is built around - it is measured off")
    print("   the rendered cue, not off the synthesis recipe, because a 26 ms click leaks.")
    print("   Two bands are reserved and nothing else may use them:")
    print("   BODY below %.0f Hz = the world side only, buses 0-1 (%s);" % (BODY_HZ, ", ".join(sorted(WORLD_BODY))))
    print("   AIR above %.1f kHz = Pivot and Telegraph only - the two cues that have to be"
          % (AIR_HZ / 1000.0))
    print("   heard over a room full of other people's sounds.")
    print("   %-11s %-8s %9s %9s" % ("cue", "family", "low Hz", "high Hz"))
    for k in sorted(CUES, key=lambda k: (CUES[k]["fam"], k)):
        if not CUES[k]["parts"]:
            continue
        lo, hi = footprint(PROF[k])
        print("   %-11s %-8s %9.0f %9.0f" % (k, CUES[k]["fam"], lo, hi))
    bad = []
    for k in CUES:
        if not CUES[k]["parts"]:
            continue
        lo, hi = footprint(PROF[k])
        if k not in WORLD_BODY and lo < BODY_HZ:
            bad.append((k, "takes a band below %.0f Hz" % BODY_HZ, lo))
        if k not in AIR_ONLY and hi > AIR_HZ:
            bad.append((k, "takes the air band above %.1f kHz" % (AIR_HZ / 1000.0), hi))
    for k in AIR_ONLY:
        assert footprint(PROF[k])[1] > AIR_HZ, k
    for k in WORLD_BODY:
        assert footprint(PROF[k])[1] < 1200.0, k
    print("   -> reserved bands respected by all %d cues: %s"
          % (sum(1 for k in CUES if CUES[k]["parts"]), "ok" if not bad else bad))
    assert not bad
    print("   -> the two air cues are the only ones up there, and the three body cues stay")
    print("      below 1.2 kHz, where the verbs live: ok")
    tl = max(dur_ms(BUF[k], -30.0) for k in CUES if k.startswith("tick"))
    print("   a tick's whole envelope is %.0f ms, against DEBOUNCE = %.0f ms: the metronome"
          % (tl, DEBOUNCE))
    print("   can never smear into a double note however fast you press: %s"
          % ("ok" if tl < DEBOUNCE else "FAIL"))
    assert tl < DEBOUNCE

    print("\n-- 16.5 the worst legal collision (14.2-i: presses during the %.0f ms resolve "
          "window are buffered, so they land ON the commit cue) --" % RESOLVE_ANIM)
    print("   worst legal overlap = a Frantic Lunge commit + the hit it schedules (hurt) + "
          "the presses")
    print("   you kept making during the resolve window: %d ticks at DEBOUNCE spacing (%.0f ms "
          "apart)." % (int(RESOLVE_ANIM // DEBOUNCE), DEBOUNCE))
    n = int(0.9 * SR)
    ev = [("lunge", 2, 0), ("hurt", 0, 0), ("telegraph", 1, 0)]
    ev += [("tick.t2.r5", 3, DEBOUNCE * (i + 1)) for i in range(int(RESOLVE_ANIM // DEBOUNCE))]
    def render(duck):
        buf = [0.0] * n
        for k, bus, ms in ev:
            g = 1.0
            for h, hbus, hms in ev:                 # plate: higher bus ducks lower buses
                if hbus < bus and hms <= ms + RESOLVE_ANIM + DUCK_PAD:
                    g *= 10 ** (-duck / 20.0)
            for i, v in enumerate(BUF[k]):
                j = int(ms * SR / 1000) + i
                if 0 <= j < n:
                    buf[j] += v * g
        return buf
    for label, duck in (("no plate", 0.0), ("plate %.0f dB" % DUCK_DB, DUCK_DB)):
        b = render(duck)
        pk = peak_db(b)
        print("   %-12s peak %7.1f dBFS against the %.1f dBFS ceiling -> %s"
              % (label, pk, MIX_CEIL, "ok" if pk <= MIX_CEIL else "CLIPS"))
        at = 0
        for t in range(0, n, int(0.01 * SR)):
            ms = 1000.0 * t / SR
            at = max(at, sum(1 for k, _, s0 in ev if s0 <= ms <= s0 + dur_ms(BUF[k], -30)))
        print("   %-12s most voices sounding at once: %d (cap %d)" % ("", at, VOICES))
        assert at <= VOICES
        tag = "no_plate" if duck == 0.0 else "with_plate"
        with open("mockups/cues/mix_worst_%s.wav" % tag, "wb") as fh:
            fh.write(wav(b))
    assert peak_db(render(DUCK_DB)) <= MIX_CEIL
    print("   reserved headroom on the level channel: the loudest recurring cue is %.1f dBFS,"
          % TICK["lvl_db"])
    print("   the loudest thing in the game is %.1f dBFS -> %.1f dB of the channel is "
          "consequence and nothing else"
          % (peak_db(BUF["hurt"]), peak_db(BUF["hurt"]) - TICK["lvl_db"]))

def mix(events, duck, mode="max", seconds=0.9):
    """Render a set of (cue, bus, start_ms) with the plate applied to lower buses.
    mode="max" ducks a bus by the DEEPEST duck that applies to it; mode="sum" adds them.
    This is the instrument for 16.12: the plate is one curve per bus, not one per cue."""
    n = int(seconds * SR)
    buf = [0.0] * n
    for k, bus, ms in events:
        g = 1.0
        deeper = [duck for h, hbus, hms in events
                  if hbus < bus and hms <= ms + RESOLVE_ANIM + DUCK_PAD]
        if deeper:
            total = max(deeper) if mode == "max" else sum(deeper)
            g = 10 ** (-total / 20.0)
        for i, v in enumerate(BUF[k]):
            j = int(ms * SR / 1000) + i
            if 0 <= j < n:
                buf[j] += v * g
    return buf


def peak_db_window(sig, t0_ms, t1_ms):
    """Peak inside a time window - for measuring one cue's level inside a mix where the
    other cues have already gone silent."""
    a, b = int(t0_ms * SR / 1000), int(t1_ms * SR / 1000)
    return peak_db(sig[a:b])


def voices_at(events, buf):
    at = 0
    for t in range(0, len(buf), int(0.01 * SR)):
        ms = 1000.0 * t / SR
        at = max(at, sum(1 for k, _, s0 in events
                         if s0 <= ms <= s0 + dur_ms(BUF[k], -30)))
    return at


def wiring_report():
    """16.10-16.12: what the cue table does NOT say - what triggers a cue, what happens
    when the same fact lands twice, what happens when two ducks overlap, and which clock
    `at` is in. Every number here comes off the rendered cues."""
    LADDER = {1: "step", 2: "strike", 3: "lunge", 4: "guard", 5: "sprint"}

    print("\n-- 16.10 can a verb cue ever be retriggered ONTO ITSELF? The earliest next")
    print("   commit is set by 2.3's own constants: n presses cannot arrive faster than")
    print("   n*DEBOUNCE apart, and the burst only commits COMMIT_WINDOW after the last --")
    margins = []
    for n_taps in range(1, 6):
        name = LADDER[n_taps]
        earliest = n_taps * DEBOUNCE + COMMIT_WINDOW
        audible = dur_ms(BUF[name], -40.0)          # 16.2's len column, same measure
        margins.append((earliest - audible, name, earliest, audible))
        print("   %d taps -> %-6s earliest next commit %4.0f ms, cue audible for %4.0f ms"
              "  -> clears itself by %3.0f ms" % (n_taps, name, earliest, audible,
                                                  earliest - audible))
    tight = min(margins)
    print("   -> no verb cue can land on itself. The tightest pair the grammar allows is")
    print("      two Sprints %3.0f ms apart against a cue %3.0f ms long: %3.0f ms of air."
          % (tight[2], tight[3], tight[0]))
    two = mix([("sprint", 2, 0.0), ("sprint", 2, tight[2])], 0.0)
    print("      rendered: peak %6.1f dBFS, one alone %6.1f dBFS -> the ladder's own"
          % (peak_db(two), peak_db(BUF["sprint"])))
    print("      timing is the guard; `cue()` needs no self-overlap check, and no cue is")
    print("      ever heard doubled. Sprint's three internal plosives at 200 ms are the")
    print("      only repetition inside a cue, and they are the cue (16.2).")
    assert all(m[0] > 0 for m in margins)

    print("\n-- 16.10 one cue per FACT, not per instance: what a naive per-instance mix")
    print("   does when two instances of the same fact land in one commit --")
    ticks = [("tick.t2.r5", 3, DEBOUNCE * (i + 1)) for i in range(int(RESOLVE_ANIM // DEBOUNCE))]
    base = [("lunge", 2, 0.0), ("hurt", 0, 0.0), ("telegraph", 1, 0.0)] + ticks
    cases = [
        ("16.5's worst legal mix, as specified", base),
        ("+ a second hurt (two enemies hit you)", base + [("hurt", 0, 0.0)]),
        ("+ a second kill (Twin Cut Strike)", base + [("kill", 1, 0.0), ("kill", 1, 0.0)]),
        ("no hit: lunge + telegraph + 2 kills + 3 ticks",
         [("lunge", 2, 0.0), ("telegraph", 1, 0.0), ("kill", 1, 0.0), ("kill", 1, 0.0)] + ticks),
        ("no hit: lunge + telegraph + 1 kill + 3 ticks",
         [("lunge", 2, 0.0), ("telegraph", 1, 0.0), ("kill", 1, 0.0)] + ticks),
    ]
    for label, ev in cases:
        b = mix(ev, DUCK_DB)
        pk = peak_db(b)
        print("   %-38s voices %d  peak %6.1f dBFS -> %s"
              % (label, voices_at(ev, b), pk, "ok" if pk <= MIX_CEIL else "CLIPS"))
    naive = peak_db(mix(cases[1][1], DUCK_DB))
    print("   -> two co-scheduled `hurt` cues sum in phase: %+.1f dBFS, %.1f dB over the"
          % (naive, naive - MIX_CEIL))
    print("      %.1f ceiling, and the plate cannot help because they share a bus."
          % MIX_CEIL)
    assert naive > MIX_CEIL, "per-instance stacking is supposed to be the thing that breaks"
    print("   -> so the rule is not taste: a per-instance mix cannot be built. One event")
    print("      per fact per commit, `n` carried as data and DRAWN (15.2 pips, 15.8 shake), never")
    print("      heard: 16.1 rules 1 and 3 forbid carrying magnitude on level or pitch.")

    print("\n-- 16.11 two cues needing the plate at once: one curve per BUS (the deepest")
    print("   duck that applies), never one per cue (summing them) --")
    stacked = [("lunge", 2, 0.0), ("telegraph", 1, 0.0), ("hurt", 0, 0.0)] + ticks
    print("   the collision mix, three ducking cues and three ticks:")
    for mode in ("max", "sum"):
        b = mix(stacked, DUCK_DB, mode)
        print("     duck by %-3s -> mix peak %6.1f dBFS (%s)"
              % (mode, peak_db(b), "ok" if peak_db(b) <= MIX_CEIL else "CLIPS"))
    # ... and what it does to the metronome, measured where the ducking cues have already
    # gone silent, so the peak we read is the tick's own
    # ... and what it does to the metronome. Measured in a window where the two ducking
    # cues have gone silent but their duck is still held, so the peak read IS the tick's.
    quiet = [("lunge", 2, 0.0), ("telegraph", 1, 0.0)] + \
            [("tick.t2.r5", 3, 300.0 + DEBOUNCE * i) for i in range(3)]
    bare = peak_db(mix(ticks, 0.0))
    got = {}
    for mode in ("max", "sum"):
        b = mix(quiet, DUCK_DB, mode)
        got[mode] = peak_db_window(b, 300.0, 300.0 + 3 * DEBOUNCE + 40.0)
        print("     the tick under those two ducks, duck by %-3s -> %6.1f dBFS (alone: %6.1f)"
              % (mode, got[mode], bare))
    print("   -> the ceiling does not discriminate between the two policies; the metronome")
    print("      does: %.1f dB apart. Summing ducks pumps the only recurring voice in" % (got["max"] - got["sum"]))
    print("      the game, which 16.1 rule 6 says is ONE voice, and 16.5's voice-drop rule")
    print("      ('never cut the metronome') is the same promise seen from the other side.")
    print("      So: bus_gain is a level per bus, held while any higher bus is sounding,")
    print("      restored over 80 ms (16.7) - not a duck per cue.")
    assert got["max"] > got["sum"] + 15.0

    print("\n-- 16.12 what is NOT measurable here: the clock seam --")
    print("   `cue(name, at)` takes `at` in the AudioContext clock while the recogniser runs")
    print("   on the input clock (2.3, 14.2-i). The two are related by one linear map that")
    print("   the page samples on first gesture and on every suspend/resume; no cue may call")
    print("   ctx.currentTime itself (16.9), so the map is one pure function, testable in")
    print("   14.6 without WebAudio. 16.1 rule 5's 25 ms attack floor is a promise about")
    print("   landing WITH the commit flash, and a fixed output delay would break it silently")
    print("   if nothing compensated for it.")


def wav(samples):
    data = b"".join(struct.pack("<h", max(-32000, min(32000, int(round(v * 32000)))))
                    for v in samples)
    return (b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVEfmt " +
            struct.pack("<IHHIIHH", 16, 1, 1, SR, SR * 2, 2, 16) +
            b"data" + struct.pack("<I", len(data)))

# ---------------------------------------------------------------- the figure
PAL = {"ink0": "#0b0d10", "ink1": "#14171c", "wall": "#1e232b", "dust": "#7d838c",
       "chalk": "#e6e4df", "careful": "#6f7883", "normal": "#d8a53f", "frantic": "#e0553f",
       "guard": "#5fa8c7", "ghost": "#b9c2cb"}
FAMCOL = {"tick": "careful", "plosive": "dust", "struck": "chalk", "hum": "guard",
          "sweep": "dust", "chime": "normal", "impact": "frantic", "silence": "wall"}

def C(n):
    h = PAL[n].lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def F(s):
    assert s >= 11, "15.11-v6: nothing in this game is drawn below 11 px"
    return ImageFont.load_default(size=s)

def sheet():
    # the 13 verb/world cues, then the rung ladder for one tier - the 15 sampled ticks
    # would be 15 near-identical rows and would say nothing
    keys = ([k for k in sorted(CUES, key=lambda k: (CUES[k]["fam"], k))
             if not k.startswith("tick")] + ["tick.t2.r%d" % r for r in (1, 2, 3, 4, 5)])
    W, H = 980, 46 * len(keys) + 210
    im = Image.new("RGB", (W, H), C("ink0"))
    d = ImageDraw.Draw(im)
    d.text((18, 12), "CADENCE - sound cue sheet (DESIGN.md 16.2-16.5)", font=F(16), fill=C("chalk"))
    d.text((18, 36), "one row per cue: envelope (300 px = the cue's full length), then its "
                     "band profile.", font=F(12), fill=C("dust"))
    d.text((18, 50), "hue here is family, for reading the sheet only - in the game hue means "
                     "cadence and nothing else (15.1).", font=F(12), fill=C("dust"))
    y = 70
    for k in keys:
        c, p, s = CUES[k], PROF[k], BUF[k]
        col = C(FAMCOL[c["fam"]])
        if not c["parts"]:
            d.text((18, y + 6), "%-11s" % k, font=F(13), fill=C("dust"))
            d.text((110, y + 6), "silence  %-6s" % c["kind"], font=F(12), fill=C("dust"))
            d.text((230, y + 6), "no cue exists: the whiff is silence (15.8, 16.6)",
                   font=F(12), fill=C("dust"))
            d.line([18, y + 40, W - 18, y + 40], fill=C("wall"))
            y += 46
            continue
        d.text((18, y + 6), "%-11s" % k, font=F(13), fill=C("chalk"))
        d.text((110, y + 6), "%-8s %-6s" % (c["fam"], c["kind"]), font=F(12), fill=col)
        bw, bh, x0 = 300, 26, 230
        d.rectangle([x0, y + 2, x0 + bw, y + 2 + bh], outline=C("wall"))
        if s:
            top, bot = [], []
            for x in range(bw):
                seg = s[x * len(s) // bw:(x + 1) * len(s) // bw] or [0.0]
                a = max(abs(v) for v in seg) / 10 ** (c["lvl"] / 20.0)
                top.append((x0 + x, y + 2 + bh / 2.0 - a * bh / 2.0))
                bot.append((x0 + x, y + 2 + bh / 2.0 + a * bh / 2.0))
            d.polygon(top + bot[::-1], fill=col)
        bx = 560
        nmax = max(p)
        for i, db in enumerate(p):
            hgt = max(0.0, min(bh, (db - (nmax - 40)) / 40.0 * bh))
            d.rectangle([bx + i * 8, y + 2 + bh - hgt, bx + i * 8 + 6, y + 2 + bh], fill=col)
        d.text((790, y + 6), "%6.1f dB %5.0f ms" % (c["lvl"], c["total"]), font=F(12), fill=C("dust"))
        d.line([18, y + 40, W - 18, y + 40], fill=C("wall"))
        y += 46
    d.text((18, y + 8), "tier ticks (the metronome face): pitch = tier (+%.0f st/step), "
                        "lowpass = rung (x%.2f/rung), level fixed at %.0f dBFS"
           % (TICK["tier_st"], TICK["filt_x"], TICK["lvl_db"]), font=F(13), fill=C("chalk"))
    for i, nm in enumerate(("careful", "normal", "frantic")):
        d.ellipse([18 + i * 200, y + 34, 34 + i * 200, y + 50], outline=C(nm), width=2)
        d.text((42 + i * 200, y + 36), "%.0f Hz" % semis(TICK["root"], TICK["tier_st"] * i),
               font=F(12), fill=C("dust"))
    d.text((18, y + 62), "bump is silent. mono output, no panning. voice cap %d. mix ceiling "
                         "%.0f dBFS." % (VOICES, MIX_CEIL), font=F(13), fill=C("dust"))
    return im

if __name__ == "__main__":
    BL = measure()
    n = 0
    for k in CUES:
        if CUES[k]["parts"]:
            with open("mockups/cues/%s.wav" % k, "wb") as fh:
                fh.write(wav(BUF[k]))
            n += 1
    print("wrote %d cue files to mockups/cues/" % n)
    im = sheet()
    with open("mockups/sound.png", "wb") as fh:
        buf = io.BytesIO()
        im.save(buf, "PNG")
        fh.write(buf.getvalue())
    print("wrote mockups/sound.png (%dx%d)" % (im.width, im.height))
    report(BL)
    wiring_report()
