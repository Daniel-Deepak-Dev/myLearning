---
vault: SF_Sales
format: light
level: working
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [sharing]
---
# Account & Opportunity Teams

**One line:** The named people who sell an account or a deal with its owner, the role each plays, and how the credit is split.

**Reach for it when:** a deal is worked by several reps and each needs a role on the record and a share of the revenue.

## Key points

- **Two switches.** Account teams: Setup → **Account Teams** → **Enable Account Teams**. Opportunity teams: Setup → **Opportunity Team Settings** → **Enable Team Selling**, then pick the layouts that get the related list.
- **One role list for both.** Setup → **Team Roles**. Adding or renaming a role changes it on account *and* opportunity teams; the field is `TeamMemberRole` (label *Team Role*) on all four team objects.
- **Member rows.** `AccountTeamMember` holds `AccountAccessLevel`, plus `OpportunityAccessLevel`, `CaseAccessLevel` and `ContactAccessLevel` for the account's children. `OpportunityTeamMember` holds one `OpportunityAccessLevel` (Read, Edit, All), never below the OWD.
- **Who adds members:** the owner, or anyone above the owner in the role hierarchy, with Read on users and Edit on opportunities. What the new row grants is covered in SF_core 07·10.
- **Default opportunity team** (`UserTeamMember`): personal settings → **Advanced User Details** → **Default Opportunity Team**. Two boxes: *Automatically add my default opportunity team to opportunities that I create or open opportunities that are transferred to me*, and *Update open opportunity teams with these members*.
- **An owner change keeps the old owner** on the team, in the same role. Through the API the old owner drops to Read or the opportunity OWD, whichever is higher; the UI lets you choose.
- **Splits need Team Selling first.** Then Setup → **Opportunity Splits Settings**, which needs Modify All Data. Enabling puts each opportunity's owner on its team at 100% — extra rows that use data storage.
- **Two default split types on Amount** (`OpportunitySplitType`). **Revenue** must total 100% (`IsTotalValidated = true`, rows 0–100%); **Overlay** can total anything (rows 0–1,000%). Admins can add up to six custom types on currency or roll-up summary fields, never formula fields.
- **Split rows** (`OpportunitySplit`: `SplitOwnerId`, `SplitPercentage`, `SplitTypeId`) are edited by the owner or anyone above them, with Edit on opportunities. **Opportunity product splits** (`OpportunityLineItemSplit`, GA Summer '23) split per product line; revenue types allow at most 200 products per opportunity.

## Gotchas

- **Leave the *Opportunity Owner* role alone.** Help: *"Leave the role of Opportunity Owner unchanged. It's required for opportunity splits."*
- **A member who holds a split can't be removed:** *"Can't remove a team member assigned to a split from an opportunity."* A deactivated split type hides its rows but keeps them, so query `OpportunitySplit` by `OpportunityId` and delete the hidden row first.
- **Default teams reach saved records only on request.** Edits touch nothing already saved unless you tick *Update open opportunity teams…*. The **Add Default Team** button adds the **owner's** default team, not the clicker's.
- **Group-based adders don't stick.** Account team members added by a user whose access comes from a group are removed on an owner change, even with **Keep account team** ticked. Only an admin, a Modify All Data user, the owner or someone above them in the *direct* role chain adds members that survive.
- **Account and opportunity teams don't sync.** Removing an account team member who receives splits leaves them on the account's open opportunities; remove them there too.
- **Deleted team rows skip the Recycle Bin.** A directly deleted `AccountTeamMember` or `OpportunityTeamMember` can't be undeleted, and `IsDeleted` won't find it — use `getDeleted()`.
- **One territory per member, per split type.** *"All splits of one split type for a team member, including the opportunity owner, must have a unique territory"* — the territory sits in `OpportunitySplit.Territory2Id` (API 62.0).

## Gaps to close

- [ ] Is there a documented cap on members per account team or per opportunity team?
- [ ] Does *Update open opportunity teams with these members* touch only opportunities the user owns, and does it overwrite an existing member's role or access?
- [ ] What happens to a split type's `OpportunitySplit` rows, and to split-based forecasts, when the type is deactivated rather than deleted?

## Confirm in org

- 🚩 Does an API `delete` of an `OpportunityTeamMember` who holds a split fail with the same message as the UI? — Developer Console → Execute Anonymous on that row; copy the exception.

## Hands-on

- [ ] **SLS-TEAM-01** · 15 min · Enable Account Teams and Team Selling, add a *Solution Engineer* role under Account Teams → Team Roles, then open the Team Role picklist on an opportunity team. **Proves:** one role list serves both teams — the account role appears on the opportunity side. **Needs:** nothing.
- [ ] **SLS-TEAM-02** · 20 min · Enable splits, give the owner 60% and a second user 30% of the Revenue split and save; then set Overlay rows totalling 150%. **Proves:** Revenue refuses anything but 100% — copy the error — while Overlay accepts 150%. **Needs:** second user.
- [ ] **SLS-TEAM-03** · 20 min · Give the second user an Overlay split, deactivate the Overlay type, then remove them from the opportunity team. **Proves:** a hidden split from an inactive type still blocks removal — find it with `SELECT Id, SplitTypeId FROM OpportunitySplit WHERE OpportunityId = '<id>'`. **Needs:** SLS-TEAM-02.
- [ ] **SLS-TEAM-04** · 15 min · Build a default opportunity team for the second user with both boxes clear, transfer one of your opportunities to them, then click **Add Default Team** yourself. **Proves:** nothing is added on transfer, and the button adds the owner's team, not yours. **Needs:** second user.

## Related

- [Enterprise Territory Management](enterprise-territory-management.md) — the other way to decide who covers an account, and the territory each split row carries
- [Collaborative Forecasts](collaborative-forecasts.md) — where split amounts are forecast, by owner or by territory
- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the record the team and its splits hang off
- [SF_core · 07-security · 10 Teams, territories & account sharing](../SF_core/07-security-and-sharing/10-teams-territories-and-account-sharing.md) — the share rows (`RowCause = Team`) a member row creates, and what removing one revokes
- [SF_core · 02-apex · 11 Sharing keywords & Apex managed sharing](../SF_core/02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md) — when code must keep team membership in step with a field, such as a helper lookup that swaps members

## Sources

- [Facilitate Team Selling by Enabling Opportunity Teams](https://help.salesforce.com/s/articleView?id=sales.teamselling_enabling.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Opportunity Team Settings → *"Select Enable Team Selling and click Save"*; layouts for the related list
- [Enable Account Teams](https://help.salesforce.com/s/articleView?id=sf.tpm_task_enable_account_teams.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Account Teams → Enable Account Teams → *Account Teams Enabled*
- [Customize Account Team Roles](https://help.salesforce.com/s/articleView?id=sales.accountteam_customize_roles.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"Account teams and opportunity teams share roles with each other"*
- [Customize Opportunity Team Roles](https://help.salesforce.com/s/articleView?id=teamselling_customize_roles.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Setup → Team Roles; *"Leave the role of Opportunity Owner unchanged"*; *"retains the original owner on the opportunity team with that same role"*
- [Add Opportunity Team Members](https://help.salesforce.com/s/articleView?id=sf.salesteam_add.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · owner or above in the role hierarchy; *"Read on users AND Edit on opportunities"*
- [Set Up a Default Opportunity Team](https://help.salesforce.com/s/articleView?id=sf.salesteam_default.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Advanced User Details; the two checkbox labels; Add Default Team adds the owner's team
- [Considerations for Using Account Teams](https://help.salesforce.com/s/articleView?id=accountteam_def.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · group-based adders removed *"even if you've selected Keep account team"*; the four kinds of user who add lasting members
- [Working with Teams on Your Accounts](https://help.salesforce.com/s/articleView?id=sales.accountteam_add.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · removing an account team member who receives splits from open opportunities too
- [Enable Opportunity Splits](https://help.salesforce.com/s/articleView?id=sales.teamselling_opp_splits_enable.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Team Selling first; Modify All Data; owner *"assigned 100% of the split amount"*; *"use more data storage"*
- [Customize Opportunity Split Types](https://help.salesforce.com/s/articleView?id=sales.teamselling_opp_splits_create_custom_splits.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"create up to six custom opportunity split types"*; currency and roll-up summary fields, not formula fields
- [Guidelines and Considerations for Using Opportunity Splits and Opportunity Product Splits](https://help.salesforce.com/s/articleView?id=sales.teamselling_guidelines_opp_and_opp_prod_splits.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · edit permissions; 200 products; *"must have a unique territory"*
- [Split Revenue by Product Mix with Opportunity Product Splits (Generally Available)](https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_features_core_split_revenue_by_product.htm&language=en_US&release=244&type=5) — Salesforce Release Notes, Summer '23 · via search 2026-09-24 · product splits GA
- [Can't Remove a Team Member Assigned to an Opportunity Split](https://help.salesforce.com/s/articleView?id=000387684&language=en_US&type=1) — Salesforce Help KB 000387684 · read 2026-09-24 · the error string; the hidden-split query and delete
- [Cannot Remove a Team Member Assigned to an Opportunity Split](https://help.salesforce.com/s/articleView?id=000381173&language=en_US&type=1) — Salesforce Help KB 000381173 · read 2026-09-24 · inactive split types are hidden in the UI to *"preserve the history of split lines"*
- [Team Selling & Opportunity Splits](https://trailhead.salesforce.com/content/learn/modules/leads_opportunities_lightning_experience/sell-as-a-team-and-split-the-credit) — Trailhead · read 2026-09-24 · owner or above adjusts splits; revenue vs overlay totals
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers, Winter '27, last updated 18 September 2026 · read 2026-09-24 · `AccountTeamMember`, `OpportunityTeamMember`, `UserTeamMember` and `UserAccountTeamMember` fields; API owner change *"Read Only or the access specified in your organization-wide default"*; deleted rows skip the Recycle Bin; `OpportunitySplit.SplitPercentage` *"0 to 100 … 0 to 1,000"*; `OpportunitySplit.Territory2Id` API 62.0; `OpportunitySplitType` *"revenue splits, which must total 100%, and overlay splits, which can total any percentage"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
