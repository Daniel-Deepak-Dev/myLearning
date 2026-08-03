# Metadata, Tooling & Connect APIs

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The three APIs that operate on the org's **configuration and features** rather than its records. How pipelines actually use Metadata API is [09-devops](../09-devops-sfdx-and-release-management/INDEX.md); this is the API surface itself.

## Core idea

Data APIs move records. These three move everything else — object definitions, Apex, layouts, permission sets, debug logs, feeds — and the reason to know them as APIs, not as tool features, is that **you already depend on all three without calling them directly.** `sf project deploy`, DevOps Center, the VS Code extensions and every CI pipeline are Metadata API clients. Code completion, debug logs and test results in an IDE are Tooling API calls. Experience Cloud and Chatter surfaces run on Connect.

The distinction that matters day to day is **granularity**. Metadata API is file-based and whole-component: it deploys and retrieves packages, asynchronously, with ~400 types. Tooling API is record-based and surgical: ~70 types, but each is queryable with SOQL and editable field by field, which is what makes interactive tooling possible at all.

## How it works

| API | Protocol | Shape | Reach for it to |
|---|---|---|---|
| **Metadata** | **SOAP only** for deploy/retrieve | zipped files + `package.xml`, **asynchronous** | deploy, retrieve, migrate an org |
| **Tooling** | REST **and** SOAP | sObject-like records, SOQL-queryable | read one Apex class, set a trace flag, run a test |
| **Connect REST** | REST | feature-shaped resources | Chatter, feeds, files, Experience Cloud |

- **Tooling API has its own query endpoint** — `/services/data/v67.0/tooling/query` — and **its objects are not visible to ordinary SOQL**. That is the answer to *"why can't I query `ApexClass`?"*: right query, wrong endpoint.
- **The developer-facing Tooling objects are the useful ones:** `ApexClass` (including `Body`), `ApexLog`, `ApexTestResult`, `TraceFlag`, `ApexExecutionOverlayResult`, `FlexiPage`, `EntityDefinition`, `CustomField`.
- **Metadata API deploys are asynchronous**: submit, receive an ID, poll for status. Any tool that appears to deploy synchronously is polling for you.
- **Apex classes carry their own API version** in metadata, which is how a 2019 class keeps 2019 behaviour in a 67.0 org. → [02](02-api-versions-and-the-retirement-treadmill.md)
- **Connect REST API is the "features, not records" surface** — it returns what a feature needs rather than raw rows, and it has an Apex counterpart in **Connect in Apex**.
- **This is where SOAP genuinely persists.** Metadata API has no REST equivalent for deploy/retrieve. → [05](05-soap-api-and-where-it-persists.md)

## 2026 currency

**Connect REST API's limits changed at 67.0 and it is a relief, not a restriction.** Orgs migrated off the old restrictive **per-user, per-app, per-hour** limit onto the org's **per-24-hour Platform API limit**; only requests that genuinely require Chatter keep an hourly throttle. **The same change applies to Connect in Apex.** Integrations previously architected around that hourly ceiling can be simplified. Separately, tooling built on these APIs is now the fastest-moving part of the platform — the **Metadata API Context MCP server** exposes metadata to agents as five granular tools, and the `sf` CLI's underlying libraries ship weekly. Both, with the Node-version and supply-chain caveats that come with them, are tracked in [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Gotchas

- **`SELECT Body FROM ApexClass` fails on the normal query endpoint** and succeeds on `/tooling/query`. The error does not say so.
- **Metadata API retrieve writes attacker-influenceable bytes to disk.** A zip-slip in static-resource conversion was patched in July 2026 and the fix is gated behind a major version — retrieve is not a read-only operation. → [AI_Data radar](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)
- **Tooling API can edit production Apex directly.** It is how "someone changed a class in production" happens without a deployment record.
- **`TraceFlag` records expire and accumulate.** Debug logging that silently stops is usually an expired trace flag, not a broken log level.
- **Metadata coverage is not total.** Some configuration has no metadata type at all, which is what turns a "fully automated" pipeline into a documented manual step. → [09-devops](../09-devops-sfdx-and-release-management/INDEX.md)
- **These APIs need administrative permissions**, so an integration user scoped for data has no business holding them. → [07-security · 03](../07-security-and-sharing/03-profiles-and-the-permission-set-led-model.md)

## Recall

Q: Why can't you query `ApexClass` with ordinary SOQL?
A: Tooling objects live behind the Tooling API's own endpoint — `/services/data/vXX.0/tooling/query`.

Q: What is the granularity difference between Metadata API and Tooling API?
A: Metadata is file-based, whole-component, asynchronous, ~400 types; Tooling is record-based, field-level, SOQL-queryable, ~70 types.

Q: Which protocol does Metadata API deploy/retrieve use?
A: SOAP — there is no REST equivalent, which is a large part of why SOAP persists.

Q: What changed for Connect REST API at 67.0?
A: It moved off the per-user/per-app/per-hour limit onto the org's per-24-hour Platform API limit. Only Chatter-requiring requests keep an hourly throttle.

Q: Name three Tooling API objects worth knowing.
A: `ApexLog`, `TraceFlag` and `ApexTestResult` — debug logs, log configuration and test results. (`ApexClass` and `EntityDefinition` also count.)

## Related

- [05 · SOAP API & where it persists](05-soap-api-and-where-it-persists.md) — the protocol these keep alive
- [02 · API versions & the retirement treadmill](02-api-versions-and-the-retirement-treadmill.md) — per-class API versions live in metadata
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — the pipelines built on Metadata API
- [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md) — the weekly-moving tooling layer
