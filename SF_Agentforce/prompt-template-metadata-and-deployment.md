# Prompt Template Metadata & Deployment

> Folder: SF_Agentforce · Level: working · Status: ✅ complete
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
- **The pointer cannot go stale on its own.** `activeVersionIdentifier` and `templateVersions[]` sit in one file and deploy as one unit, so the target never receives a pointer without the version it names — unless you hand-edit the XML.
- **Published versions cannot be edited by UI *or* Metadata API.** The immutability rule is platform-wide, not a Prompt Builder nicety → [Versions & Access](prompt-template-versions-and-access.md).
- **`GenAiPromptTemplateActv` is a different type.** It applies **only to Salesforce-provided templates** and just sets `accessLevel` — `Allowed` or `Blocked`. It is not how you activate your own version.
- **Retrieve pulls what you name, not what the template needs.** A **Data 360 retriever is not part of this component**, so a source retrieve never brings one along; dependent metadata comes only from `rootTypesWithDependencies` on the underlying `RetrieveRequest` → [SF_core · 09-devops · 05](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

## Gotchas

- **Every dependency must exist in the target first** — custom fields named in the XML, Apex classes named in the content, and **Data 360 retrievers**. Retriever **IDs are org-specific**, so a template referencing one fails until the ID is remapped.
- **A template linked to a Flow containing an Apex action fails to deploy.** Documented as a Salesforce bug — deploy the Flow and Apex first, the template in a second pass.
- **Agent actions do not pin a version.** Deploying a template with a different `activeVersionIdentifier` changes what every agent calling it does, with nothing in the diff to say so → [Agent Actions](prompt-templates-as-agent-actions.md).

## Confirm in org

- 🚩 Is there a cap on how many versions one component can carry? None is documented in the Metadata API or the Limits page.
- 🚩 Is the Flow-with-Apex-action deployment bug still live at Summer '26? The source is third-party and undated.

## Hands-on

- [ ] **AF-META-01** · 20 min · Retrieve a template that has several versions and read the XML. **Proves:** `templateVersions[]` carries every version, plus `activeVersionIdentifier` naming the live one.
- [ ] **AF-META-02** · 30 min · Deploy a retriever-grounded template into a second org. **Proves:** retriever IDs are org-specific and the deploy fails until remapped — copy the error verbatim. **Needs:** 2nd org.
- [ ] **AF-META-03** · 20 min · Save version after version and keep going. **Settles:** whether there is a cap on versions per component 🚩.
- [ ] **AF-META-04** · 30 min · Deploy a template linked to a Flow containing an Apex action, in one pass. **Settles:** whether that deployment bug is still live 🚩. **Needs:** 2nd org.

## Related

- [Prompt Template Versions & Access](prompt-template-versions-and-access.md) — the same versions seen from the UI
- [Prompt Templates as Agent Actions](prompt-templates-as-agent-actions.md) — what consumes the active version at run time
- [SF_core · 09-devops · 05 Metadata API & deployment mechanics](../SF_core/09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — how any component moves, which this inherits
- [SF_core · 09-devops · 12 Metadata coverage & manual steps](../SF_core/09-devops-sfdx-and-release-management/12-metadata-coverage-and-manual-steps.md) — where AI metadata sits on the coverage map
- [SF_core · 31 Apex-grounded prompt templates](../SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) — `type` here and `capabilityType` there are the same strings

## Sources

- [GenAiPromptTemplate](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplate.htm), [GenAiPromptTemplateActv](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaiprompttemplateactv.htm) and [GenAiFunction](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_genaifunction.htm) — Metadata API Developer Guide · read 2026-08-28 · the last has no version field, hence the unpinned-action gotcha
- [Deploying GenAiPromptTemplate metadata](https://docs.gearset.com/en/articles/10300034-how-to-deploy-agentforce-prompt-template-genaiprompttemplate-metadata) — third party 🚩 · read 2026-08-28 · dependency and Flow-bug detail

## History

- 2026-08-28 · created from the deployment question left open by [Versions & Access](prompt-template-versions-and-access.md); then extended with why the active-version pointer cannot arrive orphaned, what retrieve does and does not pull, and the unpinned-agent-action consequence
