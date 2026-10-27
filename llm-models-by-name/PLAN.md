# Plan: LLM models by name

Status: implemented, uncommitted, for Nick's review (2026-10-23). Full suite green (1012 passed),
frontend `tsc -b --noEmit` clean. Docs untouched: the proposed edits are at the end. The agent's
own calls where this plan was silent are marked "(agent's call)" under "Decided", and what to
watch on the prod rollout is under "Rollout risks".

## The idea

Every LLM call names its model at the moment it's made: a build turn asks for `deepseek-4.1`, a
play gate call for `qwen-flash-next`, a design call for `opus`. Settings only say how to bring each name
up. When a job lands for a name with nothing serving it, the infrastructure brings it up. No
setting says which part uses which model.

## Today

- Every LLM job goes on queue `llm`. `jobs.model` is recorded, then overwritten on completion
  with the id the server reports (`db/jobs.py` `complete_job`, `COALESCE(served_model, model)`).
- `/worker/claim` filters on queue only (`db/jobs.claim_job`). Any llm worker takes any llm job.
- One `llm` settings block: `model`, `n_ctx`, `max_tokens`, `reasoning`, `basalt_args`, `slots`.
  Every caller uses it via `get_connector()`.
- The scaler loops over `runpod.queues` (policy + RunPod launch config); `aws.queues` holds EC2
  launch config for the same queue names. An llm pod gets `LLM_MODEL = llm.model` (the alias the
  engine serves under), `LLM_N_CTX`, `BASALT_ARGS_EXTRA`, `WORKER_SLOTS`.
- Every worker row is written by its spawner before the worker claims: the scaler at launch,
  local_gpu at leg start, and the api worker at start. A claim from an unknown worker id gets a
  403 (`api/routers/workqueue.py`).

## Settings

`llm` becomes a map of entries. The key is the name a call asks for. Each entry has exactly one of
`self_hosted`, `api` or `local_gpu`, which says how it comes up. Underscores match the rest of
settings (`job_timeout_seconds`, `network_volume_ids`).

```json
"scaler": {"tick_seconds": 15, "stale_worker_seconds": 180,
           "max_workers": 3, "min_jobs_per_pod": 6, "cooldown_seconds": 300},
"llm": {
  "qwen-flash-next": {
    "model": "qwen3.8-flash-next-basalt",
    "n_ctx": 131072, "max_tokens": 50000, "reasoning": "medium", "slots": 2,
    "self_hosted": {
      "engine_args": "",
      "providers": {
        "runpod": {"template_id": "...", "gpu_type_ids": ["..."], "network_volume_ids": ["..."],
                   "allowed_cuda_versions": ["13.0"],
                   "boot_seconds": 240, "boot_deadline_seconds": 300, "idle_exit_seconds": 60},
        "aws": {"instance_types": ["..."], "markets": ["spot", "on-demand"], "amis": {"us-east-1": "ami-..."},
                "boot_seconds": 180, "boot_deadline_seconds": 300, "idle_exit_seconds": 60}
      }
    }
  },
  "qwen-flash-next-api": {
    "model": "qwen3.8-flash-next", "n_ctx": 131072, "max_tokens": 50000, "reasoning": "medium", "slots": 4,
    "api": {"base_url": "https://...", "api_key": "...",
            "usd_per_mtok": {"input": 0.0, "cached_input": 0.0, "output": 0.0}}
  },
  "deepseek-4.1": {
    "model": "deepseek-v4.1-flash", "n_ctx": 131072, "max_tokens": 50000, "reasoning": "high", "slots": 4,
    "api": {"base_url": "https://api.deepseek.com/v1", "api_key": "...", "effort": {"xhigh": "high"},
            "usd_per_mtok": {"input": 0.0, "cached_input": 0.0, "output": 0.0}}
  }
}
```

The fields every entry has:
- `model`: the id sent in the request body. For a `self_hosted` entry, it's the alias the engine serves
  under (`LLM_MODEL`, unchanged). For an API entry, it's the provider's model id.
