# Data 360 Orientation — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Salesforce's lakehouse platform that ingests → models → unifies → derives insight → activates customer data — repositioned in 2026 from a passive data store into the **context engine that grounds AI agents**.

## Key terms
| Term | Definition |
|---|---|
| Data 360 | The current name (Dreamforce 2025). Sixth in the lineage; same product as Data Cloud. |
| Lakehouse | Lake's cheap open storage + warehouse's query performance and governance. |
| Unified profile | One individual after identity resolution. **Also the billing unit** (~$240/1,000). |
| Accelerated Data Ingest | Real-time CRM data, no pipeline lag. **GA** in Summer '26. |
| Data Cloud One | One Data 360 instance shared across orgs: one **home org** holds the tenant, **companion orgs** consume selected data spaces. |
| Home / companion org | Home does all ingestion, resolution and governance. Companions get **metadata, not data** — 3 connections included. |

## Rules of thumb

- **The grounding is the product.** Agent quality is capped by data freshness, resolution quality and chunking strategy.
- Data 360 is the system of **context**; CRM stays the system of **record**. Not a replacement.
- **Check the monthly release notes**, not just the three seasonal ones — most Data 360 changes ship monthly.
- Read Beta labels literally: AWS Glue federation is **GA** (proposal-safe), Fabric OneLake is **Beta** (prototype only).
- Multi-org: you're not choosing an **owner**, you're choosing a **partition boundary** — brand, region or legal entity. Near-irreversible.

## Exam traps / common confusions

- **The cert is now Data 360 Consultant** (renamed 2026-03-27) — exam code `Data-Con-101` unchanged.
- Six names all still circulate: Customer 360 Audiences → Salesforce CDP → Marketing Cloud CDP → Genie → Data Cloud → **Data 360**.
- Trailhead and much documentation still say "Data Cloud." Lag, not error.
- **DLOs ≠ Platform objects** — different null/empty-string semantics, and dataspace is required when querying them.
- A "profile" for billing is a **unified individual after resolution**, not a raw source row.
- **Data Cloud One residency follows the HOME org's region**, not the companion's — the trap that disqualifies the pattern for regulated EU/UK subsidiaries.
- **A data space is not access control.** For "different teams see different data" use permission sets; keep the unified profile intact.
- Sandbox home ↔ sandbox companions only; production ↔ production. No crossing.

## Minimal example

```
CRM · Marketing Cloud · S3 · web SDK · Snowflake
                    ↓  ingest
              DSO → DLO → DMO          (model)
                    ↓  identity resolution
              UNIFIED PROFILE          (unify)
                    ↓  calculated insights + semantic layer
                    ↓  activate
        Marketing/ads  ·  CRM  ·  AGENT GROUNDING
```

## Multi-org shape

```
   HOME ORG  ──  tenant + ingest + identity resolution + governance
        │
        ├── data space EMEA ──→ companion org 1
        ├── data space AMER ──→ companion org 2
        └── data space Brand-X  (not shared)
```
