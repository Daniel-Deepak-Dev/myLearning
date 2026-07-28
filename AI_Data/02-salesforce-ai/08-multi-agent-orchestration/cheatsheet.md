# Multi-Agent Orchestration — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

An orchestrator agent fronts many narrow specialist subagents — and **Atlas 3.0 routes by reading their descriptions**, which makes the description field executable configuration rather than documentation.

## Key terms
| Term | Definition |
|---|---|
| Orchestrator | The agent presenting a single point of contact, delegating to subagents. |
| Subagent description | **The routing contract.** What Atlas 3.0 actually reads to decide. |
| Agent Router | Add subagents under *Actions Available for Reasoning*; reference with `@`. |
| A2A | Open protocol for agents on *different* platforms to discover and call each other. |

## Rules of thumb

- One domain per subagent. Split on real boundaries, not tidiness — two agents that always run together should be one.
- **Every description states its exclusions** ("does NOT handle billing"). That clause prevents more failures than the positive text.
- Keep orchestration shallow: each hop is billed actions, so three subagents ≈ 3× cost.
- Mis-routing? Debug the **description** first. Not the model, not the prompt.

## Exam traps / common confusions

- **Status conflict:** GA dated June 15, 2026, but Help still labels *Connect Agent as Subagent* **(Beta)**. Verify in-org before quoting.
- Atlas 3.0 routes on descriptions, **not** a fixed decision tree — this is the change from earlier versions.
- **Multi-Agent Interoperability ≈ 5%** of the Agentforce Specialist exam: MCP, A2A, Agent API. Real overlap with the Claude track; not a reason to over-invest.
- Vague descriptions fail **intermittently** — they survive testing and surface in production.

## Minimal example

```
ORCHESTRATOR
├─ Order Support Agent
│    "Delivery status, shipping exceptions, refunds on
│     Delivered orders. Does NOT handle plan changes."
└─ Billing Agent
     "Plan changes, upgrades, downgrades, invoices.
      Does NOT handle physical delivery."

The "Does NOT" lines are the reliability mechanism.
```
