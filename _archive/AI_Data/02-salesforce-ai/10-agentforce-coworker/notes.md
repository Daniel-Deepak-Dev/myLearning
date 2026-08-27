# Agentforce Coworker

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · Product status: **Beta — no announced GA date** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** what Agentforce Coworker is, the surfaces it runs in, the setup path, federation vs ingestion of data sources, its billing model, and the governance shift it forces.

> **Why this folder exists.** Every other topic in this track is about **authoring** an agent — Agent Script, actions, orchestration, scorers. Coworker is the opposite: you author nothing. You turn it on and it inherits your org. That inversion changes the architect's job from *"what should this agent do"* to *"what is it allowed to see"*, and that question has a different answer in every org you'll ever work in.

## What is it?

An AI teammate that lives **in the search bar** — Salesforce's own, and eventually every other one your users type into. Marc Benioff announced it on **May 21, 2026** and described it as the biggest thing Salesforce had shipped that quarter; the framing in Salesforce's own material is that it *replaces* Salesforce Search. *(Date caveat: a third-party setup walkthrough is published at a May 10 URL, and no first-party page states an announcement date — see the [radar entry](../../05-release-radar/01-agentforce/2026-07-28.md). Nothing below depends on it.)*

The docs call it "your single entry point for getting work done." The loop is **discover → research → act**: surface something, dig into it, then hand off to a specialized agent that actually does the thing — updating a case, advancing an opportunity — without leaving the search box.

### Surfaces

| Surface | Status (as of 2026-07-28) |
|---|---|
| **Salesforce** — the global search bar | Beta, available today |
| **Slack** | Beta, available today (federated — see below) |
| Web, **Microsoft Teams**, **ChatGPT**, **Claude**, desktop app | "later this year" |

One capability, many entry points — the same pattern as [agent surfaces](../02-agentforce-anatomy/notes.md), but arriving from the opposite direction: instead of publishing an agent you built to a channel, Coworker is already in the channel and reaches back into your org.

## Why it matters (for the AI-Salesforce architect role)

**Nothing is authored, so everything is inherited.** No Agent Script, no topics, no actions, no subagent descriptions. Deployment is a Setup toggle and a permission assignment. What Coworker can answer is determined entirely by the org's sharing model, field-level security and data-source configuration — which means **turning it on is the fastest audit of a sharing model anyone will ever run**, whether or not they asked for one. If sharing is loose, Coworker makes that visible instantly, org-wide, to every licensed user. Plan the enablement conversation accordingly.

**It's a front door onto the agent estate, not a competitor to it.** Coworker routes to specialized agents — the documented examples are a Sales Coach Agent and a Support Agent. That makes the work you do in [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) *more* valuable, not less: the narrow, well-tested agents you build become the things Coworker can reach. Same lesson as orchestration — a specialist agent nobody can find might as well not exist.

**It puts CRM data behind third-party surfaces.** Coworker is slated to run inside **ChatGPT and Claude**. That is a governance discussion, not a feature bullet, and it's the point where this track meets [the Claude track](../../03-claude-cca/05-mcp/notes.md): what leaves the org, under whose identity, logged where. Have the answer before a client asks.

## How it works

```
  user types in the SEARCH BAR  (Salesforce · Slack · Teams · ChatGPT · Claude)
        │
        ▼
  Search Agent  ── 100 RPM
        │
        ├──► Salesforce CRM records ── respects sharing rules + FLS
        ├──► Data 360 objects (DMOs) ── ingested + indexed
        └──► Slack ── FEDERATED, not ingested (queried live via Slack auth)
        │
        ▼
  synthesized answer  ── with automatic data classification + dynamic masking
        │
        ▼
  routes to a SPECIALIZED AGENT  (Sales Coach · Support · your own)
        │
        ▼
  action executes ── update the case, the record, the opportunity
```

### Setup — the actual click path

1. Setup → Quick Find → **Agentforce Coworker**.
2. *(Optional)* **Set Up Data Space** — only if you have more than one; otherwise the default is used.
3. **Get Started with Agentforce Coworker** → **Turn On** → confirm.
4. **Turn on End User Experience** → *Manage* → read the Global Search Bar disclaimers → tick the consent box → **Turn On**.
5. **Manage Users** → *Manage* → select users → **Assign** → **Done**.

**Prerequisites:** Salesforce Admin Role **and** the **Agentforce Coworker Admin** permission set. Editions: **Enterprise, Unlimited, Agentforce 1**.

User access is technically granted by the **`Access_Ai_Search`** permission set group — but Salesforce explicitly recommends assigning through the *Manage Users* section rather than assigning the group directly. Know both; use the recommended one.

### Data sources — federation vs ingestion

This is the distinction that actually explains the product, and it's the one worth carrying into a design conversation:

