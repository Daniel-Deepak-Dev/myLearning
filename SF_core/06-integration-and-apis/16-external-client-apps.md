---
vault: SF_core
area: 06-integration-and-apis
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 13
tags: [currency-new, currency-warning]
---
# External Client Apps

**Scope:** The app object an external caller authenticates through, and what replaced the connected app. The flows themselves are [15](15-oauth-flows-and-authorization.md); what an authenticated caller may then reach is [24](24-api-limits-monitoring-and-access-control.md).

> **What changed.** *"Create a connected app"* is a broken runbook step. Connected-app **creation is restricted from Spring '26** — a new one requires a Salesforce Support case, which Salesforce says will eventually go away — after UI creation was disabled by default for new orgs in Winter '26. **External Client Apps are the model for new integrations.** Existing connected apps keep working and are **not retired** — but **support for them ends in Summer '27**: they keep running, and Salesforce stops fixing them.

## Core idea

A connected app was one object doing three jobs at once: describing an app, holding its OAuth configuration, and carrying org-specific policy. That made it impossible to package cleanly — the thing you shipped and the thing an admin tuned were the same record, so a subscriber's changes were overwritten on upgrade.

An **external client app** splits them. The app's identity and OAuth settings live in one metadata type; the org's policy — who may use it, IP ranges, token lifetimes, session requirements — lives in **separate settings** records. A packaged app can now ship its definition and leave the subscriber's policy alone, and an admin can tighten policy without editing the app.

## How it works

- **Setup → External Client App Manager → New External Client App.** Fill in basic information, then expand **API (Enable OAuth Settings)** and check *Enable OAuth*.
- **Distribution state is a first-class choice** — *local* to this org, or *packaged* for distribution — and it is decided at creation.
- **Policy lives outside the app definition**: permitted users (*Admin approved users are pre-authorized* vs *All users may self-authorize*), IP relaxation, refresh-token lifetime, session policies.
- **It is the required setup object for hosted MCP servers.** The documented path creates an ECA with the `mcp_api` and `refresh_token` scopes → [25](25-mcp-servers-and-agent-facing-apis.md).
- **A new ECA takes up to 30 minutes to become usable.** Salesforce compares it to DNS propagation; the failure before then looks like a bad client ID.
- **Connected apps remain manageable.** You can view, edit, install, block and revoke existing ones — you just cannot create new ones without Support.
- **A local connected app migrates in place.** App Manager → the app → **Migrate to External Client App**, shown only when the app is eligible. The original stays as a read-only record and users do not re-authenticate. An app using the **username-password flow cannot migrate**, because ECAs do not support that flow. A packaged app waits for its vendor's ECA version.

## 2026 currency

The creation gate is the headline, but a second enforcement has been live since **early September 2025** and bites orgs that never created anything: the **Connected App Usage Restrictions Change**. Access to **uninstalled** connected apps — ones users authorized directly without an admin installing them — is blocked for **new** users; previously authorized users keep access; and **OAuth 2.0 device flow is blocked outright, even for prior users**. The bypass is a new **`Approve Uninstalled Connected Apps`** permission, and the inventory tool is Setup → **Connected Apps OAuth Usage**: review what is in use, install what you trust, block the rest. Salesforce's migration guidance for both retiring password flows names external client apps explicitly → [15](15-oauth-flows-and-authorization.md).

Winter '27 put the rest of the connected-app story on dates. The *Migrate All Connected Apps to External Client Apps* Release Update is **available from Winter '27 and enforced in production in Summer '27**, when support ends in all environments. Before that, **device flow is restricted to local ECAs with a `localhost` callback from 30 November 2026**, and a **30-day idle limit on refresh tokens** applies to connected apps and ECAs alike from 4 November 2026 in production. None of the three was enforced by the Winter '27 upgrade itself.

## Gotchas

- **"Superseded" is not "retired", and "unsupported" is not "switched off".** After Summer '27 an existing connected app still runs, with no bug fixes and no support. Saying it stops working is wrong; saying nothing changes is also wrong.
- **The 30-minute delay is not documented in the error.** A brand-new ECA returns an authentication failure that reads exactly like a wrong client ID or a wrong callback URL.
- **Policy no longer travels with the app.** An admin who tightened a packaged connected app and expects the same edit to survive on an ECA is editing a different record — that separation is the point, and it surprises people.
- **`All users may self-authorize` is how uninstalled apps happened.** It is now the setting that puts an app on the wrong side of the September 2025 restriction.
- **Device flow is gone for uninstalled apps** — a CLI or headless tool relying on it fails for everyone until an admin installs the app.
- **Blocking an app revokes its tokens.** That is the intent, and it takes down every integration using it at once, so inventory before blocking.

## Recall

Q: Can you still create a connected app?
A: Not normally — creation is restricted from Spring '26 and needs a Salesforce Support case. Existing connected apps continue to work, unsupported from Summer '27.

Q: What did external client apps split apart?
A: The app definition and OAuth settings from the org's policy settings, so a packaged app can ship without overwriting a subscriber's configuration.

Q: What broke in early September 2025?
A: Uninstalled connected apps were blocked for new users, and **OAuth device flow was blocked entirely** — the bypass is the `Approve Uninstalled Connected Apps` permission.

Q: Why does a brand-new external client app fail to authenticate?
A: It can take up to 30 minutes to propagate. The error looks like a bad client ID.

Q: Which Setup page inventories what is actually in use?
A: Connected Apps OAuth Usage.

## Related

- [15 · OAuth flows & authorization](15-oauth-flows-and-authorization.md) — the flows configured on this object
- [25 · MCP servers & agent-facing APIs](25-mcp-servers-and-agent-facing-apis.md) — the ECA is a prerequisite, not an option
- [24 · API limits, monitoring & access control](24-api-limits-monitoring-and-access-control.md) — API Access Control, which allowlists apps org-wide
- [07-security · 17 Authentication & MFA](../07-security-and-sharing/17-authentication-and-mfa.md) — the human half of the same tightening

## Sources

- [Connected App & External Client App Security Requirement Updates (005461287)](https://help.salesforce.com/s/articleView?id=005461287&language=en_US&type=1) — Salesforce Help · via search 2026-10-28 · connected-app end of support Summer '27 (all environments); device flow restricted to local ECAs 30 Nov 2026; refresh-token idle TTL 30 days from 4 Nov 2026 (production)
- [Release Updates (Winter '27)](https://help.salesforce.com/s/articleView?id=release-notes.rn_ru.htm&release=264&type=5&language=en_US) — Winter '27 release notes · via search 2026-10-28 · *Migrate All Connected Apps to External Client Apps* available Winter '27, enforced for production in Summer '27
- [Migrate a Local Connected App to an External Client App](https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.migrate_connected_app_to_external_client_app.htm&type=5) — Salesforce Help · via search 2026-10-28 · migration button, read-only original, no re-authentication; username-password apps cannot migrate; packaged apps depend on the ISV
- [Winter '27 Release Architect Highlights](https://www.salesforce.com/blog/winter-27-release-architect-highlights/) — Salesforce Architecture Blog, 5 Oct 2026 · read 2026-10-28 · *"Support ends by Summer '27, so start migrating to external client apps soon"*

## History

- 2026-10-28 · Winter '27 currency check: connected-app support ends Summer '27; added the migration Release Update and button, the 30 Nov 2026 device-flow restriction and the refresh-token idle limit
