"""Ask JEV yes/no on every row of prompts/design/systems.json, with one control ask's frame as state.
usage: systems.py <control run id> [question with {item}]"""
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.paths import REPO, SRC

sys.path.insert(0, str(Path.home() / "Documents" / "gamesummoner-images"))
from contract.decide import HEAD_DIR, Head, prompt, run_chain

HERE = Path(__file__).resolve().parent
SYSTEMS = SRC / "maestro" / "codegen" / "prompts" / "design" / "systems.json"
QUESTION = "Does this mechanic make sense for this game: {item}?"
SWAP = json.loads((REPO / "src" / "config" / "settings.json").read_text())["local"]["llama_swap"]
HEAD = Head(HEAD_DIR)


def one(kind, text, n):
    body = {"model": SWAP["decide"], "prompt": text, "max_tokens": 1, "temperature": 1.0, "top_p": 1.0,
            "top_k": 0, "logprobs": n, "allowed_token_ids": HEAD.ids(kind, n),
            "return_tokens_as_token_ids": True, "add_special_tokens": False}
    request = urllib.request.Request(f"{SWAP['url'].rstrip('/')}/v1/completions",
                                     json.dumps(body).encode(), {"Content-Type": "application/json"})
    top = json.load(urllib.request.urlopen(request, timeout=900))["choices"][0]["logprobs"]["top_logprobs"][0]
    return HEAD.probabilities(kind, {int(k.split(":")[1]): v for k, v in top.items()}, n)


def read(kind, state, questions):
    return [one(kind, prompt(kind, state, q, options), len(options)) for q, options in questions]


def frame_state(run):
    lines = json.loads((HERE / "control" / f"{run}.json").read_text())["state"].splitlines()
    return "\n".join(lines[:next(i for i, line in enumerate(lines) if line.startswith("mechanics:"))])


def main():
    run = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else QUESTION
    systems = json.loads(SYSTEMS.read_text(encoding="utf-8"))
    state = frame_state(run)
    step = {"key": "systems", "kind": "noul", "question": question, "keep_over": 0.6,
            "items": [{"name": name, "text": f"{name}: {text}"} for name, text in systems.items()]}
    result = run_chain(read, state, [step])
    probabilities = result["steps"][0]["probabilities"]
    print(state, "\n")
    print(question)
    for name, p in sorted(probabilities.items(), key=lambda kv: -kv[1]):
        print(f"  {p:.3f}  {'KEEP' if p > 0.6 else '    '}  {name}")
    out = HERE / "systems"
    out.mkdir(exist_ok=True)
    runs = out / f"{run}.jsonl"
    with runs.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"state": state, "question": question, "systems": systems,
                            "probabilities": probabilities}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