- `n_ctx`, `max_tokens`, `reasoning`: per entry now, because windows differ between models.
- `slots`: jobs one worker runs at once.

How each kind comes up:
- **`self_hosted`:** the scaler rents machines for it. `providers` holds one block per provider,
  keyed by the provider's name (`runpod`, `aws`). A missing block means that provider doesn't
  serve this entry, and an unknown key fails settings validation. Engine config (`engine_args`)
  sits beside `providers`, never inside it. `engine_args` replaces
  `llm.basalt_args`.
- **`api`:** the control plane spawns one API worker for the entry at boot (it costs nothing idle).
  `base_url` and `usd_per_mtok` are required. `api_key` and `effort` are optional.
- **`local_gpu`:** local_gpu serves it on the card, e.g. `{"engine_args": "..."}`, or
  `{"llama_swap": "<model>"}` when `local.llama_swap` is set.

Scaling policy and host facts are kept apart:
- **Policy, in `scaler`:** when to add machines, the same for every pool. That's `max_workers`
  (a cap per pool: each model gets up to that many), `min_jobs_per_pod` and `cooldown_seconds`,
  plus `tick_seconds` and `stale_worker_seconds`, which move here from `runpod`.
- **Host facts, in each provider block:** `boot_seconds`, `boot_deadline_seconds` and
  `idle_exit_seconds`, because the same model boots at different speeds on RunPod and AWS.

comfy has the same split. Its facts go into `runpod.queues.comfy` and `aws.queues.comfy` next to
its launch config, and its policy follows `scaler`. Today comfy's cooldown is 90 s and llm's is
300 s, and they become one value. That's safe because booting machines already count as capacity.

The same name means the same model everywhere, while how it comes up differs per box. Prod's
`qwen-flash-next` is `self_hosted` and a dev box's is `local_gpu`. The code doesn't change.

`runpod` and `aws` keep their account-level keys (keys, `cp_url`, `pod_prefix`, `security_group`,
...). `runpod.queues` and `aws.queues` keep the non-llm queues (`comfy`,
`decide`) as they are now. Only llm moves into entries.

Validation happens at the settings boundary (settings load). An entry needs `model`, `n_ctx`, and
exactly one of `self_hosted`, `api` and `local_gpu`. Its name matches `[a-z0-9-]+` with at most 32
characters, because it goes into pod names and EC2 tags.

## Jobs and workers

**Schema:**
- `jobs.model` holds the entry name. It's set at enqueue and never rewritten: `complete_job` drops
  its `COALESCE(served_model, model)` write, and `jobs.served_model()` goes.
- New `workers.model` holds the entry this worker serves (NULL for non-llm queues). The spawner
  writes it in `worker_created`.

**Claim:** `claim_job(queue, worker_id, ...)` reads the worker's row, then takes the oldest pending
job on the queue whose `model` equals the worker's model (`IS`, so NULL matches NULL for comfy and
decide). `queue_has_work` gets the same filter for the long-poll. The workers repo and the pod
images don't change: a worker sends nothing new.

**Enqueue:** an llm enqueue whose model isn't an entry in settings raises `UnknownModel` from
`enqueue_job`. Without that, the job would sit pending forever with nothing able to bring it up.
The build sees it as a failed turn with that text.

**Indexes:** `jobs(queue, model, status, created_at)` for claims and stats.

## Scaler

A scaling unit becomes a pool: `(queue, model)`.
- For llm, there's one pool per entry with a `self_hosted` block, and its provider blocks come from
  that entry.
- For the other queues, there's one pool per key in `runpod.queues` or `aws.queues` (model NULL).
  Its provider blocks are `runpod.queues.<q>` and `aws.queues.<q>`.
- Every pool takes its policy from `scaler`.

