# Cross-Domain — Architect Scenarios

> Area: Cross-domain · Set 01 of 01 · Scenarios: 6 · Level: complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the questions with no single-domain answer. Every one of these fails if you reason inside one area — the constraint that decides it sits in another. This is the set that separates a strong senior developer from an architect, and the one to work through last.

---

### Q1 · The agent that must see everything and must see nothing

**Level:** Complex · **Probes:** [Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md) · [Code execution context & security](../../SF_core/07-security-and-sharing/14-code-execution-context-and-security.md) · [Restriction rules](../../SF_core/07-security-and-sharing/11-restriction-rules.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md)

**Scenario.** A private bank wants a relationship-manager agent that answers "give me the full picture on this client before my 3pm meeting." The picture spans a Data 360 unified profile over CRM, custody, a Snowflake transaction warehouse and a document corpus. Two constraints arrived from different rooms in the same week, both signed off. Compliance: an RM must never see holdings for a client outside their own book, and there are hard information barriers between two divisions. The business: "a partial answer is useless — the whole point is that it sees everything."

**Asked as:** "Two signed-off requirements that contradict. How do you resolve it, and what do you go back and tell them?"

<details><summary><b>Model answer</b></summary>

**Lead with.** They do not contradict — one of them is imprecise. "The agent must see everything" is a statement about the *corpus*; compliance's requirement is about the *reader*. The resolvable version: the agent reaches every source and returns only what this RM is entitled to. The barrier is non-negotiable, so the design starts there and the business requirement gets restated.

**Then work through.**
- **Establish the control point first, because everything follows from it.** An agent has **no access boundary of its own** — it runs as a user and inherits that user's access exactly. So the RM's own permissions are the enforcement mechanism, not a configuration detail. The Trust Layer does not substitute for this: **secure data retrieval** fetches grounding data under the running user's permissions, which is the behaviour you want, and it is only correct if the access model underneath it is.
- **Say what "runs as the RM" costs, because this is the part that gets glossed.** Under 67.0 defaults the agent's queries return less for an RM outside the book — correctly. So **the answer is legitimately partial**, and the business needs to hear that as a feature. The design deliverable is that the agent *discloses it*: "holdings outside your book are excluded" rather than silently returning a subset that reads as complete. A silently partial answer to "give me the full picture" is the real danger here, not a refused one.
- **The information barrier is the harder half and it is not a sharing rule.** A cross-division barrier is an exclusion, and exclusions are only expressible by subtracting — which means **restriction rules**. Check the object list first: the core CRM objects are **not** supported, but custom and external objects are, which is likely where custody and transaction data sit. So the barrier lands cleanly on part of the estate and needs a different answer on Account and Opportunity. Establish that on day one rather than discovering it in UAT.
- **Then the Data 360 layer, where the barrier can quietly leak.** Identity resolution builds one profile across all four sources. **Over-matching merges two people into one profile** — here, one client's holdings surfacing inside another's profile, *underneath* every sharing control, because the merge happened before records were the unit of access. Match on the highest-precision key available — a client identifier, never fuzzy name and address — and treat the profile-count ratio as a compliance metric rather than a cost one.
- **And the reach decision.** Snowflake stays federated for analytical depth; the identity-bearing and grounding-relevant slice gets ingested, because identity resolution needs the data locally and agent grounding needs predictable latency. Here that is also a control decision: what is ingested is what the unified profile — and therefore the barrier — has to be correct about.
- **What you go back and tell them.** Compliance's requirement stands unchanged. The business requirement is rewritten from "sees everything" to "reaches every source, returns what you are entitled to, and tells you when something is withheld." Then the caveat, in writing: an agent inherits a user's access and **composes and aggregates far faster than a person browsing**, so a permission set tolerable for a human who would never assemble those records needs re-reviewing for a caller that will. That is the reasoning behind the 67.0 flip and it applies directly to a private bank.

