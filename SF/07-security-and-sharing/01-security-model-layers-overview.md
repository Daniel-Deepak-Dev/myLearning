# Security Model Layers Overview

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The mental model the other 23 notes hang off — which layer answers which question, and in what order. Every layer has its own note; this one exists to stop you debugging the wrong one.

## Core idea

Salesforce access is not one system. It is five independent gates, each answering a different question, and a user needs **all** of them to pass. The order matters because it is also the debugging order: a licence problem and a sharing problem produce completely different symptoms, and the commonest wasted afternoon is tuning sharing rules for a user whose licence never permitted the object. The second thing to internalise is that the gates are not all shaped the same way. Object, record and field access are **granted** — a union of everything assigned, where more assignments mean more access and nothing subtracts. Restriction rules are the exception and they **subtract**. Scoping rules do neither: they change the default view without changing access at all.

## How it works

| # | Layer | Question | Granted by | Note |
|---|---|---|---|---|
| 1 | **Licence** | may this user be *granted* the feature at all? | user licence, PSL, feature licence | [02](02-licences-and-what-they-gate.md) |
| 2 | **Org** | may this user log in, from here, now? | login hours, IP ranges, MFA, session | [17](17-authentication-and-mfa.md), [18](18-session-security-login-policies-and-step-up.md) |
| 3 | **Object** | may this user create/read/edit/delete this object? | profile + permission sets | [03](03-profiles-and-the-permission-set-led-model.md), [04](04-permission-set-groups-and-muting.md) |
| 4 | **Record** | *which* rows of that object? | OWD → hierarchy → sharing → teams | [06](06-org-wide-defaults-and-record-access.md)–[10](10-teams-territories-and-account-sharing.md) |
| 5 | **Field** | which columns of those rows? | field-level security | [13](13-field-level-security-and-visibility-layers.md) |

- **Layers 3–5 are additive.** Access is the union of the profile and every assigned permission set. There is no "deny" checkbox; you remove access by removing an assignment, not by adding one.
- **`View All` and `Modify All` short-circuit layer 4** for one object. **`View All Data` / `Modify All Data`** short-circuit it for the whole org — and `Modify All Data` is effectively administrator.
- **Restriction rules subtract from layer 4** and are the only thing in the model that does. → [11](11-restriction-rules.md)
- **Scoping rules are not a layer.** They set the default filter on list views, reports and SOQL; the user can still widen it back. → [12](12-scoping-rules.md)
- **Code can bypass layers 3–5 deliberately.** Apex defaults to user mode at 67.0, but Flow's triggered types do not. → [14](14-code-execution-context-and-security.md)

## 2026 currency

The headline for this area is a change that **did not happen**: Salesforce announced in January 2023 that permissions would be retired from profiles starting Spring '26, and **cancelled that retirement on 6 June 2026**. Profiles keep their permissions with no end-of-life date; permission-set-led design is a recommendation, not a deadline. → [03](03-profiles-and-the-permission-set-led-model.md), [../CURRENCY.md](../CURRENCY.md)

Two Summer '26 changes touch the layers themselves rather than the tooling: **queues gained a `Grant Access Using Hierarchies` setting** whose default differs between new and existing queues ([08](08-groups-queues-and-the-grantee-model.md)), and **Object Manager gained a read-only Field Access tab** that finally answers *which* permission set grants a field ([13](13-field-level-security-and-visibility-layers.md)).

## Gotchas

- **A licence failure looks like a permission failure.** The checkbox is missing or greyed out rather than unchecked — you cannot grant a Platform-licensed user the Opportunity object at any layer. → [02](02-licences-and-what-they-gate.md)
- **Object access without record access shows an empty list view**, not an error. Users report "the tab is broken".
- **Record access without field access shows the record with blank columns.** Users report "the data is missing".
- **`View All Data` is not `Modify All Data`**, and neither is a role. Both are user permissions and both are audit findings when assigned casually.
- **Layer 4 has no effect on objects whose OWD is Public Read/Write** — sharing rules on such an object are dead configuration that still costs recalculation time. → [16](16-sharing-recalculation-and-performance.md)
- **Hiding a field on a layout is not layer 5.** Three mechanisms hide a field and only FLS is security. → [13](13-field-level-security-and-visibility-layers.md)
- **Debug in layer order.** Licence → login → object → record → field. Jumping to sharing first is the habit worth breaking. → [15](15-auditing-and-troubleshooting-access.md)

## Recall

Q: What are the five gates a user must pass, in order?
A: Licence, org (login), object, record, field. All five must pass; they answer different questions.

Q: Which layer is subtractive, and why does that matter?
A: Restriction rules subtract from record access. Everything else is a union, so "the sum of everything granted" stopped being the complete answer.

Q: A user sees the tab and an empty list view. Which layer is failing?
A: Record access — object access clearly passed, or the tab would not render.

Q: Do scoping rules restrict access?
A: No. They set a default filter on list views, reports and SOQL; the user can widen it again.

Q: What happened to the plan to retire permissions from profiles?
A: It was cancelled on 6 June 2026. Profiles keep their permissions and no end-of-life date exists.

## Related

- [02 · Licences & what they gate](02-licences-and-what-they-gate.md) — the outermost gate, and the one people forget is a gate
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — how to ask the org which layer is refusing
- [02-apex · 10 Apex security: user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the same layers as enforced by code at 67.0
