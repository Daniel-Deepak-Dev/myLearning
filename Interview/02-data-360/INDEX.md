# 02 · Data 360

Scenario questions on the data layer that decides whether an agent is any good. Source knowledge: [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md).

> **Data Cloud is Data 360.** A real rename — SKUs, release notes and the certification all use it. Folder paths in the source vault keep the old name so links don't break; the content doesn't, and neither should you in an interview.

> ⚠️ **The pricing model changed on March 2, 2026** and it changes the answer to almost every question in this area. Data 360 is billed on a **profile-based SKU** — roughly **$240 per 1,000 unified profiles** baseline — where a profile means a unified individual *after* identity resolution, not a raw source row. Match quality stopped being a data-quality concern and became a recurring line item.

| Set | Scenarios it drills | Level |
|---|---|---|
| [01 · Ingestion & modeling](01-ingestion-and-modeling.md) | The silent zero-rows dataspace trap 🆕 · batch vs streaming vs Accelerated Data Ingest under an SLA · custom DMO proliferation and how a mapping error propagates · a breaking upstream schema change with four weeks' notice | medium → complex |
| [02 · Identity & segmentation](02-identity-and-segmentation.md) | RFM ranks are relative, not absolute · a cost-driven ruleset loosening that is a privacy incident · landing a ruleset change on live activations · one metric, two definitions, and an agent that doesn't ask 🆕 | medium → complex |
| [03 · Zero copy & activation](03-zero-copy-and-activation.md) | Federating everything then needing features locally · a Beta capability load-bearing in a dated proposal · inherited query latency becoming an agent SLA problem · "zero copy, zero cost" at a finance review | medium → complex |

**12 scenarios.** The recurring shape: a data decision that is invisible until it surfaces as an AI failure, a privacy exposure, or a recurring bill.

## The four highest-value things to be able to say

1. **You are billed on unified profiles, not source rows.** So poor matching is a recurring cost. And the two failure directions are asymmetric: under-matching fragments a customer and you pay several times; **over-matching merges two people, which is cheaper and is a privacy incident**. Never tune matching on cost alone.
2. **Everything downstream inherits the DLO → DMO mapping.** Identity resolution matches on DMO fields, insights compute over them, segments filter them, agents ground on them. A mapping mistake does not stay local.
3. **Zero copy removes Data 360 storage cost and nothing else.** You still pay source-side compute on every query, and query performance is inherited from the source — a slow warehouse is a slow agent.
4. **If an agent grounds on it, it needs to be real-time; if a dashboard reads it, scheduled is fine.** Decide per data stream, not per project. Stale grounding is the #1 root cause of "the agent was wrong" and is misdiagnosed as a model problem almost every time.

## Read the status labels literally

The distinction that decides whether a capability goes in a delivery plan or stays in a demo:

| Capability | Status |
|---|---|
| AWS Glue Data Catalog federation | **GA** — proposal-safe |
| Accelerated Data Ingest | **GA** — the default for CRM going forward |
| Microsoft Fabric OneLake federation | **Beta** — prototype only, never load-bearing |
| ADL Connect API (grounding as code) | **Beta** — fine to build on, not contractually load-bearing |

## Related

- [AI_Data/01-data-cloud/](../../AI_Data/01-data-cloud/INDEX.md) — the source notes every answer links into
- [AI_Data/01-data-cloud/10-lab-environment/labs/](../../AI_Data/01-data-cloud/10-lab-environment/labs/README.md) — the Data 360 lab ladder, including the deliberately-over-match lab that makes the privacy failure concrete
- [_cert-data-cloud-consultant/](../../AI_Data/01-data-cloud/_cert-data-cloud-consultant/exam-guide.md) — exam prep. The mapping discipline in set 01 is the heart of that exam
- [04-cross-domain/](../04-cross-domain/INDEX.md) — where this collides with Agentforce and platform limits