| Source | Mechanism | Consequence |
|---|---|---|
| **Slack** | **Federated** — queried live, *not* ingested into Data 360 | Requires Slack Authentication configured in Salesforce first. Always fresh; bound by Slack's rate limits. |
| **Google Drive, SharePoint** | **Ingested** — crawled and indexed | 1 hr incremental refresh, so answers lag. Subject to hard file/size caps. |
| **Data 360 objects** | Any **DMO** in the data space | The extensibility path — everything you modeled in [Data 360](../../01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) becomes searchable. |
| **Salesforce CRM** | Native | Sharing rules and FLS apply. |

Federation vs ingestion is the same trade-off you met in [zero-copy / BYOL](../../01-data-cloud/06-zero-copy-byol/notes.md): freshness and no duplication versus latency and rate limits. Coworker just makes you choose per source.

### Billing — and why it's a design input

Two models, and they can run **side by side in the same org**, billed per user according to that user's license:

- **Seat-based** — Agentforce 1 Edition, or Agentforce for Sales / Service / Industries. Searching **Salesforce CRM or Slack consumes zero Flex Credits and zero Data Services Credits**. This is the cheap path and most orgs on the right license should be on it.
- **Usage-based** — **Flex Credits** cover Standard, Basic and Advanced prompts plus Data 360 unstructured processing, intelligent processing and querying. **Data Services Credits** cover data queries, unstructured data processed and intelligent processing.

**Guest, unauthenticated and portal users are always usage-based** regardless of anything else. And connecting extra sources through Data 360 generates processing and indexing charges that exist whether or not anyone searches.

The trap: a seat-licensed user can still burn credits if user-based AI permissions aren't configured. Configure them at rollout, not after the first invoice.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Turn it on in a dev org and **watch what else lights up** — enabling Coworker automatically enables Einstein.
- [ ] Add one Data 360 DMO **and** one Slack workspace, then ask a question that can only be answered by joining the two. That's the demo that sells it.
- [ ] **The governance exercise:** log in as a restricted user and ask Coworker something that user shouldn't be able to see. Confirm sharing rules hold. Do this before any client ever does.
- [ ] Compare the same question against a federated Slack source and an ingested Drive source; note the freshness gap the 1 hr incremental crawl produces.
- [ ] Assign access both ways — via *Manage Users* and via the `Access_Ai_Search` permission set group — and note what differs.

## Gotchas & sharp edges

- **Marketing says "270+ data sources." The Beta docs say three.** Salesforce CRM, Data 360 objects, and Slack. **Google Drive, SharePoint and Jira are pilot-only** and need an account executive to enable. Never scope a client project on the marketing number — check the limits page.
- **Turning on Coworker automatically enables Einstein.** A much bigger switch than the button implies. Know what that means for the org before you flip it.
- **Beta consumption is non-refundable.** The Beta Services Terms state that consumption of entitlements arising from use of Non-GA services gives rise to **no refund or credit rights**. Prototyping costs real money you can't claw back.
- **Not supported on Government Cloud Plus.** Salesforce says don't activate it; contact your AE.
- **Seat-licensed users can still burn credits** if user-based AI permissions aren't configured. That's the documented reason the setup guide exists.
- **Hard limits worth memorizing:**

  | Limit | Value |
  |---|---|
  | Slack queries, sustained | **180 per minute** per user JWT token |
  | Slack queries, burst | up to **1000** per user |
  | Search Agent | **100 RPM** |
  | Google Drive | **5,000 files** per shared drive · **1 hr** incremental |
  | SharePoint | **10–15 GB** and **5,000 files** per site · **1 hr** incremental |
  | File size | PDFs ≤ **100 MB** · other files ≤ **4 MB** |
  | SharePoint unsupported | files with security labels or tags, empty Excel files, OneNote |

- **Governance is inherited, not authored.** Good news and bad news in one sentence: you can't misconfigure Coworker's permissions, but you also can't fix a bad sharing model from inside it.
- **Coworker is not an Employee Agent.** Employee Agents are purpose-built and authored, with their own subagents and actions. Coworker is zero-config and org-wide. Expect this to be confused constantly, including by people selling it.
- **No GA date announced** as of 2026-07-28. Prototype freely; don't put it on a delivery commitment.

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — Service Agent vs Employee Agent, and where Coworker sits beside both
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — the specialist agents Coworker routes to
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — masking and classification, which Coworker applies automatically
- [RAG on Platform](../../01-data-cloud/08-rag-on-platform/notes.md) — the grounding discipline underneath the search
- [Zero copy & BYOL](../../01-data-cloud/06-zero-copy-byol/notes.md) — federation vs ingestion, the same trade-off
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) — what it means for CRM data to be reachable from Claude and ChatGPT
