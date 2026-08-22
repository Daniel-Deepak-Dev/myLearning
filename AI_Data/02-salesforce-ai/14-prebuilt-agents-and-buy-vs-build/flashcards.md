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

Q: What is Missionforce National Security, as distinct from "Agentforce 360"?
A: The defense and intelligence vertical estate — the thing a government customer actually buys. "Agentforce 360" is the portfolio name for the agents, data capabilities and apps inside it, not a SKU.

Q: In the U.S. Army HRC deployment, what stays with the human?
A: The decision. The agent answers routine inquiries, summarizes case histories and surfaces policy and career information from approved Army sources; anything touching benefits or other sensitive determinations routes to an HRC specialist who retains decision-making authority.

Q: Why is "retrieve and summarize, human decides" the design worth copying from Army HRC?
A: It gets an autonomous agent past a risk review by scoping what it is allowed to conclude, rather than by making it more accurate. Accuracy is unbounded work; scope is a design decision you can assert and test.

Q: The Army HRC release cites 55M agent conversations a month and $6M annual savings. How should you cite them?
A: As projections at full scale, not results. 55M across 9.2M people is about six conversations per person per month — plausible as a ceiling, not an observed rate. The deployment was announced as in progress.

Q: What is Agentforce Operations, and when did it go GA?
A: The back-office prebuilt agent family — supply chain, procurement, finance and IT — GA 2026-04-29. Its agents do process coordination, data verification, compliance clearance and approvals, rather than converse with a customer.

Q: What is a "digital blueprint"?
A: Agentforce Operations' authoring artifact — an unstructured document or diagram converted into an executable workflow, then updated in plain language rather than redrawn.

Q: Why is the digital blueprint worth noticing next to Agent Script?
A: They are opposite trades shipped in the same year. Agent Script made authoring explicit and version-controlled; a blueprint is generated and prose-edited. One governance model does not cover both.

Q: Agentforce Operations claims blueprints "trigger actions with Salesforce Flows". What is the catch?
A: That ecosystem integration was Beta from May 2026, not GA at the 2026-04-29 launch. At GA it was a promise, not a shipped surface.

Q: How should you quote Agentforce Operations' "50-70% cycle time" and "80% less manual data entry"?
A: As vendor claims with no published methodology — and note that no first-party page was reachable to verify them. Pricing and licensing are also unestablished, so the buy-vs-build comparison cannot be closed on cost.

Q: What single expression gates every Service Cloud ITSM CMDB Connect API?
A: `orgHasCMDBEnabled = orgHasCMDBPermission && OrgPreferences.CMDBEnabled`, where the first term is the org permission `ITSrvcsCnfgMgmnt`. Until both hold, every CMDB API returns `403 FUNCTIONALITY_NOT_ENABLED`.

Q: Why is Layer 0 of CMDB enablement different in kind from the layers above it?
A: `ITSrvcsCnfgMgmnt` comes from the org's edition, licence or template and **no API can grant it**. Every other layer is something you can turn on; this one is a purchasing decision made before the org existed. If it is absent, setup stops — nothing downstream helps.

Q: A user gets `403 FUNCTIONALITY_NOT_ENABLED` from a CMDB read. What are the two possible causes, and how do you tell them apart?
A: Either the org feature is off, or the running user holds no CMDB permission set. Disambiguate on the **feature `status == ENABLED`** — never on a CMDB data read such as `bundleListView`, because that read enforces both gates and returns the same code for each.

Q: Name the four CMDB permission sets and the one that bundle management specifically requires.
A: `ItSrvcCnfgItmReadPermissionSet` (Reader), `ItSrvcCnfgItmOwnerPermissionSet` (Owner), `ItSrvcCnfgItmTypReadPermissionSet` (Type Reader), `ItSrvcCnfgItmTypManagerPermissionSet` (Type Manager) — each with its own backing PSL. **Type Manager** is the one that clears `403` on bundle operations; the other three do not.

Q: What is the cheapest reliable probe for whether an org carries the CMDB SKU?
A: Query for the permission-set licence `ItSrvcCnfgItmReadPsl`. It is provisioned by the same licence that grants `ITSrvcsCnfgMgmnt`, and unlike an org-permission read it works on every org type including scratch and sandbox.

Q: Why does `CMDBEnabled` not appear as a toggle you can set?
A: It is not directly settable. It flips as a side effect of enabling the feature `service-cloud-itsm-cmdb-integration` (Layer 2). Looking for a preference to flip is the wrong search.

Q: `PATCH /services/data/v67.0/setup/org/preferences/ITSMTeamsEnabled` returns `401 INSUFFICIENT_ACCESS`. What is wrong?
A: The route, not the credentials. `ITSMTeamsEnabled` is a **Salesforce Go page toggle**: its UDD definition (`ServiceItsmTeams.settings.xml`) declares `orgAccess="always"` with **no `editAccess` attribute**, so it is readable by design and writable by nothing. Enable the feature instead — `POST /connect/setup/discovery/feature/service-cloud-itsm-teams-integration/enable` — and the preference flips as a side effect. Same pattern as `CMDBEnabled`.

Q: Name the four tracks of the ITSM setup program and what owns each track's prerequisites.
A: Incident Management (SLA & Milestones), Agentforce for ITSM (Studio, Fulfiller Agent, Employee Agent), CMDB, and Microsoft Teams (IT Desk, IT Service, Swarming). **Prerequisites are enforced inside each sub-orchestrator, never at the top level** — deliberately, so the track menu still runs on a bare org where no gate is satisfied yet.

Q: Teams extension registration fails with `403 FUNCTIONALITY_NOT_ENABLED [MsTeamsAppApiFamily]`. What unlocks it?
A: Nothing self-service that has been found. It is not a Go feature — seven candidate API names all return `400 NOT_FOUND` — and none of the org's 112 permission-set licences grant it, including `TeamsForEmployeePsl` and `TeamsForITSrvcsPsl`. Treat it as an org/edition-level gate and stop retrying enablement guesses; it is also the true cause of the "Unable to fetch tenant ID" error.

Q: A Teams portal user logs in and sees "you don't have access to the Microsoft account in Salesforce." Why?
A: The Apex registration handler `MsTeamsItsmSSOHandler` resolves the Microsoft user with `SELECT Id FROM User WHERE Username = :data.email` — the Microsoft UPN must equal **`User.Username`**, not `User.Email` and not `FederationIdentifier`. `canCreateUser` is false, so there is no JIT provisioning, and both 0 and >1 matches deny login. One handler serves both the IT Desk and IT Service apps.

Q: What does provisioning a Unified Employee License (UEL) user actually involve, and which permission sets go on it?
A: Four linked records — `User` on the Unified Employee profile, a Person `Account` (auto-generating its `Contact`, read back as `PersonContactId`), and an `Employee2` linked by `UserId`/`ContactId`. **Exactly one permission set**: `EmployeeHubEmployeeUser`. It is managed, uneditable and does not grant `ApiEnabled`, so add an unmanaged set for that — and never `ChatterInternalUser`, which the licence rejects. Fulfiller and case-agent sets belong to Service Cloud fulfillers, not Employee Hub requesters.
