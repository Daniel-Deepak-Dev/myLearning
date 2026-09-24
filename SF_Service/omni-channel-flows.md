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
# Omni-Channel Flows

**One line:** A flow type that routes one work item with logic — to a queue, a rep, skills, a bot or an Agentforce agent — instead of the queue's fixed routing configuration.

**Reach for it when:** the right destination depends on the record, the pre-chat answers or who is online right now.

## Key points

- **Omni-Channel Flow is its own flow type** in Flow Builder. Help calls it the unified routing setup for voice calls, chats, messaging sessions, cases, leads and custom objects.
- **Two documented inputs,** both **Available for input:** `recordId` (Text) receives the work item's Id. `input_record` (Record, of the object) is for routing on field values.
- **Route Work** is the action that routes. You set the **Service Channel**, a **Route To** target — Queue, a rep, Skills, Bot or Agentforce Service Agent — and a **Fallback Queue ID**. Older Help pages label the rep option *Agent*.
- **The fallback queue is the safety net.** It gets the work when the target can't accept it, and when the flow itself throws an exception.
- **Check Availability for Routing** returns an estimated wait time and a count of reps online. Put it before Route Work and branch on it.
- **Skills can be set per item.** Route To Skills takes skills and levels. That is why a rep should reassign to a flow, not a skill: **Reassign** to a skill sets every level to 0.
- **Real-time channels launch the flow themselves** (outline below — not metadata). A messaging channel with **Routing Type = Omni-Flow** names the flow and a fallback queue; a voice channel does the same in its **Omni-Channel Routing** section.
- **Pre-chat values arrive as flow variables.** On the channel, **Parameter Mapping** pairs a pre-chat field with a flow variable name; save values to the MessagingSession with Update Records if the rep needs them. The form itself → [Enhanced Chat setup chain](enhanced-chat-setup-chain.md).
- **Records do not launch it.** A Case, Lead or custom object reaches an Omni-Channel flow as a **subflow of a record-triggered flow**, or through the Email-to-Case routing setting.

```
  recordId   Text, Available for input      ← MessagingSession Id
  Tier       Text, Available for input      ← pre-chat, via Parameter Mapping
  Check Availability for Routing   (Service Channel = Messaging, queue = VIP)
  Decision   Tier = "Gold" and reps online > 0 ?
    yes → Route Work   Queue = VIP,     Fallback Queue = General
    no  → Route Work   Agentforce Service Agent,  Fallback Queue = General
```

## Gotchas

- **The receiving variable must match twice:** its API name equals the mapping's **Flow Variable Name** exactly, and its type is Text, because every pre-chat value arrives as a string → [setup chain](enhanced-chat-setup-chain.md).
- **An inactive agent is invisible.** If the agent is not listed under Route To, activate it and refresh Flow Builder.
- **A fallback queue with no members still accepts the work.** It then waits where nobody sees it → [SF_core · 07 · 08](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md).

## Gaps to close

- [ ] What are the exact output variable API names of Check Availability for Routing, and does "online" include reps already at full capacity?
- [ ] If a case owned by an Omni queue is also sent through an Omni-Channel flow, which routing wins?
- [ ] Which routing fields can Route Work set per item — routing priority, `TargetAcceptDateTime` — rather than inherit from a routing configuration?

## Confirm in org

- 🚩 What happens when a Parameter Mapping name does not match any flow variable — silent blank, or a routing error? — Messaging Settings → channel → Parameter Mapping, then a test chat.

## Hands-on

