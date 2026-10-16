"""The worker's needs: tool calls, thinking split from the answer, and a screenshot turn."""
import base64, json
from common import *

proc = start(config(PACKS["q4"]), "compat")
try:
    tools = [{"type": "function", "function": {"name": "write_file", "description": "Write a file in the game folder",
              "parameters": {"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                             "required": ["path", "content"]}}}]
    r = post({"model": "m", "max_tokens": 4000, "tools": tools, "messages": [
        {"role": "user", "content": "Create index.html containing a single h1 that says Hello. Use the tool."}]})
    m = r["choices"][0]["message"]
    print("TOOLS finish:", r["choices"][0]["finish_reason"], "| tool_calls:", json.dumps(m.get("tool_calls"))[:300],
          "| reasoning chars:", len(m.get("reasoning_content") or ""), "| content:", (m.get("content") or "")[:100], flush=True)
    r = post({"model": "m", "max_tokens": 3000, "messages": [{"role": "user", "content": "What is 17 * 23? Think, then answer."}]})
    m = r["choices"][0]["message"]
    print("THINK reasoning chars:", len(m.get("reasoning_content") or ""), "| content:", (m.get("content") or "")[:200], flush=True)
    img = base64.b64encode(open(f"{W}/shot.png", "rb").read()).decode()
    r = post({"model": "m", "max_tokens": 2000, "chat_template_kwargs": {"enable_thinking": False}, "messages": [
        {"role": "user", "content": [{"type": "text", "text": "Describe this game screenshot in two sentences."},
                                     {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}}]}]})
    print("IMAGE:", (r["choices"][0]["message"].get("content") or "")[:400], flush=True)
finally:
    stop(proc)
