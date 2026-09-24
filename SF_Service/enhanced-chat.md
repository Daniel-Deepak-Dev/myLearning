---
vault: SF_Service
format: light
level: basic
status: open
gaps: 2
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [retirement]
---
# Enhanced Chat (formerly Messaging for In-App and Web)

**One line:** Service Cloud's chat channel for your website and mobile app. Conversations are asynchronous and persist, and Omni-Channel routes them to a rep, an enhanced bot or an Agentforce agent.

**Reach for it when:** a customer has to chat from your site or app. Legacy Chat is retired, so this is the only native chat channel left.

## Key points

- **MIAW and Enhanced Chat are one product.** *Messaging for In-App and Web* became **Enhanced Chat** in June 2025; Help still uses both names, and many page ids still start `miaw_`.
- **Two surfaces:** **Enhanced Web Chat** on a website, **Enhanced In-App Chat** in an iOS or Android app → [Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md).
- **Legacy Chat retired on 14 February 2026** — LiveAgent, Salesforce Chat, Embedded Chat and Service Chat (Help 001790618). Orgs still on it run as-is, with no warranty and no SLA.
- **It runs on the Messaging platform**, alongside Voice and the enhanced WhatsApp, SMS, Facebook Messenger, Apple Messages for Business and LINE channels. The objects and the Omni-Channel routing are shared with them.
- **Before migrating, run the Chat Transition Readiness Report** (Summer '25). It lists active legacy deployments, configurations and customisations, so you can decide what to replace, retire or adapt.
- **Reps need the Enhanced Chat User permission set licence**, plus a permission set you create. The standard permission set named *Messaging for In-App and Web user* does not apply to reps.

| | Legacy Chat (retired) | Enhanced Chat |
|---|---|---|
| Conversation | one session; ends when the window closes or the connection drops | pauses and resumes, across tabs and devices |
| Automation | standard bots only; no AI agents | enhanced bots and Agentforce agents |
| Record per chat | `LiveChatTranscript` | `MessagingSession`, tied to a `MessagingEndUser` on a `MessagingChannel` |
| Reporting | reports on legacy Chat objects | Messaging Session and Messaging Session Metrics |
| Sneak Peek | yes | no |

## Gotchas

- **Nothing migrates by itself.** Pre-chat is set up again because its structure differs; standard bots are cloned into enhanced bots, and legacy Chat reports are rebuilt.
- **Messaging Session Metrics start on 30 September 2024.** Sessions created before that date have no metrics, so a year-on-year KPI report has a hole in it.
- **Sneak Peek is gone** — reps used to read what the customer was typing before it was sent. Enhanced Chat has no equivalent.
- **One org-wide ceiling: 50 new messaging sessions per second**, shared by every enhanced Messaging channel and Enhanced Chat channel.
- **"Enhanced" means four things:** Enhanced Chat, enhanced Messaging channels, enhanced bots and Enhanced Omni-Channel are separate products. Say which one.

## Gaps to close

- [ ] Which editions include Enhanced Chat without the Digital Engagement add-on at Summer '26? Help's *Supported Editions for Messaging* page holds the matrix.
- [ ] Where in Setup is the Chat Transition Readiness Report launched, and does it still run after the retirement date?

## Confirm in org

- 🚩 Does Setup → Messaging Settings → New Channel list the type as **Enhanced Chat** or still as **Messaging for In-App and Web**? — open the *Add a Messaging Channel* modal in a Summer '26 sandbox.

## Hands-on

- [ ] **SVC-CHAT-01** · 20 min · Start a web chat as a customer, close the tab, reopen the page and send a second message. **Proves:** the conversation resumed — Enhanced Chat is asynchronous, where legacy Chat ended with the window. **Needs:** an Enhanced Chat channel and web deployment.
- [ ] **SVC-CHAT-02** · 15 min · Give a rep only the standard *Messaging for In-App and Web user* permission set, no licence, and have them try to accept a chat. **Proves:** that permission set is not rep access — the Enhanced Chat User licence is. Copy the failure verbatim.
- [ ] **SVC-CHAT-03** · 15 min · After a test chat, query `MessagingChannel`, `MessagingEndUser` and `MessagingSession` for it. **Proves:** which record is the channel, the customer and the session — and that the message text sits on none of them.
- [ ] **SVC-CHAT-04** · 10 min · Open Messaging Settings → New Channel and write down the channel type names offered. **Settles:** whether the Summer '26 UI says Enhanced Chat or Messaging for In-App and Web.

## Related

- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — the channel → deployment → snippet order, and the pre-chat form that needs a flow
- [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) — the Agentforce-first web client that sits on the same channel
- [Enhanced Chat Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) — the session statuses, and how long a conversation survives for an unknown customer
- [Enhanced Chat Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md) — the "In-App" half of the old name, and the REST API
- [Omni-Channel Fundamentals](omni-channel-fundamentals.md) — the routing engine every Enhanced Chat conversation goes through
- [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) — moving a conversation from an enhanced bot or agent to a rep
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the widget on a site, and why a public agent's reach is its agent user, not the guest
- [SF_Experience_Cloud · 25 Enhanced Chat on a site, step by step](../SF_Experience_Cloud/25-enhanced-chat-on-a-site-step-by-step.md) — this channel on a site end to end, including the rep licence and the legacy Chat it must replace
- [SF_Agentforce/](../SF_Agentforce/INDEX.md) — where the Service Agent this channel routes to is built
- [SF_core · CURRENCY](../SF_core/CURRENCY.md) — the retirement and rename rows this note rests on

## Sources

- [What's Enhanced Chat?](https://help.salesforce.com/s/articleView?id=service.reimagine_miaw.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"Beginning in June 2025, Messaging for In-App and Web is changing its name to Enhanced Chat"*
- [Chat & Live Agent End of Support and Retirement](https://help.salesforce.com/s/articleView?id=001790618&language=en_US&type=1) — Salesforce Help 001790618 · via search 2026-09-24 · retired 14 February 2026, provided "as-is" with no SLA
- [Compare Enhanced Chat Capabilities to Legacy Chat Capabilities](https://help.salesforce.com/s/articleView?id=service.miaw_chat_vs_messaging.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · session-based legacy Chat, standard bots only, Sneak Peek not supported
- [Replace Legacy Chat with Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_replacing_chat_considerations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · pre-chat set up anew; clone standard bots into enhanced bots
- [Assess Your Readiness to Transition to Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_chat_readiness_report.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Prepare for a Seamless Shift from Chat to Messaging for In-App and Web](https://help.salesforce.com/s/articleView?id=release-notes.rn_chat_transition_readiness_report.htm&language=en_US&release=256&type=5) — Salesforce release notes, Summer '25 · via search 2026-09-24
- [Enhanced Chat and Messaging Glossary](https://help.salesforce.com/s/articleView?id=service.miaw_glossary.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"a new conversation platform that also houses Salesforce Voice, Enhanced Messaging channels such as WhatsApp, and Partner Messaging Channels"*
- [Provide Conversation Support with Messaging](https://help.salesforce.com/s/articleView?language=en_US&id=service.livemessage_intro.htm&type=5) — Salesforce Help · via search 2026-09-24 · WhatsApp, Facebook Messenger, Apple Messages for Business, LINE, SMS, website and app
- [Give Users Access to Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_prepare_users.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Enhanced Chat User permission set licence
- [Messaging Limits and Considerations](https://help.salesforce.com/s/articleView?id=service.livemessage_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · 50 new messaging sessions per second
- [Messaging Object Model](https://developer.salesforce.com/docs/service/messaging-object-model/guide/messaging-object-model.html) — Salesforce Developers · via search 2026-09-24 · Messaging Session Metrics only for sessions after 30 September 2024
- [Explore Enhanced Chat](https://trailhead.salesforce.com/content/learn/modules/migrating-from-legacy-chat-to-enhanced-chat/explore-enhanced-chat) — Trailhead · read 2026-09-24 · asynchronous vs synchronous, new data model
- [Walk Through a Migration](https://trailhead.salesforce.com/content/learn/modules/migrating-from-legacy-chat-to-enhanced-chat/walk-through-a-migration) — Trailhead · read 2026-09-24 · what must be rebuilt, reporting on Messaging Session
- [Discover Rollout Strategies and Best Practices](https://trailhead.salesforce.com/content/learn/modules/migrating-from-legacy-chat-to-enhanced-chat/discover-rollout-strategies-and-best-practices) — Trailhead · read 2026-09-24 · readiness report → replace, retire or adapt

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; takes over the rename, retirement and product-level facts from SF_Experience_Cloud · 19
- 2026-09-24 · linked SF_Experience_Cloud · 25, the step-by-step site guide; reworded the 19 link after its agent-user correction
