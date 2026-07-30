# MuleSoft Agent Fabric — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is MuleSoft Agent Fabric?
A: A unified control plane — a single pane of glass to register, manage, govern and observe every agent and MCP endpoint in an enterprise, including agents built outside Agentforce. Launched September 2025. It is a MuleSoft product, licensed separately from Agentforce.

Q: State the distinction between Agentforce Multi-Agent Orchestration and Agent Fabric in one sentence.
A: Agentforce orchestration coordinates agents inside one org; Agent Fabric coordinates agents across vendors.

Q: What are the four pillars of Agent Fabric and the component behind each?
A: Discovery → Agent Registry. Governance → Omni Gateway plus Governance Strategies. Orchestration → Agent Broker plus Agent Networks. Observation → Agent Visualizer plus monitoring.

Q: What can be registered in the Agent Registry?
A: Every agentic asset — custom-built agents, agents embedded in SaaS applications, MCP servers fronting legacy systems, and A2A endpoints for inter-agent collaboration.

Q: What does it mean that the Agent Registry is federated?
A: Anyone can run a registry and registries can reference each other, so the catalog grows without a central authority — closer in shape to DNS than to a single corporate directory. It is what makes cross-company agent discovery plausible.

Q: What are the five ways an asset gets into the Agent Registry?
A: Manual registration in the Portfolio/Exchange; automated scanners; MCP Bridge (converts an existing API into an MCP server by configuration); MCP Connector (build a custom MCP server); A2A Connector (make an application A2A-compliant).

Q: What are Agent Scanners, which platforms do they cover, and when did they go GA?
A: They continuously discover and register agents across other platforms — Agentforce, Amazon Bedrock, Google Vertex AI and Microsoft Copilot Studio. GA January 2026. They are the feature that finds shadow agents.

Q: What is an Agent Network and how is it defined?
A: A multi-agent composition — which agents, brokers, LLMs and MCP servers participate — declared in YAML and deployed to CloudHub 2.0. The topology becomes a versionable artifact rather than a diagram.

Q: What happened to MuleSoft Flex Gateway?
A: It was renamed Omni Gateway. Same runtime, carried forward and expanded to govern AI agents, MCP and A2A traffic alongside APIs. The change is non-breaking and cosmetic to UI and docs (Omni Gateway 1.13.0), so CI/CD pipelines are unaffected. Both names still circulate.

Q: What is guided determinism, and when was it announced?
A: Announced April 15, 2026 as part of the Agent Fabric expansion: pairing autonomous goal-based LLM reasoning with codified handoff rules and human checkpoints. It is the same design point as Agent Script's Hybrid Reasoning, applied at the network layer instead of inside a single agent.

Q: What else shipped in the April 15, 2026 Agent Fabric expansion?
A: Automated cross-platform agent discovery, a drag-and-drop workflow authoring canvas, guided determinism, and a centralised LLM governance layer covering cost, compliance and model routing across providers.

Q: Why is "Agent Script" an ambiguous term?
A: It names two different things — the Agentforce authoring language that compiles to JSON (Apache 2.0), and "Agent Script for Agent Broker", the guided-determinism feature in Agent Fabric. Same words, different products and different layers.

Q: Registering an agent in the Registry — does that govern it?
A: No. Registration makes it discoverable. Policy only applies to traffic that actually routes through Omni Gateway. An agent that is registered but reached directly is catalogued and ungoverned, which is worse than either alone because it looks managed.

Q: Does Agent Fabric change what a Salesforce agent is allowed to see?
A: No. Gateway policy governs agent-to-agent and agent-to-tool traffic. What a Salesforce agent may see is still decided by the org's sharing rules and field-level security.

Q: What is the status of Agent Broker, and why is that answer unsatisfying?
A: Genuinely unclear. Launch-era coverage puts Agent Broker GA in October 2025, while coverage of the April 2026 expansion describes a Beta starting April 2026. The likely reconciliation is that the base Broker is GA and the new guided-determinism capability entered Beta — but that is inference. Verify before quoting.

Q: What does Agent Fabric cost?
A: Unknown. No public pricing or licensing detail was found in any source consulted, and it is licensed through MuleSoft rather than as part of an Agentforce SKU. Confirm with an account executive before scoping client work.

Q: What is the "agent sprawl" argument for Agent Fabric?
A: That what happened to APIs around 2015 is now happening to agents — shadow agents get built, nobody can find them to reuse, and each negotiates its own security. Agent Fabric applies the API-management playbook to agents, which is the playbook MuleSoft already owns.
