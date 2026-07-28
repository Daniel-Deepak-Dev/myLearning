# Capstone: MCP Server for Salesforce — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: Why did this project's premise change in Summer '26?
A: Salesforce hosted MCP servers went GA. Building one from scratch against the REST API now demonstrates less than choosing correctly between three architectures and justifying the choice.

Q: What are the three MCP architecture options for reaching a Salesforce org?
A: Standard hosted (GA — SObject CRUD/SOQL/search, Data 360, Tableau), custom hosted (Salesforce-hosted, you choose the exposed tools), and self-hosted (your own server against the REST API).

Q: What is the single most important property of custom hosted MCP servers?
A: They respect the org's full sharing and security model. A self-built server enforces only what you remembered to implement.

Q: What can a custom hosted MCP server build tools from?
A: Apex @InvocableMethod actions, autolaunched Flows, Apex REST endpoints, @AuraEnabled methods, the Named Query API (parameterized SOQL), Prompt Builder templates as MCP prompts, whole Agentforce agents, and curated API Catalog endpoints.

Q: When is self-hosting still the right answer?
A: When you need tools composing across Salesforce and other systems in one call, custom caching/rate-limiting/transformation logic, the client can't route through Salesforce-hosted infrastructure, or you need something the hosted tool-construction options can't express.

Q: What is the inversion that hosted MCP servers represent?
A: Instead of building an MCP server to reach Salesforce, you configure one and Salesforce enforces sharing and FLS for you.

Q: What is the facade-tool pattern and why use it?
A: Fronting a large API surface with a few intent-based tools — search, payload_examples, execute — instead of exposing hundreds of flat tools. A flat list of 200 tools consumes the context window before the model does any work.

Q: What is the actual deliverable of this capstone project?
A: The decision record — the three options, the choice made, and the criteria behind it. Not the code.

Q: Which demo makes the security argument most persuasively?
A: Connect the same standard server as an admin user and then as a restricted user, and show the agent seeing less. Same server, no code changed.

Q: Why must MCP write tools be idempotent?
A: Agents retry after timeouts. A non-idempotent write can execute twice.

Q: What governance question does GA hosted MCP raise?
A: Who is permitted to create custom hosted MCP servers — they expose org data to external AI clients, so it belongs on a security-review checklist rather than being a developer preference.

Q: How should MCP tool descriptions be written?
A: Like prompts, with explicit exclusions — the same principle as agent action descriptions, because descriptions drive tool selection.
