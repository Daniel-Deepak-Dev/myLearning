# 04 · Cross-Domain

The scenarios with no single-domain answer. In every one of these the constraint that decides the question sits in a different area from the symptom — which is why they are the architect-level ones, and why they come last.

> **Work the other three areas first.** These six assume you can already answer within Agentforce, Data 360 and the core platform separately. The skill being tested here is different: noticing that the question you were asked is not the question that needs answering.

| Set | Scenarios it drills | Level |
|---|---|---|
| [01 · Architect scenarios](01-architect-scenarios.md) | Two signed-off requirements that appear to contradict · a six-axis cost model across three products · isolating which layer is lying when an agent is partly wrong · an ungoverned hosted MCP server · a bulk intervention designed as per-record automation · a seven-agent roadmap with no grounding layer | complex |

**6 scenarios.** All complex by construction — a cross-domain question that resolves inside one area is not one.

## What is actually being tested

| The move | What it looks like |
|---|---|
| **Refusing the framing** | Four of the six arrive with a premise that is wrong or imprecise. "Will it scale?", "which number is right?", "sequence these seven" — answering as asked is the failure |
| **Locating the constraint** | The symptom is in Agentforce; the cause is in sharing, or ingestion, or a match rule. Naming the layer is most of the answer |
| **Pricing the trade-off** | Not "which is better" but what the alternative costs, in credits, in profiles, in maintenance, in risk |
| **Saying the uncomfortable thing** | The requirement is wrong; the business case was incomplete; the roadmap is three agents too long. Delivered with a plan attached, not as a critique |

## The seams these scenarios exploit

Three facts that reach across all three areas, and every scenario here turns on at least one:

1. **An agent has no access boundary of its own.** It runs as a user and inherits that user's access exactly. So a sharing gap presents as an AI defect, and a permission set scoped for a human is not scoped for a caller that aggregates at machine speed.
2. **The Trust Layer governs the model interaction — one layer of three.** Platform security governs who can see which records; agent design governs what the agent may do. Treating the Trust Layer as the whole security answer is the most common expensive misreading in this material.
3. **Grounding quality is a data-architecture output.** Stale ingestion, a fragmented profile or an undefined metric produces a fluent, specific, confident wrong answer — and it is reported as a model problem almost every time.

## Related

- [01-agentforce/](../01-agentforce/INDEX.md) · [02-data-360/](../02-data-360/INDEX.md) · [03-core-platform/](../03-core-platform/INDEX.md) — the three areas these compose
- [AI_Data/04-capstone/](../../AI_Data/04-capstone/INDEX.md) — the shipped proof. A capstone you have built is the strongest possible answer to any of these, because it converts an argument into an artifact
- [WEAK-ANSWERS.md](../WEAK-ANSWERS.md) — expect to log misses from this set. That is the set working, not you failing
