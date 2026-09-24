---
vault: SF_Service
format: light
level: deep
status: open
gaps: 3
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [integration]
---
# Enhanced Chat Custom Client & In-App SDK

**One line:** Two ways past the stock web widget — your own client over the Enhanced Chat REST API, or the Enhanced In-App Chat SDK inside an iOS or Android app.

**Reach for it when:** the web snippet will not do — a native app, or a chat UI you must own end to end.

## Key points

- **The deployment type decides the client:** Web gets the snippet, Mobile gets the In-App SDK, Custom Client gets the REST API → [which surfaces need one](embedded-service-deployments.md). The In-App SDKs are for native apps, not for Experience Cloud templates.
- **The Enhanced Chat API** is the old *Messaging for In-App and Web API*, GA since Winter '25, and it needs a **Custom Client** deployment. That deployment's Code Snippet panel gives the org ID, the deployment API name (`esDeveloperName`) and the SCRT URL.
- **Endpoints, by reference title:** access token (unauthenticated or authenticated), continuation token, create conversation, send message, send file, list conversations, list conversation entries, close conversation, end messaging session, retrieve transcript. Unauthenticated means an unverified guest; authenticated takes a user-verification JWT → [Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md).
- **Incoming traffic is Server-Sent Events:** `CONVERSATION_MESSAGE`, `CONVERSATION_ROUTING_RESULT`, `CONVERSATION_PARTICIPANT_CHANGED`, `CONVERSATION_QUEUE_POSITION`, `CONVERSATION_PROGRESS_INDICATOR` (an AI agent is working), `CONVERSATION_SESSION_STATUS_CHANGED` and more. Your client creates the conversation ID — a lowercase UUID in Salesforce's sample app 🚩.
- **The In-App SDK has two layers per platform:** the **UI SDK** (`SMIClientUI`; Android `messaging-inapp-ui`) is a ready chat screen, the **Core SDK** (`SMIClientCore`; `messaging-inapp-core`) is APIs with no UI. Both read the config file downloaded from the Mobile deployment — Service API URL, org ID, deployment API name.

```http
# Paths from Salesforce's sample app on GitHub 🚩 · {scrt} = SCRT URL from the Code Snippet panel
POST {scrt}/iamessage/api/v2/authorization/unauthenticated/access-token
     {"orgId":"00D…","esDeveloperName":"My_Client","capabilitiesVersion":"1","platform":"Web"}
     → accessToken (a JWT) + lastEventId
POST {scrt}/iamessage/api/v2/conversation            Authorization: Bearer <JWT>
     {"conversationId":"<uuid>","esDeveloperName":"My_Client","routingAttributes":{…}}
POST {scrt}/iamessage/api/v2/conversation/<uuid>/message
GET  {scrt}/eventrouter/v1/sse     headers: Authorization, X-Org-ID, Last-Event-ID
```

| | Enhanced In-App Chat SDK | Agentforce Mobile SDK |
|---|---|---|
| Packages | `SMIClientUI`, `SMIClientCore` (iOS); `messaging-inapp-ui`, `-core` (Android) | `AgentforceMobileSDK-iOS`, `-Android`; React Native `@salesforce/react-native-agentforce` |
| Talks to | an Enhanced Chat channel — reps, enhanced bots and agents, via Omni-Channel | an Agentforce agent — Service Agent or Employee Agent; full UI with voice and multimodal input, or headless |
| Setup | a Mobile Embedded Service deployment | Service Agent: an Enhanced Chat Mobile deployment; Employee Agent: OAuth through the Salesforce Mobile SDK |

## Gotchas

- **The Agentforce Mobile SDK is not the In-App SDK.** Its Service Agent mode reads `esDeveloperName` and `serviceApiURL` from the same Mobile deployment — one channel, two different SDKs, versioned separately → [RELEASE-RADAR · Agentforce platform](../RELEASE-RADAR/agentforce-platform.md).
- **Your client owns reconnection.** A dropped SSE connection is not re-established for you; reconnect with `Last-Event-ID`, and after a reload or in a second tab use the continuation token.
- **`CONVERSATION_CLOSE_CONVERSATION` fires only when the end user closes.** A rep ending the session arrives as a session-status change instead.

## Gaps to close

- [ ] What are the Enhanced Chat API's rate limits? Help's *Rate Limits for Enhanced Chat* page holds them.
- [ ] How long does an unauthenticated access token live, and does a continuation token extend it or replace it?
- [ ] Is there an 8 KB cap on a message payload? Only third-party write-ups 🚩 state it.

## Hands-on

