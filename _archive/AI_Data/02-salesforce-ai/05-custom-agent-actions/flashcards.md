# Custom Agent Actions — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What are the two classic platform building blocks for custom agent actions?
A: Invocable Apex methods (@InvocableMethod) and autolaunched Flows.

Q: Which two action types were added in Spring '26, and why do they matter?
A: Apex REST endpoints and @AuraEnabled controller methods. Logic already written for LWC and integrations becomes agent-callable without a rewrite — inventory what exists before building new invocables.

Q: Why do an action's input/output descriptions matter so much?
A: They ARE the agent's understanding of the tool — the reasoning engine reads them, never your Apex, to decide whether the action is relevant and what to pass. Write them like prompts.

Q: What makes an action description strong rather than weak?
A: Negative boundaries as well as positive ones — "Issues a refund on a Delivered order. Do not use for exchanges." The exclusion is what prevents mis-selection between two similar actions.

Q: Which API 67.0 change breaks existing Agentforce Apex actions?
A: Custom Apex types used as invocable action inputs must expose a visible no-argument constructor — public, or global for packaged classes. Check this first when an action fails after an API bump.

Q: What is the default access mode for Apex SOQL and DML at API 67.0?
A: User mode — the running user's object permissions, FLS and sharing rules are enforced. Elevated access is opt-in via WITH SYSTEM_MODE.

Q: What happens to a class compiled at 67.0 with no sharing keyword?
A: It defaults to `with sharing`. Previously it inherited the calling class's sharing context, which meant sharing went unenforced when that class was the entry point.

Q: Why is WITH USER_MODE better than the retired WITH SECURITY_ENFORCED?
A: It handles polymorphic fields (Owner, Task.whatId), checks the WHERE clause rather than only the SELECT list, and reports every FLS violation instead of just the first.

Q: What is the asymmetric migration risk with the 67.0 security defaults?
A: They apply only to classes compiled at 67.0, so nothing breaks on upgrade day — but the moment someone bumps a class's API version for an unrelated reason, its data access semantics change underneath them.

Q: What changed for Apex triggers at 67.0?
A: They always run in system mode and can no longer declare sharing or access modes — so a trigger is the wrong place for security-sensitive logic. Push it into a handler class.

Q: Why return typed structures from an action rather than prose?
A: A Custom Lightning Type can attach a purpose-built UI to typed output — defined once, it renders on desktop LWC and natively in the mobile app. Prose can't be rendered specially anywhere.

Q: Why does idempotency matter more for agent actions than for UI code?
A: An agent may retry after a timeout. A non-idempotent "issue refund" action can issue two.

Q: How does an @InvocableMethod reach an external AI client like Claude?
A: Exposed as a tool on a custom hosted MCP server — which respects the org's full sharing and security model, so the same method serves an agent and an external client under the same enforcement.
