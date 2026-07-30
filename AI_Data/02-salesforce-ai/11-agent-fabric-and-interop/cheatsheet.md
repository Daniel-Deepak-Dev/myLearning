# MuleSoft Agent Fabric — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

A **MuleSoft-licensed control plane** that registers, governs, routes and visualizes every agent and MCP endpoint an enterprise runs — **including the ones not built in Agentforce**. Launched September 2025; scanners GA January 2026; guided determinism announced April 15, 2026.

## Key terms
| Term | Definition |
|---|---|
| Agent Registry | Central, **federated** catalog of agents, MCP servers and A2A endpoints. Registries reference each other — DNS-shaped, not a corporate directory. GA Oct 2025. |
| Agent Broker | Graph-based routing that delegates tasks across A2A agents, grouped into business domains. **Status disputed — verify.** |
| Omni Gateway | **Formerly Flex Gateway.** Same runtime, expanded to govern AI/MCP/A2A traffic. Rename is cosmetic and non-breaking (1.13.0). |
| Agent Visualizer | Live map: network structure, request flows, latency, error rates. GA Oct 2025. |
| Agent Networks | Multi-agent composition declared in **YAML** (agents, brokers, LLMs, MCP servers), deployed to CloudHub 2.0. |
| Agent Scanners | Auto-discover agents in **Agentforce, Bedrock, Vertex AI, Copilot Studio**. GA Jan 2026. The shadow-agent finder. |
| Guided determinism | Goal-based LLM reasoning + codified handoff rules + human checkpoints. Hybrid Reasoning, one level up. Apr 15 2026. |
| MCP Bridge | Turns an existing API into an MCP server **by configuration**, no code. |

## Rules of thumb

- **The one-sentence distinction:** Agentforce orchestration coordinates agents *inside one org*; Agent Fabric coordinates agents *across vendors*.
- **Registered ≠ governed.** Policy applies only to traffic routed through the gateway. A registered but directly-reachable agent is catalogued *and* ungoverned — and looks managed.
- If a client already runs Copilot Studio or Bedrock agents, **this is the product that answers "what happens to those"**.
- Gateway policy governs traffic. **Sharing rules and FLS still decide what a Salesforce agent may see.**

## Exam traps / common confusions

- **"Agent Script" names two products.** Agentforce's authoring language (Apache 2.0) *and* "Agent Script for Agent Broker" (guided determinism). Ask which.
- **Flex Gateway ≠ retired.** It was *renamed* to Omni Gateway. Both names circulate; older docs say Flex.
- **Agent Fabric is MuleSoft, not Agentforce.** Separate licence. **No public pricing found — do not scope on it.**
- **Agent Broker status is genuinely unclear**: launch coverage says GA Oct 2025, later coverage says Beta from Apr 2026. Don't quote a status you haven't checked.
- Registry is **federated**, not centralized — a common misread.

## Minimal example

```
Agent Fabric — four pillars, four components

  Discovery     → Agent Registry     (manual · scanners · MCP Bridge · MCP/A2A Connector)
  Governance    → Omni Gateway       (ex-Flex Gateway) + Governance Strategies
  Orchestration → Agent Broker       + Agent Networks (YAML → CloudHub 2.0)
  Observation   → Agent Visualizer   + service/org monitoring

scanners cover: Agentforce · Amazon Bedrock · Google Vertex AI · Microsoft Copilot Studio
```
