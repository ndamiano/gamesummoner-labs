"""JEV-style POST /v1/decide (kind, state, question, options) served by a Decision 3.0 model's system_one.

usage: shim.py MODEL_DIR PORT
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from transformers import AutoModel

MODEL = AutoModel.from_pretrained(sys.argv[1], trust_remote_code=True, device_map="cuda:0")
LOCK = threading.Lock()


def decide(req):
    state = req.get("state", "")
    if not isinstance(state, str):
        state = json.dumps(state, ensure_ascii=False)
    if req["kind"] == "noul":
        q = {"q": {"type": "noul", "instructions": req["question"]}}
    else:
        q = {"q": {"type": "choice", "instructions": req["question"], "criteria": {o: None for o in req["options"]}}}
    t = time.time()
    with LOCK:
        a = MODEL.system_one(state=state, questions=q)["answers"]["q"]
    if req["kind"] == "noul":
        opts, probs = ["false", "true"], [1 - a["noul"], a["noul"]]
    else:
        opts = req["options"]
        probs = [a["probabilities"][o] for o in opts]
    best = max(range(len(opts)), key=lambda i: probs[i])
    return {"kind": req["kind"], "options": opts, "probabilities": probs, "choice_index": best, "choice": opts[best],
            "elapsed_seconds": round(time.time() - t, 3)}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def reply(self, code, body):
        raw = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        self.reply(200, {"status": "ok"})

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.reply(200, decide(req))


ThreadingHTTPServer(("127.0.0.1", int(sys.argv[2])), H).serve_forever()
