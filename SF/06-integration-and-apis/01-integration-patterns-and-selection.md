# Integration patterns & selection

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The decision framework the other 24 topics hang off — which pattern a requirement is, and which API implements it. Every mechanism named here gets its own note; none is explained twice.

## Core idea

Integration questions arrive as products — *"can we use Pub/Sub?"* — and have to be answered as **patterns**. The pattern is fixed by three properties of the requirement: **who initiates**, **whether the caller waits**, and **how many records move**. Once those are settled the API choice is usually forced, and arguing about it is arguing about the requirement. The six patterns below are Salesforce's own vocabulary and have been stable for a decade; what changes release to release is which API is the *current* implementation of each, which is why this note is a map and not a tutorial.

The trap worth naming up front: **most integration defects are pattern errors, not API errors.** A synchronous callout inside a trigger is not a bad use of `Http` — it is fire-and-forget written as request-reply.

## How it works

| Pattern | Who initiates | Caller waits? | Implement with |
|---|---|---|---|
| **Request-reply** | Salesforce | yes | Apex `Http` callout → [02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md), Flow HTTP Callout → [04-flow · 12](../04-flow-and-automation/12-http-callout-and-external-services-in-flow.md), External Services → [17](INDEX.md) |
| **Fire-and-forget** | Salesforce | no | Platform Events [12](12-platform-event-design.md), Queueable/`@future` [02-apex · 13](../02-apex-and-triggers/13-queueable-apex-and-chaining.md), outbound messaging [14](14-legacy-streaming-and-outbound-messaging.md) |
| **Remote call-in** | external system | yes | REST [04](04-rest-api-fundamentals.md), SOAP [05](05-soap-api-and-where-it-persists.md), composite [06](06-composite-batch-and-graph-apis.md), Apex REST [16](INDEX.md) |
| **Batch data sync** | either, scheduled | no | Bulk API 2.0 [07](07-bulk-api-2.md) |
| **UI update on data change** | Salesforce | no | CDC [13](13-change-data-capture.md) and Pub/Sub [11](11-pub-sub-api.md); in-org, `lightning/empApi` |
| **Data virtualization** | external system | yes | Salesforce Connect / external objects [20](INDEX.md) |

- **Volume decides more than anything else.** Under a few thousand records, REST or composite; above that, Bulk 2.0. The middle is where designs go wrong, because REST *works* at 50,000 records right up until the day it times out.
- **"Real time" is two different requirements.** *Sub-second, caller blocked* is request-reply. *Eventually, within seconds, caller free* is an event — and it is what people usually mean.
- **Direction is not symmetric.** Salesforce calling out has governor limits ([02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)); external systems calling in have org API request limits. Different budgets, different failure modes.
- **The composability question comes before the API question.** If one logical operation spans several objects, [06](06-composite-batch-and-graph-apis.md) decides the transaction boundary — no other choice restores it later.

## 2026 currency

The pattern vocabulary has not moved; three implementations have. **Bulk API 2.0** is the default for batch ([07](07-bulk-api-2.md)). **Pub/Sub API** is the recommended transport for events in new work, though the Streaming API it supersedes is **not retired** ([11](11-pub-sub-api.md), [14](14-legacy-streaming-and-outbound-messaging.md)). And **Headless 360** adds a consumer the patterns were not written for: an autonomous agent, which turns "can an agent do this without a UI?" into a design question with a real answer → [23](INDEX.md).

> **From my notes.** *`SF - Integration Patterns and Practices`* (2026-02) is the most current page in the seed corpus and its pattern taxonomy matches the table above. Its one stale line is the middle row: it names **outbound messaging** as a first-choice fire-and-forget mechanism. It still works, but it is not where new work goes — see [14](14-legacy-streaming-and-outbound-messaging.md) for what changed and what did not.

## Gotchas

- **A trigger that calls out is a design smell, not a limit problem.** It needs `@future(callout=true)` or a Queueable to compile at all — that requirement is the platform telling you the pattern is wrong.
- **`allOrNone` is a pattern decision made at request time.** Choosing it in the client, after the design is fixed, is how partial writes reach production. → [06](06-composite-batch-and-graph-apis.md)
- **Polling is not an integration pattern.** It is the absence of one, and it burns API requests against the org's 24-hour limit for nothing. → [24](INDEX.md)
- **Data virtualization has no offline story and no reporting story.** External objects are not a cheaper way to avoid loading data. → [20](INDEX.md)
- **Middleware does not remove the pattern choice**, it relocates it. MuleSoft calling Salesforce still picks one of these six. → [19](INDEX.md)
- **The org's API request limit is per 24 hours, org-wide**, so one badly written integration degrades every other one. → [24](INDEX.md)

## Recall

Q: What three properties of a requirement fix the integration pattern?
A: Who initiates, whether the caller waits for a response, and how many records move.

Q: Which pattern is a synchronous callout inside a trigger usually a broken version of?
A: Fire-and-forget — written as request-reply. The `@future(callout=true)` requirement is the platform signalling it.

Q: What implements batch data synchronization at 2026?
A: Bulk API 2.0. v1 still exists but is legacy.

Q: What does "real time" resolve to, and why is the distinction load-bearing?
A: Either request-reply (sub-second, caller blocked) or an event (eventually, caller free). People usually mean the second, which is a completely different design.

Q: Which pattern choice can no later decision recover?
A: The transaction boundary — whether a multi-object operation rolls back together. That is set by the composite choice at design time.

## Related

- [02 · API versions & the retirement treadmill](02-api-versions-and-the-retirement-treadmill.md) — the clock running under every choice on this page
- [03 · API endpoints, hostnames & Edge Network](03-api-endpoints-hostnames-and-edge-network.md) — where to point the client once the API is chosen
- [11 · Pub/Sub API](11-pub-sub-api.md) — the event transport for new work
- [02-apex · 19 Callouts & named credentials](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) — the outbound half, in code
