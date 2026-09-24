---
vault: SF_Service
format: light
level: basic
status: open
gaps: 3
org_checks: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Enhanced Conversation Component

**One line:** The standard Lightning App Builder component that is the rep's chat window — the live transcript plus the message composer — on the **Messaging Session** record page.

**Reach for it when:** reps accept Enhanced Chat or enhanced messaging work and need somewhere to read and reply, or you need to take a button away from them.

> **From my notes.** *"Enhanced Conversation (standard component) in Messaging Session object record page what does it do"* — it is the conversation window itself. Omni-Channel opens a `MessagingSession` record for the rep, and this component on that record's page shows the thread and holds the composer.

## Key points

| The rep can… | Property that hides it — all off by default |
|---|---|
| Transfer the session, or invite another rep (conference) | **Hide transfer action** (plus *Keep tab open after transfer*) · **Hide conference action** |
| Send files — .pdf, .png, .jpeg, .jpg, .bmp, .tiff, .gif, up to 5 MB each | **Hide file attachment action**; *Blur file preview* blurs files the customer sends |
| Send messaging components, or record voice messages | **Hide messaging component action** · **Hide voice message action** |
| Mark the customer inactive, or raise a flag to a supervisor | **Hide customer inactive action** · a flag option exists — exact label 🚩 |
| Use Quick Text, emoji and **End Chat** | none found |

- **It is a real-time transcript** of customer, rep, bot and agent turns, files, messaging components, and events such as transfers, flags and supervisor whispers. The **Voice Call** page uses the same component for live Salesforce Voice transcripts, because a conversation can hold calls as well as sessions.
- **Earlier sessions show too.** One conversation holds many sessions — **End Chat** closes only the current one — so previous sessions appear above it, loading as the rep scrolls, unless **Limit conversation history** is ticked.
- **Enhanced only:** Enhanced Chat and enhanced channels need **Enhanced Conversation**; standard channels used the older **Conversation** component, which does not work on enhanced sessions. A session with a value in its **Conversation** field is enhanced.
- **Setup, as the Trailhead did it:** App Manager → **Service Console** → Pages → New Page → Record Page → **Messaging Session** → clone the Salesforce default → add a **Messaging** tab → drag **Enhanced Conversation** under it → Save → Activate. Org Default is not required — Help's Voice Call page uses **App Default → Service Console** instead.
- **Other properties:** **Hide Translation Preview**, **Enter starts a new text line**, and **Adjust Height** (500–1000 px; the component errors below 320 px wide).
- **The Conversation Toolkit API** (`lightning/conversationToolkitApi`, API 60.0+) lets your own LWC act in the chat: `getConversationLog`, `getEnhancedConversationLog`, `sendTextMessage`, `setAgentInput`, `setMessagingComponent`, `sendMessagingComponent`, `inactivateConversation`, `endConversation`. Its events, such as `lightning__conversationEndUserMessage`, arrive over Lightning Message Service, and both need this component rendered on the open page.

## Gotchas

- **Swap, don't stack.** When a standard channel upgrades — WhatsApp by 30 July 2025, SMS and Facebook Messenger by 14 February 2026 — remove the old Conversation component and add this one in its place.
- **Messages only appear after a refresh?** The Server-Sent Events connection is blocked; allow `https://*.salesforce-scrt.com` on the proxy and turn off any "block malicious downloads" feature (Help 002232058).
- **The page beats the API.** A transfer hidden in Lightning App Builder stays hidden even when the Interaction Service API enables transfers for that session.

## Gaps to close

- [ ] What is the exact property label that hides the flag action, and which release added it?
- [ ] In an org with both standard and enhanced channels, how is each session sent to its own Messaging Session page? Help only says an enhanced session has a Conversation value.
- [ ] What does Help 002239358 say goes missing when **Limit conversation history** is on?

## Confirm in org

- 🚩 With the component removed, can a rep still accept a messaging session in Omni-Channel — and then reply anywhere at all? — delete it from the active page, then accept a chat as the rep.
- 🚩 Does the component work in a standard-navigation app, or only a console app? — assign the page to a standard app and accept a chat there.

## Hands-on

- [ ] **SVC-CONV-01** · 20 min · Build the Trailhead page but activate it as **App Default** for the Service Console only, then accept a chat in the console and in a standard-navigation app. **Proves:** Org Default is not required. **Settles:** whether the component works outside a console app. **Needs:** rep user, an Enhanced Chat channel.
- [ ] **SVC-CONV-02** · 15 min · Remove Enhanced Conversation from the active page, then accept a chat as the rep. **Settles:** whether Omni-Channel still hands over work the rep cannot answer — copy what the tab shows verbatim. **Needs:** rep user.
- [ ] **SVC-CONV-03** · 15 min · End a chat, start a second from the same browser, open it as the rep, then tick **Limit conversation history** and reopen it. **Proves:** earlier sessions show by default, and the property hides them. **Needs:** rep user.
- [ ] **SVC-CONV-04** · 15 min · Tick **Hide file attachment action** and **Hide transfer action**, save, and reopen an active session. **Proves:** the properties strip the toolbar for everyone on that page — note which icons are left. **Needs:** rep user.

## Related