Changes in each file:
- **`autoscaler.tick`:** loops over pools instead of `runpod.queues`. Everything per queue becomes
  per pool: stats, live/stale/booting/terminated workers, `_last_scale_up`.
- **Pod names:** `maestro-llm-<entry>-<hex8>` for llm and `maestro-comfy-<hex8>` otherwise. A pod
  belongs to a pool when `name.rsplit("-", 1)[0] == f"{prefix}-{pool}"`. That's an exact match, so
  `qwen` never catches `qwen-flash-next` pods. A prefix match would.
- **`StartPod` env:**
  - `LLM_MODEL` = entry `model`.
  - `LLM_N_CTX` = entry `n_ctx`.
  - `BASALT_ARGS_EXTRA` = `self_hosted.engine_args`.
  - `WORKER_SLOTS` = entry `slots`.
  - `WORKER_QUEUE=llm`.
  - The worker row is written with `model=<entry>`.
- **`Provider.rungs` / `launch`:** take the pool's provider block instead of looking up
  `queues[queue]`. `Ec2Provider.machines` collects regions from every pool's aws block.
- **`policy.decide`:** still pure, with the host facts now per provider:
  - **Boot deadline:** applied per machine. `PodInfo` carries its provider's
    `boot_deadline_seconds`, since the provider is known from whoever listed the machine.
  - **Idle exit:** delivered at launch (`IDLE_EXIT_SECONDS`), once the rung's provider is known.
  - **Boot time in the add-a-machine math:** the slower of the pool's providers' `boot_seconds`.
    The math runs before the ladder picks a provider. Taking the slower one never buys a machine
    the faster boot wouldn't have.
- **`stats` / `db.workers` / `db.jobs`:** the per-queue queries (`queue_stats`,
  `recent_job_seconds`, `live_workers`, `booting_workers`, `stale_workers`,
  `terminated_workers_with_pods`) take `model` too.
- **`pod_refusals` and `pod_request_days`:** get a `model` column, because two entries can ask for
  different cards and their stock-outs are different facts.

"No flash-next hosts, a job lands for it, now there is one" is exactly the existing scale-from-zero
arm (`effective == 0 and pending > 0`), now per pool.

## API worker

`src/workqueue/api_worker.py` (uncommitted) is reworked:
- The control plane spawns one process for each `api` entry: `ApiWorkerProcess(port, entry)`,
  with the entry name passed as an argument.
- The worker serves that entry. It writes its row with `model=<entry>`, sends the entry's `model`
  as-is because the body already carries it, applies `effort`, and sends `Authorization` only when
  there's an `api_key`.
- `engine_body` stops renaming the model, because the connector already put the entry's `model` in
  the body.
- `app.py`'s lifespan starts one per `api` entry and stops them all on shutdown.

## local_gpu

- Its legs are keyed by `(queue, model)` instead of queue. Each `local_gpu` llm entry is its own leg in
  the same one-card rotation, with pending counted per pool.
- The llm leg's basalt gets `--alias <entry model>` and the entry's `local_gpu.engine_args`. Its worker
  row gets `model=<entry>`.
- `_gpu_queues` (added in the uncommitted diff) goes away: an entry that isn't `local_gpu` simply isn't
  a local leg.
- `install_models.py` (the TUI) writes a `local_gpu` entry instead of `llm.model`. `summon_view.py`
  shows pools.

## Code: each call names its model

- **Connector:** `get_connector()` becomes `get_connector(model)`, cached per entry. It reads that
  entry's `n_ctx`, `max_tokens` and `reasoning`, puts the entry's `model` in the body and the entry
  name on the job.
- **Call sites:** the name is a literal at each call, e.g.
  `get_connector("qwen-flash-next").generate_with_tools(...)`, with no per-module constant. At
  landing every call names today's model, so behaviour doesn't change. The calls:
  - `maestro/codegen/design.py`: spec turns and the tool-less design call.
  - `maestro/codegen/build_chain.py`: each turn's enqueue, and the meta log records that turn's
    model.
  - `maestro/codegen/error_gate.py` and `maestro/codegen/play_gate.py`.
  - `maestro/codegen/assets.py` `_merge_prompt`.
  - `maestro/worldgen/llm.py`.
