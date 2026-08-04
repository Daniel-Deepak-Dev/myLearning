# 09 · DevOps, SFDX & Release Management

Source-driven delivery on `sf` v2 and 2GP. **24 topics** · phases [16](PHASES.md), [17](PHASES.md).

> Currency: **Summer '26 (API 67.0)** · [flag legend](../README.md#flag-legend) · [what changed](../CURRENCY.md)

> ⚠️ **Three shifts define this area, and only one of them is a retirement.** **`sfdx force:…` commands were removed on 6 November 2024** — `sf` v2 uses a different topic grammar, and `sfdx` v7 gets no updates. **Change Sets are superseded** by DevOps Center and source-driven pipelines, but **not retired** and with no announced end of life. **1GP packaging is legacy** — 2GP unlocked/managed is where new capability lands — and it is **not retired either**. Any tutorial using `sfdx force:source:deploy` is teaching a dead CLI; any tutorial calling Change Sets or 1GP dead is overstating.

| # | Topic | Scope | Phase |
|---|---|---|---|
| 01 | [`sf` CLI v2 fundamentals](01-sf-cli-v2-fundamentals.md) 🆕⚠️ | `sf` replaces `sfdx`; topic grammar, config precedence, `--json`, weekly train | 16 |
| 02 | [SFDX project structure & source format](02-sfdx-project-structure-and-source-format.md) | `sfdx-project.json`, source vs metadata format, `.forceignore`, decomposition | 16 |
| 03 | [Org auth & environment management](03-org-auth-and-environment-management.md) ⚠️ | auth flows, aliases, Dev Hub, headless JWT, **secrets redacted since May 2026** | 16 |
| 04 | [Scratch orgs & org shape](04-scratch-orgs-and-org-shape.md) 🆕 | definition files, features, shapes, snapshots, Dev Hub allocations | 16 |
| 05 | [Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) | manifests, destructive changes, **validate + quick deploy**, size limits | 16 |
| 06 | [Source tracking & sandbox workflow](06-source-tracking-and-sandbox-workflow.md) | tracked orgs, conflicts, reset, **Source Mobility** | 16 |
| 07 | [Branching strategy for Salesforce](07-branching-strategy-for-salesforce.md) | trunk-based vs environment branches, why metadata merges badly | 16 |
| 08 | [Unlocked packages (2GP)](08-unlocked-packages-2gp.md) 🆕⚠️ | 2GP model, beta→released, coverage gate, org-dependent; 1GP legacy | 16 |
| 09 | [Managed 2GP & ISV concerns](09-managed-2gp-and-isv-concerns.md) 🆕 | namespaces, ancestry, push upgrades, **Package Migrations GA Summer '25** | 16 |
| 10 | [Modularization & dependency strategy](10-modularization-and-dependency-strategy.md) | when to decompose, base-package pattern, dependency pinning | 16 |
| 11 | [DevOps Center](11-devops-center.md) 🆕⚠️ | **next-generation release is native, GA at TDX 2026**; work items, change bundles | 16 |
| 12 | [Metadata coverage & manual steps](12-metadata-coverage-and-manual-steps.md) ⚠️ | what a pipeline cannot carry, the Coverage Report, the runbook | 16 |
| 13 | [The DX MCP server & agent-driven development](13-dx-mcp-server-and-agent-driven-development.md) 🆕 | `@salesforce/mcp`, toolsets, org allowlist, per-toolset maturity | 16 |
| 14 | CI/CD with GitHub Actions | JWT auth, delta deploys, gates and approvals | 17 |
| 15 | Apex test strategy in CI | RunSpecifiedTests, coverage gates, parallel test contention | 17 |
| 16 | Code Analyzer v5 🆕⚠️ | unified engine config, graph engine, CI wiring | 17 |
| 17 | ApexGuru & performance review 🆕 | hotspot detection and remediation workflow | 17 |
| 18 | Linting, formatting & pre-commit | ESLint for LWC, Prettier apex plugin, hooks | 17 |
| 19 | Code review conventions for metadata | review checklist, diff noise, ownership | 17 |
| 20 | Release management & org upgrades ⚠️ | release windows, Release Updates, preview testing | 17 |
| 21 | Observability, logging & prod debugging 🆕 | log limits, custom logging, Event Monitoring | 17 |
| 22 | Agentforce DX & AI-assisted development 🆕 | agent metadata in source, generated-code review | 17 |
| 23 | Hyperforce & instance operations 🆕 | instance refreshes, maintenance windows, migration prep | 17 |
| 24 | VS Code, Code Builder & tooling ⚠️ | extension pack, Web Console, retired tooling | 17 |

## Related

- **[03](03-org-auth-and-environment-management.md)** collides with [06-integration · 16 External Client Apps](../06-integration-and-apis/16-external-client-apps.md) — the classic JWT runbook says "create a connected app", which is Support-gated since Spring '26.
- **[12](12-metadata-coverage-and-manual-steps.md)** is the honest counterweight to every pipeline note in the area.
- **15** depends on [02-apex · 20–21 testing](../02-apex-and-triggers/INDEX.md).
- **20** pairs with [01-admin · 02 Release cadence & Release Updates](../01-admin-and-declarative-platform/INDEX.md).
- **[13](13-dx-mcp-server-and-agent-driven-development.md)** and **22** are the seam into [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) — that note carries the `sf agent` command chain.
- **23** pairs with [08-data · 23 Hyperforce, residency & data locality](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md) — same platform shift, ops side vs data side. **Migration delays ended 1 July 2026.**
- **24** overlaps [03-lwc · 21 Local dev](../03-lwc-and-slds/INDEX.md).
- Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

## Seed notes

[_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) flags `Important commands` (2025), `Package.XML` (2019), `Salesforce force VSC and Chrome extensions` (2019) and `Local Dev` (2024). **The vault holds the inventory line only, not the note bodies** — so phase 16 could not harvest them verbatim. The inventory's own warning is the usable lesson and is quoted in [01](01-sf-cli-v2-fundamentals.md): a 2025 command cheatsheet is not automatically safe, because `force:source:*` had already been removed for over a year when it was written.
