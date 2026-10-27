# GameSummoner internal evidence: compaction, re-reads, synthetic history, JEV

All sources are local files in `/home/nick/Documents/ai-agent-test` (main repo, "src/", "docs/") and
its `labs/` sub-repo. Paths below are relative to that root. Line numbers are as of 2026-10-20 (HEAD
d05a659 main repo, 6828d74 labs). Memory notes (`~/.claude/projects/.../memory/*.md`) were cross-checked
against code; where a memory note is stale, that is flagged.

## (a) How compaction works in the build loop today

### Takeaway
Compaction is a deterministic, harness-side trim (no model-written summary) in
`src/maestro/codegen/build_steps.py`: it fires when the next prompt would leave <16K tokens of the window,
strips all reasoning, stubs superseded/old file-write bodies, drops read-only rounds, drops oldest rounds
until ~33% of the window, and inserts ONE user "note" holding a regex code map of the whole project, a
"files you already read are unchanged" block, and an art listing. File contents themselves are not carried
in the note; the build prompt still tells the model "you will need to re-read".

### Cited Findings
- Constants: `_COMPACT_ROOM = 16_000` tokens, `_COMPACT_KEEP = 0.33`, `_DEDUP_ENOUGH = 0.30`, `_OUT_CAP = 30_000`, `_MIN_OUT = 2_000` — [build_steps.py:26-31](src/maestro/codegen/build_steps.py)
- Trigger: `_infer` compacts when `_estimate(cursor) > ctx - _COMPACT_ROOM`, or on a cut-off re-send (`full_window=True`) when the estimate is above `ctx * 0.33`; also force-compacts when less than 2K tokens of output room remain — [build_steps.py:306-322](src/maestro/codegen/build_steps.py)
- The estimate is the server's last counted `prompt_tokens` plus chars added since //3; the keep target converts tokens→chars at the measured chars-per-token of the last prompt (3 until the server counts one) — [build_steps.py:290-303](src/maestro/codegen/build_steps.py); [build_state.py:40-43](src/maestro/codegen/build_state.py); commit d89f202 (2026-09-11: fixed a guessed 4 chars/token; real transcripts run ~2.9, so "a third" had been ~60K not ~43K)
- A server "context_length_exceeded"/"max_context" refusal sets `prompt_tokens = n_ctx` and re-infers, forcing a compaction; if nothing can be trimmed the build ends "stalled: the prompt is over the window" — [build_steps.py:97-106](src/maestro/codegen/build_steps.py)
- `n_ctx` comes from settings `llm.n_ctx` (default 32768 in code); prod/local run 131,072 — [build_steps.py:85-87](src/maestro/codegen/build_steps.py); memory `project_window_131k_engine_args`
- Pipeline in `compact()`: remove the previous note → `strip_reasoning` (all `reasoning_content` dropped) → `dedupe_bodies` (every write of a path older than the newest write becomes a stub "[the N chars written to PATH — a newer copy is later in this transcript]") → `drop_read_only_rounds` (rounds whose programs only called read_file/list_files/check_syntax/play are deleted entirely) → if dedupe alone saved ≥30% stop there → else stub write bodies oldest-round-first until under keep ("— on disk; not repeated here") → else drop whole oldest rounds — [build_steps.py:376-536](src/maestro/codegen/build_steps.py)
- Stubbing applies only to literal bodies ≥200 chars passed to `write_file` (positional or keyword, a literal, a name bound once to a literal, or `+` of those), found by AST parse of the model's Python program — [build_steps.py:349-398](src/maestro/codegen/build_steps.py); commit "the trim tier reads the writes a model actually makes" ([experiments.md:2227-2244](docs/experiments.md))
- Read RESULTS (tool messages) are not stubbed per se; read-only rounds are deleted whole, and the history after the first message is otherwise kept or dropped by round — inference from [build_steps.py:432-457](src/maestro/codegen/build_steps.py)
- Note text: "[Earlier steps were trimmed to save room. Every file is on disk exactly as you last wrote or read it. Below is the whole project: each file, what it imports, and every declaration with its line range. Read a file only to edit it, and read the lines you need with offset and lines rather than the whole file.]" + `code_map.render(root)` + `file_state.render` block + "Art on disk:" listing of assets with byte sizes — [build_steps.py:482-531](src/maestro/codegen/build_steps.py)
- The note is placed right after the original request (`history[:1] + [note] + kept`); only one note is kept (previous note replaced, since 90d82c3, 2026-09-15) — [build_steps.py:530](src/maestro/codegen/build_steps.py); commit 90d82c3
- Code map: regex over .js/.mjs/.html/.css/.json/.md (skips assets/, world/, vendor), each file with line count, imports, top-level and one-level-inner declarations with line ranges, and markdown headings with line ranges (so design.md is addressable by section) — [code_map.py:1-30](src/maestro/codegen/code_map.py); commit 2e2af82 says "~3K tokens for that project against a 58K-token sweep"
- File-state block: `reads.json` stores sha256[:12] of the WHOLE file at every read (partial reads included); at compaction it lists "You have already read these files and they have NOT changed since — reading them again returns exactly what you were shown" plus changed files with sizes. Rendered once per compaction, deliberately not per turn, to protect the KV prefix — [file_state.py:1-83](src/maestro/codegen/file_state.py); [tools.py:172](src/maestro/codegen/tools.py)
- Reasoning: each turn's `reasoning_content` rides the transcript until the next compaction, then all is dropped (commit 4945ef3, 2026-09-11; motivated by KV-cache prefix reuse) — [build_steps.py:143-144, 460-461](src/maestro/codegen/build_steps.py); [experiments.md:2176-2210](docs/experiments.md)
- Assistant content over 2,000 chars is truncated to its last 2,000 at append time; only the first tool call of a turn is kept — [build_steps.py:153-157](src/maestro/codegen/build_steps.py)
- The design is NOT in the prompt: since spec-skeleton the spec lives on disk in `design/` and the model reads it (it previously rode `history[0]`, 25–33K tokens, never compacted) — [labs/spec-skeleton/README.md:698-700](labs/spec-skeleton/README.md); [build.txt:1-5](src/maestro/codegen/prompts/build.txt)
- The system prompt still says: "For context compaction, we will drop most of the history, and you will need to re-read. Given that, combined with the fact that you only get what you print into context, try to only print exactly what you need." — [build.txt:34-36](src/maestro/codegen/prompts/build.txt)
- Read mechanics: `read_file(path, offset, lines)` returns text into the Python program; only what the program prints reaches context, and stdout is capped at `MAX_STDOUT = 20_000` chars per turn. `MAX_READ_CHARS` is 8,000,000 (effectively uncapped). Partial reads end with "[showed lines a-b of N; read the rest with offset …]" — [tools.py:24, 124-173](src/maestro/codegen/tools.py); [pyexec/runner.py:31, 168](src/maestro/codegen/pyexec/runner.py)
- Turn log replays compactions exactly (`kind: compact`, trimmed/dropped/note) so labs can reconstruct any prompt — [turn_log.py:32-82](src/maestro/codegen/turn_log.py)
- Memory note `project_compaction_reread_cycle.md` describes a 62% trigger / `_FRESH_ROUNDS=3` / `MAX_READ_CHARS=20K` shape: that is the pre-2026-09-06 design and is STALE vs code (trigger is now n_ctx−16K, `_FRESH_ROUNDS` deleted in 7022895, read cap 8M) — [build_steps.py:26-27](src/maestro/codegen/build_steps.py); commit 7022895

