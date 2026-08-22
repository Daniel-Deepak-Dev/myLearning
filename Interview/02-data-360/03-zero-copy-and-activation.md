# Data 360 — Zero Copy & Activation

> Area: Data 360 · Set 03 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the decisions that get made in a proposal and discovered in month three. Federation status labels, inherited performance, and the two words clients hear differently from how you mean them — "zero copy".

---

### Q1 · Federated everything

**Level:** Complex · **Probes:** [Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md)

**Scenario.** A retail group's data team spent four months federating their Snowflake estate into Data 360 via AWS Glue rather than ingesting any of it — the reasoning was sound at the time: 40TB of customer and transaction data, a hard "no duplication" position from their data governance board, and no appetite for an ETL programme. It works. Now phase two begins: identity resolution across Snowflake customer records plus the CRM plus a loyalty platform, segments for activation, and a service agent grounding on unified profiles. Nothing in phase two is behaving as designed, and the data team's position is that Data 360 was mis-sold.

**Asked as:** "They avoided a migration and now phase two doesn't work. Were they mis-sold?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Not mis-sold — they made the right phase-one decision and then assumed it generalized. Zero copy is the **reach** leg of grounding, and reach is not the same as the ability to run Data 360's own features over the data. **Not every Data 360 feature works identically on federated data**, and identity resolution and segmentation are exactly where that bites.

**Then work through.**
- **Name the trap precisely, because it runs in both directions.** Teams federate everything to avoid duplication and then discover identity resolution and segmentation need the data locally; or they ingest everything and pay to store what a query could have reached. This client hit the first one. It is a known failure mode, not bad luck, which also means the answer is not "start again."
- **Do not re-litigate phase one.** 40TB, a governance prohibition on copying, and no ETL appetite — federation was correct for analytics and reach, and it delivered. The error is that "no duplication" was adopted as an architectural principle rather than as a constraint to be tested per use case.
- **The decision is per dataset, and here is the test.** Choose **zero copy** when the data is large and expensive to duplicate, already governed where it lives, freshness matters and the source is current, or compliance forbids copying. Choose **ingestion** when you need Data 360 features on it — identity resolution, segmentation performance — when the source cannot serve interactive queries, when you need predictable query latency, or when it is needed for **real-time agent grounding**. Phase two is three items from the right-hand column.
- **So the shape of the answer is hybrid, and it is smaller than they fear.** Ingest the *identity-bearing and grounding-relevant* slice — the customer attributes matching runs on, the transaction aggregates segments filter, whatever the agent grounds on. Leave the bulk of the 40TB federated, because most of it is analytical depth that nothing in phase two touches. That is a fraction of the estate, which is the number to put in front of the governance board rather than "we need to copy 40TB."
- **Reframe it for the governance board in their own terms.** Their position was about uncontrolled duplication. A defined, minimal, governed subset ingested for a named purpose is a different proposition from a bulk copy, and it is one a governance board can actually approve. Note also that ingestion **is** the classic ETL/ELT path — that is worth saying plainly rather than dressing up, because the board will recognise it and trust the answer more for being named.
- **And check the thing they have probably not checked.** Query performance under federation is inherited from the source. If phase two's grounding queries were going to hit Snowflake live, agent latency becomes Snowflake's provisioning problem — an operational dependency on whoever owns the warehouse, which belongs in a design conversation now rather than a production incident later.

**The trap.** Accepting the mis-sold framing and proposing to ingest the estate — a 40TB migration, the exact programme they successfully avoided, plus a fight with the governance board they will lose. It is the answer that follows from taking "federation doesn't support phase two" as a global fact instead of a per-feature one, and it turns a scoping correction into a project restart.

