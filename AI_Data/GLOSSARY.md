# Glossary — 109 Terms

Extracted from [the roadmap](ai-salesforce-architect-roadmap.html) glossary tab, grouped by track and alphabetized. Greppable and extendable — **add new terms here as you meet them**, in the right section, keeping alphabetical order. If a term deserves depth, it also earns a flashcard in its topic folder.

> **Currency:** definitions reflect **Summer '26 (API 67.0)**, the current release as of 2026-07-28. Where a term changed meaning in 2026, the entry says so — knowing the old meaning is what stops you answering an exam question from 2025 memory. Running detail and sources live in [05-release-radar/](05-release-radar/README.md).

## Salesforce AI

| Term | Definition |
|---|---|
| A2A (Agent-to-Agent Protocol) | Open protocol for agents built on different platforms to discover and call each other. Examinable: part of the Agentforce Specialist *Multi-Agent Interoperability* section — **weight disputed, 5% or 15% depending on the source**. In MuleSoft Agent Fabric, A2A traffic is governed at Omni Gateway. |
| ADLC (Agent Development Lifecycle) | Salesforce's five-phase lifecycle for agents: Ideation & Design → Development (**inner loop**) → Testing & Validation → Deployment → Monitoring & Tuning (**outer loop**). Differs from SDLC in that deployment is day one, drift is expected, and token economics are a test result. Also the name of the `agentforce-adlc` research repo — say which you mean. |
| Agent Action | A unit of work an agent can execute — an autolaunched Flow, invocable Apex method, prompt template, Apex REST endpoint, `@AuraEnabled` method, or external API call. |
| Agent Broker | MuleSoft Agent Fabric's routing service: groups agents and tools into business domains and delegates tasks across A2A-compliant agents using graph-based routing. **Status disputed** — GA per launch coverage, Beta per April 2026 coverage. |
| Agent Fabric (MuleSoft) | The control plane for agents you didn't build — one pane of glass to register, govern, route and observe every agent and MCP endpoint across vendors. Four pillars: **Agent Registry** (discovery), **Omni Gateway** (governance), **Agent Broker** (orchestration), **Agent Visualizer** (observation). Launched Sept 2025; MuleSoft-licensed, **not** part of an Agentforce SKU. |
| Agent Network | A multi-agent composition in Agent Fabric declared in **YAML** — which agents, brokers, LLMs and MCP servers participate — deployed to CloudHub 2.0. Makes topology a versionable artifact. |
| Agent Registry | Agent Fabric's catalog of every agentic asset: custom agents, SaaS-embedded agents, MCP servers, A2A endpoints. **Federated** — anyone can run a registry and registries reference each other, DNS-shaped rather than a single corporate directory. |
| Agent Scanner | Agent Fabric component that auto-discovers and catalogs agents across **Agentforce, Amazon Bedrock, Google Vertex AI and Microsoft Copilot Studio**. GA January 2026. The shadow-agent finder. |
| Agent Script | The language agents are authored in since 2026: human-readable, compiles to portable JSON, blends deterministic rules (conditionals, explicit hand-offs) with LLM reasoning. Open source, Apache 2.0. **Replaced topic-and-instruction configuration as the default authoring model.** |
| Agentforce | Salesforce's platform for building autonomous AI agents that plan and execute tasks across CRM. In 2026 the platform umbrella is **Agentforce 360**. |
| Agentforce Builder | The current agent authoring UI, built around Agent Script. Since the week of **July 13, 2026** the *New Agent* button opens only this — the legacy builder can still edit existing agents but cannot create new ones. |
| Agentforce Commerce | Three prebuilt commerce agents, **GA July 6 2026**: **Shopper** (B2C storefront, discovery→checkout→service), **Buyer** (B2B via WhatsApp/SMS), **Merchant** (back-office catalogue in natural language). Sells natively inside ChatGPT with the catalogue synced from Business Manager — but **checkout stays on the merchant's own site**. |
| Agentforce Contact Center | Salesforce's native CCaaS, **GA 2026-02-23** (Enterprise Connect 2026), unifying voice, digital channels, CRM data and AI agents in one system. Note the position: Salesforce partners with Genesys/Five9/NiCE at the Voice layer and competes with them here. |
| Agentforce Coworker | **Beta (announced 2026-05-21, no GA date).** An agent embedded in the search bar — Salesforce and Slack today; Teams, ChatGPT, Claude and web later. **You author nothing**: it inherits the org's sharing rules, FLS and permissions, so what it can answer is a governance question, not a configuration one. Searches CRM, Data 360 DMOs and Slack, then routes to specialized agents to act. |
| Agentforce Data Library (ADL) | A managed grounding store: indexes Knowledge articles or uploaded files into a vector index and exposes a retriever for RAG. Lifecycle is scriptable via the ADL Connect API (Beta). |
| Agentforce Specialist | Salesforce certification for building, configuring and deploying agents. Restructured around how agents *think, interact and collaborate*, with a new AI Agents domain and a Multi-Agent Interoperability section. |
| Agentforce Vibes | Salesforce's agentic IDE (**2.0 is Developer Preview**): plans before acting, Plan Mode, MCP integration, built-in Skills and Rules, live LWC previews, current Claude and GPT models in one picker. Free in every Developer Edition org since April 2026. |
| Agentforce Voice | Autonomous inbound **and outbound** calls over **PSTN or SIP trunking** — Salesforce's replacement for the IVR. Live transcription into Salesforce Voice with human takeover mid-call; **barge-in** supported. Amazon Connect is native; Five9, Genesys, NiCE and Vonage connect via **Partner Telephony**. A voice action costs **30 Flex Credits** vs 20 standard. **US/Canada only as of early 2026**, global languages Beta. GA dates conflict — see [12-voice-and-contact-center](02-salesforce-ai/12-voice-and-contact-center/notes.md). |
| Atlas Reasoning Engine | The "brain" of Agentforce: interprets a request, plans steps and chooses actions. **Version 3.0 routes to subagents by reading their descriptions** rather than following a fixed decision tree. |
| BYOM (Bring Your Own Model) | Connecting an external foundation model (e.g. Claude on Amazon Bedrock) so Salesforce features call it through your own endpoint. |
| Custom Lightning Type | A purpose-built UI attached to an agent action's structured output. Defined once, renders idiomatically everywhere — LWC on desktop, native UI in the mobile app. |
| Custom Scorer | A user-defined quality metric graded against live agent sessions (Beta). Deployable as `aiAgentScorerDefinitions` metadata, so evaluation lives in source control. |
| Data Masking | Trust Layer step that replaces PII in a prompt with placeholder tokens before it leaves Salesforce, then re-inserts real values in the response. |
| Data Services Credits | The consumption unit for **data** work — data queries, unstructured data processed, intelligent processing — as distinct from **Flex Credits**, which cover prompts. Both can be drawn by the same feature; Agentforce Coworker bills against each for different operations. |
| Dynamic Grounding | Injecting live CRM or Data 360 data into a prompt at runtime so the model answers from your data instead of general knowledge. |
| Einstein | Umbrella brand for Salesforce's AI features, spanning older predictive tools and current generative capabilities. |
| Einstein Copilot | **Historical.** The predecessor conversational CRM assistant, folded into Agentforce. You'll still meet the name in 2024–25 material; it is not current product vocabulary. |
| Einstein Trust Layer | The security layer between Salesforce and LLM providers: prompt-injection defence, data masking, secure retrieval, zero retention, toxicity scoring, audit trail. |
| Flex Credits | The consumption billing unit for Agentforce and Data 360, drawn from one pooled balance. ~$500 per 100,000 credits; a standard action is 20 credits (~$0.10). **Billed per action, not per conversation.** |
| Guided Determinism | Agent Fabric's April 15 2026 capability: goal-based LLM reasoning paired with **codified handoff rules and human checkpoints**. Hybrid Reasoning's design point applied at the network layer instead of inside one agent. Shipped as "Agent Script for Agent Broker" — **not** the Agentforce authoring language of the same name. |
| Help Agent (Agentforce) | Prebuilt self-service support agent, **GA July 2026** — guided setup in "six clicks or less", web/text/voice from one screen, alongside a Customer Service Portal rebuilt as a single conversation bar. Billed **pay-per-resolution**. Salesforce's own benchmark: 4.3M inquiries, 70% resolved on `help.salesforce.com`. |
| Hybrid Reasoning | The Agent Script design point: you dial how much of an agent is deterministic business logic versus left to model reasoning. |
| Inner loop / outer loop | ADLC vocabulary. **Inner loop** = the tight build-and-try cycle run many times a day. **Outer loop** = the slow cycle of monitoring production and feeding improvements back. The outer loop is what catches drift — and **drift has no commit**. |
| Instructions (Guardrails) | Natural-language rules constraining agent behavior — what to always do, never do, how to respond. In Agent Script these become explicit script constructs rather than free-text fields. |
| Model Builder | Tool to register and configure LLMs — Salesforce-hosted or bring-your-own via Bedrock/Vertex — for use across Prompt Builder and Agentforce. |
| Multi-Agent Orchestration (MAO) | An **orchestrator agent** connecting to specialized subagents and presenting one point of contact, with shared context across channels. GA June 15, 2026. |
| Omni Gateway | **Formerly Flex Gateway** — same MuleSoft runtime, renamed and expanded to govern AI agents, MCP and A2A traffic alongside APIs. The rename is non-breaking and cosmetic (1.13.0), so CI/CD is unaffected; both names still circulate. In Agent Fabric it is the runtime policy layer between agents and the systems they reach. |
| Pay-per-resolution | Outcome-based pricing introduced with the Agentforce Help Agent: **$2 per issue resolved autonomously end-to-end**. Human escalations and negative-feedback sessions are free, and consumption during the interaction is unmetered. Third commercial model alongside Flex Credits and a negotiated **AELA** (Agentic Enterprise License Agreement — the VA's $1.6B/3yr, July 2026). |
| Prompt Builder | Declarative tool for creating reusable prompt templates that merge CRM record data and grounding sources before calling an LLM. Templates can also be exposed as MCP prompts. |
| Prompt Template | A reusable, versioned prompt definition with merge fields, resolved with live data at runtime. |
| Subagent (Agentforce) | A specialized agent invoked by an orchestrator. Its **description is the routing contract** — Atlas 3.0 reads it to decide routing, so write it like an API doc, not a label. |
| Topic (Agentforce) | **Legacy authoring concept.** A job category grouping related actions and instructions. Still present in agents built before mid-2026; superseded by Agent Script for new work. |
| Triggered Agent | An agent that fires on a defined event — a deal stage change, a Data 360 customer signal — rather than on a human utterance. |
| Zero Data Retention | Guarantee that model providers processing prompts via the Trust Layer don't store them or use them for training. |

## Data 360

> Formerly **Data Cloud**. The folder is still named `01-data-cloud/` so existing links and the dashboard keep working — the product name is Data 360.

| Term | Definition |
|---|---|
| Accelerated Data Ingest | Real-time CRM data into Data 360 with no pipeline lag (**GA**, Summer '26). Removes the most common cause of an agent answering confidently from stale state. |
| Activation | Publishing a segment or data to a target — Marketing Cloud, ad platforms, CRM — where action happens. |
| Calculated Insight | A metric (e.g. lifetime value, engagement score) computed over Data 360 data on a schedule with a SQL-like definition. |
| CDP (Customer Data Platform) | System category that unifies customer data into persistent profiles. Data 360 began as Salesforce's CDP; **the 2026 framing is a context engine that grounds agents**, which is a bigger job than a CDP. |
| Code Extension | Custom **Python** scripts and functions deployed to isolated containers inside Data 360. Current uses: batch data transformations and **custom chunking logic** on search index creation. |
| Data 360 | Salesforce's lakehouse-based platform that ingests, harmonizes, unifies and activates data from any source, and grounds AI agents in it. Renamed from Data Cloud at Dreamforce 2025. |
| Data 360 Consultant | The certification covering ingestion, modeling, identity resolution, insights, segmentation and activation. Renamed from *Data Cloud Consultant* on 2026-03-27; **exam code `Data-Con-101` unchanged**. |
| Data Graph | A precomputed, denormalized view of related data around a profile, built for millisecond real-time reads by agents and personalization. |
| Data Kit | The DevOps package that promotes Data 360 configuration — including code extensions and the data transforms built from them — from sandbox to production. |
| Data Stream | A configured ingestion feed bringing data into Data 360 from a connector, on a batch or streaming schedule. |
| Dataspace | A logical partition of Data 360 data. **Required when a SOQL query targets a DLO** — omit it and the query returns zero records silently, with no error. |
| DLO (Data Lake Object) | The stored, source-shaped table in the data lake created from a data stream — raw material awaiting harmonization. Does *not* share Platform object semantics. |
| DMO (Data Model Object) | A standardized object in Data 360's canonical data model that DLOs are mapped into, enabling cross-source consistency. |
| DSO (Data Source Object) | Representation of raw data exactly as it arrives from the source, before any mapping. |
| Federated Search | Querying a source **live at search time instead of ingesting and indexing it**. Always fresh and no data duplicated, but bound by the source's own rate limits. Agentforce Coworker federates **Slack** (180 queries/min per user) while *ingesting* Google Drive and SharePoint on a 1 hr incremental crawl — the same freshness-vs-latency trade-off as zero-copy federation. |
| Harmonization | Mapping disparate source fields into the standard data model so "email" from five systems becomes one consistent attribute. |
| Identity Resolution | Matching records across sources into one unified individual using match rules and reconciliation rules. Under profile-based pricing, its quality is a **direct recurring cost lever**. |
| Intelligent Context | Automatic extraction of unstructured content (PDFs, tables, images, flowcharts) into grounding data via a low-code pipeline. The same document can be interpreted from multiple business perspectives. |
| Lakehouse | Architecture combining a data lake's cheap open storage with a warehouse's query performance and governance. |
| Lakehouse Federation (Databricks) | Databricks' feature for querying an external system as if it were a native table. The mechanism behind **Data 360 File Sharing into Unity Catalog** — the *inward* path, where a Databricks notebook reads Salesforce data in place. Do not confuse with Data 360's own zero-copy federation, which points *outward*. |
| Match Rules | Criteria (exact or fuzzy — email, name+phone, etc.) that decide when two records represent the same person. |
| OSI | A vendor-neutral, YAML-based open-source standard for interoperable semantic models, metrics and relationships. Core spec finalized February 2026. |
| Profile (billing sense) | A **unified individual after identity resolution** — the unit Data 360 is priced on (~$240 per 1,000 baseline). Not a raw source row, so duplicates inflate a recurring bill. |
| Reconciliation Rules | Rules that pick the winning value (most recent, most frequent, source priority) when matched records conflict. |
| Retriever | A configured query against a search index or data graph that fetches the most relevant content to ground a prompt — Salesforce's RAG building block. |
| Search Index | Unstructured content (PDFs, transcripts, knowledge) that Data 360 has chunked and embedded so it's semantically searchable. |
| Segment | A defined audience slice built from profiles, attributes and insights — the unit you activate to other systems. |
| Semantic Layer | A governed layer of business definitions (what counts as "revenue") between raw data and consumers. **Tableau Semantics** is the Salesforce implementation: an agent asked "what was churn last quarter" gets the company's definition rather than inventing one. |
| `SET OPTIONS` | SOQL clause (Summer '26) specifying the Data 360 dataspace and controlling `NULL` / empty-string handling. Goes at the **very end** of the query. |
| STDM (Standard Data Model) | Salesforce's prebuilt Data 360 schema, so data landing from different sources arrives in a shape the platform already understands instead of one you map by hand. Agentforce writes **production agent session traces** as STDM records — which is why debugging a live agent is a Data 360 query. |
| Unified Profile | The single individual record produced after identity resolution, linking all source records and behaviors. |
| Unity Catalog | Databricks' governance layer for data and AI assets. **Salesforce Data 360 File Sharing into Unity Catalog** (GA October 2025) registers Data 360 objects as shared files that Databricks SQL reads directly, authenticated by **IAM Workload Identity Federation** — secretless, no long-lived key on either side. |
| Vector Database (Data 360) | Data 360's built-in store of embeddings for unstructured content, powering semantic search and grounded AI answers. |
| Zero Copy / BYOL | Federation pattern: query data in Snowflake, BigQuery, Databricks or Redshift in place — bring your own lake — without copying it into Data 360. |

## Platform & integration (Summer '26)

| Term | Definition |
|---|---|
| `accessCheck` | Agent Skill frontmatter declaring the **org permission** a skill needs (e.g. `userPerm: "ManageSandboxes"`), so it fails fast instead of dying inside a REST call. Sibling of `cliTools`, which declares the local CLI it needs. Both added to `forcedotcom/sf-skills` in late July 2026. |
| `findSessions` | The documented entry point in the `agentforce-observe` skill for locating a specific production agent conversation in Data 360 STDM trace records before analysing it. Companion reference: `stdm-queries.md`. |
| Headless 360 | The organizing idea of Summer '26: every major Salesforce capability reachable as an **API, an MCP tool, or a CLI command**, by a human, an app or an autonomous agent. |
| Hosted MCP Server | A Salesforce-hosted MCP server exposing org capability to any MCP client over standard OAuth. Standard servers (SObject, Data 360, Tableau) are **GA**; custom servers **respect the org's full sharing and security model**. |
| System Mode | Execution context ignoring the running user's permissions. Apex **triggers always run in system mode** at 67.0 and can no longer declare sharing or access modes. |
| User Mode | Execution context enforcing the running user's object permissions, FLS and sharing rules. **The default for Apex SOQL/SOSL/DML at API 67.0** — elevated access is now opt-in. |
| `with sharing` (default) | At API 67.0 a class with no sharing keyword defaults to `with sharing`. Previously it inherited the caller's context, which silently skipped sharing when it was the entry point. |
| `WITH SECURITY_ENFORCED` | **Retired — no longer compiles at 67.0.** Replaced by `WITH USER_MODE`, which handles polymorphic fields, checks the `WHERE` clause and reports every FLS violation instead of the first. |

## Claude / CCA

| Term | Definition |
|---|---|
| Agentic Loop | The core agent pattern: reason → act (call a tool) → observe the result → repeat until the goal is met. |
| CCA-F (Claude Certified Architect — Foundations) | Anthropic's proctored Foundations certification: 60 scenario-based questions across agentic architecture, Claude Code, MCP, prompting and context management. |
| Claude Agent SDK | Anthropic's framework for building production agents with the same loop, tools and context management that power Claude Code. |
| Claude Code | Anthropic's terminal-based agentic coding tool that reads, edits, tests and commits code in your repo. |
| CLAUDE.md | A project memory file Claude Code reads automatically — conventions, architecture notes, commands — shaping every session's behavior. |
| Compaction | Summarizing earlier conversation/tool history to reclaim context window space in long-running agent sessions. |
| Context Window | The maximum tokens a model can consider at once — the hard budget every agent design must manage. |
| Evals | Systematic tests that score prompt or agent output against defined criteria — how you improve AI systems on evidence instead of vibes. |
| Extended Thinking | A mode where Claude reasons step-by-step in a visible scratchpad before producing its final answer — better on hard problems. |
| Facade Tool Pattern | Fronting a large API surface with a few intent-based tools (`search` / `payload_examples` / `execute`) instead of hundreds of flat ones. The canonical fix for context-window blowout in MCP design; Data 360's MCP server uses it over ~200 REST operations. |
| Headless Mode (-p) | Running Claude Code non-interactively with a prompt flag, typically in CI pipelines, often with JSON output for automation. |
| JSON Schema | A contract describing required fields, types and constraints — used to define tools and validate structured output. |
| MCP (Model Context Protocol) | Open standard for connecting AI applications to external tools and data through one protocol — often described as USB-C for AI. |
| MCP Host / Client / Server | Host = the AI application (e.g. Claude Desktop); client = the connection handler inside it; server = the program exposing capabilities. |
| MCP Primitives | The three things a server can expose: tools (actions the model can invoke), resources (data to read) and prompts (reusable templates). |
| Orchestrator-Worker | Multi-agent pattern where a lead agent decomposes a task and delegates slices to specialized subagents, then synthesizes results. |
| Prompt Caching | Reusing a cached prompt prefix (system prompt, documents, tools) across calls to cut latency and cost dramatically. |
| Skills (Agent Skills) | A lightweight open format for extending a coding agent with specialized knowledge and workflows. Salesforce ships a library at `forcedotcom/sf-skills`; same format Claude Code uses. |
| Structured Output | Constraining a model's response to a JSON schema so downstream code can parse it reliably. |
| Subagent (Claude) | A worker agent running in its own separate context window, handling a delegated task without polluting the lead agent's context. |
| System Prompt | Instructions set before any user message that define the model's role, rules and output expectations. |
| Tool Use (Function Calling) | The model requests a structured call to a tool you defined; your code executes it and returns the result for the model to continue with. |

## Data & AI Core

| Term | Definition |
|---|---|
| Attention | The core transformer operation: for each token, score how relevant every other token is, and blend information accordingly. |
| Chunking | Splitting documents into pieces before embedding — chunk size and overlap strongly affect retrieval quality. Usually the single biggest lever on RAG quality. |
| Data Lineage | Tracking where data came from and how it was transformed — key for trust, debugging and compliance. |
| Data Pipeline | An automated flow that moves and transforms data between systems on a schedule or trigger. |
| Embedding | A numeric vector representing meaning; similar texts map to nearby vectors, enabling semantic comparison. |
| ETL / ELT | Pipeline patterns: transform before loading (ETL) vs load raw then transform inside the warehouse (ELT, the modern default). |
| Few-Shot Prompting | Steering a model by including a handful of worked examples in the prompt instead of retraining it. |
| Fine-tuning | Further training a model on domain data to shift its behavior — contrast with RAG, which supplies knowledge at runtime. |
| Hallucination | Confident but false model output; mitigated by grounding, RAG, citations and validation. |
| Idempotency | Property that re-running a pipeline or action produces the same result — essential for safe retries, and for agents that may repeat an action after a timeout. |
| Inference | Running a trained model to produce output; what you pay for per token on every API call. |
| LLM (Large Language Model) | A model trained on massive text corpora to predict tokens, capable of reasoning, generation and tool use. |
| Multi-Agent System | Multiple AI agents interacting — cooperating or competing — to solve a task no single agent handles well; the theory behind orchestrator-worker designs. |
| Prompt Injection | Attack where malicious instructions hidden in data (an email, a web page) hijack an agent — a core security concern in tool-using systems, and a Trust Layer control point. |
| RAG (Retrieval-Augmented Generation) | Pattern: retrieve relevant content, inject it into the prompt, and generate an answer grounded in it — the antidote to hallucination. |
| Semantic Search | Retrieval by meaning using embedding similarity rather than keyword matching. |
| Temperature | Sampling parameter controlling randomness: low = deterministic and repeatable, high = varied and creative. |
| Token | The unit models read and write — roughly ¾ of an English word. Context limits and API pricing are measured in tokens. |
| Transformer | The neural architecture behind modern LLMs, built on attention — the mechanism that lets a model weigh which parts of the input matter for each output token. |

## New terms (unsorted — file into sections above during weekly review)
