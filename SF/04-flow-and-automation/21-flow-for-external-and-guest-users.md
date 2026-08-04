# Flow for External & Guest Users

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** Running a flow for somebody who is not a licensed internal user — how access is granted, and what an unauthenticated visitor can reach. The general context model is [19](19-flow-run-context-and-sharing.md); site hardening is [05-experience-cloud · 07](../05-experience-cloud-lwr/07-guest-user-security-model.md).

> **What changed.** *"Give the guest user profile the `Run Flows` permission"* is the answer in almost every tutorial and **that permission no longer exists on the guest profile.** Salesforce discontinued it for new orgs in **Winter '22** and removed it from every org's Guest User profile in **Spring '23**. Access is now granted **one flow at a time** — *Enabled Flow Access* on the guest user profile, or *Edit Access* on the flow itself. There is no blanket switch, deliberately.

## Core idea

A guest user is an unauthenticated visitor executing your automation, and the thing that makes this dangerous is not the flow — it is the combination of a flow with an elevated context and a profile nobody audits. Two independent decisions stack here. The **access** decision says which specific flows a guest may run at all, and since Spring '23 it is per-flow by design. The **context** decision says what those flows may see, and a screen flow's default is *Depends on How Flow is Launched*, which for a guest means the guest's own limited access — until somebody sets it to system context to fix a permissions error, at which point an anonymous visitor is executing logic that bypasses sharing. That is not a hypothetical: the 2025 Experience Cloud incidents were **configuration**, not a platform vulnerability, and this is one of the configurations.

> **From my notes.** A profile-by-profile audit of the **`Run Flows`** permission across a production org — *"allows the user to launch and interact with any flow made available to them"* — with roughly half the profiles enabled and half not. Still exactly the right exercise, and still valid for **internal** profiles, where `Run Flows` is alive and is genuinely all-or-nothing. What has changed is that the guest profile is no longer on that list: the permission was removed from it in Spring '23, and the equivalent audit for guests is the **Enabled Flow Access** list, one flow at a time.

## How it works

| Question | Where it is answered |
|---|---|
| May this guest run this flow? | Experience Builder → Settings → **Public Access** → guest user profile → **Enabled Flow Access** |
| …or per flow | Setup → Flows → the flow → **Edit Access** |
| What may it see? | Flow Properties → *How to Run the Flow* → [19](19-flow-run-context-and-sharing.md) |
| Which records? | guest sharing model — guests own nothing and see nothing by default |

- **Authenticated external users are a different problem.** A community or portal user has a licence, a profile and permission sets; the ordinary access model applies, and the licence decides which objects exist for them at all.
- **Guest users cannot own records**, so any flow creating a record for a guest must assign an owner explicitly — usually a default internal user or a queue.
- **A screen flow reaches a site through the Flow component in Experience Builder**, and the Orchestration Work Guide component is the equivalent for orchestration work items. → [16](16-flow-orchestrator.md)
- **External Services actions became reachable by guest users in Winter '22**, which means an HTTP callout is now part of the guest attack surface too. → [12](12-http-callout-and-external-services-in-flow.md)
- **The recommended shape is a narrow elevation**: leave the guest-facing screen flow in the guest's own context and put the one privileged operation in a subflow set to system context.

## 2026 currency

The subject's centre of gravity moved from *how do I make this work* to *how do I stop this leaking*, driven by a sustained 2025–26 campaign against over-permissive Experience Cloud guest configurations. Salesforce's position is worth repeating precisely because it is correct and unhelpful: the platform was not vulnerable, the configurations were. The practical checklist that came out of it is short — remove **API Enabled** from the guest profile, strip object access back to what the public site genuinely needs, keep *Secure guest user record access* on, and treat every flow on the *Enabled Flow Access* list as something a stranger can run today. Nothing in Summer '26 changes the mechanics; what changed is that this is now an audit item rather than a design note. → [05-experience-cloud](../05-experience-cloud-lwr/INDEX.md), [07-security](../07-security-and-sharing/INDEX.md)

## Gotchas

- **`Run Flows` is gone from the guest profile.** Any guide telling you to grant it is pre-Spring '23 and its other advice is likely as old.
- **Enabled Flow Access is a list a stranger can run.** Review it like a public API surface, because that is what it is.
- **Setting a guest-facing screen flow to system context hands sharing bypass to an anonymous visitor.** Elevate a subflow instead.
- **Data pulled into an elevated screen flow is in the browser**, reachable through developer tools whether or not a component displays it. → [04](04-screen-flows-and-ux-design.md)
- **Guest users cannot own records.** A Create Records element without an explicit owner fails or assigns unexpectedly.
- **Fault messages leak.** `$Flow.FaultMessage` on a public screen tells an attacker about your schema. → [10](10-fault-paths-and-custom-errors.md)
- **A flow packaged in a managed package cannot have its guest access edited**, which constrains what you can expose from AppExchange content.
- **Authenticated external users are not guests.** Do not carry guest hardening advice onto community licences, or you will debug access errors that are licence limits.

## Recall

Q: How do you let a guest user run a flow, and what is the trap in older instructions?
A: Per flow, via *Enabled Flow Access* on the guest profile or *Edit Access* on the flow. The old `Run Flows` permission was removed from the guest profile in Spring '23.

Q: What is the effective context of a guest-facing screen flow left on the default setting?
A: The guest's own access — *Depends on How Flow is Launched*. The danger begins when someone changes it to system context.

Q: Why can't a flow simply create a record owned by the guest who submitted it?
A: Guest users cannot own records. The owner has to be set explicitly.

Q: Were the 2025 Experience Cloud guest-user incidents a platform vulnerability?
A: No — over-permissive customer configuration. That is precisely why the guest profile and the flow access list are audit items.

Q: Which permission should almost always be removed from a guest user profile?
A: **API Enabled**.

## Related

- [19 · Flow run context & sharing](19-flow-run-context-and-sharing.md) — the setting that turns a guest-facing flow into an exposure
- [05-experience-cloud · 07 Guest user security model](../05-experience-cloud-lwr/07-guest-user-security-model.md) — site-level guest hardening, written in phase 18
- [05-experience-cloud · 11 Public site exposure audit](../05-experience-cloud-lwr/11-public-site-exposure-audit.md) — the runbook the checklist above became
- [12 · HTTP callout & External Services](12-http-callout-and-external-services-in-flow.md) — the callout surface guests gained in Winter '22
