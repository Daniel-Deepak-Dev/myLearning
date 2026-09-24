---
vault: SF_Service
format: light
level: working
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Bot & Agent to Human Handoff

**One line:** Two Omni-Channel flows bracket every AI conversation — an inbound one routes it to the agent, an outbound one routes it from the agent to a rep.

**Reach for it when:** a customer must move from an Agentforce Service Agent or an enhanced bot to a person without repeating themselves.

## Key points

- **In:** the channel's inbound Omni-Channel flow uses Route Work → **Agentforce Service Agent** (or **Bot** for an enhanced Einstein bot), plus a fallback queue for when the agent can't take it → [Omni-Channel flows](omni-channel-flows.md).
- **One channel, one agent.** An agent can serve many inbound channels, but an inbound channel connects to only one agent. The agent itself is built in [SF_Agentforce](../SF_Agentforce/INDEX.md).
- **Out:** an **outbound** Omni-Channel flow, chosen in the agent's **Messaging** connection → Escalations → **Escalation Flow**. The agent's **Escalation** subagent runs it. An enhanced bot uses a **Default Outbound Omni-Channel Flow** instead.
- **The escalation message** goes out before the transfer. It has an editable default and is auto-translated to the customer's language.
- **Context survives because it is one conversation.** The same `MessagingSession` continues, and Help says the history *"including messages and information gathered"* moves to the destination. The rep reads the transcript.
- **The record shows who handled it.** `MessagingSession.AgentType` reads `Bot`, `Agent` or `BotToAgent`. `AgentWork.BotType` separates `Bot` (Einstein bot) from `ExternalCopilot` (an AI agent), API 63.0+.
- **A failed transfer is not a dead end.** If the transfer doesn't complete, the agent carries on with the context it had. It tries the Escalation subagent **once per session**.
- **Check before promising a person.** Put **Check Availability for Routing** in the outbound flow; if no rep is free the flow ends and the agent keeps the conversation. The agent can also call the **Check Rep Availability for Routing** action itself.
- **Measure the gap.** The `ServiceRepFirstResponseTime` session metric (API 67.0) times the wait from routing to a human to the rep's first reply.

## Gotchas

- **"Escalation loses context" really means "escalation was never wired".** The transcript rides on the session. What breaks is a missing Escalation Flow, an outbound flow that ends without Route Work, or a second request after a failed transfer.
- **The transcript is not a form.** A rep should not have to read 40 messages to find an order number. Have an action write key facts to `MessagingSession` or `Case` fields before escalating 🚩 (design practice, not a documented requirement).
- **There is no channel-level "we're closed" switch.** `MessagingChannel.OutsideBusinessHoursResponse` is *"Reserved for future use"* in the object reference. Out-of-hours behaviour has to be built in the outbound flow or the agent.
- **A public site runs the agent as the guest user,** so a site handoff also inherits guest-user limits → [SF_Experience_Cloud · 19](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md).
- **Voice escalation is configured separately,** in the agent's call routing and escalation settings, and has telephony prerequisites of its own → [RELEASE-RADAR](../RELEASE-RADAR/agentforce-platform.md) 🚩.

## Gaps to close

- [ ] On escalation, is a new `PendingServiceRouting` and `AgentWork` created against the same `MessagingSession`, and what does `AgentWork.IsTransfer` show?
- [ ] Is there a declarative business-hours check for an outbound Omni-Channel flow, or does it need invocable Apex over `BusinessHours.isWithin`?
- [ ] Do the agent's context variables reach the rep as fields, or only as transcript text?

## Confirm in org

- 🚩 With the Escalation Flow field left empty, what does the agent say when a customer asks for a human? — Agentforce Builder → Explorer panel → the Messaging connection → Escalations, then a test chat.

## Hands-on

