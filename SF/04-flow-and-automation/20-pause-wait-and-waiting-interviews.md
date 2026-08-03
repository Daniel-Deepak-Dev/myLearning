# Pause, Wait & Waiting Interviews

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Flows that stop and resume later — the Pause and Wait elements, the `FlowInterview` records they leave behind, and the operational debt that follows. Leaving the transaction *without* waiting is [07](07-platform-event-and-async-path-flows.md).

> **What changed.** *"There is an org-wide cap on paused and waiting flow interviews"* was true and is not. The limit was **removed in Spring '23**, so the constraint on a design that parks thousands of interviews is now **storage and housekeeping**, not a ceiling that stops you. That is a worse problem in practice: nothing fails, the records simply accumulate until someone notices.

## Core idea

A waiting flow is the only construct in Flow that survives a transaction *and* keeps its state. An async path starts a fresh transaction and forgets; a paused interview serialises every variable, every collection and its position in the canvas into a **`FlowInterview` record**, and picks up exactly where it left off when its resume condition fires. That persistence is the feature and the liability in one. It buys genuine long-running behaviour with no Apex, and it means a design decision made in the builder quietly creates rows in your org that outlive the flow version, the requirement and often the person who built it. The question to ask before adding a Wait is not "can this flow wait?" but **"who deletes these, and when?"**

## How it works

| Element / mechanism | Waits for | Available in |
|---|---|---|
| **Wait for Amount of Time** | a duration | autolaunched, scheduled |
| **Wait Until a Date** | an absolute or field-relative date | autolaunched, scheduled |
| **Wait for Conditions** | a record matching criteria | autolaunched, scheduled |
| **Pause button** | the user coming back | screen flows |
| **Scheduled path** | an offset from the trigger or a date field | record-triggered |

- **Record-triggered flows do not support Wait elements.** Their waiting mechanism is the **scheduled path**, configured on the Start element. → [03](03-record-triggered-flows.md)
- **A record-triggered flow that calls a subflow containing a Wait element errors**, which is the practical form the restriction takes and it fails at run time, not at save. → [08](08-subflows-and-modular-flow-design.md)
- **Paused and waiting interviews live at Setup → Process Automation → Paused and Waiting Interviews**, and the *Paused and Failed Flow Interviews* list view is where operational triage starts.
- **Interview size is capped at 1,000,000 bytes.** An interview holding a large collection **cannot be persisted**, so the flow fails at the Wait rather than at the Get that filled it. → [13](13-flow-limits-and-bulkification.md)
- **An interview resumes on the flow version it started on**, not the version that is active when it wakes. Deploying a fix does not fix work already in flight. → [24](24-flow-deployment-versioning-and-governance.md)

## 2026 currency

Nothing in Summer '26 changes the mechanics, and the currency worth carrying is the removed limit plus one contrast. The cap's removal (Spring '23) turned this from a capacity question into a **data-retention** question, and no native retention policy arrived with it — deleting stale interviews is still a manual list-view operation or a scripted one. Meanwhile Summer '26 gave schedule-triggered flows a **batch size of 1–200** → [06](06-scheduled-and-autolaunched-flows.md), which is the nearest thing to throughput control anywhere in this area; waiting interviews got no equivalent. If a design parks tens of thousands of interviews that all resume on the same date, nothing shapes that spike for you.

## Gotchas

- **The org-wide paused-interview limit is gone, and that is not good news.** Nothing stops the accumulation, so nothing tells you it happened.
- **Record-triggered flows cannot wait.** Use a scheduled path; a subflow with a Wait inside one errors at run time.
- **An interview over 1 MB cannot be paused at all.** The failure surfaces at the Wait element, far from the Get Records that caused it.
- **Resuming uses the version the interview started on.** A bug fixed and deployed today does not reach interviews that paused yesterday.
- **A screen flow's Pause button is on by default.** If the flow commits records mid-way, a user pausing between steps leaves half-finished data. Hide it in the footer. → [04](04-screen-flows-and-ux-design.md)
- **Deactivating a flow does not cancel its waiting interviews**, and deleting the flow version can strand them.
- **Wait Until a Date with a past date resumes immediately**, which is rarely what the builder meant.
- **Nobody owns this list.** Put a recurring check on Paused and Waiting Interviews in the same place you keep the flow error-email recipient. → [24](24-flow-deployment-versioning-and-governance.md)

## Recall

Q: What happened to the org-wide limit on paused and waiting interviews?
A: Removed in Spring '23. The remaining constraint is storage and housekeeping, and nothing warns you.

Q: Which flow type cannot use Wait elements, and what does it use instead?
A: Record-triggered flows. They use scheduled paths on the Start element.

Q: What does a paused flow leave behind, and where do you find it?
A: A `FlowInterview` record, listed under Setup → Process Automation → Paused and Waiting Interviews.

Q: You deploy a fix to a flow. What happens to interviews that paused before the deploy?
A: They resume on the version they started on. The fix does not reach them.

Q: Why can a flow fail at a Wait element because of a Get Records element much earlier?
A: Pausing serialises the whole interview, and the interview is capped at 1,000,000 bytes.

## Related

- [07 · Platform event & async path flows](07-platform-event-and-async-path-flows.md) — leaving the transaction without keeping state
- [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md) — where the 1 MB interview size sits among the other numbers
- [24 · Deployment, versioning & governance](24-flow-deployment-versioning-and-governance.md) — why in-flight interviews complicate every flow deployment
