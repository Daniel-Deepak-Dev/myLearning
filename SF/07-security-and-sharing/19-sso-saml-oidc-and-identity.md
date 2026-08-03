# SSO, SAML, OIDC & Identity

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Delegating the authentication decision of [17](17-authentication-and-mfa.md) to an external identity provider, and the licences that pay for it. OAuth as an *API authorization* protocol is [06-integration · 15](../06-integration-and-apis/15-oauth-flows-and-authorization.md); Experience Cloud login pages, self-registration and headless identity are [05-experience-cloud · 10](../05-experience-cloud-lwr/INDEX.md).

## Core idea

SSO moves one question — *is this person who they claim to be* — out of Salesforce and into a system that already answers it for every other application. Everything downstream is unchanged: the assertion arrives, Salesforce maps it to a `User` record, and the access model in [02](02-licences-and-what-they-gate.md)–[15](15-auditing-and-troubleshooting-access.md) takes over exactly as before. Two consequences follow and both surprise people. First, **SSO is an authentication control, not an access control** — a federated user with a wide profile is still a wide user. Second, Salesforce can play either role: **service provider** (the common case) or **identity provider** for other applications, which is what Identity licences are for.

## How it works

| Concept | SAML 2.0 | OpenID Connect |
|---|---|---|
| the token | signed XML **assertion** | signed JWT **ID token** |
| who starts it | **IdP-initiated** (portal tile) or **SP-initiated** (My Domain login page) | usually SP-initiated |
| the user match | `Federation ID` on the User, or Username, or a custom SAML attribute | the `sub` claim mapped by an *Authentication Provider* |
| typical use | workforce SSO from Entra ID, Okta, Ping | social sign-on, customer identity, App-to-app |
| trust anchor | certificate exchange, signed both ways | discovery document + client secret |

- **`Federation ID` is the field that makes SSO portable.** Matching on Username couples your IdP to Salesforce's username namespace, which then blocks the sandbox refresh that appends `.sandboxname`.
- **JIT provisioning creates or updates the `User` on first login** from assertion attributes — profile, role, permission set assignments, locale. It removes the joiner delay and quietly makes your IdP's attribute mapping into access configuration. → [05](05-user-access-policies-and-lifecycle.md)
- **My Domain is a prerequisite, not an accessory.** SP-initiated SSO, login discovery and multiple concurrent IdPs all require it. → [20](20-my-domain-enhanced-domains-and-trusted-urls.md)
- **SSO is included in the core licences.** Every Professional, Enterprise, Unlimited and Performance org also gets **100 complimentary Identity licences**, so buying Identity purely to enable SSO is a common and unnecessary spend.
- **External Identity is licensed per *monthly active* user**, which is why dormant customer accounts are cheap and over-provisioning is not — the opposite of the internal licence model in [02](02-licences-and-what-they-gate.md).
- **Delegated Authentication is not SSO.** It posts the typed password to a SOAP endpoint you host; it predates SAML, is enabled by Salesforce Support, and should be treated as legacy.

## 2026 currency

Two things to carry. **Triple DES is being retired from SAML configurations**, so any single sign-on set up before roughly 2015 needs its encryption algorithm reviewed — an SSO configuration is one of the few places a decade-old cipher choice quietly survives. And **certificate rotation cycles have shortened**, which matters more than it sounds: a Salesforce-generated self-signed certificate used to sign SAML requests, or held by the IdP to validate them, has an expiry date that appears in nobody's release plan. Set a calendar reminder at issue time and re-check *both* ends — the org's certificate under Setup → Certificate and Key Management, and the IdP's signing certificate uploaded into the Single Sign-On Settings. This is the outage that arrives at 2am with no deployment to blame.

## Gotchas

- **An expired signing certificate takes down every federated login at once**, and the error message names neither the certificate nor the expiry.
- **IdP-initiated SSO bypasses the My Domain login page**, so login flows and discovery behaviour differ between the two entry points. Test both.
- **JIT provisioning failures look like login failures.** A missing required field or an unmatched profile name in the assertion rejects the user with no useful detail — check the SAML Assertion Validator and Login History.
- **`Is Single Sign-On Enabled` on a profile does not force SSO.** Password login remains possible unless you also remove it; auditors ask for the second half.
- **Sandbox refresh does not carry the IdP's trust.** Endpoints, entity IDs and certificates all change, so SSO breaks by design on every refresh.
- **SSO satisfies MFA only as strongly as the IdP does** — privileged users need phishing-resistant methods at the IdP too. → [17](17-authentication-and-mfa.md)
- **Two-factor at Salesforce plus two-factor at the IdP double-prompts users** and is the commonest reason people disable something they should not.

## Recall

Q: Which field should an SSO integration match on, and why not Username?
A: `Federation ID`. Username matching breaks on sandbox refresh, when Salesforce appends the sandbox name to every username.

Q: What does JIT provisioning do, and what does it turn your IdP into?
A: It creates or updates the `User` record from assertion attributes on first login — which makes the IdP's attribute mapping part of your access configuration.

Q: Do you need Identity licences to enable SSO?
A: No. SSO is included in the core licences, and PE/EE/UE/Performance orgs also get 100 free Identity licences.

Q: How is External Identity licensed, and what behaviour does that encourage?
A: Per monthly active user — so dormant accounts cost nothing and over-provisioning is penalised.

Q: What is the identity-side outage with no deployment to blame?
A: An expired signing certificate, at either end of the SAML trust. Rotation cycles shortened in 2026.

## Related

- [17 · Authentication & MFA](17-authentication-and-mfa.md) — what SSO delegates, and the strength the IdP must still meet
- [20 · My Domain, enhanced domains & Trusted URLs](20-my-domain-enhanced-domains-and-trusted-urls.md) — the prerequisite for SP-initiated SSO
- [02 · Licences & what they gate](02-licences-and-what-they-gate.md) — Identity and External Identity in the licence hierarchy
- [06-integration · 15 OAuth flows & authorization](../06-integration-and-apis/15-oauth-flows-and-authorization.md) — OAuth for API authorization, the other half of the identity story
