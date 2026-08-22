# Core Platform — Apex, Triggers & Limits

> Area: Core Platform · Set 01 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** code that passes every test and is wrong at volume. Three of these four are invisible in a sandbox with one record and unmissable on the first real load — which is the definition of the class of bug this area exists to catch.

---

### Q1 · Nineteen thousand records, twelve updated

**Level:** Medium · **Probes:** [Order of execution & recursion](../../SF/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Bulkification patterns](../../SF/02-apex-and-triggers/08-bulkification-patterns.md)

**Scenario.** An `Opportunity` after-update trigger rolls a value up to the parent `Account`. It has a recursion guard — `private static Boolean hasRun = false;` set on entry — added two years ago to stop an infinite loop, and it worked. A data migration updates 19,000 opportunities via Data Loader. Afterwards, 12 accounts have correct rollup values and several thousand do not. No errors, no failed rows, the job reports complete success. Apex test coverage on the handler is 94%.

**Asked as:** "Clean job, no errors, wrong data. What did the guard do?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The guard is **per-transaction, not per-record**. The first chunk of 200 sets `hasRun = true`, and every subsequent record in that transaction is skipped silently. Data Loader sent 19,000 records in batches, so a handful of chunks did work and the rest were discarded with no error anywhere.

**Then work through.**
- **Why it looks like success.** Nothing threw. The guard's whole purpose is to make the handler return early, and it did exactly that — for records it had never seen. Silent correctness failure, which is why the migration reported clean.
- **The fix is to track Ids, not a flag.** Keep a `static Set<Id> processed`, remove already-processed Ids from the incoming map, return if nothing is left, and add the remainder before doing the work. That skips only what this transaction genuinely already did.
- **Why 12 succeeded and thousands did not.** The 12 are the accounts touched by whichever chunks ran before the flag was set within each transaction boundary. The pattern is arbitrary, which is a useful tell: arbitrary partial success on a bulk load usually means a per-transaction flag, not a data problem.
- **Why 94% coverage proved nothing.** Almost certainly a single-record test. The guard is correct for one record and wrong for 201, and coverage measures lines executed, not batch sizes exercised. The fix to the *test* is as important as the fix to the code: assert on a 200+ record insert.
- **The reframe worth stating.** The purpose of a recursion guard is not to prevent re-entry — re-entry is normal platform behaviour. A roll-up updating a parent or an after-save flow updating the record will legitimately re-run your trigger. The job of the guard is to make the second pass **cheap and idempotent**, not to block it.

**The trap.** Concluding the guard should be removed because it caused data loss. Remove it and the original infinite loop comes back — and the loop was real, which is why someone added the flag. The answer is a correctly-scoped guard, not no guard. The second trap is chasing this as a Data Loader batch-size problem and lowering the batch size to 1, which "fixes" it by accident and leaves a broken handler for the next caller.

**Follow-ups they will ask.**
- "What resets the static?" — the transaction boundary. Each batch chunk, each Queueable, each API call starts with an empty set, and that is correct: each is a separate transaction with its own budget.
- "Anything else to watch with the set-based guard?" — a guard set inside a `try` and never released blocks legitimate later work in the same transaction; clear it in `finally` if the operation can be retried. And statics are **not** reverted by a savepoint rollback — the data goes back, the `processed` set does not.
- "Is there a hard ceiling regardless of the guard?" — yes, trigger stack depth is **16**, and exceeding it throws rather than looping forever.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names per-transaction vs per-record immediately, prescribes the `Set<Id>` guard, explains why the test suite could not catch it, and reframes the guard's purpose as making re-entry cheap rather than preventing it |
| 🟡 Partial | Identifies the static flag as the cause but proposes removing it, or does not connect it to the 200-record chunking |
| 🔴 Weak | Investigates Data Loader, the rollup logic or the data; or treats arbitrary partial success as a platform issue |

**Ask this if they stall:** "Data Loader sent 19,000 records. How many does the trigger see per invocation, and what is the flag's value on the second invocation?"

</details>

---

### Q2 · The trigger reads the wrong number ⚠️

**Level:** Medium · **Probes:** [Order of execution & recursion](../../SF/02-apex-and-triggers/07-order-of-execution-and-recursion.md) · [Order of execution — declarative view](../../SF/01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md)

