# Data 360 — Identity & Segmentation

> Area: Data 360 · Set 02 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the layer where a data-quality decision became a recurring bill and a privacy exposure at the same time. Since March 2026 you are billed on unified profiles, which means match quality is a line item — and the cheaper direction is the dangerous one.

---

### Q1 · The churn alert that fires on nobody

**Level:** Medium · **Probes:** [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md)

**Scenario.** A subscription client has an RFM insight producing tier labels — champion, loyal, at risk, lapsed. Marketing has built an automation on the *transition*: when a profile moves from champion to loyal, trigger a retention campaign. It ran beautifully for two months. Last week it fired on 34,000 profiles overnight, including customers who had bought that same week. Nobody deployed anything. The insight definition has not changed.

**Asked as:** "Thirty-four thousand retention emails to active customers. What happened?"

<details><summary><b>Model answer</b></summary>

**Lead with.** **RFM ranks are relative, not absolute.** Quintiles re-cut on every run, so a profile can fall from champion to loyal because the *population* moved, not because its behaviour changed. Building an automation on the transition means building it on a moving boundary.

**Then work through.**
- **What almost certainly happened.** A cohort of high-activity customers arrived — a promotion, a seasonal peak, a new-market launch, or simply an ingestion backfill landing a batch of purchase history. Quintile boundaries shifted upward. Everyone near the champion/loyal line got re-cut into loyal without doing anything differently. Customers who bought that week are the tell: their behaviour improved and their *rank* fell, which is only possible if the population improved faster.
- **Why it worked for two months.** The population was stable, so the boundaries were stable, so relative ranks behaved like absolute ones. That is the trap: the design flaw is invisible for exactly as long as nothing changes upstream, which is long enough to build confidence on.
- **The fix depends on what marketing actually meant.** Two different questions were merged. If they mean "this customer's behaviour has deteriorated", that is an **absolute** measure — days since last purchase, purchase count over a window — and RFM is the wrong input. If they genuinely mean "this customer is no longer in our top segment relative to everyone else", RFM is right, and the automation needs to tolerate population movement: require the transition to persist across two consecutive runs, or gate on an absolute recency floor as well as the rank drop.
- **The structural point worth making.** LTV emits **one number per profile**, so a segment needs someone to decide what "high value" means. RFM emits a **classification**, so the meaning travels with the value — which is what makes it the more natural thing to hand an agent. But a classification whose boundaries are recomputed each run is not a stable event source, and "the tier changed" is not the same claim as "the customer changed."
- **Say this before someone builds the next one.** That is the note's own framing and it is the right instinct: this failure mode should be raised at design time, out loud, because it is not discoverable from the insight definition.

**The trap.** Debugging the insight definition, the SQL expression, or the refresh schedule. Nothing is broken — the insight computed exactly what it was asked to. Looking for a defect in a system that has none is how a day goes, and it also means the automation gets re-enabled unchanged.

**Follow-ups they will ask.**
- "Would you have caught this in testing?" — only with a test that moves the population, which nobody writes. It is a design-review catch, not a test catch.
- "What if a fragmented profile estate contributed?" — plausible and worth checking. Insights compute per unified profile, so a wave of new unresolved fragments changes the population the quintiles are cut against. The error would originate in identity resolution rather than in the insight.
- "How do you explain this to marketing without sounding like you are blaming them?" — they asked a reasonable question and got a technically correct answer to a different one. The useful output is a definition: does "at risk" mean *worse than before* or *worse than others*?

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names relative quintile re-cutting immediately, explains why customers who bought that week are the diagnostic, and separates "behaviour deteriorated" from "rank fell" as two different requirements |
| 🟡 Partial | Suspects the population shifted and the ranking is relative, but proposes only a technical dampener without resolving what marketing meant |
| 🔴 Weak | Debugs the insight SQL, the schedule or the automation; or assumes 34,000 customers genuinely churned |

**Ask this if they stall:** "Some of those profiles bought something that week. Their recency improved. How does their rank get worse?"

</details>

---

### Q2 · The cheaper direction

**Level:** Complex · **Probes:** [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md) · [Privacy, consent & data protection](../../SF/07-security-and-sharing/25-privacy-consent-and-data-protection.md)

