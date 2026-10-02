---
area: Core
topic: Apex & Triggers
id_prefix: core-apex
---
# Core › Apex & Triggers

Interview cards for Apex, written for a technical architect or senior developer. Facts are as of Summer '26 (API 67.0), the release the linked notes were checked against. Answers are short on purpose: the reasoning lives in the linked note. The vocabulary is drilled separately in [apex-terminology.md](apex-terminology.md). Format and rules are in the README one folder up.

## Foundations

#flashcards/core/apex/foundations

### Limits & language

What are the synchronous and asynchronous per-transaction limits for SOQL queries, DML statements, CPU time and heap? <!--id:core-apex-001-->
?
SOQL **100 / 200** queries, with 50,000 rows either way. DML **150** statements in both. CPU **10,000 / 60,000 ms**. Heap **6 / 12 MB**. Crossing any of them throws `LimitException`, which no `catch` can stop, so check `Limits.getQueries()` against `Limits.getLimitQueries()` before the work.
Trap: `catch (Exception e)` around the heavy loop. It does not catch `LimitException`.
Source: [Apex Language Core & Governor Limits](../../SF_core/02-apex-and-triggers/01-apex-language-core-and-governor-limits.md)

Which Apex syntax is new at Summer '26 (API 67.0), and which "modern" operators are older than most articles claim? <!--id:core-apex-002-->
?
New at 67.0: multiline strings (`'''…'''`) and `String.template()` for `${key}` placeholders. Older: `switch` (Summer '18, 43.0), `?.` (Winter '21, 50.0) and `??` (Spring '24, 60.0). An article calling `??` new is out of date.
Source: [Modern Apex Syntax](../../SF_core/02-apex-and-triggers/02-modern-apex-syntax.md)

### Queries & DML

`Database.insert(records, false)`: what does it return, and how do you find which input record failed? <!--id:core-apex-003-->
?
A `Database.SaveResult[]` that is **positional**: result *i* belongs to input record *i*. Good rows commit; failed rows carry `getErrors()` with `getMessage()`, `getStatusCode()` and `getFields()`. Match failures by index, because `getId()` is null on a failed insert. The statement form, `insert records;`, rolls back everything on any failure instead.
Source: [DML, Database Methods & Savepoints](../../SF_core/02-apex-and-triggers/05-dml-database-methods-and-savepoints.md)

What are the limits of `Database.Cursor`, and when did it go GA? <!--id:core-apex-004-->
?
Up to **50 M** rows per cursor, a **2-day** lifetime, and **100** `fetch()` calls per transaction, shared with pagination cursors. Each `fetch()` costs one SOQL query. The org can create 10,000 cursors per 24 hours. Beta in Summer '24 (61.0), GA in Spring '26 (66.0).
Trap: "a cursor gets you past 50,000 rows per transaction." Fetched rows still count. It saves heap and lets you resume in the next transaction.
Source: [Database.Cursor & Large Result Sets](../../SF_core/02-apex-and-triggers/17-database-cursor-and-large-result-sets.md)

### Triggers & order of execution

In the save order, ==before-save record-triggered flows== run at step 3, ahead of ==before triggers== at step 4. The record is written at step 7 and ==after triggers== run at step 8. After-save flows run at step 14, ==roll-up summaries== recalculate at steps 16–17, and the transaction ==commits== at step 19. <!--id:core-apex-005-->
Source: [Order of Execution & Recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Order of execution: declarative view](../../SF_core/01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md)

Which trigger context variables are missing or read-only, and in which contexts? <!--id:core-apex-006-->
?
`before insert` has no `Trigger.newMap`, `Trigger.old` or `Trigger.oldMap`: no Ids and no prior version exist yet. Delete contexts have no `Trigger.new`. `Trigger.new` is editable only in `before` triggers; assigning to it in an `after` trigger throws. `Trigger.old` and both maps are always read-only, even in `before update`.
Source: [Triggers & the Handler Framework](../../SF_core/02-apex-and-triggers/06-triggers-and-the-handler-framework.md)

### Security & sharing

What changed in Apex data access at API 67.0, and which classes does it apply to? <!--id:core-apex-007-->
?
SOQL, SOSL, DML and `Database` methods default to **user mode** (CRUD, FLS and sharing enforced). A class with no sharing keyword defaults to **`with sharing`**. `WITH SECURITY_ENFORCED` no longer compiles, and triggers always run in system mode. It applies only to classes **compiled at 67.0**, so behaviour changes when someone bumps a class's API version, not on upgrade day.
Trap: "nothing broke on upgrade day, so nothing changed."
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Sharing Keywords & Apex Managed Sharing](../../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

What does `Security.stripInaccessible` return, and when do you use it instead of `WITH USER_MODE`? <!--id:core-apex-008-->
?
`Security.stripInaccessible(AccessType.UPDATABLE, records)` removes the fields the user can't touch and returns an `SObjectAccessDecision`: `getRecords()` for the cleaned list, `getRemovedFields()` for what it took out. It never throws. Use it when the operation should carry on without those fields, such as cleaning an untrusted payload before DML.
Trap: assuming the DML will now succeed. Object permission is still checked: no Create access still means a `DmlException`.
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

### Async

What are the shared async limits: the daily ceiling, the flexible queue and the enqueue limits? <!--id:core-apex-009-->
?
Daily: **250,000** async executions or **200 × user licences**, whichever is greater, shared by `@future`, Queueable, batch chunks and scheduled runs. The flexible queue holds **100** unstarted jobs; past that, `System.enqueueJob` throws. A synchronous transaction can enqueue **50** Queueables, an async one only **1**.
Source: [Async Apex Overview & Choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md) · [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md)

What can a batch `start()` return, how big is each `execute()` chunk, and how many batch jobs can run at once? <!--id:core-apex-010-->
?
A `Database.QueryLocator` (up to **50 M** rows) or an `Iterable<sObject>` (capped at **50,000**). Scope is 1–2,000 records, default **200**, and each `execute()` is its own transaction. **5** jobs can be queued or active at once; further submissions wait in `Holding`, up to 100.
Source: [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

### Events & callouts

How does an Apex platform event subscriber run: which trigger event, how many messages, as which user, under which limits? <!--id:core-apex-011-->
?
An `after insert` trigger only. It receives up to **2,000** messages per run, in its own transaction, under **synchronous** limits (100 SOQL, 10,000 ms CPU). It runs as the **Automated Process user** unless `PlatformEventSubscriberConfig` sets another, so `UserInfo.getUserId()` is not the person who made the change.
Source: [Platform Events & CDC in Apex](../../SF_core/02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

What are the three callout limits per Apex transaction? <!--id:core-apex-012-->
?
**100** callouts, **120 s** of cumulative callout time, and a per-callout timeout that defaults to **10 s** and can be raised to 120 s with `req.setTimeout()`. The 120 s is a shared budget: five 30-second calls exceed it, and the fifth one fails.
Source: [Callouts, Named Credentials & HTTP in Apex](../../SF_core/02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md)

### Testing

Which of these reset governor limits in a test: `@TestSetup`, `Test.startTest()`/`stopTest()`, `System.runAs`? <!--id:core-apex-013-->
?
Only `Test.startTest()`/`stopTest()`, once per method; a second pair throws. `stopTest()` also runs queued async work. `@TestSetup` resets nothing: what it uses counts against every test method, so wrap its body in `startTest`/`stopTest`. `System.runAs` resets nothing and costs one DML statement per call.
Trap: "`@TestSetup` resets the DML limits but not SOQL." Neither is reset.
Source: [Apex Testing Fundamentals](../../SF_core/02-apex-and-triggers/20-apex-testing-fundamentals.md)

What code coverage does a deployment require, and what does that gate not check? <!--id:core-apex-014-->
?
**75%** org-wide, plus some coverage on every trigger, checked at deploy time rather than per class. It never checks that a single assertion exists. The current assertion class is `Assert` (Winter '23, API 56.0); `System.assertEquals` still works and is not deprecated.
Exact: 75%
Source: [Apex Testing Fundamentals](../../SF_core/02-apex-and-triggers/20-apex-testing-fundamentals.md)

### Design, interop & AI

What are the signature rules for an `@InvocableMethod`, and what must its return value guarantee? <!--id:core-apex-015-->
?
Exactly one per class, on an outer class. `static`, and `public` or `global`. At most one parameter, a `List<>`; it returns a `List<>` or `void`. The output list must match the input list in size and order, because Flow calls in bulk and maps results by position. An agent reads the `label` and `description` to decide whether to call it.
Source: [Invocable Apex & Agentforce Actions](../../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)

How do you call `aiplatform.ModelsAPI`, and which two budgets does every call spend? <!--id:core-apex-016-->
?
Through instance methods on `new aiplatform.ModelsAPI()`; a static call does not compile. The four methods are `createGenerations`, `createChatGenerations`, `createEmbeddings` and `submitFeedback`. Each call is an Apex **callout**, so it counts toward the 100 per transaction, and it is billed as an **Einstein Request**.
Source: [Models API in Apex](../../SF_core/02-apex-and-triggers/33-models-api-in-apex.md)

## Hard

#flashcards/core/apex/hard

### Limits & language

An `after update` trigger on Opportunity fails with `Apex CPU time limit exceeded`. The developer spent a day optimising the handler class named in the error; on its own it now runs in 900 ms. The save still fails. What are they missing? <!--id:core-apex-017-->
?
CPU time is cumulative across the whole save order. Flows and other automation earlier in the same transaction spent the budget, so the class that throws is rarely the one that spent it. Attribute the cost first: read `CUMULATIVE_PROFILING` and `LIMIT_USAGE_FOR_NS` at the end of the debug log, or log `Limits.getCpuTime()` deltas around each block.
Hint: whose budget is the 10,000 ms?
Trap: optimising the class named in the exception.
Source: [Apex Performance & Profiling](../../SF_core/02-apex-and-triggers/24-apex-performance-and-profiling.md)

Code review. This compiles and deploys at API 67.0. What happens when it runs, and what else is wrong? <!--id:core-apex-018-->
```apex
String body = '''
Hi ${nmae},
Your order shipped on ${shipped}.'''.template(new Map<String, Object>{
    'name'    => c.FirstName ?? 'there',
    'shipped' => o.Shipped_At__c
});
```
?
It throws a runtime `StringException`: `${nmae}` has no matching key, and `.template()` has no compile-time key checking. Quieter bug: the `Datetime` renders in **GMT** as `yyyy-MM-dd HH:mm:ss`, not in the user's locale, so format it before putting it in the map.
Hint: when are the placeholders matched against the map?
Trap: "the compiler would have caught the typo."
Source: [Modern Apex Syntax](../../SF_core/02-apex-and-triggers/02-modern-apex-syntax.md)

### Queries & DML

A service hits `Too many SOQL queries: 101` halfway through. A developer proposes: set a savepoint at the start, catch the failure, roll back, and retry with a smaller batch. What is wrong with the plan? <!--id:core-apex-019-->
?
Two things. `LimitException` can't be caught, so the `catch` never runs. And even for catchable failures, a rollback restores **data only**: queries and DML already spent stay spent, and static variables keep their values. The savepoint costs one DML statement and the rollback another. Fix the cost instead: bulkify, or move the work to a batch.
Hint: what does a rollback give back, and what doesn't it?
Trap: treating a savepoint as a way to retry past a limit.
Source: [DML, Database Methods & Savepoints](../../SF_core/02-apex-and-triggers/05-dml-database-methods-and-savepoints.md) · [Apex Language Core & Governor Limits](../../SF_core/02-apex-and-triggers/01-apex-language-core-and-governor-limits.md)

A component on a customer portal builds a filter from user input. The developer concatenates the input into a SOQL string and runs `Database.query(soql, AccessLevel.USER_MODE)`. "User mode makes it safe." Do you agree? <!--id:core-apex-020-->
?
No. User mode limits the damage to what the running user can already see, which on a portal can still be a lot. It does nothing about injection. Pass values through `Database.queryWithBinds(soql, bindMap, AccessLevel.USER_MODE)`, which resolves binds from the map by key. Binds can't replace identifiers, so field and object names need an allowlist.
Hint: what does user mode limit, and what does a bind limit?
Trap: "user mode makes dynamic SOQL injection-safe."
Source: [Dynamic SOQL, SOSL & Describe in Apex](../../SF_core/02-apex-and-triggers/04-advanced-soql-sosl-and-dynamic-queries.md)

### Triggers & order of execution

An Opportunity after-update trigger rolls a value up to Account, guarded by `private static Boolean hasRun`. Data Loader updates 19,000 opportunities. The job reports full success, but only 12 accounts are right. Coverage on the handler is 94%. What happened? <!--id:core-apex-021-->
?
The guard is per transaction, not per record. The first chunk of 200 sets `hasRun = true`, and every later record in that transaction is skipped silently. Track Ids instead: a `static Set<Id> processed`, remove the Ids already done, and process the rest. The 94% came from a single-record test; add one that saves 200+ records.
Hint: how many records does one trigger invocation see, and how long does a static live?
Trap: deleting the guard. The infinite loop it was added for comes back. Setting Data Loader's batch size to 1 only hides the bug.
Source: [Order of Execution & Recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Interview set](../../Interview/03-core-platform/01-apex-triggers-and-limits.md)

An `after update` trigger on Account reads a roll-up summary field and writes a tier, but the tier is always one save behind. Separately, a field the `before update` trigger sets is sometimes already populated when the trigger starts. There is only one trigger on the object. Explain both. <!--id:core-apex-022-->
?
Both are save-order facts. Roll-ups recalculate at steps 16–17, after after-triggers run at step 8, so the trigger reads the old value: compute the aggregate yourself with a `GROUP BY` query, or move the tier logic later. The pre-set field comes from a before-save flow at step 3, which runs ahead of every before trigger. Flow Trigger Explorer shows it.
Hint: where is each value produced, relative to the code reading it?
Trap: hunting for a second trigger or a race condition. The order is fixed and deterministic.
Source: [Order of Execution & Recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Interview set](../../Interview/03-core-platform/01-apex-triggers-and-limits.md)

### Security & sharing

A service class compiled at 67.0 calls an old selector class still at API 55.0. The team assumes every query now runs in user mode. Does it? <!--id:core-apex-023-->
?
No. The API version that counts is the one on the class that runs the query, so the 55.0 selector still runs its SOQL in system mode. The day someone bumps the selector to 67.0 "for consistency", its queries start enforcing FLS and sharing with no code change. Treat a version bump on a data-access class as a security change, and state the mode with `WITH USER_MODE` or `AccessLevel`.
Hint: which class's API version does the platform apply?
Trap: "the caller's version applies to everything it calls."
Source: [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

A bulkified handler collects `AccountId`s, runs one query into a `Map<Id, Account>`, and calls `accounts.get(o.AccountId)` in the loop. It has run in production for three years. Since it was recompiled at 67.0, one support tier gets intermittent `NullPointerException`s; sales users never do. The data is fine. What changed, and what is the fix? <!--id:core-apex-024-->
?
The query now runs in user mode, so it returns only the accounts that user can see, and `Map.get()` returns null for the rest. Null now means "no such record" **or** "this user can't see it". The fix is a decision, not a null check: skip the record, `addError()` it, or elevate that one query with `AccessLevel.SYSTEM_MODE` and write down why.
Hint: same code, same records, different users.
Trap: adding a null check and moving on. The support tier's results then silently come from a subset of accounts.
Source: [Bulkification Patterns](../../SF_core/02-apex-and-triggers/08-bulkification-patterns.md) · [Apex Security: User Mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) · [Interview set](../../Interview/03-core-platform/01-apex-triggers-and-limits.md)

### Async

A nightly process hits `Too many SOQL queries: 101`. The pull request moves the work into a Queueable enqueued per record from the trigger: "async gets fresh limits". The org processes 80,000 records a night and runs three other scheduled jobs. The test passes. Name three things wrong. <!--id:core-apex-025-->
?
- A sync transaction can enqueue only 50 Queueables, and the flexible queue holds 100 unstarted jobs, so per-record enqueues throw almost at once.
- The daily async ceiling (250,000 or 200 × licences) is shared; 80,000 enqueues a night eats it.
- The trigger's transaction still has to fit its own budget. If the 101 comes from a query in a loop, bulkify it; if the work is bigger than one transaction, use Batch Apex.
Hint: async gives you another transaction, not more budget.
Trap: accepting "async gets fresh limits" and reviewing only the code. The test passes because `stopTest()` runs async work synchronously.
Source: [Async Apex Overview & Choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md) · [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md) · [Interview set](../../Interview/03-core-platform/03-integration-and-async.md)

Monitoring checks that the nightly batch's `AsyncApexJob.Status` is `Completed`, and it always is. Users still report records that were never archived. How can both be true, and how should it be monitored? <!--id:core-apex-026-->
?
A failed chunk rolls back only itself. The job still reaches `Completed`, with `NumberOfErrors` greater than zero. Check `NumberOfErrors` too, and implement `Database.RaisesPlatformEvents` so each failed chunk publishes a `BatchApexErrorEvent` with the job Id, the exception and the chunk's record Ids. At 67.0, also check the `QueryLocator`: it defaults to user mode, so the scope may be quietly smaller.
Hint: what does one failing `execute()` take down?
Trap: "Completed means every record was processed."
Source: [Batch Apex & Stateful Processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

### Events & callouts

A platform event trigger calls an ERP. During a 3-hour ERP outage it throws `EventBus.RetryableException` on every failure. Afterwards the trigger processes nothing new, although publishing still succeeds. What happened, and what should the trigger have done? <!--id:core-apex-027-->
?
After **10 runs** (1 attempt + 9 retries) the trigger goes into an error state and stops processing until the class is fixed and saved. Cap retries yourself by reading `EventBus.TriggerContext.currentContext().retries`, then dead-letter the message. `setResumeCheckpoint(replayId)` makes a retry resume after the last message you finished, instead of replaying the whole batch.
Hint: is there a ceiling on retries?
Trap: "it retries until the ERP comes back."
Source: [Platform Events & CDC in Apex](../../SF_core/02-apex-and-triggers/18-platform-events-and-cdc-in-apex.md)

A service inserts a `Payment__c` and then calls the payment gateway. It fails with `You have uncommitted work pending. Please commit or rollback before calling out.` An old team note says "use `@future`". What is the current answer? <!--id:core-apex-028-->
?
The open transaction holds row locks, and the platform won't hold them while a third party responds. Often the fix isn't async at all: make the callout first, then the DML. If it must come after, use a Queueable that implements `Database.AllowsCallouts`: typed state and a job Id. A trigger can't make a synchronous callout at all, so trigger-driven callouts are async from the start.
Hint: why won't the platform let you wait on a third party here?
Trap: `@future(callout=true)`. It still works, but it is legacy.
Source: [Callouts, Named Credentials & HTTP in Apex](../../SF_core/02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) · [Queueable Apex & Chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md)

### Testing

A CDC test inserts 50 Accounts, calls `Test.enableChangeDataCapture()`, then `Test.getEventBus().deliver()`, and asserts that the change-event trigger created 50 Tasks. It finds 0. The trigger works in the sandbox. Why? <!--id:core-apex-029-->
?
`Test.enableChangeDataCapture()` must be the first line, before any DML. Called after the inserts it does nothing, so no change events were generated. A green CDC test also proves nothing about production: the test makes change triggers fire whatever is selected in Setup, so check that CDC is enabled for the object in the target org.
Hint: when does the test start capturing changes?
Trap: debugging the subscriber. It works; the events were never generated.
Source: [Testing Platform Events & CDC](../../SF_core/02-apex-and-triggers/26-testing-platform-events-and-cdc.md)

A class calls `ConnectApi.EinsteinLLM.generateMessagesForPromptTemplate`. The developer's test registers an `HttpCalloutMock`; when that does nothing, they try the Stub API. What actually works? <!--id:core-apex-030-->
?
Neither. A `ConnectApi` call is not an HTTP callout, `EinsteinLLM` publishes no `setTest*` methods, and the Stub API can't stub a static method in a namespace you don't own. The only route: wrap the call behind your own interface (an `LlmGateway`), inject a fake at a `@TestVisible` seam, and assert which template and inputs were passed, not the generated text.
Hint: is it a callout, and can you subclass it?
Trap: branching on `Test.isRunningTest()` inside the class, or asserting on the generated text.
Source: [Testing AI Apex & Mocking LLMs](../../SF_core/02-apex-and-triggers/34-testing-ai-apex-and-mocking-llms.md) · [Invoking Prompt Templates from Apex](../../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md)

### Design, interop & AI

An invocable action's input class has worked for years. Last sprint someone added `public Input(Id orderId)` for convenience. It compiles and deploys, but the action now fails at runtime in Flow and in the agent. Why? <!--id:core-apex-031-->
?
Declaring a constructor with arguments removes the compiler's default no-arg constructor. The platform creates the input object itself, and from API 66.0 it needs a visible no-arg constructor; a Release Update enforces it in Summer '26. Add `public Input() {}` back, and make it `global` if callers sit outside the package.
Hint: who creates the input object?
Trap: expecting a compile error, or calling it "a 67.0 change".
Source: [Invocable Apex & Agentforce Actions](../../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)

Code review. A tax calculator is chosen per org from custom metadata. In one org the save fails with a `NullPointerException` on the `newInstance()` line. What is wrong, and what risk does this design carry? <!--id:core-apex-032-->
```apex
Tax_Setting__mdt s = Tax_Setting__mdt.getInstance('Default');
Type t = Type.forName(s.Implementation_Class__c);
return (TaxCalculator) t.newInstance();
```
?
The class name in the record is wrong, or the class was renamed. `Type.forName()` returns **null** for an unknown class instead of throwing, so the error appears one line later. Check for null and throw a clear message; in a managed package use `Type.forName(namespace, className)`. The risk: the binding is a string, so renaming or deleting the class deploys cleanly and breaks in production.
Hint: what does `Type.forName` return for a name it can't find?
Trap: debugging `newInstance()` or the implementation class.
Source: [Dependency Injection & Pluggable Apex](../../SF_core/02-apex-and-triggers/28-dependency-injection-and-pluggable-apex.md)
