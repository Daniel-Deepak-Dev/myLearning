# Phases for 01 · Admin & Declarative Platform

19 topics across 2 runs — **both complete**. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

---

## Phase 01 — Declarative bedrock · 11 files ✅

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
- **13** — ~~Data Loader now runs on **Bulk API 2.0** by default.~~ **Corrected during phase 01 against the Data Loader Guide: this was wrong.** Data Loader **still defaults to the SOAP-based API**; *Use Bulk API* (v1) and *Use Bulk API 2.0* are two separate opt-in checkboxes. The real correction is that the old "tick Use Bulk API" advice is now ambiguous, and that enabling either Bulk path silently disables *Insert null values* and *Allow field truncation*.

**Watch:** **14** must agree exactly with [02-apex · 07 Order of execution](../02-apex-and-triggers/INDEX.md), which is written in phase 03. Whichever lands second reconciles against the first — do not let two save-order lists drift.

---

## Phase 02 — Modern admin surface & org ops · 8 files ✅

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

**🆕 — research before writing, do not draft from recall** · *all four researched; findings below*
- **05** — coverage: **all LWC-enabled standard objects since Winter '24** (`Note` excluded, fixed layout). Deprecation posture: **page layouts are NOT deprecated** — no retirement announced, and they still own related lists, actions, compact layouts, Classic and the required/read-only field properties.
- **12** — **Flow Approval Processes** is the platform name; it runs as an approval orchestration. Classic is **neither deprecated nor retired** — the docs were renamed *Classic Approval Processes* and Flow approvals are positioned as the "modern alternative". The real news is licensing: **Flow Orchestration became a standard flow type on 2026-02-18**, no add-on, no usage-based run limits.
- **18** — **$0 built-in add-on**; Enterprise, Unlimited, Einstein 1 Sales, Einstein 1 Service. Auto-provisions **Data 360**; ships **200K Flex credits** and ~2,000 email sends/month; overage bills after that.
- **19** — **Setup with Agentforce is GA** and **Setup actions are non-billable** (no Flex credits). Acts only on approval, only within the running user's permissions, and writes to **Setup Audit Trail**.

**⚠️ corrections to lead with** · *both held, 05 needed a guard rail*
- **05** — page layouts are no longer where field visibility is designed; Dynamic Forms are. **But do not overstate it into "layouts are legacy/gone"** — that was the wording in this plan and in the INDEX row, and the docs do not support it. Both corrected.
- **06** — button/action visibility is set by **Dynamic Actions** rules, not by layout assignment per record type. Held. Added gate: standard-object dynamic actions require Setup → *Salesforce Mobile App* → **Enable Dynamic Actions on Mobile**.

**Cross-links:** **19** → [AI_Data/02-salesforce-ai/INDEX.md](../../AI_Data/02-salesforce-ai/INDEX.md). Link, don't duplicate. **12** → [04-flow · 17 Approval Orchestration](../04-flow-and-automation/17-approval-orchestration.md), written in phase 09 *(numbered 15 at plan time; area 04 renumbered in phase 09)* — that one carries the Flow mechanics, this one carries the admin-surface view.

---

## Seed material

[../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) has **almost nothing** for this area. Treat both phases as greenfield and source from current docs.
