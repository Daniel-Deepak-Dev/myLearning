# Platform Event design

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** What to put in an event and how it behaves once published — payload design, publish behaviour, delivery guarantees. The transport is [11](11-pub-sub-api.md); publishing and subscribing from Apex is [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md); Flow subscribers are [04-flow · 07](../04-flow-and-automation/07-platform-event-and-async-path-flows.md).

## Core idea

A platform event is a **message defined as metadata** — an `__e` object with fields, versioned and deployable like anything else. Publishing one decouples the publisher from every consumer: the publisher does not know who subscribes, how many there are, or whether any exist. That is the entire value, and also the entire risk, because nothing tells the publisher that a subscriber broke.

The design decisions are not about mechanics but about **contract**. An event is a published interface: once something subscribes, changing the payload is a breaking change with no compiler to catch it. Events therefore want to be **small, self-describing and about a business fact** — `OrderShipped__e`, not `AccountFieldsChanged__e`. When the requirement really is "tell me when this record changed", the answer is not a hand-written event at all; it is [13](13-change-data-capture.md).

## How it works

| Choice | Options | Consequence |
|---|---|---|
| **Publish behaviour** | *Publish After Commit* / *Publish Immediately* | after-commit is rolled back with the transaction; immediate is not |
| **Event type** | **high-volume — the only option** | standard-volume has been uncreatable since Spring '19 and is retiring → [27](27-event-bus-allocations-limits-and-monitoring.md) |
| **Subscriber** | Apex trigger, Flow, Pub/Sub client, `empApi`, Event Relay | each has its own retry and error story |

- ***Publish After Commit* is the one that behaves like you expect.** The event fires only if the transaction commits, so a rolled-back save publishes nothing. *Publish Immediately* fires regardless — useful for logging an attempt, dangerous for anything else.
- **Delivery is at-least-once, not exactly-once.** Consumers must be idempotent; a dedupe key in the payload is the standard answer. → [21](INDEX.md)
- **Retention is three days**, shared with the rest of the event bus. → [11](11-pub-sub-api.md)
- **Put an idempotency key and a timestamp in every event.** Neither is provided for you in a form you should depend on.
- **Carry the record ID plus what changed, not the whole record.** Subscribers that need more can query; a fat payload is a contract you cannot alter later.
- **Flow subscribers cannot be tuned.** Flow has no equivalent of Apex's `PlatformEventSubscriberConfig`, so a declarative subscriber takes the 2,000 default batch size — and cannot call subflows at all. → [04-flow · 07](../04-flow-and-automation/07-platform-event-and-async-path-flows.md)

## 2026 currency

Event *design* has been stable; the surrounding platform has not. **Apex subscriber triggers default to user mode at 67.0** like all other Apex, so a subscriber that quietly processed everything may now process a subset without erroring → [02-apex · 10](../02-apex-and-triggers/INDEX.md). **Flow's triggered types did not follow that flip** and still run in system context without sharing, which means the same subscriber logic is now *more permissive* in Flow than in Apex → [04-flow · 19](../04-flow-and-automation/19-flow-run-context-and-sharing.md). And events are increasingly an **agent** surface: an event is one of the cleanest ways to hand work to an autonomous consumer, with Event Relay carrying it off-platform → [20](INDEX.md), [AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md](../../AI_Data/02-salesforce-ai/11-agent-fabric-and-interop/notes.md).

> **From my notes.** The seed `Platform Event / Salesforce Events` page treats an event as a notification to fire and forget. Correct as far as it goes; what it omits is the part that costs money later — **an event is a published contract**, and its payload cannot be narrowed once anything subscribes.

## Gotchas

- **You cannot query past events.** There is no `SELECT … FROM MyEvent__e` over history; if it must be auditable, write a record too.
- **Nothing tells a publisher that a subscriber failed.** Silent divergence is the default failure mode, which is why subscriber-side monitoring is not optional. → [24](INDEX.md)
- **Adding a required field breaks existing subscribers.** Additive-and-optional is the only safe evolution.
- **A rollback does not recall a *Publish Immediately* event**, and neither does a composite `allOrNone` failure. → [06](06-composite-batch-and-graph-apis.md)
- **Event triggers are bulk by construction** — the subscriber receives a batch, never one event, and code written for one is the classic defect. → [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)
- **Publishing is not free, and the two meters have different windows.** Enterprise gets **250,000 publishes per hour** and a separate **25,000 deliveries per rolling 24 hours** — the latter shared with CDC and spent only by external subscribers. A per-field-change event on a busy object exhausts them. → [27](27-event-bus-allocations-limits-and-monitoring.md)

## Recall

Q: What is the difference between the two publish behaviours?
A: *Publish After Commit* fires only if the transaction commits; *Publish Immediately* fires regardless, and a rollback does not recall it.

Q: What delivery guarantee do platform events give?
A: At-least-once — so consumers must be idempotent.

Q: Why should an event carry a record ID and the change, not the whole record?
A: The payload is a published contract that cannot be narrowed once anything subscribes.

Q: What can't a Flow platform-event subscriber do?
A: Be tuned — there is no Flow equivalent of `PlatformEventSubscriberConfig`, so it takes the 2,000 default — and it cannot call subflows.

Q: How do you audit events after the fact?
A: You write a record as well. Past events are not queryable, and retention is three days.

## Related

- [11 · Pub/Sub API](11-pub-sub-api.md) — how external subscribers receive these
- [13 · Change Data Capture](13-change-data-capture.md) — when the requirement is "the record changed"
- [27 · Event bus allocations, limits & monitoring](27-event-bus-allocations-limits-and-monitoring.md) — what publishing costs, and the standard-volume retirement
- [02-apex · 18 Platform events & CDC in Apex](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) — publishing and subscribing in code
- [04-flow · 07 Platform event & async path flows](../04-flow-and-automation/07-platform-event-and-async-path-flows.md) — the declarative subscriber and its ceiling
