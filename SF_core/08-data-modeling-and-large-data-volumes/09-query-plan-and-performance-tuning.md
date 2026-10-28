---
vault: SF_core
area: 08-data-modeling-and-large-data-volumes
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 14
---
# Query Plan & Performance Tuning

**Scope:** Proving *why* a specific query is slow, rather than guessing. The rules it tests against are [08](08-indexes-and-query-selectivity.md); Apex-side profiling is [02-apex · 24](../02-apex-and-triggers/24-apex-performance-and-profiling.md).

## Core idea

The Query Plan tool shows you what the optimizer decided and what it expects to cost. It turns "this report is slow" into a number, and that number has a threshold: **Cost above 1.0 means the filter was not selective and the query fell back to a table scan.** Cost is expressed *relative* to the selectivity threshold, which is why 1.0 is the line rather than some tuning-dependent value.

What the tool will not do is tell you what to fix. It reports statistics for fields that are **already indexed** — it never suggests a field worth indexing. So the workflow is always two-step: read the plan to find out which access path was chosen, then reason about the filter using [08](08-indexes-and-query-selectivity.md) to work out why a better one was not available.

## How it works

Enable it once per developer: **Developer Console → Help → Preferences → Enable Query Plan = true**, then the Query Plan button appears in the Query Editor.

| Column | What it tells you |
|---|---|
| **Leading Operation Type** | the access path chosen — `Index`, `Sharing`, `TableScan` or `Other` |
| **Cost** | relative to the selectivity threshold; **> 1.0 is non-selective** |
| **Cardinality** | estimated rows the leading operation returns |
| **sObject Cardinality** | approximate total rows in the object |
| **Fields** | which indexed fields were actually used |

- **`Index`** — an index was used. **`TableScan`** — everything was read. **`Sharing`** — the sharing tables drove the query, which happens when the running user's access is narrower than the filter. **`Other`** is an internal optimization.
- **Plans are listed best-first**, and the tool shows the alternatives it rejected — often more informative than the winner.
- **The plan is per running user and per data shape.** Run it as a user who resembles the one complaining, and in an org with realistic volume; a Developer sandbox will report everything as fast.
- **Cardinality vs sObject Cardinality is the ratio that matters.** 300,000 out of 100,000,000 is selective; 300,000 out of 400,000 is not.
- Beyond the plan: **Setup → Optimizer** and the **Lightning Usage App** for org-wide patterns, and Event Monitoring's `URI` and `API` event types for what real users actually run → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

> **From my notes.** The `QUERY PLAN` page (2025) is one of the few current pages in the seed corpus, and its worked example is right: `WHERE Industry = 'Technology'` gives `TableScan`, cost **1.5**; adding `AND CreatedDate > LAST_YEAR` gives `Index`, cost **0.5**. Two things to add and one to correct. It says *lower cost is better* but never states the threshold — **1.0 is the line**, and that is the number you actually use. Its list of standard indexed fields is accurate. **The correction:** it says custom indexes are created "by requesting Salesforce Support **or enabling them in Setup**." There is no Setup screen for custom indexes. Support is one route; the only self-service route is marking a field **External ID** or **Unique**, which creates an index as a side effect → [08](08-indexes-and-query-selectivity.md). Worth noting too that its "optimized query" worked only because `CreatedDate` is standard-indexed *and* the date filter cut the row count below threshold — adding a filter that is itself non-selective changes nothing.

## 2026 currency

**Web Console is GA (September 2026)**, and its SOQL Builder generates a query plan — a second way into the same tool. In **Winter '27 the Developer Console is hidden from the Setup menu by default**; turn it back on at Setup → **Web Console** → *Enable Developer Console* = Active. The Winter '27 LDV guide also names a **`CustomIndex` metadata file** as a route to a custom index, but the Metadata API guide says using it still means contacting Support — so External ID and Unique remain the only self-service routes.

## Gotchas

- **The tool only reports on indexed fields.** A blank `Fields` column means no usable index existed, not that none could exist.
- **A plan from an admin account is not evidence.** `View All Data` skips the sharing check, so the plan is not the one your users get.
- **Cost is relative, not milliseconds.** 0.9 and 0.2 are both selective; the difference between them is rarely worth chasing.
- **`Sharing` as leading operation is a sharing-model finding**, not a query finding — the fix may be in the access model → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).
- **Reports and list views cannot be pasted into the Query Editor.** Reconstruct the filter as SOQL, or the plan describes a different query from the slow one.
- **Fixing the query is not always the fix.** If the distribution is lopsided, no plan improves until the skew does → [10](10-data-skew.md).

## Recall

Q: What Cost value separates a selective query from a non-selective one, and why that number?
A: 1.0. Cost is expressed relative to the optimizer's selectivity threshold, so crossing 1.0 means the filter exceeded it.

Q: What do the four Leading Operation Type values mean?
A: `Index` — an index was used; `TableScan` — the whole object was read; `Sharing` — the sharing tables drove the query; `Other` — an internal optimization.

Q: What can the Query Plan tool not tell you?
A: Which field you should index. It only reports statistics for fields that are already indexed.

Q: How do you enable the tool?
A: Developer Console → Help → Preferences → Enable Query Plan = true. In Winter '27 the Developer Console is hidden by default, so first set Setup → Web Console → Enable Developer Console to Active — or use Web Console's own query plan.

Q: Why is a query plan run as a System Administrator misleading?
A: `View All Data` bypasses the sharing check, so the plan omits the cost your ordinary users actually pay.

## Related

- [08 · Indexes & query selectivity](08-indexes-and-query-selectivity.md) — the rules the plan is measuring against
- [10 · Data skew](10-data-skew.md) — when the plan is fine and the distribution is not
- [11 · Skinny tables & support levers](11-skinny-tables-and-support-levers.md) — what is left when tuning runs out
- [02-apex · 24 Apex performance & profiling](../02-apex-and-triggers/24-apex-performance-and-profiling.md) — the transaction-level view around the query

## Sources

- [Announcing General Availability: Web Console](https://developer.salesforce.com/blogs/2026/09/announcing-general-availability-web-console-your-modern-in-browser-ide) — Salesforce Developers blog · via search 2026-10-28 · Web Console GA; SOQL Builder; *"generating a query plan"*
- [Web Console — Frequently Asked Questions](https://developer.salesforce.com/docs/platform/webconsole/guide/faq.html) — Salesforce Developers · via search 2026-10-28 · Developer Console not visible in Setup by default; Setup → Web Console → Enable Developer Console
- [The Salesforce Developer's Guide to the Winter '27 Release](https://developer.salesforce.com/blogs/2026/10/developers-guide-to-the-winter-27-release) — Salesforce Developers blog · via search 2026-10-28 · *"In Winter '27, Developer Console doesn't appear in the Setup menu by default"*; Web Console query plans
- [Best Practices for Deployments with Large Data Volumes (PDF, Winter '27)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_large_data_volumes_bp.pdf) — Salesforce Developers · read 2026-10-28 · custom indexes via Support *"or by deploying a custom index XML file via the Metadata API"*; thresholds unchanged
- [Metadata API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-10-28 · `CustomIndex` (API 50.0+): *"To use this metadata and create a custom index … contact Salesforce Customer Support"*

## History

- 2026-10-28 · Winter '27 currency check: Developer Console hidden by default; Web Console GA as the second query-plan route; `CustomIndex` metadata still Support-gated
