---
vault: SF_Service
format: light
level: deep
status: open
gaps: 3
org_checks: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [security]
---
# Enhanced Chat Sessions & User Verification

**One line:** A conversation outlives its sessions, and user verification is what ties it to a known person — a JWT your server signs, checked against a keyset in Setup.

**Reach for it when:** history must follow a logged-in customer across devices, or sessions are stuck, piling up or ending too soon.

## Key points

| Status | Means — each `MessagingSession` is one routed stint of a longer conversation |
|---|---|
| New | a rep sent an opening message (rep-initiated session) |
| Waiting | being routed or transferred — or rep-initiated and waiting for the customer (expires unanswered after 48 hours on an enhanced channel 🚩) |
| Active | a rep, bot or agent accepted it, or the customer answered an outbound session |
| Inactive | the customer stopped replying before the issue was solved; the rep's capacity is freed |
| Paused | parked by status-based capacity in Enhanced Omni-Channel |
| Consent | a consent exchange, so a routing flow can exclude it |
| Ended | closed by a rep or by the inactivity timer; an automated notification is created Ended |

- **Inactive is set by the rep** (**Mark Inactive** beside **End Chat**) **or by a customer-inactivity time limit** on the channel, and turns Ended after about 30 hours. With tab-based capacity, a customer reply turns it back to Waiting and reroutes it to the next free rep.
- **Unverified history is short-lived:** on the web it shows for up to 6 hours; in-app it is lost on uninstall or a cleared cache, and never moves device. **Verified history persists**, on every device where the same user is verified.
- **Token-based setup, three steps:** (1) Setup → **User Verification** — upload JSON Web Keys or give a JWKS endpoint, and make a keyset; (2) Messaging Settings → the channel — turn verification on, set token expiry, add the keyset; (3) the client sends the JWT, on the web with `embeddedservice_bootstrap.userVerificationAPI.setIdentityToken` after `onEmbeddedMessagingReady`.
- **The JWT:** RS256 or RS512, RSA key of 2048 bits or more, the JWK's `n` and `e` Base64URL-encoded. The `sub` claim lands in `MessagingEndUser.MessagingPlatformKey`, e.g. `v2/iamessage/AUTH/{auth_id_info}/uid:user-123`.
- **Token lifetimes:** *Authorization Token Expiration Time for Verified Users* defaults to 60 minutes. When both tokens expire the client fires `onEmbeddedMessagingIdentityTokenExpired`; send a fresh token within 30 seconds to keep the session.
- **Where token-based verification works:** an external website, and three Aura templates — Build Your Own (Aura), Help Center, Customer Service. Help says it is *"not supported on other Experience Cloud or Commerce Cloud sites"*; a second route, **credential-based** verification, uses the login on a Salesforce site.
- **The messages are not in your org:** enhanced conversation entries live off-platform (AWS), outside SOQL and standard reports. Read them through the Conversation Data GET API or the Conversation Entries Connect REST API (one conversation at a time, own hourly limit), or sync to Data 360 for bulk.

## Gotchas

- **Automation on the session objects can stop sessions ending.** A trigger or required field on `MessagingSession` or `MessagingEndUser` fails the update; the reason lands in the session's **Error Reason** field (Help 005132462).
- **Call `clearSession` on logout.** It clears messaging and user data from every tab and window.
- **Subdomain session continuity breaks where third-party storage is blocked:** Chrome incognito, Edge balanced tracking prevention, Firefox's default, and iOS WebKit partitioning.

## Gaps to close

- [ ] Which site templates does credential-based verification support — does it cover LWR, where token-based does not?
- [ ] Which JWT claims are mandatory besides `sub`, and how is `iss` matched to a keyset?
- [ ] What range does the customer-inactivity time limit accept, and where on the channel page is it set?

## Confirm in org

- 🚩 Can token-based verification be switched on for a deployment placed on a Build Your Own (LWR) site at all? — the channel's user-verification setting, then the site's Enhanced Chat component.
- 🚩 Does a verified customer's `MessagingEndUser.ContactId` fill with no linking flow in place? — query `MessagingEndUser` after a verified chat.

## Hands-on

- [ ] **SVC-CHVER-01** · 15 min · Chat unverified in one browser, then open the same page in a second browser. **Proves:** unverified history lives in one browser's storage — nothing crosses devices.
- [ ] **SVC-CHVER-02** · 45 min · Make a 2048-bit RSA key pair, publish its JWK as a keyset, sign a JWT with a `sub`, pass it with `setIdentityToken`, then chat from two browsers. **Proves:** one `sub` sees one history everywhere, and it appears in `MessagingPlatformKey`. **Needs:** an external web page, Node or OpenSSL.
- [ ] **SVC-CHVER-03** · 20 min · Sign the same JWT with HS256, then with a 1024-bit RSA key, and pass each one. **Proves:** only RS256/RS512 with 2048-bit keys verify — copy each failure verbatim.
- [ ] **SVC-CHVER-04** · 15 min · Add a validation rule on `MessagingSession` that blocks Status = Ended, then click **End Chat**. **Proves:** automation on the session object can stop sessions ending — find what **Error Reason** records.

