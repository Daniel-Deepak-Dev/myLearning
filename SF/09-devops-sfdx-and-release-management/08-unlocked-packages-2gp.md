# Unlocked Packages (2GP)

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Packaging your *own org's* metadata as versioned, installable units. ISV and namespace concerns are [09](09-managed-2gp-and-isv-concerns.md); whether to modularize at all is [10](10-modularization-and-dependency-strategy.md).

> **What changed.** **First-generation packaging is legacy**, and second-generation unlocked packages are the model for org modularization. Note the word: legacy, **not retired** — 1GP packages still install, still upgrade, and Salesforce has announced no end-of-life for them. What changed is where new capability lands. 2GP is source-driven, created from a Dev Hub with no packaging org, and its metadata coverage is ahead of 1GP's — most notably for the Agentforce and GenAI types, where 1GP support is only partial.

## Core idea

An unlocked package is a **versioned, installable, upgradable and removable** bundle of metadata built straight from a package directory in your DX project. "Unlocked" means the subscriber org can still edit what it installed — nothing is locked down, which is what makes it right for internal use and wrong for commercial IP.

The property that earns the complexity is **removability**. Metadata deployed loose into an org has no boundary and no owner; the only way to remove it is to know what it was and delete it destructively. Metadata that arrived in a package can be uninstalled as a unit, and the platform will tell you what depends on it.

## How it works

```bash
sf package create --name Billing --package-type Unlocked --path force-app/billing -v devhub
sf package version create --package Billing --code-coverage --installation-key-bypass -w 30 -v devhub
sf package version promote --package 04t... -v devhub      # beta -> released
sf package install --package 04t... -o prod -w 20
```

- **Versions are `major.minor.patch.build`**, declared per package directory in `sfdx-project.json`, with `NEXT` and `LATEST` as build keywords.
- **A new version is a beta** (`04t…`) installable only in scratch orgs and sandboxes. **Promoting** makes it released and installable in production — and promotion is **irreversible**.
- **75% Apex coverage is required to promote**, computed at version-create time when `--code-coverage` is passed.
- **`--skip-validation`** makes creation dramatically faster by skipping dependency validation *and* coverage calculation — so a skip-validation version cannot clear the promotion gate. It is an inner-loop tool, not a release tool.
- **Org-dependent unlocked packages** (`--org-dependent`) are allowed to reference unpackaged metadata in the installing org; dependencies are validated at **install** time instead of at version-create time, and no coverage is calculated.
- **`sf package push-upgrade schedule | abort | list`** pushes a new version to installed orgs, and since mid-2025 this covers unlocked packages, not only managed ones.

## Gotchas

- **A component belongs to exactly one package.** Moving it between packages is a remove-and-add across two versions, and both must be installed in the right order.
- **Uninstalling deletes the data too.** Custom objects that came from a package take their records with them — there is no "keep the data" option.
- **A released version can never be deleted**, only deprecated. Version numbers are permanent public history.
- **Not everything is packageable.** The Metadata Coverage Report has a separate column for unlocked packages, and a type supported by the Metadata API may still be unpackageable → [12](12-metadata-coverage-and-manual-steps.md).
- **Profiles in packages behave as subsets**, exactly as in a deployment — permission sets are the packageable unit of access → [07-security · 03](../07-security-and-sharing/03-profiles-and-the-permission-set-led-model.md).
- **Dev Hub daily package-version-create limits are real** and are the usual reason a busy CI day stops building. Check `sf org list limits` against the Dev Hub.
- **`--installation-key-bypass` means anyone with the `04t` ID can install it.** Fine internally, careless if the ID escapes.

## Recall

Q: Is 1GP retired?
A: No. It is legacy — still installing and upgrading, with no announced end of life. New capability, including most Agentforce metadata coverage, lands in 2GP.

Q: What does promoting a package version do, and can it be undone?
A: It moves the version from beta to released so it can be installed in production. It cannot be undone, and a released version can only be deprecated, never deleted.

Q: Why can't a `--skip-validation` version be promoted?
A: Skipping validation also skips code-coverage calculation, and promotion requires 75% coverage.

Q: What is an org-dependent unlocked package for?
A: Packaging metadata that legitimately references unpackaged org metadata. Dependencies are checked at install time rather than at version creation, and coverage is not calculated.

Q: What happens to records when an unlocked package is uninstalled?
A: They are deleted along with the objects that held them.

## Related

- [09 · Managed 2GP & ISV concerns](09-managed-2gp-and-isv-concerns.md) — the same machinery aimed at subscribers you do not control
- [10 · Modularization & dependency strategy](10-modularization-and-dependency-strategy.md) — whether to split at all
- [02 · SFDX project structure & source format](02-sfdx-project-structure-and-source-format.md) — package directories are where this starts
- [12 · Metadata coverage & manual steps](12-metadata-coverage-and-manual-steps.md) — what cannot go in a package
