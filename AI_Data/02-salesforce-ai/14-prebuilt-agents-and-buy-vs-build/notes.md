# Prebuilt agents & buy vs build

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · Product status: **GA across the board** — Help Agent and Commerce July 2026, Contact Center February 2026 · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** the agents Salesforce now ships finished — Help Agent, Commerce, IT Service, industry packs — what each one is, the three commercial models behind them, and the decision framework for when a prebuilt agent beats a custom build.

> **Why this folder exists.** Through 2025 the question was "can you build an agent." In 2026 Salesforce started shipping *finished* agents, and the question became **"should you build one at all."** That's an architect's decision, and it had no notes behind it — Agentforce Commerce and Contact Center appeared nowhere in this study base outside the radar. The deliverable here is a **decision framework**, not a product catalogue: the catalogue will be stale in a quarter, the framework won't.

## What is it?

Prepackaged agents with guided setup, sold as products rather than as capabilities to assemble. The pattern across all of them: minutes-to-deploy, opinionated defaults, channels pre-wired, and grounding as the only real configuration surface.

| Product | What it is | Status |
|---|---|---|
| **Agentforce Help Agent** + Customer Service Portal | Prebuilt self-service support agent. Guided setup — Salesforce claims **six clicks or less**. Web, text and voice channels from one screen. The portal became a single conversation bar with dynamic AI-generated cards | **GA July 2026** |
| **Agentforce Commerce** | Three agents: **Shopper** (B2C — discovery → checkout → post-purchase), **Buyer** (B2B via WhatsApp and SMS), **Merchant** (back office — catalogue and trends in natural language) | **GA July 6, 2026** |
| **IT Service Domain Pack** | 50+ prebuilt agents into Slack, Teams and the IT Service Desk | GA — see the [2026-07-27 scan](../../05-release-radar/01-agentforce/2026-07-27.md) |
| **Agentforce Contact Center** | Native CCaaS — see [12-voice-and-contact-center](../12-voice-and-contact-center/notes.md) | **GA February 23, 2026** |
| **Industry packs** — Agentforce Public Sector, Agentforce Health, **Missionforce** | Vertical agent estates; behind the VA's $1.6B agreement | GA |

### The Help Agent benchmark worth memorising

Salesforce runs Agentforce on `help.salesforce.com` and publishes the numbers: **4.3 million inquiries handled, 70% resolved.** It's first-party and self-interested, but it's the strongest single reference point available for a business case — and unlike most vendor statistics you can point at the site and say "that one."

Second useful benchmark, from a real customer: **Oviva** handles **300,000+ inbound messages/month**, deflecting half of all inquiries and resolving 40% of operational support requests without a human.

## Why it matters (for the AI-Salesforce architect role)

**The differentiation moved.** When Salesforce ships a support agent that deploys in six clicks, "we can build you a support agent" stops being a proposition. What remains valuable is **how well yours is grounded** — the Knowledge hygiene, the data model, the sharing rules, the retrieval quality. That's the Data 360 work in [RAG on Platform](../../01-data-cloud/08-rag-on-platform/notes.md), and it's now the billable part.

**Three commercial models now coexist, and they price the same work differently.**

| Model | Unit | Where it applies |
|---|---|---|
| **Flex Credits** | ~$0.10 per standard action (20 credits); $500 per 100k | The default for custom builds |
| **Pay-per-resolution** | **$2** per autonomous end-to-end resolution — consumption unmetered *during* the interaction | Help Agent, July 2026 |
| **Agentic Enterprise License Agreement (AELA)** | Negotiated enterprise-wide | The VA's **$1.6B / three-year** deal, July 24 2026 |

Pay-per-resolution is the interesting one: it ties revenue to *outcomes* rather than conversations, which inverts the usual ROI conversation. Under Flex Credits a chatty agent that never resolves anything costs you money; under pay-per-resolution it costs Salesforce money. Know which model a client is on before you model anything.

**Commerce inverts the grounding problem.** With the Shopper Agent selling natively inside ChatGPT — catalogue synced straight from Business Manager, no middleware — the customer's session *starts outside Salesforce entirely*. Normally you worry about giving your agent good context; here you publish your context into a model you don't control. **Product data quality becomes an externally-visible asset**: attribute mapping and catalogue hygiene decide whether ChatGPT recommends your product or a competitor's. Note also that Salesforce keeps **checkout on the merchant's own site**, which preserves order data and the post-purchase relationship — competing agentic-commerce designs don't all make that choice.

## How it works

### The buy-vs-build decision framework

Work it in this order. The first question that returns a clear answer usually decides it.

