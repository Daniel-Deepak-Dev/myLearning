# SF_Agentforce

Agentforce only. Prompt templates, agents, actions, Agent Script, Atlas Reasoning, Einstein Trust Layer.

The code underneath lives in [SF_core/](../SF_core/README.md) and is linked from each note.

> Currency: **Summer '26 (API 67.0)** · what changed: [RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md)

## Learning path

Read top to bottom. `#` is display order only — filenames carry no number, so reordering costs one row edit.

**9 topics** · 30 gaps open · 1 complete · newest 2026-08-28 · oldest 2026-08-27

| # | Topic | One line | Level | Status | Pre | Created | Updated |
|---|---|---|---|---|---|---|---|
| 1 | [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) | The tool, and the reusable prompt it produces | basic | ✅ complete | — | 2026-08-27 | 2026-08-28 |
| 2 | [Prompt Template Types](prompt-template-types.md) | The six types and what each grounds on | basic | 🌱 3 open | 1 | 2026-08-27 | 2026-08-28 |
| 3 | [Prompt Template Versions & Access](prompt-template-versions-and-access.md) | Who can build one, who can run one, and editing a live version | basic | 🌱 3 open | 1 | 2026-08-28 | 2026-08-28 |
| 4 | [Prompt Template Metadata & Deployment](prompt-template-metadata-and-deployment.md) | The XML, and what breaks moving it between orgs | working | 🌱 4 open | 3 | 2026-08-28 | 2026-08-28 |
| 5 | [Grounding a Prompt Template](grounding-a-prompt-template.md) | The six ways data reaches the prompt | working | 🌱 4 open | 2 | 2026-08-28 | 2026-08-28 |
| 6 | [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) | How a template becomes something an agent calls | working | 🌱 4 open | 2 | 2026-08-28 | 2026-08-28 |
| 7 | [Template-Triggered Prompt Flows](template-triggered-prompt-flows.md) | Feeding a template when merge fields cannot reach the data | working | 🌱 4 open | 5 | 2026-08-27 | 2026-08-27 |
| 8 | [Einstein Trust Layer](einstein-trust-layer.md) | The guardrails every call passes through | basic | 🌱 4 open | 1 | 2026-08-27 | 2026-08-27 |
| 9 | [Atlas Reasoning Engine](atlas-reasoning-engine.md) | The part that decides what to do | basic | 🌱 4 open | 1 | 2026-08-27 | 2026-08-27 |

## Seams into SF_core

These `SF_core` notes own the code side. Link to them rather than restating.

| Topic | SF_core note |
|---|---|
| Apex as an agent action | [02-apex · 22 Invocable Apex & Agentforce actions](../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) |
| Apex data inside a prompt template | [02-apex · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) |
| Calling a prompt template from code | [02-apex · 32 Invoking prompt templates from Apex](../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) |
| Raw model calls | [02-apex · 33 Models API in Apex](../SF_core/02-apex-and-triggers/33-models-api-in-apex.md) |
| Testing AI code | [02-apex · 34 Testing AI Apex & mocking LLMs](../SF_core/02-apex-and-triggers/34-testing-ai-apex-and-mocking-llms.md) |
| Flow as an agent action | [04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) |
| Agent-facing APIs | [06-integration · 25 MCP servers & agent-facing APIs](../SF_core/06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) |
| Agents in a site | [05-experience · 19 Embedded messaging & agents in sites](../SF_core/05-experience-cloud-lwr/19-embedded-messaging-and-agents-in-sites.md) |
| Moving AI metadata between orgs | [09-devops · 05 Metadata API & deployment mechanics](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) |

## Backlog — referenced elsewhere, not yet fed

Other notes in the repo link here for these topics. The count is how many places expect them, so it doubles as a priority order.

| Topic | Wanted by | Status |
|---|---|---|
| Custom agent actions | 18 | prompt-template route covered by [Agent Actions](prompt-templates-as-agent-actions.md); Apex and Flow routes still open |
| ADLC & Agentforce DX | 12 | — |
| Agent Fabric & interop | 9 | — |
| Observability & testing | 7 | — |
| Model Builder & BYOM | 7 | — |
| Agent Script | 6 | — |
| Prebuilt agents, buy vs build | 3 | — |
| Multi-agent orchestration | 3 | — |
| Agentforce landscape | 1 | — |

## Unfiled

[_inbox.md](_inbox.md) — anything captured that does not have a home yet.
