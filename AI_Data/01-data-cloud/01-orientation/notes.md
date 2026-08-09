# Data 360 Orientation

> Track: Data 360 · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/data-360.md](../../05-release-radar/data-360.md)

**Roadmap scope:** What it is (a lakehouse-based CDP), how it sits beside core CRM orgs, and the flow: ingest → model → unify → insight → activate.

> **Naming:** this folder is `01-data-cloud/` and the roadmap says "Data Cloud". The product is **Data 360**. Folder paths stay put so existing links and the dashboard keep working — the content uses the current name throughout.

## What is it?

Data 360 is Salesforce's **lakehouse-based platform** that ingests, harmonizes, unifies and activates customer data from any source — and, since 2026, grounds AI agents in it.

**Lakehouse** = a data lake's cheap open storage plus a warehouse's query performance and governance. That matters practically: you can land raw data cheaply *and* query it fast, without choosing between the two.

### The rename is real, not marketing

Salesforce began calling Data Cloud **"Data 360"** at Dreamforce 2025 (October 14, 2025), positioning it inside the **Agentforce 360** umbrella. The underlying product, licence, integrations and data model are unchanged — but the rename shows up everywhere that counts:

- Salesforce's pricing calculator is branded **"Data 360 (Formerly Data Cloud)"**
- There's a **Data 360 Starter** SKU (~$60k/yr) plus a $0 Provisioning (Everywhere) SKU
- The Summer '26 release-notes section is titled **Data 360**
- The certification is now the **Salesforce Certified Data 360 Consultant** (renamed 2026-03-27; exam code `Data-Con-101` unchanged)

**This is the sixth name.** Customer 360 Audiences → Salesforce CDP → Marketing Cloud CDP → Salesforce Genie → Salesforce Data Cloud → **Data 360**. Knowing the lineage is genuinely useful: you'll meet all six in documentation, blog posts and client orgs.

### The real shift isn't the name

It's the repositioning from *passive customer data store* to **active context engine that grounds AI agents**. Every 2026 feature follows from that premise — real-time ingest, custom chunking, the semantic layer, the MCP server. If you only remember one thing about Data 360 in 2026, remember that its job changed.

## Why it matters (for the AI-Salesforce architect role)

**The grounding is the product.** An Agentforce agent without Data 360 behind it is a chatbot with good manners. The agent's answer is only ever as good as the context it was given, which means the data architect's decisions — what's ingested, how fresh, how well resolved, how it's chunked — set the ceiling on agent quality.

That's the career argument for this track, and it's why the roadmap puts Data 360 *before* Agentforce.

**Three specific consequences worth carrying into every design:**

| Decision | Downstream effect |
|---|---|
| Ingestion freshness | Stale data → agent answers confidently from old state |
| Identity resolution quality | Duplicates → wrong profile → wrong answer, **and** a higher recurring bill |
| Chunking strategy | Usually the single biggest lever on retrieval quality |

### How it sits beside core CRM

Data 360 is **not** a replacement for your CRM org. It sits alongside:

```
   Core CRM org(s)        Marketing Cloud       External systems
   (Accounts, Cases)      (engagement)          (S3, Snowflake, web SDK)
          │                     │                      │
          └─────────────────────┼──────────────────────┘
                                ▼
                          ┌───────────┐
                          │  DATA 360 │   ingest → model → unify
                          │ lakehouse │   → insight → activate
                          └─────┬─────┘
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
        Agentforce         Activation        Tableau /
        (grounding)        (MC, ads, CRM)    analytics
```

CRM remains the system of record for transactions. Data 360 is the system of *context*.

### When there's more than one org: Data Cloud One

The diagram above shows *one* Data 360 beside *one* CRM org. Most enterprises don't look like that — they have five orgs from five acquisitions and want one customer view. The instinct is to ask which org "owns" Data 360, or to propose five instances. **Data Cloud One** is the answer to both, and it reframes the question.

**One Data 360 instance, many orgs.** One org is the **home org** and holds the tenant. Others attach as **companion orgs**.

```
        Home org — holds the Data 360 tenant
   ┌──────────────────────────────────────────────┐
   │  ingestion · connectors · streams            │
   │  identity resolution · harmonization         │
   │  governance · tagging · masking              │
   │       (all configured HERE, only here)       │
   │                                              │
   │   data space: EMEA   AMER   Brand-X          │
   └───────┬──────────────┬────────┬──────────────┘
           │              │        └── not shared
           ▼              ▼
     Companion org 1   Companion org 2
     (metadata, not data — records stay home)
```

| Fact | Consequence |
|---|---|
| All ingestion, resolution and governance live in the home org | Companion-org admins configure nothing; don't promise them the full Setup surface |
| Data spaces are the sharing unit | You pick which spaces each companion sees |
| Companions receive **metadata, not data** | Records never leave the home tenant; a subset of functionality via the Data Cloud One app |
| **Three companion connections are included** | The fourth is a commercial conversation, not a config change |
| **Data residency follows the home org's region** | An EU subsidiary on a US home org inherits US residency |

