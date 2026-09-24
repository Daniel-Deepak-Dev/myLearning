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
# Campaigns & Campaign Influence

**One line:** A Campaign groups the leads and contacts one marketing effort touched. Campaign Influence credits opportunities back to the campaigns that shaped them.

**Reach for it when:** marketing asks which campaigns produced pipeline, or you need response and ROI numbers per campaign.

## Key points

- **Marketing User gates the work.** Only users with **Marketing User** ticked on their user record, plus campaign permissions, can create, edit and delete campaigns and manage members. Everyone else can view and report, subject to sharing.
- **`CampaignMember` is the junction.** Each row joins one campaign to one Lead or one Contact; insert both IDs and only `ContactId` is kept. With **Accounts as Campaign Members** on, a row can point at an account instead.
- **Statuses belong to each campaign** (`CampaignMemberStatus`), and from API 39.0 each campaign needs a default plus at least one status with `HasResponded = true`. Setting a member's `Status` sets its read-only `HasResponded` flag, which `NumberOfResponses` counts for contacts and unconverted leads.
- **Hierarchy:** the **Parent Campaign** field (`ParentId`) nests campaigns up to five levels. Parents get `Hierarchy…` rollups such as `HierarchyActualCost`, `HierarchyNumberOfResponses` and `HierarchyAmountWonOpportunities`.
- **Primary Campaign Source** (`Opportunity.CampaignId`) names the one campaign that produced a deal, and lead conversion fills it from the lead's most recent campaign. `AmountWonOpportunities` (*Value Won Opportunities in Campaign*) sums the closed/won deals that name this campaign.
- **ROI** comes from the **Campaign ROI Analysis Report**: (Value Won Opportunities − `ActualCost`) ÷ `ActualCost`. `BudgetedCost` and `ExpectedRevenue` sit beside it as the plan.
- **Customizable Campaign Influence** (Setup → **Campaign Influence Settings** → Enabled) adds `CampaignInfluence` and `CampaignInfluenceModel` (API 37.0). Models look for members of active campaigns who hold a contact role on an open opportunity, and record an `Influence` % and a `RevenueShare`.
- **Models:** **Primary Campaign Source** is the default — 100% to that one campaign, by auto-association, with no manual edits. Custom models take manual percentages and can be locked to API-only; First Touch, Last Touch and Even Distribution need Account Engagement.
- **The auto-association time frame** is the number of days between a contact joining a campaign and the related opportunity being created. A campaign joined earlier than that is not counted as influential.

## Gotchas

- **No contact role, no influence.** Auto-association needs the contact in the campaign first and then on the opportunity as a contact role; a contact added to the campaign after the opportunity exists is ignored. Closed opportunities get no new influence records.
- **Member status doesn't matter to influence.** Every campaign member counts, responded or not — and a status never changes by itself when someone interacts.
- **The Primary Campaign Source model is system-owned.** Rows you add to it through the API are deleted at the next recalculation — a settings change, a Close Date change, or a member added or removed.
- **Deactivating a model deletes its records**, and going back to the Classic-only **Campaign Influence 1.0** deletes every Customizable Campaign Influence record.
- **Developer Edition allows one custom model.** Professional and Enterprise allow 3, Performance and Unlimited 5.
- **Parent statistics ignore sharing.** Hierarchy rollups include every child campaign whatever the viewer can see, and one hierarchy supports only one currency.
- **A Web-to-Lead form with a Campaign field inserts the member itself.** Help says not to add a trigger or flow that also inserts members for those leads.

## Gaps to close

- [ ] Which member statuses does a new campaign start with, and which one is the default?
- [ ] With the auto-association time frame left blank, does every earlier campaign membership count as influential?
- [ ] After a member lead converts, does its `CampaignMember` row keep `LeadId` beside the new `ContactId`, and which of `NumberOfLeads` and `NumberOfContacts` counts it?

## Confirm in org

