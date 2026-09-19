# Atlas Reasoning Engine

> Folder: SF_Agentforce · Level: basic · Status: 🌱 4 gaps open
> Created: 2026-08-27 · Updated: 2026-08-27

**One line:** The reasoning and planning engine behind Agentforce — the part that decides what to do, not the part that says it.

**Reach for it when:** Explaining why an agent picked the action it picked.

## Key points

- Salesforce calls it the **"brain" of Agentforce**. It sits between the user's request and the actions available.
- The published loop is **plan → retrieve → reason → act → refine**.
- It **refines the query first**, expanding it with context before retrieving anything.
- Retrieval is **RAG**, and it assesses the quality of its own response rather than answering blindly.
- It runs a **ReAct loop** — reason, act, observe — repeating until the goal is met or it gives up.
- Salesforce describes this as **System 2 inference-time reasoning**: deliberate rather than reflexive.
- **Version 3.0 routes to subagents by reading their descriptions**, not by following a fixed decision tree.

> **From my notes.** *"Agentic Orchestration Framework"* — close, but it undersells it. Orchestration implies routing to a predefined path. Atlas **plans**: it decides what to retrieve, judges whether the answer is good enough, and loops. Routing is one thing it does, not the whole job.

## Gotchas

- **A vague subagent description is a bug, not a style problem.** From v3.0 the description *is* what routing reads. Vague ones cause intermittent mis-routing that looks like a model failure.
- **"The agent ignored my instruction" is usually a retrieval or routing problem**, not a prompt-wording problem.

## Gaps to close

- [ ] What is actually configurable about Atlas, and what is fixed platform behaviour?
- [ ] Where do you see its reasoning after the fact — is there a trace or a log?
- [ ] What makes it stop looping — a step limit, a confidence threshold, or something else?
- [ ] How does it choose between two actions whose descriptions both fit?

## Related

- [Einstein Trust Layer](einstein-trust-layer.md) — the guardrails wrapped around everything Atlas sends and receives
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — how a template becomes something Atlas can choose to call
- [SF_core · 22 Invocable Apex & Agentforce actions](../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — why an action's `description` is read as prompt text, not documentation

## Sources

- [How the Atlas Reasoning Engine Powers Agentforce](https://www.salesforce.com/agentforce/what-is-a-reasoning-engine/atlas/) — Salesforce · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Discover the Atlas Reasoning Engine](https://trailhead.salesforce.com/content/learn/modules/reasoning-in-artificial-intelligence/discover-the-atlas-reasoning-engine) — Trailhead · via search 2026-08-27 — page is JS-rendered, open it to verify
- [Inside Agentforce: Revealing the Atlas Reasoning Engine](https://engineering.salesforce.com/inside-the-brain-of-agentforce-revealing-the-atlas-reasoning-engine/) — Salesforce Engineering · via search 2026-08-27 — page is JS-rendered, open it to verify

## History

- 2026-08-27 · created from your Day-3 terms note · sharpened the "orchestration framework" definition
