# Glossary — 77 Terms

Extracted from [the roadmap](ai-salesforce-architect-roadmap.html) glossary tab, grouped by track and alphabetized. Greppable and extendable — **add new terms here as you meet them**, in the right section, keeping alphabetical order. If a term deserves depth, it also earns a flashcard in its topic folder.

## Salesforce AI

| Term | Definition |
|---|---|
| Agent Action | A unit of work an agent can execute — an autolaunched Flow, invocable Apex method, prompt template, or external API call. |
| Agentforce | Salesforce's platform for building autonomous AI agents that plan and execute tasks across CRM using topics, actions, and the Atlas Reasoning Engine. |
| Agentforce Specialist | Salesforce certification validating skills in building, configuring, and deploying Agentforce agents and prompt templates. |
| Atlas Reasoning Engine | The "brain" of Agentforce: interprets a request, classifies it into a topic, plans steps, and chooses which actions to run. |
| BYOM (Bring Your Own Model) | Connecting an external foundation model (e.g., Claude on Amazon Bedrock) so Salesforce features can call it through your own endpoint. |
| Data Masking | Trust Layer step that replaces PII in a prompt with placeholder tokens before it leaves Salesforce, then re-inserts real values in the response. |
| Dynamic Grounding | Injecting live CRM or Data Cloud data into a prompt at runtime so the model answers from your data instead of general knowledge. |
| Einstein | Umbrella brand for Salesforce's AI features, spanning older predictive tools and current generative capabilities. |
| Einstein Copilot | The predecessor conversational CRM assistant, since folded into the Agentforce platform. |
| Einstein Trust Layer | The security layer between Salesforce and LLM providers: data masking, secure retrieval, zero retention, toxicity scoring, and an audit trail. |
| Instructions (Guardrails) | Natural-language rules attached to topics/agents that constrain behavior — what to always do, never do, and how to respond. |
| Model Builder | Tool to register and configure LLMs — Salesforce-hosted or bring-your-own via Bedrock/Vertex — for use across Prompt Builder and Agentforce. |
| Prompt Builder | Declarative tool for creating reusable prompt templates that merge CRM record data and grounding sources before calling an LLM. |
| Prompt Template | A reusable, versioned prompt definition with merge fields, resolved with live data at runtime. |
| Topic (Agentforce) | A job category inside an agent that groups related actions and instructions, scoping what the agent is allowed to do for that kind of request. |
| Zero Data Retention | Guarantee that model providers processing prompts via the Trust Layer don't store them or use them for training. |

## Data Cloud

| Term | Definition |
|---|---|
| Activation | Publishing a segment or data to a target — Marketing Cloud, ad platforms, CRM — where action happens. |
| Calculated Insight | A metric (e.g., lifetime value, engagement score) computed over Data Cloud data on a schedule with a SQL-like definition. |
| CDP (Customer Data Platform) | System category that unifies customer data from many sources into persistent profiles usable by other tools; Data Cloud is Salesforce's CDP and more. |
| Data Cloud | Salesforce's lakehouse-based customer data platform that ingests, harmonizes, unifies, and activates data from any source. |
| Data Cloud Consultant | Salesforce certification covering ingestion, modeling, identity resolution, insights, segmentation, and activation. |
| Data Graph | A precomputed, denormalized view of related data around a profile, built for millisecond real-time reads by agents and personalization. |
| Data Stream | A configured ingestion feed bringing data into Data Cloud from a connector, on a batch or streaming schedule. |
| DLO (Data Lake Object) | The stored, source-shaped table in the data lake created from a data stream — raw material awaiting harmonization. |
| DMO (Data Model Object) | A standardized object in Data Cloud's canonical data model that DLOs are mapped into, enabling cross-source consistency. |
| DSO (Data Source Object) | Representation of raw data exactly as it arrives from the source, before any mapping. |
| Harmonization | Mapping disparate source fields into the standard data model so "email" from five systems becomes one consistent attribute. |
| Identity Resolution | Matching records across sources into one unified individual using match rules and reconciliation rules. |
| Lakehouse | Architecture combining a data lake's cheap open storage with a warehouse's query performance and governance. |
| Match Rules | Criteria (exact or fuzzy — email, name+phone, etc.) that decide when two records represent the same person. |
| Reconciliation Rules | Rules that pick the winning value (most recent, most frequent, source priority) when matched records conflict. |
| Retriever | A configured query against a search index or data graph that fetches the most relevant content to ground a prompt — Salesforce's RAG building block. |
| Search Index | Unstructured content (PDFs, transcripts, knowledge) that Data Cloud has chunked and embedded so it's semantically searchable. |
| Segment | A defined audience slice built from profiles, attributes, and insights — the unit you activate to other systems. |
| Unified Profile | The single individual record produced after identity resolution, linking all source records and behaviors. |
| Vector Database (Data Cloud) | Data Cloud's built-in store of embeddings for unstructured content, powering semantic search and grounded AI answers. |
| Zero Copy / BYOL | Federation pattern: query data in Snowflake, BigQuery, or Databricks in place — bring your own lake — without copying it into Data Cloud. |

