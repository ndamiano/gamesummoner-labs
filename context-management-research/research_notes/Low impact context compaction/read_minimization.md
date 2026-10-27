# Read minimization and context compression for a self-hosted coding agent

Scope: levers that shrink what file reads and tool outputs bring into context, or keep it from piling up,
ranked for Qwen3.8 Flash-Next (131K window, SGLang/llama.cpp, one RTX PRO 6000 96GB or one 5090 32GB).
Research date 2026-10-20. Many sources are 2026 preprints. Their numbers are author-reported and unreplicated
unless noted. One (Blast Radius) has been withdrawn.

Sources marked "(abstract, from prior knowledge, not re-fetched)" are well-known papers whose headline claims
I recall from their abstracts. I did not re-open them this session, so the report writer should check the
exact figures before quoting them.

## Read shaping: outlines, ranged reads, unchanged-read stubs, dedupe, grep-first

### Takeaway
File reads are the largest single token sink in coding agents: over 70% of tokens in one SWE-bench Verified
measurement. The cheap, engine-neutral levers are:
- an unchanged-read stub (Claude Code ships one);
- deterministic line pruning of tool outputs: up to 92% removed by a 2B pruner, or 35-39% by an in-engine head;
- a ranked symbol map (Aider).

None of these comes with a clean published end-to-end resolve-rate ablation. Pruning hurt Qwen-family
backbones slightly in the one study that tested them.

