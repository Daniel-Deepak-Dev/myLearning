# Metadata Coverage & the Manual-Steps Problem

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** What a pipeline cannot carry, how to find out before release night, and the runbook that covers the gap. The deployment mechanics themselves are [05](05-metadata-api-and-deployment-mechanics.md).

> **What changed — and it keeps changing, which is the point.** *"If you can configure it in Setup, you can deploy it"* has never been true, and the shape of the exception moves **every release, in both directions**. The authority is the **Metadata Coverage Report**, which is published **per API version** and has separate columns for Metadata API, source tracking, Change Sets, unlocked packages and managed packages — a type can be supported in one and not another. A remembered answer from 2021, in either direction, is not evidence: coverage has been added since, and packaging support has been added faster than Metadata API support for the newer Agentforce types.

## Core idea

Every real Salesforce go-live has a **manual-steps document**, and teams that pretend otherwise discover it at the worst moment. Three separate things hide behind "we'll just deploy it":

**Not covered** — the metadata type does not exist, so nothing can carry it. **Covered but not round-trippable** — it deploys, but what you retrieve is not what you deployed, so the repo cannot be the source of truth. **Covered but not sufficient** — the component lands and something else has to happen before it does anything.

The skill is not memorising the list. It is knowing the three categories, checking the report **for the API version you deploy at**, and rehearsing in an org that resembles production.

## How it works

| Category | Examples | What to do |
|---|---|---|
| **One-way feature enablement** | Person Accounts, multi-currency, state/country picklists | decide once, rehearse in a Full sandbox, never in production first |
| **Secrets and keys** | named credential passwords, certificate private keys | provisioned per environment, never in git |
| **Runtime state, not metadata** | scheduled Apex jobs, custom setting *records* | scripted post-deploy; note CMDT records **are** deployable → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) |
| **Deployed but inert** | flows without *Deploy processes and flows as active* | activation step in the runbook → [04-flow · 24](../04-flow-and-automation/24-flow-deployment-versioning-and-governance.md) |
| **Retrieved as a subset** | profiles | manage access in permission sets → [07-security · 03](../07-security-and-sharing/03-profiles-and-the-permission-set-led-model.md) |

- **The runbook has three sections** — pre-deploy (things that must exist first), deploy, post-deploy (activation, scheduling, secrets, data) — each step with a named owner and a way to verify it.
- **Rehearse where it counts.** A step that only exists in production is a step that has never been tested; a Full sandbox is the closest available proxy → [08-data · 20](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md).
- **Convert steps into automation one at a time** — an anonymous Apex script for scheduling, a `replacements` entry for an endpoint, a data load for reference records. The runbook should shrink release over release, and if it does not, nobody owns it.

## Gotchas

- **Check the report at your `sourceApiVersion`**, not the latest. Coverage is version-scoped and your project may be several behind → [02](02-sfdx-project-structure-and-source-format.md).
- **"Supported by Metadata API" does not imply packageable.** Unlocked and managed packages have their own columns, and a modularization plan can die on one unpackageable type → [08](08-unlocked-packages-2gp.md).
- **Round-trip is the real test.** Deploy it, retrieve it, diff it. A type that comes back different will produce a permanent phantom diff and eventually be ignored by reviewers.
- **A scratch org proves less than you think.** Its feature set is declared, so a manual production step may simply not exist there → [04](04-scratch-orgs-and-org-shape.md).
- **Nothing in Setup warns you** that a change is not deployable. There is no flag, no icon, no error — the metadata simply is not in the retrieve.
- **Manual steps are where the audit trail breaks.** They are performed by a person in production and attributed to that person, not to a commit → [01-admin · 17](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md).
- **One-way enablements have no rollback and no sandbox undo** — Person Accounts cannot be disabled at all, in any org.

## Recall

Q: What is the canonical source for whether something can be deployed?
A: The Metadata Coverage Report, read at the API version you deploy at, with its per-mechanism columns.

Q: What are the three ways "we'll just deploy it" fails?
A: The type is not covered; it is covered but does not round-trip; or it deploys and still needs another step before it does anything.

Q: Which is deployable — custom setting records or custom metadata type records?
A: Custom metadata type records are metadata and deploy. Custom setting records are data and do not.

Q: Why rehearse manual steps in a Full sandbox rather than documenting them?
A: A step that has only ever been performed in production has never been tested, and one-way enablements cannot be undone.

Q: How should a manual-steps runbook change over time?
A: It should shrink — each release converts one or two steps into scripted automation. A runbook that stays the same size has no owner.

## Related

- [05 · Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) — what a deployment can carry
- [08 · Unlocked packages (2GP)](08-unlocked-packages-2gp.md) — a second, stricter coverage column
- [01-admin · 09 Custom metadata vs custom settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — the deployable-configuration decision
- [20 · Release management & org upgrades](20-release-management-and-org-upgrades.md) — where the runbook is executed
