---
vault: SF_core
area: 09-devops-sfdx-and-release-management
format: dense
status: learning
created: 2026-08-04
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 16
---
# Metadata API & Deployment Mechanics

**Scope:** Moving metadata between orgs — manifests, deploy/retrieve, validation and quick deploy, destructive changes. What *cannot* be moved is [12](12-metadata-coverage-and-manual-steps.md).

## Core idea

Every deployment is the same transaction: a zip containing a **`package.xml` manifest** and the components it names, sent to the Metadata API, compiled and validated server-side, and applied **all or nothing**. In production `rollbackOnError` is forced, so a deployment either lands completely or changes nothing.

The mechanic worth building a release process around is **validate-then-quick-deploy**. A validation runs the full deployment including Apex tests against production without committing anything and returns a job ID. That job ID is **valid for 10 days**, and passing it to a quick deploy applies the already-validated payload **without re-running the tests**. That is how a two-hour test run turns into a two-minute release window.

## How it works

```bash
sf project deploy validate  --source-dir force-app --test-level RunLocalTests -o prod
# ... returns Deploy ID 0Af...
sf project deploy quick --job-id 0Af... -o prod
```

- **Selecting components:** `--manifest package.xml`, `--source-dir`, or `--metadata ApexClass:Foo`. Generate a manifest with `sf project generate manifest`.
- **Test levels:** `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`, plus **`RunRelevantTests` (still Beta at 68.0)** which runs only the tests the deployment touches → [02-apex · 20](../02-apex-and-triggers/20-apex-testing-fundamentals.md). Production deployments require tests unless the payload contains no Apex.
- **Deleting** uses `destructiveChangesPre.xml` / `destructiveChangesPost.xml` alongside the manifest — `--pre-destructive-changes`, `--post-destructive-changes`. Deletion is never inferred from source absence.
- **Async by default:** `deploy resume`, `deploy report`, `deploy cancel` operate on the job ID.
- **Limits:** **10,000 files** per deploy or retrieve, **39 MB compressed**, **400 MB uncompressed**. The 39 MB figure is a consequence of the 50 MB SOAP message cap and base-64 encoding, not an arbitrary number.
- **Retrieve** takes `rootTypesWithDependencies` on the underlying `RetrieveRequest`, so a root type can be pulled with its dependent metadata instead of enumerating every component by hand.

## 2026 currency

Two things to carry into 2026. First, **`RunRelevantTests` changes the economics of validation** — combined with quick deploy it attacks the same problem from both ends, and it is steered by `@IsTest(testFor=…)` annotations you have to actually write. Second, **retrieve is not a read-only operation**. A zip-slip in static-resource conversion (fixed in `@salesforce/source-deploy-retrieve` 13.0.1, 31 July 2026) let a crafted static resource write outside the project during `project retrieve start` or `project convert mdapi`, and the fix is gated behind a major version bump plus Node 22 — so "I updated the CLI" is not the same sentence as "I have the fix". Detail and the dependency graph: [RELEASE-RADAR/developer-tooling-and-apis.md](../../RELEASE-RADAR/developer-tooling-and-apis.md).

**Winter '27 (API 68.0) adds compile-side tools.** On the Apex Classes and Apex Triggers Setup pages, **Compile only invalid classes** and **Compile only invalid triggers** recompile just the code marked invalid instead of the whole org. The Tooling API resource **`apexCompileResults`** (POST an empty `{}`; needs Author Apex) returns the invalid classes and triggers that still fail, with line, column and message — it does not set `IsValid`. CLI 2.154.4 (14 Oct 2026) added `sf apex get compile-status`, which lists invalid classes and those with compile warnings (🚩 CLI release notes on GitHub). And the compiler now **warns on deploy** for Apex saved at API 9.0–19.0, which Salesforce says will be retired in a future release → [02-apex · 02](../02-apex-and-triggers/02-modern-apex-syntax.md).

## Gotchas

