# Basalt UD-Q4_K_XL on one RTX PRO 6000

Status: done

Question: is Basalt + the Unsloth UD-Q4_K_XL pack of Qwen3.8-Flash-Next viable on one RTX PRO 6000, and how fast?
Prod today is Pennyroyal SGLang on the same card (203 tok/s short, ~100 at 54K, 428 aggregate at 4 concurrent
short-context, conc 4 collapses at warm context).

Box: EC2 g7e.2xlarge on-demand, us-east-1b, $3.36/hr (spot refused in eu-north-1, us-west-2 and us-east-1 on
2026-10-15), DLAMI Ubuntu 24.04, driver 595.91, CUDA 13.2. `userdata.sh` builds Basalt (jesdga95/basalt dee7ac9) and
pulls `Qwen3.8-FN-UD-Q4_K_XL.basalt` (107 GB in 214 s). `bench.py PARALLEL [SPEC]`, prompt `longctx.json` (the
same ~30K prompt as the local IQ3_S bench).

## Log

2026-10-15. The whole Q4 pack fits on the card: 81-84 GB VRAM, every one of the 24,576 experts resident, ~22 GB
host RAM. Startup 60-73 s.

| | tok/s |
|---|---|
| 1 stream, 30K context, spec 7 | 276-282 |
| 1 stream, short prompt, spec 7 | 239-244 |
| 1 stream, spec 0 | 155-160 |
| 30K prompt read | 4.5-5.3 s |
| 2 concurrent, spec 0 (patched) | 197 aggregate, 105-108 per stream |
| 4 concurrent, spec 0 (patched) | 207 aggregate, 61-88 per stream |
| any concurrent, spec 7 | fails |

Two faults in Basalt's concurrent (batch) path:
1. Every expert resident: the verifier records the zero-doorbell graph, and the solo host loop skips the
   per-layer doorbell waits for it, but the batch host loop (`run_slot_segs`) always waits for doorbells the graph
   never rings: "verify batch: timed out at layer 0". Same on Oct 13 upstream (92d9e2f). Local fix
   `patch_batch_ar.py`: record batch windows with the doorbell graph (`ar_off_` forced on around
   `record_window` in `capture_batch`).
2. Concurrent + speculation needs the PLE window kernels, which need the PLE key/value weights in bf16; the
   Unsloth Q4 pack does not have them: "batch segments of several rows need the PLE window kernels". Not patched.

With experts forced partly into RAM (`--expert-cache 8000`), one stream works through the doorbells at 174 tok/s,
so the doorbell path itself is fine on EC2.

2026-10-15, rebuilt Q4 and IQ3_S. No one publishes a Basalt pack with a BF16 PLE key besides jesdga's GSQ-RCO
packs (the IQ3_S pack has `ple_key` BF16; the UD-Q4_K_XL pack keeps it Q8_0 because the converter lists Q8_0 as a
native key form). `rebuild.sh` reconverted UD-Q4_K_XL from Unsloth's GGUF with `NATIVE_PLE_KEY = {"Q2_0"}`, same
inputs as the published pack (--compat-bf16, mmproj, mtp, profile, draft vocab): downloads ~2 min, convert 411 s,
`ple_key` Q8_0 -> BF16 (max abs err 0.0016). All runs below on the batch patch, speculation on (spec 7).

| | Q4 rebuilt | IQ3_S |
|---|---|---|
| VRAM | 84 GB | 57 GB |
| 1 request, 30K context | 254-292 | 342-356 |
| 1 request, short prompt | 241 | 306 |
| 2 at once, aggregate (per stream) | 280 (152-154) | 374-377 (192-216) |
| 4 at once, aggregate (per stream) | 228 (64-107) | 224 (87-182); rerun 102, streams stopped early |

Open: with `--parallel` > 1 the prompt cache does not hit between turns: the same 30K prompt again, and the next
turn, take 3.3-4.0 s to first token where the single-slot server takes 0.1 s. The 2- and 4-at-once runs include
those re-reads, so their aggregates are pessimistic for the decode alone; for a build, each turn would pay the
re-read too.

