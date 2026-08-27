# Approval processes & Approval Orchestration

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** The admin-surface view — which approval engine to choose, what each one can route, and how submissions are tracked. Flow mechanics (stages, interactive steps, work guide) belong to [04-flow · 16](../04-flow-and-automation/16-flow-orchestrator.md) and [17](../04-flow-and-automation/17-approval-orchestration.md).

> **What changed.** Two things at once. Approvals are now authored in Flow as **Flow Approval Processes**, and **Flow Orchestration stopped being a paid add-on on 2026-02-18** — it is a standard flow type with no usage-based run limits in Enterprise, Performance, Unlimited, all Einstein 1 and Developer editions. What has *not* happened: classic approval processes are **not retired and not deprecated**. Salesforce renamed the docs to *Classic Approval Processes* and calls Flow approvals a "modern alternative".

## Core idea

A classic approval process is a fixed ladder bolted to one object: entry criteria, ordered steps, an approver per step, and lock/unlock actions. A **flow approval process** is an orchestration — a sequence of **stages**, each holding one or more **steps** that are either *approval steps* (they assign an approval work item to a user, group or queue) or *background steps* (they run automation with nobody waiting). Because the routing is Flow logic rather than step criteria, approvers can be computed from data instead of chosen from a short list of assignment options, and a stage can run steps in parallel. Choosing between them is now a capability question, not a licence question.

## How it works

| | Classic approval process | Flow approval process |
|---|---|---|
| Authored in | Setup → Approval Processes | Flow Builder (orchestration) |
| Bound to | one object, ordered process list | Flow logic; can trigger on record change |
| Routing | manager field, queue, related user, manual | any data or business rule, dynamic |
| Parallel work | parallel approvers within a step | parallel **steps** within a stage |
| Extensibility | approval actions (field update, email, task, outbound message) | full Flow + **Apex** |
| Tracking | Approval History related list | **Approval Submissions** and **Orchestration Runs** |
| Cost | none | **none** — no automation credits, no orchestration-run charge |

- **Approval work items** are what an approver actually acts on; they can be approved or rejected with or without running the step's associated flow.
- **The submitter's view** is unchanged in spirit: a *Submit for Approval* action, then a record that is locked while in flight.
- **Classic still owns some plumbing** — notably **email approval response**, which requires the approver to hold the **API Enabled** user permission.
- **Monitoring** is where flow approvals earn their keep: submissions and runs are records, so bottlenecks are queryable and reportable rather than inferred from an approval history list.

## 2026 currency

The 2026-02-18 licensing change is the decision-relevant fact: cost was the standard reason to stay on classic, and it is gone. Orchestration runs are included in the editions listed above with no usage-based limitation. Treat any guide that describes Orchestrator as a paid add-on, or that quotes a per-run price, as out of date. Migration is still a rewrite, not a wizard — plan it as one. Detail and dates: [AI_Data/05-release-radar/](../../AI_Data/05-release-radar/README.md).

## Gotchas

- **Do not confuse the platform feature with the AppExchange package** also called "Approval Orchestrator". The platform feature is *Flow Approval Processes*, running as approval orchestrations.
- Classic being alive is a trap in both directions: do not tell a client it is retired, and do not start new complex approvals on it because it exists.
- Record locking behaves differently from ordinary Flow — an in-flight approval locks the record, so a trigger or flow that edits it mid-approval fails unless it runs with the right context.
- Classic processes are evaluated in **process order** and the **first matching entry criteria wins**; a new process added at the top silently changes which one fires.
- Email approval response silently does nothing for an approver without **API Enabled** — the request arrives, the reply is ignored.
- Approval history fields are populated only when the process instance is next acted on, so reports built on them show gaps that look like data loss.
- Delegated approvers inherit the item, not the permission set — a delegate who cannot see the record cannot act on it.
- An orchestration is metadata, so it deploys; classic processes are notoriously awkward to deploy and often get rebuilt by hand per org.

## Recall

Q: What changed about Flow Orchestration on 2026-02-18?
A: It became a standard flow type — no add-on purchase and no usage-based run limits — in Enterprise, Performance, Unlimited, all Einstein 1 and Developer editions.

Q: Are classic approval processes deprecated?
A: No. They are fully supported; the docs were renamed *Classic Approval Processes* and Flow approvals are positioned as the modern alternative. No retirement date has been announced.

Q: What are the two kinds of step inside a flow approval process stage?
A: Approval steps, which assign an approval work item to a user, group or queue, and background steps, which run automation with no assignee.

Q: Where do you look to find a stuck approval under each model?
A: Approval History related list for classic; Approval Submissions and Orchestration Runs records for flow approval processes.

Q: Which classic capability depends on a user permission that is easy to miss?
A: Email approval response — the approver needs **API Enabled** or their emailed reply is discarded.

## Related

- [04-flow · 17 Approval Orchestration](../04-flow-and-automation/17-approval-orchestration.md) — the Flow mechanics of approvals, written in phase 09; this note stays on the admin surface
- [11 · Queues, assignment & escalation rules](11-queues-assignment-and-escalation-rules.md) — queues as approval assignees
- [14 · Order of execution](14-order-of-execution-declarative-view.md) — where approval field updates land in the save
