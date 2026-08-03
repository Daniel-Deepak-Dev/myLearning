# REST API fundamentals

> Area: 06-integration-and-apis · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 12

**Scope:** The default inbound surface — sObject CRUD, query, describe, and the response headers that tell you how much budget is left. Multi-request transactions are [06](06-composite-batch-and-graph-apis.md); high volume is [07](07-bulk-api-2.md); custom endpoints are [16](INDEX.md).

## Core idea

REST API is the answer unless something specific rules it out. It speaks JSON over HTTPS, authenticates with a bearer token from any OAuth flow, versions in the path, and exposes every object the running user can see — including custom objects — with no per-object configuration. Its shape is deliberately boring: one resource per record, verbs mapped the obvious way, and describe calls that let a client discover the schema instead of hardcoding it.

What matters most is the last property. **REST enforces the running user**, so every response is already shaped by profile, permission set, FLS and sharing. An integration user with broad access is not a REST decision, it is an access-model decision made in [07-security](../07-security-and-sharing/INDEX.md) — and it is where over-permissioned integrations come from.

## How it works

| Need | Resource |
|---|---|
| List versions / resources | `/services/data/` · `/services/data/v67.0/` |
| Record CRUD | `/sobjects/Account/{id}` — `GET`, `POST`, `PATCH`, `DELETE` |
| Upsert on external ID | `PATCH /sobjects/Account/ExtId__c/{value}` |
| Query | `/query?q=SELECT+Id+FROM+Account` · `/queryAll` for deleted and archived |
| Search | `/search?q=FIND+{Acme}` |
| Describe | `/sobjects/Account/describe` · `/sobjects/` for the global list |
| Org limits | `/limits` |

- **Upsert by external ID is the integration primitive.** It removes the "do I already have this record?" round trip and makes retries idempotent — the same call twice produces one record. → [21](INDEX.md), [08-data · 03](../08-data-modeling-and-large-data-volumes/03-record-ids-external-ids-and-upsert.md)
- **Large query results paginate.** The response carries `nextRecordsUrl` until `done` is `true`; a client that ignores it silently processes the first page only.
- **`Sforce-Limit-Info` comes back on every response** with the org's API request count against its 24-hour allowance. Read it rather than guessing. → [24](INDEX.md)
- **Composite is still REST.** When one logical operation needs several calls, [06](06-composite-batch-and-graph-apis.md) keeps them in one round trip and one transaction — reach for it before writing a client-side loop.
- **`PATCH` is a partial update.** Only the fields in the body are touched, which is what makes concurrent integrations survivable.

## 2026 currency

**REST runs in the running user's context and always has** — but the surrounding platform moved, so the phrasing matters at 67.0. Apex defaults to user mode ([02-apex · 10](../02-apex-and-triggers/INDEX.md)), which means an Apex REST endpoint ([16](INDEX.md)) now enforces the caller by default too, closing the gap where custom endpoints were more permissive than standard ones. Also new at 67.0: **UI API gained `GET /ui-api/session/csrf`** ([08](08-ui-api-and-metadata-aware-clients.md)), and **Connect REST API moved off its old per-user/per-app/per-hour throttle** onto the org's per-24-hour Platform API limit ([09](09-metadata-tooling-and-connect-apis.md)).

## Gotchas

- **A `GET` on a record the user cannot see returns 404, not 403.** The platform will not confirm a record exists — correct, and it sends debugging toward "bad ID" when the fault is access.
- **`/queryAll` is the only way to see soft-deleted rows.** `/query` silently excludes the Recycle Bin, which makes "the record vanished" reports hard to reproduce → [08-data · 13](../08-data-modeling-and-large-data-volumes/13-deletes-recycle-bin-and-physical-deletion.md).
- **Batch your reads with relationship queries, not with loops.** N+1 over `/sobjects/{id}` is the commonest way an integration exhausts the org's daily API allowance.
- **Error responses are an array, even for one error.** Clients that read `body.message` instead of `body[0].message` log `undefined` and lose the actual cause.
- **`describe` responses are large and stable** — cache them with the `If-Modified-Since` header rather than fetching per run.
- **Field-level security silently omits fields.** A field missing from a response is more often FLS than a wrong query. → [07-security · 13](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md)

## Recall

Q: Why is upsert on an external ID the integration primitive?
A: It removes the existence check and makes retries idempotent — the same call twice yields one record.

Q: What tells a client there are more query results?
A: `nextRecordsUrl` in the response, present until `done` is `true`.

Q: Which header reports remaining API budget, and how often?
A: `Sforce-Limit-Info`, on every response.

Q: What does a `GET` return for a record the running user cannot access?
A: 404 — the platform does not confirm the record exists.

Q: What is the difference between `/query` and `/queryAll`?
A: `/queryAll` includes soft-deleted and archived records; `/query` silently excludes them.

## Related

- [06 · Composite, Batch & Graph APIs](06-composite-batch-and-graph-apis.md) — several REST calls in one transaction
- [07 · Bulk API 2.0](07-bulk-api-2.md) — where REST stops being the right answer
- [10 · GraphQL API](10-graphql-api.md) — one round trip instead of many, for reads
- [07-security · 13 Field-level security](../07-security-and-sharing/13-field-level-security-and-visibility-layers.md) — why a field is missing from a response
