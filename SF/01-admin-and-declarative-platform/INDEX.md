# 01 · Admin & Declarative Platform

The declarative surface an architect must know cold before writing any code. **19 topics** · phases [01](PHASES.md), [02](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **The near-total greenfield area.** [_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) found essentially no legacy notes behind this area — the old corpus is lopsided toward Apex and SOQL. Expect to author all 19 from current docs.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | Org anatomy & editions | org types, editions, Setup map, hard limits | 01 |
| 02 | Release cadence & Release Updates ⚠️ | 3 releases/yr, preview orgs, Release Updates auto-enforce | 01 |
| 03 | Objects, fields & relationships | standard vs custom, lookup/master-detail/junction, field types | 01 |
| 04 | Record types & picklist architecture | record types, global value sets, dependent picklists | 01 |
| 05 | Dynamic Forms & Lightning App Builder 🆕⚠️ | Dynamic Forms now cover all objects; page layouts legacy | 02 |
| 06 | Dynamic Actions & list views ⚠️ | action visibility rules replace layout-driven buttons | 02 |
| 07 | Formula fields & roll-up summaries | cross-object formulas, compile size, roll-up limits | 01 |
| 08 | Validation rules & duplicate management | enforcement point, matching vs duplicate rules | 01 |
| 09 | Custom Metadata vs Custom Settings ⚠️ | CMDT is deployable, packageable, limit-free in SOQL | 01 |
| 10 | Custom labels & Translation Workbench | label reuse across Apex/LWC/Flow, translation workflow | 01 |
| 11 | Queues, assignment & escalation rules | declarative routing, evaluation order, ownership effects | 01 |
| 12 | Approval processes & Approval Orchestration 🆕⚠️ | Flow Approval Orchestrator supersedes classic approvals | 02 |
| 13 | Data import, export & loading tools ⚠️ | Import Wizard, Data Loader, Bulk API 2.0 default | 01 |
| 14 | Order of execution — declarative view | where each automation type fires in the save | 01 |
| 15 | Mobile app, Notification Builder & Briefcase | mobile config, custom notifications, offline briefcase | 02 |
| 16 | Search configuration & Einstein Search | search layouts, synonyms, pinned/personalized results | 02 |
| 17 | Setup Audit Trail, monitoring & usage | Audit Trail, Lightning Usage App, background jobs | 02 |
| 18 | Salesforce Foundations & org strategy 🆕 | Foundations SKU, single-org vs multi-org trade-offs | 02 |
| 19 | Agentforce in Setup & AI-assisted admin 🆕 | AI metadata assist, describe-to-config, review discipline | 02 |

## Related

- [14 · Order of execution](#) pairs with [02-apex-and-triggers · 07 Order of execution & recursion](../02-apex-and-triggers/INDEX.md) — the declarative view and the Apex view are the same save order seen from two sides.
- [19 · Agentforce in Setup](#) is the seam into [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md).
