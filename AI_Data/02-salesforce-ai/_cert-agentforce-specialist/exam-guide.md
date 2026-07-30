# Salesforce Certified Agentforce Specialist — Exam Guide Breakdown

- Validates: building, configuring, and deploying Agentforce agents and prompt templates.
- Roadmap milestone: end of Phase 03 (week 14), alongside one working agent with a custom Apex action in a dev org.
- Official exam guide: https://trailhead.salesforce.com/credentials/agentforcespecialist
- Prep module: https://trailhead.salesforce.com/content/learn/modules/cert-prep-agentforce-specialist/get-started-with-salesforce-agentforce-specialist-certification-prep

## The exam was restructured — this is the important part

The exam was **significantly restructured** in the revision announced October 2025, redesigned around **how agents think, interact and collaborate** rather than the older emphasis on configuration and prompt building.

**What changed:**

- **A new AI Agents domain** replaces the older Agentforce Concepts, Service Cloud and Sales Cloud sections. The Service Cloud and Sales Cloud sections were **retired outright**; relevant material folded into AI Agents.
- **A new Multi-Agent Interoperability section**, weighted around **5%** — covering the **Model Context Protocol (MCP)**, the **Agent-to-Agent (A2A) protocol**, and the **Agent API**.
- **More weight on deterministic behaviour**, filters and variables, plus how agents connect to channels like email and Slack.

**Why the 5% matters more than 5% sounds:** MCP and A2A moved from "adjacent Claude topic" to "examinable Salesforce topic". The hosted-MCP work in the [capstone](../../04-capstone/01-mcp-server-salesforce/notes.md) serves this exam *and* the CCA-F.

> ⚠️ **The ~5% figure is now in doubt — and if it's wrong, the advice that used to sit here inverts.** This section previously concluded that at ~5% interoperability was "a welcome overlap, not a reason to reallocate serious study time." Several 2026 study resources instead report **Multi-Agent Interoperability at 15%**, and a **Development Lifecycle and Observability** domain worth **15–20%** that this file didn't list at all. If those numbers are right, MCP/A2A/Agent API is a **primary** study target and the lifecycle material is too. **Do not plan study time off this table until the official guide is read** — see the domain table below.

**Also worth noting:** Agentforce content has been added to the **Salesforce Administrator** exam. The topic is no longer a specialist silo.

## Open question — Agent Script

**The exam guide doesn't explicitly name Agent Script**, despite it becoming the default authoring model in July 2026 (the legacy builder stopped creating new agents the week of **July 13, 2026**).

Given the guide's new emphasis on **deterministic behaviour, filters and variables** — which is precisely what Agent Script is for — assume it's implicitly in scope. **Re-check the guide before booking**; Salesforce exam guides typically lag GA by a release or two.

## Retirement check — not affected

24 certifications retire February 1, 2027 (registration closed July 24, 2026; last sitting August 31, 2026). **Agentforce Specialist is not among them.** Separately, 16 certifications were *renamed* on July 24, 2026 with *Agentforce* replacing old cloud branding — cosmetic, and this exam's name was already current.

## Domains & weights

> 🚩 **UNVERIFIED — secondary sources conflict. Read the official guide before planning study time.**
>
> The official exam guide could not be read first-party during the 2026-07-28 research pass: the Trailhead credential page returns truncated content to automated fetching, and `salesforce.com` / `help.salesforce.com` return HTTP 403. Every weight below comes from third-party study resources, **and they disagree with each other**. Two competing readings are recorded side by side rather than averaged, because averaging would invent a number nobody published.

| Domain | Weight — reading A | Weight — reading B | Study folder |
|---|---|---|---|
| AI Agents _(new — absorbed Concepts / Service / Sales)_ | 30% | 35% | [02-agentforce-anatomy](../02-agentforce-anatomy/notes.md) · [07-agent-script](../07-agent-script/notes.md) |
| Prompt Engineering | 20% | 20% | [03-prompt-builder](../03-prompt-builder/notes.md) |
| Agentforce & Data Cloud / grounding | 20% | 20% | [08-rag-on-platform](../../01-data-cloud/08-rag-on-platform/notes.md) |
| **Development Lifecycle & Observability** 🆕 | **15%** | **20%** | [09-observability-and-testing](../09-observability-and-testing/notes.md) · [13-adlc-and-agentforce-dx](../13-adlc-and-agentforce-dx/notes.md) |
| **Multi-Agent Interoperability** | **15%** | **~5%** | [08-multi-agent-orchestration](../08-multi-agent-orchestration/notes.md) · [11-agent-fabric-and-interop](../11-agent-fabric-and-interop/notes.md) · [MCP](../../03-claude-cca/05-mcp/notes.md) |

