# Salesforce AI Landscape

> Track: Salesforce AI · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/](../../05-release-radar/README.md)

**Roadmap scope:** The arc from Einstein → Einstein GPT → Agentforce. Where Prompt Builder, Model Builder, and the Einstein Trust Layer each fit.

## What is it?

"Salesforce AI" is not one product — it's four generations of product stacked on top of each other, and most confusion in this space comes from mixing vocabulary across generations.

| Era | Name | What it did | Status |
|---|---|---|---|
| 2016–2022 | **Einstein** | Predictive ML on CRM data: lead scoring, opportunity insights, forecasting. Statistical, not generative. | Still shipping, still sold |
| 2023 | **Einstein GPT** | First generative layer — draft an email, summarize a case. Human presses the button, model writes text. | Name retired |
| 2024 | **Einstein Copilot** | Conversational assistant inside CRM. Could call actions, but reactive: it waited to be asked. | **Folded into Agentforce — historical name** |
| 2025–26 | **Agentforce / Agentforce 360** | Autonomous agents that plan multi-step work and act without a human in the loop. | Current |

The 2026 platform umbrella is **Agentforce 360**, and it covers more than agents: Data 360 (the grounding layer), Tableau (analytics), Slack (the surface), and the agent runtime itself.

**The one-line arc:** *predict* → *draft* → *assist* → *act*. Each generation moved work further from the human. That's why the security model changed in Summer '26 — see [Trust Layer](../04-einstein-trust-layer/notes.md).

## Why it matters (for the AI-Salesforce architect role)

Three reasons this map is worth memorizing before any deep dive:

1. **Client conversations start here.** A client saying "we already have Einstein" may mean predictive lead scoring from 2019. Knowing which generation they're on determines whether the project is an upgrade or a greenfield build.
2. **Exam questions use current vocabulary; the internet uses old vocabulary.** Most blog content still says "Einstein Copilot" and "topics and instructions". Both are historical. Search results will actively mislead you.
3. **The layers compose.** Agentforce without Data 360 grounding is a chatbot with good manners. The architect's value is knowing which layer solves which failure — see the diagnostic table below.

### The layer map

```
        ┌──────────────────────────────────────────┐
        │  Surfaces: Lightning · Slack · Mobile ·   │
        │  Voice · Web · MCP clients (Claude, etc.) │
        └────────────────────┬─────────────────────┘
                             │
        ┌────────────────────▼─────────────────────┐
        │  AGENTFORCE                              │
        │  Agent Script → Atlas Reasoning 3.0      │
        │  actions · orchestration · subagents     │
        └────────────────────┬─────────────────────┘
                             │
        ┌────────────────────▼─────────────────────┐
        │  EINSTEIN TRUST LAYER                    │
        │  masking · injection defence · audit ·   │
        │  zero retention                          │
        └────────────────────┬─────────────────────┘
                             │
        ┌──────────┬─────────▼─────────┬───────────┐
        │ PROMPT   │  MODEL BUILDER    │ DATA 360  │
        │ BUILDER  │  (incl. BYOM)     │ grounding │
        └──────────┴───────────────────┴───────────┘
```

Read it top-down for a request, bottom-up for a failure.

### Which tool solves which problem

| Symptom | Layer at fault | Where to go |
|---|---|---|
| Agent invents facts about a customer | Grounding | [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) |
| Agent answers from stale data | Ingestion | [Ingestion](../../01-data-cloud/02-ingestion/notes.md) — Accelerated Data Ingest |
| Agent's tone/format is wrong | Prompt | [Prompt Builder](../03-prompt-builder/notes.md) |
| Agent picks the wrong action | Reasoning / routing | [Agentforce anatomy](../02-agentforce-anatomy/notes.md), [Agent Script](../07-agent-script/notes.md) |
| Agent routes to the wrong subagent | Subagent **description** | [Multi-agent orchestration](../08-multi-agent-orchestration/notes.md) |
| Agent exposes data it shouldn't | Access mode / sharing | [Custom actions](../05-custom-agent-actions/notes.md) — user mode at 67.0 |
| Cost is higher than forecast | Architecture | Flex Credits — you pay per *action*, not per conversation |

That table is the single most useful thing on this page. Most "the AI is bad" reports resolve to row 1, 2 or 5 — not to the model.

## How it works

**Model choice is now yours.** The Atlas Reasoning Engine supports Anthropic (Claude on Amazon Bedrock), OpenAI, and **Google Gemini**. You can also register your own via Model Builder / BYOM, and since Agent Script you can **pin a model per agent** rather than accepting one org-wide setting. Model selection is a cost-and-latency architecture decision you own — see [Model Builder & BYOM](../06-model-builder-byom/notes.md).

**Everything is reachable headlessly.** *Headless 360* is the organizing idea of Summer '26: every major capability is an API, an MCP tool, or a CLI command. Agents are not a UI feature bolted onto CRM; they're a first-class caller of the platform, on equal footing with a browser.

**Prepackaged agents now exist.** Salesforce ships finished agents, not just tooling — the **Agentforce Help Agent** (GA July 2026) deploys in minutes across voice, web, portal and messaging. That moves the differentiation from *can you build an agent* to *how well is yours grounded*.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Trailhead: **Agentforce Basics** (Phase 1 milestone badge)
- [ ] In a Dev org, open Setup → Einstein and list which generation each enabled feature belongs to. Most orgs have a mix — that's the point.
- [ ] Open Agentforce Builder and create one throwaway agent. You'll land in Agent Script whether you expected to or not — confirm that for yourself early.

## Gotchas & sharp edges

- **"Einstein Copilot" is a dead name.** If a source uses it as current, that source predates mid-2025 — discount its other claims too.
- **"Agentforce" is overloaded.** It means the agent platform, *and* it's now a branding prefix on 16 renamed certifications (Sales Cloud Consultant → **Agentforce Sales Consultant**, from 2026-07-24). The cert rename is cosmetic — no content or exam-code change.
- **Einstein ≠ generative.** Classic Einstein predictive features are still sold and still on exams. Don't assume every "Einstein" feature involves an LLM.
- **Agentforce 360 ≠ Agentforce.** The 360 suffix is the platform umbrella (agents + Data 360 + Tableau + Slack), not a version number of the agent product.
- **Don't learn the topic/instruction model as current.** It's legacy as of July 13, 2026. Most tutorials online still teach it — see [Agentforce anatomy](../02-agentforce-anatomy/notes.md) for what replaced it and why the distinction matters on the exam.

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — the layer below this one
- [Agent Script](../07-agent-script/notes.md) — how agents are actually authored in 2026
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — the control point under everything
- [Data 360 Orientation](../../01-data-cloud/01-orientation/notes.md) — the grounding half of the platform
- [Release radar: Agentforce platform](../../05-release-radar/agentforce-platform.md) — running story with sources
