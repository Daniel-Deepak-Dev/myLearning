# Lab Environment & Testing Craft

> Track: Data 360 · Roadmap: Phase 02 · Weeks 5–8 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [resources.md](resources.md)

**Scope:** What you can plug into what when you don't have an enterprise tenant — and, more importantly, how you *prove* each layer worked. The practice topic for this track: the other nine are what to build, this one is where to build it and how to test it.

> **Why this folder exists.** Every other topic in this track ends with an unchecked "Hands-on / labs" list. This one holds the environment those labs run in, and the [lab ladder](labs/README.md) they became.

## What is it?

A Data 360 lab environment is a **topology decision, not a signup**. The question isn't "where do I get an org" — it's "which orgs play which role, and what does each connection actually teach me".

There are exactly **four ways to get Salesforce data into a Data 360 tenant**, and confusing the middle two is the single most common misconception:

| Mechanism | Source org needs a Data 360 licence? | Direction | Works on a free DE tenant? |
|---|---|---|---|
| **Home org connector** | n/a — the tenant lives *in* that org | in (+ data actions out) | ✅ built in, zero setup |
| **Standard Salesforce CRM connection** | ❌ **No** — permission set + OAuth only | in (+ data actions out) | ✅ **Yes** |
| **Data Cloud One companion connection** | Needs companion licences | metadata *out* to the companion | ❌ No |
| **Ingestion API** | ❌ No — works from *any* org or system | in | ✅ Yes |

**So: yes, you can connect an org with no Data Cloud licence to a Dev Edition org that has Data 360.** You do it with a **standard CRM connection**, and the licence lives entirely on the Data 360 side. What you *can't* do on a free DE is a **Data Cloud One companion connection** — that's the one that needs companion licences and only pairs production↔production or sandbox↔sandbox.

The two are easy to conflate because both are described as "connecting an org". They point in opposite directions:

```
   STANDARD CRM CONNECTION              DATA CLOUD ONE COMPANION
   (ingest data in)                     (push metadata out)

   source org  ──── data ────►          home org ──── metadata ────►  companion org
   (no licence needed)                  (companion licence needed)
        ◄──── data actions ────              records never leave home
```

## Why it matters (for the AI-Salesforce architect role)

**Two things clients pay for, neither of which is learnable from documentation.**

The first is the **connector permission model**. Every failed Data 360 connection in the wild is a permissions problem wearing a different hat — a missing field-level read, an integration user without View All, a permission set assigned to the wrong user. You will diagnose this in an hour if you've wired it once and in a day if you haven't.

The second is the **verification habit**. Data 360 fails quietly more often than loudly: a data stream reports success having ingested nothing, a DLO query returns zero rows because the data space was wrong, an unmapped field looks exactly like a null. "It's green in the UI" is not evidence. Knowing what to check at each layer — and what each layer lies about — is the difference between an implementation consultant and someone who followed a Trailhead module.

Both are cheap to learn on a free tenant and expensive to learn on a client project.

## How it works

### 1. Home org connector

The org where Data 360 is provisioned is the **home org**. Its CRM objects are available immediately through the built-in Salesforce CRM connector — no connection to create, just pick objects and go. This is where you learn DSO → DLO → DMO without any auth in the way. See [data modeling](../03-data-modeling-dso-dlo-dmo/notes.md).

### 2. Standard Salesforce CRM connection (an external org)

Data 360 in org A ingests from org B. **Any Salesforce org built on the CRM core can be a source** — production, sandbox, another Developer Edition — and **org B needs no Data 360 licence of its own**.

What you configure, and where:

| Side | What you set up |
|---|---|
| **Source org (B)** | A permission set granting the **Data 360 Salesforce Connector** integration permissions, plus **Read + View All** on each object and **Read** on each field you intend to ingest. Assigned to the user who authorises the connection. |
| **Data 360 org (A)** | Setup → the Salesforce CRM connector → new connection → OAuth as that source-org user → select objects → create data streams. |

