# Data Model Design Principles

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** How to decide what becomes an object, and why *standard first* is a cost argument rather than a style preference. The schema primitives are [01-admin · 03](../01-admin-and-declarative-platform/03-objects-fields-and-relationships.md); the consequences of each relationship type are [02](02-relationships-deep-dive.md).

## Core idea

Salesforce is not an empty database. It ships with a working CRM graph — Account, Contact, Opportunity, Case — and nearly everything Salesforce builds is written against that graph. A custom object does not merely cost you a table; it costs you the features that only ever look at the standard one: forecasting, Einstein scoring, lead conversion, the Activity timeline, most AppExchange packages, and every future release note.

The model is also pulled in two directions at once. Normalization says split the data; reporting says keep it joinable — and **Salesforce reports cannot join arbitrary objects**, only the paths a report type defines. So the target is not "as normalized as possible" but "as normalized as the reporting requirement tolerates". Deliberate denormalization is a design decision here, not a failure of nerve.

Third, and the reason this whole area exists: **schema decisions are close to permanent and volume is close to irreversible.** A relationship type chosen on day one constrains sharing, deletion and roll-ups forever ([02](02-relationships-deep-dive.md)), and ten million rows loaded into a badly shaped object cannot be un-loaded cheaply ([13](13-deletes-recycle-bin-and-physical-deletion.md)).

## How it works

**Standard → extend → build**, in that order, with the third step justified in writing.

| Question | If yes |
|---|---|
| Does a standard object already mean this? | Use it — rename the tab, not the model |
| Is this the same thing in a different state? | Record type or picklist, not a new object |
| Does it have its own lifecycle, owner and security? | Custom object |
| Is it configuration read by automation? | Custom metadata type → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) |
| Is it write-once, high-volume and never edited? | Big object → [14](14-big-objects-and-the-archive-tier.md) |

- **Record types are not a modelling tool for different things.** They vary picklist values, layouts and process on *one* concept. Two genuinely different concepts sharing an object become a permanent filter tax on every report, rule, sharing rule and query.
- **Model for the query you will run most.** Selectivity is decided by field shape and index availability ([08](08-indexes-and-query-selectivity.md)), not by the elegance of the table design.
- **Every lookup you add is a future skew risk.** Ask what the distribution looks like at ten million rows, not at a hundred → [10](10-data-skew.md).
- **Junction objects are the supported many-to-many.** A multi-select picklist is not a relationship and cannot be filtered selectively.
- **Name the growth rate, not the row count.** A review that knows an object gains 4M rows a year makes different decisions from one that is told "it's big".

## Gotchas

- **Renaming a standard object's label changes nothing that matters.** The API name, behaviour and licence implications are unchanged; `Account` is still `Account` to every integration and package.
- **Custom objects do not inherit the CRM feature set.** Forecasting, lead conversion, the Activity timeline and most Einstein features are wired to named standard objects and cannot be repointed.
- **"We'll normalize it later" is usually false at volume.** Splitting an object after 50M rows is a migration with downtime, not a refactor.
- **A field is not free.** It consumes an allocation, appears in every describe call, and enlarges page and API payloads → [06](06-storage-model-and-schema-limits.md).
- **Reports cannot join two unrelated objects.** If the requirement is "one report showing both", the relationship must exist in the model — discovering that after go-live forces denormalization under pressure.
- **Deleting a custom object is a soft delete for 15 days**, and its fields keep consuming their allocation until purged.
- **Some switches have no off ramp.** Person Accounts is the headline one → [05](05-person-accounts-and-one-way-modeling-decisions.md).

## Recall

Q: What is the real cost of choosing a custom object over a standard one?
A: The platform features wired only to the standard object — forecasting, Einstein scoring, lead conversion, the Activity timeline, most packages — none of which can be repointed.

Q: Why is a Salesforce data model less normalized than a textbook relational one?
A: Reports can only traverse relationships a report type defines and cannot join arbitrary objects, so joinability is a modelling constraint rather than a reporting detail.

Q: When is a record type the wrong answer?
A: When the two things are genuinely different concepts rather than one concept in different states — sharing an object then taxes every report, rule and query with a filter forever.

Q: What should a design review ask about an object's size?
A: Its growth rate, not its current row count. Growth rate is what decides indexing, skew and archiving strategy.

Q: Which kind of reference data does not belong in a custom object?
A: Configuration read by automation — that is a custom metadata type, which deploys with the code and consumes no record storage.

## Related

- [02 · Relationships deep dive](02-relationships-deep-dive.md) — the consequences that make schema choices permanent
- [04 · Standard CRM object map](04-standard-crm-object-map.md) — what the standard graph already gives you
- [06 · Storage model & schema limits](06-storage-model-and-schema-limits.md) — what a record and a field actually cost
- [01-admin · 03 Objects, fields & relationships](../01-admin-and-declarative-platform/03-objects-fields-and-relationships.md) — the primitives this note assumes
