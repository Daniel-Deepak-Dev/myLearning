# 04 · Flow & Automation

Flow as the **only** declarative automation tool you may build in, after Workflow Rules and Process Builder went out of support. **23 topics** · phases [08](PHASES.md), [09](PHASES.md).

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
| 13 | Flow limits & bulkification ⚠️ | shares Apex governor limits; loop-DML is the classic failure | 09 |
| 14 | Trigger order & Flow Trigger Explorer | Trigger Order 1–2000, run order across many flows | 09 |
| 15 | Flow testing & debugging *(GA Spring '23)* | Flow Tests, debug runs, rollback mode | 09 |
| 16 | Flow Orchestrator *(GA Spring '22)* | multi-stage, multi-user work items, decision steps | 09 |
| 17 | Approval Orchestration 🆕⚠️ | the modern approval path; classic approvals in maintenance | 09 |
| 18 | Migrate to Flow & legacy retirement 🆕⚠️ | migration tool, support timeline, conversion traps | 09 |
| 19 | Flow for external & guest users | run-as context, guest hardening, Experience Cloud embedding | 09 |
| 20 | Data Cloud-triggered flows & data actions 🆕 | Data 360 triggers, data actions into core | 09 |
| 21 | Flows as Agentforce actions 🆕 | autolaunched flow actions, description-as-contract | 09 |
| 22 | Flow deployment, versioning & governance | active-version deploys, naming, ownership, sprawl control | 09 |
| 23 | AI-assisted flow authoring 🆕 | describe-to-flow generation and how to review output | 09 |

## Related

- **11, 13** depend on [02-apex · 01 governor limits](../02-apex-and-triggers/01-apex-language-core-and-governor-limits.md) and **· 22 invocable Apex** — Flow shares the same transaction budget.
- **04–05** pair with [03-lwc · 11 LWC in Flow screens](../03-lwc-and-slds/11-lwc-in-flow-screens-and-quick-actions.md) — that note owns the component-authoring contract, these own the designer's side.
- **12** pairs with [02-apex · 19 Callouts & named credentials](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) — one credential model, two ways to reach it.
- **17** pairs with [01-admin · 12 Approval processes](../01-admin-and-declarative-platform/12-approval-processes-and-approval-orchestration.md).
- **19** pairs with [05-experience-cloud · 07 Guest user security](../05-experience-cloud-lwr/INDEX.md).
- **20–21, 23** are seams into [AI_Data/](../../AI_Data/README.md) — the agent and Data 360 story lives there.
