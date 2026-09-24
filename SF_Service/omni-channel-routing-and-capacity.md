---
vault: SF_Service
format: light
level: working
status: open
gaps: 3
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Omni-Channel Routing & Capacity

**One line:** The four ways Omni-Channel picks a rep, and the arithmetic that decides whether that rep can take one more item.

**Reach for it when:** work sits in a queue while reps look free, or one rep drowns while another idles.

## Key points

| Routing | Work goes to | Set up in | Backlog shows in |
|---|---|---|---|
| **Queue-based** | a rep in the Omni queue, by the queue's routing configuration | queue + routing configuration | Queues Backlog |
| **Skills-based** | the first available rep holding **every** required skill | **Enable Skills-Based and Direct-to-Agent Routing**; rules or a flow | Skills Backlog |
| **Direct-to-agent** | one named rep (`PreferredUserId`), with a fallback | the same setting; a flow or **Reassign** | — |
| **External** | a third-party router that creates `AgentWork` itself | its own routing configuration and queue | Queues Backlog |

- **Routing configuration fields** (`QueueRoutingConfig`): **Routing Priority** — the lower number is routed first; **Routing Model**; **Push Timeout** in seconds, `0` = off; work size as **Units of Capacity** *or* **Percentage of Capacity**, never both; **Overflow Assignee**, a user or queue.
- **Least Active** picks the rep with the fewest open items. **Most Available** picks the most spare capacity. On a tie: reps with no work first, earliest login first, then the rep whose last assignment is oldest.
- **Secondary routing priority** lives on the **service channel**: a field (`SecRoutingPriorityField`) plus value-to-priority rows (`ServiceChannelFieldPriority`), e.g. Case Priority High = 1.
- **Skills:** the work carries `SkillRequirement` rows with a level (0–99.99) and an `IsAdditionalSkill` flag. Rep skills live on `ServiceResource` → `ServiceResourceSkill`; Field Service does not need to be on.
- **Additional skills drop** after **Drop Additional Skills Time-Out** (minimum 5 seconds), highest `SkillPriority` value first. **Skills-based routing rules** map picklist, boolean and lookup values to skills — up to 10 fields and 100 values — once the routing configuration ticks **Use with Skills-Based Routing Rules**.
- **Capacity:** the presence configuration sets the rep's total (`PresenceUserConfig.Capacity`). Each item deducts its weight or percentage. A voice call must take 100%.
- **Tab-based vs status-based** is set per **service channel**. Tab-based frees capacity when the rep closes the work tab. Status-based frees it when a picklist **Status Field** reaches a value mapped as Completed, and caps a rep at 100 items.
- **Status-based keeps work assigned** when the rep closes the tab or goes offline. **Paused** is a third mapped value, Enhanced Omni-Channel only; paused items carry their own capacity weight (`PausedCapacityWeight`).
- **Interruptible capacity** (API 57.0+) splits primary work, such as a call, from interruptible work, such as a case, so one can pause for the other.
- **Fallback Mode** keeps routing alive if the Omni routing service is down. It needs Enhanced Omni-Channel, tab-based capacity and external routing, Support switches it on, and it polls for new work every 60 seconds.

## Gotchas

- **A decline or push timeout is final for that rep.** Omni-Channel never offers the item to them again, even if they are the only rep online. Capacity is released, but the item stays theirs until it routes again.
- **Status-based needs honest statuses.** A Status value not mapped as Completed or Paused keeps capacity consumed after the case is really done.
- **Tab-based fails in apps with standard navigation.** It needs a console app, because the tab is the session.
- **`IsPreferredUserRequired = true` plus a push timeout is unsupported.** The item waits for that rep and nobody else.
- **One object and one channel per Omni queue.** Mixing `Case` and `MessagingSession` in one queue can cause routing conflicts and failures.

## Gaps to close

- [ ] What exactly does the Overflow Assignee on a routing configuration receive, and what triggers the overflow?
- [ ] How do routing priority, secondary routing priority and `TargetAcceptDateTime` (API 65.0) combine when ordering one backlog?
- [ ] Can one rep hold a tab-based channel and a status-based channel at once, and how is their capacity summed?

## Hands-on

