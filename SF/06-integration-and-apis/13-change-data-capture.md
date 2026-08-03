# Change Data Capture

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The platform-generated stream of record changes — channels, what a change message contains, and using it to keep an external store in sync. The transport is [11](11-pub-sub-api.md); the Apex side is [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md).

## Core idea

CDC is what you want when the requirement is *"keep that system in step with Salesforce"* and you were about to build it yourself. Enable it on an object and Salesforce publishes a change event for every create, update, delete and undelete — including changes made by other integrations, by Bulk loads, by admins in Setup and by automation. That last part is why hand-rolled alternatives fail: a trigger-published custom event captures the paths you thought of, and CDC captures the ones you did not.

It is delivered on the same event bus as platform events, with the same replay and retention model, so everything in [11](11-pub-sub-api.md) applies unchanged. The difference is authorship: **you design a platform event; the platform designs a change event.** You choose which objects and which fields, not the message shape.

## How it works

| Concept | Detail |
|---|---|
| **Standard channel** | `/data/ChangeEvents` — every enabled object |
| **Per-object channel** | `/data/AccountChangeEvent`, `/data/MyObject__ChangeEvent` |
| **Custom channel** | a chosen set of objects, so a subscriber gets only what it needs |
| **Enablement** | Setup → Change Data Capture, per object, with an entitlement cap |

- **The payload carries the *changed fields only*, plus a header.** The `ChangeEventHeader` holds `changeType`, `changedFields`, `recordIds`, `commitTimestamp`, `commitNumber` and `commitUser` — that header is where most of the useful information lives.
- **One message can cover many records.** `recordIds` is a list, because a bulk update commits together — so subscribers are bulk by construction.
- **`commitNumber` and `commitTimestamp` are how you order things.** Arrival order is not guaranteed to be commit order.
- **Enrichment fields** add selected fields to *every* message even when unchanged, which is how a downstream system gets a stable external ID it can match on without a callback query.
- **Deletes and undeletes are included**, which is precisely what a replication target needs and what a `LastModifiedDate` poll can never see.
- **Field-level security applies to the subscribing user**, so a change event can arrive with fields omitted. → [07-security · 13](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md)

## 2026 currency

CDC is the recommended replacement for **PushTopic events**, which are the piece Salesforce actually labels *(Legacy)* → [14](14-legacy-streaming-and-outbound-messaging.md). On transport, new external subscribers should use **Pub/Sub API**, while `lightning/empApi` remains the supported in-org subscriber and remains CometD-based — the two facts coexist and neither is a retirement → [11](11-pub-sub-api.md). Where the destination is a data platform rather than an application, compare CDC against **zero-copy Data 360** before building a replication pipeline at all: the cheapest sync is often the one you do not run → [08-data · 18](../08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md).

> **From my notes.** `Change data capture` and `lightning/empApi - Change Data Capture` (2023) are both still structurally correct — channel names, header shape and the `empApi` subscribe/unsubscribe pattern are unchanged. One thing to add rather than correct: they present `empApi` as *the* way to subscribe. It is the way to subscribe **inside a Lightning component**; an external system should be on Pub/Sub.

## Gotchas

- **CDC is not an audit trail.** Three-day retention, and it captures the change, not the reason. Field History and Field Audit Trail are the audit answer. → [07-security · 22](../07-security-and-sharing/22-field-audit-trail-and-data-retention.md)
- **`changedFields` is empty on create and delete** — everything is "changed" on insert and nothing is on delete. Branch on `changeType` first.
- **Enabling CDC on a busy object is a volume decision.** Every automated update publishes, including your own integrations' writes — which is how a sync loop starts.
- **Gap events exist.** When the platform cannot deliver the detail it publishes a gap event; a subscriber that ignores them will silently diverge.
- **Your own writes come back to you.** Filter on `commitUser` or a marker field, or a two-way sync will oscillate.
- **Enablement is capped by entitlement**, so "enable it on everything" is usually not available and should not be the design anyway.

## Recall

Q: Why is CDC more reliable than a trigger-published custom event for replication?
A: It captures every change path — other integrations, Bulk loads, Setup edits, automation — not only the ones you anticipated.

Q: What lives in the `ChangeEventHeader`?
A: `changeType`, `changedFields`, `recordIds`, `commitTimestamp`, `commitNumber` and `commitUser`.

Q: How do you order change events correctly?
A: By `commitNumber` / `commitTimestamp` — arrival order is not guaranteed to be commit order.

Q: What are enrichment fields for?
A: Including chosen fields in every message even when unchanged, so a downstream system always has a key to match on.

Q: Why is CDC not an audit trail?
A: Three-day retention, and it records the change rather than the reason. Field Audit Trail is the audit mechanism.

## Related

- [11 · Pub/Sub API](11-pub-sub-api.md) — the transport, replay and retention model
- [12 · Platform Event design](12-platform-event-design.md) — when you author the message instead
- [14 · Legacy streaming & outbound messaging](14-legacy-streaming-and-outbound-messaging.md) — PushTopic, which this replaces
- [02-apex · 18 Platform events & CDC in Apex](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) — subscribing in code
