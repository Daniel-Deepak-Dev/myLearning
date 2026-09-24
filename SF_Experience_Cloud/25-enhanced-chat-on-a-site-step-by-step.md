---
vault: SF_Experience_Cloud
format: light
level: working
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [deployment]
---
# Enhanced Chat on a Site, Step by Step

**One line:** The chat bubble on an Experience Cloud site is an Enhanced Chat **Web** deployment for the site's domain, shown by the **Embedded Messaging** component. There is no snippet to paste.

**Reach for it when:** you are putting chat on a site end to end, or the button never appears.

> **"Chat bubble" is not a Salesforce term.** Setup, the component and the API call it the **chat button** — search for that.

## Key points

| # | Where | Do | Watch for |
|---|---|---|---|
| 0 | Service Setup | queue, Omni-Channel flow, Enhanced Chat channel; reps get the Enhanced Chat User licence and **Enhanced Chat Rep** | in full → [setup chain](../SF_Service/enhanced-chat-setup-chain.md) steps 1–2 |
| 1 | Setup → Domains | copy the **Experience Cloud Site Domain** | a domain, not a URL |
| 2 | Embedded Service Deployments → New → Enhanced Chat → **Web** | pick the channel, paste the domain, Save, **Publish** | type and channel are fixed → [deployments](../SF_Service/embedded-service-deployments.md) |
| 3 | the deployment's Code Snippet → Setup → **Trusted URLs** | copy only `scrt2URL`; add it with context **Experience Builder Sites** | directives → [24](24-site-csp-security-level-and-trusted-scripts.md); the Trailhead also adds the site to CORS 🚩 |
| 4 | Experience Builder → Components | drag **Embedded Messaging** into the footer; **Chat Button Visibility** = Always Visible | Aura: the **Template Footer**. LWR: the theme layout's footer 🚩 |
| 5 | Experience Builder → Settings, then **Publish** | public site: tick *Guest users can see and interact with the site without logging in* | a site publish is separate from the deployment's |
| 6 | an incognito window | chat as a guest while the rep is **Available** in Omni-Channel | the button hides outside business hours |

- **Seven templates are supported:** Build Your Own (Aura), Customer Account Portal, Partner Central, Help Center, Customer Service, Build Your Own (LWR) and Microsite (LWR). Help warns that some features are limited on LWR.
- **Where LWR and Aura differ.** Token-based user verification works on three Aura templates only, so chat on an LWR site stays unverified → [Sessions & verification](../SF_Service/enhanced-chat-sessions-and-user-verification.md). A Mobile Publisher app built from an LWR site cannot download chat files or transcripts → [17](17-mobile-publisher-and-pwa-delivery.md).
- **The button's look lives on the deployment:** colours and font in its branding, text in its custom labels. Position is `settings.chatButtonPosition` — bottom right by default, at `25px,30px` (Summer '24).
- **On a site, code goes in head markup,** not a snippet: Settings → Advanced → **Edit Head Markup** takes `hideChatButtonOnLoad`, `chatButtonPosition`, `utilAPI.launchChat()` for your own button, and hidden pre-chat → [setup chain](../SF_Service/enhanced-chat-setup-chain.md). An inline script there needs Relaxed CSP → [24](24-site-csp-security-level-and-trusted-scripts.md) — the site rule applied to chat, since no chat page says so 🚩.
- **The guest user gates the page, not the conversation.** The visitor becomes an anonymous `MessagingEndUser`. An Agentforce Service Agent behind the channel acts as its own **agent user** → [19](19-embedded-messaging-and-agents-in-sites.md).

## Gotchas

- **Two publishes, two caches.** The deployment's Publish takes up to 10 minutes to reach the site, and neither publish triggers the other.
- **Legacy chat blocks it.** Embedded Service Chat or Channel Menu cannot share a site with Enhanced Web Chat — remove them first.
- **Closed business hours hide the button.** A test at 9 pm against a 9-to-5 schedule looks like a broken site.
- **"We can't display the conversation"** in the window is the Fallback Message setting, not the site → [deployments](../SF_Service/embedded-service-deployments.md).

