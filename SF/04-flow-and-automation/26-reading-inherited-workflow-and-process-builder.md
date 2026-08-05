# Reading Inherited Workflow Rules & Process Builder

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 24

**Scope:** How the two legacy tools actually fire, so you can read what an inherited org is already doing. The conversion tool is [18](18-migrate-to-flow-and-legacy-retirement.md); the migration programme is [27](27-legacy-automation-migration-runbook.md).

> **What changed.** This vault has said *"out of support, not retired"* in a dozen places and never taught the thing that follows from it: **if they still execute, you still have to be able to read them.** The skill going scarce is *comprehension*, not authoring — creation of Workflow Rules was blocked in **Winter '23** and Process Builder in **Summer '23**, so nobody is learning these by building one. Help **001096524** is the support boundary; **000220431** is the operational sentence: *"After December 31, 2025, existing workflow rules continue to run, and you can activate, deactivate, and edit them."*

## Core idea

A workflow rule is four separate things and reading one means naming all four: an **object**, an **evaluation criteria** setting deciding which saves are considered at all, **rule criteria** deciding whether this particular save qualifies, and **actions** split into *immediate* and *time-dependent*. Nearly every baffling legacy behaviour traces to the first, because it is the one with **no equivalent in Flow** — a record-triggered flow has entry conditions and `$Record__Prior`, but nothing that natively means *"only when this becomes true, having previously been false."* A process is a different shape entirely: an ordered list of criteria nodes evaluated top to bottom, first match wins by default. Most of the work is knowing which switch you are looking at.

## How it works

| Evaluation criteria | Fires on | Reading it |
|---|---|---|
| **created** | insert only | the safe one — no re-entry risk, time triggers allowed |
| **created, and every time it's edited** | every insert and every update | fires even when criteria were **already** true — the usual duplicate-email cause. **Time triggers are blocked here**: the record could requeue endlessly |
| **created, and any time it's edited to subsequently meet criteria** | insert, plus updates crossing from not-meeting to meeting | the recursion guard, and the option Flow cannot express directly. Time triggers allowed |

- **Immediate actions run inside the save at step 11. Time-dependent actions do not run then at all** — they are parked in the **time-based workflow queue** with a computed fire time, which is why the automation you are reading may have no visible effect today. → [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md)
- **`Re-evaluate Workflow Rules after Field Change`**, a checkbox on a *field update*, re-runs **every** rule on the object. This is the legacy recursion engine and the reason one save produces a debug log with the same trigger in it repeatedly. → [02-apex · 07](../02-apex-and-triggers/07-order-of-execution-and-recursion.md)
- **A cross-object field update reaches the master-detail parent only** — never a lookup parent, never downward — and that parent then runs **its own** complete save order.
- **Process Builder's Recursion option** — *"Allow process to evaluate a record multiple times in a single save operation"* — lets one process re-evaluate the same record **up to five times per transaction.**
- **A node set to *evaluate the next criteria* turns first-match-wins off**, which is how a single process ends up doing five unrelated things to one record.

## 2026 currency

Nothing about how these fire has changed — that is the point of the note, and it is why a 2015 blog post about workflow rules is still *mechanically* accurate while being strategically useless. What changed is entirely around them: support ended **31 December 2025**, **no retirement date has been announced**, and both tools keep executing at save-order steps 11 and 13. The operational consequence to carry into an inherited org is that **an unsupported automation that breaks stays broken** — there is no case to open — so reading them is now a risk-assessment skill rather than a maintenance one. → [CURRENCY.md](../CURRENCY.md), [01](01-automation-landscape-and-tool-selection.md)

## Gotchas

- **`Re-evaluate Workflow Rules after Field Change` is the single most expensive checkbox in a legacy org.** One field update re-runs every rule on the object, and nothing in Setup summarises which updates have it ticked.
- **A rule with no immediate actions can still be doing something right now** — its work is sitting in the time-based queue, invisible unless you look at Setup → Monitoring → **Time-Based Workflow**. → [27](27-legacy-automation-migration-runbook.md)
- **"Every time it's edited" fires when the criteria were already true**, so a rule that looks like *"when Stage = Closed Won"* actually means *"on every save while Stage = Closed Won."*
- **Time triggers cannot exist on an "every time it's edited" rule**, so finding a time-dependent action tells you the evaluation criteria before you look.
- **A deactivated rule is not a disabled rule.** Pending queue entries survive deactivation and still fire → [27](27-legacy-automation-migration-runbook.md).
- **Cross-object field updates make the parent's automation run**, so an Opportunity rule can trigger every Account trigger, flow and rule in the org.
- **Process error emails go to the last person who modified the process**, not to an owner or a queue — the same defect Flow had before *Send Process or Flow Email to*. → [24](24-flow-deployment-versioning-and-governance.md)
- **Flow Trigger Explorer will not show you any of this.** It lists flows only, so it is a partial map of an inherited object. → [14](14-trigger-order-and-flow-trigger-explorer.md)

## Recall

Q: What are the three workflow rule evaluation criteria?
A: *created*; *created, and every time it's edited*; and *created, and any time it's edited to subsequently meet criteria*.

Q: Which evaluation criteria cannot have time-dependent actions, and why?
A: *created, and every time it's edited* — the record could requeue itself endlessly, so Salesforce blocks the combination.

Q: What does `Re-evaluate Workflow Rules after Field Change` do?
A: It re-runs every workflow rule on the object after that field update — the legacy recursion engine, and the reason one trigger appears repeatedly in a debug log.

Q: How many times can a Process Builder process evaluate one record in a single transaction?
A: Up to five, when its Recursion option is enabled.

Q: Which relationships can a workflow cross-object field update reach?
A: The master-detail **parent** only — never a lookup parent and never downward — and that parent then runs its own save order.

## Related

- [27 · Legacy automation migration runbook](27-legacy-automation-migration-runbook.md) — what to do once you can read it, including the queue tail
- [18 · Migrate to Flow & legacy automation](18-migrate-to-flow-and-legacy-retirement.md) — the tool that converts what this note teaches you to read
- [01-admin · 14 Order of execution](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) — where steps 11 and 13 sit, and why they are not vestigial
- [14 · Trigger order & Flow Trigger Explorer](14-trigger-order-and-flow-trigger-explorer.md) — why Explorer is not a complete picture of an inherited object
