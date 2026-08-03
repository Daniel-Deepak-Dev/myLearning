# Record-Triggered Flows

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The single flow type that carries most declarative automation — trigger configuration, before-save vs after-save, and entry criteria. Run order across *several* flows on one object is [14 · Trigger order](14-trigger-order-and-flow-trigger-explorer.md).

## Core idea

Everything about a record-triggered flow follows from one choice made in the Start element and never revisited: **before-save or after-save**. A before-save flow runs at step 3 of the save order, ahead of every before trigger, and it modifies `$Record` in memory — no DML, no extra query, and it is the fastest automation the platform has by a wide margin. An after-save flow runs at step 14, after the record is written, and it can do everything else: touch related records, call actions, send email. The two are not variants of the same tool. Choosing before-save when you only need to set a field on the triggering record is the difference between a flow that costs nothing and a flow that costs a DML statement per save. In the UI the choice is disguised as a performance question — *Optimize the Flow for* — which is why so many flows are built on the wrong one.

## How it works

| Setting | Value | Effect |
|---|---|---|
| *Optimize the Flow for* | **Fast Field Updates** | **before-save**, step 3, modifies `$Record` in memory |
| | **Actions and Related Records** | **after-save**, step 14, everything else |
| Trigger | Created / Updated / Created or Updated / Deleted | deleted is after-save only |
| Entry conditions | formula or condition builder | evaluated before the flow starts |
| *Only when a record is updated to meet the condition requirements* | checkbox | fires on the **transition**, not on every qualifying save |

- **`$Record` is the new version; `$Record__Prior` is the old one.** `$Record__Prior` is null on create and unavailable in before-save *insert* context.
- **Assign to `$Record` in a before-save flow — never use an Update Records element on the triggering record.** The element costs a DML statement and re-enters the save order; the assignment costs nothing.
- **Entry criteria are the cheapest optimisation available.** A flow that starts and immediately hits a Decision that sends it nowhere has already paid to start.
- **Scheduled paths** run after commit at an offset from a date field or from the trigger; **async paths** run after commit in a separate transaction. → [07](07-platform-event-and-async-path-flows.md)
- **Deleted-record flows** cannot modify the record and run before the delete commits.

## 2026 currency

Summer '26's ~20 new **Decision date operators** land here more than anywhere else, because record-triggered entry logic is mostly date comparison: `Is Today`, `Is Anniversary of Today`, `Last N Days`, `Next N Months` and the rest replace formula resources built for exactly that. **They do not support DateTime**, so `LastModifiedDate` logic still needs a formula. The structural point has not moved since Winter '23: with the legacy tools out of support, before-save and after-save flows now bracket your Apex on both sides of the save order rather than trailing it, which makes trigger re-entry *more* likely than under the old model. → [02-apex · 07](../02-apex-and-triggers/07-order-of-execution-and-recursion.md)

## Gotchas

- **Using an Update Records element on the triggering record in a before-save flow** costs a DML statement and re-enters the save order. Assign to `$Record` instead.
- **`$Record__Prior` is null on insert.** A formula comparing it without a null guard evaluates in ways nobody predicts.
- **Leaving *Only when a record is updated to meet the condition requirements* unchecked** means the flow fires on every save that still matches — including saves your own automation caused. This is the usual recursion source.
- **Entry criteria are not a substitute for a recursion guard** when two flows update each other; there is no `static` in Flow. → [02-apex · 07](../02-apex-and-triggers/07-order-of-execution-and-recursion.md)
- **A before-save flow cannot make a callout, send email, or call most actions.** If the builder greys an action out, the trigger type is why.
- **Roll-up summary fields are stale in an after-save flow** — they recalculate at steps 16–17, after step 14.
- **Changing *Optimize the Flow for* on an existing flow is not a toggle** in practice; the elements valid on one side are often invalid on the other.

## Recall

Q: Which *Optimize the Flow for* value produces a before-save flow, and where does it run?
A: **Fast Field Updates** — step 3 of the save order, ahead of every before trigger, modifying `$Record` in memory.

Q: How do you set a field on the triggering record in a before-save flow?
A: Assign to `$Record`. An Update Records element costs a DML statement and re-enters the save order.

Q: What does `$Record__Prior` hold, and when is it unusable?
A: The pre-save version of the record. It is null on insert.

Q: What does the *"Only when a record is updated to meet the condition requirements"* checkbox change?
A: The flow fires only on the transition into the criteria, not on every subsequent save that still matches.

Q: Why can't a before-save flow make a callout?
A: It runs inside the save transaction before the record is written; callouts and most actions require the after-save or asynchronous context.

## Related

- [14 · Trigger order & Flow Trigger Explorer](14-trigger-order-and-flow-trigger-explorer.md) — what happens when several flows sit on the same object
- [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — the canonical 20-step pipeline steps 3 and 14 belong to
- [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md) — how a record-triggered flow blocks a save and rolls it back
