"""Before and after of each vision-ux loop, named and side by side: the build the UX rounds started
from and the build they ended on.

    venv/bin/python labs/grade/serve_pairs.py [--port 9101]
"""

import argparse
import html
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

RUNS = Path("/var/lib/gamesummoner/output/runs")
PAIRS = [
    ("cat (ux-cat-paired, 3 rounds kept)", "49faeca8b1f1", "9afc08d0940e"),
    ("skatemall (pv2, 2 rounds kept)", "ff2340f0be3a", "22bb93190cea"),
    ("dungeon", "4f9345ab2787", "c105c9dcfb9a"),
    ("turtlecity", "287bd67059f5", "806b477ffbf9"),
    ("timeloop", "5f691020d0fa", "411a86a2d054"),
    ("penguin3", "e5a661b16f28", "759994e44c22"),
    ("farm3", "3f28dc497d54", "33cb8b33fc46"),
    ("catdefense3", "0861810a6846", "9fdb9b39f73b"),
]
SHOWN = {rid for _, *rids in PAIRS for rid in rids}

PAGE = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{title}</title><style>
body{{font:15px system-ui;margin:0;background:#16181d;color:#e8e8e8}}a{{color:#8fc7ff}}
main{{padding:16px}}td{{padding:6px 14px;border-bottom:1px solid #333}}
.two{{display:flex;gap:12px;flex-wrap:wrap}}iframe{{width:960px;height:540px;border:0;background:#000}}
</style><main>{body}</main>"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: bytes, ctype: str = "text/html; charset=utf-8") -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _page(self, title: str, body: str) -> None:
        self._send(200, PAGE.format(title=html.escape(title), body=body).encode())

    def do_GET(self) -> None:
        path = unquote(urlparse(self.path).path)
        if path == "/":
            rows = "".join(
                f"<tr><td><a href='/pair/{n}'>{html.escape(name)}</a></td>"
                f"<td><a href='/g/{before}/index.html'>before {before}</a></td>"
                f"<td><a href='/g/{after}/index.html'>after {after}</a></td></tr>"
                for n, (name, before, after) in enumerate(PAIRS))
            return self._page("UX pairs", f"<h1>UX before and after</h1><table>{rows}</table>")
        if path.startswith("/pair/"):
            name, before, after = PAIRS[int(path.split("/")[2])]
            return self._page(name, (
                f"<p><a href='/'>All pairs</a></p><h1>{html.escape(name)}</h1><div class='two'>"
                f"<div><h2>Before {before}</h2><iframe src='/g/{before}/index.html'></iframe></div>"
                f"<div><h2>After {after}</h2><iframe src='/g/{after}/index.html'></iframe></div></div>"))
        if path.startswith("/g/"):
            parts = path.split("/", 3)
            rid, rest = parts[2], (parts[3] if len(parts) > 3 else "index.html")
            if rid not in SHOWN:
                return self._send(404, b"no such game")
            root = (RUNS / rid / "game").resolve()
            file = (root / rest).resolve()
            if not file.is_relative_to(root) or not file.is_file():
                return self._send(404, b"not found")
            return self._send(200, file.read_bytes(), mimetypes.guess_type(file.name)[0] or "application/octet-stream")
        self._send(404, b"not found")

    def log_message(self, *args) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9101)
    args = parser.parse_args()
    ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()


if __name__ == "__main__":
    main()
