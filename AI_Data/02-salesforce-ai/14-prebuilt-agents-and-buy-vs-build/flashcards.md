# Prebuilt agents & buy vs build — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What changed in 2026 that makes "buy vs build" an architect's question for agents?
A: Salesforce started shipping finished agents rather than only the tooling to build them — Help Agent, Commerce, IT Service Domain Pack, Contact Center, industry packs. When a support agent deploys in six clicks, "we can build you one" stops being a proposition and grounding quality becomes the differentiator.

Q: What is the Agentforce Help Agent and when did it go GA?
A: A prebuilt self-service support agent with guided setup — Salesforce claims six clicks or less — with web, text and voice channels enabled from a single screen, alongside a reimagined Customer Service Portal that became a single conversation bar with dynamic AI-generated cards. GA July 2026.

Q: Name the three Agentforce Commerce agents and what each does.
A: Shopper Agent — B2C, discovery through checkout and into post-purchase service on the brand's storefront. Buyer Agent — B2B ordering through WhatsApp and SMS. Merchant Agent — back office, managing catalogue and reacting to trends in natural language. GA July 6, 2026.

Q: What are the three commercial models now coexisting for Agentforce?
A: Flex Credits (about $0.10 per standard action, $500 per 100,000 credits) as the default for custom builds; pay-per-resolution at $2 per autonomous end-to-end resolution, introduced with the Help Agent in July 2026; and a negotiated Agentic Enterprise License Agreement, as in the VA's $1.6 billion three-year deal announced July 24, 2026.

Q: Why does pay-per-resolution invert the usual ROI conversation?
A: Because it bills outcomes rather than conversations, and consumption is unmetered during the interaction. Under Flex Credits a chatty agent that resolves nothing costs the customer money; under pay-per-resolution it costs Salesforce money.

Q: What must be settled contractually before quoting pay-per-resolution?
A: The definition of "resolution" — what counts as autonomous and end-to-end, who adjudicates it, and how a partial resolution is treated. These are commercial questions, not technical ones, and they need answering in writing.

Q: What is the single question that decides most buy-vs-build cases?
A: Whether the client's differentiation lives in the conversation or in the data. If it is what the agent knows — right answers, right records, right permissions — buy the agent and spend the budget on grounding. If it is how the conversation goes — unusual approval chains, regulated scripting, bespoke decisioning — build it in Agent Script.

Q: Which buy-vs-build question do people most often forget?
A: Who owns the agent through drift. A custom agent is an ongoing commitment, not a delivered artifact — somebody owns the ADLC outer loop forever. A prebuilt agent moves that cost to Salesforce. Price the maintenance, not just the build.

Q: What do you give up by buying a prebuilt agent?
A: Deep behavioural customization, since setup is deliberately opinionated; control over upgrade timing, which moves to Salesforce's schedule; and some observability, because you are reading behaviour you didn't specify.

Q: What is Salesforce's own Help Agent benchmark, and how should it be used?
A: Agentforce on help.salesforce.com handled 4.3 million inquiries and resolved 70% of them. It is the strongest available reference point for a business case, but it is first-party and self-interested — cite it as Salesforce's number, not as an independent benchmark.

Q: What deflection benchmark does Oviva provide?
A: The European digital health company handles 300,000+ inbound messages per month with Agentforce, deflecting half of all inquiries and resolving 40% of operational support requests without a human.

Q: Why does Agentforce Commerce invert the grounding problem?
A: Because the Shopper Agent sells natively inside ChatGPT with the catalogue synced directly from Business Manager, the customer's session starts outside Salesforce entirely. Instead of giving your agent good context, you publish your context into a model you don't control — so attribute mapping and catalogue hygiene become externally-visible assets that decide whether ChatGPT recommends your product or a competitor's.

Q: Where does checkout happen in Agentforce Commerce, and why note it?
A: On the merchant's own site, not inside the assistant. That preserves order data ownership and the post-purchase relationship — and it is worth noting because competing agentic-commerce designs do not all make that choice.

Q: What is the IT Service Domain Pack?
A: A pack of 50+ prebuilt agents delivered into Slack, Microsoft Teams and the IT Service Desk.

Q: Do prebuilt agents escape platform limits?
A: No. Flex Credits, voice credit rates and Einstein Trust Layer behaviour apply identically whether or not you authored the agent.

Q: What is Missionforce?
A: The public-sector and health vertical agent estate — Agentforce Public Sector and Agentforce Health — behind the VA's $1.6B Agentic Enterprise License Agreement, providing 24/7 virtual contact centre support for patient triage, intake and care coordination.
