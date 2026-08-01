# 04 · Flow & Automation

Flow as the **single** declarative automation tool, post Workflow/Process Builder end-of-life. **21 topics** · phases [08](PHASES.md), [09](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Workflow Rules and Process Builder are retired.** Any tutorial that offers a "which tool should I use?" decision tree with three declarative options is out of date. The answer is Flow, and the remaining decision is *which kind* of Flow.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Automation landscape & tool selection ⚠️ | Flow-first; WF and Process Builder retired | 08 |
| 02 | Flow anatomy & builder basics | elements, resources, auto-layout, versioning | 08 |
| 03 | Record-triggered flows | before-save vs after-save, entry criteria, run order | 08 |
| 04 | Screen flows & UX design | screen components, validation, navigation model | 08 |
| 05 | Reactive screen flows 🆕 | cross-component reactivity, formula-driven visibility | 08 |
| 06 | Scheduled & autolaunched flows | schedule paths, batch behaviour, bulk safety | 08 |
| 07 | Platform event & async path flows | event-triggered flows, async path use cases | 08 |
| 08 | Subflows & modular flow design | reuse, contracts, when to split | 08 |
| 09 | Collections, loops & the Transform element 🆕 | filter/sort, Transform replaces loop-assign | 08 |
| 10 | Fault paths & custom errors | fault connectors, custom error element, rollback behaviour | 08 |
| 11 | Flow & Apex interop | invocable Apex, generic sObject inputs, typed UDTs | 08 |
| 12 | Flow limits & bulkification ⚠️ | shares Apex governor limits; loop-DML is the classic failure | 09 |
| 13 | Flow testing & debugging *(GA Spring '23)* | Flow Tests, debug runs, rollback mode | 09 |
| 14 | Flow Orchestrator *(GA Spring '22)* | multi-stage, multi-user work items, decision steps | 09 |
| 15 | Approval Orchestration 🆕⚠️ | the modern approval path; classic approvals in maintenance | 09 |
| 16 | Migrate to Flow & legacy retirement 🆕⚠️ | migration tool, retirement timeline, conversion traps | 09 |
| 17 | Flow for external & guest users | run-as context, guest hardening, Experience Cloud embedding | 09 |
| 18 | Data Cloud-triggered flows & data actions 🆕 | Data 360 triggers, data actions into core | 09 |
| 19 | Flows as Agentforce actions 🆕 | autolaunched flow actions, description-as-contract | 09 |
| 20 | Flow deployment, versioning & governance | active-version deploys, naming, ownership, sprawl control | 09 |
| 21 | AI-assisted flow authoring 🆕 | describe-to-flow generation and how to review output | 09 |

## Related

- **11–12** depend on [02-apex · 01 governor limits](../02-apex-and-triggers/INDEX.md) and **· 22 invocable Apex** — Flow shares the same transaction budget.
- **15** pairs with [01-admin · 12 Approval processes](../01-admin-and-declarative-platform/INDEX.md).
- **17** pairs with [05-experience-cloud · 07 Guest user security](../05-experience-cloud-lwr/INDEX.md).
- **18–19, 21** are seams into [AI_Data/](../../AI_Data/README.md) — the agent and Data 360 story lives there.
