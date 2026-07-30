# Data 360 (formerly Data Cloud)

Newest entries at the top. Data 360 ships **monthly**, not per-seasonal-release — check the [monthly section of the release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&release=262&type=5) regularly.

---

## Naming: "Data Cloud" vs "Data 360" — get this straight

Salesforce began calling Data Cloud **"Data 360"** at Dreamforce 2025 (Oct 14, 2025), positioning it inside the **Agentforce 360** platform umbrella. Underlying product, licence, integrations and data model are unchanged. Salesforce's own developer documentation now consistently writes "Data 360."

**The rename is real, not just marketing.** Salesforce's own pricing calculator is branded **"Data 360 (Formerly Data Cloud)"**, there is a **Data 360 Starter** SKU (~$60k/yr) plus a $0 Provisioning (Everywhere) SKU, the Summer '26 release-notes section is titled **Data 360**, and the certification is now the **Salesforce Certified Data 360 Consultant**. A minority of analysts still call it positioning-only — safe to disregard, but check a current price book before writing a specific SKU into a contract.

**Lineage, for context** — this is the sixth name: Customer 360 Audiences → Salesforce CDP → Marketing Cloud CDP → Salesforce Genie → Salesforce Data Cloud → Data 360.

**The real shift isn't the name.** It's the repositioning from *passive customer data store* to *active context engine that grounds AI agents*. Every 2026 feature below follows from that.

---

## 2026-07-30 · The Python Data 360 connector: v1 deprecated, v2 still beta

