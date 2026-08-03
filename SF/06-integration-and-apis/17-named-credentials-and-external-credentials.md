# Named Credentials & External Credentials

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 13

**Scope:** Outbound authentication — how Salesforce calls someone else's API without your code holding a secret. The Apex mechanics are [02-apex · 19](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md); certificates and mutual TLS are [26](26-certificates-mutual-tls-and-the-pki-changes.md); inbound auth is [15](15-oauth-flows-and-authorization.md).

> **What changed.** The single-object named credential in every tutorial is the **legacy** one, and it is **deprecated**. Since Winter '23 the model is two objects: an **external credential** holding the authentication protocol and its principals, and a **named credential** holding the base URL and pointing at one. The migration is not a rename — the legacy object has no principals, so it cannot express *who* may call out. Note carefully: deprecated, **with no published retirement date**.

## Core idea

Every callout answers two questions that older configuration merged: *where am I calling* and *as whom*. Splitting them is what makes outbound access reviewable. The endpoint is deployment-specific — it differs between sandbox and production — while the identity is a governance decision that belongs to security, not to whoever wrote the class.

The seam pays off immediately. One external credential describes how to authenticate to a system and which **principals** exist; any number of named credentials point at it for different base URLs. And because principals map to **permission sets**, granting a user or an integration the right to call an external system becomes a permission set assignment — auditable in the same place as everything else.

## How it works

| Object | Owns |
|---|---|
| **Named credential** | base URL, and which external credential to use |
| **External credential** | authentication protocol — OAuth 2.0, JWT, AWS Signature v4, Basic, custom |
| **Principal** | the identity the call is made as — **Named Principal** (one shared) or **Per User Principal** |
| **Permission set** | who may use that principal, granted per external credential principal |

- **`callout:My_Named_Credential/path` is the whole surface** in Apex, Flow HTTP Callout, External Services and Salesforce Connect. No endpoint literal, no Remote Site Setting, no token handling.
- **The platform injects the header and refreshes the token.** Secrets never reach a debug log, and `{!$Credential.Password}`-style merge fields let a custom header reference a secret without reading it.
- **Named Principal is one identity for everyone; Per User Principal is one per caller.** The second is what portals and per-user OAuth need, and what batch jobs cannot use.
- **Summer '26: the Salesforce Connect cross-org adapter now supports named credentials**, closing a gap where org-to-org connections needed weaker configuration → [20](20-salesforce-connect-and-external-objects.md).
- **Legacy named credentials still work.** They are a separate Setup list, receive no enhancements, and cannot be upgraded in place.

## 2026 currency

Deprecated is exactly the right word and the whole word: Salesforce says legacy named credentials *"will be discontinued in a future release"* and **publishes no date**. Plan the migration on maintainability grounds — no principals means no permission-set-based grant, so an org on legacy credentials has no way to answer *"who is allowed to call this system"* — not on a deadline that does not exist. This is the ninth time in this build that "old" and "dead" would have been conflated; see [../CURRENCY.md](../CURRENCY.md). The direction of travel is the same one [16](16-external-client-apps.md) is on: named, scoped, permission-gated app identities everywhere.

## Gotchas

- **Migration is a rebuild, not an upgrade.** There is no in-place conversion, and every consumer — Apex, Flow, External Services, Salesforce Connect — must be repointed at the new name.
- **A user without permission-set access to the principal gets an *authentication* failure**, not a permissions error, which sends the investigation to the remote system.
- **Per User Principal has no answer for automation.** A batch job, a scheduled flow or a platform-event subscriber runs as an automation user with no stored credential, and it fails at runtime in production.
- **Deleting an external credential does not warn about the named credentials pointing at it**, and the callouts fail as authentication errors afterwards.
- **The name is the contract.** Renaming a named credential breaks every `callout:` reference silently at runtime — they are strings, so nothing fails to compile.
- **Sandbox refresh carries the configuration but not the trust.** Client secrets and per-user tokens do not survive; the callouts fail on the first run after every refresh.

## Recall

Q: What are the two objects, and what does each own?
A: The external credential owns the authentication protocol and its principals; the named credential owns the base URL and points at an external credential.

Q: When are legacy named credentials retired?
A: There is no published retirement date. They are deprecated and receive no enhancements — that is the whole claim.

Q: Why is migrating off legacy not a rename?
A: The legacy object has no principals, so it cannot express who may call out via a permission set. The access model is the thing being added.

Q: How is permission to make an authenticated callout granted?
A: By assigning a permission set mapped to the external credential's principal.

Q: What broke on the last sandbox refresh even though the named credential is there?
A: Secrets and per-user tokens do not survive a refresh — the configuration copies, the trust does not.

## Related

- [02-apex · 19 Callouts & HTTP in Apex](../02-apex-and-triggers/19-callouts-named-credentials-and-http-in-apex.md) — the limits, and `callout:` in code
- [26 · Certificates, mutual TLS & the PKI changes](26-certificates-mutual-tls-and-the-pki-changes.md) — when the credential is a certificate rather than a secret
- [20 · Salesforce Connect & external objects](20-salesforce-connect-and-external-objects.md) — a named-credential consumer that is not code
- [15 · OAuth flows & authorization](15-oauth-flows-and-authorization.md) — the same decisions, inbound
