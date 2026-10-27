# Low-impact context compaction in production and open-source coding agents

Scope: what state survives compaction, what gets re-attached, how the agent resumes, and measured impact. Researched 2026-10-20. Source code was read directly where it was public (Codex, OpenHands SDK, Roo Code, Cline docs, Aider, SWE-agent, qwen-code). For Claude Code, the source is a community mirror of the leaked or reconstructed client (`claude-code-best/claude-code`). A code comment in it dates it to after 2026-03-10. I did not verify the exact version, so treat its constants as "a 2026 build", not current production. "MEASURED" means a number with a stated eval. "CLAIM" means a vendor statement with no eval.

## Claude Code: trigger, summary prompt, post-compaction restoration; Anthropic context editing / memory tool / context-engineering numbers

### Takeaway
Claude Code is the most elaborate "low-impact" design. It runs three tiers:
1. Microcompact clears old tool results.
2. A full 9-section LLM summary follows.
3. A restoration step re-attaches content after the summary:
   - the 5 most recently read or edited files, at 5K tokens each and 50K tokens in total
   - the plan file and plan-mode state
   - invoked skills, at 5K tokens each and 25K tokens in total
   - SessionStart hook output
   - a pointer to the full transcript on disk

It also clears its read-file cache at compaction, so the "file unchanged, don't re-read" dedup stub stops protecting files that weren't restored. Anthropic's only published numbers are for API-level context editing and the memory tool (29% / 39% / 84%). None exist for Claude Code's compaction itself.

