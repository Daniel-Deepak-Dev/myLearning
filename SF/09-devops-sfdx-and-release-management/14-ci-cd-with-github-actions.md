# CI/CD with GitHub Actions

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Assembling the pipeline — jobs, headless auth in CI, delta, gates, promotion. The deploy *mechanics* it drives are [05](05-metadata-api-and-deployment-mechanics.md), the CLI grammar is [01](01-sf-cli-v2-fundamentals.md), and what happens when a deploy goes wrong is [25](25-deployment-rollback-hotfix-and-destructive-changes.md).

> **What changed — twice, and both land in the first ten lines of every tutorial.** *"Create a connected app for JWT"* is a broken step: creation has been Support-gated since Spring '26 and the object is now an **External Client App** → [06-integration · 16](../06-integration-and-apis/16-external-client-apps.md). And *"pipe `sf org display --verbose` into `grep` for the auth URL"* stopped working on **27 May 2026**, when the CLI began redacting credentials from command output → [03](03-org-auth-and-environment-management.md). Existing connected apps still authenticate fine — this is a creation gate, not a switch-off — but a recipe older than mid-2026 fails on one of these two lines.

## Core idea

A Salesforce pipeline has one structural difference from every other CI/CD pipeline: **there is no artifact and no rollback.** A deploy is an API call that mutates a live, stateful org, and the org will not give you the previous state back. Everything the pipeline does is therefore about moving risk *earlier* — into validation against a real org, before the change reaches production.

That is why **validate-then-quick-deploy** is the spine of a serious pipeline: the expensive part happens while the release is still a pull request, and promotion becomes a few seconds rather than an hour nobody can abort. The mechanic and its 10-day job ID belong to [05](05-metadata-api-and-deployment-mechanics.md); what follows is how to wire it into jobs that a team can actually operate.

## How it works

- **Auth is a signed JWT, never a password.** Generate an RSA key pair, upload the certificate to an External Client App, pre-authorize an integration user, and store the private key as a repository secret.

```yaml
- run: sf org login jwt --client-id "$CLIENT_ID" --jwt-key-file server.key \
    --username "$SF_USERNAME" --instance-url https://mydomain.my.salesforce.com --alias prod
```

- **Three jobs, not one:** *check* on every push (lint, Jest, [16](16-code-analyzer-v5.md)), *validate* on every PR against the target org, *deploy* on merge.
- **Delta beats full-source** once the repo is real. `sfdx-git-delta` builds a manifest from the commit range so a one-field change does not redeploy 4,000 components.
- **`sf project deploy validate` on the PR → `sf project deploy quick --job-id` on merge.** The validation job carries the test run; the promotion job carries nothing.
- **`--json` on every command.** Exit codes tell you pass or fail; the JSON tells you *what* failed, which is the difference between a useful pipeline log and a screenshot.
- **Pin the CLI version.** It ships weekly, and `npm dist-tags` are **not ordered by version number** — `latest` can be behind `latest-rc` and `nightly` → [01](01-sf-cli-v2-fundamentals.md). An unpinned global install changes the pipeline on a Tuesday.

## 2026 currency

The redaction above is the change that breaks pipelines *today*, and the migration is to stop extracting credentials at all: authenticate with JWT each run rather than storing an auth URL to `grep` back out. `SF_TEMP_SHOW_SECRETS` exists and is a countdown, not a fix → [03](03-org-auth-and-environment-management.md). Two smaller CI-specific items: **`SF_CI_UPDATE_FREQUENCY_MS` and `SF_CI_HEARTBEAT_FREQUENCY_MS`** keep long-running commands emitting output so a runner does not kill them as idle; and the **zip-slip fix in metadata retrieve** matters more on a runner than on a laptop, because `retrieve` writes org-controlled bytes into the workspace → [05](05-metadata-api-and-deployment-mechanics.md). Check `npm ls @salesforce/source-deploy-retrieve` in the pipeline, not the CLI version.

## Gotchas

- **`actions/checkout` defaults to a shallow clone.** Without `fetch-depth: 0` the delta step compares against nothing and silently deploys an empty manifest.
- **`invalid_grant` on JWT almost always means the user is not pre-authorized**, not that the key is wrong. Fix it in the app's permitted-users policy.
- **Delete `server.key` after login.** A private key left in the workspace is available to every subsequent step, including third-party actions.
- **A hotfix in the middle of a release invalidates the release**, because it invalidates the validation job ID the promotion job is holding → [05](05-metadata-api-and-deployment-mechanics.md).
- **`NoTestRun` cannot be quick-deployed.** The validation must have run `RunLocalTests`, `RunAllTestsInOrg` or `RunSpecifiedTests`.
- **A green pipeline is not a green org.** Deploys succeed while leaving post-deploy manual steps undone → [12](12-metadata-coverage-and-manual-steps.md).
- **Secrets in a fork PR do not exist.** `pull_request` from a fork gets no repository secrets, so the validate job needs `pull_request_target` or a trusted-branch model — and that choice is a security decision.

## Recall

Q: Why is "create a connected app" no longer a valid first step for CI auth?
A: Connected-app creation has been restricted since Spring '26 and requires a Support case. New integrations use an External Client App.

Q: What makes `validate` + `quick deploy` the standard promotion pattern?
A: The Apex test run happens during validation, so promotion to production is seconds long instead of an hour with no abort button.

Q: Which pre-2026 CI recipe stopped working on 27 May 2026?
A: Extracting an auth URL by piping `sf org display --verbose` into `grep` — the CLI redacts credentials from command output.

Q: What breaks a delta deployment in GitHub Actions specifically?
A: `actions/checkout` does a shallow clone by default; `sfdx-git-delta` needs `fetch-depth: 0` to compute a diff.

Q: Why pin the Salesforce CLI version in a workflow?
A: It publishes weekly, so an unpinned global install changes the pipeline's behaviour without a commit.

## Related

- [15 · Apex test strategy in CI](15-apex-test-strategy-in-ci.md) — what the validate job actually runs
- [25 · Deployment rollback, hotfix & destructive changes](25-deployment-rollback-hotfix-and-destructive-changes.md) — the half of the pipeline this one cannot do
- [06-integration · 16 External client apps](../06-integration-and-apis/16-external-client-apps.md) — the object the pipeline authenticates through
- [05 · Metadata API & deployment mechanics](05-metadata-api-and-deployment-mechanics.md) — validate, quick deploy and the API every job is a client of
- [03 · Org auth & environment management](03-org-auth-and-environment-management.md) — JWT setup and the credential redaction this note inherits
