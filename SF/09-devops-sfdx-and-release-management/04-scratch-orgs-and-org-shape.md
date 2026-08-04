# Scratch Orgs & Org Shape

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** Disposable development orgs — definition files, shapes, snapshots and their limits. Sandbox *data* is [08-data · 20](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md); the sandbox *workflow* is [06](06-source-tracking-and-sandbox-workflow.md).

## Core idea

A scratch org is an **empty, disposable org built from a text file**. It has no production metadata, no production data and no history — you declare the edition, the features and the settings you want, the Dev Hub builds it, and you throw it away. That is the whole point: an environment whose contents are entirely described by something in git.

The consequence people underestimate is the inverse. Because nothing carries over, **anything your code needs must be declared or deployed**. A scratch org is the honest test of whether your source is complete, which is exactly why an org that only ever deploys to sandboxes accumulates undeclared dependencies for years without noticing.

## How it works

```json
{
  "orgName": "Acme Dev",
  "edition": "Developer",
  "features": ["EnableSetPasswordInApi", "PersonAccounts"],
  "settings": { "lightningExperienceSettings": { "enableS1DesktopEnabled": true } }
}
```

- **Create:** `sf org create scratch --definition-file config/project-scratch-def.json --alias dev --duration-days 30`. Duration is **1–30 days, default 7**; there is no extension, only a new org.
- **Shape** — `sf org create shape --target-org <source>` captures an *existing* org's edition, features, settings and licences so a scratch org can be created in that image. `org list shape`, `org delete shape`.
- **Snapshot** — `sf org create snapshot` freezes a **configured scratch org** (metadata *and* the data in it), and `sf org create scratch --snapshot <name>` builds from it with no definition file at all. GA since **Summer '24**.
- **Allocations live on the Dev Hub**, not on you: active and daily scratch org counts vary by Dev Hub edition and contract. `sf org list limits --target-org <devhub>` is the only reliable answer.
- **Async creation:** `--async` returns a job ID; `sf org resume scratch --job-id … --wait 10` polls it. Snapshot-based creation is slow enough that this matters.

## 2026 currency

Snapshots are the meaningful change of the last two years and they are under-adopted: a snapshot turns a ten-minute "create, install dependencies, deploy, seed" chain into one command, which is what makes per-pull-request orgs affordable in CI. **Shapes and snapshots answer different questions** — a shape describes the *shell* (edition, features, licences, limits), a snapshot captures what an org *became* after setup. A separate, very current trap: Salesforce now requires emails to come from verified domains, so Apex tests that send email fail in a fresh scratch org unless the definition file sets `EmailAuthorizationSettings.enableSubstituteFromAddress` to `true`.

## Gotchas

- **A snapshot is pinned to a release.** When the platform moves, a snapshot built on the old release goes stale and eventually cannot be used — they need rebuilding on a schedule, and nothing reminds you.
- **A feature not named in `features` is not there.** The failure is a deploy error about an unknown type, not a helpful "enable this first".
- **Some things cannot be enabled in a scratch org at all**, and some enable one-way — Person Accounts and multi-currency among them → [12](12-metadata-coverage-and-manual-steps.md).
- **A scratch org is not a performance environment.** No data volume, no skinny tables, no realistic sharing — every LDV conclusion drawn in one is worthless → [08-data · 11](../08-data-modeling-and-large-data-volumes/11-skinny-tables-and-support-levers.md).
- **Expiry is silent and total.** There is no grace period and no recovery; uncommitted work in an expired scratch org is gone.
- **The Dev Hub's release matters during preview windows.** Set the definition file's release to `preview` or `previous` deliberately, or you will get whichever side of the window the Dev Hub happens to be on.
- **Scratch org users are not production users.** Licences, profiles and the role hierarchy are minimal, so sharing behaviour tested here proves very little → [07-security · 08](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md).

## Recall

Q: What is the maximum life of a scratch org?
A: 30 days, default 7, with no extension — you create a new one.

Q: What is the difference between an org shape and a snapshot?
A: A shape captures the shell — edition, features, settings, licences — from a source org. A snapshot captures a configured scratch org's metadata and data at a point in time.

Q: Which command creates a scratch org from a snapshot, and what does it not need?
A: `sf org create scratch --snapshot <name>` — no definition file is required.

Q: Why does a scratch org expose incomplete source when a sandbox does not?
A: A sandbox already contains production metadata, so an undeclared dependency still resolves. A scratch org has nothing, so anything not declared or deployed is simply missing.

Q: Where do scratch org allocations come from?
A: The Dev Hub — its edition and contract set the active and daily counts. Check with `sf org list limits`.

## Related

- [03 · Org auth & environment management](03-org-auth-and-environment-management.md) — `target-dev-hub` and where scratch orgs are billed
- [06 · Source tracking & sandbox workflow](06-source-tracking-and-sandbox-workflow.md) — the tracking that makes the loop work
- [08-data · 20 Sandboxes, seeding & Data Mask](../08-data-modeling-and-large-data-volumes/20-sandboxes-seeding-and-data-mask.md) — the data side of non-production orgs
- [12 · Metadata coverage & manual steps](12-metadata-coverage-and-manual-steps.md) — what a definition file cannot turn on