**Both readings sum to exactly 100%** (A: 30+20+20+15+15 · B: 35+20+20+20+5). That's the uncomfortable part — neither is a garbled half-memory of the other, so both are plausibly real published breakdowns, possibly from **different exam revisions**. Which makes guessing worse, not better: pick wrong and you under-prepare a 15% domain by a factor of three.

**A third, older breakdown also circulates** — Prompt Engineering 30% / Agentforce Concepts 30% / Data Cloud 20% / Service Cloud 10% / Sales Cloud 10%, labelled "Spring '26". That one contradicts the documented retirement of the Service Cloud and Sales Cloud sections, so treat it as stale rather than as a third opinion.

**What is *not* in doubt:** 60 questions, 105 minutes, **73% to pass**, $200 (retake $100). Trust & security is examinable via the [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) but wasn't named as a standalone domain in any breakdown found — it's likely folded into AI Agents.

**Multi-Agent Interoperability names three things explicitly:** **MCP** (connecting agents to external systems and data), **A2A** (agents exchanging context, delegating tasks, coordinating responses), and the **Agent API** (REST access so external systems or websites talk to an agent directly). Learn all three by name.

## Vocabulary warning

Most Agentforce material online — including a lot of video content — still teaches **topics, actions and instructions** as the current authoring model. It is **legacy**. Check the publication date on anything you study, and see [Agentforce anatomy](../02-agentforce-anatomy/notes.md) for the legacy-vs-current comparison.

Likewise, **Einstein Copilot** is a historical name. A source using it as current product predates mid-2025.

## Summer '26 material likely to appear

- **Agent Script** and the new Agentforce Builder — the July 13, 2026 cutoff
- **Atlas Reasoning Engine 3.0** — routes on subagent descriptions
- **Multi-Agent Orchestration** — GA June 15, 2026 _(note: Help still labels the in-builder step Beta — verify in-org)_
- **Model choice** — Anthropic, OpenAI, **Gemini**; per-agent pinning
- **API 67.0 security** — user mode default, `with sharing` default, `WITH SECURITY_ENFORCED` retired, no-arg constructor rule
- **Hosted MCP servers GA** — standard and custom; custom respects org sharing
- **Observability** — Refined Agent Analytics, Custom Scorers (Beta), `aiAgentScorerDefinitions`
- **Flex Credits** — billed per action (~$0.10), not per conversation
- **ADLC** — the five phases, inner vs outer loop, `sf agent` commands ([13-adlc-and-agentforce-dx](../13-adlc-and-agentforce-dx/notes.md)) — likely scope if the lifecycle domain is real
- **MCP · A2A · Agent API** by name, and where **Agent Fabric** sits relative to in-org orchestration ([11-agent-fabric-and-interop](../11-agent-fabric-and-interop/notes.md))
- **Voice** — a voice action costs 30 credits vs 20, and voice is region-limited ([12-voice-and-contact-center](../12-voice-and-contact-center/notes.md))

## Registration / logistics
<!-- exam date booked, delivery method, cost, retake policy -->

## Prep loop

1. **Settle the domain table first.** Download the official exam guide PDF from the credential page, replace the two-reading table above with the real weights, and confirm whether Agent Script is now named. Everything below depends on which reading is true — under reading A, interoperability and lifecycle are **30% combined**.
2. Work topics 01–09 in this track in order; add [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) from the Data 360 track, then topics **11–14** for the lifecycle and interoperability domains.
3. Build one real agent in Agent Script with a custom Apex action — the milestone and the best revision.
4. Mock exam → log every miss in [practice-questions.md](practice-questions.md) **with the reason**.
5. Update [weak-areas.md](weak-areas.md) after each mock.