**Scenario.** A financial-services client's Data 360 bill is over budget. Their profile count is 4.1M against an estimated 2.6M customers, and someone has calculated that closing the gap saves roughly $360k a year at ~$240 per 1,000 profiles. The data team has proposed a looser ruleset: add fuzzy name plus address matching alongside the existing exact-email rule. Modelling says it brings the count to about 2.7M. The CFO likes it. Their agent grounds on these profiles, and their customers include joint account holders and multi-generational households.

**Asked as:** "The numbers work. Do you approve it?"

<details><summary><b>Model answer</b></summary>

**Lead with.** No, and the reason is not that the saving is wrong — it is that **fuzzy name plus address is the textbook household-collapse rule**, and this client's population is joint account holders and multi-generational households. The proposal converts a cost problem into a privacy incident, in a regulated industry, and the incident is invisible on every dashboard because it looks like the saving working.

**Then work through.**
- **The asymmetry is the whole answer.** Under-matching (too strict) splits one person into three profiles: you pay three times *and* the agent sees a third of their history. Over-matching (too loose) merges two people into one: it is **cheaper** and you have shown Person A's data to Person B. Over-matching is the dangerous direction *and* the one cost pressure pushes you toward. That is why "never tune matching on cost alone" is a rule.
- **Why this specific rule, on this specific population.** Fuzzy name plus address is the lowest-precision strategy — a last resort — and its known failure is households collapsing into individuals. A father and son sharing a name and an address, or two joint account holders at one address, merge. In financial services that is one customer seeing another's balances and transaction history through an agent that is grounding on the merged profile and answering confidently.
- **The 1.5M gap is real and worth investigating — just not with this rule.** Work it as a diagnosis rather than a lever. Where is the fragmentation coming from? Duplicate-heavy sources inflate profile counts at ingestion. Is there a **shared customer identifier** across systems? Exact match on a customer ID is the highest-precision strategy available and financial-services clients usually have one. Is email reliably captured, and is the existing exact-email rule actually firing, or failing on case and whitespace variance? Those routes close part of the gap with precision rather than by loosening.
- **Reconciliation is a separate lever nobody has touched.** Set strategies **per attribute**, not globally — most recent for changeable attributes like phone and address, source priority where one system is genuinely authoritative, most frequent where one source is often but not consistently wrong. A global strategy is almost always wrong for something, and the right answer for `Email` is rarely the right answer for `LifetimeValue`.
- **What to take to the CFO.** Not "no." The saving is real and part of it is achievable — quantify how much comes from precision routes, and price the rest honestly as the cost of not merging customers who should not be merged. The framing that works: identity resolution quality is now a recurring line item, which is why it deserves investment, and the same fact means a bad merge is a recurring exposure rather than a one-off error.

**The trap.** Approving it with a mitigation — run it and monitor for bad merges, or exclude shared addresses. Both sound responsible and neither works. Monitoring detects a merge *after* the agent has already served one customer's data to another, and there is no clean signal to monitor for: **a merged profile looks exactly like a correctly resolved one**. And "exclude shared addresses" excludes precisely the population the rule was going to match, which removes most of the modelled saving — so the business case evaporates while the risk stays for whatever remains.

**Follow-ups they will ask.**
- "How would you ever detect over-matching?" — the profile-count ratio falling below expectation, and that is weak, because on a cost dashboard it reads as success. Better to catch it in a sandbox: deliberately over-match on test data with two people at one address and look at the merged profile once. Seeing the privacy failure makes it memorable in a way a policy does not.
- "What if the CFO overrules you?" — then it is their decision, documented, with the specific risk named in writing and the regulator's likely view on it. Note also that the agent grounding on merged profiles makes the exposure *active* rather than latent — it is not a dormant data-quality issue, it is a system that will read one customer's history out to another.
- "Is there a middle ground?" — fuzzy name plus *exact phone* is meaningfully higher precision than name plus address, and does not collapse households the same way. Worth modelling as an alternative.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Leads with the asymmetry, names household collapse against this specific population, refuses monitoring as a mitigation because a merged profile is indistinguishable from a correct one, and returns with precision routes plus a defensible partial saving |
| 🟡 Partial | Rejects the proposal on privacy grounds but does not name the household failure mode, or offers no alternative route to the saving |
| 🔴 Weak | Approves with monitoring or an address exclusion; or treats it purely as a data-quality trade-off with no privacy dimension; or rejects it with no business answer for the CFO |

**Ask this if they stall:** "Two joint account holders, one address, surname in common. What does fuzzy name plus address do with them, and what does the agent then say to one about the other?"

</details>

---