**The trap.** Resolving it by elevating — a broad service running user, or `without sharing` on the retrieval action, plus prompt instructions or scoping to stop the agent *saying* the wrong thing. It satisfies both requirements on paper and puts a compliance barrier in the hands of a model's judgement. Prompt-level controls are not access controls, and a barrier enforced by instruction fails on the phrasing nobody tested. The mirror trap is refusing the business requirement outright instead of restating it, which loses a project that is buildable.

**Follow-ups they will ask.**
- "How do you prove the barrier holds?" — run the same grounded prompt as two RMs in different divisions and compare outputs. A demonstration rather than an assurance.
- "What if the barrier must cover Account?" — restriction rules cannot, so it becomes an OWD-and-sharing design, and you price the recalculation. Tightening an OWD is the most expensive single action in that area.
- "Where does the audit trail fit?" — every prompt sent, datum accessed and response generated is logged. It is a compliance artifact, not just a debugging tool, so know its retention before promising anything to a regulator.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Dissolves the contradiction by separating corpus from reader, makes the RM's own access the control, requires disclosure of withheld data, checks restriction-rule object support, and spots over-matching as a leak beneath the sharing layer |
| 🟡 Partial | Runs the agent as the RM and relies on user-mode enforcement, but does not address the cross-division barrier or the identity-resolution exposure |
| 🔴 Weak | Elevates the running user and controls disclosure through prompts; or cites the Trust Layer as satisfying compliance; or calls the requirements irreconcilable |

**Ask this if they stall:** "Two clients get merged into one unified profile by a loose match rule. Which of your access controls catches that?"

</details>

---

### Q2 · Four bills, one project

**Level:** Complex · **Probes:** [Prebuilt agents & buy vs build](../../AI_Data/02-salesforce-ai/14-prebuilt-agents-and-buy-vs-build/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Zero Copy & BYOL](../../AI_Data/01-data-cloud/06-zero-copy-byol/notes.md) · [Multi-Agent Orchestration](../../AI_Data/02-salesforce-ai/08-multi-agent-orchestration/notes.md) · [Observability & Testing](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md)

**Scenario.** Price a two-year run cost for a service-agent programme before it reaches an investment committee: an orchestrator over three subagents, grounded on Data 360 with a federated Snowflake warehouse, ~2.6M customers, ~40,000 support conversations a month, evaluation suite running in CI on every deploy. The previous estimate was one line — "Flex Credits: $0.10 per action × estimated actions" — and the committee rejected it as not credible. You have a week.

**Asked as:** "Build the model. What are the axes, and which one will they not have thought of?"

<details><summary><b>Model answer</b></summary>

**Lead with.** A one-axis model is why it was rejected. There are at least six metered dimensions across three products, they are metered in different units, and two of them are driven by **design decisions rather than volume** — which is what makes the model credible, because it means the number is something you can influence.

**The axes.**
- **Agent actions.** Roughly **20 credits (~$0.10)** per standard action, $500 per 100k. The multiplier the old estimate missed is **orchestration depth**: you pay per action, so an orchestrator routing through three subagents costs roughly three times a direct hit — and **mis-routing bills twice**, the wrong hop and the right one. Description quality is therefore a cost input, not only a quality one. That is the line the committee will not have thought of.
- **Unified profiles.** Roughly **$240 per 1,000** baseline under the March 2026 profile-based SKU, billed on unified profiles **after** identity resolution rather than source rows. 2.6M customers at a 15% duplicate rate is a materially different recurring number from 2.6M clean. Model both; the delta is the business case for identity-resolution work.
- **Source-side query compute.** Federation avoids Data 360 storage and charges **source-side compute on every query**. Grounding and segment evaluation against Snowflake at 40,000 conversations a month is a Snowflake bill nobody has counted, and it belongs in this model even though it arrives on a different invoice.
- **Evaluation and testing.** Testing Center actions are **16 credits (~$0.08)** each — cheaper than standard actions, not free. A suite on every deploy scales with deploy frequency rather than with users.
- **Data 360 storage and ingestion**, for whatever slice is ingested rather than federated.
- **Licences and platform entitlements**, including API allocations for anything that integrates.