```
1. Does a prebuilt agent already cover the use case?
      no  → build. Done.
      yes → continue.

2. Is the differentiating logic in the CONVERSATION or in the DATA?
      conversation (unusual process, bespoke decisioning) → build
      data (right answers, right records, right permissions) → buy, invest in grounding

3. Which commercial model fits the outcome?
      outcomes are countable and discrete   → pay-per-resolution favours you
      long exploratory sessions, few resolutions → Flex Credits may be cheaper
      enterprise-wide, many agents          → ask about an AELA

4. What's the upgrade path?
      prebuilt → Salesforce maintains it; you inherit improvements
      custom   → you maintain it, including through model drift  (see ADLC outer loop)

5. Can the prebuilt one be extended where it matters?
      yes → buy, then extend at that seam
      no  → build, and accept the maintenance
```

**Question 2 is the one that actually decides most cases.** If what makes the client different is *what the agent knows*, buy the agent and spend the budget on Data 360. If what makes them different is *how the conversation goes* — an unusual approval chain, regulated scripting, bespoke decisioning — build it in [Agent Script](../07-agent-script/notes.md).

**Question 4 is the one people forget.** A custom agent is not a delivered artifact, it's an ongoing commitment: drift has no commit, so somebody owns the outer loop forever. Prebuilt agents move that cost to Salesforce. Price the maintenance, not just the build.

### What you give up by buying

- Deep behavioural customization — the setup is deliberately opinionated.
- Control over the upgrade timing; Salesforce improves it on Salesforce's schedule.
- Some observability surface: you didn't author the topics, so you're reading behaviour you didn't specify.

### What you gain

- Time-to-value measured in minutes, not sprints.
- A supported upgrade path, and channels already wired.
- Salesforce's own benchmark numbers to point at in a business case.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Deploy the Help Agent in a dev org and time it. Then ask it something your Knowledge base answers badly — that gap *is* the consulting engagement.
- [ ] Run the framework above against one real Geeksoft opportunity and write down which question decided it. Keep the write-up; it's reusable.
- [ ] Model the same 1,000-conversation month under Flex Credits and under pay-per-resolution. Find the crossover point where they cost the same.
- [ ] Compare the Help Agent's grounding configuration against a custom agent's `knowledge:` block — see [Agentforce Data Library Connect API](../../05-release-radar/agentforce-platform.md). Note what you can and can't reach.
- [ ] Write the two-sentence answer to "why not just use the prebuilt one?" You will be asked it.

## Gotchas & sharp edges

- **Pay-per-resolution needs a definition of "resolution."** $2 per *autonomous end-to-end* resolution — so what counts, who adjudicates it, and what happens on a partial resolution are commercial questions, not technical ones. Get them answered in writing before this reaches a proposal.
- **"Deployable in minutes" is true and misleading.** Deployment is minutes; *grounding it well* is the project. Both statements can be quoted at you in the same meeting.
- **Salesforce's 70% resolution figure is first-party.** Use it, cite it as theirs, and don't present it as an independent benchmark.
- **Commerce publishes your catalogue into ChatGPT.** That's a data-governance conversation — what leaves the org, under whose identity, and how a bad attribute becomes a lost sale. Have it early.
- **Checkout stays on the merchant's site** in Salesforce's design. Don't assume that of competing agentic-commerce platforms.
- **Prebuilt agents still run on the same platform limits.** Flex Credits, voice rates, and Trust Layer behaviour don't change because you didn't author the agent.
- **The catalogue changes fast.** Everything in the product table above was announced in the first seven months of 2026. Treat the table as a snapshot and the framework as the durable part.
- **An AELA is not a product, it's a negotiation.** Interesting as a signal that Salesforce will sell agents enterprise-wide; not something to design around.

## Related topics

- [Voice & Contact Center](../12-voice-and-contact-center/notes.md) — Contact Center as the largest prebuilt product
- [Salesforce AI Landscape](../01-landscape/notes.md) — where Help Agent and Flex Credits first appear
- [Agent Script](../07-agent-script/notes.md) — the build side of the decision
- [RAG on Platform](../../01-data-cloud/08-rag-on-platform/notes.md) — the grounding work that becomes the billable part
- [ADLC & Agentforce DX](../13-adlc-and-agentforce-dx/notes.md) — the maintenance cost a custom build commits you to
- [Capstone: Agentforce use case](../../04-capstone/03-agentforce-use-case/notes.md) — where this framework gets applied
- [Release radar: pricing & certification](../../05-release-radar/pricing-and-certification.md) — the three commercial models, dated
