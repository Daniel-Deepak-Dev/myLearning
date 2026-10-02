---
area: Core
topic: Apex Terminology
id_prefix: core-apex-term
---
# Core › Apex Terminology

The Apex vocabulary, one term per card, as of Summer '26 (API 67.0), the release the linked notes were checked against. Each answer gives two things: what the term **means**, and what it is **used for**. Read it out loud as one sentence each.

Foundations is the glossary. Hard is the terms people mix up in a design review, each with the trap. The scenarios live in [apex.md](apex.md), and this deck leaves out the limits and facts already carded there. Format and rules are in the README one folder up.

## Foundations

#flashcards/core/apex-terminology/foundations

### Limits & language

**Governor limit** — what is it, and what is it for? <!--id:core-apex-term-001-->
?
**Means:** a per-transaction ceiling the multitenant runtime enforces on Apex, such as 100 SOQL queries. Crossing one throws `LimitException`.
**Used for:** protecting the other tenants on the same servers. It is a runtime contract, not performance advice, so most Apex design is about where the transaction boundary goes.
Source: [Apex Language Core & Governor Limits](../../SF_core/02-apex-and-triggers/01-apex-language-core-and-governor-limits.md) · [Glossary](../../GLOSSARY.md)

**Transaction** — what is it in Apex, and why does it matter? <!--id:core-apex-term-002-->
?
**Means:** one synchronous execution context: a record save with all its triggers, one controller action, one Queueable, or one batch `execute()`.
**Used for:** counting governor limits and scoping static variables. Everything inside shares one budget, and the budget resets at the boundary.
Source: [Apex Language Core & Governor Limits](../../SF_core/02-apex-and-triggers/01-apex-language-core-and-governor-limits.md)

**`LimitException`** — what is it, and how do you deal with it? <!--id:core-apex-term-003-->
?
**Means:** the exception thrown when a governor limit is crossed. No `catch` clause in the language can stop it.
**Used for:** nothing you can catch. The defence is checking the `Limits` class before the work, or a Transaction Finalizer that runs after a Queueable dies.
Source: [Exception Handling & Custom Exceptions](../../SF_core/02-apex-and-triggers/09-exception-handling-and-custom-exceptions.md) · [Transaction Finalizers](../../SF_core/02-apex-and-triggers/16-transaction-finalizers.md)

**`Limits` class** — what is it, and what is it for? <!--id:core-apex-term-004-->
?
**Means:** methods that read the current transaction's usage and ceiling as pairs, such as `Limits.getQueries()` and `Limits.getLimitQueries()`, or `getCpuTime()` and `getHeapSize()`.
**Used for:** degrading before a limit (defer the rest to async) and attributing cost by logging deltas around a block. `System.OrgLimits.getMap()` answers the daily, org-wide question instead.
Source: [Apex Performance & Profiling](../../SF_core/02-apex-and-triggers/24-apex-performance-and-profiling.md) · [Apex Language Core & Governor Limits](../../SF_core/02-apex-and-triggers/01-apex-language-core-and-governor-limits.md)

**CPU time** — what does it measure, and what does it leave out? <!--id:core-apex-term-005-->
?
**Means:** the time your own code spends executing: loops and collection work. It excludes database time, callout time and DML processing.
**Used for:** telling a slow transaction from an expensive one. A transaction that takes 40 seconds of wall clock can use 300 ms of CPU.
Source: [Apex Performance & Profiling](../../SF_core/02-apex-and-triggers/24-apex-performance-and-profiling.md)

**Heap** — what is it, and what keeps it small? <!--id:core-apex-term-006-->
?
**Means:** the memory a transaction holds, counted on what is still reachable. A list you have finished with keeps its memory until the reference leaves scope.
**Used for:** sizing how much data one transaction can hold. A SOQL `for` loop, streaming JSON and a cursor are the usual ways to keep it flat.
Source: [Apex Performance & Profiling](../../SF_core/02-apex-and-triggers/24-apex-performance-and-profiling.md)

**Safe navigation (`?.`)** — what is it, and where is it not allowed? <!--id:core-apex-term-007-->
?
**Means:** an operator that returns null as soon as any link in a chain is null, instead of throwing. GA Winter '21 (API 50.0).
**Used for:** replacing nested null-check `if` ladders, as in `o.Account?.Owner?.Email`. It won't compile on static member access, `Trigger.new`, assignment targets or SOQL bind variables.
Source: [Modern Apex Syntax](../../SF_core/02-apex-and-triggers/02-modern-apex-syntax.md)

**Null coalescing (`??`)** — what is it, and what is it for? <!--id:core-apex-term-008-->
?
**Means:** `a ?? b` returns `a` unless it is null, then `b`. The left operand is evaluated exactly once. GA Spring '24 (API 60.0).
**Used for:** defaults, without the ternary that evaluated `a` twice. It is not an assignment: Apex has no `??=`.
Source: [Modern Apex Syntax](../../SF_core/02-apex-and-triggers/02-modern-apex-syntax.md)

