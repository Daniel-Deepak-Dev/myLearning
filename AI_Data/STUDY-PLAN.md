# Study Plan — Phase → Folder Map

The roadmap runs in 5 phases over 26 weeks; this folder is organized by track. This file is the bridge: what to open, in what order. Check items off in [the roadmap HTML](ai-salesforce-architect-roadmap.html) as you go.

> **Currency: Summer '26 (API 67.0).** Content was brought current on 2026-07-28. Two structural changes since the roadmap was written: **Data Cloud is now Data 360**, and agents are authored in **Agent Script**, not topics — which added four topic folders (marked 🆕 below). Running updates: [05-release-radar/](05-release-radar/README.md).

## Phase 01 · Weeks 1–4 — Foundations & Landscape
*Build the mental map before the deep dives.*

| Roadmap item | Study folder |
|---|---|
| SQL fluency refresh | [00-core-skills/01-sql](00-core-skills/01-sql/notes.md) |
| Python for data work | [00-core-skills/02-python-for-data](00-core-skills/02-python-for-data/notes.md) |
| Data 360 orientation | [01-data-cloud/01-orientation](01-data-cloud/01-orientation/notes.md) |
| Ingestion basics | [01-data-cloud/02-ingestion](01-data-cloud/02-ingestion/notes.md) |
| Salesforce AI landscape | [02-salesforce-ai/01-landscape](02-salesforce-ai/01-landscape/notes.md) |
| Claude API first calls | [03-claude-cca/01-claude-api](03-claude-cca/01-claude-api/notes.md) |
| AI theory essentials | [00-core-skills/03-ai-theory](00-core-skills/03-ai-theory/notes.md) |

**Milestone:** Trailhead badges Data Cloud Basics + Agentforce Basics · first Claude API script in a personal repo.

## Phase 02 · Weeks 5–8 — Data 360 Depth
*Own the data layer — it's what makes the AI work trustworthy later.*

| Roadmap item | Study folder |
|---|---|
| Data modeling DSO → DLO → DMO | [01-data-cloud/03-data-modeling-dso-dlo-dmo](01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) |
| Harmonization & identity resolution | [01-data-cloud/04-identity-resolution](01-data-cloud/04-identity-resolution/notes.md) |
| Calculated insights & segmentation | [01-data-cloud/05-insights-segmentation](01-data-cloud/05-insights-segmentation/notes.md) |
| Zero copy & BYOL federation | [01-data-cloud/06-zero-copy-byol](01-data-cloud/06-zero-copy-byol/notes.md) |
| Vector database & unstructured data | [01-data-cloud/07-vector-db-unstructured](01-data-cloud/07-vector-db-unstructured/notes.md) |
| Data 360 DevOps 🆕 | [01-data-cloud/09-data-360-devops](01-data-cloud/09-data-360-devops/notes.md) |
| Pipeline patterns | [00-core-skills/04-data-engineering](00-core-skills/04-data-engineering/notes.md) |

**Milestone:** 🏅 **Data 360 Consultant** _(renamed from Data Cloud Consultant, 2026-03-27; exam code `Data-Con-101` unchanged)_ → prep in [_cert-data-cloud-consultant](01-data-cloud/_cert-data-cloud-consultant/exam-guide.md)

## Phase 03 · Weeks 9–14 — Salesforce AI Depth
*Build agents on the platform. Apex + Flow = home turf.*

