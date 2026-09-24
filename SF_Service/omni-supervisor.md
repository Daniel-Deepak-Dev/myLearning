---
vault: SF_Service
format: light
level: basic
status: open
gaps: 2
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Omni Supervisor

**One line:** The supervisor's live view of Omni-Channel — who is online, what is waiting, who holds what — with actions to move reps and help them mid-conversation.

**Reach for it when:** a queue is backing up now and you need to see why, and move people or work before the next report runs.

## Key points

- **Same tool, new name.** Help and Trailhead now call it **Command Center for Service**. The Winter '27 PDF guide is still titled *Omni Supervisor*, and the object is still `OmniSupervisorConfig`.
- **Switching it on:** Setup → **Supervisor Settings** to pick features. Then App Manager → the console app → **Navigation Items** → add **Command Center for Service**. Supervisors also need the tab visible.
- **A supervisor configuration** (Setup → **Supervisor Configurations**) scopes one group of supervisors. It sets **Which Supervisors Are Impacted?** (users or profiles), the visible reps or public groups, queues and skills, the visible tabs and their order, and the allowed actions.
- **It filters the view; it grants nothing.** It changes what supervisors see on the tabs, not their access to reps, queues or records.
- **Five tabs:** **Service Reps** (was *Agents*), **Queues Backlog**, **Skills Backlog**, **In-Progress Work** (was *Assigned Work*) and **Wallboard**. Which appear depends on routing — queue-only or external routing shows no Skills Backlog.
- **Service Reps** shows each rep's status, channels, queues, work and capacity. A supervisor can change a rep's status there, and open a timeline of their `AgentWork` history.
- **Queues Backlog** shows waiting counts and wait times per queue. **Assign Agents** adds reps to a queue; they keep their old queues too.
- **Helping live:** a rep **raises a flag** with a message. The supervisor clicks **Monitor**, reads the conversation and sends **whisper** messages the customer never sees. Voice calls add **Listen In**.
- **Wallboard** shows the last hour: reps by status and capacity, work by status (Assigned, Waiting, In Progress), wait times, handle time and speed to answer, raised flags.
- **Real-time only.** Every tab is live. History comes from reports — custom report types with **Agent Work** as the primary object, and `UserServicePresence` for time in each status.

## Gotchas

- **No configuration means everything.** A supervisor with no supervisor configuration sees all queues.
- **Membership must be direct.** Users added through roles or *Grant Access Using Hierarchies* don't count; only users directly in a public group do. A user with no presence status is missing from the picker.
- **Missing Change Queues or Change Skills buttons** means those actions are not in the configuration. Voice queues never appear in Change Queues — use Queues Backlog.
- **Whispers are kept.** The rep–supervisor exchange is added to the conversation transcript in real time.
- **Enhanced Omni-Channel has no transfer icon.** Moving work to a skill uses the **Reassign** action or a screen flow on the record page → [Omni-Channel flows](omni-channel-flows.md).
- **Offline stops tracking.** Setting a rep Offline from the tab means their work is no longer tracked there.

## Gaps to close

- [ ] When did Omni Supervisor become Command Center for Service, and did any Setup label or permission change with the name?
- [ ] In Enhanced Omni-Channel, can a supervisor reassign one waiting or in-progress item from these tabs, or only change a rep's queues and skills?

## Confirm in org

- 🚩 In a Summer '26 Developer Edition org, is the navigation item named Omni Supervisor or Command Center for Service? — App Manager → Service Console → Edit → Navigation Items.

## Hands-on

- [ ] **SVC-SUPV-01** · 20 min · Create a supervisor configuration limited to one queue, assign it to yourself, then open a record from the other queue directly. **Proves:** the configuration hides the queue from the tabs but leaves record access untouched. **Needs:** second rep user.
- [ ] **SVC-SUPV-02** · 15 min · Put the rep in a public group only through their role, point the configuration at that group, then look for them. **Proves:** membership through a role is ignored — only direct group members appear. **Needs:** second rep user.
- [ ] **SVC-SUPV-03** · 20 min · Have the rep raise a flag in a chat, whisper back, end the chat, then read its transcript. **Proves:** the whisper is stored in the transcript. **Needs:** second rep user, an Enhanced Chat channel.
- [ ] **SVC-SUPV-04** · 15 min · Set a rep Offline from the Service Reps tab while they hold open work, then query their `AgentWork`. **Proves:** what "no longer tracked" does to live work — copy the statuses you see. **Needs:** second rep user.

## Related

- [Omni-Channel Fundamentals](omni-channel-fundamentals.md) — the statuses, queues and `AgentWork` rows these tabs display
- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — the capacity and routing type behind every percentage and backlog shown here
- [Bot & Agent to Human Handoff](bot-and-agent-to-human-handoff.md) — the escalations that arrive in these queues from an agent
- [SF_core · 07-security · 08 Groups, queues & the grantee model](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — public groups and queues, and why a supervisor configuration only reads direct members

## Sources

- [Omni Supervisor (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/omnichannel_supervisor.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · tabs by routing type; Agents tab status change and *"the agent's work isn't tracked anymore"*; Assign Agents; flags, Monitor and whisper; *"added in real time to the conversation transcript"*; Wallboard metrics; no configuration shows all queues; *"The transfer icon doesn't appear in Enhanced Omni-Channel"*
- [Get to Know the Command Center for Service Tabs](https://help.salesforce.com/s/articleView?id=service.omnichannel_supervisor_tabs_intro.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Service Reps, Queues Backlog, Skills Backlog, In-Progress Work, Wallboard
- [Set Up Command Center for Service](https://help.salesforce.com/s/articleView?id=service.omnichannel_supervisor_intro.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Supervisor Settings
- [Add Command Center for Service to a Lightning App](https://help.salesforce.com/s/articleView?id=service.omnichannel_add_supervisor_console_LEX.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Navigation Items; tab visibility
- [Change What Supervisors See in Command Center for Service](https://help.salesforce.com/s/articleView?id=service.omnichannel_create_supervisor_configuration.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Supervisor Configurations; *Which Supervisors Are Impacted?*; direct public-group members only; filters the view, not access
- [Monitor and Support Your Service Reps](https://help.salesforce.com/s/articleView?id=service.omnichannel_supervisor_whisper.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Monitor Your Contact Center with Command Center](https://trailhead.salesforce.com/content/learn/modules/omni-channel-lex/omni-supervisor) — Trailhead · read 2026-09-24 · the Command Center name; adding it via App Manager
- [Enhance Team Performance with Real-Time Supervision Tools](https://trailhead.salesforce.com/content/learn/modules/agentforce-contact-center-for-service-reps-and-managers/empower-your-team-with-real-time-supervision) — Trailhead · read 2026-09-24 · Listen In; real-time tabs vs the Reports tab
- [Create Custom Report Types for Omni-Channel](https://help.salesforce.com/s/articleView?id=sf.omnichannel_custom_report_types.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Agent Work as primary object
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `OmniSupervisorConfig` *"represents the Command Center for Service configuration"*, `SkillVisibility` (`AllSkills` / `AnySkill`), `IsTimelineHidden`, `OmniSupervisorConfigAction`

## History

- 2026-09-24 · created — research pass for the new SF_Service vault
