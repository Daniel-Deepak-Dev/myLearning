# Legacy Automation Migration Runbook

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 24

**Scope:** Sequencing a Workflow Rule and Process Builder migration end to end, and the tail it leaves behind. The tool's own conversion behaviour is [18](18-migrate-to-flow-and-legacy-retirement.md); how the legacy automation fires is [26](26-reading-inherited-workflow-and-process-builder.md).

## Core idea

Salesforce's recommendation is unambiguous and has not changed: **migrate to Flow, using the Migrate to Flow tool**, which is GA — Workflow Rules since **Summer '22**, Process Builder since **Spring '23** — and is the only supported path. What the recommendation does not tell you is that running the tool is stage three of seven, and **the risk is concentrated in the two stages after it.** A migration that is declared done at "the flow exists" has typically changed nothing, and one declared done at "the rule is deactivated" has left live automation in a queue nobody is looking at. Treat it as a decommissioning programme with a **tail as long as your longest time trigger**, not as a conversion exercise.

## How it works

| Stage | What you do | The trap |
|---|---|---|
| 1 · Inventory | `sf org list metadata --metadata-type WorkflowRule`, then retrieve what it names | **Setup is per-object** — scoping from those screens always undercounts |
| 2 · Cull | delete what has not fired in years; check `LastModifiedDate` and the queue | converting dead automation doubles the work and preserves the mess |
| 3 · Convert | Migrate to Flow, one rule or process at a time | one-to-one — five bad rules become five bad flows → [18](18-migrate-to-flow-and-legacy-retirement.md) |
| 4 · Test | open the new flow in Flow Builder, debug-run it | **Flow Tests are record-triggered only** → [15](15-flow-testing-and-debugging.md) |
| 5 · Cut over | **Switch Activations** — deactivates the rule and activates the flow together | the flow is created **inactive**; skipping this changes nothing |
| 6 · Drain | Setup → Monitoring → **Time-Based Workflow**, delete pending entries | deactivating the rule does **not** empty the queue |
| 7 · Decommission | delete the rule, then the orphaned field updates and email alerts | **a rule with pending actions cannot be deleted at all** |

- **Two commands do the whole inventory.** `sf org list metadata --metadata-type WorkflowRule` is the **org-wide census** the Setup screens cannot give you — every rule as `Object.RuleName`; swap in `ApprovalProcess` or `Flow` to see what else is on the object. Then `sf project retrieve start -m Workflow` pulls one `.workflow` file per object carrying `rules`, `fieldUpdates`, `alerts` and `timeTriggers` — greppable and diffable, which is how you risk-rank rather than guess. → [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md), [10-soql-and-sosl · 10](../10-soql-and-sosl/10-querying-across-stores-and-tooling.md)
- **Retrieve the container, not the parts.** `Workflow` is the deployable unit; addressing `WorkflowRule` / `WorkflowFieldUpdate` individually in `package.xml` is unreliable for **standard** objects.
- **Rehearse in a sandbox that has queue entries in it.** A freshly refreshed sandbox will not, so stage 6 is the stage nobody tests.
- **Migrate inactive rules too.** They convert fine and need no activation switch, which makes them the safe place to learn the tool.

## 2026 currency

The one genuine change to the mechanics is **Winter '24**, and it is easy to misread: an **at-rest pending time-based action is migrated to a scheduled path when the associated record is changed.** That is a conditional, not a sweep — the entry moves when something touches the record, so pending actions on records nobody edits stay in the legacy queue indefinitely. The other 2026 shift is economic rather than mechanical: **stage 7 used to be where migrations were abandoned**, because consolidating twenty converted flows was unfunded work, and Summer '26's natural-language flow editing and flow summarisation make it materially cheaper. → [25](25-ai-assisted-flow-authoring.md)

## Gotchas

- **The migrated flow arrives inactive.** The most common failed migration is a complete set of correct flows sitting in Draft while the old rules carry on — nothing errors, nothing changes, and the project reports success.
- **Deactivating a rule does not cancel its pending actions.** They remain in the time-based queue and still fire; they leave only when processed, or when re-evaluation finds the record no longer meets criteria.
- **You cannot delete a workflow rule that has pending actions**, so the queue is not housekeeping — it is a hard blocker on decommissioning, and it dictates the programme's end date.
- **You cannot add or edit time-dependent actions on a deactivated rule that has pending actions**, which is how teams get stuck mid-migration unable to move either direction.
- **Activating the flow without deactivating the rule runs both**, and duplicate field updates and duplicate emails are the visible half; the invisible half is doubled DML.
- **Approval processes are entirely out of the tool's scope** — rebuilding them is a separate project, not a stage here. → [17](17-approval-orchestration.md)
- **Outbound messages have no real Flow equivalent**; budget for an HTTP callout or a platform event per message. → [12](12-http-callout-and-external-services-in-flow.md), [06-integration · 14](../06-integration-and-apis/14-legacy-streaming-and-outbound-messaging.md)
- **Converted time-dependent actions become scheduled paths**, which run in a different context and against different limits than the queue-based originals. → [06](06-scheduled-and-autolaunched-flows.md)

## Recall

Q: What is Salesforce's stated recommendation for Workflow Rules and Process Builder?
A: Migrate to Flow using the Migrate to Flow tool — GA for Workflow Rules since Summer '22 and Process Builder since Spring '23, and the only supported path.

Q: What does Switch Activations do?
A: Deactivates the workflow rule and activates the migrated flow together. The flow is created inactive, so without this step nothing changes.

Q: Does deactivating a workflow rule cancel its pending time-dependent actions?
A: No. They stay in the time-based workflow queue and still fire while the record meets criteria. Clear them at Setup → Monitoring → Time-Based Workflow.

Q: Why can a workflow rule refuse to be deleted?
A: It has pending actions in the time-based queue. The queue must be cleared first, which sets the real end date of a migration.

Q: What did Winter '24 change about pending time-based actions?
A: An at-rest pending action migrates to a scheduled path **when the associated record is changed** — a conditional, so untouched records keep their entries in the legacy queue.

## Related

- [26 · Reading inherited Workflow Rules & Process Builder](26-reading-inherited-workflow-and-process-builder.md) — the comprehension this runbook assumes
- [18 · Migrate to Flow & legacy automation](18-migrate-to-flow-and-legacy-retirement.md) — what the tool converts and what it silently changes
- [13 · Flow limits & bulkification](13-flow-limits-and-bulkification.md) — why a converted after-save flow can cost more than the rule it replaced
- [24 · Flow deployment, versioning & governance](24-flow-deployment-versioning-and-governance.md) — getting the converted flows through a pipeline as active
