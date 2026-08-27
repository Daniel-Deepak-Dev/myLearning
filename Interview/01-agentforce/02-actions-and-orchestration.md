# Agentforce — Actions & Orchestration

> Area: Agentforce · Set 02 of 03 · Scenarios: 4 · Level: medium→complex · Currency: **Summer '26 (API 67.0)**

**Drills:** the description field is executable configuration, and the reasoning engine never reads your Apex. Three of these four failures look like model failures and are specification failures. The fourth is an API upgrade that breaks working code.

---

### Q1 · The agent issues two refunds

**Level:** Medium · **Probes:** [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Idempotency & retries](../../SF_core/06-integration-and-apis/23-idempotency-retries-and-error-handling.md)

**Scenario.** A commerce client's agent has an `IssueRefund` action — invocable Apex, well-tested, 100% coverage, works perfectly when called from Flow. Since going live with the agent, finance has found eleven customers who received two identical refunds within seconds of each other. The Apex has no loop, and the agent's trace shows a single user request. The action's own logs show two invocations. The developer's position is that the Apex is correct and the agent is "calling it twice for no reason."

**Asked as:** "The developer says their code is fine. Are they right?"

<details><summary><b>Model answer</b></summary>

**Lead with.** The Apex is correct and also the defect. It is not idempotent, and an agent is a caller that retries — so an action that could safely be non-idempotent when a human clicked a button in Flow cannot be non-idempotent when an agent invokes it after a timeout.

**Then work through.**
- **Why the agent legitimately calls twice.** A timeout is not a failure — it means the caller does not know whether the work happened. The agent times out waiting, does not know the refund was issued, and retries. That is correct behaviour from the caller. **Correctness has to come from the receiver.**
- **Why Flow never exposed this.** A human waits, sees an error or a success, and decides. Nobody re-clicks in under a second. The retry semantics are new, not the code.
- **The fix.** An **idempotency key** the caller sends on every attempt, stored on a custom object with a **unique external ID**. The uniqueness constraint does the deduplication and `DUPLICATE_VALUE` is the signal to return the first result rather than issue a second refund. Idiomatic on this platform and cheap to add.
- **Give the key an expiry from day one**, or the dedupe table becomes the largest object in the org.
- **The scope question this raises.** Eleven cases found by finance means the blast radius is every non-idempotent action wired into an agent, not just this one. The review is: inventory every action an agent can invoke, and for each ask "if this runs twice, what happens?" Actions written for Flow or LWC were never reviewed against that question. This is the same exposure an MCP client creates — a retrying external client hitting endpoints nobody reviewed for repeats.

**The trap.** Fixing it in the agent — instructing it not to retry, or adding a guardrail. You cannot make a distributed caller stop retrying, and you should not want to: retrying is how it recovers from real transient failures. Suppressing the retry converts double-refunds into silently-dropped refunds, which finance will like even less.

**Follow-ups they will ask.**
- "Where else does this bite?" — anything that creates, charges, sends, or increments. Reads are safe. `Upsert` on an external ID is idempotency you get for free.
- "How would you have caught it in testing?" — invoke the action twice with the same inputs and assert one effect. That is a one-line test nobody writes because the Flow contract never required it.
- "Cost angle?" — every action invocation is roughly **20 credits (~$0.10)**, so a retry storm is a billing event as well as a correctness one.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | "A timeout is not a failure" reasoning, puts correctness in the receiver, names the unique-external-ID pattern, and widens the finding to every agent-invocable action |
| 🟡 Partial | Identifies the double-invocation as a retry and suggests a dedupe check, but frames it as a bug in the agent rather than a contract change for the action |
| 🔴 Weak | Agrees the Apex is fine and looks for the bug in Agentforce; or proposes a `static Boolean alreadyRan` guard, which does not survive two transactions |

**Ask this if they stall:** "The agent waited four seconds, got nothing back, and had to decide something. What were its options?"

</details>

---

### Q2 · Nothing changed except the version number ⚠️

**Level:** Medium · **Probes:** [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Invocable Apex & Agentforce actions](../../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md) · [Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md)

**Scenario.** A developer bumps one Apex class from API 64.0 to 67.0 to use an unrelated new method. The class is an `@InvocableMethod` wired into a live agent, and it takes a custom Apex type as its input. They deploy to a full sandbox. The deployment succeeds. The agent action now fails at runtime, and a second action in the same class returns fewer records than it did yesterday for some users but not others. Nobody touched the agent, the Flow, or the data.

