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
# Lead Management & Conversion

**One line:** A Lead is an unqualified prospect. Converting it creates an Account, a Contact and, optionally, an Opportunity — and it cannot be undone.

**Reach for it when:** prospects arrive from a web form or a list, need routing to a rep, and the qualified ones must become pipeline.

## Key points

- **Lead Status is a special picklist.** Each value is a `LeadStatus` row, and `IsConverted = true` marks the values offered at conversion. Setting `Status` to a converted value through the API does not convert the lead.
- **Web-to-Lead** (Setup → **Web-to-Lead**) generates an HTML form that posts to your org. New web leads get the default Lead Status and stay Unread (`IsUnreadByOwner = true`) until the owner opens them.
- **The cap is 500 Web-to-Lead requests a day.** Extra requests wait in a pending queue shared with Web-to-Case, capped at 50,000, and the Default Lead Creator gets an email. Support can raise the cap.
- **Spam:** **Require reCAPTCHA Verification** rejects submissions without a valid reCAPTCHA. It is on by default in orgs created after Winter '19, and only reCAPTCHA v2 is supported.
- **Auto-response rules** (Setup → **Lead Auto-Response Rules**) pick the reply template. Only one lead rule is active, and the **Default Response Template** covers leads that no entry matches.
- **Routing** is the lead assignment rule (Setup → **Lead Assignment Rules**). An API insert must send `AssignmentRuleHeader`, or the rule does not run.
- **Conversion** runs from the Convert button or `Database.convertLead()` with a `Database.LeadConvert` — `setLeadId()` and `setConvertedStatus()` are required, `setDoNotCreateOpportunity(true)` skips the deal. The lead stays, read-only, with `IsConverted`, `ConvertedDate`, `ConvertedAccountId`, `ConvertedContactId` and `ConvertedOpportunityId` set.
- **Existing records only get blanks filled.** Converting into an existing account or contact never overwrites its data, except `LeadSource` if you opt in. Campaign members move to the contact, and activities attach to every new record.
- **Custom fields need a map:** Object Manager → Lead → Fields & Relationships → **Map Lead Fields**; standard fields map themselves. Most custom types map only to the same type, and in Lightning one lead field can feed all three objects.

## Gotchas

- **No undo.** Only users with **View and Edit Converted Leads** can open or edit a converted lead; everyone else meets it in reports only.
- **Lead validation rules can be skipped.** They gate conversion only when **Require Validation for Converted Leads** (Setup → **Lead Settings**) is on; with it off, lookup filters are ignored too. Triggers fire either way.
- **Duplicate rules are partly out.** Cross-object duplicate rules never fire on conversion, custom duplicate alerts don't show, and orgs still on the old PL/SQL convert run no duplicate rules and get no **Map Lead Fields**.
- **A blank Company can mean a person account.** With person accounts on, Lightning converts a lead with no `Company` into a person account, and a `Title` over 80 characters then fails the conversion.
- **Record types come from a user, not the lead.** Help says new records take the converting user's default record type; the SOAP API guide says the new owner's 🚩.
- **A required custom field on `OpportunityContactRole`** blocks creating the opportunity at conversion, because nothing maps into it.
- **The Default Lead Creator needs Modify All Data and Send Email**, both from the profile or both from a permission set — Help says not to mix the two.

## Gaps to close

- [ ] Does Web-to-Lead run the active lead assignment rule by itself, and who owns a web lead that no entry matches?
- [ ] Which hidden inputs must a Web-to-Lead form post (`oid`, `retURL`, campaign and member status), and what happens to a field name the org does not know?
- [ ] Which Lead Settings shape the convert window — a default of creating no opportunity, and what exactly does **Preserve Lead Status** keep?

## Confirm in org

- 🚩 With **Require Validation for Converted Leads** off, does an **Account** validation rule still block conversion? Help's *Considerations for Converting Leads* says validation rules "are enforced", KB 000386058 says they need the setting — put one rule on Lead and one on Account, then convert.
- 🚩 Is a new Developer Edition org on Apex Lead Convert? — Object Manager → Lead → Fields & Relationships: **Map Lead Fields** only works there.

## Hands-on

- [ ] **SLS-LEAD-01** · 20 min · Add a Lead validation rule requiring `Industry`, leave **Require Validation for Converted Leads** off and convert a lead with no Industry; then tick it and convert another. **Proves:** lead validation rules gate conversion only with the setting on — copy the error text. **Needs:** nothing.
- [ ] **SLS-LEAD-02** · 25 min · Turn on **Require reCAPTCHA Verification**, generate the form, delete the reCAPTCHA block from the HTML and submit it from a local file. **Proves:** the post is rejected and no lead appears; untick the setting and the same post lands as an Unread lead. **Needs:** a Google reCAPTCHA v2 key pair.
- [ ] **SLS-LEAD-03** · 20 min · Create `Budget_Notes__c` (Text) on Lead and Opportunity, convert a lead without mapping it, then map it in **Map Lead Fields** and convert another. **Proves:** unmapped custom lead data is dropped silently at conversion. **Needs:** nothing.
- [ ] **SLS-LEAD-04** · 15 min · Convert a lead into an existing contact that has `Phone` filled and `Title` blank, with different values on the lead. **Proves:** conversion fills blanks only — `Title` arrives, `Phone` keeps the contact's value. **Needs:** nothing.