| Roadmap item | Study folder |
|---|---|
| Agentforce anatomy | [02-salesforce-ai/02-agentforce-anatomy](02-salesforce-ai/02-agentforce-anatomy/notes.md) |
| **Agent Script** 🆕 — the current authoring model | [02-salesforce-ai/07-agent-script](02-salesforce-ai/07-agent-script/notes.md) |
| Prompt Builder | [02-salesforce-ai/03-prompt-builder](02-salesforce-ai/03-prompt-builder/notes.md) |
| Einstein Trust Layer | [02-salesforce-ai/04-einstein-trust-layer](02-salesforce-ai/04-einstein-trust-layer/notes.md) |
| Custom agent actions | [02-salesforce-ai/05-custom-agent-actions](02-salesforce-ai/05-custom-agent-actions/notes.md) |
| Model Builder & BYOM | [02-salesforce-ai/06-model-builder-byom](02-salesforce-ai/06-model-builder-byom/notes.md) |
| Multi-agent orchestration 🆕 | [02-salesforce-ai/08-multi-agent-orchestration](02-salesforce-ai/08-multi-agent-orchestration/notes.md) |
| Observability & testing 🆕 | [02-salesforce-ai/09-observability-and-testing](02-salesforce-ai/09-observability-and-testing/notes.md) |
| RAG on platform | [01-data-cloud/08-rag-on-platform](01-data-cloud/08-rag-on-platform/notes.md) |

**Study Agent Script immediately after Agentforce anatomy** — the anatomy notes explain *why* it replaced topics; this is where you learn it. Most online tutorials still teach the retired model.

**Milestone:** 🏅 **Agentforce Specialist** + one working agent with a custom Apex action → prep in [_cert-agentforce-specialist](02-salesforce-ai/_cert-agentforce-specialist/exam-guide.md)

## Phase 04 · Weeks 15–20 — Claude Stack & CCA-F
*Anthropic Academy courses (~15–20 hrs) + hands-on builds. Percentages = exam weight.*

| Roadmap item | Study folder |
|---|---|
| Claude API depth | [03-claude-cca/01-claude-api](03-claude-cca/01-claude-api/notes.md) |
| Agentic architecture & orchestration (27%) | [03-claude-cca/02-agentic-architecture](03-claude-cca/02-agentic-architecture/notes.md) |
| Claude Code configuration & workflows (20%) | [03-claude-cca/03-claude-code](03-claude-cca/03-claude-code/notes.md) |
| Prompt engineering & structured output (20%) | [03-claude-cca/04-prompt-engineering](03-claude-cca/04-prompt-engineering/notes.md) |
| Tool design & MCP integration (18%) | [03-claude-cca/05-mcp](03-claude-cca/05-mcp/notes.md) |
| Context management & reliability (15%) | [03-claude-cca/06-context-management](03-claude-cca/06-context-management/notes.md) |

**Milestone:** 🏅 **CCA-F** (60 questions · 120 min · 720/1000) → prep in [_cert-cca-f](03-claude-cca/_cert-cca-f/exam-guide.md)

## Phase 05 · Weeks 21–26 — Capstone
*Convert learning into architect-track proof.*

| Roadmap item | Project folder |
|---|---|
| MCP server for Salesforce | [04-capstone/01-mcp-server-salesforce](04-capstone/01-mcp-server-salesforce/notes.md) |
| RAG assistant over CRM data | [04-capstone/02-rag-assistant-crm](04-capstone/02-rag-assistant-crm/notes.md) |
| End-to-end Agentforce use case | [04-capstone/03-agentforce-use-case](04-capstone/03-agentforce-use-case/notes.md) |
| Write-up & internal pitch | [04-capstone/04-writeup](04-capstone/04-writeup/notes.md) |

**Milestone:** one demoable AI + Data project shipped + the dual credential (Salesforce certs + CCA-F). The rare pairing.

## Weekly rhythm

1. Study the phase's topics → extend `notes.md` with what you learned hands-on.
2. Distill anything new into its `cheatsheet.md` (half a page — that's the constraint that makes it useful).
3. Friday: run the track's `flashcards.md` files + write the week's entry in [journal/](journal/).
4. Anything off-roadmap you stumbled on → [99-inbox/INBOX.md](99-inbox/INBOX.md).
5. Skim the newest [05-release-radar/](05-release-radar/README.md) note for your track — Data 360 ships monthly, and Agentforce moves fast enough that a topic can drift between now and your exam date.
