# Trigger Order & Flow Trigger Explorer

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** What happens when several record-triggered flows sit on one object — the run order you can control, the run order you cannot, and the tool that shows you both. Configuring a single flow is [03](03-record-triggered-flows.md).

## Core idea

The old advice was one flow per object per trigger type, and it existed for exactly one reason: before Spring '22 you could not control the order in which flows ran, so the only way to sequence logic was to put it all in one flow. **Trigger Order** removed that constraint, and the advice did not update. A number between **1 and 2,000** in a flow's Advanced settings fixes its position relative to other flows *of the same trigger type on the same object* — and that qualifier is the whole subtlety. Trigger Order does not reorder before-save against after-save, and it cannot make a flow run before Apex or after a validation rule. Those positions are fixed by the save order and no setting changes them. So the modern shape is several small, well-named flows with explicit order numbers, rather than one flow with forty elements that nobody dares edit.

## How it works

| | Controls | Does not control |
|---|---|---|
| **Trigger Order** (1–2,000) | flows of the **same trigger type** on the **same object** | before-save vs after-save, Apex vs Flow, validation rules |
| **Flow Trigger Explorer** | viewing and drag-reordering that sequence | anything about Apex triggers |
| **Save order** | everything else | you |

- **Flow Trigger Explorer has existed since Spring '22**, reached from the object's flow list or from Setup, and groups flows into **Fast Field Updates** (before-save), **Actions and Related Records** (after-save) and **Run Asynchronously**.
- **Summer '22 added drag-to-reorder** behind an *Edit Order* button, which writes the Trigger Order values for you.
- **A flow with no Trigger Order runs after every flow that has one**, and ties fall back to created-date then last-modified order — which is to say, unpredictably.
- **Order is per trigger type.** A before-save flow numbered 100 still runs before an after-save flow numbered 1, because they occupy different steps of the save order entirely. → [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md)
- **Apex triggers and flows interleave by save-order step, not by any shared ordering mechanism.** There is no way to say "this flow runs after that trigger" beyond choosing before-save or after-save.

## 2026 currency

Nothing structural has changed, but the surrounding facts have and they change the recommendation. With **Workflow Rules and Process Builder out of support since 31 December 2025 — and still running** — an inherited object can have flows at steps 3 and 14 *and* legacy automation at steps 11 and 13, none of which Flow Trigger Explorer shows you. Explorer is a Flow tool, not an automation tool, and reading it as a complete picture of what happens on save is the current version of an old mistake. Summer '26's **Element Error Rate column** on the Flows list view pairs well with it: Explorer tells you what runs and in what order, the error rate column tells you which of them is failing. → [18](18-migrate-to-flow-and-legacy-retirement.md)

## Gotchas

- **Trigger Order is per trigger type**, so a low number on an after-save flow will never beat a before-save flow.
- **Unnumbered flows run last, in an order you do not control.** Number all of them or none of them; a mix is the worst case.
- **Flow Trigger Explorer does not show Apex triggers**, Workflow Rules, Process Builder, validation rules or roll-up recalculation. It is a partial map.
- **Gaps are free — use them.** Numbering 10, 20, 30 leaves room to insert later; numbering 1, 2, 3 means renumbering everything to add one flow.
- **Changing Trigger Order creates a new flow version** and needs activating like any other change. → [24](24-flow-deployment-versioning-and-governance.md)
- **Two flows that update each other still recurse regardless of order.** Order is not a recursion guard, and Flow has no `static`. → [02-apex · 07](../02-apex-and-triggers/07-order-of-execution-and-recursion.md)
- **The "one flow per object" rule is obsolete but its opposite is not a rule either.** Twelve tiny flows on Account is its own maintenance problem; the unit should be a business capability.

## Recall

Q: What exactly does Trigger Order control, and what is its range?
A: 1–2,000, controlling order among flows of the **same trigger type on the same object** — nothing else.

Q: A before-save flow is numbered 500 and an after-save flow is numbered 1. Which runs first?
A: The before-save flow, at step 3 of the save order. Trigger Order never crosses trigger types.

Q: When does a flow with no Trigger Order run?
A: After every flow that has one, with ties broken by created and last-modified date — effectively unpredictably.

Q: Since when has Flow Trigger Explorer existed, and what does it deliberately not show?
A: Spring '22. It shows only flows — not Apex triggers, legacy automation, validation rules or roll-ups.

Q: Why is "one flow per object" out of date?
A: It was a workaround for having no ordering control before Spring '22. Trigger Order replaced the need for it.

## Related

- [03 · Record-triggered flows](03-record-triggered-flows.md) — configuring the single flow whose position this note orders
- [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — the save-order steps Trigger Order operates inside
- [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md) — what several flows on one object cost from one shared budget
