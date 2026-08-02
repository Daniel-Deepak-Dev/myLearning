# Automation Landscape & Tool Selection

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** Which automation tool to reach for, and the honest boundary between Flow and Apex. Not a Flow Builder tutorial — that is [02](02-flow-anatomy-and-builder-basics.md).

> **What changed.** *"Workflow Rules and Process Builder are retired"* is wrong, and the overstatement costs you the room where it gets said. Salesforce **ended support on 31 December 2025** — no bug fixes, no customer support — and blocked creation of new ones years earlier. **Existing Workflow Rules and Process Builder automations still run, and no date has been announced for when they stop.** Flow is the only tool you may *build* in; it is not yet the only tool *running* in an org you inherit.

## Core idea

The three-way declarative decision tree — workflow rule, process, flow — is dead for new work, and every tutorial that opens with it is dated. What replaced it is not a simpler question but a differently shaped one, asked twice. First: **which kind of Flow**, because the flow type fixes where you sit in the save order, what you can touch and what limits apply. Second, and harder: **Flow or Apex**, which is a question about maintainability and testing rather than capability. Flow can now do most of what a trigger can, including callouts, so "can it?" stopped being the deciding question around 2023. The deciding question is who will own this in two years.

## How it works

| Flow type | Runs when | Typical use |
|---|---|---|
| **Record-triggered** | a record is saved — before or after | field defaulting, cross-record updates → [03](03-record-triggered-flows.md) |
| **Screen** | a user launches it | guided data entry, wizards → [04](04-screen-flows-and-ux-design.md) |
| **Autolaunched (no trigger)** | called by something else | subflows, invocable actions, agent actions → [08](08-subflows-and-modular-flow-design.md) |
| **Schedule-triggered** | a clock | nightly batches → [06](06-scheduled-and-autolaunched-flows.md) |
| **Platform event-triggered** | an event message arrives | integration fan-out → [07](07-platform-event-and-async-path-flows.md) |

- **The Flow-vs-Apex boundary that actually holds.** Flow when the logic is a sequence a competent admin will still recognise in a year; Apex when it needs real data structures (maps, sets, recursion), genuine unit tests, or precise bulk control over more than a few hundred records. → [02-apex · 06](../02-apex-and-triggers/06-triggers-and-the-handler-framework.md)
- **"Clicks not code" is not a limits argument.** Flow spends the same per-transaction budget as Apex and offers less control over how. → [13 · Flow limits & bulkification](INDEX.md)
- **Mixing both on one object is normal**, not a smell. A before-save flow for field defaulting plus a trigger for the complex path is a common, defensible design.
- **Flow has no Map type**, no true unit-test isolation and no interfaces. When a design needs any of those, it has already left Flow.

## 2026 currency

**Workflow Rule creation was disabled in Winter '23** and Process Builder followed; the **Migrate to Flow** tool shipped in the same window. Support for both ended **31 December 2025**, which is a support boundary, not an execution one — an inherited org can still be running dozens of them, and steps 11 and 13 of the save order may be genuinely occupied rather than vestigial. → [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md). The other 2026 shift is commercial: **Flow Orchestration became a standard feature on 2026-02-18** with no usage-based run limits, so cost is no longer a reason to avoid it. Migration mechanics and the conversion traps are [18 · Migrate to Flow](INDEX.md).

## Gotchas

- **Saying "retired" in a scoping call and being corrected costs the room.** The precise words are *end of support*: no bug fixes, no support cases, automations still executing.
- **An unsupported automation that breaks stays broken.** That is the real risk, not switch-off — there is no one to escalate to.
- **You cannot create new Workflow Rules or processes**, but you can still activate, deactivate and edit existing ones, which is how they quietly survive.
- **Choosing the flow type is choosing your save-order position**, and it cannot be changed later without rebuilding the flow.
- **"Flow can't do callouts" is out of date** — it has been able to since Winter '24. → [12](12-http-callout-and-external-services-in-flow.md)
- **Apex is not the answer to "Flow hit a limit."** The same limit usually applies; the fix is bulkification. → [13](INDEX.md)

## Recall

Q: Are Workflow Rules and Process Builder retired?
A: No. Support ended 31 December 2025 — no bug fixes or support cases — but existing automations still run and no retirement date has been announced.

Q: When did creating new Workflow Rules stop being possible?
A: Winter '23, with Process Builder following. Existing ones can still be activated, deactivated and edited.

Q: What is the first decision once you've chosen Flow?
A: Which flow type — it fixes your position in the save order, what you can modify, and which limits apply.

Q: What is the honest Flow-vs-Apex line?
A: Apex when you need real data structures, unit tests or precise bulk control; Flow when an admin must still own it in a year. Capability stopped being the deciding factor.

Q: Why is "clicks, so no limits" wrong?
A: Flow shares the same per-transaction governor budget as Apex, with less control over how it is spent.

## Related

- [03 · Record-triggered flows](03-record-triggered-flows.md) — the type you will build most, and the before/after-save decision
- [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — where each automation type sits in the save pipeline
- [02-apex · 06 Triggers & the handler framework](../02-apex-and-triggers/06-triggers-and-the-handler-framework.md) — the other side of the boundary this note draws
