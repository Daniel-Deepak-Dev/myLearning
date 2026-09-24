---
vault: SF_Sales
format: light
level: basic
status: open
gaps: 3
org_checks: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Opportunities, Sales Process & Path

**One line:** An Opportunity is a deal in flight. Its Stage sets probability, forecast category and won/lost, and Path coaches reps through the stages.

**Reach for it when:** you design the stages a deal moves through, split them by business line, or need to explain why a pipeline number moved.

## Key points

- **Stage (`StageName`) drives the deal's other fields.** Each Stage value carries a Probability, a Forecast Category and a Type of Closed/Won, Closed/Lost or open. Changing Stage resets `Probability`, `ForecastCategoryName`, `IsClosed` and `IsWon` from that mapping.
- **Stage values live on the field:** Object Manager → Opportunity → Fields & Relationships → **Stage**, up to 100 values of 40 characters each. Code reads the mapping from `OpportunityStage` (`DefaultProbability`, `IsClosed`, `IsWon`), which is read-only via the API.
- **Overrides are allowed, within limits.** Users with edit access can override `Probability`, and owners can override Forecast Category — in Lightning every category is offered for every stage. `IsClosed` and `IsWon` change only through Stage.
- **A sales process** is the Opportunity business process: a named subset of Stage values (Setup → **Sales Processes**). It is assigned to an opportunity record type, and the record type decides which profiles use it.
- **Path** (Setup → **Path Settings** → Enable) is built once per object, record type and picklist. Each step shows up to five **key fields** and up to 1,000 characters of **Guidance for Success**, and confetti fires on the values you pick at a frequency such as Always, Often or Sometimes.
- **Stage History** (`OpportunityHistory`) gets a row whenever Amount, Probability, Stage or Close Date changes. You can't choose the fields, rows are never auto-deleted, and other fields need field history tracking (`OpportunityFieldHistory`).
- **Historical Trending** (Setup → **Historical Trending**) snapshots opportunity fields for trend reports: five by default (Amount, Close Date, Forecast Category, Probability, Stage) plus up to three more. Turning on Pipeline Inspection enables it, copying 3 months plus the current one and keeping 12.
- **Contact roles:** `OpportunityContactRole` gives each contact a `Role`, and one row per opportunity is `IsPrimary`. `Opportunity.ContactId` (API 46.0) mirrors that primary and can't be updated — flip `IsPrimary` instead.
- **Close Date** is required and decides which forecast period a deal counts in. `PushCount` (API 53.0) counts how often it slipped by a calendar month, and `LastStageChangeDate` (API 52.0) dates the last stage move.

## Gotchas

- **Closing moves the Close Date.** Setting a Closed/Won stage on a deal with a future Close Date resets it to today in UTC, which can be a day off in your time zone. A past Close Date stays.
- **Stage overwrites Probability** on every change, even when `Probability` is read-only on the page layout.
- **`Amount` ignores you once products exist.** It becomes the sum of the line items, and an API update to it is dropped with no error while the rest of the call saves.
- **Two forecast category fields.** `ForecastCategoryName` holds the labels — Pipeline, Best Case, Commit, Closed, Omitted — while the read-only `ForecastCategory` enum calls Commit `Forecast`. Filter on the wrong one and Commit deals go missing.
- **A sales process is not access control.** Profiles govern who can create and edit with a business process, not who can read it, so keep sensitive words out of stage names and descriptions.
- **Path and reports disagree on time in stage.** Path rounds up and adds every visit to a stage; reports don't round and count only the first stay.
- **Path can't make fields required per step.** Use a validation rule on the stage instead — its message shows at page level even when set on a field.

## Gaps to close

- [ ] Can Setup require a primary contact role before an opportunity is saved or closed, and which setting does it?
- [ ] What happens to an opportunity's Stage when its record type changes to one whose sales process lacks that stage?
- [ ] Which report types show stage history and time in stage, and how long is Historical Trending data kept when Pipeline Inspection is off?

## Confirm in org

- 🚩 Does an Apex or API update to a Closed/Won stage also reset a future Close Date, or only the UI? — Anonymous Apex, then query `CloseDate`.
- 🚩 Does a new Developer Edition org ship with Path enabled and a sample opportunity path? — Setup → **Path Settings**.

