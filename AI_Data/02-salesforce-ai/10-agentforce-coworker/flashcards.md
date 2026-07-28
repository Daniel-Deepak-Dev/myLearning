# Agentforce Coworker — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is Agentforce Coworker?
A: An AI teammate that lives in the search bar — Salesforce's, Slack's, and eventually Teams, ChatGPT, Claude and a desktop app. It searches CRM, Data 360 objects and Slack, synthesizes an answer, and routes to specialized agents to act. Announced May 21, 2026; Beta, with no announced GA date as of 2026-07-28.

Q: What makes Coworker architecturally different from every other topic in the Salesforce AI track?
A: Nothing is authored. No Agent Script, no topics, no actions, no subagent descriptions — you turn it on and it inherits the org's setup, sharing rules and permissions. The design question moves from "what should this agent do" to "what is it allowed to see".

Q: Coworker vs Employee Agent vs Service Agent?
A: Service Agent is customer-facing and anonymous. Employee Agent is internal, authenticated, and purpose-built with its own subagents and actions. Coworker is zero-config and org-wide — not authored at all — and routes to specialized agents rather than being one.

Q: What is the setup path for Agentforce Coworker?
A: Setup → Quick Find "Agentforce Coworker" → (optional) Set Up Data Space → Get Started with Agentforce Coworker → Turn On → Turn on End User Experience (tick the Global Search Bar disclaimer consent) → Manage Users → select users → Assign.

Q: What does an admin need to set up Coworker, and which editions support it?
A: Salesforce Admin Role plus the Agentforce Coworker Admin permission set. Available in Enterprise, Unlimited and Agentforce 1 Editions. Not supported on Government Cloud Plus.

Q: Which permission set group grants users access to Coworker, and what's the nuance?
A: `Access_Ai_Search`. The nuance is that Salesforce recommends assigning access through the Manage Users section of Coworker Setup instead of assigning the group directly.

Q: Which data sources work in Coworker Beta, and which don't?
A: Beta supports Salesforce CRM, Data 360 objects and Slack — three sources. Google Drive, SharePoint and Jira are pilot-only and require an account executive. Marketing material citing "270+ data sources" does not describe what Beta can actually search.

Q: What's the difference between how Slack and Google Drive reach Coworker?
A: Slack is federated — queried live, never ingested into Data 360, requiring Slack Authentication configured in Salesforce. Google Drive and SharePoint are ingested and indexed on a 1 hr incremental crawl, so their answers can be stale.

Q: When does Coworker consume no credits at all?
A: Under seat-based pricing — Agentforce 1 Edition, or Agentforce for Sales, Service and Industries — searching Salesforce CRM or Slack consumes zero Flex Credits and zero Data Services Credits.

Q: Flex Credits vs Data Services Credits in Coworker?
A: Flex Credits cover Standard, Basic and Advanced prompts plus Data 360 unstructured processing, intelligent processing and querying. Data Services Credits cover data queries, unstructured data processed and intelligent processing. Both models can run side by side in one org, billed per user's license.

Q: Which users are always billed usage-based, regardless of the org's model?
A: Guest, unauthenticated and portal users.

Q: What are Coworker's headline rate limits?
A: Slack: 180 queries per minute sustained per user JWT token, up to 1000 burst. Search Agent: 100 RPM.

Q: What are the ingestion caps for Google Drive and SharePoint?
A: Google Drive: 5,000 files per shared drive, 1 hr incremental. SharePoint: 10–15 GB and 5,000 files per site, 1 hr incremental. Both: PDFs up to 100 MB, other files up to 4 MB. SharePoint can't ingest files with security labels or tags, empty Excel files, or OneNote.

Q: What unexpected thing happens when you turn on Agentforce Coworker?
A: It automatically enables Einstein — a much bigger switch than the button implies.

Q: Why is enabling Coworker effectively a sharing-model audit?
A: Because it authors nothing and inherits everything. Whatever the sharing model and field-level security actually permit becomes instantly visible to every licensed user across the whole org, through a conversational interface that's easy to probe.

Q: What's the financial risk of prototyping Coworker during Beta?
A: Consumption of entitlements arising from use of Non-GA services gives rise to no refund or credit rights under the Beta Services Terms — the spend is unrecoverable.
