# Core Platform — Integration & Async

> Area: Core Platform · Set 03 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the distributed-systems layer integration reviews actually fail on. **Most integration defects are pattern errors, not API errors** — and the two facts underneath the whole set are that a timeout is not a failure, and that every event bus here is at-least-once.

---

### Q1 · "Can we use Pub/Sub?"

**Level:** Medium · **Probes:** [Integration patterns & selection](../../SF_core/06-integration-and-apis/01-integration-patterns-and-selection.md) · [Callouts, named credentials & HTTP in Apex](../../SF_core/02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) · [Async Apex overview & choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md)

**Scenario.** A client's requirement: "when an opportunity closes, tell the ERP." Their architect has asked whether you can use Pub/Sub API, because that is what their last integrator recommended. Their current implementation is an HTTP callout from a `@future(callout=true)` method invoked by an after-update trigger. It works. Volume is around 400 closures a day. The ERP team says their endpoint is sometimes down for maintenance windows of up to two hours, and closures are currently lost when that happens.

**Asked as:** "They asked about an API. What do you ask them?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Integration questions arrive as products and have to be answered as **patterns**. Before naming any API, three properties of the requirement fix the answer: **who initiates**, **whether the caller waits**, and **how many records move**. Here: Salesforce initiates, the caller does not wait, and volume is trivial. That is **fire-and-forget**, and the real problem is not the transport at all — it is that there is no durability across the ERP's maintenance windows.

**Then work through.**
- **What is actually wrong with the current build.** Nothing, at 400 a day — and that is worth saying, because the existing implementation is a reasonable fire-and-forget. The defect is narrow: a `@future` callout that fails during a two-hour outage has nowhere to go, so the closure is lost. That is a missing **retry and dead-letter path**, not a wrong API.
- **Where Pub/Sub does and does not fit.** Pub/Sub API is the recommended *transport* for events in new work, and it is the right answer if the ERP is willing to be a **subscriber** — then Salesforce publishes `OpportunityClosed__e`, the ERP consumes it, and the maintenance window stops mattering because events sit in the bus. If the ERP can only receive an HTTP call, Pub/Sub is irrelevant and you need durable retry on the Salesforce side instead. **So the question to ask the client is about the ERP team, not about Salesforce:** can they subscribe, or only receive?
- **If they can subscribe, design the event properly.** Small, self-describing, about a business fact — `OpportunityClosed__e`, carrying the record ID and what changed rather than the whole record, because the payload is a **published contract** that cannot be narrowed once anything subscribes. Include an idempotency key and a timestamp; neither is provided in a form you should depend on. Use **Publish After Commit** so a rolled-back save publishes nothing. And know the retention: **three days**, which comfortably covers a two-hour window and does not cover a long holiday outage.
- **If they cannot subscribe, the fix is smaller than a re-architecture.** Move from `@future` to a **Queueable**, which is the default async choice and can chain — so a failed callout can enqueue a retry with backoff. Add a dead-letter record for anything that fails *n* times, and an alert on it. **A dead-letter path is mandatory:** something must hold the message that failed repeatedly, and with no alert an integration fails invisibly for months.
- **And name the pattern smell in the current code, since it is the transferable lesson.** A trigger that calls out needs `@future(callout=true)` or a Queueable to compile at all. That requirement **is the platform telling you the pattern is wrong** — a synchronous callout in a trigger is fire-and-forget written as request-reply. Here it was handled correctly, which is why it works; the point is that the compiler error is a design signal rather than an obstacle.

**The trap.** Answering the question asked — yes or no on Pub/Sub. Either answer commits to a transport before establishing that the ERP can consume it, and neither addresses the lost closures, which is the only thing actually broken. The related trap is over-correcting into middleware: **middleware does not remove the pattern choice, it relocates it.** MuleSoft calling Salesforce still picks one of the same six patterns, and adding it here buys nothing the Queueable-plus-dead-letter does not.

