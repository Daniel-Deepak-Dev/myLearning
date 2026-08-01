# Salesforce Foundations & org strategy

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** What the Foundations add-on actually puts in an org, and how that lands on the single-org vs multi-org decision. Editions and limits are [01 · Org anatomy](01-org-anatomy-and-editions.md); Data 360 depth lives in [AI_Data/01-data-cloud](../../AI_Data/01-data-cloud/INDEX.md).

## Core idea

**Salesforce Foundations is a $0 add-on** that switches on a slice of Sales, Service, Marketing, Commerce and **Data 360** inside an org that already has one of the qualifying editions. Free is the headline and the trap: adding it **automatically provisions Data 360** and starts an Agentforce credit meter, so a commercially free change is an architectural one. For an architect the interesting part is what it does to org strategy — Foundations pushes cross-cloud capability *into the existing org*, which strengthens the already-strong default of consolidating on one org rather than spinning up a second.

## How it works

- **Editions:** included at no extra cost with **Enterprise, Unlimited, Einstein 1 Sales** and **Einstein 1 Service**.
- **Adding it:** Setup → *Salesforce Foundations* → **Add via Your Account** → select the Foundations entitlements → complete checkout. It is an entitlement purchase at $0, not a checkbox.
- **What arrives**, roughly by pillar:

| Pillar | Included capability |
|---|---|
| Sales | lead and case management, quoting, macros, email campaigns |
| Service | omni-channel case routing, Service Console, macros, Knowledge |
| Marketing | segments over CRM + Data 360 data, Flow-driven outreach, **up to 2,000 email sends/month** |
| Commerce | D2C storefront, cart and checkout, Pay Now links |
| Data & AI | **Data 360 auto-provisioned**, Agentforce built in, **200,000 Flex credits** to start |

- **Consumption is where cost re-enters.** Data 360 and Agentforce usage draws on the included credits and then bills as overage. The 200K credits are for proving use cases, not for running production agents.
- **Admin work remains.** Provisioning is automatic for Data 360; the other feature sets need deliberate setup before anyone can use them.
- **Org strategy in one line:** consolidate unless something forces separation. A single org gives one data model, native cross-cloud reporting, one sharing model and one release calendar. Separate orgs buy isolation and independent governance — and pay for it in duplicated metadata, cross-org integration, duplicated licences and no native cross-org reporting.
- **Legitimate reasons for a second org:** acquisition with an incompatible model, data-residency or regulatory separation, genuinely disjoint business processes, or a release cadence one business unit cannot accept.

## 2026 currency

Foundations is current product, not a promotion to wait out, and Agentforce is part of it — which means the AI conversation now starts inside standard Enterprise-edition orgs rather than as a separate purchase. Anything written before Foundations describes AI and Data 360 as add-on projects; that framing is stale. Credit mechanics and pricing move fastest here — check [AI_Data/05-release-radar/pricing-and-certification.md](../../AI_Data/05-release-radar/pricing-and-certification.md) rather than trusting a number in a note.

## Gotchas

- **"Free" provisions Data 360.** Adding Foundations changes the org's data architecture and its consumption profile; treat it as a change with a rollback conversation, not a trial.
- The **200K Flex credits are a starter allowance.** Building an agent on them and then going to production without a credit forecast is how orgs discover overage billing.
- The email send allowance (**~2,000/month**) is a Foundations-level entitlement, not Marketing Cloud — do not size a campaign programme on it.
- Foundations capability is a *slice* of each cloud. It is not "Service Cloud for free"; the licence boundary still exists and is easy to promise past in a sales conversation.
- Multi-org is often chosen for **permission** isolation that permission set groups and restriction rules would have solved in one org. → [07-security](../07-security-and-sharing/INDEX.md)
- Cross-org reporting does not exist natively. Anyone planning a second org is also planning an integration and a reporting layer.
- Edition matters: Professional Edition does not qualify, so "just add Foundations" is not an answer for every org.

## Recall

Q: What does Salesforce Foundations cost, and which editions include it?
A: $0 as a built-in add-on, in Enterprise, Unlimited, Einstein 1 Sales and Einstein 1 Service.

Q: What happens to Data 360 when Foundations is added?
A: It is provisioned automatically; the other Foundations feature sets still need explicit setup by an admin.

Q: How many Agentforce Flex credits does Foundations include, and what are they for?
A: 200,000 — enough to test use cases and build proofs of concept, after which usage bills as overage.

Q: Give three defensible reasons to run a second production org.
A: Incompatible data model from an acquisition, regulatory or data-residency separation, and a release cadence a business unit cannot share.

Q: What does a single org give you that two orgs cannot?
A: One data model and sharing model, native cross-cloud reporting, and one release calendar to manage.

## Related

- [01 · Org anatomy & editions](01-org-anatomy-and-editions.md) — the edition and limit context Foundations sits inside
- [19 · Agentforce in Setup & AI-assisted admin](19-agentforce-in-setup-and-ai-assisted-admin.md) — the AI that arrives with it, from the admin's seat
- [AI_Data/01-data-cloud · INDEX](../../AI_Data/01-data-cloud/INDEX.md) — what Data 360 actually does once provisioned