**Scenario.** An `after update` trigger on `Account` reads a roll-up summary field, `Total_Open_Opportunity_Amount__c`, and writes a tier onto the account. It is consistently one save behind — the tier reflects the previous state, not the current one. Separately, a developer reports that a field their `before update` trigger sets is sometimes already populated with a different value when the trigger runs, and they suspect another trigger. There is one trigger on the object. The org migrated off Process Builder last year but has some legacy automation nobody has audited.

**Asked as:** "Two symptoms, one object, one trigger. Explain both."

<details><summary><b>Model answer</b></summary>

**Lead with.** Both are save-order facts rather than defects. The stale roll-up is because **roll-up summaries recalculate at steps 16–17, long after after-triggers run at step 8**. And the pre-populated field is almost certainly a **before-save record-triggered flow at step 3**, which fires *ahead* of every before trigger — so a flow may already have altered `Trigger.new` by the time the Apex sees it.

**Then work through.**
- **Correcting the mental model that causes both.** Any save-order list beginning "before triggers run first" is wrong. New declarative automation now lands at steps 3 and 14, which **brackets** your Apex on both sides rather than trailing it. That single change explains the second symptom entirely and makes re-entry more likely than under the old model, not less.
- **Fixing the roll-up read.** The after trigger cannot see a value that does not exist yet. Options, in order of preference: compute the aggregate in the trigger itself with a `COUNT`/`SUM` `GROUP BY` query rather than reading the roll-up field; move the tier logic to where the roll-up is current — a subsequent transaction, or a flow at step 14 if it can tolerate re-entry; or trigger the tier calculation from the child object's change instead of the parent's.
- **Confirming the flow.** Flow Trigger Explorer shows what is registered on the object and at which step. This is a two-minute check that the developer has not done because they were looking for another *trigger*.
- **The legacy automation matters and is the trap-adjacent detail.** Workflow Rules and Process Builder, at steps 11 and 13, went **out of support on 31 December 2025 but were not retired**. You cannot build new ones, and in an unmigrated org they still fire — between the after-trigger and the after-save flow. "Migrated off Process Builder last year" plus "legacy automation nobody has audited" is exactly the state where an unexplained value change is a surviving workflow rule rather than a ghost.
- **The one to state as a general principle.** Most "why did my trigger see the wrong value?" questions resolve the same way: the value is produced *later* in the pipeline than the code reading it. That single sentence answers this whole class.

**The trap.** Hunting for a second trigger, an unsaved change, or a race condition. There is one trigger and no race — the pipeline is a fixed, documented, deterministic twenty steps. Treating deterministic ordering as nondeterminism sends you looking for a concurrency bug that does not exist, and the fix that follows — a retry, a re-query, a `Database.setSavepoint` — makes the code worse without addressing either symptom.

**Follow-ups they will ask.**
- "Where is the record written, and where is it committed?" — written at step 7, committed at step 19. Everything in between is still discardable, so an unhandled exception at step 18 discards the step-7 write entirely.
- "What about a trigger asking whether a user can see the record?" — criteria-based sharing recalculates at **step 18**, so it is asking before the answer exists.
- "Same trigger twice in a debug log — bug?" — usually correct behaviour, not a defect. A step-14 flow or a step-16 roll-up re-entered the update path.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Places roll-ups at 16–17 and before-save flows at step 3 without hedging, knows Workflow/Process Builder are out of support but not retired, and generalizes to "the value is produced later than the code reading it" |
| 🟡 Partial | Knows roll-ups recalculate after after-triggers, and suspects a flow, but cannot place the steps or misses the legacy-automation possibility |
| 🔴 Weak | Looks for a second trigger or a race condition; or proposes a re-query loop; or asserts before triggers always run first |

**Ask this if they stall:** "Draw the save order from memory. Where does a roll-up summary recalculate relative to an after trigger?"

</details>

---

### Q3 · Null for some users 🆕