**Then the commercial model, which can change the shape entirely.** Three coexist and they price the same work differently. Under **Flex Credits** a chatty agent that resolves nothing costs the client money; under **pay-per-resolution** — **$2** per autonomous end-to-end resolution, consumption unmetered *during* the interaction — it costs Salesforce money. For a support agent with countable discrete outcomes that inversion may be the biggest single lever in the model. 🚩 It carries a commercial precondition: get the definition of "resolution" in writing — what counts, who adjudicates, what happens on a partial. Contract questions, not design ones.

**What to hand the committee.** Two scenarios, Flex Credits and pay-per-resolution, with the crossover point identified, every assumption on its own line, and the two design-driven axes flagged as levers rather than forecasts: orchestration depth and profile duplication. A committee will accept a range with visible assumptions and reject a point estimate — which is what happened the first time.

**The trap.** Producing a bigger, more precise version of the same one-axis model. More careful action arithmetic reads as diligence and repeats the original error. The subtler trap is scoping out the Snowflake compute because it lands on a different invoice: the committee is approving a programme, not a Salesforce line item, and a 60% warehouse increase discovered in month four is exactly what kills the next phase.

**Follow-ups they will ask.**
- "Which axis has the widest error bar?" — actions per resolution, because it depends on orchestration depth and routing quality, both still being designed. Which is the argument for a range plus early instrumentation.
- "How do you tighten it before signature?" — count the actions consumed by one orchestrated resolution in preview and multiply out. That number is available pre-go-live.
- "Would buying a prebuilt agent change this?" — it changes build cost and the maintenance commitment, not the platform meters. Flex Credits, voice rates and Trust Layer behaviour do not change because you did not author the agent.
- "They want one number anyway." — give one, with the assumptions attached and the two levers named. A number you can defend beats a range you cannot explain.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names five or more axes in different units, identifies orchestration depth and profile duplication as design-driven levers, includes source-side compute despite the separate invoice, and models both commercial models with a crossover |
| 🟡 Partial | Gets actions and profiles and knows profiles are billed post-resolution, but misses federated query compute or the pay-per-resolution inversion |
| 🔴 Weak | Refines the action arithmetic; or quotes list pricing without design levers; or treats the warehouse bill as out of scope |

**Ask this if they stall:** "One resolution goes through the orchestrator and two subagents. How many billed actions is that, and what happens if it routes wrong first?"

</details>

---

### Q3 · Which layer is lying

**Level:** Complex · **Probes:** [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md) · [Identity Resolution](../../AI_Data/01-data-cloud/04-identity-resolution/notes.md) · [Bulkification patterns](../../SF_core/02-apex-and-triggers/08-bulkification-patterns.md) · [Code execution context & security](../../SF_core/07-security-and-sharing/14-code-execution-context-and-security.md) · [Observability & Testing](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md)

**Scenario.** A live agent answers "what is this customer's current balance and open case count?" It is right for most users. For one team — recently onboarded, in a new role under a new branch of the hierarchy — it returns a balance that is correct, a case count that is too low, and occasionally "I don't have information about that." An Apex action supplies the case count; a Data 360 data graph supplies the balance. Nothing was deployed this week. The team's manager has escalated it as an AI accuracy problem.

**Asked as:** "One symptom, three candidate layers. How do you isolate it?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The distribution is the diagnostic: **one team, recently onboarded, new roles**, and the balance is right while the case count is wrong. That combination points hard at **access**, not at AI. Two different sources behaving differently for the same user rules out most explanations that live in the agent.

