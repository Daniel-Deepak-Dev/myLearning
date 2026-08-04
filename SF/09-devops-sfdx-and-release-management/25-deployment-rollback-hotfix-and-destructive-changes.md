# Deployment Rollback, Hotfix & Destructive Changes

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Getting *out* of a deployment — the reversal *strategy*, the emergency path, and what deletion costs you. The destructive-manifest mechanics are [05](05-metadata-api-and-deployment-mechanics.md); the forward pipeline is [14](14-ci-cd-with-github-actions.md); recovering **data** is [08-data · 21](../08-data-modeling-and-large-data-volumes/21-backup-restore-and-recovery.md).

> **What changed.** Nothing changed — this is a belief that was never true. **There is no rollback in Salesforce.** A single deployment to production is atomic (`rollbackOnError` is forced true there, so a failure leaves the org untouched), but a *release* is not: once a deploy succeeds, the only reversal is **another deployment**, forward, of the previous state. It cannot delete what it created, cannot restore what it destroyed, and cannot un-run a data migration.

## Core idea

Because reversal does not exist, the recovery plan has to be built before the deployment rather than after it. That reduces to three decisions, and a team that has made all three can survive a bad release in minutes.

**First, roll forward, always** — from a tag of what production actually had, not from a reconstructed guess. **Second, put a switch on anything risky**, because toggling a custom metadata record off is the only true instant reversal the platform offers. **Third, treat deletions as a separate, reviewed change**, since they are the operations that make roll-forward impossible.

## How it works

- **Tag every production deployment.** `git revert` plus a deploy from the tag is the rollback procedure; without the tag you are diffing against memory.
- **A revert does not delete.** Removing a file from git removes nothing from the org — deletion is never inferred from source absence, so components created by the bad release survive the revert and stay. Removing them is a separate destructive manifest → [05](05-metadata-api-and-deployment-mechanics.md).
- **`--purge-on-delete` skips the Recycle Bin** — and it works in **Developer Edition and sandboxes only**, never production.
- **Deleted custom fields are recoverable for 15 days** in Setup, which is the one genuine undo on this page. After that the data goes with them.
- **Rehearse the reversal once.** Deploy the previous tag to a Full sandbox on a calm afternoon and time it; that number is what you will be asked for during the incident, and it is the only way to find the components a revert leaves behind.
- **The real kill switch is configuration, not deployment.** Ship behind a custom metadata flag and the reversal is a record edit an admin can make at 2 a.m. → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md).
- **Hotfix branches from the production tag**, never from the development branch — then merge back into every long-lived branch, immediately.

## Gotchas

- **The merge-back is the step teams skip**, and it re-breaks production on the next release. The hotfix must exist in every branch it will ever be deployed over.
- **A hotfix invalidates the release validation.** Any deployment to the org between `validate` and `quick deploy` kills the job ID → [14](14-ci-cd-with-github-actions.md).
- **Reverting Apex is easy; reverting a schema change is not.** A deleted field takes its data with it, and a changed field type may have already coerced values.
- **`--ignore-errors` is ignored in production.** Partial deployment is a sandbox convenience; production is all-or-nothing.
- **Deactivating is not deleting.** Many components must be deactivated or dereferenced before a destructive change will succeed, which is why deletion order is its own design problem.
- **Metadata backup is not data backup, and the data service is expensive.** Salesforce's Data Recovery Service exists and is **$10,000, 6–8 weeks, data only, no metadata**, with no guarantee → [08-data · 21](../08-data-modeling-and-large-data-volumes/21-backup-restore-and-recovery.md).
- **A one-way feature enablement has no reversal at all** — not a slow one, none. Person Accounts is the standard example, and it is a decision, not a deployment → [12](12-metadata-coverage-and-manual-steps.md).

## Recall

Q: What is the rollback mechanism for a successful Salesforce deployment?
A: There is not one — you deploy the previous state forward, and that cannot delete newly created components or restore destroyed data.

Q: What is atomic, then?
A: A single production deployment. `rollbackOnError` is forced true in production, so a failing deploy leaves the org unchanged.

Q: Why does reverting the commit not undo the release?
A: Deletion is never inferred from source absence — components the bad release created stay in the org until a destructive manifest removes them.

Q: Where does `--purge-on-delete` work?
A: Developer Edition and sandboxes only — never production.

Q: What is the fastest true reversal available on the platform?
A: A feature flag in custom metadata — an admin toggles the record and the behaviour stops, with no deployment involved.

## Related

- [05 · Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) — the destructive manifests and the atomicity this note reasons about
- [14 · CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md) — the forward path, and the validation a hotfix invalidates
- [12 · Metadata coverage & the manual-steps problem](12-metadata-coverage-and-manual-steps.md) — the manual work a roll-forward has to repeat
- [01-admin · 09 Custom metadata vs custom settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — the switch that makes reversal instant
- [08-data · 21 Backup, restore & recovery](../08-data-modeling-and-large-data-volumes/21-backup-restore-and-recovery.md) — what to do when the data went too
