---
vault: SF_core
area: 06-integration-and-apis
format: dense
status: learning
created: 2026-08-04
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 20
tags: [currency-new, currency-warning]
---
# Event bus allocations, limits & monitoring

**Scope:** What the event bus costs and how to see what it is doing — publish and delivery allocations, the CDC entity cap, and the two monitoring surfaces. Event *design* is [12](12-platform-event-design.md), CDC semantics are [13](13-change-data-capture.md), the transport is [11](11-pub-sub-api.md).

> **What changed.** Treating standard-volume and high-volume platform events as two live choices is wrong. **Standard-volume events have been unavailable to create since Spring '19** — the only ones in existence were defined before it — they receive **no support and no bug fixes**, and Salesforce has announced their **retirement** (Help **002280033**), with a migration tool to high-volume by Summer '26. High-volume is not the modern default; it is the only option. **The retirement date is Summer '27.** The 68.0 Platform Events Developer Guide, updated 9 October 2026 after the Winter '27 rollout, says *"Standard-volume custom platform events will be retired in Summer '27"*. Help 002280033 and an August 2026 Salesforce Japan notice read Winter '27, and nothing was retired at that upgrade.

## Core idea

The event bus meters two different things and most designs only budget for one. **Publishing** is capped per hour. **Delivery** is capped per 24-hour rolling window — and delivery counts only messages that leave the platform: Pub/Sub API and CometD clients, `empApi` Lightning components, and event relays. **Apex triggers, flows and Process Builder subscribers consume no delivery allocation at all.** So an in-org subscriber is effectively free on this meter, and one external client can exhaust an org's daily budget on its own.

The second thing worth internalising is that **high-volume platform events and Change Data Capture share the same delivery pool.** Enabling CDC on a busy object does not draw from a separate CDC budget; it spends the same allocation the integrations are already using.

## How it works

| Allocation | Enterprise | Unlimited / Performance | Developer |
|---|---|---|---|
| **Publish**, per hour | 250,000 | 250,000 | 50,000 |
| **Delivery**, per 24 h rolling | 25,000 | 50,000 | 10,000 |
| Concurrent CometD clients | 1,000 | 2,000 | 20 |

- **Delivery is shared** between high-volume platform events and change events. Professional Edition with the API add-on matches Enterprise on both meters.
- **A change event message and a platform event message both cap at 1 MB**, and the bus retains everything for **72 hours**. → [11](11-pub-sub-api.md)
- **CDC is capped at 5 entities** selected for change notifications across all channels, by default, in Enterprise, Performance and Developer. **Custom channels cap at 100.**
- **The add-on licence changes the shape, not just the size.** It adds **100,000 deliveries per day (3 million a month)** and **25,000 publishes per hour**, removes the 5-entity CDC cap entirely, and moves the org onto a **monthly usage-based entitlement with a grace allocation** for spikes.
- **Two monitors, covering disjoint halves.** `PlatformEventUsageMetric` (API 50.0+) counts volume; `EventBusSubscriber` shows subscriber health. Neither sees what the other sees.

## 2026 currency

**Parallel subscriptions for Apex triggers are GA at 67.0** — the first real answer to a subscriber that cannot keep up. A trigger is spread across **up to 10 internal partitions** via `PlatformEventSubscriberConfig`, keyed on a required custom field or the standard `EventUuid`. The trade is explicit and permanent: **ordering holds within a partition and not across them.** It applies to **custom high-volume platform events only** — not standard events, not change events, which is another reason the standard-volume position above is not a live choice. → [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

## Gotchas

- **`EventBusSubscriber` does not see external subscribers.** It represents triggers, flows and processes only — CometD and Pub/Sub API clients are absent from it. The subscriber you are most worried about is the one it cannot show you.
- **`PlatformEventUsageMetric` is the inverse**: it counts deliveries to exactly those external clients and relays, and ignores the in-org subscribers entirely. Query `PLATFORM_EVENTS_PUBLISHED`, `PLATFORM_EVENTS_DELIVERED`, `CHANGE_EVENTS_PUBLISHED`, `CHANGE_EVENTS_DELIVERED` with `StartDate`/`EndDate`; data is kept **at least 45 days** and updated **hourly**.
- **Hourly updates mean you find out after the fact.** There is no live counter, so a runaway publisher is diagnosed retrospectively.
- **Enabling CDC on a sixth object is not a decision you can make alone** — the 5-entity cap is contractual, not a setting to raise.
- **A `Retries` count climbing on `EventBusSubscriber` is the only early sign of a failing subscriber** before it hits ten runs and stops entirely. Nothing pushes that at you. → [02-apex · 18](../02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)
- **The publish meter is hourly and the delivery meter is daily.** Quoting one figure without its window is how "we get 250,000 events" becomes a capacity plan that fails at 3 a.m.
- **Enhanced Usage Metrics (API 58.0+) is opt-in** and is what gives per-event-name, per-client and 15-minute breakdowns. Without it you have org-level totals and no way to attribute a spike.

## Recall

Q: Which subscribers consume the event delivery allocation?
A: Pub/Sub API and CometD clients, `empApi` components and event relays. Apex triggers, flows and Process Builder consume none of it.

Q: Do platform events and Change Data Capture have separate delivery budgets?
A: No — high-volume platform events and change events share one delivery pool.

Q: What are the Enterprise publish and delivery allocations, with their windows?
A: 250,000 publishes **per hour** and 25,000 deliveries **per rolling 24 hours**.

Q: How many objects can CDC be enabled on by default, and how do you raise it?
A: Five entities across all channels. Only the add-on licence removes the cap.

Q: Why do you need both `PlatformEventUsageMetric` and `EventBusSubscriber`?
A: They cover disjoint halves — the first counts external deliveries and publishes, the second shows in-org trigger/flow subscriber health including `Retries` and `LastError`.

## Related

- [12 · Platform Event design](12-platform-event-design.md) — the payload decisions these allocations price
- [13 · Change Data Capture](13-change-data-capture.md) — the 5-entity cap in the context of choosing objects
- [11 · Pub/Sub API](11-pub-sub-api.md) — the transport whose clients spend the delivery allocation
- [24 · API limits, monitoring & access control](24-api-limits-monitoring-and-access-control.md) — the wider request budget this sits beside
- [02-apex · 26 Testing platform events & CDC](../02-apex-and-triggers/26-testing-platform-events-and-cdc.md) — proving the subscriber works before it reaches these meters

## Sources

- [Platform Events Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/platform_events.pdf) — Salesforce Developers · read 2026-10-28 · *"Standard-volume custom platform events will be retired in Summer '27"* (twice); publish 250,000/50,000 per hour and delivery 50,000/25,000/10,000 per 24 h unchanged; last updated 9 October 2026
- [(2026年8月) Salesforceの運用に関する重要なお知らせ](https://successjp.salesforce.com/article/NAI-001321) — Salesforce Japan Success Navi, 24 Aug 2026 · read 2026-10-28 · said *"Winter '27 リリースをもって廃止される予定"* (retirement with Winter '27) — superseded by the 68.0 guide

## History

- 2026-10-28 · Winter '27 currency check: settled the standard-volume retirement date as Summer '27 from the 68.0 guide; allocations re-checked, unchanged
