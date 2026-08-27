# Licences & What They Gate

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The outermost gate — what a user may be *granted* before any permission is assigned. Internal licences only; **external and community user types are [05-experience-cloud · 08](../05-experience-cloud-lwr/08-licences-and-external-user-types.md)**. Editions and org shape are [01-admin · 01](../01-admin-and-declarative-platform/01-org-anatomy-and-editions.md).

## Core idea

A permission set cannot grant what the licence does not include. Salesforce's own documentation uses the image and it is worth keeping: **permissions are locks, licences are rings of keys** — assigning a permission a user's licence has no key for simply fails, and it usually fails by the checkbox not being there rather than by an error you can read. This is the layer people skip, because it looks commercial rather than architectural. It is not: the licence mix decides which access designs are even available to you, and discovering mid-build that half the user base cannot hold the Opportunity object is a re-architecture, not a configuration change.

## How it works

| Kind | How many per user | Grants | Example |
|---|---|---|---|
| **User licence** | exactly **one** | the baseline — which objects and features are reachable at all | Salesforce, Salesforce Platform, Identity |
| **Permission set licence (PSL)** | any number | an add-on capability, and **gates the permission sets that reference it** | Sales Planning, Pipeline Inspection, CRM Analytics |
| **Feature licence** | any number | a single feature flag on the user record | Marketing User, Knowledge User, Service Cloud User |
| **Usage-based entitlement** | org-level | a consumable, metered over a period | Experience Cloud monthly logins |

- **A PSL is a separate assignment from the permission set that needs it.** Assigning the permission set without the PSL fails; the two are managed on different parts of the user record, which is why "I assigned the permission set and nothing happened" is so common.
- **The Salesforce Platform licence excludes the core CRM objects** — Lead, Opportunity, Case, Campaign, Solution and Forecast are unreachable at any permission layer. Accounts, Contacts, Reports, custom objects, Flow and Apex are included.
- **Feature licences live as checkboxes on the User record**, not in a permission set, so they are invisible to a permission-set audit and easy to miss when cloning a user.
- **User Access Policies can assign PSLs and managed package licences**, which is the cleanest way to keep licence and permission assignment in step. → [05](05-user-access-policies-and-lifecycle.md)
- **Check consumption at Setup → Company Information**, which lists used and remaining counts for user licences, feature licences and PSLs separately.

## 2026 currency

Two 2026 shifts change licence reasoning rather than licence lists. **Salesforce Foundations is a $0 add-on** on the qualifying editions — free commercially, but it auto-provisions Data 360 and starts an Agentforce credit meter, so it changes the org's data and consumption posture without changing anyone's user licence → [01-admin · 18](../01-admin-and-declarative-platform/18-salesforce-foundations-and-org-strategy.md). And **Agentforce is metered in Flex Credits, not licensed per user** — an agent's *reach* is still governed by the licence and permissions of the user it runs as, which is the point [14](14-code-execution-context-and-security.md) develops. Credit mechanics live in [AI_Data/](../../AI_Data/README.md); do not duplicate them here.

## Gotchas

- **A missing licence hides the permission rather than refusing it.** You look for an unchecked box and find no box, which reads as a UI bug.
- **Only one user licence per user, ever.** Moving a user between licence types is a change to the User record with knock-on effects on role, profile and permission set validity.
- **Permission set licences are consumed on assignment, not on use.** A departed user still holds theirs until the assignment is removed, and Company Information can lag a revocation.
- **A permission set that references a PSL cannot be assigned without it** — including by a User Access Policy, which logs the shortfall in *Recent User Access Changes* rather than raising an error.
- **Platform-licensed users can own Accounts and Contacts but never Opportunities**, so any "sales ops on Platform licences" design dies at layer 1. → [01](01-security-model-layers-overview.md)
- **Feature licences do not appear in permission set exports.** A deployment that recreates profiles and permission sets faithfully still leaves Marketing User unchecked.
- **Editions gate what you can buy; licences gate what a user can hold.** Restriction rules existing in your edition is a separate question from a user being licensed for the object.

## Recall

Q: How many user licences can a single user hold?
A: Exactly one. Permission set licences and feature licences are add-ons and a user can hold any number of each.

Q: Why does assigning a permission set sometimes silently do nothing?
A: The permission set references a permission set licence the user has not been assigned. The PSL is a separate assignment.

Q: Which standard objects are unreachable on a Salesforce Platform licence?
A: Lead, Opportunity, Case, Campaign, Solution and Forecast. Accounts, Contacts, Reports and custom objects are included.

Q: Where do feature licences live, and why does that matter for audits?
A: As checkboxes on the User record — so they are invisible to a permission-set audit and are not carried by metadata deployments.

Q: What is Salesforce's own analogy for permissions versus licences?
A: Permissions are locks, licences are rings of keys. A permission without the matching key on the licence cannot be granted.

## Related

- [03 · Profiles & the permission-set-led model](03-profiles-and-the-permission-set-led-model.md) — what you assign once the licence permits it
- [05 · User Access Policies & lifecycle](05-user-access-policies-and-lifecycle.md) — automating PSL and permission set assignment together
- [05-experience-cloud · 08 Licences & external user types](../05-experience-cloud-lwr/08-licences-and-external-user-types.md) — the customer, partner and external identity half of this note
- [01-admin · 01 Org anatomy & editions](../01-admin-and-declarative-platform/01-org-anatomy-and-editions.md) — the note that hands off to this one
