# Source Tracking & Sandbox Workflow

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Letting the tooling work out what changed, and the discipline that keeps a sandbox and a repo in agreement. Sandbox *data* is [08-data · 20](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md).

## Core idea

Source tracking makes the org and the local project both **report their own changes**, so `sf project deploy start` and `sf project retrieve start` can run with no component list at all. The org maintains `SourceMember` rows for what changed in Setup; the CLI keeps local state under `.sf/`; the difference between the two is the work.

It is available in **scratch orgs** and in **Developer and Developer Pro sandboxes** (GA since Spring '21) — and nowhere else. Partial and Full sandboxes and production have no tracking, which is why the workflow bifurcates: tracked orgs get pull-based development, untracked orgs get manifest-based deployment → [05](05-metadata-api-and-deployment-mechanics.md).

## How it works

- **`sf project deploy preview` / `sf project retrieve preview`** show what each direction would move, including conflicts. These replaced `force:source:status`.
- **`sf project deploy start` / `retrieve start`** with no selection flags act on tracked changes only.
- **Conflicts** are raised when a component changed on both sides since the last sync. `--ignore-conflicts` is the override, and it always loses one side's work.
- **`sf project reset tracking`** declares the two sides identical without moving anything — the escape hatch after a manual fix, and a loaded gun.
- **`sf project delete source`** removes locally *and* in the org, keeping tracking consistent — deleting a file alone does not delete the component.

## 2026 currency

**Source Mobility went GA in June 2025** and is on by default: moving a source file within the project no longer registers as *delete the component, create a new one*. Two limits define its usefulness — it handles **moves, not renames** (a rename is still a delete plus a create), and a child file can only move to an identically named parent, so a custom field can cross package directories only between `Account/` folders. Opt out with `SF_DISABLE_SOURCE_MOBILITY=true`; the old Beta variable `SF_BETA_TRACK_FILE_MOVES` was removed. This matters more than it sounds: reorganising a project into package directories was previously a destructive-looking diff, which is precisely the step modularization begins with → [10](10-modularization-and-dependency-strategy.md).

## Gotchas

- **Tracking state is local to your machine.** It lives in `.sf/`, is not committed, and is not shared — CI has no idea what you have already deployed, which is why pipelines use manifests or git diffs rather than tracking.
- **A sandbox refresh resets everything**: new My Domain host, no tracking history, and every alias pointing at the old instance → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md).
- **Not every Setup change produces a `SourceMember` row.** Things outside the Metadata API's coverage change nothing that tracking can see, and they will not be in your retrieve → [12](12-metadata-coverage-and-manual-steps.md).
- **`reset tracking` does not verify anything.** It asserts parity; if the sides genuinely differ you have just made the difference invisible.
- **Conflict detection compares timestamps, not content.** A retrieve that rewrites a file identically still marks it changed, and noisy types (flexipages, permission sets) generate phantom conflicts.
- **Renaming is still destructive.** Source Mobility does not cover it, so a rename shows as a delete plus a create — and on a tracked org that will actually delete the component.
- **Two developers in one Developer sandbox share one tracking surface.** Each CLI's local state is private, but the org's `SourceMember` rows are not, so each sees the other's changes as incoming.

## Recall

Q: Which orgs support source tracking?
A: Scratch orgs, and Developer and Developer Pro sandboxes. Not Partial, not Full, not production.

Q: What replaced `sfdx force:source:status`?
A: `sf project deploy preview` and `sf project retrieve preview`.

Q: What does Source Mobility handle and what does it not?
A: Moves within the project are tracked as moves. Renames are still interpreted as a delete plus a create.

Q: Why can't a CI pipeline rely on source tracking?
A: Tracking state is machine-local and uncommitted, so a runner has no history — pipelines deploy from a manifest or a git diff instead.

Q: What does `sf project reset tracking` actually do?
A: Asserts that org and local source are in sync without moving anything. It hides a real difference just as readily as it clears a false one.

## Related

- [04 · Scratch orgs & org shape](04-scratch-orgs-and-org-shape.md) — the other tracked environment
- [05 · Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) — the untracked path
- [07 · Branching strategy for Salesforce](07-branching-strategy-for-salesforce.md) — how many people share one sandbox
- [08-data · 20 Sandboxes, seeding & Data Mask](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md) — this note owns tracking, that one owns the data