- 🚩 Is Customizable Campaign Influence already on in a fresh Developer Edition org, with Primary Campaign Source as the default model? — Setup → **Campaign Influence Settings** → Model Settings.
- 🚩 Can an API user without **Marketing User** insert a `CampaignMember`? The object reference says create needs only read on campaigns, yet calls the object marketing-user-only — try it in Workbench as that user.

## Hands-on

- [ ] **SLS-CAMP-01** · 15 min · Untick **Marketing User** on a second user, then as that user try to create a campaign and add a contact to an existing one. **Proves:** which actions the missing checkbox removes — copy the exact message or note the missing button. **Needs:** second user.
- [ ] **SLS-CAMP-02** · 20 min · Build parent → child → grandchild campaigns with an Actual Cost on each, then close-win an opportunity whose Primary Campaign Source is the grandchild. **Proves:** the parent's `HierarchyActualCost` and `HierarchyAmountWonOpportunities` include the children while its own `ActualCost` does not. **Needs:** nothing.
- [ ] **SLS-CAMP-03** · 25 min · Turn on Customizable Campaign Influence with auto-association, add a contact to an active campaign, create an open opportunity on its account with no contact roles, then add the contact as a role. **Proves:** nothing is credited until the contact role exists — the account link alone does nothing. **Needs:** nothing.
- [ ] **SLS-CAMP-04** · 20 min · In Workbench, insert a `CampaignInfluence` row into the Primary Campaign Source model, then change that opportunity's Close Date and query again. **Proves:** the hand-written row is wiped at recalculation — that model is system-owned. **Needs:** SLS-CAMP-03 done.

## Related

- [Lead Management & Conversion](lead-management-and-conversion.md) — how a web lead joins a campaign, and how conversion moves the membership to the contact and fills Primary Campaign Source
- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the contact roles, Close Date and closed stages that decide which deals get influence
- [SF_core · 08-data · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) — where `Campaign` and `CampaignMember` sit in the Lead and Contact graph, and the `WhatId` that points activities at a campaign

## Sources

- [Sales Cloud Basics (PDF)](https://resources.docs.salesforce.com/262/latest/en-us/sfdc/pdf/sales_core.pdf) — Salesforce, Spring '26, last updated 31 March 2026 · read 2026-09-24 · *"A campaign hierarchy can support up to five levels"*, Parent Campaign field, *"only one currency"*, statistics *"regardless of the current user's sharing settings"*; *"An administrator must select the Marketing User option"*; *"their member status doesn't change automatically"*; ROI formula; Primary Campaign Source filled at conversion; Customizable Campaign Influence: *"members who are also assigned a contact role on an open opportunity"*, *"After an opportunity's stage is closed (won or lost), influence records are no longer created"*, *"considers every campaign member, regardless of their member status"*, the models and their recalculation events, custom-model counts per edition, the time-frame example, Campaign Influence 1.0 Classic-only and *"your existing campaign influence records are deleted"*; Web-to-Lead *"automatically inserts the lead as a campaign member"*
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers, Winter '27, last updated 18 September 2026 · read 2026-09-24 · `Campaign` hierarchy fields, `AmountWonOpportunities`, `NumberOfResponses` *"contacts and unconverted leads"*, marketing-user-only access; `CampaignMember` *"only the ContactId is inserted"*, Accounts as Campaign Members, *"your account only requires read access to campaigns"*, `Status` *"Controls the HasResponded flag"*, `FirstRespondedDate`; `CampaignMemberStatus` API 39.0 default and responded rules; `CampaignInfluence` *"Records added to the Primary Campaign Source model via the API are deleted when the model is recalculated"*; `CampaignInfluenceModel` *"Deactivating a model deletes its campaign influence records"*, `IsModelLocked`, `ModelType` values
- [Campaign Members Tracking](https://trailhead.salesforce.com/content/learn/modules/campaign_basics/campaigns_basics_unit_3) — Trailhead · read 2026-09-24 · one status set per campaign type; the **Responded** box on the Campaign Member Statuses related list

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
