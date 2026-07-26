# Salesforce AI Research and benchmarks

The research org behind Agentforce, and the benchmarks that say what agents can actually do. Newest entries at the top.

---

## Who they are, and why you should care

**Salesforce AI Research** (`SFResearch`) is separate from the product teams that ship Agentforce and Data 360. They publish papers, open-source models, and — most usefully for a practitioner — **benchmarks that measure where agents fail on CRM work**.

That last part is the reason to track them. Vendor marketing tells you what agents can do; this group publishes the numbers on what they can't. When you're sizing what to promise a client, their benchmarks are the only first-party evidence that cuts against the sales deck, which makes them unusually quotable in a design review.

Their tooling also lands here: [`agentforce-adlc`](developer-tooling-and-apis.md) is theirs.

---

## 2026-07-26 · CRMArena-Pro accepted to TMLR — the numbers to quote

**CRMArena-Pro** is their benchmark for LLM agents on realistic CRM work, now **accepted by TMLR** (*Transactions on Machine Learning Research*, peer-reviewed). It runs agents inside real Salesforce org environments built on Salesforce schemas, in both **B2B and B2C** variants, across multiple personas and multi-turn interactive scenarios.

**How to run it yourself.** [Repo](https://github.com/SalesforceAIResearch/CRMArena) ships the evaluation scripts; datasets are on Hugging Face; the orgs come with test credentials. You connect a model by API and score it.

**The findings, which are the actual deliverable:**

- Structured, single-turn workflow tasks — lookups, updates, routing — land around **83%**. Largely solved.
- Performance **degrades sharply** on tasks needing sustained multi-turn context.
- **Confidentiality awareness is close to absent** unless the agent is explicitly prompted for it. Agents will disclose data they shouldn't, and won't flag that they did.

**What to do with it.** This is the citation for when a stakeholder assumes an agent will "just handle service cases." It also implies a specific architecture: narrow, well-scoped agents with **deterministic Agent Script guardrails** around anything touching sensitive fields — not one broad agent trusted to exercise discretion. That's precisely what Multi-Agent Orchestration and the Einstein Trust Layer exist to support, and now you have a peer-reviewed reason rather than an instinct.

**Status:** Accepted to TMLR, 2026. Benchmark and datasets are open but **research-only** — not licensed for commercial deployment.

**Study action:** run one B2C task set against two models and read the failure transcripts, not the scores. The failure modes are the transferable part.

**Sources:** [CRMArena repo](https://github.com/SalesforceAIResearch/CRMArena) · [CRMArena-Pro (arXiv 2505.18878)](https://arxiv.org/abs/2505.18878) · [CIO coverage](https://www.cio.com/article/4008228/salesforce-study-warns-against-rushing-llms-into-crm-workflows-without-guardrails.html) · [Generative AI Benchmark for CRM](https://www.salesforceairesearch.com/crm-benchmark)

---

## SCUBA — why you build MCP tools instead of pointing a computer-use agent at Salesforce

**SCUBA** (Salesforce Computer Use Benchmark) evaluates *computer-use* agents — ones that drive the GUI by looking at the screen and clicking, rather than calling APIs — on CRM workflows in the Salesforce UI. **300 task instances** drawn from real user interviews, across three personas: platform admin, sales rep, service agent.

**The numbers:**

| Setting | Task success |
|---|---|
| Open-source models, zero-shot | **under 5%** |
| Closed-source models, zero-shot | **up to 39%** |
| With demonstrations | **~50%** |

**Why it matters.** This is the empirical answer to "why not just let an agent click through Salesforce?" — because it fails somewhere between half and nineteen-twentieths of the time. That gap is the entire argument for the [Headless 360 / hosted-MCP direction](developer-tooling-and-apis.md): give the agent typed, permissioned, API-shaped access instead of pixels. The demonstration-augmented number carries a second lesson worth generalizing — showing an agent a worked example beat using a bigger model.

**Status:** Published benchmark (2025), research-only.

**Sources:** [SCUBA (arXiv 2509.26506)](https://arxiv.org/abs/2509.26506) · [Salesforce AI Research](https://www.salesforceairesearch.com/)

---

## GIFT-Eval — the forecasting scoreboard

**GIFT-Eval** is their open leaderboard for time-series forecasting models, taking submissions continuously from outside teams. It sits next to Salesforce's own `uni2ts` / **Moirai** foundation-model line.

**When you'd reach for it.** Forecasting is the quiet other half of enterprise AI — pipeline, demand, capacity, churn timing. When a project asks "time-series foundation model or classical method here?", this is the neutral scoreboard to answer from rather than arguing by vendor claim.

Low urgency for the Agentforce tracks — a bookmark, not a study block.

**Status:** Ongoing open benchmark, Apache-2.0.

**Sources:** [gift-eval](https://github.com/SalesforceAIResearch/gift-eval) · [uni2ts / Moirai](https://github.com/SalesforceAIResearch/uni2ts)

---

## Reading their direction of travel

Salesforce AI Research had **21 papers accepted to ICLR 2026** (April 23–27, 2026, Rio de Janeiro), across LLM reasoning, evaluation systems, knowledge graphs and agent architectures.

The through-line worth internalizing is the **house style**: across CRMArena, SCUBA, GIFT-Eval and the adversarial probes baked into `agentforce-adlc`, their default question about an agent is *"how do we prove it's wrong?"* Adopting that stance — build the evaluation before you build the agent — is most of what separates a production agent from a demo, and it's free to copy.

**Sources:** [Salesforce AI Research at ICLR 2026](https://www.salesforce.com/blog/salesforce-iclr-2026/) · [Salesforce AI Research](https://www.salesforceairesearch.com/) · [GitHub org](https://github.com/SalesforceAIResearch)
