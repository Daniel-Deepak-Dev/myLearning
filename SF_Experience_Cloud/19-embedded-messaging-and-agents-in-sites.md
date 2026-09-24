---
vault: SF_Experience_Cloud
format: dense
status: learning
gaps: 1
created: 2026-08-04
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
phase: 19
tags: [currency-new, currency-warning]
---
# Embedded Messaging & Agents in Sites

**Scope:** Putting a chat channel — human-routed messaging or an **Agentforce agent** — on a site, and why an agent on a *public* site is the highest-risk surface on the platform. The agent itself is built in [SF_Agentforce/](../SF_Agentforce/INDEX.md); an agent is also **a new line item on the exposure audit**, [11](11-public-site-exposure-audit.md).

> **What changed.** Legacy **Chat / Live Agent was retired on 14 February 2026**, and its replacement *Messaging for In-App and Web* was **renamed Enhanced Chat in June 2025**. The product, the rename and the v2 client are now owned by [SF_Service · Enhanced Chat](../SF_Service/enhanced-chat.md); this note keeps only what a **site** does to it.

## Core idea

The delivery mechanism is **Enhanced Chat** (formerly Messaging for In-App and Web): you create a **Messaging Channel**, wrap it in an **Embedded Service Deployment**, and drop the **Embedded Messaging** component onto site pages in Experience Builder. That same channel can route to a human via Omni-Channel or to an **Agentforce Service Agent** — the site doesn't care which; it's a routing decision behind the channel. This is the seam where Experience Cloud meets Agentforce, and it is dangerous by construction: on a public site the agent faces **unauthenticated input, its agent user's data reach, and a reasoning engine** at once. That combination is why the **Einstein Trust Layer** and tight action-scoping aren't optional — they're the only thing between a public visitor and your data and prompt.

## How it works

- **The site's step is the last one.** The channel and its **Embedded Service Deployment** are built in Service Setup → [SF_Service · setup chain](../SF_Service/enhanced-chat-setup-chain.md). The site's part is dragging the **Embedded Messaging** component into the **Template Footer** in Experience Builder — drag and drop is the only supported method — then publishing the site. Every step in order, Service side included → [25](25-enhanced-chat-on-a-site-step-by-step.md).
- **Routing happens behind the channel**, in an Omni-Channel flow — to a queue or an **Agentforce Service Agent**. Nothing on the site changes when routing does → [SF_Service · handoff](../SF_Service/bot-and-agent-to-human-handoff.md).
- **Agent user, not guest user:** a Service Agent that cannot use the visitor's user record acts as its own **agent user** — the *EinsteinServiceAgent User* in Trailhead. Its data reach is that user's permission sets and role; the guest user only gates the site's pages, [07](07-guest-user-security-model.md).
- **Trust Layer** governs every turn — masking, toxicity, grounding, audit. Cross-link, don't restate: [SF_Agentforce · Einstein Trust Layer](../SF_Agentforce/INDEX.md).

## 2026 currency

Deploying an Agentforce Service Agent to a site is now a channel-configuration exercise rather than custom code — the native Embedded Messaging component handles the widget. That lowers the effort and *raises* the stakes: a public agent is trivial to ship and non-trivial to secure. Agent platform detail: [RELEASE-RADAR/agentforce-platform.md](../RELEASE-RADAR/agentforce-platform.md).

## Gotchas

- **A public agent does not run as the guest user.** Every action and grounding query is bounded by its **agent user** — scope that user's permission sets *and* the agent's actions, and treat the input as hostile, [11](11-public-site-exposure-audit.md). A locked-down guest profile protects nothing the agent user can reach.
- **Prompt injection is an open door on a public site.** Unauthenticated free-text into a reasoning engine — Trust Layer and action allow-lists are mandatory, not optional.
- **Agent actions inherit the running context.** An over-broad action exposed to a guest agent is a data-exfiltration path, not a convenience.
- **The retirement, the rename and the escalation design are not site problems.** Legacy Chat's end date, *Enhanced Chat* vs *Messaging for In-App and Web*, and why a handoff drops context all live in [SF_Service/](../SF_Service/INDEX.md). A site cannot fix any of them.
- **The Trailhead's site chat adds two allowlists, pointing opposite ways.** The deployment's `scrt2URL` goes in **Trusted URLs** with CSP context *Experience Builder Sites*. It also adds the site URL to **CORS** — 🚩 no Salesforce source says Enhanced Chat needs that entry, so it is an open org check → [SF_core · CORS](../SF_core/06-integration-and-apis/28-cors-allowlist.md), [· Trusted URLs](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md).
- **Consumption billing.** Agent turns consume Flex/agent credits — a public agent's cost scales with traffic, not with resolved cases.