### Inferences
- The post-compaction floor is set by the newest copy of every file's body staying resident (only superseded/oldest bodies are stubbed), which is why the labs measure a ~60K-token floor on a 131K window once the game is 130–150K chars.
- The note gives structure (map) and freshness facts but not content; any decision needing bytes requires a read. The surviving build.txt line 34 actively primes a re-read after every compaction, contradicting the note's "Read a file only to edit it".
- Compaction is a full re-prefill (prefix breaks at the note right after `history[0]`).

### Gaps
- No model-written summary exists in prod; the only summary-style compactor tried is the lab "dsh" arm (see b).
- I did not find a recorded measurement of the note's token size on a large game beyond the ~3K figure in commit 2e2af82.

## (b) Measured results: compaction, re-read cycle, read cost

### Takeaway
The re-read cycle is the single largest measured waste: it ate steps 76–200 (~$12 of ~$22) of the best game GameSummoner ever made (Opus 5.5) and caused both prod 200-step cap-outs on 2026-09-06. Five note-content interventions (fact block, rule, no map, bare map, bodies pasted, bodies as a synthetic read round) did not move re-read rates (~50% of post-compaction turns re-read). What has helped: a bigger window, the code map with md headings (ranged design reads), dedupe/trim-to-fit.

### Cited Findings
**Frontier ceiling (Opus 5.5, 2026-10-18, n=1)**
- Opus build d086d499669b: capped at 200, $20.70 for 200 calls; tier 1 + its DoD rows done by ~step 75. Steps 1–75: 25 writes, 9 edits, 8 plays, 37 reads. Steps 76–200: 114 reads, 3 writes, 0 plays, 15 compactions "each followed by re-reading its own large files until the 131K window filled again" — [labs/frontier-ceiling/README.md:125-131](labs/frontier-ceiling/README.md)
- Cost split restated: "steps 76–200 lost to the re-read cycle (~$12)" of ~$22; Nick scored the game 9 — [docs/experiments.md:2561, 2586, 2595](docs/experiments.md)
- Compaction-floor lab's breakdown of the same build: turns 1–79: 5 compactions, 63 read_file calls, 47 writes/edits; turns 80–200: 10 compactions, 175 read_file calls, 2 writes/edits. Each compaction resumed at 42–84K prompt tokens (mean ~62K) on 131K, with 158 KB of game JS and a 54 KB spec on disk; refilled in ~10 turns. Compactions at 15/25/31/60/79 then every 8–21 turns to 190 — [labs/compaction-floor/README.md:3-21](labs/compaction-floor/README.md) (note: counts differ slightly from the frontier-ceiling README's 114 reads/15 compactions for 76–200; different turn boundaries/counting)
- Same ask, Flash-Next control 524b1c3efa1c: 6 compactions, tier 1 at ~step 155, 74 reads / 50 plays / 44 edits / 19 writes; DeepSeek V4.1 Flash 01a723c0555a: 9 compactions, 88 reads; Nick: Opus "would likely have gone further without the compaction re-read loop" — [labs/frontier-ceiling/README.md:150-168](labs/frontier-ceiling/README.md)

