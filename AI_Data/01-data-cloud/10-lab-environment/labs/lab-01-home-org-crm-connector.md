# Lab 01 — Home Org Connector

> Status: ⬜ not started · Date run: —

## Goal

Ingest CRM data from the org the tenant lives in, map it to a DMO, and verify the row count three independent ways. This is the shortest possible path through **ingest → model** with no authentication in the way, which is exactly why it goes first: when lab-02 breaks, you'll know it's the connection and not the concept.

## Prereqs

- [Lab 00](lab-00-tenant-baseline.md) done, default data space name written down.
- 20–50 Contacts in the home org. Invent them; you need to know the right answer in advance.

## Steps

1. **Count the source.** In the home org, run `SELECT COUNT() FROM Contact` (Developer Console or `sf data query`). Write the number down *now*, before anything else.
2. **New data stream.** Data 360 Setup → Data Streams → New → **Salesforce CRM**. The home org connection already exists — no OAuth, no setup. Pick `Contact`.
3. **Fields.** Select a handful, deliberately: an ID, `Email`, `FirstName`, `LastName`, and one field you'll *leave out* — you'll want it in the "break it" step.
4. **Category.** Set it to **Profile**. Category drives what the DMO can be used for downstream (identity resolution needs Profile); getting it wrong here is a rebuild, not an edit.
5. **Deploy and run.** Watch the refresh history until it reports a status *and a row count*.
6. **Map to a DMO.** Map the new DLO to the standard **Individual** DMO. Map email and name; leave one source field unmapped on purpose.
7. **Query the DLO.** Query Workspace:
   ```sql
   SELECT COUNT(*) FROM Contact_Home__dll
   SET OPTIONS (dataspace = '<your default space>')
   ```
8. **Query the DMO.** Same count against the mapped DMO.

## How you know it worked

Three numbers agree: source `COUNT()`, stream row count, DLO `COUNT(*)`. If the DMO count differs from the DLO count, mapping is the reason — go find it.

Then check the field you left unmapped: it returns **null**, not an error. Sit with that for a second. In a client org, that null looks exactly like missing data, and nobody gets an alert.

## Break it on purpose

1. **Drop the `SET OPTIONS` clause** and re-run the DLO query. Zero rows, no error, no warning. This is the single most expensive gotcha in the track — see [data modeling](../../03-data-modeling-dso-dlo-dmo/notes.md).
2. **Query a data space you don't have** — same silence.

Write down what the output looked like. That blank result set is what you'll be staring at in six months wondering why a client's DLO is "empty".

## Credits spent

—

## Notes from my run

—
