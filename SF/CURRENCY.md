# Currency — what "current" means here

Everything in `SF/` targets **Summer '26 · API 67.0**. Last reviewed **2026-08-01**.

## Version map

| Release | API | Notes |
|---|---|---|
| Winter '26 | 65.0 | |
| Spring '26 | 66.0 | |
| **Summer '26** | **67.0** | **The target.** Security defaults flipped here. |
| Winter '27 | 68.0 | Not yet GA — preview only. Nothing here should assume it. |

Older mapping for reading legacy code: Spring '24 = 60.0, Summer '24 = 61.0, Winter '25 = 62.0, Spring '25 = 63.0, Summer '25 = 64.0.

## The six defaults that invalidate older tutorials

Anything written before ~2024 will get at least one of these wrong. Every ⚠️-flagged note opens by correcting the relevant one.

| # | Was | Is now | Where it bites |
|---|---|---|---|
| 1 | Apex SOQL/DML ran in **system mode** | **User mode is the default at API 67.0** — elevated access is opt-in | [02-apex](02-apex-and-triggers/INDEX.md), [07-security](07-security-and-sharing/INDEX.md) |
| 2 | Keyword-less class **inherited** caller's sharing | Defaults to **`with sharing`**; bypass is a deliberate `without sharing` | [02-apex](02-apex-and-triggers/INDEX.md) |
| 3 | `WITH SECURITY_ENFORCED` | **Retired — no longer compiles.** Use `WITH USER_MODE` | [02-apex](02-apex-and-triggers/INDEX.md) |
| 4 | **Locker Service** | **Lightning Web Security (LWS)** | [03-lwc](03-lwc-and-slds/INDEX.md) |
| 5 | **CometD** streaming | **Pub/Sub API** (gRPC) | [06-integration](06-integration-and-apis/INDEX.md) |
| 6 | `sfdx force:…` | **`sf` CLI v2** topic grammar | [09-devops](09-devops-sfdx-and-release-management/INDEX.md) |

