# Apex Security: User Mode & FLS

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** How Apex decides whether the running user may touch an object and its fields, and how you deliberately exceed that. Record-level visibility is [11](11-sharing-keywords-and-apex-managed-sharing.md); the org-wide access model it enforces is [07-security](../07-security-and-sharing/INDEX.md).

> **What changed.** `WITH SECURITY_ENFORCED` **no longer compiles** at API 67.0. SOQL, SOSL, DML and `Database` methods now default to **user mode**, so elevating to system access is the thing you write explicitly — not the thing you get for free.

## Core idea

Apex answers two separate questions about every data operation: *may this user see this object and field* (CRUD and field-level security) and *may this user see this record* (sharing). For a decade the answer to both was an unconditional yes, and enforcement was something a careful developer opted into — which is why every older tutorial opens with a describe check. At 67.0 that default is inverted. A bare `[SELECT ...]` or `insert` now runs as the user, and `AccessLevel.SYSTEM_MODE` is how you step outside them. The practical shift is what the code review question becomes: no longer *did you remember to check FLS*, but *where does this codebase genuinely need to exceed its user, and is that decision written down anywhere*.

## How it works

| Mechanism | What it enforces | How it fails |
|---|---|---|
| `SELECT … WITH USER_MODE` | CRUD, FLS **and** sharing, across the whole query | `QueryException`, listing every violation |
| `SELECT … WITH SYSTEM_MODE` | nothing — explicit elevation of inline SOQL | — |
| `AccessLevel` argument on `Database` methods | the same, for dynamic SOQL and for DML | `QueryException` / `DmlException` |
| `Security.stripInaccessible(AccessType, records)` | FLS and object perms, by **removing** fields | never throws — returns a decision object |
| `Schema.DescribeFieldResult.isAccessible()` … | whatever you write yourself | whatever you write yourself |

- **The keywords are now for the exceptions.** Untagged SOQL and DML in a 67.0 class are already user mode; `WITH USER_MODE` is worth writing anyway as a statement of intent that survives a version bump.
- **`WITH USER_MODE` / `WITH SYSTEM_MODE` are inline-SOQL syntax only.** The `AccessLevel` enum is the equivalent for `Database.query`, `queryWithBinds`, `getQueryLocator` and every DML method. → [04](04-advanced-soql-sosl-and-dynamic-queries.md)
- **`stripInaccessible` is the tool for continuing rather than failing** — sanitising an untrusted payload before DML, or trimming a record before handing it to a component. `getRemovedFields()` reports exactly what it took out, per object.
- **Describe checks are now a UI concern.** `isAccessible()`, `isCreateable()`, `isUpdateable()` decide what to *render*; they are no longer the guard in front of the query.

```apex
List<Account> visible = [SELECT Id, Rating FROM Account WHERE Industry = :ind];  // user mode
SObjectAccessDecision d = Security.stripInaccessible(AccessType.UPDATABLE, incoming);
update d.getRecords();                                    // user mode DML, sanitised input
System.debug(d.getRemovedFields());                       // what was stripped, by object

List<Audit__c> log = Database.query(                      // deliberate elevation: the running
    'SELECT Id FROM Audit__c WHERE Account__c IN :ids',    // user cannot read the audit object
    AccessLevel.SYSTEM_MODE);
```

> **From my notes.** My 2021 page said to append `WITH SECURITY_ENFORCED` to every query and treat FLS as handled. **Both halves are wrong now.** The clause does not compile at 67.0 — and it never did what the page claimed: it checked only the `SELECT` and `FROM` clauses, ignored fields referenced in `WHERE`, could not resolve polymorphic fields such as `Owner` or `Task.WhatId`, and threw on the *first* violation so that fixing one exposed the next. `WITH USER_MODE` covers all four, and on a 67.0 class you get the enforcement whether you type it or not.

## 2026 currency

The reasoning matters more than the mechanics: the platform stopped assuming the surface in front of Apex had already filtered the data. That was a safe assumption when the caller was a Lightning page and is not when the caller may be an autonomous agent over MCP. The migration is deliberately asymmetric — the new defaults apply to classes **compiled at 67.0**, so nothing breaks on upgrade day, and the risk arrives later when someone bumps an old class's API version and its data-access semantics change underneath unchanged code. That is an argument for a written team convention, not a code comment. Sources and dates: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **The API version that matters is the one on the class containing the query**, not the caller's. A 67.0 service calling a 55.0 selector still gets system-mode SOQL out of the selector.
- **User mode enforces sharing too.** It is not an FLS-only switch — a query that used to return every record now returns only the user's, which reads as a data bug rather than a security change.
- **`stripInaccessible` does not check the operation itself.** It removes fields the user cannot touch; a user with no Create permission on the object still gets a `DmlException` from the `insert`.
- **`Database.getQueryLocator` takes an `AccessLevel` as well** — batch jobs are not exempt, and a user-mode locator filters the entire job's scope.
- **The `QueryException` lists every violated field at once.** Read the whole message; fixing them one at a time is a self-inflicted loop.
- **Triggers always run in system mode** and can no longer declare an access mode, so none of this applies inside trigger bodies. Put anything security-sensitive in the handler. → [11](11-sharing-keywords-and-apex-managed-sharing.md)
- **`AccessLevel.SYSTEM_MODE` in a code review is a question, not a defect** — but an unexplained one is the single most likely place a permission bypass hides.

## Recall

Q: What replaced `WITH SECURITY_ENFORCED`, and why is it not merely a rename?
A: `WITH USER_MODE`. It handles polymorphic fields, checks the `WHERE` clause and not just the `SELECT` list, and reports every FLS violation instead of only the first.

Q: What is the default execution mode for SOQL and DML in a class compiled at 67.0?
A: User mode — object permissions, field-level security and sharing are all enforced unless you opt out with `AccessLevel.SYSTEM_MODE` or `WITH SYSTEM_MODE`.

Q: Why does nothing break on the day an org upgrades to 67.0?
A: The new defaults apply to classes compiled at 67.0. Older classes keep their old behaviour until someone bumps their API version.

Q: When would you reach for `Security.stripInaccessible` instead of `WITH USER_MODE`?
A: When you want the operation to continue with the inaccessible fields removed rather than throw — typically sanitising an untrusted payload before DML.

Q: Does `stripInaccessible` guarantee the following DML will succeed?
A: No. It only removes fields. Object-level Create, Update or Delete permission is still checked by the DML itself.

## Related

- [11 · Sharing keywords & Apex managed sharing](11-sharing-keywords-and-apex-managed-sharing.md) — the record-level half of the same 67.0 flip
- [04 · Advanced SOQL, SOSL & dynamic queries](04-advanced-soql-sosl-and-dynamic-queries.md) — where `AccessLevel` is passed to `queryWithBinds` and injection defence lives
- [07-security · Access model](../07-security-and-sharing/INDEX.md) — the object and field permissions this note merely enforces
