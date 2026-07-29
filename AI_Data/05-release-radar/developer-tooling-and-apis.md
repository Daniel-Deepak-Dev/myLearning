# Developer tooling and APIs

MCP, Headless 360, Apex, LWC, CLI, IDEs. Newest entries at the top.

---

## 2026-07-29 · ADLC security testing is now generated from the agent, not from a catalogue

On **July 28, 2026** the [`agentforce-adlc`](https://github.com/SalesforceAIResearch/agentforce-adlc) toolkit merged five PRs. The one that changes how you work: **[`/agentforce-secure` is deleted](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/44)**, folded into `/agentforce-test` as **Mode C**.

The old skill shipped **57 static OWASP LLM Top 10 cases hard-coded around Salesforce-the-vendor**. Aimed at an airline complaint agent, it asked about citing Salesforce security bulletins while never testing rebooking without passenger verification. Mode C derives cases from the agent instead: it profiles the **Agent Script** for actions, authorization gates, LLM-filled inputs (injection sinks) and subagent topology, infers the **business domain** from 12 weighted vocabularies, then emits only cases that fit the actual surface — no write actions, no bulk-mutation tests. Of the 59-entry payload catalogue, **50 neutral entries deploy by default** and 9 Salesforce-platform entries need `--include-platform`.

Three sub-modes, ordered by blast radius: **`C1-author`** writes test YAML and deploys nothing; **`C1-run`** deploys and executes but **refuses non-sandbox orgs** unless given `--allow-production`, after a gate that queries `Organization.IsSandbox`; **`C2`** probes live via `sf agent preview` and returns severity-weighted A–F grades. **Live actions now require `--live-actions`; the default simulates.**

Also merged: a hook that **blocks `DELETE` without `WHERE` in quoted SOQL** ([#27](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/27)) — closing the gap where an LLM assembles a destructive query inside a string literal that static checks never see; **hooks gated to Salesforce projects only** ([#13](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/13)), so a global plugin install stops firing in unrelated repos; an **MCP server registry management skill** ([#41](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/41)); and **eight voice latency anti-patterns plus seven voice-safe action rules** ([#45](https://github.com/SalesforceAIResearch/agentforce-adlc/pull/45), docs only).

**Why it matters.** A security suite that doesn't know what your agent does is theatre — it returns green and means nothing. "Cases generated from the agent's own script and domain" is the answer that carries weight when a client asks how an agent was tested. Two patterns are worth copying regardless of this toolkit: **simulate by default, execute on an explicit flag**, and **validate generated queries at execution, not at authoring**. Caveat: CC BY-NC 4.0 research tooling, **not a supported Salesforce product**.

Full write-up: [01-agentforce/2026-07-29](01-agentforce/2026-07-29.md).

---

## 2026-07-29 · Data 360 MCP Server — ~200 REST operations behind three facade tools

[`forcedotcom/d360-mcp-server`](https://github.com/forcedotcom/d360-mcp-server) (announced **May 2026**, **Developer Preview**) exposes the Data 360 Connect API to MCP clients. **Distinct from Headless 360** below: that is the platform-wide Beta with ~100 skills; this is Data 360-specific and one maturity step behind.

The interesting move is architectural. Registering ~200 REST operations as ~200 MCP tools would consume the model's context before any work starts, so the server fronts everything with **three facade tools** — **`search`** (find operations by intent, keyword or family), **`payload_examples`** (fetch a working JSON payload), **`execute`** (run any operation by name). Behind them: **201 operations across 22 tool families** — DLOs, DMOs, streams, mappings, transforms, identity resolution, segments, queries, ML.

**Why it matters.** `payload_examples` is the pattern to steal: when a model must produce nested JSON for an unfamiliar API, **serve it a known-good example rather than a schema description** — hallucinated shapes are the default failure otherwise. Preview constraints rule it out of shared use: **STDIO only, single user/org per process, Java 17+ and Maven 3.9+ locally**. A **hosted GA version is planned for 2026**, no date confirmed. One governance flag: semantic search is powered by an **optional OpenAI API key**, so enabling it sends search terms to a third party — fine on a personal dev org, a conversation to have anywhere else.

Full write-up: [02-data-cloud/2026-07-29](02-data-cloud/2026-07-29.md).

---

## 2026-07-26 · Headless 360 — the organizing idea of Summer '26

[Headless 360](https://developer.salesforce.com/blogs/2026/05/headless-360-what-it-means-for-developers) makes every major Salesforce capability available as an **API, an MCP tool, or a CLI command**, accessible to any authenticated caller — an app, a human, or an autonomous AI agent.

**Why it matters.** Read this as Salesforce accepting that the primary consumer of its platform will increasingly be a machine rather than a browser. Every design choice below (hosted MCP, secrets redaction, user-mode defaults, scriptable grounding) follows from that premise. When you architect on Salesforce now, the question "can an agent do this without a UI?" has a real answer.

---

## 2026-07-26 · Salesforce Hosted MCP Servers (Standard servers GA)

Connect any MCP-compatible client — Claude, ChatGPT, Cursor, custom agents — to a Salesforce org through the open MCP standard. Every connection uses standard [OAuth](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/setup-overview.html). Salesforce hosts them, so there's no infrastructure to run.

### Standard servers (GA)

| Server | Capability |
|---|---|
| [SObject Servers](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/servers-reference.html#sobject-servers) | SObject CRUD, SOQL queries, search |
| [Data 360](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/references/reference/data-cloud-sql.html) | Data 360 queries and graph traversal |
| [Tableau](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/references/reference/tableau-next.html) | Analytics and visualization |

### Custom servers

When the standard servers aren't enough, [build custom MCP servers](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/custom-servers.html) with granular control over exposed tools and prompts. **Custom MCP servers respect the org's full sharing and security model** — this is the single most important sentence in the feature. Tools can be built from:

- **Apex Actions** — expose [`@InvocableMethod`](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/invocable-actions.html) methods
- **Lightning Flows** — expose autolaunched flows
- **Apex REST** — expose custom REST endpoints
- **`@AuraEnabled`** methods
- **[Named Query API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/resources_named_query_intro.htm)** — parameterized SOQL as a tool
- **[Prompt Builder](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/prompt-builder.html)** — prompts exposed as MCP prompts
- **[Agentforce](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/agentforce.html)** — whole agents exposed as MCP tools
- **[API Catalog](https://developer.salesforce.com/docs/platform/hosted-mcp-servers/guide/api-catalog.html)** — curated REST endpoints mapped to tools

**Why it matters.** This is the most directly relevant Salesforce feature to the Claude/MCP track. It also inverts a familiar problem: instead of building an MCP server to *reach* Salesforce, you configure one and Salesforce enforces sharing and FLS for you. Walkthroughs: [Connect Claude with Salesforce Hosted MCP Servers](https://developer.salesforce.com/blogs/2026/05/connect-claude-with-salesforce-hosted-mcp-servers) and [Expose Custom Apex as a Hosted MCP Tool for Agents](https://developer.salesforce.com/blogs/2026/05/expose-custom-apex-as-a-hosted-mcp-tool-for-agents).

**Study action:** connect Claude Desktop or Claude Code to a Dev Edition org via a standard SObject server, then expose one `@InvocableMethod` as a custom tool. That single exercise covers both the CCA-F and Agentforce tracks.

---

## 2026-07-26 · MCP servers for developers and designers

| Server | Status | What it gives you |
|---|---|---|
| [Salesforce DX MCP](https://developer.salesforce.com/docs/atlas.en-us.sfdx_dev.meta/sfdx_dev/sfdx_dev_mcp.htm) | Beta | [SLDS Guideline tools](https://developer.salesforce.com/docs/platform/lwc/guide/mcp-slds.html) for styling-hook and component-blueprint guidance; [ApexGuru](https://developer.salesforce.com/blogs/2026/04/performance-first-apex-development-with-apexguru-in-salesforce-dx-mcp-server) for Apex review driven by your org's *runtime* metrics |
| [Metadata API Context MCP](https://developer.salesforce.com/docs/atlas.en-us.api_meta.meta/api_meta/meta_salesforce_api_mcp_intro.htm) | Beta | Now five granular tools instead of one — faster responses, more efficient token usage |
| [Data 360 MCP](https://developer.salesforce.com/blogs/2026/05/introducing-the-data-360-mcp-server-developer-preview) | Dev Preview | Three facade tools over ~200 REST ops (see [data-360.md](data-360.md)) |
| [Omnistudio MCP](https://developer.salesforce.com/blogs/2026/01/accelerate-flexcard-development-with-omnistudio-mcp) | Beta | Turn text, screenshots or UX mockups into FlexCard templates |
| [B2C DX MCP](https://salesforcecommercecloud.github.io/b2c-developer-tooling/mcp/) | — | Figma-to-Component for Storefront Next |
| [Marketing Cloud Engagement MCP](https://developer.salesforce.com/blogs/2026/06/the-mcp-server-for-marketing-cloud-engagement-is-now-ga) | GA | Data extensions and journeys as natural-language tools |

**ApexGuru is the standout.** It flags anti-patterns inline — SOQL/DML inside loops, redundant SOQL — using *actual runtime metrics from your org*, not static analysis. Its Test Case Insights surface inefficient tests that drag coverage down.

---

## 2026-07-26 · Agent Skills for coding agents (open source)

[Agent Skills](https://agentskills.io/home) is a lightweight open format for extending an AI agent with specialized knowledge and workflows. Salesforce open-sourced a library of Salesforce development skills at [github.com/forcedotcom/sf-skills](https://github.com/forcedotcom/sf-skills).

Install into any coding agent: `npx skills add forcedotcom/sf-skills` (pre-packaged with Agentforce Vibes; works with Claude Code, Codex, etc.)

Includes skills for [building](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-agentforce), [testing](https://github.com/forcedotcom/sf-skills/tree/main/skills/testing-agentforce) and [observing](https://github.com/forcedotcom/sf-skills/tree/main/skills/observing-agentforce) Agentforce, plus [Data 360 code extensions](https://github.com/forcedotcom/sf-skills/tree/main/skills/developing-datacloud-code-extension).

**Why it matters.** Same skill format Claude Code uses — these drop straight into your existing setup. This is the highest ratio of value to effort in the whole release.

---

## 2026-07-26 · Salesforce CLI — Agentforce DX and credential safety

**Build agents from a working start:**

- **Agent project scaffolding** — the `agent` template generates a runnable **Local Info Agent** demonstrating Apex, Prompt Template and Flow subagents.
- **One-command agent user** — automates service agent user setup, no manual provisioning.

**Test, preview, debug:**

- **Agent preview is GA** — script interactive test sessions end to end with `agent preview start`, `send`, `sessions`, `end`.
- **Trace files** — inspect traces from a preview session to see exactly how the agent routed and acted.
- **Richer evaluations (Beta)** — YAML- or JSON-defined evaluation tests for repeatable agent testing.

**Credential safety:**

- **Secrets redacted by default** — access tokens, SFDX auth URLs and passwords are stripped from `org display`, `org list --json` and similar, preventing leaks in CI logs.
- **Deliberate retrieval** — when you actually need a credential you must ask for it explicitly.

Details: [Salesforce CLI release notes](https://github.com/forcedotcom/cli/blob/main/releasenotes/README.md). The CLI ships weekly.

---

## 2026-07-26 · Platform API v67.0

- **GraphQL chaining** — [mutations](https://developer.salesforce.com/docs/platform/graphql/guide/mutations-intro.html) can now reference *any field* returned by an earlier operation in the same request, not just its record ID. Use `@{ref.Record.FieldName.value}` for a field value and `@{ref.Record.Id}` (shorthand `@{ref}`) for the ID. Linked records in one round trip.
- **JWT tokens for SOAP API** — SOAP now accepts [JWT-based access tokens](https://help.salesforce.com/s/articleView?id=release-notes.rn_api_soap_jwt.htm&release=262&type=5) in the `sessionId` header, reaching parity with REST auth.
- **Connect REST API limits relaxed** — orgs migrated off the restrictive per-user/per-app/per-hour limit onto the [per-org, per-24-hour Platform API limit](https://help.salesforce.com/s/articleView?id=release-notes.rn_connect_api.htm&release=262&type=5). Only Chatter-requiring requests keep the hourly throttle. Same change applies to Connect in Apex.
- **CSRF token for UI API** — new [`GET /ui-api/session/csrf`](https://developer.salesforce.com/docs/atlas.en-us.uiapi.meta/uiapi/ui_api_resources_session_csrf.htm) resource.

See [trust-security-and-governance.md](trust-security-and-governance.md) for the SOAP `login()` retirement, which is the most consequential API change.

---

## 2026-07-26 · Apex at API 67.0 — ergonomics

Security changes are in [trust-security-and-governance.md](trust-security-and-governance.md). The quality-of-life additions:

- **Multiline strings** — triple single-quotes (`'''`) give real [multiline literals](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_multiline_string.htm&release=262&type=5). No more `+ '\n' +` chains for JSON payloads, email bodies or SOQL. *The newline immediately after the opening `'''` is trimmed.*
- **[`String.template()`](https://developer.salesforce.com/docs/atlas.en-us.apexref.meta/apexref/apex_methods_system_string.htm#apex_System_String_template)** — named interpolation with `${variableName}`, replacing the index-juggling of `String.format()`. *Renders a `Datetime` in **GMT** as `yyyy-MM-dd HH:mm:ss`, not the user's local time the way `String.valueOf()` does — format it yourself if the zone matters.*
- **Elastic limits for async jobs (Beta)** — enqueue `Queueable` and `@future` jobs [up to twice your licensed daily limit](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_elastic_async_limit.htm&release=262&type=5); overflow is throttled, not rejected. Track via `DailyAsyncApexElasticExecutions` and `DailyAsyncApexProcessed` in `System.OrgLimits.getMap()`.
- **No-arg constructors required** — any custom Apex type used as an [invocable action input](https://help.salesforce.com/s/articleView?id=release-notes.rn_apex_constructor_visibility_invocable_custom_classes_v66.htm&release=262&type=5) must expose a visible no-argument constructor (public, or global for packaged classes) at API 67.0+. **This one breaks existing Agentforce Apex actions** — check your invocable input classes.

---

## 2026-07-26 · LWC — a maturity release

Five features most likely to change how you build:

**1. State Managers (GA)** — the most consequential. [State Managers](https://developer.salesforce.com/docs/platform/lwc/guide/state-management.html) move data and the logic that mutates it *out* of components into a reusable, testable layer. Build one as a plain JS module with `defineState` from `@lwc/state`:

- `atom(value)` — reactive state, read through `.value`
- `computed([deps], fn)` — derived value, recomputes when a dependency changes
- `setAtom(atom, value)` — the **only** way to update an atom

`defineState` returns a **factory**; each call yields a fresh independent instance, which makes managers trivially unit-testable. Salesforce also ships [built-in Lightning state managers](https://developer.salesforce.com/docs/platform/lwc/guide/reference-state-managers.html) wrapping LDS access to common UI API data (`lightning/stateManagerRecord`, `lightning/stateManagerObjectInfo`, etc.) — they participate fully in LDS caching, normalization and subscriptions, so reach for those before rolling your own. Runnable examples in [lwc-recipes](https://github.com/trailheadapps/lwc-recipes/tree/main/force-app/main/default/lwc/opportunitiesStateManager).

**2. `lightning/accApi` — drive Agentforce from a component.** The [Agentforce Conversation Client API](https://developer.salesforce.com/docs/platform/accsdk/guide/acc-api.html) is a *headless* module that lets an LWC drive the native Agentforce side panel in Lightning Experience. Three async methods, all returning a `Promise` and **queued** to run in sequence:

| Method | Purpose |
|---|---|
| `open(botId?)` | Open the side panel, optionally to a specific agent |
| `close()` | Close the side panel |
| `execute(utterance, botId)` | Run a natural-language utterance on an agent |

**`execute` does *not* return the reply** — the conversation renders in the panel, not in your component. Expose `botId` as a design-time property (`<property name="botId" type="String">` in the bundle's `.js-meta.xml` `targetConfig`) so admins can wire the agent without code. Get `botId` from the URL in Agentforce Builder. Think "Summarize this record" buttons and context-aware console launchers.

**3. Dynamic lists (Developer Preview)** — [`lightning-dynamic-list-container`](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-dynamic-list-container.html?type=Example) and [`lightning-dynamic-list-item`](https://developer.salesforce.com/docs/platform/lightning-component-reference/guide/lightning-dynamic-list-item.html) use virtualization to render only viewport rows and stream the rest — 50 items to 5,000. Fires `renderlistitems` on scroll and `loadmore` near the end. Includes focus preservation and built-in accessibility. *Keep container and item adjacent, give every item a unique `item-id`, and don't set `overflow: scroll` on your own container — the component handles scrolling.*

**4. API 67.0 niceties** — faster, more memory-efficient hot module reloading, and you can group native `<details>` elements with the `name` attribute for a zero-JavaScript exclusive accordion (same `name` = only one open at a time). Set `<apiVersion>67.0</apiVersion>` in the bundle `.js-meta.xml`.

**5. Secure downloads — LWS now blocks `data:` URIs.** `HTMLAnchorElement.prototype.href` blocks the `data:` scheme. **If you trigger client-side downloads by setting an anchor's `href` to a `data:` URL, that breaks.** Fix: build a Blob and use a `blob:` object URL (origin-bound, revoke after use). Other new [distortions](https://help.salesforce.com/s/articleView?id=release-notes.rn_lc_lws_distortion_changes.htm&release=262&type=5) cover `Element.getAttribute`, `innerHTML`/`outerHTML` getters, `MutationObserver.observe`, the `IndexedDB` factory and `Promise.then/catch/finally`. Run the updated [ESLint package](https://developer.salesforce.com/docs/platform/lightning-components-security/guide/lws-tools-lint.html) and check the [LWS Distortion Viewer](https://developer.salesforce.com/tools/lws-distortion-viewer) before upgrading components.

---

## 2026-07-26 · IDEs and pro-code environments

- **[Agentforce Vibes 2.0 (Developer Preview)](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-agentforce-vibes-2)** — agentic development environment that reasons through complex tasks, builds structured implementation plans and asks clarifying questions before acting. You keep control via approvals, permissions and native VS Code diff reviews. New: redesigned multi-tab chat, **Plan Mode**, deeper MCP integration, built-in Skills and Rules, live LWC previews, and the latest Claude and GPT models in one picker.
- **[Web Console (Beta)](https://developer.salesforce.com/docs/platform/webconsole/guide/get-started)** — a full IDE running inside your org in the browser. Write, debug and deploy Apex, LWC and other metadata without leaving Salesforce; run anonymous Apex, set trace flags and debug log levels in one place. vs. the Agentforce Vibes IDE: available on **every** org, loads faster, entirely browser-based — but supports only Salesforce-provided extensions. Enable under Setup → Development → Web Console (Beta).
- **[Live Preview VS Code extension](https://developer.salesforce.com/docs/platform/lwc/guide/get-started-test-components.html)** — the renamed Local Dev. Real-time single-component updates in the browser, VS Code, or the Agentforce Web IDE.
- **[Metadata Visualizer](https://marketplace.visualstudio.com/items?itemName=salesforce.salesforcedx-metadata-visualizer-vscode)** — turns raw metadata XML into interactive diagrams that update as you edit; plugs into Agentforce Vibes to visualize AI-generated metadata. Currently covers objects, permission sets and flexipages (Beta).

---

## Release timing reference

Summer '26 sandbox preview **May 8, 2026**; production rollouts **May 15, June 5, June 12, June 13, 2026** depending on instance. API version **67.0**. Check the [maintenance calendar](https://status.salesforce.com/products/all/maintenances) for your org. Winter '27 release notes are not yet public; Release Update **enforcement** begins September 2026.

---

## Sources

- [The Salesforce Developer's Guide to the Summer '26 Release](https://developer.salesforce.com/blogs/2026/06/the-salesforce-developers-guide-to-the-summer-26-release)
- [Headless 360: What It Means for Developers](https://developer.salesforce.com/blogs/2026/05/headless-360-what-it-means-for-developers)
- [Salesforce Summer '26 Release Notes](https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.salesforce_release_notes.htm)
- [Salesforce Winter '27 Release: What to Expect (Salesforce Ben)](https://www.salesforceben.com/salesforce-winter-27-release-what-to-expect-and-how-to-prepare/)
