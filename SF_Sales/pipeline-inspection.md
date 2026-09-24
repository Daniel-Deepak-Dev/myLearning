---
vault: SF_Sales
format: light
level: basic
status: open
gaps: 4
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [licensing]
---
# Pipeline Inspection

**One line:** An opportunity list with a metrics bar on top. It shows the pipeline for a period, what changed since a chosen date, and AI deal insights, so a manager can see which deals moved.

**Reach for it when:** a pipeline review needs "what changed this week" — pushed close dates, cut amounts, stage moves — without building a historical trending report.

## Key points

- **What you see:** opportunities with their week-to-week changes to close date, amount, stage and forecast category. Changed values are coloured green or red. A side panel adds deal insights, activity and who's involved. Lightning Experience only.
- **Two metric groups.** *Forecast Category*: Total, Closed Won, Commit, Most Likely, Best Case, Open Pipeline, Closed Lost. *Pipeline Changes*: New, Won, Lost, Moved In, Moved Out, Increased, Decreased, Overdue. Click a metric to filter the list.
- **Two date filters.** **Close Date** picks the period. **Changes Since** picks the window changes are measured over, e.g. *Start of the Period*. You can also filter by owner, team or territory.
- **Switching it on:** Setup → **Pipeline Inspection Setup** → turn it on, then **Add Button** to put it on the Opportunities list view. Historical trending must be on for Opportunity, tracking Amount, Close Date, Forecast Category and Stage.
- **Editions:** included with Sales Cloud in Enterprise, Performance and Unlimited, with no add-on since March 2023. Revenue Intelligence, a paid add-on, also includes it.
- **Access:** assign the **Pipeline Inspection User** permission set. Standard User and System Administrator profiles get access automatically. The Revenue Intelligence permission sets grant it too.
- **The flow chart needs Revenue Intelligence.** Only users with Revenue Intelligence access can use it. The waterfall chart comes with the Pipeline Changes metrics.
- **Deal insights:** Einstein Deal Insights (deal-health predictions with recommended actions) and tiered Einstein Opportunity Scores show in the side panel. Richer insights need Einstein Activity Capture for email and activity, and Einstein Conversation Insights for calls.
- **Forecasts link:** forecast-category metrics use each opportunity's forecast category. The rollup method — cumulative (default) or single category — is set in Pipeline Inspection Setup, *separately* from forecasting's own rollup setting.

## Gotchas

- **Two rollup settings can disagree.** Pipeline Inspection's Best Case can differ from the Forecasts tab's Best Case when one is cumulative and the other single category.
- **2,000+ records hide the totals.** Metric totals don't show and charts don't render. Narrow the filter.
- **Amount highlights need one currency.** A change is highlighted only when the currency is the same.
- **Views don't cross over.** Pipeline views and saved filters don't sync with Opportunity list views. The default views (My Pipeline, My Important Opportunities) can't be shared, cloned or deleted, and the *All Opportunities* owner filter isn't supported.
- **Inline edit has holes.** Forecast Category and Probability can't be edited inline. Up to 200 opportunities per user can be marked important, and that mark is private.
- **Activity data changed in Summer '25.** Activity Metrics and Activity 360 Reporting data no longer show unless already set up, which empties activity counts and Who's Involved in new setups.
- **`PushCount`** counts close dates pushed out by a calendar month. It's hidden from list views by default.

## Gaps to close

- [ ] Is **Pipeline Inspection User** backed by a permission set licence, and what does "consumes multiple license seats" mean when Revenue Intelligence is also assigned?
- [ ] Does Einstein Deal Insights need an add-on in Enterprise Edition, or does it come with Pipeline Inspection?
- [ ] Do the Close Date filter's periods follow the org's fiscal year settings or a forecast type's period?
- [ ] What does the **Alerts** column announced for September 2026 need, and which signals does it raise?

## Confirm in org

- 🚩 Does a Summer '26 Developer Edition org have Pipeline Inspection Setup at all? — Setup → Quick Find *Pipeline Inspection*.

## Hands-on

- [ ] **SLS-PIPE-01** · 15 min · Turn it on, then push one opportunity's Close Date into next month and raise another's Amount. Open it with *Changes Since* = start of the period. **Proves:** Moved Out and Increased catch both, highlighted, and `PushCount` goes up by one. **Needs:** Pipeline Inspection in the org — see Confirm in org.
- [ ] **SLS-PIPE-02** · 15 min · Give a second user a cloned custom profile and no Pipeline Inspection User permission set, then open Opportunities as them. **Proves:** access comes from the permission set, not the licence — copy what they see. **Needs:** a spare Salesforce user licence.
- [ ] **SLS-PIPE-03** · 15 min · Set Pipeline Inspection to single-category rollups while forecasts stay cumulative, then compare Best Case in both. **Proves:** the two settings are independent, so the numbers differ. **Needs:** forecasts enabled.
- [ ] **SLS-PIPE-04** · 10 min · Try to turn on the Pipeline Inspection flow chart. **Proves:** it's gated by Revenue Intelligence — copy the message, or note that the toggle is missing. **Needs:** nothing; the block is the point.

