# Sharing Keywords & Apex Managed Sharing

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Record-level visibility in Apex — which keyword a class runs under, and how to grant access in code that the declarative model cannot express. Object and field permissions are [10](10-apex-security-user-mode-and-fls.md); the sharing model itself belongs to [07-security](../07-security-and-sharing/INDEX.md).

> **What changed.** A class with **no sharing keyword now defaults to `with sharing`**. It used to inherit the caller's context, which meant sharing silently went unenforced whenever such a class was the entry point. Bypassing sharing is now a deliberate `without sharing`. Separately, **triggers always run in system mode** and can no longer declare a sharing or access mode at all.

## Core idea

The sharing keyword answers exactly one question — *which records does this code see* — and it is independent of the object and field permissions covered in [10](10-apex-security-user-mode-and-fls.md). Those two used to move together in people's heads because both were off by default; at 67.0 both are on by default and they are enforced by different machinery, so it is worth keeping them apart. The second half of this topic exists because sharing rules are declarative and criteria-based, and some grants simply are not expressible that way — access derived from a related record, a rolling date window, or an external system's answer. **Apex managed sharing** is the escape hatch: you write rows into the object's `__Share` table yourself and tag them with a reason the platform will respect.

## How it works

| Declaration | Record visibility | When to use it |
|---|---|---|
| *(none)* | **`with sharing`** — the 67.0 default | anything you have not thought about |
| `with sharing` | running user's sharing rules enforced | say it out loud anyway; it survives a version bump |
| `without sharing` | sharing ignored; all records visible | a deliberate, reviewed elevation |
| `inherited sharing` | takes the caller's context; `with sharing` if entered directly | shared utilities and selectors called from both |

- **A share row has four fields that matter**: `ParentId` (the record), `UserOrGroupId` (who), `AccessLevel` (`Read`, `Edit` — never `All`, which is owner-only), and `RowCause` (why).
- **`RowCause` is the whole point.** A row with `RowCause = 'Manual'` is deleted the moment the record owner changes. A row tagged with an **Apex sharing reason** — declared on the custom object in Setup and referenced as `Schema.Project__Share.RowCause.Partner_Access__c` — survives owner changes and is visible in the sharing UI with your label.
- **Apex sharing reasons are custom-object only.** Standard objects have `AccountShare`, `OpportunityShare` and friends but no custom reasons, so a code-written share on them is a manual share with a manual share's fragility.
- **Register a recalculation class** on the object — a `Database.Batchable` that rebuilds the shares — so the platform can restore your grants after an OWD change or a `Recalculate Sharing` run. Without it, one admin action silently drops every row your code wrote.

```apex
List<Project__Share> shares = new List<Project__Share>();
for (Project__c p : scope) {
    shares.add(new Project__Share(
        ParentId      = p.Id,
        UserOrGroupId = p.Partner_User__c,
        AccessLevel   = 'Edit',
        RowCause      = Schema.Project__Share.RowCause.Partner_Access__c
    ));
}
// Writing shares is a privileged act — elevate on purpose, and keep the failures.
Database.SaveResult[] rs = Database.insert(shares, false, AccessLevel.SYSTEM_MODE);
```

> **From my notes.** My note on the `UserRecordAccess` query recorded it as the clean way to ask *can this user see this record*. It is — within two limits worth knowing before you design around it. **The query must filter on `RecordId`, and `RecordId IN :ids` is capped at 200 records**, so it does not bulkify the way ordinary SOQL does: 1,000 records means five queries against the 100-query limit. And it answers a *sharing* question only — `HasEditAccess` can be `true` for a user who has no Edit permission on the object at all.

## 2026 currency

The default flip is the meaningful change, and its shape is the same as user mode's: it applies to classes **compiled at 67.0**, so an inherited codebase does not change behaviour until someone bumps a class's API version. The class most likely to break is the shared utility that never declared a keyword and quietly ran `without sharing` because its caller did — that class now filters, and the symptom is missing rows rather than an exception. Triggers moving permanently to system mode is the other half: it removes an ambiguity but also means a trigger body is the wrong place for security-sensitive logic, which is an argument for the handler pattern in [06](06-triggers-and-the-handler-framework.md) regardless. Detail: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **Inner classes do not inherit the outer class's sharing declaration.** They take the default, which at 67.0 means an inner class inside a `without sharing` class now enforces sharing.
- **`with sharing` does not enforce CRUD or FLS.** A user with no read access to a field still gets its value out of a `with sharing` class on an older API version — that is [10](10-apex-security-user-mode-and-fls.md)'s job, and the two are enforced separately.
- **The two axes are genuinely independent at 67.0**: a `without sharing` class still runs its SOQL in user mode, so it sees every record but only the fields the user may read.
- **You cannot share a record with its owner**, and you cannot grant less than the org-wide default — both are insert errors, not silent no-ops.
- **Manual share rows vanish on owner change.** If a grant must outlive a reassignment it needs an Apex sharing reason, which means the object must be custom.
- **Without a registered recalculation class**, an admin clicking *Recalculate Sharing* wipes every row your Apex wrote and nothing reports it.
- **`without sharing` on the class that runs a batch's `execute()` does not elevate `start()`** — the `QueryLocator` carries its own `AccessLevel`. → [14](14-batch-apex-and-stateful-processing.md)

## Recall

Q: What does a class with no sharing keyword do at API 67.0?
A: It runs `with sharing`. Previously it inherited the calling class's context, so sharing went unenforced when that class was the entry point.

Q: Which keyword should a shared selector or utility class carry?
A: `inherited sharing` — it takes the caller's context and falls back to `with sharing` when something enters it directly.

Q: What is the difference between a `RowCause` of `'Manual'` and an Apex sharing reason?
A: A manual share is deleted when the record owner changes; a share tagged with an Apex sharing reason survives, and shows your label in the sharing UI.

Q: Why does Apex managed sharing need a registered recalculation class?
A: Because an OWD change or a *Recalculate Sharing* run rebuilds the share table, discarding rows the platform cannot regenerate itself.

Q: What are the two constraints on a `UserRecordAccess` query?
A: It must filter on `RecordId`, and `RecordId IN` accepts at most 200 records per query — so it does not bulkify like ordinary SOQL.

## Related

- [10 · Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) — the object and field half of the same 67.0 flip
- [06 · Triggers & the handler framework](06-triggers-and-the-handler-framework.md) — why security-sensitive logic belongs in the handler now that triggers are always system mode
- [07-security · Access model & record sharing](../07-security-and-sharing/INDEX.md) — the declarative sharing model that Apex managed sharing extends
