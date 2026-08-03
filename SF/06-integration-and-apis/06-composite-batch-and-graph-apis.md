# Composite, Batch & Graph APIs

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** Sending several REST calls in one round trip, and — the part that actually matters — **what rolls back together**. Single calls are [04](04-rest-api-fundamentals.md); volumes past a few thousand records are [07](07-bulk-api-2.md).

## Core idea

Three resources look interchangeable and differ on exactly one axis: **the transaction boundary**. All three cut round trips; only some make a set of writes atomic. Choosing on latency alone is how integrations end up with half-created object graphs that no retry can clean up, because the second call failed after the first committed.

The second thing they buy is **referencing** — a subrequest can use an ID returned by an earlier one, so a client can create an Account and its Contacts without knowing the Account ID in advance. That removes the round trip *and* the client-side bookkeeping, which is where the other class of bugs lives.

## How it works

| Resource | Subrequests | Reference earlier results? | Rolls back together? |
|---|---|---|---|
| **Batch** (`/composite/batch`) | 25 | **no** | **no** — each is independent |
| **Composite** (`/composite`) | 25 | **yes**, via `referenceId` | **only if `allOrNone` is true** |
| **Composite Graph** (`/composite/graph`) | **500 nodes per graph** | **yes** | **yes, always** — per graph |
| **sObject Tree** (`/composite/tree`) | 200 records | parent/child by structure | yes |

- **Batch is a bundling optimisation, nothing more.** Independent reads are its use case; it cannot express a dependency and it cannot roll back.
- **Composite defaults to *not* atomic.** `allOrNone` is opt-in, and forgetting it is the single most common composite defect — the request "succeeds" with a 200 while some subrequests failed.
- **Composite Graph's atomicity is implicit and per graph.** Each graph rolls back independently, so one request can carry several graphs and have some commit while others fail — which is the feature: unrelated work does not share a fate.
- **Subrequests cannot reference across graphs.** That independence is what makes per-graph rollback coherent, and it is a modelling constraint at design time.
- **Graph requires API v50.0+**, so it is unavailable to exactly the pinned old clients most likely to need it. → [02](02-api-versions-and-the-retirement-treadmill.md)
- **The whole request counts as one API call against the org limit** — the real reason composite scales an integration's budget, beyond latency.

## 2026 currency

The resources themselves are stable; what moved is around them. **Apex invoked from a composite subrequest runs in user mode by default at 67.0** ([02-apex · 10](../02-apex-and-triggers/INDEX.md)), so a subrequest that used to see everything may now see a subset — and in an `allOrNone: false` request that surfaces as partial data rather than an error. For read-heavy shapes, **GraphQL** ([10](10-graphql-api.md)) now covers much of what composite was used for, and its Summer '26 mutation chaining (`@{ref.Record.FieldName.value}`) can reference **any field** from an earlier operation, not just an ID — a strictly larger referencing model than composite's `referenceId`.

## Gotchas

- **`allOrNone: false` returns HTTP 200 with failures inside the body.** Clients that branch on status code record success for a partially-failed write.
- **A rollback does not undo everything.** Platform events published in the transaction are not recalled, and neither are emails already sent. → [12](12-platform-event-design.md)
- **Governor limits apply to the whole composite request**, not per subrequest — 25 subrequests share one transaction's SOQL and DML budget. → [02-apex · 03](../02-apex-and-triggers/INDEX.md)
- **`referenceId` is scoped to the request.** It is not a durable key and must never be stored as one.
- **Graph's 500 nodes are nodes, not records.** A node is one subrequest; an sObject Tree node can carry many records, so the effective ceilings differ.
- **Mixed DML rules still apply.** Setup and non-setup objects in one atomic composite fail exactly as they do in Apex. → [02-apex · 03](../02-apex-and-triggers/INDEX.md)

## Recall

Q: What is the one axis on which batch, composite and graph genuinely differ?
A: The transaction boundary — what rolls back together.

Q: Does composite roll back by default?
A: No. `allOrNone` is opt-in, and omitting it is the commonest composite defect.

Q: How does Composite Graph's atomicity differ from composite's?
A: It is implicit and **per graph** — always on, and each graph succeeds or fails independently of the others in the request.

Q: Why can't subrequests reference across graphs?
A: That independence is what makes per-graph rollback coherent.

Q: How many API calls does a 25-subrequest composite request consume?
A: One, against the org's 24-hour limit.

## Related

- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — the single-call surface these bundle
- [10 · GraphQL API](10-graphql-api.md) — a larger referencing model, and the read-side alternative
- [07 · Bulk API 2.0](07-bulk-api-2.md) — where record counts outgrow all of this
- [21 · Idempotency, retries & error handling](INDEX.md) — what to do when a subrequest fails