**Asked as:** "Deployment green, runtime broken, no functional change. Walk me through it."

<details><summary><b>Model answer</b></summary>

**Lead with.** Two separate 67.0 behaviour changes fired at once, both triggered purely by the version bump. The failure is almost certainly the **missing no-arg constructor** on the input type, and the shrinking result set is **user mode becoming the default** for database operations.

**Then work through.**
- **The hard failure.** Any custom Apex type used as an invocable action input must expose a visible **no-argument constructor** — `public`, or `global` for packaged classes. The mechanism is ordinary OO behaviour: declaring any constructor with arguments removes the compiler-generated default one. This is the first thing to check when an action breaks after an API bump, and it is the most common casualty. Note the actual boundary: **the requirement starts at API 66.0**, not 67.0 — Summer '26 is when the Release Update auto-activates, which is why most write-ups misdate it.
- **The quiet one.** At 67.0, SOQL, SOSL, DML and `Database` methods default to **user mode** — enforcing the running user's object permissions, FLS and sharing. Fewer records for *some users but not others* is that working correctly, which is why it is not a bug. If elevated access is genuinely required, opt in explicitly with `WITH SYSTEM_MODE` and document why. Also check whether the class relied on having no sharing keyword: keyword-less classes now default to **`with sharing`** instead of inheriting the caller's context.
- **The one that would not have deployed.** `WITH SECURITY_ENFORCED` no longer compiles at 67.0. Grep for it before any upgrade. The replacement, `WITH USER_MODE`, is materially better rather than renamed — it handles polymorphic fields, checks the `WHERE` clause and not just the `SELECT` list, and reports every FLS violation instead of only the first.
- **Why the deployment stayed green.** All of these are runtime semantics, not compile errors — except `SECURITY_ENFORCED`. The compiler had nothing to complain about.

**The trap.** And this is the actual point of the question: treating this as one developer's mistake. The risk is **asymmetric and organisational**: these semantics apply to classes *compiled at 67.0*, so nothing breaks on upgrade day, and existing classes keep their old behaviour indefinitely. Which means the trigger is somebody bumping a class's API version **for an unrelated reason** — exactly what happened here — and its data access semantics changing underneath them. That deserves a written team convention, not a verbal one: bumping an API version on an agent-facing class is a security-relevant change and gets reviewed as one.

**Follow-ups they will ask.**
- "How do you find the exposure across the org?" — inventory classes below 66.0 that are invocable or agent-facing, and grep for `SECURITY_ENFORCED` and for classes with no sharing keyword.
- "The running user now sees less. Bug or feature?" — feature. Under user mode the running user's permissions *are* the access control, not the code. An action returning less may be correct for the first time.
- "Where does this leave triggers?" — triggers now **always** run in system mode and cannot declare sharing or access modes at all. Which makes a trigger the wrong place for security-sensitive logic; push it into a handler where you control the mode explicitly.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Names the no-arg constructor first, separately explains the user-mode default for the shrinking result set, and lands on the asymmetric-risk point — the danger is an unrelated version bump, so it needs a written convention |
| 🟡 Partial | Knows 67.0 changed access defaults and can explain the user-mode half, but does not get to the constructor, or treats both symptoms as one cause |
| 🔴 Weak | Debugs the agent, the action wiring or the data; or blames the sandbox; or suggests rolling the version back without knowing what changed |

**Ask this if they stall:** "One symptom is a hard failure and the other is a smaller result set for some users. Are those the same root cause?"

</details>

---

### Q3 · The orchestrator routes fine on Tuesdays 🆕

**Level:** Complex · **Probes:** [Multi-Agent Orchestration](../../AI_Data/02-salesforce-ai/08-multi-agent-orchestration/notes.md) · [Observability & Testing](../../AI_Data/02-salesforce-ai/09-observability-and-testing/notes.md) · [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md)

**Scenario.** A telco runs an orchestrator over four subagents: Order Support, Billing, Technical Support, Retention. It passed a 200-utterance UAT suite. In production, roughly 8% of sessions reach the wrong subagent, and the pattern is maddening — the *same* utterance routes correctly most of the time and incorrectly sometimes. "My bill is wrong because my upgrade never activated" is the worst offender, landing in Billing or Order Support unpredictably. Separately, finance has flagged that average cost per resolved session is 3.4× the projection. The client wants to fine-tune a model.

