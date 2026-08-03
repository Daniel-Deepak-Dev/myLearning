# Phases for 09 · DevOps, SFDX & Release Management

22 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs before Experience Cloud (phases 18–19)**, which assumes 2GP and pipeline vocabulary.
> Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

> ⚠️ **Every command in this area must use `sf` v2 grammar.** Not one `sfdx force:` invocation may appear except inside an explicit "this is retired" correction. Grep the phase output before committing.

---

## Phase 16 — Source-driven dev & 2GP packaging · 11 files ⬜

```
01-sf-cli-v2-fundamentals.md                       🆕⚠️
02-sfdx-project-structure-and-source-format.md
03-org-auth-and-environment-management.md
04-scratch-orgs-and-org-shape.md                   🆕
05-metadata-api-and-deployment-mechanics.md
06-source-tracking-and-sandbox-workflow.md
07-branching-strategy-for-salesforce.md
08-unlocked-packages-2gp.md                        🆕⚠️
09-managed-2gp-and-isv-concerns.md
10-modularization-and-dependency-strategy.md
11-devops-center.md                                🆕⚠️
```

**⚠️ corrections to lead with**
- **01** — **`sfdx force:…` is retired.** `sf` v2 uses a different topic grammar (`sf project deploy start`, not `sfdx force:source:deploy`). Include a small old→new mapping table; it's the highest-utility half-page in the area.
- **08** — **1GP is legacy.** 2GP unlocked packages are the model for org modularization.
- **11** — **Change Sets are superseded.** DevOps Center's work-item/pipeline model replaces them.

**🆕 — research before writing:** **01** (current command surface), **04** (org shape, features, **snapshots**), **08**, **11**.

**Notes on scope**
- **02** — the genuinely confusing part is **source format vs metadata format**, and when a conversion is still required. Lead with that.
- **05** — **validate + quick deploy** is the single most useful mechanic here for real release work.
- **07, 10** are judgment topics with no docs page. Their value is an opinion, honestly argued: when a monolith should stay a monolith.

**Seed harvest** ([../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md)) — `Important commands` (2025) → **01**, but **check it for retired `sfdx force:` syntax first**; it may be exactly what the correction is for. `Package.XML` (2019) → **05**.

---

## Phase 17 — CI/CD, code quality & release ops · 11 files ⬜

```
12-ci-cd-with-github-actions.md
13-apex-test-strategy-in-ci.md
14-code-analyzer-v5.md                             🆕⚠️
15-apexguru-and-performance-review.md              🆕
16-linting-formatting-and-pre-commit.md
17-code-review-conventions-for-metadata.md
18-release-management-and-org-upgrades.md          ⚠️
19-observability-logging-and-prod-debugging.md     🆕
20-agentforce-dx-and-ai-assisted-development.md    🆕
21-hyperforce-and-instance-operations.md           🆕
22-vscode-code-builder-and-tooling.md              ⚠️
```

**⚠️ corrections to lead with**
- **14** — **Code Analyzer v5** unified the engines under one config. Older PMD/`sfdx scanner` guidance describes a different tool.
- **18** — Release Updates **auto-enforce**. Preview-window testing is not optional. Pairs with [01-admin · 02](../01-admin-and-declarative-platform/INDEX.md).
- **22** — several tools in the old ecosystem are retired. Name what's current; don't inventory history.

**🆕 — research before writing:** **14**, **15** (ApexGuru), **19**, **20**, **21**.

**Notes on scope**
- **13** — the underdocumented failure is **parallel test contention** in CI. Depends on [02-apex · 20–21](../02-apex-and-triggers/INDEX.md).
- **19** — the real constraint is that **debug logs are capped and expire**; production debugging needs a custom logging strategy plus Event Monitoring. Say so.
- **20** — seam into [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md), which already carries the `sf agent` command chain and the five ADLC phases. **Link, don't duplicate** — this note owns the *review discipline for generated code*, which that one doesn't cover.
- **21** pairs with [08-data · 23](../08-data-modeling-and-large-data-volumes/INDEX.md) *(phase 15)*: same platform shift, ops side vs data side.