## Gaps to close

- [ ] Where does Help place the component on an LWR site? Only the Aura *Template Footer* is documented, in Trailhead.
- [ ] Does the deployment's Domain field accept a site's custom domain as well as its `my.site.com` domain?
- [ ] What did Summer '25's *Customize Your Messaging for Web Chat Button* add — icon, text, shape — and does it reach a site?

## Confirm in org

- 🚩 Does the chat render on a **Strict CSP** site with nothing in head markup? — Experience Builder → Settings → Security & Privacy, publish, load as a guest.

## Hands-on

- [ ] **EC-CHAT-01** · 30 min · Run steps 1–6 on a Build Your Own (LWR) site, then chat as a guest from an incognito window. **Proves:** once the channel exists, the site side is five steps and two publishes. **Needs:** an Enhanced Chat channel with a queue and a rep — SF_Service lab SVC-CHSET-01.
- [ ] **EC-CHAT-02** · 20 min · Change the deployment's button colour and publish only the deployment; then change Chat Button Visibility and publish only the site. **Proves:** which publish each change needs, and how long each takes to show.
- [ ] **EC-CHAT-03** · 15 min · Point the deployment's Domain at another domain, publish, and load the site. **Proves:** what a domain mismatch looks like — copy the console output verbatim, then restore it.
- [ ] **EC-CHAT-04** · 20 min · On a Strict CSP site, set `chatButtonPosition` in head markup and publish; then switch to Relaxed CSP and publish again. **Proves:** site code means head markup, and inline script needs Relaxed CSP — copy the console error. **Settles:** whether the chat renders on Strict CSP.

## Related

- [19 · Embedded messaging & agents in sites](19-embedded-messaging-and-agents-in-sites.md) — why a chat on a public site, and an agent behind it, is the riskiest thing on a site
- [24 · Site CSP, security level & trusted scripts](24-site-csp-security-level-and-trusted-scripts.md) — why head-markup code needs Relaxed CSP, and which directives the `scrt2URL` entry needs
- [03 · Site setup, domains & publishing](03-site-setup-domains-and-publishing.md) — the site domain step 1 copies, and why publish is not activate
- [04 · Experience Builder layouts & theme layouts](04-experience-builder-layouts-and-theme-layouts.md) — the Template Footer and the theme layout regions the component drops into
- [07 · Guest user security model](07-guest-user-security-model.md) — what the guest-access checkbox in step 5 opens beyond the chat
- [17 · Mobile Publisher & PWA delivery](17-mobile-publisher-and-pwa-delivery.md) — the app wrapper that loses chat file and transcript downloads
- [SF_Service · Enhanced Chat Setup Chain](../SF_Service/enhanced-chat-setup-chain.md) — step 0 in full: the queue, the flow, the channel and the pre-chat mapping chain
- [SF_Service · Embedded Service Deployments](../SF_Service/embedded-service-deployments.md) — what the Web deployment in step 2 holds, and the open question of which deployment the component reads
- [SF_Service · Enhanced Chat](../SF_Service/enhanced-chat.md) — the Enhanced Chat User licence step 0 gives reps, and the retired legacy Chat the site must not still carry
- [SF_Service · Sessions & User Verification](../SF_Service/enhanced-chat-sessions-and-user-verification.md) — why chat on an LWR site stays unverified, and what an unverified guest keeps
- [SF_core · 07-security · 27 Trusted URLs & CSP](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md) — the org list and CSP context the `scrt2URL` in step 3 goes on

## Sources

