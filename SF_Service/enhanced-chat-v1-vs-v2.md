---
vault: SF_Service
format: light
level: working
status: open
gaps: 4
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Enhanced Chat v1 vs v2

**One line:** v2 is the Agentforce-first web client for the same Messaging channel — a new deployment, not a new channel — and the only version that renders Custom Lightning Types.

**Reach for it when:** you are putting an Agentforce Service Agent on a website, or deciding whether an existing v1 deployment should switch.

## Key points

- **v2 shipped in Winter '26 (24 October 2025)** as *"a new customer interface for Enhanced Web Chat"*. Only the web client changes — both versions connect Service agents through the same channel and Omni-Channel flow, and the In-App SDKs are a separate line → [Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md).
- **v2 attaches to an existing channel.** Create a new Embedded Service deployment, pick the existing Messaging Channel, save, then click **Switch to v2** → **Switch & Publish**; the channel's **Embedded Service Deployments** list shows what is attached.
- **Custom Lightning Types render in v2 only.** The override goes in the type's `enhancedWebChat` channel folder; a renderer under `lightningDesktopGenAi` alone does nothing here → [SF_core · 03-lwc · 19](../SF_core/03-lwc-and-slds/19-custom-lightning-types-for-agent-output.md).
- **`setSessionContext` is v2 only.** `embeddedservice_bootstrap.utilAPI.setSessionContext` passes `currentPage` and `search` (both optional), plus custom context variables defined in Agentforce Builder.
- **Inline mode** (`displayMode = 'inline'`) embeds the v2 client inside an element on your page, instead of a floating button.
- **Built as a new stack.** Salesforce Engineering (February 2026): Lightning Types, LWC and the Service Cloud Realtime backend, one-click upgrade or downgrade through preview and publish, and 3,000+ live tenants migrated.
- **v2 is still catching up on v1.** Summer '26 Help titles include *File Sharing in Enhanced Chat v2* and *Pre-Chat* for v2 🚩 — the release pages themselves were not reachable.

```js
// v2 only. Set before embeddedservice_bootstrap.init(...), like other settings flags 🚩
embeddedservice_bootstrap.settings.displayMode = 'inline';

window.addEventListener('onEmbeddedMessagingReady', () => {
  // Never in initEmbeddedMessaging. Keys: currentPage, search — copy the shape from Context Events
  embeddedservice_bootstrap.utilAPI.setSessionContext(/* … */);
});
```

## Gotchas

- **Never mix v1 and v2 on one domain.** Messages may fail to appear in the v1 window, especially Lightning Types, which v1 cannot draw.
- **A missing renderer is silent.** Register it for desktop only and nothing renders from it in v2, with no error — it looks like a broken action, not a missing folder.
- **Republish after testing any new feature.** That is Help's own advice for v2; an unpublished change never reaches the snippet.

## Gaps to close

- [ ] Which v1 settings does v2 still not support at Summer '26? *Compare Enhanced Chat v1 to Enhanced Chat v2* groups them under Messaging Channel Settings, Embedded Service Deployment Settings and Additional Features — copy the "no" rows here.
- [ ] Does v2 support token-based user verification (`userVerificationAPI.setIdentityToken`) on the same terms as v1?
- [ ] Which setting names the host element for inline mode, and does inline mode work on an Experience Builder page?
- [ ] In which release did v2 gain pre-chat and file sharing?

## Confirm in org

- 🚩 After **Switch & Publish**, does Setup offer a switch back to v1 on the same deployment, and does the code snippet change? — Embedded Service Deployments → the v2 deployment.

## Hands-on

