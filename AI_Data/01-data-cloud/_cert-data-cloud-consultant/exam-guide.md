# Salesforce Certified Data 360 Consultant — Exam Guide Breakdown

> **Renamed.** This was the *Data Cloud Consultant*. It became the **Data 360 Consultant** on **2026-03-27**; the exam code **`Data-Con-101` is unchanged** and no retake is required. The folder is still `_cert-data-cloud-consultant/` so existing links keep working.

- Covers: ingestion, modeling (DSO/DLO/DMO), identity resolution, calculated insights, segmentation, activation.
- Roadmap milestone: end of Phase 02 (week 8).
- Official exam guide: https://trailhead.salesforce.com/credentials/datacloudconsultant

## Retirement check — not affected

**24 certifications retire on February 1, 2027.** Registration for those closed **July 24, 2026** and the last sitting is **August 31, 2026**. **Data 360 Consultant is not among them** — so there's no deadline pressure on this milestone. Re-confirm against Salesforce's Certification Name Changes FAQ before booking, since the list is Salesforce's to change.

## Domains & weights
<!-- copy from the official exam guide, then link each domain to your topic folders -->

| Domain | Weight | Study folder |
|---|---|---|
| _(fill from the official guide)_ | | [01-orientation](../01-orientation/notes.md) |
| | | [02-ingestion](../02-ingestion/notes.md) |
| | | [03-data-modeling-dso-dlo-dmo](../03-data-modeling-dso-dlo-dmo/notes.md) |
| | | [04-identity-resolution](../04-identity-resolution/notes.md) |
| | | [05-insights-segmentation](../05-insights-segmentation/notes.md) |
| | | [06-zero-copy-byol](../06-zero-copy-byol/notes.md) |
| | | [07-vector-db-unstructured](../07-vector-db-unstructured/notes.md) |
| | | [08-rag-on-platform](../08-rag-on-platform/notes.md) |
| | | [09-data-360-devops](../09-data-360-devops/notes.md) |

## Vocabulary warning

The exam and current release notes use **Data 360**. Trailhead modules, most blog content and a lot of official documentation still say **Data Cloud**. Both refer to the same product — don't let the inconsistency make you doubt an answer.

Also expect all six historical names in the wild: Customer 360 Audiences → Salesforce CDP → Marketing Cloud CDP → Genie → Data Cloud → Data 360.

## Summer '26 material likely to appear

Newer than most study material, so worth deliberate attention:

- **`SET OPTIONS`** — dataspace required for DLO queries (omit it → zero records, silently); `honorEmptyStrings`
- **Accelerated Data Ingest** — **GA**; real-time CRM data
- **Federation status** — AWS Glue **GA**, Microsoft Fabric OneLake **Beta**
- **Code Extension** — Python, custom chunking, author ≠ operator permission split
- **Data kits** — promoting code extensions and transforms between orgs
- **Profile-based pricing** (March 2, 2026) — ~$240 per 1,000 unified profiles; makes match quality a cost lever
- **Semantic layer / Tableau Semantics**, and **OSI** (core spec finalized February 2026)

## Registration / logistics
<!-- exam date booked, delivery method, cost, retake policy -->

## Prep loop

1. Read the official guide, fill the domain table above, and map each domain to its folder.
2. Work the folders in numbered order — they follow the ingest → model → unify → insight → activate flow.
3. Mock exam → log every miss in [practice-questions.md](practice-questions.md) **with the reason**, not just the answer.
4. Update [weak-areas.md](weak-areas.md) after each mock.
5. Check the [Data 360 monthly release notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_c360_truth.htm&release=262&type=5) weekly — Data 360 ships monthly, not seasonally, so material can move between now and your exam date.
