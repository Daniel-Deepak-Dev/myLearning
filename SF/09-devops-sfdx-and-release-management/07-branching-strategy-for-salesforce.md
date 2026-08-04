# Branching Strategy for Salesforce

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** An argued opinion about branches, environments and merges on this platform. There is no docs page for this; the value is the reasoning. The pipeline that enforces it is [11](11-devops-center.md).

## Core idea

Salesforce breaks two assumptions that every general-purpose branching model rests on.

**The environment is shared mutable state.** Admins configure in a sandbox, not in a branch. A branch can hold their work only after someone retrieves it, and until then the environment *is* the source of truth — the reverse of every git workflow ever written.

**Metadata merges badly.** It is generated XML with ordering that is not stable, elements that carry no identity, and several types (profiles, permission sets, custom labels, flows) that arrive as one enormous file. Git can merge it textually; it cannot merge it *meaningfully*. A flow with a three-way conflict is generally faster to rebuild than to resolve.

Both push in the same direction: **short-lived branches, small changes, frequent integration.** Long-lived branches on this platform do not diverge, they rot.

## How it works

| Model | Fits | Cost |
|---|---|---|
| **Trunk-based**, feature branches of 1–3 days, scratch org per branch | pro-code teams, packaged source | needs real test automation and scratch org discipline |
| **Environment branches** (`dev` → `int` → `uat` → `main`), one branch per org | admin-heavy teams, DevOps Center orgs | branches drift; each promotion is a merge, not a deploy |
| **Release branches** cut per Salesforce release | regulated release trains | conflicts accumulate for the length of the train |

- **Package-aligned branches** only make sense once the source is genuinely modular — one repo per package, or one directory per package with independent versioning → [10](10-modularization-and-dependency-strategy.md).
- **The hotfix path is not optional.** Production diverges the moment someone fixes something in Setup at 2am; decide in advance whether that lands on `main` and is merged back, or is re-done through the pipeline.
- **Decompose the conflict-prone types** — `sourceBehaviorOptions` for permission sets, custom labels, sharing rules and workflows removes whole categories of collision → [02](02-sfdx-project-structure-and-source-format.md).

## Gotchas

- **Environment branches are not a strategy, they are a mapping.** They tell you where code is, not how it gets integrated, and they hide the fact that `uat` and `main` have silently different content.
- **Declarative work cannot be branched.** Two admins in one sandbox are working on one branch whether or not the repo says so — separate sandboxes are the only real isolation, and they cost.
- **`.forceignore`d metadata is invisible to every branch.** Ignoring profiles removes the conflicts and removes the review; the trade is deliberate, not free.
- **Reverting a merge does not revert an org.** Git reverts source; the deployed component stays until something deploys over it or a destructive change removes it → [05](05-metadata-api-and-deployment-mechanics.md).
- **Salesforce's three releases a year are not your release train**, but they set immovable dates for preview testing and Release Updates.
- **A long-lived branch's Apex still compiles against the org it deploys to**, so a branch cut before a Release Update lands can pass CI in a stale sandbox and fail in production.
- **The org's audit trail attributes every deployed change to the deploying user**, so git history is the only real record of who changed what → [01-admin · 17](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md).

## Recall

Q: Why do long-lived branches fail worse on Salesforce than elsewhere?
A: Metadata is generated XML with unstable ordering and monolithic files, so it merges textually but not meaningfully — divergence becomes unresolvable rather than merely painful.

Q: What does an environment-branch model actually give you?
A: A mapping from branch to org. It does not define an integration strategy, and it lets environments drift while looking orderly.

Q: What is the honest limit of branching for declarative work?
A: Admins configure in a shared sandbox. Isolation costs another sandbox; a branch cannot provide it.

Q: Which project-level change most reduces merge conflicts?
A: Decomposing the monolithic types — permission sets, custom labels, sharing rules, workflows — via `sourceBehaviorOptions`.

Q: Does reverting a merge undo a deployment?
A: No. It changes source only; the org keeps the component until something deploys over it or deletes it destructively.

## Related

- [02 · SFDX project structure & source format](02-sfdx-project-structure-and-source-format.md) — decomposition as conflict prevention
- [06 · Source tracking & sandbox workflow](06-source-tracking-and-sandbox-workflow.md) — how work leaves a shared sandbox
- [10 · Modularization & dependency strategy](10-modularization-and-dependency-strategy.md) — when branches should follow packages
- [11 · DevOps Center](11-devops-center.md) — a pipeline that picks the model for you
