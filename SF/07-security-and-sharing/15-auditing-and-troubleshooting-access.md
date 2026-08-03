# Auditing & Troubleshooting Access

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** How to answer *"why can this user see this?"* and *"why can't they?"* from the org itself rather than by reading configuration. The layers being interrogated are [01](01-security-model-layers-overview.md)–[14](14-code-execution-context-and-security.md).

## Core idea

By this point the model has eight mechanisms that grant, three that subtract or narrow, two hierarchies, and a set of implicit grants nobody configured. **Reading the configuration no longer produces a reliable answer** — you have to ask the org. That shift is why this note exists as a topic rather than a tip: in a mature org, access questions are answered with tools, and an architect who reaches for the profile list first will be wrong slowly. The good news is that the native tooling finally caught up in Winter '25 and Summer '26, and the two most useful surfaces are free.

## How it works

| Question | Tool | Layer |
|---|---|---|
| what does this user have, and **who granted it**? | **User Access Summary** — *View Summary* on the user record, then *Access Granted By* | object, field, user perms |
| who grants access to **this field**? | **Field Access tab** in Object Manager *(Summer '26, read-only)* | field |
| who can see **this record**, and why? | the record's **Sharing** button / Sharing Hierarchy | record |
| programmatically, can user X read record Y? | `SELECT RecordId, HasReadAccess, HasEditAccess FROM UserRecordAccess WHERE UserId = … AND RecordId IN …` | record |
| **why** does this share row exist? | query the object's share table and read `RowCause` | record |
| who changed the configuration? | **Setup Audit Trail** | all |
| org-wide, five lenses over the whole model | **Who Sees What Explorer** — objects, records, users, system permissions, profiles & permission sets | all |

- **`Access Granted By` is the row-level action that ends most arguments.** It names the profile, permission set or permission set group responsible for a specific permission. → [03](03-profiles-and-the-permission-set-led-model.md)
- **`RowCause` distinguishes a rule-derived share from a manual one**, which is what tells you whether a grant will survive an owner change. → [09](09-sharing-rules-and-manual-sharing.md)
- **Group membership is queryable** through `Group` and `GroupMember`, so "who is actually in this group" never needs to be taken on trust. → [08](08-groups-queues-and-the-grantee-model.md)
- **Who Sees What Explorer lives in Security Center**, which is a **paid add-on** — check entitlement before designing a process around it. **Security Center *Essentials* went free in every org in July 2026 and does not include the Explorer**, so "we have Security Center now" is not the same answer. The product and posture story is [24](24-security-center-and-health-check.md).
- **An audit team needs `View All Users` and `View Setup and Configuration`** — not `View All Data`, which is a far larger grant than the job requires.

> **From my notes.** My 2025 page on querying `UserRecordAccess` **from a Flow** records a trap the Apex form does not have. In a *Get Records* element you must **not** use *Store All Fields*: Flow tries to retrieve unsupported fields such as `Id` and the element errors ([Salesforce KB 000383422](https://help.salesforce.com/s/articleView?id=000383422&language=en_US&type=1)). Select `RecordId` plus only the access fields you need, store each in its own variable, and enable *When no records are returned, set specified variables to null* — because "no access" **is** the zero-row case and without that setting it fails downstream instead of answering. The SOQL-side constraints still apply: filter on `RecordId`, at most **200** per query, and the answer is about **sharing only**. → [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

## 2026 currency

Two additions changed what is possible without third-party tooling. **User Access Summary gained *Access Granted By* in Winter '25**, which is the first native answer to "which permission set is responsible". **Summer '26 added the Field Access tab** in Object Manager, covering the field layer the same way → [13](13-field-level-security-and-visibility-layers.md). Both are read-only diagnostics; remediation still happens in the permission set. Against that, one thing got *harder* to see: restriction rules leave the share rows in place and filter afterwards, so no share-table query reveals them ([11](11-restriction-rules.md)).

## Gotchas

- **Restriction rules are invisible from the grant side.** Share rows still exist and every sharing audit will report access the user does not actually have.
- **`UserRecordAccess` answers a sharing question only.** `HasEditAccess` can be `true` for a user with no Edit permission on the object at all.
- **The Field Access tab cannot change anything.** It is diagnosis; the fix is still in the profile or permission set.
- **Teams and territories scatter grants across records**, so Setup shows you nothing — audit them by querying `AccountTeamMember`, `OpportunityTeamMember` and the territory model. → [10](10-teams-territories-and-account-sharing.md)
- **Recent User Access Changes is not an audit trail** — it drops entries that were later overridden. Setup Audit Trail is the durable record. → [05](05-user-access-policies-and-lifecycle.md)
- **Session-based permission sets do not show as active** in a summary taken outside the qualifying session. → [04](04-permission-set-groups-and-muting.md)
- **Debug in layer order.** Licence, then login, then object, then record, then field — jumping to sharing first is the habit that costs the afternoon. → [01](01-security-model-layers-overview.md)

## Recall

Q: Which native tool names the profile or permission set responsible for a specific permission?
A: User Access Summary on the user detail page — *View Summary*, then the *Access Granted By* row action. Improved in Winter '25.

Q: What does the Summer '26 Field Access tab give you, and what can it not do?
A: It shows how each field's access is granted across profiles, permission sets and permission set groups. It is read-only and cannot change access.

Q: Why can a share-table audit report access a user does not have?
A: Restriction rules filter after sharing resolves. The share rows remain; the records are simply not returned.

Q: What two permissions should an access-audit team be granted?
A: `View All Users` and `View Setup and Configuration`. `View All Data` is a much broader grant than the task needs.

Q: What is the constraint on a `UserRecordAccess` query?
A: It must filter on `RecordId`, takes at most 200 records per query, and answers about sharing only — not object or field permissions.

## Related

- [01 · Security model layers overview](01-security-model-layers-overview.md) — the order to debug in
- [13 · Field-level security & visibility layers](13-field-level-security-and-visibility-layers.md) — the field layer and its new tab
- [11 · Restriction rules](11-restriction-rules.md) — the one thing none of these tools shows from the grant side
- [01-admin · 17 Setup Audit Trail & monitoring](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md) — the durable record of configuration change