**`String.template()`** — what is it, and what is it for? <!--id:core-apex-term-009-->
?
**Means:** the Summer '26 (API 67.0) method that fills `${key}` placeholders from a `Map<String, Object>`, usually on a multiline `'''…'''` string.
**Used for:** replacing concatenation in email bodies, request bodies and dynamic SOQL. Keys are only matched at runtime, and a `Datetime` renders in GMT.
Source: [Modern Apex Syntax](../../SF_core/02-apex-and-triggers/02-modern-apex-syntax.md) · [Glossary](../../GLOSSARY.md)

### Queries & DML

**Bind variable** — what is it, and what can't it do? <!--id:core-apex-term-010-->
?
**Means:** an Apex variable used inside inline SOQL with a colon, such as `WHERE AccountId IN :accountIds`.
**Used for:** filtering by values gathered earlier, which is the core of bulkification, and keeping input out of the query text. It can't substitute an object or field name.
Source: [SOQL in Apex](../../SF_core/02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md)

**SOQL `for` loop** — what is it, and what is it for? <!--id:core-apex-term-011-->
?
**Means:** a loop over the query itself, `for (Account a : [SELECT …])`, which pulls records in chunks of 200.
**Used for:** keeping heap flat over a large result set. It saves memory, not budget: the rows still count against 50,000.
Source: [SOQL in Apex](../../SF_core/02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md)

**`AggregateResult`** — what is it, and how do you read it? <!--id:core-apex-term-012-->
?
**Means:** the row type an aggregate query returns instead of sObjects, such as `COUNT(Id)` with `GROUP BY`. Read values with `ar.get('alias')`; unaliased columns come back as `expr0`, `expr1`.
**Used for:** counting children per parent in one query instead of one query per parent. Only the rows it returns count against the 50,000-row limit.
Source: [SOQL in Apex](../../SF_core/02-apex-and-triggers/03-soql-fundamentals-and-relationship-queries.md) · [Bulkification Patterns](../../SF_core/02-apex-and-triggers/08-bulkification-patterns.md)

**`Database.queryWithBinds`** — what is it, and what is it for? <!--id:core-apex-term-013-->
?
**Means:** dynamic SOQL that takes the query, a `Map<String, Object>` of bind values, and an `AccessLevel`. Binds resolve from the map by key, not from Apex variables in scope.
**Used for:** any query built at runtime from input. A bind named in the string but missing from the map throws, naming the key.
Source: [Dynamic SOQL, SOSL & Describe in Apex](../../SF_core/02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md)

**`allOrNone`** — what is it, and when do you set it to false? <!--id:core-apex-term-014-->
?
**Means:** the second argument of the `Database` DML methods. `false` commits the good rows and reports each failure in a `SaveResult[]` instead of throwing.
**Used for:** partial-success loads, such as a 500-row import with an error report. A two-record transfer should stay all-or-nothing. It makes the operation survivable, not safe.
Source: [DML, Database Methods & Savepoints](../../SF_core/02-apex-and-triggers/05-dml-database-methods-and-savepoints.md)

**Savepoint** — what is it, and what does a rollback restore? <!--id:core-apex-term-015-->
?
**Means:** a marker in a transaction that you can roll the data back to. Setting one costs a DML statement, and rolling back costs another.
**Used for:** undoing data after inspecting an outcome. Rollback restores data only: spent limits stay spent and statics keep their values. Rolling back invalidates every later savepoint.
Source: [DML, Database Methods & Savepoints](../../SF_core/02-apex-and-triggers/05-dml-database-methods-and-savepoints.md) · [Glossary](../../GLOSSARY.md)

**Mixed DML** — what is it, and how do you avoid it? <!--id:core-apex-term-016-->
?
**Means:** writing a setup object (`User`, `Group`, `GroupMember`, `PermissionSetAssignment`, `QueueSobject`) and a standard or custom object in the same transaction. It throws.
**Used for:** knowing why the second write has to move into an async context. In tests, `System.runAs()` creates the boundary.
Source: [DML, Database Methods & Savepoints](../../SF_core/02-apex-and-triggers/05-dml-database-methods-and-savepoints.md) · [Glossary](../../GLOSSARY.md)

**`Database.Cursor`** — what is it, and what is it for? <!--id:core-apex-term-017-->
?
**Means:** a server-side handle to a query's results that you page through yourself with `fetch(position, count)`. It can be stored in a Queueable and survives into later transactions.
**Used for:** walking a result set too big for one transaction, in ordinary Apex and without writing a batch class.
Source: [Database.Cursor & Large Result Sets](../../SF_core/02-apex-and-triggers/17-database-cursor-and-large-result-sets.md) · [Glossary](../../GLOSSARY.md)

**`PaginationCursor`** — what is it, and how does it differ from a cursor? <!--id:core-apex-term-018-->
?
**Means:** the object `Database.getPaginationCursor()` returns. `fetchPage(start, pageSize)` gives a `CursorFetchResult` with `getRecords()`, `getDeletedRows()`, `getNextIndex()` and `isDone()`. Capped at 100,000 rows.
**Used for:** UI paging. It skips deleted rows so page sizes stay stable; a standard cursor is for background jobs.
Source: [Database.Cursor & Large Result Sets](../../SF_core/02-apex-and-triggers/17-database-cursor-and-large-result-sets.md)

### Triggers & order of execution

**Trigger handler** — what is it, and why use one? <!--id:core-apex-term-019-->
?
**Means:** the class that holds a trigger's logic. The trigger itself only answers "which context is this?" and hands off.
**Used for:** one trigger per object, logic you can unit-test and call from elsewhere, and a place that can declare sharing. At 67.0 a trigger can't declare a sharing or access mode at all.
Source: [Triggers & the Handler Framework](../../SF_core/02-apex-and-triggers/06-triggers-and-the-handler-framework.md)

**`Trigger.operationType`** — what is it, and what is it for? <!--id:core-apex-term-020-->
?
**Means:** the context of the current trigger run, as a `System.TriggerOperation` enum value: `BEFORE_INSERT`, `AFTER_UPDATE` and so on.
**Used for:** turning the whole trigger body into one `switch on` that calls the handler.
Source: [Triggers & the Handler Framework](../../SF_core/02-apex-and-triggers/06-triggers-and-the-handler-framework.md) · [Glossary](../../GLOSSARY.md)

**`addError()`** — what is it, and what is it for? <!--id:core-apex-term-021-->
?
**Means:** the trigger's veto. Called on a record, it blocks that row with a field-level or record-level message.
**Used for:** rejecting one invalid row while the rest of a partial-success batch commits. In a `before` trigger it prevents the save; in an `after` trigger it rolls back the row already written, which costs more.
Source: [Triggers & the Handler Framework](../../SF_core/02-apex-and-triggers/06-triggers-and-the-handler-framework.md)

**Order of execution** — what is it, and why does it matter to Apex? <!--id:core-apex-term-022-->
?
**Means:** the fixed, documented 20-step pipeline every record save runs through. Apex occupies four of the steps, between declarative automation on both sides.
**Used for:** answering "why did my trigger see the wrong value?". The answer is nearly always that the value is produced later in the pipeline than the code reading it.
Source: [Order of Execution & Recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Order of execution: declarative view](../../SF_core/01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md)

**Recursion guard** — what is it, and what should it actually do? <!--id:core-apex-term-023-->
?
**Means:** static state that stops a trigger redoing work when a save re-enters it. Done right, it is a `static Set<Id>` of the records already processed.
**Used for:** making the second pass cheap and idempotent, not blocking it: re-entry from a flow or roll-up is normal. Trigger stack depth is hard-capped at 16 regardless.
Source: [Order of Execution & Recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Glossary](../../GLOSSARY.md)

**Bulkification** — what is it, and how do you do it? <!--id:core-apex-term-024-->
?
**Means:** writing Apex so the cost of a transaction does not scale with the number of records in it.
**Used for:** surviving the first real data load. Collect keys into a `Set`, query once outside the loop into a `Map<Id, sObject>`, and look up inside it.
Source: [Bulkification Patterns](../../SF_core/02-apex-and-triggers/08-bulkification-patterns.md) · [Glossary](../../GLOSSARY.md)

### Security & sharing

**User mode** — what is it, and what is it for? <!--id:core-apex-term-025-->
?
**Means:** an execution context that enforces the running user's object permissions, field-level security and sharing. The default for SOQL, SOSL and DML in classes compiled at 67.0.
**Used for:** making Apex safe when the caller may be an autonomous agent rather than a filtered UI. Reading a field the user can't see throws a `QueryException`.
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Glossary](../../GLOSSARY.md)

**System mode** — what is it, and when is it right? <!--id:core-apex-term-026-->
?
**Means:** an execution context that ignores the running user's permissions and sharing. Triggers always run in it at 67.0.
**Used for:** deliberate, documented elevation with `AccessLevel.SYSTEM_MODE` or `WITH SYSTEM_MODE`. An unexplained one in a code review is the likeliest place a permission bypass hides.
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Glossary](../../GLOSSARY.md)

**`AccessLevel`** — what is it, and where is it used? <!--id:core-apex-term-027-->
?
**Means:** the enum `AccessLevel.USER_MODE` / `AccessLevel.SYSTEM_MODE`, passed as an argument to `Database.query`, `queryWithBinds`, `getQueryLocator`, cursors and the DML methods.
**Used for:** stating the mode of dynamic SOQL and DML, where the inline `WITH USER_MODE` syntax can't go.
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Glossary](../../GLOSSARY.md)

**`WITH USER_MODE`** — what is it, and what did it replace? <!--id:core-apex-term-028-->
?
**Means:** an inline SOQL clause that enforces CRUD, FLS and sharing across the whole query, and reports every violation at once in one `QueryException`.
**Used for:** replacing `WITH SECURITY_ENFORCED`, which no longer compiles at 67.0 and never checked the `WHERE` clause or polymorphic fields. Worth writing even where it is the default, so the intent survives a version bump.
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Glossary](../../GLOSSARY.md)

**`inherited sharing`** — what is it, and where does it belong? <!--id:core-apex-term-029-->
?
**Means:** a class keyword that takes the caller's sharing context, and falls back to `with sharing` when the class is entered directly.
**Used for:** shared utilities and selectors called both from elevated and from ordinary code.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) · [Glossary](../../GLOSSARY.md)

**Apex managed sharing** — what is it, and what is it for? <!--id:core-apex-term-030-->
?
**Means:** granting record access from code by inserting rows into an object's `__Share` table, with `ParentId`, `UserOrGroupId`, `AccessLevel` (`Read` or `Edit`) and `RowCause`.
**Used for:** access the declarative sharing model can't express, such as access derived from a related record or an external system's answer.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) · [Glossary](../../GLOSSARY.md)

**Apex sharing reason** — what is it, and why does it matter? <!--id:core-apex-term-031-->
?
**Means:** a custom `RowCause` declared on a custom object in Setup, referenced as `Schema.Project__Share.RowCause.Partner_Access__c`.
**Used for:** code-written shares that survive an owner change; `Manual` shares are deleted when the owner changes. Custom objects only.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

**Sharing recalculation class** — what is it, and what is it for? <!--id:core-apex-term-032-->
?
**Means:** a `Database.Batchable` class registered on a custom object that rebuilds the object's Apex-managed shares.
**Used for:** restoring your grants after an org-wide default change or a *Recalculate Sharing* run. Without one, that admin action wipes every share your code wrote, and nothing reports it.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

**`UserRecordAccess`** — what is it, and what are its limits? <!--id:core-apex-term-033-->
?
**Means:** a queryable object answering "can this user see this record?", with `HasReadAccess`, `HasEditAccess` and `HasDeleteAccess`.
**Used for:** per-record access checks. It must filter on `RecordId`, `IN` takes at most 200 Ids, and it answers sharing only: `HasEditAccess` can be true for a user with no Edit permission on the object.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) · [Glossary](../../GLOSSARY.md)

### Async

**`@future`** — what is it, and should new code use it? <!--id:core-apex-term-034-->
?
**Means:** an annotation that runs a static method later, in its own transaction. Parameters must be primitives; `@future(callout=true)` allows callouts.
**Used for:** legacy fire-and-forget work. It is not deprecated, but a Queueable does everything it does and more, so new code starts there.
Source: [Async Apex Overview & Choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md) · [Glossary](../../GLOSSARY.md)

**Queueable** — what is it, and what is it for? <!--id:core-apex-term-035-->
?
**Means:** a class implementing `Queueable` with `execute(QueueableContext)`, handed to `System.enqueueJob`, which returns a job Id.
**Used for:** the default async choice: typed state in member variables, one chained child job, a delay of up to 10 minutes, duplicate detection and finalizers.
Source: [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md) · [Glossary](../../GLOSSARY.md)

**`AsyncOptions`** — what is it, and what is it for? <!--id:core-apex-term-036-->
?
**Means:** an object passed to `System.enqueueJob(job, asyncOptions)`, carrying `MinimumQueueableDelayInMinutes`, `MaximumQueueableStackDepth` and `DuplicateSignature`.
**Used for:** delaying a job, capping a chain's depth, and suppressing duplicates. A second enqueue with the same signature throws `DuplicateMessageException` in the caller.
Source: [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md)

**`AsyncInfo`** — what is it, and what is it for? <!--id:core-apex-term-037-->
?
**Means:** methods that let a running Queueable ask where it is: `getCurrentQueueableStackDepth()`, `getMaximumQueueableStackDepth()`, `hasMaxStackDepth()`.
**Used for:** a chain's exit condition. A static counter can't do it, because statics reset at every transaction boundary.
Source: [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md)

**`AsyncApexJob`** — what is it, and what is it for? <!--id:core-apex-term-038-->
?
**Means:** the queryable record of every async job except platform events, with `Status`, `JobType`, `NumberOfErrors` and `ExtendedStatus`.
**Used for:** monitoring and failure alerts as a SOQL query rather than a trip to Setup → Apex Jobs.
Source: [Async Apex Overview & Choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md)

**Batch Apex (`Database.Batchable`)** — what is it, and what is it for? <!--id:core-apex-term-039-->
?
**Means:** a class with three methods: `start()` describes the whole record set, `execute()` gets one slice at a time, `finish()` runs once at the end. Each `execute()` is a separate transaction.
**Used for:** processing a record set too large for one transaction. A failed chunk takes only itself down.
Source: [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md) · [Glossary](../../GLOSSARY.md)

**`Database.Stateful`** — what is it, and what is it for? <!--id:core-apex-term-040-->
?
**Means:** a marker interface that keeps a batch class's instance member variables across `execute()` chunks.
**Used for:** running totals and summaries for `finish()`. The state is serialized between chunks, so keep it small.
Source: [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md) · [Glossary](../../GLOSSARY.md)

**Scheduled Apex** — what is it, and what should its `execute()` contain? <!--id:core-apex-term-041-->
?
**Means:** a class implementing `Schedulable`, started with `System.schedule(name, cron, job)`. Salesforce CRON has seven fields starting with Seconds, and one of day-of-month or day-of-week must be `?`.
**Used for:** clock-driven work. `execute()` runs under synchronous limits and can't call out, so it should only hand off to a batch or a Queueable.
Source: [Scheduled Apex & CRON](../../SF_core/02-apex-and-triggers/15-scheduled-apex-and-cron.md) · [Glossary](../../GLOSSARY.md)

**`CronTrigger`** — what is it, and what is it for? <!--id:core-apex-term-042-->
?
**Means:** the record of a scheduled job, with `NextFireTime`, `PreviousFireTime`, `State`, `TimesTriggered` and `CronExpression`, joined to `CronJobDetail` for the job's name.
**Used for:** monitoring scheduled jobs. At 67.0, also for auditing `OwnerId`: the job runs with its scheduler's access.
Source: [Scheduled Apex & CRON](../../SF_core/02-apex-and-triggers/15-scheduled-apex-and-cron.md)

**Transaction Finalizer** — what is it, and what is it for? <!--id:core-apex-term-043-->
?
**Means:** a class implementing `Finalizer`, attached inside a Queueable's `execute()` with `System.attachFinalizer()`. It runs in a new transaction after the job ends, however it ended.
**Used for:** logging and retrying after failures no `catch` can see, such as a CPU or heap blowout. It may make callouts and enqueue one job.
Source: [Transaction Finalizers](../../SF_core/02-apex-and-triggers/16-transaction-finalizers.md) · [Glossary](../../GLOSSARY.md)

### Events, callouts & cache

**`PlatformEventSubscriberConfig`** — what is it, and what is it for? <!--id:core-apex-term-044-->
?
**Means:** the metadata that configures an Apex platform event trigger's subscription.
**Used for:** running the subscriber as a chosen user instead of the Automated Process user, which also decides whose debug logs it lands in. At 67.0 it also sets up parallel subscriptions: up to 10 partitions with a partition key.
Source: [Platform Events & CDC in Apex](../../SF_core/02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md) · [Testing Platform Events & CDC](../../SF_core/02-apex-and-triggers/26-testing-platform-events-and-cdc.md)

**Resume checkpoint** — what is it, and what is it for? <!--id:core-apex-term-045-->
?
**Means:** `EventBus.TriggerContext.currentContext().setResumeCheckpoint(replayId)`, which marks the last event message the trigger finished.
**Used for:** resuming a retry after that message. Throwing `EventBus.RetryableException` instead replays the whole batch.
Source: [Platform Events & CDC in Apex](../../SF_core/02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

**`ChangeEventHeader`** — what is it, and what is it for? <!--id:core-apex-term-046-->
?
**Means:** the header on every Change Data Capture message: `changeType`, `recordIds`, `changedFields`, `commitUser`, `commitTimestamp` and `transactionKey`.
**Used for:** knowing what changed and who changed it (`commitUser`), and regrouping one user action from several messages (`transactionKey`). A delete carries `recordIds` and nothing else.
Source: [Platform Events & CDC in Apex](../../SF_core/02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

**`callout:` endpoint** — what is it, and what is it for? <!--id:core-apex-term-047-->
?
**Means:** `req.setEndpoint('callout:Named_Credential/path')`: the endpoint names a named credential instead of a URL. The platform adds the auth header and refreshes the token.
**Used for:** callouts with no endpoint literal, no Remote Site Setting and no token code. The same code works in sandbox and production because the name resolves per org.
Source: [Callouts, Named Credentials & HTTP in Apex](../../SF_core/02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)

**`Continuation`** — what is it, and what is it for? <!--id:core-apex-term-048-->
?
**Means:** an Apex class for a long-running callout started from a Lightning component: up to three callouts in parallel, released from the request thread while waiting, resumed in a callback.
**Used for:** "this API takes 40 seconds and the user is watching".
Source: [Callouts, Named Credentials & HTTP in Apex](../../SF_core/02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)

**`Database.AllowsCallouts`** — what is it, and what is it for? <!--id:core-apex-term-049-->
?
**Means:** a marker interface that lets a Queueable or a batch class make HTTP callouts.
**Used for:** async callouts, including the fix for a callout that has to come after DML. It replaces `@future(callout=true)` in new code.
Source: [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md) · [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

**Platform Cache** — what is it, and what is it for? <!--id:core-apex-term-050-->
?
**Means:** an in-memory key-value store that outlives the transaction: org cache (`Cache.Org`, shared by all users) and session cache (`Cache.Session`, one user's session).
**Used for:** not repeating expensive work, such as a callout response or an aggregate. Entries can vanish at any time, so a miss is the normal path.
Source: [Platform Cache](../../SF_core/02-apex-and-triggers/25-platform-cache.md) · [Glossary](../../GLOSSARY.md)

**Cache partition** — what is it, and what is it for? <!--id:core-apex-term-051-->
?
**Means:** a named slice of the org's cache capacity, at least 1 MB, split between org and session cache. Keys are addressed as `local.MyPartition.myKey`.
**Used for:** stopping one feature's entries evicting another's.
Source: [Platform Cache](../../SF_core/02-apex-and-triggers/25-platform-cache.md)

**`Cache.CacheBuilder`** — what is it, and what is it for? <!--id:core-apex-term-052-->
?
**Means:** an interface with one method, `doLoad(String key)`, which the platform calls only when the key is missing.
**Used for:** removing the check-then-populate branch: `Cache.Org.get(ConfigCache.class, 'Billing')` returns the value either way.
Source: [Platform Cache](../../SF_core/02-apex-and-triggers/25-platform-cache.md) · [Glossary](../../GLOSSARY.md)

### Testing

**`@TestSetup`** — what is it, and what is it for? <!--id:core-apex-term-053-->
?
**Means:** a method annotation that creates test records once per class, before any test method runs. Each method's changes roll back when it ends.
**Used for:** shared test data. `@IsTest(SeeAllData=true)` silently disables it, and a fatal error in it fails the whole class.
Source: [Apex Testing Fundamentals](../../SF_core/02-apex-and-triggers/20-apex-testing-fundamentals.md) · [Glossary](../../GLOSSARY.md)

**Data isolation (`SeeAllData`)** — what is it, and why is `SeeAllData=true` a defect? <!--id:core-apex-term-054-->
?
**Means:** since API 24.0, tests see only the data they create, plus setup objects such as `User`, `Profile`, `RecordType`, custom settings and custom metadata. `@IsTest(SeeAllData=true)` turns isolation off.
**Used for:** tests that pass in any org. With `SeeAllData=true` a test passes where it was written and fails in a fresh scratch org.
Source: [Apex Testing Fundamentals](../../SF_core/02-apex-and-triggers/20-apex-testing-fundamentals.md) · [Glossary](../../GLOSSARY.md)

**`System.runAs`** — what is it, and why did it become necessary? <!--id:core-apex-term-055-->
?
**Means:** a test block that runs code as a given user. It costs one DML statement and resets no limits.
**Used for:** testing what a real user gets. At 67.0, user mode and the `with sharing` default mean the running identity decides the result, so a suite without it only tests the admin.
Source: [Apex Testing Fundamentals](../../SF_core/02-apex-and-triggers/20-apex-testing-fundamentals.md) · [Glossary](../../GLOSSARY.md)

**`HttpCalloutMock`** — what is it, and what is it for? <!--id:core-apex-term-056-->
?
**Means:** the interface a test registers with `Test.setMock(HttpCalloutMock.class, new MyMock())` to supply HTTP responses. `WebServiceMock` is the SOAP version.
**Used for:** testing callout code, including its error branches. An unmocked callout throws in every test, and one mock covers every callout in the test.
Source: [Apex Testing Advanced & Mocking](../../SF_core/02-apex-and-triggers/21-apex-testing-advanced-and-mocking.md) · [Glossary](../../GLOSSARY.md)

**Stub API** — what is it, and what is it for? <!--id:core-apex-term-057-->
?
**Means:** `Test.createStub(Type, provider)` builds a runtime subclass and routes every call to your `System.StubProvider.handleMethodCall`, which gets six arguments, the method name as a `String`.
**Used for:** replacing a collaborator object that is expensive, non-deterministic or not the subject of the test. A rename of the real method breaks it silently.
Source: [Apex Testing Advanced & Mocking](../../SF_core/02-apex-and-triggers/21-apex-testing-advanced-and-mocking.md) · [Glossary](../../GLOSSARY.md)

**`Test.getEventBus().deliver()`** — what is it, and what is it for? <!--id:core-apex-term-058-->
?
**Means:** delivers the platform events published since the previous `deliver()` call in a test. Publishing alone never runs the subscriber.
**Used for:** making the subscriber actually run before you assert, and stepping through a retry sequence one attempt at a time.
Source: [Testing Platform Events & CDC](../../SF_core/02-apex-and-triggers/26-testing-platform-events-and-cdc.md)

**`EventBusSubscriber`** — what is it, and what is it for? <!--id:core-apex-term-059-->
?
**Means:** a queryable object holding a subscriber's state: `Position`, `Retries`, `LastError`, `Topic`, `Type` and `Name`.
**Used for:** asserting that a retry really happened. A `RetryableException` leaves `Position` where it was.
Source: [Testing Platform Events & CDC](../../SF_core/02-apex-and-triggers/26-testing-platform-events-and-cdc.md) · [Glossary](../../GLOSSARY.md)

**`Test.setFixedSearchResults()`** — what is it, and what is it for? <!--id:core-apex-term-060-->
?
**Means:** a test method that seeds the record Ids a SOSL search returns.
**Used for:** testing code that calls `Search.find()`, which returns nothing in a test unless seeded.
Source: [Dynamic SOQL, SOSL & Describe in Apex](../../SF_core/02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md)

### Design, interop & AI

**`@InvocableVariable`** — what is it, and what is it for? <!--id:core-apex-term-061-->
?
**Means:** an annotation on a `public` or `global` field of an invocable action's input or output class, with `label`, `description` and `required`.
**Used for:** exposing the field to Flow, agents and the Actions API. Private fields are skipped silently.
Source: [Invocable Apex & Agentforce Actions](../../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)

**Apex-Defined Type (ADT)** — what is it, and what is it for? <!--id:core-apex-term-062-->
?
**Means:** an Apex class with `@AuraEnabled` members, used as a Flow variable's data type or an LWC payload.
**Used for:** holding a shape with no custom object behind it, such as a parsed API response. Since Winter '26, Flow Data Tables can display one.
Source: [UserDefinedType & Typed Interop](../../SF_core/02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md) · [Glossary](../../GLOSSARY.md)

**`UserDefinedType`** — what is it? <!--id:core-apex-term-063-->
?
**Means:** not an interface. It is the Apex docs' phrase for an ordinary class you write and use as a typed payload; nothing implements it.
**Used for:** answering the trick question "which interface does it refer to?": none.
Source: [UserDefinedType & Typed Interop](../../SF_core/02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md) · [Glossary](../../GLOSSARY.md)

**`equals` / `hashCode` contract** — what is it, and what is it for? <!--id:core-apex-term-064-->
?
**Means:** a class implements both `public Boolean equals(Object)` and `public Integer hashCode()`, which collections use to decide identity.
**Used for:** using your own class as a map key or set element. Implement both or neither, and don't change a hashed field after insertion, or the entry can't be found.
Source: [UserDefinedType & Typed Interop](../../SF_core/02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md)

**Apex Enterprise Patterns** — what are they, and when are they worth it? <!--id:core-apex-term-065-->
?
**Means:** layers above the trigger handler: **Selector** (all SOQL for one object), **Domain** (per-record logic), **Service** (a use case across objects) and **Unit of Work** (all DML).
**Used for:** multi-team orgs and long-lived code, where each layer gets one reason to change and can be mocked. On a small single-team org they cost more than they return.
Source: [Apex Enterprise Patterns & Layered Design](../../SF_core/02-apex-and-triggers/27-apex-enterprise-patterns-and-layered-design.md) · [Glossary](../../GLOSSARY.md)

**Unit of Work** — what is it, and what is it for? <!--id:core-apex-term-066-->
?
**Means:** the layer that owns every DML statement: `registerNew`, `registerDirty` and `registerRelationship`, then one `commitWork()` that issues one DML statement per object type inside a single savepoint.
**Used for:** deleting the "insert parents, collect Ids, insert children" ritual. It doesn't lift the 10,000-row DML limit, and one bad record rolls back everything.
Source: [Apex Enterprise Patterns & Layered Design](../../SF_core/02-apex-and-triggers/27-apex-enterprise-patterns-and-layered-design.md) · [Glossary](../../GLOSSARY.md)

**fflib** — what is it, and who supports it? <!--id:core-apex-term-067-->
?
**Means:** the community open-source library implementing the Apex Enterprise Patterns, in the `apex-enterprise-patterns` GitHub org. It began as FinancialForce's Apex Commons.
**Used for:** ready-made Selector, Domain and Unit of Work base classes. It is not a Salesforce product, so adopting it means owning its upgrades with no Salesforce support path.
Source: [Apex Enterprise Patterns & Layered Design](../../SF_core/02-apex-and-triggers/27-apex-enterprise-patterns-and-layered-design.md)

**`Type.forName`** — what is it, and what is it for? <!--id:core-apex-term-068-->
?
**Means:** turns a class name `String` into a `Type`, whose `newInstance()` creates an object through a visible no-arg constructor. Across packages, use `Type.forName(namespace, className)`.
**Used for:** choosing an implementation at runtime, typically from a class name in a custom metadata record, so behaviour changes with a data deploy.
Source: [Dependency Injection & Pluggable Apex](../../SF_core/02-apex-and-triggers/28-dependency-injection-and-pluggable-apex.md) · [Glossary](../../GLOSSARY.md)

**`System.Callable`** — what is it, and when is it the right seam? <!--id:core-apex-term-069-->
?
**Means:** an interface with one method, `call(String action, Map<String, Object> args)`. Arguments and return value are untyped `Object`.
**Used for:** one package invoking another it can't compile against. Inside one codebase it is too loose.
Source: [Dependency Injection & Pluggable Apex](../../SF_core/02-apex-and-triggers/28-dependency-injection-and-pluggable-apex.md) · [Glossary](../../GLOSSARY.md)

**`capabilityType`** — what is it, and what does it change? <!--id:core-apex-term-070-->
?
**Means:** a parameter on `@InvocableMethod`, such as `PromptTemplateType://einstein_gpt__salesEmail` or `FlexTemplate://<template_API_Name>`. The `Response` class must expose `@InvocableVariable public String Prompt`.
**Used for:** turning an invocable method into a grounding provider. The platform calls it while resolving a prompt, and the `Prompt` string is spliced into the template.
Source: [Apex-Grounded Prompt Templates](../../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md)

**`ConnectApi.EinsteinLLM`** — what is it, and what is it for? <!--id:core-apex-term-071-->
?
**Means:** the Apex class whose static `generateMessagesForPromptTemplate(devName, input)` (API 60.0) runs a prompt template, and `getPromptTemplates` (API 62.0) lists templates.
**Used for:** running a prompt template from code. The response carries the resolved `prompt` and the `generations`; `isPreview = true` resolves the template without calling the model.
Source: [Invoking Prompt Templates from Apex](../../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) · [Glossary](../../GLOSSARY.md)

**`JSONGenerator` / `JSONParser`** — what are they, and what are they for? <!--id:core-apex-term-072-->
?
**Means:** streaming JSON classes: `writeStartObject()` and `writeStringField()` to write, `nextToken()` and `getText()` to read.
**Used for:** payloads big enough that holding both the object graph and the JSON string would exceed heap.
Source: [JSON, Serialization & Untyped Data](../../SF_core/02-apex-and-triggers/29-json-serialization-and-untyped-data.md)

## Hard

#flashcards/core/apex-terminology/hard

### Commonly confused

In a review: "The outer class is `without sharing`, so its inner helper class `Loader` sees every record too." After a recompile at 67.0, `Loader`'s queries return fewer rows. Which assumption is wrong? <!--id:core-apex-term-073-->
?
Inner classes don't inherit the outer class's sharing keyword. They take the default, which at 67.0 is `with sharing`. Declare the keyword on the inner class itself, deliberately.
Hint: does a sharing keyword carry over to an inner class?
Trap: "inner classes inherit the outer class's sharing."
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

In a review: "This class is `without sharing`, so it bypasses security and returns every field of every record." It is compiled at 67.0 and uses plain inline SOQL. What does it actually return? <!--id:core-apex-term-074-->
?
Every record, but only the fields the running user can read. `without sharing` controls record visibility only; CRUD and FLS come from the execution mode, and at 67.0 plain SOQL runs in user mode. Reading restricted fields would need `WITH SYSTEM_MODE` or `AccessLevel.SYSTEM_MODE`, chosen on purpose.
Hint: sharing keyword and execution mode are two separate axes.
Trap: treating `without sharing` as system mode.
Source: [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) · [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

In a review: "The batch keeps its running total in a `static Integer`, so `finish()` can email it." The email always reports about 200. Which two terms are confused? <!--id:core-apex-term-075-->
?
A static and a `Database.Stateful` instance member. A static lives for one transaction, and each `execute()` chunk is its own transaction, so the total is the last chunk's count. Implement `Database.Stateful` and keep the total in an **instance** member, which survives across chunks.
Hint: how long does a static live, and how many transactions does a batch run?
Trap: "`Database.Stateful` keeps statics too."
Source: [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

In a design review: "We'll wrap the Queueable's work in `try/catch` to log failures, and attach a Transaction Finalizer to the nightly batch for the same." What is wrong with each half? <!--id:core-apex-term-076-->
?
A `catch` can't see a `LimitException`, which is exactly when the log matters. A finalizer runs in a new transaction after the job ends, however it ended, so it is the right tool for the Queueable. But finalizers are Queueable-only. For the batch, implement `Database.RaisesPlatformEvents` and subscribe to `BatchApexErrorEvent`.
Hint: which async types can attach a finalizer?
Trap: "a finalizer is a `catch` block that works on any async job."
Source: [Transaction Finalizers](../../SF_core/02-apex-and-triggers/16-transaction-finalizers.md) · [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

In a design review: "The batch might pass 50 million rows one day, so return an `Iterable` from `start()` instead of a `QueryLocator`, because iterables scale better." Respond. <!--id:core-apex-term-077-->
?
Backwards. A `QueryLocator` handles 50 M rows; an `Iterable` is assembled inside a normal transaction, so it is capped at the 50,000-row query limit. Use an `Iterable` only when the scope can't be written as SOQL: an aggregate result, a decoded file, pages from an external API.
Hint: in which transaction is the `Iterable` built?
Trap: "iterables are lazy, so they scale further."
Source: [Custom Iterators & Iterables](../../SF_core/02-apex-and-triggers/30-custom-iterators-and-iterables.md) · [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md) · [Glossary](../../GLOSSARY.md)

A class implements both `Iterator<Integer>` and `Iterable<Integer>`, and `iterator()` returns `this`. The first `for` loop over an instance prints 3, 2, 1. A second loop over the same instance prints nothing, with no error. Why? <!--id:core-apex-term-078-->
?
`Iterator` is the cursor that holds the position; `Iterable` is the factory that should hand out a fresh cursor. Returning `this` makes the object single-use: the second loop starts from the exhausted position and runs zero times. Return a new instance from `iterator()`.
Hint: which of the two interfaces holds the position?
Trap: "every `for` loop restarts the iterator."
Source: [Custom Iterators & Iterables](../../SF_core/02-apex-and-triggers/30-custom-iterators-and-iterables.md) · [Glossary](../../GLOSSARY.md)

A 5,000-row Order import dies on row 12 and nothing is saved. The trigger handler runs `throw new OrderException('Exceeds credit limit')` when one order is over its limit. Which mechanism should it have used? <!--id:core-apex-term-079-->
?
`addError()` on the offending record. It rejects that one row, and in a partial-success load the rest still commit. `throw` abandons the whole transaction. `throw` belongs in a service class, where the calling code decides what a failure means; `addError()` belongs at a record boundary.
Hint: should one bad row reject the whole batch?
Trap: catching the exception in the trigger. A `catch` can't reject a single row or undo work.
Source: [Exception Handling & Custom Exceptions](../../SF_core/02-apex-and-triggers/09-exception-handling-and-custom-exceptions.md)

A partner API returns `{"id": "A-1", "currency": "EUR", "amount": 12.5}`. The developer's typed Apex class for it won't compile, and a colleague suggests `JSON.deserializeStrict` "to be safe". What do you use? <!--id:core-apex-term-080-->
?
`JSON.deserializeUntyped`, which returns a `Map<String, Object>`. `currency` is an Apex reserved word, so no typed class can declare it. `deserializeStrict` throws on any unknown field, which is wrong for a third-party API that adds fields; plain `deserialize` ignores them. Cast untyped numbers carefully: `12.5` comes back as a `Double`, not a `Decimal`.
Hint: can an Apex class declare a field named `currency`?
Trap: `deserializeStrict` "for safety".
Source: [JSON, Serialization & Untyped Data](../../SF_core/02-apex-and-triggers/29-json-serialization-and-untyped-data.md) · [Glossary](../../GLOSSARY.md)

`RefundLine` is used both as a Flow variable (an Apex-Defined Type) and as an invocable action's input. Its `public` field `amount` appears on the Flow variable but not in the action's inputs in Flow Builder. What is missing? <!--id:core-apex-term-081-->
?
`@InvocableVariable`. `@AuraEnabled` exposes a field to Flow variables and LWC; `@InvocableVariable` exposes it to an action's inputs. Neither implies the other, so a class used both ways often needs both annotations on the same field.
Hint: which annotation does an action read?
Trap: "`@AuraEnabled` exposes the field everywhere."
Source: [UserDefinedType & Typed Interop](../../SF_core/02-apex-and-triggers/23-userdefinedtype-and-typed-interop.md)

In a design review: "Admins want to tweak the case-summary wording without a deploy, so we'll call `aiplatform.ModelsAPI` and keep the prompt text in Apex." Which API fits, and how do the two differ? <!--id:core-apex-term-082-->
?
`ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate` with a prompt template: the wording lives in metadata that admins edit in Prompt Builder, with grounding and versioning. `aiplatform.ModelsAPI` calls a model with no template, so the prompt is a string in Apex and every wording change is a deploy. `EinsteinLLM` is static; `ModelsAPI` is instantiated and each call is a callout.
Hint: where does the prompt text live in each?
Trap: "they are two names for the same call."
Source: [Invoking Prompt Templates from Apex](../../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) · [Models API in Apex](../../SF_core/02-apex-and-triggers/33-models-api-in-apex.md) · [Glossary](../../GLOSSARY.md)

In a design review: "We'll store each user's visible Accounts in org cache for 48 hours so pages load faster." Which two terms are confused, and what goes wrong? <!--id:core-apex-term-083-->
?
Org cache (`Cache.Org`) is shared by all users; session cache (`Cache.Session`) belongs to one user's session. Worse, cache applies no FLS or sharing on read: whatever goes in comes back to whoever asks, so one user's records leak to everyone. Cache a computed answer, not raw records, and treat a miss as normal.
Hint: who can read an org cache entry?
Trap: "the cache applies the reader's sharing."
Source: [Platform Cache](../../SF_core/02-apex-and-triggers/25-platform-cache.md)

A team wants to test `InvoiceService` without its `TaxCalculator` dependency, a class with only static methods. They register an `HttpCalloutMock`, then try `Test.createStub(TaxCalculator.class, provider)`. Neither helps. Why, and what is the fix? <!--id:core-apex-term-084-->
?
`HttpCalloutMock` fakes an HTTP response, not an object, so it only helps when the code makes a callout. The Stub API fakes an object by subclassing it, and it can't stub static methods (nor private methods, properties, inner classes or `Batchable` classes). The fix is a design change: put `TaxCalculator` behind an interface and inject it.
Hint: what does each one replace, the wire or the object?
Trap: hunting for a test trick instead of changing the design.
Source: [Apex Testing Advanced & Mocking](../../SF_core/02-apex-and-triggers/21-apex-testing-advanced-and-mocking.md) · [Dependency Injection & Pluggable Apex](../../SF_core/02-apex-and-triggers/28-dependency-injection-and-pluggable-apex.md)