- [ ] **SVC-CHAPI-01** · 30 min · On a Custom Client deployment, get an unauthenticated token, create a conversation, send one message and read the reply off the SSE stream with curl. **Proves:** the whole client is four calls you own — token, conversation, message, event stream. **Needs:** a Custom Client deployment, curl.
- [ ] **SVC-CHAPI-02** · 20 min · Drop the SSE connection mid-conversation, have the rep send two messages, then reconnect once without `Last-Event-ID` and once with it. **Proves:** nothing reconnects for you, and `Last-Event-ID` is what brings back the missed events.
- [ ] **SVC-CHAPI-03** · 15 min · Create a conversation with an upper-case UUID, then with a lower-case one. **Settles:** whether the API rejects the upper-case form — copy the error verbatim.
- [ ] **SVC-CHAPI-04** · 45 min · Run the In-App UI SDK sample against a Mobile deployment, then point an Agentforce Mobile SDK Service Agent at the same deployment. **Proves:** two SDKs on one channel, and what each one renders. **Needs:** Xcode or Android Studio, Agentforce.

## Related

- [Enhanced Chat Sessions & User Verification](enhanced-chat-sessions-and-user-verification.md) — the JWT behind the authenticated token, and how long a conversation lives
- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — where the deployment type is chosen, and why web or mobile cannot be changed later
- [Enhanced Chat](enhanced-chat.md) — the "In-App and Web" of the old name, and the channel both SDKs talk to
- [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) — v2 is a web client only, so it never replaces this note's two routes
- [RELEASE-RADAR · Agentforce platform](../RELEASE-RADAR/agentforce-platform.md) — the Agentforce Mobile SDK's three separately versioned packages
- [SF_core · 06-integration · 04 REST API fundamentals](../SF_core/06-integration-and-apis/04-rest-api-fundamentals.md) — the org's own REST API, which this one is not: a different host and a different token

## Sources

- [Configure a Custom Client Deployment for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_deployment_custom.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"create conversations that house messaging sessions, generate access tokens, and send messages and files"*
- [The Messaging for In-App and Web API Is Generally Available](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_rest_api.htm&language=en_US&release=252&type=5) — Salesforce release notes, Winter '25 · via search 2026-09-24
- [Enhanced Chat API Endpoints](https://developer.salesforce.com/docs/service/messaging-api/references) — Salesforce Developers · via search 2026-09-24 · the endpoint titles listed above
- [Get Started | Enhanced Chat API](https://developer.salesforce.com/docs/service/messaging-api/guide/get-started.html) — Salesforce Developers · via search 2026-09-24 · `esDeveloperName`; JWT for verified users
- [Authorization | Enhanced Chat API](https://developer.salesforce.com/docs/service/messaging-api/guide/authorization.html) — Salesforce Developers · via search 2026-09-24 · authenticated and unauthenticated users; `Authorization: Bearer`
- [Server-Sent Events | Enhanced Chat API Reference](https://developer.salesforce.com/docs/service/messaging-api/references/about/server-sent-events.html) — Salesforce Developers · via search 2026-09-24 · event types; `Last-Event-Id`; custom clients must re-establish dropped connections
- [Server-Sent Events Structure](https://developer.salesforce.com/docs/service/messaging-api/references/about/server-sent-events-structure.html) — Salesforce Developers · via search 2026-09-24 · close-conversation event vs session-status event
- [Get Started | Enhanced In-App Chat](https://developer.salesforce.com/docs/service/messaging-in-app/guide/introduction.html) — Salesforce Developers · via search 2026-09-24 · UI SDK vs Core SDK; config file contents
- [Install the SDK (iOS)](https://developer.salesforce.com/docs/service/messaging-in-app/guide/ios-installation.html) and [Install the SDK (Android)](https://developer.salesforce.com/docs/service/messaging-in-app/guide/android-installation.html) — Salesforce Developers · via search 2026-09-24 · `Messaging-InApp-UI` / `-Core` pods; `com.salesforce.service:messaging-inapp-core`
- [Considerations and Limitations for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · In-App SDKs *"not intended to be used with Experience Cloud templates"*
- [Before You Begin | Agentforce Mobile SDK](https://developer.salesforce.com/docs/ai/agentforce-mobile-sdk/guide/agentforce-mobile-sdk-before-you-begin.html) — Salesforce Developers · via search 2026-09-24 · Service Agent needs Enhanced Chat and a Mobile deployment; `esDeveloperName`, `serviceApiURL`
- [Agentforce APIs and SDKs](https://developer.salesforce.com/docs/ai/agentforce/guide/get-started-agents.html) — Salesforce Developers · via search 2026-09-24 · Employee vs Service Agent; full UI with voice and multimodal input, or headless
- [messaging-web-api-sample-app](https://github.com/Salesforce-Async-Messaging/messaging-web-api-sample-app) — Salesforce-Async-Messaging on GitHub, third party 🚩 · read 2026-09-24 · `src/services/messagingService.js` and `eventSourceService.js`: the paths, headers and request bodies in the code block
- [Salesforce Enhanced Chat API — Send Message to a Conversation](https://levelup.gitconnected.com/salesforce-enhanced-chat-api-send-message-to-a-conversation-f97a77fa1443) — Level Up Coding, third party 🚩 · via search 2026-09-24 · the 8 KB payload and lowercase-UUID claims

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; new ground beyond SF_Experience_Cloud · 19, which only covers the web widget