**Follow-ups they will ask.**
- "How do you decide which fields are identity-bearing?" — the fields the match rules run on, which is a data-modeling decision made before identity resolution. The primary key especially: it is consumed by matching and changing it later is painful.
- "Is federated data cheaper?" — not free. You avoid Data 360 storage and you pay source-side compute on **every query**. For high-frequency agent grounding that can invert the comparison entirely.
- "Would you have caught this in phase one?" — yes, by asking what phase two needed before committing to a federation-only architecture. The one-paragraph deliverable — for this dataset, which of the two and why — is what that looks like as a habit.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Refuses the mis-sold framing without dismissing the complaint, names the known both-directions trap, proposes a hybrid with the ingested slice scoped to identity-bearing and grounding-relevant data, and reframes it for the governance board |
| 🟡 Partial | Identifies that identity resolution needs local data and proposes selective ingestion, but does not scope it or address the governance position |
| 🔴 Weak | Proposes ingesting the estate; or defends the federation-only design; or agrees they were mis-sold |

**Ask this if they stall:** "Identity resolution matches on DMO fields. Where do those fields live right now, and what has to happen for a ruleset to run over them?"

</details>

---

### Q2 · The word in brackets

**Level:** Medium · **Probes:** [Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md)

**Scenario.** You are reviewing a colleague's proposal the day before it goes to a client. The architecture diagram shows Data 360 federating the client's **Microsoft Fabric OneLake** estate as the primary grounding source for a customer-service agent. It is drawn as a solid line, described as "zero-copy federation to OneLake", and the delivery plan has a go-live date twelve weeks out with a payment milestone attached to it. Your colleague has a working demo.

**Asked as:** "The demo works. What is your objection?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Fabric OneLake federation is **Beta**. It carries no support commitment, and this proposal makes it load-bearing for a dated go-live with money attached. The demo working is not the question — Beta means it may change, may not be supported, and cannot be escalated the way a GA capability can.

**Then work through.**
- **Read the label literally.** That is the whole discipline here, and it is the single most practical distinction in the topic. **AWS Glue Data Catalog federation is GA and is proposal-safe** — you can commit to it. **Fabric OneLake is Beta**: fine to prototype, fine to demo, and it must not become load-bearing in a delivery plan.
- **Why it matters more than it sounds.** "Is this GA?" is the question that decides whether a capability goes in a delivery plan or stays in a demo. Getting it wrong is the kind of mistake that surfaces three months into a project — which is roughly the twelve-week go-live, so the exposure lands exactly when the milestone does.
- **What to change in the proposal.** Three things, none of which kill it. Draw the OneLake line as Beta and say so in the text. Move the payment milestone off it. And name the fallback: either the client's data reachable through a GA path, or ingestion for the slice the agent actually grounds on. A proposal that names its own risk and its fallback is stronger with a client's architecture reviewer, not weaker.
- **Then the question worth asking your colleague.** Does the design *need* OneLake federation, or is it there because that is where the data happens to sit? If the agent grounds on a modest slice, ingesting that slice is GA, predictable, and removes the dependency entirely. The Beta capability may be solving a problem the design does not have.

**The trap.** Treating "the demo works" as evidence that the risk is theoretical. It is the most persuasive argument in the room and it is answering a different question — Beta is a *support and stability* commitment, not a statement about whether the feature functions today. A Beta capability that works perfectly and then changes behaviour in a release, with no support path, is the scenario the label exists to warn about.

**Follow-ups they will ask.**
- "The client is a Microsoft shop and will push back." — then say it plainly: the capability is coming, it is Beta today, and here is what we commit to now versus what we adopt when it goes GA. Clients accept a staged answer; they do not accept a missed milestone.
- "What else in that status table is worth knowing?" — AWS Glue federation GA, Accelerated Data Ingest GA as the copy-based alternative, and Databricks file federation gaining **identity-provider authentication** in Summer '26.
- "Why does the Databricks IdP change matter?" — because "can we govern this connection centrally?" is the question that stalls zero-copy projects, not the technology. Central IdP auth is often what gets a connection through security review. It is an unblocker rather than a feature.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names OneLake as Beta and AWS Glue as GA unprompted, separates "it works" from "it is supported", moves the payment milestone, and asks whether the design needs federation at all |
| 🟡 Partial | Raises Beta as a risk and suggests a caveat in the proposal, but leaves it load-bearing and dated |
| 🔴 Weak | Accepts it because the demo works; or objects on general caution with no knowledge of the status table |

**Ask this if they stall:** "Twelve weeks in, the connector's behaviour changes in a release. What is your support path?"