- [ ] **SVC-OFLOW-01** · 30 min · Build an Omni-Channel flow that reads `recordId`, set a messaging channel's Routing Type to Omni-Flow, then start a chat. **Proves:** the channel launches the flow, and `recordId` holds the MessagingSession Id. **Needs:** second rep user.
- [ ] **SVC-OFLOW-02** · 20 min · Rename the flow variable so it no longer matches its Parameter Mapping, then submit pre-chat. **Settles:** the mismatch behaviour in Confirm in org — copy the result verbatim.
- [ ] **SVC-OFLOW-03** · 20 min · Add a fault on purpose before Route Work, such as a Get Records on a malformed Id. **Proves:** a flow exception sends the conversation to the fallback queue, not to nowhere.
- [ ] **SVC-OFLOW-04** · 25 min · Call the Omni-Channel flow as a subflow from a record-triggered flow on new cases. **Proves:** a record enters Omni-Channel flow routing only through a parent flow. **Needs:** second rep user.

## Related

- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — the four routing types Route Work chooses between, and the capacity rules it still obeys
- [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) — the inbound flow that reaches an agent, and the outbound flow that leaves it
- [Enhanced Chat setup chain](enhanced-chat-setup-chain.md) — the channel and pre-chat form whose values this flow receives
- [SF_core · 04-flow · 01 Automation landscape & tool selection](../SF_core/04-flow-and-automation/01-automation-landscape-and-tool-selection.md) — the flow-type table that Omni-Channel Flow is missing from
- [SF_core · 07-security · 08 Groups, queues & the grantee model](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — the memberless-queue trap a fallback queue can fall into

## Sources

- [Advanced Routing with Omni-Channel Flows](https://help.salesforce.com/s/articleView?id=service.omnichannel_flows.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"unifies the routing setup for all supported channels, including voice calls, chats, messaging sessions, cases, leads, and custom objects"*
- [Create the recordId](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_create_recordid.htm&type=5) — Salesforce Help · via search 2026-09-24 · Text, Available for input
- [Create the input_record](https://help.salesforce.com/s/articleView?id=service.omnichannel_create_input_record.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Record data type, for routing on field values
- [Route Work with Omni-Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_route_work.htm&type=5) — Salesforce Help · via search 2026-09-24 · route to reps, skills, queues, AI agents or bots; a record-triggered parent flow for cases, leads and custom objects; exceptions go to the fallback queue
- [Configure Omni-Channel Routing](https://help.salesforce.com/s/articleView?id=service.configure_omni_channel_routing.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"Specify Queue, Agent, Bot, or Skills as the Route To value"*
- [Route to an Agentforce Service Agent](https://help.salesforce.com/s/articleView?id=service.omnichannel_route_to_ai_agent_target.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · activate the agent and refresh Flow Builder
- [Make Smarter Routing Decisions by Checking Service Rep Availability](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_check_availability_for_routing.htm&type=5) — Salesforce Help · via search 2026-09-24 · Estimated Wait Time and reps online as outputs
- [Set Up Routing for Messaging Channels](https://help.salesforce.com/s/articleView?id=service.messaging_omnichannel_routing.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Routing Type Omni-Flow, Flow Definition and Fallback Queue
- [Map Pre-Chat Values in Omni-Channel Flow](https://help.salesforce.com/s/articleView?id=service.miaw_map_messaging_2.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Parameter Mapping; matching API name; Text only; values converted to strings
- [Assign an Omni-Channel Flow to Route Cases from Email-to-Case](https://help.salesforce.com/s/articleView?id=sf.omnichannel_route_email_to_case.htm&language=en_US) — Salesforce Help · via search 2026-09-24
- [Reassign Work Manually](https://help.salesforce.com/s/articleView?id=service.omnichannel_agent_reassign_work.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · reassigning to a skill sets the level to 0; use a flow to set a level
- [Optimize Call Routing with Omni-Channel Flows for Voice](https://trailhead.salesforce.com/content/learn/modules/ai-integration-for-agentforce-contact-center/manage-inbound-call-routing) — Trailhead · read 2026-09-24 · `recordId` for the voice call; Route To *Agentforce Service Agent*; Fallback Queue as a *"safety net when your primary routing target can't accept the work"*

## History

- 2026-09-24 · created — research pass for the new SF_Service vault
