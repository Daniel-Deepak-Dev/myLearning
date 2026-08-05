# Phases for 04 · Flow & Automation

27 topics across 3 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs after Apex (phases 03–07)** because Flow notes reference governor limits and invocable Apex signatures. Don't reorder.

> **The area grew from 21 to 23 at phase-08 plan time**, and phase 09's block was renumbered from 12–21 to 13–23. This was safe because none of those files existed and **nothing in the vault links to area 04 by number** — every cross-link points at `INDEX.md`. Verified by grep before the change.

> **It grew again to 25 at phase-09 plan time, and this renumber was *not* free.** Two topics were inserted at 19 and 20, pushing the old 19–23 to 21–25. By then files 01–12 *did* link forward by number and three other areas linked in by number. It was done anyway because the phase-08 debt sweep had to touch exactly those links in the same run — the marginal cost was one extra grep. **Do not renumber this area again without one.**

---

## Phase 08 — Flow fundamentals → Apex interop · 12 files ✅

```
01-automation-landscape-and-tool-selection.md          ⚠️
02-flow-anatomy-and-builder-basics.md
03-record-triggered-flows.md
04-screen-flows-and-ux-design.md
05-reactive-screen-flows.md                            🆕
06-scheduled-and-autolaunched-flows.md
07-platform-event-and-async-path-flows.md
08-subflows-and-modular-flow-design.md
09-collections-loops-and-the-transform-element.md      🆕
10-fault-paths-and-custom-errors.md                    ⚠️ ← flag added at plan time
11-flow-and-apex-interop.md
12-http-callout-and-external-services-in-flow.md       🆕 ← added at plan time
```

**One file added before the run, appended** so no planned number moved: **12** closes the largest hole in the taxonomy — nothing in 01–21 owned calling an API from Flow without Apex, a capability GA since **Winter '24**. It is also the natural counterweight to 11: the note's job is the boundary, not the recipe.

**A second addition went to phase 09 instead.** *Trigger order & Flow Trigger Explorer* is a scale question — what happens when five flows sit on one object — so it sits next to the limits note at **14** rather than crowding **03**.

### Retro

**⚠️ — the plan's headline correction was itself wrong, and it was wrong in five other files**

- **01 — the plan said "Workflow Rules and Process Builder are retired." They are not.** Salesforce KB `001096524` is explicit: *"Your active Workflow Rules and Process Builder processes continue to run as they do today, even after 2025."* Support ended **31 December 2025** — no bug fixes, no support cases — and **no retirement date has been announced.** Creation was blocked in **Winter '23**. This is the same "old ≠ dead" distinction the vault already makes for Lightning Locker, `if:true`, `System.assertEquals`, page layouts and classic approvals, and it is now the fifth instance. The consequence is architectural, not cosmetic: **save-order steps 11 and 13 can still be occupied and executing**, so calling them "vestigial" sent debugging to the wrong place.
- **10 — a ⚠️ the plan did not give it, and it is the most useful finding in the run.** *"Add a fault path"* is error **reporting**, not error handling: **a fault path does not roll back the transaction.** Records already written stay written. The **Custom Error element (Winter '24)** shows a message **and** rolls back; **Roll Back Records (Winter '22)** rolls back silently but is **screen-flow only** and reaches back only to the previous screen, because every screen boundary ends a transaction.

**🆕 the plan did not flag**

