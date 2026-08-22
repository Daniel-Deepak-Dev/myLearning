# Data 360 — Ingestion & Modeling

> Area: Data 360 · Set 01 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the layer everything downstream inherits. A mapping mistake does not stay local — it propagates into identity resolution, insights, segments and every answer an agent gives, and it is expensive to unwind once things are built on top.

---

### Q1 · Zero rows, no error 🆕

**Level:** Medium · **Probes:** [Data modeling DSO → DLO → DMO](../../AI_Data/01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) · [Query anatomy & the SOQL model](../../SF/10-soql-and-sosl/01-query-anatomy-and-the-soql-model.md)

**Scenario.** A developer has written an Apex-backed agent action that queries a DLO with SOQL. It returns zero records. No exception, no error in the debug log, no FLS violation. They have spent the afternoon on it: checked the `WHERE` clause against the data, confirmed the records exist in the Data 360 UI, verified the running user's permissions, rewritten the filter three ways, and added `LIMIT 1` with no filter at all — still zero. They are now convinced it is a platform bug and want to raise a case.

**Asked as:** "Zero rows, no error, records visibly exist. What is it?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The query is missing the **dataspace**. A DLO query without one silently returns zero records — no error, no warning — and zero rows looks exactly like "no matching data", which is why an afternoon disappears into the `WHERE` clause.

**Then work through.**
- **The fix.** Specify the dataspace in a `SET OPTIONS` clause, and note where it goes: **at the very end of the query.** Not after the `FROM`, not before `ORDER BY`. Getting the position wrong is the second mistake people make after learning about the clause.
- **Why `LIMIT 1` with no filter was the diagnostic they should have trusted.** Stripping the filter entirely and still getting nothing rules out the `WHERE` clause completely. At that point the query is not the problem — the query's *context* is. That reasoning step is what separates a systematic debugger from someone rewriting filters hopefully.
- **The general principle, which is the point of the question.** **DLOs are not Platform objects.** They are lake tables, and carrying over assumptions about semantics, indexing and behaviour is where this whole class of bug comes from. `SET OPTIONS` is the seam where the difference becomes explicit.
- **The sibling gotcha, worth naming in the same breath.** `honorEmptyStrings` controls whether Data 360 treats `NULL` and `''` as distinct. The default (`false`) collapses them the way Platform objects do; lake data often does not *mean* it that way. That one is nastier than the dataspace trap because it returns rows — just not the right ones. Wrong-but-plausible beats obviously-broken every time for how long it survives.
- **Same trap on the newer path.** Summer '26 added running **SQL from Apex** against Data 360, which is a genuine capability increase — SOQL cannot express the joins, aggregations and window functions lakehouse work needs. The dataspace requirement applies there identically.

**The trap.** Raising the platform case. It burns a day of support cycles, and the "no error on a missing dataspace" behaviour is documented rather than defective. The deeper trap is the instinct behind it: after five failed hypotheses about the filter, the conclusion was "the platform is wrong" rather than "my model of what this query runs against is wrong."

**Follow-ups they will ask.**
- "Why would the platform not error?" — the query is valid and executes; without a dataspace there is simply nothing in scope. It is an empty result, not a malformed request.
- "How do you stop the whole team hitting this?" — the fifteen-minute lab: run the query without `SET OPTIONS`, watch zero records with no error, then add the dataspace. Once seen, never forgotten. Better as a shared runbook step than as folklore.
- "What is the equivalent risk on the `honorEmptyStrings` side?" — a segment or insight whose row counts are quietly wrong, so nobody investigates, and the number ends up in front of a client.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names the dataspace immediately, knows `SET OPTIONS` goes at the end of the query, and generalizes to "DLOs are not Platform objects" — bonus for volunteering `honorEmptyStrings` as the nastier sibling |
| 🟡 Partial | Reasons that the query must be running against the wrong scope, without knowing the specific clause |
| 🔴 Weak | Keeps debugging the filter, permissions or FLS; or endorses the platform case |

**Ask this if they stall:** "They removed the `WHERE` clause entirely and still got nothing. What does that rule out, and what does it leave?"

</details>

---

### Q2 · Fresh enough for the dashboard

**Level:** Medium · **Probes:** [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md) · [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md)

