# Record IDs, External IDs & Upsert

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** How records are identified — inside Salesforce and from outside it — and the one DML operation that depends on the difference. The API mechanics of upsert are [06-integration · 04](../06-integration-and-apis/04-rest-api-fundamentals.md) and [07](../06-integration-and-apis/07-bulk-api-2.md); the key *design* is here.

## Core idea

A Salesforce Id is meaningful only inside the org that minted it. Sandboxes, other orgs and every external system have their own idea of what a record is called, so an integration that keys on Salesforce Ids has to store a mapping and keep it correct forever. An **external ID** removes that job: it is your key, held on the Salesforce record, and it lets a caller say *"the customer whose ERP number is 4471"* without ever having asked Salesforce what its Id is.

That property is what makes **upsert idempotent**, and idempotency is the whole reason integrations use it. Send the same upsert twice and you get one record, so a retry after a timeout is safe. Without an external ID, "insert if new, update if not" requires a query first, and the gap between the query and the write is a race.

## How it works

- **15 vs 18 characters.** The 15-char Id is **case-sensitive**; the 18-char form appends a 3-character checksum so it survives case-insensitive systems. Both address the same record and the API accepts either. Use `CASESAFEID()` in formulas.
- **The first 3 characters are the key prefix** and identify the object — `001` Account, `003` Contact, `006` Opportunity, `00Q` Lead, `500` Case. Useful for routing a polymorphic Id without a describe call.
- **Ids are never reused.** Deleting a record does not free its Id.
- **External IDs: 25 per object**, a ceiling **shared with `Unique` fields**, and a soft limit Support can raise. Allowed types are **Text, Number and Email** (plus Auto Number).
- **Marking a field External ID creates an index on it** as a side effect — one of only two self-service routes to a custom index → [08](08-indexes-and-query-selectivity.md).
- **Upsert matching is strictly counted.** 0 matches → insert. 1 match → update. **2 or more → the row fails** with a duplicate-value error; it does not pick one.
- **A relationship can be set by the parent's external ID in the same call**, which removes the "look up the parent's Id first" round trip from every loader.

## Gotchas

- **Excel and CSV tooling lowercase 15-char Ids** and silently collide records that differ only by case. Export 18-char, always.
- **Upsert with a blank external ID inserts.** Blanks never match each other, so a retried file with empty keys creates a fresh duplicate on every run — the exact failure upsert was chosen to prevent.
- **`Unique` and External ID share one allocation of 25.** An object already carrying unique fields has fewer external-ID slots than the number suggests.
- **`Unique` on text is case-insensitive by default**, so `ACME` and `acme` collide unless the case-sensitive variant is chosen — and that choice changes upsert matching too.
- **External IDs conflict with probabilistic Shield encryption.** Unique and external-ID fields need deterministic encryption, which is weaker → [07-security · 21](../07-security-and-sharing/21-shield-platform-encryption.md).
- **An external ID is only as unique as the source system.** Two source systems feeding one field will eventually collide, and the failure appears as unexplained upsert errors months later. Namespace the value or use one field per system.
- **Upsert still fires all automation.** It is not a bulk back door → [01-admin · 14](../01-admin-and-declarative-platform/14-order-of-execution-declarative-view.md).

## Recall

Q: Why is the 18-character Id form necessary if 15 characters already identifies the record?
A: The 15-character form is case-sensitive. The 18-character form adds a checksum so case-insensitive systems — Excel especially — cannot merge two distinct records.

Q: What does upsert do when the external ID matches two existing records?
A: The row fails with a duplicate-value error. It never chooses one of them.

Q: How many external ID fields can an object have, and what shares that limit?
A: 25, shared with `Unique` fields. It is a soft limit that Support can raise.

Q: What is the side effect of marking a field as an External ID?
A: Salesforce indexes it — one of the two self-service ways to get a custom index, the other being `Unique`.

Q: Why can a retried upsert file still create duplicates?
A: Rows whose external ID is blank never match anything, so every run inserts them again.

## Related

- [08 · Indexes & query selectivity](08-indexes-and-query-selectivity.md) — the index an external ID quietly creates
- [06-integration · 04 REST API fundamentals](../06-integration-and-apis/04-rest-api-fundamentals.md) — upsert as the integration primitive
- [06-integration · 23 Idempotency, retries & error handling](../06-integration-and-apis/23-idempotency-retries-and-error-handling.md) — why idempotence is the point
- [07-security · 21 Shield Platform Encryption](../07-security-and-sharing/21-shield-platform-encryption.md) — the encryption scheme external IDs force
