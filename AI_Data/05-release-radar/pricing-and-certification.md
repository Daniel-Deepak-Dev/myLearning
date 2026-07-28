# Pricing and certification

Commercial model and exam changes — the two things clients and recruiters ask about that aren't in the release notes.

---

## 2026-07-24 · Certification retirements and renames — two hard dates

**24 certifications retire on February 1, 2027.** Registration for those exams **closed July 24, 2026**; the **last day to sit one is August 31, 2026**. Passing before the deadline still counts — the credential stays on your Trailblazer profile permanently, flagged as retired from February 1, 2027, and remains valid evidence of knowledge. What it loses is **public verification**: retired credentials stop appearing on the public verification pages.

**16 certifications were renamed on July 24, 2026**, with *Agentforce* replacing the old cloud branding. Cosmetic only — no content change, no exam-code change, no retake. Trailblazer profiles updated automatically.

| Old name | New name |
|---|---|
| Sales Cloud Consultant | Agentforce Sales Consultant |
| Service Cloud Consultant | Agentforce Service Consultant |
| Data Cloud Consultant | Data 360 Consultant _(renamed earlier, 2026-03-27; exam code `Data-Con-101` unchanged)_ |

**Why it matters.** The rename doesn't touch your CV, LinkedIn or email signature — and recruiters search the new terms. Also read it as directional: Salesforce is aligning the credential catalogue with the Agentforce 360 portfolio, so expect exam *content* to drift toward agentic material at the next refresh.

Full list in Salesforce's Certification Name Changes FAQ. Sources: [Salesforce Ben — retiring 24 certifications](https://www.salesforceben.com/salesforce-is-retiring-24-certifications-heres-what-you-need-to-know/) · [Apex Hours — 2027 retirements](https://www.apexhours.com/salesforce-2027-certification-retirements-everything-you-need-to-know/) · [Salesforce Time — retirements and renames](https://salesforcetime.com/2026/06/10/salesforce-certification-retirements-and-renames-explained/) · [The Salesforce Certification Lifecycle](https://www.salesforce.com/blog/salesforce-certification-lifecycle/)

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

## 2026-07-27 · Data 360 pricing — profiles, pooled credits, free Tableau

_Effective **March 2, 2026**. Added on 2026-07-27 as a gap-fill; see [02-data-cloud/2026-07-27.md](02-data-cloud/2026-07-27.md) for the full write-up._

| Change | Detail |
|---|---|
| **Profile-based SKU** | **~$240 per 1,000 profiles** (baseline) · **~$420 per 1,000** (premium) — bundles essential Data 360 actions into a flat per-profile cost |
| **Data 360 joins Flex Credits** | Data 360 and Agentforce consumption now draw from **one pooled, fungible credit balance** |
| **Tableau usage un-metered** | Querying Data 360 from Tableau no longer burns credits |

A "profile" is a **unified individual after identity resolution**, not a raw source row — so you are billed on the *output* of your identity-resolution ruleset.

**Why it changes design, not just the invoice.** Credit metering rewarded processing less. Profile pricing rewards **resolving fewer, better profiles** — duplicates and under-matches now inflate a recurring bill directly, which puts money behind identity-resolution quality for the first time. Credit pooling removes the "is this the data team's cost or the AI team's cost?" argument that stalls grounding projects. Tableau un-metering is a deliberate nudge toward using Data 360 as the reporting substrate.

Verify against a live quote before any commercial use — public list pricing moves and varies by region.

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