**compaction-floor lab (planned, not run)**
- Status planned. Hypothesis: a lower keep ratio, or bodies replaced by a file listing plus per-file line counts, drops the floor and the re-read count without costing the builder; metrics = turns between compactions, re-reads per compaction, turns to done, on collector and platformer specs. Idea failure: "the builder re-reads everything it lost anyway". Log and Outcome empty — [labs/compaction-floor/README.md:23-38](labs/compaction-floor/README.md)
- Control collector c6b51ec35d89: compactions at 43/83/144/186; after 83 it re-read `design/` 39 times (turns 96–199), 56 edits / 45 plays / 3 writes, never called done; "Post-compaction floor ≈ 60K tokens = the newest body of every game file" — [labs/spec-skeleton/README.md:719-727](labs/spec-skeleton/README.md)

**2026-09-06 prod cap-outs (pre-fix compactor)**
- Visual novel 4ce312b2ab09 written by step 28, then 17 compactions / 151 read-only steps; Zelda-like c83920af40a2 written by step 23, then 21 compactions / 149 read-only steps; period 10–12 steps = one full project read; 0-compaction builds finish in 21–68 steps; dropped=0 on 23 of 24 compactions; Zelda 120/200 turns' reasoning = verify/elided; project 116–200K chars ≈ 35–60K tokens — memory `project_compaction_reread_cycle.md` (from prod turns.jsonl); corroborated by commit 7022895 ("150 of 200 steps, 17–21 compactions, never a done")
- Fix 7022895 (dedupe newest-copy-wins, trim oldest-first only until it fits, factual stub wording): replayed on the VN transcript at first compaction, 9 of 12 files live instead of 3 — commit 7022895
- Then 2e2af82 (code map in the note, drop read-only rounds): "moved the re-read loop, it did not end it: on a 26-file tactics build 149 of 176 post-compaction reads were of files already stubbed … a 52K-token project cannot fit beside its transcript" — commit 2e2af82 (2026-09-07)
- Then e5c632d (file-state block): "90 of 95 post-compaction reads were of files the build had ALREADY read" (run 67a1f6e389f4, 10 compactions); cites openai/codex #16839 (three files read 53/24/17 times, ~90% of one session's reads) and notes Cline's FileContextTracker tracks only the inverse — commit e5c632d; [file_state.py:3-12](src/maestro/codegen/file_state.py)

**The note cannot stop a re-read (2026-09-08, replay lab, local 27B)**
- Six real compaction points, 18 samples/arm: 8/18 turns re-read with the block, 9/17 without. Also null: a rule ("must NOT be read again"), code map deleted, map alone with prose stripped, file bodies pasted into the note, and the bodies delivered as a completed `read_file` round (most reads of any arm: 19 vs baseline 16). "Handing the model the exact bytes does not stop it fetching them." — [docs/experiments.md:2093-2117](docs/experiments.md); [labs/replay/README.md:8-13](labs/replay/README.md)
- Arms implemented in [labs/replay/arms_reads.py:71-191](labs/replay/arms_reads.py) and [arms_compaction.py](labs/replay/arms_compaction.py); preread question framed as "Is the re-read about information, or about procedure?" — [arms_preread.py:1-6](labs/replay/arms_preread.py)

**Token accounting / read cost**
- Local 27B: writing 34%, reading 31%, empty turns 17% of generated tokens; prod Flash-Next: reading 52%, writing 34%, empty 2.5%; 77% of prod's reads are of files already read; fix builds read most (they start with an empty transcript) — [labs/replay/README.md:18-21](labs/replay/README.md); [docs/experiments.md:2112-2116](docs/experiments.md)
- Reads are cheap per step (1–4 s) but burn steps toward the 200 cap — memory `project_compaction_reread_cycle.md`
- Typical sizes: ~10-file game read back whole ≈ 40K tokens (memory, 2026-09-04); 26-file tactics project 52K tokens / 58K-token sweep vs ~3K map (2e2af82); Opus game 158 KB JS + 54 KB spec; collector 10 files 140K chars; ~128 KB codebase ≈ 35K tokens ([experiments.md:124-127](docs/experiments.md)); 24,168 chars of JS = 8,173 tokens raw (~2.96 chars/token) ([experiments.md:1959-1963](docs/experiments.md)); fix build a736b5 "seven turns printed whole files (13–20K characters each)", first edit at turn 30 with 65K in prompt ([experiments.md:2287-2289](docs/experiments.md))

**Window size and trim tier**
- 2K-word RPG design: 65K window → 110 turns, 134 reads, 29 compactions (787 rounds trimmed, 101 dropped), 60% of turns reads ("read → stubbed three rounds later → re-read"); 131K window → 61 turns, 32 reads, 2 compactions. "the fix is the window, not the trim" — [docs/experiments.md:113-135](docs/experiments.md)
- 2026-08 shape (trigger 0.62, keep 0.33): "every cut forgets ~half the transcript"; ≥60% of transcript is file bodies also on disk; identical no-op edit loops began after the 2nd–3rd cut — [docs/experiments.md:181-190](docs/experiments.md)
- Trim tier never ran for a period: DeepSeek Flash 214-turn build, 30 compactions all `trimmed: 0`, 88 whole rounds dropped (matcher only saw keyword-literal writes) — [docs/experiments.md:2147-2174](docs/experiments.md); fixed matcher recovers 21% (8988a28a746e) and 87% (f7f816519d16) of program bytes — [experiments.md:2236-2242](docs/experiments.md)
- A cut kept two-thirds not one-third (chars/token mis-conversion): 7 compactions in 95 turns, ~112K→~83K each — [docs/experiments.md:2212-2225](docs/experiments.md)
- Post-compaction stale edits: skyrim ecs3 re-read every module after each compaction and "edited against a stale picture of files whose read it had lost": six `old_text was not found` on world3d.js (turns 55–64), lighting block replaced twice (99–101, 126–134) — [docs/experiments.md:1432-1438](docs/experiments.md)
- Indoor3d: 18 byte-identical failing edit_file calls "editing from memory after a compaction" — [docs/experiments.md:318-322](docs/experiments.md)

