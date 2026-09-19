# Prompt Template Versions & Access

> Folder: SF_Agentforce · Level: basic · Status: 🌱 3 gaps open
> Created: 2026-08-28 · Updated: 2026-08-28

**One line:** Who can build a template, who can run one, and what happens when you change one that is live.

**Reach for it when:** You cannot find Prompt Builder, or you need to edit a template that is already in use.

## Getting access

- **Setup → Einstein Setup → Enable Einstein.** That switch comes first; nothing works without it.
- **Prompt Template Manager** — the permission set for people who **create and manage** templates.
- **Prompt Template User** — the permission set for end users who **run** them.
- **The two are alternatives, not a hierarchy.** Assign one or the other, not both. 🚩 Whether Manager also confers User's run rights is not documented.
- Separate from both: **Execute Prompt Template**, which is what *Setup with Agentforce* needs → [SF_core · 01-admin · 19](../SF_core/01-admin-and-declarative-platform/19-agentforce-in-setup-and-ai-assisted-admin.md).

## Versions

- Every saved version gets a **version number**, and all of them travel together as metadata → [Metadata & Deployment](prompt-template-metadata-and-deployment.md).
- **An activated version is immutable.** You cannot edit it. To change it, **Save As → new version**.
- Activate from the **Versions** menu; deactivate whenever you like. **Rollback is really "activate an earlier version"** — no undo button, but the old one is still there.

## Gotchas

- **Deactivate the active version and no version is active at all.** The template stops working until you pick one — this is the sharp edge, because nothing prompts you to choose.
- **A template must be activated before anything can call it.** A draft is invisible to agents, flows and Apex alike.

## Gaps to close

- [ ] 🚩 Is there a cap on how many versions a template can keep? None is documented in the Limits page or the Metadata API.
- [ ] 🚩 Does Prompt Template Manager also confer the run rights that Prompt Template User grants?
- [ ] Do either of the two permission sets reach Data 360 or agent configuration, or are they Prompt Builder only?

## Related

- [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md) — what a template is in the first place
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — activation is what gates a template appearing there
- [Prompt Template Metadata & Deployment](prompt-template-metadata-and-deployment.md) — the same versions as XML, and what breaks moving them between orgs
- [SF_core · 32 Invoking prompt templates from Apex](../SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md) — `getPromptTemplates` filters on active state, which is how code avoids a hardcoded dev name

## Sources

- [Use Multiple Versions](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_use_multiple_versions.htm&language=en_US&type=5) and [Activate and Deactivate](https://help.salesforce.com/s/articleView?id=sf.prompt_builder_activate_deactivate_templates.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 — both JS-rendered, open to verify
- [Give Users Access to a Prompt Template](https://help.salesforce.com/s/articleView?id=ai.prompt_builder_give_users_access.htm&language=en_US&type=5) — Salesforce Help · via search 2026-08-28 — page is JS-rendered, open it to verify

## History

- 2026-08-28 · split out of [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md); absorbed its activation gotcha
- 2026-08-28 · Manager-vs-User relationship added; deployment answered and split into its own note
