# 09 · DevOps, SFDX & Release Management

Source-driven delivery on `sf` v2 and 2GP. **22 topics** · phases [16](PHASES.md), [17](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three retirements define this area.** **`sfdx force:…` is gone** — `sf` v2 uses a different topic grammar. **Change Sets** are superseded by DevOps Center and source-driven pipelines. **1GP packaging** is legacy; 2GP unlocked/managed is the model. Any tutorial using `sfdx force:source:deploy` is teaching a dead CLI.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | `sf` CLI v2 fundamentals 🆕⚠️ | `sf` replaces `sfdx`; new topic grammar, `--json` | 16 |
| 02 | SFDX project structure & source format | `sfdx-project.json`, source vs metadata format | 16 |
| 03 | Org auth & environment management | auth flows, aliases, Dev Hub, headless auth | 16 |
| 04 | Scratch orgs & org shape 🆕 | definition files, features, snapshots | 16 |
| 05 | Metadata API & deployment mechanics | deploy/retrieve, manifests, validate + quick deploy | 16 |
| 06 | Source tracking & sandbox workflow | tracked sandboxes, conflicts, retrieve discipline | 16 |
| 07 | Branching strategy for Salesforce | trunk-based vs gitflow, package-aligned branches | 16 |
| 08 | Unlocked packages (2GP) 🆕⚠️ | 2GP model, versions, dependencies; 1GP legacy | 16 |
| 09 | Managed 2GP & ISV concerns | namespaces, ancestry, push upgrades | 16 |
| 10 | Modularization & dependency strategy | decomposing a monolith org, dependency graphs | 16 |
| 11 | DevOps Center 🆕⚠️ | work items and pipelines replace Change Sets | 16 |
| 12 | CI/CD with GitHub Actions | JWT auth, delta deploys, gates and approvals | 17 |
| 13 | Apex test strategy in CI | RunSpecifiedTests, coverage gates, parallel test contention | 17 |
| 14 | Code Analyzer v5 🆕⚠️ | unified engine config, graph engine, CI wiring | 17 |
| 15 | ApexGuru & performance review 🆕 | hotspot detection and remediation workflow | 17 |
| 16 | Linting, formatting & pre-commit | ESLint for LWC, Prettier apex plugin, hooks | 17 |
| 17 | Code review conventions for metadata | review checklist, diff noise, ownership | 17 |
| 18 | Release management & org upgrades ⚠️ | release windows, Release Updates, preview testing | 17 |
| 19 | Observability, logging & prod debugging 🆕 | log limits, custom logging, Event Monitoring | 17 |
| 20 | Agentforce DX & AI-assisted development 🆕 | agent metadata in source, generated-code review | 17 |
| 21 | Hyperforce & instance operations 🆕 | instance refreshes, maintenance windows, migration prep | 17 |
| 22 | VS Code, Code Builder & tooling ⚠️ | extension pack, Code Builder, retired tooling | 17 |

## Related

- **13** depends on [02-apex · 20–21 testing](../02-apex-and-triggers/INDEX.md).
- **18** pairs with [01-admin · 02 Release cadence & Release Updates](../01-admin-and-declarative-platform/INDEX.md).
- **20** is the seam into [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) — that note already carries the `sf agent` command chain.
- **21** pairs with [08-data · 19 Hyperforce & residency](../08-data-modeling-and-large-data-volumes/INDEX.md) — same platform shift, ops side vs data side.
- **22** overlaps [03-lwc · 21 Local dev](../03-lwc-and-slds/INDEX.md).
- Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Seed notes

[_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) flags `Important commands` (2025) — **check it for `sfdx force:` syntax before reuse**; it likely teaches the retired CLI.