- [ ] **SVC-CHV2-01** · 30 min · Add a v2 deployment to your existing v1 channel, Switch & Publish, and chat through each deployment on its own domain. **Proves:** one channel serves both clients — v2 is a deployment choice, not a new channel.
- [ ] **SVC-CHV2-02** · 20 min · Load the v1 and v2 snippets on the same page and trigger an agent reply that uses a Custom Lightning Type. **Proves:** why mixing versions on one domain is unsupported — record what the v1 window shows. **Needs:** Agentforce, a deployed Custom Lightning Type.
- [ ] **SVC-CHV2-03** · 20 min · Register a renderer only under `lightningDesktopGenAi`, trigger the action in v2, then add the `enhancedWebChat` folder and redeploy. **Proves:** renderers are per channel, and the failure is silence. **Needs:** Agentforce, a Salesforce DX project.
- [ ] **SVC-CHV2-04** · 15 min · Call `setSessionContext` inside `initEmbeddedMessaging`, then move it into the `onEmbeddedMessagingReady` listener. **Proves:** context only reaches the agent when it is set after ready — copy any console error verbatim. **Needs:** an Agentforce Service Agent with a context variable.

## Related

- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — the channel and deployment steps a v2 deployment reuses
- [Enhanced Chat](enhanced-chat.md) — the product under both versions, and the MIAW rename
- [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) — what happens when the v2 agent hands over to a rep
- [Enhanced Chat Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) — verification as documented for v1, which gap 2 asks about for v2
- [SF_core · 03-lwc · 19 Custom Lightning Types for agent output](../SF_core/03-lwc-and-slds/19-custom-lightning-types-for-agent-output.md) — the renderer contract and the `enhancedWebChat` folder v2 reads
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — a v2 agent on a public site, and the agent user it acts as
- [SF_Agentforce/](../SF_Agentforce/INDEX.md) — where the Service Agent and its context variables are built

## Sources

- [What's Enhanced Chat v2?](https://help.salesforce.com/s/articleView?id=service.enhanced_chat_v2_intro.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"a new customer interface for Enhanced Web Chat on Service Cloud"*
- [Compare Enhanced Chat v1 to Enhanced Chat v2](https://help.salesforce.com/s/articleView?language=en_US&id=service.enhanced_chat_feature_comparison.htm&type=5) — Salesforce Help · via search 2026-09-24 · *"v1 does not support Lightning Types"*; the three comparison groups
- [Create an Enhanced Chat v2 Deployment for an Existing Messaging Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.enhanced_chat_v2_existing_channel_deployment.htm&type=5) — Salesforce Help · via search 2026-09-24 · Switch to v2 → Switch & Publish; the channel's deployment list
- [Switch to Enhanced Chat v2](https://help.salesforce.com/s/articleView?language=en_US&id=service.enhanced_chat_v2_setup.htm&type=5) — Salesforce Help · via search 2026-09-24
- [Optimize Enhanced Chat v2 Setup](https://help.salesforce.com/s/articleView?id=service.enhanced_chat_v2_optimize_setup.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · republish after testing; don't mix v1 and v2 on one domain
- [Create Customer Chats using Enhanced Chat v2](https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-enhanced-chat.html) — Salesforce Developers · via search 2026-09-24 · *"messages may fail to appear in the Enhanced Chat v1 version"*
- [Context Events](https://developer.salesforce.com/docs/service/messaging-web/guide/context-events.html) — Salesforce Developers · via search 2026-09-24 · `setSessionContext`, `currentPage`, `search`, call after `onEmbeddedMessagingReady`
- [Inline Mode in Enhanced Chat v2](https://developer.salesforce.com/docs/ai/agentforce/guide/enhanced-chat-inline-mode.html) — Salesforce Developers · via search 2026-09-24 · `displayMode = 'inline'`
- [How Agentforce Enhanced Chat Built an Agent-first Chat Experience](https://engineering.salesforce.com/how-agentforce-enhanced-chat-built-an-agent-first-chat-experience-while-ensuring-easy-migration-for-3000-customers/) — Salesforce Engineering, 2 February 2026 · read 2026-09-24
- [Messaging release notes, Summer '26](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_service.htm&language=en_US&release=262&type=5) — Salesforce release notes · via search 2026-09-24 · v2 file-sharing and pre-chat titles; content not reachable 🚩

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; takes over the v2 facts from SF_Experience_Cloud · 19 and adds the feature-parity questions
- 2026-09-24 · reworded the 19 link after its agent-user correction