</details>

---

### Q3 · The agent is slow on Monday mornings

**Level:** Medium · **Probes:** [Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) · [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md)

**Scenario.** A B2B client's service agent grounds partly on order history federated from BigQuery. Response times are fine most of the week — under two seconds — but between 8am and 10am on Mondays the agent takes eight to twelve seconds and occasionally times out. The Agentforce side shows nothing unusual. The client has opened a case with Salesforce and copied you in, asking you to escalate it.

**Asked as:** "They want you to escalate to Salesforce. What do you say?"

<details><summary><b>Model answer</b></summary>

**Lead with.** This is almost certainly not a Salesforce problem to escalate. Under zero copy, **query performance is inherited from the source** — if BigQuery is slow or under-provisioned at query time, Data 360 is slow, and so is any agent grounded on it. A weekly time-of-day pattern is the signature of contention in the warehouse, not of anything in Agentforce.

**Then work through.**
- **What to look for, and it is on the client's side.** Monday 8–10am is when scheduled analytics jobs and week-start reporting typically run. Ask the warehouse owner what runs in that window and how BigQuery is provisioned for concurrency. The agent's grounding query is competing with a reporting workload for the same compute.
- **Why the Agentforce side showing nothing is confirmatory rather than puzzling.** The agent is waiting on a federated query. From Agentforce's perspective nothing is wrong — it is doing exactly what it was asked and the latency is downstream.
- **Say the uncomfortable part.** This is a **genuine operational dependency**, and it belongs in a design conversation with whoever owns the warehouse. It usually is not, which is why it gets discovered as a production incident. The client's agent SLA is now partly owned by a team that never agreed to one.
- **Three fixes, and they are different commitments.** Provision BigQuery for the concurrency — the warehouse owner's call, and it costs money. Move the analytics jobs out of the window — cheapest if politically possible. Or **ingest the order-history slice the agent grounds on**, which gives predictable query latency and removes the dependency, at the cost of storage and a freshness decision. Predictable latency and real-time agent grounding are both explicitly reasons to choose ingestion over federation.
- **Recommend the third for the agent path specifically.** An agent's latency budget should not depend on a warehouse's Monday-morning reporting schedule. Federation stays right for the analytical bulk; the grounding slice is the part that needs to be predictable.

**The trap.** Escalating it, because the client asked and it is the path of least friction. It burns support cycles, and when Salesforce comes back with "the federated query took eleven seconds", the client has lost two weeks and you have lost the credibility to say what you could have said now. The related trap is proposing a timeout increase — it converts a timeout into a twelve-second wait, which is not a fix and is arguably worse for the rep on the call.

**Follow-ups they will ask.**
- "How do you prove it before making the claim?" — compare query latency federated versus ingested for the same dataset, and correlate the slow window against the warehouse's own query logs. The number is the argument.
- "Is federation cheaper here?" — you avoid Data 360 storage, and you pay source-side compute on every query. For agent grounding at volume that is a recurring cost, not a saving.
- "Would Accelerated Data Ingest help?" — that is for CRM data. This is BigQuery, so the option is a normal ingestion path with a refresh cadence chosen against how fresh order history actually needs to be for the agent.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Declines the escalation with a reason, identifies the Monday window as warehouse contention, names the operational dependency as a design gap, and recommends ingesting the grounding slice specifically rather than the whole estate |
| 🟡 Partial | Suspects the source system and suggests investigating BigQuery, but escalates anyway or offers no structural fix |
| 🔴 Weak | Escalates; or investigates Agentforce; or raises the timeout |

**Ask this if they stall:** "The agent is waiting on something. Where is the query actually executing?"

</details>

---

### Q4 · Zero copy, zero cost

**Level:** Complex · **Probes:** [Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) · [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md)

**Scenario.** Four months into a Data 360 programme, the client's finance director calls a review. Three costs have overshot: their Snowflake bill is up 60%, the Data 360 profile count is 1.9× the estimate, and Marketing Cloud activation volumes are triple what was forecast. The original business case said "zero-copy architecture — no data duplication cost." The finance director's opening line is that they were told this would be cheaper.