## Hands-on

- [ ] **SLS-OPP-01** · 15 min · In Anonymous Apex, insert an opportunity with a Close Date next month, update `StageName` to `Closed Won`, then query `CloseDate`. **Proves:** whether the API path also resets a future Close Date to today (UTC) — record which way it goes. **Needs:** nothing.
- [ ] **SLS-OPP-02** · 20 min · Add a product to an opportunity, then set `Amount` to 1 in Anonymous Apex and query it again. **Proves:** the update succeeds but `Amount` keeps the line-item total — no error is raised. **Needs:** an active standard price book entry.
- [ ] **SLS-OPP-03** · 25 min · Create a four-stage sales process, a `New_Business` record type that uses it, and a Path with two key fields per step and confetti on Closed Won set to Always. **Proves:** the record type limits the Stage picklist and the Path to that process, and closing fires the confetti. **Needs:** nothing.
- [ ] **SLS-OPP-04** · 15 min · On one opportunity change Stage, then Amount, then Description; query `OpportunityHistory` and `OpportunityFieldHistory`. **Proves:** only the four fixed fields write stage-history rows — Description appears only if field history tracking is on for it. **Needs:** nothing.

## Related

- [Lead Management & Conversion](lead-management-and-conversion.md) — where most opportunities are born, with Close Date and Primary Campaign Source filled in
- [Products & Price Books](products-and-price-books.md) — the line items that take `Amount` away from the rep
- [Collaborative Forecasts](collaborative-forecasts.md) — what Forecast Category and Close Date feed into
- [Pipeline Inspection](pipeline-inspection.md) — the main consumer of Historical Trending and stage-change data
- [Campaigns & Campaign Influence](campaigns-and-campaign-influence.md) — why contact roles and closed stages decide which deals get campaign credit
- [SF_core · 01-admin · 04 Record types & picklist architecture](../SF_core/01-admin-and-declarative-platform/04-record-types-and-picklist-architecture.md) — how a record type ties a business process to profiles, and why the business process must exist first

## Sources

- [Sales Cloud Basics (PDF)](https://resources.docs.salesforce.com/262/latest/en-us/sfdc/pdf/sales_core.pdf) — Salesforce, Spring '26, last updated 31 March 2026 · read 2026-09-24 · Close Date *"set to the current date in Coordinated Universal Time (UTC)"* on Closed/Won; Stage *"up to 100 available values"*, 40 characters; *"The probability value is always updated by a change in the stage value, even if the Probability field is marked as read only"*; stage-to-category table and *"In Lightning Experience, all forecast categories are available for all stages"*; Path: supported objects, *"up to five key fields"*, *"up to 1,000 characters of guidance"*, confetti frequency, last step Closed/Won or Closed/Lost, stage durations in paths vs reports, page-level validation messages; Stage History *"Your admin can't choose which fields to track"* and *"isn't automatically deleted"*; Historical Trending five default fields *"for a total of 8"*, *"3 months of historical data plus the current month"*, *"stored for 12 months"*
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers, Winter '27, last updated 18 September 2026 · read 2026-09-24 · `StageName` updates `ForecastCategoryName`, `IsClosed`, `IsWon`, `Probability`; `IsClosed`/`IsWon` *"can only be set via StageName"*; `ForecastCategory` enum (`BestCase`, `Forecast`, `MostLikely`…); `Amount` update *"will be ignored"*; `ContactId` API 46.0; `PushCount` API 53.0; `LastStageChangeDate` API 52.0; `OpportunityStage` read-only; `OpportunityHistory` tracks *"Amount, Probability, Stage, or Close Date"*; `OpportunityContactRole.IsPrimary` *"Each Opportunity has only one primary contact"*
- [BusinessProcess](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_businessprocess.htm) — Metadata API Developer Guide · read 2026-09-24 · *"A sales, support, lead, or solution process is assigned to a record type"*; *"Don't use business processes as an access control mechanism"*
- [Create Multiple Business Processes](https://help.salesforce.com/s/articleView?language=en_US&id=platform.creating_multiple_business_processes.htm&type=5) — Salesforce Help · via search 2026-09-24 · Setup → Processes; copy values from an existing process or Master; add the process to a record type

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
