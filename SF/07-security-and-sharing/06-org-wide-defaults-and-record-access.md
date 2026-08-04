# Org-Wide Defaults & Record Access

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The baseline of record-level access and the grants layered on top of it — including the ones the platform creates without being asked. Who those grants reach is [08](08-groups-queues-and-the-grantee-model.md); the rules that create them are [09](09-sharing-rules-and-manual-sharing.md).

## Core idea

Org-wide defaults set the **floor**, and everything else in record access only ever raises it. That is why the design rule is counter-intuitive but absolute: **set the OWD to the most restrictive access anyone should have, then open it back up**. You cannot claw access back later with a sharing rule, because sharing rules are additive — the only thing that subtracts is a restriction rule ([11](11-restriction-rules.md)), and it is deliberately narrow. The part that catches architects is not the OWD itself but **implicit sharing**: a set of grants the platform maintains automatically between accounts and their children, and between portal users and their account, that appear in no rule you wrote and cannot be switched off.

## How it works

| OWD | Who sees the record |
|---|---|
| **Private** | owner, everyone above them in the hierarchy, plus explicit grants |
| **Public Read Only** | every internal user can read; only owner and hierarchy can edit |
| **Public Read/Write** | every internal user can read and edit |
| **Public Read/Write/Transfer** | as above plus change of owner — Case and Lead only |
| **Controlled by Parent** | the child's access is the parent's, exactly |

- **Every object has two OWDs — internal and external.** The external default governs Experience Cloud and portal users and cannot be more permissive than the internal one. → [05-experience-cloud · 07](../05-experience-cloud-lwr/07-guest-user-security-model.md)
- **`Grant Access Using Hierarchies`** is a per-object switch. It is **forced on for standard objects** and optional for custom ones; turning it off on a custom object stops managers inheriting their subordinates' records. → [07](07-role-hierarchy-and-ownership.md)
- **Implicit sharing is created by the platform and is not configurable.** The important cases: a contact, case, opportunity or order under an account grants **read** on the parent account; account access can imply access to its children depending on the child object's OWD; and a portal user's account and contact are implicitly shared to them.
- **Tightening an OWD triggers a full sharing recalculation** of that object and everything below it. On a large object this is measured in hours, not seconds. → [16](16-sharing-recalculation-and-performance.md)
- **Deferred sharing calculation** lets an admin batch a series of model changes and recalculate once, instead of once per change.

> **From my notes.** My 2025 Sharing & Visibility prep has the implicit-sharing trap twice, in two disguises, and it is worth memorising in the concrete form. *Account OWD is Private; a rep has Create/Edit on Opportunity. What access do they have to the parent Account?* **Read-only** — not none, and not edit. And when a finance analyst is temporarily granted one opportunity and turns out to be able to read the account and its contacts, **the cause is implicit sharing from Opportunity to Account and from Account to Contact**, not the role hierarchy. Temporary access to a child is permanent-feeling read access to a chunk of the parent's tree, and no rule you wrote will show it.

## 2026 currency

Record access is the most stable part of the platform and the OWD values have not changed. One Summer '26 change reaches into it from the side: **queues gained their own `Grant Access Using Hierarchies` setting**, so records owned by a queue no longer automatically flow up the role hierarchy — and the default differs between queues created before and after the release. Any model that assumed queue-owned records were visible to managers needs checking. → [08](08-groups-queues-and-the-grantee-model.md)

## Gotchas

- **You cannot restrict with a sharing rule.** If the OWD is too open, no amount of rule-writing fixes it — only changing the OWD does. → [11](11-restriction-rules.md)
- **Implicit sharing means "Private" is not private.** A user with access to a child record gets read on the parent account whether you wanted that or not.
- **`Controlled by Parent` is not a lookup behaviour.** It is master-detail, and it removes the child's own OWD, sharing rules and manual sharing entirely. → [08-data · 02](../08-data-modeling-and-large-data-volumes/02-relationships-deep-dive.md)
- **The external OWD is a separate setting that people forget exists.** Leaving it at the internal value is how guest and community users end up over-privileged. → [05-experience-cloud · 07](../05-experience-cloud-lwr/07-guest-user-security-model.md)
- **Loosening an OWD is fast; tightening it is a recalculation.** Plan tightening for a maintenance window and use deferred sharing for a batch of changes.
- **Sharing rules on a Public Read/Write object are dead configuration** that still consumes recalculation time and still appears in audits as intent.
- **`Grant Access Using Hierarchies` cannot be turned off for standard objects**, so "managers must not see their reports' opportunities" is unachievable declaratively on Opportunity.

## Recall

Q: What is the design rule for setting org-wide defaults?
A: Set the most restrictive access anyone should have, then grant back upwards. Nothing except a restriction rule subtracts.

Q: What is implicit sharing and why does it surprise people?
A: Grants the platform maintains automatically — child record access implying read on the parent account, portal users' own account and contact. It is not configurable and appears in no rule you wrote.

Q: How many org-wide defaults does an object have?
A: Two — internal and external. The external default cannot be more permissive than the internal one.

Q: What does `Controlled by Parent` remove?
A: The child's own OWD, sharing rules and manual sharing. Access is exactly the parent's.

Q: Which direction of OWD change is expensive, and what mitigates it?
A: Tightening — it forces a full sharing recalculation. Deferred sharing calculation batches several model changes into one run.

## Related

- [07 · Role hierarchy & ownership](07-role-hierarchy-and-ownership.md) — the automatic upward grant this baseline assumes
- [09 · Sharing rules & manual sharing](09-sharing-rules-and-manual-sharing.md) — the explicit grants layered on top
- [11 · Restriction rules](11-restriction-rules.md) — the only mechanism that reduces what this grants
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — how to see which of these actually granted a given record
