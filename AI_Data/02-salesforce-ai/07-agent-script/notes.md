# Agent Script

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** The language agents are authored in since 2026 — syntax, the compile-to-JSON model, the open-source toolchain, CI linting outside an org, and per-agent model pinning.

> **Why this folder exists.** It wasn't in the original 26-week roadmap because it didn't exist when the roadmap was written. Agent Script became the default authoring model in July 2026 and is now the highest-leverage topic in this track.

## What is it?

A **human-readable expression language for defining agents that compiles to portable JSON**. It blends two things that used to be alternatives:

- **Deterministic control** — conditionals, if/then, explicit hand-offs, precise tool invocation
- **Agentic reasoning** — letting the LLM plan and choose within bounds you set

Salesforce calls the dial between them **Hybrid Reasoning**. You decide, per decision point, how much is business logic and how much is model judgement. That's the core idea: not "how do I make the LLM behave" but "which parts of this should the LLM even be deciding."

**It is open source under Apache 2.0** — [github.com/salesforce/agentscript](https://github.com/salesforce/agentscript) ships the parser, linter, compiler, Language Server Protocol implementation and editor integrations.

## Why it matters (for the AI-Salesforce architect role)

**Agent definitions became source code.** That one sentence carries most of the consequence, so it's worth unpacking into the four things it actually enables:

| Because agents compile to JSON… | You get |
|---|---|
| There's a text artifact | **Diffs and pull-request review** — a behaviour change is visible |
| The compiler is open source | **Linting and testing in a plain CI job**, with no Salesforce connection |
| The output is portable | Third-party harnesses can execute it — the community already runs compiled Agent Script under Pydantic AI |
| The model is declared in the script | **Model pinning per agent**, versioned with the logic |

For an architect, the third row is the strongest signal in the whole release: **Salesforce wants agent logic to be portable rather than org-locked.** That is not a small strategic statement.

The practical framing for your own study: topic-and-instruction configuration was the Agentforce skill of 2025. Agent Script is the Agentforce skill of 2026, and it rewards a developer background — you already know why a compiled, diffable, testable artifact beats a form field full of prose.

## How it works

### The problem it replaced

Under the legacy model, behaviour lived in natural-language instructions across topics. That meant:

- Two instructions could quietly contradict each other, with no error
- Nothing compiled, so nothing could be validated before deployment
- No diff worth reviewing — a behaviour change looked like a prose edit
- Nothing testable outside an org
- Reliability problems were untraceable because there was no artifact to trace

Agent Script addresses each of those directly. When you're asked "why did Salesforce replace topics?", that list is the answer.

### The shape of a definition

An agent definition declares, in one reviewable file: the **model**, the **subagents** it can route to and their descriptions, the **actions** available, the **knowledge/grounding** it draws on (e.g. a `knowledge:` block wiring in an Agentforce Data Library), and the **control flow** — where you branch deterministically and where you hand off to reasoning.

The `knowledge:` block is the seam to RAG: it's how a Data Library becomes groundable, after which a subagent invokes `AnswerQuestionsWithKnowledge`. See [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md).

> Syntax specifics change faster than these notes will. Treat the [official Agent Script guide](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html) as authoritative and record concrete snippets you've actually run in `./labs/` rather than transcribing docs here.

### The CI story — the part worth building

Because the compiler is open source and runs without an org:

```
edit .agent file
   → lint locally (LSP in your editor)
   → compile to JSON in CI          ← no Salesforce connection needed
   → run agent evaluations           ← sf CLI, YAML/JSON-defined (Beta)
   → deploy via Metadata API
   → grade live sessions with Custom Scorers
```

That pipeline is a strong portfolio artifact in itself, and it's what the [Agentforce capstone](../../04-capstone/03-agentforce-use-case/notes.md) should demonstrate.

### Migration from legacy

One click. Upgrading a legacy agent converts all subagents, actions, system messages, data and connections into Agent Script, then optionally optimizes the result for reliability. **Then diff the two behaviours in preview** — the conversion is mechanical, and the optimization step can change behaviour in ways worth seeing before they reach production.

### Tooling that helps

- **Salesforce CLI** — `agent preview start` / `send` / `sessions` / `end` (GA), plus **trace files** showing exactly how the agent routed and acted
- **CLI `agent` project template** — scaffolds a runnable *Local Info Agent* demonstrating Apex, Prompt Template and Flow subagents
- **Agent Skills** — `npx skills add forcedotcom/sf-skills` drops Salesforce agent-building skills straight into Claude Code
- **`agentforce-adlc`** — Salesforce AI Research's Claude Code skills covering the whole agent lifecycle in Agent Script

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Clone [salesforce/agentscript](https://github.com/salesforce/agentscript) and compile a definition locally, with no org connected. Seeing it work offline is the moment the "it's source code" claim becomes real.
- [ ] Take a legacy topic-based agent → one-click upgrade → **diff the behaviours in preview**.
- [ ] Pin a different model in the script and measure the latency and cost difference.
- [ ] Wire up a GitHub Action that lints and compiles the definition on every push.
- [ ] `npx skills add forcedotcom/sf-skills` and use Claude Code to draft an Agent Script definition.

## Gotchas & sharp edges

- **Exact GA date is murky.** Secondary sources conflict between February 2026 and the Summer '26 cadence; no first-party announcement pins it. What *is* confirmed: the legacy builder stopped creating new agents the **week of July 13, 2026**.
- **Agent Script isn't named in the Agentforce Specialist exam guide** despite being the default authoring model. Given the guide's emphasis on deterministic behaviour, filters and variables, assume implicit scope — and re-check before booking. Exam guides lag GA by a release or two.
- **Subagent descriptions are executable configuration.** Atlas 3.0 routes on them. This is the single highest-value thing to get right in a definition.
- **The upgrade's "optimize" step can change behaviour.** Diff before trusting it.
- **Compiling clean ≠ behaving well.** The compiler validates structure, not judgement. Evaluations and scorers are how you check behaviour — see [observability & testing](../09-observability-and-testing/notes.md).
- **Portability has limits.** The JSON is portable; the *actions* it invokes are still org-bound Apex and Flows. Don't oversell "runs anywhere" to a client.

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — the legacy-vs-current comparison in full
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — subagents and routing
- [Observability & testing](../09-observability-and-testing/notes.md) — proving behaviour, not just structure
- [Custom Agent Actions](../05-custom-agent-actions/notes.md) — what the script invokes
- [Model Builder & BYOM](../06-model-builder-byom/notes.md) — what model pinning selects from
- [Capstone: Agentforce use case](../../04-capstone/03-agentforce-use-case/notes.md) — build it for real
