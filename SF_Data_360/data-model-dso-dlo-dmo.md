---
vault: SF_Data_360
format: light
level: basic
status: open
gaps: 2
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Data Model: DSO, DLO & DMO

**One line:** Data moves from a raw **data source object** (DSO) to a stored **data lake object** (DLO), then is mapped into a standard **data model object** (DMO) that every other feature reads.

**Reach for it when:** you are mapping a new source, or two answers about the same customer disagree.

## Key points

| Stage | What it is | Shape |
|---|---|---|
| **DSO** | The data as it arrives from the source | the source's |
| **DLO** | The stored container in the lake, created by a data stream | still the source's |
| **DMO** | A harmonized object that DLOs are mapped into; standard or custom | Salesforce's canonical model |

- **Harmonization is the DLO → DMO mapping.** "Email" from five systems becomes one attribute on one DMO.
- **Everything downstream reads DMOs.** Identity resolution matches on DMO fields. Insights compute over them, segments filter them, and agents ground on them. A mapping mistake spreads into every one of those.
- **Prefer standard DMOs.** Cross-source consistency is the point, and standard DMOs carry downstream behaviour. A custom DMO per source rebuilds the silos.
- **A data space is a logical partition** for profile unification, insights and marketing. Every org starts with a **default data space**, which can't be deleted. DLOs are associated with a data space, with or without filters.
- **API names carry a suffix.** A DLO is queried as `Name__dll`. Standard DMOs use the `ssot__` prefix, and standard DMOs added after January 2026 end in `_std__dlm`.
- **Querying a DLO with SOQL needs `SET OPTIONS (dataspace = …)`** at the very end of the query. The dataspace option is valid **only for DLO queries**, not DMO queries.
- **`honorEmptyStrings`** controls `NULL` vs `''`. DLOs store them as different values; the default (`false`) treats them as the same, like Platform objects.

## Gotchas

- **No dataspace on a DLO query returns zero rows, with no error.** The afternoon goes on the `WHERE` clause.
- **Field data types on DLOs and DMOs can't be changed** once created. Decide them while mapping.
- **A data space is not access control for teams.** Use it for boundaries that must never be crossed (legal entities, residency). For "team A sees less", use permission sets.
- **`NULL` vs `''` is a silent matching risk.** An upstream change from nullable to empty-string-defaulted alters what match rules see.

## Gaps to close

- [ ] Re-read Data Objects in Data 360, About Data Spaces and `SET OPTIONS` in full once help.salesforce.com is reachable. This note was built from search extracts.
- [ ] What exactly does a DMO "physical or virtual view" mean for query cost and freshness?

## Hands-on

- [ ] **D360-MODEL-01** · 20 min · Map a Contact DLO to the standard Individual and Contact Point Email DMOs, then compare DMO row counts with `COUNT()` in the source org. **Proves:** mapping is where rows become model; an unmapped field reads as null, not as an error.
- [ ] **D360-MODEL-02** · 15 min · Query a DLO with SOQL without `SET OPTIONS`, then with the dataspace. **Proves:** the missing dataspace returns zero rows silently.
- [ ] **D360-MODEL-03** · 15 min · Load rows holding both `NULL` and `''`, then filter with `honorEmptyStrings` true and false. **Proves:** the default collapses the two; the row counts differ.

## Related

- [Ingestion & Data Streams](ingestion-and-data-streams.md) — how rows reach the DLO
- [Identity Resolution](identity-resolution.md) — the first consumer of the DMO mapping
- [Calculated Insights & Segmentation](calculated-insights-and-segmentation.md) — computed over DMOs
- [SF_core · 08-data · 19 Data quality, deduplication & MDM](../SF_core/08-data-modeling-and-large-data-volumes/19-data-quality-deduplication-and-mdm.md) — CRM-side dedup, which Data 360 does not replace
- [RELEASE-RADAR · Data 360](../RELEASE-RADAR/data-360.md) — the `SET OPTIONS` and `sfsqlquery` entries

## Sources

- [Data Objects in Data 360](https://help.salesforce.com/s/articleView?id=sf.c360_a_data_lake_objects.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · *"A data lake object (DLO) is a container for the data brought into Data 360"*
- [Model Data in Data 360](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-model-data.html) — Salesforce Developers · via search 2026-10-02 · DLOs map into standard or custom DMOs
- [Data 360: Data Type of Data Lake Object and Data Model Object Fields Cannot be Changed](https://help.salesforce.com/s/articleView?id=001233477&language=en_US&type=1) — Salesforce Help · via search 2026-10-02
- [SET OPTIONS](https://developer.salesforce.com/docs/platform/salesforce-soql-sosl/guide/sforce-api-calls-soql-select-set-options.html) — Salesforce Developers · via search 2026-10-02 · zero records without a dataspace; DLO-only; `honorEmptyStrings`
- [Data Lake Object Naming Standards](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_data_lake_object_naming.htm&type=5) — Salesforce Help · via search 2026-10-02 · `__dll` appended to the DLO API name
- [SSOT DMOs](https://developer.salesforce.com/docs/data/data-cloud-dmo-mapping/guide/c360dm-datamodelobjects.html) — Salesforce Developers · via search 2026-10-02 · `ssot__` prefix; `_std__dlm` for standard DMOs added after January 2026
- [About Data Spaces](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_data_spaces.htm&type=5) — Salesforce Help · via search 2026-10-02 · logical partition; default data space can't be deleted

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts
