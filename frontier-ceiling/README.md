# frontier-ceiling

Status: done
Control: local Flash-Next build 524b1c3efa1c on the same ask, code and day (the planned prod
control, launch-battery 3e4f28885cfd, never finished).

## Purpose

Google Playground (Gemini + Nano Banana + Lyria) beats our games on coherence, sound, art and feel
(Nick, 2026-10-07, playing its gallery). We have never measured how much of that gap is the model
and how much is the harness. The 2026-08-28 design transplant arm showed a stronger designer
lifts a weaker builder (Flash-Next designs on local 27B, 10/10 gated), so model strength is a live
lever. A frontier model in the llm seat gives the ceiling: if the harness with Opus 5.5 still makes
a bad game, the gap is the harness; if it makes a great one, the gap is the model and the
question becomes which model we can afford and run.

## Hypothesis

Only the model behind the llm queue changes: Claude Opus 5.5 via the Anthropic API instead of
Flash-Next. Image, mesh and decide queues stay on their usual engines. Measured per game: runs or
crashes, done vs capped, steps, API cost, and Nick's play verdict on coherence, sound, art and feel
against the Flash-Next game for the same ask.

Expected: done well under the cap, fewer steps, and a game Nick rates clearly above the Flash-Next
control on coherence and feel. Art is unchanged by construction (same image models), so any art
lift comes only from better prompts to them.

Idea failure: an Opus game that plays about as well as the Flash-Next game. That says the ceiling
is the harness, prompts or art, and a bigger model is not the lever.

## Setup

Engine: `anthropic_engine.py` in this folder, an OpenAI-chat-shaped server on :8091 that
translates each canonical request to the Anthropic Messages API (`claude-opus-5-5`, adaptive
thinking, effort mapped from `llm.reasoning`) and the response back. The stock llm contract server
(`gamesummoner-images/local/llm/server.py`) and the stock worker sit in front of it, so the control
plane, queue and worker are unchanged.

Ask, run 1: `roguelike deckbuilder where you're a wizard cat climbing a tower` (launch-battery
control 3e4f28885cfd).

Run from the repo root with the control plane up (`venv/bin/python run.py`) and the key in
`~/.anthropic_key`:

    labs/frontier-ceiling/run.sh            # MODEL=claude-opus-5-5 BUDGET=40 by default
    labs/frontier-ceiling/kickoff.sh "roguelike deckbuilder where you're a wizard cat climbing a tower"

The engine stops serving once BUDGET dollars are spent (`calls.jsonl` is the ledger, one costed
row per call). `run.sh` serves the other queues with `local_gpu.auto` minus llm, under the 45G
`safe` cap.

## Log

**2026-10-18 17:03, run 7befe62d67c4.** Implementation fix and rerun. The engine clamped
max_tokens to 64K; the design write asks for 100K. Both write calls (the call and its one retry)
spent all 64K output tokens thinking at xhigh and returned no text (692 s and 686 s, $1.29 each),
so the design fell back to the raw ask and the build started off the prod chain. Stopped at
build turn 3. Engine now passes the harness's max_tokens through up to 128K and logs thinking
and text sizes per call. $2.82 spent.

