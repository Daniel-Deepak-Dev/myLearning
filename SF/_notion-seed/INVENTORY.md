# Notion seed inventory

The old notes, mapped to where they land in `SF/`. Captured **2026-08-01**.

## What this is for

Phases use this two ways: to sanity-check that the taxonomy covers what you actually studied, and to harvest genuine hard-won gotchas into `> **From my notes.**` callouts. It is **not** a migration list — the substance gets authored fresh against API 67.0.

## Honest assessment of the source

Sampled 8 pages in depth. **3 substantive, 2 thin fragments, 3 pure stubs.** Total prose across all 8 ≈ 900 words. Most were written 2019–2021 and **not one references an API version.**

Three specific hazards:

- **Inline-database embeds don't export.** `Trigger Basics`, `Trigger Context Variable` and `Future vs Queueable` consist of *nothing but* an embedded table. Via the API they return an empty tag. The comparison matrix that is the entire value of those notes is invisible — it must be read in the Notion UI or rebuilt from scratch.
- **`evernote:///` deep links** appear on at least 2 pages. Permanently dead — they point into a legacy Evernote account.
- **At least one factual contradiction.** `Group By` states "COUNT() cannot be used with GROUP BY — use COUNT(Id)" and then shows `select count() from case group by status` with no label marking it as the counter-example. Do not reuse verbatim.

## Where the notes actually live

The URL originally supplied (`862649e799ed4c039c10a924cb19f2a4`) is an **empty "Company Home" wiki** — a Notion template that was never used. The real content is in sibling databases under:

**📘 Salesforce KB** — https://app.notion.com/p/33d9685ffed381efac0ac0492e397673

| Database | URL | Rows | Status |
|---|---|---|---|
| SF Knowledge Base | `ba9bd2a103f948a09e2b7b61249e0b17` | 100+ | ⚠️ **truncated** — see below |
| Apex && Triggers | `cdf16496c53243a3bdd2286d5a55f940` | 24 | ✅ captured |
| SOQL & SOSL | `6a3aa50adaa446479ac2a59f8bd253c9` | 6 | ✅ captured |
| Flow (untitled) | `0676b9320ba94500a042985f1dd98518` | 2 | ✅ captured |
| Apex Callouts | `1f2f00dca72141f280959d9cbcf890d2` | 4 | ✅ captured |
| Experience Cloud / "Community Builder" | `1289f9d770f448f5adab21a3eafb1478` | 1 | ✅ captured |
| untitled | `6c632b98ff044dce9335881f9f7f8a22` | 2 | ✅ captured (both rows have no title) |
| Omnistudio | `3059685ffed3801ebc1de14820e74937` | 0 | ✅ empty — content is in SF Knowledge Base |
| untitled | `93a8d046ffff46e8986a80dc8e73acdd` | 0 | ✅ empty |
| Trigger | `54dd1432dd8843b484d92e073c1043ce` | ? | ❌ **TODO: re-query** |
| untitled | `cf820ea785374ae5b9b0dcb287a01003` | ? | ❌ **TODO: re-query** |
| VisualForce | `6348d3ebcbd9413aa6555a6ab5950fd9` | ? | ⛔ out of scope — VF excluded |

### Open items

1. **`SF Knowledge Base` is truncated at 100 rows.** Sorted by page ID, the capture stops at `8138b072…` — roughly halfway through the ID space, so expect **~180–200 rows total**. Roughly half the KB is unseen.
2. **Two databases un-enumerated** (`Trigger`, `cf820ea7…`).

Both are because the workspace **hit its Notion `query_data_sources` usage limit** on 2026-08-01. Re-run when the quota resets:

```
notion-query-data-sources → SELECT * FROM "collection://<id>" LIMIT 100
```

Neither blocks any phase. This inventory informs gotcha-harvesting and ordering, not the taxonomy.

---

## Mapping — Apex && Triggers → area 02

| Notion page | Target | Value |
|---|---|---|
| Trigger Basics | `06-triggers-and-the-handler-framework` | ⛔ stub — empty embed + dead Evernote link |
| Trigger Context Variable | `06-triggers-and-the-handler-framework` | ⛔ stub — the matrix is an unexported embed |
| Control Recursive Trigger | `07-order-of-execution-and-recursion` | ✅ usable |
| Steps to create handler using trigger factory | `06-triggers-and-the-handler-framework` | ⚠️ substantive but the pattern is ~2013-era `ITrigger`/`TriggerFactory`. Keep the "Manthras" (SOQL in bulk phases, DML only in `andFinally()`); **do not present the pattern as current** |
| Prevent Deleting if Parent has Child Record | `06-triggers-and-the-handler-framework` | ✅ `addError` pattern |
| Future Method / Future vs Queueable | `13-queueable-apex-and-chaining` | ⛔ comparison is an unexported embed |
| Batch For Loop - maintains heap size | `14-batch-apex-and-stateful-processing` | ✅ **best gotcha in the corpus** — measured heap 1050→20000 vs 1050→1200 for 450 records. Harvest verbatim |
| Continuation | `19-callouts-named-credentials-and-http-in-apex` | — |
| Mixed DML Exception | `05-dml-database-methods-and-savepoints` | ✅ usable |
| Upsert : DML Operation | `05-dml-database-methods-and-savepoints` | ✅ |
| Test Annotations | `20-apex-testing-fundamentals` | ✅ **richest page (~450 words).** `SeeAllData` + `@TestSetup` conflict, "DML limits reset by testSetup but not SOQL limits". Note only 4 of its 12 agenda items were ever written |
| Test class consideration / LinkedIn test-pattern link | `21-apex-testing-advanced-and-mocking` | ⚠️ link-only |
| Data Types / Data type - Object | `01-apex-language-core-and-governor-limits` | ✅ thin |
| Interface / Abstract Class | `01-apex-language-core-and-governor-limits` | ✅ thin |
| Apex Properties | ⛔ VF-flavoured (`get;set;` for VF) — skip |
| TIPS!: Get Picklist Value / Get Dependent Picklist Values | `04-advanced-soql-sosl-and-dynamic-queries` | ✅ schema-describe recipes |
| Utils | — | unclassifiable |

