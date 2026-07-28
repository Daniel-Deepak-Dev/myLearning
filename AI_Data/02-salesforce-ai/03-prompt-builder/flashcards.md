# Prompt Builder — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Prompt Builder?
A: Declarative tool for creating reusable prompt templates that merge CRM record data and grounding sources before calling an LLM.

Q: What is a prompt template?
A: A reusable, versioned prompt definition with merge fields, resolved with live data at runtime. It is deployable metadata, not a string buried in Apex.

Q: What is dynamic grounding?
A: Injecting live CRM or Data 360 data into a prompt at runtime so the model answers from your data instead of general knowledge.

Q: Which prompt template type do you use for an agent action, and why?
A: Flex — it takes arbitrary declared inputs, which is what allows it to be invoked as an agent action. The other types are bound to a fixed context.

Q: Name the five grounding sources available to a prompt template.
A: Record merge fields, Flow output, Apex output, a Data 360 retriever, and an Agentforce Data Library.

Q: In what order should you prefer grounding sources, and why?
A: Record merge fields → Flow → Apex → retriever. Cheapest first: every extra token is paid on every invocation, and Agentforce bills per action.

Q: Does Prompt Builder call the LLM directly?
A: No. Every invocation routes through the Einstein Trust Layer — masking and injection checks on the way out, unmasking, toxicity scoring and audit logging on the way back.

Q: How can a prompt template be consumed outside Salesforce?
A: Exposed as an MCP prompt through a custom hosted MCP server, so an external client like Claude invokes your governed, grounded template instead of improvising wording. The Trust Layer still applies.

Q: Which record should you test a prompt template with?
A: The one that will break it — empty fields, missing related records, unusual picklist values. Merge fields resolve to nothing and the model invents a replacement.

Q: Two paths using the "same" template produce noticeably different output. What do you check?
A: Which model each actually used. The model is set per template and can differ from the org default and from the model pinned in an agent's Agent Script.

Q: How did API 67.0 change Apex-based grounding?
A: Apex now runs in user mode by default, so a grounding class enforces the running user's FLS and sharing — it may legitimately return less data than before.
