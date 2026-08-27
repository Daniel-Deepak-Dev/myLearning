# Hyperforce & Instance Operations

> Area: 09-devops-sfdx-and-release-management · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 17

**Scope:** The org as a thing that runs somewhere — instances, maintenance windows, and the migration work that lands on release operations. The residency and data-locality view is [08-data · 23](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md); same platform shift, other side.

## Core idea

Every org sits on a named **instance**, and that instance — not your calendar and not your contract — determines when the org upgrades, when it is maintained, and which hostnames resolve to it. Most teams never think about this until something moves it. Then three things break at once: an allowlist, a hard-coded URL, and a scheduled job that assumed a maintenance window.

Hyperforce is the largest example of that move, and as of Summer '26 it is **behind us as a decision**. Salesforce Help is explicit that from **1 July 2026 it is no longer possible to delay upgrades to Hyperforce** — you get **30 days' notice** and a **15-day reminder**. The operational question is not whether the org moves but whether anyone inventoried its integrations first.

## How it works

- **Salesforce Trust status (`status.salesforce.com`) is the operational source of truth.** Search by My Domain or instance; the **Maintenance** tab carries major-release windows, instance refreshes and planned maintenance.
- **Instance refreshes are routine and separate from Hyperforce.** Salesforce moves orgs between instances for capacity; the instance name changes and the same breakage list applies at smaller scale.
- **Maintain an endpoint inventory** — every inbound caller, every outbound target, every allowlist entry on both sides. This is the deliverable that makes a migration a Tuesday rather than an incident.
- **Egress addresses change with the infrastructure**, so a customer-side firewall allowlist is the failure nobody in your org can see or test.
- **Hard-coded instanced hostnames are the classic breakage** — in integrations, Visualforce, email templates and bookmarks. Use the My Domain URL, and note that API traffic on instanced URLs has its own deadline → [06-integration · 03](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md).
- **The free Hostname Redirects event type is the inventory tool** for finding callers still using the old form → [07-security · 23](../07-security-and-sharing/23-event-monitoring-and-transaction-security.md).
- **Some limits are better on Hyperforce** — Salesforce Connect's hourly ceilings on new external object rows and OData callouts are removed there — so confirm where the org runs before designing on that.

## 2026 currency

The dates have all landed, which changes how you talk about this. Hyperforce delays ended **1 July 2026**; **legacy My Domain hostname redirections ended in Spring '26**, so an old URL now **404s rather than redirecting** → [07-security · 20](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md). Those two together mean the migration's most common symptom — a caller on an old hostname — no longer degrades gracefully. There is also a quiet one worth knowing in ops: **file previews are generated as JPG rather than SVG on Hyperforce**, regardless of the account preference, which breaks custom UI that read vector previews and leaves pre-migration previews intact so the failure looks intermittent.

## Gotchas

- **A sandbox and its production org can be on different sides of the migration** for a period, so a passing test proves less than usual.
- **Maintenance windows shift with the region.** Nightly batch jobs, integration schedules and monitoring silences were all set against the old one.
- **"Managed migration" means users notice nothing**, which is exactly why nobody prepares. The integrations notice.
- **Instance names appear in places nobody greps** — Visualforce pages, email templates, an old MuleSoft config, a partner's documentation.
- **Residency is not sovereignty.** Region choice answers where data sits at rest, not who can access it or where a request is served from → [08-data · 23](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md).
- **Trust status is per instance, not per org.** After a move you are watching the wrong page until someone updates the bookmark.
- **The 30-day notice is the whole window.** Treat the inventory as standing work, not as something to start when the email arrives.

## Recall

Q: Can an org still defer its Hyperforce migration?
A: No — delays ended **1 July 2026**; notice is 30 days with a 15-day reminder.

Q: Where do you find a specific org's maintenance and release windows?
A: Salesforce Trust status, searching by My Domain or instance, on the Maintenance tab.

Q: What is the single most useful artefact to hold before any instance move?
A: A complete endpoint and allowlist inventory — inbound, outbound, and both sides' firewalls.

Q: Why does an old instanced hostname fail hard now rather than redirecting?
A: Legacy My Domain redirections ended in Spring '26; the old URL 404s.

Q: Which non-obvious behaviour changes on Hyperforce?
A: File previews are generated as JPG rather than SVG, regardless of the account preference.

## Related

- [08-data · 23 Hyperforce, residency & data locality](../08-data-modeling-and-large-data-volumes/23-hyperforce-residency-and-data-locality.md) — the data-side half of this topic
- [20 · Release management & org upgrades](20-release-management-and-org-upgrades.md) — the calendar an instance move rewrites
- [06-integration · 03 API endpoints, hostnames & Edge Network](../06-integration-and-apis/03-api-endpoints-hostnames-and-edge-network.md) — the instanced-URL deadline
- [07-security · 20 My Domain, enhanced domains & trusted URLs](../07-security-and-sharing/20-my-domain-enhanced-domains-and-trusted-urls.md) — why the old hostname 404s
