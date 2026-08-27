# Session Security, Login Policies & Step-Up

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Everything the platform decides *after* the credential check in [17](17-authentication-and-mfa.md) — where a login may originate, how long it lasts, how strong it is held to be, and what forces a user to re-prove identity mid-session.

## Core idea

A session is not a boolean. Salesforce tags every session with an **assurance level**, and individual permissions, connected apps and now individual *actions* can demand a higher level than the one the user arrived with. That is the mechanism behind the whole 2026 hardening wave: instead of making every login painful, the platform lets ordinary work proceed at standard assurance and raises the bar at the moment something sensitive happens. Understanding it is what separates "turn on MFA" from a design that survives an audit — because the same three settings (session level, login IP ranges, step-up period) also decide whether an integration silently starts failing.

## How it works

| Control | Where | What it decides |
|---|---|---|
| **Session Security Level** | Session Settings; per login method | *Standard* or *High Assurance* for sessions from that method |
| **Session-level policies** | profile / permission set → *Session Activation Required* | which permissions only activate in a high-assurance session |
| **Login IP Ranges** | profile (hard block) and *Trusted IP Ranges* (org-wide, skips verification) | where a login may originate |
| **Login Hours** | profile | when — and it ends an in-flight session at the boundary |
| **Step-Up Authentication Period (Minutes)** | Session Settings, **1–120** | how long a completed step-up verification stays valid |
| **Login Flows** | Setup → Login Flows, per profile | a screen flow injected *after* authentication, before the app |

- **Profile Login IP Ranges block; org-wide Trusted IP Ranges do not.** Outside a *trusted* range a user is challenged; outside their *profile* range they cannot log in at all. Confusing the two produces both false lockouts and false confidence.
- **`Enforce login IP ranges on every request`** in Session Settings extends the check from the login moment to every subsequent request — which is what makes an IP range a session control rather than a door policy.
- **Step-up is triggered by an action, not by the login.** The first enforced trigger is **report export of more than 10,000 rows through the UI**, internal users only, and it prompts for the user's MFA method.
- **Login IP restrictions are an exemption path from that prompt** — step-up on report export is skipped when the profile has login IP restrictions and either the user's IP is unchanged since login or *Enforce login IP ranges on every request* is on.
- **A login flow can deny the login**, set a session level, or collect something (an acceptance, a second factor of your own). It runs for the profiles you assign it to and is the supported place for custom post-authentication logic.

## 2026 currency

Step-up authentication for report export reached production in **July 2026**, and it arrived attached to a Transaction Security Policy rather than a checkbox — in orgs with Shield or Event Monitoring and no existing `ReportEvent` policy, Salesforce **auto-created a default one**, fully editable. That is unusual and worth internalising: the platform provisioned security configuration into customer orgs. The policy side, and the new `Modify Transaction Security Policy` permission needed to touch it, are owned by [23](23-event-monitoring-and-transaction-security.md). The dated wave this belongs to is in [../CURRENCY.md](../CURRENCY.md). Also new: **login IP restrictions on profiles moved from best practice to expectation** in the same wave, which makes the exemption rule above a design lever rather than trivia.

## Gotchas

- **The auto-created policy landed only in Shield and Event Monitoring orgs.** Two orgs on the same release can behave differently on report export, and neither admin changed anything.
- **10,000 rows is a UI-export threshold**, not an API one. Bulk API and Analytics extracts are governed elsewhere. → [06-integration · 24](../06-integration-and-apis/24-api-limits-monitoring-and-access-control.md)
- **Login Hours terminate a session mid-work**, they do not merely prevent new logins — users lose unsaved work at the boundary.
- **Session timeout is per profile and silently generous by default.** It is one of the first things Health Check flags. → [24](24-security-center-and-health-check.md)
- **A high-assurance requirement on a permission does not warn the user usefully** — the permission simply appears absent, which sends the investigation to the permission set. → [15](15-auditing-and-troubleshooting-access.md)
- **Login IP ranges break integrations from new IPs**, and cloud middleware changes egress IPs without telling you. That is a change-management dependency, not a one-time setting.
- **A login flow that errors locks out every user on that profile.** Test it against a sandbox profile you are not using to log in.
- **Session-based permission sets look inactive to any audit taken outside the qualifying session.** → [04](04-permission-set-groups-and-muting.md)

## Recall

Q: What is the difference between profile Login IP Ranges and org-wide Trusted IP Ranges?
A: The profile ranges block login outright. Trusted ranges only skip identity verification — outside them the user is challenged, not refused.

Q: What triggers step-up authentication as first enforced in 2026?
A: Exporting more than 10,000 rows from a report through the UI, for internal users.

Q: What is the Step-Up Authentication Period, and what are its bounds?
A: How long a completed step-up verification stays valid before the user is asked again — settable from 1 to 120 minutes.

Q: How can an org legitimately avoid the report-export prompt?
A: Login IP restrictions on the profile, with either an unchanged IP since login or *Enforce login IP ranges on every request* enabled.

Q: What does a login flow let you do that Session Settings cannot?
A: Run arbitrary screen-flow logic after authentication and before the app — collect an acceptance, add a custom factor, set the session level, or block the login.

## Related

- [17 · Authentication & MFA](17-authentication-and-mfa.md) — the credential check this note picks up from
- [23 · Event Monitoring & Transaction Security](23-event-monitoring-and-transaction-security.md) — the policy that actually implements report-export step-up
- [24 · Security Center & Health Check](24-security-center-and-health-check.md) — where weak session settings surface as a score
- [04 · Permission Set Groups & muting](04-permission-set-groups-and-muting.md) — session-based activation, the older use of assurance levels
