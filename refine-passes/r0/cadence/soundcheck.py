"""Render the whole sound table to WAVs and print the mix budget.

15.9 says the sound asset is the parameter table, not recordings - so this is
the check that the asset exists: every source in the table is rendered through
each tier treatment, every verb motif is rendered, and the loudness budget of
15.6 is printed out so it can be read against the design.

    python3 -m cadence.soundcheck            # writes out/sound/*.wav
"""
import os

from .audio import SR, TABLE, MOTIF, BUS_LEVEL, Synth, TIER_TREAT
from .sound import write_wav

OUT = "out/sound"


def rms(samples):
    if not samples:
        return 0.0
    return (sum(v * v for v in samples) / len(samples)) ** 0.5


def peak(samples):
    return max((abs(v) for v in samples), default=0.0)


def main():
    os.makedirs(OUT, exist_ok=True)
    s = Synth(seed=7)
    print("%-10s %-8s %8s %8s  %s" % ("source", "tier", "ms", "peak", "family/bus"))
    for src in TABLE:
        for tier in ("careful", "normal", "frantic"):
            if src == "tick" and tier != "normal":
                continue
            buf = s.cue(src, tier)
            write_wav(os.path.join(OUT, "%s_%s.wav" % (src, tier)), buf)
            print("%-10s %-8s %8d %8.3f  %s/%s" %
                  (src, tier, int(len(buf) / SR * 1000), peak(buf),
                   TABLE[src]["family"], TABLE[src]["bus"]))
    print()
    print("verb motifs (grains = the number of things the verb does):")
    for verb, grains in MOTIF.items():
        for tier in ("careful", "normal", "frantic"):
            buf = s.verb_cue(verb, tier, gaps=[300, 320])
            write_wav(os.path.join(OUT, "verb_%s_%s.wav" % (verb.lower(), tier)), buf)
        print("  %-7s %d grains  %s" % (verb, len(grains),
                                        " ".join("%s@%s" % g for g in grains)))
    print()
    print("loudness budget (15.6):")
    for bus, lvl in sorted(BUS_LEVEL.items(), key=lambda kv: -kv[1]):
        print("  %-8s %.2f" % (bus, lvl))
    print()
    print("tier treatments (15.5):")
    for tier, tr in TIER_TREAT.items():
        print("  %-8s gain %.2f  attack +%d ms  tail x%.1f  pitch %+.0f semitones  lp %s" %
              (tier, tr["gain"], tr["atk_add"], tr["tail"], tr["semis"], tr["lp"] or "-"))
    print()
    print("wrote %d files to %s" % (len(os.listdir(OUT)), OUT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