**Asked as:** "Intermittent mis-routing and a 3.4× cost overrun. Related or not?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Related, and both trace to the same design decision. Atlas 3.0 routes by **reading subagent descriptions**, so intermittent mis-routing is a specification failure in overlapping descriptions — not a model failure. And the cost overrun is orchestration depth: you pay per action, so every hop multiplies. Fine-tuning a model addresses neither.

**Then work through.**
- **Why intermittent is the diagnostic.** Consistent mis-routing means a wrong description. *Intermittent* mis-routing on identical input means **two descriptions both look plausible** to the reasoning engine, and the tie breaks non-deterministically. That is worse than failing consistently, because it survives testing and only surfaces at production volume — which is exactly what happened to the 200-utterance suite.
- **The fix is the `does NOT` clause.** Descriptions have to state exclusions, not just capabilities. Billing: "Handles plan changes, upgrades, downgrades and invoice queries. Does **NOT** handle physical order delivery or provisioning failures." Order Support: the mirror. Those explicit negative boundaries are what make routing reliable, and their absence is the whole bug.
- **The worst offender is genuinely cross-domain, and that is a design answer not a wording one.** "My bill is wrong because my upgrade never activated" contains a billing symptom and a provisioning cause. No single description makes that unambiguous, because it legitimately spans two domains. Either the orchestrator is allowed to consult both and synthesize — which costs two hops — or one subagent owns the composite journey. Pick deliberately and price it.
- **Read the traces, do not theorize.** Trace files show which description won each routing decision. That is the difference between guessing and knowing, and it is the first thing to pull on the 8%.
- **Now the cost.** Each hop is billed actions at roughly **20 credits (~$0.10)** per invocation. A 3.4× overrun says the projection assumed roughly one subagent per session and reality is closer to three — partly genuine cross-domain work, partly **re-routing after a mis-route**, which bills both the wrong hop and the right one. So fixing the descriptions cuts the bill directly. The two problems have one fix, which is the answer to the question as asked.
- **The structural check.** Four subagents on a domain this entangled invites the question of whether the decomposition is right. Two agents that always run together should probably be one — do not decompose on tidiness, only on genuine domain boundaries. Depth is a budget decision as much as an architecture one.

**The trap.** Reading intermittency as model non-determinism and reaching for a model lever — fine-tuning, pinning a stronger model, lowering temperature. It is a plausible read and it is wrong: the routing input is the description text, and ambiguous input produces ambiguous output from any model. A stronger model resolves an ambiguous tie *more confidently*, not more correctly, and you have then paid more per hop for the same 8%.

**Follow-ups they will ask.**
- "How do you test for this properly?" — cross-domain utterances specifically, since the failure only appears when two subagents both look plausible. Then encode them as agent evaluations in YAML so they run in CI, and put a scorer on routing correctness against live sessions.
- "Shared context across subagents — problem?" — it is a feature and a risk. Context flows across the session, so be deliberate about what each subagent can see, especially where two have different data sensitivities.
- "How would you have priced this upfront?" — count the actions consumed by one orchestrated resolution in preview and multiply out. The number is available before go-live.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Connects both symptoms to one cause, treats intermittency as the signature of overlapping descriptions, prescribes `does NOT` clauses, reads traces before theorizing, and identifies the genuinely cross-domain utterance as needing a design decision rather than better wording |
| 🟡 Partial | Gets that descriptions drive routing and should be tightened, but treats the cost overrun as a separate problem, or misses that re-routing bills twice |
| 🔴 Weak | Model tuning, temperature, prompt rewrites; or proposes a hard-coded keyword router, discarding the reason to use orchestration at all |

**Ask this if they stall:** "The same sentence routes two different ways. What is the routing decision actually reading?"

</details>

---

### Q4 · Six weeks to build what already exists 🆕

**Level:** Complex · **Probes:** [Custom Agent Actions](../../AI_Data/02-salesforce-ai/05-custom-agent-actions/notes.md) · [Flows as Agentforce actions](../../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) · [Custom Lightning types for agent output](../../SF_core/03-lwc-and-slds/19-custom-lightning-types-for-agent-output.md) · [Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md)

**Scenario.** You inherit an Agentforce project mid-flight. The team has scoped six weeks to build fourteen new `@InvocableMethod` actions. Reading the org, you find that eleven of the fourteen capabilities already exist — four as Apex REST endpoints serving a partner integration, five as `@AuraEnabled` controller methods behind existing LWCs, two as autolaunched Flows the admin team maintains. The team's reasoning: "those aren't agent actions, they're APIs and controllers." Delivery is fixed and the client is watching the burn rate.

