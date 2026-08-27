# Scheduled & Autolaunched Flows

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** The two flow types with no user and no record trigger — autolaunched flows, which something else starts, and schedule-triggered flows, which a clock starts. Reuse patterns are [08](08-subflows-and-modular-flow-design.md).

## Core idea

An **autolaunched flow (no trigger)** is the platform's unit of reusable declarative logic. It has no UI and no trigger of its own, so it only ever runs because something called it — a subflow reference, an invocable action, Apex, the REST API, an Agentforce action, a Screen Action. That makes it the flow type you build when you want the logic to have more than one caller, and it is the substrate under half of this area. A **schedule-triggered flow** is a different thing wearing a similar shape: an autolaunched flow with a clock bolted to its Start element, optionally iterating a set of records. The important property is not the schedule but the running user — it is not you, and it is not the record owner, which is where most schedule-triggered flow bugs come from.

## How it works

| | Autolaunched (no trigger) | Schedule-triggered |
|---|---|---|
| Started by | subflow, action, Apex, API, agent | the schedule, and nothing else |
| Running user | **the caller's** context | the **Default Workflow User** |
| Screens | not allowed | not allowed |
| Callouts | allowed | allowed |

- **A schedule-triggered flow can name an object and a filter**, in which case it runs one interview per matching record with `$Record` populated — this is the declarative equivalent of a batch job.
- **Start Time is interpreted in the org's default time zone**, not the scheduler's and not the running user's.
- **The daily ceiling is 250,000 scheduled interviews**, or user licences × 200, whichever is greater.
- **`$User` in a schedule-triggered flow is the Default Workflow User**, so any logic keyed to the running user's role, permissions or record access is evaluated as that account.
- **You cannot start a schedule-triggered flow any other way** — not from a button, not from Apex. If you need both, build the logic as an autolaunched flow and call it from a thin scheduled wrapper.

## 2026 currency

Summer '26 added the control this flow type was missing: **a configurable batch size, 1–200, set directly on the Start element** of a schedule-triggered flow. Before it, a schedule that matched far more records than anticipated would process them in fixed chunks and fail as a block; you can now trade throughput for headroom explicitly. It is the same lever `Database.executeBatch(job, scopeSize)` gives Apex, and it should be reached for under the same conditions — heavy per-record work, or DML fanning out to related records. Note the asymmetry it exposes: **schedule-triggered flows got batch-size control while platform event-triggered flows still have none** → [07](07-platform-event-and-async-path-flows.md). → [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md)

## Gotchas

- **The Default Workflow User is the single biggest surprise here.** If it is unset, inactive, or lacks access to the records the flow touches, the flow fails or quietly processes nothing.
- **A schedule-triggered flow reports success while doing nothing** when its running user cannot see the filtered records. Sharing, not logic, is the usual cause. → [07-security](../07-security-and-sharing/INDEX.md)
- **Start Time uses the org's default time zone**, which bites orgs whose admins and users are in different ones.
- **Deploying a schedule-triggered flow does not always carry its schedule.** Verify the start date and frequency in the target org after every deploy. → [24 · Deployment & versioning](24-flow-deployment-versioning-and-governance.md)
- **A past start date does not backfill.** The schedule begins from the next occurrence.
- **An autolaunched flow inherits the caller's context by default**, so the same flow called from a trigger, an agent action and a scheduled wrapper runs as three different users with three different limit budgets — and the default setting is literally named *Depends on How Flow is Launched*. → [19](19-flow-run-context-and-sharing.md)
- **Neither type may contain a Screen element**, and the builder will not let you add one — this is the usual reason a working screen flow cannot simply be reused as a subflow.

## Recall

Q: Who runs a schedule-triggered flow?
A: The **Default Workflow User** set in Process Automation Settings — not the flow's author and not the record owner.

Q: What does adding an object and filter to a schedule-triggered flow do?
A: It runs one interview per matching record with `$Record` populated, making it the declarative equivalent of a batch job.

Q: What did Summer '26 add to schedule-triggered flows?
A: A configurable batch size of 1–200 on the Start element, so an unexpectedly large record set can be processed in smaller chunks.

Q: In which time zone is a schedule-triggered flow's Start Time interpreted?
A: The org's default time zone.

Q: Why can an autolaunched flow behave differently depending on who calls it?
A: It runs in the caller's context, so the running user, record access and remaining limit budget all come from the caller.

## Related

- [08 · Subflows & modular flow design](08-subflows-and-modular-flow-design.md) — the most common caller of an autolaunched flow
- [02-apex · 15 Scheduled Apex & cron](../02-apex-and-triggers/15-scheduled-apex-and-cron.md) — the coded alternative, and when a cron expression beats a schedule
- [07 · Platform event & async path flows](07-platform-event-and-async-path-flows.md) — the other two ways work leaves the triggering transaction
