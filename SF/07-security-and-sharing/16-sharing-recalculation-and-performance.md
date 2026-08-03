# Sharing Recalculation & Performance

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** What it costs the platform to keep [06](06-org-wide-defaults-and-record-access.md)–[10](10-teams-territories-and-account-sharing.md) true, and why an access change that takes a second to configure takes hours to apply. Ownership skew as a *query* problem is [08-data · 08](../08-data-modeling-and-large-data-volumes/INDEX.md); the recalculation mechanics are here.

> **What changed.** *"Change a group's membership and the share rows exist the moment the DML commits"* is on its way to being wrong. Salesforce now runs sharing recalculation **asynchronously** after group-membership and role changes when it judges that faster — rolled out from Summer '25, fully enabled April 2026, and a **Release Update available Spring '26 and enforced Spring '27**. Apex and Flow that update a group and then immediately act on newly-shared records will fail.

## Core idea

Every grant in this area resolves into a physical row in `AccountShare`, `Opportunity__Share` and the rest. Nothing is computed at read time — the platform pre-materialises the answer so queries stay fast, and pays for it at **write** time. Recalculation is the batch job that rebuilds those rows when the *rules* change, and it is the reason a five-second click in Setup can occupy an org for hours. Design conversations that ignore it produce models that are correct and unusable: the question is never only *who should see this*, but *how often does the thing that decides it change*.

## How it works

| Change | What recalculates | Rough cost |
|---|---|---|
| Tighten an **OWD** | the whole object, plus its detail children | the largest job there is — hours at LDV |
| **Role hierarchy** move | every record owned by users under the affected roles | scales with ownership, not with roles |
| **Group / queue membership** | shares derived through that group | **now often asynchronous** |
| **Sharing rule** create or edit | that rule's shares only | deferrable |
| **Owner change** on one record | that record, its implicit children, both hierarchies | small unless the parent is skewed |

- **Defer Sharing Calculation** is the tool for bulk change: the `Defer Sharing Calculation` permission unlocks Setup → Sharing Settings → *Defer Sharing*, where you suspend recalculation, make all the role and group edits, then resume once. Resuming runs a **full** recalculation, so it is a way to pay the cost once rather than a way to avoid it.
- **Granular locking** narrowed the lock scope on group membership so unrelated role and group edits no longer serialise behind each other. It is the enabling feature for large realignments — [08](08-groups-queues-and-the-grantee-model.md) owns that framing.
- **Ownership skew** — one user owning more than ~10,000 records of an object — is the classic multiplier: every role change for that user recalculates all of them. → [07](07-role-hierarchy-and-ownership.md)
- **Share rows are rows.** Teams and territories both multiply them, and they occupy storage and lengthen every future recalculation. → [10](10-teams-territories-and-account-sharing.md)
- **A sharing rule on a Public Read/Write object is dead configuration** that still costs recalculation time. → [01](01-security-model-layers-overview.md)

## 2026 currency

The asynchronous recalculation Release Update is the one to plan for. Salesforce decides dynamically — by data volume, ownership pattern and system load — whether to recalculate inline or in the background, so the same code passes in a small sandbox and fails in production. Two documented breakages: a **SOQL query or assertion for share rows with `RowCause = 'Rule'` fails when it expects them immediately**, and **`System.runAs()` does not reflect the new access** until the background work finishes. Salesforce ships a *Test asynchronous sharing recalculation in Apex tests* flag so you can force the new behaviour in a sandbox before Spring '27 enforces it. Audit anything that inserts a `GroupMember` and then asserts on access in the same test.

## Gotchas

- **The failure mode is a passing test that later fails in production**, because the platform chooses sync or async by volume. Force it with the test flag rather than trusting a small sandbox.
- **`System.runAs()` is not a shortcut around this.** After the update it sees the old access until recalculation completes.
- **Deferring sharing does not defer everything** — it suspends rule and group recalculation, not ownership changes, and the resume can run longer than the edits would have.
- **Tightening an OWD is the most expensive single action in the area.** Schedule it; do not do it at 4pm on a Friday.
- **Restriction rules never appear in a recalculation** because they are a runtime filter, not a share row. That is also why no share audit reveals them. → [11](11-restriction-rules.md)
- **Deleting a role or a public group recalculates too** — cleanup is not free, and "tidying up" an inherited org is a maintenance-window job.
- **Implicit sharing recalculation rides on account data skew.** More than ~10,000 children under one Account and every parent change is a large job. → [06](06-org-wide-defaults-and-record-access.md)

## Recall

Q: Why does the platform recalculate sharing at all, instead of evaluating access at read time?
A: Share rows are pre-materialised so reads stay fast. The cost is moved to write time, which is what recalculation is.

Q: What does the asynchronous sharing recalculation Release Update change, and when is it enforced?
A: Recalculation after group-membership and role changes may run in the background. Available Spring '26, enforced **Spring '27**.

Q: Name the two documented ways Apex breaks under it.
A: A query or assertion expecting `RowCause = 'Rule'` share rows immediately, and `System.runAs()` not yet reflecting the new access.

Q: What does Defer Sharing Calculation actually buy you?
A: It lets you make many role and group changes and pay for one full recalculation on resume, instead of one per change.

Q: Which access-model feature never triggers a recalculation?
A: Restriction rules — they filter at runtime and create no share rows.

## Related

- [07 · Role hierarchy & ownership](07-role-hierarchy-and-ownership.md) — ownership skew, the input this note prices
- [08 · Groups, queues & the grantee model](08-groups-queues-and-the-grantee-model.md) — granular locking as the realignment tool
- [10 · Teams, territories & account sharing](10-teams-territories-and-account-sharing.md) — where share-row multiplication actually comes from
- [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) — the query-side twin: skew as a selectivity problem
