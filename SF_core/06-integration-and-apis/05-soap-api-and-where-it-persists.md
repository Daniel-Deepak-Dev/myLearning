---
vault: SF_core
area: 06-integration-and-apis
format: dense
status: learning
created: 2026-08-03
updated: 2026-10-28
currency: "Winter '27 (API 68.0)"
phase: 12
---
# SOAP API & where it persists

**Scope:** The XML/WSDL surface — the two WSDL flavours, what still genuinely runs on it, and the one call being withdrawn. The administration APIs that are *only* SOAP are [09](09-metadata-tooling-and-connect-apis.md).

## Core idea

SOAP API is the original programmatic surface and it is **not retired, not deprecated, and not going away** — a fact worth stating plainly, because "SOAP is dead" is repeated confidently and is wrong in a way that misleads scoping. What is true is narrower: **no new capability lands here first**, REST is the default for new integrations, and one authentication call is on a retirement clock.

Where SOAP genuinely persists is not legacy inertia. **The Metadata API is SOAP**, which means every deployment tool — the `sf` CLI, DevOps Center, VS Code, every CI pipeline — is a SOAP client whether its users know it or not. That alone guarantees the protocol outlives most of the code written against it.

## How it works

| WSDL | Shape | Use it when |
|---|---|---|
| **Enterprise** | strongly typed, generated **for one org's schema** | a single known org; compile-time type safety |
| **Partner** | loosely typed, schema-agnostic | many orgs, or a schema that changes — ISVs and middleware |

- **The enterprise WSDL is regenerated when the schema changes.** Adding a custom field can require a rebuild of the client, which is the trade for type safety and the reason ISVs choose partner.
- **Authentication has two paths.** `login()` returns a session ID from a username, password and security token; OAuth returns a bearer token usable in the same `sessionId` header. Only the first is being withdrawn.
- **A session ID and an OAuth access token are interchangeable in the header** — which is what makes the migration off `login()` a credential change rather than a rewrite.
- **The `AllOrNoneHeader` sets the transaction boundary** for multi-record calls, the SOAP equivalent of REST's `allOrNone`. → [06](06-composite-batch-and-graph-apis.md)
- **Metadata API and Tooling API both expose SOAP**, and Metadata API has no REST equivalent for its core deploy/retrieve cycle. → [09](09-metadata-tooling-and-connect-apis.md)

## 2026 currency

Two changes, in opposite directions. **`login()` is being retired for API versions 31.0–64.0 in Summer '27** — it mints a session from a password alone, which is precisely what MFA exists to prevent, so treat remaining use as an authentication finding rather than an integration one → [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md). Meanwhile SOAP **gained** capability at 67.0: it now accepts **JWT-based access tokens** in the `sessionId` header, reaching parity with REST authentication. An API receiving new authentication support in the same release as a retirement announcement is the clearest possible evidence that the protocol is being narrowed, not withdrawn. Dates and sourcing: [../CURRENCY.md](../CURRENCY.md).

Summer '27 is the last date, not the first. Winter '27 shipped the *Assign Use Any API Auth Permission for SOAP login()* Release Update: from **1 December 2026**, in every org and sandbox, a user without **`Use Any API Auth`** gets an error from `login()`. Then a one-time check **turns `login()` off in any org with no `login()` call in the previous six months** — sandboxes from **15 December 2026**, production from **31 January 2027**. An annual or disaster-recovery job is exactly what that check misses.

> **From my notes.** *`SOAP API`* (2019) is structurally sound — the enterprise/partner split and the header model are unchanged — but its worked example authenticates with `login()`, and it presents SOAP as the default choice for new integrations. Both were fair in 2019. Today REST is the default and `login()` is on a clock; the WSDL material is still worth keeping.

## Gotchas

- **"SOAP is retired" is wrong and costs credibility.** `login()` is retiring; the API is not. Nothing has an announced end-of-life. → [02](02-api-versions-and-the-retirement-treadmill.md)
- **The security token is not MFA** and is not required when the caller's IP is in a trusted range — which is why the same client works from one network and fails from another.
- **Enterprise WSDL clients break on schema changes** they were never told about. A field deletion in a sandbox surfaces as a compile error in someone else's build.
- **SOAP faults are not HTTP errors.** A fault can arrive with HTTP 500 *and* a well-formed body explaining the real cause; clients that branch on status code alone discard it.
- **Sandbox usernames carry the sandbox suffix.** Refresh, and every stored `login()` credential is wrong — a recurring outage that has nothing to do with the API.
- **`login()` through a Visualforce page had a documented interaction** with the instanced-URL blocking switch, fixed June 2026. → [03](03-api-endpoints-hostnames-and-edge-network.md)

## Recall

Q: Is SOAP API retired?
A: No — no announced end-of-life. Only the `login()` call is retiring, for API 31.0–64.0 in Summer '27.

Q: When do you choose the partner WSDL over the enterprise WSDL?
A: When the client must work across many orgs or against a changing schema — ISVs and middleware. Enterprise gives type safety for one known org.

Q: What did SOAP gain at API 67.0?
A: JWT-based access tokens in the `sessionId` header, reaching parity with REST authentication.

Q: Why does SOAP survive regardless of REST's dominance?
A: The Metadata API is SOAP, so every deployment tool and CI pipeline is a SOAP client.

Q: Why is remaining `login()` use an authentication finding rather than an integration one?
A: It mints a session from a username and password alone — exactly what MFA was introduced to prevent.

## Related

- [09 · Metadata, Tooling & Connect APIs](09-metadata-tooling-and-connect-apis.md) — the SOAP surfaces with no REST equivalent
- [02 · API versions & the retirement treadmill](02-api-versions-and-the-retirement-treadmill.md) — why `login()`'s version range is not a version retirement
- [07-security · 17 Authentication & MFA](../07-security-and-sharing/17-authentication-and-mfa.md) — the reason password-only session minting is going
- [15 · OAuth flows & authorization](INDEX.md) — what replaces `login()`

## Sources

- [Assign Use Any API Auth Permission for SOAP login() (Release Update)](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_api_soap_login.htm&release=264&type=5) — Winter '27 release notes · via search 2026-10-28 · enforced 1 December 2026 in all orgs and environments; grant by profile or permission set
- [Platform SOAP API login() Retirement & new Security Requirements (005132110)](https://help.salesforce.com/s/articleView?id=005132110&language=en_US&type=1) — Salesforce Help · via search 2026-10-28 · Summer '27 retirement for 31.0–64.0 unchanged; one-time six-month inactivity check from 15 Dec 2026 (sandboxes) and 31 Jan 2027 (production); login from a broad IP range needs a security token
- [(2026年10月) Salesforceの運用に関する重要なお知らせ](https://successjp.salesforce.com/article/NAI-001341) — Salesforce Japan Success Navi, 27 Oct 2026 · read 2026-10-28 · the SOAP `login()` permission update is one of the five Release Updates enforced in Winter '27

## History

- 2026-10-28 · Winter '27 currency check: added the 1 Dec 2026 `Use Any API Auth` enforcement and the six-month inactivity shut-off before the Summer '27 retirement
