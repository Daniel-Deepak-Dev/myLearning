# Prompt Template Metadata & Deployment

> Folder: SF_Agentforce · Level: working · Status: 🌱 4 gaps open
> Created: 2026-08-28 · Updated: 2026-08-28

**One line:** What a prompt template looks like as metadata, and what breaks when you move it between orgs.

**Reach for it when:** Putting templates in source control, or a deployment fails.

## The component

`GenAiPromptTemplate` · API **60.0+** · directory `genAiPromptTemplates/` · suffix `.genAiPromptTemplate`. The three fields that carry the version story:

| Field | Holds |
|---|---|
| `type` | The template type — `einstein_gpt__salesEmail`, `__fieldCompletion`, … the **same strings** Apex uses as `capabilityType` |
| `templateVersions[]` | **Every version**, each with `versionNumber`, `status` (`Draft` / `Published`), `content`, `primaryModel` |
| `activeVersionIdentifier` | Which version is live |

- **All versions travel together, plus a pointer to the active one.** Deployment is not "the active version" — it is the whole history and the choice of which is on.
- **Published versions cannot be edited by UI *or* Metadata API.** The immutability rule is platform-wide, not a Prompt Builder nicety → [Versions & Access](prompt-template-versions-and-access.md).
- **`GenAiPromptTemplateActv` is a different type.** It applies **only to Salesforce-provided templates** and just sets `accessLevel` — `Allowed` or `Blocked`. It is not how you activate your own version.

## Gotchas

- **Every dependency must exist in the target first** — custom fields named in the XML, Apex classes named in the content, and **Data 360 retrievers**. Retriever **IDs are org-specific**, so a template referencing one fails until the ID is remapped.
- **A template linked to a Flow containing an Apex action fails to deploy.** 🚩 Documented as a Salesforce bug, undated — deploy the Flow and Apex first, the template in a second pass.

## Gaps to close

- [ ] Is there a cap on how many versions one component can carry? None is documented.
- [ ] What happens if `activeVersionIdentifier` names a version the target org does not have?
- [ ] 🚩 Is the Flow-with-Apex-action deployment bug still live at Summer '26? The source gives no date.
- [ ] Does `sf project retrieve start` pull dependent retrievers, or only the template?

## Related

- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — the same versions seen from the UI
- [SF_core · 09-devops · 05 Metadata API & deployment mechanics](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — how any component moves, which this inherits
- [SF_core · 09-devops · 12 Metadata coverage & manual steps](../SF_core/09-devops-sfdx-and-release-management/12-metadata-coverage-and-manual-steps.md) — where AI metadata sits on the coverage map
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — `type` here and `capabilityType` there are the same strings

## Sources

- [GenAiPromptTemplate](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplate.htm) and [GenAiPromptTemplateActv](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplateactv.htm) — Metadata API Developer Guide · read 2026-08-28
- [Deploying GenAiPromptTemplate metadata](https://docs.gearset.com/en/articles/10300034-how-to-deploy-agentforce-prompt-template-genaiprompttemplate-metadata) — third party 🚩 · read 2026-08-28 · dependency and Flow-bug detail

## History

- 2026-08-28 · created from the deployment question left open by [Versions & Access](prompt-template-versions-and-access.md)
