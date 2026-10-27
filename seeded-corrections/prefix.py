"""The arms: harness-written rounds after the request, answered by the real turn machine."""

import json
from typing import Dict, List

SEEDED = [
    ("read_file", {"path": "design/design.md"}),
    ("python", {"code": 'print(open("design/design.md").read())'}),
    ("python", {"code": 'print([f["path"] for f in list_files()])'}),
]
READ = [
    ("python", {"code": 'print(read_file("design/design.md", lines=100))'}),
]
LIST = [
    ("python", {"code": "print(list_files())"}),
]
LIST_READ = LIST + READ


def seed(history: List[Dict], tools: Dict, run_dir, rounds=SEEDED) -> List[Dict]:
    from maestro.codegen import build_state, build_steps

    scratch = build_state.BuildCursor(build_id="seed", started=True)
    out = history[:1]
    for i, (name, args) in enumerate(rounds):
        tc = {"id": f"call_seeded_{i}", "type": "function",
              "function": {"name": name, "arguments": json.dumps(args)}}
        out.append({"role": "assistant", "content": "", "tool_calls": [tc]})
        scratch.history = []
        build_steps._apply(tools, scratch, tc, run_dir)
        out.extend(scratch.history)
    return out + history[1:]


def seed_read(history: List[Dict], tools: Dict, run_dir) -> List[Dict]:
    return seed(history, tools, run_dir, READ)


def seed_list(history: List[Dict], tools: Dict, run_dir) -> List[Dict]:
    return seed(history, tools, run_dir, LIST)


def seed_list_read(history: List[Dict], tools: Dict, run_dir) -> List[Dict]:
    return seed(history, tools, run_dir, LIST_READ)


def _is_seeded(m: Dict) -> bool:
    ids = [tc.get("id", "") for tc in m.get("tool_calls") or []] + [m.get("tool_call_id") or ""]
    return any(i.startswith("call_seeded_") for i in ids)


def pin():
    """Keep the seeded rounds right after the request through every compaction."""
    from maestro.codegen import build_steps

    original = build_steps.compact

    def compact(run_dir, cursor, keep_chars):
        seeded = [m for m in cursor.history if _is_seeded(m)]
        cursor.history = [m for m in cursor.history if not _is_seeded(m)]
        try:
            return original(run_dir, cursor, keep_chars)
        finally:
            cursor.history = cursor.history[:1] + seeded + cursor.history[1:]

    build_steps.compact = compact
    return original


def unpin(original) -> None:
    from maestro.codegen import build_steps
    build_steps.compact = original
