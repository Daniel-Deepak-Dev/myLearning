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
tags: [licensing, integration, retirement]
---
# Einstein Activity Capture

**One line:** Syncs reps' Google or Microsoft 365 email and calendar into Salesforce — as real `Task` and `EmailMessage` records since Summer '25, as off-platform timeline data before that.

**Reach for it when:** reps won't log email by hand, and you must know whether the activity you see is reportable, queryable and kept.

## Key points

| | Legacy storage | Sync Email as Salesforce Activity |
|---|---|---|
| **Email lives** | Activity Platform on Hyperforce, outside the org's database | `Task` and `EmailMessage` records in the org |
| **Reports, SOQL, flows** | no — activity timeline only | yes — standard activity report types |
| **Storage** | not counted; kept 6 months (Standard only) or 24 months (any paid licence) | counts towards the org's data storage |
| **Default for** | orgs set up before Summer '25 that never switched | new EAC setups from Summer '25 |

- **What it does.** Captures email, and syncs events and contacts, between a connected Google or Microsoft 365 account and Salesforce, then links them to matching contacts, leads, accounts and opportunities. Events land as `Event` records; sync is continuous, not real time.
- **Three gates per user:** an EAC licence, a permission set such as **Standard Einstein Activity Capture**, and membership of a **configuration**. Setup → **Einstein Activity Capture** → Settings runs the guided setup.
- **A configuration** sets the email service and authentication, what to capture and sync, and who is in it — users or profiles (`UserEmailCalendarSync` holds the assignments). Exclusions keep a person's or company's email and events out.
- **Licences.** Every Sales Cloud licence brings one **EAC Standard** seat. Sales Cloud Einstein, Inbox, Sales Engagement, Revenue Intelligence, and Performance or Unlimited Edition give the paid version.
- **Header-only capture** keeps sender, recipients, date and time, but not subject or body. `EmailMessage.Source` (API 64.0) records it: *Einstein Activity Capture* for full mail, *Einstein Activity Capture Limited* for header-only.
- **Turning on Sync Email as Salesforce Activity** can pull in up to 180 days of past email. It needs the **Enhanced Email** org setting.
- **Neighbours.** The Outlook and Gmail integrations are the side panel for logging by hand; **Inbox** ships an *Inbox With Einstein Activity Capture* permission set. Einstein Conversation Insights uses EAC's calendar data to match call speakers to contacts.

## Gotchas

- **Microsoft Graph deadline: 1 October 2026.** A Microsoft 365 connection set up before Spring '26 must move off EWS by then, and the upgrade can't be rolled back.
- **Legacy reporting retires in Spring '27** (February 2027): Activity 360 Reports, the Activities Dashboard, Activity Metrics and Recommended Connections. Since Summer '25 they are unavailable unless set up earlier, and so is the data they fed into Pipeline Inspection and ECI.
- **Legacy email is deleted on a clock.** Retention counts from when the activity was added to Salesforce, not when it happened.
- **A permission set alone captures nothing.** A user outside every configuration is not captured.
- **Each user must accept the terms of service** once email capture is on, with user-level authentication. `ActivityUsrConnectionStatus.IsTermsOfServiceAccepted` shows who has.
- **Enhanced Email is locked on** in the Outlook and Gmail integration while Sync Email as Activity is on.

## Gaps to close

- [ ] Did Spring '26 switch every existing EAC org to Sync Email as Salesforce Activity, and was email already on Activity Platform migrated? The *Migrated Captured Email* `Source` value suggests it can be.
- [ ] With Sync Email as Salesforce Activity, who owns the captured `Task`, and do the configuration's sharing settings still decide who sees the email?
- [ ] Does EAC Standard sync only the user's primary email address, and does a paid licence lift that?

## Confirm in org

- 🚩 Does a Summer '26 Developer Edition org include EAC Standard and the **Standard Einstein Activity Capture** permission set? — Setup → Company Information → Permission Set Licenses, then Setup → Einstein Activity Capture → Settings.

## Hands-on

- [ ] **SLS-EAC-01** · 25 min · Run the guided setup with a test mailbox, put yourself in a configuration, email a Contact, then query `SELECT Subject, Source FROM EmailMessage ORDER BY CreatedDate DESC LIMIT 5`. **Proves:** captured email is now a real `EmailMessage` row — or, if nothing returns, that the org is on legacy storage. **Needs:** a Gmail or Microsoft 365 test mailbox.
- [ ] **SLS-EAC-02** · 15 min · Take yourself out of the configuration but keep the permission set, then send another email. **Proves:** the configuration is the third gate — nothing is captured. **Needs:** SLS-EAC-01.
- [ ] **SLS-EAC-03** · 15 min · Add the Contact's domain to the configuration's exclusions and email them again. **Proves:** excluded mail reaches neither the timeline nor `EmailMessage`. **Needs:** SLS-EAC-01.
- [ ] **SLS-EAC-04** · 20 min · Switch capture to header-only, send an email with a subject and body, then query `Subject`, `TextBody` and `Source`. **Proves:** only sender, recipients and time are kept — copy the `Source` value you get. **Needs:** SLS-EAC-01.

