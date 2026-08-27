# Agentforce Anatomy — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Agentforce?
A: Salesforce's platform for building autonomous AI agents that plan and execute tasks across CRM, authored in Agent Script and reasoned over by the Atlas Reasoning Engine.

Q: What replaced topics-and-instructions as the Agentforce authoring model?
A: Agent Script, in the new Agentforce Builder. Since the week of July 13, 2026 the *New Agent* button no longer opens the legacy builder.

Q: Can you still use legacy topic-based agents?
A: Yes — existing legacy agents can be edited, activated, versioned and managed. What was removed is the ability to *create* a new agent that way.

Q: What is Agent Script?
A: A human-readable expression language that compiles to portable JSON, blending deterministic rules (conditionals, hand-offs, precise tool use) with agentic LLM reasoning. Open source under Apache 2.0.

Q: What is Hybrid Reasoning?
A: The Agent Script design point — you dial how much of the agent is structured business logic versus how much is left to the model.

Q: Why does compiling to JSON matter architecturally?
A: Agent definitions behave like source code: versioned, diffed, reviewed in a PR, linted in a plain CI job with no org connection, and deployed through a pipeline.

Q: What does the Atlas Reasoning Engine do?
A: Interprets a request, plans steps, chooses which actions to run, and routes to subagents.

Q: How does Atlas Reasoning Engine 3.0 decide which subagent to route to?
A: It reads each subagent's description, rather than following a fixed decision tree. The description is therefore executable configuration — a vague one causes intermittent mis-routing that looks like a model failure but is a specification failure.

Q: What can be an agent action?
A: An autolaunched Flow, an invocable Apex method, a prompt template, an Apex REST endpoint, an @AuraEnabled method, or an external API call.

Q: Service Agent vs Employee Agent?
A: Service Agent is customer-facing and anonymous (no login) — good for public apps. Employee Agent is internal and authenticated, obtaining OAuth tokens.

Q: What is a triggered agent?
A: An agent that fires on a defined event — a deal stage change, a Data 360 customer signal — instead of waiting for a human utterance.

Q: What happens when you upgrade a legacy agent?
A: One click converts all subagents, actions, system messages, data and connections into Agent Script, then optionally optimizes the result for reliability.

Q: Why should agent actions return typed structures rather than prose?
A: A Custom Lightning Type can then attach a purpose-built UI to the output — defined once, it renders idiomatically on every surface (LWC on desktop, native UI on mobile).

Q: What is the Agentforce cost unit, and what's the trap?
A: You are billed per *action* (~20 credits, ~$0.10), not per conversation. A real resolution is often five to fifteen actions, and an orchestrator routing through three subagents multiplies that again.

Q: Which Apex change at API 67.0 breaks existing Agentforce actions?
A: Custom Apex types used as invocable action inputs must expose a visible no-argument constructor — public, or global for packaged classes.

Q: Agentforce Mobile SDK "262.1.2" sounds like a patch. Why is it not?
A: The marketing name and the git tag are different version lines. 262.1.0 → 262.1.2 is patch-shaped; the tag went 17.31.6 → 18.26.8, a major, because the SDK moved to Swift 6 strict concurrency. Read the tag, not the release title.

Q: Which five Gen UI components did Agentforce Mobile SDK 262.1.2 add, and why do they matter?
A: `Table`, `Schedule`, `DataGroup`, `QueryOption` and `VerticalCard`. They are exactly the action returns that previously got flattened into prose — more reason to design agent action outputs as typed structures rather than sentences.

Q: The Agentforce mobile stack has three separately versioned artifacts. What is the trap in late July 2026?
A: The SDK (tag `18.26.8`) declares a dependency on `AgentforceService` 6.10.0 while `AgentforceMobileService-iOS` is already at 6.11.2. The SDK's floor lags the service's head — the newest service build is not the tested one.
