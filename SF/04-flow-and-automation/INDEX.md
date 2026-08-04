# 04 · Flow & Automation

Flow as the **only** declarative automation tool you may build in, after Workflow Rules and Process Builder went out of support. **25 topics** · phases [08](PHASES.md), [09](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Workflow Rules and Process Builder are *out of support*, not retired.** Support ended **31 December 2025** — no bug fixes, no support cases — and creation was blocked back in Winter '23. **Existing automations still run and no retirement date has been announced.** Any tutorial offering a three-way declarative decision tree is out of date; so is anyone telling a client the old tools have stopped.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Automation landscape & tool selection](01-automation-landscape-and-tool-selection.md) ⚠️ | Flow-first; WF/PB end of support; the Flow-vs-Apex line | 08 |
| 02 | [Flow anatomy & builder basics](02-flow-anatomy-and-builder-basics.md) | elements vs resources, auto-layout, versioning | 08 |
| 03 | [Record-triggered flows](03-record-triggered-flows.md) | before-save vs after-save, entry criteria, `$Record__Prior` | 08 |
| 04 | [Screen flows & UX design](04-screen-flows-and-ux-design.md) | screen components, validation, navigation model | 08 |
| 05 | [Reactive screen flows](05-reactive-screen-flows.md) 🆕 | cross-component reactivity **+ Screen Actions** | 08 |
| 06 | [Scheduled & autolaunched flows](06-scheduled-and-autolaunched-flows.md) | the running user, schedule paths, Summer '26 batch size | 08 |
| 07 | [Platform event & async path flows](07-platform-event-and-async-path-flows.md) | leaving the save transaction, event subscriber limits | 08 |
| 08 | [Subflows & modular flow design](08-subflows-and-modular-flow-design.md) | the input/output contract; **no limit relief** | 08 |
| 09 | [Collections, loops & the Transform element](09-collections-loops-and-the-transform-element.md) 🆕 | filter/sort, Transform replaces loop-assign | 08 |
| 10 | [Fault paths & custom errors](10-fault-paths-and-custom-errors.md) ⚠️ | **fault paths don't roll back; Custom Error does** | 08 |
| 11 | [Flow & Apex interop](11-flow-and-apex-interop.md) | invocable actions, Apex-defined types, `Flow.Interview` | 08 |
| 12 | [HTTP callout & External Services](12-http-callout-and-external-services-in-flow.md) 🆕 | calling an API with no Apex, and where that stops | 08 |
| 13 | [Flow limits & bulkification](13-flow-limits-and-bulkification.md) ⚠️ | **the 2,000-element cap was removed at API 57.0**; CPU is the wall | 09 |
| 14 | [Trigger order & Flow Trigger Explorer](14-trigger-order-and-flow-trigger-explorer.md) | Trigger Order 1–2,000, per trigger type only | 09 |
| 15 | [Flow testing & debugging](15-flow-testing-and-debugging.md) ⚠️ | **Flow Tests are record-triggered only**; debug run does the rest | 09 |
| 16 | [Flow Orchestrator](16-flow-orchestrator.md) *(GA Spring '22)* | stages, steps, work items — **standard feature since 2026-02-18** | 09 |
| 17 | [Approval Orchestration](17-approval-orchestration.md) 🆕⚠️ | **classic approvals are not deprecated**; approvals callable from any flow | 09 |
| 18 | [Migrate to Flow & legacy automation](18-migrate-to-flow-and-legacy-retirement.md) 🆕⚠️ | one-to-one conversion, recursion loss, the double-run trap | 09 |
| 19 | [Flow run context & sharing](19-flow-run-context-and-sharing.md) ⚠️ | **running user ≠ execution context**; triggered flows bypass sharing | 09 |
| 20 | [Pause, Wait & waiting interviews](20-pause-wait-and-waiting-interviews.md) ⚠️ | **the paused-interview cap is gone**; `FlowInterview` debt | 09 |
| 21 | [Flow for external & guest users](21-flow-for-external-and-guest-users.md) | **`Run Flows` is gone from the guest profile** — per-flow access | 09 |
| 22 | [Data 360-triggered flows & data actions](22-data-cloud-triggered-flows-and-data-actions.md) 🆕 | DMO/CIO triggers, data action targets, activation-triggered flows | 09 |
| 23 | [Flows as Agentforce actions](23-flows-as-agentforce-actions.md) 🆕 | autolaunched only, description-as-contract, the locked interface | 09 |
| 24 | [Flow deployment, versioning & governance](24-flow-deployment-versioning-and-governance.md) ⚠️ | **`FlowDefinition` is not how you activate**; 50 versions; error email | 09 |
| 25 | [AI-assisted flow authoring](25-ai-assisted-flow-authoring.md) 🆕 | generate, edit and summarise in natural language — and how to review it | 09 |

## Related

- **11, 13** depend on [02-apex · 01 governor limits](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md) and **· 22 invocable Apex** — Flow shares the same transaction budget.
- **04–05** pair with [03-lwc · 11 LWC in Flow screens](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md) — that note owns the component-authoring contract, these own the designer's side.
- **12** pairs with [02-apex · 19 Callouts & named credentials](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) — one credential model, two ways to reach it.
- **17** pairs with [01-admin · 12 Approval processes](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md).
- **19** is the security spine of the area — [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) is its coded counterpart, and Flow did **not** follow Apex's 67.0 flip to user mode.
- **21** pairs with [05-experience-cloud · 07 Guest user security model](../05-experience-cloud-lwr/07-guest-user-security-model.md), and every flow on *Enabled Flow Access* is an item on [**· 11** the public site exposure audit](../05-experience-cloud-lwr/11-public-site-exposure-audit.md).
- **22–23, 25** are seams into [AI_Data/](../../AI_Data/README.md) — the agent and Data 360 story lives there.