## Related

- [Enhanced Chat Setup Chain](enhanced-chat-setup-chain.md) — the channel page where verification, the keyset and token expiry are switched on
- [Enhanced Chat Custom Client & In-App SDK](enhanced-chat-custom-client-and-mobile-sdk.md) — the authenticated access-token endpoint, and verification inside a mobile app
- [Enhanced Chat v1 vs v2](enhanced-chat-v1-vs-v2.md) — whether v2 supports verification on the same terms is still an open question there
- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — tab-based vs status-based capacity, which decides how Inactive and Paused behave
- [Enhanced Chat](enhanced-chat.md) — why legacy Chat had no conversations to persist in the first place
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the unverified case on a public site: the guest user, and why that is the risky one
- [SF_core · 06-integration · 15 OAuth flows & authorization](../SF_core/06-integration-and-apis/15-oauth-flows-and-authorization.md) — JWTs and signing keys in the platform's own flows; this JWT is yours, not an OAuth token

## Sources

- [Lifecycle of a Messaging Session](https://help.salesforce.com/s/articleView?id=service.messaging_life_cycle.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · New, Waiting, Active, Inactive, Ended, Paused, Consent; Inactive → Ended about 30 hours
- [Ending or Inactivating Messaging Sessions Automatically](https://help.salesforce.com/s/articleView?language=en_US&id=service.messaging_auto_end.htm&type=5) — Salesforce Help · via search 2026-09-24 · inactivity time limit; tab-based capacity reroutes on reply
- [Automated Session Expiry and Inactivity Handling for Enhanced Channels](https://help.salesforce.com/s/articleView?id=service.messaging_auto_session_expiry_enhanced.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"24 hours for a standard channel or 48 hours for an enhanced channel"*
- [Inactive Messaging Sessions Not Ending After 24–30 Hours](https://help.salesforce.com/s/articleView?id=005132462&language=en_US&type=1) — Salesforce Help 005132462 · via search 2026-09-24 · triggers or required fields; Error Reason field
- [Verify Your End User and Share Messaging History](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/verify-end-user-share-msg-history) — Trailhead · read 2026-09-24 · the three setup steps; 6 hours on the web; in-app loss on uninstall
- [Message with a Customer](https://trailhead.salesforce.com/content/learn/modules/messaging-optimization-for-in-app-and-web/message-with-a-customer) — Trailhead · read 2026-09-24 · Customer Inactive, End Chat
- [Understanding Token-Based User Verification](https://help.salesforce.com/s/articleView?id=service.user_verification_overview.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · JWK upload or endpoint; 2048-bit minimum; `n` and `e` Base64URL
- [User Verification | Enhanced Web Chat](https://developer.salesforce.com/docs/service/messaging-web/guide/user-verification.html) — Salesforce Developers · via search 2026-09-24 · RS256/RS512; `setIdentityToken`; `onEmbeddedMessagingIdentityTokenExpired` and the 30-second window; `clearSession`; `sub` → Messaging Platform Key; 60-minute default
- [Set Up Credential-Based User Verification](https://help.salesforce.com/s/articleView?id=service.miaw_credential_user_verification_setup.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · token-based or credential-based on a Salesforce site
- [Considerations and Limitations for Enhanced Chat](https://help.salesforce.com/s/articleView?id=service.miaw_considerations_and_limitations.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"User verification is supported on an external website and on some Aura sites … It's not supported on other Experience Cloud or Commerce Cloud sites"*
- [Settings | Enhanced Web Chat Reference](https://developer.salesforce.com/docs/service/messaging-web/references/m4w-reference/settingsAPI.html) — Salesforce Developers · via search 2026-09-24 · browsers that block subdomain session continuity
- [Store and Access Your Conversation Data](https://help.salesforce.com/s/articleView?language=en_US&id=service.conversation_transcript_access.htm&type=5) — Salesforce Help · via search 2026-09-24 · Core storage or AWS by channel; the two APIs; Connect API not for bulk
- [Access Conversation Data](https://developer.salesforce.com/docs/service/messaging-object-model/guide/messaging-object-model-access-data.html) — Salesforce Developers · via search 2026-09-24 · off-platform entries not available through SOQL; ConversationEntry (Off-Core) schema
- [Identify Customers with Individual-Object Linking](https://help.salesforce.com/s/articleView?id=service.support_individual_object_linking_intro.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Search Individual flow action and linking templates

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; new ground beyond SF_Experience_Cloud · 19, which keeps the guest-user side of an unverified chat
