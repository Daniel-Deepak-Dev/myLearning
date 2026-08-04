# SFDX Project Structure & Source Format

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 16

**Scope:** The shape of a DX project on disk — `sfdx-project.json`, source format vs metadata format, and `.forceignore`. Deploying it is [05](05-metadata-api-and-deployment-mechanics.md).

## Core idea

There are **two on-disk representations of the same metadata**, and confusing them is the single most common early mistake.

**Metadata format** is what the Metadata API accepts: a `package.xml` manifest plus folders of monolithic XML files, one file per component. **Source format** is what a DX project holds: the same metadata **decomposed** into smaller, git-friendly files — a custom object becomes a folder with one file per field, one per validation rule, one per list view. Source format exists for version control; metadata format exists for the wire.

The CLI converts between them, and the conversion is still required whenever something outside DX is involved: an Ant/`package.xml` artifact from an older pipeline, a `--metadata-dir` deployment, or a vendor tool that emits metadata format.

## How it works

```json
{
  "packageDirectories": [{ "path": "force-app", "default": true }],
  "namespace": "",
  "sourceApiVersion": "67.0",
  "sourceBehaviorOptions": ["decomposePermissionSetBeta2"]
}
```

- **`packageDirectories`** is the list of source roots. One entry is `default: true` and receives anything the CLI generates or retrieves without an explicit target. Multi-directory projects are how modularization starts → [10](10-modularization-and-dependency-strategy.md).
- **`sourceApiVersion`** stamps the `package.xml` the CLI builds. It is *not* the org's API version and *not* the `apiVersion` config variable — three separate dials that regularly disagree.
- **`.forceignore`** excludes paths from **source-format** operations (deploy, retrieve, conversion, tracking). It has no effect on a metadata-format deploy, and it is the usual home for `**/profiles/**` and `**/jsconfig.json`.
- **`replacements`** performs string substitution at deploy time, which is the supported way to vary an endpoint or a label per environment without branching the source.
- **`sf project convert source` / `sf project convert mdapi`** move between formats. Neither touches an org.

## 2026 currency

The interesting movement is **further decomposition**, all still Beta and all opt-in through `sourceBehaviorOptions`: `decomposePermissionSetBeta2`, `decomposeCustomLabelsBeta2`, `decomposeSharingRulesBeta`, `decomposeWorkflowBeta`, `decomposeExternalServiceRegistrationBeta`. Run `sf project convert source-behavior --behavior <name>` and the CLI rewrites both the project file and the affected source. The motivation is merge conflicts: a single `CustomLabels.labels-meta.xml` or one permission set file guarantees that two people touching unrelated things collide, and decomposition is the only real fix → [07](07-branching-strategy-for-salesforce.md). Treat the Beta label seriously — the layouts have already changed once, which is why there is both a `Beta` and a `Beta2` variant of two of them.

## Gotchas

- **`sourceApiVersion` is not the org's API version.** Bumping the org's release does not bump it, and a stale value silently deploys at an older API version.
- **`.forceignore` does not retro-remove anything.** It stops files being written or sent; it does not delete what is already committed, and it does not stop the org having the component.
- **Ignoring profiles is the norm, not a hack.** A retrieved profile is a *subset* shaped by what else was in the manifest, so committing whole profiles produces diffs that mean nothing → [12](12-metadata-coverage-and-manual-steps.md).
- **Only one `packageDirectories` entry can be default**, and the CLI will happily scatter retrieved source into it if you forget `--output-dir`.
- **Decomposition changes file paths**, so it rewrites history-adjacent things: code owners, `.forceignore` patterns and any script globbing on the old layout.
- **`replacements` runs on deploy, not on retrieve** — the substituted value goes to the org and the token stays in git, so the two are permanently out of sync by design.
- **The project file is read from the current directory upward.** Running a command outside the project root gives "no project found" rather than a useful hint.

## Recall

Q: What is the difference between source format and metadata format?
A: Metadata format is the Metadata API's wire shape — `package.xml` plus monolithic XML. Source format decomposes the same metadata into small, git-friendly files for version control.

Q: When is a format conversion still required?
A: Whenever something non-DX is involved — an Ant or `package.xml` artifact, a `--metadata-dir` deployment, or a third-party tool that emits metadata format.

Q: What does `sourceApiVersion` control, and what does it not?
A: It stamps the manifest the CLI generates. It is not the org's API version and not the `apiVersion` config variable.

Q: Which operations does `.forceignore` affect?
A: Source-format operations only — deploy, retrieve, convert and source tracking. It does nothing on a metadata-format deploy.

Q: Why decompose permission sets or custom labels?
A: Because one monolithic file makes every concurrent edit a merge conflict. `sourceBehaviorOptions` plus `sf project convert source-behavior` splits them — still Beta.

## Related

- [01 · `sf` CLI v2 fundamentals](01-sf-cli-v2-fundamentals.md) — the commands that read this file
- [05 · Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) — where `package.xml` actually matters
- [07 · Branching strategy for Salesforce](07-branching-strategy-for-salesforce.md) — why metadata merges badly
- [10 · Modularization & dependency strategy](10-modularization-and-dependency-strategy.md) — when one package directory becomes several
