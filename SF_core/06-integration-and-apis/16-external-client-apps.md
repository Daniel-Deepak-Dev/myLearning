# External Client Apps

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** The app object an external caller authenticates through, and what replaced the connected app. The flows themselves are [15](15-oauth-flows-and-authorization.md); what an authenticated caller may then reach is [24](24-api-limits-monitoring-and-access-control.md).

> **What changed.** *"Create a connected app"* is a broken runbook step. Connected-app **creation is restricted from Spring '26** — a new one requires a Salesforce Support case, which Salesforce says will eventually go away — after UI creation was disabled by default for new orgs in Winter '26. **External Client Apps are the model for new integrations.** Existing connected apps keep working and are **not retired**; this is a creation gate, not a switch-off.

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

## 2026 currency

The creation gate is the headline, but a second enforcement has been live since **early September 2025** and bites orgs that never created anything: the **Connected App Usage Restrictions Change**. Access to **uninstalled** connected apps — ones users authorized directly without an admin installing them — is blocked for **new** users; previously authorized users keep access; and **OAuth 2.0 device flow is blocked outright, even for prior users**. The bypass is a new **`Approve Uninstalled Connected Apps`** permission, and the inventory tool is Setup → **Connected Apps OAuth Usage**: review what is in use, install what you trust, block the rest. Salesforce's migration guidance for both retiring password flows names external client apps explicitly → [15](15-oauth-flows-and-authorization.md).

## Gotchas

- **"Superseded" is not "retired."** Existing connected apps run indefinitely; saying otherwise in a scoping call is wrong. What changed is that you cannot make a new one.
- **The 30-minute delay is not documented in the error.** A brand-new ECA returns an authentication failure that reads exactly like a wrong client ID or a wrong callback URL.
- **Policy no longer travels with the app.** An admin who tightened a packaged connected app and expects the same edit to survive on an ECA is editing a different record — that separation is the point, and it surprises people.
- **`All users may self-authorize` is how uninstalled apps happened.** It is now the setting that puts an app on the wrong side of the September 2025 restriction.
- **Device flow is gone for uninstalled apps** — a CLI or headless tool relying on it fails for everyone until an admin installs the app.
- **Blocking an app revokes its tokens.** That is the intent, and it takes down every integration using it at once, so inventory before blocking.

## Recall

Q: Can you still create a connected app?
A: Not normally — creation is restricted from Spring '26 and needs a Salesforce Support case. Existing connected apps continue to work.

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
