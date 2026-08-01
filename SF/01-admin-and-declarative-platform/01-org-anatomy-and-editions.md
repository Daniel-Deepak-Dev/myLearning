# Org Anatomy & Editions

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** What an org *is*, the environment types around it, and how editions gate features and limits. Stops at licences and permission assignment — that is [07-security](../07-security-and-sharing/INDEX.md).

## Core idea

An **org** is Salesforce's unit of tenancy: one bundle of metadata, data, users, licences and limits, addressed by an Org ID and hosted on a specific instance. Everything you configure is scoped to it, and nothing crosses an org boundary without an integration. Editions are the commercial gate — they decide which features exist and how much of each you get, which is why "can I do X?" is frequently an edition question rather than a technical one. Non-production work happens in sandboxes and scratch orgs, which are themselves separate orgs that copy metadata, and sometimes data, from a production org.

## How it works

- **Production org** — the live tenant, created by a signup or a contract. You do not get a second one for free.
- **Developer Edition** — free, feature-complete, tiny limits. *Not* a sandbox: it has no parent org, so metadata has to be deployed in.
- **Sandboxes** — child environments of one production org, licensed by type:

| Type | Copies | Refresh interval | Storage |
|---|---|---|---|
| Developer | metadata only | 1 day | 200 MB |
| Developer Pro | metadata only | 1 day | 1 GB |
| Partial Copy | metadata + a sampled subset of data | 5 days | 5 GB |
| Full | metadata + **all** production data | 29 days | matches production |

- **Scratch orgs** — ephemeral, source-driven, built from a definition file and thrown away. The unit of work in [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).
- **Setup is two navigations people conflate:** the **Setup tree** (org-wide configuration, reached via Quick Find) and **Object Manager** (per-object configuration — fields, layouts, validation, triggers).
- **Edition allocations cap what you build.** Custom fields per object: **500** in Enterprise (plus up to 400 from a certified managed package), **800** in Unlimited (plus 100). Most objects have a hard ceiling of **800** custom fields whatever the edition.

## 2026 currency

SKU names churn far faster than the platform does — the Starter / Pro Suite / Foundations layer post-dates most tutorials and is covered by [18 · Salesforce Foundations](INDEX.md) in phase 02. Treat any edition list you read, including this one, as perishable: confirm against the **Available in** box at the top of the Help article in front of you.

## Gotchas

- A refresh **replaces** the sandbox. Anything created there and not in source control is gone, and the refresh interval is a floor, not a schedule.
- Partial Copy sampling is driven by a **sandbox template**. Without one you get metadata and no data, which reads as a failed refresh.
- Sandbox usernames get the sandbox name appended (`user@example.com.uat`). Integrations authenticating with a stored username break on every new sandbox.
- Data storage and file storage are **separate** allocations — exhausting file storage does not surface as a record limit.
- Org ID is *not* stable across a refresh of the same sandbox; do not use it as an environment fingerprint.
- Editions gate *features*, and a missing feature usually shows up as an absent Setup node rather than an error message.

## Recall

Q: What are the four sandbox types and their refresh intervals?
A: Developer (1 day), Developer Pro (1 day), Partial Copy (5 days), Full (29 days).

Q: Which sandbox types copy production data?
A: Only Partial Copy — a 5 GB sampled subset driven by a sandbox template — and Full, which copies everything.

Q: How many custom fields can one object hold in Enterprise Edition?
A: 500 that you create, plus up to 400 from a certified managed package; most objects cap at 800 overall.

Q: Why is a Developer Edition org not a substitute for a sandbox?
A: It has no parent production org, so there is no metadata or data to copy in and nothing to diff a deployment against.

Q: Where do you configure a custom field — the Setup tree or Object Manager?
A: Object Manager. The Setup tree carries org-wide configuration; anything per-object lives under the object.

## Related

- [02 · Release cadence & Release Updates](02-release-cadence-and-release-updates.md) — what happens to the org three times a year
- [13 · Data import, export & loading tools](13-data-import-export-and-loading-tools.md) — getting data into these environments
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — scratch orgs and the source-driven model