- **Reactivity is two mechanisms and the plan named one.** Reactive **components** went Beta Summer '23 → **GA Winter '24**, flow API **59.0+**; **Screen Actions** went Beta Spring '25 → **GA Summer '25** and are the half that can *fetch* rather than merely recalculate. UnofficialSF calls Screen Actions "the final piece of the reactivity journey" and the plan did not mention them at all. Four unsignposted limits persist: cross-object formulas are not reactive, formulas cap at **3,900 characters**, **a reactive change does not fire validation**, and reactivity is per-component. The API 57.0/58.0 back-port setting **expired in Winter '25**.
- **Transform is GA Summer '24, not "recent."** Beta Winter '24. Limits: **one nested collection** per transformation, **10 levels** of Apex-defined nesting. Spring '25 added multi-collection merge.
- **Summer '26 changed the Apex-action surface, which lands in 11 and 09** — **Formula Mode** and **Transform Mode** in the action property panel, **direct field-setting** for Apex-defined inputs, and the *Include* toggle replaced by **red asterisks** on required parameters.
- **Summer '26 items given a home rather than a file** — native **`Show Toast Message`** and **`Open a Page`** actions, Radio Button Group, Data Table lookup names as links, styling overrides on 11 more components, and **Send Email v3.0.1+ storing templates by name not Id** → **04**. **Custom batch size 1–200 for scheduled flows** → **06**. **~20 Decision date operators, DateTime unsupported** → **02**, **03**. Collapsible fault paths → **10**.
- **The `Show Toast Message` action closes a phase-07 loop.** [03-lwc · 18](../03-lwc-and-slds/18-error-handling-and-user-feedback.md) recorded that `ShowToastEvent` fails *silently* in LWR; in Lightning Experience a screen flow now needs no toast component at all.

**Other corrections made while writing**

- **A subflow does not start a new transaction.** One transaction, one SOQL budget, one DML budget, however deep the nesting — subflows buy maintainability and **zero** limit relief. Recorded in [../CURRENCY.md](../CURRENCY.md) as a myth correction because the opposite belief is widespread.
- **Platform event-triggered flows cannot call subflows at all**, and Flow has **no equivalent of `PlatformEventSubscriberConfig`** — the declarative subscriber takes the 2,000-message default and cannot be tuned. Sharpened by contrast with Summer '26 giving *scheduled* flows a batch size.
- **The Default Workflow User runs schedule-triggered flows**, which is the source of the "runs fine, processes nothing" failure when that account cannot see the filtered records.
- **Flow has no Map data type at all** — the seed note's `Map<String,Decimal>` observation generalises, and it is why so much Flow↔Apex plumbing looks clumsy.

**Seed harvest** · *the Notion connector held; one page found that the inventory does not list*

- **11** — `Flow Invocable Methods and Variable` (**2025**). → *harvested. Its sample code is unremarkable; its last line is not — `@InvocableVariable` fields don't support `Map<String,Decimal>`. Generalised in the note: **no map of any value type crosses the boundary, because Flow has no Map type.***
- **11** — **`Call Flow in Apex` (2023), which is not in [../\_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md).** → *harvested, and it supplies the direction the plan under-weighted: `Flow.Interview.createInterview(name, inputs)` plus `getVariableValue()`, with the page's own red callout — **autolaunched and user-provisioning flows only.** Worth adding to the inventory's Flow mapping.*
- **02** — `Flow Builder` (2023). → *harvested as an artefact rather than a note: a sixteen-item agenda with **one box ticked**. Two lines aged into answers — "use flow to make a callout" was unchecked because the feature was in beta (now **12**), and "`$Record` vs `$Record__Prior`" was a question with nothing under it (now **03**).*
- **08** — `Sub Flow`. → *re-read and confirmed **structure only** — a single YouTube embed, no prose, exactly as the inventory predicted. The callout in **08** is built on the one ticked box in the `Flow Builder` agenda instead.*
- **01, 03, 04, 05, 06, 07, 09, 10, 12 carry no `From my notes.` callout** — confirmed zero seed coverage. The corpus has three Flow pages total and two of them are 2023 stubs; reactivity, Transform, fault handling, HTTP callout and scheduled flows did not exist as concerns in it.

**Rule 1 exceeded deliberately, with approval.** The "retired" claim was corrected outside area 04 as well — [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) and [02-apex · 07](../02-apex-and-triggers/07-order-of-execution-and-recursion.md) — because leaving a known-wrong sentence in the currency file costs more than the sprawl. Precedent recorded here so it is visible.

**A vault defect found while verifying.** The post-phase line-count check used `Measure-Object -Line`, which **skips blank lines**: an 81-line file reported as 59, ~27% low, so the `-gt 85` gate was really at ~117 real lines and had never fired. Fixed in [../PHASES.md](../PHASES.md). All 12 files here are 60–64 real lines.