2026-10-15, decode scaling (`conc.py`: K simultaneous short-prompt requests, 600 tokens each, one `--parallel 8`
server, patched Basalt). Aggregate tok/s (per stream):

| at once | Q4 rebuilt spec 7 | Q4 rebuilt spec 0 | IQ3_S spec 7 | IQ3_S spec 0 |
|---|---|---|---|---|
| 1 | 239 | 158 | 305 | 192 |
| 2 | 264 (139-146) | 202 (104-108) | 343 (178-195) | 245 (127-134) |
| 4 | 337 (89-91) | 320 (83-85) | 445 (118-122) | 325 (58-118) |
| 8 | 425 (56-59) | 424 (56-58) | 534 (72-76) | 532 (71-75) |

Speculation and batching spend the same headroom: spec 7 is worth 1.5x alone and nothing at 8 at once, where both
settings meet. Without speculation the MoE scales 2.7x at 8 (Q4), well short of linear (each request reads its own
experts). 2 at once barely beats 1 with speculation on (+10% Q4, +12% IQ3_S); the patch's per-layer host doorbells
(48 per window, nothing for the CPU to do) are a likely part of that and are unmeasured.

Prompt re-reads with `--parallel` > 1, cause found in `serve/engine/process.py`: a slot is reused only when what
it holds is an exact prefix of the new prompt (`pick_slot` / `_resumes`); the solo path keeps turn-boundary GDN
checkpoints and resumes from the longest match. An agent's next turn never matches exactly (the reply comes back
re-rendered, thinking dropped), so every turn re-reads the whole conversation in parallel mode.