**Design-map (2026-09-15)**
- md headings in the map + one note: design reads whole/ranged per build 0/33, 1/23, 2/21, 18/31, 10/23 vs control f91ade83c0d0's 41 whole reads; design-named tests 58/58, 65/66, 35/36 vs control 1/121 (478 turns). Five asks, one control — "a direction, not a measured rate". Merged in 90d82c3 — [docs/experiments.md:2452-2490](docs/experiments.md)
- Two cap-outs spent 40–55 turns after a green suite reading one DoD row per turn — [experiments.md:2472-2474](docs/experiments.md)

**KV cache**
- KV cache on ninfer is frontier-only: any edit behind the last frontier (compaction, elided image) = full re-prefill (~15 s at 83K) — memory `project_ninfer_admission_reserve.md`; spec-skeleton logged ≈27 min of re-prefill across one build — [labs/spec-skeleton/README.md:289](labs/spec-skeleton/README.md)
- With thinking sent back: 49,361 of 49,378 tokens reused, 90 ms TTFT vs 7,134 reused / 6.7 s without — [docs/experiments.md:2186-2190](docs/experiments.md)

**DSH-shaped summary compaction (lab arm, unreported)**
- `labs/replay/arms_dsh.py`: DeepSeek-Harness-style compaction installed over `build_steps.compact`: fire at 80% of window, keep newest 16% verbatim (round-aligned), replace prefix with one model-written summary (max 8,192 tokens) under 8 headings (request, concepts, files and code, errors, pending, current work, next step, critical context) — [arms_dsh.py:1-22](labs/replay/arms_dsh.py); [dsh_summary.txt](labs/replay/dsh_summary.txt)
- Grid (3 cells × 3 reps) only partly ran 2026-09-11; logs in `~/output/dsh-grid/` (not committed, no README entry): 67a1f6e389f4@49 r1: 94 turns, 84 reads (81 already shown), 72/94 turns re-read, done after 143; r2: 23 turns, 13 reads (13 already shown), 10/23 turns re-read, done after 72; after the r1 summary cut (prompt 79,318 → 28,637) the next four turns were all reads of already-shown files; de0187bf4529 crashed (KeyError 'trimmed' in turn_log); no control numbers for these cells — `~/output/dsh-grid/*.log` (raw logs)

### Inferences
- Across every attempt, the post-compaction re-read looks procedural ("verify before acting/finishing"), not informational: even exact bytes in context (prose or synthetic round) and a model-written summary still produced re-reads of already-shown files at roughly half of turns.
- Size matters more than wording: the 131K window and dedupe/trim reduced cycles; the remaining floor (~60K = newest body of every file) leaves ~55K headroom, roughly one full read of a 130–150K-char game, so a full "verify pass" re-triggers compaction.
- Waste concentrates late (after tier 1/DoD green), where reads are verification loops.

### Gaps
- No battery on the 2026-09-06+ compactor arms vs control on Flash-Next or hosted models; the replay null results are on the local 27B only ("prod's model reads more and repeats more, and has not been probed").
- compaction-floor lab never ran; the dsh arm's results were never written up or controlled.
- No per-read token size distribution exists as a single table; sizes above are scattered anecdotes.

## (c) Seeded / fabricated history experiments

### Takeaway
Two families: (1) the 2026-09-08 "synthetic-read-round" arm (a fabricated assistant `read_file` call + real-bytes tool result after the compaction note) — the model re-read anyway, most of any arm; (2) labs/seeded-corrections (2026-10-20): harness-written rounds placed after the request and pinned through compaction. Failure examples get imitated; a single seeded successful `read_file` round removed ~99% of lost turns at fix starts (0.74 → 0.01 lost turns/branch; later recount 0.84 → 0.42 after an undercount fix). The post-compaction leg of the successful arm has not been run.

