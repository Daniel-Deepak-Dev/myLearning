# Data Import, Export & Loading Tools

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01

**Scope:** Choosing and operating the declarative and desktop data-movement tools. Bulk API mechanics as an *integration* surface are [06-integration](../06-integration-and-apis/INDEX.md).

> **What changed.** The old instruction "tick *Use Bulk API* for large loads" is now ambiguous and usually wrong. Data Loader offers **two** separate Bulk options and **still defaults to the SOAP-based API** — Bulk API 2.0 is opt-in, and it is the one to choose.

## Core idea

Three tools, chosen by scale and by who is driving. The browser **Data Import Wizard** handles small admin-scale loads on a handful of objects with built-in duplicate matching. **Data Loader** is the desktop workhorse: every object, every operation, millions of rows, and a command-line mode for scheduling. The **`sf` CLI bulk commands** are the scripted, pipeline-friendly path and use Bulk API 2.0 throughout. Whichever you pick, the platform does not care that the write came from a loader — validation rules, triggers, flows and duplicate rules all fire exactly as they would for a user.

## How it works

| | Import Wizard | Data Loader | `sf data … bulk` |
|---|---|---|---|
| Runs in | browser | desktop app / CLI | terminal |
| Ceiling | 50,000 records | ~5 million rows | Bulk API 2.0 limits |
| Objects | a limited set + custom | all | all |
| Delete / hard delete | no | yes | via Bulk API 2.0 |
| Duplicate matching | built in | no | no |

- **Data Loader's API choice lives in Settings** — *Use Bulk API* (the legacy v1) and *Use Bulk API 2.0* are separate checkboxes. Neither is on by default; unticked means SOAP.
- **Enabling a Bulk path changes two behaviours:** *Insert null values* becomes unavailable — empty fields are simply ignored, and you must send `#N/A` to null a field — and *Allow field truncation* stops working, so an oversized value **fails the row** instead of being trimmed.
- **Hard delete** requires a Bulk path plus the *Bulk API Hard Delete* permission, and bypasses the Recycle Bin entirely.
- **Upsert** keys on a field marked **External ID**; make it Unique too, or an ambiguous match fails the row.
- **`sf data import bulk`**, `sf data update bulk`, `sf data export bulk` and `sf data bulk results` all run on Bulk API 2.0, with `… resume` variants for long jobs.
- **Export** is Data Loader's *Export* (respects soft-deleted exclusion) versus *Export All* (includes them), or the org's scheduled **Data Export** service for a full backup.

## 2026 currency

Legacy Salesforce Platform API versions **21.0–30.0 were deprecated in Summer '22 and retired in Summer '25**, so an old Data Loader build can stop working outright rather than degrade. Bulk API 2.0 is where Salesforce puts new capability; v1 persists only for compatibility and shows up as **Bulk V1** jobs under Setup → Bulk Data Load Jobs, which is the way to audit who is still on it.

## Gotchas

- **The default is SOAP.** Teams routinely believe they are loading via Bulk and are not — verify in the Settings dialog, then confirm the job appears under Bulk Data Load Jobs.
- Blanks in your CSV do **not** clear fields on a Bulk load. They are ignored; `#N/A` is the explicit null.
- Bulk API 2.0 chunks server-side, so the Data Loader batch-size setting no longer does what v1-era guidance says it does.
- Validation rules and required fields fire per row, so a 50,000-row load can half-succeed. Always keep the error file.
- Assignment rules do **not** run on a load unless the assignment-rule setting is enabled — see [11 · Queues, assignment & escalation](11-queues-assignment-and-escalation-rules.md).
- Hard delete is irreversible: no Recycle Bin, no undo, and it is a separate permission for exactly that reason.
- Loading child records grouped by the same parent ID creates lock contention and ownership skew at volume — see [08-data](../08-data-modeling-and-large-data-volumes/INDEX.md).
- Data Loader CLI mode stores credentials in an encrypted key file; treat that file as a secret in any scheduled setup.

## Recall

Q: Which API does Data Loader use if you change nothing?
A: The SOAP-based API. Both *Use Bulk API* and *Use Bulk API 2.0* are opt-in checkboxes in Settings.

Q: How do you null out a field on a Bulk API load?
A: Send `#N/A`. Empty values are ignored on Bulk paths because *Insert null values* is unavailable there.

Q: What two Data Loader behaviours change once a Bulk path is enabled?
A: *Insert null values* and *Allow field truncation* both stop working — oversized values fail the row rather than being trimmed.

Q: What does Data Loader's upsert operation match on?
A: A field marked External ID, which should also be Unique to avoid ambiguous-match row failures.

Q: How do you find out whether anything in the org still uses the legacy Bulk API?
A: Setup → Bulk Data Load Jobs, and look for jobs labelled **Bulk V1**.

## Related

- [08 · Validation rules & duplicate management](08-validation-rules-and-duplicate-management.md) — what rejects your rows mid-load
- [14 · Order of execution](14-order-of-execution-declarative-view.md) — everything a loaded record still triggers
- [06-integration · INDEX](../06-integration-and-apis/INDEX.md) — Bulk API 2.0 as a programmatic integration surface
