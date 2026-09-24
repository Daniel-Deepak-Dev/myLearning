---
vault: SF_Service
format: light
level: basic
status: open
gaps: 2
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
tags: [retirement]
---
# Omni-Channel Fundamentals

**One line:** The Service Cloud engine that pushes each work item — a case, chat, messaging session or call — to one available rep, based on presence and capacity.

**Reach for it when:** work has to reach a rep now, not just land in a queue that someone might check later.

## Key points

- **Ownership on create vs who works it now.** Queue-plus-assignment-rule is still right for record routing: it decides the owner when a record is created → [SF_core · 01-admin · 11](../SF_core/01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md). It does not distribute live work. Omni-Channel does, using presence and capacity.
- **Five building blocks:** service channel, routing configuration, queue, presence status, presence configuration. The rep works in the **Omni-Channel** component of a Lightning console app — sidebar (recommended) or utility bar.
- **A service channel** makes an object routable. `ServiceChannel.RelatedEntity` is unique in the org, so there is one channel per object: `Case`, `MessagingSession`, `VoiceCall`, `Lead`, a custom object.
- **A routing configuration** sets how a queue's work is pushed: priority, routing model, work size. It is attached to the **queue** → [Routing & capacity](omni-channel-routing-and-capacity.md).
- **A presence status** (Online, Busy, Away…) lists the channels a rep takes work from while in it. Reps get statuses through a permission set, or a profile's **Enabled Service Presence Status Access** list.
- **A presence configuration** sets a rep's total **capacity** and behaviour: auto-accept, decline, decline reasons. You assign it to users or profiles.
- **The lifecycle in objects:** work waits as a `PendingServiceRouting` row → Omni-Channel pushes it → an `AgentWork` row is created with `Status = Assigned` → `Opened` on accept → `Closed`. Rep presence is logged in `UserServicePresence`.
- **Licences.** Omni-Channel comes with **Agentforce Service** (Service Cloud's current name) or an add-on: Digital Engagement, Enhanced Chat, Salesforce Voice, Workforce Management. The **Service Cloud User** feature licence gates the Service Console → [SF_core · 07 · 02](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md).

## There is one Omni-Channel now

- **Standard Omni-Channel retired in Summer '26.** Salesforce auto-upgraded orgs to **Enhanced Omni-Channel** in the Summer '26 rollout — but only orgs on **Hyperforce** with **no active standard channels**, such as legacy Chat.
- **An org that was not upgraded is stuck.** Reps cannot log in to Omni-Channel or Omni Supervisor, so no work is assigned.
- **Nothing is lost by upgrading.** Routing configurations, queues and skills carry over. Enhanced adds paused work, the **Reassign** action and a single inbox list in place of the **New** and **My Work** tabs.
- **Manual upgrade:** upgrade standard channels first, then Setup → **Omni-Channel Settings** → **Enhanced Omni-Channel Routing**. Do it while reps are offline, and allowlist `*.salesforce-scrt.com`.

## Gotchas

- **Treat "Standard or Enhanced?" as a migration question, not a design one.** Tutorials and exam dumps still teach Standard. Anything that mentions New / My Work tabs is describing a retired UI.
- **The two retirements are coupled.** An org still running legacy Chat (retired 14 February 2026) had an active standard channel, so it also missed the Omni auto-upgrade → [Enhanced Chat](enhanced-chat.md).
- **One presence configuration per user.** Assigning a user to a second one removes them from the first, with no warning. A user-level assignment beats a profile-level one.
- **Auto-accept and decline exclude each other.** `OptionsIsAutoAcceptEnabled` is only available when `OptionsIsDeclineEnabled` is false.
- **No presence status access, no work.** A rep who cannot pick a status never goes online, and does not appear in a supervisor configuration's user list either.

## Gaps to close

- [ ] Does a rep need the Service Cloud User feature licence to use the Omni-Channel component, or only a Lightning console app plus a presence status?
- [ ] For an org that missed the Summer '26 auto-upgrade, can an admin still switch on Enhanced Omni-Channel, or does it need Salesforce Support?

## Hands-on

- [ ] **SVC-OMNI-01** · 30 min · Enable Omni-Channel, build a Case service channel, a queue with a routing configuration, a status and a presence configuration, then assign a case to the queue while the rep is Online. **Proves:** assignment to the queue triggers the push — `PendingServiceRouting` appears, then an `AgentWork` row replaces it. **Needs:** second rep user.
- [ ] **SVC-OMNI-02** · 10 min · Assign the rep to a second presence configuration, then reopen the first. **Proves:** a user holds one configuration — the first assignment was dropped without a warning. **Needs:** second rep user.
- [ ] **SVC-OMNI-03** · 15 min · Remove the rep's status access from their permission set, then try to go Online. **Proves:** no status access means no Omni-Channel — copy what the component shows, verbatim. **Needs:** second rep user.
- [ ] **SVC-OMNI-04** · 15 min · Allow declines with reasons, push a case, decline it, then query `AgentWork`. **Proves:** the decline and its reason live on `AgentWork` (`Status = Declined`, `DeclineReason`), not on the Case. **Needs:** second rep user.

## Related

- [Omni-Channel Routing & Capacity](omni-channel-routing-and-capacity.md) — what the routing configuration and presence configuration actually compute
- [Omni-Channel Flows](omni-channel-flows.md) — the routing setup that replaces a queue's fixed routing configuration with logic
- [Omni Supervisor](omni-supervisor.md) — the live view of the statuses, queues and `AgentWork` rows this note introduces
- [Enhanced Chat](enhanced-chat.md) — the retirement that decided which orgs got the Omni auto-upgrade
- [SF_core · 01-admin · 11 Queues, assignment & escalation rules](../SF_core/01-admin-and-declarative-platform/11-queues-assignment-and-escalation-rules.md) — ownership on create, the half of routing that is not Omni-Channel
- [SF_core · 07-security · 08 Groups, queues & the grantee model](../SF_core/07-security-and-sharing/08-groups-queues-and-the-grantee-model.md) — an Omni queue is still a `Group`, with the same sharing and hierarchy rules
- [SF_core · 07-security · 02 Licences & what they gate](../SF_core/07-security-and-sharing/02-licences-and-what-they-gate.md) — the Service Cloud User feature licence, and why it hides on the User record
- [SF_core · CURRENCY](../SF_core/CURRENCY.md) — the Standard Omni-Channel retirement row, beside the legacy Chat one

## Sources

- [Standard Omni-Channel Retirement](https://help.salesforce.com/s/articleView?id=004868010&language=en_US&type=1) — Salesforce Help 004868010 · via search 2026-09-24 · *"retired with the Summer '26 release"*; Hyperforce and no active standard channels; users can't log in to Omni-Channel or Omni Supervisor
- [Standard Omni-Channel Is Scheduled for Retirement](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.rn_omnichannel_stnd_eol.htm&release=262&type=5) — Summer '26 release notes · via search 2026-09-24 · *"users will not be able to login to Omni-Channel, and therefore would not be assigned any work"*
- [Eligible Salesforce Orgs Automatically Upgraded to Enhanced Omni-Channel](https://help.salesforce.com/s/articleView?id=release-notes.rn_omnichannel_auto_org_migration.htm&language=en_US&release=256&type=5) — Summer '25 release notes · via search 2026-09-24 · the earlier auto-upgrade wave
- [Comparison of Standard and Enhanced Omni-Channel](https://help.salesforce.com/s/articleView?id=service.omnichannel_std_vs_enhanced.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · *"All preexisting Standard Omni-Channel features are fully supported by the enhanced version"*
- [Upgrade Standard Omni-Channel to Enhanced](https://help.salesforce.com/s/articleView?id=service.omnichannel_upgrade_standard_to_enhanced.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · upgrade standard channels first
- [Understand Enhanced Omni-Channel for Customer Service](https://trailhead.salesforce.com/content/learn/modules/enhanced-omni-channel-quick-look/get-to-know-enhanced-omni-channel) — Trailhead · read 2026-09-24 · the Enhanced Omni-Channel Routing toggle; reassign to rep, skill, queue or flow
- [Deploy and Optimize Enhanced Omni-Channel for Success](https://trailhead.salesforce.com/content/learn/modules/enhanced-omni-channel/prepare-and-deploy-enhanced-omni-channel) — Trailhead · read 2026-09-24 · offline window, `*.salesforce-scrt.com`, what carries over
- [Master Omni-Channel Routing for Effective Service Management](https://trailhead.salesforce.com/content/learn/modules/omni-channel-lex/start-routing-omnichannel) — Trailhead · read 2026-09-24 · the building blocks plus the Omni-Channel utility; status access through **Enabled Service Presence Status Access**
- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `AgentWork`, `PendingServiceRouting`, `ServiceChannel.RelatedEntity`, `UserServicePresence`, `PresenceUserConfig` options — a Winter '27 build; only fields at API 67.0 or earlier are used here
- [Omni Supervisor (PDF)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/omnichannel_supervisor.pdf) — Salesforce, Winter '27, last updated 22 July 2026 · read 2026-09-24 · the Enhanced component's inbox format; sidebar recommended
- [Create Presence Configurations](https://help.salesforce.com/s/articleView?language=en_US&id=service.service_presence_create_presence_configurations.htm&type=5) — Salesforce Help · via search 2026-09-24 · one configuration per user; user level overrides profile
- [Set Access to Presence Statuses](https://help.salesforce.com/s/articleView?id=service.omnichannel_set_access_presence_statuses.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24
- [Enable and Configure Omni-Channel](https://help.salesforce.com/s/articleView?language=en_US&id=service.omnichannel_enable.htm&type=5) — Salesforce Help · via search 2026-09-24 · the product licence and add-on list
- [Assign the Service Cloud Feature License to Users](https://help.salesforce.com/s/articleView?language=en_US&id=service.console2_assign_service_feature_license.htm&type=5) — Salesforce Help · via search 2026-09-24
- [Omni-Channel Component for Lightning Console Apps](https://help.salesforce.com/s/articleView?id=service.console_lex_custom_utilities_omnichannel.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24

## History

- 2026-09-24 · created — research pass for the new SF_Service vault; takes over the Omni-Channel paragraph from SF_core · 01-admin · 11
