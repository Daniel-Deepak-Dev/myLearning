# Multi-Agent Orchestration — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Multi-Agent Orchestration?
A: An orchestrator agent connects to other specialized agents in the org and presents a single point of contact, so a user handles a cross-domain task without switching sessions, with context shared across channels.

Q: How does Atlas Reasoning Engine 3.0 choose a subagent?
A: It reads each subagent's description, rather than following a fixed decision tree. The description is therefore executable configuration.

Q: An orchestrated agent keeps routing to the wrong subagent. Where do you start debugging?
A: The subagent descriptions. Vague or overlapping descriptions cause intermittent mis-routing that looks like a model failure but is a specification failure.

Q: What single element makes a subagent description reliable?
A: An explicit exclusion clause — "does NOT handle billing plan changes". Without it, two plausibly-overlapping descriptions produce non-deterministic routing.

Q: How do you connect a subagent in Agentforce Builder?
A: Open a draft agent as the orchestrator, then in the Explorer panel choose + → Connect Agent as Subagent, and give it a description. With Agent Router, add it under *Actions Available for Reasoning* and reference it with @.

Q: Why is the "many narrow agents" pattern preferred over one omniscient agent?
A: Smaller surface to test, independent ownership, and failures stay contained — the same reasoning as microservices over a monolith.

Q: What is the cost consequence of orchestration depth?
A: You pay per action, so an orchestrator routing through three subagents costs roughly three times a direct hit. Depth is a budget decision.

Q: What is the A2A protocol, and how does it differ from Multi-Agent Orchestration?
A: A2A is an open protocol for agents built on different platforms to discover and call each other. MAO orchestrates agents within the Salesforce estate; A2A crosses platforms.

Q: What is the Multi-Agent Interoperability section of the Agentforce Specialist exam?
A: MCP, the A2A protocol and the Agent API, weighted at roughly 5%.

Q: What is the unresolved status question around Multi-Agent Orchestration?
A: Secondary sources date GA to June 15, 2026, but Salesforce Help still labels the in-builder *Connect Agent as Subagent* step (Beta). Product page and setup docs disagree — verify in your own org before quoting a status.

Q: When should you NOT split into subagents?
A: When two agents would always run together. Decompose on genuine domain boundaries, not for tidiness.

Q: What risk comes with shared context across an orchestrated session?
A: Context flows to subagents, so a subagent may see data beyond its domain. Be deliberate about visibility where subagents have different data sensitivities.
