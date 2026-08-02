# Local Dev & the Lightning Dev Server

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 07

**Scope:** Seeing a component change in a browser without deploying — the `sf lightning dev` commands and the VS Code preview. Installing and configuring the CLI itself is [09-devops · 22](../09-devops-sfdx-and-release-management/INDEX.md); this owns the authoring loop.

> **What changed — twice, and the name is the trap.** The 2019-era `sfdx force:lightning:lwc:start` local dev server is **dead**, and it was a different product: it rendered components against mocks, off-org. What replaced it is `sf lightning dev`, backed by a real org. Then the branding moved: **the VS Code extension was renamed *Local Dev* → *Live Preview*, and LWC Component Preview reached GA at API 67.0** with faster, more memory-efficient hot module reloading. Anything written before Summer '26 uses a name that no longer exists.

## Core idea

The default LWC loop is deploy-and-refresh, and it is slow enough to change how people work — you batch up changes because each check costs a deploy. `sf lightning dev` replaces it with a local server that serves your components while **proxying data from a real org**, so wire adapters, `@salesforce/*` imports and Apex controllers all resolve against genuine org state rather than mocks. Save a file and the preview hot-reloads the changed module rather than rebuilding the page. The important consequence is what it is *not*: this is not a test. It proves a component renders and behaves against one org's data, which is exactly the gap Jest cannot cover ([15](15-lwc-testing-with-jest.md)) and exactly what Jest's speed and determinism buy instead. The two are complements, and neither substitutes for the other.

## How it works

- **Three entry points, three scopes.** `sf lightning dev component` previews a single component in isolation; `sf lightning dev app` previews inside a Lightning Experience shell; `sf lightning dev site` previews an Experience Cloud LWR site → [05-experience](../05-experience-cloud-lwr/INDEX.md).
- **The plugin ships with the CLI.** `@salesforce/plugin-lightning-dev` is installed by recent `sf` versions; older installs need `sf plugins install @salesforce/plugin-lightning-dev`.
- **The org has to opt in.** Setup → Quick Find → **Local Dev** → enable. For a scratch org, set it in the definition file so every new org has it.
- **Single-component preview resolves real dependencies** — Lightning Data Service wire adapters, `@salesforce/*` scoped modules and Apex controllers all work against the target org.
- **The VS Code extension is separate from the CLI.** *Salesforce Live Preview* on the Marketplace puts the preview in a tab next to the editor; the CLI is the prerequisite, not an alternative.
- **Hot module reload, not redeploy.** Editing HTML, JS or CSS and saving updates the preview in place — the component is never pushed to the org.

```json
// config/project-scratch-def.json
{
  "settings": {
    "lightningExperienceSettings": {
      "enableLightningPreviewPref": true
    }
  }
}
```

> **From my notes.** `Local Dev` (2024) is the most current LWC page in the old corpus and its four steps still describe the workflow — install `@salesforce/plugin-lightning-dev`, enable Local Dev in Setup, add `"enableLightningPreviewPref": true` to the scratch definition, run `sf lightning dev app`. **Two corrections.** The plugin install is usually unnecessary now — it comes with the CLI. And `sf lightning dev app` was the only command then; for authoring a single component the faster answer is **`sf lightning dev component`**, which arrived later and is what GA'd at 67.0. The page's title is itself the artefact: the tool it names is now *Live Preview*.

## 2026 currency

**LWC Component Preview is GA at API 67.0**, and Summer '26's contribution is performance — HMR is faster and uses less memory, which is what makes single-component preview usable as a continuous loop rather than something you start when stuck. The naming history is worth holding precisely, because search results are a minefield: *local dev server* (retired, off-org, mock-based) → *Lightning Preview* / *Local Dev* (2024, org-backed) → **Live Preview** (the VS Code extension) with **LWC Component Preview** as the single-component capability. → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **`sfdx force:lightning:lwc:start` is retired**, and blog posts about it describe a mock-backed product that no longer exists.
- **Nothing works until Local Dev is enabled in the org.** The failure is a connection error, not a helpful message about the setting.
- **A scratch org without `enableLightningPreviewPref` cannot preview** — it is a definition-file setting, so it has to be there before the org is created.
- **The preview is not a deployment.** The component is still absent from the org until you push; "it worked in preview" is not "it is deployed".
- **Preview is one org's data.** Sharing, field-level security and record availability are that user's — it is not a permissions test. → [07-security](../07-security-and-sharing/INDEX.md)
- **Not every surface previews.** Component-level preview isolates the component, so container behaviour — console tabs, quick actions, utility bar — needs `sf lightning dev app`.
- **The VS Code extension needs the CLI installed first.** Installing only the extension produces an extension that cannot start anything.

## Recall

Q: What are the three `sf lightning dev` subcommands and what does each preview?
A: `component` (a single component in isolation), `app` (inside a Lightning Experience shell), `site` (an Experience Cloud LWR site).

Q: What is the difference between the old local dev server and today's Local Dev?
A: The old `sfdx force:lightning:lwc:start` server ran off-org against mocks and is retired. `sf lightning dev` proxies a real org, so wires, `@salesforce/*` imports and Apex resolve against real data.

Q: What two things must be enabled before a preview will run?
A: Local Dev in the org's Setup (or `enableLightningPreviewPref` in the scratch definition), and the `@salesforce/plugin-lightning-dev` CLI plugin — which recent `sf` versions include.

Q: What is the current name of the VS Code extension, and what is it called in older docs?
A: **Live Preview**. Older material calls it Local Dev or Lightning Preview.

Q: Why is Live Preview not a replacement for Jest?
A: It proves behaviour against one org's data in a browser, with a human watching. Jest is deterministic, runs headless in CI, and gates a pipeline.

## Related

- [15 · LWC testing with Jest](15-lwc-testing-with-jest.md) — the deterministic half of the feedback loop
- [16 · Performance & debugging](16-lwc-performance-and-debugging.md) — profiling the component once you can see it
- [22 · LWC OSS & off-platform reuse](22-lwc-open-source-and-off-platform-reuse.md) — developing LWC with no org at all
- [09-devops · sf CLI & tooling](../09-devops-sfdx-and-release-management/INDEX.md) — installing the CLI, plugin management, scratch org definitions
- [05-experience · LWR sites](../05-experience-cloud-lwr/INDEX.md) — what `sf lightning dev site` previews
