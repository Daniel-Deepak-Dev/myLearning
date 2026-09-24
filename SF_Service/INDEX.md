# SF_Service

> **Start at [../HOME.md](../HOME.md)** — what to study next, rebuilt from the notes.

Service Cloud only. Enhanced Chat and messaging channels, Omni-Channel routing, Omni Supervisor, the handoff from a bot or agent to a human, and Knowledge.

The platform pieces underneath — queues, assignment rules, licences, Flow, LWC — live in [SF_core/](../SF_core/README.md) and are linked from each note. The agent a channel routes to is built in [SF_Agentforce/](../SF_Agentforce/INDEX.md); the chat widget's site-side exposure is [SF_Experience_Cloud · 19](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md).

> Currency: **Summer '26 (API 67.0)** · what changed: [SF_core/CURRENCY.md](../SF_core/CURRENCY.md) · Agentforce side: [RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md)

## Learning path

Read top to bottom. `#` is display order only — filenames carry no number, so reordering costs one row edit. Chat and Omni-Channel alternate on purpose: a chat channel cannot route until Omni-Channel exists.

**13 topics** · 34 gaps open · 0 complete · newest 2026-09-24 · oldest 2026-09-24

**12 org checks** sit under `## Confirm in org` across 10 notes. Those are sandbox to-dos, not research — they do not count as gaps and do not stop a note being complete.

**51 hands-on labs · ~18 h.** This file is the reading order. When the goal is to *do* something, open [PRACTICE.md](PRACTICE.md) instead — it queues every lab unblocked-first, so nothing needs Agentforce until lab #44.

| # | Topic | One line | Level | Status | Org ✓ | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|---|
| 1 | [Enhanced Chat](enhanced-chat.md) | The web and in-app messaging channel MIAW became — and what replaced legacy Chat | basic | 🌱 2 open | 1 | — | 2026-09-24 | 2026-09-24 |
| 2 | [Omni-Channel Fundamentals](omni-channel-fundamentals.md) | Service channels, presence and capacity — and why there is only Enhanced Omni now | basic | 🌱 2 open | — | — | 2026-09-24 | 2026-09-24 |
| 3 | [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) | Channel → deployment → snippet, and the pre-chat form that needs a flow | working | 🌱 1 open | 1 | 1 | 2026-09-24 | 2026-09-24 |
| 4 | [Embedded Service Deployments](embedded-service-deployments.md) | When a channel needs one — and the channels that never do | working | 🌱 3 open | 1 | 3 | 2026-09-24 | 2026-09-24 |
| 5 | [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) | Queue, skills, direct and external routing, and how capacity is counted | working | 🌱 3 open | — | 2 | 2026-09-24 | 2026-09-24 |
| 6 | [Omni-Channel Flows](omni-channel-flows.md) | Route Work in Flow Builder — the one routing setup for every channel | working | 🌱 3 open | 1 | 5 | 2026-09-24 | 2026-09-24 |
| 7 | [Enhanced Conversation Component](enhanced-conversation-component.md) | The rep's chat window on the Messaging Session page | basic | 🌱 3 open | 2 | 3 | 2026-09-24 | 2026-09-24 |
| 8 | [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) | The Agentforce-first client, and why the two never share a domain | working | 🌱 4 open | 1 | 4 | 2026-09-24 | 2026-09-24 |
| 9 | [Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) | Who the customer is, how long a conversation lives, and where verification works | deep | 🌱 3 open | 2 | 3 | 2026-09-24 | 2026-09-24 |
| 10 | [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) | Getting a conversation from an agent to a rep without losing it | working | 🌱 3 open | 1 | 6 | 2026-09-24 | 2026-09-24 |
| 11 | [Omni Supervisor](omni-supervisor.md) | Now *Command Center for Service* — watching the queues and moving work while it is live | basic | 🌱 2 open | 1 | 5 | 2026-09-24 | 2026-09-24 |
| 12 | [Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md) | Your own chat UI over the Enhanced Chat API, and the "In-App" in MIAW | deep | 🌱 3 open | — | 9 | 2026-09-24 | 2026-09-24 |
| 13 | [Knowledge](knowledge.md) | Articles, data categories, and the channels that decide who outside the org can read them | basic | 🌱 2 open | 1 | — | 2026-09-24 | 2026-09-24 |

## Seams into SF_core

These `SF_core` notes own the platform side. Link to them rather than restating.

| Topic | SF_core note |
|---|---|
| Queues, assignment rules, escalation rules | [01-admin · 11 Queues, assignment & escalation rules](../SF_core/01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) |
| Where escalation and entitlement run in a save | [01-admin · 14 Order of execution — declarative view](../SF_core/01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md) |
| Queues as sharing grantees | [07-security · 08 Groups, queues & the grantee model](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) |
| Service Cloud User and other feature licences | [07-security · 02 Licences & what they gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) |
| Rendering structured output in Enhanced Chat v2 | [03-lwc · 19 Custom Lightning Types for agent output](../SF_core/03-lwc-and-slds/19-custom-lightning-types-for-agent-output.md) |
| Case and its related objects | [08-data · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) |

## Seams into other vaults

| Topic | Note |
|---|---|
| The Enhanced Chat widget on a site, and the guest user behind it | [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) |
| Building the Service Agent a channel routes to | [SF_Agentforce/](../SF_Agentforce/INDEX.md) |

## Backlog — referenced elsewhere, not yet fed

Service Cloud topics the repo already mentions but no note owns yet. Feed notes on any of them and they land here.

| Topic | Mentioned in | Status |
|---|---|---|
| Service Cloud Voice & Contact Center | `GLOSSARY.md` (Agentforce Voice, Contact Center), `RELEASE-RADAR/agentforce-platform.md` | — |
| Case management, Email-to-Case, Web-to-Case | `SF_core/08-data · 04`, `Interview/01-agentforce · 03` | — |
| Entitlements & milestones | `SF_core/01-admin · 14` | — |
| Help Agent & prebuilt service agents | `RELEASE-RADAR/agentforce-platform.md`, `GLOSSARY.md` | — |
| Other messaging channels — WhatsApp, SMS, Apple, Bring Your Own Channel | `RELEASE-RADAR/agentforce-platform.md` (Voice for Digital Channels) | — |
| Service Console, macros, quick text | `SF_core/01-admin · 18` | the conversation window is covered by [Enhanced Conversation Component](enhanced-conversation-component.md); macros and quick text still open |
| Service Cloud ITSM & CMDB | `GLOSSARY.md` (CMDB, UEL), `RELEASE-RADAR/developer-tooling-and-apis.md` | — |
| Field Service | — | — |

## Unfiled

[_inbox.md](_inbox.md) — anything captured that does not have a home yet.
