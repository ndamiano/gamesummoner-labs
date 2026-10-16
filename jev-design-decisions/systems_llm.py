"""Ask the generator LLM the same level-1 systems question in one pass, and compare with JEV's answers."""
import json
import re
import sys
from pathlib import Path
import time

sys.path.insert(0, "/home/nick/Documents/decision-model-test")
import ask
from systems import level1

RUN = Path(sys.argv[1])

GEN = "qwen3.8-27b-quasar"


def main():
    jev = json.load(open(RUN / "systems_result.json"))
    systems = level1()
    prompt = open("prompts/systems_llm.txt").read().format(state=jev["state"], systems="\n".join(f"- {s}" for s in systems))
    ask.chat(GEN, "hi", 1, think=False)
    t = time.time()
    r = ask.chat(GEN, prompt, 16000, think=True)
    took = time.time() - t
    text = r["choices"][0]["message"]["content"].split("</think>")[-1]
    llm = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
    print(f"llm took {took:.0f}s, {r['usage']['completion_tokens']} completion tokens\n")
    for s in sorted(systems, key=lambda s: -jev["probabilities"][s]):
        j = jev["probabilities"][s] > 0.6
        print(f"{jev['probabilities'][s]:.3f} jev={'Y' if j else 'n'} llm={'Y' if llm[s] else 'n'} {'' if j == llm[s] else '<- differs'}  {s}")
    json.dump({"prompt": prompt, "seconds": took, "usage": r["usage"], "raw": r["choices"][0]["message"], "llm": llm},
              open(RUN / "systems_llm_result.json", "w"), indent=1)


if __name__ == "__main__":
    main()
