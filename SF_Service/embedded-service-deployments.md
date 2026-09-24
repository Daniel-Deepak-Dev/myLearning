---
vault: SF_Service
format: light
level: working
status: open
gaps: 3
org_checks: 1
labs: 3
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [deployment]
---
# Embedded Service Deployments

**One line:** The Setup record that exposes one Enhanced Chat channel to one kind of client — a web page, a native app or your own UI — and carries what that client needs to connect.

**Reach for it when:** you are deciding whether a surface needs one at all, or finding out why a chat client cannot reach its channel.

> **From my notes.** *"Embedded Service Deployment – when is it really needed?"* — only when Salesforce, or your own code, supplies the chat client: a website, a site, an app or your own UI. WhatsApp, SMS, Voice and agents inside Salesforce need none.

## Key points

| Surface | Deployment? | Type — what the client gets |
|---|---|---|
| Enhanced Web Chat on your own website | **Yes** | **Web** — the snippet in the **Code Snippet** tile |
| Enhanced Web Chat on an Experience Cloud site | **Yes** | **Web**, for the site's domain — read by the **Embedded Messaging** component, no snippet |
| Native iOS or Android app — In-App SDK, or the Agentforce Mobile SDK's Service Agent | **Yes** | **Mobile** — a config file with `esDeveloperName` and the Service API URL |
| Your own UI over the Enhanced Chat API | **Yes** | **Custom Client** — org ID, `esDeveloperName`, SCRT URL |
| Enhanced WhatsApp, SMS, Facebook Messenger, Apple Messages for Business, LINE | **No** | the customer's own messaging app is the client; channel setup has no deployment step |
| Salesforce Voice · an employee agent in Lightning Experience | **No** | a contact center and phone channel · the Agentforce panel, by permission set |
| Headless Agent API | **No** | an External Client App on the client credentials flow |

- **What it holds:** the allowed domain (a top-level domain covers its subdomains), business hours, branding, and the pre-chat form with its **Custom Labels**. Routing is not on it — that stays on the channel.
- **A Web deployment creates a site** in Setup → All Sites. That site hosts the chat iframe, and its URL is the third argument of `init`.
- **`scrt2URL` is your org's messaging host,** `https://<MyDomain>.my.salesforce-scrt.com`, where the client sends and receives messages. Help never expands *SCRT* 🚩 — Salesforce Engineering calls the backend *Service Cloud Realtime*.
- **One channel, many deployments — never the reverse:** the channel's **Embedded Service Deployments** list shows every client attached, v2 included → [v1 vs v2](enhanced-chat-v1-vs-v2.md). A deployment's channel and its type (web or mobile) are fixed at creation.
- **On a site, the Trailhead also added the site URL to CORS** and `scrt2URL` as a Trusted URL (CSP context *Experience Builder Sites*, all six directives). Why → [CORS allowlist](../SF_core/06-integration-and-apis/28-cors-allowlist.md) · [Trusted URLs & CSP](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md).
- **Legacy Embedded Service Chat deployments served Chat,** retired 14 February 2026, and pointed at a **Site Endpoint** you picked. They cannot share a page or site with Enhanced Web Chat — remove them and any **Channel Menu** deployment, or add Enhanced Web Chat to the Channel Menu.
- **The snippet tells them apart.** Legacy loads `…/embeddedservice/5.0/esw.min.js` and calls `embedded_svc.init`; Enhanced Chat loads `bootstrap.min.js` from its `ESW…` site and calls `embeddedservice_bootstrap.init(orgId, deploymentApiName, siteUrl, { scrt2URL })` 🚩.

## Gotchas

- **Save is not Publish, and caches lag both.** Every change needs **Publish**, up to 10 minutes to land; an edit to the Business Hours record behind a deployment can take up to 2 hours.
- **A Fallback Message left on breaks the window:** a test chat shows *"Looks like something went wrong, and we can't display the conversation"*. Turn it off in Messaging Settings, then republish (Help 005239538).
- **The Agentforce Mobile SDK wants the SCRT host.** Its commonest mistake is `https://<org>.my.salesforce.com` as the Service API URL; `esDeveloperName` is case-sensitive too.

## Gaps to close

- [ ] Is a **Custom Client** deployment's type fixed too? Help only says web or mobile cannot change.
- [ ] Does the Experience Builder **Embedded Messaging** component pick a deployment, or find it by the site's domain — and which wins when two Web deployments share that domain?
- [ ] Are `scrt2URL`, the Custom Client's "SCRT URL" and the Mobile config's Service API URL the same host for one org?

