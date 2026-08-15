# Watchlist — what the radar checks, and where each thing stands

**This file is state, not news.** Every scan updates it **in place**: bump `Last checked`, change
`Current state` only when it actually changed. `git log -p watchlist.md` is the audit trail.

**The rule this file exists to enforce:** an artifact that has not changed is **never** restated in a
dated scan note, a topic file or the README. It gets its cell bumped here and nothing else. A version
number, dist-tag position or commit hash that has not changed behaviour is state, not a finding.

A row earns prose elsewhere only when it **closes an open question** or **contradicts something the radar
already published**. Then it becomes a topic-file entry or a `> **Correction**`, and this row records the
new state.

## Salesforce DX — npm

| Artifact | Current state | Last checked (UTC) | Watching for |
|---|---|---|---|
| `@salesforce/cli` dist-tags | `latest` **2.147.7** · `latest-rc` **2.148.3** · `nightly` **2.149.3** (08-15 02:39) | 2026-08-15 03:38 | Stable ships **Wednesdays**. `2.148.3` → `latest` due **2026-08-19**; the `plugin-deploy-retrieve` 4.1.x line → `latest` due **2026-08-26** |
| `@salesforce/source-deploy-retrieve` | **13.1.1** · `13.1.2` and `12.37.3` both HTTP 404 | 2026-08-15 03:55 | Still **no 12.x backport** of the zip-slip. A third path-escape fix in `staticResourceMetadataTransformer.ts` |
| `@salesforce/plugin-deploy-retrieve` | **4.1.2** (08-14 03:31) · `4.1.3` HTTP 404 | 2026-08-15 03:55 | Reaching `latest-rc`, which is when `--root-type-with-dependencies` becomes usable without a nightly build |
| `@salesforce/plugin-agent` | **2.0.2** | 2026-08-15 03:38 | Further `--api-name` vs `--authoring-bundle` divergence |
| `@salesforce/agents` | **2.0.2** | 2026-08-15 03:38 | As above — two preview clients that do not behave alike |
| `@salesforce/core` | **9.1.2** (08-11 21:02) | 2026-08-15 03:38 | Auth, connection and API-version resolution changes |
| `forcedotcom/cli` release notes | Top entry **`## 2.148.3 (August 19, 2026) [stable-rc]`** | 2026-08-15 03:41 | Lags npm by ~3 days and dates versions by **planned stable date, not publish date** — read npm for what shipped |

## Repositories

| Artifact | Current state | Last checked (UTC) | Watching for |
|---|---|---|---|
| `salesforce/sf-pi` | **v0.266.1**, 2026-08-14 (`code-analyzer` timer fix) | 2026-08-15 03:50 | `sf-data360` and the four unexamined siblings — `sf-soql`, `sf-data-explorer`, `sf-brain`, `sf-guardrail` beyond its command gate. The `CHANGELOG` keeps shipped work under a permanent `## Unreleased` heading |
| `salesforce/agentscript` | `main` **`90d54a7`**, 2026-08-03 (CODEOWNERS chore) | 2026-08-15 03:52 | Any product change. Idle 12 days |
| `forcedotcom/sf-skills` | **1.38.0** · releases **weekly, Fridays** | 2026-08-15 03:56 | New skills, `metadata.relatedSkills`, `accessCheck`, `cliTools`, `mcpTools`, and the `plugins/builder/` marketplace gaining a second plugin |
| `SalesforceAIResearch/agentforce-adlc` | `main` **`d16d14a`**, 2026-07-30 (PR #47 sync) | 2026-08-15 03:53 | Any commit. **Idle 16 days.** Note the CC BY-NC 4.0 licence — `sf-skills` is the commercial-safe copy |
| `SalesforceAIResearch/gift-eval` | `main` **`26df758`**, 2026-08-13 (TAFSUT #195) | 2026-08-15 03:54 | Harness, submission-protocol or licence changes. Third-party leaderboard submissions do **not** clear the bar |
| `salesforce/next-gen-wealth` (Agentic Advisor) | No change surfaced | 2026-08-10 03:46 | The one public worked example of Data-360-grounded fail-safe prompt templates |
| `salesforce/AgentforceMobileSDK-Android` | **262.1.2** / tag `v15.130.1`, 2026-07-31 | 2026-08-05 03:06 | Read the git tag, not the release title — patch-shaped names have hidden majors |
| `forcedotcom/salesforcedx-vscode` | `develop` **`507721b`**, 2026-08-04, unreleased | 2026-08-05 03:07 | Apex/SOQL language-server behaviour reaching a release |
| SDR `METADATA_SUPPORT.md` | v68 list: **21 of 59** new types DX-supported | 2026-08-14 03:52 | Each minor that flips one of the 37 unsupported types to ✅ — incl. `AiAgentDefinitionPlanner` and the four telephony-provider types |

## Announcements and docs

| Artifact | Current state | Last checked (UTC) | Watching for |
|---|---|---|---|
| Salesforce newsroom / press | Newest relevant item **2026-08-05** (Army HRC, IL5) | 2026-08-15 03:52 | Quiet for 13 consecutive scans. `salesforce.com` returns 403 to automated fetching — negatives here are weaker than GitHub ones |
| Data 360 release notes | No new monthly section reachable | 2026-08-15 03:47 | `help.salesforce.com` is unreadable to automated fetching. Two Summer '26 titles (*Currency Reporting*, *Result Reuse for Data 360 Live*) are blocked on this — see README open questions |
| `mcpTools` frontmatter (`sf-skills`) | **5** servers named; **no `data360-*` server** | 2026-08-15 03:56 | An early-warning channel — it named four MCP servers before any announcement. A `data360-*` or agent-specific server appearing here |
| CVE / GitHub advisory for `W-23808206` | None located | 2026-08-15 03:55 | The zip-slip and TOCTOU fixes still ship with no advisory |

## Watched, not recorded — with a re-check date

An item belongs here only with a date. **No date means it is not worth watching**, and it goes nowhere.

| Item | Why it failed the bar | Re-check by |
|---|---|---|
| `plugin-deploy-retrieve` 4.1.x → stable | Queued behind `nightly`; nothing usable until it lands | 2026-08-26 |
| Six unnamed `sf-skills` 1.38.0 skills | GitHub truncates the `skills/` tree at 100 entries and the 1.37.0…1.38.0 compare fails to render | Next `sf-skills` release |
| *Salesforce AI Research at ICLR 2026* (21 papers) | Blog roundup, no artifact identifiers, no repo, no licence | When individual papers get named repos |
| Winter '27 Release Update list | Full list not enumerable from this environment | 2026-08-30 — Setup → Release Updates in a preview org |
