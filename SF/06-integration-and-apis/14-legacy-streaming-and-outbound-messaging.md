# Legacy streaming & outbound messaging

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The note that exists **to be the correction** — what in the older event stack is genuinely legacy, what is merely older, and what each piece migrates to. The current transport is [11](11-pub-sub-api.md).

> **What changed.** Less than the internet says, and the overstatement is the problem. **The Streaming API is not retired.** No end-of-life date is published for it, for **CometD** or for the **Bayeux** protocol underneath, and Salesforce's own wording is a recommendation: *"we recommend you use Pub/Sub API instead of Streaming API."* What carries the *(Legacy)* label in the documentation is narrower — **PushTopic events** and **generic events**. And `lightning/empApi`, the **supported** way an LWC subscribes to events, is CometD-based, which is the checkable proof that "CometD is dead" cannot be true.

## Core idea

Salesforce's event stack accumulated in layers, and each layer is at a different point on the same curve — *current*, *older but supported*, *labelled legacy*, *withdrawn*. Collapsing that into "the old streaming stuff is dead" produces two opposite failures: telling a client to fund an urgent migration that no deadline requires, and missing the pieces that genuinely are dead ends.

The honest summary is that **the transport is fine and two message types are dead ends.** CometD long-polling still works and still has a first-party consumer. PushTopic and generic events are where no new capability lands and where the documentation says so. Outbound messaging sits somewhere else again: fully supported, but reachable now mostly through a configuration surface that itself stopped accepting new work.

## How it works

| Piece | Status | Migrate to |
|---|---|---|
| **Streaming API / CometD / Bayeux** | supported; Pub/Sub recommended for new work | [11 · Pub/Sub API](11-pub-sub-api.md) |
| **PushTopic events** | **documented as (Legacy)** | [13 · Change Data Capture](13-change-data-capture.md) |
| **Generic events** | **documented as (Legacy)** | [12 · Platform events](12-platform-event-design.md) |
| **`lightning/empApi`** | **supported** — CometD-based, in-org LWC subscriber | nothing; it is current |
| **Outbound messaging** | supported, diminished reach | platform events, or an Apex callout |

- **A PushTopic is a SOQL query you subscribe to.** The idea was good and the constraints were tight — a restricted query grammar, no delete visibility, no bulk semantics — all of which CDC fixed by generating the stream from the platform instead. → [13](13-change-data-capture.md)
- **Generic events are a bare message bus** with no schema. Platform events replaced them with typed, deployable metadata. → [12](12-platform-event-design.md)
- **Outbound messaging is a declarative SOAP callout** with guaranteed retry and no code — genuinely useful, and its limitation was always that it sends a fixed message to a fixed endpoint.
- **Its practical reach narrowed for an indirect reason.** Outbound messages are configured as **workflow actions**, and new Workflow Rules cannot be created — so approval processes are the remaining path to configure one. → [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md)
- **Long-polling versus gRPC is the real technical gap**: no flow control, so a slow subscriber falls behind rather than applying backpressure. → [11](11-pub-sub-api.md)

## 2026 currency

**Nothing here acquired a retirement date in 2026.** The change worth recording is a correction to this vault's own framing: [../CURRENCY.md](../CURRENCY.md)'s six-defaults table lists CometD → Pub/Sub, and that row is **weaker than the others** — it is a recommendation, not a default flip and not a retirement. Treat it the way phase 06 had to treat Lightning Locker: the successor is where new work goes, the predecessor still runs. Where an existing CometD subscriber is stable and inside retention tolerances, *"migrate when you touch it"* is a defensible answer; where flow control or replay robustness matter, Pub/Sub is worth the gRPC adoption cost.

> **From my notes.** `CometD` (2025) is a working long-polling subscriber write-up and its mechanics are still correct. What it lacks is the framing this whole note exists to supply — it presents CometD as *the* way to subscribe. For a new external subscriber it is not; for `lightning/empApi` inside a component it still is.

## Gotchas

- **Do not tell a client "CometD is retired."** It is not, and the correction lands badly in the room. Say *recommended against for new external subscribers*.
- **PushTopic queries never see deletes**, which is the specific reason a PushTopic-based replication silently drifts.
- **Outbound messaging retries for 24 hours** and can deliver out of order — its guarantee is delivery, not sequence.
- **The outbound message payload is fixed at configuration time.** Adding a field means editing the message and re-consuming the WSDL downstream.
- **Generic events have no schema**, so every consumer parses by convention and breaks silently when the convention changes.
- **`empApi` is not a fallback for a failed Pub/Sub design** — it is an in-org component API and cannot serve an external system. → [03-lwc · INDEX](../03-lwc-and-slds/INDEX.md)

## Recall

Q: Is the Streaming API retired?
A: No. No end-of-life date is published for Streaming API, CometD or Bayeux. Pub/Sub is *recommended* for new work.

Q: Which pieces does Salesforce actually label *(Legacy)*?
A: PushTopic events and generic events.

Q: What is the checkable evidence that "CometD is dead" is false?
A: `lightning/empApi` — the supported in-org LWC subscriber — is CometD-based.

Q: What does a PushTopic migrate to, and what does a generic event migrate to?
A: PushTopic → Change Data Capture; generic event → platform events.

Q: Why did outbound messaging's reach narrow?
A: It is configured as a workflow action, and new Workflow Rules cannot be created — approval processes are the remaining configuration path.

## Related

- [11 · Pub/Sub API](11-pub-sub-api.md) — the recommended transport, and why flow control matters
- [13 · Change Data Capture](13-change-data-capture.md) — what PushTopic should have been
- [12 · Platform Event design](12-platform-event-design.md) — the typed replacement for generic events
- [../CURRENCY.md](../CURRENCY.md) — the six-defaults table, and why row 5 is the weakest of them
