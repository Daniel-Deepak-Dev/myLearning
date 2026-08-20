# Agentforce Voice & Contact Center — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: Distinguish Agentforce Voice from Agentforce Contact Center.
A: Voice is the capability — an Agentforce Service Agent handling autonomous inbound and outbound calls over PSTN or SIP trunking, replacing the IVR. Contact Center is the product — Salesforce's native CCaaS unifying voice, digital channels, CRM data and AI agents in one system, GA February 23, 2026. You can run Voice against a partner's telephony without buying Contact Center.

Q: When did Agentforce Contact Center go GA and where was it launched?
A: February 23, 2026, launched at Enterprise Connect 2026.

Q: What is the GA date for Agentforce Voice, and why is that question awkward?
A: Most sources say October 21, 2025, in the Winter '26 cycle, with native CCaaS partners. Others describe it moving from pilot to GA in Spring '26 with Atlas-powered autonomous reasoning. The likely reconciliation is progressive GA — channel first, fully reasoning agent later — but that is inference, so verify before committing to a date.

Q: Which telephony providers does Agentforce Voice work with, and which one is different?
A: Amazon Connect, Five9, Genesys, NiCE and Vonage. Amazon Connect is native — Salesforce manages provisioning — while the other four connect through Partner Telephony.

Q: What does a voice action cost compared with a standard action?
A: 30 Flex Credits (about $0.15) versus 20 (about $0.10) — 50% more per action, before accounting for voice conversations having more turns. Credits are $500 per 100,000.

Q: What is the alternative voice billing model, and why does it matter?
A: A per-minute model at roughly 60 Flex Credits per minute — about $0.30 in production and $0.24 in sandbox. It matters because a long call with few actions is cheap per-action and expensive per-minute, so the two models are not interchangeable in an ROI estimate. These are secondary-source figures; verify against the contract.

Q: What are the three prerequisites for escalating an Agentforce Voice call to a human?
A: Partner Telephony Setup configured, Service Cloud Voice enabled, and Contact Center setup completed. All three sit outside Agentforce itself, which is why a voice agent that answers calls correctly can still fail its first escalation.

Q: What is the geographic constraint on Agentforce Voice?
A: US and Canada only as of early 2026, with global languages still in Beta as of July 2026. For a Europe-based practice this is the first thing to check — it is the most likely reason a voice project doesn't proceed.

Q: What is barge-in and why does it change how you write an agent?
A: Barge-in is the customer interrupting the agent mid-sentence, which Agentforce Voice supports. It means an agent that plans a long answer will rarely finish it, so voice agents must be written for short turns.

Q: Why is latency a design constraint rather than an implementation detail in voice?
A: Because every extra grounding hop and every extra action is dead air on a live phone call. A retrieval budget that feels fine in a chat window can be unusable on the phone, and no amount of prompt tuning fixes it.

Q: What happens to context when a voice call escalates to a human?
A: Context is transferred and the call is transcribed live into Salesforce Voice, so the human rep can take over mid-call with the conversation already in front of them. The full interaction remains auditable through Data 360.

Q: What did SIP trunking change, and when did it arrive?
A: SIP routing went GA in Summer '26. Instead of pointing a dedicated carrier phone number at the agent, you point a SIP trunk that rides your existing internet connection — Salesforce positions it as the cheaper and more flexible option.

Q: What is Voice for Digital Channels?
A: The same voice capability extended beyond telephony to web chat, mobile apps, WhatsApp and messaging. GA in Q2 2026.

Q: Why should you know that Salesforce is both a partner and a competitor to Genesys, Five9 and NiCE?
A: They are partners at the Agentforce Voice layer — listed CCaaS integrations — and competitors at the Agentforce Contact Center layer, since Contact Center is Salesforce's own native CCaaS. Clients running those platforms will notice, so don't be caught out by the reaction.

Q: Agentforce Voice or Salesforce Voice — which is which?
A: Agentforce Voice is the AI agent handling the call. Salesforce Voice is the Service Cloud telephony surface where the live transcript lands and where a human takes over.

Q: Who was the first customer live on Agentforce Contact Center?
A: Compass Working Capital, deployed by TTEC Digital, announced July 23, 2026.

Q: What happens if an Agent Script `modality voice:` block mixes v1 and v2 keys?
A: The compile fails — "Invalid modality voice configuration. Both Voice schema versions were detected, use only one at a time." Adding one nested `outbound:` block to a working v1 script breaks the whole compile; it is not a merge.

Q: How does Agent Script voice v2 express per-language settings?
A: `language_settings:` maps a BCP 47 tag to its own `inbound:` / `outbound:` pair, with the agent-level block as the default. Any string is accepted as a key (`allowTypelessEntries: true`), so a mistyped locale parses cleanly and fails later in the linter.

Q: What are the two values of `session_language_switching` in Agent Script voice v2?
A: `Monolingual` (the default — one language per session) and `Multilingual` (any language on any turn).

Q: Where does Agent Script voice v2 output land in the compiled config?
A: Under `voice2_config`, with the shared `additional_configs` moved into it. Anything reading the compiled `voice` config by its v1 shape sees an empty object.
