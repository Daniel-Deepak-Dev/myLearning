# Event Relay & cloud eventing

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Forwarding Salesforce events into a cloud event bus without running a subscriber. What goes in the payload is [12](12-platform-event-design.md); the transport you would otherwise write a client for is [11](11-pub-sub-api.md).

## Core idea

Every event subscriber you run is infrastructure you own: a gRPC client, a replay store, a restart story, an on-call rotation. Event Relay removes it. You configure a relay in Setup, Salesforce pushes matching events into **Amazon EventBridge**, and from there they are ordinary AWS events — routable to Lambda, Step Functions, SQS, or anything EventBridge already reaches.

The architectural shift is where the integration lives. Instead of an external process reaching *into* Salesforce and holding a subscription, Salesforce pushes *out* into a bus the enterprise already governs. Nothing polls, nothing holds a connection, and there is no replay ID to persist.

## How it works

- **Two halves, both configured.** A **channel** in Salesforce selects which events to relay; a **relay** binds that channel to an EventBridge **partner event source** and is activated from Setup.
- **Platform events and Change Data Capture** are the supported event types → [12](12-platform-event-design.md), [13](13-change-data-capture.md).
- **The AWS side must accept it.** The partner event source appears in the target AWS account and region and has to be **associated with an event bus** before anything flows — until then events are dropped, not queued.
- **Relays have a lifecycle:** created, running, paused, error. A relay that errors stops; it does not silently degrade.
- **Bidirectional is possible** — events can be sent back to Salesforce from AWS — but that return path is an ordinary API caller, not part of the relay.
- **No subscriber code exists anywhere in this design.** That is the whole feature.

## 2026 currency

The thing to be precise about: **Event Relay targets Amazon EventBridge, and only Amazon EventBridge.** There is no Azure Event Grid or Google Pub/Sub equivalent — a multi-cloud estate reaches those through EventBridge or through a Pub/Sub API client of its own. "Cloud eventing" in this note's title describes the pattern, not a menu of destinations. The adjacent 2026 fact worth carrying over from phase 12 is that [Pub/Sub API is *recommended*, not a replacement](11-pub-sub-api.md) — so the real choice here is three-way: relay to AWS, write a Pub/Sub client, or subscribe in-org with `lightning/empApi`.

## Gotchas

- **The 72-hour retention still applies.** A relay in an error state past three days has permanently lost the events it did not forward → [11](11-pub-sub-api.md).
- **An unassociated partner event source silently discards.** The relay reports healthy on the Salesforce side while nothing arrives in AWS.
- **AWS account and region are fixed at configuration.** Moving the consuming workload to another region means a new relay and a new event source.
- **Events cross a trust boundary intact.** Whatever is in the payload leaves the org's sharing model entirely — which is why an event is a published contract, not a convenient notification → [12](12-platform-event-design.md).
- **No transformation on the way out.** Filtering and shaping happen in EventBridge rules, so the relay forwards whatever the channel selected.
- **Relay allocations are per org.** Check them before designing several fine-grained relays where one channel would do.

## Recall

Q: What destination does Event Relay support?
A: Amazon EventBridge, and only EventBridge. There is no Azure or Google equivalent.

Q: What does Event Relay remove from an event architecture?
A: The subscriber — no gRPC client, no replay store, no restart logic.

Q: What two things are configured, and what binds them?
A: A channel selecting the events, and a relay binding that channel to an EventBridge partner event source.

Q: What happens if the partner event source is never associated with an event bus?
A: Events are dropped. The Salesforce side still looks healthy.

Q: Which event types can be relayed?
A: Platform events and Change Data Capture events.

## Related

- [11 · Pub/Sub API](11-pub-sub-api.md) — the alternative where you do run the subscriber
- [12 · Platform Event design](12-platform-event-design.md) — the payload contract that leaves the org
- [13 · Change Data Capture](13-change-data-capture.md) — the other relayable source
- [23 · Idempotency, retries & error handling](23-idempotency-retries-and-error-handling.md) — at-least-once delivery does not stop at the org boundary