- **`build_steps._n_ctx`:** compaction needs the window of the model the next turn goes to. The
  build turn's model is named once in `build_chain`, which passes it to `build_steps.step`, and
  `step` reads that entry's `n_ctx`.
- **A gate's fix build is a build:** it goes through the same `build_chain` turn call.
- **Changing a call's model mid-build:** the next turn goes to the new model with the same history,
  which is fine because the wire is canonical chat. Compaction reads the new model's `n_ctx` at the
  next turn.
- **Dev boxes:** a box running code that names an entry its settings lack fails that call with
  `UnknownModel: no llm entry 'deepseek-4.1' in settings`. That's the honest failure. A fallback
  entry would be a shim.

## Billing

Today a job debits `exec_seconds × workers.usd_per_hour` from the game's micros
(`billing.estimates.calculate_job_cost`, at cost). An API worker's rate is 0, so as written, an API
job would debit $0.

Fix, in this change: `complete_job` prices a job on an `api` entry from its tokens instead.
- **The formula:** `billed = ceil(input × input + cached × cached_input + output × output)` micros,
  from the entry's `usd_per_mtok`, read through `jobs.model` → entry.
- **Where the tokens come from:** the result's `usage`, before it's elided. `prompt_tokens` and
  `completion_tokens` are standard. Cached input is
  `prompt_tokens_details.cached_tokens` on OpenAI and `prompt_cache_hit_tokens` on DeepSeek, so the
  API worker normalizes it into `usage.cached_tokens` before completing. Build turns are mostly
  cache hits, so getting this wrong overcharges by several times.
- **BYOK on a dev box:** set `usd_per_mtok` to zeros, since the user pays the provider directly.
- **Self-hosted and local_gpu jobs:** unchanged, still exec seconds × rate.
- **The admission reserve** (`QUEUE_MICRO_ESTIMATES["llm"]`, about $0.02 a turn) stays per queue.
  An API turn costs the same order.

## Migration (prod)

Per CLAUDE.md, a committed script, then a commit deleting it: `scripts/migrate_llm_models.py`.
1. Back up the platform db (the existing backup path in `docs/backups.md`).
2. `ALTER TABLE workers ADD model`, and add `model` to `pod_refusals` and `pod_request_days` (the
   last one gets its key rebuilt).
3. Backfill:
   - Set `jobs.model = '<prod entry>'` for llm rows and NULL otherwise.
   - Set `workers.model = '<prod entry>'` for llm rows.
   - Set the stock-out tables' `model` to `<prod entry>` for llm rows.