**Then work through — isolate by source, because they have different enforcement paths.**
- **The balance is right, so the data graph path is fine.** A data graph is precomputed and denormalized, serving millisecond reads. It working correctly tells you grounding, retrieval and the model are all functioning. That is most of the agent exonerated in one observation.
- **The case count is low from an Apex action, which is where user mode lives.** At 67.0 SOQL defaults to user mode, so the query returns only the cases this user can see. A new team under a new branch of the hierarchy is precisely the population whose sharing has not been set up correctly yet. **The action is very likely returning the right answer for the access these users actually have** — the defect is the access, not the code. Worth saying plainly, because it reframes the escalation.
- **Then check the second-order version, since it changes the fix.** If the action does a bulk lookup, `Map.get()` returning null because of **sharing** rather than missing data produces a silently low count with no error. Same symptom, different fix: the access still needs correcting, and the action needs a decision about the null branch — skip, `addError()`, or explicitly elevate that one query and document why.
- **The intermittent "I don't have information about that" is probably a third thing.** Uncited, occasional, and unlike the other two symptoms. Candidates: sharing recalculation still in flight from the recent onboarding — recalculation now runs **asynchronously** after group and role changes, so newly-granted access genuinely is not there yet; or a retrieval miss. Check whether failing answers carry citations, which separates an empty retrieval from a model gap.
- **The onboarding timing is the thread to pull.** New users, new roles, a new hierarchy branch, and async recalculation together explain all three symptoms without anything being broken in the agent. Confirm before theorizing further: query the share rows for one affected case and one affected user.
- **Then the instrumentation finding.** Nobody could answer this question from the org, which is why it arrived as an escalation. Trace files show what the agent routed and ran; a domain-specific **Custom Scorer** — "did the case count match a system-mode recount" — would have caught it as a metric rather than a complaint. Deploy scorers as `aiAgentScorerDefinitions` so they live in source control.

**The trap.** Accepting "AI accuracy problem" and working inside the agent — prompts, grounding config, the model. Every one of those is the wrong layer, and the tell was in the ticket: **a correct balance and an incorrect case count from the same agent for the same user is not something a model does.** The related trap is fixing the low count by elevating the Apex query to system mode, which makes the symptom disappear while leaving the sharing misconfiguration in place for every other consumer — reports, list views, and the next agent.

**Follow-ups they will ask.**
- "What is the general rule for triaging this class?" — walk the layers outward: is the data there, can this user see it, did retrieval find it, did the agent route correctly, did the model answer well. Stop at the first layer that fails. Most "the agent was wrong" reports resolve before the last two.
- "If the balance had *also* been wrong?" — then suspect the shared layer instead: stale ingestion or a fragmented profile. Both produce fluent, specific wrongness across every source at once.
- "Does an agent add an access boundary?" — no. It inherits its running user's access exactly, which is why a sharing gap presents as an AI defect.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Uses the one-team distribution and the right-balance/wrong-count split to rule out the agent, lands on user-mode plus incomplete sharing, connects the intermittent failures to async recalculation after onboarding, and refuses to fix it by elevating |
| 🟡 Partial | Suspects sharing and checks the Apex action's access, but treats all three symptoms as one cause or proposes system mode as the fix |
| 🔴 Weak | Investigates prompts, grounding or the model; or asks for a model change; or treats "recently onboarded" as incidental |

**Ask this if they stall:** "The balance is right and the case count is wrong, for the same user in the same conversation. What kind of cause could do that?"

</details>

---

### Q4 · The MCP server nobody reviewed

**Level:** Complex · **Probes:** [MCP servers & agent-facing APIs](../../SF_core/06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) · [Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md) · [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Idempotency, retries & error handling](../../SF_core/06-integration-and-apis/23-idempotency-retries-and-error-handling.md) · [MCP (Claude track)](../../AI_Data/03-claude-cca/05-mcp/notes.md)

**Scenario.** A developer at your client has stood up a custom hosted MCP server exposing eleven `@InvocableMethod` tools, so the engineering team can query and update org data from Claude Code during development. It is genuinely useful and has spread — about thirty people now use it, including two in support who use it against production. It was never security-reviewed; the developer's view is that it inherits the org's security model, so there is nothing to review. The CISO has just found out.

**Asked as:** "He's technically right about the security model. Is there nothing to review?"

