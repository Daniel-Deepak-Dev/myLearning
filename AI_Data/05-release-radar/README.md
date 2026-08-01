# 05-release-radar — Salesforce AI / Agentforce / Data 360 updates

**What this is:** a running log of Salesforce technical updates worth knowing as an AI-Salesforce architect. Fed by the `daily-agentforce-updates` scheduled task, which writes to the contract in [Writing contract](#writing-contract) below.

**How it's organized — two layers, one of them primary.**

- **Topic files** sit at the root of this folder and are **the layer to learn from**. Each holds the *running story* of one subject — dated entries newest-first, so a topic reads as a narrative over time. Every entry carries **What changed / Why it matters / Gotchas / Study action / Status / Sources**. They stay at the root deliberately: most cut across areas (developer tooling covers both Agentforce and Data 360; pricing covers both), so filing them under one area would lose information.
- **Dated scan notes** live in three **area folders** — [`01-agentforce/`](01-agentforce/), [`02-data-cloud/`](02-data-cloud/), [`03-salesforce-ai-research/`](03-salesforce-ai-research/). One `YYYY-MM-DD.md` per area per scan, and they are **audit logs, not write-ups**: what window was checked, what changed and which topic file it went into, and named verified negatives. A quiet day should read as a quiet day, not as a missed scan.

**How to read it:** skim this README for the current state of play → open the topic file for the subject you care about → use the dated notes only when you need to know *when* something was recorded or what a scan checked.

> Notes dated 2026-07-26 → 2026-07-30 predate this contract and are full write-ups. They are left as-is; the routine rewrites entries into the contract shape as it touches them.

## Areas — dated scan notes

| Folder | Covers | Latest |
|---|---|---|
| [01-agentforce/](01-agentforce/) | Agentforce platform, builder and Agent Script, developer tooling, governance, pricing | [2026-08-01](01-agentforce/2026-08-01.md) · [07-31](01-agentforce/2026-07-31.md) · [07-30](01-agentforce/2026-07-30.md) · [07-29](01-agentforce/2026-07-29.md) · [07-28](01-agentforce/2026-07-28.md) · [07-27](01-agentforce/2026-07-27.md) · [07-26](01-agentforce/2026-07-26.md) |
| [02-data-cloud/](02-data-cloud/) | Data 360 (ex-Data Cloud): ingestion, modeling, grounding, zero-copy, semantic layer | [2026-08-01](02-data-cloud/2026-08-01.md) · [07-31](02-data-cloud/2026-07-31.md) · [07-30](02-data-cloud/2026-07-30.md) · [07-29](02-data-cloud/2026-07-29.md) · [07-28](02-data-cloud/2026-07-28.md) · [07-27](02-data-cloud/2026-07-27.md) · [07-26](02-data-cloud/2026-07-26.md) |
| [03-salesforce-ai-research/](03-salesforce-ai-research/) | Salesforce AI Research: benchmarks (CRMArena, SCUBA, GIFT-Eval), open models, agent-lifecycle tooling | [2026-08-01](03-salesforce-ai-research/2026-08-01.md) · [07-31](03-salesforce-ai-research/2026-07-31.md) · [07-30](03-salesforce-ai-research/2026-07-30.md) · [07-29](03-salesforce-ai-research/2026-07-29.md) · [07-28](03-salesforce-ai-research/2026-07-28.md) · [07-27](03-salesforce-ai-research/2026-07-27.md) · [07-26](03-salesforce-ai-research/2026-07-26.md) |

## Topic files — the running story

| File | Covers |
|---|---|
| [agentforce-platform.md](agentforce-platform.md) | Agentforce Builder, Agent Script, Multi-Agent Orchestration, Voice, Contact Center, mobile SDK, observability |
| [data-360.md](data-360.md) | Data 360 (ex-Data Cloud): SOQL changes, Code Extension, Intelligent Context, semantic layer, zero-copy |
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | Hosted MCP servers, Headless 360, **MuleSoft Agent Fabric**, **ADLC workflow**, Apex/LWC changes, CLI, Agentforce Vibes, Agent Skills |
| [trust-security-and-governance.md](trust-security-and-governance.md) | Einstein Trust Layer, user-mode defaults, SOAP login retirement, secrets handling |
| [pricing-and-certification.md](pricing-and-certification.md) | Flex Credits, pay-per-resolution, Agentforce Specialist exam changes |

## State of play — as of 2026-08-01

Five things define the current Salesforce AI landscape. If you only retain five, retain these.

1. **Headless 360 is the organizing theme of Summer '26.** Every major Salesforce capability is now reachable as an API, an MCP tool, or a CLI command — by a human, an app, or an autonomous agent. Salesforce-hosted MCP servers are GA.
2. **Agent Script + the new Agentforce Builder are GA**, and from the week of **July 13, 2026** the *New Agent* button no longer opens the legacy builder. Agent Script is also **open source** (Apache 2.0). Learning it is no longer optional.
3. **Data Cloud is now Data 360** — a real rename (SKUs, release notes and the consultant cert all use it), and a reframing from CDP/warehouse into the *context engine* that grounds agents. Its developer surface grew a lot: `SET OPTIONS` in SOQL, Python Code Extensions, a Data 360 MCP server.
4. **Security defaults flipped.** At API 67.0, Apex DML/SOQL run in **user mode** by default and classes default to **`with sharing`**. `WITH SECURITY_ENFORCED` no longer compiles. Expect real migration work in older codebases.
5. **Commercials moved to consumption.** Flex Credits ($500 / 100k credits, ~$0.10 per action) is the recommended model, and the new Help Agent introduced **pay-per-resolution** at $2 per autonomous resolution — billed on outcomes, with consumption unmetered during the interaction.

**Newest additions (scan of 2026-08-01, 12:18 UTC second pass):** the 24-hour window was **dry** — nothing shipped in `agentforce-adlc`, `agentscript`, `sf-pi` or `sf-skills` since the 03:19 pass — so this run spent itself on **routing**, which is where the value turned out to be. Three findings. First, a routing audit found **substance stranded in ephemeral dated notes**: the **Databricks ↔ Data 360 Unity Catalog file sharing** distinction — *inward* file sharing versus *outward* zero-copy, the pair people reverse in design reviews — had sat only in a 07-27 scan note, and the **Data 360 MCP Server was written up twice** in two topic files with the copies disagreeing. Both now have one canonical home per the contract's tie-breaker, and `agentforce-platform.md`'s broken newest-first ordering is repaired. Second, the 03:19 pass's own output was **rewritten into contract shape** — ~4,000 words of `sf-skills` 1.33.0, dual-licence and `agentforce-observe` substance moved out of the dated notes and into `developer-tooling-and-apis.md`, `pricing-and-certification.md` and `data-360.md`, where it can be learned from. Third, a **Data 360 gap check turned up three Summer '26 features absent from the entire study base** — *Currency Reporting*, *Result Reuse for Data 360 Live*, and a no-code *semi-join / anti-join* builder. They are named in the release notes but no detail is obtainable (`help.salesforce.com` is 403), and the semi-join item may belong to **CRM Analytics rather than Data 360** — its doc page ID is `analytics.bi_explorer_data_join.htm`. **Logged as an open question rather than written up:** a padded entry is worse than a recorded gap. One live increment: `gift-eval` gained **three more submissions (#184–#186, two from LG AI Research), all still open** — making the point that *submitted to* and *on* a leaderboard are different states. **The largest remaining structural gap: the Salesforce AI Research area has seven dated notes and no topic file**, so none of its findings are durable.

**Previous additions (scan of 2026-08-01, 03:19 UTC pass):** no Salesforce product announcement, press release or release-note change landed in the window — the fifth consecutive scan without one — but the repositories were busy. The headline is **`forcedotcom/sf-skills` 1.33.0** (July 31, 17:57 UTC): **10 new + 16 updated skills**, 2,393 files, led by **`service-helpagent-coordinate`**, the first skill dedicated to standing up a **Help Agent** — the product that went **GA in July '26** with pay-per-resolution pricing — via a guided four-checkpoint flow. Also new: three `service-digital-engagement-*` channel skills, three Experience Cloud front-end skills, and **`platform-sandbox-configure` at version 1.0**, which introduces an **`accessCheck`** metadata field declaring the org permission a skill needs (`ManageSandboxes`) — the sibling of the `cliTools` field added July 30. `agentforce-test` **0.8 now covers security testing explicitly** (OWASP LLM Top 10, red-teaming, prompt-injection, a security grade), and `agentforce-generate` **0.11 names `sf agent mcp`** for MCP server registration. This library releases **weekly, on Fridays**. **The most consequential finding is a licensing correction to the July 31 note:** the three `agentforce-*` skills are published in **two** public repositories from the same internal source — `SalesforceAIResearch/agentforce-adlc` under **CC BY-NC 4.0** (non-commercial, blocks client work) and `forcedotcom/sf-skills` under **Apache-2.0** since June 29, 2026 — at **identical versions with byte-identical frontmatter**. Same content, different licence: **the restriction attaches to the copy you took, not to the skill**, so prefer `forcedotcom/sf-skills` for anything commercial. Data 360 was **empty for the third consecutive scan**; the only relevant movement was `agentforce-observe` 0.8, the STDM/Data 360 session-trace skill, shipping inside that Agentforce release — a reminder that Data 360 practitioner surfaces increasingly ship under Agentforce labels. On research, **five external teams pushed results onto the GIFT-Eval leaderboard in a four-minute window on July 31** (PRs #179–#183, now 117 result sets), including one from **Google Cloud AI Research** — a competitor consenting to be ranked on Salesforce infrastructure. But **only one of the five declares `replication_code_available: "Yes"`**, and the leakage field is self-declared: treat a leaderboard position as a claim, not a result.

**Previous additions (scan of 2026-07-30):** the window is non-empty, and the lead item is the first thing in weeks that can **break a green pipeline tomorrow morning**. Between **20:21 and 22:22 UTC on July 29**, the DX Node library stack cut majors on one breaking change: **`@salesforce/core` 9.0.0, `@salesforce/source-deploy-retrieve` 13.0.0, `@salesforce/agents` 2.0.0** all now require **Node ≥ 22** and **drop Node 18 and 20** (both past EOL). That matters because **`@salesforce/agents` implements the `sf agent` command family** (`generate`, `test`, `preview`) and **SDR is the engine behind `sf project deploy`** — so it sits under agent testing *and* under every metadata deploy, **Data 360 metadata included**. The break is quiet, not loud: npm installs on Node 20 with only an `EBADENGINE` warning, then fails later in ways that look like metadata problems. **Check CI images, not laptops** — installer/tarball `sf` bundles its own Node (v24 since February 2026) and is insulated; `npm install -g @salesforce/cli` and `actions/setup-node` pinned to 18/20 are not. Also shipped: **`sf-pi` v0.250.0/v0.251.0** added **native Agent Script quality analysis** — an **18-rule catalogue where High findings block publication** — and the design detail worth stealing, **release evidence that expires on identity rather than on time** ("valid while the exact org, `BotVersion`, baseline identity and suite digest are unchanged"); and **`@salesforce/react-native-agentforce` 0.3.0** reached npm (voice for Service Agents, configurable silence timeout, `UIDelegate` event bridge, native SDKs at the 262.1 line). Two **open, unmerged** PRs are worth knowing but not relying on: an **Agent Script "doctor"** in `agentforce-adlc` ([#46](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/46)) whose **six named anti-patterns** — misleading pipe-text indentation, fake step sequencing, ungated actions, turn-ending setters, stale state, competing side-effect owners — are a review checklist you can apply today with no tooling; and a **GIFT-Eval leaderboard submission** ([#182](https://github.com/SalesforceAIResearch/gift-eval/pull/182)) whose real lesson is the **submission protocol**: 98 fixed configurations, a declared **test-data-leakage flag printed beside every result**, and a required replication link. On Data 360: **no product news for the fifth consecutive scan**, but the **Python `salesforce-cdp-connector` is deprecated** with its replacement `salesforce-datacloud-connector` still at **2.0.0b1 beta** and no GA date — and a Salesforce reference app ([`next-gen-wealth`](https://github.com/salesforce/next-gen-wealth)) added **fail-safe messaging to its Data 360-grounded prompt templates**, which is the standing question to ask of every template you write: *what does this say when its grounding returns nothing?* Two method notes: an **org-wide OSPO CODEOWNERS sweep on July 29** makes many repositories look freshly updated and means nothing technically, and `arxiv.org`/`huggingface.co` both returned **403**, so "no new paper" is well-supported for GitHub artifacts and weaker elsewhere.

**Previous additions (scan of 2026-07-29):** the empty-window streak broke. **`agentforce-adlc` merged five pull requests on the evening of July 28** (21:48–22:50 UTC) — and note the correction this forces on yesterday's entry below: that scan reported "no commits since July 24" and debunked the repo's July 28 timestamp as stale metadata. **That was right when checked and wrong hours later.** A negative finding carries a timestamp. The consequential change is a **removal**: the **`/agentforce-secure` skill is deleted**, folded into `/agentforce-test` as **Mode C**. The old suite hard-coded **57 OWASP LLM Top 10 cases around Salesforce-the-vendor** — pointed at an airline complaint agent it asked about Salesforce security bulletins while never testing rebooking-without-verification. Mode C instead **generates cases from the agent's own Agent Script and inferred business domain**, and flips the default to **simulate-unless-`--live-actions`**, with `C1-run` refusing non-sandbox orgs. Also merged: a hook that **blocks `DELETE` without `WHERE` in quoted SOQL** (the LLM-authored-dynamic-SOQL risk), **hooks now gated to Salesforce projects only** (they previously fired in every repo), an **MCP server registry management** skill, and **eight voice latency anti-patterns plus seven voice-safe action rules** — of which *look up internal IDs rather than asking for them* is the one that decides whether an action is usable by voice at all. On research, **AnchorBench** landed publicly on **July 27** — long-horizon persona stability over **85–130 sessions**, and its findings transfer straight to long-lived service agents: **user-state changes are recalled at chance (~0.25)**, **no memory setting wins** (0.430–0.459), and **emotional vulnerability exposes more failures than explicit attacks**. Its paper is **not on arXiv**; the repo README is the only source. Data 360 was **empty for the fourth consecutive scan** — gap-fill covers the **Data 360 MCP Server** (Developer Preview, ~200 REST operations behind three facade tools), distinct from Headless 360 and one maturity step behind it.

**Previous additions (scan of 2026-07-28):** the 24-hour and 72-hour windows were **both empty across all three areas** — the third consecutive empty 24h window — so this scan again went after **verified gaps**. The largest was a flagship product this radar had never recorded at all: **Agentforce Coworker**, announced **May 21, 2026** and **in Beta for all Agentforce customers** since. It puts an agent in the search bar — Salesforce's and Slack's today, Teams/ChatGPT/Claude later this year — and it **inverts the year's pattern**: you author nothing, so what it can answer is decided entirely by the org's sharing model. Enabling it is an instant org-wide sharing audit. Two things to hold onto: the widely-repeated **"270+ data sources" is marketing** — the Beta docs list **three** (CRM, Data 360 objects, Slack), with Drive/SharePoint/Jira pilot-only — and **seat-based licences search CRM and Slack for zero credits**. Full write-up in [02-salesforce-ai/10-agentforce-coworker](../02-salesforce-ai/10-agentforce-coworker/notes.md). The gap with a live deadline: **July 24, 2026 was the last day to register** for the **24 certifications retiring February 1, 2027**, and the **last day to sit one is August 31, 2026**; separately, **16 certifications were renamed on July 24** with *Agentforce* replacing the old cloud branding (cosmetic — your Trailblazer profile updated itself, your CV and LinkedIn did not). On Data 360, three Summer '26 status changes were missing from the radar: **Accelerated Data Ingest is GA** (real-time CRM data, no pipeline lag — this kills the most common "stale grounding" failure), **AWS Glue federation is GA**, **Microsoft Fabric OneLake federation is only Beta**, plus **SQL from Apex** and IdP auth on the Databricks connector. On the research side, two benchmarks were never captured: **MFCL Audio** (voice function calling, 6.2K tasks, presented at **ICML 2026**, July 6–11, Seoul) and **LoCoBench-Agent** (long-context software engineering, 8,000 scenarios, 10K–1M tokens). Note one debunked signal: `agentforce-adlc` shows "updated July 28" on GitHub, but `main` has **no commits since July 24** and **no releases at all** — repository metadata, not code. _(**Superseded by the 2026-07-29 scan.** This was accurate when checked; five PRs then merged at 21:48–22:50 UTC on July 28, after that scan ran. The stale-metadata reasoning was sound — the conclusion simply expired.)_

**Second pass (2026-07-28, structural):** a follow-up question — *are any Agentforce topics missing?* — produced the largest single correction to this radar's coverage so far, and **not a news item**: the empty windows above were independently re-confirmed. Grepping the whole study base found four parts of the 2026 Agentforce surface that had never been captured. The worst was **MuleSoft Agent Fabric** — **zero mentions repo-wide, radar included**, despite launching **September 2025**. It's the control plane for agents you *didn't* build: **Agent Registry** (federated — registries reference each other), **Omni Gateway** (policy on every A2A and MCP call), **Agent Broker** (graph routing; networks declared in YAML), **Agent Visualizer**. Scanners for **Agentforce, Bedrock, Vertex AI and Copilot Studio** went **GA January 2026**; **guided determinism** landed **April 15, 2026**. The distinction to hold: **Agentforce orchestration coordinates agents inside one org; Agent Fabric coordinates agents across vendors.** Second, **Agentforce Voice and Contact Center** had one passing bullet between them despite **Contact Center being GA since 2026-02-23** — and voice carries three project-deciding facts: **US/Canada only** as of early 2026, **two billing models** (30 credits/action *or* ~60 credits/min, a 3× swing on a five-minute call), and **escalation prerequisites that live outside Agentforce**. Third, the **ADLC** now has a first-party command sequence (`sf agent generate` → `preview` → `test` → `publish` → `activate`) driven by three Agent Skills — and a licence distinction that matters commercially: `sf-skills` is supported, **`agentforce-adlc` is CC BY-NC 4.0 and unusable on client work**. Fourth, **prebuilt agents** (Help Agent, Commerce, IT Service, Missionforce) had no buy-vs-build framework anywhere. Two vocabulary traps recorded: **Flex Gateway was renamed Omni Gateway** (cosmetic, non-breaking), and **"Agent Script" names two different products**. Full write-ups in [02-salesforce-ai](../02-salesforce-ai/INDEX.md) topics **11–14**; the pass itself is documented in [01-agentforce/2026-07-28.md](01-agentforce/2026-07-28.md).

**Previous additions (scan of 2026-07-27):** the 24-hour window was empty and the 72-hour window produced nothing beyond the previous scan, so this scan went after **verified gaps** instead. Four of them matter. **Agentforce Commerce went GA on July 6, 2026** — Shopper, Buyer and Merchant agents, with **native ChatGPT selling** (catalogue synced straight from Business Manager, checkout kept on the merchant's own site). **Data 360 pricing was rebuilt on March 2, 2026** around a **profile-based SKU (~$240 per 1,000 profiles)**, with Data 360 folded into the **shared Flex Credits pool** and Tableau usage un-metered — which makes identity-resolution quality a direct cost lever. **Multi-Agent Orchestration is GA (June 15, 2026), not Beta** — the radar had it wrong, now corrected, and **Atlas Reasoning Engine 3.0 routes on subagent descriptions**, making that field executable configuration. And Salesforce AI Research was genuinely **silent July 24–27**: `agentforce-adlc` has had no commits since July 24.

**Previous additions (scan of 2026-07-26):** Salesforce AI Research is shipping [`agentforce-adlc`](https://github.com/SalesforceAIResearch/agentforce-adlc) — Claude Code skills covering the whole agent lifecycle in Agent Script, with voice support merged July 23 — and the **Headless 360 MCP Server** hit Beta with ~100 admin-facing *skills* rather than thousands of flat tools. On July 24 the VA awarded Salesforce a **$1.6B "Agentic Enterprise License Agreement"**, a third commercial model alongside Flex Credits and pay-per-resolution.

## Open questions to chase

- **Three Summer '26 Data 360 features are named in the release notes and absent from this entire study base** — *"Gain Accurate Financial Insights with **Currency Reporting** in Data 360"*, *"Improve Dashboard Responsiveness with **Result Reuse for Data 360 Live**"*, and a no-code **semi-join / anti-join** builder (*"identify duplicate and non-matching rows without coding"*, GA in Summer '26 after Beta in Winter '26). No technical detail is obtainable because `help.salesforce.com` is 403. **Caveat on the third:** its documentation page ID is `analytics.bi_explorer_data_join.htm`, suggesting it may be a **CRM Analytics Data Explorer** feature rather than Data 360 — and SOQL semi-joins/anti-joins (`IN` / `NOT IN` subqueries) have existed for years, so search results are conflating three distinct things. **Open the release notes in a browser and settle all three.** Currently the highest-value Data 360 question. _(Raised 2026-08-01.)_
- **The Salesforce AI Research area has seven dated notes and no topic file**, so nothing it finds is durable — GIFT-Eval's submission protocol, AnchorBench, MFCL Audio, LoCoBench-Agent and CRMArena live only in ephemeral scan notes. The [Writing contract](#writing-contract) names five topic files and none fits research. **Decide: add a sixth (`ai-research-and-benchmarks.md`), or route research findings into the existing five by consequence.** Until then `03-salesforce-ai-research/` notes are exempt from the ≤25-line cap. _(Raised 2026-08-01.)_
- **Winter '27** release notes aren't public yet; Release Update *enforcement* starts September 2026. Watch what gets enforced. Sandbox preview is expected around **August 29, 2026**, so preview notes should land within weeks — the most likely source of the next substantial radar entry.
- **Agentforce Coworker GA** — Beta since May 21, 2026 with **no announced GA date**, and no word on whether the pilot sources (Google Drive, SharePoint, Jira) reach Beta first. Also unconfirmed: the "later this year" ship dates for the Teams, ChatGPT, Claude and desktop surfaces. Re-check before it goes near a delivery commitment.
- **Context Indexing GA** — reported in June 2026 as expected "later in July 2026", but no confirmation found as of 2026-07-28. Status open; re-check against the monthly Data 360 release notes.
- **Agent Broker's real status** — launch coverage puts it **GA October 2025**; coverage of the April 2026 Agent Fabric expansion describes a **Beta from April 2026**. Likely reconciliation: base Broker GA, guided determinism in Beta — but that's inference. Also unresolved: what Agent Fabric costs and which MuleSoft entitlement it needs. **No public pricing found.**
- **The official Agentforce Specialist domain weights** — third-party resources report **Multi-Agent Interoperability at 15%** and a **Development Lifecycle & Observability domain at 15–20%**, against the ~5% and no-such-domain figures this radar recorded on July 26. Sources conflict; the official guide couldn't be read first-party. **If the higher numbers hold, ~30% of the exam sits in two areas the study plan treated as peripheral.** Read the official PDF and settle it — this is the highest-value open question here.
- **Agent Script in the Agentforce Specialist exam** — it became the default authoring model in July 2026 but isn't named in the exam guide. Assume implicit scope; re-check before booking.
- **Exact Agentforce Builder / Agent Script GA date** — no first-party announcement located; secondary sources conflict between February 2026 and the Summer '26 cadence. The July 13, 2026 legacy-builder cutoff is confirmed.
- **`salesforce-datacloud-connector` GA** — the Python Data 360 client v2 has been at **2.0.0b1 beta since June 2, 2026** with no announced GA date, while **v1 (`salesforce-cdp-connector`) is deprecated with removal tied to that GA**. Re-check before writing either into anything long-lived.
- **Fin acquisition** — Salesforce signed a definitive agreement to acquire Fin (announced June 15, 2026; expected to close Q4 FY27), an SMB-focused autonomous service agent platform used by 30,000+ companies. Watch how it lands relative to the Help Agent.

---

## Writing contract

The `daily-agentforce-updates` routine writes to this contract. It lives here rather than in the prompt so the rules travel with the repo.

### Routing — one canonical home per item

Write the full entry in exactly one topic file. Other topic files may carry a one-line cross-link, never a copy.

| Subject | Canonical file |
|---|---|
| Builder, Agent Script, orchestration, Voice, Contact Center, mobile SDK, observability, Coworker, prebuilt agents | [agentforce-platform.md](agentforce-platform.md) |
| Data 360 ingestion, modeling, grounding, SOQL, Code Extensions, connectors, zero-copy, semantic layer | [data-360.md](data-360.md) |
| MCP servers, Headless 360, Agent Fabric, ADLC, `sf` CLI, npm libraries, Apex/LWC, IDEs | [developer-tooling-and-apis.md](developer-tooling-and-apis.md) |
| Trust Layer, execution modes, sharing, auth retirements, secrets, Release Update enforcement | [trust-security-and-governance.md](trust-security-and-governance.md) |
| Flex Credits, pay-per-resolution, ELAs, certifications, acquisitions | [pricing-and-certification.md](pricing-and-certification.md) |

**Tie-breakers.** MCP servers route to `developer-tooling-and-apis.md` even when Data-360-specific — `data-360.md` gets the cross-link. A licence, price or exam-scope fact about a tool routes to `pricing-and-certification.md`; the tool itself stays in its own file.

### Topic-file entry — the primary deliverable

```markdown
## YYYY-MM-DD · <Title — names the thing, no marketing verbs>

**What changed.** <the fact, ≤60 words>

- **<Bolded lead label>.** <detail>
- **<Bolded lead label>.** <detail>

**Why it matters.** <2–4 sentences: the practitioner consequence, not a restatement of the fact.>

**Gotchas:**
- <the trap, with the exact identifier that triggers it>

**Study action:** <one concrete thing to do in a dev org, a repo or the CLI.>

**Status:** GA / Beta / Pilot / Developer Preview / Announced / Open source — plus the release and date.

**Sources:** [Title](url) · [Title](url)
```

Rules:

- **No paragraph over ~60 words.** Any inline enumeration — "four skills:", "Three concrete things", "(1)…(2)…(3)" — becomes a list.
- **`**Why it matters.**` is a fixed literal string.** Not "why it's worth your time", not "what it means practically". It has to stay greppable.
- **`**Study action:**` is mandatory on every entry.**
- **`**Gotchas:**` is mandatory when the item has an API, CLI, metadata type, permission set or config surface**, and identifiers must be exact. The bar is the Data Library entry: treat the library as ready when `retrieverId` goes non-null, not when `status` flips; `rag_feature_config_id` is `"ARFPC_" + libraryId`.
- **Mermaid diagrams belong here**, not in a scan log. Use one for a flow, a routing decision or a dependency graph.
- **A negative finding carries a timestamp.** "No commits since July 24" was true when checked on 07-28 and false hours later.

### Write discipline

- **New entry** → append at the top. Every topic file reads newest-first.
- **Status change to an existing entry** → mutate in place and prepend `> **Correction (YYYY-MM-DD):** <what this said before, what it is now>`.
- **Never bump an existing heading's date.** That is what put a 07-27 entry between two 07-26 entries in `agentforce-platform.md`.
- **Never delete a superseded claim** — supersede it visibly.
- Touching several topic files in one run is normal; top-appending in all of them at once is what caused the merge conflict in `bbff18a`, so commit once per run.

### Dated scan note — an audit log, not a write-up

Target ≤25 lines. No table of contents. No `## What this scan did not find` essay. No `**Status:** N/A — scan record`.

```markdown
# <Area> — <Month D, YYYY>

**Window:** <UTC range> (24h / extended to 72h) · **Checked:** <sources>

## What changed
- **<Item>** → [agentforce-platform.md](../agentforce-platform.md#anchor) — <one line>

## Verified negatives
- `salesforce/agentscript` — newest `main` commit 2026-07-24, "<subject>", checked <UTC time>
```

A verified negative names the artifact and when it was checked. Anything vaguer is omitted, not padded.

### Standing notes — do not restate these in dated notes

- `salesforce.com`, `salesforceben.com`, `arxiv.org` and `huggingface.co` return **403** to automated fetching. Use search-result snippets and secondary coverage; a negative from these sources is weaker than one from GitHub.
- An **org-wide OSPO CODEOWNERS sweep on 2026-07-29** makes many Salesforce repositories look freshly updated. Repository metadata is not code — check commits.
- The three `agentforce-*` skills ship from one internal source into two public repos at identical versions: `SalesforceAIResearch/agentforce-adlc` (**CC BY-NC 4.0**, blocks client work) and `forcedotcom/sf-skills` (**Apache-2.0**). The restriction attaches to the copy you took — prefer `sf-skills` for anything commercial.

### Feeding the study base

- New jargon defined in an entry → the right alphabetical section of [GLOSSARY.md](../GLOSSARY.md).
- Each scan adds strict `Q:` / `A:` pairs to the relevant `../02-salesforce-ai/NN-topic/flashcards.md`.
- An item big enough to be its own subject (a product or capability with its own surface, not a version bump) → next-numbered `NN-kebab-case` folder in [02-salesforce-ai](../02-salesforce-ai/INDEX.md) from `../_templates/`, update that INDEX, and link it from the radar entry with a `**Study folder:**` line.

### Coverage, staleness and the weekly pass

- **Every run** reports the last-touched date of all five topic files. Anything untouched **>14 days** gets a gap check that run. `trust-security-and-governance.md` went 8 commits with zero updates before anything noticed.
- **Weekly (first run on or after Sunday):** rewrite *State of play*, prune resolved *Open questions* and add new ones, refresh the areas-table `Latest` column and the footer date, and reconcile any item that has landed in two topic files.

## Coverage and staleness — 2026-08-01

| Topic file | Last touched *before* this run | Age | Touched this run |
|---|---|---|---|
| [agentforce-platform.md](agentforce-platform.md) | 2026-07-30 | 2d | ✅ mobile version-line gotchas; heading order repaired |
| [data-360.md](data-360.md) | 2026-07-30 | 2d | ✅ two new entries; MCP duplicate reconciled |
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | 2026-07-30 | 2d | ✅ `sf-skills` 1.33.0; MCP entry consolidated |
| [trust-security-and-governance.md](trust-security-and-governance.md) | 2026-07-26 | **6d** | — no security or governance change in window |
| [pricing-and-certification.md](pricing-and-certification.md) | 2026-07-30 | 2d | ✅ the dual-licence rule for the `agentforce-*` skills |

**No topic file exceeded the 14-day gap-check threshold.** `trust-security-and-governance.md` is the oldest at 6 days — worth watching, given it once went eight commits with zero updates. The real coverage hole is not a stale file but a **missing one**: see the research-topic-file question above.

---

---

_Last updated: 2026-08-01 · Sources are linked inline in each topic file._
