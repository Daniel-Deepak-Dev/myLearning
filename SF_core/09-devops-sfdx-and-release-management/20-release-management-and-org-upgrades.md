---
vault: SF_core
area: 09-devops-sfdx-and-release-management
format: dense
status: learning
created: 2026-08-04
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 17
tags: [currency-warning]
---
# Release Management & Org Upgrades

**Scope:** The releases you do not control — Salesforce's three a year — and the operating rhythm around them. The admin-side feature view is [01-admin · 02](../01-admin-and-declarative-platform/02-release-cadence-and-release-updates.md); this note is the release manager's calendar and gates.

> **What changed.** Release Updates are **not a recommendations list**. Each one carries an enforcement release, and on that date it **auto-activates whether or not anyone tested it**. Guidance that treats the preview window as optional, or Release Updates as something to review "when we get to it", describes a platform that stopped existing years ago. The only variable you control is whether the change is discovered in a sandbox in May or in production in June.

## Core idea

Salesforce ships three major releases a year into an org you own but do not version. That inverts normal release management: your own deployments are the predictable part, and the **uncontrolled** change is a vendor upgrade landing on a date set by which instance your org happens to sit on.

So release management here is two calendars kept in one place — your pipeline's, and Salesforce's — and the discipline is making sure they never collide. Deploying a release during your org's upgrade weekend is a self-inflicted incident.

## How it works

- **Three releases a year**, Spring / Summer / Winter, each rolled out over several weekends rather than on one date.
- **Your date is instance-specific.** Salesforce Trust status (`status.salesforce.com`) → search your My Domain or instance → **Maintenance** tab → filter **Major Release**. That is the authoritative date; a blog's "release date" is the first weekend, not yours.
- **Preview sandboxes are the test bed**, and they are earned by *timing*: a sandbox has to sit on a preview instance before the cutoff, so a refresh scheduled a day late costs you the whole window. For Summer '26 the checkpoint was **7 May 2026** with preview from **8–9 May**, ahead of production rollouts on **9 May, 5 June and 12 June**. For **Winter '27** it was **27 Aug 2026, 6:00 PM PT**; preview instances upgraded on **28–29 Aug**, and the last non-preview instances on **9–10 Oct 2026**.
- **Setup → Release Updates is the work list.** Each item states what changes, what to test, and the release in which it is **enforced**.
- **Freeze the pipeline across your upgrade weekend.** Nothing deploys, nothing validates — an in-flight validation is invalidated by the upgrade anyway.
- **Re-run the regression suite after the upgrade, not before.** The pre-upgrade run tells you about the old platform.

## 2026 currency

Summer '26 is the release where "enforced" stopped being abstract, and the sharpest example is small: the **no-argument-constructor requirement for custom Apex types used as invocable action inputs**. The requirement actually starts at **API 66.0** — the release-note ID carries `_v66` — and Summer '26 is when the Release Update auto-activates, which is why it is so widely mis-dated to 67.0. It **breaks existing Agentforce Apex actions**, because declaring any constructor with arguments removes the compiler-generated default → [02-apex · 22](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md). The pattern generalises: read the release-note ID, not the marketing date, and test the enforced items first — the security defaults, then anything touching authentication or Apex behaviour. Winter '27 adds a variant: an enforcement **date that is not a release weekend**. The *Assign Use Any API Auth Permission for SOAP login()* Release Update is enforced on **1 December 2026** in every org, sandboxes included — so a script or tool still logging in through SOAP `login()` needs that permission before then, not before an upgrade.

## Gotchas

- **The API version in a bundle does not follow the org.** An upgraded org still runs your class at whatever `<apiVersion>` it was saved with — which is how a security default flip misses the class that needed it most.
- **Preview and non-preview sandboxes diverge for a month.** A test that passes in one proves nothing about the other, and both are "the sandbox" in conversation.
- **Release Updates have staggered enforcement.** Three items on the page can be enforced in three different releases; sorting by due date is the only sane way to read it.
- **Activating an update early is reversible only until it is enforced.** After that the toggle is gone, so the early activation *is* the test.
- **Managed packages upgrade on their own schedule**, which is a fourth calendar nobody tracks until a push upgrade lands mid-sprint.
- **An org's instance can change.** A Hyperforce migration or an instance refresh moves your maintenance window without moving your calendar invite → [23](23-hyperforce-and-instance-operations.md).
- **"We'll test in the preview sandbox" needs a named owner.** The window is roughly four weeks and it closes silently.

## Recall

Q: Where is the authoritative upgrade date for a given org?
A: Salesforce Trust status — the instance's Maintenance tab, filtered to Major Release. Not the general release date.

Q: What happens to a Release Update nobody activates?
A: It auto-activates in its enforcement release. The choice is only *when* you find out.

Q: How does a sandbox end up on the preview instance?
A: By being created or refreshed before the preview cutoff — for Winter '27, 6:00 PM PT on 27 Aug 2026, with preview from 28–29 Aug.

Q: Why was the invocable no-arg-constructor change mis-dated to 67.0?
A: The requirement begins at API 66.0; Summer '26 is only when its Release Update auto-activates.

Q: Why freeze deployments during the upgrade weekend?
A: The upgrade invalidates in-flight validations, and a failure during the window is indistinguishable from a platform issue.

## Related

- [01-admin · 02 Release cadence & Release Updates](../01-admin-and-declarative-platform/02-release-cadence-and-release-updates.md) — the same calendar from the admin's side
- [23 · Hyperforce & instance operations](23-hyperforce-and-instance-operations.md) — what moves your maintenance window
- [14 · CI/CD with GitHub Actions](14-ci-cd-with-github-actions.md) — the pipeline this calendar freezes
- [25 · Deployment rollback, hotfix & destructive changes](25-deployment-rollback-hotfix-and-destructive-changes.md) — the hotfix path a frozen pipeline still needs

## Sources

- [Salesforce Sandbox Preview Instructions](https://help.salesforce.com/s/articleView?id=000391927&language=en_US&type=1) — Salesforce Help · via search 2026-10-28 · Winter '27 cutoff 27 Aug 2026 at 6:00 PM PT (01:00 UTC 28 Aug); preview instances upgraded 28–29 Aug; non-preview instances 9–10 Oct 2026
- [Assign Use Any API Auth Permission for SOAP login() (Release Update)](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_api_soap_login.htm&release=264&type=5) — Salesforce Help · via search 2026-10-28 · Winter '27 release note: enforced on 1 December 2026 across all orgs and environments, including sandboxes; `INSUFFICIENT_ACCESS` without the permission

## History

- 2026-10-28 · Winter '27 currency check: added the Winter '27 preview and rollout dates, and a Release Update enforced on a date between releases
