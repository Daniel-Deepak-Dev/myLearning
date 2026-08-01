# Currency — what "current" means here

Everything in `SF/` targets **Summer '26 · API 67.0**. Last reviewed **2026-08-01**.

## Version map

| Release | API | Notes |
|---|---|---|
| Winter '26 | 65.0 | |
| Spring '26 | 66.0 | |
| **Summer '26** | **67.0** | **The target.** Security defaults flipped here. |
| Winter '27 | 68.0 | Not yet GA — preview only. Nothing here should assume it. |

Older mapping for reading legacy code: Spring '24 = 60.0, Summer '24 = 61.0, Winter '25 = 62.0, Spring '25 = 63.0, Summer '25 = 64.0.

## The six defaults that invalidate older tutorials

Anything written before ~2024 will get at least one of these wrong. Every ⚠️-flagged note opens by correcting the relevant one.

| # | Was | Is now | Where it bites |
|---|---|---|---|
| 1 | Apex SOQL/DML ran in **system mode** | **User mode is the default at API 67.0** — elevated access is opt-in | [02-apex](02-apex-and-triggers/INDEX.md), [07-security](07-security-and-sharing/INDEX.md) |
| 2 | Keyword-less class **inherited** caller's sharing | Defaults to **`with sharing`**; bypass is a deliberate `without sharing` | [02-apex](02-apex-and-triggers/INDEX.md) |
| 3 | `WITH SECURITY_ENFORCED` | **Retired — no longer compiles.** Use `WITH USER_MODE` | [02-apex](02-apex-and-triggers/INDEX.md) |
| 4 | **Locker Service** | **Lightning Web Security (LWS)** | [03-lwc](03-lwc-and-slds/INDEX.md) |
| 5 | **CometD** streaming | **Pub/Sub API** (gRPC) | [06-integration](06-integration-and-apis/INDEX.md) |
| 6 | `sfdx force:…` | **`sf` CLI v2** topic grammar | [09-devops](09-devops-sfdx-and-release-management/INDEX.md) |

Detail, sources and dates for all six: [AI_Data/05-release-radar/trust-security-and-governance.md](../AI_Data/05-release-radar/trust-security-and-governance.md) and [developer-tooling-and-apis.md](../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Retirements to know

- **Workflow Rules & Process Builder** — retired; Flow is the only declarative automation tool. → [04-flow](04-flow-and-automation/INDEX.md)
- **Aura templates for new Experience Cloud sites** — LWR is the default. → [05-experience-cloud](05-experience-cloud-lwr/INDEX.md)
- **Connected Apps for new integrations** — superseded by External Client Apps. → [06-integration](06-integration-and-apis/INDEX.md)
- **Change Sets** — superseded by DevOps Center / source-driven pipelines. → [09-devops](09-devops-sfdx-and-release-management/INDEX.md)
- **1GP packaging** — legacy; 2GP unlocked/managed is the model. → [09-devops](09-devops-sfdx-and-release-management/INDEX.md)
- **SOAP `login()`** — retirement announced for Summer '27.

## Keeping this file honest

When a phase discovers a currency fact, it goes **here** as a row and into the relevant note — not duplicated into five notes. If it's genuinely new news rather than a stable fact, it belongs in [AI_Data/05-release-radar/](../AI_Data/05-release-radar/README.md) instead and this file links to it.
