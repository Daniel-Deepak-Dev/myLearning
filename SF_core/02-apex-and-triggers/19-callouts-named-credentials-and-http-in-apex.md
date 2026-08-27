# Callouts, Named Credentials & HTTP in Apex

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 04

**Scope:** Calling out of Salesforce from Apex — the HTTP classes, the limits, and where the credentials live. Integration patterns, inbound APIs and OAuth flows are [06-integration](../06-integration-and-apis/INDEX.md).

> **What changed.** A hardcoded endpoint plus a Remote Site Setting is no longer how this is done, and neither is the single-object named credential most tutorials show. Since Winter '23 the model is **two objects** — an *external credential* holding the authentication protocol and its principals, and a *named credential* holding the URL and pointing at it. **Legacy named credentials are deprecated** and will be discontinued.

## Core idea

Every callout is two decisions that older code habitually merged: *where am I calling* and *as whom*. Named credentials exist to take the second one out of Apex entirely — the platform injects the authorisation header, refreshes the token, and stores the secret somewhere your debug log cannot reach. What Winter '23 added was a seam in the middle of that: one external credential describes how to authenticate to a system and who may do so, and any number of named credentials can point at it for different base URLs. The practical consequence is that granting a user or an integration the right to call an external system became a **permission set assignment** rather than a Setup edit, which is what makes it reviewable. Everything else in the topic is limits, and the limits exist because a callout holds a transaction open while a third party thinks.

## How it works

| Object | Owns | Example |
|---|---|---|
| **Named credential** | the base URL, and which external credential to use | `https://api.acme.com` |
| **External credential** | the authentication protocol and its principals | OAuth 2.0, JWT, AWS Signature v4, Basic |
| **Principal** | the identity the call is made as | Named Principal (one shared) or Per User Principal |
| **Permission set** | who is allowed to use that principal | assigned per external credential principal |

- **`callout:Named_Credential/path` is the whole integration surface in Apex.** No endpoint literal, no Remote Site Setting, no token handling, and the same code works in sandbox and production because the name resolves differently in each.
- **Three limits, and the middle one surprises people**: 100 callouts per transaction, a **cumulative 120 seconds** of callout time per transaction, and a per-callout timeout that defaults to 10 seconds and can be raised to 120.
- **Custom headers can reference the stored secret** without reading it — `{!$Credential.Password}` and friends are resolved by the platform at send time.
- **`Continuation` is for a long-running call made from a Lightning component**: up to three parallel callouts, released from the request thread while waiting, resumed in a callback. It is the answer to "this API takes 40 seconds and the user is watching".

```apex
public class AcmeClient {
    public static HttpResponse fetchOrder(String externalId) {
        HttpRequest req = new HttpRequest();
        req.setEndpoint('callout:Acme_API/v2/orders/'
                        + EncodingUtil.urlEncode(externalId, 'UTF-8'));
        req.setMethod('GET');
        req.setTimeout(20000);                     // default is 10s; the ceiling is 120s
        HttpResponse res = new Http().send(req);   // auth header injected by the platform
        if (res.getStatusCode() >= 400) {
            throw new AcmeCalloutException(res.getStatusCode() + ': ' + res.getBody());
        }
        return res;
    }
}
```

> **From my notes.** *Can we perform a callout after a DML operation?* No — and the exception says so in words: `You have uncommitted work pending. Please commit or rollback before calling out.` My note's answer was "use `@future`". That works and is no longer the advice: a `Queueable implements Database.AllowsCallouts` does the same job with typed state and a job ID. The reasoning is the part worth keeping — an open transaction holds row locks, and the platform will not let you hold them while a third party takes its time. Often the better fix is not async at all: **do the callout first**, then the DML.

## 2026 currency

Legacy named credentials still function but are deprecated and no longer receive enhancements, so the migration is a *when*, not an *if* — and it is not a rename, because the legacy object has no principals to map to permission sets and therefore no way to express who may call out. The wider direction is the same one Connected Apps are on: **External Client Apps** are the supported model for new external integrations, and outbound auth from Apex sits inside that story. Anything here that touches OAuth setup, JWT, or the client-app model is owned by [06-integration](../06-integration-and-apis/INDEX.md); the retirement list is [../CURRENCY.md](../CURRENCY.md) and dated detail is in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md).

## Gotchas

- **A trigger cannot make a synchronous callout at all.** It compiles and it throws at runtime, so the design has to be async from the start. → [13](13-queueable-apex-and-chaining.md)
- **The 120-second budget is cumulative per transaction, not per callout.** Five perfectly legal 30-second calls exceed it, and the fifth one dies rather than the slow one. The per-callout default is only **10 seconds**, so a partner that usually answers in 8 fails intermittently under load and looks like a network problem.
- **Per User Principal means every caller needs their own stored credential.** A batch job running as an automation user has none, and the failure appears at runtime in production, not at deployment.
- **A user without permission-set access to the external credential's principal gets an authentication failure**, not a permissions error — which sends people to debug the remote system.
- **An un-mocked callout throws in every test.** `Test.setMock` with an `HttpCalloutMock` is mandatory, and mocking it is also the only way to test the error branches.
- **Unencoded path segments break the endpoint silently.** `EncodingUtil.urlEncode` on anything user-supplied, always — an ID with a space becomes a 404 that looks like missing data.

## Recall

Q: What are the two objects in the current named credential model, and what does each own?
A: The external credential owns the authentication protocol and its principals; the named credential owns the base URL and points at an external credential.

Q: How is permission to make an authenticated callout granted?
A: By assigning a permission set that maps to the external credential's principal — not by editing Setup for each user.

Q: What are the three callout limits per transaction?
A: 100 callouts, 120 seconds of cumulative callout time, and a per-callout timeout defaulting to 10 seconds with a 120-second ceiling.

Q: Why can't you call out after a DML operation in the same transaction?
A: The uncommitted transaction holds row locks. The platform refuses to hold them while waiting on an external system — do the callout first, or move it into a Queueable.

Q: What is `Continuation` for?
A: A long-running callout initiated from a Lightning component — up to three in parallel, released from the request thread while waiting and resumed in a callback.

## Related

- [13 · Queueable Apex & chaining](13-queueable-apex-and-chaining.md) — `Database.AllowsCallouts`, and the way a trigger actually reaches an external system
- [06-integration · 17 Named Credentials & External Credentials](../06-integration-and-apis/17-named-credentials-and-external-credentials.md) — the same two objects, from the integration side
- [06-integration · 15 OAuth flows & authorization](../06-integration-and-apis/15-oauth-flows-and-authorization.md) — the inbound direction, and External Client Apps
- [09 · Exception handling & custom exceptions](09-exception-handling-and-custom-exceptions.md) — turning a 500 from a partner into something the org can act on
- [29 · JSON, serialization & untyped data](29-json-serialization-and-untyped-data.md) — reading the body once it arrives, and why a partner's field named `currency` forces `deserializeUntyped`
