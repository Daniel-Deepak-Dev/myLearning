# Phases for 01 · Admin & Declarative Platform

19 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

---

## Phase 01 — Declarative bedrock · 11 files ⬜

The vocabulary everything else assumes. No 🆕 topics — this is stable platform, so it can be written without release-note research, **except** the ⚠️ ones.

```
01-org-anatomy-and-editions.md
02-release-cadence-and-release-updates.md          ⚠️
03-objects-fields-and-relationships.md
04-record-types-and-picklist-architecture.md
07-formula-fields-and-roll-up-summaries.md
08-validation-rules-and-duplicate-management.md
09-custom-metadata-vs-custom-settings.md           ⚠️
10-custom-labels-and-translation-workbench.md
11-queues-assignment-and-escalation-rules.md
13-data-import-export-and-loading-tools.md         ⚠️
14-order-of-execution-declarative-view.md
```

**⚠️ corrections to lead with**
- **02** — Release Updates are not optional advisories; they **auto-enforce** on a stated release. The old "review when convenient" posture is wrong.
- **09** — Custom Settings are not the default choice any more. **Custom Metadata Types are deployable, packageable and don't consume SOQL queries.** Reach for Custom Settings only for per-user/per-profile hierarchy values.
- **13** — Data Loader now runs on **Bulk API 2.0** by default. Guidance written against Bulk v1 batch-splitting no longer describes what happens.

**Watch:** **14** must agree exactly with [02-apex · 07 Order of execution](../02-apex-and-triggers/INDEX.md), which is written in phase 03. Whichever lands second reconciles against the first — do not let two save-order lists drift.

---

## Phase 02 — Modern admin surface & org ops · 8 files ⬜

Everything an admin does that changed after 2021.

```
05-dynamic-forms-and-lightning-app-builder.md      🆕⚠️
06-dynamic-actions-and-list-views.md               ⚠️
12-approval-processes-and-approval-orchestration.md 🆕⚠️
15-mobile-app-notification-builder-and-briefcase.md
16-search-configuration-and-einstein-search.md
17-setup-audit-trail-monitoring-and-usage.md
18-salesforce-foundations-and-org-strategy.md      🆕
19-agentforce-in-setup-and-ai-assisted-admin.md    🆕
```

**🆕 — research before writing, do not draft from recall**
- **05** — confirm current Dynamic Forms object coverage and the page-layout deprecation posture.
- **12** — confirm what Approval Orchestration supports vs classic approval processes today, and whether classic is deprecated or merely in maintenance. **Do not assert a retirement date without a source.**
- **18** — Foundations SKU: what's actually included, and which editions.
- **19** — the AI-assisted Setup surface moves fast; cite what you find.

**⚠️ corrections to lead with**
- **05** — page layouts are no longer where field visibility is designed; Dynamic Forms are.
- **06** — button/action visibility is set by **Dynamic Actions** rules, not by layout assignment per record type.

**Cross-links:** **19** → [AI_Data/02-salesforce-ai/INDEX.md](../../AI_Data/02-salesforce-ai/INDEX.md). Link, don't duplicate. **12** → [04-flow · 15 Approval Orchestration](../04-flow-and-automation/INDEX.md), written in phase 09 — that one carries the Flow mechanics, this one carries the admin-surface view.

---

## Seed material

[../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) has **almost nothing** for this area. Treat both phases as greenfield and source from current docs.
