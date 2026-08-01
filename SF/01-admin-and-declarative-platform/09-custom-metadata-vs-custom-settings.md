# Custom Metadata vs Custom Settings

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** Where configuration values live, and the decision between Custom Metadata Types and Custom Settings. Runtime access patterns in Apex are expanded in [02-apex](../02-apex-and-triggers/INDEX.md).

> **What changed.** Reaching for Custom Settings as the default home for configuration is wrong. **Custom Metadata Types are stored as metadata, so their *records* deploy and package** — Salesforce's own guidance is to use CMDT instead of list custom settings. Custom Settings survive for one job: hierarchy values that vary per user or profile.

## Core idea

Both mechanisms exist to keep configuration out of code. The distinction that decides everything is *what the records are*: Custom Metadata Type records are **metadata**, so they travel through the Metadata API, change sets and packages exactly like a field definition. List Custom Setting records are **data**, so they do not — you deploy the container and then reload the contents by hand in every org. That is the whole argument, and it is why "which environment is this value different in?" is the question that picks the tool.

## How it works

| | Custom Metadata Type | Custom Setting (hierarchy) |
|---|---|---|
| Records are | metadata — deployable, packageable | data — not deployable |
| Per-user / per-profile values | no | **yes, this is its purpose** |
| SOQL cost in Apex | **unlimited queries** — does not consume the governor limit | cached, no query |
| SOQL cost in Flow | **counts toward Apex governor limits** | cached |
| Written at runtime | only via Metadata API, asynchronously | ordinary DML |

- **Access without a query.** `getAll()`, `getInstance(recordId)` and `getInstance(qualifiedApiName)` read from the application cache, so they cost nothing at all. Direct SOQL on a `__mdt` object is also exempt from the per-transaction query limit in Apex.
- **Reachable declaratively too** — CMDT values can be referenced from formula fields, validation rules and Flow, not just Apex.
- **Allocations:** 200 CMDT per org (plus up to 150 from certified packages), 100 fields per type, 10 million characters of custom metadata per org, 50,000 records returned per transaction.
- **Runtime writes are awkward by design.** Updating a CMDT record from Apex means building a `Metadata.DeployContainer` and enqueuing it — asynchronous, so you cannot write and read back in the same transaction. If a value changes during normal business operation, it is *data*, not configuration.
- **List Custom Settings are legacy.** Anything you would have modelled as one belongs in a CMDT.

## Gotchas

- **The SOQL exemption is not universal.** CMDT queries are free in Apex but **count against governor limits inside Flow**, and queries pulling **long text area** fields count everywhere.
- CMDT records are metadata, so a "config change" in production is a **deployment** and is audited as one — usually what you want, occasionally a surprise to an admin expecting to edit a row.
- Storage is metered in **characters, not records**: picklists and checkboxes each count as 10 characters, metadata relationship fields as 10–15.
- Record counts returned by SOQL can differ from what the UI shows, because CMDT visibility settings and the user's permissions filter results.
- You cannot write a CMDT record synchronously — code that tries to update config mid-transaction and re-read it will not work.
- Hierarchy custom settings resolve **user → profile → org default**; a `null` at the user level falls through, so "unset" and "set to false" are not the same thing.
- Protected CMDT and protected custom settings are invisible to subscriber orgs — useful for packaged secrets, confusing when debugging someone else's package.

## Recall

Q: What is the single decisive difference between a CMDT record and a list custom setting record?
A: The CMDT record is metadata, so it deploys and packages; the custom setting record is data and must be reloaded per org.

Q: Do SOQL queries against a `__mdt` object consume the Apex query governor limit?
A: No — they are unlimited in Apex. But they *do* count inside Flow, and queries including long text area fields count everywhere.

Q: What is the remaining legitimate use case for Custom Settings?
A: Hierarchy settings — values that differ per user or per profile, with an org-wide default.

Q: How do you update a Custom Metadata Type record from Apex, and what is the catch?
A: Through `Metadata.DeployContainer`, which is asynchronous — you cannot write and read the value back in the same transaction.

Q: How is custom metadata storage measured?
A: In characters, not record count — 10 million per org, with picklists and checkboxes counting 10 characters each.

## Related

- [08 · Validation rules & duplicate management](08-validation-rules-and-duplicate-management.md) — the custom-permission and hierarchy-setting bypass pattern
- [02-apex · INDEX](../02-apex-and-triggers/INDEX.md) — governor limits and the runtime access methods
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — why deployable configuration matters to a pipeline