The connection is **OAuth as a real user of the source org**, so the source org's own sharing and FLS bound what Data 360 can ever see. That's the design point worth carrying into a governance conversation: you don't grant Data 360 access, you grant a *user* access and Data 360 borrows it.

Data actions travel back the other way over the same connection — see [lab-06](labs/lab-06-data-actions-round-trip.md).

### 3. Data Cloud One companion connection

Bidirectional, and the metadata flows *outward*: the companion org gets unified metadata and a subset of Data 360 features, while records stay in the home tenant. Requires companion licences and strict environment pairing — a sandbox home org pairs only with sandbox orgs, production only with production. **Not testable on a free DE**; covered as theory in [orientation](../01-orientation/notes.md#when-theres-more-than-one-org-data-cloud-one).

### 4. Ingestion API

The universal fallback: push records into Data 360 over REST from anything at all — an org with no connector, a script, a serverless function. Two patterns: **bulk** (CSV, periodic) and **streaming** (incremental, near-real-time).

From an Apex org the shape is: **custom auth provider (JWT) → Named Credential → Apex callout**, against a **tenant-specific endpoint** published on the Ingestion API connector's setup page. You upload an **OpenAPI (OAS) YAML schema** describing your objects; that schema defines the DLO. The open-source `lightweight-data-cloud-auth-provider` / `lightweight-data-cloud-util` pair does the plumbing (see [resources](resources.md)).

This is the most *educational* mechanism because nothing is hidden: you see the payload, the primary key, the upsert semantics, and the failure body.

## The testing playbook

The core of this topic. **For every layer: how you prove it, and what it lies about.**

| Layer | How you prove it worked | Where it lies to you |
|---|---|---|
| **Data stream** | Refresh history: last run, status, **row count** | Reports **Success with 0 rows**. Green ≠ ingested. |
| **DLO** | Query Workspace SQL, with `SET OPTIONS` for the data space | Wrong/missing data space → **zero rows, no error** |
| **DMO mapping** | Data Explorer row count vs. `COUNT()` in the source org | An **unmapped field reads as null**, not as an error |
| **Identity resolution** | Match/reconciliation output + deliberately built collision records | Over-matching *looks like* success: fewer profiles, cleaner data, wrong people merged |
| **Calculated insight** | Recompute the same metric as raw SQL and compare | Refresh **schedule** looks identical to a staleness bug |
| **Segment** | Membership count vs. the equivalent SQL query | Publish lag — the count is true, just not now |
| **Data action** | The triggered Flow's own debug log **and** the record in the target org | Fails **silently** on a permission problem |
| **Credits** | Usage monitoring, before vs. after | Attribution: nothing tells you *which* job burned them |

Two habits that follow from the table:

**Baseline before you build.** Record counts and credit usage before a change, or you have nothing to compare against. That's all [lab-00](labs/lab-00-tenant-baseline.md) is.

**Break it on purpose.** Every lab in the ladder ends with a deliberate failure — remove a field permission, query the wrong data space, send the same payload twice. Recognising a failure signature is a skill you can only acquire by having caused it.

## Governance: the client sandbox question

You have access to a client/employer sandbox. **Don't connect it as a source to a personal DE tenant.** The technology permits it; the mechanism is exactly the standard CRM connection above. But it moves client data into a tenant Geeksoft doesn't control, doesn't monitor and can't wipe — a GDPR conversation you don't want to have retrospectively, and the sandbox may well contain copied production data.

Two correct alternatives:

1. **For labs — a second free Developer Edition org as the source.** Identical learning, seeded with data you invented. Every mechanism above behaves the same way.
2. **For real work — the $0 Data 360 Provisioning SKU** (a.k.a. "Data Cloud Everywhere"). Enterprise and Unlimited edition orgs can provision Data 360 at **no cost**: ~250,000 Data Services credits, 1 TB storage, 1 admin, ~100 users, 5 integration users. That puts Data 360 *inside* the client's own estate where it belongs, and it's a genuinely useful thing to know in a pre-sales conversation — "you already have this, it costs nothing to switch on" is a better opening than a licence quote.

The rule generalises: **the tenant should sit inside the trust boundary that owns the data.** Personal dev orgs sit outside every client's boundary, permanently.

## What you cannot learn on a free DE

Say this out loud so you don't quietly assume otherwise in a design review:

- **Data Cloud One companion connections** — needs licences and prod↔prod / sandbox↔sandbox pairing
- **Real sandbox → production promotion** — needs two real orgs; you can still practise the *mechanics* with data kits and the CLI ([lab-07](labs/lab-07-promotion-and-packaging.md))
- **Marketing Cloud activation** — no licence, no target
- **Scale and performance behaviour** — 10 GB and a few hundred test records tells you nothing about a 200M-row stream
- **Production credit economics** — you'll learn *what* consumes credits, not what it costs at volume

For all five, the honest position is "I've read the constraints, I haven't run it." That's a fine thing to say. Claiming otherwise is how people get caught in interviews.

## Hands-on / labs

**→ [The lab ladder](labs/README.md)** — nine runbooks, each with a *break it on purpose* step.

- [ ] [lab-00](labs/lab-00-tenant-baseline.md) — tenant baseline
- [ ] [lab-01](labs/lab-01-home-org-crm-connector.md) — home org connector
- [ ] [lab-02](labs/lab-02-external-org-connection.md) — **external org connection** (the one that answers the licence question)
- [ ] [lab-03](labs/lab-03-ingestion-api-any-org.md) — Ingestion API from any org
- [ ] [lab-04](labs/lab-04-identity-resolution.md) — identity resolution across three sources
- [ ] [lab-05](labs/lab-05-insights-and-segments.md) — insight & segment validation
- [ ] [lab-06](labs/lab-06-data-actions-round-trip.md) — data action round trip
- [ ] [lab-07](labs/lab-07-promotion-and-packaging.md) — promotion & packaging
- [ ] [lab-99](labs/lab-99-parked-external-sources.md) — parked (needs accounts you don't have yet)

## Gotchas & sharp edges

- **A standard CRM connection needs no licence in the source org — a Data Cloud One companion connection does.** The distinction that answers most "can I connect X" questions.
- **Identity resolution burns credits hardest**, because you're billed on records *reviewed* during unification. Keep lab datasets in the hundreds. A careless fuzzy ruleset over a large stream is how a free tenant dies.
- **A free DE gives you 1 data space and 10 GB.** Enough for every lab here; not enough to be careless.
- **A Developer Edition expires if unused** — log in roughly every 45 days or lose the work.
- **If Data 360 Setup isn't in your DE org**, the fallback is a **Partner Developer Edition** org from Environment Hub (Geeksoft's partner org can mint one). Historically PDE was the *only* dev-tier route to Data Cloud; the current free developer signup ships with it enabled, but not every existing org was retrofitted.
- **Docs, Trailhead and the UI still say "Data Cloud" in places.** Search both names or you'll conclude a feature doesn't exist.
- **Green is not evidence.** Successful stream, zero rows. Check the count, every time.
- **Data actions fail silently on permissions.** If a round trip "does nothing", start at the target org's FLS, not at the data action.
- **Test data you invented beats sample data you downloaded** — you know what the right answer is, so you can tell when the platform is wrong. This matters most for identity resolution.

## Related topics

- [Orientation](../01-orientation/notes.md) — Data Cloud One, the home/companion architecture in full
- [Ingestion](../02-ingestion/notes.md) — connectors, batch vs streaming, freshness
- [Data modeling](../03-data-modeling-dso-dlo-dmo/notes.md) — `SET OPTIONS`, the zero-rows trap this topic keeps citing
- [Identity resolution](../04-identity-resolution/notes.md) — match rules, and the cost lever
- [Insights & segmentation](../05-insights-segmentation/notes.md) — what lab-05 validates
- [Zero copy & BYOL](../06-zero-copy-byol/notes.md) — the parked labs in lab-99
- [Data 360 DevOps](../09-data-360-devops/notes.md) — data kits, `@IntegrationTest`, where lab-07 leads