[`salesforce-cdp-connector`](https://github.com/forcedotcom/salesforce-cdp-connector) — the **read-only Python client** most people use to query Data 360 and pull results into **pandas** — states plainly: *"This package is deprecated and will be removed once `salesforce-datacloud-connector` reaches GA."* The replacement, **`salesforce-datacloud-connector` 2.0.0b1**, landed alongside it on **June 2, 2026** and is a **pre-release**: `pip install --pre salesforce-datacloud-connector`, because pip won't resolve a beta without the flag. **No GA date is published.** On **July 29, 2026** maintainers broadened v1 CI to run on all PRs — reassuring for the gap, not a promise.

Auth covers JWT, username/password, OAuth token and client credentials, and you can target a **non-default dataspace** at connection time — remember that one, because querying the wrong dataspace returns a confidently **empty result**, not an error.

**Why it matters.** This is the standard route for notebook analysis, feature engineering and anything putting Data 360 data next to a training loop. New work should take v2 with `--pre`; existing scripts should **pin v1 explicitly and budget a migration**. General rule for this ecosystem: **a package rename usually carries a support-status change** — `cdp` → `datacloud` tracks CDP → Data Cloud → Data 360, and the rename is the tell that a lifecycle boundary is close.

**Also, on deploys:** `@salesforce/source-deploy-retrieve` **13.0.0** (July 29, 2026) requires **Node ≥ 22** and drops Node 18/20. SDR is what `sf project deploy` runs, so **any pipeline deploying Data 360 metadata** — streams, DLOs/DMOs, mappings, transforms, identity resolution, data kits — inherits that floor. It installs on Node 20 with only an `EBADENGINE` warning, then fails later in ways that look like metadata errors.

Full write-up: [02-data-cloud/2026-07-30](02-data-cloud/2026-07-30.md).

---

## 2026-07-28 · Summer '26 ingest and federation status changes

Three status changes that decide what you can put in production versus only prototype:

| Capability | Status |
|---|---|
| **Accelerated Data Ingest** — real-time CRM data into Data 360, no pipeline delay | **GA** |
| **AWS Glue Data Catalog** federation | **GA** |
| **Microsoft Fabric OneLake** federation | **Beta** |
| **Databricks** file federation connector — identity-provider (IdP) authentication | Summer '26 |
| **Run SQL from Apex** against Data 360 | Summer '26 |

**Why Accelerated Data Ingest matters most.** Scheduled ingestion meant Data 360's copy of a Case or Opportunity always lagged the live CRM record. Tolerable for analytics; fatal for agents, which then answer confidently from stale state. This removes the most common cause of a "the agent was wrong" ticket that turns out not to be a model problem at all — and it removes the workaround of bypassing Data 360 to call CRM directly from an action, which cost you the unified profile and its governance.

**Read the Beta label literally.** Fabric OneLake federation is fine to prototype and demo; it carries no support commitment and must not become load-bearing in a delivery plan. AWS Glue at GA is proposal-safe. The Databricks IdP change is a **security-review unlock** — "can we govern this connection centrally?" is the question that stalls zero-copy projects.

**SQL from Apex** removes the impedance mismatch: SOQL can't express the joins, aggregations and window functions that lakehouse work needs, and the alternative was HTTP callouts to the Direct API. An Apex-backed Agentforce action can now compute a rolling aggregate or multi-table join in one query. Same trap applies as with `SET OPTIONS` below — **specify the dataspace for DLO queries or get zero records, silently.**

Sources: [Developer's Guide to Summer '26](https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release) · [Data 360 in Summer '26: New Connectors, Document AI, and Real-Time Ingest](https://agentexchange.in/blog/data-360-summer-26) · [Zero Copy Connectivity](https://www.salesforce.com/data/connectivity/zero-copy/)

> **Unverified — do not rely on:** *Context Indexing* was reported in June 2026 as expected to reach GA "later in July 2026." No confirmation of that GA could be found as of 2026-07-28. Treat its status as open. Same for the precise status of *Document AI upgrades* and *secondary indexes*.

---

## 2026-07-26 · `SET OPTIONS` clause in SOQL

A new [`SET OPTIONS` clause](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql_select_set_options.htm) lets SOQL queries specify a Data 360 **dataspace** and control `NULL` / empty-string handling. The clause goes at the **very end** of the query.

Two rules that will bite you:

- **Dataspace is required for DLO queries.** Omit it and the query silently returns **zero records** — not an error. This is the kind of failure that costs an afternoon.
- **`honorEmptyStrings = true`** makes Data 360 treat `NULL` and `''` as distinct values. The default (`false`) collapses them the way Salesforce Platform objects do.

**Why it matters.** Data lake objects don't share Platform object semantics. `SET OPTIONS` is the seam where that difference becomes explicit, and the empty-string default is a classic source of wrong-but-plausible query results.

---

## 2026-07-26 · Code Extension — run Python inside Data 360

[Code Extension](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html) deploys custom **Python** scripts and functions that run in isolated containers on the platform. Current supported uses:

- Functions for complex **batch data transformations** — string manipulation, custom computations, data cleansing.
- Scripts implementing **custom chunking logic** on search index creation.

Salesforce says other Data 360 capabilities and languages will follow.

**Workflow.** Author and debug locally using the project scaffold from the [Data Custom Code Python SDK](https://pypi.org/project/salesforce-data-customcode/) plus the [Salesforce CLI Code Extension plugin](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/set-up-sdk.html). Validate against a sandbox with the CLI, deploy, run, then monitor via the new **code extensions log DLO**. Developers author the code; users with the **Data Cloud Architect** permission set run and monitor it. Salesforce recommends the [code extension Agent Skill](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-datacloud-code-extension) and the Data 360 MCP server to automate the build/debug/deploy loop. [Demo video](https://www.youtube.com/watch?v=96PC1KSnmfk).

**Why it matters.** Custom chunking logic is the headline for anyone doing RAG. Chunking strategy is usually the single biggest lever on retrieval quality, and until now it was a black box. Also note the separation of duties baked into the permission model — author ≠ operator.

---

## 2026-07-26 · Deploy code extensions with data kits

A DevOps **data kit** can now move [code extensions](https://help.salesforce.com/s/articleView?id=release-notes.rn_cdp_2026_summer_code_extension_data_kit.htm&release=262&type=5) — or the data transforms built from them — from sandbox to production. Adding such a transform to a data kit automatically pulls in its associated code extension.

**Why it matters.** Data 360 logic can now be promoted through a CI/CD pipeline the same way Apex and LWC metadata are. This closes one of the more painful gaps in Data Cloud DevOps.

---

## 2026-07-26 · Data 360 MCP Server (Developer Preview)

An [open-source MCP server](https://developer.salesforce.com/blogs/2026/05/introducing-the-data-360-mcp-server-developer-preview) connecting a coding agent to Data 360.

The design choice is worth studying on its own: rather than exposing roughly **200 REST operations** as 200 tools, it fronts them with **three facade tools** —

| Tool | Purpose |
|---|---|
| `search` | find a capability by intent |
| `payload_examples` | fetch a working request body |
| `execute` | run it |

**Why it matters.** This is the canonical answer to context-window blowout in MCP design: a searchable facade over a large API surface instead of a flat tool list. Directly transferable if you build your own MCP servers — see [03-claude-cca/](../03-claude-cca/INDEX.md).

There is also a **Data 360 standard hosted MCP server** (GA) for Data 360 queries and graph traversal — see [developer-tooling-and-apis.md](developer-tooling-and-apis.md).

---

## 2026-07-26 · Integration tests for Data 360 and Agentforce (Developer Preview)

The new `@IntegrationTest` Apex annotation allows **live callouts** and mid-transaction data commits via `IntegrationTest.commitTestOnly()`, with cleanup in a `@TearDown` method. Standard unit tests mock every callout and roll everything back, which makes asserting on real Agentforce or Data 360 behaviour impossible.

Constraints: **scratch orgs only**; add `ApexIntegrationTests` to the `features` array in the scratch org definition; tests run asynchronously, one at a time, via the Tooling API `runTestsAsynchronous` resource.

**Why it matters.** "You can't really test it" was a legitimate objection to grounding-heavy designs. This is the beginning of an answer — though scratch-org-only keeps it out of most real pipelines for now.

---

## Platform capabilities to know (current baseline)

**Intelligent Context** — automatically extracts and structures unstructured documents (PDFs, tables, images, flowcharts) into grounding data via a low-code pipeline. The distinctive bit: you can configure context so the same content is interpreted from **multiple business perspectives**. Create a search index with AI, then activate it everywhere.

**Tableau Semantics / semantic layer** — standardizes metric definitions and translates data into business language, so an agent asking "what was churn last quarter" gets the company's definition of churn rather than inventing one. Related: **OSI**, a vendor-neutral YAML-based open-source standard for interoperable semantic models, metrics and relationships; core spec finalized February 2026.

**Zero-Copy federation** — query data where it lives (Snowflake, BigQuery, Databricks, Amazon Redshift and others) with no physical movement, duplication or reconciliation jobs.

**Why these matter together.** They're the three legs of "grounding at enterprise scale": unstructured content (Intelligent Context), agreed meaning (semantic layer), and reach without copying (zero-copy). An agent answer is only as trustworthy as the weakest of the three.

---

## Sources

- [The Salesforce Developer's Guide to the Summer '26 Release](https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release)
- [Salesforce Summer '26 Release Notes](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.salesforce_release_notes.htm)
- [Build Trusted Semantic Layers for AI Agents with Data 360](https://www.salesforce.com/blog/semantic-layer-ai-agents-data-360/)
- [Architectural Lessons: The Salesforce Customer Zero Implementation of Data 360](https://www.salesforce.com/blog/data-architecture-customer-zero-data-360/)
- [Data Cloud – Zero Copy Connectivity](https://www.salesforce.com/data/connectivity/zero-copy/)
- [Salesforce Data Cloud Renamed to 'Data 360' As Part of 'Agentforce 360' (Salesforce Ben)](https://www.salesforceben.com/salesforce-data-cloud-renamed-to-data-360-as-part-of-agentforce-360/)
