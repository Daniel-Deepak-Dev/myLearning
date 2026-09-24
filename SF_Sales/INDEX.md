# SF_Sales

> **Start at [../HOME.md](../HOME.md)** — what to study next, rebuilt from the notes.

Sales Cloud only — now branded **Agentforce Sales**. Leads and conversion, opportunities and Path, products, quotes and orders, teams and splits, territories, forecasts, campaigns, Pipeline Inspection and Einstein Activity Capture.

The platform pieces underneath — assignment rules, record types, the share rows teams add, the object graph, multi-currency — live in [SF_core/](../SF_core/README.md) and are linked from each note. A Sales agent is built in [SF_Agentforce/](../SF_Agentforce/INDEX.md); a partner site's licence and sharing are [SF_Experience_Cloud · 08](../SF_Experience_Cloud/08-licences-and-external-user-types.md).

> Currency: **Summer '26 (API 67.0)** · what changed: [SF_core/CURRENCY.md](../SF_core/CURRENCY.md), section *New in Sales Cloud* · renames that kept their API names: [AGENTS.md](AGENTS.md#four-live-currency-traps)

## Learning path

Read top to bottom. `#` is display order only — filenames carry no number, so reordering costs one row edit. Leads and opportunities come first because every other note hangs off the opportunity. Forecasts come after teams and territories because two of their forecast types need them.

**10 topics** · 31 gaps open · 0 complete · newest 2026-09-24 · oldest 2026-09-24

**13 org checks** sit under `## Confirm in org` across 10 notes. Those are sandbox to-dos, not research — they do not count as gaps and do not stop a note being complete.

**40 hands-on labs · ~13 h.** This file is the reading order. When the goal is to *do* something, open [PRACTICE.md](PRACTICE.md) instead — it queues every lab unblocked-first, so the first 19 need nothing but a Developer Edition org.

| # | Topic | One line | Level | Status | Org ✓ | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|---|
| 1 | [Lead Management & Conversion](lead-management-and-conversion.md) | Web-to-Lead, lead routing, and the one-way convert into Account, Contact and Opportunity | basic | 🌱 3 open | 2 | — | 2026-09-24 | 2026-09-24 |
| 2 | [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) | Stage drives probability, forecast category and won/lost; sales processes, Path, history | basic | 🌱 3 open | 2 | 1 | 2026-09-24 | 2026-09-24 |
| 3 | [Products & Price Books](products-and-price-books.md) | Product2 → PricebookEntry → line item: standard price first, one price book per deal | basic | 🌱 3 open | 1 | 2 | 2026-09-24 | 2026-09-24 |
| 4 | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) | Quote sync, quote PDFs, order and contract activation — and what locks after it | working | 🌱 3 open | 1 | 3 | 2026-09-24 | 2026-09-24 |
| 5 | [Campaigns & Campaign Influence](campaigns-and-campaign-influence.md) | Members and statuses, hierarchy rollups, ROI, and credit back to opportunities | basic | 🌱 3 open | 2 | 2 | 2026-09-24 | 2026-09-24 |
| 6 | [Account & Opportunity Teams](account-and-opportunity-teams.md) | Who sells an account or deal with its owner, in what role, and how splits share credit | working | 🌱 3 open | 1 | 2 | 2026-09-24 | 2026-09-24 |
| 7 | [Enterprise Territory Management](enterprise-territory-management.md) | Now *Sales Territories* — models and rules that place accounts, leads and users in territories | working | 🌱 4 open | 1 | 6 | 2026-09-24 | 2026-09-24 |
| 8 | [Collaborative Forecasts](collaborative-forecasts.md) | Now *Pipeline Forecasting* — forecast types, categories, rollups, hierarchy, adjustments, quotas | working | 🌱 2 open | 1 | 2 | 2026-09-24 | 2026-09-24 |
| 9 | [Pipeline Inspection](pipeline-inspection.md) | The opportunity list with pipeline-change metrics and deal insights, and what gates it | basic | 🌱 4 open | 1 | 8 | 2026-09-24 | 2026-09-24 |
| 10 | [Einstein Activity Capture](einstein-activity-capture.md) | Gmail and Microsoft 365 email and calendar capture: where the data lives, licences, configurations | working | 🌱 3 open | 1 | — | 2026-09-24 | 2026-09-24 |

