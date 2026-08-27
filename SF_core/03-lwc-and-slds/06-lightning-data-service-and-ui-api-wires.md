# Lightning Data Service & UI API Wires

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** Reading and writing records without writing Apex — the UI API wire adapters, the shared cache behind them, and the record-form components layered on top. Arbitrary queries are [07](07-graphql-wire-adapter.md); anything needing server logic is [08](08-apex-in-lwc-wire-vs-imperative.md).

## Core idea

Lightning Data Service is a **shared client-side record cache**, and almost everything worth knowing follows from the word *shared*. Five components on a page wired to the same record produce one server request and hold one normalised copy; when any of them writes through LDS, all five see the new value without being told. It also enforces the running user's object permissions, field-level security and sharing rules for free, which is why an LDS-only component has no security review surface — there is no `with sharing` decision to get wrong because you never wrote the query. The price is that LDS is **record-shaped**: one record, or a known set of IDs, with spanning fields at most. There is no aggregate, no arbitrary `WHERE`, no "give me the ten most recent". The moment you need that, you have left LDS, and the honest next step is GraphQL or Apex — not a wire adapter fetching everything and filtering in JavaScript.

## How it works

| Import from `lightning/uiRecordApi` | Purpose |
|---|---|
| `getRecord` / `getRecords` | read one record, or several in one round trip |
| `getFieldValue(record, FIELD)` / `getFieldDisplayValue` | safe extraction, including spanning fields |
| `createRecord` / `updateRecord` / `deleteRecord` | imperative, promise-returning DML |
| `notifyRecordUpdateAvailable([{recordId}])` | tell LDS its cached copy is stale |
| `getObjectInfo`, `getPicklistValues` (`lightning/uiObjectInfoApi`) | metadata: fields, record types, picklists |

- **`fields` and `optionalFields` behave differently on no access.** A field in `fields` the user cannot see **errors the whole wire**; the same field in `optionalFields` is silently omitted. Use `optionalFields` for anything not every persona can read.
- **Import field references from `@salesforce/schema`.** `import NAME from '@salesforce/schema/Account.Name'` is compile-checked and registers a metadata dependency, so the field cannot be deleted out from under the component. A raw `'Account.Name'` string works and gives up both.
- **The three form components are one decision.** `lightning-record-form` is zero-config and gives you no layout control; `lightning-record-edit-form` hands you the fields so you can arrange and wrap them; `lightning-record-view-form` is the read-only version. All three go through LDS, so all three participate in the cache.
- **`getFieldValue` exists because the raw shape is awkward.** `record.fields.Owner.value.fields.Name.value` is what a spanning field actually looks like; the helper collapses it and returns `undefined` rather than throwing on a missing link.
- **Writes are imperative, reads are declarative.** There is no `@wire(updateRecord)`. You call it, you get a promise, and the cache broadcasts the result to every other consumer.

```js
import { LightningElement, api, wire } from 'lwc';
import { getRecord, getFieldValue } from 'lightning/uiRecordApi';
import NAME from '@salesforce/schema/Account.Name';
import OWNER from '@salesforce/schema/Account.Owner.Name';   // spanning — one hop only

export default class AccountHeader extends LightningElement {
    @api recordId;
    @wire(getRecord, { recordId: '$recordId', fields: [NAME], optionalFields: [OWNER] })
    account;                                                  // { data, error }

    get name()  { return getFieldValue(this.account.data, NAME); }
    get owner() { return getFieldValue(this.account.data, OWNER); }
}
```

## 2026 currency

The interesting movement is that LDS is no longer only a wire adapter. **Built-in Lightning state managers went GA at 67.0** — `lightning/stateManagerRecord`, `lightning/stateManagerObjectInfo` and siblings wrap the same UI API access in the `defineState` model and **participate fully in LDS caching, normalisation and subscriptions**, so they are not a parallel cache competing with this one. Reach for those before hand-rolling a manager over `getRecord`; the mechanics are in [05](05-decorators-and-the-reactivity-model.md) and are not repeated here. The other thing worth knowing in 2026 is a *negative*: the GraphQL wire adapter added a great deal of read power and **still has no mutations**, so LDS remains the only supported client-side create, edit and delete path. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`getRecord` requires `fields`, `optionalFields` or `layoutTypes`.** Omitting all three is not "give me everything" — the wire errors.
- **UI API does not support every object.** Coverage is broad for standard and custom objects but not universal, and the failure is a wire error at runtime, not a compile error. Check before designing around it.
- **Spanning fields go one level.** `Account.Owner.Name` is fine; `Account.Owner.Manager.Name` is not.
- **Wire results are immutable.** Copy before changing — mutating `data` throws in strict mode. → [05](05-decorators-and-the-reactivity-model.md)
- **`notifyRecordUpdateAvailable` does not return data.** It invalidates the cache entry and lets the subscriptions re-fetch; awaiting it does not mean the new value has arrived.
- **`lightning-record-form` cannot do custom layout, and switching to `record-edit-form` is not a small edit** — you take on every field, the submit button and the toast.
- **Record-edit-form runs validation rules server-side only.** Client-side you get required-field checks; a validation rule failure comes back as an error on submit.
- **LDS enforces FLS, so a field the user cannot edit is silently read-only in a form** rather than erroring — which looks like a bug until you check the profile.

## Recall

Q: Why does an LDS-only component have no sharing decision to make?
A: UI API enforces the running user's object permissions, FLS and sharing rules server-side. You never wrote a query, so there is nothing to run in system mode by accident.

Q: What is the difference between `fields` and `optionalFields`?
A: A no-access field listed in `fields` errors the entire wire; in `optionalFields` it is silently dropped.

Q: Why import field references from `@salesforce/schema` instead of using strings?
A: The import is compile-checked and creates a metadata dependency, so the field cannot be deleted while the component uses it.

Q: What can LDS not do that pushes you to GraphQL or Apex?
A: Arbitrary filtering, sorting, aggregation and multi-level relationship traversal. LDS addresses records by ID with one-hop spanning fields.

Q: Which client-side operations can only be done through LDS at 67.0?
A: Create, update and delete — the GraphQL wire adapter still has no mutation support.

## Related

- [08 · Apex in LWC — wire vs imperative](08-apex-in-lwc-wire-vs-imperative.md) — what to do when the data does not fit the record shape
- [07 · GraphQL wire adapter](07-graphql-wire-adapter.md) — filtering, sorting and aggregation without Apex
- [05 · Decorators & the reactivity model](05-decorators-and-the-reactivity-model.md) — `$` reactivity, and the state managers that wrap these adapters