## Claude / CCA

| Term | Definition |
|---|---|
| Agentic Loop | The core agent pattern: reason → act (call a tool) → observe the result → repeat until the goal is met. |
| CCA-F (Claude Certified Architect — Foundations) | Anthropic's proctored Foundations certification: 60 scenario-based questions across agentic architecture, Claude Code, MCP, prompting, and context management. |
| Claude Agent SDK | Anthropic's framework for building production agents with the same loop, tools, and context management that power Claude Code. |
| Claude Code | Anthropic's terminal-based agentic coding tool that reads, edits, tests, and commits code in your repo. |
| CLAUDE.md | A project memory file Claude Code reads automatically — conventions, architecture notes, commands — shaping every session's behavior. |
| Compaction | Summarizing earlier conversation/tool history to reclaim context window space in long-running agent sessions. |
| Context Window | The maximum tokens a model can consider at once — the hard budget every agent design must manage. |
| Evals | Systematic tests that score prompt or agent output against defined criteria — how you improve AI systems on evidence instead of vibes. |
| Extended Thinking | A mode where Claude reasons step-by-step in a visible scratchpad before producing its final answer — better on hard problems. |
| Headless Mode (-p) | Running Claude Code non-interactively with a prompt flag, typically in CI pipelines, often with JSON output for automation. |
| JSON Schema | A contract describing required fields, types, and constraints — used to define tools and validate structured output. |
| MCP (Model Context Protocol) | Open standard for connecting AI applications to external tools and data through one protocol — often described as USB-C for AI. |
| MCP Host / Client / Server | Host = the AI application (e.g., Claude Desktop); client = the connection handler inside it; server = the program exposing capabilities. |
| MCP Primitives | The three things a server can expose: tools (actions the model can invoke), resources (data to read), and prompts (reusable templates). |
| Orchestrator-Worker | Multi-agent pattern where a lead agent decomposes a task and delegates slices to specialized subagents, then synthesizes results. |
| Prompt Caching | Reusing a cached prompt prefix (system prompt, documents, tools) across calls to cut latency and cost dramatically. |
| Structured Output | Constraining a model's response to a JSON schema so downstream code can parse it reliably. |
| Subagent | A worker agent running in its own separate context window, handling a delegated task without polluting the lead agent's context. |
| System Prompt | Instructions set before any user message that define the model's role, rules, and output expectations. |
| Tool Use (Function Calling) | The model requests a structured call to a tool you defined; your code executes it and returns the result for the model to continue with. |

## Data & AI Core

| Term | Definition |
|---|---|
| Attention | The core transformer operation: for each token, score how relevant every other token is, and blend information accordingly. |
| Chunking | Splitting documents into pieces before embedding — chunk size and overlap strongly affect retrieval quality. |
| Data Lineage | Tracking where data came from and how it was transformed — key for trust, debugging, and compliance. |
| Data Pipeline | An automated flow that moves and transforms data between systems on a schedule or trigger. |
| Embedding | A numeric vector representing meaning; similar texts map to nearby vectors, enabling semantic comparison. |
| ETL / ELT | Pipeline patterns: transform before loading (ETL) vs load raw then transform inside the warehouse (ELT, the modern default). |
| Few-Shot Prompting | Steering a model by including a handful of worked examples in the prompt instead of retraining it. |
| Fine-tuning | Further training a model on domain data to shift its behavior — contrast with RAG, which supplies knowledge at runtime. |
| Hallucination | Confident but false model output; mitigated by grounding, RAG, citations, and validation. |
| Idempotency | Property that re-running a pipeline or action produces the same result — essential for safe retries. |
| Inference | Running a trained model to produce output; what you pay for per token on every API call. |
| LLM (Large Language Model) | A model trained on massive text corpora to predict tokens, capable of reasoning, generation, and tool use. |
| Multi-Agent System | Multiple AI agents interacting — cooperating or competing — to solve a task no single agent handles well; the theory behind orchestrator-worker designs. |
| Prompt Injection | Attack where malicious instructions hidden in data (an email, a web page) hijack an agent — a core security concern in tool-using systems. |
| RAG (Retrieval-Augmented Generation) | Pattern: retrieve relevant content, inject it into the prompt, and generate an answer grounded in it — the antidote to hallucination. |
| Semantic Layer | A governed layer of business definitions (what counts as "revenue") sitting between raw data and consumers, human or AI. |
| Semantic Search | Retrieval by meaning using embedding similarity rather than keyword matching. |
| Temperature | Sampling parameter controlling randomness: low = deterministic and repeatable, high = varied and creative. |
| Token | The unit models read and write — roughly ¾ of an English word. Context limits and API pricing are measured in tokens. |
| Transformer | The neural architecture behind modern LLMs, built on attention — the mechanism that lets a model weigh which parts of the input matter for each output token. |

## New terms (unsorted — file into sections above during weekly review)