## Related

- [Collaborative Forecasts](collaborative-forecasts.md) — the forecast categories and rollups the metrics bar mirrors, and the rollup setting it doesn't share
- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the stage-to-forecast-category mapping behind every metric
- [Einstein Activity Capture](einstein-activity-capture.md) — the email and activity data behind deal insights and Who's Involved
- [SF_core · 07-security · 02 Licences & what they gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) — permission set licences, and why a permission set that needs one fails without it

## Sources

- [Pipeline Inspection](https://help.salesforce.com/s/articleView?id=sales.pipeline_inspection.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"week-to-week changes in close dates, amounts, stages, forecast categories"*; the Summer '25 Activity Metrics and Activity 360 notice
- [Pipeline Inspection Editions](https://help.salesforce.com/s/articleView?id=sales.pipeline_inspection_editions.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Enterprise, Performance, Unlimited; *"Only users with access to Revenue Intelligence can use the Pipeline Inspection flow chart"*; Lightning only
- [Get Pipeline Inspection in Enterprise Edition Without an Add-On License](https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_pipeline_inspection_enterprise_edition.htm&language=en_US&release=242&type=5) — Salesforce Help, Spring '23 release notes · via search 2026-09-24 · no add-on *"As of March 2023"*
- [Select Who Can Use Pipeline Inspection](https://help.salesforce.com/s/articleView?id=sf.pipeline_inspection_assign_users.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Pipeline Inspection User permission set; Standard User and System Administrator profiles; Revenue Intelligence permission sets
- [Considerations for Setting Up Pipeline Inspection](https://help.salesforce.com/s/articleView?language=en_US&id=sf.pipeline_inspection_considerations.htm&type=5) — Salesforce Help · read 2026-09-24 · historical trending; Revenue Intelligence licence for the flow chart; Einstein Activity Capture and Conversation Insights for more insights
- [Guidelines and Limits for Pipeline Inspection](https://help.salesforce.com/s/articleView?id=pipeline_inspection_guidelines.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · 2,000-record totals and charts; same-currency Amount highlights; 200 important opportunities; views don't sync; no inline Forecast Category or Probability; *All Opportunities* filter unsupported
- [Pipeline Inspection Metrics and Fields](https://help.salesforce.com/apex/HTViewHelpDoc?id=sf.pipeline_inspection_metrics_and_fields.htm&language=en_US) — Salesforce Help · read 2026-09-24 · both metric groups; Push Count definition and *"isn't shown in list views by default"*
- [Select a Forecast Rollups Method in Pipeline Inspection](https://help.salesforce.com/s/articleView?id=sf.pipeline_inspection_setup_rollups.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"separate from the forecast rollup setting for Salesforce Forecasting"*; cumulative is the default
- [Enhance Sales with Pipeline Inspection Setup Guide](https://trailhead.salesforce.com/content/learn/modules/revenue-intelligence-setup/set-up-pipeline-inspection) — Trailhead · read 2026-09-24 · Pipeline Inspection Setup, Add Button, the four trended fields, the flow chart toggle
- [Analyze Pipeline Health Using Metrics and Charts](https://trailhead.salesforce.com/content/learn/modules/sell-smarter-with-pipeline-inspection/understand-pipeline-health-with-metrics-and-charts) — Trailhead · read 2026-09-24 · Close Date and Changes Since filters; waterfall and flow charts
- [Einstein Features in Pipeline Inspection](https://help.salesforce.com/s/articleView?id=sf.pipeline_inspection_einstein_features.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Einstein Deal Insights and tiered opportunity scores
- [Agentforce Pipeline Management Overview](https://help.salesforce.com/s/articleView?id=sales.pipeline_mgmt_overview.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · agent suggestions in the Agent Activity column; needs the Agentforce for Sales add-on
- [Agentforce Sales Release Notes](https://www.salesforce.com/blog/sales/sales-cloud-product-release/) — Salesforce blog · read 2026-09-24 · September 2026: *"A new 'Alerts' column in Pipeline Inspection surfaces real-time risk signals"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