- **The quick-deploy job ID expires after 10 days**, and it is invalidated early by anything that changes the target org's relevant metadata. A validation is not a release ticket you can sit on.
- **Quick deploy skips tests, it does not skip validation** — the payload is fixed at validation time, so you cannot amend one component and quick-deploy the rest.
- **Deployment order is Salesforce's, not yours.** A manifest is a set; if component A needs B, both go in the same deployment or the first one fails.
- **The CLI deploys over SOAP by default.** `sf config set org-metadata-rest-deploy=true` (or `SF_ORG_METADATA_REST_DEPLOY`) switches to REST, which is the lever when a payload is bumping the compressed-size ceiling.
- **Profiles deploy as a subset of what else is in the package**, so a profile deployed alone can strip nothing and grant nothing — a permanent source of "the deployment succeeded and the permission is missing" → [07-security · 03](../07-security-and-sharing/03-profiles-and-the-permission-set-led-model.md).
- **A deployed flow is not an active flow** unless *Deploy processes and flows as active* is set, and that setting appears only in production → [04-flow · 24](../04-flow-and-automation/24-flow-deployment-versioning-and-governance.md).
- **`NoTestRun` is silently unavailable in production**, and the resulting error names the test level rather than the rule.

## Recall

Q: How long is a validated deployment's job ID good for?
A: 10 days — after which the validation must be re-run before a quick deploy.

Q: What does quick deploy actually skip?
A: Re-running the Apex tests. The payload was already compiled and validated; nothing about it can be changed.

Q: What are the Metadata API deployment size limits?
A: 10,000 files, 39 MB compressed, 400 MB uncompressed.

Q: How do you delete metadata through a deployment?
A: A `destructiveChangesPre.xml` or `destructiveChangesPost.xml` alongside the manifest. Absence from source never deletes anything.

Q: Why is `project retrieve start` a security-relevant operation?
A: It takes org-controlled bytes and writes them to a laptop or CI runner — a zip-slip in static-resource conversion allowed writes outside the project until SDR 13.0.1.

## Related

- [02 · SFDX project structure & source format](02-sfdx-project-structure-and-source-format.md) — the two formats a deployment can be built from
- [06 · Source tracking & sandbox workflow](06-source-tracking-and-sandbox-workflow.md) — deploying without naming components
- [12 · Metadata coverage & manual steps](12-metadata-coverage-and-manual-steps.md) — the components no manifest can carry
- [04-flow · 24 Flow deployment & versioning](../04-flow-and-automation/24-flow-deployment-versioning-and-governance.md) — deployed does not mean active
- [SF_Agentforce · Prompt Template Metadata & Deployment](../../SF_Agentforce/prompt-template-metadata-and-deployment.md) — `GenAiPromptTemplate` carries every version plus a pointer to the active one
- [SF_Experience_Cloud · 02 LWR architecture & build model](../../SF_Experience_Cloud/02-lwr-architecture-and-build-model.md) — the two site bundle types, and which one a pipeline can actually carry
- [SF_Experience_Cloud · 18 Experience Cloud DevOps](../../SF_Experience_Cloud/18-experience-cloud-devops.md) — what deploying a site adds on top of these mechanics

## Sources

- [Tooling API Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_tooling.pdf) — Salesforce Developers · read 2026-10-28 · `apexCompileResults`: API 68.0+, POST `{}`, Author Apex, `OK` / `PARTIAL_FAILURE`, problems with line and column; the Setup buttons update `IsValid`, the resource does not
- [Apex Developer Guide (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf) — Salesforce Developers · read 2026-10-28 · Version 68.0 behaviour list: recompile only invalid Apex; compiler warnings for API 9.0–19.0; `RunRelevantTests` and its `@IsTest` annotations still *"pilot or beta services"*
- [Reduce Overhead by Recompiling Only Invalid Apex Classes and Triggers](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_apex_recompile_invalid_apex.htm&type=5&release=264) — Salesforce Help · via search 2026-10-28 · Winter '27 release note; the *Compile only invalid classes / triggers* buttons; Enterprise, Performance, Unlimited and Developer editions
- [Salesforce CLI Command Reference (PDF, Winter '27)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/sfdx_cli_reference.pdf) — Salesforce Developers · read 2026-10-28 · `--test-level` still describes `RunRelevantTests (Beta)`
- [Salesforce CLI release notes](https://github.com/forcedotcom/cli/blob/main/releasenotes/README.md) — 🚩 GitHub, not a Salesforce domain · read 2026-10-28 · `sf apex get compile-status`, new in 2.154.4 (14 Oct 2026)

## History

- 2026-10-28 · Winter '27 currency check: added recompile-only-invalid Apex and `apexCompileResults`; `RunRelevantTests` confirmed still Beta at 68.0
