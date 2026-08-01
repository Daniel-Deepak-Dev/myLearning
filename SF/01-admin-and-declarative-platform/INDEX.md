# 01 · Admin & Declarative Platform

The declarative surface an architect must know cold before writing any code. **19 topics** · phases [01](PHASES.md), [02](PHASES.md) — **both complete ✅**.

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **The near-total greenfield area.** [_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) found essentially no legacy notes behind this area — the old corpus is lopsided toward Apex and SOQL. All 19 were authored from current docs, so every claim here is as good as its source and dated by [CURRENCY.md](../CURRENCY.md).

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [Org anatomy & editions](01-org-anatomy-and-editions.md) | org types, editions, Setup map, hard limits | 01 |
| 02 | [Release cadence & Release Updates](02-release-cadence-and-release-updates.md) ⚠️ | 3 releases/yr, preview orgs, Release Updates auto-enforce | 01 |
| 03 | [Objects, fields & relationships](03-objects-fields-and-relationships.md) | standard vs custom, lookup/master-detail/junction, field types | 01 |
| 04 | [Record types & picklist architecture](04-record-types-and-picklist-architecture.md) | record types, global value sets, dependent picklists | 01 |
| 05 | [Dynamic Forms & Lightning App Builder](05-dynamic-forms-and-lightning-app-builder.md) 🆕⚠️ | all LWC-enabled standard objects since Winter '24; layouts demoted, **not retired** | 02 |
| 06 | [Dynamic Actions & list views](06-dynamic-actions-and-list-views.md) ⚠️ | action visibility rules replace layout-driven buttons | 02 |
| 07 | [Formula fields & roll-up summaries](07-formula-fields-and-roll-up-summaries.md) | cross-object formulas, compile size, roll-up limits | 01 |
| 08 | [Validation rules & duplicate management](08-validation-rules-and-duplicate-management.md) | enforcement point, matching vs duplicate rules | 01 |
| 09 | [Custom Metadata vs Custom Settings](09-custom-metadata-vs-custom-settings.md) ⚠️ | CMDT is deployable, packageable, limit-free in **Apex** SOQL (not Flow) | 01 |
| 10 | [Custom labels & Translation Workbench](10-custom-labels-and-translation-workbench.md) | label reuse across Apex/LWC/Flow, translation workflow | 01 |
| 11 | [Queues, assignment & escalation rules](11-queues-assignment-and-escalation-rules.md) | declarative routing, evaluation order, ownership effects | 01 |
| 12 | [Approval processes & Approval Orchestration](12-approval-processes-and-approval-orchestration.md) 🆕⚠️ | Flow approvals are the modern path; Orchestration free since 2026-02-18; classic **not** retired | 02 |
| 13 | [Data import, export & loading tools](13-data-import-export-and-loading-tools.md) ⚠️ | Import Wizard, Data Loader, Bulk API 2.0 **opt-in** (SOAP is the default) | 01 |
| 14 | [Order of execution — declarative view](14-order-of-execution-declarative-view.md) | where each automation type fires in the save | 01 |
| 15 | [Mobile app, Notification Builder & Briefcase](15-mobile-app-notification-builder-and-briefcase.md) | mobile config, custom notifications, offline briefcase | 02 |
| 16 | [Search configuration & Einstein Search](16-search-configuration-and-einstein-search.md) | search layouts, synonyms, Einstein Search on by default | 02 |
| 17 | [Setup Audit Trail, monitoring & usage](17-setup-audit-trail-monitoring-and-usage.md) | Audit Trail 180 days, Lightning Usage App, job monitors | 02 |
| 18 | [Salesforce Foundations & org strategy](18-salesforce-foundations-and-org-strategy.md) 🆕 | $0 add-on, auto-provisions Data 360, single vs multi-org | 02 |
| 19 | [Agentforce in Setup & AI-assisted admin](19-agentforce-in-setup-and-ai-assisted-admin.md) 🆕 | Setup with Agentforce GA, non-billable, review discipline | 02 |

## Related

- [14 · Order of execution](14-order-of-execution-declarative-view.md) pairs with [02-apex-and-triggers · 07 Order of execution & recursion](../02-apex-and-triggers/INDEX.md) — the declarative view and the Apex view are the same save order seen from two sides. **The declarative view landed first (phase 01), so it is the reference the Apex note reconciles against.**
- [19 · Agentforce in Setup](19-agentforce-in-setup-and-ai-assisted-admin.md) is the seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — the admin surface here, the agent platform there.
- [05 · Dynamic Forms](05-dynamic-forms-and-lightning-app-builder.md) and [06 · Dynamic Actions](06-dynamic-actions-and-list-views.md) are one shift seen twice: visibility became a rule on a component instead of an assignment of a layout. Read them together.
- [12 · Approvals](12-approval-processes-and-approval-orchestration.md) pairs with [04-flow · 15 Approval Orchestration](../04-flow-and-automation/INDEX.md), written in phase 09 — this note holds the choice and the admin surface, that one holds the Flow mechanics.
