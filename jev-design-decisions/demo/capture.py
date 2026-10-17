"""Record a Playwright page losslessly: CDP screencast PNG frames with their timestamps, encoded to a 30 fps mp4."""
import base64
import shutil
import subprocess
import time
from pathlib import Path


class Capture:
    def __init__(self, page, out):
        self.page, self.out, self.frames = page, Path(out), []
        self.dir = self.out.parent / (self.out.stem + "_frames")
        shutil.rmtree(self.dir, ignore_errors=True)
        self.dir.mkdir()
        self.cdp = page.context.new_cdp_session(page)
        self.cdp.on("Page.screencastFrame", self._frame)

    def _frame(self, f):
        path = self.dir / f"{len(self.frames):06d}.png"
        path.write_bytes(base64.b64decode(f["data"]))
        self.frames.append((f["metadata"]["timestamp"], path))
        self.cdp.send("Page.screencastFrameAck", {"sessionId": f["sessionId"]})

    def start(self):
        self.cdp.send("Page.startScreencast", {"format": "png", "everyNthFrame": 1})

    def stop(self):
        self.page.wait_for_timeout(200)
        end = time.time()
        self.cdp.send("Page.stopScreencast")
        lines = []
        for (t, path), (nxt, _) in zip(self.frames, self.frames[1:] + [(end, None)]):
            lines += [f"file '{path.name}'", f"duration {max(nxt - t, 0.001):.4f}"]
        lines.append(f"file '{self.frames[-1][1].name}'")
        (self.dir / "list.txt").write_text("\n".join(lines) + "\n")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(self.dir / "list.txt"),
                        "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "10", "-preset", "slow",
                        str(self.out)], check=True)
        shutil.rmtree(self.dir)
        return len(self.frames)
