# Idempotency, retries & error handling

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** The distributed-systems layer that integration reviews actually fail on. No Salesforce docs page owns it, which is why it has a note. Platform-specific error surfaces are [24](24-api-limits-monitoring-and-access-control.md).

## Core idea

Two facts do all the work here. **A timeout is not a failure** — it means you do not know whether the work happened. And **every event bus on this platform is at-least-once**, so a consumer will eventually see the same event twice. Neither is a bug to fix; both are properties to design around.

The consequence is that correctness comes from the *receiver*, not the sender. A sender that retries is doing the right thing. A receiver that cannot recognise a repeat is the defect. Every mechanism below is a way of making a repeated request cheap and safe rather than a way of preventing one.

## How it works

- **Idempotency key.** The caller generates a stable key per logical operation and sends it on every attempt. The receiver stores it and returns the *first* result on any repeat. On Salesforce, the natural store is a custom object with a **unique external ID** — the uniqueness constraint does the deduplication, and the `DUPLICATE_VALUE` error is the signal.
- **Upsert is idempotency you get for free.** `PATCH /sobjects/Account/Ext_Id__c/12345` run twice leaves one record → [04](04-rest-api-fundamentals.md).
- **Exponential backoff with jitter**, not a fixed interval. Fixed retries from many clients re-converge into the same spike that caused the failure.
- **Classify before retrying.** A `429`/`503` or a `REQUEST_LIMIT_EXCEEDED` is retryable; a `400`, a validation rule failure or `INVALID_FIELD` is not — retrying it burns the allowance and never succeeds → [24](24-api-limits-monitoring-and-access-control.md).
- **Replay IDs make an event consumer restartable**, and only if persisted **after** processing → [11](11-pub-sub-api.md).
- **A dead-letter path is mandatory.** Something must hold the message that failed *n* times, or a poison message blocks the stream forever — and with a 72-hour event retention, "blocked" becomes "lost".

## 2026 currency

Nothing here changed in Summer '26, which is precisely the point: this is the stable layer under everything that did. Two platform facts make it more relevant than it was. **Publishing is not transactional with DML** — a rollback does not recall a published event, so a consumer can legitimately receive an event for a record that never persisted → [12](12-platform-event-design.md). And an **agent** is now a caller: a retrying MCP client or an agent that re-invokes an action after a timeout produces duplicate writes in exactly the same way middleware does, against endpoints that were never reviewed for it → [25](25-mcp-servers-and-agent-facing-apis.md).

## Gotchas

- **Retrying a non-idempotent `POST` is how duplicate orders happen.** The first call succeeded; only the response was lost.
- **`allOrNone` defaults to false on composite.** The request returns HTTP 200 with failures buried in the body, and a client checking the status code reports success → [06](06-composite-batch-and-graph-apis.md).
- **`JobComplete` on a Bulk job means processing finished, not that records succeeded.** Read the failed-results file → [07](07-bulk-api-2.md).
- **A fault path in Flow does not roll back.** Error *reporting*, not error handling — records already written stay written → [04-flow · 10](../04-flow-and-automation/10-fault-paths-and-custom-errors.md).
- **Row lock contention looks like a random failure.** `UNABLE_TO_LOCK_ROW` is retryable, and the fix is usually serialising by parent rather than retrying harder → [07](07-bulk-api-2.md).
- **A dedupe table with no retention policy becomes the largest object in the org.** Give the key an expiry from the day it is created.
- **Silent success is the worst outcome.** An integration with no alert on its dead-letter path fails invisibly for months.

## Recall

Q: Why is a timeout different from a failure?
A: It tells you nothing about whether the work happened — which is why the receiver, not the sender, must make a repeat safe.

Q: What is the idiomatic Salesforce implementation of an idempotency key?
A: A unique external ID field; the uniqueness constraint deduplicates and `DUPLICATE_VALUE` is the signal. Upsert on an external ID is the built-in case.

Q: Which errors are worth retrying?
A: Transient ones — `429`, `503`, `REQUEST_LIMIT_EXCEEDED`, `UNABLE_TO_LOCK_ROW`. Validation and malformed-request errors never succeed on retry.

Q: When should a consumer persist a replay ID?
A: After processing, never on receipt.

Q: What happens to an event stream with no dead-letter path?
A: A poison message blocks it, and with 72-hour retention the backlog behind it is permanently lost.

## Related

- [24 · API limits, monitoring & access control](24-api-limits-monitoring-and-access-control.md) — the limit errors worth retrying, and where to see them
- [12 · Platform Event design](12-platform-event-design.md) — publish behaviour and delivery guarantees
- [11 · Pub/Sub API](11-pub-sub-api.md) — replay IDs and the 72-hour window
- [07 · Bulk API 2.0](07-bulk-api-2.md) — partial success at volume, and lock contention
