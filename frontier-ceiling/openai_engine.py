"""OpenAI-chat pass-through to a hosted OpenAI-compatible API, with auth, model and effort mapping.

Sits where SGLang or basalt would, behind the stock llm contract server. The canonical request
already is the API's shape, so the engine renames the model, maps the harness's effort onto the
levels the API accepts, adds the key, and costs every call into a ledger (peak hours doubled),
refusing work once --budget-usd is spent.
"""

import argparse
import json
import logging
import threading
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

logger = logging.getLogger("openai_engine")

HERE = Path(__file__).resolve().parent
PRICES = {"deepseek-flash": {"hit": 0.003, "miss": 0.15, "out": 0.60, "peak": True},
          "gemini-4-argon": {"hit": 0.20, "miss": 2.00, "out": 10.00, "peak": False}}
EFFORT = {"none": "low", "minimal": "low", "low": "low", "medium": "high", "high": "high",
          "xhigh": "high", "max": "max"}


def peak(now: datetime) -> bool:
    return now.weekday() < 5 and (1 <= now.hour < 4 or 6 <= now.hour < 10)


def cost(model: str, usage: dict, when: datetime) -> float:
    p = PRICES[model]
    prompt = usage.get("prompt_tokens", 0)
    hit = usage.get("prompt_cache_hit_tokens",
                    (usage.get("prompt_tokens_details") or {}).get("cached_tokens") or 0)
    miss = usage.get("prompt_cache_miss_tokens", prompt - hit)
    out = max(usage.get("completion_tokens", 0), usage.get("total_tokens", 0) - prompt)
    usd = (hit * p["hit"] + miss * p["miss"] + out * p["out"]) / 1e6
    return usd * (2 if p["peak"] and peak(when) else 1)


class Engine:
    def __init__(self, args):
        self.url = args.base_url.rstrip("/") + "/chat/completions"
        self.key = Path(args.key_file).expanduser().read_text().strip()
        self.model = args.model
        self.alias = args.alias
        self.ledger = HERE / args.ledger
        self.budget = args.budget_usd
        self.lock = threading.Lock()
        self.spent = sum(json.loads(l)["usd"] for l in self.ledger.open()) if self.ledger.exists() else 0.0

    def complete(self, body: dict) -> tuple[int, dict]:
        if self.spent >= self.budget:
            return 402, {"error": {"message": f"budget spent: ${self.spent:.3f}"}}
        effort = body.pop("reasoning_effort", None) or body.pop("reasoning", None)
        body = {**body, "model": self.model}
        if effort in EFFORT:
            body["reasoning_effort"] = EFFORT[effort] if self.model.startswith("deepseek") \
                else {"xhigh": "high", "max": "high", "none": "low", "minimal": "low"}.get(effort, effort)
        started = time.time()
        req = urllib.request.Request(self.url, data=json.dumps(body).encode(), method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": f"Bearer {self.key}"})
        try:
            with urllib.request.urlopen(req, timeout=1700) as r:
                out = json.load(r)
        except urllib.error.HTTPError as e:
            text = e.read().decode(errors="replace")[:2000]
            logger.error("api %s: %s", e.code, text)
            return (400 if e.code == 400 else 502), {"error": {"message": f"Status {e.code}: {text}"}}
        except (OSError, ValueError) as e:
            logger.error("api unreachable: %s", e)
            return 502, {"error": {"message": f"api unreachable: {e}"}}
        self.record(out, body, time.time() - started)
        out["model"] = self.alias
        return 200, out

    def record(self, out: dict, body: dict, seconds: float) -> None:
        usage = out.get("usage") or {}
        when = datetime.now(timezone.utc)
        usd = cost(self.model, usage, when)
        msg = (out.get("choices") or [{}])[0].get("message") or {}
        row = {"id": uuid.uuid4().hex[:12], "t": round(time.time(), 1), "seconds": round(seconds, 1),
               "model": self.model, "peak": PRICES[self.model]["peak"] and peak(when), "effort": body.get("reasoning_effort"),
               "finish": (out.get("choices") or [{}])[0].get("finish_reason"),
               "msgs": len(body.get("messages", [])), "hit": usage.get("prompt_cache_hit_tokens"),
               "miss": usage.get("prompt_cache_miss_tokens"), "out": usage.get("completion_tokens"),
               "total": usage.get("total_tokens"), "prompt": usage.get("prompt_tokens"),
               "reasoning": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
               "text_chars": len(msg.get("content") or ""), "usd": round(usd, 5)}
        with self.lock:
            self.spent += usd
            row["spent_total"] = round(self.spent, 5)
            with self.ledger.open("a") as f:
                f.write(json.dumps(row) + "\n")
        logger.info("call %s %s %.0fs hit=%s miss=%s out=%s reasoning=%s $%.4f total $%.3f%s",
                    row["id"], row["finish"], seconds, row["hit"], row["miss"], row["out"],
                    row["reasoning"], usd, self.spent, " PEAK" if row["peak"] else "")


def make_handler(engine: Engine):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _send(self, status: int, body: dict) -> None:
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/v1/models":
                self._send(200, {"object": "list", "data": [{"id": engine.alias, "object": "model"}]})
            else:
                self._send(404, {"error": {"message": f"no route {self.path}"}})

        def do_POST(self):
            if self.path != "/v1/chat/completions":
                self._send(404, {"error": {"message": f"no route {self.path}"}})
                return
            length = int(self.headers.get("Content-Length") or 0)
            status, out = engine.complete(json.loads(self.rfile.read(length) or b"{}"))
            self._send(status, out)

        def log_message(self, fmt, *args):
            pass

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="https://api.deepseek.com")
    parser.add_argument("--model", default="deepseek-flash", choices=sorted(PRICES))
    parser.add_argument("--alias", required=True, help="the model id the control plane asks for")
    parser.add_argument("--key-file", default="~/api_keys/deepseek-api.key")
    parser.add_argument("--budget-usd", type=float, required=True)
    parser.add_argument("--ledger", default="deepseek_calls.jsonl")
    parser.add_argument("--port", type=int, default=8091)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    engine = Engine(args)
    logger.info("serving %s as %s on :%d, spent $%.3f of $%.2f", args.model, args.alias, args.port,
                engine.spent, args.budget_usd)
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(engine)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
