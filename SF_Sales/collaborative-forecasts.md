---
vault: SF_Sales
format: light
level: working
status: open
gaps: 2
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Collaborative Forecasts

**One line:** Opportunities rolled up by forecast category, period and hierarchy, with adjustments and quotas on top. Help now calls it **Pipeline Forecasting**.

**Reach for it when:** leaders need a committed number per rep, team and period, built from opportunities rather than a spreadsheet.

## Key points

| Forecast on | Measure | Hierarchy | Needs |
|---|---|---|---|
| **Opportunity** | Amount, Quantity, custom currency or number field | role or territory | nothing — the default type (Amount · Close Date · role) |
| **Opportunity Product** | Total Price, Quantity, custom field; groups by product family or picklist | role or territory | products on opportunities |
| **Opportunity Split** | split Amount (revenue, overlay, custom split types), custom currency | role or territory | team selling and splits |
| **Opportunity Product Split** | split Amount, custom currency — product family only | role only | team selling and product splits |
| **Line Item Schedule** | Revenue, Quantity, custom field; by schedule date | role or territory | product schedules |

- **Pipeline Forecasting since Spring '25**; the older Customizable Forecasting retired in Summer '20. Orgs created in Winter '24 or later have it on with the default type; older orgs enable it at Setup → **Forecasts Settings**. Up to **four** types can be active at once — more needs Salesforce Support.
- **Forecast category comes from Stage.** Each Stage value maps to Pipeline, Best Case, Commit, Closed or Omitted (left out) at Object Manager → Opportunity → Fields → Stage. **Most Likely** is an optional extra in Lightning.
- **Cumulative rollups** (the default) show Open Pipeline, Best Case Forecast, Commit Forecast and Closed Only; each column adds the categories nearer to Closed. **Single category** rollups keep each category apart.
- **The role-based hierarchy** is generated from the role hierarchy. Each user needs **Allow Forecasting** (User record, or Setup → **Forecasts Hierarchy** → Enable Users), and each manager role needs one **Forecast Manager** (Edit Manager).
- **Territory-based types** follow the active territory model, with managers set in the territory hierarchy. Each opportunity rolls up to one territory only.
- **Adjustments** add a judgment; the gross rollup is unchanged. Managers adjust direct reports (`ForecastingAdjustment`), owners adjust themselves (`ForecastingOwnerAdjustment`); both need **Override Forecasts**, and neither crosses forecast types.
- **Quotas** live in `ForecastingQuota` (`QuotaAmount` or `QuotaQuantity`, `QuotaOwnerId`, `StartDate`, `ForecastingTypeId`). Enter them at Setup → **Forecasts Quotas** or load them by API; editing needs **Manage Quotas**.
- **The grid is read-only rows.** `ForecastingItem` holds each cell (`OwnerOnlyAmount`, `AmountWithoutAdjustments`, `AmountWithoutManagerAdjustment`, `ForecastAmount`); `ForecastingFact` links it to its opportunities. Report through a custom report type on **Forecasting Items**.

## Gotchas

- **A role is not a forecast manager.** A VP above two sales managers sees only their own forecast until named Forecast Manager for the VP role. Only one person per level can hold it.
- **Deactivating a forecast type deletes its forecast data.** Its filter definitions also lock once the type is activated.
- **Switching the rollup method deletes adjustments** on every active forecast type.
- **Monthly ↔ quarterly, or a standard fiscal year change, purges** all adjustments, manager judgments and quotas. The date range tops out at 15 months, 15 fiscal periods or 8 quarters.
- **Nobody sets their own quota.** `ForecastingQuota` lets a user edit only subordinates' or child territories' quotas.
- **Dated exchange rates aren't used.** Forecasts convert at the current rate, so a rate change restates every period — past, current and future.

## Gaps to close

- [ ] What does forecast submission add (`ForecastingSubmission`, API 62.0) — who submits, and what does the manager see?
- [ ] How long does the recalculation after a period or fiscal-year change take at volume, and can an admin watch its progress?

## Confirm in org

- 🚩 Does a new Summer '26 Developer Edition org already have the default forecast type active, and a Forecasts tab in the Sales app? — Setup → Forecasts Settings, then App Manager → Sales → Navigation Items.

## Hands-on

