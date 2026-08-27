# Lab 03 — Ingestion API From Any Org

> Status: ⬜ not started · Date run: —

## Goal

Push records into Data 360 over REST, from an org with no connector at all. This is the universal fallback — and the most educational mechanism, because nothing is hidden: you see the payload, the primary key, the upsert behaviour and the raw error body.

## Prereqs

- [Lab 02](lab-02-external-org-connection.md) done.
- The same source org (or any third org). No Data 360 licence needed — again.
- Read [Justus van den Berg's write-up](https://medium.com/@justusvandenberg/building-a-data-cloud-ingestion-api-utility-on-the-salesforce-platform-0e754bea8385) first; the `lightweight-data-cloud-auth-provider` and `lightweight-data-cloud-util` packages it links save you an afternoon of JWT debugging.

## Steps

### In the DATA 360 org

1. **Ingestion API connector.** Data 360 Setup → Ingestion API → New. Name it.
2. **Upload the schema.** An **OpenAPI (OAS) YAML** file describing your object — say `LoyaltyEvent` with an `event_id` (primary key), `email`, `event_type`, `event_timestamp`. The schema defines the DLO; get the primary key right or the upsert semantics won't be what you expect.
3. **Note the tenant-specific endpoint** shown on the connector page. It is the only reliable source for your ingestion URLs — don't copy one from a blog post.
4. **Create a data stream** on that connector so the DLO actually materialises.

### In the SOURCE org

5. **Connected app + auth.** Set up the custom auth provider (JWT) and a **Named Credential** pointing at the tenant endpoint. This is the fiddly part; the packages above do it for you.
6. **Streaming push.** Apex callout with a small JSON payload — three records.
7. **Bulk push.** Create a job, upload CSV, close the job, watch it process.

## How you know it worked

- Streaming records appear in the DLO within seconds-to-minutes; query with `SET OPTIONS`.
- Bulk job reports complete, and the row count matches your CSV lines.
- Compare observed latency between the two and write the numbers down — that comparison is the answer to "should this be bulk or streaming?" in a real design.

## Break it on purpose

1. **Send the same streaming payload twice.** Same `event_id`. Does the DLO have one row or two? That's your upsert-on-primary-key proof, and it's the single most useful thing this lab teaches — retry safety in an integration depends on it.
2. **Send a payload with a field that isn't in the schema.** Record the error body verbatim.
3. **Send a malformed timestamp.** Note whether it fails the record, the batch, or silently nulls the field.

## Credits spent

—

## Notes from my run

—
