# Field Audit Trail & Data Retention

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Shield's second pillar — keeping *field history* for years instead of months, and the retention policy object that governs it. The free Setup-side monitoring surfaces are [01-admin · 17](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md), which forward-links here for exactly this. Configuration-change auditing is Setup Audit Trail, not this.

## Core idea

Standard field history tracking is a convenience feature wearing a compliance feature's name. It keeps up to **20 fields per object** and retains rows for about **18 months in the UI / 24 months via the API**, after which the platform silently deletes them — which is fine until an auditor asks what a field held three years ago. Field Audit Trail raises both numbers and, more importantly, changes where the data lives: history is **archived into a big object** rather than purged, so it stops competing with your data storage allocation and starts behaving like an archive. The decision it forces is a retention *policy* — an explicit statement, per object, of how long history matters — which most orgs have never written down.

## How it works

| | Field History Tracking | Field Audit Trail |
|---|---|---|
| fields per object | 20 | **60** |
| retention | ~18 months UI / 24 months API, then purged | up to **10 years** |
| where it lives | `<Object>History` | archived into **`FieldHistoryArchive`** (a big object) |
| counts against data storage | yes | **no**, once archived |
| licensing | standard | **Shield** (or as a standalone add-on) |

- **Archiving does not replace the standard object.** Salesforce keeps writing to `AccountHistory` and friends as normal; at the end of the standard window it moves those rows into `FieldHistoryArchive` instead of deleting them.
- **`HistoryRetentionPolicy` is metadata, per object.** It states how many months of history to keep in the standard object before archiving, and how long to keep the archive. Deploy it like any other metadata — it is not a Setup checkbox.
- **Defaults are 18 months in production and one month in sandboxes**, with archived data kept until you delete it. The sandbox default surprises people testing the feature.
- **Query it with SOQL like any big object**, subject to big-object query rules: you filter on the index fields in order, and there is no arbitrary `WHERE`. → [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **Turning field history tracking *on* is still per field, in Object Manager.** Field Audit Trail changes the ceiling and the destination, not the act of tracking.

## Gotchas

- **History is not versioning.** It records that a field changed from A to B, not the whole record — you cannot reconstruct a record's state at a date from it alone.
- **Long text, rich text and multi-select picklists are not tracked**, and formula fields never were — the values people most want in an audit are often the untrackable ones.
- **Deleting the tracked field deletes its meaning**, not its rows: the archive keeps entries referencing a field that no longer exists.
- **The one-month sandbox default makes the feature look broken in testing.** Set `HistoryRetentionPolicy` explicitly in the sandbox before concluding anything.
- **Big object queries are index-ordered, not ad hoc.** An "just query the archive" plan that assumes normal SOQL will not survive contact with it.
- **Archived history is not covered by a normal data export.** Backup and restore tooling frequently skips big objects entirely — verify rather than assume. → [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md)
- **This is a Shield SKU.** Scoping a compliance requirement around it without checking entitlement is the same mistake as designing around Who Sees What Explorer. → [24](24-security-center-and-health-check.md)
- **Field Audit Trail answers *what the data was*. Setup Audit Trail answers *who changed the configuration*.** Different questions, different tools, routinely conflated in requirements documents. → [15](15-auditing-and-troubleshooting-access.md)

## Recall

Q: What are the two numbers Field Audit Trail changes?
A: Fields tracked per object, 20 → 60; and retention, ~18 months → up to 10 years.

Q: Where does archived field history actually go?
A: The `FieldHistoryArchive` big object, which does not count against data storage.

Q: What object defines the retention policy, and is it configured in Setup?
A: `HistoryRetentionPolicy`, per tracked object — it is metadata you deploy, not a Setup checkbox.

Q: What are the default archiving windows?
A: 18 months in production, one month in sandboxes, with archived data retained until explicitly deleted.

Q: What question does Field Audit Trail *not* answer?
A: Who changed the org's configuration — that is Setup Audit Trail. It also cannot reconstruct a whole record's state at a past date.

## Related

- [21 · Shield Platform Encryption](21-shield-platform-encryption.md) — Shield's first pillar
- [23 · Event Monitoring & Transaction Security](23-event-monitoring-and-transaction-security.md) — the third, and the one that records *access* rather than change
- [01-admin · 17 Setup Audit Trail, monitoring & usage](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md) — the free tier, and the note that forward-links here
- [25 · Privacy, consent & data protection](25-privacy-consent-and-data-protection.md) — retention as a privacy obligation rather than an audit one