## Seams into SF_core

These `SF_core` notes own the platform side. Link to them rather than restating.

| Topic | SF_core note |
|---|---|
| Lead assignment rules, and the `AssignmentRuleHeader` an API load needs | [01-admin · 11 Queues, assignment & escalation rules](../SF_core/01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) |
| The validation and duplicate rules lead conversion partly skips | [01-admin · 08 Validation rules & duplicate management](../SF_core/01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) |
| Record types and the business process a sales process is | [01-admin · 04 Record types & picklist architecture](../SF_core/01-admin-and-declarative-platform/04-record-types-and-picklist-architecture.md) |
| The share rows teams and territories add — the sharing half of #6 and #7 | [07-security · 10 Teams, territories & account sharing](../SF_core/07-security-and-sharing/10-teams-territories-and-account-sharing.md) |
| The role hierarchy forecasts are generated from and territories run beside | [07-security · 07 Role hierarchy & ownership](../SF_core/07-security-and-sharing/07-role-hierarchy-and-ownership.md) |
| Permission set licences — Pipeline Inspection, Einstein Activity Capture | [07-security · 02 Licences & what they gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) |
| Apex that keeps team membership in step with a field | [02-apex · 11 Sharing keywords & Apex managed sharing](../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) |
| The Lead → Opportunity → PricebookEntry object graph | [08-data · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) |
| A lead with no Company converting to a person account | [08-data · 05 Person Accounts & one-way modeling decisions](../SF_core/08-data-modeling-and-large-data-volumes/05-person-accounts-and-one-way-modeling-decisions.md) |
| Multi-currency, and the dated rates forecasts ignore | [08-data · 22 Multi-currency, multi-language & locale](../SF_core/08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md) |

## Seams into other vaults

| Topic | Note |
|---|---|
| Building a Sales agent that nurtures leads or coaches a rep | [SF_Agentforce/](../SF_Agentforce/INDEX.md) |
| The Sales Email prompt template and its recipient | [SF_Agentforce · Prompt template types](../SF_Agentforce/prompt-template-types.md) |
| Partner users working leads and opportunities on a partner site | [SF_Experience_Cloud · 08 Licences & external user types](../SF_Experience_Cloud/08-licences-and-external-user-types.md) |
| Omni-Channel pushing a lead to a rep | [SF_Service · Omni-Channel Flows](../SF_Service/omni-channel-flows.md) |

## Backlog — referenced elsewhere, not yet fed

Sales Cloud topics the repo already mentions but no note owns yet. Feed notes on any of them and they land here.

| Topic | Mentioned in | Status |
|---|---|---|
| Sales Engagement & cadences (formerly High Velocity Sales) | [Einstein Activity Capture](einstein-activity-capture.md) (licences) | — |
| Einstein Lead & Opportunity Scoring | [Pipeline Inspection](pipeline-inspection.md) (deal insights) | — |
| Einstein Conversation Insights | [Einstein Activity Capture](einstein-activity-capture.md), [Pipeline Inspection](pipeline-inspection.md) | — |
| Revenue Cloud Advanced & Salesforce CPQ | [Quotes, Orders & Contracts](quotes-orders-and-contracts.md), `SF_core/CURRENCY.md` | CPQ is end of sale, not end of life |
| Agentforce for Sales & the Sales agents (SDR, Sales Coach) | `RELEASE-RADAR/agentforce-platform.md` (Coworker → Sales Coach Agent), `RELEASE-RADAR/pricing-and-certification.md` | build side belongs in `SF_Agentforce/` |
| Contacts to Multiple Accounts (`AccountContactRelation`) | `SF_core/08-data · 04` | — |
| Partner relationship management & deal registration | `SF_Experience_Cloud · 01`, `· 08` | — |
| Outlook & Gmail integration, Lightning Sync | [Einstein Activity Capture](einstein-activity-capture.md), `SF_core/CURRENCY.md` | Lightning Sync retires 1 April 2027 |
| Sales Planning | `SF_core/07-security · 02` (a PSL example) | — |
| Salesforce Maps | — | — |
| Sales Console, Sales Programs & Big Deal Alerts | — | — |

## Unfiled

[_inbox.md](_inbox.md) — anything captured that does not have a home yet.