- [ ] **SVC-HAND-01** · 30 min · Route an Enhanced Chat channel to a Service Agent, wire an outbound flow to a queue, then ask for a human. **Proves:** the rep gets the same `MessagingSession` with the full transcript, and `AgentType` reads `BotToAgent`. **Needs:** Agentforce Service Agent, second rep user.
- [ ] **SVC-HAND-02** · 20 min · Set every rep Offline, ask for a human, then ask again. **Proves:** the failed transfer leaves the agent in charge with its context, and the second request is not re-attempted. **Needs:** Agentforce Service Agent.
- [ ] **SVC-HAND-03** · 15 min · Clear the Escalation Flow field and ask for a human. **Settles:** the Confirm in org question — copy the agent's reply verbatim. **Needs:** Agentforce Service Agent.
- [ ] **SVC-HAND-04** · 25 min · Add Check Availability for Routing to the outbound flow and route only when reps are online. **Proves:** the flow, not the agent, decides whether a handoff can happen. **Needs:** Agentforce Service Agent, second rep user.

## Related

- [Omni-Channel Flows](omni-channel-flows.md) — Route Work, fallback queues and Check Availability for Routing, which both handoff flows are made of
- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — why "no rep available" can mean no capacity, not nobody online
- [Enhanced Chat](enhanced-chat.md) — the channel most handoffs run on
- [Omni Supervisor](omni-supervisor.md) — where a supervisor sees the escalated conversation land and can step in
- [SF_Agentforce · INDEX](../SF_Agentforce/INDEX.md) — where the Service Agent, its subagents and actions are built
- [SF_Experience_Cloud · 19 Embedded messaging & agents in sites](../SF_Experience_Cloud/19-embedded-messaging-and-agents-in-sites.md) — the site-side half: the widget, the guest user, and the exposure audit
- [SF_core · 04-flow · 23 Flows as Agentforce actions](../SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) — the other way a flow meets an agent: as an action it calls, not a route around it
- [RELEASE-RADAR · Agentforce platform](../RELEASE-RADAR/agentforce-platform.md) — Voice, Contact Center and their escalation prerequisites

## Sources

- [Transfer Conversations from an Agent with an Omni-Channel Flow](https://help.salesforce.com/s/articleView?language=en_US&id=ai.service_agent_escalation.htm&type=5) — Salesforce Help · via search 2026-09-24 · Escalation Flow field; escalation message auto-translated; *"conversation history, including messages and information gathered, is also transferred"*; *"only once per session"*
- [Route to an Agentforce Service Agent](https://help.salesforce.com/s/articleView?id=service.omnichannel_route_to_ai_agent_target.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · one inbound channel per agent; fallback messaging queue
- [Connect a Service Agent to Other Messaging Channels](https://help.salesforce.com/s/articleView?id=ai.service_agent_messaging.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Route Work Items to an Enhanced Bot](https://help.salesforce.com/s/articleView?id=service.omnichannel_route_to_bot.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Specify a Default Outbound Omni-Channel Flow](https://help.salesforce.com/s/articleView?id=service.bots_service_enhanced_route_from_default.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the enhanced-bot handoff
- [Create a Sample Outbound Flow and Handle Routing for Agentforce Service Agents](https://developer.salesforce.com/docs/service/messaging-byoc-ccaas/guide/create-agentforce-service-agent.html) — Salesforce Developers · via search 2026-09-24 · the flow checks availability; if no rep, *"the flow ends and the agent continues the conversation session"*
- [Service | Check Rep Availability for Routing](https://help.salesforce.com/s/articleView?id=ai.copilot_actions_ref_check_availability_for_routing.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · the agent-side action
- [Configure Call Routing and Call Escalation for the Agent](https://help.salesforce.com/s/articleView?id=ai.agent_call_routing_escalation.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · voice escalation is its own setup
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `MessagingSession.AgentType`, `AgentWork.BotType` (API 63.0), the `ServiceRepFirstResponseTime` metric type (API 67.0), `MessagingChannel.OutsideBusinessHoursResponse` *"Reserved for future use"*
- [Optimize Call Routing with Omni-Channel Flows for Voice](https://trailhead.salesforce.com/content/learn/modules/ai-integration-for-agentforce-contact-center/manage-inbound-call-routing) — Trailhead · read 2026-09-24 · Route To *Agentforce Service Agent* for calls, then hand off to a rep

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; takes over the escalation gotcha from SF_Experience_Cloud · 19