**Asked as:** "How much of that six weeks do you give back, and what do you do with the rest?"

<details><summary><b>Model answer</b></summary>

**Lead with.** Most of it. Since Spring '26, **Apex REST endpoints and `@AuraEnabled` methods can be exposed directly as agent actions** — so nine of those eleven need wiring and description work, not a rewrite. The team's premise is a year out of date, and it is the single most commonly missed item when scoping an Agentforce project.

**Then work through.**
- **What the six weeks becomes.** Inventory what is already exposed before building anything new — that is the first scoping step on any Agentforce engagement. Here: nine existing methods get wired and described, the two Flows stay Flows, and three genuinely new capabilities get built. Call it two weeks of real work, and the recovered time is not free budget — it goes to the parts that actually determine whether this ships.
- **Where the recovered time goes, in priority order.**
  - **Descriptions**, and this is the highest-leverage work on the project. The reasoning engine never reads your Apex — it reads the action description to decide relevance, the input descriptions to decide what to pass, and the output descriptions to decide what the result means. Write them like prompts, not field labels: not `Account ID` but "The 18-character Salesforce ID of the Account to credit. Must be an existing Account the running user can edit." And include the **negative** boundary — "Do not use for exchanges" — because that clause is how you stop mis-selection between two similar actions. Fourteen actions with vague descriptions is a mis-selection problem waiting to happen.
  - **A security review of the reused nine**, which is the real cost of reuse and the thing to raise before the client hears "we saved four weeks." Those methods were written for a partner integration and for LWCs — callers with a known shape and a human or a contract behind them. An agent is a different caller: it may invoke them in combinations nobody designed for, and it may retry. Two specific checks. Are they **idempotent**? And what do they do under **user mode**, now the 67.0 default — a method that assumed system-mode access may return less, or a keyword-less class may now default to `with sharing` where it previously inherited the caller's context.
  - **Typed outputs.** Where an action returns a structured type rather than prose, a **Custom Lightning Type** attaches purpose-built UI — defined once, rendering on desktop LWC and natively in mobile. Prose output cannot be rendered specially anywhere. Worth doing on the handful of actions whose results reps actually read.
- **Keep the Flows as Flows.** The admin team owns and maintains them. Rewriting working declarative logic into Apex to make it "a proper action" adds a maintainer dependency and removes it from the people who understand the business rules.

**The trap.** Presenting this purely as a four-week saving and moving on. Reuse transfers the *caller* assumptions without transferring the *review*: nine endpoints hardened for a partner integration and a UI are now reachable by an autonomous caller. That is precisely why the platform flipped to user mode by default — it stopped assuming the caller had already filtered the data, an assumption that was safe for a Lightning page and is not safe for an agent. Claiming the saving without the review is how the saving becomes an incident.

**Follow-ups they will ask.**
- "Which of the eleven would you *not* reuse?" — anything whose partner contract makes it non-idempotent or destructively broad; and anything whose description you cannot write honestly without a long list of exclusions, which is a signal the method does too much for an agent to select safely.
- "The client wants all fourteen anyway, for consistency." — consistency of implementation is not a client outcome. The agent cannot tell the difference; the maintenance cost can.
- "Same methods over MCP?" — that is the other half of the reuse story. An `@InvocableMethod` exposed through a custom hosted MCP server serves an external Claude client with the org's full sharing and security model enforced. Same method, same enforcement, two consumers — but "who can create a hosted MCP server" belongs on a security review checklist, not in a developer's discretion.

</details>

<details><summary><b>Interviewer rubric</b></summary>

| Signal | Sounds like |
|---|---|
| 🟢 Strong | Knows Apex REST and `@AuraEnabled` became agent-callable in Spring '26, reallocates the time to descriptions rather than banking it, and raises the security review of reused endpoints unprompted — including idempotency and the user-mode default |
| 🟡 Partial | Spots the reuse opportunity and the saving, but treats the reused endpoints as done once wired, or undervalues description work as documentation |
| 🔴 Weak | Accepts that agent actions must be purpose-built; or proposes rewriting the working Flows into Apex for consistency |

**Ask this if they stall:** "Those four Apex REST endpoints — what is actually different between a partner system calling one and an agent calling one?"

</details>
