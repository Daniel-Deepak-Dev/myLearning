# Release Cadence & Release Updates

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** The three-releases-a-year rhythm, how a release reaches your org, and the Release Updates mechanism. The release→API version map is not repeated here — it lives in [CURRENCY.md](../CURRENCY.md).

> **What changed.** Treating Release Updates as optional advisories to "review when convenient" is wrong. Every Release Update carries a **stated enforcement release**, and on that release the platform applies it whether or not you did anything.

## Core idea

Salesforce ships three major releases a year — Spring, Summer, Winter — and every org gets all of them. You do not choose to upgrade and you cannot decline; the only thing you control is *when you test*. Most of a release is additive and harmless, but a subset of changes alter existing behaviour in ways that could break customisations. Those are packaged as **Release Updates**: individually listed, individually testable, each with a deadline after which the platform enforces it for you. The admin's job is to work the Release Updates queue ahead of its deadlines, not to react afterwards.

## How it works

- **Preview window.** Roughly four to five weeks before general availability, sandboxes on **preview instances** are upgraded early. This is the only window in which you can run your org against the new release before production gets it — and you must have provisioned the sandbox on a preview instance to get it.
- **Instance upgrade.** Production instances are upgraded on scheduled maintenance windows, staggered across instances. Your date comes from Salesforce Trust, not from you.
- **Release Updates node.** Setup → Quick Find → **Release Updates**. Each entry shows what changes, the steps to take, and a **Complete Steps By** release — the release in which enforcement happens.
- **Test Run.** Many, not all, updates offer a Test Run: you switch the new behaviour on early, exercise the org, and switch it back. Where offered, this is the cheapest way to find breakage.
- **Salesforce can move the goalposts.** Updates are sometimes **postponed** to a later release or **cancelled** outright. Postponement is common enough to notice and never something to plan around.
- **API version pinning does not protect you.** Release Updates change *org behaviour*. Pinning an Apex class or an integration to an older API version does not opt it out.

## 2026 currency

The Summer '26 wave is where the security defaults flipped — user-mode Apex, `with sharing` by default, `WITH SECURITY_ENFORCED` no longer compiling. Those arrived as enforced platform defaults, not as opt-in toggles, which is exactly the pattern this note describes. The six of them are tabulated in [CURRENCY.md](../CURRENCY.md); running detail and dates live in [AI_Data/05-release-radar/](../../AI_Data/05-release-radar/README.md).

## Gotchas

- **Complete Steps By is a release, not a date you pick.** Missing it does not generate a warning; the behaviour simply changes.
- A Test Run is not always reversible in the way you assume — read the specific update before enabling it in a sandbox you still need.
- Enforced updates commonly surface as **failing Apex tests** rather than as user-visible errors, so a green test suite before the release proves nothing about after.
- Only sandboxes on **preview instances** get the early release. Provisioning one after the preview window opens is too late.
- Release notes are versioned by `release=NNN` in the Help URL — reading the wrong release's page is an easy and silent mistake.
- Updates already enforced can be **relaunched** by Salesforce when a related change ships; "I completed that one years ago" does not mean the node is empty.

## Recall

Q: How many major Salesforce releases ship per year, and can an org decline one?
A: Three — Spring, Summer, Winter. No org can decline; you only control when you test.

Q: What does the "Complete Steps By" column on a Release Update mean?
A: The release in which Salesforce enforces the update automatically, whether or not you have taken the steps.

Q: Does pinning Apex to an older API version opt you out of a Release Update?
A: No. Release Updates change org behaviour, which is not API-versioned.

Q: What is a Test Run, and is it offered for every Release Update?
A: A way to enable the new behaviour early and switch it back after testing. It is offered for many updates but not all.

Q: Which sandboxes receive a release early, and how long before GA?
A: Only sandboxes on preview instances, roughly four to five weeks ahead of general availability.

## Related

- [01 · Org anatomy & editions](01-org-anatomy-and-editions.md) — the environments a release lands on
- [CURRENCY.md](../CURRENCY.md) — the release→API map and the six flipped defaults
- [AI_Data/05-release-radar/](../../AI_Data/05-release-radar/README.md) — the running record of what changed and when
