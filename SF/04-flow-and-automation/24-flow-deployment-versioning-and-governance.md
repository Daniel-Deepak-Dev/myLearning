# Flow Deployment, Versioning & Governance

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Getting a flow from one org to another and keeping the estate maintainable — versions, activation, ownership and sprawl. The pipeline itself is [09-devops](../09-devops-sfdx-and-release-management/INDEX.md).

> **What changed.** *"Use the `FlowDefinition` metadata type to set which version is active"* was correct and is not. Since **Metadata API v44** only the **latest** version of a flow is retrievable and deployable, the `Flow` type carries its own **`status`** field (`Active` / `Draft` / `Obsolete` / `InvalidDraft`), and flow file names no longer carry version numbers. `FlowDefinition` still exists and using it to activate is explicitly discouraged.

## Core idea

Flow's versioning model is the source of most of its deployment surprises, and it comes down to two facts. **A flow can have many versions and exactly one active version**, so deploying a flow and enabling a flow are different operations — a change set or a `sf project deploy` that lands successfully in production can change absolutely nothing until something activates the version it delivered. And **the estate is the real problem, not the artefact**: fifty flows across twelve objects with no naming convention, no owner and error emails going to a developer who left is a governance failure that no deployment tool fixes. The version limit makes this concrete rather than aesthetic — **50 versions per flow**, after which you cannot save until you delete old ones, which is the platform's own way of telling you to stop editing production.

## How it works

| Concern | Mechanism |
|---|---|
| Which version is active | the `Flow` metadata **`status`** field — not `FlowDefinition` |
| Deploying as active | Setup → **Process Automation Settings** → *Deploy processes and flows as active* — **production only** |
| Version ceiling | **50 per flow** |
| Error email recipient | Process Automation Settings → *Send Process or Flow Email to* |
| Comparing versions | **Visual Flow Version Comparison** (Summer '26) |

- **The deploy-as-active setting does not appear in sandboxes or scratch orgs**, because there you can always deploy an active version. Its absence in a dev org is not a bug and is a common false alarm.
- **`Send Process or Flow Email to` has two values**: *User Who Last Modified the Process or Flow* — the default, and the reason so many flows fail silently — or *Apex Exception Email Recipients*. Change this on day one of any new org. → [10](10-fault-paths-and-custom-errors.md)
- **In-flight interviews stay on the version they started on**, so a deployed fix does not reach paused work. → [20](20-pause-wait-and-waiting-interviews.md)
- **Flow Tests deploy with the flow** as metadata and can gate a release. → [15](15-flow-testing-and-debugging.md)
- **A schedule does not always travel with a schedule-triggered flow** — verify start date and frequency in the target org after every deploy. → [06](06-scheduled-and-autolaunched-flows.md)

## 2026 currency

Summer '26 gives governance its first genuinely useful native instruments, which is notable because this has always been the part of Flow you were expected to solve with spreadsheets. **Visual Flow Version Comparison** puts two versions side by side on the canvas with a breakdown of Transform-element changes — the first credible answer to "what changed between these versions?" without a metadata diff. The **Element Error Rate column** on the Flows list view shows the failure percentage from the last execution, turning "which flow is broken?" into a sort. And **flow summarisation** can generate a description from the canvas and write it back to the flow's description metadata, which makes the naming-and-documentation part of governance cheap enough to actually do. → [25](25-ai-assisted-flow-authoring.md), [09-devops](../09-devops-sfdx-and-release-management/INDEX.md)

## Gotchas

- **Deploying does not activate.** Without *Deploy processes and flows as active*, a successful production deployment changes nothing.
- **`FlowDefinition` is the old activation mechanism.** Pipelines and tooling built before v44 still use it and produce confusing results.
- **50 versions per flow is a hard stop.** You cannot save a 51st until you delete old ones.
- **Only the latest version is retrievable** at v44+, so source control holds one version, not your version history.
- **Error emails default to the last modifier.** In an org with turnover that means nobody.
- **In-flight interviews ignore your deployment.** Fixing a bug does not fix work already paused. → [20](20-pause-wait-and-waiting-interviews.md)
- **Reordering flows creates versions too.** A Trigger Order change is a new version needing activation. → [14](14-trigger-order-and-flow-trigger-explorer.md)
- **Naming is the cheapest governance there is** and the first thing dropped. `Object_Trigger_Purpose` beats `New Flow 3` for the rest of the org's life.

## Recall

Q: Why can a successful flow deployment to production change nothing?
A: Deploying does not activate. *Deploy processes and flows as active* must be enabled in Process Automation Settings.

Q: What replaced `FlowDefinition` as the way to control which version is active?
A: The `Flow` metadata type's own `status` field, from Metadata API v44.

Q: How many versions can one flow have?
A: 50. After that you must delete old versions before you can save a new one.

Q: Who receives flow error emails by default, and where do you change it?
A: The user who last modified the flow. Process Automation Settings → *Send Process or Flow Email to*.

Q: What happens to a paused interview when you deploy a new active version?
A: Nothing — it resumes on the version it started on.

## Related

- [15 · Flow testing & debugging](15-flow-testing-and-debugging.md) — the tests that deploy alongside the flow
- [20 · Pause, Wait & waiting interviews](20-pause-wait-and-waiting-interviews.md) — the in-flight work a deployment cannot reach
- [09-devops](../09-devops-sfdx-and-release-management/INDEX.md) — `sf` CLI, packaging and the pipeline this fits inside