- [Omni-Channel Fundamentals](omni-channel-fundamentals.md) — the push that opens the Messaging Session tab this component lives on
- [Enhanced Chat Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) — sessions versus the conversation, and why a verified customer brings more earlier sessions with them
- [Omni Supervisor](omni-supervisor.md) — the other end of the flag and the whisper
- [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) — the agent's turns a rep reads here after an escalation
- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — the messaging components and auto-responses the toolbar sends
- [Embedded Service Deployments](embedded-service-deployments.md) — the customer's end of the conversation; this note is the rep's end
- [SF_core · 03-lwc · 12 Lightning Message Service](../SF_core/03-lwc-and-slds/12-lightning-message-service.md) — the `lightning__conversation…` events arrive as LMS message channels

## Sources

- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead, *Build an Experience Cloud Site with Knowledge and Enhanced Chat* · read 2026-09-24 · the Messaging Session page steps, activated as Org Default for desktop and phone
- [Add Messaging to the Service Console](https://help.salesforce.com/s/articleView?id=service.livemessage_create_console_app.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"Enhanced channels and Enhanced Chat require the Enhanced Conversation page component, while standard channels require the Conversation component"*; the Conversation field; the property list, all deselected or blank by default; height 500–1000 px, 320 px minimum width — page is JS-rendered, open it to verify
- [Enhance Customer Messaging Experience](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/message-with-a-customer) — Trailhead · read 2026-09-24 · *"A messaging session opens in the enhanced conversation component"*; emoji, Quick Text, messaging components; file types up to 5MB; transfer icon; flag and whisper; Customer Inactive; End Chat
- [Prepare to Upgrade](https://trailhead.salesforce.com/content/learn/modules/upgrading-to-enhanced-messaging/prepare-to-upgrade) — Trailhead · read 2026-09-24 · *"The Conversation page component, used in standard channels, can't be used in enhanced channels"*; assign the page to reps on upgraded channels
- [Benefits of Upgrading to Enhanced Messaging Channels](https://trailhead.salesforce.com/content/learn/modules/upgrading-to-enhanced-messaging/explore-enhanced-messaging) — Trailhead · read 2026-09-24 · quick text, messaging components, files, emoji; upgrade by 30 July 2025 (WhatsApp) and 14 February 2026 (Facebook Messenger, SMS)
- [Customize the Enhanced Conversation Component in the Agent Console](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_prevent_agents_sending_files.htm&language=en_US&release=246&type=5) — Salesforce release notes, Winter '24 · via search 2026-09-24 · hide file attachments
- [Extend Customization of the Enhanced Conversation Component](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_enhanced_conversation_component.htm&language=en_US&release=248&type=5) — Salesforce release notes, Spring '24 · via search 2026-09-24 · title only; content not reachable
- [Control the Enhanced Conversation Component's Height](https://help.salesforce.com/s/articleView?id=release-notes.rn_voice_enhanced_conversation_component.htm&language=en_US&release=250&type=5) — Salesforce release notes, Summer '24 · via search 2026-09-24
- [Create the Voice Call Record Page](https://help.salesforce.com/s/articleView?language=en_US&id=service.voice_setup_create_vc_page.htm&type=5) — Salesforce Help · via search 2026-09-24 · Enhanced Conversation fits medium and large areas only; Assign as App Default → Service Console
- [Configure Call Transcription](https://help.salesforce.com/s/articleView?id=service.voice_setup_transcription.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · add Enhanced Conversation to the Voice Call page to see transcriptions in real time
- [Salesforce Console Developer Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/api_console.pdf) — Salesforce, v68.0 Winter '27, last updated 11 September 2026 · read 2026-09-24 · the eight LWC methods; *"The conversation component must also be rendered for the APIs to work"*; events need *"the Enhanced Conversation Component … visible on the page"* and subscribe through `lightning/messageService`; scroll-based lazy loading past 200 entries; whisper notes and flag events as entry types — a Winter '27 build, so method availability at API 67.0 is not re-checked
- [Conversation Toolkit API | Lightning Component Reference](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-conversation-toolkit-api.html) — Salesforce Developers · via search 2026-09-24 · `lightning/conversationToolkitApi` needs API 60.0 or later; the `lightning-conversation-toolkit-api` markup form is deprecated
- [Control Messaging Actions | Bring Your Own Channel for CCaaS](https://developer.salesforce.com/docs/service/messaging-byoc-ccaas/guide/control-messaging-actions.html) — Salesforce Developers · via search 2026-09-24 · App Builder settings take precedence over dynamically controlled actions
- [Agent Unable to See Real-Time Messages / Transcription in Conversation Component](https://help.salesforce.com/s/articleView?id=002232058&language=en_US&type=1) — Salesforce Help 002232058 · via search 2026-09-24 · SSE blocked by firewall or proxy; allow `https://*.salesforce-scrt.com`
- [Salesforce Messages Not Displayed When Using "Limit …"](https://help.salesforce.com/s/articleView?id=002239358&language=en_US&type=1) — Salesforce Help 002239358 · via search 2026-09-24 · title only; content not reachable
- [Messaging Object Model](https://developer.salesforce.com/docs/service/messaging-object-model/guide/messaging-object-model.html) — Salesforce Developers · via search 2026-09-24 · a conversation is one or more messaging sessions or voice calls

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
