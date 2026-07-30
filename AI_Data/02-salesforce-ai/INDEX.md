# 02 · Salesforce AI

Agents on the platform — where Apex/Flow experience becomes a superpower. Roadmap tag: **Salesforce AI** (amber).
Cert target: **[Agentforce Specialist](_cert-agentforce-specialist/exam-guide.md)** (end of Phase 03).

> ⚠️ **The authoring model changed in 2026.** Since the week of **July 13, 2026**, the *New Agent* button no longer opens the legacy topic-and-instruction builder — agents are authored in **[Agent Script](07-agent-script/notes.md)**. Existing legacy agents can still be edited and managed, but most tutorials you'll find online teach a model you can no longer create new agents in. Start with [Agentforce Anatomy](02-agentforce-anatomy/notes.md) for the comparison.

| Topic | What it covers | Quick recall |
|---|---|---|
| [Salesforce AI Landscape](01-landscape/notes.md) | Einstein → Einstein GPT → Copilot → **Agentforce 360**; the failure-triage table; model choice incl. Gemini | [cheatsheet](01-landscape/cheatsheet.md) · [flashcards](01-landscape/flashcards.md) |
| [Agentforce Anatomy](02-agentforce-anatomy/notes.md) | Agents, actions, grounding, guardrails; **legacy vs Agent Script**; Atlas Reasoning Engine 3.0 | [cheatsheet](02-agentforce-anatomy/cheatsheet.md) · [flashcards](02-agentforce-anatomy/flashcards.md) |
| [Prompt Builder](03-prompt-builder/notes.md) | Prompt templates, merge fields, dynamic grounding — and templates exposed as **MCP prompts** | [cheatsheet](03-prompt-builder/cheatsheet.md) · [flashcards](03-prompt-builder/flashcards.md) |
| [Einstein Trust Layer](04-einstein-trust-layer/notes.md) | Masking, secure retrieval, zero retention, injection defence, audit — and why it matters *more* in 2026 | [cheatsheet](04-einstein-trust-layer/cheatsheet.md) · [flashcards](04-einstein-trust-layer/flashcards.md) |
| [Custom Agent Actions](05-custom-agent-actions/notes.md) | Apex/Flow/Apex REST/`@AuraEnabled` as actions; **the API 67.0 breaking changes**; descriptions as specification | [cheatsheet](05-custom-agent-actions/cheatsheet.md) · [flashcards](05-custom-agent-actions/flashcards.md) |
| [Model Builder & BYOM](06-model-builder-byom/notes.md) | Registering external models incl. Claude via Bedrock; **per-agent model pinning** as a cost lever | [cheatsheet](06-model-builder-byom/cheatsheet.md) · [flashcards](06-model-builder-byom/flashcards.md) |
| [Agent Script](07-agent-script/notes.md) 🆕 | The current authoring language: compile-to-JSON, open-source toolchain, CI linting without an org | [cheatsheet](07-agent-script/cheatsheet.md) · [flashcards](07-agent-script/flashcards.md) |
| [Multi-Agent Orchestration](08-multi-agent-orchestration/notes.md) 🆕 | Orchestrator + subagents, **descriptions as routing contracts**, Agent Router, A2A | [cheatsheet](08-multi-agent-orchestration/cheatsheet.md) · [flashcards](08-multi-agent-orchestration/flashcards.md) |
| [Observability & Testing](09-observability-and-testing/notes.md) 🆕 | Agent Analytics, Custom Scorers as metadata, `agent preview`, trace files, `@IntegrationTest` | [cheatsheet](09-observability-and-testing/cheatsheet.md) · [flashcards](09-observability-and-testing/flashcards.md) |
| [Agentforce Coworker](10-agentforce-coworker/notes.md) 🆕 | **Beta.** The agent you don't author — search-bar surface, federation vs ingestion, inherited governance | [cheatsheet](10-agentforce-coworker/cheatsheet.md) · [flashcards](10-agentforce-coworker/flashcards.md) |
| [Agent Fabric & interop](11-agent-fabric-and-interop/notes.md) 🆕 | The control plane for agents you **didn't** build — registry, broker, Omni Gateway; MCP/A2A as governed traffic | [cheatsheet](11-agent-fabric-and-interop/cheatsheet.md) · [flashcards](11-agent-fabric-and-interop/flashcards.md) |
| [Voice & Contact Center](12-voice-and-contact-center/notes.md) 🆕 | Autonomous calls over PSTN/SIP, CCaaS partners, escalation prerequisites, **30 credits vs 20**, region limits | [cheatsheet](12-voice-and-contact-center/cheatsheet.md) · [flashcards](12-voice-and-contact-center/flashcards.md) |
| [ADLC & Agentforce DX](13-adlc-and-agentforce-dx/notes.md) 🆕 | Five phases, inner/outer loop, Agent Skills, the `sf agent` command chain — **the seam with the Claude track** | [cheatsheet](13-adlc-and-agentforce-dx/cheatsheet.md) · [flashcards](13-adlc-and-agentforce-dx/flashcards.md) |
| [Prebuilt agents & buy vs build](14-prebuilt-agents-and-buy-vs-build/notes.md) 🆕 | Help Agent, Commerce, IT Service, industry packs; three commercial models; **the decision framework** | [cheatsheet](14-prebuilt-agents-and-buy-vs-build/cheatsheet.md) · [flashcards](14-prebuilt-agents-and-buy-vs-build/flashcards.md) |

Grounding lives in the Data 360 track — see [RAG on Platform](../01-data-cloud/08-rag-on-platform/notes.md).

> **Topics 11–14 were added 2026-07-28** as structural gap-fill, not from a news cycle. Agent Fabric had **zero mentions** anywhere in this study base despite launching in September 2025; Voice and Contact Center had one passing line despite Contact Center being GA since February 2026. Nothing in them is breaking news — that's precisely why a daily radar scan kept missing them.

## Cert prep
- [Exam guide breakdown](_cert-agentforce-specialist/exam-guide.md) — **restructured**, and the domain weights are 🚩 **unverified**: sources disagree on whether Multi-Agent Interoperability is 5% or 15%, and on a Development Lifecycle & Observability domain worth 15–20%. Settle this from the official PDF before planning study time.
- [Practice questions](_cert-agentforce-specialist/practice-questions.md)
- [Weak areas](_cert-agentforce-specialist/weak-areas.md)

## Staying current
[05-release-radar/agentforce-platform.md](../05-release-radar/agentforce-platform.md) carries the running story with sources and status flags.