**Level:** Complex · **Probes:** [Bulkification patterns](../../SF/02-apex-and-triggers/08-bulkification-patterns.md) · [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Apex security, user mode & FLS](../../SF/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

**Scenario.** A textbook-correct bulkified handler: collect `AccountId` into a `Set<Id>`, one query into a `Map<Id, Account>`, look up inside the loop with `accounts.get(o.AccountId)`. It has run in production for three years. The class was recompiled at 67.0 last month as part of a wider upgrade. Since then, a support tier gets intermittent `NullPointerException`s from this handler, and sales users never do. The data is fine — every opportunity has a valid `AccountId`, and the accounts exist.

**Asked as:** "Same code, same records, different users. What changed?"

<details><summary><b>Model answer</b></summary>

**Lead with.** At 67.0, database operations default to **user mode**, so the bulk query now returns only the rows the running user can see. `accounts.get(o.AccountId)` is coming back null because of **sharing**, not because of missing data — which is why it is per-user and intermittent rather than universal.

**Then work through.**
- **Why the support tier and not sales.** Sales users can see the accounts they work; the support tier evidently cannot see some of them. The opportunities are visible to them, the parent accounts are not, and the handler assumed the query returned every Id it asked for.
- **The mechanical point that makes this a genuinely new failure mode.** `Map.get()` on a missing key returns **null**, silently — never an exception, never an empty value. That has always been true and has always been the reason to null-check a bulk lookup. What changed at 67.0 is that the null now has a *second meaning*: "no such record" or "the running user cannot see it." Same code, same data, different user.
- **So null-handling stopped being defensive coding and became a branch that needs a decision.** Three legitimate answers, and the right one is a business question rather than a coding preference: **skip** the record silently, which is right when the rollup is informational; **`addError()`** it, which is right when proceeding without the parent would write wrong data and the user should know; or **elevate that one query** with `AccessLevel.SYSTEM_MODE` and document why, which is right when the handler legitimately needs org-wide data to compute a correct result. Choosing "skip" because it stops the exceptions is how you get quietly wrong rollups.
- **The rest of the 67.0 checklist, since the class was recompiled.** Keyword-less classes now default to **`with sharing`** rather than inheriting the caller's context, so check what this class declares. `WITH SECURITY_ENFORCED` no longer compiles — it would have failed the deploy, but grep the wider codebase before the next one. And if this handler is invoked as an agent action with a custom Apex input type, that type needs a visible **no-arg constructor** (a requirement from **66.0**, auto-activated in Summer '26).
- **Name the organisational risk, because it is the real lesson.** These semantics apply to classes **compiled at 67.0**, so nothing breaks on upgrade day and older classes keep their old behaviour indefinitely. The trigger is somebody bumping an API version *for an unrelated reason* — exactly what happened in a "wider upgrade." That asymmetry deserves a written team convention: bumping the API version on a class that touches data is a security-relevant change and gets reviewed as one.

**The trap.** Fixing it with a null check and moving on. It stops the exception, and it silently changes behaviour for the support tier — their rollups are now computed from a subset of accounts and nobody will notice until a number is wrong in a report. The mirror trap is reaching straight for `SYSTEM_MODE` to restore the old behaviour: that is sometimes the right answer, but taken reflexively it discards an access control the platform deliberately turned on, and it should never be the fix chosen because it is the one that makes the symptom disappear fastest.

**Follow-ups they will ask.**
- "Is the platform's behaviour correct here?" — yes. Under user mode the running user's permissions *are* the access control. An action returning less may be correct for the first time.
- "Why `WITH USER_MODE` over the old keyword?" — it handles polymorphic fields like `Owner` and `Task.WhatId`, checks the `WHERE` clause and not just the `SELECT` list, and reports **every** FLS violation rather than only the first.
- "Would a trigger have the same issue?" — no, and that is its own trap: triggers now **always** run in system mode and cannot declare sharing or access modes. Which makes a trigger the wrong place for security-sensitive logic — push it into a handler where the mode is explicit.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Connects user-mode-by-default to a null map lookup, treats the null branch as a business decision with three named options, rejects a bare null check as silently wrong, and raises the API-bump convention |
| 🟡 Partial | Knows 67.0 changed access defaults and that sharing now filters the query, but resolves it with a null check or an unexamined `SYSTEM_MODE` |
| 🔴 Weak | Debugs the data or the `Set<Id>` collection; or blames the recompile without knowing what it changed; or adds a try/catch |

**Ask this if they stall:** "Every opportunity has a valid `AccountId` and every account exists. So why did the query not return them all?"

</details>

---

### Q4 · The query plan looks fine

**Level:** Complex · **Probes:** [Data skew](../../SF/08-data-modeling-and-large-data-volumes/10-data-skew.md) · [Record locking & concurrency](../../SF/08-data-modeling-and-large-data-volumes/12-record-locking-and-concurrency.md) · [Sharing recalculation & performance](../../SF/07-security-and-sharing/16-sharing-recalculation-and-performance.md)

