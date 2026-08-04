# Sharing Rules & Manual Sharing

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The explicit record grants layered on the OWD — declarative rules, ad-hoc shares, and the share rows underneath both. Grantees are [08](08-groups-queues-and-the-grantee-model.md); writing share rows from code is [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md).

## Core idea

Everything here reduces to rows in a **share table**. Every object whose OWD is not Public Read/Write has one — `AccountShare`, `OpportunityShare`, `Project__Share` — and every grant, whoever made it, is a row in it with four meaningful columns: which record, which grantee, what access level, and **why**. That last column, `RowCause`, is the one that matters architecturally, because it decides the row's lifetime. A row created by a sharing rule is owned by the rule and rebuilt whenever the rule recalculates. A row created by hand has `RowCause = 'Manual'` and is **deleted the moment the record's owner changes**. Knowing which kind of row you have is the difference between a grant that survives a reorganisation and one that quietly evaporates.

## How it works

| Mechanism | `RowCause` | Survives owner change | Recalculated |
|---|---|---|---|
| **Owner-based sharing rule** | `Rule` | yes | on rule or membership change |
| **Criteria-based sharing rule** | `Rule` | yes | on record field change |
| **Guest user sharing rule** | `GuestRule` | yes | read-only grants only |
| **Manual share** (*Sharing* button) | `Manual` | **no** | never |
| **Apex managed sharing** | your custom reason | yes | only if you register a recalculation class |

- **Sharing rules grant, never restrict**, and only ever run in one direction: from a set of records to a grantee, at Read Only or Read/Write.
- **Owner-based rules key off who owns the record**; **criteria-based rules key off field values** and re-evaluate when those fields change, which makes them the more expensive of the two at volume.
- **Manual sharing needs the *Sharing* button**, which only appears when the object's OWD is more restrictive than Public Read/Write — the button's absence is the OWD telling you there is nothing to grant.
- **Access levels are Read Only, Read/Write and Full Access**, and Full Access is owner-only — you cannot grant it, and you cannot grant *less* than the OWD.
- **Rule limits are per object and per type**, and criteria-based rules are the scarcer of the two; check the current per-object caps before designing a model that needs dozens.
- **Guest sharing rules are the only way a guest user sees a record**, are read-only by construction, and guests cannot own records at all. → [05-experience-cloud · 07](../05-experience-cloud-lwr/07-guest-user-security-model.md)

## 2026 currency

Sharing rules themselves are unchanged, but two things around them are. **Queue-owned records may no longer flow up the hierarchy** ([08](08-groups-queues-and-the-grantee-model.md)), which changes what an owner-based rule on a queue actually reaches. And **restriction rules subtract from whatever this note grants** ([11](11-restriction-rules.md)) — so a sharing rule is now a *proposal* rather than a guarantee, and reading only the sharing rules no longer tells you the answer. That is the single most under-known change in this area.

## Gotchas

- **A manual share dies on owner change.** Every one of them, silently. A grant that must outlive a reassignment needs a sharing rule or an Apex sharing reason. → [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)
- **No *Sharing* button means the OWD is Public Read/Write.** People raise this as a bug; it is the model working.
- **You cannot grant below the OWD**, and you cannot share a record with its owner — both are errors, not silent no-ops.
- **Criteria-based rules recalculate on field change**, so a nightly integration that touches the criteria field re-runs sharing for everything it touched.
- **Deleting a sharing rule deletes its rows immediately.** There is no soft removal and no report of who just lost access.
- **Sharing rules cannot reference a formula field or a cross-object field** in their criteria, which is the usual reason a "criteria-based rule" ends up as an Apex managed share.
- **Guest sharing rules cannot grant edit.** Any tutorial that grants a guest write access is describing a pre-2021 org. → [04-flow · 21](../04-flow-and-automation/21-flow-for-external-and-guest-users.md)

## Recall

Q: What does every sharing mechanism ultimately produce?
A: A row in the object's share table, with a record, a grantee, an access level and a `RowCause`.

Q: Why does a manual share sometimes disappear on its own?
A: It has `RowCause = 'Manual'`, and manual rows are deleted when the record's owner changes.

Q: When is the *Sharing* button absent from a record?
A: When the object's OWD is Public Read/Write — there is no access left to grant.

Q: What is the difference between an owner-based and a criteria-based sharing rule?
A: Owner-based keys off the record's owner; criteria-based keys off field values and re-evaluates whenever those fields change.

Q: Can a sharing rule reduce access?
A: No. Sharing rules only grant. Only a restriction rule subtracts.

## Related

- [06 · Org-wide defaults & record access](06-org-wide-defaults-and-record-access.md) — the floor these rules raise, and the reason the button appears
- [08 · Groups, queues & the grantee model](08-groups-queues-and-the-grantee-model.md) — who the rules grant to
- [11 · Restriction rules](11-restriction-rules.md) — why a sharing rule is now a proposal, not a guarantee
- [02-apex · 11 Sharing keywords & Apex managed sharing](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) — writing share rows that outlive an owner change
