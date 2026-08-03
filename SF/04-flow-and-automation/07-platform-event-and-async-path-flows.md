# Platform Event & Async Path Flows

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The two declarative ways work leaves the triggering transaction — the **asynchronous path** on a record-triggered flow, and the **platform event-triggered flow**. The event *platform* itself is [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) and [06-integration](../06-integration-and-apis/INDEX.md).

## Core idea

Both of these exist to answer the same question — *how does a flow do something the save transaction will not allow?* — and they answer it differently enough that picking wrongly is expensive. An **async path** is a branch on an after-save record-triggered flow that runs in its own transaction once the original save has committed. It is the right answer for a callout, for a Mixed DML situation, and for anything slow enough that the user should not wait; it keeps the triggering record in `$Record` and stays conceptually part of the same automation. A **platform event-triggered flow** is not part of anything — it subscribes to an event bus and runs when a message arrives, decoupled from whoever published it. Reach for the first when you want the same automation, later. Reach for the second when publisher and subscriber should not know about each other at all.

## How it works

| | Async path | Platform event-triggered flow |
|---|---|---|
| GA | **Spring '22** | Summer '21 |
| Trigger | after-save flow, after commit | an event message on the bus |
| Running user | the user who saved the record | **Automated Process** |
| Batch | inherits the save | **2,000 messages**, not configurable in Flow |
| Rollback | independent — a failure does not undo the save | independent |

- **An async path runs in a separate transaction with a fresh limit budget**, which is half its value; the other half is that it may make callouts.
- **Async paths are also the declarative fix for Mixed DML** — setup and non-setup objects can be written in the two transactions separately. → [02-apex · 05](../02-apex-and-triggers/05-dml-database-methods-and-savepoints.md)
- **A platform event-triggered flow cannot call a subflow.** This is a hard restriction and it shapes how you factor the logic. → [08](08-subflows-and-modular-flow-design.md)
- **Flow gives you no batch-size control over events.** Apex triggers can set one through `PlatformEventSubscriberConfig`; Flow subscribers take the 2,000 default.
- **Undelivered events sit on the bus for 72 hours** and are then gone. A subscriber that was down for a long weekend has lost messages, not queued them.

## 2026 currency

Neither mechanism changed materially at 67.0, and the currency worth carrying is a comparison rather than a feature. **Summer '26 gave schedule-triggered flows a configurable batch size of 1–200** → [06](06-scheduled-and-autolaunched-flows.md), and platform event-triggered flows still have none — so the declarative subscriber remains the one place where you cannot tune throughput without dropping to Apex. The wider platform context also matters when choosing: **Pub/Sub API is Salesforce's recommendation for new external subscribers** — a recommendation, not a replacement, since **no end-of-life is published for Streaming API, CometD or Bayeux**. It does not change how a *flow* subscribes, but it does change what a new integration on the other end looks like. → [06-integration · 11](../06-integration-and-apis/11-pub-sub-api.md), [14](../06-integration-and-apis/14-legacy-streaming-and-outbound-messaging.md), [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **An async path failure does not roll back the save that triggered it.** The record is committed and the follow-up is simply gone — often with no user-visible sign. Put a fault path on it. → [10](10-fault-paths-and-custom-errors.md)
- **A platform event-triggered flow runs as Automated Process**, so record access, `$User` and every ownership assumption differ from the publisher's context.
- **A platform event-triggered flow cannot call a subflow**, which forces duplication when the same logic is needed elsewhere.
- **Events are fire-and-forget.** A publisher gets no confirmation that any subscriber ran, and there is no retry you control from Flow.
- **72 hours is the whole retention window.** After that an unprocessed message cannot be recovered.
- **Async paths run "after commit", not "immediately".** Under load the gap is observable, and building a UI that assumes the work is already done is a bug.
- **Async paths belong to after-save flows only.** A before-save flow cannot have one, which is another reason the *Optimize the Flow for* choice is hard to reverse. → [03](03-record-triggered-flows.md)

## Recall

Q: What are the two things an async path buys that the save transaction cannot give you?
A: A fresh governor-limit budget in a separate transaction, and the ability to make callouts. It also resolves Mixed DML.

Q: Which user runs a platform event-triggered flow?
A: The **Automated Process** user, not the publisher and not the record owner.

Q: What is the platform event batch size for a flow subscriber, and can you change it?
A: 2,000 messages, and no — Flow exposes no equivalent of Apex's `PlatformEventSubscriberConfig`.

Q: Name the restriction that most shapes how you factor a platform event-triggered flow.
A: It cannot call a subflow, so shared logic has to be duplicated or moved into an invocable action.

Q: How long do undelivered platform events survive on the bus?
A: 72 hours, after which they are unrecoverable.

## Related

- [03 · Record-triggered flows](03-record-triggered-flows.md) — where an async path is configured, and why only after-save flows have one
- [02-apex · 18 Platform events & CDC in Apex](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) — the coded subscriber, including the batch-size control Flow lacks
- [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md) — why an unhandled async path failure is invisible
