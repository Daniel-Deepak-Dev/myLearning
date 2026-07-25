# Agentforce platform

Builder, Agent Script, orchestration, channels, observability. Newest entries at the top.

---

## 2026-07-26 · Agentforce Builder and Agent Script are GA

**What changed.** Both the new [Agentforce Builder](https://help.salesforce.com/s/articleView?id=ai.agent_builder_tour.htm&type=5) and [Agent Script](https://developer.salesforce.com/docs/ai/agentforce/guide/agent-script.html) went generally available in the Summer '26 monthly cadence, per the Salesforce developer release guide. *(Exact GA date is not stated in a first-party announcement I could find — some secondary sources say February 2026, others still showed Beta docs as late as April 2026. The July 13 cutoff below is confirmed.)*

- **The new builder is now the default.** Starting the **week of July 13, 2026**, the *New Agent* button in Setup no longer opens the legacy builder. New agents are created only in Agentforce Builder. Note this removes agent *creation* only — existing legacy agents can still be edited, activated, versioned and managed.
- **One-click upgrade path.** [Upgrading a legacy agent](https://help.salesforce.com/s/articleView?id=ai.agent_setup_create_upgrade.htm&type=5) converts all subagents, actions, system messages, data and connections into Agent Script, then optionally optimizes the result for reliability.
- **Model choice moved into the script.** You can now [pin the model for an agent directly in Agent Script](https://developer.salesforce.com/docs/ai/agentforce/guide/ascript-model.html) instead of relying only on the org-wide model setting.

**What Agent Script actually is.** A human-readable expression language that compiles to portable JSON. It blends deterministic rules (conditionals, if/then, explicit hand-offs, precise tool use) with agentic LLM reasoning — the point being predictability. This is the mechanism behind "Hybrid Reasoning" in the Atlas Reasoning Engine: you dial how much is structured business logic vs. how much is left to the model.

**Why it matters.** Topic-and-instruction configuration was the Agentforce skill of 2025. Agent Script is the Agentforce skill of 2026 — it's the artifact that gets versioned, reviewed, diffed and deployed. Because agents compile to JSON, agent definitions finally behave like source code in a CI/CD pipeline.

**Study action:** rebuild one existing topic-based agent in Agent Script and diff the two behaviours in preview.

---

## 2026-07-26 · Agent Script is open source (Apache 2.0)

Salesforce open-sourced the whole Agent Script toolchain at [github.com/salesforce/agentscript](https://github.com/salesforce/agentscript): parser, linter, compiler, Language Server Protocol implementation and editor integrations.

**Why it matters.** An open parser/compiler means agent definitions can be linted and tested *outside* an org — in a plain CI job, with no Salesforce connection. It also means third-party harnesses (the community is already running compiled Agent Script under Pydantic AI) can execute the same logic. For an architect, this is the strongest signal yet that Salesforce wants agent logic to be portable rather than org-locked.

---

## 2026-07-26 · Multi-Agent Orchestration (Beta)

[Multi-Agent Orchestration](https://help.salesforce.com/s/articleView?id=ai.agent_multi_orch.htm&type=5) lets an **orchestrator agent** connect to other specialized agents in the org and present a single point of contact, so a user handles a cross-domain task without switching sessions.

**How you wire it.** In Agentforce Builder, open a draft agent as the orchestrator, then in the Explorer panel: **+ → Connect Agent as Subagent (Beta)**. Give each connected subagent a description — that description governs routing behaviour. With Agent Router, add each subagent under *Actions Available for Reasoning* and reference it with `@`.

**Why it matters.** The realistic enterprise pattern is many narrow, well-tested agents rather than one omniscient one. Orchestration is what makes that pattern usable, and the subagent *description* becomes a first-class design artifact — it's effectively the routing contract. Write it like an API doc, not a label.

---

## 2026-07-26 · Observability: Refined Agent Analytics + Custom Scorers (Beta)

- **[Refined Agent Analytics](https://help.salesforce.com/s/articleView?id=release-notes.rn_einstein_analytics_new_experience.htm&release=262&type=5)** unifies Service Agent and Employee Agent analytics into one view with 40+ metrics.
- **[Custom Scorers (Beta)](https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_scorers.htm&type=5)** lets you grade live sessions against your own KPIs — Sentiment, Tone of Voice, Product Interest, Escalation Trigger, Politeness — alongside Salesforce's standard quality metrics.

**The developer workflow is the interesting part.** Build scorers with [Next Gen Testing](https://help.salesforce.com/s/articleView?id=ai.agent_studio_testing_center_setup_tests.htm&type=5) in Agentforce Studio, *or* deploy them via Metadata API using the `aiAgentScorerDefinitions` type so they live in source control, then activate them from the **Scorer Hub** to run against live sessions. Requires the *Agentforce Scorer Beta* permission set.

**Why it matters.** "Is the agent good?" becomes a versioned, testable definition rather than a vibe. Metadata API support is the tell — evaluation is being treated as deployable infrastructure.

---

## 2026-07-26 · Agentforce Mobile SDK

The [Agentforce Mobile SDK](https://github.com/salesforce/AgentforceMobileSDK-iOS) embeds agents in native **iOS**, **Android** and **React Native** apps, either as a pre-built chat UI or headless (you own the UI).

- **React Native support:** one TypeScript codebase for both platforms, via a single `AgentforceService` object. Integration is three calls: **configure → (optional) add context → launch**.
- **Two agent types to choose between:** a **Service Agent** is customer-facing and *anonymous* (no login, good for public apps); an **Employee Agent** is internal and *authenticated* (the SDK obtains OAuth tokens through the Salesforce Mobile SDK).
- **Session context** is optional typed variables passed at launch so the agent can personalize replies.
- On iOS you supply the logged-in user's access token plus the published agent's 18-character **Bot Id**, and the SDK returns a complete native chat view.

**[Custom Lightning Types](https://developer.salesforce.com/blogs/2026/05/use-custom-lightning-types-in-agent-script-for-rich-agent-ui)** are the companion feature and are *not* mobile-specific: when an agent action returns structured data, a custom Lightning type attaches a purpose-built UI to it. Define once against the action output and it renders idiomatically everywhere — an LWC on desktop/web, the matching native UI in the mobile app.

**Why it matters.** Cross-surface rendering from a single definition is a genuine architecture win. Design agent action outputs as *typed structures*, not prose, and the UI follows for free.

---

## 2026-07-26 · Agentforce Data Library Connect API (Beta)

Agentforce Data Libraries (ADL) ground an agent in trusted content — they index Knowledge articles or uploaded files into a vector index and expose a retriever for RAG. Creating one used to be a manual Setup step; the new **ADL Connect API (Beta)** makes the whole lifecycle scriptable and CI/CD-ready.

Base resource: `/services/data/v67.0/einstein/data-libraries`

The five-step provisioning flow for a file-based library:

1. **Create the library** — a single `POST`. Note that `sourceType` is *nested* under `groundingSource` (`SFDRIVE` for files, or `KNOWLEDGE` / `RETRIEVER`). The response returns the `libraryId` every later step needs.
2. **Wait for upload readiness** — poll `GET …/{libraryId}/upload-readiness`. Data 360 is provisioning the objects that hold file metadata behind the scenes.
3. **Upload the file** — request a pre-signed S3 URL from `POST …/{libraryId}/file-upload-urls`, then `PUT` the file to that URL. Forward the returned headers verbatim or S3 rejects it with a 403.
4. **Index it** — `POST …/{libraryId}/indexing` chunks, embeds and builds the retriever.
5. **Ground the agent** — wire the library into the `.agent` file's `knowledge:` block and invoke `AnswerQuestionsWithKnowledge` from a subagent.

**Two gotchas worth memorizing:**

- Treat the library as ready when **`retrieverId` goes non-null**, *not* when the top-level `status` flips — status leads the retriever by 10–30 minutes.
- `rag_feature_config_id` is `"ARFPC_" + libraryId`, **not** the raw ID.

**Why it matters.** This is the "grounding as code" half of Headless 360. RAG configuration stops being click-ops and becomes a pipeline step.

---

## 2026-07-26 · Agentforce Help Agent + Customer Service Portal (GA July '26)

A prepackaged, self-service support agent with guided setup Salesforce describes as **deployable in minutes**, with **voice, web, portal and messaging** channels all turned on from a single screen. GA in **July 2026**, with **pay-per-resolution pricing** ($2 per autonomous end-to-end resolution) the same month.

**Salesforce's own benchmark:** Agentforce on `help.salesforce.com` handled **4.3 million inquiries and resolved 70%** of them. That's a first-party number and the strongest reference point available for a business case.

**Why it matters.** Two signals here. First, Salesforce is shipping *finished* agents, not just the tooling to build them — the differentiation moves from "can you build an agent" to "how well is yours grounded." Second, pay-per-resolution ties revenue to outcomes rather than conversations, which changes how you'd model ROI. See [pricing-and-certification.md](pricing-and-certification.md).

---

## 2026-07-26 · Agentforce Voice, Intelligent Context and model choice (Agentforce 360 baseline)

Context for anything built on the current platform:

- **Agentforce Voice** — low-latency, brand-tuned voice agents with live transcription into Salesforce Voice so a human can take over mid-call. First-class CCaaS support for **Amazon Connect, Five9, Genesys, NiCE and Vonage**. Full auditability runs through Data 360.
- **Intelligent Context** — automatically extracts and structures unstructured content (PDFs, tables, images, flowcharts) into grounding data, configured through a low-code pipeline. Notably, you can configure context so the *same* document is interpreted from multiple business perspectives.
- **Model choice** — the Atlas Reasoning Engine now supports **Google Gemini** alongside OpenAI and Anthropic on Amazon Bedrock.

**Why it matters.** Model choice at the reasoning-engine level plus model pinning in Agent Script means "which model runs this agent" is now an architecture decision you own, with cost and latency consequences per agent.

---

## Field notes

- **TTEC Digital** completed the first customer go-live of **Agentforce Contact Center** (client: Compass Working Capital), announced 2026-07-23.
- **Oviva**, a European digital health company, uses Agentforce to autonomously handle **300,000+ inbound messages/month**, deflecting half of all inquiries and resolving 40% of operational support requests without a human. Useful as a real deflection benchmark when sizing a business case.
- Salesforce committed **$1B to Switzerland over five years** (announced 2026-07-07) for Agentforce deployments, partner network growth and AI skills programs.

---

## Sources

- [The Salesforce Developer's Guide to the Summer '26 Release](https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release)
- [Agentforce 360 Announcements](https://www.salesforce.com/agentforce/what-is-new/)
- [Salesforce Announces Prepackaged Agentforce Help Agent](https://www.salesforce.com/news/stories/agentforce-help-agent-announcement/)
- [Salesforce Summer 2026 Product Release Announcement](https://www.salesforce.com/news/stories/summer-2026-product-release-announcement/)
- [TTEC Digital deploys first live Salesforce customer on Agentforce Contact Center](https://www.globenewswire.com/news-release/2026/07/23/3332068/0/en/TTEC-Digital-Deploys-First-Live-Salesforce-Customer-on-Agentforce-Contact-Center.html)
- [agentscript on GitHub](https://github.com/salesforce/agentscript)