**Follow-ups they will ask.**
- "Why is 'real time' ambiguous?" — because it is two requirements. *Sub-second, caller blocked* is request-reply. *Eventually, within seconds, caller free* is an event. People almost always mean the second, and it is a completely different design.
- "What if volume grew to 400,000 a day?" — then the pattern is unchanged but the implementation is not: watch the event bus allocations, and for bulk reconciliation rather than per-record notification, Bulk API 2.0 is the batch-sync answer.
- "Could they poll instead?" — polling is not an integration pattern, it is the absence of one, and it burns API requests against the org's 24-hour limit for nothing.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Reframes from API to pattern with the three properties, identifies durability as the real defect, makes the answer conditional on whether the ERP can subscribe, and prescribes a dead-letter path with an alert |
| 🟡 Partial | Identifies fire-and-forget and proposes platform events, but does not check whether the ERP can subscribe, or omits the retry/dead-letter gap |
| 🔴 Weak | Answers yes or no on Pub/Sub; or proposes middleware; or rewrites the callout without addressing the lost records |

**Ask this if they stall:** "During the two-hour window, where should the closure sit? Which of your options has somewhere to put it?"

</details>

---

### Q2 · An event for a record that never existed

**Level:** Complex · **Probes:** [Platform Event design](../../SF_core/06-integration-and-apis/12-platform-event-design.md) · [Idempotency, retries & error handling](../../SF_core/06-integration-and-apis/23-idempotency-retries-and-error-handling.md) · [Order of execution & recursion](../../SF_core/02-apex-and-triggers/07-order-of-execution-and-recursion.md)

**Scenario.** A fulfilment integration consumes `OrderPlaced__e` and creates a shipment in a warehouse system. Twice this month the warehouse has shipped against an order that does not exist in Salesforce. The event is published from an Apex service using *Publish Immediately*, chosen deliberately two years ago "so we never lose an event." The publishing transaction also does DML on `Order` and a related `Payment__c`, and a validation rule on `Payment__c` occasionally fires. The consumer is a Pub/Sub client that persists its replay ID on receipt.

**Asked as:** "Two phantom shipments. There are two defects here — find both."

<details><summary><b>Model answer</b></summary>

**Lead with.** Two independent defects. **Publishing is not transactional with DML** — *Publish Immediately* fires regardless of outcome, and **a rollback does not recall it** — so when the validation rule fails, the order never persists and the event has already gone. And separately, the consumer persists its replay ID **on receipt** rather than after processing, which means it can lose work on a crash and cannot replay correctly.

**Then work through.**
- **Defect one, and the fix.** *Publish After Commit* fires only if the transaction commits, so a rolled-back save publishes nothing. That is the behaviour the design wanted. The original reasoning — "so we never lose an event" — solved a problem that was not there and created this one: after-commit does not lose events for transactions that succeeded, and events for transactions that failed are events you must not send. *Publish Immediately* is useful for logging an attempt and dangerous for anything else.
- **Where the same trap hides elsewhere.** A composite request with `allOrNone` failing does not recall an immediately-published event either. And `allOrNone` **defaults to false** on composite, which returns HTTP 200 with failures buried in the body — a client checking the status code reports success. Worth auditing if anything else in this integration writes through composite.
- **Defect two, and why it is separate.** A replay ID marks "I have seen up to here." Persisting it **on receipt** means a consumer that crashes mid-processing restarts *past* work it never completed. It must be persisted **after processing**. This has not caused the phantom shipments, and it will cause silently missing ones.
- **The third thing to fix even though nobody asked.** Delivery is **at-least-once**, not exactly-once, so the consumer will eventually see the same event twice and must be idempotent. A dedupe key in the payload is the standard answer, and it needs to be *in* the payload because nothing usable is provided for you. Two phantom shipments today; duplicate shipments are the same class of incident waiting on a redelivery.
- **Then the framing that makes this reviewable rather than a bug list.** Correctness comes from the **receiver**, not the sender. A sender that retries or redelivers is behaving correctly; a receiver that cannot recognise a repeat, or that acknowledges before it has done the work, is the defect. Every mechanism here is a way of making a repeated or replayed message cheap and safe rather than a way of preventing one.
- **And the operational gap.** **Nothing tells a publisher that a subscriber failed.** Silent divergence is the default failure mode of this whole pattern, which is why subscriber-side monitoring and a dead-letter path are not optional — with three-day retention, "blocked" becomes "lost".

