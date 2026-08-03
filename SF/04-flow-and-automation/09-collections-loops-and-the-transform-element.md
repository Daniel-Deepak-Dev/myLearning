# Collections, Loops & the Transform Element

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** Working with more than one record — collection resources, the loop patterns worth keeping, and the **Transform** element that replaces most of them. Limit numbers live in [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md).

## Core idea

Flow's Loop element is the most-used and most-misused element on the canvas, and the reason is that it looks like a `for` loop while behaving like a governor-limit multiplier. Every Data element inside a loop body executes once per iteration, so a Get Records inside a loop over 200 records is 200 SOQL queries and a flow that dies on the 101st. The correct instinct is that **a loop should contain no Data elements at all** — you query once outside, iterate over the collection in memory, add to an output collection, and do a single Create or Update after the loop. Since Summer '24 there is a better answer still for the most common case: **Transform**, which maps one collection onto another declaratively, with no loop at all, roughly ten times faster and without touching the loop-iteration budget.

## How it works

| Need | Element |
|---|---|
| Query many records once | Get Records, with filter and sort |
| Narrow a collection in memory | **Collection Filter** — no SOQL |
| Reorder a collection in memory | **Collection Sort** — no SOQL |
| Map collection A to collection B | **Transform** — no loop |
| Genuinely per-item branching | Loop + Assignment, Data elements **outside** |

- **Transform (Beta Winter '24, GA Summer '24)** maps source fields to target fields, with a formula per target where needed. Available in **screen, autolaunched-without-trigger and record-triggered** flows.
- **Transform's real reach is nested data.** It flattens **Apex-defined types** → [11](11-flow-and-apex-interop.md) and **HTTP callout responses** → [12](12-http-callout-and-external-services-in-flow.md) into record collections, which is where the loop-and-assign pattern was ugliest.
- **Its two structural limits**: at most **one nested collection** per transformation, and an Apex-defined resource may be referenced **10 levels deep**.
- **Collection Filter and Collection Sort cost nothing** — they operate on a collection already in memory. Filtering in a loop with a Decision does the same job for more elements.
- **The bulk pattern that always works**: Get once → Loop → Assignment into a collection → single Create/Update **after** the loop.

## 2026 currency

Transform has been steadily absorbing work that used to need a loop. **Spring '25 added merging several collections into one**, which covers the "display related records together" case that previously needed nested loops. **Summer '26 added Transform Mode inside the action property panel**, so a transformation can be defined where an action's inputs are configured rather than as a separate canvas element — the same capability, one element fewer. Alongside it, actions gained **Formula Mode** for writing a formula directly into a parameter. Both reduce element count — though **not for the reason usually given**: the 2,000-executed-elements cap was removed at API 57.0, so what fewer elements actually buy you is CPU time, which is the limit a large loop now hits. → [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md), [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **A Get Records inside a Loop is one SOQL query per iteration.** This is the classic production failure in this area, and the fix is always to query outside the loop.
- **An Update Records inside a Loop is one DML statement per iteration** — the same failure, with a lower ceiling.
- **A Subflow inside a Loop hides the same problem behind one element.** Everything inside it runs per iteration. → [08](08-subflows-and-modular-flow-design.md)
- **The loop variable is a copy.** Assigning to it does not change the collection; you have to add it to a new collection.
- **Transform handles one nested collection per transformation.** Two levels of nesting needs two Transforms or a loop.
- **Transform is not offered in every flow type.** If the element is missing, the trigger type is why — check before designing around it.
- **A collection variable and a record collection are not interchangeable.** A Data Table's output is a collection even when the user selected one row, and assigning it to a single record variable fails at run time.
- **`Collection Filter` cannot reach related records.** It filters fields already on the records in the collection; anything cross-object still needs a query.

## Recall

Q: Why is a Get Records element inside a Loop a production bug?
A: It runs once per iteration — 200 records is 200 SOQL queries, and the flow fails at the 100-query limit.

Q: What is the bulk-safe loop pattern?
A: Query once before the loop, iterate in memory, assign into an output collection, and do a single Create or Update after the loop.

Q: When did the Transform element go GA, and what does it replace?
A: Summer '24, after a Winter '24 beta. It replaces the loop-and-assign pattern for mapping one collection onto another, about ten times faster.

Q: What are Transform's two structural limits?
A: One nested collection per transformation, and Apex-defined resources may be referenced up to 10 levels deep.

Q: What does Summer '26's Transform Mode change?
A: A transformation can be defined inside an action's property panel rather than as a separate canvas element, reducing element count.

## Related

- [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md) — the actual numbers behind every rule in this note
- [12 · HTTP callout & External Services](12-http-callout-and-external-services-in-flow.md) — the nested JSON responses Transform exists to flatten
- [02-apex · 08 Bulkification patterns](../02-apex-and-triggers/08-bulkification-patterns.md) — the same discipline in code, where the limits are identical
