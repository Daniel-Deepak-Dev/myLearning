# Data Quality, Deduplication & MDM

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Quality as an architectural property — matching strategy, merge consequences, and where mastery lives when there is more than one system. The *mechanics* of matching and duplicate rules are [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md).

## Core idea

Deduplication looks like a matching problem and is actually a **merge** problem. Deciding that two rows are the same person is the easy half and the half every tool sells; deciding **which value wins, what happens to the children, and what you lose** is the half that goes wrong, and it is irreversible.

Above that sits the question the org cannot answer for itself: **which system is master?** Salesforce is frequently the place a record is *seen* and rarely the place it is *born*. Writing that down — per object, per field — is the whole of MDM as it applies here. Without it, every integration is entitled to overwrite every field, and quality decays to whatever the noisiest source says.

## How it works

- **Matching is deterministic or fuzzy, and the choice is a policy.** Exact matching under-catches; fuzzy matching over-catches and merges two real people. Tune against a labelled sample, not intuition.
- **A merge is a delete.** The losing records are deleted (recoverable from the Recycle Bin for a time), their children are reparented onto the winner, and the surviving field values are chosen at merge time. Field history and anything keyed on the losing Id do not survive intact.
- **Survivorship needs stating before the merge**, not during: most-recently-updated, most-complete, source-of-record precedence, or per-field rules. "The user picks" is a survivorship rule too — just an unauditable one.
- **Duplicate rules only guard the save path.** Existing duplicates need a scan — Duplicate Jobs, which are edition-gated, or your own report/batch → [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md).
- **Prevention beats detection.** A unique **External ID** on the record's true business key stops the duplicate ever being created, and makes every load an upsert → [03](03-record-ids-external-ids-and-upsert.md).
- **The four MDM styles still apply**: registry (index only), consolidation (a reporting golden copy), coexistence (each system masters some fields), centralized (one system masters everything). Coexistence is what most Salesforce estates actually run, usually without admitting it.
- **Data 360 solves a different problem with similar words.** Identity resolution builds a **unified profile** across sources with match and reconciliation rules — it does not merge or delete the CRM rows → [AI_Data](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md).

## 2026 currency

The meaningful shift is that quality stopped being only a reporting concern. An agent grounded on the org answers from whatever it finds, so a duplicate Account is no longer a tidiness problem — it is a wrong answer delivered confidently to a customer. Data 360's identity resolution is the tier where that gets reconciled without destroying CRM rows, which makes "unify for grounding, merge only where the business truly has one record" a defensible split. Nothing structural changed in matching or duplicate rules themselves.

## Gotchas

- **Merging is irreversible in practice.** Undelete restores the losing row, not the children you reparented or the values you discarded.
- **Duplicate rules do not run on every path.** Lead conversion and some bulk operations bypass them, so they are not a guarantee.
- **Matching rule activation is asynchronous.** Testing straight after activating gives a false negative.
- **Fuzzy matching at scale is a selectivity problem too** — a dedup scan over 20M rows is an LDV job → [08](08-indexes-and-query-selectivity.md).
- **Person Accounts double the surface**, because one person is two records by design → [05](05-person-accounts-and-one-way-modeling-decisions.md).
- **An integration with no field-level mastery rule will win every conflict**, silently, at whatever cadence it runs.
- **Quality has to be measured to be managed** — completeness, validity, uniqueness and staleness per critical field, trended. An unmeasured "data quality initiative" is a one-off cleanup with a budget.

## Recall

Q: Why is deduplication a merge problem rather than a matching problem?
A: Matching decides sameness; merging decides which values survive, what happens to children, and what is lost — and it cannot be undone cleanly.

Q: What is the cheapest way to prevent duplicates entirely?
A: A unique External ID on the true business key, so every inbound write is an upsert rather than an insert.

Q: How does Data 360 identity resolution differ from merging?
A: It builds a unified profile across sources without deleting or merging the underlying CRM records.

Q: Which four MDM styles are on the table, and which do most Salesforce estates actually run?
A: Registry, consolidation, coexistence and centralized — most run coexistence, usually undocumented.

Q: What does a duplicate rule *not* protect you from?
A: Duplicates that already exist, and paths that bypass the rules such as lead conversion and some bulk operations.

## Related

- [01-admin · 08 Validation rules & duplicate management](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) — matching and duplicate rule mechanics
- [03 · Record IDs, external IDs & upsert](03-record-ids-external-ids-and-upsert.md) — the prevention story
- [25 · Data migration & cutover](25-data-migration-and-cutover.md) — where quality is decided once and for all
- [AI_Data · Identity resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) — unification without merging