### Q3 · Re-running the ruleset on 4 million profiles

**Level:** Complex · **Probes:** [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Data 360 DevOps](../../AI_Data/01-data-cloud/09-data-360-devops/notes.md) · [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md)

**Scenario.** The precision fixes from the previous engagement are agreed: add exact-match on a newly-available shared customer ID, tighten the email rule, and change reconciliation on `Email` from most-recent to source-priority. The client has 4.1M profiles, six activated segments publishing to Marketing Cloud and two ad platforms, a live service agent grounding on these profiles, and a nightly insight refresh. Change board wants a plan. There is no full-volume lower environment.

**Asked as:** "Ruleset change, live consumers, no full-scale sandbox. How do you land it?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The change is right and the risk is entirely in the transition, not the destination. Three consumers see profiles change under them — activated segments, the agent, and the insights — and the ruleset runs on a **schedule**, so there is a window where records are resolved under one set of rules and consumers are reading the results of another.

**Then work through — what breaks, per consumer.**
- **Activated segments are the highest-risk consumer, because activation is irreversible.** Membership is recomputed against the new profiles. If a segment halves, it has already published a halved audience to Marketing Cloud and two ad platforms before anyone reads a dashboard. Ad platforms in particular do not un-receive an audience.
- **The agent is the most visible.** Profiles merging means conversation-relevant history appearing or disappearing mid-day. Not wrong afterwards — genuinely better — but a rep or customer sees inconsistency across the boundary.
- **The insights are the quietest and the most likely to be wrong for longest.** They compute per unified profile, so every metric shifts. A number that moves 8% overnight and renders fine is one nobody investigates.
- **And the reconciliation change is a distinct risk from the matching change.** Switching `Email` from most-recent to source-priority does not merge or split anything — it changes *which value wins* on profiles that already exist. Every downstream consumer keyed on email sees values change without any profile count moving, so the count-based checks that catch matching problems are blind to it. Worth validating separately.

**The plan.**
- **Baseline first, and take it deliberately** — profile count, source-row count and the ratio; the six segment sizes; the two insight values. Without a full-volume lower environment this baseline is the only control you have, so it is a step, not an assumption.
- **Split the change.** Three modifications with different risk profiles landing together is one unattributable outcome. Sequence them: the customer-ID exact match first, since it is the highest-precision and most predictable; the email tightening second; reconciliation last, because its effects are invisible to count checks and you want a clean population when you validate it.
- **Pause activations across each cutover.** This is the one non-negotiable — segment publishing is the irreversible consumer, and pausing costs a cycle while not pausing costs an audience.
- **Use what the lack of a full-volume sandbox still allows.** A representative subset in a lower environment will not predict the profile count, but it *will* validate rule correctness and reconciliation behaviour, which is what you actually need it for. Promote the change through the normal [Data 360 DevOps](../../AI_Data/01-data-cloud/09-data-360-devops/notes.md) path rather than hand-editing production. Do not let "no full-scale sandbox" become "no sandbox."
- **After each step:** check the ratio against baseline, then validate insights against hand-written SQL rather than trusting a UI count, then resume activations once segment sizes are sane.
- **Expect the direction and state it upfront.** Tightening plus a new high-precision key should *reduce* the count. If it rises, matching got stricter than intended and you are now paying for fragmentation — which is the failure mode this whole engagement was reversing.

**The trap.** Landing all three changes in one window because the change board wants one approval and one outage. It is the path of least organisational resistance and it destroys attributability: if segment sizes move 20%, you cannot say which change did it, and the rollback is all-or-nothing. The related trap is treating "no full-volume sandbox" as licence to test in production — the subset environment still validates correctness, which is most of what testing was for.

**Follow-ups they will ask.**
- "Rollback plan?" — reverting the ruleset and re-running restores the profile shape, but anything already **activated** is gone. That asymmetry is exactly why activations pause rather than why the rollback is good.
- "How do you tell the client's agent users?" — tell them, with a date. Profiles improving mid-day looks like a bug to anyone who was not told, and an unexplained inconsistency erodes trust in the agent more than a scheduled change does.
- "Rulesets run on a schedule — does that help or hurt?" — both. It means the change lands predictably rather than record-by-record, which is what makes a controlled cutover possible. It also means a new record is not resolved the instant it lands, so an agent can briefly see an unresolved fragment regardless of any of this.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Enumerates the consumers by risk, identifies activation as the irreversible one and pauses it, splits three changes into sequenced steps for attributability, treats reconciliation as invisible to count checks, and states the expected direction of the count in advance |
| 🟡 Partial | Plans a baseline, a sandbox test and a monitored cutover, but lands all three changes together, or misses that activated audiences cannot be recalled |
| 🔴 Weak | Runs it in a maintenance window and monitors; or blocks on getting a full-volume sandbox; or treats the reconciliation change as equivalent to the matching changes |

