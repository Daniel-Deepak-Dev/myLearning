# Data 360-Triggered Flows & Data Actions

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** The seam between Data 360 and core Flow — what can start a flow from the data layer, and the three ways data leaves Data 360. The data platform itself lives in [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md); this note owns only the Flow side.

## Core idea

Data 360 holds data that is not in your org's database — ingested, federated, unified — and Flow is one of the exits. There are three distinct mechanisms and they are routinely conflated. A **Data Cloud-triggered flow** starts inside core Salesforce when a **data model object (DMO)** or **calculated insight object (CIO)** meets criteria, and from there it is an ordinary flow with ordinary elements. A **data action** does not involve Flow at all: it forwards a change event from Data 360 to a **data action target** — a platform event, a webhook, or Marketing Cloud Engagement. An **activation** pushes a segment or DMO out to a destination system. Choosing between them is a question of where the logic should live, and the honest default is: if the work is CRM work, trigger a flow; if the work leaves Salesforce, use a data action or an activation and let the receiver own it.

## How it works

| Mechanism | Starts | Ends |
|---|---|---|
| **Data Cloud-triggered flow** | DMO or CIO change matching criteria, within a **data space** | anywhere Flow can reach |
| **Data action** | DMO / CIO change | **platform event**, **webhook**, or Marketing Cloud Engagement |
| **Activation** | a segment or DMO | an activation target — ads, email, external systems |
| **Activation-triggered flow** | a Data 360 activation, as the flow's start node | anywhere Flow can reach |

- **A data space is part of the trigger definition**, not an afterthought — the same DMO in two data spaces is two different trigger sources. → [AI_Data/01-data-cloud/03](../../AI_Data/01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md)
- **A platform event data action is the bridge worth knowing**, because it converts a Data 360 change into something a platform event-triggered flow already knows how to consume. → [07](07-platform-event-and-async-path-flows.md)
- **A Data Cloud-triggered flow fires after the DMO change has committed**, so it has no before-save equivalent and no reliable prior-value semantics — do not expect `$Record__Prior` behaviour here.
- **DMO field API names are not CRM field API names.** A flow written against `Individual` in Data 360 does not read like one written against Contact.
- **Data 360 ships monthly**, not on the three seasonal releases, so this surface moves faster than the rest of this area. → [AI_Data/05-release-radar/data-360.md](../../AI_Data/05-release-radar/data-360.md)

## 2026 currency

The name moved first: **Data Cloud is Data 360** since Dreamforce 2025, and the Flow UI, the docs and every blog post are at different points in that rename — expect to see both. The substantive addition is **activation-triggered flows**, introduced in **January 2026**: a Data 360 activation becomes the flow's *start node*, so the fan-out to CRM records, API calls and MuleSoft connectors is orchestrated in Flow Builder rather than configured per activation target. That closes a real gap — activations previously ended at a target and any follow-up logic lived outside Salesforce. Treat the older "Data Cloud-triggered flow" material as still correct but no longer the only entry point. → [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md)

## Gotchas

- **Three mechanisms, one vocabulary.** *Data action*, *activation* and *Data Cloud-triggered flow* are different things; getting them mixed up in a design conversation is expensive.
- **The data space is part of the trigger.** Pointing a flow at the wrong one produces a flow that never fires and reports nothing.
- **There is no before-save.** The flow runs after the DMO change commits, so it cannot veto anything.
- **Prior values are unreliable on update triggers.** Do not port `$Record__Prior` habits from record-triggered flows. → [03](03-record-triggered-flows.md)
- **Latency is real and unspecified.** "Near real time" is not "immediately", and a UI built on the assumption will show stale state.
- **Data 360 documentation for this surface is thinner than the rest of Flow.** Verify behaviour in an org rather than from a blog.
- **The monthly release cadence means currency rots faster here** than anywhere else in area 04.
- **Data actions cost Data Services Credits at volume.** A chatty trigger on a high-throughput DMO is a billing decision. → [AI_Data/GLOSSARY.md](../../AI_Data/GLOSSARY.md)

## Recall

Q: What are the three ways data leaves Data 360, and which one involves Flow directly?
A: Data Cloud-triggered flows (Flow), data actions (to a platform event, webhook or Marketing Cloud target), and activations. Activation-triggered flows now bridge the third to Flow as well.

Q: What can trigger a Data Cloud-triggered flow?
A: A data model object (DMO) or calculated insight object (CIO) meeting criteria, within a specific data space.

Q: Which data action target lets existing Flow automation consume a Data 360 change with no new concepts?
A: A Salesforce platform event — a platform event-triggered flow then handles it normally.

Q: What arrived in January 2026 and what gap did it close?
A: Activation-triggered flows — a Data 360 activation as a flow start node, so post-activation logic lives in Flow Builder instead of outside Salesforce.

Q: Why is `$Record__Prior` thinking a trap here?
A: These flows run after the DMO change commits and prior-value semantics are not reliable.

## Related

- [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — DMOs, CIOs, data spaces and activations, where this half of the story is owned
- [07 · Platform event & async path flows](07-platform-event-and-async-path-flows.md) — the flow type a platform event data action lands in
- [23 · Flows as Agentforce actions](23-flows-as-agentforce-actions.md) — the other seam where Flow meets the AI stack
