# Salesforce Connect & external objects

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Reading and writing data that lives in another system as if it were an object, without copying it in. When to copy instead is [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md); the credentials are [17](17-named-credentials-and-external-credentials.md).

## Core idea

Salesforce Connect is a **virtual data layer**. An external object (`__x`) has fields, a tab, list views, reports, and can appear in a related list — but no rows are stored. Every query becomes a live callout to the source system, translated on the fly.

That single property decides every design conversation about it. There is no sync job, no storage cost and no staleness — and equally no offline access, no reliable performance and no participation in the parts of the platform that assume rows exist locally. The right question is never "external object or not"; it is **"how often is this read, and does anything need to act on it?"**

## How it works

| Adapter | Source | Notes |
|---|---|---|
| **OData 2.0 / 4.0 / 4.01** | any OData producer | the common case; 4.01 is the current version |
| **Cross-org** | another Salesforce org | **gained named credential support in Summer '26** |
| **Custom (Apex Connector Framework)** | anything with an API | you write `DataSource.Connection` and `DataSource.Provider` |

- **The external ID field is the join key.** Every external object gets an `ExternalId` and a `DisplayUrl`; relationships hang off it.
- **Two relationship types exist because record IDs do not.** An **external lookup** points from a Salesforce record to an external object using the external ID; an **indirect lookup** points from an external object back to a Salesforce record by matching a custom field marked *External ID* and *Unique*.
- **Authentication is a named credential**, per data source — including per-user OAuth, which is how a portal shows each user only their own external data.
- **Writes are supported where the source supports them.** OData 4.01 with a writable source gives create/update/delete from the standard UI.
- **Sync is the opposite feature.** *Files Connect* and external data sources can also be indexed for search; a copy is a different design → [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).

## 2026 currency

The design-changing news is that **Salesforce removed the per-hour limits on new external object rows and OData callouts** for the OData 2.0, 4.0 and 4.01 adapters — available for orgs **hosted on Hyperforce**, in Enterprise, Performance, Unlimited and Developer editions. Those hourly ceilings were the standard reason an architecture that "should" have used external objects used a replicated copy instead, so an assessment written before this is worth revisiting. Two things did not change: the **per-callout latency** of every single query, and the fact that a non-Hyperforce org still has the ceilings. Summer '26 also brought named credential support to the **cross-org adapter**, which removes the weakest link in org-to-org connections → [17](17-named-credentials-and-external-credentials.md).

## Gotchas

- **No triggers, no workflow, no roll-up summaries.** External objects do not fire automation, so anything that must *react* to the data needs a copy or an event.
- **The source system's outage is your page's outage.** A list view backed by an external object fails when the remote API does, inside the user's page load.
- **Filtering and sorting are only as good as the adapter.** An OData producer that does not support a `$filter` you wrote makes Salesforce fetch and discard, which reads as an unexplained slowdown.
- **Indirect lookups need the target field to be both *External ID* and *Unique*** — miss either and the relationship cannot be created, with an error that names neither.
- **External objects do not participate in the sharing model the way you expect.** Row-level access comes from the source system or from per-user authentication, not from sharing rules.
- **Limits removed on Hyperforce is not limits removed everywhere.** Check where the org actually runs before designing on it.

## Recall

Q: What is stored locally for an external object?
A: Nothing. Every query is a live callout; the object provides the schema, tab, reports and relationships.

Q: What is the difference between an external lookup and an indirect lookup?
A: External lookup points from a Salesforce record to an external object via its external ID; indirect lookup points from an external object back to a Salesforce record by matching a custom field marked External ID and Unique.

Q: Which Salesforce Connect limits were removed, and for whom?
A: The per-hour limits on new rows and OData callouts, for OData 2.0/4.0/4.01 adapters, on Hyperforce-hosted orgs in EE/PE/UE/DE.

Q: Why can't a record-triggered flow react to an external object?
A: External objects fire no automation — no triggers, no workflow, no roll-ups.

Q: What changed for the cross-org adapter in Summer '26?
A: It supports named credentials.

## Related

- [17 · Named Credentials & External Credentials](17-named-credentials-and-external-credentials.md) — how a data source authenticates
- [08-data · external objects vs replicated copies](../08-data-modeling-and-large-data-volumes/INDEX.md) — the copy-or-federate decision
- [01 · Integration patterns & selection](01-integration-patterns-and-selection.md) — where data virtualization sits among the patterns
- [21 · MuleSoft & API-led boundaries](21-mulesoft-and-api-led-boundaries.md) — when the source should be fronted rather than reached directly
