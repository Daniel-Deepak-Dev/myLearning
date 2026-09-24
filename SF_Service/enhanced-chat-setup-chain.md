---
vault: SF_Service
format: light
level: working
status: open
gaps: 1
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [deployment]
---
# Enhanced Chat Setup Chain

**One line:** Five steps in a fixed order — Omni-Channel, a Messaging channel, an Embedded Service deployment, publish, then the code snippet or the site component.

**Reach for it when:** you are standing up a chat channel, or finding out why the chat button never appears.

## Key points

| # | Where in Setup | What you set | Watch for |
|---|---|---|---|
| 1 | Omni-Channel Settings, Queues, Flows | Omni-Channel on; a queue for Messaging Session; an Omni-Channel flow with **Messaging** as the service channel | the flow does the routing → [Omni-Channel Flows](omni-channel-flows.md) |
| 2 | Messaging Settings → New Channel → Enhanced Chat | the channel; Channel Routing = that flow plus a **fallback queue** | the fallback queue takes work when the flow is unavailable |
| 3 | Embedded Service Deployments → New Deployment → Enhanced Chat | **Web**, **Mobile** or **Custom Client**; the top-level domain | type and channel cannot be changed later → [do you need one?](embedded-service-deployments.md) |
| 4 | the deployment's settings page → **Publish** | every change, every time | changes take up to 10 minutes to land (caching) |
| 5 | Code Snippet, or Experience Builder | the `embeddedservice_bootstrap` snippet on your page, or the component on a site page | on a site, drag and drop is the only supported method |

- **The Domain field covers subdomains** — enter `example.com`, not a full URL. For a site, copy the **Experience Cloud Site Domain** from Setup → Domains.
- **Pre-chat has two kinds of field.** *Visible:* First Name, Last Name, Email, Subject, plus custom Email, Number, Phone, Checkbox, Dropdown or Text; *hidden:* always text, set from page code with `embeddedservice_bootstrap.prechatAPI.setHiddenPrechatFields` after `onEmbeddedMessagingReady`.
- **Pre-chat values reach the flow through a mapping chain:** custom parameter (its **Channel Variable Name**) → **parameter mapping** (a flow variable name) → the flow's input variable → e.g. Update Records on `MessagingSession`.
- **A working pre-chat form needs Routing Type set to Omni-Flow**, and a flow that reads the pre-chat values. Queue-based routing is simpler, but it has no flow to receive them.
- **Business hours go on the deployment:** on the web the button hides outside hours, in-app shows a banner instead. Set `embeddedservice_bootstrap.settings.hideChatButtonOnLoad` before `init` to override.
- **Auto-responses are messaging components on the channel:** Conversation Acknowledgement, Start Conversation, End Conversation, Inactive Conversation. Formula templates can read Messaging Session and Messaging User fields — except in Conversation Acknowledgement, which fires before a flow could fill them.
- **Components reps send** are built in **Messaging Component Builder**: enhanced links, questions with static or dynamic options, secure forms (beta), time selectors.

## Gotchas

- **Every pre-chat value arrives as a string** — checkboxes and numbers too. Convert before you compare.
- **Pre-chat data does not follow the customer into a new session** by default, when they carry on after a session ended.
- **A custom pre-chat field needs a Custom Label** in the deployment settings (Label Group **Pre-Chat**, up to 1,000 characters). There is no default text.
- **A web deployment creates a site** in Setup → All Sites to host its iframe. Do not reuse that URL for anything else — it has reduced security.
- **Old and new cannot share a page.** Remove Embedded Service Chat and Channel Menu deployments before adding Enhanced Web Chat, or add Enhanced Web Chat to the Channel Menu.
- **The web client needs a supported language to load at all.** Swapping business hours and publishing can also take up to 10 minutes to show.

## Gaps to close

- [ ] What are the exact Routing Type values on a channel at Summer '26? Only a third-party Genesys page 🚩 names the queue option "Omni-Queue".

## Confirm in org

- 🚩 On queue-based routing with the pre-chat form still on, does the form render and drop its values, or not render at all? — Messaging Settings → the channel → routing, then load the page.

## Hands-on

- [ ] **SVC-CHSET-01** · 45 min · Build the chain in order — queue, Omni-Channel flow, channel, web deployment — and load the snippet before you publish, then after. **Proves:** each step needs the one before it, and nothing reaches the page until Publish. **Needs:** Service Cloud sandbox, a web page on a domain you control.
- [ ] **SVC-CHSET-02** · 20 min · Add a custom Number pre-chat field, map it to a Number flow variable and submit `42`. **Proves:** pre-chat values arrive as strings — record what the variable receives or copy the error verbatim, then fix it with a Text variable.
- [ ] **SVC-CHSET-03** · 20 min · Give the deployment business hours that are closed right now, publish, and reload the page every two minutes. **Proves:** the button hides outside hours, and a publish takes minutes to reach the page.
- [ ] **SVC-CHSET-04** · 15 min · Switch the channel from the Omni-Channel flow to queue routing, keep the pre-chat form on, and start a chat. **Settles:** what pre-chat does without Omni-Flow.