<details><summary><b>Model answer</b></summary>

**Lead with.** He is right about the mechanism and wrong about the conclusion. Custom hosted MCP servers **do respect the org's full sharing and security model** — that is the good news and it is the reason this is fixable rather than an incident. But "who can create a hosted MCP server" belongs on a **security review checklist, not in a developer's discretion**, precisely because they expose org data to external AI clients. The thing to review is not whether enforcement exists; it is everything enforcement does not cover.

**Then work through what a review actually finds.**
- **Whose access, and is it appropriate for this surface?** Each user's own permissions apply, which is correct — and the question nobody asked is whether those permissions were designed for a caller that **composes and aggregates far faster than a person browsing**. A support user's access is scoped for a human working cases one at a time, not for a client that can sweep and correlate. That is the reasoning behind the 67.0 flip and it lands directly here.
- **Are the eleven tools idempotent?** An MCP client is a retrying caller. A timeout is not a failure, so a client that re-invokes an update tool after one produces duplicate writes exactly the way middleware does — against endpoints nobody reviewed for repeats. Any tool that creates, charges, sends or increments needs an idempotency key on a unique external ID.
- **Which tools write at all, and should they, from here?** Read tools against production are a disclosure question. Write tools against production from a development-convenience surface are a change-control question, and that is the one the CISO will care about most. The likely landing point is read-only against production, full toolset against sandboxes.
- **What is the Trust Layer doing on this path?** Less than people assume, and this is worth being precise about. The Trust Layer governs the **Agentforce and Prompt Builder** model interaction. Data flowing out through an MCP server to an external Claude client is a different path — so masking, toxicity scoring and the audit trail are not the controls here. **Enforcement on this path is the access model, and the access model alone.**
- **Then the two things that make it governance rather than configuration.** Nobody knows what those thirty people have queried, because this surface was not built with an audit expectation. And the API version on the classes behind the tools determines their data-access semantics — if any sit below 66.0 they are running in system mode with sharing inherited, which quietly removes the enforcement the whole "it inherits the security model" argument depends on. **Check that before repeating the argument.**

**What to recommend.** Do not switch it off — it is useful, thirty people depend on it, and killing it teaches the organisation to build the next one quietly. Bring it under governance: an owner, a documented tool inventory, read-only against production, writes confined to sandboxes, idempotency on every mutating tool, an access review for the support users, a verified minimum API version on the backing classes, and a named approval path for the next server. Then the durable output — a policy that creating a hosted MCP server requires review, since this will happen again and the next developer will be just as well-intentioned.

**The trap.** Agreeing that platform enforcement makes review unnecessary. It is the most defensible-sounding wrong answer in this area, and it survives because the claim it rests on is true. The mirror trap is shutting it down on discovery: it converts a governance gap into a political problem, loses real productivity, and guarantees the next one is not disclosed.

**Follow-ups they will ask.**
- "Same eleven methods as agent actions — same review?" — largely yes, and that is the useful framing: one `@InvocableMethod` can serve an Agentforce agent and an external Claude client with the same enforcement. The review is per *surface*, because the callers differ, not per method.
- "Two support users on production — biggest risk?" — that their access was scoped for a human pace. Bulk extraction through a legitimate account is the realistic scenario, not privilege escalation.
- "How would you detect misuse?" — you would need this instrumented, which it is not. Event Monitoring on the API surface is the platform answer, and it is a gap to close rather than a control you have.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Concedes the enforcement claim then shows what it does not cover, says MCP-server creation belongs on a security checklist, raises idempotency for a retrying client, notes the Trust Layer does not govern this path, and checks the backing classes' API versions |
| 🟡 Partial | Requires a review and identifies the production write risk, but accepts the Trust Layer as covering the path or misses idempotency |
| 🔴 Weak | Agrees there is nothing to review; or orders it switched off; or reviews only authentication |

**Ask this if they stall:** "One of those classes is on API 58. What is its sharing and access mode, and what happens to the 'it inherits the security model' argument?"

