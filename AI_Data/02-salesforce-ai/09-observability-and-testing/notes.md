# Observability & Testing

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** Refined Agent Analytics, Custom Scorers, `aiAgentScorerDefinitions` via Metadata API, Next Gen Testing, `agent preview`, trace files, and `@IntegrationTest`.

> **Why this folder exists.** "You can't really test it" used to be a legitimate objection to agent projects. Summer '26 is the release where that stopped being true, and answering the objection is now an architect-level differentiator.

## What is it?

The tooling that turns *"is the agent any good?"* from a vibe into a **versioned, testable definition**.

| Tool | Status | What it does |
|---|---|---|
| **Refined Agent Analytics** | GA | Unifies Service and Employee Agent analytics into one view, 40+ metrics |
| **Custom Scorers** | Beta | Grade live sessions against your own KPIs alongside Salesforce's standard quality metrics |
| **Next Gen Testing** | — | Build scorers and tests in Agentforce Studio |
| **`agent preview`** | GA | Scripted interactive test sessions from the CLI |
| **Trace files** | — | See exactly how an agent routed and acted in a preview session |
| **Agent evaluations** | Beta | YAML/JSON-defined evaluation tests for repeatable runs |
| **`@IntegrationTest`** | Dev Preview | Apex tests with live callouts and mid-transaction commits |

## Why it matters (for the AI-Salesforce architect role)

**The Metadata API support is the tell.** Custom Scorers can be deployed via the `aiAgentScorerDefinitions` metadata type, which means **evaluation is being treated as deployable infrastructure** — it lives in source control, gets reviewed, and ships through a pipeline like anything else.

Put that next to Agent Script compiling to JSON and a pattern emerges: Salesforce is deliberately making the *whole* agent lifecycle — definition, evaluation, deployment — behave like software engineering rather than configuration. If you come from an Apex/Flow background, that's your advantage.

**Commercially, this is what makes outcome pricing legible.** Under pay-per-resolution ($2 per autonomous resolution, escalations free) and Flex Credits, "how well is it working" is a revenue question, not a quality-assurance nicety. A client asking for ROI needs numbers from Agent Analytics, not assurances.

## How it works

### Custom Scorers — the developer workflow

Two paths, and the second is the one that matters:

1. **Agentforce Studio** — build scorers with Next Gen Testing in the UI.
2. **Metadata API** — deploy them as `aiAgentScorerDefinitions` so they live in source control, then activate from the **Scorer Hub** to run against live sessions.

Requires the **Agentforce Scorer Beta** permission set.

Salesforce ships standard quality metrics; scorers let you add your own — examples given include **Sentiment, Tone of Voice, Product Interest, Escalation Trigger, Politeness**. The useful ones are usually domain-specific: "did it cite a policy document", "did it avoid promising a refund".

### The full testing pyramid for an agent

```
 Custom Scorers (live sessions)     ← is it good in production?
 Agent evaluations (YAML/JSON)      ← repeatable behaviour tests, CI
 agent preview + trace files        ← did it route and act correctly?
 @IntegrationTest (scratch org)     ← does the action work against real callouts?
 Standard Apex unit tests           ← does the action's logic work?
```

Each layer catches something the layer below can't. The two new-in-2026 layers are the top and the middle-bottom.

### `@IntegrationTest` — and its limit

The `@IntegrationTest` Apex annotation allows **live callouts** and mid-transaction data commits via `IntegrationTest.commitTestOnly()`, with cleanup in a `@TearDown` method. Standard unit tests mock every callout and roll everything back, which makes asserting on real Agentforce or Data 360 behaviour impossible.

**Constraints:** scratch orgs only; add `ApexIntegrationTests` to the `features` array in the scratch org definition; tests run asynchronously, one at a time, via the Tooling API `runTestsAsynchronous` resource.

Be honest about that first constraint — **scratch-org-only keeps it out of most real pipelines for now.** It's the beginning of an answer, not the whole one.

### Trace files

After `sf agent preview start` → `send` → `end`, inspect the trace to see exactly how the agent routed and which actions ran. This is the primary diagnostic for [mis-routing](../08-multi-agent-orchestration/notes.md) — it shows you which subagent description won, which is the difference between guessing and knowing.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Run a preview session and read the trace file end to end.
- [ ] Write one domain-specific Custom Scorer (e.g. "cited a source") and deploy it via Metadata API rather than the UI.
- [ ] Define an agent evaluation in YAML and run it from the CLI.
- [ ] Write one `@IntegrationTest` in a scratch org against a real Data 360 callout.
- [ ] Open Refined Agent Analytics and pick the three metrics you'd put in front of a client. Most of the 40+ are noise for any given conversation.

## Gotchas & sharp edges

- **`@IntegrationTest` is scratch-org only** and runs asynchronously, one at a time. Don't plan a CI pipeline around it yet.
- **Custom Scorers are Beta** and need the *Agentforce Scorer Beta* permission set. Fine to prototype; don't make it load-bearing in a delivery commitment.
- **Scorers grade live sessions** — which means real customer conversations. Think about what you're logging and who can read it.
- **Compiling clean ≠ behaving well.** The Agent Script compiler validates structure only. This folder is where behaviour gets verified.
- **40+ metrics is too many.** Pick the few that map to the business outcome; the rest are dashboard decoration.
- **Testing Center actions are cheaper but not free** — 16 credits (~$0.08) each. A large evaluation suite has a real bill.
- **Preview ≠ production.** Preview sessions don't reproduce real user phrasing. Scorers on live sessions are what close that gap.

## Related topics

- [Agent Script](../07-agent-script/notes.md) — the CI pipeline this plugs into
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — trace files diagnose routing
- [Custom Agent Actions](../05-custom-agent-actions/notes.md) — what the lower test layers cover
- [Capstone: Agentforce use case](../../04-capstone/03-agentforce-use-case/notes.md) — measure the outcome with scorers
- [Evals (Claude track)](../../03-claude-cca/02-agentic-architecture/notes.md) — the vendor-neutral discipline
