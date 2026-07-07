# Agentforce Anatomy — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Agentforce?
A: Salesforce's platform for building autonomous AI agents that plan and execute tasks across CRM using topics, actions, and the Atlas Reasoning Engine.

Q: What does the Atlas Reasoning Engine do?
A: Interprets a request, classifies it into a topic, plans steps, and chooses which actions to run.

Q: What is a topic (in Agentforce)?
A: A job category inside an agent that groups related actions and instructions, scoping what the agent is allowed to do for that kind of request.

Q: What can be an agent action?
A: An autolaunched Flow, an invocable Apex method, a prompt template, or an external API call.

Q: What are instructions (guardrails)?
A: Natural-language rules attached to topics/agents that constrain behavior — what to always do, never do, and how to respond.
