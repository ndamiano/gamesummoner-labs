"""Render the 'later' card: a clock counting up to the real prompt-to-game time, the stage it is in, then the total."""
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 960, 640, 30
BG, INK, DIM, ACCENT = (10, 12, 20), (238, 230, 214), (140, 136, 128), (232, 112, 58)
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def clock(s):
    s = int(s)
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60}:{s % 60:02d}"


def main():
    out, stages = sys.argv[1], [(name, float(sec)) for name, sec in (a.split("=") for a in sys.argv[2:])]
    total = sum(sec for _, sec in stages)
    head, big, small = ImageFont.truetype(SERIF, 30), ImageFont.truetype(MONO, 96), ImageFont.truetype(SERIF, 26)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                           "-r", str(FPS), "-i", "-", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", out],
                          stdin=subprocess.PIPE)
    count, hold = int(2.0 * FPS), int(1.8 * FPS)
    for i in range(count + hold):
        p = min(1.0, i / count)
        t = total * (1 - (1 - p) ** 2)
        img = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(img)
        d.text((W / 2, 200), "A little bit later…", font=head, fill=INK, anchor="mm")
        d.text((W / 2, 320), clock(t), font=big, fill=INK if p < 1 else ACCENT, anchor="mm")
        if p < 1:
            acc = 0
            for name, sec in stages:
                if t < acc + sec:
                    break
                acc += sec
            d.text((W / 2, 430), name, font=small, fill=DIM, anchor="mm")
        else:
            m, s = divmod(int(round(total)), 60)
            d.text((W / 2, 430), f"From prompt to playable in {m} min {s} s", font=small, fill=INK, anchor="mm")
        ff.stdin.write(img.tobytes())
    ff.stdin.close()
    ff.wait()


if __name__ == "__main__":
    main()
