# Core Platform — Sharing & Security

> Area: Core Platform · Set 02 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the access model after it stopped being a pure union and after Apex and Flow stopped agreeing with each other. Every answer in this set turns on one question — **whose access is being enforced here, and is it being enforced at all?**

---

### Q1 · Same logic, two builders ⚠️🆕

**Level:** Complex · **Probes:** [Code execution context & security](../../SF_core/07-security-and-sharing/14-code-execution-context-and-security.md) · [Flow run context & sharing](../../SF_core/04-flow-and-automation/19-flow-run-context-and-sharing.md) · [Apex security, user mode & FLS](../../SF_core/02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

**Scenario.** A compliance review asks a question your team cannot answer. The same requirement — "when a case closes, look up the account's credit record and stamp a risk field" — exists twice in the org: once as Apex in a trigger handler compiled at 67.0, once as a record-triggered flow built last month by the admin team for a different record type. Security's question: "are these two equivalent from an access-control standpoint?" A senior developer has answered yes, on the basis that both are automation and automation runs as an administrator.

**Asked as:** "Is the developer right? And which of the two would you rather explain to an auditor?"

<details><summary><b>Model answer</b></summary>

**Lead with.** They are not equivalent, and the developer's reasoning is wrong in both directions. "Automation runs as an administrator, so the access model is a UI concern" was the standard answer for a decade and is now false. **At 67.0 Apex defaults to user mode and `with sharing`** — it enforces the model unless told not to. **Flow's triggered types did not move**, and still run in system context without sharing, with no setting that changes it. The safe-by-default assumption has **swapped sides**: the same logic is now more permissive built in Flow than built in Apex.

**Then work through.**
- **What each one actually does.** The Apex handler queries the credit record under the running user's object permissions, FLS and sharing — so it may legitimately return nothing and stamp nothing. The record-triggered flow reads whatever exists, regardless of who triggered the save. Same requirement, two different security postures, and the *more* permissive one is the one built by the admin team without a code review.
- **The auditor answer, which is the real question.** The Apex one, because you can state what it enforces and point at the version that makes it true. The flow's reach is not configurable and not obvious from looking at it — a record-triggered flow at 67.0 has exactly the reach it had in 2019.
- **The distinction that catches people out.** If someone offers Flow's *"System Context With Sharing"* as the fix, it is not one. It enforces **record-level sharing only** — object permissions and FLS are still bypassed. It is not Apex's `with sharing` and it is not user mode. And it is unavailable on the triggered types here anyway.
- **A second-order trap in the same org.** The API version that decides Apex behaviour is the one on **the class containing the query**, not the caller's. So a 67.0 service calling an older selector class gets system-mode SOQL from the selector. "Our handler is on 67.0" is not sufficient — check the class that holds the query.
- **What to actually recommend.** Consolidate: one implementation, invoked from both paths, with the access decision made once and documented. If the elevated read is genuinely required — a credit check that must not depend on the closing user's visibility — then make it explicit in Apex with `AccessLevel.SYSTEM_MODE` and a comment saying why. That is reviewable. The flow's identical behaviour is not, because nothing in it declares an intent.
- **Then say the thing the review actually needs to hear.** Whether elevated access is *right* here is a business question nobody has been asked. Right now the org has two different answers to it by accident, and the difference has never been decided.

**The trap.** Answering "yes, equivalent" — which is the intuitive answer, was correct for years, and is the reason this question is worth asking. The subtler trap is answering "no" and getting the direction backwards: assuming Apex is the more permissive one because code has historically been the thing that bypasses the model. At 67.0 it is the opposite, and getting the direction wrong in front of a security team is worse than not knowing.

**Follow-ups they will ask.**
- "Where does a trigger body sit?" — always system mode, and it can no longer declare an access mode at all. Which is why security-sensitive logic belongs in the handler, not the trigger.
- "How do you find every place this matters?" — inventory contexts, not classes: triggered flows, classes below 66.0, unexplained `AccessLevel.SYSTEM_MODE`, and every `@AuraEnabled` method, since each one is an endpoint for anyone who can load the component.
- "What made Salesforce flip the Apex default?" — the platform stopped assuming the surface in front of it had already filtered the data, because that caller may now be an autonomous agent. It is a security change driven by agents, which is why it lands in this area rather than in Apex.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | States the flip and gets the direction right — Flow now more permissive than Apex — knows "System Context With Sharing" covers sharing only, raises the query-holding-class version rule, and turns it into a business decision about whether elevation is warranted |
| 🟡 Partial | Knows they are not equivalent and that Apex enforces more at 67.0, but cannot say what Flow's system context does or does not cover |
| 🔴 Weak | Agrees they are equivalent; or asserts Apex is the more permissive one; or offers "System Context With Sharing" as making them equal |

**Ask this if they stall:** "Both run without a person watching. Which one consults the sharing model, and which one cannot be made to?"

</details>

---

### Q2 · The audit says they can see it

**Level:** Medium · **Probes:** [Restriction rules](../../SF_core/07-security-and-sharing/11-restriction-rules.md) · [Auditing & troubleshooting access](../../SF_core/07-security-and-sharing/15-auditing-and-troubleshooting-access.md)

**Scenario.** A user raises a ticket: a custom object's list view shows 40 records, they expect around 300, and a report they built returns the same 40. An admin has checked everything on the grant side — profile, permission sets, OWD, sharing rules, role hierarchy — and a sharing audit confirms the user *does* have access to the missing records. Share rows exist. The admin has `View All Data` and can see all 300, and has concluded the list view is broken and wants to raise a case.

**Asked as:** "Share rows exist and the user still can't see the records. How?"

<details><summary><b>Model answer</b></summary>

**Lead with.** A **restriction rule**. It subtracts — it runs after everything else and filters the result down — so reading every grant no longer tells you what a user can see. The share rows genuinely exist; the user simply does not get the records back.

**Then work through.**
- **Why the audit was misleading rather than wrong.** A restriction rule filters the *result* of sharing, not the sharing itself. Nothing on the grant side reveals it, and a sharing audit will faithfully report access the user does not have. That is the defining characteristic and the reason this ticket ate an afternoon.
- **Why the object is a custom one, and why that is the clue.** Restriction rules apply to a **fixed list**: custom objects, external objects, Contract, Event, Quote, Task, Time Sheet and Time Sheet Entry. The core CRM objects — Account, Contact, Opportunity, Lead, Case — are not on it. A shrinking list view on a custom object is a candidate; the same symptom on Opportunity is not.
- **Why the admin's own view proved nothing.** **Admins are not exempt.** A restriction rule applies to users matching its criteria regardless of `View All Data` — the admin can see all 300 because they do not match the rule's user criteria, not because the rule does not exist. This is the first thing that confuses an admin debugging it.
- **Where to actually look.** The `RestrictionRule` metadata for that object. Restriction rules are built and deployed as metadata and manageable through the Tooling API, so they should be in source control — and if this one is not, that is a second finding.
- **The breadth to be aware of once found.** They apply to list views, reports, SOQL, **SOSL, search, lookups and related lists**. So this user's experience of the object is filtered everywhere, not just in the list view they reported. Worth checking whether anything else they use is quietly returning less. And user-mode SOQL respects them too — a 67.0 Apex class returns the filtered set where a system-mode query does not.
- **Then the correction to the mental model, because it is the reusable part.** "A user's record access is the union of everything that grants it" became incomplete at **Winter '22**. Three narrowing controls exist now: restriction rules subtract from record access, muting subtracts inside a permission set group, and queues stopped granting up the hierarchy by default. The summary sentence needs all three exceptions attached.

**The trap.** Raising the platform case, and more specifically believing the audit. A sharing audit answers "what grants exist" and the question being asked is "what will this user actually get back" — and since Winter '22 those are different questions. The related trap is checking whether the *admin* can see the records as a diagnostic; that tests the wrong user against the wrong criteria and produces a false all-clear.

**Follow-ups they will ask.**
- "Is there any indicator in the UI?" — none. Report and list-view results shrink without explanation; there is no "some records were hidden" message anywhere.
- "How is this different from a scoping rule?" — a scoping rule changes the *default view* without changing access, and reaches only list views, reports and SOQL. A restriction rule removes access and reaches search, SOSL, lookups and related lists as well.
- "What are the limits?" — two active rules per object in Enterprise and Developer, five in Performance and Unlimited. Low ceiling, and it is per object.
- "What if two rules match the same user?" — that is a design error, not a documented merge. One rule per object per user population.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names restriction rules, explains that they filter after sharing so the audit is answering a different question, uses "custom object" as the supporting clue, and knows `View All Data` does not exempt anyone |
| 🟡 Partial | Reaches restriction rules with a prompt, or knows they subtract but thinks admins are exempt |
| 🔴 Weak | Keeps auditing grants; or endorses the case; or uses the admin's own visibility as evidence the records are accessible |

**Ask this if they stall:** "Every mechanism the admin checked adds access. Is there anything in this model that takes it away?"

</details>

---

### Q3 · The test that will fail next year 🆕

**Level:** Complex · **Probes:** [Sharing recalculation & performance](../../SF_core/07-security-and-sharing/16-sharing-recalculation-and-performance.md) · [Groups, queues & the grantee model](../../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md)

**Scenario.** An onboarding process runs in Apex: create the user, insert a `GroupMember` row to add them to a public group, then query the records now shared with them to seed a personalised dashboard. There is a test that inserts the `GroupMember` and asserts on `RowCause = 'Rule'` share rows immediately afterwards. It passes. It has passed for three years. A colleague read a release note and thinks this code is a time bomb, but cannot say why, and the team is inclined to ignore it because the test is green.

**Asked as:** "Green test, three years in production. Is your colleague right?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Your colleague is right and the green test is the problem, not the reassurance. Salesforce now runs sharing recalculation **asynchronously** after group-membership and role changes when it judges that faster. Apex and Flow that update a group and then immediately act on newly-shared records will fail — and this code does exactly that, twice.

**Then work through.**
- **The timeline, because it decides urgency.** Rolled out from Summer '25, **fully enabled April 2026**, with a Release Update **available Spring '26 and enforced Spring '27**. So this is not hypothetical and it is not distant: the behaviour is already live and the enforcement date is fixed.
- **Why the test passes and production will not.** The platform decides **dynamically** — by data volume, ownership pattern and system load — whether to recalculate inline or in the background. A small sandbox recalculates inline every time. Production, at volume, will not. That is the failure mode in one sentence: **a passing test that later fails in production**, and it is unusually nasty because the test is not wrong, it is just measuring an environment that behaves differently.
- **Both documented breakages are present in this code.** A SOQL query or assertion for share rows with `RowCause = 'Rule'` fails when it expects them immediately — that is the test. And the seeding query after the `GroupMember` insert is the production half of the same assumption.
- **Do not trust `System.runAs()` as a workaround.** After the update it does not reflect the new access until the background work finishes. It is the obvious escape hatch and it is explicitly closed.
- **What to do, concretely.** Salesforce ships a ***Test asynchronous sharing recalculation in Apex tests*** flag — turn it on in a sandbox to force the new behaviour and watch the test fail, which is how you convert a colleague's suspicion into something the team will act on. Then restructure: the onboarding cannot assume access exists synchronously. Insert the membership, and defer the dashboard seeding — a Queueable or a scheduled step that runs once the shares exist, with the seeding tolerant of not-yet-shared records rather than asserting on them.
- **Then widen it, because this is never one class.** Audit anything that inserts a `GroupMember` and then asserts on or acts on access in the same transaction. Onboarding, territory realignment, role changes, any "add to group then do something" pattern.

**The trap.** Trusting the green test — which is precisely what the team is proposing, and it is a reasonable-sounding position. Deferring the work to Spring '27 is a second trap: the behaviour is *already* enabled and chosen by volume, so production can start failing at any growth threshold, with no deploy and no warning. The enforcement date is when the option to opt out disappears, not when the risk begins.

**Follow-ups they will ask.**
- "Why did Salesforce make it async at all?" — recalculation rebuilds physical share rows, which is a batch job. Nothing is computed at read time: the platform pre-materialises the answer so reads stay fast and pays for it at write time. Moving that off the synchronous path is a performance win everywhere except in code that assumed it was instant.
- "What would you use for a bulk realignment?" — **Defer Sharing Calculation**: suspend recalculation, make all the role and group edits, resume once. It pays the cost once rather than per change — it is not a way to avoid it, and the resume can run longer than the edits would have.
- "Which access feature never triggers recalculation?" — restriction rules, because they filter at runtime and create no share rows. Which is also why no share audit reveals them.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names the async recalculation update with the Spring '27 enforcement, explains that the platform chooses by volume so a small sandbox lies, knows `System.runAs()` is not a workaround, and reaches for the test flag to prove it before restructuring |
| 🟡 Partial | Recognises that sharing recalculation may be asynchronous and that the assumption is unsafe, but treats it as a Spring '27 problem or has no way to demonstrate it |
| 🔴 Weak | Trusts the green test; or adds a retry or a wait loop; or proposes `System.runAs()` to prove access in the test |

**Ask this if they stall:** "The test runs in a sandbox with fifty records. Production has six million. What might the platform do differently in each?"

</details>

---

### Q4 · The agent's running user

**Level:** Medium · **Probes:** [Code execution context & security](../../SF_core/07-security-and-sharing/14-code-execution-context-and-security.md) · [Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md) · [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md)

**Scenario.** A security review of an Agentforce build. The agent has six actions; two are Apex classes declared `without sharing` because "the agent needs to see everything to give a complete answer." The agent's running user has a permission set with `View All Data`. The Trust Layer is on, masking is configured, and the project lead's position is that the Trust Layer is the security boundary, so the running user's permissions are an implementation detail. The agent is customer-facing through an Experience Cloud site.

**Asked as:** "Sign it off or block it? And what is the one sentence that decides it?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Block it. The one sentence: **an agent has no access boundary of its own** — it runs as a user and inherits that user's access exactly. The Trust Layer governs the *model interaction*; it does not scope what the agent can reach or do. So the running user's permissions are not an implementation detail, they are the control.

**Then work through.**
- **What the Trust Layer does and does not do.** It masks PII outbound, demasks and scores inbound, defends against injection at the prompt boundary, and logs everything. It does **not** scope actions, and it does **not** fix an over-permissioned running user. An agent with an over-permissioned running user is insecure no matter how good the Trust Layer is — masking PII in the prompt does not stop a badly-scoped action from reading or writing what it should not.
- **Why `View All Data` plus `without sharing` is the finding.** Two independent bypasses stacked on a customer-facing surface. Under 67.0 defaults the platform would have enforced the running user's access automatically; both of these deliberately opt out of that. And the reasoning given — "needs to see everything to give a complete answer" — is a *product* preference stated as a technical requirement. Nobody has asked whether a complete answer is appropriate for the person asking.
- **The three-layer framing to give the review.** Platform security governs who can see which records. The Trust Layer governs what reaches the model and what comes back. Agent design governs what the agent is permitted to do — which actions are exposed, guardrails, orchestration scope. This build has hardened the middle layer and disabled the outer one.
- **What "an unexplained `without sharing`" means in review.** It is a question, not automatically a defect. So ask it: for each of the two classes, what specifically does the running user need that they cannot be granted? Often the honest answer is one object or one field, which is a permission-set change rather than a blanket bypass. Where elevation genuinely is required, it stays — narrowed to the query that needs it, with a documented reason.
- **Then the amplification argument, which is what makes this urgent rather than tidy.** An agent inherits a user's access and **composes and aggregates far faster than a person browsing**. A permission set that was tolerable for a human who would never assemble those records is not tolerable for something that will. That is the stated reasoning behind the 67.0 flip, and it applies directly here.
- **Two more things to check while you are in there.** Customer-facing through Experience Cloud means asking whether the running user is appropriate for an external context at all. And confirm the six actions are idempotent — an agent retries after a timeout, so a non-idempotent write is a separate finding.

**The trap.** Accepting "the Trust Layer is the security boundary." It is confidently stated, it names a real feature, and it is the single most common misreading in this area — treating the Trust Layer as *the* security answer when it governs one layer of three. The mirror trap is blocking on the presence of `without sharing` as automatically wrong; sometimes elevated access is correct, and a review that cannot distinguish a justified bypass from an unjustified one gets ignored.

**Follow-ups they will ask.**
- "What is the primary access control for an agent, then?" — the running user's permissions. Under user mode at 67.0 that is the control, not the code.
- "Does the answer change if the agent is internal-only?" — the severity drops, the principle does not. Internal is not a boundary; it is a smaller population.
- "Same question for a hosted MCP server?" — the same exposure, wider door. Custom hosted MCP servers respect the org's full sharing and security model, which is the good news — but who can create one belongs on a security review checklist rather than in a developer's discretion, because they expose org data to external AI clients.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | "An agent has no access boundary of its own", separates the three layers, treats `without sharing` as a question to be answered per class rather than a blanket defect, and raises the aggregation-speed argument |
| 🟡 Partial | Blocks it and identifies the over-permissioned running user, but accepts the Trust Layer as covering the model interaction *and* the access model, or rejects `without sharing` categorically |
| 🔴 Weak | Signs it off on the strength of the Trust Layer and masking; or focuses only on the Trust Layer configuration; or treats the running user as an implementation detail |

**Ask this if they stall:** "Masking is working perfectly. One of those actions deletes records. What has masking done about that?"

</details>
