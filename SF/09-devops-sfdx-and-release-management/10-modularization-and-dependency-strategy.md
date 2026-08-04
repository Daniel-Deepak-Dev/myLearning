# Modularization & Dependency Strategy

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** An argued opinion about when to break an org's source into packages and when not to. The packaging mechanics are [08](08-unlocked-packages-2gp.md) and [09](09-managed-2gp-and-isv-concerns.md).

## Core idea

Modularization is usually presented as obviously good and rarely costed. It is not free: every package adds a version number to reason about, a dependency edge to keep acyclic, a build to run, and an install ordering to get right on every environment. A five-package org has a build graph, and someone has to own it.

The honest position: **most orgs should not modularize, and the ones that should know why.** The three arguments that actually justify it are **independent release cadence** (two teams that must ship on different days), **removability** (a capability that has to be uninstallable as a unit), and **reuse across orgs** (the same component set installed in several orgs). "Cleaner structure" is not one of them — package directories give you that without packages.

## How it works

```json
"packageDirectories": [
  { "path": "force-app/base",    "package": "Base",    "versionNumber": "1.2.0.NEXT", "default": true },
  { "path": "force-app/billing", "package": "Billing", "versionNumber": "0.4.0.NEXT",
    "dependencies": [{ "package": "Base", "versionNumber": "1.2.0.LATEST" }] }
]
```

- **Dependencies are declared, directional and acyclic.** A package can depend on a version of another package by name plus version number, or by a hard `subscriberPackageVersionId`.
- **`LATEST` floats, an `04t` ID pins.** Floating is convenient in development and is a reproducibility hole in a release build.
- **A component lives in exactly one package**, so the first real design act is drawing the boundary — and the boundary is decided by dependencies, not by team names.
- **The base-package pattern** — one package holding the shared objects, utilities and permission sets everything else depends on — is the shape almost every successful decomposition converges on.
- **An unpackaged remainder always exists.** Layouts, record types, org settings, profiles and everything the Metadata Coverage Report excludes stay loose → [12](12-metadata-coverage-and-manual-steps.md).

## Gotchas

- **Circular dependencies are impossible, and you will discover one.** Two "independent" capabilities that reference each other's objects are one package until somebody breaks the cycle with an interface or an event.
- **Splitting an existing org is a data migration, not a refactor.** Moving a custom object into a package means the records move with it — or do not move at all, if you get it wrong → [08-data · 25](../08-data-modeling-and-large-data-volumes/25-data-migration-and-cutover.md).
- **Permission sets cut across packages badly.** A permission set granting access to two packages' objects belongs to one of them and breaks if the other is not installed.
- **Install order is your problem on every environment**, including every scratch org in CI, and it multiplies the setup time per pull request — which is what snapshots are for → [04](04-scratch-orgs-and-org-shape.md).
- **Version pinning drift is silent.** `LATEST` in a dependency means two builds of the same commit can produce different orgs.
- **Package boundaries do not enforce runtime isolation** in an unlocked package — subscribers can edit, triggers still fire across boundaries, and nothing stops one package's Apex querying another's objects.
- **Modularizing to fix deployment time usually fails**, because the slow part is the test run, not the payload → [05](05-metadata-api-and-deployment-mechanics.md).

## Recall

Q: What are the three arguments that genuinely justify splitting an org into packages?
A: Independent release cadence, removability as a unit, and reuse across multiple orgs.

Q: What shape do most successful decompositions converge on?
A: A base package holding shared objects, utilities and permission sets, with capability packages depending on it.

Q: What is the risk of declaring a dependency with `LATEST`?
A: Two builds of the same commit can resolve to different package versions, so the build is not reproducible.

Q: Why is splitting an existing org not a refactor?
A: Moving an object into a package moves its records with it — it is a data migration with a rollback problem.

Q: Does an unlocked package enforce runtime isolation?
A: No. Subscribers can edit its components, and other code can query its objects freely. The boundary is for versioning and removal, not encapsulation.

## Related

- [08 · Unlocked packages (2GP)](08-unlocked-packages-2gp.md) — the unit being created
- [07 · Branching strategy for Salesforce](07-branching-strategy-for-salesforce.md) — package-aligned branches
- [04 · Scratch orgs & org shape](04-scratch-orgs-and-org-shape.md) — where install ordering costs you every build
- [08-data · 25 Data migration & cutover](../08-data-modeling-and-large-data-volumes/25-data-migration-and-cutover.md) — the half of decomposition that is data