**The trap.** Fixing the publish behaviour and stopping, because it is the defect that produced the reported symptom and the fix is a one-field change. The replay-ID bug produces the opposite symptom — *missing* shipments rather than phantom ones — so it will be investigated separately, months later, as an unrelated problem. The second trap is treating "we never lose an event" as a requirement to preserve and reaching for something clever to keep immediate publishing; the requirement was always "never lose an event for an order that exists", and after-commit satisfies it exactly.

**Follow-ups they will ask.**
- "How would you have caught the phantom orders sooner?" — you cannot query past events, so if it must be auditable you write a record as well. An `Order` with no matching audit row is a queryable reconciliation check.
- "Anything to check on the subscriber's Apex, if it were Apex?" — event triggers are bulk by construction: the subscriber receives a batch, never one event, and code written for one is the classic defect. At 67.0 Apex subscriber triggers also default to user mode, so a subscriber that quietly processed everything may now process a subset without erroring.
- "What if they had used a Flow subscriber?" — it cannot be tuned. There is no Flow equivalent of `PlatformEventSubscriberConfig`, so it takes the 2,000 default batch size, and it cannot call subflows. Flow's triggered types also still run in system context without sharing, so the same subscriber logic is *more* permissive in Flow than in Apex.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Finds both defects unprompted, states that publishing is not transactional with DML and that a rollback does not recall an immediate publish, corrects replay-ID persistence to after-processing, and adds idempotency for at-least-once delivery |
| 🟡 Partial | Diagnoses the publish behaviour correctly and fixes it, but misses the replay-ID bug or treats at-least-once delivery as exactly-once |
| 🔴 Weak | Blames the validation rule or the warehouse system; or proposes a reconciliation job as the primary fix; or wants to keep immediate publishing |

**Ask this if they stall:** "The validation rule fires and the transaction rolls back. What happens to the event that was already published?"

</details>

---

### Q3 · The partner retries

**Level:** Medium · **Probes:** [Idempotency, retries & error handling](../../SF_core/06-integration-and-apis/23-idempotency-retries-and-error-handling.md) · [REST API fundamentals](../../SF_core/06-integration-and-apis/04-rest-api-fundamentals.md) · [Bulk API 2.0](../../SF_core/06-integration-and-apis/07-bulk-api-2.md)

**Scenario.** A partner posts orders into a custom Apex REST endpoint. During a peak week, 240 duplicate orders appeared. The partner's logs show they received timeouts and 503s and retried on a fixed 5-second interval, sometimes several times. Salesforce logs show every request succeeded. The partner's position is that Salesforce was too slow. Your client's position is that the partner double-posted. Both are adamant, and the client wants you to confirm the partner is at fault.

**Asked as:** "Who is at fault, and what do you actually change?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Neither, in the sense that will help — and no, I would not confirm the partner is at fault. **A timeout is not a failure**: it tells the partner nothing about whether the work happened, so retrying was the correct thing to do. The endpoint accepting a repeat as a new order is the defect. Correctness has to come from the **receiver**.