### Cited Findings
- Synthetic read round: assistant message with `tool_calls` (id `call_replay_preread`) whose program reads every already-read file within a 60K-char budget, plus a matching `tool` message with the printed bodies and "ran 1 tool: read_file xN"; deliberately well-formed so the chat template accepts it — [labs/replay/arms_reads.py:142-181](labs/replay/arms_reads.py)
- Result: "delivering those same bodies as a completed read_file round … produced the most reads of any arm (19 against a baseline 16)" — [docs/experiments.md:2107-2109](docs/experiments.md)
- seeded-corrections arm 1 (3 rounds: direct read_file call → real no-code reply; `open()` program → real refusal; working `list_files` program → real output), all tool replies produced by real harness code paths, pinned through compaction, not counted as steps — [labs/seeded-corrections/README.md:36-71](labs/seeded-corrections/README.md)
- Arm 1 n=1: "First real turn copied the seeded open()" — [README.md:107-111](labs/seeded-corrections/README.md)
- Arm 1 fix-start battery (200 branches × 5 turns): direct calls 5.3%→3.5%/turn (n.s., p=0.69), open() 9.5%→8.3%, lost turns/branch 0.74→0.59 (p=0.06), reads/branch +1.42 (p<0.0001) — [README.md:118-136](labs/seeded-corrections/README.md)
- Arm 1 post-compaction battery (7 positions, 200 branches): direct calls 18→36 branches (p=0.012), doubled; "failed examples in context get imitated"; verdict idea failure — [README.md:138-162](labs/seeded-corrections/README.md)
- Arm 3 (seeded `list_files()` only): refusals 95→174 branches (p<0.0001); refused programs `open()` the very paths the listing showed — "a file list with no read beside it reads as a filesystem to open"; idea failure — [README.md:217-231](labs/seeded-corrections/README.md)
- Arm 4 (list → 100-line design read): direct 37→0 branches, refused 95→50, lost 0.74→0.25, reads 2.44→4.92; every refusal `open('design/design.md')` to search the whole design — [README.md:240-255](labs/seeded-corrections/README.md)
- Arm 2 (one seeded `print(read_file("design/design.md", lines=100))` round, real reply): 200 branches: direct 37→0 (p<1e-11), refused 95→2 (p<1e-31), lost turns 0.74→0.01, reads 2.44→3.82 per branch; prompt 4,264 vs 1,888 tokens; "Post-compaction leg not run yet" — [README.md:257-270](labs/seeded-corrections/README.md); first attempt was an implementation failure (seed indexed `["content"]` and showed a TypeError) — [README.md:198-203](labs/seeded-corrections/README.md)
- Correction: refusal counter missed import refusals; recount at fix starts: ctrl 0.84 lost/branch, read seed 0.42 (77 of 83 import refusals = a dead `import subprocess`), list→read 0.47, open-shim real files 0.23 — [README.md:164-190](labs/seeded-corrections/README.md)
- Motivation data: direct-call rate is 2.36% on the first turn after a compaction vs 0.71% overall (13,416 turns) — "highest where the context holds few or no earlier python calls" — [README.md:20-32](labs/seeded-corrections/README.md)
- Seeded rounds are lab-only (installed in a branch `install()`, nothing in src/); pinning needed because `rounds()` treats everything after `history[0]` as trimmable — [README.md:62-67](labs/seeded-corrections/README.md)
- Related harness-injected (non-fabricated) messages: nudges as user messages ([build_steps.py:32-49](src/maestro/codegen/build_steps.py)); the cut-off nudge exchange itself inflated a replay from 1,934 to 14,160 generated tokens (n=4) — "the telling is what carries it" — [docs/experiments.md:2079-2085](docs/experiments.md); the no-write-streak nudge ended loops but lost bug fixes, not shipped — [experiments.md:2246-2282](docs/experiments.md)
- Interrogation of a replayed transcript: the model called its own whole-design reading "cross-reference anxiety", "reading felt like progress"; its proposed reading map, placed as asked, did not stop the read — [labs/spec-skeleton/README.md:708-714](labs/spec-skeleton/README.md)
- Related standing law: "never show the model an encoded rendering of something it will be asked to reproduce" (JSON-escaped reads caused 17/32 turns of a failing-edit loop; raw `<file>` view: 6 steps, zero failed edits) — memory `project_escaped_read_view.md`; commit 8b35aa0

### Inferences
- The model does not appear "confused" by harness-written turns; it treats them as its own precedent and imitates them — good examples help, bad examples are copied. A fabricated read round satisfied neither an information need nor the "verify" procedure.
- The seed that worked is a real tool output from a real code path; that design (real strings, well-formed ids, pinned through compaction) is the house pattern for any future synthetic-history arm.

