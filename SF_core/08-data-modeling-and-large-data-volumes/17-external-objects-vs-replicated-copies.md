# External Objects vs Replicated Copies

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** The copy-or-federate decision and what each side costs you. The Salesforce Connect *mechanism* is [06-integration · 20](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md); the zero-copy third option is [18](18-zero-copy-and-data-360-as-data-tier.md).

> **What changed.** The standard reason to replicate rather than federate was Salesforce Connect's **per-hour ceilings on new external object rows and OData callouts**. Those were **removed for the OData 2.0/4.0/4.01 adapters on Hyperforce** (EE/PE/UE/DE). Any copy-or-federate assessment written before that was decided on a limit that no longer exists — though a **non-Hyperforce org still has the ceilings**.

## Core idea

There are only three things you can do with data that lives somewhere else: **copy it in**, **read it in place**, or **query it where it lies**. The instinct is to compare them on freshness and storage, which is the least interesting axis. The decision is actually made by two questions: **how often is this read**, and **does anything on the platform need to act on it?**

Automation is the one that settles most arguments. An external object fires no triggers, no flows and no roll-ups, and does not participate in sharing the way a real row does. The moment a requirement says *"when this changes, do something"*, federation is out — not because it is slow, but because there is nothing to hook.

## How it works

| | Replicated copy | External object | Zero-copy federation |
|---|---|---|---|
| Where rows live | your org | source system | the lake |
| Freshness | as good as the sync | always current | always current |
| Storage cost | full | none | none |
| Automation, roll-ups, sharing rules | yes | **no** | no |
| Reports | full | limited | analytics-side |
| Fails when source is down | no | **yes, inside the page load** | yes |
| Latency | none at read | per query | per query |

- **The join key is an external ID, not a record Id.** An *external lookup* points out from a Salesforce record; an *indirect lookup* points back in by matching a field marked **External ID and Unique** → [03](03-record-ids-external-ids-and-upsert.md).
- **A copy has an ongoing cost nobody budgets** — the sync job, its failures, its backfill, and the storage → [06](06-storage-model-and-schema-limits.md).
- **Read frequency decides the economics.** Data read once a quarter should never be copied; data on every account page probably should be.
- **A partial copy is often the right answer** — replicate the five fields you filter and report on, federate the rest.
- **Change Data Capture is the copy's transport** when the flow is outbound → [06-integration · 13](../06-integration-and-apis/13-change-data-capture.md).

## 2026 currency

Beyond the ceiling removal above, the shape of the decision changed: it is no longer two options. **Zero-copy federation in Data 360 is GA**, which gives you a third answer that is neither a copy nor an external object, and it is usually the right one when the requirement is analysis rather than transaction → [18](18-zero-copy-and-data-360-as-data-tier.md). In the other direction, the classic org-to-org copy mechanism is going away: **Salesforce-to-Salesforce stops functioning in Spring '27** → [26](26-cross-org-data-sharing-and-consolidation.md). Summer '26 also gave the **cross-org adapter named credential support**, which makes federating between two Salesforce orgs materially less unpleasant than it was.

## Gotchas

- **"No storage cost" is not "no cost".** You pay per query, in latency, on the user's page.
- **The source system's outage becomes your list view's outage** — and it surfaces as a Salesforce bug report.
- **Filtering is only as good as the adapter.** An unsupported `$filter` makes Salesforce fetch and discard, which reads as an unexplained slowdown.
- **Indirect lookups need the target field marked both External ID and Unique.** Miss either and the error names neither.
- **External objects cannot be the parent of a master-detail** and cannot carry roll-up summaries — any KPI over federated data has to be computed elsewhere.
- **A replicated copy inherits every LDV problem in this area** — selectivity, skew, locking — and the source system's data quality on top → [19](19-data-quality-deduplication-and-mdm.md).
- **Limits removed on Hyperforce is not limits removed everywhere.** Check where the org actually runs → [23](23-hyperforce-residency-and-data-locality.md).

## Recall

Q: Which single requirement rules out an external object fastest?
A: Anything that must *react* to the data — external objects fire no triggers, flows or roll-ups.

Q: Which Salesforce Connect limits were removed, and for which orgs?
A: The per-hour ceilings on new external object rows and OData callouts, for the OData 2.0/4.0/4.01 adapters on Hyperforce-hosted EE/PE/UE/DE orgs.

Q: What is the difference between an external lookup and an indirect lookup?
A: External lookup points from a Salesforce record out to an external object via its external ID; indirect lookup points from an external object back in by matching a field marked External ID and Unique.

Q: When is a partial copy the right design?
A: When you need to filter, report or automate on a few fields but only display the rest — replicate those fields, federate the remainder.

Q: What is the third option beyond copying and external objects?
A: Zero-copy federation in Data 360 — the data stays in the lake and is queried there, which suits analysis rather than transactions.

## Related

- [18 · Zero-copy & Data 360 as data tier](18-zero-copy-and-data-360-as-data-tier.md) — the 2026 answer to the same question
- [26 · Cross-org data sharing & consolidation](26-cross-org-data-sharing-and-consolidation.md) — the same decision between two Salesforce orgs
- [06-integration · 20 Salesforce Connect & external objects](../06-integration-and-apis/20-salesforce-connect-and-external-objects.md) — adapters, relationships and authentication
- [06-integration · 13 Change Data Capture](../06-integration-and-apis/13-change-data-capture.md) — how a copy stays current