Detail, sources and dates for all six: [AI_Data/05-release-radar/trust-security-and-governance.md](../AI_Data/05-release-radar/trust-security-and-governance.md) and [developer-tooling-and-apis.md](../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Retirements to know

- **Workflow Rules & Process Builder** — retired; Flow is the only declarative automation tool. → [04-flow](04-flow-and-automation/INDEX.md)
- **Aura templates for new Experience Cloud sites** — LWR is the default. → [05-experience-cloud](05-experience-cloud-lwr/INDEX.md)
- **Connected Apps for new integrations** — superseded by External Client Apps. → [06-integration](06-integration-and-apis/INDEX.md)
- **Change Sets** — superseded by DevOps Center / source-driven pipelines. → [09-devops](09-devops-sfdx-and-release-management/INDEX.md)
- **1GP packaging** — legacy; 2GP unlocked/managed is the model. → [09-devops](09-devops-sfdx-and-release-management/INDEX.md)
- **SOAP `login()`** — retirement announced for Summer '27.
- **Platform API versions 21.0–30.0** — deprecated Summer '22, **retired Summer '25**. Old Data Loader builds and pinned integrations stop working rather than degrade. → [01-admin · 13](01-admin-and-declarative-platform/13-data-import-export-and-loading-tools.md)
- **Bulk API v1** — not retired, but legacy; Bulk API 2.0 is where new capability lands. Audit remaining v1 usage under Setup → Bulk Data Load Jobs, filtering for **Bulk V1** jobs.

> **Not a retirement — a myth corrected in phase 01.** Data Loader does **not** default to Bulk API 2.0. It still defaults to the SOAP-based API, with *Use Bulk API* and *Use Bulk API 2.0* as separate opt-in checkboxes.

## Two more things that are *not* retired — checked in phase 02

Both are commonly asserted as dead. Neither is, and saying so to a client is a credibility loss.

- **Page layouts.** Demoted, not retired. Dynamic Forms owns field composition and visibility ([01-admin · 05](01-admin-and-declarative-platform/05-dynamic-forms-and-lightning-app-builder.md)), but the layout still owns related lists, actions, compact layouts, Salesforce Classic, and the **required/read-only field properties** Dynamic Forms inherits.
- **Classic approval processes.** Fully supported; the docs were renamed *Classic Approval Processes* and Flow approvals are the "modern alternative". **No retirement date has been announced.** → [01-admin · 12](01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md)

## New in Apex at 67.0 — checked in phase 03

- **Multiline strings and `String.template()`** are the Summer '26 Apex language additions, both GA. Triple single quotes (`'''`) open and close a literal block; `.template(Map<String, Object>)` fills `${key}` placeholders from a map. They retire the concatenation chains behind email bodies, JSON payloads, HTTP request bodies and assembled SOQL. Two traps: the newline immediately after the opening `'''` is **trimmed**, and `.template()` renders a `Datetime` in **GMT** as `yyyy-MM-dd HH:mm:ss`, which is not what `String.valueOf()` does. → [02-apex · 02](02-apex-and-triggers/02-modern-apex-syntax.md)
- **Dynamic SOQL carries an access level explicitly.** `Database.queryWithBinds(query, bindMap, AccessLevel)` — Spring '23, and defaulting to user mode at 67.0. Binds resolve from the map by key rather than from Apex locals, which removes the old scoping surprise. → [02-apex · 04](02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md)

> **Not new — a myth corrected in phase 03.** `??`, `?.` and `switch on` are routinely written up as modern Apex. None of them is new at 67.0: `switch on` is **Summer '18 (43.0)**, safe navigation is **Winter '21 (50.0)**, null coalescing is **Spring '24 (60.0)**. Useful for dating an inherited codebase; not a release-notes talking point.

## New in async Apex at 67.0 — checked in phase 04

- **Elastic limits for async jobs are Beta.** `Queueable` and `@future` jobs can be enqueued up to **twice** the licensed daily limit, with the overflow throttled rather than rejected. This changes a *failure mode*, not just a ceiling: a runaway chain used to stop with a `LimitException` and now merely slows down. Read `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` from `System.OrgLimits.getMap()` rather than assuming headroom. → [02-apex · 12](02-apex-and-triggers/12-async-apex-overview-and-choosing.md), [13](02-apex-and-triggers/13-queueable-apex-and-chaining.md)
- **The security flip reaches async, and it fails quietly there.** A batch `QueryLocator`, a scheduled job's query and a finalizer's audit insert all default to **user mode** at 67.0. The symptom is not an exception — it is a nightly job that processes a subset of its scope and still reports `Completed`. Audit `CronTrigger.OwnerId` and any unqualified `Database.getQueryLocator` in scheduled work. → [02-apex · 14](02-apex-and-triggers/14-batch-apex-and-stateful-processing.md), [15](02-apex-and-triggers/15-scheduled-apex-and-cron.md)

> **Not new — a myth corrected in phase 04.** `Database.Cursor` is routinely written up as a Summer '26 addition and as a way around the 50,000-row query limit. **Both are wrong.** Apex cursors have been **GA since Summer '24 (API 61.0)**, and `Cursor.fetch()` costs a SOQL query whose rows count against the row limit — so a cursor buys you **heap and resumability across transactions** (2-day lifetime), not row budget. → [02-apex · 17](02-apex-and-triggers/17-database-cursor-and-large-result-sets.md)

> **A retirement to add to the list above.** **Legacy named credentials are deprecated** and will be discontinued. Since Winter '23 the model is two objects — an *external credential* (authentication protocol plus principals) and a *named credential* (base URL, pointing at one). The migration is not a rename: the legacy object has no principals, so it cannot express *who* may call out via a permission set. → [02-apex · 19](02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)

## Licensing changes that change a design decision

- **Flow Orchestration is a standard flow type as of 2026-02-18** — previously a paid add-on. Included with no usage-based run limits in Enterprise, Performance, Unlimited, all Einstein 1 and Developer editions. Cost was the usual reason to stay on classic approvals; that reason is gone. → [01-admin · 12](01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md)
- **Salesforce Foundations is a $0 add-on** on Enterprise, Unlimited, Einstein 1 Sales and Einstein 1 Service — and it **auto-provisions Data 360** and starts an Agentforce credit meter. Free commercially, not free architecturally. → [01-admin · 18](01-admin-and-declarative-platform/18-salesforce-foundations-and-org-strategy.md)
- **Setup with Agentforce is GA and its Setup actions are non-billable** — no Flex credits consumed. Runtime agents in the same org still bill normally. → [01-admin · 19](01-admin-and-declarative-platform/19-agentforce-in-setup-and-ai-assisted-admin.md)

## Keeping this file honest

When a phase discovers a currency fact, it goes **here** as a row and into the relevant note — not duplicated into five notes. If it's genuinely new news rather than a stable fact, it belongs in [AI_Data/05-release-radar/](../AI_Data/05-release-radar/README.md) instead and this file links to it.
