# Offline LWC & Mobile Constraints

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** What a component can and cannot do in the Salesforce mobile app with no network, and the device APIs it gains in exchange. The online GraphQL adapter is [07](07-graphql-wire-adapter.md).

## Core idea

LWC Offline is not "the same component, slower." It is a **different runtime with a different data source**: a local store on the device, primed in advance, served by the UI API wire adapters. Everything that requires a server is therefore gone — and the single fact that reorganises the whole topic is that **Apex does not run offline at all**, neither `@wire`d nor imperative. So does every trigger, validation rule and flow: they execute at *sync*, not at save, which means an offline save can succeed on the device and fail hours later on the server. That inverts two habits. Validation has to be client-side, because the server's will not run in time to help the user. And any component that reaches for Apex — the default answer for "the wire adapters can't express this" ([08](08-apex-in-lwc-wire-vs-imperative.md)) — is simply not an offline component.

## How it works

| Capability | Offline |
|---|---|
| `lightning/ui*Api` wire adapters (`getRecord`, `createRecord`, …) | ✅ against the local store |
| Apex — `@wire` **and** imperative | ❌ not available at all |
| `getListUi`, `getRecordUi` | ❌ |
| `getRelatedListRecords` / `getRelatedListCount` | ⚠️ do not reflect offline creates/deletes until sync |
| GraphQL | ✅ but only via **`lightning/uiGraphQLApi`** |
| Triggers, validation rules, flows | ❌ deferred to sync |

- **Draft records are the write model.** A record created or edited offline is stored locally and queued; it is not a real record and has no real Id until the queue drains.
- **Priming decides what exists offline.** **Briefcase Builder** declares which records are pushed to the device — a component can only read what was primed, so "it works online" proves nothing.
- **Offline GraphQL is the older module.** `lightning/uiGraphQLApi`, *not* `lightning/graphql`, and it does **not** support optional fields or dynamic query construction. Queries need metaschema directives for priming and referential integrity.
- **GraphQL query limits still apply**: up to 10 subqueries, up to 2000 records per subquery.
- **Mobile is also a form factor, not only a network state.** `@salesforce/client/formFactor` returns `Small`/`Medium`/`Large`, and `supportedFormFactors` in `js-meta.xml` decides where the component is even offered.
- **Device APIs are the upside.** `lightning/mobileCapabilities` exposes barcode scanning, location, biometrics, NFC and document scanning — capabilities a desktop component has no equivalent for.

## 2026 currency

The two GraphQL stories have **diverged and are easy to conflate**. Online, the wire adapter is the modern one and gains features release by release ([07](07-graphql-wire-adapter.md)); offline, you are on `lightning/uiGraphQLApi`, which is explicitly documented as not carrying the newer capabilities. A query that works in a desktop component may not be expressible offline, and the failure is at prime time rather than at run time. The framing that survives is the one the docs use: *LWC Offline is not the full Salesforce service.* Treat an offline component as a deliberately narrower build against the local store, not as a normal component with a flaky connection. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **Apex is unavailable offline — both call shapes.** Any component whose data path runs through an `@AuraEnabled` method is an online-only component, full stop.
- **Validation rules do not fire on an offline save.** They fire at sync, so the user is told hours later, out of context. Duplicate the check client-side.
- **A draft record has no real Id**, so navigation, related lists and anything keyed on Id behave differently until sync.
- **Un-primed data is simply absent** — not slow, not an error. Briefcase Builder configuration is part of the component's contract.
- **`getRelatedListRecords` and `getRelatedListCount` lag.** A record created offline does not appear in the related list, and the count is stale until sync.
- **`lightning/graphql` is not the offline module.** Using it offline fails; `lightning/uiGraphQLApi` is the one, with fewer features.
- **Toasts, navigation and container-dependent modules behave differently in the mobile container** — the same portability question as [18](18-error-handling-and-user-feedback.md) and [10](10-navigation-and-page-references.md).
- **`supportedFormFactors` omitting `Small` hides the component on phones entirely**, which looks like a deployment failure and is a metadata line.

## Recall

Q: Can an offline LWC call Apex?
A: No — neither `@wire`d nor imperative. Apex runs only on the server, so an Apex-dependent component is online-only.

Q: When do validation rules and triggers run for a record created offline?
A: At sync, not at save. The user can be told an offline save was rejected long after they made it, which is why client-side validation is mandatory.

Q: Which GraphQL module does Mobile Offline require, and what does it not support?
A: `lightning/uiGraphQLApi`. It does not support optional fields or dynamic query construction, and offline queries need metaschema directives.

Q: What is a draft record?
A: A record created or modified offline, held in a local queue with no server Id until it synchronises.

Q: What decides which records a component can read offline?
A: Priming — Briefcase Builder configuration. Data that was not primed is absent, with no error.

## Related

- [07 · GraphQL wire adapter](07-graphql-wire-adapter.md) — the online adapter, and how far it has moved past the offline one
- [08 · Apex in LWC](08-apex-in-lwc-wire-vs-imperative.md) — the dependency that makes a component online-only
- [06 · Lightning Data Service](06-lightning-data-service-and-ui-api-wires.md) — the wire adapters that do survive offline
- [16 · Performance & debugging](16-lwc-performance-and-debugging.md) — every client cost is larger on a phone
- [08-data · Data modeling](../08-data-modeling-and-large-data-volumes/INDEX.md) — priming is a data-volume decision as much as a mobile one
