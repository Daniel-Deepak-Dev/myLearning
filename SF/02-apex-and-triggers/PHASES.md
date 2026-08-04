# Phases for 02 · Apex & Triggers

26 topics across 4 runs — **phases 03–05 and 20 complete, the area is done.** Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

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

**🆕** — **17** ~~`Database.Cursor`: research the actual limits and how it differs from `QueryLocator` before writing.~~ **Researched during phase 04, and the framing in the plan was wrong twice over.** Cursors are not a Summer '26 feature — they appeared at **Summer '24 (API 61.0)**, so 🆕 holds only in the flag legend's 2024–2026 sense. *(**Phase 22 corrected this line.** Phase 04 wrote "GA and have been since Summer '24". Summer '24 was **Beta**; **GA is Spring '26, API 66.0**. See the phase-22 section and [../CURRENCY.md](../CURRENCY.md).)* More importantly, **a cursor is not a row-limit escape hatch**: `Cursor.fetch()` costs a SOQL query and the rows it returns count against the query row limit, so 50,000 rows per transaction still applies. What a cursor actually buys is **heap** and **resumability** — the handle survives into the next transaction (2-day lifetime), which makes it the Queueable-chain counterpart to a batch `QueryLocator`. Real numbers now in the note: 50 M rows per cursor, 100 `fetch()` calls per transaction shared across cursor types, 10,000 cursors / 200,000 pagination cursors per org per 24 h, and two exception types where only `TransientCursorException` is retryable. The `PaginationCursor` / `Database.CursorFetchResult` variant was a genuine discovery and is covered.

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

## Phase 05 — Apex closeout + LWC entry · 10 files ✅

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

**⚠️** — **20**: held, and it is sharper than the plan knew. `SeeAllData=true` is not merely bad practice — it **silently disables `@TestSetup`**, because setup methods are supported only in the default isolation mode. So the annotation removes your data factory rather than erroring, which is why the tests it breaks look unrelated to it.

