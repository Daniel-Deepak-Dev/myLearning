# Authentication, Self-Registration & SSO

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 18

**Scope:** How an external person becomes an authenticated user of your site — login page, self-registration, federated sign-on, and the headless option. The identity protocols are [07-security · 19](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md); OAuth as API authorization is [06-integration · 15](../06-integration-and-apis/15-oauth-flows-and-authorization.md).

## Core idea

Experience Cloud login is one Setup page — the site's **Login & Registration** workspace — sitting over four independent decisions: *who authenticates* (Salesforce, a social provider, a SAML IdP), *how an account gets created* (admin, self-registration, JIT provisioning), *what the user sees* (default pages, custom pages, or no Salesforce-rendered page at all), and *what happens around it* (login flows, verification, MFA).

The reason to hold them apart is that they compose in ways that surprise people. Self-registration with an external IdP, for instance, is not self-registration — it is just-in-time provisioning, and the two have different failure modes and different places to look when a user cannot get in.

## How it works

- **Login & Registration** per site configures the login page, the allowed identity providers, self-registration, forgot-password and the user-creation behaviour.
- **Self-registration creates a user and a Contact** against a configured Account and profile. That profile is a public-facing grant surface — everyone who registers gets it.
- **Site as service provider / relying party** delegates authentication: **SAML** when the third party only authenticates, an **authentication provider** when it also authorises access to its data. Social sign-on (Google, Facebook, Apple, OpenID Connect) is the same mechanism with a pre-built provider.
- **Just-in-time provisioning** creates the user on first federated login from assertion attributes — the right answer when the IdP is the source of truth for who exists.
- **Login flows** run a flow *after* credentials are accepted and before the session is granted — the hook for terms acceptance, extra verification or profile completion.
- **Headless Identity** is the no-Salesforce-UI option: the **Headless Registration**, **Headless Login**, **Headless Forgot Password** and **headless passwordless** APIs let an off-platform front end own the whole experience while Salesforce owns authentication. Enabled per site from the same Login & Registration page.
- **Passwordless login** registers verification methods — email, SMS, TOTP, U2F security key, Salesforce Authenticator — and is the usual answer for consumer-scale sites that don't want to hold passwords.

## 2026 currency

**MFA is enforced, not recommended**, and the privileged-user tier now requires **phishing-resistant** methods — but read the scope precisely before quoting it at a portal project: the July 2026 phishing-resistant requirement targets **administrative** access (System Administrator plus `Modify All Data`, `View All Data`, `Customize Application`, `Author Apex`), not ordinary external users → [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md). The Experience Cloud consequence is indirect and worth stating anyway: **the internal staff who administer the site are in scope**, so the project needs hardware keys or platform passkeys for its own admins even if its end users authenticate with a magic link. Separately, **legacy My Domain redirections ended in Spring '26**, so a hardcoded old login URL in a welcome email now 404s → [03](03-site-setup-domains-and-publishing.md).

## Gotchas

- **The self-registration profile is granted to strangers.** It is the most over-permissive profile in most orgs, and it is public by construction → [11](11-public-site-exposure-audit.md).
- **Self-registration with an external IdP is JIT provisioning**, not self-registration. Debug it in the SAML assertion, not the registration handler.
- **A login flow that errors locks everyone out**, because it sits between valid credentials and the session.
- **Custom login pages are still guest-rendered pages.** Everything in [07](07-guest-user-security-model.md) applies to them.
- **Headless Identity moves the UI, not the licensing.** A headless user still consumes an external licence → [08](08-licences-and-external-user-types.md).
- **Deactivating a Contact deactivates the community user** attached to it, which is how portal access disappears without anyone touching a user record.

## Recall

Q: Where is Experience Cloud login configured?
A: Per site, in the Login & Registration workspace — identity providers, self-registration, forgot password and user creation behaviour.

Q: What is the difference between self-registration and JIT provisioning?
A: Self-registration creates the user from a Salesforce-hosted form; JIT creates them from an external IdP's assertion on first federated login.

Q: What does a login flow sit between?
A: Accepted credentials and a granted session — which is why an error in one locks every user out.

Q: What is Headless Identity for?
A: Letting an off-platform front end own the entire login, registration and password-reset UI while Salesforce remains the authentication authority.

Q: Does the 2026 phishing-resistant MFA requirement apply to portal users?
A: No — it targets privileged internal access. It reaches an Experience Cloud project through the admins who run the site, not its external users.

## Related

- [07 · Guest user security model](07-guest-user-security-model.md) — the login page is a guest page
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — the self-registration profile as an exposure surface
- [07-security · 19 SSO, SAML, OIDC & identity](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md) — the federation protocols underneath
- [06-integration · 15 OAuth flows & authorization](../06-integration-and-apis/15-oauth-flows-and-authorization.md) — OAuth as API authorization, which this is not
