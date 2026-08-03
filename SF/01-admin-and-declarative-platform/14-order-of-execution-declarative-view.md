# Order of Execution — Declarative View

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** The save order as an admin sees it — where each declarative automation fires. The Apex-side view of the same order, plus recursion control, is [02-apex · 07](../02-apex-and-triggers/INDEX.md). **These two notes must not drift.**

## Core idea

One record save is a fixed pipeline, not a set of independent automations. Knowing the order answers most "why did my automation see the wrong value?" questions outright: anything reading a value produced later in the pipeline reads a stale one. Two facts do the most work. First, the record is written to the database at step 7 but **not committed until step 19** — everything between them is inside the same transaction and can still roll back. Second, roll-up summaries and criteria-based sharing recalculate near the *end*, long after triggers have run.

## How it works

| # | What fires | Note |
|---|---|---|
| 1 | Load original record, or initialise for upsert | |
| 2 | Load new field values, run system validation | |
| 3 | **Before-save record-triggered flows** | cheapest place to set a field |
| 4 | All **before** triggers | |
| 5 | System validation again + **custom validation rules** | |
| 6 | **Duplicate rules** | |
| 7 | **Record saved to the database** | not committed |
| 8 | All **after** triggers | |
| 9 | **Assignment rules** | |
| 10 | **Auto-response rules** | |
| 11 | *Workflow rules* | **out of support** — but still executes if any exist |
| 12 | **Escalation rules** | business-hours aware |
| 13 | *Process Builder & workflow-launched flows* | **out of support** — but still executes if any exist |
| 14 | **After-save record-triggered flows** | |
| 15 | **Entitlement rules** | |
| 16 | **Roll-up summaries — parent** | |
| 17 | **Roll-up summaries — grandparent** | |
| 18 | **Criteria-based sharing** evaluation | |
| 19 | **Commit** all DML | |
| 20 | **Post-commit logic** | email, async jobs, async flow paths |

- Steps 11 and 13 are **not vestigial.** Workflow Rules and Process Builder went **out of support on 31 December 2025 but were not retired**, so in an org that never migrated these slots still execute. You cannot create new ones — creation was blocked in Winter '23 — but you can inherit hundreds. See [CURRENCY.md](../CURRENCY.md).
- A field update at step 11 or 16–17 can **re-enter** the before/after update trigger path, which is why the same trigger appears twice in a debug log.
- Nothing before step 19 is durable. An unhandled exception at step 18 discards the step-7 write.

## 2026 currency

All *new* declarative automation now lands at steps 3 and 14, which is the practical argument for record-triggered Flows: you choose your position in the save order explicitly instead of inheriting whatever slot the old tool occupied. The nuance to hold on to when debugging an inherited org is that steps 11 and 13 can still be live — **end of support is not retirement**, and an unmigrated workflow rule will happily fire between your after-trigger and your after-save flow. → [04-flow · 01](../04-flow-and-automation/01-automation-landscape-and-tool-selection.md); migration mechanics are [04-flow · 18](../04-flow-and-automation/18-migrate-to-flow-and-legacy-retirement.md).

## Gotchas

- **Before-save flow beats every alternative for same-record field defaults** — no extra DML, no re-entry, and it runs before validation so the corrected value is what gets validated.
- An after-trigger reading a **roll-up summary** gets the pre-update value: roll-ups recalculate at 16–17, well after step 8.
- Validation rules at step 5 see values set by before-save flows and before triggers — which is what makes "correct then validate" work.
- **Criteria-based sharing recalculates at step 18**, so any automation checking whether a user *can see* the record is asking too early.
- Post-commit work at step 20 is outside the transaction: an email sent there cannot be unsent by a later rollback.
- Cascade deletes and roll-up-driven parent updates run their **own** save order on the affected records, so one user action can execute this pipeline many times.

## Recall

Q: At which step is the record written to the database, and at which is it committed?
A: Written at step 7, committed at step 19 — everything between is still rollback-able.

Q: Why does an after-trigger see a stale roll-up summary value?
A: Roll-up summaries recalculate at steps 16–17, after all after-triggers at step 8.

Q: Where do validation rules fire relative to before-save flows?
A: After them — flows at step 3, validation at step 5 — so a value corrected by a flow is the value validated.

Q: What happened to the workflow rule and Process Builder steps?
A: Both tools went out of support on 31 December 2025 but were **not retired** — you cannot create new ones, and existing ones still execute at steps 11 and 13. New automation goes to step 3 or 14 as a record-triggered Flow.

Q: Why can the same trigger appear twice in one debug log?
A: A later field update can re-enter the before/after update trigger path within the same save.

## Related

- [02-apex · INDEX](../02-apex-and-triggers/INDEX.md) — the Apex view of this same order, plus recursion control
- [08 · Validation rules & duplicate management](08-validation-rules-and-duplicate-management.md) — steps 5 and 6 in detail
- [07 · Formula fields & roll-up summaries](07-formula-fields-and-roll-up-summaries.md) — why steps 16–17 land where they do