**Asked as:** "Three overruns, one business case. Take it apart."

<details><summary><b>Model answer</b></summary>

**Lead with.** Three unrelated costs, and the business case conflated them under one phrase. **"Zero copy" is a marketing-friendly term that clients hear as "no cost" or "no work"** — and the honest answer is that it removes *Data 360 storage* cost and nothing else. Each of the three overruns has a different owner and a different fix.

**Then work through, one at a time.**
- **The Snowflake bill — this one is the direct consequence of the architecture.** Federated is not free: you avoid Data 360 storage and you pay **source-side compute on every query**. Sixty percent up means the query volume was never modelled — likely agent grounding and segment evaluation hitting Snowflake far more often than the business case assumed. The fix is to identify the highest-frequency query paths and ingest those specific datasets. Federation is right for what is queried occasionally; it inverts for anything queried constantly.
- **The profile count — unrelated to zero copy entirely.** Under the March 2026 profile-based SKU you are billed on **unified profiles after identity resolution**, at roughly $240 per 1,000 baseline. 1.9× the estimate is either under-matching fragmenting customers across several profiles, or duplicate-heavy sources inflating the count at ingestion. Diagnose with the profile-count-to-source-row ratio. And say the hard part: **do not fix this by loosening the ruleset**, because over-matching is the cheaper direction and it is a privacy incident. The precision routes — a shared customer ID, a reliable email rule — are the legitimate way to close it.
- **The activation volumes — a configuration problem, not an architecture one.** Segment refresh cadence and publish schedule are cost levers, and **over-publishing to activation targets costs without benefit**. Match cadence to the activation target's own rhythm, not to "as often as possible". Triple the forecast usually means segments refreshing and republishing far more often than Marketing Cloud consumes them. This is the cheapest of the three to fix and worth leading with for that reason.
- **Then the structural point about the business case itself.** It priced storage, which was the one cost zero copy actually removes, and left three metered dimensions unmodelled: source-side query compute, unified profiles, and activation volume. That is the finding — not that the architecture was wrong, but that the cost model covered one axis of a four-axis system.

**How to handle the room.** Concede the business case was incomplete, because it was, and do it first — the finance director's grievance is legitimate and arguing it costs you the rest of the meeting. Then separate what was an architecture decision (federation, still defensible) from what was a modelling omission (three unmetered dimensions) and what is straightforward remediation (activation cadence, today; profile precision, weeks; selective ingestion, scoped). Give a revised model with all four axes and the assumptions visible, so the next review is against numbers rather than a phrase.

**The trap.** Defending "zero copy" as technically accurate. It is technically accurate — no data was duplicated — and it is exactly the reading that produced this meeting. **Set the expectation early** is the actual lesson, and the moment for it was the business case. Litigating the wording now reads as evasion and forfeits the credibility you need to be trusted with the revised model. The second trap is fixing the profile count the cheap way to make one number go away in front of a finance director who would approve it.

**Follow-ups they will ask.**
- "Which do you fix first?" — activation cadence: fastest, cheapest, no architectural change. Then profile precision, since it is a recurring line item. Then selective ingestion, which needs analysis to scope.
- "Was federation the wrong call?" — no, and be clear about that. 40TB estates and governance prohibitions are real, and it delivered reach without a migration. The error is that reach was priced and query volume was not.
- "How would you have modelled it upfront?" — four axes: Data 360 storage, source-side query compute at expected query volume, unified profiles at the expected match ratio, and activation volume at the target's consumption rhythm. Then state the assumptions, because the assumptions are what a review can check.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Separates three unrelated cost drivers, knows zero copy removes only Data 360 storage while source compute is per-query, refuses to loosen matching to cut the profile count, concedes the business case first, and returns a four-axis model |
| 🟡 Partial | Explains that federated queries cost source compute and that profiles are billed post-resolution, but blends the three overruns or misses the activation cadence lever |
| 🔴 Weak | Defends the wording of the business case; or attributes all three to the architecture; or proposes looser matching to bring the profile count down |

**Ask this if they stall:** "Which of those three numbers would have changed if they had ingested everything instead?"

</details>