**Ask this if they stall:** "One of those six segments halves and publishes before you notice. Which of the three targets can you take it back from?"

</details>

---

### Q4 · Whose churn number is it 🆕

**Level:** Medium · **Probes:** [Insights & segmentation](../../AI_Data/01-data-cloud/05-insights-segmentation/notes.md) · [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md)

**Scenario.** An exec asks the agent "what was churn last quarter?" and gets 11.2%. The finance team's board pack says 7.8%. Both numbers are defensible: finance excludes customers who downgraded rather than cancelled, and counts on contract end date; the Data 360 calculated insight counts any subscription lapse on the lapse date. The exec's question to you is short: "which one is right, and why is the agent making up numbers?"

**Asked as:** "Is this a tooling problem?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The agent is not making up numbers — it computed one definition of churn correctly and stated it without hedging. And no, this is not a tooling problem. **A metric with two definitions in two systems is a governance problem**; the semantic layer makes the disagreement visible, it does not decide for you.

**Then work through.**
- **The behavioural difference that matters.** When a human reads a dashboard labelled "churn", they bring context — they know which definition the company uses, or they know to ask. **An agent does not ask.** Given an ambiguous metric it produces a confident number from whichever definition it found. That is the failure this whole topic exists to prevent, and it is not fixable by making the agent more cautious.
- **What to actually build.** Define churn once in the **semantic layer** — Tableau Semantics standardizes metric definitions and translates data into business language, so an agent asked for churn returns the company's definition rather than one it inferred. That is the mechanism. But it only works after somebody decides *which* definition, which is a finance decision, not an architecture one.
- **So the deliverable is a decision, then a definition.** Take both computations to whoever owns the number. Most likely outcome: finance's definition is the company's, and the insight is remodelled to match — excluding downgrades, counting on contract end date. Possible better outcome: they turn out to be two legitimately different metrics, in which case name them differently. "Churn" and "subscription lapse rate" can coexist; two things called churn cannot.
- **Then check the exec's real question.** They asked which is right, but the thing that will actually shape their behaviour is whether they can trust the agent's numbers at all. The answer is that they can trust the ones that are defined, which is an argument for doing this across the metrics that reach agents rather than just for churn.
- **The general rule this generalizes to.** Prefer grounding an agent on a **calculated insight** over raw records when the question is analytical — fewer tokens, governed meaning, and no chance the model computes its own aggregate wrongly. An insight defines *how* a number is computed; the semantic layer defines *what it means*. Agents need both, and this scenario is what having only the first looks like.

**The trap.** Answering the question as asked — picking a number. Whichever you pick, you have made a finance policy decision in a hallway conversation, and the other number stays in production. The mirror trap is blaming the agent and adding a caution instruction so it hedges or cites its source. Hedged wrong numbers are still wrong, and an agent that qualifies every metric is one nobody uses.

**Follow-ups they will ask.**
- "Freshness — could that explain the gap?" — worth ruling out, since insights run on a schedule and an agent can ground on a stale one. But a 3.4-point gap with two documented methodologies is a definition gap, not a lag.
- "What is OSI?" — a vendor-neutral, YAML-based open-source standard for interoperable semantic models and metrics, core spec finalized **February 2026**. Semantic definitions becoming portable is the same move as Agent Script compiling to JSON: the definition stops being locked in the tool that computes it.
- "Who owns this in the client organisation?" — the honest answer, and the reason this recurs: usually nobody, until an agent forces the question. Which is a real argument for the AI project rather than against it.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | "Agents don't ask what a metric means", names the semantic layer as the mechanism but insists the decision is finance's, and offers the rename-both option where the two metrics are genuinely different |
| 🟡 Partial | Explains the definition mismatch and proposes aligning the insight to finance, without reaching the semantic layer or the governance framing |
| 🔴 Weak | Picks a number; or blames the insight SQL; or adds a hedging instruction to the agent |

**Ask this if they stall:** "If the exec had read the same number off a dashboard instead of asking the agent, would they have been misled?"

</details>
