# Migrate to Flow & Legacy Automation

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Getting Workflow Rules and Process Builder off an org — the tool, what it converts, and the traps in what it produces. The tool-choice argument is [01](01-automation-landscape-and-tool-selection.md).

> **What changed.** *"Workflow Rules and Process Builder are retired"* is wrong and it is the most common thing said about them. **Support ended 31 December 2025** — no bug fixes, no support cases. **Creation was blocked in Winter '23.** **No retirement date has been announced, and existing automations still run today.** That makes the migration argument stronger, not weaker: unsupported automation that breaks stays broken, and you cannot open a case about it.

## Core idea

The **Migrate to Flow** tool at Setup → Process Automation → Migrate to Flow converts a Workflow Rule or a Process Builder process into a record-triggered flow. It is a genuine time-saver and it is a translator, not an architect: it performs a **one-to-one conversion** of criteria and actions and makes no judgement about whether the result is a good design. Five workflow rules on Account become five flows. The redundancy, the overlapping criteria and the field updates that fight each other all survive the trip. So the tool is best understood as the first of two jobs — it gets the logic into Flow correctly, and the consolidation, ordering and bulkification are yours afterwards. The second job is where the value is, because it is also the opportunity: this is the only moment anyone will fund a look at what that automation actually does.

## How it works

| | Converted | You do by hand |
|---|---|---|
| Workflow Rules | criteria, field updates, email alerts, tasks, outbound messages, time-dependent actions | unsupported operators, consolidation |
| Process Builder | criteria and actions per node | **recursion**, some invocable configurations |
| Approval processes | **nothing** — not supported by the tool | all of it |

- **The tool does not deactivate the source.** The new flow and the old rule both exist, and if both are active the logic runs **twice**. Deactivation is a deliberate, separate step.
- **Process Builder recursion is not supported.** A process configured to re-evaluate is migrated so that the record is evaluated **once only** — behaviour silently changes.
- **The `does not contain` operator has no direct equivalent** in entry criteria; convert it with custom condition logic.
- **Unsupported entry criteria become a Decision element** inside the flow rather than a start condition — which works, but the flow now starts and pays to start on every save. → [03](03-record-triggered-flows.md)
- **Check which side of the save you landed on.** A workflow field update on the triggering record cost nothing at step 11; the same logic as an *after-save* flow costs a DML statement. Convert those to before-save. → [13](13-flow-limits-and-bulkification.md)

## 2026 currency

The support boundary passed on 31 December 2025, so the whole subject moved from "planned modernisation" to "known operational risk" without any of the automation stopping. Two consequences are worth carrying into a scoping conversation. First, **save-order steps 11 and 13 may be genuinely occupied** in an inherited org — assuming they are vestigial sends debugging to the wrong place, and Flow Trigger Explorer will not show you what is there. → [14](14-trigger-order-and-flow-trigger-explorer.md), [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md). Second, the AI tooling changes the economics of the *second* job: Summer '26's natural-language flow editing and flow summarisation make consolidating a pile of converted flows meaningfully cheaper than it was. → [25](25-ai-assisted-flow-authoring.md)

## Gotchas

- **Saying "retired" in a scoping call is a credibility loss.** Out of support, creation blocked, still running, no retirement date.
- **Running the old rule and the new flow at the same time doubles the automation.** The tool will not stop you.
- **Migrated Process Builder recursion silently evaluates once.** Nothing errors; the behaviour just changes.
- **One-to-one conversion preserves your mess.** Five bad rules become five bad flows unless you consolidate afterwards.
- **Time-dependent workflow actions become scheduled paths**, which run in a different context and against different limits than the queue-based originals. → [06](06-scheduled-and-autolaunched-flows.md)
- **Approval processes are out of scope for the tool entirely.** Rebuilding them is a separate project. → [17](17-approval-orchestration.md)
- **Outbound messages have no Flow equivalent** worth the name; they usually become an HTTP callout or a platform event. → [12](12-http-callout-and-external-services-in-flow.md)
- **Audit before you migrate.** A rule that has not fired in two years should be deleted, not converted.

## Recall

Q: Are Workflow Rules and Process Builder retired?
A: No. Out of support since 31 December 2025, creation blocked since Winter '23, still executing, no retirement date announced.

Q: What does the Migrate to Flow tool do to the original Workflow Rule?
A: Nothing. It stays active unless you deactivate it — and until you do, the logic runs twice.

Q: What happens to a Process Builder process that relies on recursion?
A: It is migrated so the record is evaluated once only. The behaviour changes without an error.

Q: Why can a converted flow be slower than the workflow rule it replaced?
A: A workflow field update on the triggering record cost no DML at step 11; the same work in an after-save flow costs a DML statement. Convert it to before-save.

Q: Which legacy automation does the tool not convert at all?
A: Approval processes.

## Related

- [01 · Automation landscape & tool selection](01-automation-landscape-and-tool-selection.md) — why Flow is the only tool you may build in now
- [14 · Trigger order & Flow Trigger Explorer](14-trigger-order-and-flow-trigger-explorer.md) — why Explorer is not a complete picture of an inherited object
- [25 · AI-assisted flow authoring](25-ai-assisted-flow-authoring.md) — the tooling that makes post-migration consolidation affordable
