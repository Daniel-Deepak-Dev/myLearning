# Fault Paths & Custom Errors

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 08

**Scope:** What happens when a flow fails, and the three mechanisms for controlling it. Testing failure deliberately is [15 · Flow testing & debugging](INDEX.md).

> **What changed.** *"Add a fault path"* is not error handling — it is error *reporting*. **A fault path does not roll back the transaction**: every record the flow already wrote stays written, and the flow simply continues down a different branch with partial data committed. The **Custom Error element (Winter '24) does roll back**, and it is the element most "handle the error" advice should have been naming since.

## Core idea

Flow gives you three tools that all look like error handling and do different things, and choosing by name rather than by behaviour is how half-finished data gets into production. A **fault connector** catches a failure on one element and routes execution somewhere else — useful for logging and for telling the user something went wrong, but the transaction is untouched and anything already written stays written. A **Custom Error element** stops the flow, shows a message you wrote, and **rolls the transaction back**, which is what you want when the whole operation should be all-or-nothing. A **Roll Back Records element** does the rollback without the message, for screen flows. The question to ask at every failure point is therefore not "did I handle this?" but **"what is on disk if this fails here?"**

## How it works

| Mechanism | Since | Where | Rolls back? |
|---|---|---|---|
| **Fault connector** | always | any element that can fail | **no** |
| **Custom Error** | **Winter '24** | record-triggered flows | **yes** — whole transaction |
| **Roll Back Records** | **Winter '22** | **screen flows only** | yes — *current* transaction |

- **`$Flow.FaultMessage`** holds the text of the failure and is the only thing a fault path knows about what went wrong. It is often unreadable to a user; log it, don't display it raw.
- **A Custom Error can target a specific field or the whole record**, which is what makes it a genuine replacement for a validation rule when the logic is too complex for one. → [01-admin · 08](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md)
- **With no fault path, an unhandled error emails the flow's last modifier** and shows the user an unhelpful runtime message. That default is why so many flows fail unnoticed in orgs where the last modifier has left.
- **Every screen boundary in a screen flow ends a transaction.** `Roll Back Records` therefore undoes only what happened since the previous screen — earlier commits are gone for good.
- **Data and Action elements are the ones that fail**; Assignment, Decision and Loop do not take a fault connector.

## 2026 currency

The Custom Error element is the substantive change and it is now several releases old, which makes "use a fault path" a dated answer rather than a wrong one — fault paths still have a job, it is just narrower than the advice implies. Summer '26's contribution is presentational but genuinely useful at scale: **fault paths collapse on the canvas**, joining the collapsible Decisions and Loops that arrived in Spring '26. A well-instrumented flow has a fault path on every Data and Action element, and before this the canvas became unreadable as a result — which is precisely why so many flows have none. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **A fault path leaves committed records committed.** If three of five updates succeeded before the failure, those three are on disk and the fault path cannot undo them.
- **An async path failure is invisible.** It runs after commit in its own transaction, so nothing about the original save reports it. → [07](07-platform-event-and-async-path-flows.md)
- **The unhandled-error email goes to the flow's last modifier**, which after a few years of turnover is usually nobody who is watching.
- **`$Flow.FaultMessage` is a system string.** Showing it to a user leaks internals and explains nothing.
- **`Roll Back Records` is screen-flow only**, and it only reaches back to the last screen.
- **A fault path that goes nowhere is worse than none** — it swallows the error and reports success.
- **A Custom Error inside a before-save flow blocks the save entirely**, which is correct behaviour and surprises people expecting a warning.
- **A subflow's unhandled fault propagates to the parent** and takes down the whole interview. → [08](08-subflows-and-modular-flow-design.md)

## Recall

Q: Does a fault path roll back the transaction?
A: No. Everything already written stays written; the flow just continues down another branch.

Q: Which element both shows a message and rolls back, and where can it be used?
A: The Custom Error element, Winter '24, in record-triggered flows.

Q: What does `Roll Back Records` actually undo in a screen flow?
A: Only the current transaction — which begins at the previous screen. Anything committed before that screen survives.

Q: Who is told when a flow fails with no fault path?
A: The flow's last modifier, by email — which is why unowned flows fail silently for years.

Q: What is the right question to ask at each failure point in a flow?
A: Not "did I handle this?" but "what is on disk if it fails here?"

## Related

- [07 · Platform event & async path flows](07-platform-event-and-async-path-flows.md) — the failure mode with no user to report to
- [01-admin · 08 Validation rules](../01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) — the other way to reject a save, and when Custom Error beats it
- [02-apex · 09 Exception handling](../02-apex-and-triggers/09-exception-handling-and-custom-exceptions.md) — savepoints and rollback semantics in code, where the same question applies