**🆕 — both premises wrong, in different ways.** **22**: ~~the contract changed at 67.0.~~ The no-arg constructor requirement starts at **API 66.0** (Spring '26) — Summer '26 is only when the *Release Update* auto-activates. Salesforce's own release-note ID ends `_v66`, and **our `AI_Data/` notes had it wrong in seven files**; phase 05 corrected them. `public` outside a managed package, **`global`** cross-package. The mechanism is ordinary OO meeting a platform assumption: **declaring any constructor with arguments removes the compiler-generated default one**, and the platform stopped guessing what to pass — so it fails at runtime in Flow or an agent action, never at compile time. Also added: invocable actions gained **custom property editors, definable picklists and custom headers**, GA at 67.0. · **23**: ~~research the `UserDefinedType` support surface.~~ **There is no such interface, and there never was.** The name reads like `Comparable` or `Callable`; "user-defined type" is the *Apex docs' own phrase* for a plain class used as an invocable payload — *"a list of a user-defined type, containing variables of the supported types."* Rebuilt around the three unrelated mechanisms that actually carry typed payloads: **`@InvocableVariable`** (Flow and agent actions), **`@AuraEnabled` Apex-Defined Types** (Flow variables and LWC), **`equals`/`hashCode`** (map keys and sets). A class often needs two of the three and neither annotation implies the other. **Filename kept deliberately** — the wrong name is what a reader will search for.

**Seed harvest** · *one of two harvested; **21** is link-only, confirmed dead, and carries no callout*
- **20** — `Test Annotations`, the richest page in the corpus (~450 words). **The `SeeAllData` + `@TestSetup` conflict is right and became part of the ⚠️ opener.** The second claim — *"DML limits are reset by testSetup but SOQL limits are not"* — is **inverted, and it became the callout**. Neither is reset: everything a setup method consumes counts against **every** test method in the class. The only reset is `Test.startTest()`/`stopTest()`, and it works *inside* the setup method. Corroborated by three independent sources including a standing Salesforce Idea to remove the behaviour; the Apex docs do not state it either way, which is presumably how the myth survives.

**Other corrections made while writing**
- **The Stub API's restriction list is the story, not the API.** No static (incl. `@future`) or private methods, **no properties — getters and setters both**, no triggers, inner classes, system types, `Batchable` classes, private-constructor-only classes, or iterators as parameter/return types; and the stub must share the caller's namespace. Those exclude most utility classes, so stubbing is a **design** constraint: interface or `virtual`, injected not instantiated inline. Dispatch is on the method name **as a `String`**, so a rename leaves the stub compiling and silently returning `null`.
- **Two testing features the plan missed.** **Apex Integration Tests** — Developer Preview at 67.0, and narrower than the name: the feature is *for **Agentforce and Data 360 Services***, scratch orgs only via the `ApexIntegrationTests` feature (`@IntegrationTest`, `IntegrationTest.commitTestOnly()`, `@TearDown`). **`RunRelevantTests`** — Beta from Spring '26, steered by `@IsTest(testFor=…)` and overridden by `@IsTest(critical=true)`; Unified Logic Testing (Beta) runs Apex and Flow tests in one request, which matters because **22** is the seam between them.
- **Three small facts that earned their place.** `System.runAs` **costs one DML statement per call** — easy to hit in a loop over test users. **No coverage is calculated for a non-test method called from `@TestSetup`**, so building data through your own service layer looks like it covers that layer and does not. The `Assert` class is **Winter '23 (API 56.0)** and `System.assertEquals` is **not** deprecated with no announced retirement — "the old methods are dead" is a common overstatement.

---

## Phase 20 — Platform Cache & event testing · 2 files ✅

**The area was marked done at 24 topics and had two holes in it.** Both were found by grepping the finished vault rather than by working through a plan — the first maintenance run in the build.

```
25-platform-cache.md
26-testing-platform-events-and-cdc.md
```

**Appended, not renumbered.** Area 02 is named by number from at least four other areas, so 25–26 went on the end. See the master [../PHASES.md](../PHASES.md) for the standing position on this.

**25 — no `## 2026 currency` section, deliberately.** Research found nothing about Platform Cache that changed in the 2024–2026 window; the template's own instruction is to delete the heading rather than pad it, and this is the first note in the vault to take that option. The facts that carry the note are old and stable: **LRU eviction on partition fill**, TTL ceilings of **8 h session / 48 h org** (org defaults to 24 h), **100 KB per item**, **50-character keys**, and capacity of **EE 10 MB · UE/Performance 30 MB · Developer 0 until trial · Professional none**. What makes it worth a topic is the design consequence, which most write-ups bury: **a cache miss is the normal path, not an error branch** — Salesforce's own wording is *"Ensure that your code handles cache misses by testing cache requests that return null."*

**Two things 25 says that the internet mostly does not.** Cache **enforces neither FLS nor sharing on read**, so what you cache is what any later caller gets — cache the computed answer, not raw record data. And **custom settings and custom metadata are already in an application cache**, so config is the wrong thing to reach for Platform Cache with; callout responses and expensive aggregates are the right thing.

**26 exists because an event subscriber can be entirely broken and still show green.** Publishing inside a test does not run the subscriber — the message sits on a test-context bus until `Test.getEventBus().deliver()` or `Test.stopTest()`. A test that asserts on the `SaveResult` alone proves the bus accepted a message and nothing more. Specifics that earned their place: `deliver()` delivers **only what was published since the last `deliver()` call**, which is what makes stepping through a retry sequence possible; `Test.enableChangeDataCapture()` must be **the first statement, before any DML**; `EventBusSubscriber.Retries` counts attempts while **`Position` does not advance** on a `RetryableException`; and test context delivers **at most 500** change event messages.

**One 67.0 discovery that reached three files.** **Parallel subscriptions for Apex platform event triggers are GA at Summer '26** — up to **10 internal partitions** via `PlatformEventSubscriberConfig`, keyed on a required custom field or the standard `EventUuid`, for **custom high-volume platform events only** (not standard events, not change events). The testing consequence is the reason it is in 26 as well as [06-integration · 27](../06-integration-and-apis/27-event-bus-allocations-limits-and-monitoring.md): **order holds within a partition and not across them**, so a test asserting that one event's effect precedes another's asserts something a partitioned production subscriber no longer guarantees. Neither 18 nor 04-flow · 07 knew this feature existed.

---

## Phase 21 — Architecture, serialization & iteration · 4 files ✅

**The second maintenance run, and the first driven by a coverage question rather than a currency one.** The area was marked done at 26 topics. Auditing it against a standard advanced-Apex surface — rather than against the release notes — found four holes, each confirmed by grepping the whole vault for zero hits, not merely area 02.

```
27-apex-enterprise-patterns-and-layered-design.md
28-dependency-injection-and-pluggable-apex.md
29-json-serialization-and-untyped-data.md
30-custom-iterators-and-iterables.md
```

**Appended, not renumbered** — the phase-20 position, unchanged. 27–28 belong pedagogically right after [06](06-triggers-and-the-handler-framework.md), and putting them there would have rewritten inbound links from four other areas to buy reading order.

**The gap 06 left open for three phases.** [06](06-triggers-and-the-handler-framework.md) retires the ~2013 `ITrigger`/`TriggerFactory` pattern with the right argument — *"keep the discipline, drop the framework"* — and then names nothing above handler-class level. That was defensible while the area stopped at one handler per object and indefensible for an architect track. **27** supplies the replacement and **28** supplies the reason it is testable rather than merely tidy.

**27 — the fflib framing is the part most write-ups get wrong.** It is **community-maintained open source in the `apex-enterprise-patterns` GitHub org**, originally FinancialForce's Apex Commons. Salesforce promotes the *patterns* and ships, supports and versions **none** of the code — so adopting it is taking on an unsupported dependency, and a hand-rolled Selector and Unit of Work are entirely legitimate. The note keeps the pattern as the durable content and the library as one implementation.

**A 67.0 consequence nobody has written up.** fflib Selectors carry `enforceFLS` / `enforceCRUD` toggles, and every pre-2026 tutorial turns them **on** — correctly, because Apex ran system-mode by default. **At 67.0 that inverts.** User mode is the default, so a Selector's notable case is now deliberate elevation to `AccessLevel.SYSTEM_MODE`, and a base class carrying an unexamined "enforce security" flag inherited from a 2019 fork is the *surprising* path rather than the safe one. This is the same shape as the phase-04 finding about batch `QueryLocator`: the flip reaches library code that predates it, and it fails quietly.

**28 exists because of a sentence already in [21](21-apex-testing-advanced-and-mocking.md).** The Stub API cannot touch static or private methods, properties, inner classes, `Batchable` implementations or private-constructor-only classes. Phase 05 recorded that and drew the right conclusion in half a clause — *"injected rather than instantiated inline"* — then never wrote the note. **Injection is not a style preference in Apex; it is the precondition for the Stub API being usable at all.** Three specifics that earned their place: `Type.forName()` **returns `null` rather than throwing**, so the failure lands on the following line; it is **namespace-sensitive**, needing the two-argument form in a managed package; and `newInstance()` requires a visible no-arg constructor — **the same rule, from the same cause, as the API 66.0 invocable constructor requirement** in [22](22-invocable-apex-and-agentforce-actions.md).

**29 ships with no `## 2026 currency` section — and this time it was checked, not assumed.** The brief specifically asked whether JSON serialization had gained anything recently. Verified against the `System.JSON` class reference at 67.0 (nine methods, **no version badges and no new markers**) and the Summer '26 developer release guide, whose Apex changes are the security flip, multiline strings, `String.template()`, `@IntegrationTest` and triggers-always-system-mode — **none of them JSON**. So: nothing about JSON or Apex serialization changed in the 2024–2026 window, and the heading was deleted per the template's own instruction. **30 took the same option**, for `Iterator`/`Iterable`, which have been stable far longer — so 29 and 30 are the second and third notes in the vault to delete the heading, after [25](25-platform-cache.md). **Recording the negative result matters more than the notes do** — the next person to ask gets an answer with a date on it instead of repeating the search. Worth noticing that three of the four notes this run needed no currency section: **a coverage gap and a currency gap are different defects**, and the topics an area forgets tend to be the stable ones precisely because no release note ever forced anyone to look at them.

**Two genuine Apex additions found while checking, and deliberately not written.** **`Compression`** (zip generate/extract) and **`FormulaEval`** (evaluate dynamic formulas in Apex) both went **GA in Spring '25 (API 63.0)** after a Spring '24 Developer Preview — inside the 🆕 window, and **absent from the entire vault**. Out of scope for this run's brief; logged here so the next audit does not have to rediscover them. Note the trap encountered on the way: a search result attributed both to Summer '26, sourced from a release-notes URL pinned to an older release. **A release-notes page reached without checking its `release=` parameter is not evidence.**

**30 — the correction is a scale claim.** `Database.Batchable.start()` accepting an `Iterable` is routinely presented as the flexible alternative to `QueryLocator`. It is, and it costs three orders of magnitude: **`QueryLocator` supports 50 million records, the `Iterable` path is bounded by the ordinary 50,000-row query limit**, because the collection is assembled in a normal transaction. Reach for it when the scope is not queryable, never to handle more data. The other trap is silent: **a class implementing both interfaces and returning `this` from `iterator()` is single-use** — the second loop resumes from the exhausted position and runs zero times, with no exception.
