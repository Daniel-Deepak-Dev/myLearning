---
vault: SF_core
area: 09-devops-sfdx-and-release-management
format: dense
status: learning
created: 2026-08-04
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 16
tags: [currency-new, currency-warning]
---
# DevOps Center

**Scope:** Salesforce's own change-and-release product — work items, pipelines and what it does to your repo. The CI/CD you build yourself is [14 CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md).

> **What changed — twice, and the second one is recent.** **DevOps Center is no longer a managed package.** The **Next-Generation DevOps Center**, announced at **TDX 2026 (April 2026)** and **generally available**, is a **native platform capability**: nothing to install, no package version to manage, enabled in the hub org and immediately usable. Everything written between its December 2022 GA and early 2026 describes the managed-package product with a fixed pipeline and GitHub as the only option. And the older ⚠️ still stands with a correction of its own: **Change Sets are superseded, not retired.** They still work, and Salesforce has announced no end-of-life for them.

## Core idea

DevOps Center replaces "pick components in a Change Set" with **a work item that owns a set of changes and a pipeline that promotes it**. You work in a development sandbox; DevOps Center watches source tracking, lets you select changed components, **commits them to a real git branch**, and promotes that branch through pipeline stages, each mapped to an org.

The design decision that makes it interesting to a developer, not just an admin, is that **the repository is not a black box**. The commits are ordinary commits in your own GitHub repository, so a pro-code team can run its CLI, its reviews and its CI against exactly the same branches an admin is clicking through.

## How it works

- **Work item** — the unit of change: a branch, a selected component set, a review, and a position in the pipeline.
- **Pipeline** — ordered stages, each bound to an org and a branch. The next-generation release makes stage structure **customisable** rather than fixed, so a real governance model can be expressed.
- **Change Bundle** — groups work items that must move together, promoted or **rolled back across connected orgs as one unit**. This is the answer to the classic "these three work items are one release" problem.
- **Version control hosts** — **GitHub.com is GA**, **Bitbucket Cloud is Beta**, **GitLab and Azure DevOps are roadmap**, not shipped.
- **Agentic operation** — DevOps Center exposes tools through the **Salesforce DX MCP Server**, so a coding agent can manage work items, reason about conflicts and diagnose deployment failures → [13](13-dx-mcp-server-and-agent-driven-development.md).

## 2026 currency

The move from managed package to native capability is the substantive change: no install, no upgrade cycle, no separate configuration surface, and the product is now on the platform's release train instead of its own. Read the older material with that in mind — the criticisms that stuck to DevOps Center in 2023–24 (fixed pipeline, GitHub-only, no grouping of work items, no rollback story) are precisely what the next-generation release addresses. Verify feature-by-feature rather than by reputation, in either direction.

**Beginning October 2026 the product is called Lifecycle Center** (formerly Next-Generation DevOps Center). Help warns that *DevOps Center*, *DevOps Project* and *DevOps Pipeline* still appear during the transition, so search both names. New installs of the **DevOps Center managed package** have been unsupported since April 2026; an existing install keeps working, and moving its projects into Lifecycle Center is a **Developer Preview**. Lifecycle Center is not available in the EU Operating Zone. Winter '27's **governance for coding agents** (policies, approvals, audit log) is **not GA** — the release-note change log says Beta and the Help page says Developer Preview — so it is not yet a production control.

## Gotchas

- **It is free and it is not a full DevOps platform.** No test orchestration, no static analysis, no data seeding, no environment provisioning. Those remain [14 CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md), [16 Code Analyzer v5](16-code-analyzer-v5.md) and [08-data · 20](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md), or a paid vendor.
- **It commits what you select, not what changed.** A component nobody ticked is not in the work item, and the pipeline is perfectly happy — the same failure mode as a Change Set, one layer up.
- **It owns the branches it creates.** Pushing to a work-item branch by hand desynchronises the UI from the repository, and the UI is what governs the promotion.
- **Anything outside the Metadata API is still manual.** A pipeline does not change what is deployable → [12](12-metadata-coverage-and-manual-steps.md).
- **Bitbucket Cloud support is Beta**, which means Beta Services Terms — not a supported production dependency.
- **Change Sets still exist**, so an inherited org may be running both, and the same component moving by two routes is a genuine conflict nobody is watching.
- **Deployed flows are still inactive** unless production's *Deploy processes and flows as active* is set — the pipeline does not change that → [04-flow · 24](../04-flow-and-automation/24-flow-deployment-versioning-and-governance.md).

## Recall

Q: What is the single biggest change in Next-Generation DevOps Center?
A: It is native — a platform capability with nothing to install — instead of a managed package. GA, announced at TDX 2026, and renamed **Lifecycle Center** from October 2026.

Q: Are Change Sets retired?
A: No. They are superseded by DevOps Center and source-driven pipelines, and no end-of-life has been announced.

Q: Which version control hosts does DevOps Center support today?
A: GitHub.com is GA, Bitbucket Cloud is Beta, GitLab and Azure DevOps are on the roadmap.

Q: What problem does a Change Bundle solve?
A: Work items that must ship together — it promotes or rolls them back across connected orgs as a single deployment unit.

Q: Why can a pro-code team share a repo with DevOps Center?
A: It writes ordinary commits to ordinary branches in your own repository, so the CLI, reviews and CI all operate on the same branches.

## Related

- [07 · Branching strategy for Salesforce](07-branching-strategy-for-salesforce.md) — the model DevOps Center imposes if you let it
- [13 · The DX MCP server & agent-driven development](13-dx-mcp-server-and-agent-driven-development.md) — how it is operated agentically
- [14 · CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md) — what DevOps Center does not do
- [01-admin · 02 Release cadence & Release Updates](../01-admin-and-declarative-platform/INDEX.md) — the other calendar a pipeline lives inside

## Sources

- [Lifecycle Center](https://help.salesforce.com/s/articleView?language=en_US&id=platform.next_generation_devops_center.htm&type=5) — Salesforce Help · via search 2026-10-28 · *"Beginning October 2026, DevOps Center is changing its name to Lifecycle Center"*; old names still appear during the transition; managed-package installs unsupported since April 2026; migration is Developer Preview; governance section labelled Developer Preview; not in the EU Operating Zone
- [Set Up Bitbucket as Your Source Control](https://help.salesforce.com/s/articleView?id=platform.devops_center_setup_bitbucket_as_source_control.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-28 · Lifecycle Center supports Bitbucket Cloud; the overview still lists *Review Changes in Bitbucket (Beta)*
- [Release Note Changes](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_change_log.htm&type=5) — Salesforce Help · via search 2026-10-28 · *Govern Coding Agents at Scale with Lifecycle Center Governance (Beta)*, added week of 28 Sep 2026
- [Winter '27 Release: Top Development & Security Features](https://www.salesforce.com/blog/platform-winter-27-release/) — Salesforce · via search 2026-10-28 · calls it *Lifecycle Center (formerly DevOps Center)*; its blanket "GA unless noted" claim conflicts with the change log for governance

## History

- 2026-10-28 · Winter '27 currency check: renamed Lifecycle Center from October 2026; managed-package installs closed; coding-agent governance marked not GA
