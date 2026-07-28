# Agentforce Anatomy — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

An agent = actions + grounding + guardrails, wired together by **Agent Script** (compiled, diffable) and executed by **Atlas Reasoning Engine 3.0** — which replaced the prose-based topics-and-instructions model in July 2026.

## Key terms
| Term | Definition |
|---|---|
| Agent Script | Human-readable language compiling to portable JSON. Apache 2.0 open source. The current authoring model. |
| Topic | **Legacy.** Job category grouping actions + instructions. Editable, no longer creatable. |
| Hybrid Reasoning | The dial: how much is deterministic business logic vs. left to the LLM. |
| Service vs Employee Agent | Customer-facing/anonymous vs internal/authenticated. Drives the security model. |
| Triggered Agent | Fires on an event (deal stage change, Data 360 signal), not on a human utterance. |

## Rules of thumb

- **Subagent descriptions are executable config**, not labels — Atlas 3.0 routes on them. Write like an API doc.
- Return **typed structures** from actions, not prose: a Custom Lightning Type then renders them on every surface for free.
- Legacy agent to migrate? One-click upgrade converts everything to Agent Script, then diff behaviours in preview.
- Cost scales with **actions**, so orchestration depth is a budget decision.

## Exam traps / common confusions

- **Week of July 13, 2026:** *New Agent* stopped opening the legacy builder. Creation removed — **not** editing, activation, versioning or management.
- Most tutorials online still teach topics-and-instructions. Check the publication date.
- Apex actions at 67.0 run in **user mode**, and invocable input classes need a **visible no-arg constructor** — this breaks existing actions.
- **Unresolved:** MAO is dated GA (June 15, 2026) but Help still labels *Connect Agent as Subagent* **(Beta)**. Verify in-org before quoting.

## Minimal example

Runtime path, compressed:

```
utterance/trigger → Trust Layer (injection check, mask)
   → Atlas 3.0 plans → routes to subagent BY DESCRIPTION
   → selects action → grounds (retriever / Data Library)
   → executes (Apex now USER MODE by default)
   → Trust Layer unmasks + audits → renders
```
