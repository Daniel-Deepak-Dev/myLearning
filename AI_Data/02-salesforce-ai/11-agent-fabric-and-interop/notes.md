# MuleSoft Agent Fabric & cross-vendor interop

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26** · Product status: **mostly GA, with one Beta** — see the status table below · sources in [05-release-radar/developer-tooling-and-apis.md](../../05-release-radar/developer-tooling-and-apis.md)

**Scope:** the control plane for agents you did *not* build — registry, broker, gateway, visualizer — plus how MCP and A2A actually get governed at the network level, and where this sits relative to Agentforce's own orchestration.

> **Why this folder exists.** Every other topic in this track assumes the agent is yours: you author it, ground it, test it, deploy it. Agent Fabric assumes the opposite — that a large enterprise already runs agents in Agentforce *and* Bedrock *and* Vertex AI *and* Copilot Studio, nobody has a list of them, and no policy applies consistently across them. That's the architect's problem, not the builder's, and it's the problem this product exists for. It was also **completely absent from this study base until 2026-07-28** despite launching in September 2025.

## What is it?

**MuleSoft Agent Fabric** is a unified control plane — "a single pane of glass to register, manage, govern and observe all of your agents and MCP endpoints." Note the vendor in the name: this is a **MuleSoft** product, sold and licensed separately from Agentforce, that happens to treat Agentforce as one registered platform among several.

Salesforce's framing is *agent sprawl*: the same thing that happened to APIs in 2015 is happening to agents now. Shadow agents get built, nobody can find them to reuse, and each one negotiates its own security. Agent Fabric is the API-management playbook applied to agents — and MuleSoft is the part of Salesforce that already knows that playbook.

### The four pillars

| Pillar | Component | What it does |
|---|---|---|
| **Discovery** | **Agent Registry** | Central catalog of every agentic asset: custom agents, agents embedded in SaaS apps, MCP servers fronting legacy systems, A2A endpoints |
| **Governance** | **Omni Gateway** + Governance Strategies | Runtime layer *between* agents and the systems they reach; enforces security, compliance and cost policy |
| **Orchestration** | **Agent Broker** + Agent Networks | Graph-based routing that delegates tasks across A2A-compliant agents |
| **Observation** | **Agent Visualizer** + monitoring | Live map of network structure, request flows, latency and error rates |

### Status and dates

| Thing | Status | Date |
|---|---|---|
| Agent Fabric launched | — | **September 2025** |
| Agent Registry | GA | October 2025 |
| Agent Visualizer | GA | October 2025 |
| Agent Governance (via gateway) | Available | at launch |
| Agent Broker | **GA per launch-era coverage; a later source still calls it Beta in April 2026** | see caveat below |
| Agent Scanners — Agentforce, Amazon Bedrock, Google Vertex AI, Microsoft Copilot Studio | GA | **January 2026** |
| Curated third-party MCP servers in the Registry | GA | January 2026 |
| Guided determinism, drag-and-drop canvas, LLM governance layer | announced | **April 15, 2026** |

> ⚠️ **Conflicting sources on Agent Broker.** Launch coverage says Broker GA'd in October 2025; later coverage of the April 2026 expansion describes a Broker Beta beginning April 2026. The most likely reconciliation is that the *base* Broker is GA and the *new guided-determinism* capability entered Beta in April — but that is inference, not a sourced fact. **Verify current status before quoting it**; see the radar's open questions.

## Why it matters (for the AI-Salesforce architect role)

**It's the answer to a question clients will ask before they ask anything else.** "We already have agents in Copilot Studio and Bedrock — what happens to those?" Without Agent Fabric the honest answer is "nothing, they stay separate." With it, the answer is a registry entry, a scanner and a policy. That is an architecture conversation, and it's one you can only have if you know this product exists.

**It reframes MCP and A2A from protocols into governed traffic.** [MCP](../../03-claude-cca/05-mcp/notes.md) and A2A are covered in this study base as *how agents connect*. Agent Fabric adds the missing layer: every A2A and MCP call routes through the gateway, so policy applies at every endpoint rather than per integration. This is the enterprise answer to "who authorised that agent to call that tool" — and it's the same instinct behind Salesforce's hosted MCP servers respecting org sharing.

**It draws the boundary around [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md).** Learn the distinction as a single sentence:

> **Agentforce orchestration coordinates agents *inside one org*. Agent Fabric coordinates agents *across vendors*.**

Both route on descriptions, both need well-specified subagents, but they operate at different altitudes and are licensed differently. Confusing them in a client conversation is the fastest way to lose the room.

**Exam relevance.** The Agentforce Specialist exam's **Multi-Agent Interoperability** domain covers MCP, A2A and the Agent API — see [the exam guide](../_cert-agentforce-specialist/exam-guide.md), noting the unresolved weighting question there. Agent Fabric is not itself named in the guide, but it is the product that makes those three protocols concrete.

## How it works