</details>

---

### Q5 · Real-time, at limits

**Level:** Complex · **Probes:** [Ingestion](../../AI_Data/01-data-cloud/02-ingestion/notes.md) · [Data Cloud-triggered flows & data actions](../../SF_core/04-flow-and-automation/22-data-cloud-triggered-flows-and-data-actions.md) · [Async Apex overview & choosing](../../SF_core/02-apex-and-triggers/12-async-apex-overview-and-choosing.md) · [Zero copy & Data 360 as data tier](../../SF_core/08-data-modeling-and-large-data-volumes/18-zero-copy-and-data-360-as-data-tier.md) · [Platform Event design](../../SF_core/06-integration-and-apis/12-platform-event-design.md)

**Scenario.** A telco wants an agent to intervene during a service outage: when Data 360 detects a customer's connection has been degraded for over ten minutes, the agent should proactively contact them with a status and a credit offer. Volume during a major incident is 60,000–200,000 affected customers within a few minutes. The client's design has a Data Cloud-triggered flow per affected profile, invoking an Apex action that calls the agent and issues the credit. Their architect wants to know if it will scale.

**Asked as:** "Will it scale? And if not, what is the design?"

<details><summary><b>Model answer</b></summary>

**Lead with.** No — and it fails on at least three independent ceilings, which is the useful answer because they need different fixes. The deeper problem is that the design treats a **bulk incident-response** requirement as **per-record automation**, and that is a pattern error rather than a tuning problem.

**Then work through the ceilings.**
- **Async execution budget.** A per-profile Apex action across 200,000 profiles draws on the shared daily async ceiling — **250,000 executions per 24 hours, or 200 × user licences, whichever is greater** — shared across `@future`, Queueable, batch chunks and scheduled Apex. One major incident can consume the org's entire daily async allowance and take every other scheduled job down with it. And 🚩 elastic limits, Beta at 67.0, would only throttle the overflow rather than reject it, which converts a hard failure into an incident that runs for hours.
- **The flexible queue.** **100 unstarted jobs**, after which `System.enqueueJob` throws. A burst of trigger-driven enqueues is the textbook way to hit this, and 200,000 in a few minutes is that in its purest form.
- **Action cost.** Every agent action is roughly **20 credits (~$0.10)**. Two hundred thousand outbound contacts, each involving at least one action and probably several, is a five-figure spend **per incident** — and a credit issued per customer is a real financial exposure on top. That number needs to be in front of the client before the architecture discussion, because it may change the requirement.
- **And the non-idempotency, which is the one that will actually hurt.** An agent retries after a timeout. A non-idempotent "issue credit" action under retry pressure during an incident — exactly when timeouts are most likely — issues duplicate credits at scale. Every mutating step needs an idempotency key on a unique external ID before any of this goes live.

**The design.**
- **Decide what has to be per-customer and what does not.** The *detection* is a bulk set operation. The *credit* is a bulk write. Only the *message* is arguably per-customer, and during a major outage even that is a templated notification rather than a conversation. So the agent is the wrong tool for the fan-out and the right tool for the follow-up — the customer who replies and asks a question.
- **Shape it as batch plus events.** Detect the affected cohort as a set. Issue credits through **Batch Apex**, which exists for a record set too large for one transaction. Publish a **platform event** per customer for the notification fan-out — small, self-describing, about a business fact, with an idempotency key and a timestamp in the payload, published **after commit** so a rolled-back credit does not notify. Then let the agent handle inbound replies, where per-customer reasoning is genuinely worth $0.10.
- **Check the freshness path too, since it is the trigger.** Detection depends on ingestion latency. If the connection-quality stream is scheduled rather than real-time, "degraded for ten minutes" is measured against stale data and the whole intervention fires late or wrongly. Agent-facing and intervention-triggering data needs real-time — and for CRM data specifically, **Accelerated Data Ingest** rather than a workaround that bypasses Data 360.
- **State the operational risk explicitly.** This system fires hardest exactly when the platform is under most stress. A design that consumes the daily async budget during an incident has removed the org's capacity to do anything else at the worst possible moment — and that is an argument the architect will recognise, because it is the same reasoning they would apply to their own network.

