# Embedded Messaging & Agents in Sites 🆕

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Putting a chat channel — human-routed messaging or an **Agentforce agent** — on a site, and why an agent on a *public* site is the highest-risk surface on the platform. The agent itself is built in [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md); an agent is also **a new line item on the exposure audit**, [11](11-public-site-exposure-audit.md).

## Core idea

The delivery mechanism is **Messaging for In-App and Web**: you create a **Messaging Channel**, wrap it in an **Embedded Service Deployment**, and drop the **Embedded Messaging** component onto site pages in Experience Builder. That same channel can route to a human via Omni-Channel or to an **Agentforce Service Agent** — the site doesn't care which; it's a routing decision behind the channel. This is the seam where Experience Cloud meets Agentforce, and it is dangerous by construction: on a public site the agent faces **unauthenticated input, guest-user data context, and a reasoning engine** at once. That combination is why the **Einstein Trust Layer** and tight action-scoping aren't optional — they're the only thing between a public visitor and your data and prompt.

## How it works

- **Setup chain:** Messaging Settings → **New Channel** (In-App and Web) → **Embedded Service Deployment** → add the **Embedded Messaging** component in Experience Builder → publish.
- **Routing:** the channel links to Omni-Channel; route to a queue (human) or an **Agentforce Service Agent**. Escalation agent→human is routing configuration, not a rebuild.
- **Guest context:** on a public site the conversation runs as the **guest user** — the agent's data reach is exactly the guest's sharing, [07](07-guest-user-security-model.md).
- **Trust Layer** governs every turn — masking, toxicity, grounding, audit. Cross-link, don't restate: [AI_Data · Einstein Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md).

## 2026 currency

Deploying an Agentforce Service Agent to a site is now a channel-configuration exercise rather than custom code — the native Embedded Messaging component handles the widget. That lowers the effort and *raises* the stakes: a public agent is trivial to ship and non-trivial to secure. Agent platform detail: [AI_Data/05-release-radar/agentforce-platform.md](../../AI_Data/05-release-radar/agentforce-platform.md).

## Gotchas

- **A public agent runs as the guest user.** Every action and grounding query is bounded by guest sharing — scope the guest profile *and* the agent's actions, and treat the input as hostile, [11](11-public-site-exposure-audit.md).
- **Prompt injection is an open door on a public site.** Unauthenticated free-text into a reasoning engine — Trust Layer and action allow-lists are mandatory, not optional.
- **Agent actions inherit the running context.** An over-broad action exposed to a guest agent is a data-exfiltration path, not a convenience.
- **Escalation loses context if unplanned** — handing off to a human without transcript/routing config drops the thread.
- **Messaging ≠ legacy Chat/Live Agent.** Building on the retired chat product is a dead end; use Messaging for In-App and Web.
- **Consumption billing.** Agent turns consume Flex/agent credits — a public agent's cost scales with traffic, not with resolved cases.

## Recall

Q: What is the deployment chain for putting a chat or agent on a site?
A: Messaging Channel (In-App and Web) → Embedded Service Deployment → Embedded Messaging component in Experience Builder → publish.

Q: How does the site know whether a conversation goes to a human or an agent?
A: It doesn't — the channel routes via Omni-Channel to a queue or an Agentforce Service Agent; routing is configured behind the channel.

Q: Why is an agent on a public site the highest-risk deployment surface?
A: It combines unauthenticated input, guest-user data context, and a reasoning engine — so prompt injection and over-broad actions can exfiltrate data.

Q: As which user does a public-site agent operate, and what does that bound?
A: The guest user — its data reach and every action are limited to guest sharing, so the guest profile and agent actions must both be tightly scoped.

Q: Where does an embedded agent belong on the exposure audit?
A: It's a new line item on the public-site exposure audit ([11](11-public-site-exposure-audit.md)) — not a separate subject — plus the Trust Layer controls.

## Related

- [11 · Public site exposure audit](11-public-site-exposure-audit.md) — an embedded agent is a new item on that audit
- [AI_Data · Einstein Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md) — the guardrails a public agent depends on
- [AI_Data/02-salesforce-ai/](../../AI_Data/02-salesforce-ai/INDEX.md) — where the agent, its actions and topics are built
