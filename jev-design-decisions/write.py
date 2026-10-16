"""Hand every JEV decision to the generator LLM as fixed and have it write the full design.md."""
import json
import sys
from pathlib import Path
import time

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask

RUN = Path(sys.argv[1])

GEN = "qwen3.8-27b-quasar"


def main():
    prompt = json.load(open(RUN / "frame_result.json"))["prompt"]
    state = json.load(open(RUN / "look_sound_result.json"))["state"]
    full = open("prompts/write.txt").read().format(state=state, prompt=prompt)
    ask.chat(GEN, "hi", 1, think=False)
    t = time.time()
    r = ask.chat(GEN, full, 100000, think=True)
    took = time.time() - t
    json.dump({"seconds": took, "response": r}, open(RUN / "write_raw.json", "w"), indent=1)
    text = r["choices"][0]["message"]["content"].split("</think>")[-1].strip()
    open(RUN / "design.md", "w").write(text + "\n")
    print(f"{took:.0f}s, usage {r['usage']}, finish {r['choices'][0]['finish_reason']}, design {len(text)} chars")


if __name__ == "__main__":
    main()