**The trap.** Answering the question as asked — will it scale — and tuning: batch size, a bigger licence tier, chunked enqueues. It concedes that per-record automation is the right shape and buys headroom until the next incident is 20% larger. The second trap is the reverse: rejecting the requirement as unbuildable. Proactive outage response is a legitimate and valuable thing to build; it just is not built one agent invocation at a time.

**Follow-ups they will ask.**
- "Why not the agent for the outbound message?" — cost and reliability with no benefit. During an outage every customer gets substantially the same message; paying per action for per-customer reasoning nobody reads is spend without value.
- "What about ordering?" — there is **no ordering guarantee between independent async jobs**. If credits must precede notifications, chain them or sequence the phases; do not enqueue both and hope.
- "How would you have caught this before build?" — count the limits against the peak case rather than the average. The peak here is 200,000 in minutes, and every ceiling in the design is a per-day or per-queue number.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names three independent ceilings, reframes it as a pattern error rather than a scale problem, redesigns to batch plus events with the agent on inbound only, raises non-idempotent credits under retry, and points out the system peaks when the platform is already stressed |
| 🟡 Partial | Identifies the async and queue limits and proposes Batch Apex, but keeps the agent in the fan-out or misses the cost and idempotency exposure |
| 🔴 Weak | Tunes batch sizes or licence tiers; or says it will scale with monitoring; or rejects the requirement outright |

**Ask this if they stall:** "Two hundred thousand customers, each getting an agent action at ten cents. What is the bill for one incident, and does the requirement survive it?"

</details>

---

### Q6 · The thing you would tell them not to build

**Level:** Complex · **Probes:** [Prebuilt agents & buy vs build](../../AI_Data/02-salesforce-ai/14-prebuilt-agents-and-buy-vs-build/notes.md) · [ADLC & Agentforce DX](../../AI_Data/02-salesforce-ai/13-adlc-and-agentforce-dx/notes.md) · [RAG on Platform](../../AI_Data/01-data-cloud/08-rag-on-platform/notes.md) · [Agent Script](../../AI_Data/02-salesforce-ai/07-agent-script/notes.md) · [Automation landscape & tool selection](../../SF_core/04-flow-and-automation/01-automation-landscape-and-tool-selection.md)

**Scenario.** A manufacturing client's CTO has a twelve-month agentic roadmap: seven custom agents across service, sales, field operations, procurement, HR onboarding, IT helpdesk and an internal "ask anything" knowledge agent. Budget is approved and the board has seen the roadmap. Their platform reality: an unmigrated org with surviving Workflow Rules and Process Builder, no Data 360, Knowledge last audited in 2021, and one Salesforce developer. They want you to sequence delivery. Nobody has asked whether the roadmap is right.

**Asked as:** "They asked for a sequence. What do you actually give them?"

<details><summary><b>Model answer</b></summary>

**Lead with.** A sequence, and a shorter roadmap — because at least three of the seven should not be built, and the first quarter has almost nothing to do with agents. Grounding is what determines whether any of these work, and right now there is no grounding layer: no Data 360, and a Knowledge base last audited five years ago.