**Scenario.** A utilities client has 23 data streams into Data 360, all on a nightly batch refresh — a configuration inherited from an analytics project two years ago and never revisited. They are now adding a service agent that answers "what is the status of my outage report?" A junior consultant has proposed moving all 23 streams to streaming ingestion "so everything is real-time." The client's data team has pushed back on cost. The agent goes live in three weeks.

**Asked as:** "Both sides have a point. What do you actually do?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Neither position — the decision is **per data stream, not per project**, and framing it as one setting is what produced both the two-year-old nightly default and the proposal to flip everything. Most projects either over-refresh everything, which costs money invisibly, or under-refresh the one stream an agent depends on, which produces the failure that gets blamed on the model.

**Then work through.**
- **The rule.** If an agent grounds on it, it needs to be real-time. If a dashboard reads it, scheduled is fine.
- **Classify all 23 with four questions.** Does an *agent* read this? → real-time. Does a *segment* use it for activation? → match the activation cadence, not "as often as possible". Does only a *dashboard* read it? → scheduled is fine. Is it historical or immutable? → one-time load. That audit is a day of work and it is the actual deliverable here.
- **For the outage-status stream specifically, the answer is not streaming.** It is CRM data, so **Accelerated Data Ingest** — GA in Summer '26 and the default for CRM going forward. Real-time with no pipeline lag, and it is the purpose-built path rather than a generic streaming connector.
- **Name the failure the client is three weeks from shipping.** An agent grounded on a nightly stream will tell a customer their outage report is open when it was resolved at 6am. The signature is distinctive: **fluent, specific, and wrong**, and everyone blames the model. It is not the model. It was told the case was open.
- **The junior consultant's instinct is right about the agent and wrong about the other 22 streams.** The data team's cost objection is right about the 22 and wrong about the outage stream. Say both out loud — this is a scenario where the interviewer is watching whether you can decline a false choice without dismissing either party.

**The trap.** There are two, and they are opposites. Flipping everything to streaming is a recurring cost with no proportionate benefit for streams only a dashboard reads. But the trap in the *other* direction is worse and more tempting under time pressure: leaving the outage stream on nightly and having the agent action call CRM directly for freshness. That works, and it costs you the unified profile and its governance, and it quietly reintroduces the sharing problems Data 360 was there to solve. **Accelerated Data Ingest exists precisely so you do not have to do that.**

**Follow-ups they will ask.**
- "How do you demonstrate the risk to the client rather than assert it?" — ground the agent on the nightly stream in a sandbox, change the source record, and ask the agent before the refresh. Watching it answer confidently and wrongly is the argument.
- "What does over-refreshing actually cost?" — it is a cost lever on every stream, and invisible because nothing breaks. Which is why an inherited configuration survives two years unexamined.
- "Where does ingestion's job end?" — at the DLO. Landing data does nothing useful until it is mapped to a DMO, and new starters routinely think they are done at ingestion.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Rejects the per-project framing, gives the agent/segment/dashboard classification, names Accelerated Data Ingest for the CRM stream specifically, and identifies "call CRM directly from the action" as the tempting wrong answer |
| 🟡 Partial | Says decide per stream and prioritize the agent-facing one, but reaches for generic streaming rather than Accelerated Data Ingest |
| 🔴 Weak | Picks a side — everything streaming, or leave it and monitor; or proposes bypassing Data 360 for freshness |

**Ask this if they stall:** "The agent tells a customer their outage is unresolved. It was fixed at 6am. Whose fault is that going to look like?"

</details>

---

### Q3 · Fourteen custom DMOs

**Level:** Complex · **Probes:** [Data modeling DSO → DLO → DMO](../../AI_Data/01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md)

**Scenario.** You are reviewing a Data 360 implementation six months in. Seven source systems have been ingested. The team created **fourteen custom DMOs** — roughly one per source, plus a few variants — because "the standard DMOs didn't quite fit our fields." Identity resolution currently produces a profile count 2.8× the estimated customer base. Four calculated insights and eleven segments are built on top. The client is now asking why their agent gives inconsistent answers about the same customer depending on how the question is phrased.

**Asked as:** "Where do you start, and what do you tell them it will cost?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The custom DMOs are the root cause and everything else on that list is a symptom. A custom DMO per source **recreates the silos Data 360 was there to remove** — and standard DMOs exist precisely so cross-source consistency is possible. The 2.8× profile count and the inconsistent agent answers are both downstream of that one decision.

