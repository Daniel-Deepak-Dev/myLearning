# Data Engineering & Pipeline Patterns

> Track: Core skills · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Vendor-neutral. Platform application lives in [01-data-cloud/](../../01-data-cloud/INDEX.md).

**Roadmap scope:** ETL vs ELT, orchestration concepts, idempotent loads, data quality checks. Enough general data engineering to talk shop beyond Salesforce.

## What is it?

The discipline of moving data reliably. Four ideas carry most of it:

| Idea | The point |
|---|---|
| **ETL vs ELT** | Transform before loading, vs load raw then transform in the warehouse (ELT — the modern default, and what a lakehouse assumes) |
| **Idempotency** | Re-running produces the same result — the property that makes retries safe |
| **Orchestration** | Scheduling, dependencies, retries, alerting |
| **Data quality** | Checks that fail loudly rather than propagating silently |

## Why it matters (for the AI-Salesforce architect role)

**Two of these became sharper when agents entered the picture, and that's what's worth internalizing.**

### 1. Batch vs real-time is now a correctness decision, not a cost one

Scheduled loads were always a trade-off between freshness and cost. For analytics, "four hours stale" is invisible — a churn dashboard doesn't care.

For an agent, four hours stale means **answering confidently from a case that closed twenty minutes ago**. Same pipeline, same lag, entirely different consequence.

**Accelerated Data Ingest (GA in Summer '26)** is the platform's answer for CRM data. The general principle transfers: *if an agent reads it, it needs to be current; if a dashboard reads it, scheduled is fine.* Decide per stream. See [ingestion](../../01-data-cloud/02-ingestion/notes.md).

### 2. Idempotency moved from pipelines into actions

Idempotency has always mattered for retries after a failed load. Agents extend it somewhere new: **an agent may retry an action after a timeout**, without a human deciding to.

A non-idempotent "issue refund" action can issue two. That's not a pipeline concern any more — it's an application-design concern for every agent action you write. See [custom agent actions](../../02-salesforce-ai/05-custom-agent-actions/notes.md).

**How to make an operation idempotent:** natural keys instead of auto-increment, upserts instead of inserts, an explicit idempotency key on write endpoints, or a check-then-act guarded by a unique constraint.

## How it works

### ETL vs ELT

```
ETL   source → transform → load       (transform outside; classic, tool-heavy)
ELT   source → load → transform       (transform in the warehouse; modern default)
```

ELT won because storage got cheap and warehouse compute got fast. It also keeps the raw data, so a transformation bug is re-runnable rather than lost — which is why lakehouses assume it. Data 360's DSO → DLO → DMO flow is ELT: land raw, harmonize after.

### Data quality — fail loudly

The rule is that **a check that logs a warning nobody reads is not a check**. Worth asserting on every load: row counts within an expected range, no unexpected nulls in key fields, referential integrity, and freshness (when did this last update?).

The freshness check is the one most often missing, and it's the one that catches the agent-grounding failure before a customer does.

### Data lineage

Tracking where data came from and how it was transformed. Needed for trust ("why does this number differ from the source system?"), debugging, and compliance. In an agentic context it also answers a newer question: **"which data produced this agent's answer?"** — which is what a Trust Layer audit trail is for on the AI side.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Build a small idempotent load: run it twice, confirm the result is identical.
- [ ] Add a freshness assertion to a pipeline and make it fail the run, not log a warning.
- [ ] Audit a real org's data streams and label each agent-facing or analytics-facing.
- [ ] Take one agent action and make it idempotent. Then call it twice and prove it.

## Gotchas & sharp edges

- **Agents retry.** Every write an agent can trigger should be idempotent.
- **Freshness is a correctness property for agents**, not a nice-to-have.
- **Warnings nobody reads aren't quality checks.** Fail the run.
- **Over-refreshing everything is invisible waste** — and under profile-based pricing, duplicate-heavy loads inflate a recurring bill.
- **ELT keeps raw data, which is a feature** — a transformation bug is re-runnable. Don't discard the raw layer to save storage.
- **Don't bypass the platform for freshness.** Calling a source system directly from an agent action loses the unified profile and its governance.
- **Backfills aren't reruns.** A backfill over changed business logic can rewrite history in ways downstream consumers don't expect.

## Related topics

- [Ingestion](../../01-data-cloud/02-ingestion/notes.md) — batch vs streaming vs accelerated, applied
- [Data modeling](../../01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) — the ELT flow, applied
- [Custom agent actions](../../02-salesforce-ai/05-custom-agent-actions/notes.md) — idempotency for agents
- [Insights & segmentation](../../01-data-cloud/05-insights-segmentation/notes.md) — the semantic layer
- [SQL fluency](../01-sql/notes.md) — where ELT transformations get written