Nick rewrites prod `settings.json` by hand (it holds secrets I don't touch): the `llm` block
becomes one `qwen-flash-next` `self_hosted` entry, filled from `runpod.queues.llm`, `aws.queues.llm`,
`llm.basalt_args`, `llm.n_ctx`, and so on, and the llm blocks come out of `runpod.queues` and
`aws.queues`. A new `scaler` block takes `max_workers`, `min_jobs_per_pod` and `cooldown_seconds` from
`runpod.queues.*`, plus `tick_seconds` and `stale_worker_seconds` from `runpod`. comfy's boot,
deadline and idle facts are copied into both `runpod.queues.comfy` and `aws.queues.comfy`. Then `compose restart app`.

Order on prod:
1. Pause builds (no llm job in flight).
2. Run the db script.
3. Swap the settings.
4. Deploy.
5. Do one e2e build.

Live pods from before the deploy have no `workers.model` until the backfill, which is why the
script runs first.

## Docs (need Nick's sign-off)

- `docs/local_dev.md`: the `llm` section, the `runpod` and `aws` sections (llm policy moves), and
  the `llm.model` → `LLM_MODEL` paragraph.
- `docs/deploy.md`: "Autoscaler" (pools, pod names, where llm policy lives).
- `docs/architecture.md`: claim matches on model.
- `settings.example.json`: entries.

## Tests

- **Claim routing (`tests/test_workqueue.py`):** data-driven over a table of (worker model, pending
  jobs by model) → which job is claimed, or none. It covers NULL-for-comfy, two entries on one
  queue, and the oldest-first order within an entry. It runs through the real `/worker/claim`
  route.
- **Enqueue and completion:** an unknown entry raises `UnknownModel`, and a known one lands with
  `model` = the entry name, which `complete_job` leaves alone.
- **Token billing:** a table of (usage shape, entry prices) → billed micros. It covers the OpenAI
  and DeepSeek cached-token fields, zero prices, and a self-hosted job still billing by seconds.
- **Scaler (`tests/test_autoscaler*.py`):**
  - Pools built from a settings table: `self_hosted` entries, `api` and `local_gpu` skipped, plus
    the non-llm queues.
  - Pod name to pool by exact match, including the `qwen` / `qwen-flash-next` case.
  - One pool's backlog starts a pod with the right env and worker row, and leaves another pool
    alone.
- **Settings validation:** a table of entries, valid and invalid (none of the three kinds, two of
  them, a bad name, no `model`, an `api` without prices).
- **API worker:** end to end against a fake upstream in a thread. It claims only its entry's jobs,
  the upstream sees the body model, the effort and the auth header (or no header without a key),
  and a 401 completes the job with `Status 401: ...`.
- **local_gpu:** pending per pool chooses the leg.
- **Connector:** `get_connector(name)` takes `n_ctx`, `max_tokens` and `reasoning` from its entry.

## Rollout

1. Code and tests on master, no commit until reviewed.
2. Local proof:
   - A local `qwen-flash-next` entry plus a `deepseek-4.1` `api` entry.
   - Point the build turn call at deepseek and leave the design and gates on qwen.
   - Run one build. Check that each job row's `model` shows the right entry, the card served only
     qwen jobs, and the API worker served only deepseek jobs.
   - Then flip it back.
3. Prod migration as above.

## Decided (2026-10-23)

- comfy and decide stay plain queues.
- Stock-outs are recorded per pool.
- `max_workers` is per pool.
- Policy lives in `scaler`, the same for every pool; boot, deadline and idle facts sit in each
  provider block, under `self_hosted.providers`.
- With two providers, the add-a-machine math uses the slower boot.
- No `served_model`: `jobs.model` is the entry name, period.
- Kinds are `self_hosted`, `api` and `local_gpu`.
- API jobs bill from tokens.
- Each call names its model inline.

### Agent's calls during implementation (2026-10-23)

- **The installer's entry (agent's call, Nick to confirm).** `install.sh` writes
  `llm.qwen-flash-next = {model: <picked llama-swap model>, n_ctx, max_tokens, reasoning, slots,
  local_gpu: {}}`. It keeps the entry's other fields and any other entries, and drops a
  `self_hosted` or `api` block from that one entry. On a fresh install those fields come from
  `settings.example.json`. `install_models.py` reads the saved pick back from the same entry.
  Code names `qwen-flash-next` at every call, so a local user's pick has to live under that name
  even when it is a different model.
