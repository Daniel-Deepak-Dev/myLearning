---
vault: SF_Sales
format: light
level: working
status: open
gaps: 4
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [sharing, retirement]
---
# Enterprise Territory Management

**One line:** Accounts and leads grouped into a hierarchy of territories, with users assigned per territory, built and versioned as models.

**Reach for it when:** coverage follows geography, industry or named accounts rather than who owns the record.

## Key points

- **Now called Sales Territories.** Help and the Winter '27 guide use the new name; the API keeps `Territory2`. Setup → **Territory Settings** → **Enable Sales Territories** (Customize Application), in Developer and Performance, or Enterprise and Unlimited with Sales Cloud.
- **Build objects:** `Territory2Type` (a category, carrying `Priority`), `Territory2Model` (one complete territory system) and `Territory2` (one node, with `ParentTerritory2Id`, `ForecastUserId` and a default access level per object).
- **Assignment objects.** `UserTerritory2Association` puts a user in a territory, with a `RoleInTerritory2` picklist you fill in Object Manager. `ObjectTerritory2Association` puts an Account (API 30.0+) or a Lead (API 55.0+) in one, with `AssociationCause` = `Territory2AssignmentRule` or `Territory2Manual`.
- **Rules assign accounts.** `ObjectTerritory2AssignmentRule` plus its `…RuleItem` criteria rows, up to 15 rules per territory; **Apply to child territories** makes a rule inherited. Leads go in by hand or API, from the **Assigned Territories** related list.
- **Model states.** **Planning** is where every model starts — rules run and preview, but nobody gains access; **Active** (one model at a time) grants access and drives territory forecasts; **Archived** is read-only and never comes back. In between sit Activating, Archiving, Deleting and Cloning, plus three `… Failed` states.
- **Allocations.** Models per org, clones included: Developer 4, Enterprise 2, Performance 4, Unlimited 4. Territories per model: 1,000 (Performance 99,999), raised by Support, with over 20,000 needing approval; 1,950 users per territory, and test hard above 300.
- **An opportunity carries one territory**, in `Opportunity.Territory2Id`. A user with full access to the parent account can pick any territory in the active model; anyone else only the account's own — *"The same restriction applies to territory assignments made via Apex in system mode."*
- **Filter-based opportunity territory assignment** fills that field in bulk. Enable it in Territory Settings and name a class implementing `TerritoryMgmt.OpportunityTerritory2AssignmentFilter` (Salesforce's sample is `OppTerrAssignDefaultLogicFilter`); run it with **Run Opportunity Filter** or on every opportunity create, and opt a deal out with `IsExcludedFromTerritory2Filter`.
- **Delegated territory admins** (API 63.0): a `TerritoryAdminAssignment` row plus the **Administer Territory Operations** permission set lets a user run one subtree, via `CanManageHierarchy`, `CanManageMembers` and `CanManageRecordAssociations`.

## Gotchas

- **Saving an account doesn't run rules by itself.** A UI edit needs *Evaluate this account against territory rules on save*, an API edit needs `AssignmentRuleHeader`, and inserts need *Run territory assignment rules during account inserts* in Territory Settings.
- **Archiving deletes territory forecasts** — forecast types, quotas and adjustments — plus territory sharing and group data. It also blanks `Opportunity.Territory2Id` on those deals, so snapshot or export first.
- **Active is one-way:** no return to Planning and no reactivating an archive, so iterate on a clone. Clones copy territories, rules, users and manual account assignments but **not leads**, and triggers on `Territory2Model`, `Territory2` and `UserTerritory2Association` don't fire while cloning.
- **Tied priorities assign nothing.** The sample filter picks the account territory whose type has the highest `Priority` (bigger number wins; values must be unique). Two account territories of the *same* type → `Territory2Id` stays blank.
- **Rule criteria traps.** ZIP codes are text, so *"9 is 'higher' than 80000"*; with state and country picklists on, state criteria must use *contains*, not *equals*.
- **Manage Territories is not record access.** It shows Planning and Archived territories and their account lists, name and ID only. Rule authors also need View All on Accounts, and FLS limits which fields a rule can test.
- **The objects without a `2` are dead.** `Territory` (API 7.0–52.0) and `UserTerritory` belong to original Territory Management, retired with Summer '21; its data is no longer reachable by UI or API.

## Gaps to close

- [ ] Can `ObjectTerritory2AssignmentRule` target Lead yet — its `ObjectType` still reads *"For API version 31, Account only"* — or are lead assignments manual and API only?
- [ ] Does activating a Planning model while another is Active archive the old one automatically, or must you archive first?
- [ ] What does `getOpportunityTerritory2Assignments` take and return, and how many opportunity IDs does the filter job pass per call?
- [ ] What does the filter job's *multithreading* option change, and why is it advised only when assigning opportunity or opportunity product splits?

## Confirm in org

- 🚩 Does a Summer '26 Developer Edition org label the switch **Enable Sales Territories** or **Enable Enterprise Territory Management**, and is it already on? — Setup → **Territory Settings**.

## Hands-on

- [ ] **SLS-ETM-01** · 30 min · Build a model: a parent territory with a *Billing State contains CA* rule and **Apply to child territories**, one child, the second user assigned; run rules while still Planning. **Proves:** Planning previews the assignment (View Accounts shows it) but the user still can't open the account. **Needs:** second user, Account OWD Private.
- [ ] **SLS-ETM-02** · 15 min · Activate the model, then set a new account's Billing State to CA twice — with *Evaluate this account against territory rules on save* unticked, then ticked. **Proves:** rules run on save only when the box, or `AssignmentRuleHeader`, asks. **Needs:** SLS-ETM-01.
- [ ] **SLS-ETM-03** · 30 min · Deploy Salesforce's sample `OppTerrAssignDefaultLogicFilter`, put one account in two territories of the same type, then **Run Opportunity Filter**. **Proves:** a tie on type priority leaves `Opportunity.Territory2Id` blank. **Needs:** SLS-ETM-02.
- [ ] **SLS-ETM-04** · 20 min · Clone the active model until the org refuses, then archive the active model and try to reactivate it. **Proves:** the DE ceiling is four models, clones included — copy the error — and an archived model never returns. **Needs:** SLS-ETM-03.

## Related

- [Account & Opportunity Teams](account-and-opportunity-teams.md) — the per-deal way to add sellers, and the split rows that carry a territory
- [Collaborative Forecasts](collaborative-forecasts.md) — territory forecasts roll up the active model's hierarchy, and are deleted when it is archived
- [Lead Management & Conversion](lead-management-and-conversion.md) — the leads that can sit in territories alongside accounts
- [SF_core · 07-security · 10 Teams, territories & account sharing](../SF_core/07-security-and-sharing/10-teams-territories-and-account-sharing.md) — the access a territory grants and how it flows up the territory hierarchy
- [SF_core · 07-security · 07 Role hierarchy & ownership](../SF_core/07-security-and-sharing/07-role-hierarchy-and-ownership.md) — the first hierarchy, which territories run beside rather than replace

## Sources

- [Sales Territories Implementation Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_implementing_territory_mgmt2_guide.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · Territory Settings → *Enable Sales Territories*; editions; models per edition *"This limit includes models created by cloning"*; state definitions, *"archived models can't be reactivated"*; archiving *"deletes your territory forecasts, forecast types, quotas, and adjustments"*; *"as many as 15 rules"*; the three rule-run conditions; ZIP and state-picklist criteria; `OppTerrAssignDefaultLogicFilter`, *"must implement the OpportunityTerritory2AssignmentFilter interface"*, *"the higher the number, the higher the priority"*; *Exclude from the territory assignment filter logic*; clones *"not leads"*, triggers don't fire; *"more than 300 users"*; Manage Territories shows *"Only the name and ID fields"*
- [Allocations and Considerations for Territories](https://help.salesforce.com/s/articleView?id=tm2_allocations.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · territories per model by edition (1,000; Performance 99,999); *"Requests for more than 20,000 territories per model are subject to approval"*; 15 rules and 1,950 users per territory
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers, Winter '27, last updated 18 September 2026 · read 2026-09-24 · `Territory2Model.State` values; `Territory2Type.Priority` *"must be unique"* and *"no territory is assigned"* on a same-type tie; `Territory2` access-level and `ForecastUserId` fields; `UserTerritory2Association.RoleInTerritory2`; `ObjectTerritory2Association` Account API 30.0, Lead API 55.0, `AssociationCause`; `ObjectTerritory2AssignmentRule.ObjectType`; `Opportunity.Territory2Id` system-mode restriction; `IsExcludedFromTerritory2Filter`; `TerritoryAdminAssignment` API 63.0; `Territory` *"available in API versions 7.0 to 52.0"*
- [Enterprise Territory Management Is Now Sales Territories](https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_spm_etm_to_sales_territories.htm&language=en_US&release=250&type=5) — Salesforce Release Notes, Summer '24 · via search 2026-09-24 · the rename (page title only; body did not load)
- [Enable Sales Territories (Formerly Known as Enterprise Territory Management)](https://help.salesforce.com/s/articleView?id=000396697&language=en_US&type=1) — Salesforce Help KB 000396697, published 11 May 2026 · read 2026-09-24 · the *"formerly known as"* title
- [Sales Territory Management Guide](https://trailhead.salesforce.com/content/learn/modules/sales-territories-and-forecasting/manage-territories-and-crush-your-sales-goals) — Trailhead · read 2026-09-24 · *"Sales Territories (formerly known as Enterprise Territory Management (ETM))"*; editions
- [Assign Leads to Territories (Generally Available)](https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_features_core_territory_management_leads.htm&language=en_US&release=240&type=5) — Salesforce Release Notes, Winter '23 · via search 2026-09-24 · lead support (page title only)
- [Assign Accounts and Leads to Territories Manually](https://help.salesforce.com/s/articleView?id=sales.tm2_assign_territories_manually.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Assigned Territories → Assign Territories; only the active model in Lightning
- [OpportunityTerritory2AssignmentFilter Global Interface](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_interface_TerritoryMgmt_OpportunityTerritory2AssignmentFilter.htm) — Apex Reference Guide · via search 2026-09-24 · `TerritoryMgmt` namespace; *"assign a single territory to an opportunity"* (page returned 403)
- [Managing Users and Roles Within Territories](https://help.salesforce.com/s/articleView?id=sales.tm2_assign_user_management.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *Specify Teammates Who Can Administer Territories*; Role in Territory is not the org role hierarchy
- [Original Territory Management Module Retirement](https://help.salesforce.com/s/articleView?id=000383474&language=en_US&type=1) — Salesforce Help KB 000383474, published 20 February 2026 · read 2026-09-24 · retired *"with the Summer '21 release"*; *"no longer be able to access their original Territory Management data via the UI or API"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
