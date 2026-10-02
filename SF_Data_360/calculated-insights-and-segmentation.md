---
vault: SF_Data_360
format: light
level: working
status: open
gaps: 2
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Calculated Insights & Segmentation

**One line:** **Insights** compute metrics over unified profiles; **segments** slice profiles into audiences; **activation** publishes a segment to a target where something happens.

**Reach for it when:** you need a metric an agent or a campaign can trust, or an audience to send somewhere.

## Key points

- **Calculated insights** run complex calculations over **stored** data, processed in high-volume batches. Any data can feed them.
- **Streaming insights** run over **real-time** engagement data (for example Web or Mobile SDK events) as near-real-time time-series aggregates. They drive orchestration or data actions, and **can't** be built on streaming profile data.
- **Insights feed segments.** Metrics, dimensions and filters from a calculated insight define segment criteria and personalization attributes.
- **A segment is published to an activation**, and each activation points at an **activation target**. The target holds the authentication for a platform: Marketing Cloud, Data 360 itself, B2C Commerce, Amazon Ads, Google.
- **Agents ground on insights too.** For an analytical question ("is this customer high value?"), a governed insight is cheaper and safer than letting the model aggregate raw rows.
- **RFM** (recency, frequency, monetary) emits a tier label rather than one number. Its quintile ranks are **relative**: they re-cut on every run.

## Gotchas

- **Insights compute per unified profile**, so fragmented or merged profiles produce wrong metrics. The error starts in [identity resolution](identity-resolution.md).
- **Insights run on a schedule.** An agent can ground on a stale value, the same freshness problem as ingestion one layer up.
- **Automations on RFM transitions fire on population shifts.** A customer can drop from champion to loyal because others moved, not because they did.
- **Match segment refresh to the activation's cadence.** Publishing more often than the target uses costs money and changes nothing.
- **Two definitions of one metric is a governance problem.** A semantic layer makes the disagreement visible; it does not choose the winner.

## Gaps to close

- [ ] Re-read Enhance Data with Insights and Activation for Data 360 Segments in full once help.salesforce.com is reachable. This note was built from search extracts.
- [ ] What are the segment publish-frequency options and limits at API 67.0?

## Hands-on

- [ ] **D360-SEG-01** · 30 min · Build a calculated insight for total spend per unified individual, then recompute it as raw SQL in Query Workspace. **Proves:** you can validate an insight against hand-written SQL rather than trusting the UI.
- [ ] **D360-SEG-02** · 20 min · Build a segment on that insight and publish it to the Data 360 activation target. **Proves:** segment, activation and target are three separate objects; note which one holds the schedule.
- [ ] **D360-SEG-03** · 25 min · Build an RFM-style tier insight on invented data, add 50 big spenders, and rerun. **Proves:** existing customers change tier with no change in their own behaviour.

## Related

- [Identity Resolution](identity-resolution.md) — the profiles every insight is computed over
- [Data Model: DSO, DLO & DMO](data-model-dso-dlo-dmo.md) — the DMOs insights query
- [SF_core · 04-flow · 22 Data Cloud-triggered flows & data actions](../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md) — what a streaming insight or data action triggers on the CRM side
- [Interview · Identity & segmentation](../Interview/02-data-360/02-identity-and-segmentation.md) — the RFM churn-alert and two-definitions-of-churn scenarios

## Sources

- [Enhance Data with Insights](https://help.salesforce.com/s/articleView?language=en_US&id=data.c360_a_insights.htm&type=5) — Salesforce Help · via search 2026-10-02 · calculated vs streaming insights
- [Data Cloud Insights & Use Cases](https://trailhead.salesforce.com/content/learn/modules/customer-data-platform-insights/learn-about-customer-data-platform-insights) — Trailhead · via search 2026-10-02 · batch vs streaming processing; streaming only from engagement data
- [Activation for Data 360 Segments](https://help.salesforce.com/s/articleView?id=sf.c360_a_activation_for_a_segment.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · segment → activation → activation target
- [Create Segments and Reports with Data 360 Insights](https://trailhead.salesforce.com/content/learn/projects/explore-data-cloud-core-functionality/build-a-segment-and-report) — Trailhead · via search 2026-10-02

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts
