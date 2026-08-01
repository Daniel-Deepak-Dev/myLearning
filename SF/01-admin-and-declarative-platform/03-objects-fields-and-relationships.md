# Objects, Fields & Relationships

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** The schema primitives — objects, field types, and the relationship types that connect them. Deliberately shallow on query performance: selectivity, indexing and ownership skew are [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).

## Core idea

An object is a table, a field is a column, a record is a row — but the relationship types are where Salesforce stops behaving like a plain database. Choosing lookup versus master-detail is not a modelling preference; it decides record ownership, sharing inheritance, delete cascade, whether roll-up summaries are possible at all, and which SOQL paths exist. That choice is also close to permanent: converting between the two is constrained and sometimes impossible once data exists. Get relationships right first, because almost every later decision inherits from them.

## How it works

| | Lookup | Master-detail |
|---|---|---|
| Coupling | loose, optional by default | tight, always required |
| Child ownership | its own `OwnerId` | none — inherits the master's |
| Child sharing | its own sharing rules | inherited from master |
| Delete parent | configurable: clear field, or block | **cascade-deletes children** |
| Roll-up summaries | not available | available on the master |
| Reparenting | free | only if *Allow reparenting* is set |

- **Junction object** — two master-detail relationships on one object gives many-to-many. The **first** master-detail created is *primary*: it drives look-and-feel, ownership and the record's detail behaviour. Deleting either parent deletes the junction record.
- **Hierarchical** — a self-lookup that exists only on `User` (the `ManagerId` pattern).
- **External lookup / indirect lookup** — for external objects surfaced through Salesforce Connect; they join on an external ID rather than a Salesforce ID.
- **Structural limits:** 2 master-detail relationships per object, up to 3 custom detail levels deep, and 40 relationship fields per object.
- **Field API names** carry `__c` (and a `Namespace__` prefix once packaged). `__r` is the relationship name you traverse in SOQL and formulas.

## 2026 currency

Nothing structural has changed here — this is the stable core of the platform and 2019-era material on relationship semantics is still accurate. What *has* moved is where field visibility gets designed: page layouts no longer own that, Dynamic Forms do. See [05 · Dynamic Forms](INDEX.md), phase 02.

## Gotchas

- Converting master-detail → lookup requires deleting every roll-up summary on the master first, and the child then needs an owner.
- You cannot add a master-detail relationship to an object whose existing records would have no parent — populate a lookup first, then convert.
- Deleting a field is a **soft delete**: it sits recoverable for 15 days and still counts against the field allocation until purged.
- "Required" has three independent enforcement points — field-level, layout-level, and validation rule. Only field-level applies to API and Data Loader writes.
- `Unique` on a text field is **case-insensitive by default**; the case-sensitive variant is a separate setting and changes duplicate behaviour.
- Changing a field's data type can silently null the field on existing records and invalidates formulas that reference it.
- Cascade delete on master-detail **ignores sharing** — a user who cannot see the child can still trigger its deletion by deleting the master.
- Lookup filters are validated on UI save but bypassed by some API paths; do not treat them as data integrity.

## Recall

Q: Which relationship type allows roll-up summary fields, and why?
A: Master-detail only — the child has no independent existence or owner, so the platform can safely aggregate children onto the master.

Q: In a junction object with two master-details, what does the *primary* relationship control?
A: Look-and-feel, record ownership, and the detail record's behaviour. It is whichever master-detail was created first.

Q: How many master-detail relationships can one object have, and how deep can detail nesting go?
A: Two per object, up to three custom detail levels deep.

Q: What must be true before converting a master-detail relationship to a lookup?
A: Every roll-up summary field on the master must be deleted first, and the child needs its own owner.

Q: Does a page-layout "required" setting stop Data Loader inserting a blank value?
A: No. Only field-level required enforces on API and Data Loader writes.

## Related

- [04 · Record types & picklist architecture](04-record-types-and-picklist-architecture.md) — the other half of schema configuration
- [07 · Formula fields & roll-up summaries](07-formula-fields-and-roll-up-summaries.md) — what relationships let you compute
- [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) — selectivity, indexing, skew and large-volume consequences
