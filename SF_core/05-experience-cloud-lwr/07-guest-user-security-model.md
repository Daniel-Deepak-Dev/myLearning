# Guest User Security Model

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** What an unauthenticated visitor to a site *is*, and what the platform will and will not let them reach. The model only; the audit runbook is [11](11-public-site-exposure-audit.md). Flow access for guests is [04-flow · 21](../04-flow-and-automation/21-flow-for-external-and-guest-users.md).

> **What changed.** *"Configure the guest profile like any other profile"* has been wrong since 2020–21. Guest access was **hardened by default, permanently and org-wide**: *Secure guest user record access* is on in every org with an Experience Cloud site and **cannot be disabled**, **guest user sharing rules are the only way a guest sees a record and grant Read Only**, guests **cannot own records**, and **edit, delete, View All Records and Modify All Records cannot be granted to a guest even through a permission set**. Every pre-2021 guest recipe on the internet describes a configuration the platform now refuses.

## Core idea

A guest user is a real, licence-free user record with a profile, running every unauthenticated request to your site. That is the whole model, and both halves of it matter. Because it is a *user*, everything in [07-security](../07-security-and-sharing/INDEX.md) applies unchanged — object permissions, FLS, OWD, sharing. Because it is *one shared user* with no password and no session identity, Salesforce spent 2020–21 removing every mechanism that would let it accumulate access.

The result is a profile that is subtractive by design. You are not building up a guest's access; you are deciding what to leave switched on. And because guest page views are free, **the guest surface is the only part of your org a stranger can enumerate at their leisure**.

## How it works

| Control | State |
|---|---|
| *Secure guest user record access* | on in every org, **cannot be disabled** |
| Record access | **guest user sharing rules only**, **Read Only**, 50 per object |
| Record ownership | not possible — *Assign new records created by guest users to the default owner* |
| Object permissions grantable | **read and create only** |
| `View All Users` | removed from all guest users in Winter '21 |
| External OWD | governs guests; cannot exceed the internal OWD |

- **Guest user sharing rules are a criteria-based rule type of their own** and the sole grant mechanism. Not sharing sets, not manual shares, not the role hierarchy — a guest has no role.
- **The guest profile is per-site**, reached from the site's Administration workspace. Two sites, two guest users, two blast radii.
- **Guest visibility of other members** is a per-site setting — *Let guest users see other members of this site* — not the removed `View All Users` permission.
- **Flow access is granted one flow at a time** through *Enabled Flow Access*; the `Run Flows` permission no longer exists on the guest profile → [04-flow · 21](../04-flow-and-automation/21-flow-for-external-and-guest-users.md).
- **A guest's Apex still decides its own access.** A 67.0 class enforces the model; an older one, or one in system mode, does not → [06](06-custom-lwc-in-lwr-sites.md), [07-security · 14](../07-security-and-sharing/14-code-execution-context-and-security.md).

## 2026 currency

Nothing in the *mechanics* changed in Summer '26 — and that is the point worth carrying. **On 7 March 2026 Salesforce issued a security advisory** about an active campaign against over-permissive Experience Cloud guest configurations, with data claimed from hundreds of organisations. Salesforce's position is correct and is the reason this note exists in the shape it does: **the platform was not vulnerable, the configurations were.** The hardening above has been enforced for five years; what the campaign found was orgs whose guest profiles still carried object and field permissions from before it. The subject therefore stopped being a design note and became a standing audit item → [11](11-public-site-exposure-audit.md).

## Gotchas

- **The external OWD is a separate setting and defaults are not private everywhere.** Leaving it at the internal value is how guests end up over-privileged → [07-security · 06](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md).
- **`create` is grantable to guests, and it writes.** A public form is a write endpoint for anyone with the URL.
- **A guest sharing rule is still a sharing rule** — over-broad criteria grant the whole object, read-only, to the internet.
- **Permission sets do not rescue a guest.** The blocked permissions are blocked through every assignment path.
- **`API Enabled` on a guest profile turns the site into a queryable API surface.** Remove it.
- **Error messages leak.** An unhandled exception surfaced to a guest is an information-disclosure surface → [03-lwc · 18](../03-lwc-and-slds/18-error-handling-and-user-feedback.md).

## Recall

Q: What is the only way to grant an unauthenticated guest access to a record?
A: A guest user sharing rule — criteria-based, Read Only, 50 per object. Nothing else grants a guest record access.

Q: Can a guest user own a record?
A: No. Records created by guests are assigned to a default owner, and the setting enforcing this can't be turned off.

Q: Which object permissions can a guest user hold?
A: Read and create only. Edit, delete, View All Records and Modify All Records cannot be granted, even via a permission set.

Q: What replaced the `View All Users` permission for guests?
A: The per-site *Let guest users see other members of this site* setting; the permission was removed from all guests in Winter '21.

Q: Was the 2026 Experience Cloud campaign a platform vulnerability?
A: No — it exploited over-permissive guest configurations that predated the 2020–21 hardening.

## Related

- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — the runbook for proving a site is safe
- [09 · Sharing for external users](09-sharing-for-external-users.md) — the authenticated half of the external sharing model
- [07-security · 06 Org-wide defaults & record access](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md) — the external OWD this rests on
- [04-flow · 21 Flow for external & guest users](../04-flow-and-automation/21-flow-for-external-and-guest-users.md) — the flow half, including *Enabled Flow Access*
