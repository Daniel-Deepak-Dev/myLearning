---
vault: SF_Agentforce
format: light
level: basic
status: complete
org_checks: 1
labs: 4
created: 2026-08-28
updated: 2026-08-30
---
# Prompt Template Versions & Access

**One line:** Who can build a template, who can run one, and what happens when you change one that is live.

**Reach for it when:** You cannot find Prompt Builder, or you need to edit a template that is already in use.

## Getting access

- **Setup → Einstein Setup → Enable Einstein.** That switch comes first; nothing works without it.
- **Prompt Template Manager** — the permission set for people who **create and manage** templates.
- **Prompt Template User** — the permission set for end users who **run** them.
- **The two are alternatives, not a hierarchy.** Assign one or the other, not both.
- **Both are scoped to Prompt Builder.** Every doc describes them only as create-and-manage versus run. **Agentforce and Data 360 carry their own permission sets** — budget for those separately rather than expecting either of these to reach them.
- Separate from both: **Execute Prompt Template**, which is what *Setup with Agentforce* needs → [SF_core · 01-admin · 19](../SF_core/01-admin-and-declarative-platform/19-agentforce-in-setup-and-ai-assisted-admin.md).

## Versions

- Every saved version gets a **version number**, and all of them travel together as metadata → [Metadata & Deployment](prompt-template-metadata-and-deployment.md), which also owns the open question of whether there is a version cap.
- **An activated version is immutable.** You cannot edit it. To change it, **Save As → new version**.
- Activate from the **Versions** menu; deactivate whenever you like. **Rollback is really "activate an earlier version"** — no undo button, but the old one is still there.

## Gotchas

- **Deactivate the active version and no version is active at all.** The template stops working until you pick one — this is the sharp edge, because nothing prompts you to choose.
- **A template must be activated before anything can call it.** A draft is invisible to agents, flows and Apex alike.

## Confirm in org

- 🚩 Does Prompt Template Manager also confer the run rights that Prompt Template User grants? Open the two permission sets side by side and compare.

## Hands-on

- [ ] **AF-VER-01** · 15 min · Activate a version, then try to edit it. **Proves:** an active version is immutable — **Save As** is the only way forward.
- [ ] **AF-VER-02** · 10 min · Deactivate the active version without activating another, then call the template. **Proves:** nothing is active and the template stops working — nothing prompts you to choose.
- [ ] **AF-VER-03** · 20 min · Assign only **Prompt Template Manager** to a test user and try to *run* a template as them. **Settles:** whether Manager confers User's run rights 🚩.
- [ ] **AF-VER-04** · 15 min · Save three versions, then roll back by activating v1. **Proves:** rollback is "activate an earlier version" — there is no undo button.

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — what a template is in the first place
- [Flex Prompt Templates](flex-prompt-templates.md) — the type whose four callers all hit this activation gate
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — activation is what gates a template appearing there
- [Prompt Template Metadata & Deployment](prompt-template-metadata-and-deployment.md) — the same versions as XML, and what breaks moving them between orgs
- [SF_core · 32 Invoking prompt templates from Apex](../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) — `getPromptTemplates` filters on active state, which is how code avoids a hardcoded dev name

## Sources

- [Use Multiple Versions](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_use_multiple_versions.htm&language=en_US&type=5) and [Activate and Deactivate](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_activate_deactivate_templates.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 — both JS-rendered, open to verify
- [Give Users Access to a Prompt Template](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_give_users_access.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 — page is JS-rendered, open it to verify

## History

- 2026-08-28 · split out of [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md); absorbed its activation gotcha
- 2026-08-28 · Manager-vs-User relationship added; deployment answered and split into its own note
- 2026-08-28 · both permission sets confirmed Prompt Builder-scoped; the version-cap question moved to [Metadata & Deployment](prompt-template-metadata-and-deployment.md), which owns it
- 2026-08-30 · linked to [Flex Prompt Templates](flex-prompt-templates.md) — activation is what publishes a template to all four of its callers
