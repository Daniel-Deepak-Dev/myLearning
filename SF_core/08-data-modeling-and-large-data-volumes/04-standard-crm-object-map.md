# Standard CRM Object Map

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** The standard object graph you inherit before writing anything — what connects to what, where the polymorphic joints are, and which chains surprise people. The B2C variant is [05](05-person-accounts-and-one-way-modeling-decisions.md).

## Core idea

The standard model is one connected graph with **Account at the centre**. Contacts hang off it, Opportunities hang off it, Cases hang off both, and Activities attach to nearly everything through a pair of polymorphic keys. Knowing this graph is not trivia: it tells you which relationships already exist (so you do not rebuild them), where reporting can already join (so you do not denormalize), and which objects are the high-volume ones in almost every org.

The graph also has two joints that behave unlike ordinary lookups — **polymorphic keys**, which can point at several different objects, and the **pricing chain**, which is longer than anyone expects. Both are where custom work goes wrong first.

## How it works

| Cluster | Objects | Note |
|---|---|---|
| Core | `Account` → `Contact`, `Opportunity`, `Case` | the graph everything else joins to |
| Pre-sale | `Lead` → converts to Account + Contact + optional Opportunity | `Campaign` / `CampaignMember` join Lead **and** Contact |
| Pricing | `Opportunity` → `OpportunityLineItem` → `PricebookEntry` → `Product2` + `Pricebook2` | four hops, not one |
| Post-sale | `Quote` → `QuoteLineItem`, `Order` → `OrderItem`, `Contract`, `Asset` | each with its own line-item child |
| Service | `Case` → `CaseComment`, `Entitlement`, `Solution`/Knowledge | `Case` is usually the volume leader |
| Activity | `Task`, `Event` | polymorphic; `ActivityHistory`/`OpenActivity` are read-only views |

- **`WhoId` and `WhatId` are the polymorphic joints.** `WhoId` points at a **Lead or Contact**; `WhatId` at an Account, Opportunity, Case, Campaign or custom object. Query them with `TYPEOF` → [10-soql · 04](../10-soql-and-sosl/04-relationship-queries-in-depth.md).
- **`OwnerId` is polymorphic too** — a User *or* a Queue, which is why owner-based logic needs a key-prefix check → [01-admin · 11](../01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md).
- **Lead conversion is a one-way transformation.** The Lead becomes read-only with `IsConverted = true`; it is not deleted, so converted Leads accumulate as real volume.
- **`AccountContactRelation`** is the junction enabling *Contacts to Multiple Accounts*. The Contact's own `AccountId` remains the **primary** account and does not go away.
- **`Activity` is not a queryable table.** It is a reporting abstraction over Task and Event.

## Gotchas

- **You cannot add a product to an Opportunity without an active price book entry.** The `Product2` → `PricebookEntry` → `Pricebook2` chain must be complete and active; "the product exists but won't add" is nearly always a missing or inactive `PricebookEntry`.
- **A Task cannot have a Lead `WhoId` and a `WhatId` at the same time.** Lead-related activities carry no `WhatId`.
- **Converted Leads are permanent volume.** Nothing purges them, and they still count against storage and query cost → [13](13-deletes-recycle-bin-and-physical-deletion.md).
- **`Task` and `Event` are among the largest objects in a mature org** and are frequent skew victims, because integrations log activity against a handful of records → [10](10-data-skew.md).
- **Polymorphic fields cannot be filtered selectively by type** without `TYPEOF` or a key-prefix filter, and a `WhatId` filter that spans object types will not use an index well.
- **Case has two paths to Account** — directly, and through Contact — and they can disagree. Reports built on the wrong one quietly under-count.
- **Standard objects have standard indexes you get for free**: `Id`, `Name`, `OwnerId`, `CreatedDate`, `LastModifiedDate`, `RecordTypeId` and all lookup fields → [08](08-indexes-and-query-selectivity.md).

## Recall

Q: What are the four hops between an Opportunity line and the product catalogue?
A: `Opportunity` → `OpportunityLineItem` → `PricebookEntry` → `Product2`, with `PricebookEntry` also pointing at `Pricebook2`.

Q: Which objects can `WhoId` and `WhatId` point at?
A: `WhoId` — Lead or Contact. `WhatId` — Account, Opportunity, Case, Campaign and custom objects. Query them with `TYPEOF`.

Q: What happens to a Lead after conversion?
A: It stays, marked `IsConverted = true` and read-only. It is never deleted, so converted Leads accumulate as real storage and query cost.

Q: Why is `OwnerId` awkward for automation?
A: It is polymorphic — a User or a Queue — so logic must check the key prefix before assuming a User.

Q: Can you query the `Activity` object?
A: No. `Activity` is a reporting abstraction; `Task` and `Event` are the real tables.

## Related

- [05 · Person Accounts & one-way modeling decisions](05-person-accounts-and-one-way-modeling-decisions.md) — what this graph becomes in B2C
- [02 · Relationships deep dive](02-relationships-deep-dive.md) — the consequences of each edge in this graph
- [10 · Data skew](10-data-skew.md) — why Task, Event and Case go lopsided first
- [02-apex · 04 Advanced SOQL, SOSL & dynamic queries](../02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md) — `TYPEOF` against the polymorphic joints