**You are not choosing an owner — you are choosing a partition boundary.** That choice is close to irreversible: data spaces cannot share a customer graph across the boundary, so drawing the line by *brand* when the real requirement was by *region* means rebuilding identity resolution later.

And residency turns a compliance question into an architecture question. For some EU/UK-regulated subsidiaries it disqualifies the pattern outright — separate instances are then the correct answer, not the lazy one.

## How it works

### The five-step flow

1. **Ingest** — data streams from connectors, batch or streaming. With **Accelerated Data Ingest (GA)**, CRM data arrives in real time with no pipeline lag.
2. **Model** — raw source shapes (DSO) → lake objects (DLO) → the canonical model (DMO).
3. **Unify** — identity resolution turns many source records into one **unified profile**, via match and reconciliation rules.
4. **Insight** — calculated insights compute metrics on a schedule; the semantic layer governs what those metrics *mean*.
5. **Activate** — publish segments to Marketing Cloud, ad platforms, CRM — or ground an agent.

Step 5 is where 2026 changed: "activate" used to mean marketing activation. It now equally means "answer an agent's question."

### Release cadence — important and easily missed

**Data 360 ships monthly, not on the three-times-a-year seasonal cadence.** Check the [monthly section of the release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&release=262&type=5) regularly. A feature can appear between seasonal releases, which is exactly how several Summer '26 items landed.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Trailhead: **Data Cloud Basics** (Phase 1 milestone badge — note Trailhead content may still use the old name)
- [ ] Get a Data 360 trial or Dev org and walk the five-step flow end to end with sample data.
- [ ] Map one real business question ("which customers are at churn risk?") through all five steps on paper before touching the UI.
- [ ] Bookmark the monthly release-notes section and check it once a week.
- [ ] **Data spaces:** in a Dev org with Data 360 provisioned, open **Setup → Data 360 Setup → Data Spaces**, create a second space, then run the same DLO query with and without a `SET OPTIONS` dataspace clause — record which one silently returns zero rows.
- [ ] For an org estate you actually know, write down whether the partition boundary would be brand, region or legal entity — and what breaks if you pick wrong.

## Gotchas & sharp edges

- **Six names, all still in circulation.** Genie, CDP, Data Cloud, Data 360 — expect all of them in docs and client conversations. They're the same product.
- **Trailhead and much documentation still say "Data Cloud."** Not an error, just lag. The cert and release notes use Data 360.
- **Monthly cadence, not seasonal.** Checking only the three seasonal releases means missing most Data 360 changes.
- **It isn't a CRM replacement.** A surprisingly common client misunderstanding. CRM is the system of record; Data 360 is the system of context.
- **DLOs don't behave like Platform objects.** Different semantics around nulls and empty strings, and dataspace is required when querying them. See [data modeling](../03-data-modeling-dso-dlo-dmo/notes.md).
- **Pricing changed to profile-based on March 2, 2026** (~$240 per 1,000 profiles). A "profile" is a **unified individual after identity resolution**, so poor matching directly inflates a recurring bill.
- **Some Summer '26 features are Beta.** Read the label literally: Fabric OneLake federation is Beta, AWS Glue is GA. One is proposal-safe, the other isn't.
- **A data space is not an access-control mechanism.** Use it only for boundaries that must never be crossed — distinct legal entities, incompatible residency regimes. For "different teams see different data", use permission sets and keep the unified profile intact.
- **Data Cloud One sandboxes and production don't cross.** A sandbox home org pairs only with sandbox CRM orgs, production only with production. Plan the SDLC topology in both tiers or you cannot test the connection at all.
- **Data Cloud One hasn't been renamed.** It is still "Data Cloud One" in first-party docs as of 2026-08-08 — not "Data 360 One". Search accordingly.

## Related topics

- [Ingestion](../02-ingestion/notes.md) — step 1, and why freshness matters for agents
- [Data modeling DSO → DLO → DMO](../03-data-modeling-dso-dlo-dmo/notes.md) — step 2, the heart of the exam
- [Identity resolution](../04-identity-resolution/notes.md) — step 3, and the cost lever
- [RAG on platform](../08-rag-on-platform/notes.md) — how grounding actually works
- [Salesforce AI Landscape](../../02-salesforce-ai/01-landscape/notes.md) — the other half of the platform
- [Data 360 DevOps](../09-data-360-devops/notes.md) — sandbox → production, which Data Cloud One constrains
- [Release radar: Data 360](../../05-release-radar/data-360.md) — the running story, with sources
- [Release radar: Data Cloud One](../../05-release-radar/data-360.md#2026-08-08--gap-check--data-cloud-one-the-multi-org-architecture-this-radar-never-recorded) — the full multi-org write-up
