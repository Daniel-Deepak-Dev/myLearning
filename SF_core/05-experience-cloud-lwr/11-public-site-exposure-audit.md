# Public Site Exposure Audit

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** The standing audit for any site a stranger can reach — what to check, in what order, and what "safe" means when you inherit one. The *model* is [07](07-guest-user-security-model.md); this is the runbook. Added in phase 18, beyond the original plan.

> **What changed.** Guest hardening stopped being a design decision and became an **operational control with an audit cadence**. On **7 March 2026** Salesforce issued a security advisory about an active campaign against over-permissive Experience Cloud guest configurations, with data claimed from hundreds of organisations. **No platform vulnerability was involved** — every affected org was reachable through settings the admin owned. The practical consequence: a site that was correctly configured at launch is not evidence it is correctly configured now, and "we hardened it in 2021" is not an answer.

## Core idea

Two properties make a public site different from every other surface in the org. **It is reachable without credentials**, so there is no login event to alert on and no user to disable. And **guest page views are free**, so there is no cost signal when someone enumerates it. Anything a guest can reach is reachable continuously, cheaply, by anyone, forever.

That flips the review question. Internally you ask *does this user need this access?* On a public site you ask **what would this site hand over if someone read everything it will serve?** The audit below is that question broken into checkable parts, ordered by how much damage each item does when it is wrong.

## How it works

Work the guest profile of **every** site — including inactive and preview ones — in this order:

1. **`API Enabled`.** Remove it. With it, the guest surface is a queryable API rather than a set of pages, and the record ceiling that limits page-based access no longer applies.
2. **Object permissions.** Read and create are the only ones grantable; grant neither unless a page genuinely needs it. Enumerate what is on, not what you remember turning on.
3. **Field-level security.** Objects are the coarse gate; a single exposed field carries the sensitive data. Use the **Field Access tab** in Object Manager to see what grants each field → [07-security · 13](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md).
4. **External OWD.** Must be Private for anything not deliberately public, and it cannot be more permissive than the internal OWD → [07-security · 06](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md).
5. **Guest sharing rules.** Read the criteria, not the name. A rule written to expose three articles can match the object.
6. **Apex classes and flows on the guest profile.** Every `@AuraEnabled` method is an endpoint; every entry on *Enabled Flow Access* is something a stranger can run → [06](06-custom-lwc-in-lwr-sites.md), [04-flow · 21](../04-flow-and-automation/21-flow-for-external-and-guest-users.md).
7. **Apex API version.** A class below 67.0, or one using `AccessLevel.SYSTEM_MODE`, is not enforcing the access model for the guest that calls it → [07-security · 14](../07-security-and-sharing/14-code-execution-context-and-security.md).
8. **Self-registration profile**, if enabled — it is granted to everyone who asks → [10](10-authentication-self-registration-and-sso.md).

## Gotchas

- **Every site has its own guest user.** Auditing one proves nothing about the others; an abandoned preview site is a live surface.
- **The record ceiling people rely on is not a control.** Page-based limits do not bound what an API-enabled guest can retrieve, and the 2026 campaign is what that looks like in practice.
- **Custom components do not enforce anything.** CRUD and FLS are the Apex controller's job; the component in front is decoration → [06](06-custom-lwc-in-lwr-sites.md).
- **A field added later inherits the object's guest access.** Schema changes silently widen an audited surface — re-run this after every release.
- **Verbose error messages are an exposure class of their own** — object names, field names and record counts all leak through them.
- **Event Monitoring's free tier covers Experience Cloud traffic thinly.** Detection is not the control here; configuration is → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

## Recall

Q: What is the single highest-value item to remove from a guest profile?
A: `API Enabled` — with it, the site is a queryable data surface rather than a set of pages.

Q: Why is "we hardened it at launch" not an acceptable answer?
A: Schema and permission changes widen the guest surface over time, so exposure is a standing audit item, not a one-off task.

Q: Was the March 2026 Experience Cloud campaign a platform vulnerability?
A: No. Salesforce's advisory is explicit that it exploited over-permissive customer configurations, not a platform defect.

Q: Which sites need auditing?
A: All of them, including inactive and preview sites — each has its own guest user, and preview status restricts membership, not reachability.

Q: What protects data behind a guest-facing `@AuraEnabled` method?
A: Only that class's own enforcement. A class below API 67.0, or one in system mode, isn't applying the access model at all.

## Related

- [07 · Guest user security model](07-guest-user-security-model.md) — the platform controls this audit checks
- [06 · Custom LWC in LWR sites](06-custom-lwc-in-lwr-sites.md) — why the controller, not the component, is the boundary
- [07-security · 26 Secure coding checklist](../07-security-and-sharing/26-secure-coding-checklist.md) — the code-side companion to this list
- [07-security · 15 Auditing & troubleshooting access](../07-security-and-sharing/15-auditing-and-troubleshooting-access.md) — the tooling for answering "why can this user see this"
