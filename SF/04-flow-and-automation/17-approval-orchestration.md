# Approval Orchestration

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Building approvals in Flow — approval steps, work items, recall, and how an approval is launched. The engine underneath is [16](16-flow-orchestrator.md); the choose-your-engine comparison is [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md).

> **What changed.** Two beliefs, both common, both wrong. **Classic approval processes are not deprecated, not in maintenance and have no announced retirement** — the docs were renamed *Classic Approval Processes* and Flow approvals are positioned as the "modern alternative", which is a recommendation and not a countdown. And **a flow approval process is no longer confined to an orchestration**: since **Summer '25** an invocable action launches one from *any* flow.

## Core idea

A flow approval process is an orchestration whose steps are approvals. That one sentence carries most of what makes it different from the classic model: routing is Flow logic, so an approver can be computed from data rather than picked from a fixed list of assignment options; stages give you parallel approvals without the classic "all must approve this one step" straitjacket; and the whole thing is metadata, so it deploys. The second idea is newer and easily missed. Because Summer '25 exposed approvals as an **invocable action**, an approval stopped being a destination you build a process around and became a *step* you drop into automation you already have — a record-triggered flow can now request approval mid-logic and carry on. That reframes approval from a subsystem to a capability.

## How it works

| Piece | Behaviour |
|---|---|
| **Approval step** | assigns an approval work item to a user, **public group** or **queue** |
| **Background step** | runs automation between approvals with no assignee |
| **Recall path** | *Summer '25* — a defined route for withdrawing a submission in flight |
| **Custom notification email** | configured per approval step |
| **Launch** | orchestration start, record trigger, or *Summer '25* **invocable action from any flow** |

- **GA Spring '25**, with group and queue assignment and per-step notification email from the outset.
- **Summer '25 added the recall path and a single-approver template**, which is the fastest way to see the shape of one before building your own.
- **Approval Submissions and Orchestration Runs are records**, so a stuck approval is a query rather than an inference. This is the strongest practical argument over classic.
- **The record locks while an approval is in flight**, exactly as under the classic model — automation editing it mid-approval fails unless it runs in the right context. → [19](19-flow-run-context-and-sharing.md)
- **Email approval response remains a classic capability** and needs the approver to hold **API Enabled**. → [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md)

## 2026 currency

Two changes, one commercial and one behavioural. **Flow Orchestration became a standard feature on 2026-02-18**, so flow approvals inherited a price of zero — cost was the usual reason to stay on classic, and that argument is now dead. **Summer '26 added unanimous approval for group-assigned steps**, and the mechanics matter more than the headline: every member of the group receives **their own work item**, the step advances only when all of them approve, and **those work items cannot be reassigned**. A group whose membership includes someone on leave will stall the process with no delegation route, which makes group membership an operational dependency rather than a configuration detail. Summer '26 also **ungated dependency visibility from *Manage Flow***, so an Approval Designer can now see step dependencies without full flow administration. → [../CURRENCY.md](../CURRENCY.md)

## Gotchas

- **Do not tell a client classic approvals are retired.** They are not, and no date has been announced. Recommend flow approvals on capability and cost, not on a deadline that does not exist.
- **Unanimous group steps issue one work item per member and none of them can be reassigned.** One absent member blocks the process.
- **Queue assignment is a race, group assignment is a rendezvous.** Picking the wrong one changes the semantics of the step, not just who sees it.
- **A delegated approver inherits the work item, not record access.** A delegate who cannot see the record cannot act on it.
- **Migration from classic is a rewrite, not a wizard.** The Migrate to Flow tool does not convert approval processes. → [18](18-migrate-to-flow-and-legacy-retirement.md)
- **The record lock is real.** A record-triggered flow that fires on the same record during approval will hit it.
- **"Approval Orchestrator" is also an AppExchange package name.** The platform feature is *Flow Approval Processes*, running as approval orchestrations.

## Recall

Q: Are classic approval processes deprecated or in maintenance?
A: Neither. Fully supported, docs renamed *Classic Approval Processes*, no retirement date announced.

Q: What did Summer '25 change about how a flow approval process can be started?
A: An invocable action makes it callable from **any** flow, not just an orchestration-type flow.

Q: What happens when a Summer '26 group-assigned step is set to unanimous?
A: Every group member gets their own work item, all must approve, and the work items cannot be reassigned.

Q: Why are flow approvals easier to monitor than classic ones?
A: Approval Submissions and Orchestration Runs are records — bottlenecks are queryable and reportable.

Q: What is the cost of running flow approvals since 2026-02-18?
A: Nothing. Flow Orchestration is a standard feature with no usage-based run limits.

## Related

- [16 · Flow Orchestrator](16-flow-orchestrator.md) — the stages-and-steps engine approvals are built on
- [01-admin · 12 Approval processes](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md) — classic vs flow as an admin decision, with the classic-side plumbing
- [21 · Flow for external & guest users](21-flow-for-external-and-guest-users.md) — approving from an Experience Cloud site