## Mapping — SOQL & SOSL → area 02

| Notion page | Target | Value |
|---|---|---|
| Alias Notation : SOQL | `03-soql-fundamentals-and-relationship-queries` | ✅ |
| Group By | `03-soql-fundamentals-and-relationship-queries` | ⚠️ **contains a contradiction — verify before reuse** |
| Group By Rollup / Aggregate Functions + Group By Rollup | `03-soql-fundamentals-and-relationship-queries` | ✅ |
| Date functions | `03-soql-fundamentals-and-relationship-queries` | ✅ |

## Mapping — Apex Callouts → area 06

| Notion page | Target |
|---|---|
| Bulk API | `07-bulk-api-2` — ⚠️ **confirmed v1-era in phase 12**: batch splitting, the 10,000-record batch ceiling and `Sforce-Enable-PKChunking`, all three v1 mechanics, corrected inline. Its durable lesson survives — **lock contention, not row count, makes a large load slow** |
| Platform Event / Salesforce Events | `12-platform-event-design` — thin; harvested as one line, that **an event is a published contract** |
| IN | ⛔ **inspected in phase 12: it is SOQL, not REST.** Belongs with the area-02 `IN`/semi-join cluster already covered in phase 03. Not an area-06 page |

## Mapping — Flow DB → area 04

| Notion page | Target |
|---|---|
| Apex Invocable method in Flow | `11-flow-and-apex-interop` — 4 correct bullets; the teaching content is in an embedded YouTube video |
| Sub Flow | `08-subflows-and-modular-flow-design` — ⛔ **confirmed structure-only in phase 08**: a single YouTube embed, no prose |

## Mapping — SF Knowledge Base (100 of ~190 captured)

Grouped by destination. Dates are creation dates — anything 2019–2021 needs full rewrite, 2025–2026 pages may hold current material worth reading first.

**→ 02 Apex & Triggers**
`Index of Apex Programming` (2020) · `Apex Best Practices` (2021) · `Future Methods a.k.a @future` (2019) · `@Future vs queueable apex` (2023) · `Batch apex` (2020) · `Savepoint and Rollback in Apex` (**2025**) · `Trigger Best Practices` (**2025**) · `Trigger Scenarios:` (2022) · `Wrapper Class` (2019) · `Database.SaveResult` (2019) · `Concurrency` (2022) · `Can We Perform Callout After DML Operation?` (2023) · `Apex Managed Sharing` (2023) · `WITH SECURITY_ENFORCED` (2021) — ⚠️ **this one is now actively wrong; it no longer compiles at 67.0** · `Apex Continuations…Aura & LWC` (2020) — strip the Aura half

**→ 02 Apex, SOQL half**
`SOQL basics` (2019) · `SOQL - PTR` (2019) · `SF Query cheatsheet` (2021) · `SOQL Relationship query - Notes` (2021) · `Relationship Query` (2021) · `Aggregate Query & Functions` (2021) · `Semi-Joins with IN & Anti-Joins with NOT IN` (2019) · `IN - SOQL,SOSL` (2021) · `IN` ×3 (2021/2023 — likely duplicates) · `OFFSET` (2021) · `FOR UPDATE` (2021) · `FIELDS(): ALL/CUSTOM/STANDARD` (2021) · `QUERY PLAN` (**2025**) → also `08-data`/`07-query-plan-and-performance-tuning`

**→ 03 LWC & SLDS**
`INDEX OF LWC` (2020) · `LWC Preparation` (2021) · `Interview LWC` (2023) · `LWC Scenarios` / `LWC Scenarios - Entry level` (2023) · `Events - LWC` (2020) · `dispatchEvent (CustomEvent)` (2020) · `addEventListener - LWC` (2020) · `LWC drag and drop Events` (2023) · `Wire Methods` (2020) · `Cache issue : refreshApex…imperative method` (2020) — ✅ real gotcha · `LWC : Query DOM Elements` (2023) · `LWC - Quick Action` (2022) · `LWC metadata api file` (2019) · `@Salesforce Modules` / `@salesforce modules or Importing SF values` (2020) · `Facet (== Slot in LWC)` (2021) · `Navigate to a Record's Create Page with Default Field Values` (2022) · `Local Dev` (2024) → `21-local-dev-and-lightning-dev-server`
⛔ **skip:** `Communication Between Aura and LWC`, `LWC vs Aura and VF`, `VF + SLDS`, all `<apex:*/>` pages

