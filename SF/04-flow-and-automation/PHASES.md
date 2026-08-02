# Phases for 04 · Flow & Automation

23 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs after Apex (phases 03–07)** because Flow notes reference governor limits and invocable Apex signatures. Don't reorder.

> **The area grew from 21 to 23 at phase-08 plan time**, and phase 09's block was renumbered from 12–21 to 13–23. This was safe because none of those files existed and **nothing in the vault links to area 04 by number** — every cross-link points at `INDEX.md`. Verified by grep before the change.

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

**Known debt** — files 01–12 link forward to 13, 14, 18, 21 and 22 as `[NN · Title](INDEX.md)`, which is correct while those files do not exist. Sweep after phase 09, exactly as phase 07 did for area 03.

---

## Phase 09 — Flow at scale · 11 files ⬜

```
13-flow-limits-and-bulkification.md                ⚠️   (was 12)
14-trigger-order-and-flow-trigger-explorer.md            ← added at phase-08 plan time
15-flow-testing-and-debugging.md                         (was 13, GA Spring '23)
16-flow-orchestrator.md                                  (was 14, GA Spring '22)
17-approval-orchestration.md                       🆕⚠️  (was 15)
18-migrate-to-flow-and-legacy-retirement.md        🆕⚠️  (was 16)
19-flow-for-external-and-guest-users.md                  (was 17)
20-data-cloud-triggered-flows-and-data-actions.md  🆕    (was 18)
21-flows-as-agentforce-actions.md                  🆕    (was 19)
22-flow-deployment-versioning-and-governance.md          (was 20)
23-ai-assisted-flow-authoring.md                   🆕    (was 21)
```

**⚠️ corrections to lead with**

- **13** — Flow is **not** exempt from governor limits. It shares the Apex transaction budget, and DML inside a loop is the classic production failure. Phase 08 established the patterns in **09**; this note owns the numbers. **Also correct the belief phase 08 found: a subflow shares the transaction and buys no relief.**
- **17** — Approval Orchestration is the modern path; classic approval processes are in maintenance. **State the status precisely from a source — do not invent a retirement date.** Note that [../CURRENCY.md](../CURRENCY.md) already records classic approvals as *not retired*, and phase 08 found the same shape for Workflow Rules. **Assume the plan's framing is wrong until a primary source says otherwise.**
- **18** — the Migrate to Flow tool and the **support** timeline. Phase 08 corrected the vault-wide claim: **end of support 31 Dec 2025, creation blocked Winter '23, no retirement date announced, existing automations still run.** This note owns the conversion traps, and its premise is stronger for the correction — migration is urgent because *unsupported* automation that breaks stays broken, not because a switch-off is coming.

**14 — brief.** Trigger Order is **1–2000** in Advanced Settings and orders only flows of the **same trigger type on the same object** — an after-save flow can never be made to run before a before-save one. Ties fall back to created/last-modified order. **Flow Trigger Explorer** has existed since **Spring '22**. Carry the one-flow-per-object-vs-many argument here; **03** forward-links to it.

**🆕 — research before writing:** **17**, **18**, **20**, **21**, **23**. All post-2024.

**Summer '26 findings from phase 08 that belong to this run**

- **Create Agent element in Flow Builder** (GA) — build or deploy an agent from the canvas → **21**.
- **Troubleshoot Flow Errors with Agentforce** (**Beta**; needs Data 360, Agentforce provisioning, Einstein generative AI) → **15**.
- **Visualize Execution Path when testing screen flows**, **Visual Flow Version Comparison**, **Element Error Rate column**, redesigned validation panel → **15** and **22**.
- **Update Screen Flows with natural-language prompts** (GA, extends the earlier record-/schedule-triggered capability) → **23**.
- **Unanimous approval for group-assigned steps** — every member gets their own work item and those items **cannot be reassigned**; dependency visibility is no longer gated on *Manage Flow* → **17**.
- **Flow Orchestration became a standard feature on 2026-02-18**, no usage-based caps → **16**. Already in [../CURRENCY.md](../CURRENCY.md).

**Cross-links, don't duplicate**

- **19** → [05-experience-cloud · 07 Guest user security](../05-experience-cloud-lwr/INDEX.md) (written later, phase 18 — this note owns the run-as context, that one owns site hardening).
- **20** → [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md).
- **21, 23** → [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md). **21** should reuse the description-as-contract framing already written there.
- **17** → [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md), written in phase 02.

**Seed harvest** — `Flow Updates` (2025) → **18** or **23**; check what it actually covers first. **`Limits based Things` (2025)** → **13**; found during the phase-08 harvest and not in the inventory, its highlight mentions iterating large query results, so read it before writing **13**.
