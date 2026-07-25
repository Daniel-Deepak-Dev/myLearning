# Pricing and certification

Commercial model and exam changes — the two things clients and recruiters ask about that aren't in the release notes.

---

## 2026-07-26 · Agentforce Flex Credits — the consumption model

**Headline numbers** (verify against a current quote before using in a proposal — public pricing moves):

| Item | Cost |
|---|---|
| Flex Credits | **$500 per 100,000 credits** |
| Standard action | 20 credits (~$0.10) |
| Voice action | 30 credits (~$0.15) |
| Sandbox / Testing Center action | 16 credits (~$0.08) |

A single action costs about **$0.10**; a multi-step task costs a multiple of that, because **you pay per action, not per conversation**. That's the modelling trap — a "conversation" in a demo is one action, but a real resolution is often five to fifteen.

**Three buying structures:**

- **Pre-purchase** — buy a block up front
- **Pay-as-you-go** — no commitment, highest unit cost
- **PreCommit** — favourable pricing against a forecast; if usage falls below commitment at term end, a true-up charge covers the difference. Suits organisations with a credible usage forecast that don't want cash tied up.

Flex Credits covers **every** Agentforce use case — customer-facing agents, employee-facing agents, and Agentforce Voice — and as of early 2026 is the recommended model for most new deployments.

**Why it matters architecturally, not just commercially.** Cost is now a function of agent design. An orchestrator that routes through three subagents costs three times a direct hit. Chatty grounding loops cost real money. This is the first time Salesforce agent architecture has had a direct, legible unit economics consequence — and it's the question a CFO will ask first.

---

## 2026-07-26 · Pay-per-resolution (Agentforce Help Agent)

The new prepackaged Help Agent, GA July '26, introduces **pay-per-resolution** pricing — billed on outcomes rather than actions or conversations.

| Term | Detail |
|---|---|
| Price | **$2 per issue resolved autonomously end-to-end** |
| Human escalation | **No charge** |
| Negative feedback | **No charge** |
| Data 360 + Agentforce consumption during the interaction | **Unmetered** |

That last row is the one to remember: **pay-per-resolution does not stack on top of Flex Credits.** You are not billed twice for the same conversation.

**Why it matters.** It shifts delivery risk toward Salesforce and makes ROI arithmetic simple for a buyer ($2 vs. the fully-loaded cost of a human ticket — usually $5–$15+). Expect the model to spread. It also raises the stakes on grounding quality: an unresolved conversation earns Salesforce nothing, which is exactly why the Help Agent ships pre-tuned rather than as a blank canvas.

**Benchmarks for business cases:**

- **Salesforce's own** `help.salesforce.com` — **4.3 million inquiries, 70% resolved** by Agentforce. First-party, and the strongest number available.
- **Oviva** (European digital health) — **300,000+ inbound messages/month** handled autonomously, **half** of all inquiries deflected entirely, **40%** of operational support requests resolved without a human.

Deflection rates are heavily domain-dependent; use these as ceilings, not forecasts.

---

## 2026-07-26 · Agentforce Specialist certification restructured

The exam was **significantly restructured in the Summer '25-aligned revision** (announced October 2025) and redesigned around how agents think, interact and collaborate — away from the older emphasis on configuration and prompt building.

**What changed:**

- **New AI Agents domain** replaces the older Agentforce Concepts, Service Cloud and Sales Cloud sections. The Service Cloud and Sales Cloud sections were retired outright; their relevant material folded into the AI Agents domain.
- **New Multi-Agent Interoperability section** — appears for the first time, covering the **Model Context Protocol (MCP)**, the **Agent-to-Agent (A2A) protocol** and the **Agent API**. Weighted at roughly **5%** of the exam.
- **More weight on deterministic behaviour**, filters and variables, plus how agents connect to channels like email and Slack.

**Why it matters for the study plan.** MCP and A2A moved from "adjacent Claude topic" to "examinable Salesforce topic" — so the Hosted MCP Servers work in [developer-tooling-and-apis.md](developer-tooling-and-apis.md) serves both the [02-salesforce-ai](../02-salesforce-ai/INDEX.md) and [03-claude-cca](../03-claude-cca/INDEX.md) tracks. Keep the weighting honest though: at ~5% it's a nice overlap, not a reason to reallocate serious study time.

**Open question:** the exam guide doesn't explicitly name **Agent Script**, despite it becoming the default authoring model in July 2026. Given the emphasis on deterministic behaviour, filters and variables, assume it's implicitly in scope and re-check the guide before booking. Salesforce exam guides lag GA by a release or two.

**Also worth noting:** Agentforce content has been added to the **Salesforce Administrator** exam. The topic is no longer a specialist silo.

Official prep: [Agentforce Specialist Certification Prep on Trailhead](https://trailhead.salesforce.com/content/learn/modules/cert-prep-agentforce-specialist/get-started-with-salesforce-agentforce-specialist-certification-prep).

**Naming note:** the Data Cloud Consultant certification is now the **Salesforce Certified Data 360 Consultant** — update any bookmarks or study plans referring to the old name.

---

## 2026-06-15 · Salesforce to acquire Fin

Salesforce signed a definitive agreement to acquire **Fin**, an SMB-focused autonomous customer service agent platform used by 30,000+ companies. Expected to close **Q4 FY27**.

**Why it matters.** Read alongside the Help Agent and pay-per-resolution: Salesforce is buying into the low-touch, fast-deploy, outcome-priced end of the market rather than only serving enterprise buildouts. For consulting positioning, it signals that the "configure a support agent" work will get commoditized from below — the durable value stays in grounding, data architecture and multi-agent orchestration.

---

## Sources

- [Salesforce Agentforce Credits & Cost Model: Complete Guide 2026 (Jitendra Zaa)](https://www.jitendrazaa.com/blog/salesforce/salesforce-agentforce-credits-cost-model-complete-guide-2026/)
- [Agentforce Pricing Explained 2026 (Enterprise Dreamin')](https://enterprisedreamin.org/articles/agentforce-pricing-explained-2026/)
- [Salesforce Announces Prepackaged Agentforce Help Agent](https://www.salesforce.com/news/stories/agentforce-help-agent-announcement/)
- [3 Big Changes to the Salesforce Agentforce Specialist Certification (Salesforce Ben)](https://www.salesforceben.com/3-big-changes-to-the-salesforce-agentforce-specialist-certification-you-should-know/)
- [The Salesforce Agentforce Specialist Exam Has Evolved (FocusOnForce)](https://focusonforce.com/blog/agentforce-specialist-exam-update/)
- [Salesforce commits $1 billion to Switzerland to expand Agentforce deployments](https://www.marketscale.com/industries/software-and-technology/salesforce-commits-1-billion-to-switzerland-over-five-years-to-expand-agentforce-deployments)
