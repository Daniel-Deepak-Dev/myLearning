# Event Monitoring & Transaction Security

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Shield's third pillar — seeing what users and integrations actually did, and acting on it while it happens. Configuration-change history is Setup Audit Trail ([01-admin · 17](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md)); field-value history is [22](22-field-audit-trail-and-data-retention.md).

> **What changed.** *"Write a Transaction Security policy in Apex against the legacy framework"* no longer applies — the **legacy Transaction Security framework was retired** and **Enhanced Transaction Security** replaced it, arriving automatically with Real-Time Event Monitoring. Two 2026 changes sit on top: managing policies now requires the **`Modify Transaction Security Policy`** permission alongside `Customize Application`, and Salesforce **auto-created a default report-export policy** in Shield and Event Monitoring orgs that had none.

## Core idea

Everything else in this area decides what a user *may* do. Event Monitoring records what they *did* — logins, API calls, report runs, exports, page views, Apex exceptions — as first-class data rather than as debug logs. Transaction Security is the layer that turns that stream into control: a policy watches a real-time event, evaluates a condition, and blocks, challenges or alerts **before the action completes**. That is the only place in the platform where access can be denied on behaviour rather than on configuration, which makes it the natural home for the things the permission model cannot express — *this user may run reports, but not export 400,000 rows at 2am from an unfamiliar country*.

## How it works

| | **Event Log Files** | **Real-Time Event Monitoring** |
|---|---|---|
| delivery | batch, hourly and daily — up to ~24h behind | streamed as it happens |
| access | `EventLogFile` object, CSV download | subscribe to the event, and query the big object with SOQL |
| retention | 1 day on the free tier, 30 days with Shield, **up to 1 year** opt-in since Summer '24 | stored objects, typically **180 days** and longer |
| can take an action | no — forensic only | **yes**, via Enhanced Transaction Security |

- **There is a free tier, and it is worth knowing.** Enterprise, Unlimited and Performance orgs get a handful of log types — Login, Logout, API Total Usage, Apex Unexpected Exception, CORS Violation, CSP Violation, Hostname Redirects — at **one day** of retention. Shield unlocks the full set (~74 types) and the longer windows.
- **A policy is event + condition + action.** Conditions are built in Condition Builder or written as an Apex class implementing the policy interface; actions are **Block**, **Require MFA** (step-up), **Notify**, **Freeze user** or **End session**.
- **`ApiAnomalyEvent`, `CredentialStuffingEvent` and `SessionHijackingEvent` are model-derived**, not rule-derived — the platform decides what is anomalous. Treat their output as a signal to investigate, not as a verdict.
- **`HostnameRedirects` is on the free tier and is exactly the log you need** to find integrations still calling legacy or instanced URLs before Winter '27. → [20](20-my-domain-enhanced-domains-and-trusted-urls.md)
- **The Event Monitoring Analytics app** ships prebuilt dashboards over the log files, which is usually faster than building the CSV pipeline yourself.

> **From my notes.** My 2025 page lists the use cases well — block logins from untrusted locations, cap API extractions, require MFA before a sensitive dashboard, alert on unusual report activity — and records that on the **GallagherRe project a policy was used to prevent report exports**. That bespoke control is now partly a platform default: in July 2026 Salesforce auto-created a `ReportEvent` policy in Shield and Event Monitoring orgs, with one important difference in posture — it **challenges** with step-up authentication rather than **blocks**. The page also says "Transaction Security Policies" without qualification; the framework it describes is the **Enhanced** one, and the legacy framework it inherits its name from is gone.

## 2026 currency

The auto-created policy is the unusual event: Salesforce provisioned security configuration into customer orgs. Its preconditions are narrow and worth memorising — **only** orgs with Shield or Event Monitoring, **only** where no `ReportEvent` policy already existed, triggering on **UI report exports over 10,000 rows**, **internal users only**, and **fully editable** afterwards. Sandboxes saw it from 22 June 2026, production from 13 July 2026. Separately, `Modify Transaction Security Policy` split policy management out of `Customize Application`, so an admin who could manage policies in June may not be able to in August. The full dated wave is in [../CURRENCY.md](../CURRENCY.md); the step-up mechanics are [18](18-session-security-login-policies-and-step-up.md).

## Gotchas

- **Two orgs on the same release now behave differently on report export**, depending on whether they hold a Shield or Event Monitoring licence. Neither admin changed anything.
- **Event log files are not real time.** Building an alerting story on them produces alerts up to a day late — that is what Real-Time Event Monitoring is for.
- **The free tier's one-day retention means the evidence is gone before the question is asked.** If logs matter, they must be exported on a schedule.
- **A Block action is a production incident waiting to happen.** Deploy new policies in log-only or Notify mode first and read the results for a fortnight.
- **Policies evaluate per event, not per session** — a threshold expressed "per day" needs to be built from the data, not assumed.
- **Real-time event storage is big-object storage**, so querying it obeys index-order rules rather than arbitrary `WHERE`. → [22](22-field-audit-trail-and-data-retention.md)
- **Event Monitoring shows access, not authorisation.** It tells you a user read 40,000 records; whether they were *allowed* to is still [15](15-auditing-and-troubleshooting-access.md).

## Recall

Q: What replaced the legacy Transaction Security framework, and what enables it?
A: Enhanced Transaction Security, which you get automatically with Real-Time Event Monitoring.

Q: What are the three parts of a Transaction Security policy?
A: An event type, a condition (Condition Builder or an Apex class), and an action — Block, Require MFA, Notify, Freeze user, or End session.

Q: Under exactly what conditions did Salesforce auto-create a report-export policy in 2026?
A: Orgs with Shield or Event Monitoring, with no existing `ReportEvent` policy — triggering on UI report exports over 10,000 rows, internal users only, and editable.

Q: What does the Event Monitoring free tier give an Enterprise Edition org?
A: About seven log types — including Login, Logout, API Total Usage and Hostname Redirects — at one day of retention.

Q: Which permission is now needed to manage Transaction Security policies?
A: `Modify Transaction Security Policy`, in addition to `Customize Application`.

## Related

- [18 · Session security, login policies & step-up](18-session-security-login-policies-and-step-up.md) — the step-up mechanism the report-export policy invokes
- [22 · Field Audit Trail & data retention](22-field-audit-trail-and-data-retention.md) — the other Shield pillar built on big objects
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — what the user was *allowed* to do, as opposed to what they did
- [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md) — Event Monitoring as the production-debugging tier above capped debug logs