2026-10-15, second box (i-04e72322e90ed8fab, us-east-1b on-demand). `userdata2.sh` rebuilt two Q4 packs (BF16 PLE
key; and the same with jesdga's tuned MTP layer, `--mtp-dense`), converts 360 s each, both in
s3://gamesummoner-models-385588571625/basalt-test/packs/ (upload 107 GB in 137 s). Tests from `run_all.sh`:

- Worker needs (`compat.py`): tool call returned as `tool_calls` (finish `tool_calls`), thinking split into
  `reasoning_content`, a screenshot turn described correctly.
- ~92K context (`longturn.py`), one request at a time:

| | Q4 | Q4 tuned MTP |
|---|---|---|
| cold read, 91.6K tokens | 12.6 s (~7.3K tok/s) | 12.3 s |
| decode 2048 tokens at 92K | 259 tok/s | 270 tok/s |
| next turn (reply + new message) | 0.69 s, 268 tok/s | 0.11 s, 291 tok/s |
| history changed at the last reply | 0.13 s | 0.15 s |

- Seven conversations of 61K, turns round-robin on one engine (`interleave.py`, `--conversation-cache-mib 32000
  --conversation-cache-slots 16`): first reads 8.0-8.6 s each; every later turn 0.30-0.54 s (one 1.17 s), so
  every switch restored its parked cache.
- Boot from S3 (`boottime.sh`): pull 107 GB to instance NVMe 204 s, Basalt ready 62 s, 267 s total.

Interleave detail (engine log): parking a 61K-token conversation takes 1.29 GB of RAM (~21 KB/token) and 0.55-0.91 s;
the next turn's first token still came 0.30-0.54 s after the request. 32 GB holds ~25 such builds, ~15 at 100K.

VRAM lending (`lend.py`, Q4, 30K context): `/v1/vram` refuses with `--resident-experts` on a 64 GB host ("not with
the resident low-RAM mode": RAM holds only the 15 GB complement, so evicted experts would have no source). With
`resident-experts` off and `--mmap-experts` (experts paged from the local NVMe file; startup 35 s, decode 270-274
tok/s with all on the card, against 287 resident):

| GPU free | expert cache on card | decode |
|---|---|---|
| ~16 GB (nothing lent) | 73.5 GB, all | 270-274 tok/s |
| ~20 GB (lend 20000) | 68.1 GB | 217 tok/s |
| ~30 GB (lend 30000) | 58.4 GB | 178 tok/s |

Give-back 0.0 s, take-back 0.6 s (20 GB) and 1.6 s (30 GB); speed fully back after take-back.

2026-10-15, real build. The control plane, llm image and worker stay local (the worker token never leaves the
machine); the image's engine URL is an SSM port-forward (`aws ssm start-session ... AWS-StartPortForwardingSession`,
plugin unpacked to ~/.local) from :8211 to Basalt on the box (tuned Q4, `--parallel 1`, conversation parking 32 GB /
16). A tiny request through the tunnel round-trips in 77 ms. Ask: the fridge, with the JEV design
`labs/jev-design-decisions/runs/fridge/design.md` (the one built overnight on the local 27B).

Run ec9da8853890 failed at step 30 (258 s): the harness budgets max_tokens against n_ctx 131072 with its own count,
Basalt counted the same prompts ~1.5K tokens higher (103,039 + 28,540 > 131,072) and returns 400 rather than
trimming. Basalt restarted with `--max-context 262144` and `fit-max-tokens` (prod Penny runs 524K, so it never
meets this); the worker drained when the engine went away and the image decommissioned with it, both restarted.

Run 951113d83730: 200 steps (cap) in 1,502 s, against 200 steps in 1,627 s for the overnight local-27B build of the
same design (4711fba111df). LLM time 966 s of the 1,502 (200 jobs, mean 4.8 s, max 70 s); the rest is local tools
and gates. Boots headless with no console errors (title "Fridge Escape", level select, settings). Not yet played.
Served at http://127.0.0.1:8131/index.html.

Where run 951113d83730's 1,501 s went (job timestamps from the jobs table, tool calls from turns.jsonl): LLM 969 s
(64%); between turns 434 s (29%), of which play() 427 s over 97 turns (4.4 s mean) and every other tool 7 s; queue
pickup 98 s (7%, ~0.5 s per job: the worker polls every 1 s).

2026-10-15, both non-LLM costs traced to causes and fixed on prod. Pickup: the worker split (gamesummoner-workers
b05b6db, Sep 17) claimed with `wait_seconds: 0` and slept 1 s, undoing the 50 ms long-poll (b8e218f). Prod llm
claim delay was median 0.017-0.032 s Aug 23-Sep 12, 0.580 s (p90 1.000 s) on Oct 5. Fixed in workers 61d3abb (2 s
long-poll, wake on slot free), images 85a3f59, RunPod tags llm-v23/image-v15/mesh-v24/video-v7 (worker layer over
the prod tags); the EC2 AMI still carries the old worker. Play: Chromium launch is 0.03 s, not the cost; every play
paid the error gate's 3 s settle sleep in `_open`. Prod gap after a play turn: median 6.1 s (Oct 5, 1 build), 5.8 s
with p90 13.7 s (Oct 7, 5 builds sharing the droplet CPU); 1 kill and 1 crash in 257 calls. Trivial play 3.85 s ->
0.80 s without the settle; ai-agent-test bddaea6, deployed. Confirm both with the next prod build.

## Outcome

Basalt replaces Pennyroyal on the prod RTX PRO 6000s (Nick, 2026-10-18). At one stream it is faster:
239–244 tok/s short and 259–282 at 30–92K context (Q4, speculation 7) against Pennyroyal's 203 short
and ~100 at 54K, and it boots in 267 s from S3 against ~435 s. The weights differ (Unsloth
UD-Q4_K_XL rebuilt with a BF16 PLE key, against Pennyroyal's NVFP4), and no game has been compared
across the two in one session. Nick played the fridge build (951113d83730): 4/10, "the same quality
as games out of pennyroyal"; its faults are the build's (a fridge door in front of the camera,
yaw-only look), not the quant's. Before cutover: the batch-path fix is a
local patch (`patch_batch_ar.py`), not upstream; `--parallel` > 1 re-reads the whole conversation
every turn, so serve `--parallel 1` with conversation parking; set `--max-context 262144` and
`fit-max-tokens` (Basalt counts ~1.5K tokens more than the harness); the EC2 AMI still carries the
pre-61d3abb worker.
