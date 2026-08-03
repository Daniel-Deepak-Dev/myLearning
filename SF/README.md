# SF — Core Salesforce Platform

The platform knowledge base: Apex, LWC, Flow, Admin, Experience Cloud, Integration, Security, Data, DevOps.

Sibling to [AI_Data/](../AI_Data/README.md), which covers the AI-Architect path (Agentforce, Data 360, Claude). This folder is the **platform underneath** that path — the two cross-link rather than duplicate.

> **Currency: Summer '26 · API 67.0** · see [CURRENCY.md](CURRENCY.md) for the version map and the six defaults that invalidate older tutorials.

## Map

| Area | Covers | Topics |
|---|---|---|
| [01-admin-and-declarative-platform/](01-admin-and-declarative-platform/INDEX.md) | Org anatomy, data model config, Dynamic Forms, CMDT, order of execution | 19 |
| [02-apex-and-triggers/](02-apex-and-triggers/INDEX.md) | Apex language, SOQL/SOSL, triggers, async, user-mode security, testing | 24 |
| [03-lwc-and-slds/](03-lwc-and-slds/INDEX.md) | LWC component model, LDS, GraphQL wire, LWS, SLDS 2, Jest, State Managers | 24 |
| [04-flow-and-automation/](04-flow-and-automation/INDEX.md) | Flow Builder end-to-end, HTTP callout, Orchestrator, run context, testing, agent actions | 25 |
| [05-experience-cloud-lwr/](05-experience-cloud-lwr/INDEX.md) | LWR sites, guest security, CMS, headless, SEO | 18 |
| [06-integration-and-apis/](06-integration-and-apis/INDEX.md) | REST/Bulk/GraphQL/Pub-Sub, OAuth, External Client Apps, MCP | 23 |
| [07-security-and-sharing/](07-security-and-sharing/INDEX.md) | Permission-set-led access, sharing, restriction rules, Shield | 21 |
| [08-data-modeling-and-large-data-volumes/](08-data-modeling-and-large-data-volumes/INDEX.md) | Relationships, selectivity, skew, big objects, archiving, Hyperforce | 20 |
| [09-devops-sfdx-and-release-management/](09-devops-sfdx-and-release-management/INDEX.md) | `sf` CLI v2, 2GP, DevOps Center, CI/CD, Code Analyzer v5 | 22 |
| [PHASES.md](PHASES.md) | The 19-run build plan — what each AI run produces | — |
| [_notion-seed/INVENTORY.md](_notion-seed/INVENTORY.md) | The old Notion notes, mapped to target topics | — |

**196 topics.** Rows in each `INDEX.md` are plain text until written, links once they exist.

## Out of scope — deliberately

- **Aura components** and **Visualforce.** Both are legacy; LWC is the only UI framework here. They appear only where a note must explain a migration or a coexistence rule.
- **OmniStudio**, **Reporting & Analytics**, **Sales/Service Cloud functional depth.** Not excluded on merit — just not in this build. Add as areas 10–12 later if wanted.
- **Agentforce / Data 360 / Claude.** Those live in [AI_Data/](../AI_Data/README.md). Notes here link across instead of repeating.

## The note format

One flat `.md` per topic, **hard cap ~80 lines**. Skeleton in [_template.md](_template.md):

`## Core idea` → `## How it works` → `## 2026 currency` → `## Gotchas` → `## Recall` → `## Related`

The recall layer is folded in as `## Recall` — 5 `Q:`/`A:` pairs in the same Anki-scriptable format as `AI_Data` flashcards, so tooling works across both vaults.

**Why this diverges from `AI_Data/`:** that vault uses folder-per-topic with four files. At 190 topics that is ~760 files and contradicts the whole point — short notes you can reload a topic from in five minutes.

## Flag legend

| Flag | Meaning |
|---|---|
| 🆕 | GA'd 2024–2026. **Research against release notes before writing — never draft from recall.** |
| ⚠️ | The 2019–2021 answer is now **wrong**. The note opens with a one-line *What changed* correction. |
| *(GA Winter '22)* | Post-dates most tutorials, pre-dates the 🆕 window. |

## Conventions

- **Naming:** `NN-kebab-case.md`, numbered in learning order within an area.
- **Links:** relative markdown. Browse in VS Code (`Ctrl+Shift+V`).
- **New topic:** next number in the area + a row in that area's `INDEX.md` + the phase it belongs to.
- **Currency detail** is never duplicated — link to [AI_Data/05-release-radar/](../AI_Data/05-release-radar/README.md), which is the source of truth for what changed and when.
- **New platform jargon** goes in [AI_Data/GLOSSARY.md](../AI_Data/GLOSSARY.md). One glossary for both vaults.
- **One commit per phase:** `SF: phase NN — <title>`.