## Recall

Q: What is the deployment chain for putting a chat or agent on a site?
A: An Enhanced Chat **Messaging Channel** → a **Web** Embedded Service Deployment, published → the **Embedded Messaging** component in the Template Footer in Experience Builder → publish the site.

Q: Can Enhanced Chat verify a logged-in member on a Build Your Own (LWR) site with a token?
A: Not per Help. Token-based user verification is supported on an external website and three **Aura** templates only — Build Your Own (Aura), Help Center, Customer Service. On any other site the chat is unverified.

Q: Why is an agent on a public site the highest-risk deployment surface?
A: It combines unauthenticated input, the agent user's data reach, and a reasoning engine — so prompt injection and over-broad actions can exfiltrate data.

Q: As which user does a Service Agent on a public site read and act?
A: Its own agent user (the EinsteinServiceAgent user), not the guest user — that user's permission sets bound every action, so scope them and the agent's actions tightly.

Q: Where does an embedded agent belong on the exposure audit?
A: It's a new line item on the public-site exposure audit ([11](11-public-site-exposure-audit.md)) — not a separate subject — plus the Trust Layer controls.

## Gaps to close

- [ ] When a site member is signed in or verified, does a Service Agent act as that member's user record instead of the agent user? Help's wording — *"when a Service agent can't use an end user's user record"* — implies it sometimes can; only a third-party page says when 🚩.

## Related

- [25 · Enhanced Chat on a site, step by step](25-enhanced-chat-on-a-site-step-by-step.md) — the runbook: every step from the channel to the guest test, and where LWR and Aura differ
- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — an embedded agent is a new item on that audit
- [SF_Agentforce · Einstein Trust Layer](../SF_Agentforce/INDEX.md) — the guardrails a public agent depends on
- [SF_Agentforce/](../SF_Agentforce/INDEX.md) — where the agent, its actions and topics are built
- [SF_Service · Enhanced Chat](../SF_Service/enhanced-chat.md) — the product behind the widget: the MIAW rename, the legacy Chat retirement, and what a conversation is
- [SF_Service · Enhanced Chat setup chain](../SF_Service/enhanced-chat-setup-chain.md) — the channel and deployment that must exist before the Experience Builder component has anything to show
- [SF_Service · Enhanced Chat v1 vs v2](../SF_Service/enhanced-chat-v1-vs-v2.md) — the v2 client a site's Service Agent now ships in, and why v1 and v2 must never share the site's domain
- [SF_Service · Sessions & user verification](../SF_Service/enhanced-chat-sessions-and-user-verification.md) — which site templates can verify a logged-in member, and what an unverified guest conversation keeps
- [SF_Service · Embedded Service deployments](../SF_Service/embedded-service-deployments.md) — whether a site needs a deployment at all, what one holds, and how to tell a legacy Embedded Service Chat snippet from an Enhanced Chat one
- [SF_core · 06-integration · 28 CORS allowlist](../SF_core/06-integration-and-apis/28-cors-allowlist.md) — the CORS entry the Trailhead adds for the site URL, and the open question of whether chat needs it at all
- [SF_core · 07-security · 27 Trusted URLs & CSP](../SF_core/07-security-and-sharing/27-trusted-urls-and-csp.md) — why `scrt2URL` needs a Trusted URL in the Experience Builder Sites context
- [SF_Service · Bot & agent to human handoff](../SF_Service/bot-and-agent-to-human-handoff.md) — the routing behind the channel, and why an unplanned escalation loses the thread

## Sources

- [Configure Service Agent Access](https://help.salesforce.com/s/articleView?language=en_US&id=ai.agent_user.htm&type=5) — Salesforce Help · via search 2026-09-24 · *"When a Service agent can't use an end user's user record to control access, it uses a dedicated user record … called the agent user"*; object access through its permission set; a role for record access
- [Give Your Agent More Information with Flows, Actions, and Permissions](https://trailhead.salesforce.com/content/learn/modules/programmatic-instructions-in-agentforce/give-your-agent-more-information-with-flows-actions-and-permissions) — Trailhead · read 2026-09-24 · field access granted to the **EinsteinServiceAgent User** through *Service Agent Permissions*
- [Agentforce Permissions Explained](https://www.salesforceben.com/agentforce-permissions-explained-agent-users-access-and-security/) — Salesforce Ben, third party 🚩 · via search 2026-09-24 · says the agent runs as itself, but as the logged-in user on authenticated sessions — unconfirmed by Help

## History

- 2026-09-24 · corrected: a Service Agent on a public site acts as its agent user, not the guest user — Core idea, How it works, Gotchas and Recall; linked the new step-by-step note 25