### Cited Findings
**Trigger (leaked source)**
- Auto-compact fires at the effective window minus `AUTOCOMPACT_BUFFER_TOKENS = 13_000`. The buffer scales with window size: 30K at a 400K+ window and 50K at an 800K+ window. There are warning and error thresholds at 20K below the trigger, and a manual-compact buffer of 3K. `MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20_000`. A predictive check estimates growth per turn as max output plus `TOOL_RESULT_GROWTH_ESTIMATE = 15_000`. The code comment reads: "Typical tool results (file reads, grep, bash) average ~5-10K tokens; occasional large reads can spike to 20K+". — [claude-code-best/claude-code src/services/compact/autoCompact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/autoCompact.ts)
- Circuit breaker: `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3`. The comment cites "BQ 2026-03-10: 1,279 sessions had 50+ consecutive failures (up to 3,272) in a single session, wasting ~250K API calls/day globally." — [autoCompact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/autoCompact.ts)
- Third-party blogs disagree on the threshold. One says "roughly 95% of the limit" — [okhlopkov.com](https://okhlopkov.com/claude-code-compaction-explained/). A skills page says about 83.5% — [skills.sh compact-guard](https://www.skills.sh/rohitg00/pro-workflow/compact-guard). The buffer-based formula in the source explains why the percentage varies by model window.

**Summary prompt (leaked source, `prompt.ts`)**
- The prompt opens with a no-tools preamble: "CRITICAL: Respond with TEXT ONLY. Do NOT call any tools. ... Tool calls will be REJECTED and will waste your only turn — you will fail the task." — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- The model writes an `<analysis>` scratchpad first, then a `<summary>`. The analysis is stripped before the summary enters context. The analysis must cover "file names, full code snippets, function signatures, file edits", errors and fixes, user feedback, and "security-relevant instructions ... MUST be preserved verbatim". — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- Nine required sections:
  1. Primary Request and Intent
  2. Key Technical Concepts
  3. Files and Code Sections ("include full code snippets where applicable and include a summary of why this file read or edit is important")
  4. Errors and fixes
  5. Problem Solving
  6. All user messages ("List ALL user messages that are not tool results")
  7. Pending Tasks
  8. Current Work ("precisely what was being worked on immediately before this summary request ... Include file names and code snippets")
  9. Optional Next Step ("include direct quotes from the most recent conversation showing exactly what task you were working on and where you left off. This should be verbatim to ensure there's no drift in task interpretation")

  Source: [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- Variants:
  - `PARTIAL_COMPACT_PROMPT` summarizes only "the RECENT portion" while earlier messages stay intact.
  - `PARTIAL_COMPACT_UP_TO_PROMPT` summarizes a prefix; newer messages follow it verbatim.
  - The prompt accepts user or CLAUDE.md "Compact Instructions", e.g. "Include file reads verbatim."

  Source: [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)

**Resume message (leaked source)**
- The summary is wrapped as: "This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation." — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- Optional addition: "If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: ${transcriptPath}". — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- Optional addition: "Recent messages are preserved verbatim." — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- Auto mode adds: "Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening ... Pick up the last task as if the break never happened." — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)

**Post-compaction restoration (leaked source, `compact.ts`)**
- Constants: `POST_COMPACT_MAX_FILES_TO_RESTORE = 5`, `POST_COMPACT_TOKEN_BUDGET = 50_000`, `POST_COMPACT_MAX_TOKENS_PER_FILE = 5_000`, `POST_COMPACT_MAX_TOKENS_PER_SKILL = 5_000`, `POST_COMPACT_SKILLS_TOKEN_BUDGET = 25_000`. — [compact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/compact.ts)
- On skills, the code comment says re-injecting them unbounded on every compact cost "5-10K tok/compact". It also says "Per-skill truncation beats dropping — instructions at the top of a skill file are usually the critical part." — [compact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/compact.ts)
- How files are chosen:
  - Files come from the `readFileState` cache, sorted by most recent timestamp.
  - Files already visible in preserved messages are excluded.
  - The top 5 are re-read from disk, so they arrive fresh rather than stale, at a 5K-token cap each.
  - Files are added until the 50K budget runs out.

  Source: [compact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/compact.ts)
- Other attachments, in order: plan file (`createPlanAttachmentIfNeeded`), plan-mode instructions ("so the model continues operating in plan mode after compaction"), invoked-skill content, re-announced deferred tools and MCP tools, then `processSessionStartHooks('compact')`. Final history order: boundaryMarker, summaryMessages, messagesToKeep, attachments, hookResults. — [compact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/compact.ts)
- Re-read trap: at compaction, `readFileState` is snapshotted and then `.clear()`ed. Normally the Read tool deduplicates: an identical read of an unchanged file returns `FILE_UNCHANGED_STUB`, "File unchanged since last read. The content from the earlier Read tool_result in this conversation is still current — refer to that instead of re-reading." Measured for that dedup (internal soak, a code comment): "1,734 dedup hits in 2h, no Read error regression." Because the cache is cleared at compaction, files that were not restored get a full re-read. — [FileReadTool.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/packages/builtin-tools/src/tools/FileReadTool/FileReadTool.ts), [FileReadTool/prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/packages/builtin-tools/src/tools/FileReadTool/prompt.ts)
- Microcompact clears results from Read, shell, Grep, Glob, WebSearch, WebFetch, Edit and Write. Cleared content becomes `'[Old tool result content cleared]'`, and the newest `keepRecent` results are kept.
  - A time-based variant fires when the gap since the last assistant message exceeds a threshold in minutes, i.e. when the prompt cache is cold anyway.
  - A "cached microcompact" variant, internal-only behind a feature flag, uses API-side `cache_edits` to delete results without breaking the prompt cache.

  Source: [microCompact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/microCompact.ts)
- An experimental "session memory compaction" keeps between 10K and 40K tokens of recent messages verbatim (`minTokens: 10_000`, `minTextBlockMessages: 5`, `maxTokens: 40_000`). Its summary is a separately maintained session memory, not one generated at compaction time. — [sessionMemoryCompact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/sessionMemoryCompact.ts)
- Third-party, version-agnostic table of what survives:
  - Project-root CLAUDE.md is "Re-read and re-injected".
  - Nested CLAUDE.md reloads only when matching files are read again.
  - Subagent research keeps "Only the returned summary".

  Source: [okhlopkov.com](https://okhlopkov.com/claude-code-compaction-explained/)

**Anthropic, official**
- Anthropic says Claude Code "passes the message history to the model to summarize and compress", keeping "architectural decisions, unresolved bugs, and implementation details". It then continues with the summary "plus the five most recently accessed files". — [Anthropic, Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Tuning advice: maximize recall first, then precision. Tool-result clearing is "one of the safest lightest touch forms of compaction". — [same](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Structured note-taking: Claude Code's to-do list, a NOTES.md, and the Claude-plays-Pokémon agent. That agent kept progress counters and maps across context resets. — [same](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Sub-agents explore with "tens of thousands of tokens or more" and return 1,000–2,000-token distilled summaries. — [same](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- MEASURED (internal agentic-search eval, 2025-09-29): context editing alone gave +29% over baseline, and context editing plus the memory tool gave +39%. In a 100-turn web-search eval, context editing cut token use by 84% and let otherwise-failing workflows finish. — [Claude blog, Managing context on the Claude Developer Platform](https://claude.com/blog/context-management)

### Inferences
- Claude Code deals with re-reads in two ways:
  - It pre-pays them: 5 files are re-read at compaction time and capped in size.
  - It gives an escape hatch for everything else: the transcript path.

  The 5K-per-file cap means large files come back truncated, so the model will often re-read them anyway.
- Clearing `readFileState` is the right move for correctness. The old content is gone from context, so a stub pointing to "the earlier Read" would be false. But it means every file not among the top 5 costs a full re-read.
- None of this depends on proprietary API features. The exceptions are `cache_edits`-based microcompact and server-side context editing. Recency-ordered file restoration, the 9-section prompt with the analysis stripped, the transcript pointer, and plan/todo re-attachment are all portable to SGLang or llama.cpp.
- qwen-code (QwenLM, Apache-2.0, aimed at Qwen models) ported the same scheme in `postCompactAttachments.ts`: same 5 / 5K / 50K constants, plus `POST_COMPACT_MAX_IMAGES_TO_RESTORE = 3`. It replaced qwen-code's earlier "split-point + last 30%" tail preservation. The file was first committed 2026-05-29 and last updated 2026-09-20. This is the closest open-weight reference implementation. — [QwenLM/qwen-code postCompactAttachments.ts](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/services/postCompactAttachments.ts)

### Gaps
- I found no Anthropic-published measurement of Claude Code compaction's effect on task success or re-read counts.
- The production version of the leaked constants is unverified. The time-based microcompact threshold value is remote-configured and not in the file.

## OpenAI Codex CLI and Responses API compaction

### Takeaway
Local Codex compaction is minimal:
- It keeps all user messages, newest-first, up to 20K tokens.
- It adds a short handoff summary with a fixed "another language model" prefix.
- It carries no file contents. File state is meant to be re-derived from "the state of the tools".

Server-side Responses compaction returns an opaque encrypted item plus user messages. That is proprietary and unusable with self-hosted Qwen.

### Cited Findings
- The compaction prompt in full: "You are performing a CONTEXT CHECKPOINT COMPACTION. Create a handoff summary for another LLM that will resume the task. Include: Current progress and key decisions made; Important context, constraints, or user preferences; What remains to be done (clear next steps); Any critical data, examples, or references needed to continue. Be concise, structured, and focused on helping the next LLM seamlessly continue the work." — [codex-rs/prompts/templates/compact/prompt.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/compact/prompt.md)
- Summary prefix: "Another language model started to solve this problem and produced a summary of its thinking process. You also have access to the state of the tools that were used by that language model. Use this to build on the work that has already been done and avoid duplicating work. ..." — [summary_prefix.md](https://github.com/openai/codex/blob/main/codex-rs/prompts/templates/compact/summary_prefix.md)
- The replacement history is built from collected user messages plus `SUMMARY_PREFIX\n{summary}`. User messages are kept newest-first within `COMPACT_USER_MESSAGE_MAX_TOKENS = 20_000`. When over budget, truncated sources are flagged with `mark_retained_sources_incomplete`. Initial context (instructions and environment) is re-inserted before the last real user message. — [codex-rs/core/src/compact.rs](https://github.com/openai/codex/blob/main/codex-rs/core/src/compact.rs)
- Current main also has:
  - a "token-budget" compaction mode that "skips model/server summarization and installs a fresh context window instead" — [compact_token_budget.rs](https://github.com/openai/codex/blob/main/codex-rs/core/src/compact_token_budget.rs)
  - a mechanism that retains client-marked tool outputs whole or drops them: "Retains explicitly marked, named function outputs that have no matching call. Outputs share the normal history token budget and are retained whole or dropped." — [compact_retained_tool_outputs.rs](https://github.com/openai/codex/blob/main/codex-rs/core/src/compact_retained_tool_outputs.rs)
  - PreCompact and PostCompact hooks, async compaction, and remote compaction (`compact_remote_v2*.rs`) — [compact.rs](https://github.com/openai/codex/blob/main/codex-rs/core/src/compact.rs)
- Responses API:
  - Server-side compaction uses `context_management` with `compact_threshold`; the examples use 200,000.
  - `/responses/compact` is "fully stateless and ZDR-friendly".
  - The compaction item is "opaque and not intended to be human-interpretable" and carries "key prior state and reasoning".
  - "The returned window is the canonical next context window, so pass it into your next /responses call as-is."

  Source: [OpenAI compaction guide](https://developers.openai.com/api/docs/guides/compaction)
- Per a search summary of the OpenAI reference (not opened directly), the compacted output is "a list of all user messages, followed by a single compaction item" with `encrypted_content`. — [OpenAI API reference: responses compact](https://developers.openai.com/api/reference/cli/resources/responses/methods/compact)

### Inferences
- Codex's lesson for us is "user messages verbatim + short handoff". The "you have access to the state of the tools ... avoid duplicating work" line is the only defence against re-reads, and it is a soft instruction.
- Encrypted reasoning carry-over cannot be reproduced on an open-weight stack. The closest analogue is keeping the model's last reasoning or plan text in the summary.

### Gaps
- openai.com's GPT-5.1-codex-max page returned 403, so I could not quote its native-compaction claims ("works across multiple context windows" or "millions of tokens"). Treat any such claim as unverified here.
- I found no OpenAI measurement of compaction impact on task success.

## OpenHands condensers

### Takeaway
The SDK's default is an LLMSummarizingCondenser:
- It triggers at 240 events, or at a token limit.
- It keeps the first 2 events and the newest half verbatim.
- It summarizes the older half into a structured state summary.

Measured on SWE-bench Verified, the summary halves per-turn cost with no loss in solve rate. The prompt explicitly tracks file paths (CODE_STATE) but does not re-attach file contents.

### Cited Findings
- README: "the context window is condensed by replacing the first half of all events with a single summary event". The back half "is untouched, so the agent has an easy time continuing the current task". Summaries are re-summarized in later condensations. Condensation is an append-only tombstone event (`Condensation`) applied through a `View`. — [OpenHands software-agent-sdk condenser README](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/context/condenser/README.md)
- Defaults: `max_size=240`, `keep_first=2`, `minimum_progress=0.1`, optional `max_tokens`, `hard_context_reset_max_retries=5`, `hard_context_reset_context_scaling=0.8`. Soft triggers skip if condensing would break message structure. Hard triggers, such as a context-exceeded error, forget and summarize the entire view. — [llm_summarizing_condenser.py](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/context/condenser/llm_summarizing_condenser.py)
- Summary sections: USER_CONTEXT, TASK_TRACKING ("PRESERVE TASK IDs"), COMPLETED, PENDING, CURRENT_STATE, plus CODE_STATE {File paths, function signatures, data structures}, TESTS, CHANGES, DEPS and VERSION_CONTROL_STATUS for code tasks. The prompt includes a worked example. — [summarizing_system.j2](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/context/condenser/prompts/summarizing_system.j2)
- MEASURED (2025-04-09, subset of SWE-bench Verified): about 54% solved with the condenser vs 53% baseline. Per-turn cost fell by up to 2x, and cost scaling changed from quadratic to linear. — [OpenHands blog: context condensation](https://openhands.dev/blog/openhands-context-condensensation-for-more-efficient-ai-agents)
- MEASURED (Complexity Trap, 50 instances, Gemini 2.5 Flash): on OpenHands, once the masking window was tuned, observation masking matched summary on both cost and solve rate. — [arXiv 2508.21433](https://arxiv.org/html/2508.21433v3)

### Inferences
- Keeping the "newest half verbatim" is OpenHands' main protection against re-reads. Recent file reads simply survive.

### Gaps
- The ObservationMasking, AmortizedForgetting and LLMAttention condensers appear to live in the older OpenHands V0 repo. The current SDK tree shows only the LLM-summarizing, no-op and pipeline condensers. I did not retrieve separate benchmark numbers for those older variants.

## Cline / Roo / Kilo, Aider, SWE-agent, Cursor, Amp, Factory

### Takeaway
- File-carrying designs:
  - Claude Code and qwen-code restore full recent files.
  - Roo Code re-attaches tree-sitter "folded" signatures of every file read, up to 50K characters.
  - Amp's handoff carries a list of relevant files.
  - Cursor writes the full chat history to a file the agent can grep.
- Summary-only designs: Codex, Cline, Aider.
- SWE-agent masks old observations instead of summarizing.
- Factory ran the only head-to-head probe eval. It found that "artifact trail" (which files were touched and what changed) is the weakest dimension for every method, scoring 2.19–2.45 out of 5.

### Cited Findings
- **Roo Code:**
  - The condense prompt starts "CRITICAL: This is a summarization-only request. DO NOT call any tools" and adds "This summarization request is a SYSTEM OPERATION, not a user message ... The goal is for work to continue seamlessly after condensation - as if it never happened."
  - After the summary it appends active workflows ("must be maintained across all future condensings"), then `generateFoldedFileContext(filesReadByRoo)`: tree-sitter definitions only ("hiding implementation bodies"), each in a `<system-reminder>`, capped at 50,000 characters.
  - The condense threshold is configurable from 5–100% of the window.

  Source: [Roo-Code src/core/condense/index.ts](https://github.com/RooCodeInc/Roo-Code/blob/main/src/core/condense/index.ts), [foldedFileContext.ts](https://github.com/RooCodeInc/Roo-Code/blob/main/src/core/condense/foldedFileContext.ts)
- **Cline:**
  - Auto Compact "Creates a comprehensive summary ... Replaces the conversation history with the summary ... Continues exactly where it left off".
  - CLAIM: it costs about the same as any tool call because it reuses the prompt cache.
  - "Structured task lists can help maintain progress across summarizations".
  - Unsupported models fall back to rule-based truncation.
  - Checkpoints allow rollback to before a summarization.

  Source: [cline docs/features/auto-compact.mdx](https://github.com/cline/cline/blob/main/docs/features/auto-compact.mdx)
- **Aider:**
  - Chat history is summarized recursively (`ChatSummary`, default `max_tokens=1024`): the head is summarized while a tail of up to half the budget is kept, recursing to depth 3.
  - The prompt reads: "*Briefly* summarize ... more detail about the most recent messages ... MUST include the function names, libraries, packages ... MUST include the filenames ... MUST NOT include ``` fenced code blocks ... Write *as* the user ... Start the summary with 'I asked you...'."
  - File contents are not summarized. Files the user added to the chat are re-sent every turn, alongside the repo map, which is why aider never re-reads after summarization.

  Source: [aider/prompts.py](https://github.com/Aider-AI/aider/blob/main/aider/prompts.py), [aider/history.py](https://github.com/Aider-AI/aider/blob/main/aider/history.py)
- **SWE-agent:**
  - The `LastNObservations` history processor replaces older observations with "Old environment output: (n lines omitted)".
  - A `polling` parameter keeps between n and n+polling observations, so the prompt cache is invalidated less often.
  - `TagToolCallObservations` can exempt chosen tools from masking.

  Source: [sweagent/agent/history_processors.py](https://github.com/SWE-agent/SWE-agent/blob/main/sweagent/agent/history_processors.py)
- **Cursor (Jan 2026):**
  - At summarization, Cursor saves the full chat history as a file and gives the agent a reference to it, "so it can look up anything the summary dropped".
  - Long tool outputs go to files instead of being truncated, which led to "fewer unnecessary summarizations".

  Source: [Cursor blog, dynamic context discovery](https://cursor.com/blog/dynamic-context-discovery), [InfoQ](https://www.infoq.com/news/2026/01/cursor-dynamic-context-discovery)
- **Amp:**
  - Amp removed compaction ("Handoff (No More Compaction)"). Compaction was lossy and encouraged long threads that stacked summary on summary.
  - Handoff takes a user-stated goal and drafts a new-thread prompt "along with a list of relevant files". The user reviews it before sending.
  - A later promotional listing claims the Amp "Neo" CLI re-added automatic compaction. This is unverified.

  Source: [ampcode.com/news/handoff](https://ampcode.com/news/handoff), [hunted.space](https://hunted.space/product/amp-free)
- **Factory (2025-12-16), MEASURED:**
  - Method: "anchored iterative summarization". It keeps a persistent structured summary (session intent, file modifications, decisions, next steps) and merges in only the newly truncated span.
  - Eval: probes of four types (recall, artifact, continuation, decision), graded 0–5 by a GPT-5.2 judge.
  - Results (Factory / Anthropic / OpenAI): overall 3.70 / 3.44 / 3.35; artifact trail 2.45 / 2.33 / 2.19; continuity 3.80 / 3.67 / 3.77.
  - Compression ratios: OpenAI 99.3%, Anthropic 98.7%, Factory 98.6%.
  - Quotes: "Artifact tracking remains an unsolved problem." "Those lost details eventually require re-fetching, which can exceed the token savings." "The right optimization target is not tokens per request. It is tokens per task."

  Source: [Factory, Evaluating context compression](https://factory.com/news/evaluating-compression)

### Inferences
- The designs split into two families:
  - "Summary + re-attach": Claude Code, qwen-code, Roo folded signatures, Amp file list.
  - "Summary + retrieval pointer": Claude Code transcript path, Cursor history file, Codex "state of the tools".

  Factory's low artifact scores suggest summaries alone don't carry file state reliably. A mechanically generated file list or file contents, built by the harness rather than written by the model, is the obvious fix. This is our inference; Factory proposes "a separate artifact index or explicit file-state tracking" without measuring one.
- Roo's signatures-only folding is a cheap middle ground between "full file" and "path only". For a 131K window it is attractive: about 50K characters is roughly 12–15K tokens.

### Gaps
- I found no public eval of re-read counts after compaction for any of these tools.
- No primary source covers Devin or Kilo compaction internals. Kilo is a Roo/Cline fork and likely inherits Roo's condense; this is unverified.

## Academic results: masking vs summarization, learned compression and folding

### Takeaway
On SWE-bench Verified, plain observation masking (keep the last 10 observations, replace older ones with a placeholder) halves cost and matches LLM summarization's solve rate. Summarization also makes trajectories about 15% longer. Learned or RL-trained approaches (ACON, AgentFold, Context-Folding, ReSum, MEM1) report large context reductions, but mostly on web or QA tasks. Most require training, except ACON's prompt-optimization variant.

### Cited Findings
- **Complexity Trap (Lindenbauer et al., arXiv 2508.21433), MEASURED.** SWE-agent, SWE-bench Verified, n=500, solve rate and cost per instance:

  | Model | Raw | Masking | Summary |
  |---|---|---|---|
  | Qwen3-Coder 480B | 53.4% / $1.29 | 54.8% / $0.61 | 53.8% / $0.64 |
  | Gemini 2.5 Flash | 32.8% / $0.41 | 35.6% / $0.18 | 36.0% / $0.24 |
  | Gemini 2.5 Flash (thinking) | 40.4% | 36.4% | 31.4% |
  | Qwen3-32B | 17.0% / $1.12 | 15.0% / $0.55 | 16.0% / $0.50 |
  | Qwen3-32B (thinking) | 23.0% | 24.6% | 24.8% |

  Source: [arXiv 2508.21433v3](https://arxiv.org/html/2508.21433v3)
- Complexity Trap settings:
  - Masking used window M=10.
  - Summary used N=21 turns per summary and kept M=10 tail turns.
  - The hybrid (N=43, M=W=10) cost 7% less than masking and 11% less than summary, and gave +2.6pp over Raw on Qwen3-Coder 480B (Verified-50).

  Source: [same](https://arxiv.org/html/2508.21433v3)
- Complexity Trap, trajectory elongation:
  - Summary trajectories were 15% longer than masking on Gemini 2.5 Flash (52 vs 44 turns) and 15% longer than Raw on Qwen3-Coder.
  - Quote: "context summaries act as a reinforcing signal, encouraging the agent to keep going".
  - Summary calls were 7.2% of instance cost on Qwen3-Coder.

  Source: [same](https://arxiv.org/html/2508.21433v3)
- **ACON (Microsoft/KAIST, ICLR 2026):**
  - Compression guidelines are optimized in natural language from failure pairs, where full context succeeds and compressed context fails.
  - Peak tokens fell 26–54% on AppWorld, OfficeBench and multi-objective QA, with task performance largely preserved.
  - Distilled compressors keep over 95% of the teacher's accuracy, and small models gain up to 46%.
  - A third-party review (not verified against the paper) reports AppWorld 56.5% at 7.33K peak tokens vs 56.0% at 9.93K.

  Source: [ACON arXiv 2510.00615](https://arxiv.org/pdf/2510.00615v1), [review](https://www.themoonlight.io/tw/review/acon-optimizing-context-compression-for-long-horizon-llm-agents)
- **AgentFold (Alibaba Tongyi, ICLR 2026):** proactive context folding. The 30B-A3B model scores 36.2% on BrowseComp and 47.3% on BrowseComp-ZH. Context is about 7K tokens after 100 turns and scales to 500 turns. Requires training. — [arXiv 2510.24699](https://arxiv.org/html/2510.24699v1)
- **Context-Folding (arXiv 2510.11967):**
  - The agent branches into sub-trajectories and folds each one to an outcome summary. Training uses FoldGRPO, an RL method.
  - It matches or beats ReAct on Deep Research and SWE tasks with a 10x smaller active context.
  - It "significantly outperforms" summarization-based context management.

  Source: [HF papers 2510.11967](https://huggingface.co/papers/2510.11967)
- **ReSum (arXiv 2509.13313):**
  - Training-free, it beats ReAct by 4.5%; ReSum-GRPO adds a further 8.2%.
  - A 30B agent trained on 1K samples is competitive with leading open-source models.

  Source: [papers.cool 2509.13313](https://papers.cool/arxiv/2509.13313)
- **MEM1 (arXiv 2506.15841):** RL-learned constant-size internal state, rewritten every turn. On 16-objective multi-hop QA, MEM1-7B beats Qwen2.5-14B-Instruct by 3.5x on performance with 3.7x less memory. — [arXiv 2506.15841](https://arxiv.org/pdf/2506.15841v1)

### Inferences
- For a coding agent on open weights, the cheapest evidence-backed change is masking old tool observations rather than summarizing them. Masking keeps the agent's own reasoning and actions, including file paths, and drops bulky outputs.
- In the Complexity Trap tables, the thinking variants were the most volatile under summarization. Gemini Flash thinking fell from 40.4% to 31.4% with summaries. That is relevant to a thinking-on Qwen3.8 setup.
- AgentFold, Context-Folding, ReSum-GRPO and MEM1 all need RL training of the agent model, so they don't apply to off-the-shelf Qwen3.8 Flash-Next. ACON's guideline optimization is prompt-only, so it fits a climbable-prompt workflow.

### Gaps
- None of these papers measure post-compaction re-reads directly. The 15% longer trajectories is the closest proxy.
- I did not retrieve the Complexity Trap cost figures for the thinking variants, or the exact OpenHands numbers (shown only in its Figure 5a).

## Which designs carry file contents or lists across compaction; evidence on re-reads

### Takeaway
Only Claude Code, and qwen-code which copies it, re-attach file contents (5 most recent, 5K tokens each, 50K total). Roo re-attaches folded signatures. Amp hands off a file list. OpenHands and SWE-agent keep the recent tail verbatim. Codex, Cline and Aider carry only text summaries; Aider's in-chat files are re-sent every turn anyway. Direct evidence that summaries cause re-reads comes only from Factory's qualitative claim and its low artifact-trail scores, plus the Complexity Trap's trajectory elongation. I found no published re-read count.

### Cited Findings
- **File contents:**
  - Claude Code: `createPostCompactFileAttachments`, recency-sorted, excluding files already in preserved messages, re-read from disk. — [compact.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/compact.ts)
  - qwen-code: same constants, and failed or denied reads are excluded from restoration. Its resume trailer: "Resume the prior task using the summary above. Continue from the last in-flight step; do not acknowledge the summary, do not re-introduce, do not greet the user again." It sits in the wrapper, not the summary prompt, to "prevent wording drift". — [qwen-code postCompactAttachments.ts](https://github.com/QwenLM/qwen-code/blob/main/packages/core/src/services/postCompactAttachments.ts)
- **Signatures:** Roo `foldedFileContext`, capped at 50K characters. — [foldedFileContext.ts](https://github.com/RooCodeInc/Roo-Code/blob/main/src/core/condense/foldedFileContext.ts)
- **File lists:**
  - Amp handoff. — [ampcode.com/news/handoff](https://ampcode.com/news/handoff)
  - OpenHands CODE_STATE section. — [summarizing_system.j2](https://github.com/OpenHands/software-agent-sdk/blob/main/openhands-sdk/openhands/sdk/context/condenser/prompts/summarizing_system.j2)
  - Claude Code "Files and Code Sections" section. — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
- **Retrieval pointer to the full history:**
  - Claude Code transcript path. — [prompt.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/src/services/compact/prompt.ts)
  - Cursor history file. — [Cursor blog](https://cursor.com/blog/dynamic-context-discovery)
- **Re-read evidence:**
  - Factory: "Without file tracking, coding agents may re-read files they already examined". — [Factory](https://factory.com/news/evaluating-compression)
  - Claude Code ships a non-compaction dedup stub with an internal soak count (1,734 hits in 2h). — [FileReadTool.ts](https://github.com/claude-code-best/claude-code/blob/HEAD/packages/builtin-tools/src/tools/FileReadTool/FileReadTool.ts)

### Inferences
- A low-impact recipe for a 131K open-weight harness, combining the measured pieces:
  1. Mask or clear old tool outputs first (Complexity Trap, Anthropic tool-result clearing).
  2. When a full summary is needed, keep user messages verbatim (Codex, Claude Code section 6) and use a fixed-section summary (Claude Code, OpenHands, Factory).
  3. Have the harness, not the model, re-attach the most recent N files fresh from disk under a token budget, plus folded signatures for the rest (Roo).
  4. Re-attach the plan or todo list.
  5. Give a pointer to the full pre-compaction log.

  The 50K re-attach budget sized for Claude's 200K window would scale to about 30K on a 131K window. That scaling is our extrapolation, not a measured value.
- A content-hash read cache that survives compaction for re-attached files could return an "unchanged" stub safely, because the content is then actually in context. That is a gap in Claude Code's design, which clears the whole cache.

### Gaps
- I found no source that measures re-read or duplicate-tool-call rates before and after compaction for any production agent. This would need our own lab.