- [ ] **SLS-FCST-01** · 20 min · Enable forecasting for a rep and for yourself in the role above, but name no Forecast Manager on your role; open Forecasts. **Proves:** the role hierarchy alone shows you nothing of the rep's forecast — only the Forecast Manager assignment does. **Needs:** a second Salesforce user.
- [ ] **SLS-FCST-02** · 15 min · Adjust the rep's Commit, then switch Forecasts Settings from cumulative to single category rollups and back. **Proves:** the adjustment is gone — count `ForecastingAdjustment` rows before and after. **Needs:** SLS-FCST-01.
- [ ] **SLS-FCST-03** · 15 min · As the forecast manager, insert a `ForecastingQuota` for yourself, then one for the rep. **Proves:** the own-quota rule — copy the error string from the first insert. **Needs:** SLS-FCST-01 and **Manage Quotas**.
- [ ] **SLS-FCST-04** · 25 min · Turn on multiple currencies and advanced currency management, add a dated rate, then compare a closed opportunity's converted amount in a report with its forecast cell. **Proves:** the report uses the dated rate and the forecast does not. **Needs:** a spare Developer Edition org — multiple currencies can't be turned off.

## Related

- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the Stage values that decide every opportunity's forecast category
- [Enterprise Territory Management](enterprise-territory-management.md) — the active territory model a territory forecast type rolls up through
- [Account & Opportunity Teams](account-and-opportunity-teams.md) — team selling and Opportunity Splits, which the split forecast types need
- [Products & Price Books](products-and-price-books.md) — product families and schedules behind the product and schedule forecast types
- [Pipeline Inspection](pipeline-inspection.md) — the deal-level view that sits beside the forecast grid
- [SF_core · 07-security · 07 Role Hierarchy & Ownership](../SF_core/07-security-and-sharing/07-role-hierarchy-and-ownership.md) — the role hierarchy the role-based forecast hierarchy is generated from, and why roles exist for roll-up at all
- [SF_core · 08-data · 22 Multi-Currency, Multi-Language & Locale](../SF_core/08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md) — static vs dated rates, and why a forecast and an opportunity report can disagree

## Sources

- [Pipeline Forecasting Implementation Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/forecasts.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · *"For orgs created in Winter '24 or later, forecasting is automatically enabled"*; the default type; the object/measure/hierarchy table; *"up to four active forecast types at one time"*; *"Deactivating a forecast type deletes the related forecasting data"*; *"Filter definitions aren't editable after activating"*; *"Switching from one rollup method to another deletes adjustments for all active forecast types"*; *"15 months, 15 fiscal periods, or 8 quarters"*; the period and fiscal-year purge; *"Only one person at each level in the forecasts hierarchy can be the manager"*; territory rollup to one territory; Override Forecasts; Setup → Forecasts Quotas; Forecasting Items report fields
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `ForecastingItem` and `ForecastingFact` read-only; `ForecastingAdjustment` vs `ForecastingOwnerAdjustment`; `ForecastingQuota` fields and *"Users can only edit their subordinates' or child territories' quotas, not their own"*; `ForecastingTypeId` on all five objects; `ForecastingSubmission` *"available in API version 62.0 and later"*
- [Collaborative Forecasts Is Now Pipeline Forecasting](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_sales_forecasts_naming_unification.htm&release=254&type=5) — Salesforce Help, Spring '25 release notes · via search 2026-09-24 · the rename
- [Considerations for Multiple Currencies in Salesforce Forecasting](https://help.salesforce.com/s/articleView?id=sales.forecasts3_multiple_currencies.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"Dated exchange rates aren't used in forecasting."*; *"Rate changes impact all forecast periods (historical, current, and future)."*
- [About Advanced Currency Management](https://help.salesforce.com/s/articleView?language=en_US&id=administration_about_advanced_currency_management.htm&type=5) — Salesforce Help · via search 2026-09-24 · *"Dated exchange rates are not used in forecasting, currency fields in other objects, or currency fields in other types of reports"*
- [Define Forecasts Quotas in Salesforce Setup](https://help.salesforce.com/s/articleView?id=sales.forecasts3_quota_management_in_setup.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · quotas managed *"without Data Loader or the API"*
- [Salesforce Past Product & Feature Retirements](https://help.salesforce.com/s/articleView?id=005132112&language=en_US&type=1) — Salesforce Help KB 005132112, updated 17 August 2026 · read 2026-09-24 · *"Customizable Forecasting | Summer '20 - July 2020"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
