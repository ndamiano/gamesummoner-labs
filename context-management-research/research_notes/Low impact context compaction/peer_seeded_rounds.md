# Seeded synthetic tool rounds — results relayed from session ai-agent-test-bc (2026-10-20)

Verbatim relay of the other session's answer to "how well did telling the model it did certain actions work?"

Seeded synthetic tool rounds (fake assistant calls + REAL tool replies produced by build_steps._apply) inserted right after the request. Labs: labs/seeded-corrections/ (prefix.py, positions.py, run_battery*.py, README Log) and labs/open-shim/ (arm.py, run_battery.py, lost.py, rw.py, README Log). Nothing in src/, nothing committed. Model: local Flash-Next IQ3_S (Basalt). Metric: lost turns per 5-turn branch (direct native tool calls "carried no code" + refused programs: open(), imports, syntax), 200 branches per arm at 4 real fix-build starts; also reads/branch. Early batteries undercounted import refusals; numbers below are the recount (open-shim lost.py).

Fix-start results (lost turns/branch, branches with any loss of 200):
- ctrl: 0.84, 125 (direct 53, open() 92, import 21)
- 3 rounds = direct read_file (fails) + python open() (refused) + working list_files: 0.76, 105. Failure kinds traded places by position; NOT a win.
- list_files only: 1.21, 190 — WORSE: model then open()s the listed paths (182 open refusals).
- list -> read (two rounds): 0.47, 90 (open('design/design.md') 49, import 43)
- one successful read (print(read_file("design/design.md", lines=100))): 0.42, 81 — direct calls 0, open 2, but 77 dead `import subprocess` lines (whole program refused).
- read seed + open() shim: 0.39
- real file access (Landlock-confined child, os/pathlib/glob allowed) no seed: 0.23, 34
- real files + one program (list_files + 100-line design read): 0.29, 58 (all import subprocess)
- + user nudge "Good, continue, and please do not use the subprocess module.": 0.065, 13
- + seeded FAILED `import re, subprocess` program with its real refusal, then nudge: 0.03, 6 (best; vs nudge-only p=0.16). New minor mode: 4 `__import__('re')` refusals.

Reads/branch: ctrl 2.77 -> seeded arms ~6.2-6.5. Writes in 5 turns ~0 everywhere.

Failure modes: (1) seeded FAILURES get imitated — single run copied the seeded open() verbatim (`open("design/design.md").read() if False else None`); post-compaction the 3-round seed doubled direct calls (18 -> 36 branches with one, p=0.012). (2) A listing with no read primes open() on those paths. (3) Seeded successful read primes a dead `import subprocess` habit; an explicit nudge fixes most of it. No sign of the model distrusting/repeating the seeded turns otherwise; format drift not observed.

Compaction: seeded rounds pinned at history[1:k] through compaction (wrap build_steps.compact). 3-round seed post-compaction battery (7 positions, 200/arm): direct calls doubled — idea failure. Winning arm checked through compaction in full builds only (6 compactions, pins held, 0 direct calls in a 200-turn build vs ctrl 6).

Full builds (same design, same request): run 42427fef48dd arm vs 1629ea1ae380 ctrl: arm build1 3 lost turns vs 10, passed both gates round 0, no fix build (ctrl needed a 93-turn fix); Nick: "approximately even". 6-pair battery (/var/tmp/open-shim/battery) in progress: pair 1 both passed gates first try, lost turns ctrl 10 / arm 7 (arm had 3 direct calls). Quality: n too small to claim anything yet.

Key implication for compaction: seeded reads RAISED reads/branch (2.77 -> ~6.3) — seeding a read teaches "read more", the opposite of read minimization. Seeded rounds condition behavior strongly (imitation of exact code, including failures).
