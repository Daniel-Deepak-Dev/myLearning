# Hyperforce, Residency & Data Locality

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 15

**Scope:** Where the org's data physically runs, what the migration changes underneath you, and what residency does and does not promise. The ops-side view is [09-devops · 23](../09-devops-sfdx-and-release-management/INDEX.md).

> **What changed.** Hyperforce is no longer something to plan for. Salesforce Help is explicit: **"Starting July 1, 2026, it is no longer possible to delay upgrades to Hyperforce."** Any guidance that treats the move as optional, or as a project you schedule when convenient, is out of date — you get **30 days' notice** and a **15-day reminder**, and that is the whole window.

## Core idea

Hyperforce is Salesforce re-platformed onto public cloud infrastructure — AWS — instead of first-party data centres. For a data architect it changes two things and leaves most of the platform alone.

The first is **choice of region**, which turns "where does our data live" from an answer you accept into one you specify. The second is **everything that was quietly coupled to the old instance**: hostnames, allowlisted IPs, maintenance windows, and a short list of behaviours that differ. The migration is managed and largely invisible to users; it is the integrations that notice.

## How it works

- **Regions are the residency control.** Data at rest stays in the chosen region, with multiple availability zones behind it for durability.
- **The EU Operating Zone goes further than region choice** — technical policies and operational processes that constrain what data moves out of the EU, which is the distinction a regulator actually asks about.
- **Migration is managed, not a toggle.** Salesforce schedules it, notifies the org 30 days ahead with the org Id, date and new instance name, and reminds at 15 days.
- **The instance name changes**, which is why instanced hostnames stop working — and API traffic on an instanced URL stops being supported shortly after Winter '27 anyway → [06-integration · 03](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md).
- **Some limits are better on Hyperforce.** Salesforce Connect's per-hour ceilings on new external object rows and OData callouts are removed there → [17](17-external-objects-vs-replicated-copies.md).
- **File previews are generated as JPG, not SVG**, regardless of the account preference. Previews created before migration survive; new uploads do not, and custom code that reads SVG previews breaks.

## 2026 currency

The deadline above is the headline and it is already behind us — as of Summer '26 the question is not *whether* an org moves but whether anyone audited its integrations before it did. Pair this with two facts recorded elsewhere in the vault that share the same root cause: **legacy My Domain hostname redirections ended in Spring '26**, so an old URL 404s rather than redirecting → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md), and the free **Hostname Redirects** event type is the inventory tool for finding callers still using instanced URLs → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).

## Gotchas

- **Residency is not sovereignty.** Data at rest in a region says nothing about support access, subprocessors or where a request is served from. Answer the question that was asked.
- **Hard-coded instance URLs are the classic breakage** — in integrations, bookmarks, Visualforce, and email templates nobody has opened in years.
- **IP allowlists on the customer side need reviewing**, because the egress addresses change with the infrastructure.
- **The SVG-to-JPG preview change is silent** and only shows up in custom UI that assumed vector previews.
- **Maintenance windows can shift** with the new region's schedule, which breaks assumptions baked into nightly jobs.
- **A sandbox and its production org can be on different sides of the migration** for a period — so a test that passes proves less than usual.
- **"Limits removed on Hyperforce" is conditional.** Confirm where the org actually runs before designing on it.

## Recall

Q: Can an org still delay its Hyperforce migration?
A: No — since **1 July 2026** delays are no longer possible. You get 30 days' notice and a 15-day reminder.

Q: What does the EU Operating Zone add beyond choosing an EU region?
A: Technical policies and operational processes that constrain data movement out of the EU, rather than only where data sits at rest.

Q: Which file-handling behaviour changes on Hyperforce?
A: Previews are generated as JPG rather than SVG regardless of preference; pre-migration SVGs remain but new uploads do not produce them.

Q: Why do integrations break on migration when users notice nothing?
A: The instance name changes, so hard-coded instanced hostnames and IP allowlists tied to the old infrastructure stop working.

Q: Does choosing a region satisfy a data sovereignty requirement?
A: Not by itself. Residency covers data at rest; sovereignty questions also cover access, subprocessors and operational control.

## Related

- [17 · External objects vs replicated copies](17-external-objects-vs-replicated-copies.md) — the Salesforce Connect ceilings that only Hyperforce removes
- [06-integration · 03 API endpoints, hostnames & Edge Network](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md) — the instanced-URL deadline this shares a root cause with
- [07-security · 20 My Domain, enhanced domains & trusted URLs](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md) — why the old hostname 404s
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — the same platform shift seen from release operations