- [Configure a Web Deployment](https://trailhead.salesforce.com/content/learn/projects/build-a-community-with-knowledge-and-chat/enable-and-configure-lightning-knowledge) — Trailhead, *Build an Experience Cloud Site with Knowledge and Enhanced Chat* · read 2026-09-24 · *"Drag Embedded Messaging to the Template Footer section"*; Chat Button Visibility → Always Visible; the guest-access checkbox; Domain from the Experience Cloud Sites Domain; the CORS entry; `scrt2URL` as Trusted URL `SCRT_URL`, context Experience Builder Sites
- [Considerations and Limitations for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the seven supported templates; drag and drop only; Embedded Service Chat and Channel Menu cannot share the site
- [MIAW is Supported in Lightning Web Runtime (LWR)](https://help.salesforce.com/s/articleView?id=004333228&language=en_US&type=1) — Salesforce Help 004333228 · via search 2026-09-24 · *"certain features may be limited compared to Aura templates"*
- [Configure an Enhanced Web Chat Deployment in an Experience Builder Site](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_experience_builder.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · drag Embedded Messaging onto the template, then the Property Editor
- [Give Users Access to Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_prepare_users.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Enhanced Chat User licence, then **Enhanced Chat Rep**; Messaging Session read/edit; presence statuses
- [Place the Chat Button Where You Want for Messaging for Web](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_messaging_chat_cutton_placement.htm&release=250&type=5) — Salesforce release notes, Summer '24 · via search 2026-09-24 · `chatButtonPosition`, default bottom right at `25px,30px`
- [Customize Your Messaging for Web Chat Button](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_customize_chat_button.htm&language=en_US&release=256&type=5) — Salesforce release notes, Summer '25 · via search 2026-09-24 · title only, content not reachable 🚩
- [Branding Elements Guide for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.ec_brand_elements_2.htm&language=en_US&type=5) and [Configure Custom Labels for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_custom_labels.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · colours and font; labels per deployment
- [Settings | Enhanced Web Chat Reference](https://developer.salesforce.com/docs/service/messaging-web/references/m4w-reference/settingsAPI.html) — Salesforce Developers · via search 2026-09-24 · *"If you use Enhanced Web Chat on an Experience Cloud or Commerce Cloud site, add snippet settings to the header markup"*
- [APIs | Enhanced Web Chat](https://developer.salesforce.com/docs/service/messaging-web/guide/api-overview.html) — Salesforce Developers · via search 2026-09-24 · on a site, *"add JavaScript code to the head markup section of your site"*
- [Launch Chat](https://developer.salesforce.com/docs/service/messaging-web/guide/launch-chat.html) and [Show/Hide Chat Button](https://developer.salesforce.com/docs/service/messaging-web/guide/show-hide-chat.html) — Salesforce Developers · via search 2026-09-24 · `launchChat()` after `onEmbeddedMessagingButtonCreated`, with the button hidden or not; `showChatButton` overrides `hideChatButtonOnLoad`
- [Add Markup to the Page <head>](https://help.salesforce.com/s/articleView?id=experience.community_builder_page_head.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · restricted tags; invalid head markup cannot be saved
- [Limitations for Mobile Publisher for Experience Cloud LWR Sites](https://help.salesforce.com/s/articleView?language=en_US&id=xcloud.branded_apps_lwr_gaps.htm&type=5) — Salesforce Help · via search 2026-09-24 · with Enhanced Chat in the app, no file or transcript downloads
- [Set Business Hours in Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_business_hours.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · button hidden outside hours
- [Can't display conversation Exception](https://help.salesforce.com/s/articleView?id=005239538&language=en_US&type=1) — Salesforce Help 005239538 · via search 2026-09-24 · Fallback Message
- [Configure Service Agent Access](https://help.salesforce.com/s/articleView?language=en_US&id=ai.agent_user.htm&type=5) — Salesforce Help · via search 2026-09-24 · the agent user

## History

- 2026-09-24 · created — research pass on your request for a step-by-step chat bubble guide; puts the site half of 19 and the SF_Service chain into one ordered path, with the LWR and Aura differences