**→ 04 Flow**
`Flow Builder` (2023) — ⚠️ a 16-item agenda with **one box ticked**; an artefact, not a note · `Flow Invocable Methods and Variable` (**2025**) — ✅ one real gotcha, `Map<>` unsupported as an `@InvocableVariable`
`Flow Updates` (**2025**) → **`21-flow-for-external-and-guest-users`**, ✅ harvested in phase 09. **The title is misleading and this row previously guessed wrong** — it is not about flow releases at all, it is a **profile-by-profile audit of the `Run Flows` permission** in a production org
**Found in phase 08, absent from the original capture:** `Call Flow in Apex` (2023) → `11-flow-and-apex-interop`, ✅ usable — `Flow.Interview` both forms, and the restriction to autolaunched/user-provisioning flows · `Limits based Things` (**2025**) → `13-flow-limits-and-bulkification`, ✅ harvested in phase 09 — CPU 10 s / 60 s and heap 6 MB / 12 MB still correct, but its "convert flows to Apex Triggers" advice is stale and is corrected inline

**→ 05 Experience Cloud**
`Exp Cloud Certification Prep` (2022) · `VFpage Grey Background Problem in Community` — ⛔ VF, skip

**→ 06 Integration & APIs**
`SOAP API` (2019) → **05**, ✅ structure only as predicted — enterprise/partner split and header model hold; its example authenticates with `login()` and presents SOAP as the default for new work · `SF - Integration Patterns and Practices` (**2026-02**) → **01**, ✅ **read first in phase 12 and it earned the billing** — taxonomy matched what was written; one stale line naming outbound messaging as a first-choice fire-and-forget mechanism, corrected inline · `Apex REST Callouts` (2021) + `Apex Rest Web Services` (2021) → **18**, ✅ **confirmed structure-only in phase 13** — annotations and a worked example, no prose. Two things they predate: the **user-mode default at 67.0** inverts their implicit system-mode assumption, and a published endpoint is now a candidate **agent action**. Harvested as one callout · `Change data capture` (2023) + `lightning/empApi - Change Data Capture` (2023) → **13**, ✅ both still structurally correct; one thing added rather than corrected — `empApi` is how you subscribe **inside a component**, not how an external system should · `CometD` (**2025**) → **14**, ✅ harvested — long-polling mechanics still correct, and it became the ⚠️ hook **in the opposite direction to the one the plan expected**: ⚠️ **not** retired in favour of Pub/Sub API, which is *recommended*, not a replacement · `Salesforce Edge Network` (2023) → **03**, ✅ *previously unrouted, now has a home* — treats Edge purely as a latency switch, still true and now incomplete since hostname choice became a supportability question

**→ 07 Security & Sharing**
`Sharing and Visibility Architect` (2023) · `Salesforce Certified Sharing and Visibility Architect` (**2025**) · `UserRecordAccess Query Problem` (**2025**) — ✅ real gotcha · `Transaction Security Policies` (**2025**)

**→ 08 Data modeling & LDV**
`QUERY PLAN` (**2025**) · `Optimization work` (2023) · `Lead Broker Field Migration` (2023)

**→ 09 DevOps & SFDX**
`Package.XML` (2019) · `Important commands` (**2025**) — ⚠️ check for `sfdx force:` syntax, retired · `Salesforce force VSC and Chrome extensions` (2019) · `Local Dev` (2024)

**→ ../AI_Data/ (not this vault)**
`Agentforce` (2024) · `Einstein GPT` (2023) · `Data Cloud` (2024) · `Data Cloud Prep` (2024) · `SF AI Org details` (2025)

**→ out of scope for this build**
OmniStudio set: `Vlocity`, `1. Omnistudio`, `2. Flexcards`, `3. Omniscript`, `0. Omnistudio Questions`, `OmniStudio Prep (Delete)`, `Apex Remote - (Make Apex method available to Omnistudio)` — all **2026-02**, the most recently written cluster in the KB. Strong argument for adding area 10 later.

**→ personal / not knowledge**
`My skills` · `SF Todo` · `SF - Todos Learning` · `Questions` · `Terminologies` · `Sources and Agenda` · `Navatar` · `Interview Questions` · `NSW interview questions` · `GeekSoft - Solarix Consulting Interview questions` · `Salesforce Developer Career Roadmap 2026`

---

## What the mapping reveals

Two structural gaps worth knowing before phase 01:

1. **Coverage is lopsided toward 2019–2021 Apex and SOQL.** Areas 01 (Admin), 05 (Experience Cloud), 08 (Data/LDV) and 09 (DevOps) have almost no legacy notes behind them — those phases are near-total greenfield.
2. **The newest cluster is OmniStudio (2026-02), which this build excludes.** If that reflects current work, area 10 is worth adding.
