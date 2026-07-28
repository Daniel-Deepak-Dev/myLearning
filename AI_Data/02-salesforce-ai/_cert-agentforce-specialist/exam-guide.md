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

**Why the 5% matters more than 5% sounds:** MCP and A2A moved from "adjacent Claude topic" to "examinable Salesforce topic". The hosted-MCP work in the [capstone](../../04-capstone/01-mcp-server-salesforce/notes.md) serves this exam *and* the CCA-F. But keep the weighting honest — at ~5% it's a welcome overlap, not a reason to reallocate serious study time.

**Also worth noting:** Agentforce content has been added to the **Salesforce Administrator** exam. The topic is no longer a specialist silo.

## Open question — Agent Script

**The exam guide doesn't explicitly name Agent Script**, despite it becoming the default authoring model in July 2026 (the legacy builder stopped creating new agents the week of **July 13, 2026**).

Given the guide's new emphasis on **deterministic behaviour, filters and variables** — which is precisely what Agent Script is for — assume it's implicitly in scope. **Re-check the guide before booking**; Salesforce exam guides typically lag GA by a release or two.

## Retirement check — not affected

24 certifications retire February 1, 2027 (registration closed July 24, 2026; last sitting August 31, 2026). **Agentforce Specialist is not among them.** Separately, 16 certifications were *renamed* on July 24, 2026 with *Agentforce* replacing old cloud branding — cosmetic, and this exam's name was already current.

## Domains & weights
<!-- copy exact weights from the official exam guide -->

| Domain | Weight | Study folder |
|---|---|---|
| AI Agents _(new — absorbed Concepts / Service / Sales)_ | | [02-agentforce-anatomy](../02-agentforce-anatomy/notes.md) · [07-agent-script](../07-agent-script/notes.md) |
| Prompt Engineering | | [03-prompt-builder](../03-prompt-builder/notes.md) |
| Agentforce & Data Cloud / grounding | | [08-rag-on-platform](../../01-data-cloud/08-rag-on-platform/notes.md) |
| Trust & security | | [04-einstein-trust-layer](../04-einstein-trust-layer/notes.md) |
| **Multi-Agent Interoperability** | **~5%** | [08-multi-agent-orchestration](../08-multi-agent-orchestration/notes.md) · [MCP](../../03-claude-cca/05-mcp/notes.md) |
| _(fill remaining from the official guide)_ | | |

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

## Registration / logistics
<!-- exam date booked, delivery method, cost, retake policy -->

## Prep loop

1. Read the official guide, fill the domain table, and confirm whether Agent Script is now named.
2. Work topics 01–09 in this track in order; add [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md) from the Data 360 track.
3. Build one real agent in Agent Script with a custom Apex action — the milestone and the best revision.
4. Mock exam → log every miss in [practice-questions.md](practice-questions.md) **with the reason**.
5. Update [weak-areas.md](weak-areas.md) after each mock.
