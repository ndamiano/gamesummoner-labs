"""Route each llm request to a backend engine by its game's ask, so several models share one queue.

The queue hands any llm job to any worker, so per-game models are chosen here instead: the first
user message of every design and build call carries the ask, and the first rule in routes.json
whose `ask` substring it contains (case-sensitive, rules re-read when the file changes) (and whose `tools` flag, if set, matches whether the request
has tools) names the backend URL. A request no rule matches is refused rather than guessed.
"""

import argparse
import json
import logging
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

logger = logging.getLogger("router_engine")


def first_user_text(body: dict) -> str:
    for m in body.get("messages", []):
        if m.get("role") == "user":
            c = m.get("content")
            return c if isinstance(c, str) else " ".join(p.get("text", "") for p in c or [])
    return ""


def route(rules: list, body: dict):
    text = first_user_text(body)
    has_tools = bool(body.get("tools"))
    for rule in rules:
        if rule["ask"] in text and rule.get("tools", has_tools) == has_tools:
            return rule
    return None


class Routes:
    def __init__(self, path: Path):
        self.path = path
        self.mtime = 0.0
        self.rules: list = []
        self.load()

    def load(self) -> list:
        mtime = self.path.stat().st_mtime
        if mtime != self.mtime:
            self.rules = json.loads(self.path.read_text())
            self.mtime = mtime
            for r in self.rules:
                logger.info("route %s: ask %r tools=%s -> %s", r["name"], r["ask"],
                            r.get("tools", "any"), r["backend"])
        return self.rules


def make_handler(routes: Routes, alias: str):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _send(self, status: int, data: bytes) -> None:
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/v1/models":
                self._send(200, json.dumps({"object": "list",
                                            "data": [{"id": alias, "object": "model"}]}).encode())
            else:
                self._send(404, b'{"error": {"message": "no route"}}')

        def do_POST(self):
            if self.path != "/v1/chat/completions":
                self._send(404, b'{"error": {"message": "no route"}}')
                return
            raw = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            body = json.loads(raw or b"{}")
            rule = route(routes.load(), body)
            if rule is None:
                logger.error("no route for ask %r", first_user_text(body)[:120])
                self._send(502, b'{"error": {"message": "no route for this ask"}}')
                return
            logger.info("%s -> %s", rule["name"], rule["backend"])
            req = urllib.request.Request(rule["backend"].rstrip("/") + "/v1/chat/completions",
                                         data=raw, method="POST",
                                         headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=1750) as r:
                    self._send(r.status, r.read())
            except urllib.error.HTTPError as e:
                self._send(e.code, e.read())
            except OSError as e:
                self._send(502, json.dumps({"error": {"message": f"backend down: {e}"}}).encode())

        def log_message(self, fmt, *args):
            pass

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--routes", required=True, help="JSON list of {name, ask, backend, tools?}")
    parser.add_argument("--alias", required=True, help="the model id the control plane asks for")
    parser.add_argument("--port", type=int, default=8091)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    ThreadingHTTPServer(("127.0.0.1", args.port),
                        make_handler(Routes(Path(args.routes)), args.alias)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
