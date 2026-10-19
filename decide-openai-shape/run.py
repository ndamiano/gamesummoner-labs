"""Replay a decide chain through JEV's OpenAI path (/v1/completions + logprobs) and diff it against a
control result. usage: run.py <payload.json> <expected.json> [base_url] [model]"""
import json
import math
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Documents/gamesummoner-images"))
from contract.decide import prompt, run_chain  # noqa: E402

JEV = Path("/var/lib/models/jev/JEV-27B-VL")
HEAD = json.loads((JEV / "adapter_vllm/decision_head.json").read_text())
TEMPS = json.loads((JEV / "calibration.json").read_text())["per_kind"]
URL = sys.argv[3] if len(sys.argv) > 3 else "http://localhost:8199"
MODEL = sys.argv[4] if len(sys.argv) > 4 else "jev-decision"


def one(kind, text, n):
    lo = HEAD["slots"]["ranges"][kind][0]
    ids = HEAD["verbalizer_ids"][lo: lo + n]
    body = {"model": MODEL, "prompt": text, "max_tokens": 1, "temperature": 1.0, "top_p": 1.0,
            "top_k": 0, "logprobs": n, "allowed_token_ids": ids,
            "return_tokens_as_token_ids": True, "add_special_tokens": False}
    req = urllib.request.Request(f"{URL}/v1/completions", json.dumps(body).encode(),
                                 {"Content-Type": "application/json"})
    out = json.load(urllib.request.urlopen(req, timeout=300))
    top = out["choices"][0]["logprobs"]["top_logprobs"][0]
    lp = {int(k.split(":")[1]): v for k, v in top.items()}
    z = [(lp.get(t, -1e9) + HEAD["bias"][lo + i]) / TEMPS[kind] for i, t in enumerate(ids)]
    m = max(z)
    e = [math.exp(x - m) for x in z]
    return [x / sum(e) for x in e]


def read(kind, state, questions):
    return [one(kind, prompt(kind, state, q, opts), len(opts)) for q, opts in questions]


def main():
    payload = json.loads(Path(sys.argv[1]).read_text())
    expected = json.loads(Path(sys.argv[2]).read_text())
    expected = expected.get("result", expected)
    got = run_chain(read, payload.get("state") or "", payload["steps"])
    worst, n, flips = 0.0, 0, []
    for a, b in zip(got["steps"], expected["steps"]):
        if a.get("skipped") or b.get("skipped"):
            if a.get("skipped") != b.get("skipped"):
                flips.append((a["key"], "skip differs"))
            continue
        for k, p in a["probabilities"].items():
            q = b["probabilities"].get(k)
            if q is not None:
                worst, n = max(worst, abs(p - q)), n + 1
    for k, v in expected["answers"].items():
        if got["answers"].get(k) != v:
            flips.append((k, f"{v!r} -> {got['answers'].get(k)!r}"))
    print(json.dumps({"compared": n, "max_abs_diff": round(worst, 4), "answer_flips": flips}, indent=1))
    Path("out").mkdir(exist_ok=True)
    (Path("out") / (Path(sys.argv[1]).stem + ".got.json")).write_text(json.dumps(got, indent=1))


if __name__ == "__main__":
    main()
