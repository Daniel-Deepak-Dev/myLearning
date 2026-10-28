---
vault: SF_core
area: 04-flow-and-automation
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 9
tags: [currency-warning]
---
# Flow Testing & Debugging

**Scope:** Proving a flow works before users find out it doesn't — Flow Tests, debug runs, and the Summer '26 diagnostic surface. Deploying the result is [24](24-flow-deployment-versioning-and-governance.md).

> **What changed.** *"Flow has tests now, like Apex"* overstates it. **Flow Tests (GA Spring '23) started as record-triggered only. They now cover record-triggered, autolaunched and Data Cloud-triggered flows** — autolaunched since API 66.0 — but not delete triggers, not paths that run asynchronously, and not screen, schedule-triggered or platform event-triggered flows. Everything outside that box is still tested by debug run and by hand. Summer '26's *Visualize Execution Path when testing screen flows* is an enhancement to the **debug run**, not an extension of Flow Tests, and conflating the two is how a release-notes headline becomes a false sense of coverage.

## Core idea

Flow's testing story is two unrelated tools wearing similar names. A **debug run** is an interactive session in the builder: you supply inputs, watch each element execute, and read the resulting values — repeatable by a human, not by a pipeline. A **Flow Test** is a saved, re-runnable assertion stored *with* the flow as metadata: initial record values, optional prior values for an update trigger, and assertions on what the flow produced. Only the second one survives a deployment and can gate a release. The practical consequence is that coverage in this area is uneven by design — your record-triggered automation can be genuinely tested while your screen flows cannot be, so the risk budget should move accordingly. **Flow tests do not count toward Apex code coverage** and never have; a deployment that needs 75% still needs Apex tests.

## How it works

| | Debug run | Flow Test |
|---|---|---|
| Flow types | all | **record-triggered, autolaunched, Data Cloud-triggered** |
| Paths | any, including scheduled | **not asynchronous paths** 🚩, not delete |
| Persisted | no | **yes** — metadata, deploys with the flow |
| Rollback | *Roll back mode* available | changes are rolled back |
| Run as another user | yes | no |

- **Debug run offers three switches worth knowing**: roll back the transaction at the end, run as another user, and skip the start-condition check so you can test the body without engineering a qualifying record.
- **A Flow Test defines a triggering record and, for update triggers, a prior version** — which is the only clean way to exercise `$Record__Prior` logic. → [03](03-record-triggered-flows.md)
- **Assertions are per-element outcome and per-variable value**, and a test with no assertion passes as long as the flow does not error, which is not a test.
- **Tests run from the flow's *View Tests* list or during a deployment** with the appropriate test level. → [24](24-flow-deployment-versioning-and-governance.md)
- **Fault paths need testing deliberately**, because the failure they report is invisible in a happy-path debug run. → [10](10-fault-paths-and-custom-errors.md)

## 2026 currency

Summer '26 is a diagnostics release for Flow rather than a testing one. **Troubleshoot Flow Errors with Agentforce is Beta** — it reads both design-time problems in a saved flow and runtime failures, proposes a fix and can apply it, and it requires Data 360 and Agentforce provisioning, so it is not available just because you are on 67.0. **Execution Path Visualization** highlights the route a screen flow actually took during a debug run. **Visual Flow Version Comparison** puts two versions side by side on the canvas with a breakdown of Transform-element changes, which is the first honest answer to "what did this version change?" The **redesigned validation panel** now stays closed by default and groups errors by element in cards, and the **Element Error Rate column** on the Flows list view surfaces the failure percentage from the last execution. **Winter '27 adds Flow Test Mode, and it is Beta at 68.0.** You switch it on in Process Automation Settings (*Enable Flow Test Mode (Beta)*); the builder then splits into Build and Test modes for record-triggered and autolaunched flows, saves reusable test scenarios, and can **mock the output of an Action or Subflow element** so no callout fires. A target org needs the Beta switched on too. **Troubleshoot Flow Errors with Agentforce is still Beta at 68.0.** → [SF_Agentforce/](../../SF_Agentforce/INDEX.md), [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md)

## Gotchas

- **Flow Tests do not exist for screen flows.** If your org's automation is screen-heavy, your automated coverage is zero regardless of how many tests the Flows list shows.
- **Flow Tests do not cover asynchronous paths or delete triggers**, which are exactly the paths hardest to test by hand. 🚩 One release note says scheduled paths are now supported; current Help says asynchronous paths are not — check in an org.
- **Flow tests contribute nothing to Apex code coverage.** A deployment blocked at 74% is not unblocked by adding flow tests.
- **A test with no assertions is a smoke test.** It proves the flow did not throw, not that it did the right thing.
- **Debug run *without* roll back mode writes real records.** In a sandbox that is untidy; in production it is an incident.
- **Debugging as another user does not reproduce every context difference** — a record-triggered flow's execution context is fixed regardless of who runs it. → [19](19-flow-run-context-and-sharing.md)
- **Troubleshoot with Agentforce is Beta and gated on Data 360**, so it is not a plan for orgs that do not have it.
- **The unhandled-error email still goes to the flow's last modifier**, so a test suite is not a substitute for setting an error recipient. → [10](10-fault-paths-and-custom-errors.md)

## Recall

Q: Which flow types can have Flow Tests?
A: Record-triggered, autolaunched and Data Cloud-triggered flows. Not screen, schedule-triggered or platform event-triggered flows, and not delete triggers or asynchronous paths.

Q: What is the difference between a debug run and a Flow Test?
A: A debug run is interactive and disposable; a Flow Test is metadata that deploys with the flow and can be re-run.

Q: Do flow tests count toward the 75% code coverage a production deployment needs?
A: No. That figure is Apex-only.

Q: What did Summer '26 add for screen flow testing, and what did it *not* add?
A: Execution Path Visualization on a debug run — not Flow Test support for screen flows.

Q: What are the three switches on a debug run?
A: Roll back the transaction, run as another user, and skip the start condition.

## Related

- [10 · Fault paths & custom errors](10-fault-paths-and-custom-errors.md) — the failure behaviour you should be writing tests against
- [02-apex · 20 Apex testing fundamentals](../02-apex-and-triggers/20-apex-testing-fundamentals.md) — the mature side of the same problem, and where coverage percentages come from
- [24 · Deployment, versioning & governance](24-flow-deployment-versioning-and-governance.md) — running these tests as a release gate

## Sources

- [Metadata API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-10-28 · `FlowTest`: *"Before you activate a record-triggered, autolaunched, or Data Cloud-triggered flow, you can test it"*; autolaunched data-source and isolated-object fields available in API 66.0 and later
- [Metadata API Developer Guide (PDF, v67.0)](https://resources.docs.salesforce.com/262/latest/en-us/sfdc/pdf/api_meta.pdf) — Salesforce Developers · read 2026-10-28 · same `FlowTest` wording at Summer '26, so "record-triggered only" was already wrong when this note was written
- [Automatically Test Record-Triggered, Autolaunched, and Data Cloud-Triggered Flows](https://help.salesforce.com/s/articleView?id=platform.automate_flow_test_record_data_cloud_triggered.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · flow types covered; flow tests don't support delete triggers or paths that run asynchronously
- [Test Flows in a Dedicated Test Mode (Beta)](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_automate_flow_test_mode.htm&release=264&type=5) — Salesforce Help · via search 2026-10-28 · Winter '27 Test Mode is Beta
- [Flow Test Mode (Beta): The Future of Flow Testing](https://admin.salesforce.com/blog/2026/flow-test-mode-beta-the-future-of-flow-testing) — Salesforce Admins · via search 2026-10-28 · setting name, record-triggered and autolaunched scope, mock outputs for Action and Subflow, target org needs the Beta on
- [Troubleshoot and Fix Flow Errors with Agentforce (Beta)](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_automate_flow_builder_troubleshoot_and_fix_flow_errors_with_agentforce_beta.htm&release=262&type=5) — Salesforce Help · via search 2026-10-28 · still labelled Beta; no Winter '27 GA note found

## History

- 2026-10-28 · Winter '27 currency check: corrected Flow Test scope (autolaunched and Data Cloud-triggered flows are covered), added Flow Test Mode (Beta)