**Known debt — cleared in phase 09.** Files 01–12 linked forward to 13, 14, 18, 21 and 22 as `[NN · Title](INDEX.md)`. All are now real file links, and the two that moved (21 → 23, 22 → 24) were rewritten in the same pass.

---

## Phase 09 — Flow at scale · 13 files ✅

```
13-flow-limits-and-bulkification.md                ⚠️
14-trigger-order-and-flow-trigger-explorer.md            ← added at phase-08 plan time
15-flow-testing-and-debugging.md                   ⚠️   ← flag added at plan time
16-flow-orchestrator.md                                  (GA Spring '22)
17-approval-orchestration.md                       🆕⚠️
18-migrate-to-flow-and-legacy-retirement.md        🆕⚠️
19-flow-run-context-and-sharing.md                 ⚠️   ← ADDED at plan time
20-pause-wait-and-waiting-interviews.md            ⚠️   ← ADDED at plan time
21-flow-for-external-and-guest-users.md                  (was 19)
22-data-cloud-triggered-flows-and-data-actions.md  🆕    (was 20)
23-flows-as-agentforce-actions.md                  🆕    (was 21)
24-flow-deployment-versioning-and-governance.md    ⚠️   (was 22, flag added at plan time)
25-ai-assisted-flow-authoring.md                   🆕    (was 23)
```

**Two files added before the run, inserted rather than appended**, because both are foundational rather than advanced and the area is numbered in learning order. **19** closed the largest hole in the taxonomy: nothing in 01–23 owned *execution context*, and the one line that touched it (in **06**) was incomplete. **20** closed the second: no file in the area mentioned the **Wait** or **Pause** elements at all, in a 23-topic Flow area. Both carry a "the limit you read about was removed" correction, which is what tipped them over the bar.

### Retro

**⚠️ — the plan's framing for 17 was wrong, exactly as the plan itself suspected**

- **17 — "classic approval processes are in maintenance" is not a thing Salesforce has said.** The plan flagged its own framing as suspect and told the run to assume it was wrong until a primary source said otherwise. It was wrong, and in the same shape as the phase-08 "Workflow Rules are retired" error and the phase-06 "Locker is retired" error: **classic approvals are fully supported, the docs were renamed *Classic Approval Processes*, Flow approvals are a "modern alternative", and no retirement date exists.** [../CURRENCY.md](../CURRENCY.md) and [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md) already had this right from phase 02 — the phase-09 plan text regressed against the vault's own record. **This is the sixth instance of "old ≠ dead" in this build.** The real ⚠️ for 17 turned out to be better anyway: **Summer '25 made a flow approval process callable from *any* flow** via an invocable action, so approvals stopped being confined to orchestration-type flows.

**⚠️ the plan did not give, and the strongest finding in the run**

- **13 — the 2,000-executed-elements limit was removed in Spring '23.** It is the most-quoted Flow limit on the internet, it is still in current listicles, and it is **version-gated**: gone only for flows saved at **API 57.0+**, so an inherited flow at 55.0 keeps it. Removing it moved the failure to **CPU time at 10 seconds**, which has a far worse error message. This also made a sentence in phase 08's **09** stale — *"the element executions cap is one of the limits people actually hit"* — corrected in place.
- **15 — Flow Tests are much narrower than "Flow has tests now."** **Record-triggered flows only**, **immediate paths only**, **not delete**. Screen, autolaunched, schedule- and event-triggered flows have no automated test story at all, and **flow tests contribute nothing to Apex code coverage**. Summer '26's *Visualize Execution Path when testing screen flows* is a **debug-run** enhancement and does not extend Flow Tests — the release-notes headline reads as coverage and is not.
- **24 — `FlowDefinition` is no longer how you activate a version.** Since **Metadata API v44** only the latest version is retrievable and deployable, the `Flow` type carries its own `status`, and file names dropped version numbers. Pipelines built before v44 still do it the old way. Also concrete: **50 versions per flow**, and *Send Process or Flow Email to* in Process Automation Settings — which is the fix for phase 08's finding in **10** that error emails go to the last modifier.
- **20 — the org-wide paused/waiting interview cap was removed in Spring '23**, which is worse news than it sounds: nothing stops the accumulation, so nothing tells you it happened.
- **21 — `Run Flows` was removed from the Guest User profile** (new orgs Winter '22, all orgs Spring '23). Access is per flow via **Enabled Flow Access**. Every older tutorial's instruction is now impossible to follow.

