# basalt-batch

Status: done
Control: Basalt as configured (`/var/lib/models/basalt/basalt-iq3s.json`, no `batch`), `llm.slots`
unset, so the local llm worker sends one job at a time.

## Purpose

The open-shim full-build battery runs a control and an arm build side by side, but `local_gpu.py`
starts the llm worker with `WORKER_SLOTS = llm.slots` (default 1) and Basalt runs without `--batch`,
so the two builds take turns: 33 turns took 5.9 min of inference alone, 6.9 and 8.2 min paired.
Basalt has `--batch N` ("up to N requests decode together in batch slots, 2..8"). Nick, 2026-10-20:
"I'd rather we fix our slowness", but test before committing, and test n = 2 vs 4 vs 8.

## Hypothesis

Aggregate decode tokens per second rise with N while per-request speed falls; each batch slot's
session comes out of the expert cache, so past some N the misses eat the gain. Measured: aggregate
completion tok/s on a warm second round of N real build conversations at once (≤200K chars of
history each, build.txt system, python tool schema, temperature 0.7, reasoning xhigh, 2048 max
tokens), N = 1 (two requests in sequence), 2, 4, 8. Idea failure: N = 2 aggregate not above N = 1.

## Setup

`bench.py`: per N writes `"batch": N` into the Basalt config (backup at
`/var/tmp/open-shim/basalt-iq3s.json.bak`, restored on exit), unloads through llama-swap, loads
on the next request, then a cold round and a measured warm round. The open-shim battery is paused
for it (`local_gpu.py auto` stopped; its builds wait on their next llm job).

    python3 bench.py 1 2 4 8

## Log

**2026-10-20, battery n = 1, 2, 4 (8 not run).** `results.jsonl`.

| batch | requests | aggregate tok/s | per request tok/s | cold prompt read |
|---|---|---|---|---|
| 1 (sequential) | 2 | 180.7 | 203.8, 125.3 | 19.8 s, 12.1 s (59K, 54K tokens) |
| 2 | 2 | 125.1 | 104.8, 47.4 | 16.8 s, 6.0 s |
| 4 | 4 | — | — | one 59K prompt still reading after 205 s |

At n = 4 Basalt's `/metrics` showed `expert_cache_mib` 6815 (3479 slots), 1.3 GB VRAM free: the
four slots' sessions took the expert cache, so most experts read from host RAM over PCIe; slot 0
was at 30K of 62K prompt tokens after 205 s. Stopped there (n = 8 has less cache still); config
restored from the backup. Idea failure: on this sparse model at IQ3_S on one 5090, batching
loses throughput from n = 2 (−31% aggregate). Two requests route to different experts, so a
batched step loads near the union of both sets, while every slot shrinks the cache that holds
them. A dense model shares every weight across the batch; this one shares little. One round per
N; the n = 2 drop and the n = 4 collapse are large enough not to need more.

**2026-10-20, correction: the n ≥ 2 rows ran the wrong configuration.** Source read (Basalt
`generate.cpp`, `serve/config.py`, `expert_source.cpp`): `bench.py` set engine `batch`, which
gives every slot the whole `max-context` (`generate.cpp:3105`, `slot_cap.assign(o.batch,
o.max_context)`); only the server's `parallel` option splits the context between slots
(`serve/config.py:151-166`). And `vram-elastic` turns elastic KV off (`generate.cpp:3010`), so each
slot backs all 262144 cells at startup. The expert cache is one cache shared by every slot, sized
from what is left after the sessions (`generate.cpp:3089-3090, 3171-3180`); on one GPU slot 0 is
the solo session, so N sessions, not N+1. A 262144-token int8 session ≈ 3.7 GiB + 0.2 GiB draft,
so expected cache ≈ 19.3 GB at n = 1, 15.3 GB at n = 2, 7.3 GB at n = 4 (measured 6815 MiB). The
n = 4 collapse was KV sizing, not the model. Experts are deduplicated within a decode window
(`expert_source.cpp:1465-1480`), but a window holds at most 8 rows (`generate.cpp:6742`), shared
between the slots' tokens and their speculative drafts, so batching trades one request's draft
rows (which share experts) for another request's rows (which share few): a real cost that equal
cache would not remove. Open: the fair run is server `"parallel": 2` with no engine `batch` (each
request capped at 131072, the builds' n_ctx; cache ≈ 19.1 GB). Not run yet; waits for the GPU.

**2026-10-20, rerun with server `parallel` (the fair arm).** Battery paused again. `bench.py` now
sets `server.parallel` (context split, 131072 per slot at 2) and logs `expert_cache_mib`. Two
rounds each, alternating:

| parallel | expert cache | aggregate tok/s | per request tok/s |
|---|---|---|---|
| 1 | 19447 MiB | 186.7 | 192.5, 175.1 |
| 2 | 19083 MiB | 153.8 | 87.5, 81.8 |
| 2 | 19078 MiB | 182.5 | 142.3, 72.2 |
| 1 | 19466 MiB | 183.2 | 196.6, 148.9 |

Cache now equal (−2%), so the n = 4 collapse is explained and fixed. Aggregate: parallel 2
mean 168 vs parallel 1 mean 185 tok/s, break-even at best, −9% on average; each request decodes
at about half speed. That is the draft-row cost from the correction: a step's 8 rows split between
two requests' tokens and drafts instead of one request's well-accepted drafts. Rounds were short
(~500–1300 tokens per request), so ±10% is noise, but no round showed a gain.

## Outcome

Idea failure (2026-10-20), on the corrected arm: with the cache equal, two parallel requests give
no more aggregate throughput than one at a time on this card (168 vs 185 tok/s) and halve each
request's speed, because batching spends speculative-decoding rows on a second request whose
experts barely overlap. Keep Basalt at one request at a time and `llm.slots` unset. Basalt's
README misdescribes `--batch` slot contexts on one GPU (each slot gets the whole max-context; only
`parallel` splits it).
