"""Blind grading of lab games: a numbered list in shuffled order, each game playable in a frame with
a 1-10 grade and a note. Arms and runs live in key.json and are never shown; grades go to
grades.json, keyed by the same tokens.

    venv/bin/python labs/grade/serve_grade.py [--port 9100]
"""

import argparse
import html
import json
import mimetypes
import random
import secrets
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HERE = Path(__file__).resolve().parent
RUNS = Path("/var/lib/gamesummoner/output/runs")
MANIFEST, KEY, GRADES = HERE / "manifest.json", HERE / "key.json", HERE / "grades.json"


def _load(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def _key() -> dict:
    """token -> manifest entry; new manifest entries get new tokens, old tokens keep their place."""
    key = _load(KEY, {})
    known = {e["run"] for e in key.values()}
    fresh = [e for e in _load(MANIFEST, []) if e["run"] not in known]
    random.shuffle(fresh)
    for entry in fresh:
        key[secrets.token_hex(4)] = {**entry, "order": len(key) + 1}
    KEY.write_text(json.dumps(key, indent=1))
    return key


PAGE = """<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>{title}</title><style>
body{{font:15px system-ui;margin:0;background:#16181d;color:#e8e8e8}}a{{color:#8fc7ff}}
main{{max-width:1320px;margin:0 auto;padding:16px}}table{{border-collapse:collapse}}
td{{padding:6px 14px;border-bottom:1px solid #333}}iframe{{width:1280px;height:720px;border:0;background:#000}}
form{{margin:12px 0;display:flex;gap:10px;align-items:center;flex-wrap:wrap}}
input[type=number]{{width:4em}}textarea{{width:640px;height:3.5em}}button{{padding:6px 16px}}
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
        key, grades = self.server.key, _load(GRADES, {})
        path = unquote(urlparse(self.path).path)
        if path == "/":
            rows = "".join(
                f"<tr><td><a href='/play/{t}'>Game {e['order']:02d}</a></td>"
                f"<td>{grades[t]['score'] if t in grades else ''}</td></tr>"
                for t, e in sorted(key.items(), key=lambda kv: kv[1]["order"]))
            done = sum(t in grades for t in key)
            return self._page("Grade games", f"<h1>Grade games</h1><p>{done} of {len(key)} graded.</p>"
                                             f"<table><tr><td>Game</td><td>Grade</td></tr>{rows}</table>")
        if path.startswith("/play/"):
            token = path.split("/")[2]
            if token not in key:
                return self._send(404, b"no such game")
            g = grades.get(token, {})
            order = key[token]["order"]
            return self._page(f"Game {order:02d}", (
                f"<p><a href='/'>All games</a></p><h1>Game {order:02d}</h1>"
                f"<iframe src='/g/{token}/index.html' allow='autoplay; fullscreen'></iframe>"
                f"<form method='post' action='/grade/{token}'>Grade (1-10) "
                f"<input type='number' name='score' min='1' max='10' required value='{g.get('score', '')}'>"
                f"<textarea name='note' placeholder='Note (optional)'>{html.escape(g.get('note', ''))}</textarea>"
                f"<button>Save</button></form>"))
        if path.startswith("/g/"):
            parts = path.split("/", 3)
            token, rest = parts[2], (parts[3] if len(parts) > 3 else "index.html")
            if token not in key:
                return self._send(404, b"no such game")
            root = (RUNS / key[token]["run"] / "game").resolve()
            file = (root / rest).resolve()
            if not file.is_relative_to(root) or not file.is_file():
                return self._send(404, b"not found")
            return self._send(200, file.read_bytes(), mimetypes.guess_type(file.name)[0] or "application/octet-stream")
        self._send(404, b"not found")

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        token = path.split("/")[2] if path.startswith("/grade/") else None
        if token not in self.server.key:
            return self._send(404, b"no such game")
        form = parse_qs(self.rfile.read(int(self.headers.get("Content-Length", 0))).decode())
        score = int((form.get("score") or ["0"])[0])
        if not 1 <= score <= 10:
            return self._send(400, b"grade must be 1-10")
        grades = _load(GRADES, {})
        grades[token] = {"score": score, "note": (form.get("note") or [""])[0], "at": time.strftime("%Y-%m-%dT%H:%M:%S")}
        GRADES.write_text(json.dumps(grades, indent=1))
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, *args) -> None:
        pass


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=9100)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    server.key = _key()
    print(f"grading {len(server.key)} games on http://127.0.0.1:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
