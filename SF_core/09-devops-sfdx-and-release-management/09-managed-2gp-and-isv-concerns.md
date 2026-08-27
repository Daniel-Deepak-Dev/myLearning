# Managed 2GP & ISV Concerns

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Packaging for orgs you do not control — namespaces, ancestry, upgrades, and the 1GP migration. The internal case is [08](08-unlocked-packages-2gp.md).

## Core idea

A **managed** package protects intellectual property and guarantees upgradability. Its components carry a **namespace**, subscribers cannot edit them, and the platform enforces an upgrade contract: anything you expose publicly — a `global` Apex method, an `@AuraEnabled` signature, a field's API name — you have effectively promised to keep forever.

Second-generation managed packaging replaces the 1GP model of *one packaging org that is the source of truth*. In 2GP the source of truth is your repository, versions are built from a Dev Hub, and the namespace is registered once and reused. That difference is the whole reason 2GP exists: 1GP made the packaging org a single mutable environment that could not be branched, reviewed or rebuilt.

## How it works

- **Namespace registry** — a namespace is claimed in a Developer Edition org and linked to the Dev Hub. It is permanent and appears in every packaged component's API name.
- **Ancestry** — `ancestorVersion` / `ancestorId` in `sfdx-project.json` declares which released version a new version upgrades from. Managed 2GP only; **unlocked packages have no ancestry**.
- **Beta → released** works as in [08](08-unlocked-packages-2gp.md), with **75% coverage** and every Apex trigger covered before a version can be released on AppExchange.
- **Push upgrades** — `sf package push-upgrade schedule | abort | list` moves subscribers onto a new version without their action.
- **LMA and the security review** sit outside the CLI: the License Management App tracks installs and licences, and AppExchange listing requires passing security review.

## 2026 currency

**Package Migrations went GA in Summer '25**, and it changes the 1GP conversation from "should we" to "when". The tooling automates the conversion: it extracts the 1GP package's metadata into source, **keeps the namespace**, continues the version sequence where 1GP left off, and — the part that used to make migration impossible — **migrates existing subscribers with the package already installed**. The packaging-org dependency disappears. The commercial pressure behind it is metadata coverage: **2GP covers most of the GenAI and Agentforce metadata types and 1GP's support is partial**, so an ISV shipping agent features in 2026 is choosing between migrating and not shipping → [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md).

## Gotchas

- **The public API surface is permanent.** `global` Apex, `@AuraEnabled` signatures and packaged field API names cannot be removed from a released managed package — design the surface as if it were a published contract, because it is.
- **Deleting components from a released managed package is heavily restricted**, and some types cannot be removed at all.
- **The namespace is forever and it is visible.** It prefixes every API name in every subscriber org, and there is no rename.
- **Ancestry is a linear promise.** Skipping or misdeclaring an ancestor produces an upgrade path the platform will refuse, and the fix is a new version, not an edit.
- **Subscriber debugging is deliberately blind.** Subscriber Support access and packaged debug logs exist precisely because you cannot see into their org — plan the telemetry into the package.
- **Push upgrades are a privilege, not a right.** They are constrained by version and by subscriber, and a push that breaks a subscriber's customisation is your incident.
- **Org-dependent unlocked is not a managed package.** It removes the dependency validation, not the editability — it protects nothing.

## Recall

Q: What replaced the 1GP packaging org in 2GP?
A: The repository plus a Dev Hub. Versions are built from source rather than from a single mutable packaging org.

Q: Which package type supports ancestry?
A: Managed 2GP only. Unlocked packages have no ancestry.

Q: What does Package Migrations do, and when did it become GA?
A: It automates 1GP → 2GP conversion — extracting metadata to source, keeping the namespace, continuing the version sequence and migrating existing subscribers. GA in Summer '25.

Q: What is the practical 2026 reason an ISV migrates to 2GP?
A: Metadata coverage. 2GP covers most GenAI and Agentforce metadata types; 1GP's coverage is partial.

Q: Why must a managed package's public API be designed as permanent?
A: `global` Apex, `@AuraEnabled` signatures and packaged field API names cannot be removed from a released managed package.

## Related

- [08 · Unlocked packages (2GP)](08-unlocked-packages-2gp.md) — the same versioning machinery without the namespace or the lock
- [10 · Modularization & dependency strategy](10-modularization-and-dependency-strategy.md) — how packages depend on each other
- [02-apex · 22 Invocable Apex & Agentforce actions](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) — the `global` no-arg constructor rule for cross-package invocation
- [AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) — agent metadata in source
