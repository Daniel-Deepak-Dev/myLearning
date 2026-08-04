# Licences & External User Types

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** The external half of the licence model — which licence an external person holds, what it gates, and how it is billed. **Internal licences are [07-security · 02](../07-security-and-sharing/02-licences-and-what-they-gate.md)**; the two notes deliberately meet at this boundary and do not overlap.

## Core idea

On an Experience Cloud project the licence is not a procurement detail that follows the design — **it is the design constraint that shapes everything else**. It decides whether your users have roles, and therefore whether the role hierarchy, sharing rules and manual sharing exist for them at all. It decides whether they can see reports. It decides whether "just add Opportunities to the portal" is a configuration change or a licence renegotiation.

The single most consequential split is **high-volume versus role-based**. Customer Community users are high-volume: no roles, no hierarchy, and sharing sets instead of sharing rules → [09](09-sharing-for-external-users.md). Customer Community Plus and Partner Community users have roles and behave much more like internal users. Almost every external-sharing surprise traces back to which side of that line the licence sits on.

## How it works

| Licence | Roles? | Typically for |
|---|---|---|
| **Customer Community** | no — high-volume | large B2C self-service, lowest cost per user |
| **Customer Community Plus** | yes | customers needing reports, tasks/events, advanced sharing |
| **Partner Community** | yes | B2B partners — Leads, Opportunities, Campaigns, channel sales |
| **External Apps** | yes | custom portals over custom + external data; dealer/vendor/supplier |
| **External Identity** | — | authentication and profile only; identity, not CRM access |
| **Channel Account** | — | partner access billed per account rather than per user |

- **Member-based vs login-based is a billing metric, not a feature difference.** Member-based is a provisioned seat; login-based draws from a monthly pool of logins. Sporadic users are the case for login-based; daily users are not.
- **Guests consume no licence at all**, which is exactly why the guest surface needs its own controls → [07](07-guest-user-security-model.md).
- **A permission set cannot exceed the licence.** The licence is the outer gate — the same rule as internal users, stated in [07-security · 02](../07-security-and-sharing/02-licences-and-what-they-gate.md).
- **Super user access is the escalation valve.** Partner and Customer Plus users can be granted it to see records created by others in their account at or below their role — Cases, Leads, Opportunities and custom objects.
- **Creating the first external user on a partner account creates three roles** by default, which is how partner-heavy orgs approach the role limit from an unplanned direction → [07-security · 08](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md).

## Gotchas

- **High-volume users have no role, so sharing rules and manual sharing do not apply to them.** This is the whole reason sharing sets exist → [09](09-sharing-for-external-users.md).
- **Upgrading Customer Community → Customer Community Plus is a re-provision, not a toggle**, and it changes the sharing model underneath live users.
- **Login-based licences bill on logins, not sessions.** A user who logs in daily is more expensive than the member seat you avoided.
- **External Identity is not a portal licence.** It authenticates; it does not grant CRM object access.
- **Person Accounts carry their own Experience Cloud restrictions**, and the modelling decision is one-way → [08-data · 05](../08-data-modeling-and-large-data-volumes/05-person-accounts-and-one-way-modeling-decisions.md).
- **Role counts grow three at a time on partner accounts**, silently, until the org limit is the blocker.

## Recall

Q: Which distinction between external licences matters most architecturally?
A: High-volume versus role-based. High-volume users have no role, so the role hierarchy, sharing rules and manual sharing don't apply to them.

Q: Which licences give an external user a role?
A: Customer Community Plus, Partner Community and External Apps. Customer Community is high-volume and role-less.

Q: What does a guest user consume from the licence pool?
A: Nothing — unauthenticated visitors use no external licence, which is why guest access is controlled separately.

Q: What is the difference between member-based and login-based licensing?
A: A billing metric only. Member-based is a provisioned seat; login-based draws from a monthly login pool. Sporadic use favours login-based.

Q: What does super user access grant, and to whom?
A: To Partner and Customer Community Plus users — visibility of records created by others in their account at or below their role, for Cases, Leads, Opportunities and custom objects.

## Related

- [09 · Sharing for external users](09-sharing-for-external-users.md) — the mechanisms each licence type actually uses
- [07-security · 02 Licences & what they gate](../07-security-and-sharing/02-licences-and-what-they-gate.md) — the internal half; the boundary is stated in both
- [07-security · 08 Groups, queues & the grantee model](../07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — portal roles inside "Roles and Subordinates"
- [08-data · 05 Person Accounts & one-way modeling decisions](../08-data-modeling-and-large-data-volumes/05-person-accounts-and-one-way-modeling-decisions.md) — the B2C data model this licence choice meets
