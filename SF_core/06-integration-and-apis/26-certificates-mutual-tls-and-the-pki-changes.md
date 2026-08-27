# Certificates, mutual TLS & the PKI changes

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** The certificate layer under every integration — where certificates come from, what mutual TLS actually requires, and the industry changes now breaking both. Credentials that are secrets rather than keys are [17](17-named-credentials-and-external-credentials.md); SAML signing certificates are [07-security · 19](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md).

> **What changed.** Two long-standing certificate practices stopped being viable and both break integrations rather than logins. **A single public-CA root can no longer issue both website SSL and client-authentication certificates** — dual-use certificates are gone, and mTLS built on them fails. And **maximum certificate validity is collapsing: 200 days from 15 March 2026, 100 days from 15 March 2027, 47 days from 15 March 2029.** Annual manual renewal is no longer a strategy. Salesforce also states plainly that **certificate pinning must stop**.

## Core idea

Every integration already depends on certificates; most teams only discover it when one expires. There are three distinct roles and conflating them is the source of most of the pain: a **server certificate** proves an endpoint's identity during TLS, a **client certificate** proves the *caller's* identity in mutual TLS, and a **signing certificate** signs an assertion — a SAML response, or a JWT for the OAuth bearer flow.

Salesforce lets an org hold certificates for the second and third roles under **Setup → Certificate and Key Management**, either self-signed (fine for JWT bearer, where the other side just needs the public key) or CA-signed (required whenever a third party must validate the chain).

## How it works

- **Self-signed vs CA-signed** is decided by who validates it. JWT bearer to your own org: self-signed is enough. Mutual TLS with a partner: CA-signed, from a CA they trust.
- **Mutual TLS is two-way proof.** The client presents a certificate as well as the server, so the endpoint authenticates the caller with no shared secret at all. Salesforce supports it on inbound API traffic and on outbound callouts via a named credential's certificate.
- **A JWT bearer flow's certificate is uploaded to the app**, and its expiry silently ends the integration → [15](15-oauth-flows-and-authorization.md), [16](16-external-client-apps.md).
- **Trust stores work in both directions.** Salesforce must trust the endpoint you call; the endpoint must trust Salesforce. Salesforce's guidance is to keep trust stores updated with the **Mozilla Pinset** rather than pinning individual certificates.
- **Rotation, not renewal, is the design goal.** With validity heading to 47 days, anything requiring a human to remember will fail.

## 2026 currency

The three dates above are the whole story and they are already in effect: **200-day maximum validity from 15 March 2026**, dropping to **100 days from 15 March 2027** and **47 days from 15 March 2029**. Two consequences worth stating separately. First, **any mTLS integration using a dual-use certificate from a public CA will experience outages** — organisations must obtain client-authentication-only certificates, issued from a root distinct from their website SSL root. Second, **certificate pinning is now an anti-pattern by Salesforce's own guidance**: pinned clients break every time a certificate rotates, and rotation is about to become routine. Audit both before the next renewal cycle rather than after an outage. The same tightening wave produced the MFA and instanced-hostname deadlines → [../CURRENCY.md](../CURRENCY.md).

## Gotchas

- **A dual-use certificate that works today will not be reissued.** The failure arrives at renewal, not at expiry, and looks like a CA problem.
- **Certificate pinning fails on a schedule you no longer control.** Shorter validity means more rotations, each one an outage for a pinned client.
- **Expiry is silent until it is total.** Neither a JWT bearer flow nor an mTLS endpoint warns you; the integration simply starts returning authentication errors.
- **Sandbox refresh does not carry certificate trust.** Configuration copies, the trust relationship does not — the same trap as named credentials → [17](17-named-credentials-and-external-credentials.md).
- **Self-signed is not "insecure", it is "unvalidatable by a third party".** Using it where a partner must verify a chain is the actual mistake.
- **47 days is roughly eight rotations a year.** Any process with a ticket and an approval in it is already too slow — automate now, while the window is 200 days.

## Recall

Q: What are the three certificate roles, and how do they differ?
A: Server certificates prove an endpoint's identity, client certificates prove the caller's identity in mutual TLS, and signing certificates sign assertions such as SAML responses or JWTs.

Q: What is happening to maximum certificate validity?
A: 200 days from 15 March 2026, 100 days from 15 March 2027, 47 days from 15 March 2029.

Q: Why do dual-use certificates break mutual TLS?
A: A single public-CA root can no longer issue both website SSL and client-ID certificates, so client authentication needs a separate client-auth-only certificate.

Q: What is Salesforce's guidance on certificate pinning?
A: Stop. Keep trust stores updated with the Mozilla Pinset instead — pinning breaks on every rotation.

Q: When is a self-signed certificate sufficient?
A: When only your own org validates it — a JWT bearer flow, for example. A third party validating a chain needs CA-signed.

## Related

- [17 · Named Credentials & External Credentials](17-named-credentials-and-external-credentials.md) — where an outbound certificate is configured
- [15 · OAuth flows & authorization](15-oauth-flows-and-authorization.md) — JWT bearer, the flow that depends on a key pair
- [03 · API endpoints, hostnames & Edge Network](03-api-endpoints-hostnames-and-edge-network.md) — the other dated integration deadline
- [07-security · 19 SSO, SAML, OIDC & identity](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md) — the same expiry problem, on the login path