**Scenario.** A logistics client's nightly integration has started failing intermittently with `UNABLE_TO_LOCK_ROW` on maybe 2% of rows. It has run for eighteen months without incident. Separately, an admin reports that reassigning a single account's owner "hangs" for several minutes. Storage looks normal. The Query Plan for the integration's main query shows an index being used with good selectivity. Nobody has deployed anything in six weeks, and record volume has grown about 15% over the year.

**Asked as:** "Two symptoms, nothing deployed, the query plan is clean. Where do you look?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Data skew, and the clean query plan is the diagnostic rather than an exoneration. Skew is **invisible to every performance tool**: the Query Plan looks fine, the index exists and is used, storage looks normal. What is wrong is the *shape* of the data — how unevenly it points — and the only fix is to change the shape.

**Then work through.**
- **The threshold and why 15% growth was enough.** Salesforce's working threshold is **10,000** — more than 10,000 child records under one parent, or more than 10,000 records of one object owned by one user. Past that, operations that are ordinarily per-record stop being per-record. Eighteen months of a stable integration and then intermittent failures is the signature of a parent or an owner crossing that line. And 10,000 is a working threshold, not a cliff: pain starts earlier under concurrency, so treat it as the number that starts the conversation.
- **Detect it with aggregates, not intuition.** `SELECT AccountId, COUNT(Id) FROM Contact GROUP BY AccountId HAVING COUNT(Id) > 10000`, and the equivalent grouped on `OwnerId`. That is the first thing to run, before any further theorizing.
- **Map each symptom to a type.** The lock contention on 2% of rows points at **account (parent-child) skew** or **lookup skew** — many records pointing at one target, so concurrent writes queue behind the same lock. The owner reassignment hanging points at **account skew's real cost**, which is the sharing recalculation: changing an account's owner forces the platform to re-examine every child record's sharing, walk the role hierarchy and rewrite share rows.
- **Where it almost certainly came from.** Skew arrives through **integrations, not through users**. A nightly load that attaches unmatched records to a bucket account — `Unassigned`, `Miscellaneous`, `Default Account` — or assigns everything to one API user, creates textbook skew. Eighteen months of accumulation against one bucket record is the most likely story here, and the integration is both the cause and the victim.
- **The fixes, cheapest first.** For ownership skew, the classic fix is to **take the owner out of the role hierarchy** — a user with no role does not trigger hierarchy-based recalculation, which removes most of the cost without redistributing a single record. For the bucket account, spread across several buckets. For the lock contention specifically, sorting the integration's payload by parent Id is usually more effective than retrying harder — `UNABLE_TO_LOCK_ROW` is retryable, but the fix is to stop contending.
- **And warn them about the reassignment itself.** Reassigning a skewed owner *is* the expensive operation. Do it off-hours, in batches, and consider Defer Sharing Calculation — which lets you make the role and group edits and pay for one full recalculation on resume, rather than one per change. It pays the cost once; it does not avoid it.

**The trap.** Trusting the clean query plan and moving on to look for a code or platform cause — which is the natural move, because the tool that would normally find a performance problem is explicitly telling you there isn't one. It is also why skew deserves its own diagnosis rather than being folded into query tuning. Two specific dead ends worth naming: **skinny tables do not help skew at all** — they reduce columns read, not distribution; and **deleting the skew does not immediately remove it**, because soft-deleted children still sit under the parent until purged.

**Follow-ups they will ask.**
- "Why is lookup skew the one people miss?" — nothing cascades and no sharing is inherited, so it never shows up in a query plan or a sharing report. It surfaces *only* as lock contention under concurrency, which reads as a random failure.
- "What if their OWD is currently Public Read/Write?" — then be worried about the future as well as the present. A public sharing model **hides** ownership skew until the day OWD is tightened, and the recalculation that follows can run for hours or days. Tightening an OWD is the most expensive single action in the sharing area; it gets scheduled, not done on a Friday afternoon.
- "Any other common skew victims?" — `Task` and `Event`. Converted leads and logged activities accumulate against a few records.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Reads the clean query plan as the tell, names the 10,000 threshold and the aggregate query to confirm, maps each symptom to a skew type, and offers the take-the-owner-out-of-the-role-hierarchy fix |
| 🟡 Partial | Suspects skew and proposes the aggregate detection query, but treats both symptoms as one mechanism or has no fix beyond redistributing records |
| 🔴 Weak | Tunes the query, proposes skinny tables or a custom index, or adds a retry loop for the lock errors; or attributes it to the 15% volume growth alone |

**Ask this if they stall:** "The query plan says the index is selective and it's being used. What kind of problem would that tool be unable to see?"

</details>
