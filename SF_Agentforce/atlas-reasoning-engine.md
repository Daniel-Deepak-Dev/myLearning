---
vault: SF_Agentforce
format: light
level: basic
status: complete
org_checks: 1
labs: 4
created: 2026-08-27
updated: 2026-08-28
---
# Atlas Reasoning Engine

**One line:** The reasoning and planning engine behind Agentforce — the part that decides what to do, not the part that says it.

**Reach for it when:** Explaining why an agent picked the action it picked.

## Key points

- Salesforce calls it the **"brain" of Agentforce**. It sits between the user's request and the actions available.
- The published loop is **plan → retrieve → reason → act → refine**. It **refines the query first**, expanding it with context before retrieving anything.
- Retrieval is **RAG**, and it assesses the quality of its own response rather than answering blindly.
- It runs a **ReAct loop** — reason, act, observe — repeating until the goal is met or it gives up.
- **The loop is bounded: up to seven reasoning loops per user message**, reading roughly the **last six turns**. 🚩 both figures come from a search snippet of a JS-rendered Help page.
- **Version 3.0 routes to subagents by reading their descriptions**, not by following a fixed decision tree.
- **Atlas itself is not configurable.** You author the agent around it — subagents, topics, actions, and **Agent Script** reasoning blocks: variables, action order, if/else, transitions, instruction text.
- **The platform fixes the rest** — top-to-bottom processing of reasoning instructions, how the resolved prompt is assembled, and when the LLM sees it.

## Seeing the reasoning afterwards

**Agentforce Session Tracing**, keyed by session ID: turn-by-turn interactions, reasoning-engine executions, actions, prompt and gateway input/output, errors, final response. Underneath sit two Data 360 DMOs joined on trace ID — `ssot__TelemetryTraceSpan__dlm` (LLM calls, flow runs, Apex invocations, durations, `ERROR` status) and `ssot__AiAgentInteraction__dlm` (the conversation).

> **From my notes.** *"Agentic Orchestration Framework"* — close, but it undersells it. Orchestration implies routing to a predefined path. Atlas **plans**: it decides what to retrieve, judges whether the answer is good enough, and loops. Routing is one thing it does, not the whole job.

## Gotchas

- **A vague subagent description is a bug, not a style problem.** From v3.0 the description *is* what routing reads. Vague ones cause intermittent mis-routing that looks like a model failure.
- **"The agent ignored my instruction" is usually a retrieval or routing problem**, not a prompt-wording problem.
- **A transition command discards the resolved prompt.** Reasoning ends there and the target subagent starts fresh — anything the block had built is thrown away.
- **Session Tracing needs Data 360.** Without it you have no after-the-fact view of a reasoning run at all.

## Confirm in org

- 🚩 How it breaks a tie between two actions whose descriptions both fit. Docs give the cure — make descriptions distinct — but never state a tie-break rule.

## Hands-on

- [ ] **AF-ATLAS-01** · 30 min · Hold one agent conversation, then read its session trace end to end. **Proves:** the reasoning is visible after the fact, keyed by session ID. **Needs:** Data 360.
- [ ] **AF-ATLAS-02** · 30 min · Give two subagents overlapping descriptions, force a mis-route, then fix it with explicit "does not handle" wording. **Settles:** how it breaks a tie 🚩. **Needs:** Data 360.
- [ ] **AF-ATLAS-03** · 20 min · Query `ssot__TelemetryTraceSpan__dlm` for `ERROR` spans and their durations. **Proves:** where the chain broke, and what each step cost. **Needs:** Data 360.
- [ ] **AF-ATLAS-04** · 25 min · Give the agent a task needing many actions, then count the loops in the trace. **Proves:** the loop is bounded — check the count against the seven-loop figure. **Needs:** Data 360.

## Related

- [Einstein Trust Layer](einstein-trust-layer.md) — the guardrails wrapped around everything Atlas sends and receives
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — how a template becomes something Atlas can choose to call
- [SF_core · 22 Invocable Apex & Agentforce actions](../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — why an action's `description` is read as prompt text, not documentation
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — the Flow action this engine chooses between, and the description it reads to decide

## Sources

- [How Agentforce Works](https://help.salesforce.com/s/articleView?language=en_US&id=ai.agent_reasoning_engine.htm&type=5) — Salesforce Help · via search 2026-08-28 — JS-rendered; the seven-loop and six-turn figures come from the search snippet, not the page
- [Flow of Control — Agent Script](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-flow.html) — Salesforce Developers · read 2026-08-28 · what the author controls, and what ends reasoning
- [About Agentforce Session Tracing](https://help.salesforce.com/s/articleView?id=ai.generative_ai_session_trace_about.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28
- [Agent Platform Tracing: Trace Trees, SOQL, and Slack](https://developer.salesforce.com/blogs/2026/05/agent-platform-tracing-debug-agentforce-with-trace-trees-soql-and-slack) — Salesforce Developers · read 2026-08-28 · the two trace DMOs

## History

- 2026-08-27 · created from your Day-3 terms note · sharpened the "orchestration framework" definition
- 2026-08-28 · added the configurable-vs-fixed split, the bounded loop, the transition-discards-prompt gotcha, and where the reasoning is visible afterwards
