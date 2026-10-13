"""Sound front-end: plays the synthesised cues, and maps game events to them.

The synthesiser (audio.py) is pure maths and can be rendered to a WAV with no
window at all - ``python3 -m cadence.soundcheck`` does exactly that, which is
how the sound design gets checked on a machine with no audio device.  Here we
look for an output device; if there is none the game still runs and says so
rather than pretending to make noise (15.9: the asset is the parameter table,
this is only its renderer).
"""
import os
import struct
import subprocess

from .audio import SR, TABLE, Synth


def pcm(samples):
    return b"".join(struct.pack("<h", int(max(-32767, min(32767, round(v * 32767)))))
                    for v in samples)


def write_wav(path, samples, sr=SR):
    data = pcm(samples)
    hdr = (b"RIFF" + struct.pack("<I", 36 + len(data)) + b"WAVEfmt " +
           struct.pack("<IHHIIHH", 16, 1, 1, sr, sr * 2, 2, 16) + b"data" +
           struct.pack("<I", len(data)))
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(hdr + data)
    return path


PLAYERS = [
    ["aplay", "-q", "-t", "raw", "-r", str(SR), "-c", "1", "-f", "S16_LE"],
    ["paplay", "--raw-format=S16_LE", "--channels=1", "--rate=%d" % SR, "--format=raw"],
]


class Sound:
    def __init__(self, settings, find_backend=True):
        self.settings = settings
        self.synth = Synth(quiet=settings.quiet)
        self.proc = None
        self.backend = None
        self.notice = None
        if settings.audio and find_backend:
            self._find_backend()
            if not self.backend:
                self.notice = "no audio device - cues are still synthesised, not played"

    def _find_backend(self):
        for cmd in PLAYERS:
            for p in os.environ.get("PATH", "").split(os.pathsep):
                if p and os.path.exists(os.path.join(p, cmd[0])):
                    try:
                        self.proc = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                                                     stdout=subprocess.DEVNULL,
                                                     stderr=subprocess.DEVNULL)
                        self.backend = cmd[0]
                        return
                    except OSError:
                        break

    # ---------------------------------------------------------------- play --
    def play(self, samples):
        if not self.settings.audio or not self.proc or self.proc.poll() is not None:
            return
        try:
            self.proc.stdin.write(pcm(samples))
            self.proc.stdin.flush()
        except Exception:
            self.backend = None

    def cue(self, source, tier="normal", **kw):
        if source in TABLE:
            self.play(self.synth.cue(source, tier, gains=self.settings.volume, **kw))

    def verb(self, verb, tier, gaps=()):
        self.play(self.synth.verb_cue(verb, tier, gaps, gains=self.settings.volume))

    def pulse(self):
        """15.4: a 60 bpm reference tick for players who want their rate
        audibly calibrated.  Off by default in Calm mode."""
        self.cue("pulse", "normal")

    def grammar(self):
        """15.6: the grammar sting is the loudest thing in the game and it is
        always alone - the room is silent for its 600 ms."""
        self.play(self.synth.cue("grammar", "normal", gains=self.settings.volume))

    # -------------------------------------------------------------- mapping --
    def handle(self, events):
        """game events -> the diegetic cue of 15.2 (never a UI sound)."""
        for e in events:
            t = e["type"]
            if t == "verb":
                self.verb(e["verb"], e["tier"], e.get("gaps", []))
            elif t in ("open", "switch", "stairs"):
                self.cue("door", "normal")
            elif t == "player_hit":
                self.cue("hurt", "normal")
            elif t == "beat":
                self.cue("beat", "normal")
            elif t == "relic":
                self.grammar()
            elif t == "enter_room":
                self.cue("roomtone", "normal", dur_ms=1400)
            elif t == "rest":
                self.cue("page", "normal")
            elif t == "death":
                self.play(self.synth.cue("roomtone", "careful", dur_ms=1200))

    def stop(self):
        if self.proc:
            try:
                self.proc.stdin.close()
                self.proc.terminate()
            except Exception:
                pass
