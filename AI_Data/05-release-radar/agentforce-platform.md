# Agentforce platform

Builder, Agent Script, orchestration, channels, observability. Newest entries at the top.

---

## 2026-08-03 · React Native Agentforce 0.4.0 — `onAgentResponse` was a no-op on iOS

**What changed.** [`salesforce/AgentforceMobileSDK-ReactNative`](https://github.com/salesforce/AgentforceMobileSDK-ReactNative) released **v0.4.0**, titled **262.1.2**; `@salesforce/react-native-agentforce` **0.4.0** reached npm on 2026-08-03 at 16:49 UTC under Apache-2.0. It is the React Native bridge picking up [the iOS major recorded below](#2026-07-31--agentforce-mobile-sdk-26212--a-patch-that-is-a-major-and-five-new-gen-ui-components).

- **Native floors move underneath it.** iOS `AgentforceSDK` → **18.26.8**, `AgentforceVoice` → **2.8.2**; Android → **15.130.1**.
- **`onAgentResponse` no longer no-ops on iOS.** The callback previously did nothing on iOS while working on Android; the two platforms now behave the same.
- **Tabular UI rendering** arrives on iOS, matching the `Table` Gen UI component from the native release.
- **Android** fixes absolute-URL handling in chat panels.

**Why it matters.** A callback that silently does nothing is the worst failure shape available: no error, no log, no crash — just an event that never arrives.

Teams hitting it would have papered over it by polling state or scraping the rendered UI, and that workaround is now the bug. Audit for it before upgrading, not after.

The bridge is also how the **Swift 6 strict-concurrency major** reaches a React Native app. The JS bump reads as a minor; the transitive native change does not.

**Gotchas:**
- **`peerDependencies` are `react: "*"` and `react-native: "*"`** — no floor at all. npm will happily pair 0.4.0 with an RN version the native SDKs were never tested against.
- **`engines.node` is `>=18`** on the JS package. That is unrelated to the `sf` CLI's move to Node 22 — do not treat one as evidence about the other.
- **The package bundles no Mobile SDK.** `dependencies` is empty; its own description says the host app adds the Mobile SDK. Installing it is not installing Agentforce.
- **Three version lines per release**: npm `0.4.0`, release title `262.1.2`, native tags `18.26.8` (iOS) and `15.130.1` (Android). Only the native tags carry severity.
- npm name `@salesforce/react-native-agentforce`, repo `salesforce/AgentforceMobileSDK-ReactNative`, package directory `AgentforceSDK-ReactNative-Bridge` — three different names for one artifact. Search on all three.
- [`AgentforceMobileSDK-Android`](https://github.com/salesforce/AgentforceMobileSDK-Android) shows **no August 2026 release of its own** (newest is 262.1.2 / `v15.130.1`, 2026-07-31, checked 2026-08-05 03:06 UTC). The Android floor moved inside the bridge, not on the Android line.

**Study action:** in a scratch React Native app, pin `@salesforce/react-native-agentforce` to **0.3.0**, register an `onAgentResponse` handler that logs, and run it on an iOS simulator and an Android emulator — watch iOS stay silent. Bump to **0.4.0** and run both again.

**Status:** Released **2026-08-03**. npm `@salesforce/react-native-agentforce` **0.4.0**, Apache-2.0, still **pre-1.0**. Covers Service Agent and Employee Agent.

**Sources:** [AgentforceMobileSDK-ReactNative releases](https://github.com/salesforce/AgentforceMobileSDK-ReactNative/releases) · [`@salesforce/react-native-agentforce` on npm](https://www.npmjs.com/package/@salesforce/react-native-agentforce)

---

## 2026-07-31 · Agentforce Mobile SDK 262.1.2 — a "patch" that is a major, and five new Gen UI components

**What changed.** [`salesforce/AgentforceMobileSDK-iOS`](https://github.com/salesforce/AgentforceMobileSDK-iOS) published **Agentforce Mobile SDK 262.1.2** on 2026-07-31 at 20:34 UTC under git tag **`18.26.8`**. It adds a customizable **splash screen** and moves the whole SDK to **Swift 6 strict concurrency** — declared in the notes as *"a major release, 18.0.0"*.

**Five new customizable components** join the Gen UI set, all of them shapes an agent action can now render natively rather than as prose:

- `Table`
- `Schedule`
- `DataGroup`
- `QueryOption`
- `VerticalCard`

**Fixes worth knowing by name**, because each is a symptom you would otherwise misdiagnose as your own bug:

- Record selector showed **raw IDs instead of names**
- **Lightning Out 2.0** inline scrolling and WebView reuse
- **Gen UI LWC** rendering on mobile
- Voice panel not dismissing on **session auto-end**
- **Memory leak in the pre-chat submit button**
- `INQUIRE` input values lost on re-render
- SPM/XCFramework resource lookups failing for images and HTML entities

**Why it matters.** The five components extend the *design agent output as typed structures* argument one concrete step — `Table` and `Schedule` are exactly the returns that used to be flattened into a sentence.

But the release is more useful as a versioning lesson. **262.1.2 reads like a patch and is a Swift-language major.** An app on 262.1.0 (tag `17.31.6`) that bumps to it inherits strict-concurrency compilation across the whole dependency: a sprint, not an afternoon.

**Gotchas:**
- **Two version lines on one release, and they disagree about severity.** The marketing name went `262.1.0 → 262.1.2` (patch-shaped); the git tag went `17.31.6 → 18.26.8` (major-shaped). **Read the tag, not the title.**
- The SDK declares a dependency on **`AgentforceService` 6.10.0**, while [`forcedotcom/AgentforceMobileService-iOS`](https://github.com/forcedotcom/AgentforceMobileService-iOS) is already at **6.11.2** (2026-07-31 19:51 UTC). The SDK's floor lags the service's head — do not assume the newest service build is the tested one.
- The release notes publish **no minimum iOS or Xcode version**, and Swift 6 strict concurrency implies a modern toolchain. Confirm in a branch before committing to the bump.

**Study action:** in a throwaway iOS app, pin `AgentforceMobileSDK-iOS` to tag `17.31.6`, build, then move the pin to `18.26.8` and build again — count the strict-concurrency errors. That number is the real cost of the "patch". Then render an action output through the new `Table` component and compare it against the same data returned as text.

**Status:** Released **2026-07-31**, tag `18.26.8`, marketed as Agentforce Mobile SDK **262.1.2**. iOS only; the Android and React Native lines move separately.

**Sources:** [Release 18.26.8](https://github.com/salesforce/AgentforceMobileSDK-iOS/releases/tag/18.26.8) · [AgentforceMobileSDK-iOS releases](https://github.com/salesforce/AgentforceMobileSDK-iOS/releases) · scan note [01-agentforce/2026-08-02](01-agentforce/2026-08-02.md)

---

## 2026-07-27 · Multi-Agent Orchestration is GA — status corrected

> **Correction (2026-07-27):** this entry previously recorded Multi-Agent Orchestration as **Beta**. Secondary sources date **GA to June 15, 2026** as part of Summer '26. Salesforce Help still labels the in-builder *Connect Agent as Subagent* step **(Beta)**, so product page and setup docs disagree — verify in your own org before quoting a status. See [01-agentforce/2026-07-27.md](01-agentforce/2026-07-27.md).

[Multi-Agent Orchestration](https://help.salesforce.com/s/articleView?id=ai.agent_multi_orch.htm&type=5) lets an **orchestrator agent** connect to other specialized agents in the org and present a single point of contact, so a user handles a cross-domain task without switching sessions, with shared context across channels.

**How you wire it.** In Agentforce Builder, open a draft agent as the orchestrator, then in the Explorer panel: **+ → Connect Agent as Subagent (Beta)**. Give each connected subagent a description — that description governs routing behaviour. With Agent Router, add each subagent under *Actions Available for Reasoning* and reference it with `@`.

**Why it matters.** The realistic enterprise pattern is many narrow, well-tested agents rather than one omniscient one. Orchestration is what makes that pattern usable, and the subagent *description* becomes a first-class design artifact — it's effectively the routing contract. Write it like an API doc, not a label. **Atlas Reasoning Engine 3.0 routes by reading each subagent's description rather than following a fixed decision tree**, which makes that field executable configuration, not documentation: a vague description produces intermittent mis-routing that looks like a model failure but is a specification failure.

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

## 2026-07-26 · Observability: Refined Agent Analytics + Custom Scorers (Beta)

- **[Refined Agent Analytics](https://help.salesforce.com/s/articleView?id=release-notes.rn_einstein_analytics_new_experience.htm&release=262&type=5)** unifies Service Agent and Employee Agent analytics into one view with 40+ metrics.
- **[Custom Scorers (Beta)](https://help.salesforce.com/s/articleView?id=ai.generative_ai_optimize_scorers.htm&type=5)** lets you grade live sessions against your own KPIs — Sentiment, Tone of Voice, Product Interest, Escalation Trigger, Politeness — alongside Salesforce's standard quality metrics.

**The developer workflow is the interesting part.** Build scorers with [Next Gen Testing](https://help.salesforce.com/s/articleView?id=ai.agent_studio_testing_center_setup_tests.htm&type=5) in Agentforce Studio, *or* deploy them via Metadata API using the `aiAgentScorerDefinitions` type so they live in source control, then activate them from the **Scorer Hub** to run against live sessions. Requires the *Agentforce Scorer Beta* permission set.

**Why it matters.** "Is the agent good?" becomes a versioned, testable definition rather than a vibe. Metadata API support is the tell — evaluation is being treated as deployable infrastructure.

---

## 2026-07-26 · Agentforce Mobile SDK

> **Correction (2026-08-02):** the version table below left `salesforce/AgentforceMobileSDK-iOS` blank with "independent · —". It is filled in: tag `18.26.8` = marketing version 262.1.2. The version line is not merely independent, it is **differently scaled** — see the [2026-07-31 entry](#2026-07-31--agentforce-mobile-sdk-26212--a-patch-that-is-a-major-and-five-new-gen-ui-components).

The [Agentforce Mobile SDK](https://github.com/salesforce/AgentforceMobileSDK-iOS) embeds agents in native **iOS**, **Android** and **React Native** apps, either as a pre-built chat UI or headless (you own the UI).

- **React Native support:** one TypeScript codebase for both platforms, via a single `AgentforceService` object. Integration is three calls: **configure → (optional) add context → launch**.
- **Two agent types to choose between:** a **Service Agent** is customer-facing and *anonymous* (no login, good for public apps); an **Employee Agent** is internal and *authenticated* (the SDK obtains OAuth tokens through the Salesforce Mobile SDK).
- **Session context** is optional typed variables passed at launch so the agent can personalize replies.
- On iOS you supply the logged-in user's access token plus the published agent's 18-character **Bot Id**, and the SDK returns a complete native chat view.

**[Custom Lightning Types](https://developer.salesforce.com/blogs/2026/05/use-custom-lightning-types-in-agent-script-for-rich-agent-ui)** are the companion feature and are *not* mobile-specific: when an agent action returns structured data, a custom Lightning type attaches a purpose-built UI to it. Define once against the action output and it renders idiomatically everywhere — an LWC on desktop/web, the matching native UI in the mobile app.

**Why it matters.** Cross-surface rendering from a single definition is a genuine architecture win. Design agent action outputs as *typed structures*, not prose, and the UI follows for free.

**Gotchas — the mobile artifacts do not share a version line.** Three separately versioned packages, and assuming a single "Agentforce mobile version" is an easy way to pin the wrong thing:

| Artifact | Version line | Latest seen |
|---|---|---|
| `salesforce/AgentforceMobileSDK-ReactNative` (npm `@salesforce/react-native-agentforce`) | 0.x | **0.3.0**, 2026-07-28 — bundles Agentforce SDK **262.1** (iOS 17.31.6) |
| `forcedotcom/AgentforceMobileService-iOS` | 6.11.x | **6.11.2**, 2026-07-31 19:51 UTC (commit `f86eb61`) |
| `salesforce/AgentforceMobileSDK-iOS` | independent (tag ≠ marketing name) | **tag `18.26.8`** = "262.1.2", 2026-07-31 20:34 UTC — [entry above](#2026-07-31--agentforce-mobile-sdk-26212--a-patch-that-is-a-major-and-five-new-gen-ui-components) |

`AgentforceMobileService-iOS` ships as an **SPM binary distribution** — `Package.swift` points at a precompiled `.xcframework`, so a commit there is a **pointer bump with no changelog in the repository**. The 6.11.2 bump published no release and no notes; the substance is in a binary elsewhere. Track each dependency separately.

**Study action:** in any app embedding Agentforce, list the three package versions in one place in your README, and record which Agentforce SDK build (`262.x`) each resolves to — that mapping is not published anywhere.

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

## 2026-05-21 · Agentforce Coworker (Beta) — the search bar becomes the agent

> **Backfill (recorded 2026-07-28).** This radar had no Coworker entry despite the announcement being two months old. Added as verified gap-fill, dated to the announcement, not to the scan.

**What changed.** Marc Benioff announced [Agentforce Coworker](https://www.salesforce.com/agentforce/coworker/) on **May 21, 2026**, calling it the biggest thing Salesforce shipped that quarter and describing it as effectively *replacing* Salesforce Search. It is **Beta today for all Agentforce customers**, in the Salesforce global search bar and in Slack, with web, **Microsoft Teams, ChatGPT, Claude** and a desktop app slated for "later this year."

- **You author nothing.** No Agent Script, no topics, no actions. Setup → Quick Find *Agentforce Coworker* → Turn On → Turn on End User Experience → assign users. Requires the **Agentforce Coworker Admin** permission set; **Enterprise, Unlimited and Agentforce 1** editions; **not supported on Government Cloud Plus**. Enabling it **automatically enables Einstein**.
- **Grounded on Data 360**, and the [data-source model](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-limits-and-guidelines.html) is the interesting part: **Slack is federated, not ingested** (queried live via Slack Authentication), while **Google Drive and SharePoint are ingested** on a 1 hr incremental crawl. Any DMO in the data space can be added.
- **It routes to specialized agents** — Sales Coach Agent, Support Agent — so it's a front door onto the agent estate rather than a competitor to it.
- **[Billing has two modes that coexist](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-billing-considerations.html).** Seat-based (Agentforce 1, or Agentforce for Sales/Service/Industries): searching CRM or Slack costs **zero credits**. Usage-based: **Flex Credits** for prompts, **Data Services Credits** for data queries and processing. Guest, unauthenticated and portal users are always usage-based.

**The claim that doesn't survive checking.** Secondary coverage repeats a **"270+ external data sources"** figure. The first-party Beta limits page lists **three**: Salesforce CRM, Data 360 objects, and Slack — with **Google Drive, SharePoint and Jira pilot-only**, requiring an account executive. Don't scope client work on the marketing number.

**Why it matters.** Every other Agentforce advance in 2026 has been about *authoring* — Agent Script, orchestration, scorers. Coworker inverts it: nothing is authored and everything is inherited, so what it can answer is decided entirely by the org's sharing model and field-level security. Enabling it is, in practice, an instant org-wide sharing audit performed by every licensed user through a conversational interface. That's the risk and the sales pitch in the same sentence. The ChatGPT/Claude surfaces add a second governance question — what leaves the org, under whose identity, logged where.

**Study action:** turn it on in a dev org, then log in as a restricted user and ask for something they shouldn't see. Confirm sharing holds before a client tests it for you.

**Status:** Beta, available to all Agentforce customers. Announced 2026-05-21. **No GA date announced** as of 2026-07-28. Beta Services Terms apply — consumption under Non-GA services carries no refund or credit rights.

**Sources:** [Agentforce Coworker developer guide (Beta)](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-a-home.html) · [Turn On Agentforce Coworker](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-turn-on-infrastructure.html) · [Limits and Guidelines](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-limits-and-guidelines.html) · [Billing Considerations](https://developer.salesforce.com/docs/data/agentforce-coworker/guide/agentforce-coworker-billing-considerations.html) · [Salesforce Announces Agentforce Coworker: AI 'In Every Search Bar' (Salesforce Ben)](https://www.salesforceben.com/salesforce-announces-agentforce-coworker-ai-in-every-search-bar/) · [Meet Your Users' New AI Teammate (Salesforce Admins)](https://admin.salesforce.com/blog/2026/meet-your-users-new-ai-teammate-introducing-agentforce-coworker)

**Study folder:** [02-salesforce-ai/10-agentforce-coworker](../02-salesforce-ai/10-agentforce-coworker/notes.md)

---

## 2026-02-23 · Agentforce Contact Center is GA — and Voice is a product line, not a channel

> **Backfill (recorded 2026-07-28).** Voice had exactly one line in this radar (a bullet in the Agentforce 360 baseline entry) and **"Contact Center" appeared nowhere** — despite Contact Center being GA since February. Dated to the GA, not the scan.

**What changed.** [Agentforce Contact Center](https://www.uctoday.com/unified-communications/salesforce-agentforce-contact-center/) went **GA February 23, 2026**, launched at Enterprise Connect 2026 — Salesforce's own native CCaaS, pitched as "the only contact center solution that unifies voice, digital channels, CRM data, and AI agents natively in a single system."

Separate the two things it's built on:

- **Agentforce Voice** — the capability. Autonomous **inbound and outbound** calls over **PSTN or SIP trunking**, explicitly positioned as replacing the IVR. **Barge-in** (the customer interrupting mid-sentence), automatic conversation logging, and context transfer with live transcription into Salesforce Voice on escalation. Amazon Connect is **native** (Salesforce manages provisioning); Five9, Genesys, NiCE and Vonage connect via **Partner Telephony**.
- **Agentforce Contact Center** — the product you buy instead of a partner.

**Summer '26 added SIP routing and the Mobile SDK** as GA; **Voice for Digital Channels** reached GA in Q2 2026 (web chat, mobile apps, WhatsApp, messaging). Global languages remain **Beta** per the [July 27 scan](01-agentforce/2026-07-27.md).

**Three things that decide whether a voice project happens.**

1. **Region.** Voice was **US and Canada only** as of early 2026, global languages Beta. From a European practice this is the first question, not a footnote — and the most likely reason a project doesn't proceed.
2. **Billing model.** A voice action is **30 Flex Credits** vs 20 standard — but there is also a **per-minute model at ~60 credits/min**. A five-minute call with three actions is ~90 credits one way and ~300 the other. See [pricing-and-certification.md](pricing-and-certification.md).
3. **Escalation prerequisites.** Handing a call to a human needs **Partner Telephony Setup** configured, **Service Cloud Voice** enabled *and* **Contact Center setup** completed — all outside Agentforce. A voice agent that answers calls correctly can still fail its first escalation.

**One date to hold loosely.** Most sources put Voice GA at **October 21, 2025** (Winter '26 cycle); others describe it moving "from pilot to GA" in **Spring '26** with Atlas-powered autonomous reasoning. Progressive GA is the likely reconciliation — channel first, fully reasoning agent later — but that's inference. Don't quote either date to a client without checking.

**Why it matters beyond the feature list.** Voice fails in ways text doesn't: latency is a design constraint because every grounding hop is dead air, barge-in means long planned answers rarely land, and handoff is a protocol problem rather than a prompt problem. None of it is fixed by Agent Script tuning. Also worth holding in mind commercially — Salesforce **partners** with Genesys, Five9 and NiCE at the Voice layer and **competes** with them at the Contact Center layer.

**Status:** Contact Center **GA 2026-02-23**. Voice **GA** (date disputed — see above). SIP routing and Mobile SDK **GA** Summer '26. Voice for Digital Channels **GA** Q2 2026. Global languages **Beta**. Region-limited to US/Canada as of early 2026. Now written up at [02-salesforce-ai/12-voice-and-contact-center](../02-salesforce-ai/12-voice-and-contact-center/notes.md).

**Sources:** [Agentforce Voice overview (developer guide)](https://developer.salesforce.com/docs/ai/agentforce-partner/guide/agentforce-voice-overview.html) · [Enterprise Connect 2026: Salesforce Launches Agentforce Contact Center (UC Today)](https://www.uctoday.com/unified-communications/salesforce-agentforce-contact-center/) · [Agentforce Contact Center brings native CCaaS to Salesforce (TechTarget)](https://www.techtarget.com/searchCustomerExperience/news/366639947/Agentforce-Contact-Center-brings-native-CCaaS-to-Salesforce) · [Agentforce Voice Agent Setup: From Prerequisites to Talking with the Agent (ABSYZ)](https://www.absyz.com/agentforce-voice-agent-setup-in-salesforce-from-prerequisites-to-talking-with-the-agent/) · [Meet Agentforce Voice (Trailhead)](https://trailhead.salesforce.com/content/learn/modules/agentforce-voice-quick-look/meet-agentforce-voice)

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
