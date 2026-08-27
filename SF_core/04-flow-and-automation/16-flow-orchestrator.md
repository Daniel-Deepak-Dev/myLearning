# Flow Orchestrator

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Multi-step, multi-user processes that outlive a transaction — stages, steps, work items and the orchestration run. Approvals built on this engine are [17](17-approval-orchestration.md).

## Core idea

Everything else in this area runs inside one transaction or one user's session. An **orchestration** is the flow type for work that does neither: a hiring process, an onboarding, a contract review — days long, several people, each doing their part in turn. The building blocks are deliberately few. A **stage** groups **steps** and stages run in sequence; steps *within* a stage can run **in parallel**, which is the whole reason the tool exists. A step is either **background**, which runs an autolaunched flow with nobody watching, or **interactive**, which assigns a **work item** to a user, group or queue and waits for a human to finish a screen flow. State lives in an **orchestration run** record, so the process is queryable, reportable and resumable — the thing a chain of record-triggered flows and tasks can never quite be.

## How it works

| Piece | What it is |
|---|---|
| **Stage** | ordered container of steps; stages run sequentially |
| **Step** | one unit of work; steps in a stage may run **in parallel** |
| **Background step** | runs an autolaunched flow, no user |
| **Interactive step** | creates a **work item**, assigned to user / group / queue, completed via a **screen flow** |
| **Orchestration run** | the persisted state record, with status and milestones |

- **Two orchestration types**: **autolaunched**, started by something else, and **record-triggered**, started by a record change like any other record-triggered flow.
- **Entry and exit conditions** on stages and steps decide whether that unit runs at all, which is how one orchestration covers several variants of a process.
- **Users meet their work through the Orchestration Work Guide** — a Lightning page component, and an Experience Cloud component for external participants. → [21](21-flow-for-external-and-guest-users.md)
- **The screen flow behind an interactive step is an ordinary screen flow**, reusable elsewhere. Orchestration composes existing flows rather than replacing them. → [08](08-subflows-and-modular-flow-design.md)
- **Fault paths work here too**, and a background step on a fault path is the standard way to notify someone that the process itself broke. → [10](10-fault-paths-and-custom-errors.md)

## 2026 currency

The change that matters is commercial and it is recent: **Flow Orchestration became a standard flow type on 2026-02-18**, included with no usage-based run limits in Enterprise, Performance, Unlimited, all Einstein 1 and Developer editions. It was previously a paid add-on billed per run, and that cost was the single most common reason architects designed around it — stitching a multi-step process out of record-triggered flows, tasks and custom status fields instead. Every design decision made on that basis is now worth revisiting, and the answer is often "this should have been an orchestration." The knock-on effect lands in [17](17-approval-orchestration.md): flow-based approvals run on this engine, so they inherited the same price of zero. → [../CURRENCY.md](../CURRENCY.md), [01-admin · 12](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md)

## Gotchas

- **Stages are sequential and steps are parallel.** Putting two independent steps in two stages serialises work that did not need to be serialised.
- **An interactive step needs a screen flow**, and that screen flow must be able to run for the assignee — their access, not yours. → [19](19-flow-run-context-and-sharing.md)
- **A work item assigned to a queue is claimed by one member**, whereas a group assignment can fan out to everyone. The difference is not cosmetic; it decides whether the step is a race or a rendezvous.
- **An orchestration run persists.** Abandoned runs accumulate exactly like paused interviews and want a retention plan. → [20](20-pause-wait-and-waiting-interviews.md)
- **Deactivating an orchestration does not cancel runs already in flight.**
- **Each interactive step is its own transaction**, so limits reset between steps — and so does anything you assumed was still in memory.
- **The pricing change is recent enough that most published guidance predates it.** Any 2024–25 article weighing orchestration against a hand-rolled alternative is arguing from a cost that no longer exists.

## Recall

Q: What runs in sequence in an orchestration, and what can run in parallel?
A: Stages run in sequence; steps inside a stage can run in parallel.

Q: What is the difference between a background step and an interactive step?
A: Background runs an autolaunched flow with no user. Interactive creates a work item for a person and waits on a screen flow.

Q: What changed about Flow Orchestration on 2026-02-18?
A: It became a standard flow type — included, with no usage-based run limits, instead of a paid add-on.

Q: Where does the state of a long-running orchestration live?
A: In an orchestration run record, with a status and logged milestones — queryable and reportable.

Q: How do users interact with their assigned steps?
A: Through the Orchestration Work Guide component, on a Lightning page or an Experience Cloud site.

## Related

- [17 · Approval Orchestration](17-approval-orchestration.md) — approvals built on this engine, and the classic alternative
- [08 · Subflows & modular flow design](08-subflows-and-modular-flow-design.md) — the reusable flows an orchestration composes
- [01-admin · 12 Approval processes](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md) — the declarative-admin view of the same decision
