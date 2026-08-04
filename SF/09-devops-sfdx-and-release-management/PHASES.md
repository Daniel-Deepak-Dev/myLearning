# Phases for 09 · DevOps, SFDX & Release Management

24 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs before Experience Cloud (phases 18–19)**, which assumes 2GP and pipeline vocabulary.
> Currency anchor: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

> ⚠️ **Every command in this area must use `sf` v2 grammar.** Not one `sfdx force:` invocation may appear except inside an explicit "this is retired" correction. Grep the phase output before committing.

---

## Phase 16 — Source-driven dev & 2GP packaging · 13 files ✅

```
01-sf-cli-v2-fundamentals.md                       🆕⚠️
02-sfdx-project-structure-and-source-format.md
03-org-auth-and-environment-management.md          ⚠️  (added, was unflagged)
04-scratch-orgs-and-org-shape.md                   🆕
05-metadata-api-and-deployment-mechanics.md
06-source-tracking-and-sandbox-workflow.md
07-branching-strategy-for-salesforce.md
08-unlocked-packages-2gp.md                        🆕⚠️
09-managed-2gp-and-isv-concerns.md                 🆕  (added — Package Migrations)
10-modularization-and-dependency-strategy.md
11-devops-center.md                                🆕⚠️
12-metadata-coverage-and-manual-steps.md           ⚠️  ← beyond plan
13-dx-mcp-server-and-agent-driven-development.md   🆕  ← beyond plan
```

**Two files added beyond plan, and the phase-17 block renumbered 12–22 → 14–24.**

- **12 · Metadata coverage & the manual-steps problem.** The plan taught the pipeline and never taught its boundary. Every real go-live has a manual-steps runbook, no docs page argues the judgment, and the Metadata Coverage Report is the canonical answer almost nobody checks at the right API version. Without it the area reads as though a green deployment means a finished release.
- **13 · The DX MCP server & agent-driven development.** `@salesforce/mcp` reached GA for its DevOps toolset in **April 2026**, and phase 16's own headline finding — next-generation DevOps Center — is *operated through it*. Leaving it to phase 17's Agentforce DX note would have split one mechanism across two runs; that note owns **reviewing generated code**, this one owns **the tool surface and its blast radius**.

**Renumbering was affordable, barely.** No file in the area existed, and phase 17's files do not exist either — but three other areas already name `09-devops · 14`, `· 21` and `· 22` by number ([07-security · 26](../07-security-and-sharing/26-secure-coding-checklist.md), [03-lwc · 21](../03-lwc-and-slds/21-local-dev-and-lightning-dev-server.md) + its `INDEX.md` and `PHASES.md`, [08-data · 23](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md) + its `INDEX.md`). All six are link **text** over an `INDEX.md` href, so nothing broke structurally — the same situation phase 12 renumbered through. **All six were rewritten in this commit** to `· 16`, `· 24` and `· 23`. Appending at 23–24 instead would have cost nothing but put the deployability boundary after Hyperforce ops, which is the wrong reading order for the one note that stops the rest being over-trusted.

**⚠️ corrections as written**
- **01** — the plan said *"`sfdx force:` is retired"*. Stated at full strength: the commands were **removed on 6 November 2024**, by name, and `sfdx` v7 receives no updates. `@salesforce/cli` still installs an `sfdx` shim, so the binary existing proves nothing.
- **03** — **not in the plan.** The CLI **redacted credentials from command output on 27 May 2026**; `SF_TEMP_SHOW_SECRETS` is a countdown, and every `grep sfdxAuthUrl` CI recipe is broken.
- **08** — 1GP is **legacy, not retired**, and the note says so explicitly.
- **11** — the plan's correction (*"Change Sets are superseded"*) was true and a release out of date. The larger correction is that **DevOps Center stopped being a managed package**: the next-generation release is **native and GA, announced at TDX 2026**. Change Sets remain superseded and **not retired**.
- **12** — coverage moves every release **in both directions**; a remembered answer is not evidence.

**🆕 researched:** **01** (weekly train, removed commands, `template generate` reorg), **04** (shapes vs snapshots, snapshots GA Summer '24), **08**, **09** (Package Migrations GA Summer '25), **11** (TDX 2026 native GA), **13**.

**Seed harvest.** `_notion-seed/` holds **INVENTORY.md only** — no note bodies — so nothing could be harvested verbatim from `Important commands` (2025) or `Package.XML` (2019). The inventory's own flag became the callout in **01**. Worth recording for phases 17–19: the seed corpus is a map, not a corpus.

---

## Phase 17 — CI/CD, code quality & release ops · 11 files ⬜

```
14-ci-cd-with-github-actions.md
15-apex-test-strategy-in-ci.md
16-code-analyzer-v5.md                             🆕⚠️
17-apexguru-and-performance-review.md              🆕
18-linting-formatting-and-pre-commit.md
19-code-review-conventions-for-metadata.md
20-release-management-and-org-upgrades.md          ⚠️
21-observability-logging-and-prod-debugging.md     🆕
22-agentforce-dx-and-ai-assisted-development.md    🆕
23-hyperforce-and-instance-operations.md           🆕
24-vscode-code-builder-and-tooling.md              ⚠️
```

**⚠️ corrections to lead with**
- **16** — **Code Analyzer v5** unified the engines under one config. **v4 is end-of-life**, and the `@salesforce/sfdx-scanner` plugin was removed from the CLI's just-in-time list — so `sf scanner …` now needs a manual install and is teaching a retired tool.
- **20** — Release Updates **auto-enforce**. Preview-window testing is not optional. Pairs with [01-admin · 02](../01-admin-and-declarative-platform/INDEX.md).
- **24** — several tools in the old ecosystem are retired. Name what's current — extension pack, **Live Preview** (renamed from Local Dev), **Web Console (Beta)**, Agentforce Vibes — and don't inventory history.

**🆕 — research before writing:** **16**, **17** (ApexGuru), **21**, **22**, **23**.

**Notes on scope — updated by what phase 16 found**
- **14** must carry the **credential-redaction fallout** from [03](03-org-auth-and-environment-management.md) and the **connected-app gate** on JWT setup; also `SF_CI_UPDATE_FREQUENCY_MS` / `SF_CI_HEARTBEAT_FREQUENCY_MS` for CI-aware output, and the **npm dist-tag ordering trap** — pinning the CLI version in CI is not optional.
- **15** — the underdocumented failure is **parallel test contention** in CI. Depends on [02-apex · 20–21](../02-apex-and-triggers/INDEX.md). **`RunRelevantTests` is Beta** and pairs with quick deploy → [05](05-metadata-api-and-deployment-mechanics.md).
- **21** — the real constraint is that **debug logs are capped and expire**; production debugging needs a custom logging strategy plus Event Monitoring. Say so.
- **22** — seam into [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) and into [13](13-dx-mcp-server-and-agent-driven-development.md). **Link, don't duplicate** — this note owns the *review discipline for generated code*; 13 owns the tool surface.
- **23** pairs with [08-data · 23](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md): same platform shift, ops side vs data side. **Hyperforce migration delays ended 1 July 2026**, so this is not a future-tense topic.
