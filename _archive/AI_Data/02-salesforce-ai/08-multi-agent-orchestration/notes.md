# Multi-Agent Orchestration

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** Orchestrator and subagent wiring, descriptions as routing contracts, Agent Router, the A2A protocol — and the GA-vs-Beta documentation conflict.

> **Why this folder exists.** MAO went GA on **June 15, 2026**, after the original roadmap was written, and MCP/A2A now carry ~5% of the Agentforce Specialist exam.

## What is it?

**Multi-Agent Orchestration** lets an **orchestrator agent** connect to other specialized agents in the org and present a single point of contact. The user handles a cross-domain task without switching sessions, with context shared across channels.

The pattern is the same **orchestrator-worker** shape you'll meet in the Claude track — a lead agent decomposes a task, delegates slices to specialists, and synthesizes the result. Salesforce's version is configured rather than coded, and the routing decision is made by the model reading descriptions.

## Why it matters (for the AI-Salesforce architect role)

**The realistic enterprise pattern is many narrow, well-tested agents — not one omniscient one.** That's true for the same reasons microservices beat a monolith: smaller surface to test, independent ownership, and a failure that stays contained. Orchestration is what makes that pattern usable instead of just tidy.

**And it changes what "specification" means.** In a single-agent design, the risky prose is the instructions. In an orchestrated design, the riskiest text in the whole system is the **subagent description** — because **Atlas Reasoning Engine 3.0 routes by reading it**, not by following a fixed decision tree.

That makes the description field executable configuration. A vague description produces intermittent mis-routing that *looks* like a model failure but is a **specification failure**. Two consequences:

- Debugging starts at the description, not the model or the prompt.
- Write descriptions like API documentation: what this agent handles, what it explicitly does not, what it needs as input.

**The cost angle is real too.** You pay per action. An orchestrator that routes through three subagents costs roughly three times a direct hit. Orchestration depth is a budget decision, not just an architecture one.

## How it works

### Wiring it up

In Agentforce Builder, open a draft agent as the orchestrator, then in the Explorer panel: **+ → Connect Agent as Subagent**. Give each connected subagent a description — **that description governs routing behaviour**.

With **Agent Router**, add each subagent under *Actions Available for Reasoning* and reference it with `@`.

### The routing contract

```
user: "My order hasn't arrived and I want to change my plan."
        │
   ORCHESTRATOR
        │  Atlas 3.0 reads each subagent's DESCRIPTION
        ├──► Order Support Agent
        │      "Handles delivery status, shipping exceptions and
        │       refunds on Delivered orders. Does NOT handle
        │       subscription or billing plan changes."
        │
        └──► Billing Agent
               "Handles plan changes, upgrades, downgrades and
                invoice queries. Does NOT handle physical order
                delivery or shipping."
```

The explicit *does NOT* clauses are what make this reliable. Without them, two plausibly-overlapping descriptions produce non-deterministic routing that's very hard to diagnose after the fact — the same principle as [action descriptions](../05-custom-agent-actions/notes.md).

### Design rules

| Rule | Why |
|---|---|
| One domain per subagent | Narrow scope = testable, ownable, contained failure |
| Descriptions state exclusions | Prevents overlap-driven mis-routing |
| Keep orchestration shallow | Each hop is actions, and actions are billed |
| Version descriptions with the script | They're config; treat changes as behaviour changes |
| Test cross-domain utterances | The failure mode only shows up when two subagents both look plausible |

### A2A — Agent-to-Agent protocol

Where MAO orchestrates agents **within** the Salesforce estate, **A2A** is the open protocol for agents built on **different platforms** to discover and call each other. Alongside MCP and the Agent API it forms the *Multi-Agent Interoperability* section of the Agentforce Specialist exam — weighted around **5%**.

Keep that weighting honest: it's a genuine overlap with the [Claude/MCP track](../../03-claude-cca/05-mcp/notes.md), and worth studying once for both. It is not a reason to reallocate serious study time.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Build two narrow subagents with deliberately **overlapping** descriptions, then send an ambiguous utterance and watch it mis-route. Then add *does NOT* clauses and re-run. This is the lab that teaches the topic.
- [ ] Wire an orchestrator over both and trace a cross-domain request end to end.
- [ ] Read the trace file to see which description won the routing decision.
- [ ] Count the actions consumed by one orchestrated resolution and multiply out the Flex Credits cost.

## Gotchas & sharp edges

- **Documentation conflict, unresolved.** Secondary sources date GA to **June 15, 2026**, but Salesforce Help still labels the in-builder *Connect Agent as Subagent* step **(Beta)** — product page and setup docs disagree. **Verify in your own org before quoting a status to a client.**
- **Mis-routing is a specification bug.** Debug the description before touching the model or the prompt.
- **Vague descriptions fail intermittently**, which is worse than failing consistently — it survives testing and surfaces in production.
- **Depth costs money.** Three subagents ≈ three times the actions.
- **Shared context is a feature and a risk.** Context flows across the session; be deliberate about what a subagent can see, especially where subagents have different data sensitivities.
- **Don't decompose prematurely.** Two agents that always run together should probably be one. Split on genuine domain boundaries, not on tidiness.

## Related topics

- [Agent Script](../07-agent-script/notes.md) — where subagents and descriptions are declared
- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — where routing sits in the runtime path
- [Custom Agent Actions](../05-custom-agent-actions/notes.md) — the same description-as-contract principle
- [Observability & testing](../09-observability-and-testing/notes.md) — trace files and scorers for routing quality
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) · [Agentic architecture](../../03-claude-cca/02-agentic-architecture/notes.md) — orchestrator-worker, vendor-neutral
