# Formula Fields & Roll-Up Summaries

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** The two declarative calculation mechanisms — read-time formulas and save-time roll-ups — their size limits, and where each stops being the right tool.

## Core idea

A **formula field** is computed every time it is read and stored nowhere. A **roll-up summary field** is computed when children change and *is* stored on the parent. That single difference drives everything else: formulas are always current but cannot be indexed or filtered efficiently, while roll-ups are queryable like any real column but only exist on master-detail parents. Both have hard ceilings that arrive sooner than people expect — a formula's limit is measured on the *compiled* expression including everything it transitively references, so a formula referencing three other formulas can fail while looking short.

## How it works

- **Formula limits** — 3,900 characters of source, 4,000 bytes saved, **5,000 bytes compiled**, 1,300 characters displayed. Compile size includes every field, value and referenced formula, so whitespace and comments do not help.
- **Cross-object formulas** traverse `__r` relationships up to **10 relationships away**, with a ceiling of **10 unique relationships per object** across all its formulas.
- **Roll-up summaries** require a **master-detail** relationship. Types: `COUNT`, `SUM`, `MIN`, `MAX` — optionally filtered by criteria on the child.
- **Roll-up allocation** — **25** per object by default, raisable by Salesforce Support to a hard maximum of **40**. There is no path past 40.
- `ISBLANK()` covers empty text *and* empty numbers; `ISNULL()` does not consider `''` null for text. Prefer `ISBLANK()` for text unless you specifically want the older semantics.
- When declarative calculation runs out — non-master-detail parents, cross-object aggregation, more than 40 roll-ups — the answer is a record-triggered Flow or Apex, not a workaround formula. See [04-flow](../04-flow-and-automation/INDEX.md).

## Gotchas

- Formula fields are **not indexed by default**, so filtering a report or SOQL query on one is non-selective and degrades badly at volume. The carve-out is worth knowing: Support **can** index a **deterministic** formula — one object only, no `TODAY()`/`NOW()`, no `Id`, owner or autonumber fields. Anything cross-object is non-deterministic and never indexable — see [08-data · 08](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md).
- A formula containing `TODAY()` or `NOW()` re-evaluates on every read, so a report filtered on it gives different answers at different times and cannot be trusted for a snapshot.
- Compile size counts *transitive* references. Adding one innocuous field to a shared formula can break unrelated formulas that reference it.
- Roll-up summary recalculation happens in the save order **after** after-triggers, so an after-trigger reading the parent's roll-up sees the stale value. See [14 · Order of execution](14-order-of-execution-declarative-view.md).
- Roll-up filter criteria on a picklist behave unexpectedly when the picklist's values exceed 255 characters in total.
- A formula field cannot reference itself, and cannot reference a long text area or a multi-select picklist in most contexts.
- Deleting the last roll-up summary on a master is a prerequisite for converting master-detail → lookup, and blocks it until you do.
- Formulas returning text are limited to 1,300 *displayed* characters — longer results are silently truncated on the page.

## Recall

Q: What is the compiled size limit for a formula, and why can a short formula exceed it?
A: 5,000 bytes. Compile size includes every field, value and formula it transitively references, so a brief formula pointing at other formulas can blow the limit.

Q: How many roll-up summary fields can one object have?
A: 25 by default, raisable by Salesforce Support to a hard ceiling of 40.

Q: How far can a cross-object formula traverse, and what is the per-object ceiling?
A: Up to 10 relationships away, with a maximum of 10 unique relationships per object across all its formulas.

Q: Why is filtering a SOQL query on a formula field a performance problem?
A: It is computed at read time and normally unindexed, so the filter cannot be selective. Only a **deterministic**, single-object formula can be indexed, and only by Support — a cross-object one never can.

Q: An after-trigger reads a roll-up summary on the parent and gets a stale number. Why?
A: Roll-up recalculation happens later in the save order than after-triggers.

## Related

- [03 · Objects, fields & relationships](03-objects-fields-and-relationships.md) — why roll-ups need master-detail
- [14 · Order of execution](14-order-of-execution-declarative-view.md) — exactly when roll-ups recalculate
- [08-data · 08 Indexes & query selectivity](../08-data-modeling-and-large-data-volumes/08-indexes-and-query-selectivity.md) — selectivity, and the one formula shape that *can* be indexed