**Then work through.**
- **What the logs actually reconcile to.** "Every request succeeded" and "we got timeouts" are both true. The work committed and the response was lost — which is the textbook shape of this incident. **Retrying a non-idempotent `POST` is how duplicate orders happen: the first call succeeded, only the response did not arrive.**
- **The fix on the Salesforce side.** An **idempotency key** the partner sends on every attempt, stored against a **unique external ID**. The uniqueness constraint does the deduplication and `DUPLICATE_VALUE` is the signal to return the first result instead of creating a second order. That is the idiomatic implementation here and it is a small change. Where the shape allows it, **upsert on an external ID is idempotency you get for free** — `PATCH` run twice leaves one record.
- **Give the dedupe key an expiry from day one.** A dedupe table with no retention policy becomes the largest object in the org.
- **The fix on the partner side, which is a real ask and not a deflection.** Fixed-interval retries from many clients **re-converge into the same spike that caused the failure**. Exponential backoff with jitter. And they should **classify before retrying**: a `429`, a `503`, a `REQUEST_LIMIT_EXCEEDED` or an `UNABLE_TO_LOCK_ROW` is retryable; a `400`, a validation failure or `INVALID_FIELD` is not — retrying those burns the allowance and never succeeds.
- **Then investigate why there were timeouts at all**, because the duplicates are the symptom and the slowness is the cause. Peak-week 503s point at the org's API request limit — which is **per 24 hours and org-wide**, so one badly-behaved integration degrades every other one — or at row lock contention on a shared parent, which surfaces as apparently random failures.
- **How to handle the client.** They asked for ammunition and the useful answer is a fix. Frame it as: the partner's retry behaviour is improvable and the endpoint's contract is the thing that made retries dangerous, and only one of those two is under the client's control. That is a better position going into the partner conversation than a blame finding, because it comes with something they can ship.

**The trap.** Confirming the client's position. It is what was asked for, the logs superficially support it, and it produces a blame conclusion instead of a fix — leaving an endpoint that will duplicate again on the next slow week regardless of what the partner changes. There is a mirror trap in being asked to adjudicate at all: this is not primarily a fault question, and answering it as one accepts a framing where the actual defect never gets named.

**Follow-ups they will ask.**
- "How do you find the historical duplicates?" — group by the natural business key and look for repeats within a short window; the timestamps clustering seconds apart is the signature.
- "What if they had used composite?" — `allOrNone` defaults to **false**, so the request returns HTTP 200 with failures buried in the body, and a client checking the status code reports success. Its own class of silent divergence.
- "And on Bulk?" — `JobComplete` means processing finished, not that records succeeded. You have to read the failed-results file.
- "What is the worst outcome of all of this?" — silent success. An integration with no alert on its dead-letter path fails invisibly for months.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | "A timeout is not a failure", declines to assign blame, puts correctness in the receiver with the unique-external-ID pattern, asks the partner for backoff-with-jitter and error classification, and investigates the underlying slowness |
| 🟡 Partial | Explains that retries caused it and proposes deduplication, but frames it as the partner's fault or omits the backoff and classification asks |
| 🔴 Weak | Confirms the partner is at fault; or proposes a nightly dedupe job as the fix; or tells the partner to stop retrying |

**Ask this if they stall:** "The partner's request timed out. Do they know whether the order was created?"

</details>

---

### Q4 · More async 🆕

**Level:** Complex · **Probes:** [Async Apex overview & choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md) · [Queueable Apex & chaining](../../SF_core/02-apex-and-triggers/13-queueable-apex-and-chaining.md) · [Batch Apex & stateful processing](../../SF_core/02-apex-and-triggers/14-batch-apex-and-stateful-processing.md)

**Scenario.** A nightly enrichment process hits `Too many SOQL queries: 101`. A developer's fix, already in a pull request, moves the work into a Queueable enqueued per record from the trigger — "async gets fresh limits." In review you note: the org processes around 80,000 records nightly, has three other scheduled jobs, and the same trigger fires during a daytime bulk load. The developer's test passes and shows the Queueable running correctly. Someone else on the team says elastic limits make the whole concern obsolete now.

**Asked as:** "Three things wrong with that PR. What are they?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The fix misunderstands what async buys you. **Going async is not a way to get more governor budget — it is a way to get another transaction**, with its own budget and its own failure. And enqueuing per record turns one limit problem into three worse ones.

