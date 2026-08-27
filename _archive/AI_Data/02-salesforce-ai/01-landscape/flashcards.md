# Salesforce AI Landscape — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Einstein (the brand)?
A: Umbrella brand for Salesforce's AI features, spanning older predictive tools and current generative capabilities. Note: not everything called Einstein is generative.

Q: What happened to Einstein Copilot?
A: The conversational CRM assistant was folded into Agentforce. It is a historical name — a source using it as current product predates mid-2025.

Q: The Salesforce AI arc, in four steps?
A: Einstein (predict) → Einstein GPT (draft) → Einstein Copilot (assist) → Agentforce (act). Each step moved work further from the human.

Q: What is Agentforce 360?
A: The 2026 platform umbrella covering agents, Data 360, Tableau and Slack. It is a portfolio name, not a version number of the agent product.

Q: What is Headless 360?
A: The organizing idea of Summer '26 — every major Salesforce capability is reachable as an API, an MCP tool, or a CLI command, by a human, an app, or an autonomous agent.

Q: Which models can the Atlas Reasoning Engine use?
A: Anthropic (Claude on Amazon Bedrock), OpenAI, and Google Gemini — plus your own via Model Builder / BYOM. Since Agent Script you can pin the model per agent instead of using one org-wide setting.

Q: An agent confidently states a wrong fact about a customer. Where do you look first?
A: Grounding and data freshness — not the model. Check whether it was grounded at all, then whether the data was stale (Accelerated Data Ingest addresses the second).

Q: What version is the Atlas Reasoning Engine, and what changed?
A: 3.0 — it routes to subagents by reading their descriptions rather than following a fixed decision tree, which makes the description field executable configuration.

Q: What happened to 16 Salesforce certifications on July 24, 2026?
A: They were renamed with *Agentforce* replacing the old cloud branding (e.g. Sales Cloud Consultant → Agentforce Sales Consultant). Cosmetic only: no content change, no exam-code change, no retake.
