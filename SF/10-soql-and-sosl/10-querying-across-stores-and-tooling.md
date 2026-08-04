# Querying Across Stores & the Tooling Surface

> Area: 10-soql-and-sosl · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 22

**Scope:** Where SOQL behaves differently — big objects, external objects, custom metadata, Tooling API, Data 360 — and every place you can issue a query from. Bulk query mechanics are [06-integration · 07](../06-integration-and-apis/07-bulk-api-2.md).

## Core idea

"SOQL" names one grammar over several stores that do not share behaviour. A query against a custom object hits the multitenant database and spends from the governor budget. **The same-looking query against a big object obeys a completely different index model, against an external object becomes a network callout, and against custom metadata costs no query at all.** Knowing which store you are addressing is what makes a limit calculation correct — and it is routinely wrong in both directions, with people budgeting queries for custom metadata that are free, and assuming an external object query is cheap when it is a synchronous round trip to somebody else's system. The tooling half of this note is the same point from the other side: the same query returns different results depending on whether the Query Editor, the CLI or the REST API issued it, because they differ in execution context.

## How it works

| Store | Behaviour that differs |
|---|---|
| **Custom metadata / custom settings** | **Do not consume SOQL queries or rows** — already in an application cache. `getInstance()` is cheaper still → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) |
| **Big objects** | Filters must follow the **index definition, left to right, with no gaps**; no `LIMIT`/`OFFSET` paging as usual. **Async SOQL was retired Summer '23** → [08-data · 14](../08-data-modeling-and-large-data-volumes/14-big-objects-and-the-archive-tier.md) |
| **External objects** | Each query is an **OData callout**; joins to local data are limited, and latency is the real cost → [08-data · 17](../08-data-modeling-and-large-data-volumes/17-external-objects-vs-replicated-copies.md) |
| **Tooling API** | Queries *metadata* — `ApexClass`, `FlowDefinition`, `ApexCodeCoverage` — with its own endpoint and object set → [06-integration · 09](../06-integration-and-apis/09-metadata-tooling-and-connect-apis.md) |
| **Data 360 (DMOs)** | Not SOQL at all in general — DMOs are queried through Data Cloud's own SQL surface → [08-data · 18](../08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md) |

- **Where a query can be issued from:** Developer Console **Query Editor** (system context, admin's access), **`sf data query`** with `--use-tooling-api` and `--bulk`, **Workbench**, the REST **`/query`** and **`/queryAll`** resources → [06-integration · 04](../06-integration-and-apis/04-rest-api-fundamentals.md), **Bulk API 2.0 query jobs** for extraction volumes, and **Apex** → [02-apex · 03](../02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md).
- **`/queryAll` and `ALL ROWS` are the only ways to see soft-deleted rows**; ordinary queries exclude them silently → [08-data · 13](../08-data-modeling-and-large-data-volumes/13-deletes-recycle-bin-and-physical-deletion.md).

## 2026 currency

**Named Query API reached GA in Spring '26**, after Beta in Winter '26, and it is the most consequential addition to this surface in years: an admin defines and validates a SOQL query **in Setup**, and saving it **automatically exposes it as a REST endpoint** whose name is the resource path and whose parameters become URI query parameters. The same definition can be surfaced as a **custom agent action (Beta)**. The architectural significance is that a read-only integration or agent-grounding query no longer needs an Apex REST class or a Flow — which removes the commonest reason to write `@RestResource` at all, and moves a piece of the API contract from code review into Setup. Alongside it, **Database Insights** and **Platform Cache Detection for SOQL** (Winter '26) surface inefficient and repeated queries with recommendations. → [06-integration · 18](../06-integration-and-apis/18-apex-rest-and-custom-endpoints.md), [06-integration · 19](../06-integration-and-apis/19-external-services-openapi-and-the-api-catalog.md)

## Gotchas

- **Custom metadata queries are free, and people budget for them anyway** — then hit the limit somewhere they did not count, because the free ones were the ones being counted.
- **A big object query that does not match the index prefix fails or scans catastrophically.** The index is defined at creation and is **immutable**, so a wrong index means recreating the object.
- **An external object query is a synchronous callout** — it consumes callout limits and time, and a page of a list view can issue several.
- **The Query Editor runs as an administrator in system context**, so it is the wrong place to verify anything about user-mode behaviour at 67.0. A query that works there proves nothing about a support agent.
- **Tooling API objects are not queryable from ordinary SOQL** and vice versa — `ApexClass` is Tooling, and reaching it from Apex needs a callout to the Tooling endpoint.
- **`sf data query --bulk` uses Bulk API 2.0 and returns results differently** from the synchronous path, including different limits and no row-count parity with the REST `/query` resource.
- **A Named Query is deployable metadata that exposes data.** It is a public read endpoint defined outside the code review path, and should be governed like one.

## Recall

Q: Which SOQL queries do not consume a query against the governor limit?
A: Custom metadata types and custom settings — both are held in an application cache rather than queried from the database.

Q: What constrains a big object query?
A: Its index definition, which is set at creation and immutable. Filters must match the indexed fields left to right with no gaps.

Q: Why is the Developer Console Query Editor a poor place to verify a query at 67.0?
A: It runs in system context as an administrator. User mode is the default in Apex and APIs, so the editor cannot show what a lower-privileged user would get.

Q: What is Named Query API and when did it become GA?
A: A Setup-defined SOQL query automatically exposed as a REST endpoint, and optionally as a custom agent action. Beta in Winter '26, **GA in Spring '26**.

Q: How do you see soft-deleted records?
A: `ALL ROWS` in SOQL or the `/queryAll` REST resource. Ordinary queries exclude them without saying so.

## Related

- [01 · Query anatomy & the SOQL model](01-query-anatomy-and-the-soql-model.md) — the baseline behaviour these stores diverge from
- [06-integration · 04 REST API fundamentals](../06-integration-and-apis/04-rest-api-fundamentals.md) — `/query` and `/queryAll`, and where Named Query sits beside them
- [08-data · 14 Big objects & the archive tier](../08-data-modeling-and-large-data-volumes/14-big-objects-and-the-archive-tier.md) — the immutable index model and the retired Async SOQL
- [01-admin · 09 Custom Metadata vs Custom Settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — why config reads are free