### Cited Findings
- **Where the tokens go.** File-reading commands account for over 70% of tokens consumed by Mini-SWE-Agent
  with Claude Sonnet 4.5 on SWE-bench Verified. This figure comes from a search snippet of the Blast Radius
  preprint, which has since been withdrawn. — [Blast Radius (withdrawn)](https://arxiv.org/abs/2608.07440)
- **Claude Code unchanged-read stub.** The v2.1.86 changelog says the Read tool "deduplicates unchanged
  re-reads to reduce token usage". The model receives an explicit message, quoted as "Wasted call — file
  unchanged since your last Read." The official tool docs do not describe this. — [docs-gap issue #40123](https://claudeissues.com/issue/40123-docs-read-tool-docs-omit-compact-line-number-output-and-unchanged-re-read-dedupl)
- **Stub failure mode.** The freshness check tracked only edits made by Claude's own tools (Edit, Write,
  NotebookEdit). After an external on-disk edit it served a stale "unchanged" stub. Reported fixed June 2026.
  — [bug #60684](https://claudeissues.com/issue/60684-bug-read-tool-returns-file-unchanged-after-external-on-disk-edits-serving-a-stal)
- **Little left to dedupe on top of that stub.** A third-party read-dedupe MCP server measured −2.6% savings
  (slightly negative) on a real Claude Code session corpus, because the native file-state cache already
  prevents redundant re-reads. This is vendor self-reported. — [Glama MCP listing](https://glama.ai/mcp/servers/ea9d6jki41)
- **Aider repo map, method.** Tree-sitter extracts definitions and references, PageRank ranks files and
  symbols, and a binary search fits as many ranked entries as the token budget allows (within about 15%).
  Each file is rendered as its matching definitions plus parent-scope headers, with the rest elided.
  — [hermes-agent issue #535](https://github.com/NousResearch/hermes-agent/issues/535); [fast.io Aider guide](https://fast.io/resources/aider-token-limit.md)
- **Aider repo map, budget.** Secondary sources disagree. One gives `max(1024, min(max_input_tokens/8, 4096))`,
  8x larger when no files are in the chat. Another says `--map-tokens` defaults to 1,024. I did not verify
  either against Aider's source. — [hermes-agent #535](https://github.com/NousResearch/hermes-agent/issues/535); [fast.io](https://fast.io/resources/aider-token-limit.md)
- **First-chunk selection ("Agents Don't Paginate").**
  - Session logs from a public MCP middleware showed agents never asked for a second chunk of a paginated
    tool response.
  - Setup: 500 SWE-bench Verified tasks, 5 models, an offline single-turn file-localisation probe.
  - A parameter-free keyword scorer raised gold-at-rank-1 from 24.2% to 35.0% (+10.8 pp, p=3.9e-8).
  - Adding four file-metadata signals lowered it by 4.8 pp.
  - Downstream accuracy did not move: per-model deltas were under 3 pp, with inconsistent signs and none
    significant. What mattered was whether the gold item was in the chunk at all, not its rank.
  - [arXiv 2608.26130](https://arxiv.org/abs/2608.26130)
- **Squeez.** A LoRA fine-tune of Qwen 3.5 2B prunes a tool output to the smallest verbatim evidence block for
  a focused query. It reaches 0.86 recall / 0.80 F1 while removing 92% of input tokens. It beats zero-shot
  Qwen 3.5 35B-A3B by 11 recall points and "all heuristic baselines by a wide margin". No downstream agent
  success rate is reported. — [arXiv 2604.04979](https://arxiv.org/abs/2604.04979)
- **SWE-Pruner (original).** Line-level pruning with a separate scoring model, conditioned on a goal-hint the
  agent writes every turn.
  - On Qwen3-Coder-Next it cut tokens 32.7% / 28.7% / 0% (SWE-QA / SWE-QA-Pro / Oolong).
  - SWE-bench Verified resolve rate fell 4.2% on Qwen3-Coder-Next and rose 4.2% on MiMo-V2-Flash.
  - [SWE-Pruner Pro paper](https://huggingface.co/papers/2607.18213.md); [SWE-Pruner arXiv 2601.16746](https://arxiv.org/pdf/2601.16746)
- **SWE-Pruner Pro.** Drops the extra model. An ~18M-parameter head reads the backbone's own last-layer
  hidden states from the prefill it already runs on each tool response, and keeps or prunes each line.
  - Token cuts on Qwen3-Coder-Next: −34.7% (SWE-QA), −39.4% (SWE-QA-Pro), −13.9% (Oolong).
  - SWE-bench Verified: −1.2% on Qwen3-Coder-Next, +3.8% on MiMo.
  - On MiMo, input tokens actually rose 7.4%, and API calls rose on both backbones.
  - Overhead: +15.0% generation wall time.
  - Requirements: a patched SGLang 0.5.10.post1 with hidden-state return, and a head retrained per backbone.
    Training used 22,609 samples labelled by Claude Sonnet 4.6.
  - [HF paper page 2607.18213](https://huggingface.co/papers/2607.18213.md)
- **RTK.** A shell-output filter (filter, group, truncate, dedupe) that claims 60-90% token savings on common
  dev commands. Vendor claim, no task-success data. — [Edgee blog (via search)](https://edgee.ai/blog/posts/introducing-compressor-v2-three-compression-layers-measured-end-to-end-for-a-50-cost-reduction)
- **Read-view format matters (internal).** A JSON-serialized `read_file` view caused a 17-of-32-turn edit loop.
  Switching to an unescaped view brought it down to 6 steps with zero loops. — internal memory
  `project_escaped_read_view.md` (GameSummoner)

### Inferences
- In our harness an unchanged-read stub is the lowest-risk lever. It is deterministic and needs no engine
  change, and it is a bugfix-class change, not a prompt wording change. It must hash on-disk content, not
  track our own writes, to avoid the Claude Code stale-stub bug (the model's game code is also changed by
  `pyexec` and similar tools).
- A Qwen-family backbone lost resolve rate under both SWE-Pruner variants. Together with GameSummoner's
  "quality over compute" stance, that makes learned line-pruning a lab candidate, not a default. Squeez's 2B
  model could share the image or LLM card, but it has no end-to-end result.
- The "Agents Don't Paginate" finding argues against relying on a "read more" affordance. If we truncate, the
  first chunk must already contain the relevant part.

### Gaps
- No published end-to-end ablation of an Aider-style repo map against full reads gives a resolve rate and
  tokens per task. I found none.
- I found no measured token savings for ranged reads or grep-first workflows in isolation.
- I could not confirm Aider's default map budget from its primary source.

## Tool-output pruning in history: observation masking, tool-result clearing, last-N, superseded stubs

### Takeaway
The best-evidenced lever in this whole area is observation masking: replace tool outputs older than M turns
with a placeholder.
- It roughly halves cost on SWE-bench Verified.
- It matches or beats LLM summarization on solve rate.
- LLM summarization makes trajectories about 15% longer.

The catch is that M is harness-specific: 10 in SWE-agent, 58 in OpenHands. Anthropic's tool-result clearing
reports 84% fewer tokens on a 100-turn task.

### Cited Findings
- **Complexity Trap setup.** SWE-agent on SWE-bench Verified (n=500), comparing raw, observation masking with
  M=10, and LLM-Summary (summarize N=21, keep last M=10). — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)

  | Model | Raw (solve / cost) | Masking (solve / cost) | LLM-Summary (solve / cost) |
  |---|---|---|---|
  | Qwen3-Coder 480B | 53.4% / $1.29 | 54.8% / $0.61 (−52.7%) | 53.8% / $0.64 (−50.4%) |
  | Gemini 2.5 Flash | 32.8% / $0.41 | 35.6% / $0.18 (−56.1%) | 36.0% / $0.24 (−41.5%) |
  | Gemini 2.5 Flash (thinking) | 40.4% | 36.4% (−57.1% cost) | 31.4% (−55.4% cost) |
  | Qwen3-32B | 17.0% | 15.0% (−50.9% cost) | 16.0% (−55.4% cost) |
  | Qwen3-32B (thinking) | 23.0% | 24.6% (−9.8% cost) | 24.8% (0.0% cost) |

  Both reduction methods hurt the thinking-enabled Gemini 2.5 Flash.

- **Window tuning.** Masking peaked at M=10 and dropped at M=20 in SWE-agent. In OpenHands, M=10 did not
  transfer, and masking needed M=58 to match LLM-Summary. — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- **Summaries lengthen runs.** With LLM-Summary, Gemini 2.5 Flash averaged 52 turns against 44 for masking
  (+15%). Qwen3-Coder runs were about 15% longer than raw and 13% longer than masking. Critic-enhanced
  summaries lengthened runs further with no solve gain. Summary calls cost 0.65-7.2% of instance cost.
  — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- **Hybrid.** Masking first, then summarizing late (N=43, W=10) cut cost a further 7% against masking and 11%
  against summary on Qwen3-Coder 480B (Verified-50 subset). Reusing N=21 naively made efficiency worse.
  — [arXiv 2508.21433](https://arxiv.org/abs/2508.21433)
- **Anthropic context editing.**
  - On a 100-turn web-search eval, context editing cut token consumption by 84% and let agents finish
    workflows that otherwise ran out of context.
  - On an internal agentic-search eval: +29% performance for context editing alone, +39% combined with the
    memory tool.
  - No dataset size or variance is given.
  - [Claude blog: context management](https://claude.com/blog/context-management)
- **Context editing defaults.** LangChain's middleware mirrors `clear_tool_uses_20250919`. It clears older
  tool results once the conversation passes 100,000 tokens and keeps the 3 most recent.
  — [LangChain ContextEditingMiddleware](https://reference.langchain.com/python/langchain/agents/middleware/context_editing/ContextEditingMiddleware)
- **Reversible eviction (Blast Radius, withdrawn).** Replayed 149 SWE-agent traces.
  - Its policy saved 23.5% median tokens while staying byte-exact reversible. Plain truncation saved 22.6% and
    summarization 41.7%.
  - SWE-agent's native policy collapses observations older than 5 turns into one line. It saves more, but
    irreversibly.
  - 17-26% savings across seven OpenAI models.
  - The author withdrew the paper ("major revisions needed"). Treat as unreliable.
  - [arXiv 2608.07440](https://arxiv.org/abs/2608.07440)
- **Superseded-by-later-write stubs.** I found no study that measures this lever specifically.

### Inferences
- Observation masking is the strongest-evidenced lever in this whole survey. Our own memory notes match it:
  the post-compaction re-read cycle was the #1 cost lever, and re-reading ate half the Opus frontier run.
  — internal `project_compaction_reread_cycle.md`, `project_frontier_ceiling.md`
- The window M must be tuned on our battery. M=10 failed to transfer between two harnesses, so a
  token-threshold trigger (like Anthropic's 100K) may transfer better than a turn count. This is unmeasured.
- The negative result on thinking-enabled Gemini matters for us: Flash-Next runs with thinking on
  (`project_thinking_on_measured.md`).

### Gaps
- There is no public result for masking on a game-building (non-SWE) task, or at a 131K window with thinking
  enabled.
- I found no ablation of "superseded by later write" stubs compared with generic masking.

## Prompt-cache / KV-prefix interaction (SGLang RadixAttention, llama.cpp)

### Takeaway
Any edit to history before the cache frontier forces the KV cache to be recomputed from that point onward.
That cost recurs with every rolling-window mask step. The design answer is **batched, append-only masking**:
mask in large steps, so the prefix stays stable for many turns between rewrites (the hybrid's "N" logic).

### Cited Findings
- **Masking has worse cache behaviour.** The Complexity Trap authors say masking's rolling window has worse
  cache behaviour than LLM-Summary's bounded context. They cite this as why the naive hybrid configuration
  lost efficiency. — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- **Summary calls barely use the cache.** Each summary call processes a unique turn sequence, so cache reuse
  is limited to the system prompt. Gemini cache hits can be up to 10x cheaper than misses.
  — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- **ninfer caches only the frontier (internal).** Our engine reserves prompt+max_tokens at admission, and any
  edit behind the frontier invalidates the KV cache. — internal `project_ninfer_admission_reserve.md`
- **llama.cpp.** `--cache-type-k` and `--cache-type-v` accept f32, f16 (default), bf16, q8_0, q4_0, q4_1,
  iq4_nl, q5_0 and q5_1. `cache_prompt` enables same-slot prefix reuse.
  — [llama.cpp tools README mirror](https://docs.rs/crate/llama-cpp-sys-4/0.4.4/source/llama.cpp/tools/cli/README.md); [llama-cpp-ex performance guide](https://llama-cpp-ex.hexdocs.pm/performance.html)

### Inferences
- On a single local GPU, a cache miss costs prefill time, not money. At 131K, re-prefilling 100K tokens after
  each mask step is expensive.
- A cache-friendly policy, which is an inference I have not measured:
  1. Leave history untouched until a threshold.
  2. Then mask everything older than the last K turns in one rewrite.
  3. Then append-only again until the next threshold.

  This pays one re-prefill per threshold crossing instead of one per turn.
- The policy works the same on SGLang RadixAttention (a tree match on the token prefix) and on llama.cpp slot
  reuse. Neither engine can reuse KV for tokens after the first changed position.

### Gaps
- I did not fetch the SGLang radix-cache docs. Engine behaviour on mid-history edits is inferred from how
  prefix caching works, not cited.
- I did not find whether llama.cpp's `--cache-reuse` (chunk-shift reuse after an edit) is quality-safe.
- I found no perplexity numbers for q8_0 against f16 KV.
- I found no published measurement of prefill cost per masking policy.

## Text-level and KV-level compression

### Takeaway
- **Text level.** Token-dropping compressors (LLMLingua-2) compress code poorly (under 3x) and can break
  code, JSON and paths. Task-conditioned line pruners (Squeez, SWE-Pruner) suit code better.
- **KV level.** Eviction methods (SnapKV, H2O, StreamingLLM) are essentially absent from SGLang and vLLM
  production deployments, because FlashAttention does not expose attention scores. The usable KV lever on
  our engines today is KV quantization: q8_0 in llama.cpp, and the int8 KV already used for the 131K window.
- **KVzip** reports 3-4x smaller caches with negligible loss on code comprehension. It is a research codebase,
  not an engine feature.

### Cited Findings
- **LLMLingua-2 on code.** Compression stayed under 3x in every setting as a SWE-bench Verified baseline, at
  about 0.9 s per instance. I could not see its resolve count. — [SWEzze arXiv 2603.28119](https://arxiv.org/pdf/2603.28119)
- **Token pruning breaks structure.** Token-level pruning can break JSON, code blocks and file paths. This is a
  secondary source. — [Morph prompt-compression guide](https://www.morphllm.com/prompt-compression)
- **LLMLingua-2, method.** A small encoder (XLM-RoBERTa / mBERT) classifies each token as keep or drop, trained
  by distillation from GPT-4. It reports 2-5x compression and is 3-6x faster than LLMLingua.
  — [arXiv 2403.12968](https://arxiv.org/abs/2403.12968) (abstract, from prior knowledge, not re-fetched)
- **Eviction is missing from production.** StreamingLLM and SnapKV "are not commonly used within industrial
  deployments using frameworks like vLLM or SGLang". SnapStream got a 4x KV memory cut and 4.3x decode
  throughput for DeepSeek-R1 at TP16, on SambaNova hardware, not SGLang. — [SnapStream arXiv 2511.03092](https://arxiv.org/html/2511.03092v5)
- **Why.** Attention-score eviction collides with production infrastructure because FlashAttention does not
  expose attention scores. — [NVIDIA research blog](https://research.nvidia.com/labs/eai/blogs/kv-cache-compression-and-its-infra-problems/)
- **KVzip.** Scores each KV pair by how well the model can reconstruct the context from the cache, so one
  compressed cache can be reused across future queries.
  - 3-4x smaller KV and about 2x faster FlashAttention decode, with negligible loss on QA, retrieval,
    reasoning and code comprehension.
  - Tested on LLaMA3.1, Qwen2.5 and Gemma3 up to 170K tokens.
  - Query-aware eviction methods degrade even at a 90% budget in multi-query settings.
  - The v1 abstract said "up to 70%". Later versions say 3-4x.
  - Code at snu-mllab/KVzip.
  - [arXiv 2505.23416](https://arxiv.org/pdf/2505.23416); [NeurIPS 2025](https://papers.neurips.cc/paper_files/paper/2025/hash/f4eaa4b8f2d08edb3f0af990d56134ea-Abstract-Conference.html)
- **StreamingLLM.** Keeps a few "attention sink" tokens plus a sliding window. SnapKV keeps the top tokens per
  head by observed attention. — [SnapStream](https://arxiv.org/html/2511.03092v5)
- **llama.cpp q8_0 KV.** Described as near-lossless and roughly half of f16 memory. This is a third-party
  binding guide, with no perplexity numbers. — [llama-cpp-ex guide](https://llama-cpp-ex.hexdocs.pm/performance.html)
- **Our own KV quantization (internal).** int8 KV at a 131K window halved turns.
  — internal `project_window_131k_engine_args.md`

### Inferences
- **StreamingLLM / H2O-style eviction is a poor fit for agents.** It drops mid-context tokens permanently. An
  agent re-reading a specific function needs exact recall, and "Agents Don't Paginate" shows they rarely ask
  again. Treat as low applicability.
- **KVzip is the only KV-eviction method here aimed at reuse across queries**, which is the agent setting.
  Integrating it into SGLang or llama.cpp would be custom engine work with no Qwen3.8 hybrid-attention support
  shown. Medium-low applicability.

### Gaps
- I found no evaluation of KV eviction (SnapKV, H2O, KVzip) on a multi-turn coding-agent benchmark.
- I found no current SGLang 2026 docs confirming the absence of native eviction or sparse-KV options. The
  conclusion rests on SnapStream and NVIDIA's statements.

## Learned memory: REMORY, gist tokens, ICAE, xRAG, AutoCompressors, Activation Beacon

### Takeaway
REMORY is the only learned method here with a checkpoint for a Qwen3.8 model (the 27B, not Flash-Next) and
agentic claims.
- It needs soft-token (embedding) injection, which neither stock SGLang nor llama.cpp exposes for multi-turn
  chat.
- It ships a 1.9B side network.
- Its hardware requirements are not confirmed here. The brief's "2x80GB for 27B" is not verified by anything
  I fetched.

The other learned methods need fine-tuning the base model or a custom encoder, so their applicability to
Flash-Next is low.

### Cited Findings
- **REMORY ("Learning Residual Memory for Context Compaction").** A small network generates soft memory
  tokens appended after a plain textual summary, acting as a residual over the summary.
  - On SummHay it approaches full-context joint score with 5.2% of input positions, with insight coverage
    nearly unchanged.
  - On BrowseComp and Terminal-Bench 2.1, Qwen3.8-27B and GLM-5.3-Flash showed "consistent gains" and fewer
    repeated tool outputs and tool errors. No per-task numbers are in the coverage.
  - Checkpoints: 1.9B (for Qwen3.8-27B) and 1.24B (for GLM-5.3-Flash). Code at github.com/1ring2rta/Remory.
    The HF link uses ID 2610.11287.
  - [AI Weekly write-up (secondary)](https://aiweekly.co/alerts/remory-compacts-agent-context-to-52-with-soft-memory-tokens)
- **Gist tokens.** The model is fine-tuned to compress a prompt into a few gist tokens, with up to 26x prompt
  compression. — [arXiv 2304.08467](https://arxiv.org/abs/2304.08467) (abstract, from prior knowledge, not re-fetched)
- **ICAE.** A LoRA-adapted encoder compresses context into memory slots, about 4x. — [arXiv 2307.06945](https://arxiv.org/abs/2307.06945) (abstract, from prior knowledge, not re-fetched)
- **xRAG.** Projects a retrieval embedding into one token, aimed at RAG documents, not code.
  — [arXiv 2405.13792](https://arxiv.org/abs/2405.13792) (abstract, from prior knowledge, not re-fetched)
- **AutoCompressors.** Fine-tunes the model to emit summary vectors. — [arXiv 2305.14788](https://arxiv.org/abs/2305.14788) (abstract, from prior knowledge, not re-fetched)
- **Activation Beacon.** Fine-tunes the model to condense activations into beacon tokens.
  — [arXiv 2401.03462](https://arxiv.org/abs/2401.03462) (abstract, from prior knowledge, not re-fetched)
- **Related (no numbers fetched).** "Memory as a Controlled Process" (learned memory management) also appeared
  in search. — [arXiv 2607.13591](https://arxiv.org/pdf/2607.13591)

### Inferences
- **REMORY on our hardware.**
  - Fit: a 1.9B side network plus Flash-Next could fit on the 96GB 6000 if Flash-Next's footprint allows. The
    ~48 GiB host-RAM PLE floor (`project_ple_host_ram_floor.md`) is separate.
  - Blocker: we would need a Flash-Next-specific memory network (none is released) and an embeddings-input
    path in the engine.
  - Applicability: low until both exist.
- **Gist / ICAE / AutoCompressors / Activation Beacon** all change or fine-tune the backbone. That conflicts
  with serving a stock open-weight Flash-Next quant. Applicability: low.

### Gaps
- I did not reach REMORY's primary arXiv or HF page, so the arXiv ID, hardware (the "2x80GB" claim) and
  per-benchmark numbers are unverified.
- None of the learned methods has published results on Qwen3.8 Flash-Next.

## Ranking for GameSummoner (self-hosted Flash-Next, single card)

### Takeaway
Ranked by evidence quality × fit with no extra cards and no engine forks:
1. Observation masking / tool-result clearing, triggered by a token threshold in batched rewrites to protect
   the prefix cache.
2. A content-hashed unchanged-read stub.
3. Deterministic output shaping (truncate/dedupe shell output, first chunk must hold the relevant part).
4. KV quantization, already in use.
5. A learned line pruner (Squeez 2B, or SWE-Pruner Pro on patched SGLang). Lab only, given the Qwen
   regressions.
6. LLM summarization, kept only as the late "hybrid" stage.
7. KVzip (custom engine work).
8. REMORY / gist / ICAE / Beacon (need a backbone-specific network or fine-tuning). Low.
9. StreamingLLM / H2O / SnapKV. Low: absent from SGLang, and lossy on exact recall.

### Cited Findings
- **Masking.** Halves cost with matched solve rate, best-evidenced. — [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- **Context editing.** 84% fewer tokens on a 100-turn task. — [Claude blog](https://claude.com/blog/context-management)
- **SWE-Pruner Pro.** −1.2% resolve on a Qwen backbone, +15% wall time, needs patched SGLang.
  — [HF 2607.18213](https://huggingface.co/papers/2607.18213.md)
- **Squeez.** 92% removal at 0.86 recall, no end-to-end result. — [arXiv 2604.04979](https://arxiv.org/abs/2604.04979)
- **KV eviction.** Not deployed in SGLang or vLLM. — [SnapStream](https://arxiv.org/html/2511.03092v5); [NVIDIA](https://research.nvidia.com/labs/eai/blogs/kv-cache-compression-and-its-infra-problems/)

### Inferences
- The levers in ranks 1-3 are harness-side and engine-agnostic: they work identically on ninfer, SGLang and
  llama.cpp, and on the 5090 and the 6000. That suits "local is second-class, same prod path".
- Per GameSummoner rules ("prompt lines are labs", "one run first"), any placeholder or stub wording the model
  sees should go through a lab run against the existing baseline before adoption.

### Gaps
- No source measures these levers on game-building tasks, or with Qwen3.8 Flash-Next specifically.
