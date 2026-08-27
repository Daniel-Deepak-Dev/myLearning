# Apex Test Strategy in CI

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** Which tests run, where, and what a failure is allowed to block. How to *write* an Apex test is [02-apex · 20–21](../02-apex-and-triggers/20-apex-testing-fundamentals.md); this note is about the pipeline's relationship with the test suite.

## Core idea

Salesforce is the rare platform where the test suite is not optional and not yours to tune down: **75% org-wide coverage is a deployment gate enforced by the platform**, and every production deploy pays for a test run whether the change touched Apex or not. That inverts the usual economics. Elsewhere a slow suite is a productivity tax; here it is a *release-window* constraint, because the validation is the release.

The strategy question is therefore not "how do we get coverage up" but **"which subset of tests must run for this change, and how do we keep the full run under the window."**

## How it works

- **Four test levels, plus a fifth in Beta.** `NoTestRun` (sandbox only, and not quick-deployable), `RunSpecifiedTests`, `RunLocalTests` (everything except managed packages — the production default), `RunAllTestsInOrg`, and **`RunRelevantTests` (Beta from Spring '26)** → [05](05-metadata-api-and-deployment-mechanics.md).
- **`RunRelevantTests` is the delta strategy the platform now offers**, and it moves the work from your pipeline into your annotations: it runs only what the deployment touches, steered by `@IsTest(testFor='ApexClass:MyClass')`, with `@IsTest(critical=true)` forcing a test to always run. Nobody backfills those annotations onto a legacy suite, which is the real adoption cost.
- **`RunSpecifiedTests` is the hand-rolled version of the same idea**, and it has a trap: the specified classes must themselves deliver 75% coverage **of every class in the deployment**, not of the org. Getting the list wrong fails the deploy after the tests have run.
- **Run tests asynchronously and poll** — `sf apex run test --wait 0` then `sf apex get test --test-run-id` — so a long suite does not hold a job step's connection open.
- **Coverage as a pipeline artifact.** `--code-coverage --result-format json` gives per-class numbers; publish them, because "75% org-wide" hides a 0%-covered class behind a 99%-covered one.
- **Two suites, two gates.** Fast unit tests (mocked, `SeeAllData=false`) block the PR; slow integration-ish tests run nightly against a persistent sandbox and block the release, not the commit.
- **Jest and Apex are different jobs.** LWC tests need no org at all → [03-lwc · 15](../03-lwc-and-slds/15-lwc-testing-with-jest.md), so they run first and fail fastest.

## 2026 currency

The **user-mode default at API 67.0** changes what a passing test proves. Apex now runs in user mode unless told otherwise, so a test that sets up data as an admin and asserts on rows a portal user should never see can pass in a way production will not reproduce → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md). Tests written before the flip frequently `runAs` nobody, and those are exactly the tests that now certify the wrong thing. **`@IsTest(SeeAllData=true)` is worse than it was**, because the data it sees is filtered by sharing too — so the same test gives different results in two orgs with the same data.

## Gotchas

- **Parallel test execution is the classic CI failure and it is not deterministic.** Concurrent classes contending on the same rows produce `UNABLE_TO_LOCK_ROW`, which looks like a flaky test and is really a data-design problem → [08-data · 12](../08-data-modeling-and-large-data-volumes/12-record-locking-and-concurrency.md).
- **Disabling parallel execution is a real lever** (Setup → Apex Test Execution, or `--synchronous`), and it trades a green build for a much longer one. Decide deliberately rather than after the third rerun.
- **`@TestSetup` resets DML limits between test methods but not SOQL limits** — a genuine seed-note gotcha, still true.
- **Coverage is computed at deploy time, not at test time.** A class covered only by a test that was deleted in the same commit fails the deploy, not the test run.
- **Managed-package tests do not count**, which is why `RunLocalTests` is the honest default and `RunAllTestsInOrg` mostly buys time you did not need to spend.
- **Test data that depends on org configuration is a time bomb** — a record type or picklist value renamed in production makes a test fail only in production.
- **A test that only asserts "no exception was thrown" is coverage, not a test.** It will keep the deploy gate happy through the entire regression it was supposed to catch.

## Recall

Q: What does `RunSpecifiedTests` actually have to satisfy?
A: The named classes must produce at least 75% coverage of **every class in that deployment** — org-wide coverage is not the measure being applied.

Q: Why does `UNABLE_TO_LOCK_ROW` show up in CI but rarely locally?
A: CI runs test classes in parallel, so classes touching the same parent records contend for locks; a single-threaded local run never overlaps them.

Q: What does `RunRelevantTests` need in order to work?
A: `@IsTest(testFor=…)` annotations on the suite — Beta from Spring '26, and useless on a codebase nobody annotates. `@IsTest(critical=true)` forces a test to run regardless.

Q: How did the API 67.0 security default change test meaning?
A: Apex runs in user mode, so tests must establish a running user deliberately — an admin-context test can now pass while the production behaviour differs.

Q: When is coverage evaluated?
A: At deployment, against the classes in the deployment — not when the tests are written or run ad hoc.

## Related

- [02-apex · 20 Apex testing fundamentals](../02-apex-and-triggers/20-apex-testing-fundamentals.md) — the writing discipline this pipeline depends on
- [02-apex · 21 Apex testing advanced & mocking](../02-apex-and-triggers/21-apex-testing-advanced-and-mocking.md) — Stub API, and how to make the fast suite fast
- [14 · CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md) — the jobs these levels are configured in
- [08-data · 12 Record locking & concurrency](../08-data-modeling-and-large-data-volumes/12-record-locking-and-concurrency.md) — why parallel tests deadlock
