# Flow Limits & Bulkification

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** The budget a flow spends, and the shape of a flow that stays inside it. The *patterns* — Transform, collection filters, loop hygiene — belong to [09](09-collections-loops-and-the-transform-element.md); this note owns the numbers.

> **What changed.** *"A flow can execute only 2,000 elements per interview"* is the most-quoted Flow limit on the internet and it was **removed in Spring '23**. Two qualifications make it worth stating carefully: it is removed only for flows saved at **API 57.0 or later**, so an inherited flow still sitting at 55.0 keeps the ceiling — and removing it **moved** the failure rather than deleting it. The wall a large loop hits now is **CPU time at 10 seconds**, which arrives with a far less helpful error message.

## Core idea

Flow spends the same per-transaction budget as Apex, out of the same pot, in the same transaction — and it gives you less control over how. That single sentence answers most "should this be Flow or Apex?" arguments, because the honest answer is that moving the logic to Apex usually does not raise the ceiling; it only makes the spending visible. The two things worth internalising are that **limits are per transaction, not per flow** — your flow shares with every trigger, workflow field update and other flow in the same save — and that Flow's automatic bulkification is real but shallow. It batches identical operations *across interviews at the same element*, which is why 200 records saved together cost one DML statement at an Update element. It cannot batch across *iterations of your loop*, which is why the same element inside a loop costs 200.

> **From my notes.** *"How to reduce CPU time: convert Process Builder, flows to Apex Triggers if possible."* The numbers on that page are still right — **10 seconds sync, 60 asynchronous**, plus heap at **6 MB / 12 MB** — and its list of causes is a good one: circular updates between two objects, recursion, DML'ing and querying the same object repeatedly, nested loops more than two deep. **The advice is not right.** Apex spends the same CPU budget on the same work; rewriting a flow in Apex only helps if you bulkify while you are there, and the rest of that page's own list — recursion, nested loops, repeated DML — is exactly what you would carry across unchanged.

## How it works

| Limit | Value | Shared with |
|---|---|---|
| SOQL queries | **100** | Apex, triggers, other flows |
| Query rows returned | **50,000** | everything in the transaction |
| DML statements | **150** | everything in the transaction |
| DML rows processed | **10,000** | everything in the transaction |
| CPU time | **10,000 ms** sync, 60,000 ms async | everything in the transaction |
| Executed elements per interview | **removed at API 57.0** | — |
| Flow interview size | **1,000,000 bytes** | — |

- **A record-triggered flow runs one interview per record**, and the platform groups the same element across those interviews into one operation. This is why "Flow bulkifies for you" is true and misleading in equal measure.
- **A loop breaks that grouping.** A Get or Update element inside a loop executes once per iteration, per interview, and multiplies out. This is the single failure mode behind most "works in sandbox, dies on a data load" reports.
- **A subflow shares the transaction.** One SOQL budget and one DML budget however deep the nesting — factoring a flow buys maintainability and **zero** limit relief. → [08](08-subflows-and-modular-flow-design.md)
- **Interview size matters only where an interview persists** — pausing or waiting serialises state, and an interview holding a large collection cannot be persisted at all. → [20](20-pause-wait-and-waiting-interviews.md)
- **A separate transaction is the only real relief**: an async path, a scheduled path, or a platform event each start fresh. → [07](07-platform-event-and-async-path-flows.md)

## 2026 currency

The removal of the element cap is three years old and still not in general circulation, which makes it the most useful thing to know here. Summer '26 adds two levers that reduce element count directly: **Formula Mode and Transform Mode inside the action property panel** collapse a resource plus an element into one configuration, and **a configurable batch size of 1–200 on schedule-triggered flows** finally lets you trade throughput for headroom the way `Database.executeBatch(job, scopeSize)` does in Apex → [06](06-scheduled-and-autolaunched-flows.md). The **Element Error Rate column** on the Flows list view is the first native way to find which element is actually failing in production rather than guessing. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **DML inside a loop.** The classic production failure, and it is invisible at one record. Build the collection in the loop, write it after.
- **A Get Records inside a loop is the same bug** and costs SOQL instead of DML. It hits the 100 ceiling faster than DML hits 150.
- **The element cap is only gone if the flow is at API 57.0+.** Check the version on an inherited flow before assuming.
- **Limits are per transaction, not per flow.** Your flow can be blameless and still be the one that throws.
- **CPU time is the limit with no good error message.** `Apex CPU time limit exceeded` from a flow names no element; the Element Error Rate column and a debug run are how you find it.
- **Get Records with no filter and no limit returns up to 50,000 rows into memory** and can exhaust the interview size on its own.
- **Twelve is the ceiling on repeated updates to the same record in one transaction**, and mutually triggering flows reach it quickly. → [14](14-trigger-order-and-flow-trigger-explorer.md)
- **"Move it to Apex" is not a limits fix.** Same transaction, same budget. It is a *control* fix, and only if you then bulkify.

## Recall

Q: What happened to the 2,000-executed-elements limit, and what is the catch?
A: Removed in Spring '23 — but only for flows saved at **API 57.0 or later**, and CPU time at 10 seconds becomes the new binding wall.

Q: Why does a Get Records element inside a loop behave so differently from the same element outside it?
A: Flow batches an element across interviews, not across loop iterations. Outside the loop it costs one query; inside it costs one per iteration.

Q: What does factoring a flow into subflows do to your governor budget?
A: Nothing. Parent and subflows share one transaction, one SOQL budget and one DML budget.

Q: Name the only genuine way to get a fresh limit budget from Flow.
A: Leave the transaction — an async path, a scheduled path, or a platform event-triggered flow.

Q: Whose limits are you spending when your flow throws a limit exception?
A: The transaction's. Every trigger, flow and workflow field update in the same save shares one pot.

## Related

- [09 · Collections, loops & Transform](09-collections-loops-and-the-transform-element.md) — the patterns that keep you under these numbers
- [02-apex · 01 Governor limits](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md) — the same budget, described from the code side
- [20 · Pause, Wait & waiting interviews](20-pause-wait-and-waiting-interviews.md) — where interview size stops being theoretical