## Related

- [Pipeline Inspection](pipeline-inspection.md) — shows activity data on each deal, and lost what legacy EAC reporting fed it
- [Lead Management & Conversion](lead-management-and-conversion.md) — the leads EAC matches captured email and events to
- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the opportunities whose activity timeline shows captured mail
- [SF_core · 07-security · 02 Licences & What They Gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) — why an EAC licence and its permission set are two separate assignments

## Sources

- [EAC Activity Metrics, Dashboard, Recommended Connections and A360 Reports Retirement](https://help.salesforce.com/s/articleView?id=005384640&language=en_US&type=1) — Salesforce Help KB 005384640, published 20 May 2026 · read 2026-09-24 · the four features, retirement *"Spring '27 (February 2027)"*; Sync Email as Salesforce Activity *"stores email data directly as standard Salesforce Activity records"*
- [Einstein Activity Capture (EAC): Sync Email as Activity and Enhanced Email](https://help.salesforce.com/s/articleView?id=005232917&language=en_US&type=1) — Salesforce Help KB 005232917, published 27 July 2026 · read 2026-09-24 · requires the Enhanced Email org setting; *"automatically enabled for all new orgs setting up EAC"*; the Outlook and Gmail integration setting can't be disabled
- [Salesforce Active Product & Feature Retirements](https://help.salesforce.com/s/articleView?id=000381744&language=en_US&type=1) — Salesforce Help KB 000381744, updated 17 August 2026 · read 2026-09-24 · *"EAC Activity Metrics, Dashboard, Recommended Connections and A360 Reports | Spring '27 - Feb 2027"*
- [Leverage Email Data with Sync Email as Salesforce Activity](https://help.salesforce.com/s/articleView?id=release-notes.rn_sales_productivity_eac_email_sync.htm&language=en_US&release=256&type=5) — Salesforce Help, Summer '25 release notes · via search 2026-09-24 · `EmailMessage` and `Task` records; entire message or header only; up to 180 days of historical email
- [Data Storage and Usage](https://help.salesforce.com/s/articleView?language=en_US&id=sales.activity_capture_data_storage_and_usage.htm&type=5) — Salesforce Help · via search 2026-09-24 · pre-Summer '25 email *"isn't available to reports or other platform tools"*; Task and Email Message records *"contribute to your org's core data storage"*; Activity Platform Hyperforce storage not counted
- [Data Retention and Deletion](https://help.salesforce.com/s/articleView?language=en_US&id=sales.aac_data_retention.htm&type=5) — Salesforce Help · via search 2026-09-24 · 6 months for Standard-only orgs, 24 months with one paid licence; retention runs from when the activity was added
- [Differences Between Einstein Activity Capture Editions](https://help.salesforce.com/s/articleView?language=en_US&id=sales.aac_standard_differences.htm&type=5) — Salesforce Help · via search 2026-09-24 · who gets Standard vs paid; Summer '25: legacy reporting unavailable unless set up earlier, including data in Pipeline Inspection and ECI
- [Upgrade Microsoft Office 365 Authentication Method to Microsoft Graph](https://help.salesforce.com/s/articleView?id=sales.eac_ews_graph.htm&language=en_US) — Salesforce Help · via search 2026-09-24 · set up before Spring '26 → *"upgrade to Microsoft Graph by October 1, 2026"*; no rollback to EWS
- [Give Users Access to Einstein Activity Capture](https://help.salesforce.com/s/articleView?language=en_US&id=sales.aac_setup_give_access.htm&type=5) — Salesforce Help · via search 2026-09-24 · licence, permission set and configuration membership
- [Events and Einstein Activity Capture](https://help.salesforce.com/s/articleView?language=en_US&id=sales.aac_guidelines_sync.htm&type=5) — Salesforce Help · via search 2026-09-24 · meeting data saved in event records; updates continuous, not real time
- [Select Who Can Use Inbox Features](https://help.salesforce.com/s/articleView?language=en_US&id=sales.inbox_setup_select_users.htm&type=5) — Salesforce Help · via search 2026-09-24 · *Inbox With Einstein Activity Capture* permission set
- [Outlook Integration and Einstein Activity Capture Setup](https://trailhead.salesforce.com/content/learn/modules/outlook_integration/outlook_integration_unit_3) — Trailhead · read 2026-09-24 · *"a matching number of Einstein Activity Capture Standard seats for every Sales Cloud license"*; configurations; excluding a person or company
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `EmailMessage.Source` values (API 64.0; *Migrated Captured Email* API 65.0); `UserEmailCalendarSync` (API 49.0); `ActivityUsrConnectionStatus.IsTermsOfServiceAccepted`, *"each user must accept the terms of service"*
- [Einstein Conversation Insights Implementation Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/eci_impl_guide.pdf) — Salesforce, Winter '27 · read 2026-09-24 · *"ECI can use Einstein Activity Capture calendar integration to match call participants with existing contact records"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
