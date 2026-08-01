# Agentforce Anatomy

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Roadmap scope:** Agents, topics, actions, instructions — and how the Atlas Reasoning Engine plans and picks actions at runtime.

> ⚠️ **This topic changed more than any other in 2026.** The roadmap scope line above was written against the *legacy* model. Topics-and-instructions is no longer how you author an agent. Read the "Two authoring models" section before anything else — and be aware that most tutorials, videos and blog posts you'll find online still teach the retired model.

## What is it?

An Agentforce agent is a configured unit that receives a request, decides what to do, and executes work against CRM — with the deciding done by an LLM and the executing done by ordinary platform artifacts (Flow, Apex, prompt templates, API calls).

### The parts, regardless of authoring model

| Part | What it is |
|---|---|
| **Agent** | The deployed unit. Has a type (Service = customer-facing/anonymous; Employee = internal/authenticated), channels, and a model. |
| **Actions** | What it can actually *do*: autolaunched Flow, `@InvocableMethod` Apex, prompt template, Apex REST, `@AuraEnabled` method, external API. |
| **Grounding** | The data it answers from: retrievers, Agentforce Data Libraries, record context, data graphs. |
| **Reasoning** | **Atlas Reasoning Engine 3.0** — interprets the request, plans steps, selects actions and routes to subagents. |
| **Guardrails** | Instructions plus the Einstein Trust Layer sitting under every interaction. |

What changed in 2026 is not the parts. It's **how you specify the wiring between them**.

## Two authoring models — and which one is current

### Legacy: topics → actions → instructions (2024–mid 2026)

You created **topics** (job categories), attached **actions** to each, and wrote **instructions** in natural language telling the agent when to use what. The LLM classified the incoming request into a topic, then chose an action inside it.

**Status:** existing legacy agents can still be **edited, activated, versioned and managed**. But since the **week of July 13, 2026**, the *New Agent* button in Setup no longer opens the legacy builder — you cannot create a new agent this way.

**Why it was replaced:** behaviour was specified entirely in prose. Two instructions could quietly contradict each other, there was no diff worth reviewing, nothing compiled, and nothing could be tested outside an org. Reliability problems were untraceable because there was no artifact to trace.

### Current: Agent Script in Agentforce Builder

**Agent Script** is a human-readable expression language that **compiles to portable JSON**. It blends deterministic control flow (conditionals, if/then, explicit hand-offs, precise tool invocation) with agentic LLM reasoning. Salesforce calls the resulting dial **Hybrid Reasoning**: you choose how much is structured business logic and how much is left to the model.

It is **open source under Apache 2.0** — parser, linter, compiler, LSP and editor integrations at [github.com/salesforce/agentscript](https://github.com/salesforce/agentscript).

**Migration:** upgrading a legacy agent is one click. It converts all subagents, actions, system messages, data and connections into Agent Script, then optionally optimizes the result for reliability.

Depth on the language itself lives in [07-agent-script/](../07-agent-script/notes.md).

### The comparison that matters

| | Legacy topics | Agent Script |
|---|---|---|
| Specified in | Natural-language prose | Compiled expression language |
| Artifact | Org config | Portable JSON, diffable |
| Testable outside an org | No | **Yes** — open-source compiler, plain CI job |
| Model choice | Org-wide setting | **Pinned per agent in the script** |
| Determinism | Whatever the LLM inferred | Dialled explicitly |
| Reviewable in a PR | No | Yes |

**The architect's takeaway:** agent definitions became source code. That single change is what lets agents enter a CI/CD pipeline, and it's why this is the Agentforce skill of 2026.

## How it works

### Runtime flow

```
user utterance / trigger event
        │
        ▼
  Einstein Trust Layer  ── prompt-injection check, masking
        │
        ▼
  Atlas Reasoning Engine 3.0
        │   plans steps
        ├──► routes to a SUBAGENT ── by reading its *description*
        │
        ▼
  selects ACTION(s)
        │
        ▼
  grounding: retriever / Data Library / record context
        │
        ▼
  action executes  ── Flow · Apex · prompt template · API
        │            (Apex now runs in USER MODE by default at 67.0)
        ▼
  Trust Layer ── unmask, toxicity score, audit-log the whole interaction
        │
        ▼
  response  ── rendered via Custom Lightning Type if output is structured
```

Two things on that diagram are new in 2026 and both are exam-relevant: **routing happens on subagent descriptions**, and **Apex actions run in user mode** unless you opt out.

### Agent types

- **Service Agent** — customer-facing, **anonymous** (no login). Good for public apps and portals.
- **Employee Agent** — internal, **authenticated**; the SDK obtains OAuth tokens.

This distinction drives the security model, so it's a common exam discriminator.

### Triggered agents

Agents no longer only respond to utterances. A **triggered agent** fires on a defined event — a deal stage change, a customer signal from Data 360 — and acts without a human initiating. Worth internalizing: it removes the "a human is always in the loop" assumption that older designs relied on for safety.

### Surfaces

Lightning, Slack, mobile (Agentforce Mobile SDK — iOS, Android, React Native), **Agentforce Voice** with human takeover mid-call, web, portal, and MCP clients. One agent definition, many surfaces. If an action returns a **typed structure** rather than prose, a Custom Lightning Type renders it idiomatically on every one of them.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Create one agent in Agentforce Builder. Note that you land in Agent Script whether or not you expected to.
- [ ] **The key exercise:** take an existing topic-based agent, run the one-click upgrade, then diff the two behaviours in preview. This is the single most instructive hour in this track.
- [ ] `sf agent preview start` → `send` → `end`, then read the **trace file** to see exactly how it routed and acted.
- [ ] Scaffold the CLI `agent` template — it generates a runnable **Local Info Agent** demonstrating Apex, Prompt Template and Flow subagents.

## Gotchas & sharp edges

- **Most online material teaches the retired model.** Anything written before mid-2026 shows topics-and-instructions as current. Check the date before trusting a tutorial.
- **Legacy agents didn't stop working.** The cutoff removed *creation*, not management. "Legacy agents were deleted" is wrong.
- **A vague subagent description is a bug, not a style issue.** Atlas 3.0 routes on it. Vague descriptions produce intermittent mis-routing that looks like a model failure but is a specification failure. Write them like API docs.
- **Apex actions may break on an API bump.** Custom Apex types used as invocable action inputs need a **visible no-arg constructor** (public, or global for packaged classes) — **from API 66.0**, with the Release Update auto-enforcing in Summer '26. Detail in [custom agent actions](../05-custom-agent-actions/notes.md).
- **You pay per action, not per conversation.** ~20 credits (~$0.10) each. A five-step resolution is five charges; an orchestrator through three subagents multiplies again. Chatty grounding loops cost real money.
- **Doc conflict, unresolved:** Multi-Agent Orchestration is dated GA June 15, 2026, but Salesforce Help still labels the in-builder *Connect Agent as Subagent* step **(Beta)**. Verify in your own org before quoting a status to a client.
- **Agent Script isn't named in the Agentforce Specialist exam guide** despite being the default authoring model. Given the guide's emphasis on deterministic behaviour, filters and variables, assume it's implicitly in scope — and re-check the guide before booking.

## Related topics

- [Agent Script](../07-agent-script/notes.md) — the language, in depth
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — orchestrators and subagent routing
- [Observability & testing](../09-observability-and-testing/notes.md) — proving the agent is good
- [Custom Agent Actions](../05-custom-agent-actions/notes.md) — the 67.0 security changes that bite here
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — what wraps every interaction
- [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) — where grounding comes from