### Gaps
- No experiment has fabricated a post-compaction read of the files the model is *about to* read (predictive pre-read) beyond the "all already-read files" synthetic round; no measurement of whether a pre-read of the right 1–3 files (vs all) changes behavior.
- Post-compaction leg for the read seed and open-shim is pending; open-shim full-build battery started 2026-10-20 17:00 EDT, no result yet — [labs/open-shim/README.md:249-253](labs/open-shim/README.md)

## (d) JEV decision model and next-read prediction

### Takeaway
JEV-27B-VL is a calibrated "System One" decision model (LoRA + readout head on Qwen3.8-27B) that answers typed questions (choice / noul / score) over a text (or image) state in one forward pass, ~68 ms per read serial on SGLang, with a >16-option tournament. It is used only for design decisions today; nothing has tested it on file-selection, but its interface (state + question + options → probabilities, `per_question` yes/no lists with `keep_over` thresholds) maps directly onto "which of these files will be needed next".

### Cited Findings
- JEV: `POST /v1/decide {kind: noul|score|choice, state, question, options}` → calibrated probabilities (ECE ~0.02), ~250 ms/row on a PRO 6000 in Nick's harness; vision zero-shot; vendor note: fails on raw motor commands, decompose into simple questions — memory `reference_jev_27b_vl_local.md`
- Prod decide box: serial ~68 ms/read warm, cat frame chain 0.94 s, boot to healthy 71 s with cached weights; `--max-running-requests 1` because co-batching shifted probs up to 0.05; thresholds sit on ~±0.05 kernel noise; keep_over 0.6 — memory `project_jev_decide_box.md`
- Chain executor: `prompt(kind, state, question, options)` renders "[kind] … [state] … [question] … [options]"; choice over >16 options runs balanced groups of 16 then a final; item lists are scored yes/no per item and kept if p > `keep_over` — `~/Documents/gamesummoner-images/contract/decide.py:16, 47-119`
- Whole decide chain ~16–18 s on prod (first prod job 2026-10-19: ~141 s enqueue→answer, 123 s boot, 16.6 s exec) — [labs/jev-on-flash-next/README.md:3-6](labs/jev-on-flash-next/README.md); [labs/decide-openai-shape/README.md:48-52](labs/decide-openai-shape/README.md)
- OpenAI-shape path works: vLLM `/v1/completions` + `allowed_token_ids` logprobs, mean abs diff 0.013 vs SGLang path, 21/22 answers equal; flips only on items near keep_over — [labs/decide-openai-shape/README.md:40-58](labs/decide-openai-shape/README.md)
- JEV context: 131K ctx / ~80K pool in snapshot build — memory index entry `project_jev_snapshot_build`
- Cheaper candidate qev-0.8b (3.5 ms p50 on L40S per its card) failed as a design-decision replacement on runs 1–2; card warns "weaker on long inputs" — [labs/qev-decide/README.md:3-26](labs/qev-decide/README.md)
- Planned: JEV head on Flash-Next hidden states so decide runs on the llm box (needs Basalt to return hidden states) — [labs/jev-on-flash-next/README.md](labs/jev-on-flash-next/README.md); decide + image co-tenancy planned — [labs/decide-image-cotenancy/README.md](labs/decide-image-cotenancy/README.md)
- jev-play-probe (JEV judging before/after screenshots) closed stale 2026-10-18, no write-up — [labs/jev-play-probe/README.md:124-126](labs/jev-play-probe/README.md)

### Inferences
- Ranking N candidate files for "needed next" would be N noul reads (or one tournament choice) at ~68 ms each on a warm box: ~1–2 s for a 20-file game, negligible next to a build turn — but the state would be the compacted transcript (tens of K tokens), and per-read latency was measured on short design states, so long-state latency is unmeasured.
- Running it requires a warm decide box during builds (today it is cold-booted once per game, ~120 s) or co-locating on the llm box (planned, unproven).
- Calibration was trained/validated on JEV's own tasks; whether it transfers to code-navigation questions is untested (qev's failure shows calibration does not automatically transfer).

### Gaps
- No experiment has asked JEV (or any model) to predict next reads; no ground-truth dataset exists, though turn logs (`turns.jsonl`, `reads.json`, `TurnRecord.reads`) contain every post-compaction read and could label one.
- JEV latency on a ~40–60K-token state not measured.
