# Phases for 02 · Apex & Triggers

24 topics across 3 runs — **phases 03–04 complete**, 19 of 24 written. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **The area-wide constraint.** Three defaults flipped at API 67.0 — user mode, `with sharing`, `WITH SECURITY_ENFORCED` retired. Phase 04 owns them, but **every phase must be written as if they are already true.** Never show a code sample that relies on the old defaults without labelling it. Anchor: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

---

## Phase 03 — Apex core, querying & triggers · 9 files ✅

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

**🆕** — **02**: ~~confirm which syntax additions are GA at 67.0 (`??`, `?.`, switch, safe navigation on collections).~~ **Researched during phase 03: the premise was wrong.** None of those are new — `switch on` is Summer '18 (43.0), `?.` is Winter '21 (50.0), `??` is Spring '24 (60.0). **The actual 67.0 syntax additions are multiline strings (`'''`) and `String.template()`**, both GA, and the file was rebuilt around them. Two details that do not survive a casual read: the newline after the opening `'''` is trimmed, and `.template()` renders a `Datetime` in **GMT**, not the user's locale.

**⚠️** — **07**: held. The save order does put **before-save flows** at step 3, ahead of before triggers.

**Seed harvest** (see [../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) · *all four harvested; three became `From my notes.` callouts*
- **06** — `Steps to create handler using trigger factory` is substantive but the pattern is ~2013-era `ITrigger`/`TriggerFactory`. **Keep the "Manthras"** (SOQL in bulk phases, DML only in `andFinally()`); **do not present that framework as current.** `Trigger Basics` and `Trigger Context Variable` are stubs — their content is an unexported inline table. → *done: Manthras kept as a callout, framework named as superseded by `Trigger.operationType` + `switch`.*
- **05** — `Mixed DML Exception`, `Upsert : DML Operation`, `Database.SaveResult` are usable. → *all three used. The callout went to `Savepoint and Rollback in Apex` instead: **a savepoint costs one DML statement and the rollback costs another**, and neither returns budget already spent. Mixed DML is a gotcha.*
- **03** — `Group By` **contains a self-contradiction about `COUNT()` vs `COUNT(Id)`.** Verify against docs; do not reuse verbatim. → *verified. **The note's rule is right and its example is wrong.** `COUNT()` has been invalid with `GROUP BY` since API 19.0 and must be the only element in the `SELECT` list, so its own `select count() from case group by status` does not run. Quoted with the correction inline.*
- **04** — `TIPS!: Get Picklist Value` and `Get Dependent Picklist Values` are good schema-describe recipes. → *the `validFor` base64 bitmap became the callout; still the only way to read a picklist dependency from Apex, still undocumented.*

**Watch:** ~~**07** must agree exactly with [01-admin · 14](../01-admin-and-declarative-platform/INDEX.md). Reconcile with whichever landed first.~~ **Resolved: [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) landed first and is the reference.** 07 therefore carries only the Apex-participating steps and links across for the canonical twenty — one table, not two that can drift.

**Other corrections made while writing**
- The plan's limit figure of "50 SOSL" was wrong. **SOSL is 20 queries and 2,000 rows per transaction**; the INDEX scope cell for 01 was fixed to say so.
- `Database.queryWithBinds` (Spring '23) takes `AccessLevel` as its third argument and defaults to user mode at 67.0 — it belongs in **04**, not deferred to phase 04's security files.

---

## Phase 04 — Apex security defaults, async & events · 10 files ✅

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

**🆕** — **17** ~~`Database.Cursor`: research the actual limits and how it differs from `QueryLocator` before writing.~~ **Researched during phase 04, and the framing in the plan was wrong twice over.** Cursors are not a Summer '26 feature — they are **GA and have been since Summer '24 (API 61.0)**, so 🆕 holds only in the flag legend's 2024–2026 sense. More importantly, **a cursor is not a row-limit escape hatch**: `Cursor.fetch()` costs a SOQL query and the rows it returns count against the query row limit, so 50,000 rows per transaction still applies. What a cursor actually buys is **heap** and **resumability** — the handle survives into the next transaction (2-day lifetime), which makes it the Queueable-chain counterpart to a batch `QueryLocator`. Real numbers now in the note: 50 M rows per cursor, 100 `fetch()` calls per transaction shared across cursor types, 10,000 cursors / 200,000 pagination cursors per org per 24 h, and two exception types where only `TransientCursorException` is retryable. The `PaginationCursor` / `Database.CursorFetchResult` variant was a genuine discovery and is covered.

**Seed harvest** · *two of three harvested; the third was a dead embed as predicted*
- **14** — `Batch For Loop - maintains heap size` is the **best gotcha in the whole corpus**: measured heap 1050→20000 vs 1050→1200 for 450 records. Harvest it as a `> **From my notes.**` callout. → *done, with one qualification added: inside a batch `execute()` the scope list is already bounded, so the SOQL-for-loop trick applies to any **additional** query in that method, not to the scope itself.*
- **10** — the old `WITH SECURITY_ENFORCED` page is now **actively wrong**. Good raw material for the "what changed" framing. → *used as the callout. The note claimed the clause "handled FLS"; it never checked the `WHERE` clause, never resolved polymorphic fields, and threw on the first violation only — so it was wrong before it stopped compiling.*
- **13** — `Future vs Queueable` is a stub; its comparison table doesn't export. → *confirmed dead. The comparison table in 13 was rebuilt from the current docs; **13 carries no `From my notes.` callout.***
- **11** — *unplanned harvest.* `UserRecordAccess Query Problem` turned out to be substantive and became 11's callout: the query **must** filter on `RecordId`, `RecordId IN` is capped at **200** records so it does not bulkify like ordinary SOQL, and `HasEditAccess` answers a sharing question only — it can be `true` for a user with no Edit permission on the object.
- **19** — *unplanned harvest.* `Can We Perform Callout After DML Operation?` became 19's callout. Its answer ("use `@future`") is superseded by a `Queueable implements Database.AllowsCallouts`, and the better fix is usually to reorder so the callout runs *before* the DML.

**Other corrections made while writing**
- **The plan's "queueable delay, depth limits" line understated the surface.** `AsyncOptions` carries three things, not one: `MinimumQueueableDelayInMinutes`, `MaximumQueueableStackDepth` and `DuplicateSignature`. Duplicate suppression (`QueueableDuplicateSignature.Builder` → `DuplicateMessageException`) is the most useful of the three and was missing from the plan entirely.
- **Chain depth is capped at 5 in Developer and Trial orgs only** — production has no documented ceiling. That inverts the usual testing story: a runaway chain fails safely in the sandbox and burns the daily async limit in production.
- **Finalizers can make callouts**, which the phase plan did not anticipate, and they run under *synchronous* limits with three exceptions (heap, max enqueued jobs, `@future` limits) that use the async caps.
- **Platform event subscribers fail dead, not loud.** Ten runs — one attempt plus nine retries — then the trigger enters an error state and stops processing **new** events until the class is fixed and saved. 18 was written around that rather than around the retry mechanics.
- **Elastic async limits (Beta at 67.0) change a failure mode, not just a number.** A runaway Queueable chain used to stop with a `LimitException`; throttled overflow means it now just slows down. Called out in 12, 13 and 16.
- **Batch is not exempt from the security flip.** A `QueryLocator` built in `start()` defaults to user mode, so an old nightly job processes a *subset* and still reports success. This is in 14's currency section and is the most likely real-world 67.0 regression in the run.

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
