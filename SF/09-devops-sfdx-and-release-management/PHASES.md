# Phases for 09 · DevOps, SFDX & Release Management

25 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

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

## Phase 17 — CI/CD, code quality & release ops · 12 files ✅

```
14-ci-cd-with-github-actions.md                    ⚠️  (upgraded — see below)
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
25-deployment-rollback-hotfix-and-destructive-changes.md   ⚠️  ← beyond plan
```

**One file added, one planned addition dropped — and the drop is the more useful record.** Phase 17 was drafted against the pre-renumber plan and reached the same conclusion phase 16 had: the area taught the pipeline and never taught its boundary. It wrote *Metadata coverage gaps & manual steps*. Phase 16 got there first with **[12](12-metadata-coverage-and-manual-steps.md)**, which is the better note — it has the three-category taxonomy and the per-channel reading of the Coverage Report — so phase 17's version was **deleted rather than merged**, and its four inbound links were repointed at 12. Two phases converging on the same missing topic from opposite ends is the strongest signal in this build that the gap was real.

- **25 · Deployment rollback, hotfix & destructive changes.** The surviving addition, and it sits *above* [05](05-metadata-api-and-deployment-mechanics.md) rather than beside it: 05 owns the destructive manifests and the atomicity guarantee, 25 owns what a team does at 2 a.m. — roll forward from a tag, ship behind a custom metadata kill switch, branch a hotfix from production and merge it back everywhere. No docs page argues that, and *"we'll roll it back"* is said in planning meetings constantly.

**Appended at 25, nothing renumbered.** Phase 16 had just rewritten six inbound references across four areas to land on `· 16`, `· 23` and `· 24`; moving anything again would have invalidated a commit that was one day old for no gain.

**⚠️ corrections as written**
- **14 — upgraded to ⚠️, and it carries two corrections rather than one.** The plan had this unflagged. *"Create a connected app for JWT"* has been Support-gated since Spring '26, and *"pipe `sf org display --verbose` into `grep`"* died on **27 May 2026** with the credential redaction phase 16 found. Both sit in the first ten lines of every CI tutorial written before mid-2026.
- **16** — **Code Analyzer v4 is end-of-life since August 2025.** Stated with phase 16's addition: the `@salesforce/sfdx-scanner` plugin is no longer installed just-in-time, so `sf scanner …` running at all means someone installed it by hand.
- **20** — Release Updates **auto-activate** on their enforcement release. The worked example is the invocable no-arg-constructor requirement: it begins at **API 66.0** — the release-note ID carries `_v66` — and Summer '26 is only when the update auto-activates, which is why it is so widely mis-dated to 67.0.
- **24** — **two directions in one file.** Code Builder was *renamed* Agentforce Vibes IDE, and the Developer Console is *labelled legacy with no announced retirement date*. The phase-15 product-name failure class and the standing "old ≠ dead" class, on the same page.
- **25** — **there is no rollback**, and unlike every other correction in this area nothing changed: the belief was always wrong, so no release note will ever surface it.

**🆕 researched:** **16**, **17** (ApexGuru), **21**, **22**, **23**. The finding that most changed a note was **17**: ApexGuru ships with **Scale Center** — UE production and full-copy sandboxes, Signature Success, Scale Test — and is **not supported on Government Cloud Plus**. Most orgs cannot run it, and almost no write-up leads with that. Logged in [../CURRENCY.md](../CURRENCY.md) as a third failure class: *real, current, correctly described, and unavailable to the reader.*

**Scope notes phase 16 left, and what happened to them**
- **14** carries the redaction fallout and the connected-app gate as its ⚠️, plus `SF_CI_UPDATE_FREQUENCY_MS` / `SF_CI_HEARTBEAT_FREQUENCY_MS` and the npm dist-tag ordering trap. Validate/quick-deploy *mechanics* stayed in [05](05-metadata-api-and-deployment-mechanics.md); 14 links rather than restates.
- **15** carries **`RunRelevantTests` (Beta)** and names its real adoption cost — it is steered by `@IsTest(testFor=…)` annotations nobody backfills onto a legacy suite. The underdocumented failure it leads with is still **parallel test contention**.
- **21** leads with the caps, quoted whole: **20 MB** per log, **24 h** system / **7 days** monitoring retention, **1,000 MB in 15 minutes disables every trace flag in the org**.
- **22** links to [13](13-dx-mcp-server-and-agent-driven-development.md) and to [AI_Data · ADLC](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) and duplicates neither: **13 owns the tool surface, 22 owns the review discipline.**
- **23** is not future-tense — **Hyperforce migration delays ended 1 July 2026.**

**Seed harvest — under phase 16's finding that `_notion-seed/` holds INVENTORY.md and no note bodies.** Two harvests were still possible because the inventory *quotes* what it flags, and both callouts now say so on their face. `Lead Broker Field Migration` (2023) → **19**: renaming a relationship commits you to a report-type deployment, because report types are built on relationship paths. `Salesforce force VSC and Chrome extensions` (2019) → **24**: the list has turned over entirely, and the one durable line is that a browser extension reading your org has your session.

**Area complete.** 25 topics, phases 16–17. Next: 18–19, Experience Cloud.