**Then work through, and put the buy-vs-build cut first because it changes the scope.**
- **Apply the decision framework per agent, and the question that decides most cases is whether the differentiator is in the conversation or in the data.** IT helpdesk has a **50+ agent IT Service Domain Pack**. Service has **Help Agent**, GA and deploying in minutes. HR onboarding is a process-coordination shape that prebuilt families cover. For each of those, what makes this client different is *what the agent knows*, not how the conversation goes — so buy, and spend the budget on grounding. What is left worth building is field operations and procurement, where the process genuinely is unusual, and possibly sales.
- **Then the question nobody asked, which is the real value you add.** Seven custom agents is seven **ongoing commitments**, not seven deliverables. A custom agent is not a delivered artifact: drift has no commit, so somebody owns the outer loop forever — and that somebody is one developer. Prebuilt agents move that cost to Salesforce. Pricing the maintenance rather than only the build is the argument that will change the roadmap, and it is the one the CTO has not heard.
- **The "ask anything" knowledge agent is the one to push back on hardest.** It is the least well-specified and the most dependent on the layer that does not exist. An unaudited 2021 Knowledge base guarantees confident, obsolete answers, and stale grounding is the number-one root cause of "the agent was wrong" — misdiagnosed as a model problem almost every time. Built first, it would poison internal confidence in the whole programme. It is a good agent to build *last*, on a corpus somebody owns.
- **The sequence.**
  - **Q1 — foundations, and be blunt that this quarter has no agent in it.** Audit and retire Knowledge, and give it a named owner so it does not decay back. Stand up Data 360 with a minimal, correct model — standard DMOs, high-precision matching, and the agent-facing streams real-time rather than scheduled. Finish the legacy automation migration, because Workflow Rules and Process Builder are **out of support since 31 December 2025 but not retired**, and they still fire between the after-trigger and the after-save flow — unexplained behaviour under an agent that nobody will diagnose correctly.
  - **Q2 — buy, and prove the model.** Deploy Help Agent and the IT pack on the grounding built in Q1. This is the quarter that produces visible outcomes fast, which matters because the board has seen a roadmap and needs something delivered against it.
  - **Q3 — build the first custom agent** in Agent Script, with the CI pipeline: lint, compile in CI without an org, evaluations, deploy through the Metadata API, scorers on live sessions. One agent, done properly, establishes the pattern and the pipeline for everything after it.
  - **Q4 — the second custom agent, and the knowledge agent** if Q1's ownership actually held.
- **Then name the constraint that overrides the sequence.** One developer. Whatever is agreed, the throughput ceiling is one person, and prebuilt agents plus a pipeline is the only version of this roadmap that fits inside it. Say the number out loud.

**The trap.** Sequencing all seven as asked. It is what was requested, it is easy to produce, and it commits the client to seven maintenance streams and a knowledge agent that will fail publicly — while the grounding work that determines whether any of it succeeds stays unfunded because it was not on the roadmap. The related trap is the opposite: telling them the roadmap is wrong without giving them a delivery plan. A CTO with an approved budget and a board commitment needs a sequence they can present, not a critique.

**Follow-ups they will ask.**
- "The board approved seven agents. How do you sell four?" — you are not selling fewer outcomes, you are selling the same outcomes with three delivered by Salesforce and maintained by Salesforce. That is a better story than seven, not a reduced one.
- "What if they insist on an agent in Q1?" — deploy Help Agent on the current Knowledge base in a limited pilot and let the answer quality be the argument for the audit. It makes the grounding case with evidence rather than assertion.
- "Which single Q1 item would you refuse to drop?" — Knowledge ownership. Not the audit, the *owner*. A one-off audit decays; an owner is what makes every agent after it viable.
- "Why does the legacy automation matter for an agent programme?" — because an agent triggers saves, and surviving workflow rules fire in the middle of the order of execution. An unexplained value change under agent-driven automation is a debugging problem the one developer will lose days to.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Cuts the roadmap on buy-vs-build using conversation-vs-data, prices maintenance as the argument, puts a no-agent foundations quarter first, sequences one properly-built custom agent to establish the pipeline, and names the one-developer ceiling |
| 🟡 Partial | Sequences sensibly and puts Data 360 and Knowledge first, but delivers all seven as custom builds or misses the maintenance-commitment argument |
| 🔴 Weak | Sequences the seven as requested; or critiques the roadmap without producing a plan; or starts with the knowledge agent because it looks foundational |

**Ask this if they stall:** "Eighteen months after go-live, who is maintaining seven custom agents through model drift, and how many people does this client have?"

</details>