**Then work through the three.**
- **One: the flexible queue.** Only **100 unstarted jobs** sit in it; past that `System.enqueueJob` throws. A trigger enqueuing per record over 80,000 records will hit that almost immediately — a burst of trigger-driven enqueues is the textbook way to hit it. The correct shape is one Queueable **per chunk**, or Batch Apex, which exists precisely for a record set too large for one transaction.
- **Two: the shared daily ceiling.** 250,000 executions per 24 hours, or 200 × user licences, whichever is greater — and it is **shared** across `@future`, Queueable, batch chunks and scheduled runs. 80,000 nightly enqueues plus three other scheduled jobs is a budget conversation, and the daytime bulk load draws on the same pool.
- **Three: the original problem is not solved.** Async is **not a limit reset for the transaction that queued it**. Enqueuing costs you nothing back; the synchronous trigger transaction still has to finish inside its own budget. If the 101-query error is coming from a loop in the handler, moving the work does not fix it — the real fix is bulkification: collect the keys, query once outside the loop, look up inside it.
- **Now the elastic-limits claim.** Partly true and it does not rescue this. 🚩 **Elastic limits are Beta at 67.0**: `Queueable` and `@future` jobs can be enqueued up to *twice* the licensed daily limit, with the overflow **throttled rather than rejected**. That changes the failure mode from a hard `LimitException` at the enqueue site to slower execution — better for the user, and worse for anyone relying on the exception as a signal that something has gone into a loop, which is exactly this situation. It also does nothing about the 100-job flexible queue. Track `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` in `System.OrgLimits.getMap()` rather than assuming headroom, and do not build on Beta behaviour as a limit strategy.
- **Why the passing test proves almost nothing.** `Test.startTest()`/`stopTest()` runs queued async work **synchronously**, so tests never exercise ordering, delay or concurrency. A passing test proves the code runs, not that the design is sound. That sentence is worth saying verbatim in a review.
- **What the PR should be.** Fix the bulkification first and see whether async is needed at all. If the work genuinely exceeds one transaction, Batch Apex for the nightly 80,000; a chunked Queueable if it needs typed state and chaining. And the first question before either: **does this work have to be atomic with the user's save?** If yes it stays synchronous and must fit. If no, the choice follows from the shape of the work.

**The trap.** Accepting "async gets fresh limits" as the premise and reviewing only the implementation. It is half-true — async transactions do get bigger limits, 200 SOQL queries, 12 MB heap, 60,000 ms CPU — which is what makes it persuasive, and none of it applies to the transaction doing the enqueuing. The DML statement limit does not move at all. The second trap is letting the elastic-limits comment close the discussion: a Beta feature that converts a hard failure into throttling is not a fix for a design that enqueues 80,000 jobs.

**Follow-ups they will ask.**
- "What do you lose by going async?" — atomicity with the user's save, the ability to report back synchronously, and any ability to reason about ordering. There is **no ordering guarantee between independent async jobs**; if order matters, chain them.
- "How do you monitor it?" — `AsyncApexJob` is the audit trail for everything except platform events, and it is queryable. A failure alert is a SOQL query, not a support ticket.
- "Who finds out when an async job fails?" — by default, an email to the last person who edited the class, which is nobody's monitoring strategy. Transaction finalizers are the mechanism for handling it properly.
- "Why not `@future`?" — it cannot take an sObject argument, cannot chain, and holds primitives only. Queueable is the default async choice.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Rejects "async gets fresh limits" for the enqueuing transaction, names the 100-job flexible queue and the shared 250,000 daily ceiling, insists on bulkification first, and treats elastic limits as Beta and irrelevant to the queue ceiling |
| 🟡 Partial | Spots the per-record enqueue as wrong and proposes Batch Apex, but accepts that async solves the limit problem, or does not challenge the elastic-limits claim |
| 🔴 Weak | Approves the PR; or debates Queueable vs `@future` without addressing the per-record enqueue; or accepts the passing test as evidence the design works |

**Ask this if they stall:** "The trigger enqueues one job per record. Eighty thousand records. How many jobs can sit unstarted in the queue?"

</details>