- [ ] **SVC-ROUTE-01** · 20 min · Give the rep capacity 4, size cases at 2 units, then assign three cases to the queue. **Proves:** the third case waits although the rep is Online — capacity blocks it, not availability. **Needs:** second rep user.
- [ ] **SVC-ROUTE-02** · 20 min · Switch the Case channel to status-based, accept a case, close its tab without touching Status. **Proves:** capacity stays consumed until Status reaches a Completed value — the tab is irrelevant. **Needs:** second rep user.
- [ ] **SVC-ROUTE-03** · 15 min · With one rep Online and a 10-second push timeout, ignore a pushed case. **Proves:** `AgentWork` shows `DeclinedOnPushTimeout` and the case is never offered to that rep again. **Needs:** second rep user.
- [ ] **SVC-ROUTE-04** · 30 min · Turn on skills-based routing; require two skills, one additional, with a 30-second drop time-out; give the rep only the required one. **Proves:** the case routes only after the additional skill drops. **Needs:** second rep user.

## Related

- [Omni-Channel Fundamentals](omni-channel-fundamentals.md) — the building blocks these settings sit on
- [Omni-Channel Flows](omni-channel-flows.md) — where skills, direct-to-agent routing and fallback queues are set per item instead of per queue
- [Omni Supervisor](omni-supervisor.md) — the Queues Backlog and Skills Backlog tabs that show which routing type is starving
- [SF_core · 07-security · 08 Groups, queues & the grantee model](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — why a memberless Omni queue swallows work silently

## Sources

- [Routing Model Options for Omni-Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.service_presence_routing_options.htm&type=5) — Salesforce Help · via search 2026-09-24 · Least Active vs Most Available, and the tie-break order
- [Routing Configuration Settings](https://help.salesforce.com/apex/HTViewHelpDoc?id=service_presence_routing_configuration_settings.htm) — Salesforce Help · via search 2026-09-24 · *"Size items by number of units or percentage of a service rep's capacity, but not both"*
- [Understand Capacity Models](https://help.salesforce.com/s/articleView?id=service.service_presence_capacity_model.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Set Up a Status-Based Capacity Model](https://help.salesforce.com/s/articleView?id=service.omnichannel_status_based_capacity.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Status Field values for completed, paused and in-progress work; 100 work items per rep
- [How Does Skills-Based Routing Work?](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_how_skills_based_routing_works.htm&type=5) — Salesforce Help · via search 2026-09-24 · drop time-out minimum 5 seconds
- [Enable Skills-Based Routing](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_skills_based_routing_enable.htm&type=5) — Salesforce Help · via search 2026-09-24 · the *Enable Skills-Based and Direct-to-Agent Routing* setting
- [Routing with Skills-Based Routing Rules](https://help.salesforce.com/s/articleView?id=service.omnichannel_attribute_based_routing.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · 10 fields and 100 values
- [Skills-Based Routing Setup Guide](https://trailhead.salesforce.com/content/learn/modules/omni-channel-lex/understand-sbr) — Trailhead · read 2026-09-24 · `ServiceResource` with Resource Type *Agent*, `ServiceResourceSkill`, the supported objects
- [Route Work with Omni-Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_route_work.htm&type=5) — Salesforce Help · via search 2026-09-24 · *"Omni-Channel doesn't try to route that work item to that rep again"*
- [Prioritize with Interruptible Capacity](https://help.salesforce.com/s/articleView?id=service.omnichannel_interruptible_capacity.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Routing Work with Omni-Channel Fallback Mode](https://help.salesforce.com/s/articleView?id=002186102&language=en_US&type=1) — Salesforce Help KB 002186102 · via search 2026-09-24 · Enhanced + tab-based + external routing; 60-second polling
- [External Routing for Omni-Channel](https://developer.salesforce.com/docs/atlas.en-us.omni_channel_dev.meta/omni_channel_dev/omnichannel_external_routing.htm) — Omni-Channel Developer Guide · via search 2026-09-24 · separate routing configuration and queue
- [Troubleshooting Guide for Omni-Channel Routing Issues](https://help.salesforce.com/s/articleView?id=005226660&language=en_US&type=1) — Salesforce Help KB 005226660 · via search 2026-09-24 · one object type and one channel per queue
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `QueueRoutingConfig` (lower priority value routed first, `OverflowAssigneeId`), `ServiceChannel.CapacityModel` and `SecRoutingPriorityField`, `ServiceChannelFieldPriority`, `SkillRequirement` (level 0–99.99, `SkillPriority` drop order), `PendingServiceRouting.IsPreferredUserRequired`, `AgentWork.Status`
- [Omni Supervisor (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/omnichannel_supervisor.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · *"Tab-based capacity models don't work with apps that use standard navigation"*

## History

- 2026-09-24 · created — research pass for the new SF_Service vault
