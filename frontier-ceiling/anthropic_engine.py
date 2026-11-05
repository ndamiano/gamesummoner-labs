"""OpenAI-chat-shaped engine that serves each request from the Anthropic Messages API.

Sits where SGLang or basalt would, behind the stock llm contract server. Thinking blocks never
reach the canonical history, so they are kept here by assistant turn and replayed verbatim; any
history edit the harness makes degrades to dropped thinking (drop_block) instead of a 400. Every
call is costed into calls.jsonl, and the engine refuses work once --budget-usd is spent.
"""

import argparse
import base64
import hashlib
import json
import logging
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import anthropic

logger = logging.getLogger("anthropic_engine")

HERE = Path(__file__).resolve().parent
PRICES = {
    "claude-opus-5-5": {"in": 4.00, "out": 20.00, "read": 0.20, "write": 5.00},
    "claude-sonnet-5-5": {"in": 2.00, "out": 10.00, "read": 0.20, "write": 2.50},
}
BETAS = ["thinking-binding-controls-2026-08-01", "server-side-fallback-2026-07-01"]
EFFORTS = {"low", "medium", "high", "xhigh", "max"}
AGENTIC_TURNS = 40
AGENTIC_TURN_TOKENS = 32000
AGENTIC_SECONDS = 1500
WRITE_TOOLS = [
    {"name": "write_section",
     "description": "Save one top-level section of the design spec. Calling it again with the same "
                    "heading replaces that section.",
     "input_schema": {"type": "object", "additionalProperties": False, "required": ["markdown"],
                      "properties": {"markdown": {
                          "type": "string",
                          "description": "The whole section as markdown, starting with its heading "
                                         "line exactly as the spec layout names it."}}}},
    {"name": "done",
     "description": "Hand the finished spec to the builder. Call once every section is saved.",
     "input_schema": {"type": "object", "additionalProperties": False, "properties": {}}},
]
FINISH = {"tool_use": "tool_calls", "end_turn": "stop", "stop_sequence": "stop",
          "max_tokens": "length", "refusal": "stop", "pause_turn": "stop"}


class Ledger:
    def __init__(self, path: Path, budget: float):
        self.path = path
        self.budget = budget
        self.lock = threading.Lock()
        self.spent = sum(json.loads(line)["usd"] for line in path.open()) if path.exists() else 0.0

    def over(self) -> bool:
        return self.spent >= self.budget

    def record(self, row: dict) -> None:
        with self.lock:
            self.spent += row["usd"]
            row["spent_total"] = round(self.spent, 4)
            with self.path.open("a") as f:
                f.write(json.dumps(row) + "\n")


class ThinkingStore:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()
        self.blocks = json.loads(path.read_text()) if path.exists() else {}

    def get(self, key: str) -> list:
        return self.blocks.get(key, [])

    def put(self, key: str, blocks: list) -> None:
        if not blocks:
            return
        with self.lock:
            self.blocks[key] = blocks
            self.path.write_text(json.dumps(self.blocks))


def turn_key(text: str, tool_ids: list) -> str:
    if tool_ids:
        return tool_ids[0]
    return "text:" + hashlib.sha256(text.encode()).hexdigest()


