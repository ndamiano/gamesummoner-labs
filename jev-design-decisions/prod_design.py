"""Run the prompt through the current design chain's four prompts (gameplay, visual, engineering,
integrate with continuations, one retry on an empty reply), same messages and request body, posted
straight to llama-swap. Designer docs already written in the run dir are reused."""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/nick/Documents/ai-agent-test/src")
sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from config.settings_manager import settings_manager
from maestro.codegen import design

RUN = Path(sys.argv[1])
OUT = RUN / "prod_design"

GEN = "qwen3.8-27b-quasar"


def call(step, prompt, docs, spec_so_far=""):
    llm = settings_manager.get_settings()["llm"]
    body = {"model": GEN, "messages": design._messages(step, prompt, docs, spec_so_far), "temperature": 0.7,
            "max_tokens": design.MAX_TOKENS, "reasoning": llm["reasoning"]}
    t = time.time()
    r = ask.post(f"{ask.SWAP}/v1/chat/completions", body, timeout=3600)
    took = time.time() - t
    text = design._reply_text(r)
    json.dump({"seconds": took, "response": r}, open(OUT / f"{step}_{int(t)}.raw.json", "w"), indent=1)
    print(f"{step}: {took:.0f}s, {r['usage']['completion_tokens']} tokens, {len(text)} chars", flush=True)
    return text


def main():
    OUT.mkdir(exist_ok=True)
    prompt = json.load(open(RUN / "frame_result.json"))["prompt"]
    ask.chat(GEN, "hi", 1, think=False)
    docs = {}
    t = time.time()
    for step in design.STEPS[:3]:
        done = OUT / f"{step}.md"
        if done.is_file() and done.read_text().strip():
            docs[step] = done.read_text()
            continue
        for _ in range(design.RETRIES + 1):
            docs[step] = call(step, prompt, docs)
            if docs[step].strip():
                break
        done.write_text(docs[step])
    spec = ""
    for _ in range(design.CONTINUATIONS + 1):
        spec += call("integrate", prompt, docs, spec)
        if not design.missing_sections(spec):
            break
    (OUT / "design.md").write_text(spec)
    print(f"total {time.time() - t:.0f}s, missing sections {design.missing_sections(spec)}")


if __name__ == "__main__":
    main()