**Then work through the causal chain, because the client needs to see it as one problem rather than four.**
- **Matching runs on DMO fields.** With customer data spread across fourteen unaligned DMOs, identity resolution has nothing consistent to match on. That is the 2.8× — the same person is arriving as several unrelated shapes and staying several profiles.
- **Insights compute per unified profile**, so four insights over fragmented profiles produce wrong metrics. Not missing — *wrong*, which is worse, because a number renders fine and nobody investigates it.
- **Segments filter those DMOs and insights**, so eleven segments are built on the same fault.
- **The agent grounds on the result.** Inconsistent answers depending on phrasing is exactly what a fragmented profile estate produces: different retrieval paths reach different fragments of the same customer, and each answer is confident. This is a data-architecture failure presenting as an AI failure, and it will be reported as the latter every time.
- **And the money.** Under the March 2026 profile-based SKU — roughly **$240 per 1,000 profiles** baseline — you are billed on **unified profiles after identity resolution**, not source rows. A 2.8× profile count is a recurring 2.8× line item. That is the argument that lands with a CFO rather than only with a data team, and it is what funds the remediation.

**What to do, in order.**
- **Stop the bleeding first:** no new custom DMOs, no new segments on the affected ones. This is free and it caps the blast radius while you plan.
- **Map the seven sources onto standard DMOs** where a standard one exists, which will be most of them. "Didn't quite fit our fields" is usually a mapping problem rather than a modeling one — and unmapped DLO fields still cost storage while adding no downstream value, so mapping *what is used* is the discipline, not mapping everything.
- **Then re-run identity resolution and watch the profile ratio.** Profile count versus source-record count is the measurement: far above expectation means fragmentation. That ratio is both the health metric and the bill, so it is worth tracking over time rather than checking once.
- **Rebuild insights and segments last**, on the corrected model.
- **Check the primary key before anything else.** It is consumed by identity resolution and changing it later is painful — that decision belongs in data modeling, not in the identity-resolution step.

**Be straight about the cost.** This is a re-model with four insights and eleven segments to rebuild on top, and it is expensive precisely because things were built before the model settled. "Just map it and fix it later" is the wrong instinct here specifically, and this is what later costs. The honest framing: the remediation is cheaper than the recurring profile bill plus an agent nobody trusts, and it gets more expensive every month it waits.

**The trap.** Starting with identity resolution, because the 2.8× is the most measurable number and matching rules are the obvious lever. Tuning match rules against fourteen unaligned DMOs is work you will throw away — and looser matching to bring the count down is actively dangerous. **Over-matching is the cheaper direction and it is a privacy incident:** two people merged into one profile means Person A's data is showing in Person B's. Never tune matching on cost alone, and especially not on a broken model.

**Follow-ups they will ask.**
- "When *is* a custom DMO right?" — when there is genuinely no standard DMO for the entity. The test is whether the concept is cross-source or source-specific; if two sources describe the same thing, it belongs on one standard DMO.
- "Could you leave the model and fix the agent?" — no. Grounding faithfully returns what the model holds. There is no retrieval configuration that reassembles a customer split across fourteen DMOs.
- "Which do you fix first if they only fund one?" — the model. Insights and segments rebuilt on a broken model are rework; on a fixed model they are a one-time cost.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Traces one root cause through matching → insights → segments → agent answers, converts the 2.8× into a recurring bill under profile pricing, sequences model-first, and refuses to loosen matching to reduce the count |
| 🟡 Partial | Identifies custom DMO proliferation as wrong and proposes remapping, but does not connect it to the profile count, the cost, or the agent inconsistency |
| 🔴 Weak | Starts with identity-resolution tuning; or treats the inconsistent answers as a grounding or model problem; or proposes loosening match rules to cut the profile count |

**Ask this if they stall:** "The same customer exists in three of the seven sources. On which field does identity resolution match them?"

</details>

---

### Q4 · One field, renamed

**Level:** Complex · **Probes:** [Data modeling DSO → DLO → DMO](../../AI_Data/01-data-cloud/03-data-modeling-dso-dlo-dmo/notes.md) · [Data 360 DevOps](../../AI_Data/01-data-cloud/09-data-360-devops/notes.md) · [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md)