```
   REGISTER                    GOVERN                     ORCHESTRATE
   ────────                    ──────                     ───────────
   Agentforce agents  ─┐
   Bedrock agents     ─┤                                  Agent Broker
   Vertex AI agents   ─┼──► Agent Registry ──► Omni ────►  graph-based
   Copilot Studio     ─┤    (federated)       Gateway      routing over
   MCP servers        ─┤          ▲           policy at    A2A agents
   A2A endpoints      ─┘          │           every call        │
                                  │                             ▼
                          scanners (GA Jan 2026)          Agent Networks
                          MCP Bridge / MCP Connector       defined in YAML
                          A2A Connector                    (agents, brokers,
                          manual via Exchange               LLMs, MCP servers)
                                  │                             │
                                  └──────► Agent Visualizer ◄────┘
                                           structure · flows · latency · errors
```

### Getting things into the registry

Five paths, and the middle three are the interesting ones:

- **Manual registration** in the Portfolio / Exchange — the MuleSoft catalog you may already know from APIs.
- **Automated scanners** — continuously discover and register agents across Agentforce, Bedrock, Vertex AI and Copilot Studio. GA January 2026. This is the "find the shadow agents" feature.
- **MCP Bridge** — converts an existing API into an MCP server *by configuration*, no code. If you have a REST estate, this is how it becomes agent-reachable.
- **MCP Connector** — for building custom MCP servers.
- **A2A Connector** — makes an application A2A-compliant so it can join an agent network.

**The registry is federated.** Anyone can run a registry and registries can reference each other, so the catalog grows without a central authority — deliberately the same shape as DNS rather than a single corporate directory. That design choice is what makes cross-company agent discovery plausible at all.

### Agent Networks

Multi-agent compositions are declared in **YAML** — which agents, which brokers, which LLMs, which MCP servers participate — and deployed to **CloudHub 2.0**. Same instinct as Agent Script compiling to portable JSON: the topology becomes a versionable artifact rather than a diagram in someone's slide deck.

### Guided determinism (April 15, 2026)

The headline of the April expansion. It pairs autonomous, goal-based LLM reasoning with **codified handoff rules and human checkpoints** — deterministic guardrails wrapped around non-deterministic routing. If that sounds familiar, it should: it is the same design point as Agent Script's Hybrid Reasoning, applied one level up at the network rather than inside a single agent. Shipped alongside a drag-and-drop workflow authoring canvas and a centralised **LLM governance layer** for cost, compliance and model routing across multiple providers.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Read one Agent Network YAML end to end and map each block onto the diagram above. Do this before touching any UI.
- [ ] Sketch the two-layer picture for a hypothetical Geeksoft client: Agentforce agents orchestrated in-org, that whole org registered as one node in a Fabric registry alongside a non-Salesforce agent. This diagram is the reusable client artifact.
- [ ] Write the one-sentence distinction between Agentforce orchestration and Agent Fabric from memory, then check it against the notes above.
- [ ] Trace where an MCP call from Claude to a Salesforce hosted MCP server would — and would not — be visible to Agent Fabric. See [MCP](../../03-claude-cca/05-mcp/notes.md) and the hosted-MCP entry in [developer tooling](../../05-release-radar/developer-tooling-and-apis.md).
- [ ] **Before any client work:** establish what Agent Fabric actually costs and what MuleSoft entitlement it needs. No public pricing was found.

## Gotchas & sharp edges

- **"Agent Script" means two different things.** In Agentforce it is the authoring language for a single agent ([07-agent-script](../07-agent-script/notes.md), Apache 2.0). In the April 2026 expansion, *"Agent Script for Agent Broker"* names the guided-determinism feature at the network layer. Same words, different products. Ask which one someone means.
- **Flex Gateway was renamed Omni Gateway.** Same runtime, carried forward and expanded to govern AI agents, MCP and A2A traffic alongside the APIs it already handled — a **non-breaking, cosmetic change** to UI and docs (Omni Gateway 1.13.0), so CI/CD pipelines are unaffected. Expect both names in the wild indefinitely; older MuleSoft material and some Agent Fabric launch coverage still say Flex Gateway.
- **It is MuleSoft-licensed, not part of an Agentforce SKU.** No public pricing or licensing detail was located in any source consulted. Treat commercials as **unverified** and confirm with an AE before scoping.
- **Agent Broker status is genuinely unclear** — see the warning in the status table. Don't state a status you haven't checked.
- **A registry entry is not governance.** Registering an agent makes it *discoverable*; policy only applies to traffic that actually routes through the gateway. An agent registered but reached directly is catalogued and ungoverned — the worst of both worlds, because it looks managed.
- **This is not a substitute for a sharing model.** Gateway policy governs agent-to-tool and agent-to-agent traffic. What a Salesforce agent may *see* is still decided by sharing rules and FLS — the lesson from [Agentforce Coworker](../10-agentforce-coworker/notes.md), unchanged.
- **`docs.mulesoft.com` describes the current product; launch-era articles describe September 2025.** Where they disagree — component names especially — prefer the docs.

## Related topics

- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — the in-org layer; A2A, Agent Router, subagent descriptions
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) — the protocol Agent Fabric governs
- [Agentforce Coworker](../10-agentforce-coworker/notes.md) — inherited governance, the in-org counterpart to gateway policy
- [ADLC & Agentforce DX](../13-adlc-and-agentforce-dx/notes.md) — where a registered agent comes from in the first place
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — trust inside the org, versus trust across vendors
- [Release radar: developer tooling & APIs](../../05-release-radar/developer-tooling-and-apis.md) — hosted MCP servers and the dated entry for this topic
