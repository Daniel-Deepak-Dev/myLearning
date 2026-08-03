# Pub/Sub API

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The gRPC event transport — publishing and subscribing from outside the org, with replay and flow control. What to put *in* an event is [12](12-platform-event-design.md); the older transport it supersedes is [14](14-legacy-streaming-and-outbound-messaging.md).

> **What changed.** The 2019–2022 answer was CometD long-polling over HTTP. **Pub/Sub API is the recommended transport for new external subscribers** — gRPC over HTTP/2, binary Avro payloads, and explicit flow control instead of an implicit firehose. **It has not retired anything.** Salesforce's own words are *"we recommend you use Pub/Sub API instead of Streaming API"* — a recommendation, not a replacement, and **no retirement date is published for Streaming API, CometD or Bayeux.** Saying "CometD is dead" is wrong and checkable: `lightning/empApi`, the supported in-org subscriber, runs on it. → [14](14-legacy-streaming-and-outbound-messaging.md)

## Core idea

The old model pushed events at a subscriber as fast as they occurred and left it to cope. That is fine until the subscriber is slower than the publisher, at which point it falls behind, drops its connection and loses its place. **Pub/Sub inverts the control:** it is a *pull* model. The subscriber declares how many events it can handle right now, and the server sends no more than that. Backpressure becomes a first-class part of the protocol instead of a client-side problem.

The second change is efficiency. Events are **Apache Avro** binary, not JSON, with the schema fetched separately and cached — smaller on the wire, and strongly typed. And because it is one gRPC service, **publish and subscribe live in the same API**, which the older split never offered.

## How it works

| RPC | Purpose |
|---|---|
| `Subscribe` | pull subscription; client sends `FetchRequest` with `num_requested` |
| `ManagedSubscribe` | as above, but **Salesforce keeps the replay state** |
| `Publish` / `PublishStream` | publish events, unary or streaming |
| `GetSchema` | fetch the Avro schema for a topic, by schema ID |
| `GetTopic` | topic metadata and permissions |

- **Flow control is per subscription.** `num_requested` is the client's capacity for this fetch; the server never exceeds it, and the client asks again when it has room.
- **Every event carries a `ReplayId`** — an opaque marker of its position in the stream. Store the last one processed and resubscribe from it after a failure, and no events are lost.
- **Managed subscriptions remove the replay store.** Salesforce tracks the position server-side, so a client no longer needs durable storage just to be restartable. Check its release status before designing on it.
- **Retention is three days.** The event bus holds events for **72 hours**; a subscriber down longer than that has permanently missed them.
- **The schema is fetched by ID and cached.** Payloads carry a schema ID, not the schema — which is what keeps messages small and what breaks naive clients that never call `GetSchema`.
- **gRPC means real client libraries and a proto file**, not a REST call — a genuine adoption cost worth naming in a design review.

## 2026 currency

Pub/Sub is where new event capability lands, and it is the right default for a new external subscriber. What it is **not** is a forced migration: Streaming API remains supported, and the pieces Salesforce actually labels *(Legacy)* are narrower than the headline suggests — **PushTopic events** and **generic events** — with **Change Data Capture** ([13](13-change-data-capture.md)) as the recommended answer to the first and **platform events** ([12](12-platform-event-design.md)) to the second. The distinction is recorded in [../CURRENCY.md](../CURRENCY.md), whose six-defaults table carries the same carve-out. For hybrid architectures, **Event Relay** forwards events to AWS EventBridge without a subscriber of your own → [20](INDEX.md).

## Gotchas

- **Three days is the whole safety net.** A subscriber offline over a long weekend loses events with no recovery path — replay IDs do not help past the retention window.
- **Replay IDs are opaque and not sequential.** Treat them as bookmarks; arithmetic on them is meaningless.
- **Persist the replay ID *after* processing, not on receipt**, or a crash mid-processing skips an event permanently.
- **A schema changes when the event definition changes.** A client that cached one schema ID forever will fail to deserialize after an admin adds a field.
- **`num_requested` too high recreates the old problem.** Requesting a large batch to "go faster" reintroduces the overwhelm that flow control exists to prevent.
- **Publishing is not transactional with your DML.** A rollback does not recall a published event. → [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

## Recall

Q: Did Pub/Sub API retire CometD?
A: No. It is *recommended* for new work; Streaming API has no published retirement date, and `lightning/empApi` still runs on CometD.

Q: What makes Pub/Sub a pull model, and why does it matter?
A: The subscriber sets `num_requested` per fetch, so the server never sends more than it can handle. Backpressure is part of the protocol.

Q: How long does the event bus retain events?
A: Three days — 72 hours.

Q: What do managed subscriptions remove?
A: The client-side replay store — Salesforce tracks the replay position server-side.

Q: When should a replay ID be persisted?
A: After the event is processed. Persisting on receipt loses events across a crash.

## Related

- [14 · Legacy streaming & outbound messaging](14-legacy-streaming-and-outbound-messaging.md) — what is actually legacy, and what is not
- [12 · Platform Event design](12-platform-event-design.md) — what belongs in the payload
- [13 · Change Data Capture](13-change-data-capture.md) — the record-change stream on the same transport
- [02-apex · 18 Platform events & CDC in Apex](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) — the in-org half