## Related

- [Enhanced Chat](enhanced-chat.md) — what the channel is, and the Enhanced Chat User licence step 1 assumes
- [Omni-Channel Flows](omni-channel-flows.md) — how to build the flow step 2 points at, and how it reads pre-chat values
- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — the queue-based alternative to a flow, and how a session consumes capacity
- [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) — step 3 again, for a v2 deployment on the channel you already built
- [Enhanced Chat Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md) — the Mobile and Custom Client deployment types, which skip step 5
- [Enhanced Chat Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) — the channel setting that turns on verified users
- [Embedded Service Deployments](embedded-service-deployments.md) — whether a surface needs step 3 at all, and what the deployment holds
- [SF_core · 06-integration · 28 CORS allowlist](../SF_core/06-integration-and-apis/28-cors-allowlist.md) — owns the open question of whether Enhanced Web Chat needs a CORS entry; lab SF-CORS-04 settles it
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — step 5 on a site: the Experience Builder component and the guest user behind it
- [SF_Experience_Cloud · 25 Enhanced Chat on a site, step by step](../SF_Experience_Cloud/25-enhanced-chat-on-a-site-step-by-step.md) — step 5 on a site, every step in order: the site domain, the Trusted URL, the component, two publishes and a guest test

## Sources

- [Prepare a Salesforce Org for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_prepare_org_1.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Omni-Channel flow, *"Select Messaging for the Service Channel"*
- [Set Up Routing for Messaging Channels](https://help.salesforce.com/s/articleView?id=service.messaging_omnichannel_routing.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · queue-based routing as the simple alternative to a flow
- [Configure an Enhanced Web Chat Deployment](https://help.salesforce.com/s/articleView?language=en_US&id=service.miaw_configure_web_deployment_1.htm&type=5) — Salesforce Help · via search 2026-09-24 · top-level domain covers subdomains; Code Snippet
- [Configure an Enhanced Web Chat Deployment in an Experience Builder Site](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_experience_builder.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · copy the Experience Cloud Site Domain from Domains
- [Considerations and Limitations for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · type fixed after creation, publish up to 10 minutes, generated site, supported language, custom label, Terms and Conditions, drag and drop only
- [Create Customer Flows for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_custom_field_example.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"Routing Type set as OmniFlow and a flow that uses the pre-chat dataset"*; values passed as strings
- [Persist Pre-Chat Inputs Across Messaging Sessions](https://help.salesforce.com/s/articleView?id=service.miaw_handle_sessions.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Hidden Pre-Chat](https://developer.salesforce.com/docs/service/messaging-web/guide/pre-chat.html) — Salesforce Developers · via search 2026-09-24 · `setHiddenPrechatFields` after `onEmbeddedMessagingReady`
- [Set Business Hours in Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_business_hours.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · button hidden outside hours; `hideChatButtonOnLoad`
- [Create and Send Auto-Response Components](https://help.salesforce.com/s/articleView?id=service.messaging_components_auto_response.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the four auto-response slots; Messaging Component Builder
- [Collect Information to Quickly Help End Users](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/collect-information-to-help-end-users) — Trailhead · read 2026-09-24 · visible and hidden field types, Channel Variable Name, parameter mapping
- [Decide When and How to Present the Chat Button](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/decide-when-and-how-to-present-the-chat-button) — Trailhead · read 2026-09-24 · business hours on web vs in-app
- [Send Structured Content to End Users](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/send-structured-content-to-end-users) — Trailhead · read 2026-09-24 · component types, secure forms (beta)
- [Add Your Website to the CORS Allowlist](https://help.salesforce.com/s/articleView?id=service.embedded_chat_cors_allowlist.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the legacy Embedded Chat page; the CORS question it raised now lives in SF_core · 06-integration · 28
- [Configure external routing of Salesforce messaging](https://help.mypurecloud.com/articles/routing-of-salesforce-chats/) — Genesys, third party 🚩 · via search 2026-09-24 · the "Omni-Queue" routing type name

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; takes over the setup chain from SF_Experience_Cloud · 19, which keeps the site-side component and guest exposure
- 2026-09-24 · the CORS gap handed to SF_core · 06-integration · 28, which owns it as an org check; step 3 now points at Embedded Service Deployments
- 2026-09-24 · linked SF_Experience_Cloud · 25, the step-by-step site guide
