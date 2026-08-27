# Authentication & MFA

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Proving who the user is. Layer 2 of [01](01-security-model-layers-overview.md), the half that runs *before* any permission is consulted. What happens to the session afterwards is [18](18-session-security-login-policies-and-step-up.md); federating the decision to another identity provider is [19](19-sso-saml-oidc-and-identity.md).

> **What changed.** *"MFA is contractually required"* was the 2022–2025 answer and it is now out of date in the direction that matters: **MFA is technically enforced**, not merely promised in the Trust and Compliance documents. And for privileged users a second shift landed in mid-2026 — **only phishing-resistant methods count**. Salesforce Authenticator, TOTP apps, SMS and email codes no longer satisfy the requirement for anyone with admin-grade access.

## Core idea

Authentication is the only layer where the platform's answer is binary and the blast radius is total: everything in [02](02-licences-and-what-they-gate.md)–[15](15-auditing-and-troubleshooting-access.md) assumes the person at the keyboard is who the `User` record says. That assumption is exactly what 2024–2026's breaches attacked — not the sharing model, but the login. The platform's response has been to stop treating strong authentication as a posture choice and start enforcing it, in waves, with dates. Which means an architect's job here is no longer to *recommend* MFA; it is to know **who is in scope for which strength**, and what that does to the integration users and automation nobody thought of as "logins".

## How it works

| Requirement | Who it applies to | Accepted proof |
|---|---|---|
| **MFA** | all employee-licence users logging in directly | authenticator app, security key, built-in authenticator, SMS/email codes |
| **Phishing-resistant MFA** | System Administrator profile, and anyone with `Modify All Data`, `View All Data`, `Customize Application` or `Author Apex` | **WebAuthn/FIDO2 only** — platform passkeys (Touch ID, Face ID, Windows Hello) or hardware keys (YubiKey, Titan) |
| **Satisfied at the IdP** | SSO users | the IdP's own MFA — Salesforce does not re-prompt if the assertion carries it |
| **Out of scope** | integration and API-only users authenticating by OAuth | the flow's own credentials — see [06 · 15](../06-integration-and-apis/15-oauth-flows-and-authorization.md) |

- **Enforcement is wave-rolled, not flag-day.** Sandboxes led (from 22 June 2026), production followed (from 1 July 2026), and the exact date varied by org. "It hasn't hit us yet" is a schedule position, not an exemption.
- **The four permissions, not the job title, define the privileged set.** A "read-only auditor" profile carrying `View All Data` is in scope for hardware-key MFA; check the permission, not the label. → [03](03-profiles-and-the-permission-set-led-model.md)
- **An SSO user who has never registered an MFA method still gets prompted** — Salesforce falls back to a one-time passcode by email or SMS to establish identity.
- **Device-bound is the point.** A passkey cannot be read out over the phone, typed into a lookalike domain or relayed by an attacker-in-the-middle; a TOTP code can be all three.
- **Registering a second method is operational, not optional.** A lost hardware key with no backup passkey is an admin lockout, and the recovery path runs through Salesforce Support.

## 2026 currency

The enforcement dates and the wider wave they belong to are tabulated in [../CURRENCY.md](../CURRENCY.md); do not restate them in five notes. Two adjacent retirements close the loop, because a strong front door means nothing while a weak one stands open: the **OAuth username-password flow** is being retired for connected apps (Winter '27) and **SOAP `login()` for API versions 31.0–64.0** follows in Summer '27. Both are flows where a username and password alone produce a session, which is precisely what MFA was introduced to prevent — so treat any remaining use of them as an authentication finding, not an integration one. → [26](26-secure-coding-checklist.md)

## Gotchas

- **Automation that logs in as a human breaks first.** Anything driving the UI with stored credentials — legacy test rigs, screen-scrapers, some middleware — has no way to present a passkey.
- **Sandbox enforcement arrives before production**, so the first symptom is usually a developer locked out of a sandbox admin account.
- **`Modify All Data` on a permission set counts.** People audit profiles and forget that a permission set group can grant the same thing. → [04](04-permission-set-groups-and-muting.md)
- **SSO does not exempt you** — it relocates the requirement to the IdP. If the IdP's MFA is a TOTP app, privileged users are still non-compliant.
- **Salesforce Authenticator is not dead** — it remains valid for ordinary users. Saying "it was retired" is the seventh flavour of the same mistake this vault keeps catching.
- **Login IP ranges are a control, not a substitute.** They restrict *where* a login may come from; they say nothing about *who*. → [18](18-session-security-login-policies-and-step-up.md)
- **The `User` record's identity-verification history is queryable** (`VerificationHistory`) — that, not a spreadsheet, is how you prove adoption. → [15](15-auditing-and-troubleshooting-access.md)

## Recall

Q: Is MFA a contractual requirement or a technical one in 2026?
A: Both, but the technical enforcement is what matters now — Salesforce enforces MFA at login rather than relying on the contract.

Q: Which users need phishing-resistant MFA, and what qualifies?
A: The System Administrator profile plus anyone with `Modify All Data`, `View All Data`, `Customize Application` or `Author Apex`. Only WebAuthn/FIDO2 — platform passkeys or hardware security keys.

Q: What stopped counting for those users?
A: Salesforce Authenticator, TOTP apps, SMS codes and email codes.

Q: How does SSO interact with the requirement?
A: The IdP satisfies it, so Salesforce does not re-prompt — but the IdP's own MFA must meet the same strength for privileged users.

Q: Which two legacy authentication paths are being retired for the same reason?
A: The OAuth username-password flow (Winter '27) and SOAP `login()` for API 31.0–64.0 (Summer '27) — both mint a session from a password alone.

## Related

- [18 · Session security, login policies & step-up](18-session-security-login-policies-and-step-up.md) — what the platform does once the login succeeds
- [19 · SSO, SAML, OIDC & identity](19-sso-saml-oidc-and-identity.md) — moving the authentication decision to an external IdP
- [01 · Security model layers overview](01-security-model-layers-overview.md) — where authentication sits in the debugging order
- [06-integration · 15 OAuth flows & authorization](../06-integration-and-apis/15-oauth-flows-and-authorization.md) — the flows, and the two being retired