## Related

- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — where the opportunity born at conversion goes next, with its Close Date preset to quarter-end
- [Campaigns & Campaign Influence](campaigns-and-campaign-influence.md) — how the form's Campaign field makes a web lead a member, and how conversion carries that membership to the contact
- [SF_core · 01-admin · 11 Queues, assignment & escalation rules](../SF_core/01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) — the one-active-rule, first-match-wins mechanics that route new leads, and why API loads need `AssignmentRuleHeader`
- [SF_core · 01-admin · 08 Validation rules & duplicate management](../SF_core/01-admin-and-declarative-platform/08-validation-rules-and-duplicate-management.md) — the matching and duplicate rules that conversion only partly runs, and the validation rules the Lead Settings checkbox switches on
- [SF_core · 08-data · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) — the Pre-sale row: the Account, Contact and Opportunity a conversion writes, and where `Campaign` joins the graph

## Sources

- [Sales Cloud Basics (PDF)](https://resources.docs.salesforce.com/262/latest/en-us/sfdc/pdf/sales_core.pdf) — Salesforce, Spring '26, last updated 31 March 2026 · read 2026-09-24 · Web-to-Lead setup: *"In orgs created after Winter '19, this setting is enabled by default"*, Default Lead Creator *"must have the Modify all Data and Send Email permissions"*, Default Response Template, *"The daily limit for Web-to-Lead requests is 500"*, default status and Unread; conversion considerations: *"Salesforce moves any campaign members to the new contacts"*, lookup filters ignored with the setting off, *"cross-object duplicate rules, they aren't triggered"*, *"Custom warnings ... don't appear"*, person accounts in Lightning, record type *"of the user converting the lead"*, required `OpportunityContactRole` fields, existing records not overwritten; Map Lead Fields and same-type rules; PL/SQL vs Apex Lead Convert; conversion Close Date at fiscal quarter-end
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers, Winter '27, last updated 18 September 2026 · read 2026-09-24 · `Lead.Company` *"if the value of Company is null, the lead converts to a person account"*; `Title` over 80 characters fails person-account conversion; the converted-lead fields; *"You can't convert a lead via the API by changing Status"*; View and Edit Converted Leads; `AssignmentRuleHeader`; `LeadStatus.IsConverted`
- [LeadConvert Class](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_dml_convertLead.htm) — Apex Reference Guide · read 2026-09-24 · `setLeadId()` and `setConvertedStatus()` *"This field is required"*; `setDoNotCreateOpportunity()`; `setOverwriteLeadSource()`
- [convertLead()](https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_calls_convertlead.htm) — SOAP API Developer Guide · read 2026-09-24 · *"only empty fields in the target object are overwritten"*; *"the default record type of the new owner"*; queue-owned leads need an explicit owner
- [What if my company reaches the limit for web-generated leads?](https://help.salesforce.com/s/articleView?id=sf.faq_leads_what_if_my_company.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · 500 a day; the Default Lead Creator gets an email; Support raises the cap
- [Web-to-Case and Web-to-Lead Daily Limits Exceeded Due to Spam](https://help.salesforce.com/s/articleView?id=000316100&language=en_US&type=1) — Salesforce Help KB 000316100 · via search 2026-09-24 · pending request queue *"has a limit of 50,000 combined requests"*
- [Compatible reCAPTCHA Version for Web-to-Lead and Web-to-Case (Web-to-X) Forms](https://help.salesforce.com/s/articleView?id=000394922&language=en_US&type=1) — Salesforce Help KB 000394922 · via search 2026-09-24 · *"supports only Google reCAPTCHA version 2"*
- [Set Up Auto-Response Rules](https://help.salesforce.com/s/articleView?id=service.creating_auto-response_rules.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · one active rule for leads; Setup → Lead Auto-Response Rules
- [Validation rule not firing when converting Leads](https://help.salesforce.com/s/articleView?id=000386058&language=en_US&type=1) — Salesforce Help KB 000386058 · read 2026-09-24 · *"To enforce a Validation Rule when converting leads, you need to enable 'Require validation for Converted Leads.'"*
- [Things to Know About Duplicate Rules](https://help.salesforce.com/s/articleView?language=en_US&id=sales.duplicate_rules_overview.htm&type=5) — Salesforce Help · via search 2026-09-24 · duplicate rules don't run when leads are converted and *"Use Apex Lead Convert isn't enabled"*
- [Salesforce Lead Management Implementation Guide (PDF)](https://resources.docs.salesforce.com/208/latest/en-us/sfdc/pdf/salesforce_lead_implementation_guide.pdf) — Salesforce, Summer '17 · via search 2026-09-24 · unmapped custom lead fields *"are not converted"* — an old guide; SLS-LEAD-03 re-checks it

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