def text_of(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") for p in content if p.get("type") == "text")


def user_blocks(content) -> list:
    if isinstance(content, str):
        return [{"type": "text", "text": content}] if content else []
    out = []
    for part in content or []:
        if part.get("type") == "text" and part.get("text"):
            out.append({"type": "text", "text": part["text"]})
        elif part.get("type") == "image_url":
            url = part["image_url"]["url"]
            if url.startswith("data:"):
                head, data = url.split(",", 1)
                media = head[5:].split(";")[0]
                out.append({"type": "image",
                            "source": {"type": "base64", "media_type": media, "data": data}})
            else:
                out.append({"type": "image", "source": {"type": "url", "url": url}})
    return out


def to_anthropic(body: dict, store: ThinkingStore) -> tuple[list, list]:
    system, messages = [], []
    leading = True
    for m in body.get("messages", []):
        role = m.get("role")
        if role == "system":
            text = text_of(m.get("content"))
            if leading:
                system.append({"type": "text", "text": text})
            else:
                messages.append({"role": "system", "content": text})
            continue
        leading = False
        if role == "user":
            messages.append({"role": "user", "content": user_blocks(m.get("content"))})
        elif role == "assistant":
            text = text_of(m.get("content"))
            calls = m.get("tool_calls") or []
            blocks = list(store.get(turn_key(text, [c["id"] for c in calls])))
            if text:
                blocks.append({"type": "text", "text": text})
            for c in calls:
                args = c["function"].get("arguments") or "{}"
                try:
                    parsed = json.loads(args)
                except json.JSONDecodeError:
                    parsed = {"_unparsed_arguments": args}
                blocks.append({"type": "tool_use", "id": c["id"], "name": c["function"]["name"],
                               "input": parsed if isinstance(parsed, dict) else {"value": parsed}})
            messages.append({"role": "assistant", "content": blocks or [{"type": "text", "text": "."}]})
        elif role == "tool":
            result = {"type": "tool_result", "tool_use_id": m["tool_call_id"],
                      "content": user_blocks(m.get("content")) or [{"type": "text", "text": "(empty)"}]}
            prev = messages[-1] if messages else None
            if prev and prev["role"] == "user" and prev["content"] and \
                    all(b.get("type") == "tool_result" for b in prev["content"]):
                prev["content"].append(result)
            else:
                messages.append({"role": "user", "content": [result]})
    return system, messages


def to_tools(body: dict) -> list:
    tools = []
    for t in body.get("tools") or []:
        fn = t.get("function", t)
        tools.append({"name": fn["name"], "description": fn.get("description", ""),
                      "input_schema": fn.get("parameters") or {"type": "object", "properties": {}}})
    return tools


def cost(model: str, usage) -> float:
    p = PRICES.get(model, PRICES["claude-opus-5-5"])
    return (usage.input_tokens * p["in"] + usage.output_tokens * p["out"]
            + (usage.cache_read_input_tokens or 0) * p["read"]
            + (usage.cache_creation_input_tokens or 0) * p["write"]) / 1e6


class EngineError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def prompt_tokens(usage) -> int:
    return usage.input_tokens + (usage.cache_read_input_tokens or 0) \
        + (usage.cache_creation_input_tokens or 0)


def chat_response(call_id: str, alias: str, message: dict, finish: str, prompt: int,
                  completion: int) -> dict:
    return {
        "id": f"chatcmpl-{call_id}", "object": "chat.completion", "created": int(time.time()),
        "model": alias,
        "choices": [{"index": 0, "message": message, "finish_reason": finish}],
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": prompt + completion},
    }


class Engine:
    def __init__(self, args):
        self.client = anthropic.Anthropic(api_key=Path(args.key_file).expanduser().read_text().strip(),
                                          max_retries=4)
        self.model = args.model
        self.alias = args.alias
        self.max_tokens = args.max_tokens
        self.toolless_effort = args.toolless_effort
        self.toolless_note = Path(args.toolless_note).read_text().strip() if args.toolless_note else ""
        self.agentic_note = Path(args.agentic_write).read_text().strip() if args.agentic_write else ""
        self.write_budget = args.write_budget
        self.turn_budget = args.turn_budget
        self.ledger = Ledger(HERE / args.ledger, args.budget_usd)
        self.store = ThinkingStore(HERE / args.thinking_store)

    def complete(self, body: dict) -> tuple[int, dict]:
        if self.ledger.over():
            return 402, {"error": {"message": f"budget spent: ${self.ledger.spent:.2f}"}}
        system, messages = to_anthropic(body, self.store)
        effort = body.get("reasoning_effort") or body.get("reasoning")
        effort = effort if effort in EFFORTS else "high"
        request = {
            "model": self.model,
            "max_tokens": min(int(body.get("max_tokens") or self.max_tokens), self.max_tokens),
            "system": system,
            "messages": messages,
            "thinking": {"type": "adaptive", "display": "summarized",
                         "block_binding": {"prefix_mismatch_behavior": "drop_block"}},
            "output_config": {"effort": effort},
            "cache_control": {"type": "ephemeral"},
            "betas": BETAS,
            "extra_body": {"fallbacks": "default"},
        }
        tools = to_tools(body)
        if tools:
            request["tools"] = tools
            if self.turn_budget:
                request["output_config"] = {**request["output_config"],
                                            "task_budget": {"type": "tokens", "total": self.turn_budget}}
                request["betas"] = request["betas"] + ["task-budgets-2026-03-13"]
        else:
            if self.toolless_effort:
                request["output_config"] = {"effort": self.toolless_effort}
            if self.toolless_note:
                request["messages"] = messages + [{"role": "system", "content": self.toolless_note}]
            first = (body.get("messages") or [{}])[0]
            designing = first.get("role") == "system" and \
                str(first.get("content") or "").startswith("You design browser games.")
            if self.agentic_note and designing:
                return self.agentic_write(request)
        try:
            msg, seconds = self.stream_call(request)
        except EngineError as e:
            return e.status, {"error": {"message": e.message}}
        return 200, self.respond(msg, request, seconds)

    def stream_call(self, request: dict):
        started = time.time()
        try:
            with self.client.beta.messages.stream(**request) as stream:
                self.watch(stream, started)
                msg = stream.get_final_message()
        except anthropic.BadRequestError as e:
            logger.error("400: %s", e.message)
            raise EngineError(400, e.message)
        except anthropic.APIStatusError as e:
            logger.error("api %s: %s", e.status_code, e.message)
            raise EngineError(502, e.message)
        except anthropic.APIConnectionError as e:
            raise EngineError(502, f"connection: {e}")
        return msg, time.time() - started

    def watch(self, stream, started: float) -> None:
        sizes = {"thinking": 0, "text": 0, "tool": 0}
        last = started
        for event in stream:
            if event.type != "content_block_delta":
                continue
            delta = event.delta
            if delta.type == "thinking_delta":
                sizes["thinking"] += len(delta.thinking)
            elif delta.type == "text_delta":
                sizes["text"] += len(delta.text)
            elif delta.type == "input_json_delta":
                sizes["tool"] += len(delta.partial_json)
            now = time.time()
            if now - last >= 30:
                logger.info("streaming %.0fs: thinking %d chars, text %d, tool input %d",
                            now - started, sizes["thinking"], sizes["text"], sizes["tool"])
                last = now

    def record(self, msg, request: dict, seconds: float, tag: str = "") -> str:
        text = "".join(b.text for b in msg.content if b.type == "text")
        thinking = [b for b in msg.content if b.type in ("thinking", "redacted_thinking")]
        drops = [t for t in (getattr(msg, "input_transformations", None) or [])
                 if getattr(t, "type", None) == "thinking_dropped"]
        usage = msg.usage
        usd = cost(msg.model, usage)
        call_id = uuid.uuid4().hex[:12]
        self.ledger.record({
            "id": call_id, "t": round(time.time(), 1), "seconds": round(seconds, 1), "tag": tag,
            "model": msg.model, "stop": msg.stop_reason, "msgs": len(request["messages"]),
            "in": usage.input_tokens, "read": usage.cache_read_input_tokens,
            "write": usage.cache_creation_input_tokens, "out": usage.output_tokens,
            "thinking_dropped": len(drops),
            "thinking_chars": sum(len(getattr(b, "thinking", "") or "") for b in thinking),
            "text_chars": len(text), "usd": round(usd, 4)})
        logger.info("call %s%s %s %.0fs in=%d read=%s write=%s out=%d $%.3f total $%.2f%s",
                    call_id, f" [{tag}]" if tag else "", msg.stop_reason, seconds,
                    usage.input_tokens, usage.cache_read_input_tokens,
                    usage.cache_creation_input_tokens, usage.output_tokens, usd,
                    self.ledger.spent, f" DROPPED {len(drops)} thinking" if drops else "")
        if msg.stop_reason == "refusal":
            logger.warning("refusal: %s", msg.stop_details)
        return call_id

    def respond(self, msg, request: dict, seconds: float) -> dict:
        text = "".join(b.text for b in msg.content if b.type == "text")
        calls = [b for b in msg.content if b.type == "tool_use"]
        thinking = [b.model_dump(exclude_none=True) for b in msg.content
                    if b.type in ("thinking", "redacted_thinking")]
        self.store.put(turn_key(text, [c.id for c in calls]), thinking)
        call_id = self.record(msg, request, seconds)
        message = {"role": "assistant", "content": text or None}
        if calls:
            message["tool_calls"] = [{"id": c.id, "type": "function",
                                      "function": {"name": c.name,
                                                   "arguments": json.dumps(c.input)}}
                                     for c in calls]
        return chat_response(call_id, self.alias, message, FINISH.get(msg.stop_reason, "stop"),
                             prompt_tokens(msg.usage), msg.usage.output_tokens)

    def agentic_write(self, request: dict) -> tuple[int, dict]:
        request = dict(request)
        request["tools"] = WRITE_TOOLS
        request["max_tokens"] = min(request["max_tokens"], AGENTIC_TURN_TOKENS)
        if self.write_budget:
            request["output_config"] = {**request["output_config"],
                                        "task_budget": {"type": "tokens", "total": self.write_budget}}
            request["betas"] = request["betas"] + ["task-budgets-2026-03-13"]
        messages = request["messages"] + [{"role": "system", "content": self.agentic_note}]
        sections: dict[str, str] = {}
        started = time.time()
        out_tokens, last_prompt, finished = 0, 0, False
        for turn in range(1, AGENTIC_TURNS + 1):
            if self.ledger.over() or time.time() - started > AGENTIC_SECONDS:
                logger.warning("agentic write stopped at turn %d with %d sections", turn, len(sections))
                break
            request["messages"] = messages
            try:
                msg, seconds = self.stream_call(request)
            except EngineError as e:
                if not sections:
                    return e.status, {"error": {"message": e.message}}
                logger.error("agentic write turn %d failed, returning %d sections", turn, len(sections))
                break
            self.record(msg, request, seconds, tag=f"write t{turn}")
            out_tokens += msg.usage.output_tokens
            last_prompt = prompt_tokens(msg.usage)
            messages = messages + [{"role": "assistant",
                                    "content": [b.model_dump(exclude_none=True) for b in msg.content]}]
            results = []
            for block in msg.content:
                if block.type != "tool_use":
                    continue
                if block.name == "write_section":
                    markdown = str(block.input.get("markdown", "")).strip()
                    heading = markdown.splitlines()[0].strip() if markdown else ""
                    if not heading.startswith("#"):
                        note = "Not saved: markdown must start with the section's heading line."
                    else:
                        replaced = heading in sections
                        sections[heading] = markdown
                        note = (f"{'Replaced' if replaced else 'Saved'} {heading!r} ({len(markdown)} chars). "
                                f"Sections so far: {', '.join(sections)}")
                elif block.name == "done":
                    finished = True
                    note = "Spec handed to the builder."
                else:
                    note = f"No tool named {block.name!r}."
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": [{"type": "text", "text": note}]})
            logger.info("agentic write turn %d: %d sections, %d chars", turn, len(sections),
                        sum(len(v) for v in sections.values()))
            if finished:
                break
            if results:
                messages = messages + [{"role": "user", "content": results}]
            elif sections and msg.stop_reason == "end_turn":
                break
            else:
                messages = messages + [{"role": "user", "content": [{"type": "text", "text":
                    "Save the spec with write_section, one section per call, then call done."}]}]
        spec = "\n\n".join(sections.values())
        logger.info("agentic write %s: %d sections, %d chars, %.0fs", "done" if finished else "ended",
                    len(sections), len(spec), time.time() - started)
        message = {"role": "assistant", "content": spec or None}
        return 200, chat_response(uuid.uuid4().hex[:12], self.alias, message, "stop",
                                  last_prompt, out_tokens)


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
            body = json.loads(self.rfile.read(length) or b"{}")
            status, out = engine.complete(body)
            self._send(status, out)

        def log_message(self, fmt, *args):
            pass

    return Handler


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="claude-opus-5-5", choices=sorted(PRICES))
    parser.add_argument("--alias", required=True, help="the model id the control plane asks for")
    parser.add_argument("--key-file", default="~/.anthropic_key")
    parser.add_argument("--max-tokens", type=int, default=128000)
    parser.add_argument("--toolless-effort", choices=sorted(EFFORTS), default=None,
                        help="effort for calls with no tools (the design write), overriding the harness")
    parser.add_argument("--toolless-note", default=None,
                        help="file whose text is appended as a system message to calls with no tools")
    parser.add_argument("--agentic-write", default=None,
                        help="file with the instruction for writing a tool-less reply section by section "
                             "through write_section/done; the stitched sections are the reply")
    parser.add_argument("--write-budget", type=int, default=None,
                        help="task budget in tokens, visible to the model, for the whole agentic write")
    parser.add_argument("--turn-budget", type=int, default=None,
                        help="task budget in tokens, visible to the model, for each request that has tools")
    parser.add_argument("--budget-usd", type=float, required=True)
    parser.add_argument("--ledger", default="calls.jsonl")
    parser.add_argument("--thinking-store", default="thinking.json")
    parser.add_argument("--port", type=int, default=8091)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    engine = Engine(args)
    logger.info("serving %s as %s on :%d, spent $%.2f of $%.2f", args.model, args.alias,
                args.port, engine.ledger.spent, args.budget_usd)
    ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(engine)).serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
