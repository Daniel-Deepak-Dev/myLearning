# Glossary — 163 Terms

Extracted from [the roadmap](ai-salesforce-architect-roadmap.html) glossary tab, grouped by track and alphabetized. Greppable and extendable — **add new terms here as you meet them**, in the right section, keeping alphabetical order. If a term deserves depth, it also earns a flashcard in its topic folder.

> **Currency:** definitions reflect **Summer '26 (API 67.0)**, the current release as of 2026-08-02. Where a term changed meaning in 2026, the entry says so — knowing the old meaning is what stops you answering an exam question from 2025 memory. Running detail and sources live in [05-release-radar/](05-release-radar/README.md).

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
| `AccessLevel` | The Apex enum that makes an operation's execution context explicit — `AccessLevel.USER_MODE` or `AccessLevel.SYSTEM_MODE`. Passed to `Database` methods and `Database.queryWithBinds`. At API 67.0 user mode is the default, so this is how you deliberately elevate rather than how you deliberately restrict. |
| Apex Managed Sharing | Granting record access from code by inserting rows into an object's `__Share` table — `ParentId`, `UserOrGroupId`, `AccessLevel`, `RowCause`. The `RowCause` decides survival: a `'Manual'` row is **deleted when the record owner changes**, while a row tagged with an **Apex sharing reason** (custom objects only) survives. Register a `Database.Batchable` recalculation class, or an admin's *Recalculate Sharing* silently wipes every row your code wrote. |
| Briefcase Builder | Where an admin defines which filtered records are primed onto a device for **offline** use in the Salesforce mobile/offline app, including custom objects and related objects **up to three levels deep**. No briefcase, no offline records. |
| Bulkification | Writing Apex so the cost of a transaction does not scale with the number of records in it: collect keys into a `Set`, do the query or DML once outside the loop, look results up inside it. Not optional — a trigger receives up to **200** records per invocation whether a user clicked Save or a load sent 50,000. |
| `Database.Cursor` | A server-side handle to a SOQL result set, paged with `fetch(position, count)` and surviving into later transactions for **2 days** — the Queueable-chain counterpart to a batch `QueryLocator`. **GA since Summer '24 (API 61.0), and not a row-limit escape hatch**: each `fetch()` costs a SOQL query and its rows count against the row limit. 50 M rows per cursor, 100 fetches per transaction, 10,000 cursors per org per 24 h. |
| `dist-tag` (npm) | A named pointer to one published version of an npm package. **They are not ordered by version** — `@salesforce/cli` currently has `latest` at 2.145.6, `latest-rc` at 2.146.3 and `nightly` at 2.147.3. `npm install` follows `latest`, so "the newest published version" and "the version you get" are routinely different, and a security patch can be published and still be unreachable from a plain install. |
| `Database.Stateful` | The marker interface that makes a batch class's **instance** member variables persist across `execute()` chunks. **Static variables still reset at every chunk** — which is why a running total so often ends up equal to the last chunk's count. |
| Dynamic Actions | Actions configured on the Lightning record page's Highlights Panel with per-action filters (field values, user, device type) instead of in the page layout's action section. Standard-object support is gated behind Setup → *Salesforce Mobile App* → **Enable Dynamic Actions on Mobile**. |
| Dynamic Forms | Record detail composed as individual **Field** and **Field Section** components on a Lightning page, each with its own visibility rule — replacing the monolithic Record Detail component and the record-type × profile layout matrix. Covers all **LWC-enabled standard objects** since Winter '24. Page layouts are **demoted, not retired**: they still own related lists, actions, compact layouts, Classic and the required/read-only field properties. |
| Elastic Async Limits | **Beta at API 67.0.** `Queueable` and `@future` enqueues are accepted up to **twice** the licensed daily limit, with the overflow throttled rather than rejected. It changes a failure mode, not just a ceiling: a runaway chain that used to stop with a `LimitException` now merely slows down. Track it with `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` in `System.OrgLimits.getMap()`. |
| External Credential | Half of the Winter '23 named-credential model: it holds the **authentication protocol** (OAuth 2.0, JWT, AWS Signature v4, Basic) and its **principals**, which map to permission sets — so "who may call this system" becomes a permission-set assignment. The paired **named credential** holds the base URL and points at it. **Legacy named credentials are deprecated** and have no principals to map at all. |
| `findSessions` | The documented entry point in the `agentforce-observe` skill for locating a specific production agent conversation in Data 360 STDM trace records before analysing it. Companion reference: `stdm-queries.md`. |
| Flow Approval Process | The current approval model: an orchestration of **stages**, each holding **approval steps** (which assign an *approval work item* to a user, group or queue) or **background steps**. Routes on any data or business rule, extends with Apex, and tracks in **Approval Submissions** / **Orchestration Runs**. Since **2026-02-18** Flow Orchestration is a standard flow type — no add-on, no usage-based run limits. **Classic approval processes are not retired**; the docs were renamed *Classic Approval Processes*. |
| Governor Limit | A per-**transaction** ceiling the multitenant runtime enforces on Apex — 100 SOQL queries (200 async), 50,000 rows, 20 SOSL queries, 150 DML statements, 10,000 DML rows, 10s/60s CPU, 6/12 MB heap. Breaching one throws an **uncatchable** `LimitException`, so every defence is built before the failure, by reading the `Limits` class. |
| Headless 360 | The organizing idea of Summer '26: every major Salesforce capability reachable as an **API, an MCP tool, or a CLI command**, by a human, an app or an autonomous agent. |
| Hosted MCP Server | A Salesforce-hosted MCP server exposing org capability to any MCP client over standard OAuth. Standard servers (SObject, Data 360, Tableau) are **GA**; custom servers **respect the org's full sharing and security model**. |
| `inherited sharing` | The Apex class modifier that takes the **caller's** sharing context and falls back to `with sharing` when the class is entered directly. The correct choice for a shared selector or utility now that a keyword-less class no longer inherits anything. Note that **inner classes never inherit the outer class's declaration** — they take the default. |
| Mixed DML Exception | Thrown when one transaction writes both a **setup** object (`User`, `Group`, `GroupMember`, `PermissionSetAssignment`, `QueueSobject`) and a standard or custom object. Split the second half into an async context; in tests, `System.runAs()` also creates the boundary. |
| Queueable Apex | The default async mechanism, displacing `@future`: an object with typed member variables, a job ID returned by `System.enqueueJob`, one child job for chaining, a 0–10 minute delay, `AsyncOptions.DuplicateSignature` to suppress repeats (a second enqueue throws `DuplicateMessageException`), and `System.attachFinalizer` for recovery. Chain depth is capped at 5 in **Developer and Trial orgs only** — production has no documented ceiling. |
| Release Update | A behaviour-changing platform change listed individually under Setup → Release Updates, each carrying a **Complete Steps By** release. **Not an advisory** — on that release Salesforce enforces it whether or not you acted. Many offer a reversible *Test Run*; Salesforce sometimes postpones or cancels one, and can **relaunch** an already-enforced update when a related change ships. Pinning Apex or an integration to an older API version does **not** opt you out, because the change is to org behaviour, not to an API version. |
| Salesforce Foundations | A **$0 built-in add-on** for Enterprise, Unlimited, Einstein 1 Sales and Einstein 1 Service that switches on a slice of Sales, Service, Marketing, Commerce and **Data 360** in an existing org, with Agentforce built in and **200K Flex credits** to start. Free commercially, not architecturally: it **auto-provisions Data 360** and starts a consumption meter that bills as overage. |
| Setup with Agentforce | **GA.** An agent working inside Setup — users and access troubleshooting, permission sets and sharing rules, objects and fields, flows, Lightning pages, report types, formulas — driven from a prompt bar on the reimagined Setup Home. **Setup actions are non-billable** (no Flex credits). It acts only on the admin's approval, only within that admin's permissions, and every change lands in the **Setup Audit Trail**. |
| `String.template()` | Summer '26 Apex string interpolation: `'…${key}…'.template(Map<String, Object>)`. Pairs with **multiline strings**, delimited by triple single quotes (`'''`), which arrived in the same release. Two traps — the newline right after the opening `'''` is trimmed, and a `Datetime` renders in **GMT** as `yyyy-MM-dd HH:mm:ss`, unlike `String.valueOf()`. |
| `stripInaccessible` | `Security.stripInaccessible(AccessType, records)` — **removes** the fields the running user cannot access and returns an `SObjectAccessDecision` instead of throwing, so the operation continues. `getRemovedFields()` reports what went. It does **not** check the operation itself: a user with no Create permission still gets a `DmlException` from the following `insert`. |
| System Mode | Execution context ignoring the running user's permissions. Apex **triggers always run in system mode** at 67.0 and can no longer declare sharing or access modes. |
| Transaction Finalizer | `System.Finalizer`, attached inside a Queueable's `execute()` with `System.attachFinalizer()` — the only code that still runs after an **uncatchable** `LimitException`, in a new transaction with a fresh budget. `FinalizerContext.getResult()` returns `ParentJobResult.SUCCESS` or `UNHANDLED_EXCEPTION`. It may make callouts and enqueue exactly one job, which allows the parent to be retried **five times** before the chaining limit. **Queueable only** — batch reports failures through `BatchApexErrorEvent`. |
| `Trigger.operationType` | The `System.TriggerOperation` enum (`BEFORE_INSERT`, `AFTER_UPDATE`, …) that lets a trigger body be a single `switch on` dispatch into a handler class. The modern replacement for the `Trigger.isBefore && Trigger.isInsert` ladder and for hand-rolled `TriggerFactory` frameworks. |
| User Mode | Execution context enforcing the running user's object permissions, FLS and sharing rules. **The default for Apex SOQL/SOSL/DML at API 67.0** — elevated access is now opt-in. |
| `with sharing` (default) | At API 67.0 a class with no sharing keyword defaults to `with sharing`. Previously it inherited the caller's context, which silently skipped sharing when it was the entry point. |
| `WITH SECURITY_ENFORCED` | **Retired — no longer compiles at 67.0.** Replaced by `WITH USER_MODE`, which handles polymorphic fields, checks the `WHERE` clause and reports every FLS violation instead of the first. |
| `WITH USER_MODE` | The SOQL/SOSL clause enforcing the running user's CRUD, FLS **and sharing** — the replacement for `WITH SECURITY_ENFORCED`, and already the behaviour of an untagged query in a class compiled at 67.0. Write it anyway: it survives an API-version bump as a statement of intent. Its `Database`-method equivalent is the `AccessLevel` argument. |
| Zip-slip | A path-traversal attack on archive extraction: an entry whose stored path escapes the target directory (`../../../.git/hooks/pre-commit`), so unzipping writes where the extractor never intended. Fixed in `@salesforce/source-deploy-retrieve` **13.0.1** (`W-23558165`) for static resources of `contentType` `application/zip` / `application/jar` during metadata→source conversion. The lesson beyond the CVE-shaped fact: **`sf project retrieve` is an inbound trust boundary**, executing org-controlled bytes on your machine. |

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

## AI research & benchmarks

> Salesforce AI Research's evaluation line. Running detail lives in [05-release-radar/ai-research-and-benchmarks.md](05-release-radar/ai-research-and-benchmarks.md).

| Term | Definition |
|---|---|
| AnchorBench | Benchmark for **long-horizon** persona stability, released 2026-07-27 under **CC BY-NC 4.0** (code included — blocks client work). 2,008 conversations, 27 personas, **85–130 sessions each**. Headline findings: user-state changes recalled at **chance (~0.25)**, no memory setting wins (0.430–0.459), and emotional vulnerability exposes more failures than explicit attacks. **Paper is not on arXiv** — every number comes from a README. |
| CRMArena / CRMArena-Pro | The CRM-work benchmark, **accepted to TMLR**. Runs agents inside real Salesforce org environments on Salesforce schemas, B2B and B2C. **~83% on structured single-turn tasks**, sharp degradation on multi-turn, and **confidentiality awareness close to absent unless explicitly prompted**. |
| Enterprise Deep Research (EDR) | Salesforce AI Research's **steerable** multi-agent research system (2025-10-24): a Master Planning Agent decomposing a query over four specialised search agents. *Steerable* = a human redirects mid-run rather than judging only the output. The first-party reference architecture behind Multi-Agent Orchestration's shape. |
| GIFT-Eval | Salesforce AI Research's **general time-series forecasting** benchmark, Apache-2.0. Seven frequency ranges, seven domains, a fixed **98 dataset configurations** per submission. Notable because competitors submit to it — including **Google Cloud AI Research** — which makes it neutral industry infrastructure rather than a vendor marketing surface. |
| LoCoBench-Agent | Long-context software-engineering benchmark ([arXiv 2511.13998](https://arxiv.org/abs/2511.13998)): 8,000 scenarios, 10 languages, up to 50 turns, **10K–1M tokens**. Two findings: long context degraded **less** than expected, and comprehension trades off against efficiency — so an agent that explores exhaustively is not simply better, it is more expensive under Flex Credits. |
| MFCL Audio | Function-calling benchmark evaluated **from speech**, not from a transcript — **ICML 2026**, 6,200 expert-verified tasks, two suites (**Text Audio** pipelined, **True Audio** end-to-end). Isolates **perception errors**, which corrupt tool-call *arguments* rather than intent. Grading is deterministic (AST-based), with no LLM judge. |
| Persona collapse | A model drifting off its assigned role, boundaries, values and communication style over a long conversation. Distinct from **trajectory recall** — AnchorBench's central finding is that the two come apart. |
| `replication_code_available` | A field in every GIFT-Eval submission's `config.json`. Read it before quoting a leaderboard position: of the five models merged 2026-07-31, **only one declared `"Yes"`**. Its sibling `testdata_leakage` is **self-declared, not audited**. |
| SCUBA | Named consistently alongside CRMArena-Pro and GIFT-Eval as Salesforce's agent-evaluation line. **No detail captured by this radar yet** — an acknowledged gap, not a summary. |
| Trajectory recall | Whether a model can distinguish what actually happened in a conversation from a plausible alternative that did not. Measured by AnchorBench's Trajectory Probe with four-option counterfactuals. The support-agent failure it predicts: the customer said at turn 3 they had cancelled, and at turn 40 the agent still acts on the old state. |
| Zero-shot forecasting | Forecasting a time series the model was never trained on — GIFT-Eval's target capability, and the forecasting analogue of a language model answering a question it never saw. |

## New terms (unsorted — file into sections above during weekly review)
