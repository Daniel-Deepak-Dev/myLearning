# Setup Audit Trail, monitoring & usage

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** The free monitoring surfaces in Setup — who changed config, what the org is doing, and what it is consuming. Shield Event Monitoring and Field Audit Trail are [07-security](../07-security-and-sharing/INDEX.md).

## Core idea

Every org accumulates two kinds of history: **who changed the configuration** and **what the users and jobs are doing**. Setup Audit Trail answers the first, and the answer has a hard shelf life — 180 days, downloadable, and no longer. The Lightning Usage App, Storage Usage and the job monitors answer the second. None of these cost anything, none are on by default in anyone's habits, and the audit trail in particular is the one artefact an architect wishes existed retrospectively — which is why exporting it on a schedule is a design decision, not an admin chore.

## How it works

- **Setup Audit Trail** — Setup → *View Setup Audit Trail*. The page lists the **20 most recent** setup changes: date, user, and what changed. **Download** gives the full **180-day** history as CSV.
- **The Delegate User column** matters for support workflows: when an admin acts after being granted login access, the acting admin appears as *Delegate User* and the user who granted access appears in *User*.
- **Lightning Usage App** — App Launcher → *Usage* → **Lightning Usage**. Tabs under ACTIVITY and USAGE cover daily active users, **users switching to Salesforce Classic per day**, most-visited pages, browser mix and page-performance timings. It is also the quickest read on login and MFA adoption.
- **Storage Usage** — Setup → *Storage Usage* for org data and file limits; per user, Setup → *Users* → the user → **View** beside *Used Data Space* / *Used File Space*.
- **Job and delivery monitors:** Apex Jobs, Scheduled Jobs, Bulk Data Load Jobs, Deployment Status, Paused Flow Interviews, Debug Logs, Login History, Email Log Files. Each is a different question; none of them is the audit trail.

| Question | Surface | Retention |
|---|---|---|
| Who changed this config? | Setup Audit Trail | **180 days** |
| Who changed this *record*? | Field History / Field Audit Trail | field history 18–24 months |
| Is anyone still on Classic? | Lightning Usage App | rolling window |
| Why is the org near a limit? | Storage Usage, Bulk Data Load Jobs | current state |

## 2026 currency

**Setup with Agentforce writes its changes to the Setup Audit Trail** — an agent acting in Setup is attributable exactly like an admin, which is what makes the review discipline in [19](19-agentforce-in-setup-and-ai-assisted-admin.md) workable. Treat the audit trail as the control that makes AI-assisted configuration auditable, and check it after any agent-assisted change.

## Gotchas

- **180 days is the whole history.** No setting extends it. If an org needs a longer trail, something must export the CSV on a schedule and store it elsewhere — decide that before you need it.
- The UI's 20 rows mislead people into thinking that is all there is; the answer is almost always in the download.
- The audit trail records **setup** changes, not **data** changes. "Who edited this Opportunity?" is field history, a different feature with different retention.
- Not every change type is logged in the detail you'd want; the trail tells you a change happened and by whom, not always the before-and-after value.
- A change made by an installed package or by a deployment shows as the deploying user — attribution stops at the pipeline, so the git history is the real record. → [09-devops](../09-devops-sfdx-and-release-management/INDEX.md)
- Lightning Usage App data is aggregated with a lag; it answers adoption questions, not "what did this user do five minutes ago" (that is Login History or Event Monitoring).
- File storage fills quietly and is usually attachments, not records — check *Used File Space* before assuming a data-volume problem.
- Deleted setup metadata still appears in the trail; the trail is not a list of what currently exists.

## Recall

Q: How much setup history does Setup Audit Trail keep, and how do you get all of it?
A: 180 days. The page shows only the 20 most recent changes — click **Download** for the full CSV.

Q: What does the Delegate User column mean?
A: A delegate (such as an admin using granted login access) made the change; the *User* column shows the user who granted access.

Q: Which surface tells you whether users are still falling back to Salesforce Classic?
A: The Lightning Usage App — it reports switches to Classic per day alongside active users and page views.

Q: An agent in Setup created a field. Is that attributable?
A: Yes — Setup with Agentforce changes are recorded in the Setup Audit Trail like any other admin change.

Q: Setup Audit Trail cannot answer which question?
A: Who changed a record's field value — that is field history / Field Audit Trail, not the setup trail.

## Related

- [02 · Release cadence & Release Updates](02-release-cadence-and-release-updates.md) — what to check after an auto-enforced update lands
- [19 · Agentforce in Setup & AI-assisted admin](19-agentforce-in-setup-and-ai-assisted-admin.md) — why the audit trail is the control for agent-made config
- [07-security · INDEX](../07-security-and-sharing/INDEX.md) — Event Monitoring, Field Audit Trail and the paid tier of this story
