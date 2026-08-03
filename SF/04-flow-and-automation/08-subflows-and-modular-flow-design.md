# Subflows & Modular Flow Design

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** Reuse inside Flow — the subflow contract, what it does and does not buy you, and where to draw a module boundary. Reuse across the *code* boundary is [11](11-flow-and-apex-interop.md).

## Core idea

A subflow is a flow calling another flow, and the single most important thing to know about it is what it does **not** do: it does not start a new transaction. Parent and every nested subflow share one transaction, one SOQL budget, one DML budget and one set of limits. People reach for subflows expecting relief and get none — the benefit is maintainability, not headroom, and pretending otherwise produces a factored design that fails at exactly the same record count as the monolith did. What a subflow genuinely gives you is a **contract**: a named set of inputs and outputs that hides the implementation from every caller. That contract is also the trap, because Flow enforces it loosely — a variable's input/output flags are the only thing making it visible, and nothing stops you from removing one.

## How it works

| Rule | Detail |
|---|---|
| Callable types | **autolaunched (no trigger)** and **screen** flows |
| Transaction | **shared with the parent** — same limits, same rollback |
| Inputs | parent-set values for variables flagged *Available for input* |
| Outputs | read back from variables flagged *Available for output* |
| Nesting | allowed, and every level is still the same transaction |

- **The input/output flags are the API.** A variable with neither is private; changing a flag is a breaking change to every caller. → [02](02-flow-anatomy-and-builder-basics.md)
- **A screen subflow may only be called from a screen flow.** An autolaunched parent has no surface to render it on.
- **A platform event-triggered flow cannot call a subflow at all** — the restriction that most often forces duplication. → [07](07-platform-event-and-async-path-flows.md)
- **Record-triggered flows can call subflows**, and this is the standard way to share logic between a before-save and an after-save flow on the same object.
- **The subflow's version matters.** A parent invokes the subflow's *active* version, so activating a new subflow version changes every caller at once.

## 2026 currency

Nothing structural has changed in subflows, and that is worth stating plainly because the alternatives around them have moved. The reuse decision at 67.0 is now three-way rather than two-way: a **subflow** for declarative logic that stays inside Flow, an **invocable Apex action** when the logic needs data structures Flow lacks → [11](11-flow-and-apex-interop.md), and an **autolaunched flow exposed as an agent action**, which is the same artefact as a subflow but reached through a description rather than a call → [23 · Flows as agent actions](23-flows-as-agentforce-actions.md). The practical consequence is that an autolaunched flow built as a clean, well-named contract now has three possible callers instead of one, which raises the value of naming it for *what it does* rather than for the parent that first needed it.

> **From my notes.** In a sixteen-line 2023 Flow agenda exactly one box was ticked — *"Use Sub Flow to communicate with main flow"* — and the page holds nothing but a video link. The thing the note never recorded is the thing that matters: **the communication is the easy half.** Passing values in and out is a checkbox. Knowing that no transaction boundary came with them is what stops the design from failing at scale.

## Gotchas

- **A subflow buys no limit relief whatsoever.** One transaction, one budget, however deep the nesting.
- **Un-flagging a variable breaks every parent silently at design time** — callers keep their now-dangling assignment until someone opens them.
- **A subflow inside a Loop is the same anti-pattern as a Get Records inside a loop**, magnified: every element inside it runs per iteration. → [09](09-collections-loops-and-the-transform-element.md)
- **Activating a new subflow version changes all callers immediately.** There is no per-caller version pinning.
- **Platform event-triggered flows cannot call subflows**, so shared logic must become an invocable action or be duplicated.
- **A fault inside a subflow propagates to the parent** unless the subflow handles it, and an unhandled one takes down the whole interview. → [10](10-fault-paths-and-custom-errors.md)
- **Naming a subflow after its first caller** guarantees the second caller will not find it. Name it for the operation.

## Recall

Q: Does a subflow run in its own transaction?
A: No. Parent and all nested subflows share one transaction and one set of governor limits.

Q: What makes a subflow variable visible to its parent?
A: The *Available for input* and *Available for output* flags — they are the subflow's public contract.

Q: Which flow types can be used as a subflow?
A: Autolaunched flows with no trigger, and screen flows — the latter only from a screen flow parent.

Q: Which flow type cannot call a subflow at all?
A: A platform event-triggered flow.

Q: What happens to existing callers when you activate a new version of a subflow?
A: All of them switch to it at once — a parent always invokes the subflow's active version, and there is no per-caller pinning.

## Related

- [02 · Flow anatomy & builder basics](02-flow-anatomy-and-builder-basics.md) — where the input/output flags live and what a resource is
- [11 · Flow & Apex interop](11-flow-and-apex-interop.md) — the other reuse boundary, for logic Flow cannot express
- [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md) — the budget a subflow shares rather than extends
