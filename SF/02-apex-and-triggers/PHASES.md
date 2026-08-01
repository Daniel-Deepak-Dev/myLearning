# Phases for 02 · Apex & Triggers

24 topics across 3 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **The area-wide constraint.** Three defaults flipped at API 67.0 — user mode, `with sharing`, `WITH SECURITY_ENFORCED` retired. Phase 04 owns them, but **every phase must be written as if they are already true.** Never show a code sample that relies on the old defaults without labelling it. Anchor: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

---

## Phase 03 — Apex core, querying & triggers · 9 files ⬜

```
01-apex-language-core-and-governor-limits.md
02-modern-apex-syntax.md                           🆕
03-soql-fundamentals-and-relationship-queries.md
04-advanced-soql-sosl-and-dynamic-queries.md
05-dml-database-methods-and-savepoints.md
06-triggers-and-the-handler-framework.md
07-order-of-execution-and-recursion.md             ⚠️
08-bulkification-patterns.md
09-exception-handling-and-custom-exceptions.md
```

**🆕** — **02**: confirm which syntax additions are GA at 67.0 (`??`, `?.`, switch, safe navigation on collections).

**⚠️** — **07**: the save order now includes **before-save flows** ahead of before triggers. Any ordering list that predates that is wrong.

**Seed harvest** (see [../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md))
- **06** — `Steps to create handler using trigger factory` is substantive but the pattern is ~2013-era `ITrigger`/`TriggerFactory`. **Keep the "Manthras"** (SOQL in bulk phases, DML only in `andFinally()`); **do not present that framework as current.** `Trigger Basics` and `Trigger Context Variable` are stubs — their content is an unexported inline table.
- **05** — `Mixed DML Exception`, `Upsert : DML Operation`, `Database.SaveResult` are usable.
- **03** — `Group By` **contains a self-contradiction about `COUNT()` vs `COUNT(Id)`.** Verify against docs; do not reuse verbatim.
- **04** — `TIPS!: Get Picklist Value` and `Get Dependent Picklist Values` are good schema-describe recipes.

**Watch:** **07** must agree exactly with [01-admin · 14](../01-admin-and-declarative-platform/INDEX.md). Reconcile with whichever landed first.

---

## Phase 04 — Apex security defaults, async & events · 10 files ⬜

**The most currency-sensitive run in the vault.**

```
10-apex-security-user-mode-and-fls.md              🆕⚠️
11-sharing-keywords-and-apex-managed-sharing.md    🆕⚠️
12-async-apex-overview-and-choosing.md
13-queueable-apex-and-chaining.md                  ⚠️
14-batch-apex-and-stateful-processing.md
15-scheduled-apex-and-cron.md
16-transaction-finalizers.md                       (GA Winter '22)
17-database-cursor-and-large-result-sets.md        🆕
18-platform-events-and-cdc-in-apex.md
19-callouts-named-credentials-and-http-in-apex.md  ⚠️
```

**⚠️ corrections to lead with**
- **10** — SOQL/SOSL/DML default to **user mode** at 67.0. `WITH SECURITY_ENFORCED` **no longer compiles**; `WITH USER_MODE` replaces it and is materially better (handles polymorphic fields, checks the `WHERE` clause, reports every FLS violation not just the first).
- **11** — a class with **no sharing keyword now defaults to `with sharing`**. It used to inherit the caller's context, which silently skipped sharing at entry points. Triggers always run in system mode and can no longer declare sharing or access modes.
- **13** — `@future` is legacy. Queueable is the default async choice; cover delay, depth limits, `allowCallouts`.
- **19** — hardcoded endpoints and the legacy Named Credential model are both wrong now.

**🆕** — **17** `Database.Cursor`: research the actual limits and how it differs from `QueryLocator` before writing.

**Seed harvest**
- **14** — `Batch For Loop - maintains heap size` is the **best gotcha in the whole corpus**: measured heap 1050→20000 vs 1050→1200 for 450 records. Harvest it as a `> **From my notes.**` callout.
- **10** — the old `WITH SECURITY_ENFORCED` page is now **actively wrong**. Good raw material for the "what changed" framing.
- **13** — `Future vs Queueable` is a stub; its comparison table doesn't export.

---

## Phase 05 — Apex closeout + LWC entry · 10 files ⬜

Closes Apex, opens [03-lwc-and-slds](../03-lwc-and-slds/INDEX.md). See that area's [PHASES.md](../03-lwc-and-slds/PHASES.md) for the LWC half.

```
20-apex-testing-fundamentals.md                    ⚠️
21-apex-testing-advanced-and-mocking.md
22-invocable-apex-and-agentforce-actions.md        🆕
23-userdefinedtype-and-typed-interop.md            🆕
24-apex-performance-and-profiling.md
--- then in ../03-lwc-and-slds/ ---
01-component-model-and-lifecycle.md
02-templates-directives-and-rendering.md           ⚠️
03-composition-slots-and-dynamic-components.md
04-events-and-component-communication.md
05-decorators-and-the-reactivity-model.md
```

**⚠️** — **20**: `SeeAllData=true` is not a workaround, it's a defect. Lead with that.

**🆕** — **22**: the `@InvocableMethod` contract changed at 67.0 — input classes need a **visible no-arg constructor**. Cross-check against [AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md), which already documents this. **23** `UserDefinedType` — research current support surface.

**Seed harvest** — **20**: `Test Annotations` is the richest page in the corpus (~450 words). Real gotchas worth keeping: the `SeeAllData` + `@TestSetup` conflict, and "DML limits are reset by testSetup but SOQL limits are not." Note only 4 of its 12 planned sections were ever written.
