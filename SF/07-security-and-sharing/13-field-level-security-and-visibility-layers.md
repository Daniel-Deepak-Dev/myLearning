# Field-Level Security & Visibility Layers

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The last gate — which columns of an accessible record a user may read or edit — and the two lookalike mechanisms that hide a field without securing it. Where FLS is enforced in code is [14](14-code-execution-context-and-security.md).

> **What changed.** *"Hide the field on the page layout"* was never security and is now demonstrably not: **only field-level security removes a field from the API, reports, search and every client.** Summer '26 also removes the old excuse for not auditing it — **Object Manager gained a read-only Field Access tab** that shows, per field, exactly which profile, permission set or permission set group grants it.

## Core idea

Three different mechanisms make a field disappear from a user's screen and **only one of them is security**. Field-level security removes the field everywhere — API, SOQL, reports, list views, search, exports, every LWC and every integration. Removing a field from a page layout removes it from *that layout* and nowhere else. A Dynamic Forms visibility rule removes it from the *rendered page* conditionally, based on record or user state. The first is a permission; the second is composition; the third is user experience. When someone says "that field is hidden", the only useful next question is *which of the three*, because two of them leave the value fully readable to anyone with a REST client or the report builder.

## How it works

| Mechanism | Where it applies | Is it security? |
|---|---|---|
| **Field-level security** | API, SOQL, reports, search, exports, UI — everywhere | **yes** |
| **Page layout** | that layout only | no |
| **Dynamic Forms visibility** | the rendered Lightning record page | no |

- **FLS is per field, per profile and per permission set**, with two independent flags: **Visible** and **Read-Only**. Access is the union, so one permission set granting edit beats five that do not.
- **Required and universally-required fields cannot be hidden.** A universally required field is required at the database level and overrides FLS entirely.
- **Master-detail and some system fields have no FLS.** Neither do fields on objects the user cannot access at all — the object gate has already answered.
- **The Summer '26 Field Access tab** sits at the bottom of each object in Object Manager, lists every field, and shows how access to it is granted across profiles, permission sets and permission set groups. It is **read-only** — you cannot change access from it. → [15](15-auditing-and-troubleshooting-access.md)
- **A formula field has no FLS of its own on its inputs.** Hiding a source field does not hide a formula that exposes it — the classic data leak in this area.
- **Code enforcement is now the default.** At API 67.0 Apex SOQL and DML run in user mode, so FLS is applied without `WITH USER_MODE` being written. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

## 2026 currency

**Unified Field Access review is the Summer '26 addition** and it closes a genuine gap: until now, answering *"why can this user see the salary field?"* meant opening every profile and permission set in turn, or writing Metadata API tooling. The tab answers it in one place. Two caveats worth carrying: it is **read-only**, so remediation still happens in the permission set; and it reports the field layer only — a user who cannot see the record at all will not appear as a problem here. The other Summer '26 change nearby is the **enhanced profile view's indirect-change preview**, which shows dependent permissions before you save them → [03](03-profiles-and-the-permission-set-led-model.md).

## Gotchas

- **A formula field bypasses the FLS of its inputs.** Hide `Salary__c` and expose it through `Comp_Summary__c` and you have hidden nothing.
- **Hiding a field on a layout leaves it in the API, reports and search.** Anyone with Data Loader or the report builder reads it unchanged.
- **Dynamic Forms visibility is rendering, not access.** The value can still reach the browser; treat it as UX. → [01-admin · 05](../01-admin-and-declarative-platform/05-dynamic-forms-and-lightning-app-builder.md)
- **Universally required fields ignore FLS.** You cannot hide one, and making a field universally required silently overrides every hide you configured.
- **The Field Access tab cannot fix anything.** It is a diagnostic; the change is still made in the profile or permission set.
- **FLS on a field used in a filter still leaks its existence** through report and list-view filter behaviour, even when the column is hidden.
- **Removing Visible does not remove the field from a flow.** A record-triggered flow runs in system context and reads it regardless. → [04-flow · 19](../04-flow-and-automation/19-flow-run-context-and-sharing.md)

## Recall

Q: Which of the three ways to hide a field is actually security?
A: Field-level security. Page layouts hide a field on one layout; Dynamic Forms visibility hides it in the rendered page. Both leave it readable via API, reports and search.

Q: What is the Summer '26 Field Access tab, and what can it not do?
A: A read-only tab in Object Manager showing which profiles, permission sets and permission set groups grant each field. It cannot change access.

Q: How does a formula field defeat field-level security?
A: FLS applies to the formula field itself, not to its inputs — so a formula referencing a hidden field exposes that value.

Q: What overrides field-level security entirely?
A: Making the field universally required. It is enforced at the database level and cannot be hidden.

Q: Does a record-triggered flow respect field-level security?
A: No. It runs in system context without sharing and reads fields regardless of FLS.

## Related

- [14 · Code execution context & security](14-code-execution-context-and-security.md) — where FLS is and is not enforced by running code
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — the wider set of tools the Field Access tab belongs to
- [02-apex · 10 Apex security: user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the 67.0 default that enforces this without being asked
- [01-admin · 05 Dynamic Forms & Lightning App Builder](../01-admin-and-declarative-platform/05-dynamic-forms-and-lightning-app-builder.md) — the visibility mechanism that is not security