**Scenario.** An upstream team is migrating their billing platform. In four weeks, the field currently arriving as `cust_email_primary` becomes `primary_email`, and a second field changes from a nullable string to an empty-string-defaulted one. That DLO maps to the Individual DMO, feeds the email-based match rule in the live ruleset, and three activated segments and a churn insight sit downstream. They have told you as a courtesy, not a request, and the date is fixed. Your agent grounds on the resulting profiles.

**Asked as:** "Four weeks' notice on a breaking upstream change. What is your plan?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Two changes with very different risk profiles, and the second one is the dangerous one. The rename is a **loud** failure — the mapping breaks and you know. The nullable-to-empty-string change is a **silent** one that will quietly corrupt matching, and it is the one that needs the design attention.

**Then work through.**
- **Why the rename is the easy half.** Remapping `primary_email` onto the same DMO attribute is mechanical. The risk is timing, not complexity: between the upstream cutover and your remap, the field arrives unmapped and the email match rule has nothing to match on. So it needs to be a coordinated cutover, not a fix-forward.
- **Why the empty-string change is the real problem.** Data 360 collapses `NULL` and `''` by default — the way Platform objects behave. Once the upstream sends `''` instead of `NULL`, the semantics of "no email" change, and **`honorEmptyStrings` decides whether the platform agrees with the upstream's intent**. Get it wrong and you do not get an error. You get an email match rule matching records on a shared empty value, which is **over-matching** — the cheaper direction and a privacy incident, because two people merged into one profile means one customer's data is visible in the other's. Decide this deliberately rather than inheriting the default.
- **Sequence the work.**
  - **Now:** go back to the upstream team, because "courtesy" understates it. Ask whether `''` means "no email" or "unknown", since that determines your setting, and confirm whether the two changes ship together or separately — separate cutovers are two smaller problems and worth asking for.
  - **Before the date:** replicate both changes in a lower environment with the real ruleset, and measure the **profile-count-to-source-row ratio** before and after. That ratio is the detector for both under- and over-matching, and it is also the bill under profile pricing, so it is the number to put in front of the client either way. Promote the model change through the normal [Data 360 DevOps](../../AI_Data/01-data-cloud/09-data-360-devops/notes.md) path rather than hand-editing production.
  - **On the date:** cut over the mapping in step with the upstream, then re-run the ruleset and check the ratio against the baseline you took.
  - **After:** validate the churn insight against hand-written SQL rather than trusting a row count, and verify the three activated segments still resolve to sane sizes. An activated segment that silently halves has already published to a target.
- **The blast radius is the thing to state explicitly**, because it is what justifies treating a courtesy note as a project: mapping → match rule → unified profiles → churn insight → three activated segments → agent grounding. **Everything downstream inherits the mapping.** One field, six consumers.

**The trap.** Treating this as a mapping ticket — remap the renamed field, done — because the rename is the change that was communicated and the empty-string change reads as a detail. It is the detail that produces merged profiles and an unfindable privacy problem, and unlike the rename it will not announce itself. The second trap is doing it fix-forward in production on the day, on the reasoning that a broken mapping is obvious and quick to spot. It is; the ruleset run against half-mapped data in the meantime is not.

**Follow-ups they will ask.**
- "What if you cannot get a lower environment with real-shaped data?" — then the ratio baseline in production before the cutover becomes the only control you have, and you take it deliberately rather than discovering you needed it.
- "How would you know over-matching had happened?" — profile count drops below expectation. And it is worth being blunt: the same signal reads as a *cost improvement* on a dashboard, which is exactly why "never tune matching on cost alone" is a rule rather than advice.
- "Could you keep both field names mapped for a transition period?" — that is the pragmatic answer where the platform allows it, and worth checking. 🚩 Verify the dual-mapping behaviour in an org before promising it — the notes do not cover it, and reconciliation across two attributes has its own failure mode.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Separates the loud rename from the silent semantic change, connects `''` on an email field to over-matching and a privacy incident, uses the profile-count ratio as the before/after detector, and enumerates the six downstream consumers |
| 🟡 Partial | Plans the remap and tests in a sandbox, mentions the null-handling change as a risk, but does not reach the over-matching consequence |
| 🔴 Weak | Remaps the field and moves on; or plans to fix it in production on the day; or treats the empty-string change as cosmetic |

**Ask this if they stall:** "After the cutover, forty thousand records arrive with an empty string in the email field. What does an exact-email match rule do with them?"

</details>
