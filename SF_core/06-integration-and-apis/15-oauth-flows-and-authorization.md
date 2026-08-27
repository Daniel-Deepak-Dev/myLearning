# OAuth flows & authorization

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** How an external caller gets an access token, which flow to pick, and what the token is allowed to do. The *app object* the flow runs through is [16](16-external-client-apps.md); outbound auth from Apex is [17](17-named-credentials-and-external-credentials.md); human login and MFA are [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md).

> **What changed.** Every tutorial that posts a username and password to `/services/oauth2/token` is teaching a flow on a retirement clock. Take the three dates separately, because conflating them misreads an inherited org: an org-wide **block switch** arrived in Winter '22, the flow became **blocked by default in newly created orgs** in Summer '23 — an org created in 2019 may still be running it — and the **Summer '26 Release Update retires it for connected apps in Winter '27**. **JWT bearer** and **client credentials** are the server-to-server answers.

## Core idea

OAuth exists so a caller never holds a Salesforce password. It holds a **token**: scoped, expiring, revocable, and attributable to a specific app. The flow you choose is a question about *who is present* — a human at a browser, a background job with a private key, or a daemon with a client secret — and picking the wrong one is the commonest reason an integration is either insecure or unworkable.

The second decision is **as whom**. A token names a user, and everything the token can do is what that user could do. There is no "API-level" bypass: object permissions, FLS and sharing apply, which is why the running identity behind an integration is an architectural choice rather than an operational detail.

## How it works

| Flow | Who is present | Credential | Use it for |
|---|---|---|---|
| **Web server + PKCE** | a human, at a browser | client ID + secret + code verifier | user-facing apps, MCP clients |
| **JWT bearer** | nobody | a **private key** + certificate | server-to-server, no stored secret |
| **Client credentials** | nobody | client ID + secret | server-to-server, needs a **Run As** user |
| **Refresh token** | nobody, after a first login | refresh token | keeping a user session alive |
| **Device** | a human, on a screen with no keyboard | device code | CLI and TV-style clients — **blocked for uninstalled apps** since Sept 2025 → [16](16-external-client-apps.md) |
| ~~Username-password~~ | — | username + password | **nothing. Retiring Winter '27** |

- **JWT bearer is the default for unattended work.** You sign an assertion with a private key whose certificate is uploaded to the app; no secret is transmitted and nothing needs rotating on a password policy. The user it runs as must be **pre-authorized** for the app.
- **Client credentials needs a Run As user**, chosen on the app itself. That user is the entire security boundary — it is why the free **Salesforce Integration** licence exists: an API-only identity with no UI login, paired with the *Salesforce API Integration* permission set licence.
- **Scopes narrow what the token reaches.** `api` grants the whole Platform API surface — REST, Tooling, Metadata. `mcp_api` (new) grants **only** hosted MCP servers, which is why it exists → [25](25-mcp-servers-and-agent-facing-apis.md). `refresh_token` is separate and must be requested.
- **`Any API Auth`** is a Summer '26 user permission gating who may authenticate via SOAP `login()`, enforced by default in new orgs → [05](05-soap-api-and-where-it-persists.md).
- **Tokens are revocable and auditable.** Setup → *Connected Apps OAuth Usage* lists every app a user has authorized; refresh tokens default to a **one-year** lifetime and should be shortened.

## 2026 currency

Two password-only mechanisms are ending on separate clocks: the **OAuth username-password flow in Winter '27** (a Summer '26 Release Update, scoped to connected apps, with a test run available now) and **SOAP `login()` for API 31.0–64.0 in Summer '27**. Both mint a session from a password alone, which is what MFA enforcement made untenable → [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md). The migration Salesforce names for both is the same: **an external client app with JWT** → [16](16-external-client-apps.md). Dated detail: [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **"Blocked by default" is true only for orgs created Summer '23 or later.** Auditing an older org by reading the release notes tells you nothing — check the setting.
- **A client credentials token is only as safe as its Run As user.** Pointing it at a System Administrator hands the whole org to anyone holding the client secret.
- **JWT bearer fails with an opaque `invalid_grant`** when the user is not pre-authorized, when the certificate expired, or when the clock skews — the error distinguishes none of them.
- **Scope `api` is almost always wider than needed.** It carries Metadata and Tooling with it, so an integration that only reads Accounts can deploy code.
- **A refresh token outlives the employee.** Deactivating a user does not retroactively revoke tokens issued to apps they authorized — revoke them explicitly.
- **IP restrictions on the app are enforced at token *use*, not only at issue**, so a working integration breaks when the caller's egress IP changes.

## Recall

Q: Which OAuth flows are the server-to-server answers, and what does each need?
A: JWT bearer (a private key plus an uploaded certificate, user must be pre-authorized) and client credentials (client ID/secret plus a **Run As** user configured on the app).

Q: Is the username-password flow blocked everywhere?
A: No. Blocked by default only in orgs created **Summer '23 or later**; an org-wide switch exists since Winter '22; retirement for connected apps is **Winter '27**.

Q: What does the `mcp_api` scope do that `api` does not?
A: It grants access to hosted MCP servers *only*, instead of the whole Platform API surface.

Q: What is the security boundary of a client credentials integration?
A: The Run As user. The token can do exactly what that user can do — which is the argument for a Salesforce Integration licence rather than an admin.

Q: What are the two password-only mechanisms retiring, and when?
A: The OAuth username-password flow in **Winter '27**, and SOAP `login()` for API 31.0–64.0 in **Summer '27**.

## Related

- [16 · External Client Apps](16-external-client-apps.md) — the object every one of these flows is configured on
- [17 · Named Credentials & External Credentials](17-named-credentials-and-external-credentials.md) — the same problem in the outbound direction
- [24 · API limits, monitoring & access control](24-api-limits-monitoring-and-access-control.md) — restricting which apps may call at all
- [07-security · 19 SSO, SAML, OIDC & identity](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md) — authentication as federation rather than authorization