- **Entry names allow `.` (agent's call).** The plan's own example `deepseek-4.1` breaks
  `[a-z0-9-]+`. Names are `[a-z0-9.-]{1,32}`, which is still safe in pod names and EC2 tags. Pod
  names are split on `-` only.
- **`pod_request_days.model` is `NOT NULL DEFAULT ''` (agent's call).** It is part of the primary
  key, and SQLite never treats two NULLs in a key as equal, so comfy's daily rows would duplicate.
  A non-llm pool is `''` there and only there. `jobs`, `workers` and `pod_refusals` use NULL. The
  db layer maps between the two.
- **An unknown entry in a build (agent's call).** `get_connector(name)` raises `UnknownModel`
  before anything is enqueued. The build chain catches it and finalizes the build failed with the
  text "no llm entry '…' in settings", instead of failing turn after turn until the 4-turn stall.
  Elsewhere it acts like any exception there: the error gate and `_merge_prompt` fall back, a play
  gate raise settles the run, and the design fails. `enqueue_job` still refuses an llm job for an
  unknown entry, as the plan says.
- **Input tokens (agent's call).** Fresh input is `prompt_tokens − cached_tokens`, because both
  OpenAI and DeepSeek count cache hits inside `prompt_tokens`. The micros are rounded to the nano
  before the ceiling, so float error never bills an extra micro (`billing.estimates.calculate_token_cost`).
- **Per-provider boot deadline on booting rows too (agent's call).** `stale_workers` takes
  `{provider: boot_deadline_seconds}` and checks each booting row against the deadline for its
  `workers.source`. A machine or row whose provider has no block in the pool gets deadline 0, so
  it is reaped.
- **Host-fact defaults (agent's call).** Absent host facts keep the old defaults: boot 150 s,
  deadline 300 s, idle exit 10 s. The `scaler` defaults in `settings_manager` are 15/180/3/6/300.
- **llama-swap (agent's call).** A `local_gpu` entry has no `llama_swap` key. Under llama-swap the
  entry's `model` is the swap model id the request body carries, and llama-swap routes on it.
  `local_gpu.engine_args` is the only key the card reads.
- **local_gpu CLI (agent's call).** `scripts/local_gpu.py llm` drains every `local_gpu` entry, and
  `llm-<entry>` drains one.
- **EC2 block without amis (agent's call).** `Ec2Provider.rungs` returns no rungs for a block that
  has no `amis`, the same as RunPod with no `gpu_type_ids`. That way a block holding only host
  facts never breaks a tick.
- **Admin `/queues` (agent's call).** There is one row per llm entry of every kind (api too, so
  its depth shows), then comfy and decide. Each row has a new `model` field. `workers_max` is
  `scaler.max_workers` only for a scaler pool while a provider is enabled, and 0 otherwise. The
  frontend card shows `Llm · <entry>` and keys rows on queue and model.
- **summon view (agent's call).** One line per llm entry (`llm <entry>`, idle ones included), then
  decide and comfy.
- **API worker (agent's call).** `slots` defaults to 1 like every entry, and the worker id is
  `api-<entry>-<host>-<hex6>`.
- **settings.example.json (agent's call).** It holds one `qwen-flash-next` `local_gpu` entry,
  which is the installer's starting point. The prod `self_hosted` shape is in the proposed doc
  edits below. The stale `sglang_args` key is gone, and so are the env overrides `LLM_MODEL`,
  `LLM_REASONING`, `BASALT_ARGS`, `LLM_SLOTS` and `LLM_N_CTX` in `settings_manager` (the `llm`
  default is `{}`). Nothing in compose or the Dockerfile set them.
- **Connector (agent's call).** The unused `get_context_length()` is removed, and the connector
  carries `entry`, `model_name`, `n_ctx`, `max_tokens` and `reasoning`. `build_steps.step(model,
  …)` takes the entry name first and reads `n_ctx` through `config.llm_models.entry`. The build's
  `turns.jsonl` meta records the entry name as `model`.
- **Migration script (agent's call).** `scripts/migrate_llm_models.py --db <platform.db> --entry
  qwen-flash-next`. It backs up next to the db, as the earlier one-shots did. It also drops the
  old indexes `idx_jobs_claim` and `idx_pod_refusals_queue` and creates `idx_jobs_pool` and
  `idx_pod_refusals_pool`. It was checked against a scratch sqlite built from HEAD's schema: the
  backfill, the rekeyed `pod_request_days`, the new schema applied on top, and `INSERT OR IGNORE`
  on the new key. There is no permanent test, since the script is deleted once prod has run it.

## Rollout risks

- **Settings validate at import.** Any `settings.json` still in the old `llm` shape makes the app,
  scripts and the test suite fail at import with `settings llm.model: an entry is an object`. That
  includes the main checkout's own file. Rewrite each box's file before running this code on it.
- **Old-named llm pods are orphans.** Pods launched by the old code are named `maestro-llm-<hex8>`.
  The new pool `llm-qwen-flash-next` only owns `maestro-llm-qwen-flash-next-<hex8>`, so the scaler
  neither counts nor reaps the old ones. The backfill gives their workers `model`, so they keep
  claiming, idle-exit and self-terminate, but nothing backstops a missed self-terminate. Deploy
  with zero llm pods live (pause builds, let them idle out), or check the console afterwards.
- **Pods launched between the script and the deploy.** The old code writes those worker rows
  without `model`, so they claim nothing and sit outside the pool. Builds are paused, so there
  should be none. If there are, re-run the script's `UPDATE workers SET model = ? WHERE queue =
  'llm'` line by hand after the deploy.
- **The settings swap before the deploy.** For the minutes between them, the old code reads the
  new file. Its `get_connector` falls back to model "default", and its scaler finds no
  `runpod.queues.llm`, so it scales no llm. Builds are paused, so do the two back to back.
- **API retries.** There is no 429 retry yet (out of scope). A bad key fails turns until the
  4-turn stall.

## Open questions

None.

## Out of scope, noted

- Anthropic native API (an `"anthropic": true` flag on an `api` entry) for Opus. Every `api` entry
  is OpenAI-compatible until then.
- When a bad key or 429 fails a turn, the build stalls after 4 failed turns ("stalled: 4 turns the
  server could not read"). Retry with backoff for 429 belongs in the API worker. A follow-up.

## Proposed doc edits (need Nick's sign-off, not applied)

### `docs/local_dev.md`

**Basalt section** (`--alias <llm.model>` and "`--alias` must match `llm.model`"): change it to
`--alias <llm.<entry>.model>`. `scripts/local_gpu.py` passes the entry's `model` itself, and
`local_gpu.engine_args` is appended to the line.

**Remote pods, step 2.** Replace the `llm` = "what the pod serves" sentence and "`max_workers: 1`
per queue" with:

> `llm.qwen-flash-next` = prod's `self_hosted` entry (`model` `qwen3.8-flash-next-basalt`, `n_ctx`
> 131072, `slots` 1, and `self_hosted.providers.runpod` copied from the droplet), plus the
> droplet's `runpod` account block and `runpod.queues.comfy`. `scaler.max_workers: 1` bounds
> spend, and it is a cap per pool.

In step 3 and the EC2 paragraph, the pod names become `maestro-llm-<entry>-*` and
`maestro-comfy-*`. Replace "keep the llm policy block in `runpod.queues` (…)" with "add an `aws`
block under `self_hosted.providers` of the llm entry. Policy is `scaler`'s, whatever the
provider."

**`### llm`.** Replace the section's opening with:

> A map of named entries. The key is the name a call asks for (`get_connector("qwen-flash-next")`,
> named inline at each call), at most 32 characters of `[a-z0-9.-]`. Every entry has `model` (the
> id sent in the request body), `n_ctx`, `max_tokens`, `reasoning` and `slots`, plus exactly one
> of these:
> - `self_hosted`: `{engine_args, providers: {runpod: {...}, aws: {...}}}`. The scaler rents
>   machines for it. Each provider block is that provider's launch config plus `boot_seconds`,
>   `boot_deadline_seconds` and `idle_exit_seconds`. A missing block means that provider doesn't
>   serve it.
> - `api`: `{base_url, api_key?, effort?, usd_per_mtok: {input, cached_input, output}}`. The
>   control plane runs one API worker for it, and its jobs bill from tokens at these prices (zeros
>   for BYOK).
> - `local_gpu`: `{engine_args?}`. `scripts/local_gpu.py` serves it on the card, one leg per entry.
>
> Settings load refuses an entry that breaks any of this. A call naming an entry the box's
> settings lack fails with `UnknownModel: no llm entry '…' in settings`.

The `slots`, `n_ctx` and `basalt_args` paragraphs stay, applied per entry, with `basalt_args`
renamed `engine_args`. `self_hosted.engine_args` reaches the pod as `BASALT_ARGS_EXTRA`.

**`### runpod`.** Drop `tick_seconds`, `stale_worker_seconds` and the per-queue policy keys
(`max_workers`, thresholds, cooldown). `queues.<name>` now holds the non-llm queues only
(comfy): launch config plus `boot_seconds`, `idle_exit_seconds` and `boot_deadline_seconds`.
llm launch config lives in each `self_hosted` entry. Replace the "`llm.model` must be what the
engine answers to" paragraph with:

> A `self_hosted` entry's `model` reaches its pods as `LLM_MODEL` (the alias the engine serves
> under), `n_ctx` as `LLM_N_CTX` (at most 262144), `slots` as `WORKER_SLOTS`, and
> `self_hosted.engine_args` as `BASALT_ARGS_EXTRA`.

**New `### scaler`.** Add:

> Scaling policy, the same for every pool: `tick_seconds` (15), `stale_worker_seconds` (180),
> `max_workers` (3, a cap per pool), `min_jobs_per_pod` (6) and `cooldown_seconds` (300).

**`### aws`.** Replace "Scaling policy is not here: a queue scales by its `runpod.queues` block"
with:

> llm launch blocks live under each `self_hosted` entry's `providers.aws`, and `queues.<name>`
> holds the non-llm ones, each with its own `boot_seconds`, `boot_deadline_seconds` and
> `idle_exit_seconds`. Policy is `scaler`'s. Regions are listed from every pool's amis.

### `docs/deploy.md` "Autoscaler"

- "adds at most one pod per queue" becomes "per pool". Add:

  > A pool is a queue and the llm entry its machines serve: one per `self_hosted` entry, and one
  > per non-llm queue in `runpod.queues` or `aws.queues`. Pods are named
  > `<pod_prefix>-llm-<entry>-<hex8>` or `<pod_prefix>-comfy-<hex8>`, and a pod belongs to a pool
  > by an exact match on its name without the hex.

- In the settings list, `tick_seconds` and `stale_worker_seconds` move to the `scaler` block.
  `queues.<name>` is the non-llm launch config plus its host facts, and the llm entry's
  `self_hosted.providers.runpod` takes the same keys. `max_workers`, `cooldown_seconds` and
  `min_jobs_per_pod` move to `scaler`.
- `boot_seconds`, `boot_deadline_seconds` and `idle_exit_seconds` are per provider. A machine is
  held to its own provider's deadline, `IDLE_EXIT_SECONDS` is set once the rung picks the
  provider, and the add-a-machine math uses the slower of the pool's providers' `boot_seconds`.
- In the `aws` bullet, "Policy stays in `runpod.queues`" becomes "Policy is `scaler`'s, and a
  pool with a block for both providers is served by both."
- `pod_refusals` and `pod_request_days` are kept per pool (`model` column).
- Line 25 / 73 ("so `runpod.queues` … editable", "fill in runpod.queues"): read "the `llm`
  entries and `runpod.queues`".

### `docs/architecture.md` "Queues" / "Workers"

Add under the queue table:

> An llm job carries the name of the llm entry its call asked for (`jobs.model`), and each worker
> row records the entry it serves (`workers.model`, written by whoever spawned it). A claim takes
> the oldest pending job on the queue whose model is the worker's (`IS`, so comfy and decide
> match NULL). An `api` entry is served by an API worker the control plane runs. It calls the
> provider's OpenAI-compatible API and bills its jobs from tokens.