**🆕 the plan under-specified**

- **22 — activation-triggered flows (January 2026)** were not in the plan. A Data 360 **activation** as a flow start node is a newer entry point than the Data Cloud-triggered flow the plan named, and it closed a real gap. The plan also conflated three mechanisms the note now separates: **Data Cloud-triggered flow**, **data action** (targets: platform event, webhook, Marketing Cloud Engagement) and **activation**.
- **25 — "describe-to-flow" is three capabilities, not one.** Flow Generation V2 (GA), natural-language *editing* of existing screen flows (GA Summer '26), and **flow summarisation**, which writes a generated description back into the flow's description metadata. The last one closes a loop with **23**: on an agent action that description **is** the contract another model reads.
- **19 — the default is not a context.** *How to Run the Flow* defaults to the literally-named **"Depends on How Flow is Launched"**, which is why published sources contradict each other about "the autolaunched default". The fixed fact is the other half: **record-, schedule- and event-triggered flows run in system context without sharing and cannot be changed.** Phase 08's **06** said only "inherits the caller's context" — sharpened in place.
- **Flow did not follow Apex's 67.0 security flip.** Apex defaults to user mode and `with sharing` at 67.0; Flow's triggered types did not move, so **the same logic is now more permissive in Flow than in Apex**. Recorded in [../CURRENCY.md](../CURRENCY.md) — it inverts the old "clicks are the safe option" assumption.

**Seed harvest** · *both mapped pages read, both substantive*

- **13** — `Limits based Things` (**2025**). → *harvested with an inline correction. Its numbers hold (CPU 10 s / 60 s, heap 6 MB / 12 MB) and its list of CPU-burn causes is good, but its recommendation — "convert Process Builder, flows to Apex Triggers if possible" — is the exact belief the note exists to correct.*
- **21** — `Flow Updates` (**2025**), which the inventory listed as unread and guessed might land in 18 or 23. → *it is neither: a **profile-by-profile audit of the `Run Flows` permission** in a production org. Harvested into 21, where it is the right exercise for internal profiles and impossible for guests since Spring '23.*
- **[../\_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) should be updated** — `Flow Updates` is mapped to the wrong destination there.

**Rule 1 exceeded deliberately, with approval** — two files added, and the renumber they forced touched **01-admin** (`12`, `14`, `INDEX`, `PHASES`) and **03-lwc** (`INDEX`) as well as files 01–12 here. All verified by grep after the change.

---

## Phase 24 — Reading and retiring the legacy tools · 2 files ✅

```
26-reading-inherited-workflow-and-process-builder.md   ⚠️
27-legacy-automation-migration-runbook.md              🆕
```

**Appended, not inserted, and this time the warning above was obeyed.** Phase 09 renumbered this area with live inbound links and left the instruction *"Do not renumber this area again without one [a grep]"*. Appending at 26–27 makes the question moot — no existing number moved, so no grep was needed. Same call phases 13, 15, 17, 20, 21 and 23 made.

**Why a maintenance phase at all.** A coverage grep — the phase-21 instrument — returned **zero hits across both vaults** for `WorkflowRule`, `evaluation criteria`, `Time-Based Workflow`, `workflow queue`, `time trigger`, `cross-object field update` and `immediate action`, while *Workflow Rule* and *Process Builder* appeared in **16 files**. This is the phase-22 defect — *a subject split across areas has no owner* — in a new form: **a subject mentioned constantly and owned nowhere.** Every one of those 16 mentions was a status correction; none taught the mechanics. The vault could say the tools still execute at steps 11 and 13 and could not help you read what was there.

### Retro

**⚠️ — the vault published a wrong sentence about the tool, and the error was directional**

- **18 said *"The tool does not deactivate the source… Deactivation is a deliberate, separate step."*** Both halves are wrong. The migrated flow is created **inactive**, and the tool ships a **Switch Activations** button that deactivates the rule and activates the flow **together**. The note therefore had the *direction* of the failure backwards: it warned about double-running, when the default outcome of a migration is **nothing changing** — correct flows sitting in Draft while the old rules carry on, a migration that reports success and alters no behaviour. Double-running is real but is the *second* trap, reachable only by activating the flow by hand. Fixed in the note body, in its Recall pair, and in one Gotcha. **This is the same failure class phase 19 named** — the vault's own prose, one release behind.

**🆕 the strongest finding, and it had zero coverage anywhere**

- **Deactivating a workflow rule does not empty the time-based workflow queue.** Pending time-dependent actions **remain and still fire** while the record meets criteria; they leave only when processed or when re-evaluation finds criteria false. Three consequences the vault had none of: they are visible **only** at Setup → Monitoring → **Time-Based Workflow**; **a rule with pending actions cannot be deleted at all**, which makes the queue a hard blocker on decommissioning and sets a migration's real end date; and **time-dependent actions cannot be added or edited on a deactivated rule that has pending actions**, which is how a half-migrated org gets stuck unable to move either way.
- **Winter '24 added a conditional that reads like a sweep.** *An at-rest pending time-based action is migrated to a scheduled path **when the associated record is changed**.* So pending actions on records nobody touches stay in the legacy queue indefinitely. Quoting the first half of that sentence would have been the phase-14 half-quote defect exactly.
- **Process Builder recursion has a number.** The *"Allow process to evaluate a record multiple times in a single save operation"* option permits **five** evaluations per transaction. The vault had the qualitative fact in 18 — migration silently drops recursion — without the quantity.
- **Time triggers are blocked on one evaluation criteria and it is not the intuitive one.** *created, and every time it's edited* cannot carry them — the record could requeue endlessly — while *created* and *created, and any time it's edited to subsequently meet criteria* both can. **The plan's own draft had this on the wrong row** and a verification search caught it before writing: rule 3 applied to a plan rather than to a release note, the same catch phase 23 recorded.
- **Creation-block dates are two dates, not one.** Workflow Rules **Winter '23**, Process Builder **Summer '23**. Phase 08 wrote *"with Process Builder following"*, which is true and unquotable; both INDEX and this file now carry the pair.

**Verified correct, changed nothing** — recorded because the plan expected defects and found none:

- **Help article `001096524` is the right citation** for end of support. The plan flagged a competing ID (`000389396`) surfaced by search and required the discrepancy be resolved before writing; the ID this vault has carried since phase 08 is the one Salesforce's own announcement links to. **A suspected date defect that turns out clean still needs recording**, or the next audit re-opens it.
- **No retirement date exists as of 2026-08.** Re-checked rather than inherited from phase 09, because the EOS date has now passed and that is precisely when a date would appear. It has not.
- **Migrate to Flow is GA** — Workflow Rules **Summer '22**, Process Builder **Spring '23**. Checked in the *inverse* of the phase-19 direction: the risk here was not a Beta assumed GA but a GA feature still labelled *(Beta)* in older write-ups, including the first one this run read.

**A research hazard worth naming.** Searching for workflow-queue behaviour surfaces **Oracle CRM On Demand** documentation high in the results, and it says the **opposite** — that deactivating a rule stops pending actions firing. Different product, same vocabulary. One draft of this run's headline finding was nearly reversed by it. **Check the host, not just the wording**, when one source contradicts three others.

**Cap pressure.** Both new files landed at **64 lines** and amended 18 at **65** — inside the area's 60–64 band. 27 wanted more: the inventory tooling was held to two lines and cross-linked to 09-devops and 10-soql rather than restated.
