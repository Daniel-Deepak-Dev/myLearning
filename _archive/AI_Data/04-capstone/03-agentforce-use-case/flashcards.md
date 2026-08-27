# Capstone: End-to-End Agentforce Use Case — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What must you do before building anything on this project?
A: Baseline the metric for about two weeks. Without a before-number you have a demo, not a project.

Q: What three things make this project read as architect-level rather than developer-level?
A: A measured outcome rather than a demo, stated unit economics, and an honest failure analysis of what it gets wrong and what you'd fix next.

Q: How should the agent be authored, and why not the old way?
A: In Agent Script. The legacy topic-and-instruction builder stopped creating new agents the week of July 13, 2026.

Q: What does a standard Agentforce action cost?
A: 20 credits, roughly $0.10, against Flex Credits at $500 per 100,000 credits. Voice actions are 30 credits; Testing Center actions are 16.

Q: What is the per-action billing trap?
A: You pay per action, not per conversation. A demo conversation is one action; a real resolution is often five to fifteen, and an orchestrator routing through three subagents multiplies that again.

Q: How do you compute the business case?
A: Actions per resolution × $0.10 = cost per resolution, compared against the fully-loaded cost of a human ticket, typically $5–$15 or more.

Q: How does pay-per-resolution differ from Flex Credits?
A: Pay-per-resolution ($2 per autonomous end-to-end resolution, used by the prepackaged Help Agent) bills on outcomes; escalations and negative-feedback sessions are free and consumption during the interaction is unmetered. It does not stack on top of Flex Credits.

Q: Which deflection benchmarks are worth citing, and how should you use them?
A: Salesforce's own help.salesforce.com handled 4.3 million inquiries and resolved 70%; Oviva handles 300,000+ messages a month, deflecting about half and resolving 40% of operational support without a human. Use them as ceilings, not forecasts — deflection is heavily domain-dependent.

Q: Which API 67.0 rule most often breaks the Apex action in this project?
A: Custom Apex types used as invocable action inputs need a visible no-argument constructor. Check it first when an action stops working.

Q: Why must the action be idempotent?
A: Agents retry after timeouts, and a duplicated write is a real incident rather than a cosmetic bug.

Q: How should you scope the use case?
A: Narrowly enough to measure. "Deflects password-reset cases on the EMEA queue" can be evaluated; "handles support" cannot.

Q: If the use case spans two domains, what should you build and what should you report?
A: Two narrow subagents plus an orchestrator, with each subagent description stating its exclusions. Then report the cost multiple — e.g. "orchestration cost 2.4× per resolution, and here's why it was worth it."
