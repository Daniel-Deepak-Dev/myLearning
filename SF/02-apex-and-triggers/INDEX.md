# 02 · Apex & Triggers

Expert Apex, including the **API 67.0 security rewrite that invalidates most published examples**. **30 topics** · phases [03](PHASES.md), [04](PHASES.md), [05](PHASES.md), [20](PHASES.md), [21](PHASES.md) — **area complete ✅**.

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three defaults flipped at 67.0** and they touch nearly every note in this area: SOQL/DML default to **user mode**; a keyword-less class defaults to **`with sharing`**; **`WITH SECURITY_ENFORCED` no longer compiles**. The anchor for all three is [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md) — notes here must not contradict it.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Apex language core & governor limits](01-apex-language-core-and-governor-limits.md) | types, collections, per-transaction limit map (SOSL is **20**, not 50) | 03 |
| 02 | [Modern Apex syntax](02-modern-apex-syntax.md) 🆕 | multiline `'''` + `String.template()` are the 67.0 additions; `??`/`?.`/switch are older | 03 |
| 03 | [SOQL in Apex](03-soql-fundamentals-and-relationship-queries.md) | binding, the `for` loop's flat heap, the governor budget, `AggregateResult` — **language is [10-soql](../10-soql-and-sosl/INDEX.md)** | 03 |
| 04 | [Dynamic SOQL, SOSL & describe in Apex](04-advanced-soql-sosl-and-dynamic-queries.md) | `queryWithBinds` + `AccessLevel`, `Search.find()`, describe & the `validFor` bitmap | 03 |
| 05 | [DML, Database methods & savepoints](05-dml-database-methods-and-savepoints.md) | allOrNone, SaveResult handling, savepoints cost DML and don't reset limits | 03 |
| 06 | [Triggers & the handler framework](06-triggers-and-the-handler-framework.md) | one trigger per object, `operationType` dispatch, always system mode at 67.0 | 03 |
| 07 | [Order of execution & recursion](07-order-of-execution-and-recursion.md) ⚠️ | the Apex slice of the save order; per-record guards, not `hasRun` | 03 |
| 08 | [Bulkification patterns](08-bulkification-patterns.md) | maps/sets, no SOQL-DML in loops, 200-record chunks | 03 |
| 09 | [Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) | catch scope, `addError` vs `throw`, partial-success design | 03 |
| 10 | [Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) 🆕⚠️ | user mode is the 67.0 default; `WITH SECURITY_ENFORCED` retired | 04 |
| 11 | [Sharing keywords & Apex managed sharing](11-sharing-keywords-and-apex-managed-sharing.md) 🆕⚠️ | keyword-less classes now `with sharing`; triggers always system mode | 04 |
| 12 | [Async Apex overview & choosing](12-async-apex-overview-and-choosing.md) | future vs queueable vs batch vs events; elastic async limits are **Beta** | 04 |
| 13 | [Queueable Apex & chaining](13-queueable-apex-and-chaining.md) ⚠️ | replaces `@future`; delay, stack depth, `DuplicateSignature`, allowCallouts | 04 |
| 14 | [Batch Apex & stateful processing](14-batch-apex-and-stateful-processing.md) | scope sizing, `Database.Stateful` (instance members **only**), failure isolation | 04 |
| 15 | [Scheduled Apex & CRON](15-scheduled-apex-and-cron.md) | Schedulable, 7-field CRON, the deployment lock on pending jobs | 04 |
| 16 | [Transaction Finalizers](16-transaction-finalizers.md) *(GA Winter '22)* | post-Queueable hook; the only code that survives an uncatchable failure | 04 |
| 17 | [`Database.Cursor` & large result sets](17-database-cursor-and-large-result-sets.md) 🆕 | Beta Summer '24, **GA Spring '26 (66.0)**; `fetch()` **costs a query** — saves heap, not rows | 04 |
| 18 | [Platform Events & CDC in Apex](18-platform-events-and-cdc-in-apex.md) | publish behaviours, event triggers, 10 runs then the subscriber dies | 04 |
| 19 | [Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) ⚠️ | callout limits, external + named credential split, no hardcoded endpoints | 04 |
| 20 | [Apex testing fundamentals](20-apex-testing-fundamentals.md) ⚠️ | `@TestSetup` does **not** reset limits; `SeeAllData=true` disables it outright | 05 |
| 21 | [Apex testing advanced & mocking](21-apex-testing-advanced-and-mocking.md) | HttpCalloutMock, Stub API and the long list of what it **can't** stub | 05 |
| 22 | [Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) 🆕 | `@InvocableMethod` contract; no-arg constructor from **66.0**, enforced Summer '26 | 05 |
| 23 | [`UserDefinedType` & typed interop](23-userdefinedtype-and-typed-interop.md) 🆕 | **no such interface exists** — ADTs, `@InvocableVariable`, `equals`/`hashCode` | 05 |
| 24 | [Apex performance & profiling](24-apex-performance-and-profiling.md) | CPU and heap are the two that bite; `Limits` deltas over whole-log reading | 05 |
| 25 | [Platform Cache](25-platform-cache.md) | `Cache.Org`/`Cache.Session`, `CacheBuilder`, LRU eviction — **a miss is the normal path** | 20 |
| 26 | [Testing platform events & CDC](26-testing-platform-events-and-cdc.md) | `Test.getEventBus().deliver()`, `Test.enableChangeDataCapture()`; an undelivered subscriber passes green | 20 |
| 27 | [Apex Enterprise Patterns & layered design](27-apex-enterprise-patterns-and-layered-design.md) | Selector/Domain/Service/UoW; **fflib is community code, not a Salesforce product** | 21 |
| 28 | [Dependency injection & pluggable Apex](28-dependency-injection-and-pluggable-apex.md) | constructor injection, `Type.forName()`, CMDT binding — **the Stub API's precondition** | 21 |
| 29 | [JSON, serialization & untyped data](29-json-serialization-and-untyped-data.md) | reserved-word fields force `deserializeUntyped`; strict vs lenient; streaming | 21 |
| 30 | [Custom iterators & iterables](30-custom-iterators-and-iterables.md) | `hasNext()`/`next()`; the Batch `Iterable` path caps at **50 K, not 50 M** | 21 |

## Related

- **03–04 were narrowed in phase 22 and are no longer the vault's SOQL reference.** [10-soql-and-sosl](../10-soql-and-sosl/INDEX.md) owns the query language; these two keep the Apex-specific surface — binding, the `for` loop's heap behaviour, the governor budget, `Database.queryWithBinds` + `AccessLevel`, `Search.find()` and schema describe. Filenames were kept deliberately, as with [23](23-userdefinedtype-and-typed-interop.md): eleven files link to them by name.
- **07** is the code-side twin of [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md). **That note landed first in phase 01 and is the reference** — 07 carries only the Apex slice of the save order and links across for the full twenty steps, rather than keeping a second copy that can drift.
- **01–09 were written before phase 04 owns the security defaults**, so they state the 67.0 position without explaining it. The explanation is [10](10-apex-security-user-mode-and-fls.md) and [11](11-sharing-keywords-and-apex-managed-sharing.md).
- **10–11** are the Apex projection of [07-security-and-sharing](../07-security-and-sharing/INDEX.md) — read together.
- **17 is not a row-limit escape hatch.** `Database.Cursor.fetch()` costs a SOQL query and its rows count against the row limit; the win is heap and resumability. Reach for [14](14-batch-apex-and-stateful-processing.md) when you need 50 M rows chunked for you.
- **19** continues in [06-integration-and-apis · 17 Named credentials](../06-integration-and-apis/17-named-credentials-and-external-credentials.md).
- **22–23** are the bridge into [AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) — that note owns the *agent* side (description writing, action selection, MCP exposure); **22** owns the Apex contract. The no-arg constructor rule is **API 66.0**, auto-enforced by a Summer '26 Release Update — phase 05 corrected that version across `AI_Data/`.
- **23 is not about an interface.** `UserDefinedType` is the Apex docs' phrase for a plain class used as a typed payload; nothing implements it. The real surfaces are `@InvocableVariable`, `@AuraEnabled` Apex-Defined Types, and `equals`/`hashCode`.
- **20–21 are where the security flip stops being theoretical.** User mode means the identity a test runs under decides the result, so `System.runAs` moved from optional to necessary. → [10](10-apex-security-user-mode-and-fls.md)
- **27–28 are the layer above [06](06-triggers-and-the-handler-framework.md), and they are one argument in two notes.** 06 retires the ~2013 `ITrigger`/`TriggerFactory` scaffolding without naming a replacement; **27** is the replacement (Selector/Domain/Service/Unit of Work) and **28** is why it is testable rather than merely tidy. Read 28 against [21](21-apex-testing-advanced-and-mocking.md) — the Stub API's restriction list is what turns injection from a preference into a precondition.
- **29 and 30 deliberately have no `## 2026 currency` section.** For **29** this was checked rather than assumed: the `System.JSON` class reference at 67.0 lists nine methods with no version badges, and the Summer '26 Apex changes are the security flip, multiline strings, `String.template()`, `@IntegrationTest` and triggers-always-system-mode — **nothing about JSON or Apex serialization changed in the 2024–2026 window.** **30** is the same story for `Iterator`/`Iterable`, which have been stable far longer. They are the second and third notes in the vault to take the template's delete-the-heading option, after [25](25-platform-cache.md).
