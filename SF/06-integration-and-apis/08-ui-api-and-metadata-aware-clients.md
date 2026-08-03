# UI API & metadata-aware clients

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The API that returns data *and* the metadata needed to render it — for custom clients that must look and behave like Salesforce. The in-org consumer of the same endpoints is LDS ([03-lwc · 06](../03-lwc-and-slds/06-lightning-data-service-and-ui-api-wires.md)).

## Core idea

Every other API answers *"what is the data?"* UI API also answers *"how should it be displayed?"* — field labels in the user's language, layout order, section grouping, picklist values valid for that record type, theme colours and icons. That is the difference between a client that shows a JSON blob and one that shows a Salesforce record.

The reason this matters architecturally is **maintenance**. A mobile app built on REST hardcodes labels, field order and picklist values, and diverges from the org the moment an admin changes anything. The same app on UI API inherits admin changes for free, because layout and FLS are part of the response rather than assumptions baked into the client.

**Lightning Data Service is UI API**, consumed from inside the platform. Learning one teaches the other.

## How it works

| Need | Resource |
|---|---|
| Record + display metadata | `/ui-api/record-ui/{recordIds}` |
| Record data only | `/ui-api/records/{recordId}` |
| Create defaults for a new record | `/ui-api/record-defaults/create/{objectApiName}` |
| Object metadata | `/ui-api/object-info/{objectApiName}` |
| Picklist values by record type | `/ui-api/object-info/{obj}/picklist-values/{recordTypeId}` |
| List views | `/ui-api/list-ui/{objectApiName}` |
| Lookup suggestions | `/ui-api/lookups/{objectApiName}/{fieldApiName}` |
| CSRF token *(67.0)* | `GET /ui-api/session/csrf` |

- **FLS is applied to the response, not signalled in it.** A field the user cannot see is simply absent — so a client must render from what arrived, never from a static field list. → [07-security · 13](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md)
- **Picklist values are record-type dependent**, which is why the record type ID is in the path. A client that caches one global picklist will offer invalid values.
- **`record-defaults/create` is how you build a correct new-record form** — defaults, required flags and layout, without reimplementing the org's configuration.
- **It is scoped to Lightning Experience semantics.** UI API does not expose everything REST does; it exposes what a Salesforce-shaped UI needs.
- **The natural consumers are mobile and headless front ends**, including Experience Cloud built outside Experience Builder. → [05-experience-cloud · 13](../05-experience-cloud-lwr/INDEX.md)

## 2026 currency

**Summer '26 added `GET /ui-api/session/csrf`**, giving external clients a supported way to obtain a CSRF token instead of scraping one — a small addition that removes a genuinely fragile workaround. The larger context is **Headless 360**: Salesforce's stated direction is that every capability is reachable as an API, an MCP tool or a CLI command, and UI API is the piece that lets a non-Salesforce front end stay faithful to org configuration while doing it → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md). Note the boundary with [10](10-graphql-api.md): GraphQL is the efficient way to *query* across objects; UI API remains the way to *render* like Salesforce.

## Gotchas

- **Missing field ≠ empty field.** Absent means no access; null means no value. Clients that conflate them display "—" where they should hide the row entirely.
- **`record-ui` responses are large.** Requesting layout metadata per record in a list is the standard performance mistake — fetch object metadata once, records many times.
- **Object metadata is heavily cacheable and rarely is.** `object-info` changes only when an admin changes the org.
- **Not every object is supported.** UI API's object coverage is narrower than REST's, and the gap is discovered late.
- **Mobile Offline requires `lightning/uiGraphQLApi`, not this**, and that module supports neither optional fields nor dynamic queries. → [03-lwc · 20](../03-lwc-and-slds/20-offline-lwc-and-mobile-constraints.md)
- **Do not rebuild LDS on top of it inside the platform.** In an LWC, the wire adapters already are this API, with caching and invalidation. → [03-lwc · 06](../03-lwc-and-slds/06-lightning-data-service-and-ui-api-wires.md)

## Recall

Q: What does UI API return that REST does not?
A: The display metadata — labels, layout order, record-type-specific picklist values, themes — alongside the data.

Q: What is Lightning Data Service, in terms of this note?
A: UI API consumed from inside the platform, with client-side caching on top.

Q: How does a UI API response represent a field the user cannot see?
A: It omits it. Absence means no access — distinct from a null value.

Q: What was added to UI API at 67.0?
A: `GET /ui-api/session/csrf`, a supported way for external clients to obtain a CSRF token.

Q: Why does the picklist-values resource take a record type ID?
A: Valid picklist values depend on record type; a single cached global list will offer invalid options.

## Related

- [03-lwc · 06 Lightning Data Service](../03-lwc-and-slds/06-lightning-data-service-and-ui-api-wires.md) — the same API, from inside a component
- [10 · GraphQL API](10-graphql-api.md) — the efficient cross-object read surface
- [04 · REST API fundamentals](04-rest-api-fundamentals.md) — broader object coverage, no display metadata
- [05-experience-cloud · INDEX](../05-experience-cloud-lwr/INDEX.md) — headless front ends that consume this