**2026-10-18 17:31, run aab3407e0edd.** Same ask, fixed engine. Idea-level finding, not an
implementation bug: the write call spent all 100K output tokens thinking (1103 s, $2.01, 113K
chars of summarised thinking, 0 chars of text). The summary shows Opus at xhigh drafting the
whole spec inside its reasoning, section by section (SFX table entries, melody and drum patterns,
then config module by module) and never reaching the answer. The draft itself read strong: it
reconciled HUD elements against locked mechanic tiers, put accessibility settings in tier 1, and
specified audio recipes, particles and a debug API. (Correction: write.txt's layout asks for the
"A. SANITY" section, and the Flash-Next control spec also has one and also rules "No external
assets"; neither is an Opus distinction. What its sanity rows contain is.) Stopped before the retry spent more. $4.83
spent.

**2026-10-18 17:55, run 38bf74c2b1a9.** Deliberate deviation from "only the model changes": the
tool-less design write runs at effort medium (Opus 5.5's default; `--toolless-effort medium`).
Build turns keep the harness's xhigh. The engine now logs thinking/text/tool sizes every 30 s of
a stream. Idea failure for the effort lever: at medium the write still thought without writing,
at the same pace as xhigh (~3.4K summary chars per 30 s; 67.5K chars and 0 text at 650 s). Killed
by hand at ~11 min; the partial call (~60K output tokens, ~$1.2) is billed but not in the
ledger. Effort is not what drives the drafting. Of the xhigh run's 113K-char summary, the first
~40K is design reasoning; from there it is transcription ("Writing melody and drum patterns...",
"Still filling out the sound effects table...", 18 such lines), a private draft the reply would
have to repeat. Saved as `xhigh_spec_thinking_summary.md`.

For comparison, past local write calls on the same prompt and budget: Qwen3.8 27B 54K completion
tokens (37K reasoning) for a 53.6 KB spec in 239 s; Flash-Next 43K completion for a 65.8 KB spec
in 179 s. Both think about two-thirds of the call, then write.

**2026-10-18 18:10, run 628f9b02f79c.** Second deliberate deviation: effort back to the harness's
xhigh, and the tool-less write gets `write_direct.txt` appended as a mid-conversation system
message ("Plan briefly, then write each section in full in the answer itself; do not draft the
document in your reasoning first"). Same 11-minute no-text cutoff, now enforced by the watcher.
If the note fails too, the next arm is an agentic write (a section-to-file tool).
Idea failure: the note changed nothing. Thinking tracked the medium run almost exactly (23K chars
at 216 s, 35.8K at 340 s, 70K at 680 s), 0 text; the watcher stopped the game and killed the
engine at 680 s (~64K output tokens, ~$1.3, billed, not in the ledger). Neither effort nor an
explicit instruction moves Opus 5.5 off drafting a single-shot 25K-token tool-less document in
its reasoning. Running total ~$7.3 (ledger $4.83 plus two killed partials).

**2026-10-18 18:35, run 7dc4963327ff.** Agentic write, built inside the engine
(`--agentic-write write_agentic.txt`): a tool-less request is served by an inner loop that gives
Opus `write_section(markdown)` and `done()`, saves each section by its heading line (a repeat
heading replaces it), and returns the stitched sections as the one text reply, so the design
stage and its contract are untouched. 32K output tokens per inner turn, 40 turns, 1500 s. Effort
is the harness's xhigh. Toy checks first: one turn with parallel calls, and four forced
single-call turns with thinking replayed and cache reads growing (3 cents together).
Not run: the decide box died at boot (Factorio held 3 GB of VRAM; SGLang "state cache is too small
to serve any requests"). JEV is deterministic for this ask (three runs, byte-identical results),
so `replay_decide.py` now answers a pending decide job with a stored result through the worker
API, and `run.sh` takes `AUTO=0` so the GPU queues start only when art is actually needed.

**2026-10-18 18:33, run 8f744002f56e.** Agentic write, JEV replayed, no auto. Idea failure at
xhigh: turn 1 thought for the whole 32K-token turn (352 s, $0.64) and saved nothing; turn 2,
after the "save with write_section" nudge, did the same (319 s, $0.82; its cache read was 0, a
miss worth understanding). Killed at the start of turn 3. Tools alone do not stop the drafting
on this prompt. Running total ~$8.8 (ledger $6.28 plus the two killed partials).

**2026-10-18 18:48, run d086d499669b.** Agentic write plus a task budget the model can see
(`--write-budget 60000`, beta `task-budgets-2026-03-13`), xhigh. Works: turn 1 saved a section in
85 s (8K output tokens); 12 turns, 47.5K output tokens, 467 s, $1.27 for a 54 KB, 13-section spec.
The drafting was never about effort, wording or tools alone: without a visible budget Opus tries
to settle the whole document before committing any of it. The spec read: grid combat on the same
side-on map as the climb, telegraphed intents you can step out of, fall damage with a stomp
payoff, a three-step boss, every number tabled, and an "A. SANITY" section of 20
self-checks (the layout asks for the section) that caught and fixed real contradictions (card count, pigeon pathing, hand keys,
per-floor turn tracking). Two things to watch in the build: it rules "No external assets. All
sprites are pixel arrays in code", so the image models go unused; and T1 alone is 16 cards, 4
enemies plus a boss, 10 hand-made maps, 6 screens and 5 music tracks against a 200-step cap.
Build: capped at 200 steps, ok=False, never called done; $20.70 for 200 calls (ledger $28.26
after it). "Tier completed: 1" printed and its definition-of-done rows checked off by step ~75.
Steps 1–75 were the real work (25 writes, 9 edits, 8 plays, 37 reads). Steps 76–200 were 114
reads, 3 writes and 0 plays: 15 compactions, each followed by re-reading its own large files
until the 131K window filled again. The compaction re-read cycle, not the model, ate the second
half of the budget. No image, mesh or video job was ever enqueued (the spec's "no external
assets" ruling held). Nick's first play verdict, 2026-10-18: "Okay, this is kinda insanely good."
Shared on prod for a small hand-picked survey ("worth $0.99? happy at $5?"), not advertised:
staged and shared locally, then the share folder copied into prod's maestro-shares volume
(https://gamesummoner.com/g/r12ctNpfCeWH, 2026-10-18). Remove with
`docker compose exec -u 0 app rm -rf /app/runtime/shares/r12ctNpfCeWH`.
The other wizard-cat builds were shared the same way on 2026-10-19 (Sonnet's broken one left out):
DeepSeek https://gamesummoner.com/g/jMvHoZ1bCo0h, Gemini Argon
https://gamesummoner.com/g/96sbF0IP6HI4, local Flash-Next https://gamesummoner.com/g/GZ7rQoheqoE9.
The planned control does not exist: prod game 3e4f28885cfd never finished (the front door offers
"build it" / "start from scratch"). A fair control is the same ask built locally with Flash-Next
on today's code, same design chain and harness.

**2026-10-18, control 524b1c3efa1c.** Same ask, local 5090, stock `scripts/local_gpu.py auto`
(fresh JEV, basalt Flash-Next IQ3_S for the design write and the build), no lab engine. Spec
74 KB (Opus 54 KB): same layout, far longer gameplay (~925 lines vs ~175) and contracts (~320 vs
~75). Wall-clock note, not a quality factor: every play() empties the llm queue for longer than
auto's 6 s idle window, so auto releases the card and reloads basalt (~35 s) after each test.
Build: capped at 200, ok=False, 6 compactions, "Tier completed: 1" at ~step 155 (Opus ~75). Steps:
74 reads, 50 plays, 44 edits, 19 writes (Opus: ~150 reads, 8 plays). Title "Wizard Whiskers: Tower
of the Golden Yarn". $0 API; local card time ~70 min. Nick, playing both side by side: "Holy
crap, it's not even close. This one [the Flash-Next control] is awful." Single-run read: on the
same harness, ask and day, the model is the gap.

**2026-10-19 01:13 UTC, run 01a723c0555a.** DeepSeek-V4.1-Flash (`deepseek-flash`) via
DeepSeek's OpenAI-compatible API, through `openai_engine.py` (pass-through: key, model rename,
effort xhigh → high since the API takes low/high/max, costed ledger `deepseek_calls.jsonl`, peak
Mon–Fri 01–04 and 06–10 UTC doubled). JEV replayed. No agentic write or task budget: the spec
call goes straight through, as it does for Flash-Next. $6 cap. Started at peak.
Spec: one call, 294 s, 69K output tokens (41K reasoning), 236 tok/s, 86.6 KB, $0.084 at peak; no
drafting problem. Build: capped at 200, ok=False, 9 compactions, no "Tier completed" printed. One
build turn spent its whole 30K out-cap on reasoning (harness recovered). Steps: 88 reads, 54
plays, 37 edits, 16 writes. Whole game $0.78 at peak prices (201 calls, 346K output tokens),
about 28× cheaper than the Opus game. Title "Mittens the Magnificent — of the Crooked Tower".
Nick: "a more fleshed out game, with lower polish … much better than flash-next locally, but I'd
rate it like a 6.5. It feels so messy. But at a cost of 0.78, that's kinda crazy." His read: Opus
would likely have gone further without the compaction re-read loop.

**2026-10-19 02:07 UTC, battery.** Six games in parallel through `multi.sh`: a router engine
(`router_engine.py`, `routes.json`) picks the backend per ask, since the queue hands any llm job to
any worker. Sonnet 5.5 (agentic write + 60K task budget) on the wizard-cat ask; DeepSeek V4.1
Flash on the other five launch-battery asks. Fresh JEV on the 5090 via `auto.sh`. Games in
`battery_games.tsv`. Peak pricing for DeepSeek until 04:00 UTC. At 02:16 UTC the control
plane was restarted onto today's commits (b5d0788 retires anims and the video queue; 0b2e02f moves
meshes onto the ComfyUI image queue). The old process would have sent mesh jobs to a queue
nothing serves. The kart and bullet-hell builds were around turn 10 and continued on the new code;
the other four were still writing specs and build wholly on it. The earlier wizard-cat runs used
the old code.

**2026-10-19 02:18 UTC, + Gemini 4 Argon on the wizard cat (4ab8e022c0f8).** Through
`openai_engine.py` against Google's OpenAI-compatible endpoint ($2/$10, cached input assumed
$0.20; thinking tokens are billed but left out of completion_tokens, so output is costed as
total − prompt). Argon returns a `thought_signature` in each tool call; the harness keeps tool
calls verbatim, so it survives. The router matches by ask only, so this game's ask carries a
trailing period to tell it from the Sonnet game ("…climbing a tower."), with fresh JEV. Adding the
route restarted the multi stack once (in-flight calls retried by the harness); the router now
re-reads routes.json on change. Casualty: the first Sonnet wizard cat (9a200d082d18) took four
server errors in a row across the two restarts (control plane, then the stack) and the harness
stopped it at turn 12 ("stalled: 4 turns the server could not read"). Rerun as 7e5d092ad1bc with
fresh JEV; ~$0.80 of Sonnet lost. The five DeepSeek builds rode through.

**22:37 local, Sonnet build turns.** The Sonnet rerun drafted in its reasoning on build turns too:
a 30K-token turn of pure thinking cut off, then a second one heading the same way (Opus did this
once in 200 turns). Added `--turn-budget 24000` to the Claude engine (a task budget on every
request with tools; the API counts it per request) and restarted the stack. The restart killed
builds again: while the stack went down, still-living workers claimed jobs, hit the dead contract
server, and reported failures, so Sonnet hit "stalled: 4 turns the server could not read" and
Gemini (three failures) was stranded with no follow-up job. Recovered with `POST
/api/games/<id>/resume`: Gemini re-driven in place at turn 16; Sonnet, already finalized, got a
fresh build over its on-disk files and spec. Lesson: pause the builds (`POST /pause`) before
touching the llm stack.

**Battery results (builds).**

| Ask | Model | Steps | Done? | Tiers claimed | Cost | Title |
|---|---|---:|---|---|---:|---|
| kart (3D) | DeepSeek V4.1 Flash | 200 | cap | — | ~$0.63 avg | Bonbon-9: Taffy Toot's Gobstopper Run |
| farming | DeepSeek V4.1 Flash | 200 | cap | — | 〃 | Lulla Grove |
| mystery | DeepSeek V4.1 Flash | 200 | cap | — | 〃 | NIGHTJAR — a murder on the 23:40 to Verrin |
| bullet hell | DeepSeek V4.1 Flash | 200 | cap | T1 | 〃 | HIVE WARDEN — Defend the Comb |
| zombie | DeepSeek V4.1 Flash | 200 | cap | — | 〃 | CHOMP! |
| wizard cat | Sonnet 5.5 (per-turn task budget) | 9 | done | T1 | ~$1.30 rerun | Mewlin |
| wizard cat | Gemini 4 Argon | 36 | done | T1–T4 | $2.13 | Claws & Cantrips: Spire of the Red Dot |

DeepSeek's five came to $3.14 together. Sonnet's 9-step build is shaped by the per-turn task budget,
which it read as the budget for the whole build and wrapped up ("incomplete against the spec").
Argon averaged 43 s and ~3.9K output tokens per build turn against DeepSeek's 3.6 s and ~590;
its claim of all four tiers in 36 steps is unverified until played. The error gate's checks
(screenshot probe, play-probe turns) carry no ask, so a catch-all route sends them to DeepSeek.
Argon's play gate passed after one fix round (46 steps, ok=True).

**Nick's play verdicts (2026-10-18).**

| Game | Model | Score | Notes |
|---|---|---:|---|
| kart | DeepSeek | 6.5 | a bit broken, not badly: karts appear late though you can race; track runs backwards |
| farming | DeepSeek | 7 | the spirit and bones are there, but severely lacking |
| mystery | DeepSeek | 4.5 | the most interesting and the style is cool, but the writing kills it; unclear there is a valid mystery |
| bullet hell | DeepSeek | 8 | cyber hive with traps and upgrades; easy, good, not amazing |
| zombie | DeepSeek | 5 | "a fever dream" in its organisation; would have benefited from worldclaw |
| wizard cat | DeepSeek (earlier) | 6.5 | fleshed out, messy |
| wizard cat | Gemini 4 Argon | ≤5.5 | not finishable, despite claiming all four tiers and passing the play gate |
| wizard cat | Sonnet 5.5 | — | broken, not graded (the per-turn task budget confound) |
| wizard cat | Opus 5.5 | **9** | "kinda insanely good"; the first game from any run that approaches (but does not pass) a human-made, or at least human-in-the-loop, game at this size and cost |

DeepSeek V4.1 Flash averages ~6.25 over six asks at ~$0.65 a game, well above local Flash-Next
("awful") and far below Opus. Argon's self-report and the gates both said done; play said
unfinishable (gates detect broken, not bad). Across every game: the audio is bad. Nick: let the
models write their own sound (planned: labs/model-owned-audio).

## Outcome

The model is the gap. On the same harness, ask and code, Opus 5.5 built a game Nick scored 9, the
first GameSummoner game to approach (not pass) a human-made or human-in-the-loop game at this size
and cost, where local Flash-Next built one he called awful. No cheaper model closed it: DeepSeek
V4.1 Flash averaged ~6.25 over six asks at ~$0.65 a game, and Gemini 4 Argon built an unfinishable
≤5.5 for $2.13. Sonnet 5.5 went ungraded (a per-turn task budget broke its build).

What carries beyond the scores:

- Claude Opus/Sonnet 5.5 draft a whole tool-less long document in their reasoning and never write
  it, whatever the effort, an explicit instruction, or section tools. A visible task budget fixes
  it (the agentic write plus `--write-budget 60000`: Opus spec $1.27 in 8 min). A per-turn task
  budget on build turns is read as the budget for the whole build and makes the model quit.
- The compaction re-read cycle cost Opus steps 76–200 (~$12 of ~$22); its tier 1 was done by
  step 75. It caps every model whose files outgrow the window.
- Self-reported tiers and the gates are not quality: Argon claimed all four tiers and passed the
  play gate, and could not be finished.
- Audio was bad in every game, across four models: a harness limit (build.txt routes all sound
  through lib/audio.js), not a model one.

Spend: Claude credits ~$33 (ledger $30.36 plus ~$2.5 of killed partials, billed but unlogged),
DeepSeek $3.92, Gemini $2.13. Nothing merged; the engines, router and launchers stay in this
folder. Became `docs/experiments.md` 2026-10-18 "frontier models in the llm seat". Follow-ups
planned: `labs/opus-design-deepseek-build`, `labs/model-owned-audio`.