## Confirm in org

- 🚩 Does **New Deployment** still offer **Embedded Service Chat** after the 14 February 2026 retirement? — Setup → Embedded Service Deployments → New Deployment in a Summer '26 org.

## Hands-on

- [ ] **SVC-ESD-01** · 25 min · Add a second Web deployment to your Enhanced Chat channel for another domain, give it a different branding colour, publish both and chat through each. **Proves:** one channel serves many deployments — both land in the same routing, each keeps its own branding. **Needs:** an Enhanced Chat channel, two web pages on domains you control.
- [ ] **SVC-ESD-02** · 10 min · Start **New Deployment** and note the kinds offered, then open an existing Web deployment and try to change its type or its channel. **Proves:** type and channel are fixed at creation — copy what Setup shows verbatim. **Settles:** whether Embedded Service Chat is still offered.
- [ ] **SVC-ESD-03** · 15 min · Delete the `SCRT_URL` Trusted URL in the Trailhead org, republish the site, open the chat and read the browser console. **Proves:** why the Trailhead needed it — copy the CSP error verbatim, then restore the entry. **Needs:** the Trailhead's Experience Cloud site.

## Related

- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — the five steps in order; this note only decides whether step 3 applies
- [Enhanced Chat Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md) — what the Mobile and Custom Client deployments feed their clients, call by call
- [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) — the v2 client is one more deployment on the same channel
- [Enhanced Chat](enhanced-chat.md) — the channel itself, and the legacy Chat retirement the old deployments belonged to
- [Enhanced Conversation Component](enhanced-conversation-component.md) — the rep's end of the conversation a deployment starts
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the Embedded Messaging component that reads a Web deployment on a site, and the guest user behind it
- [SF_Experience_Cloud · 25 Enhanced Chat on a site, step by step](../SF_Experience_Cloud/25-enhanced-chat-on-a-site-step-by-step.md) — the Web deployment for a site's domain, from Setup → Domains to the guest test, and where head-markup code goes instead of the snippet
- [SF_core · 06-integration · 28 CORS allowlist](../SF_core/06-integration-and-apis/28-cors-allowlist.md) — why the Trailhead added the site URL to CORS
- [SF_core · 07-security · 27 Trusted URLs & CSP](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md) — why `scrt2URL` needed a Trusted URL before the site could load the chat
- [RELEASE-RADAR · Agentforce platform](../RELEASE-RADAR/agentforce-platform.md) — the Agentforce Mobile SDK releases that read a Mobile deployment

## Sources

- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead, *Build an Experience Cloud Site with Knowledge and Enhanced Chat* · read 2026-09-24 · New Deployment → Enhanced Chat → Web; Save takes several minutes; Publish up to 10 minutes; CORS entry; `scrt2URL` from the Chat Code Snippet as Trusted URL `SCRT_URL`, CSP context Experience Builder Sites, six directives
- [Considerations and Limitations for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"After you select a deployment type, web or mobile, you can't change the type later"*; channel fixed once added; Business Hours cache up to two hours; Embedded Service Chat and Channel Menu cannot share a site with Enhanced Web Chat
- [Configure an Enhanced Web Chat Deployment](https://help.salesforce.com/s/articleView?language=en_US&id=service.miaw_configure_web_deployment_1.htm&type=5) — Salesforce Help · via search 2026-09-24 · the Code Snippet
- [Configure an Enhanced Web Chat Deployment in an Experience Builder Site](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_experience_builder.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · drag and drop is the only supported method
- [Customize an Enhanced Chat Deployment](https://help.salesforce.com/s/articleView?id=service.miaw_create_deployment_type.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the Pre-Chat tile on the deployment settings page
- [Quickly Set Up Enhanced Chat v1 or v2 for Testing](https://help.salesforce.com/s/articleView?id=service.miaw_setup_stages.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · custom labels, branding and pre-chat on the deployment
- [Create an Enhanced Chat v2 Deployment for an Existing Messaging Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.enhanced_chat_v2_existing_channel_deployment.htm&type=5) — Salesforce Help · via search 2026-09-24 · add deployments to a channel; the channel's Embedded Service Deployments list
- [Configure a Custom Client Deployment for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_custom.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Configure an Enhanced In-App Chat Deployment](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_mobile.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Before You Begin | Agentforce Mobile SDK](https://developer.salesforce.com/docs/ai/agentforce-mobile-sdk/guide/agentforce-mobile-sdk-before-you-begin.html) — Salesforce Developers · via search 2026-09-24 · Service Agent needs Enhanced Chat and an Embedded Service Deployment; Service API URL from the Mobile Configuration JSON file
- [Troubleshooting | Agentforce Mobile SDK](https://developer.salesforce.com/docs/ai/agentforce-mobile-sdk/guide/agentforce-mobile-sdk-react-native-troubleshooting.html) — Salesforce Developers · via search 2026-09-24 · `my.salesforce.com` instead of the `salesforce-scrt.com` host; `esDeveloperName` case-sensitive
- [Get WhatsApp Up and Running](https://trailhead.salesforce.com/content/learn/modules/whatsapp-for-service-cloud/get-started-with-whatsapp) — Trailhead · read 2026-09-24 · enhanced WhatsApp setup steps, none of them a deployment
- [Create or Upgrade to an Enhanced WhatsApp Channel](https://help.salesforce.com/s/articleView?id=service.messaging_whatsapp_enhanced.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Configure Your Contact Center](https://help.salesforce.com/s/articleView?language=en_US&id=sf.voice_contact_center_configure.htm&type=5) and [Create a Phone Channel](https://help.salesforce.com/s/articleView?id=sf.voice_create_phone_channel.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Voice setup runs through a contact center
- [Connect an Agent to Lightning Experience and Mobile](https://help.salesforce.com/s/articleView?id=ai.agent_deploy_emp_lex.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · employee agents in the Agentforce panel; access by permission set or profile
- [Get Started | Agent API](https://developer.salesforce.com/docs/einstein/genai/guide/agent-api-get-started.html) — Salesforce Developers · via search 2026-09-24 · an external client app on the client credential flow
- [Build Headless Agents with the Agent API](https://developer.salesforce.com/blogs/2025/04/build-headless-agents-with-the-agent-api) — Salesforce Developers blog, April 2025 · via search 2026-09-24 · the MIAW API is for human-in-the-loop UIs, Agent API for headless use
- [Salesforce Voice: Preparing for Enhanced Domains Enforcement](https://help.salesforce.com/s/articleView?id=000394652&language=en_US&type=1) — Salesforce Help 000394652 · via search 2026-09-24 · "the telephony API (SCRT2 URL)"
- [How Agentforce Enhanced Chat Built an Agent-first Chat Experience](https://engineering.salesforce.com/how-agentforce-enhanced-chat-built-an-agent-first-chat-experience-while-ensuring-easy-migration-for-3000-customers/) — Salesforce Engineering, 2 February 2026 · read 2026-09-24 · *"Service Cloud Realtime backend stack"*
- [Embedded Service Chat for Web Developer Guide (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/embedded_services_web_dev_guide.pdf) — Salesforce, v68.0 Winter '27, last updated 4 September 2026 · read 2026-09-24 · `esw.min.js` from `service.force.com/embeddedservice/5.0/`, `embedded_svc.init`; legacy chat *"in maintenance-only mode"* — a Winter '27 build, used only for legacy facts
- [Create an Embedded Service Deployment](https://help.salesforce.com/s/articleView?id=service.snapins_create_deployment.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · legacy Site Endpoint menu
- [Chat & Live Agent End of Support and Retirement](https://help.salesforce.com/s/articleView?id=001790618&language=en_US&type=1) — Salesforce Help 001790618 · via search 2026-09-24 · retired 14 February 2026
- [Salesforce Messaging for In-App and Web Can't display conversation Exception](https://help.salesforce.com/s/articleView?id=005239538&language=en_US&type=1) — Salesforce Help 005239538 · via search 2026-09-24 · Fallback Message; disable and republish
- [ESW1234 Embedded Service test pages](https://github.com/ESW1234/esw1234.github.io) — GitHub, third party 🚩 · read 2026-09-24 · the `embeddedservice_bootstrap.init` arguments, the `ESW…` site URL and `assets/js/bootstrap.min.js`

## History

- 2026-09-24 · created from your Trailhead feed (Knowledge & Enhanced Chat site project)
- 2026-09-24 · linked SF_Experience_Cloud · 25, the step-by-step site guide
