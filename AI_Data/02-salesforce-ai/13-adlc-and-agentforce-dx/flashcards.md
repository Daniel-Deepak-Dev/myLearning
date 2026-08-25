# ADLC & Agentforce DX — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: Name the five phases of the Agent Development Lifecycle.
A: Ideation and Design; Development (the inner loop); Testing and Validation; Deployment; Monitoring and Tuning (the outer loop).

Q: What is the difference between the inner loop and the outer loop?
A: The inner loop is the tight build-and-try cycle a developer runs many times a day. The outer loop is the slow, continuous cycle of monitoring production, learning from it and feeding improvements back into the agent.

Q: What makes ADLC different from a traditional SDLC?
A: It is a closed-loop learning system that manages drift in a system whose behaviour is not fully specified by its source. Deployment is day one rather than the finish line, drift is expected rather than a defect, and cost is a test result — token economics are analysed during testing so cost failures are caught before production.

Q: In which ADLC phase do token economics get analysed, and why there?
A: Testing and Validation. Analysing cost during the rapid prompt-test-evaluate cycles is what stops a working agent from turning out to be an unaffordable one after it ships.

Q: How do you install the Salesforce Agent Skills, and what are the prerequisites?
A: `npx skills add forcedotcom/sf-skills`, with Node.js and the Salesforce CLI installed.

Q: Name the three Agentforce Agent Skills and what each covers.
A: `developing-agentforce` (design, build, deploy, publish), `testing-agentforce` (preview smoke tests and YAML batch regression), and `observing-agentforce` (production trace queries against the Session Trace Data Model).

Q: What are the build-and-deploy commands in the skill-driven workflow?
A: `sf agent generate authoring-bundle` to scaffold, validate that Agent Script compiles locally, `sf project deploy start` to deploy the backing Flow and Apex, then deploy the authoring bundle. Deployment failures drive automated fix-and-retry loops.

Q: What are the test commands, and what is each for?
A: `sf agent preview start` / `send` / `end` for quick interactive smoke tests, and `sf agent test create` / `run` for repeatable batch regression against YAML test specs.

Q: How do you publish and activate an agent from the CLI?
A: `sf agent publish authoring-bundle`, then `sf agent activate`.

Q: Where do local traces live, and how do you see production ones?
A: Locally in `.sfdx/agents/[name]/sessions/…/traces/`. In production, the `observing-agentforce` skill queries the Session Trace Data Model, and the AgentLens visualizer walks the graph.

Q: What are the five workflow rules from the first-party ADLC guide?
A: Keep each project in its own folder; build only in scratch orgs or sandboxes, never production; commit Agent Script to Git; use `--json` on all commands for machine-readable output; and scope deployments explicitly so unrelated metadata isn't shipped.

Q: Why is "design-first" more than a slogan in this workflow?
A: Because the recommended flow starts in plan mode with the assistant interviewing you about architecture before anything is generated — mapping the agent as a graph with a router node and domain subagents. The specification is what the model actually executes, so writing it first is the work, not the preamble.

Q: What are the licences of Agent Script, sf-skills and agentforce-adlc, and why does the difference matter?
A: Agent Script is Apache 2.0. `forcedotcom/sf-skills` is Salesforce's supported library. `SalesforceAIResearch/agentforce-adlc` is CC BY-NC 4.0 — non-commercial, which means it cannot be used on paid client work. Three artifacts, three licences.

Q: What are the four skills in the agentforce-adlc repo?
A: `/agentforce-generate`, `/agentforce-test`, `/agentforce-observe`, and `/agentforce-secure`, the last being an OWASP LLM Top 10 assessment of the agent.

Q: What is the status of Agentforce Vibes 2.0, and what does a Developer Edition org get?
A: Developer Preview. Since April 2026 every Developer Edition org includes the Agentforce Vibes IDE, Claude Sonnet 4.5 as the default coding model, and Salesforce hosted MCP servers, at no cost.

Q: Which is GA and which is Beta — `agent preview` or agent evaluations?
A: `sf agent preview` is GA. YAML/JSON agent evaluations are Beta.

Q: Why is "drift has no commit" a useful phrase to remember?
A: Because nothing changes in version control when an agent degrades — the model, the data and user phrasing change underneath it. An agent that was good in March can be mediocre in July with no code change in between, so only the outer loop catches it.

Q: What trap does the `agentforce-adlc` repository illustrate about GitHub activity?
A: Its listing showed "updated July 28, 2026" while `main` had no commits since July 24 and no published releases at all. The Updated column reflects repository metadata, not code — verify against `commits/main.atom` and `releases.atom` before treating it as real activity.

Q: Why is ADLC the strongest overlap between the Agentforce track and the Claude CCA track?
A: Agent Skills use the same open format that Claude Code uses, so driving an Agentforce agent through the full lifecycle from Claude Code advances preparation for the Agentforce Specialist exam and the CCA-F at the same time.

Q: The three `agentforce-*` skills exist in two public repos. Which one may you use on paid client work, and why?
A: `forcedotcom/sf-skills` — Apache-2.0 since 2026-06-29. `SalesforceAIResearch/agentforce-adlc` is CC BY-NC 4.0, which forbids commercial use. The content and versions are identical; the licence attaches to the copy you took, not to the skill.

Q: What is the release cadence of `forcedotcom/sf-skills`?
A: Weekly, on Fridays. 1.33.0 shipped 2026-07-31 with 10 new and 16 updated skills.

Q: What do the `accessCheck` and `cliTools` fields in an Agent Skill's frontmatter do?
A: They declare preconditions — `accessCheck` names the required org permission (e.g. `ManageSandboxes`), `cliTools` the required local CLI — so the skill fails fast with a clear message instead of dying inside a REST call.

Q: Which skill stands up a Help Agent, and what API version floor does it declare?
A: `service-helpagent-coordinate` (0.9), a guided four-checkpoint flow — setup, channel configuration, Knowledge grounding, go-live. It declares `minApiVersion: "67.0"`, a higher floor than `agentforce-generate`'s `66.0`.

Q: Why is an Agent Skill's version number a poor change indicator?
A: `agentforce-observe` shipped in sf-skills 1.33.0 at the same `0.8` it carried in the earlier `agentforce-adlc` sync. Track the release tag and the commit, not the skill version.

Q: SDR 13.0.1 fixed a zip-slip. Why can a team on the stable `sf` channel not have the fix?
A: There is no 12.x backport — the newest 12.x is 12.37.2 (2026-07-13). `@salesforce/plugin-deploy-retrieve` 3.x pins SDR `^12.36.7`, a range that can never resolve to a patched build. Only plugin 4.x pins `^13.0.0`, and it ships in CLI 2.147.x, which requires Node ≥ 22.

Q: What is a zip-slip, and which Salesforce code path had one?
A: An archive entry whose stored path escapes the target directory (`../../../.git/hooks/pre-commit`), so extraction writes outside it. In `staticResourceMetadataTransformer.ts`, which unzips static resources of `contentType` `application/zip` or `application/jar` during metadata→source conversion — i.e. `sf project retrieve start`.

Q: Why is `npm view @salesforce/cli dist-tags` worth running before you claim your CLI is current?
A: dist-tags are not ordered by version. As of 2026-08-03, `latest` is 2.145.6, `latest-rc` 2.146.3 and `nightly` 2.147.4. A plain `npm install -g @salesforce/cli` follows `latest`, so the newest published version and the version you get are different.

Q: Does waiting for the next stable `sf` CLI get you the zip-slip fix?
A: No. `latest-rc` 2.146.3 pins `plugin-deploy-retrieve` 3.24.61 → SDR `^12.36.7` → 12.37.2, unpatched. Promoting the current release candidate would ship an unpatched stable. The fix sits on the other side of the Node 22 major, not further down the release pipeline.

Q: What is the security lesson from the SDR zip-slip that outlives the specific bug?
A: `sf project retrieve` is an **inbound** trust boundary. It takes org-controlled bytes — which a packaging partner, a compromised sandbox or an agent with metadata write access can influence — and writes them onto a developer laptop or CI runner.

Q: Which sf CLI version first required Node 22, and what else came with it?
A: **2.147.0** (2026-07-31 14:16 UTC) — not 2.147.3, which was merely the version on `nightly` when an earlier scan read the tag. The 2.147 line carries `engines.node >=22.0.0`, `@salesforce/core ^9.0.0`, `@salesforce/plugin-agent` 2.0.0 and `@salesforce/plugin-deploy-retrieve` 4.0.1. You cannot take the security patch without taking all of it.

Q: What is `relatedSkills` and why does it change how an agent picks a skill?
A: A bidirectional list of sibling skill names in SKILL.md frontmatter under `metadata:`, added across 79 skills in sf-skills 1.34.0 (2026-08-07). It turns the catalogue into a graph the agent can traverse rather than re-searching descriptions each time — selection becomes navigation.

Q: Name the three structural metadata fields sf-skills added in late July / early August 2026, and what each declares.
A: `cliTools` (2026-07-30) — the local CLI a skill needs; `accessCheck` (2026-07-31) — the org permission it needs, so it fails fast; `relatedSkills` (2026-08-07) — its neighbours in the catalogue graph.

Q: What breaking change hid inside the sf-skills release titled "79 updated skills"?
A: `automation-flow-generate` raised its minimum API version from 51.0 to 60.0. A sandbox or managed package pinned below 60.0 loses the skill, with nothing in the release title to warn you.

Q: On 2026-08-05 the `sf` CLI `latest` dist-tag moved from 2.145.6 to 2.146.3. Did that fix the SDR zip-slip?
A: No. 2.146.3 pins `@salesforce/plugin-deploy-retrieve` 3.24.61, which pins SDR `^12.36.7` and resolves to the unpatched 12.37.2. The stable channel advanced and stayed vulnerable — so a newer CLI version is actively misleading evidence.

Q: What is the fastest reliable check that your `sf` install has the patched SDR line?
A: Read the resolved SDR version, not the CLI version — `npm ls @salesforce/source-deploy-retrieve` — or check `engines.node`: `>=18.6.0` means the unpatched 12.x line, `>=22.0.0` means 13.x.

Q: npm dist-tags moved without any package being published. How do you spot that?
A: The registry's package-level `modified` timestamp advances while no new version appears in `time`. For `@salesforce/cli` on 2026-08-05, the newest publish was 2.147.7 at 03:24 UTC but `modified` read 18:41:04 UTC — that gap is the tag move.

Q: On 2026-08-06 the `sf` CLI `latest` dist-tag moved from 2.145.6 to 2.146.3. Did that ship the SDR zip-slip fix?
A: No. 2.146.3 is the previous release candidate promoted unchanged — still `engines.node >=18.6.0`, still pinning `@salesforce/plugin-deploy-retrieve` 3.24.61, which pins SDR `^12.36.7` and resolves to the unpatched 12.37.2. "I am on the newest stable" became a true statement that is also unpatched.

Q: Which dist-tag now carries the patched SDR, and what does taking it cost you?
A: `latest-rc`, now 2.147.7 — the Node 22 line promoted up from `nightly`. It requires `engines.node >=22.0.0` and `@salesforce/plugin-deploy-retrieve` 4.0.1 (SDR `^13.0.0` → 13.0.1). The patch is only reachable through a Node-major upgrade; there is still no 12.x backport.

Q: After `sf-pi` v0.258.0, a fresh CI container shows zero gateway models. Bug or expected?
A: Expected. ADR 0077 removed the bundled catalogue: model IDs come only from authenticated discovery, cached per provider, so an uncached provider exposes no models until discovery succeeds. Do not add a fallback list — that is exactly what was deleted.

Q: What is the general lesson behind deleting `sf-pi`'s bundled model catalogue?
A: A hardcoded inventory of a remote system's capabilities is a cache with no invalidation. It drifts silently and lies most convincingly when you are least authenticated — so the tool looks configured before it is authenticated, and the credential failure surfaces later as something else.

Q: `sf-pi` shows a saved configuration override. Are you authenticated?
A: Not necessarily. Since v0.259.1 setup persists overrides without awaiting the network, and status output deliberately distinguishes a saved override from an active authenticated provider. Reading one as the other is the new misread; discovery failure hands off to Doctor.

Q: What does the `sf-data360` extension in `sf-pi` expose, and what does it deliberately not use?
A: Eleven LLM tools — `data360_discover`, `_connect`, `_prepare`, `_harmonize`, `_segment`, `_activate`, `_query`, `_semantic`, `_observe`, `_orchestrate`, plus `data360_api` as a REST escape hatch. It uses no MCP runtime and no Java subprocess, routing through sf-pi's shared action registry instead.

Q: Is `sf-data360` the same thing as the Data 360 MCP Server?
A: No. Same domain, different mechanism — the MCP Server is a Developer Preview MCP server with three facade tools over ~200 REST operations; `sf-data360` is a default-enabled sf-pi extension with no MCP runtime at all.

Q: Why will grepping `sf-skills` never find `sf-data360`?
A: It ships plain reference docs rather than contributing Agent Skills, so the skills catalogue has no record of it.

Q: What does the `pi-credential-output` guardrail rule gate?
A: `pi auth check --credentials`, `pi auth print-api-key` and `pi auth print-bearer-token`, plus the `SF_TEMP_SHOW_SECRETS=true` pattern. Plain `pi auth check` is unaffected.

Q: Why does `sf-guardrail` match on the parsed command rather than the string?
A: Because a text match is defeated by `sudo`, `bash -c`, `timeout`, an environment prefix or an `npx` wrapper — by accident long before anyone attacks it. Structural detection resolves all those forms to the same rule.

Q: What is the trap in choosing "Allow for this session" on a guardrail prompt?
A: The grant persists via `pi.appendEntry` and is inherited by `/resume` and `/fork`, so it outlives the session you granted it in. Clear it with `/sf-guardrail forget`; review decisions with `/sf-guardrail audit`.

Q: Where does the effective `sf-guardrail` config live, and why does that matter on a team?
A: In `~/.pi/agent/sf-guardrail/rules.json`, outside the repo. `SF_GUARDRAIL_DEFAULTS.json` is only what ships — so one developer disabling a rule by ID is invisible to everyone else.

Q: `sf-pi` reports an org's API version as `50.0`. What does that most likely mean?
A: Not that the org is on 50.0 — it means nothing was configured and JSforce used its built-in default (Spring '21). Since v0.262.1 sf-pi labels this "unverified SDK fallback" rather than reporting it as an observed org fact.

Q: What are the three API-version provenance states sf-pi now distinguishes?
A: `configured` (an explicit `org-api-version` override), resolved from the Project Source API (`sourceApiVersion` in `sfdx-project.json`), and unverified SDK fallback (JSforce's `50.0` default).

Q: What is the difference between Project Source API and Connection API?
A: Project Source API comes from `sourceApiVersion` in `sfdx-project.json` and governs the shape of metadata deploy and retrieve. Connection API is what the SDK selected for REST calls. They are separate fields and are allowed to disagree.

Q: Why does an unverified `50.0` fallback matter beyond cosmetics?
A: Platform defaults are version-gated. At API 67.0 Apex DML and SOQL run in user mode and classes default to `with sharing`. Operating at 50.0 while believing you are at 67.0 means reasoning about behaviour you do not have.

Q: sf-pi's environment status looks stale. How do you force the truth?
A: Snapshots are cache-first by design; run `/sf-org refresh` or `/sf-devbar refresh`, which call `refreshSharedSfEnvironment()` for an explicit serialized deep refresh.

Q: In `sf-pi` v0.263.0, what wins when the org advertises API 68.0 and you have `org-api-version=60.0` configured?
A: 68.0. `sf-conn` treats discovery as authoritative and configuration as the fallback — the inverse of the usual precedence. `org-api-version` is consulted only when the `/services/data` catalog request fails.

Q: What does `sf-pi` v0.263.0 do when API-version discovery fails and no `org-api-version` is configured?
A: It rejects the operation before sending the business request. The JSforce `50.0` implicit default is no longer used as an authoritative value — v0.262.1 labelled that fallback, v0.263.0 removed it.

Q: Why does a Data 360 raw REST call through `sf-pi` fail after v0.263.0 if it passes `/services/data/v63.0/ssot/...`?
A: Callers must now pass versionless resource paths. `lib/common/sf-conn/path.ts` constructs the versioned path itself; a caller-owned `/services/data/vNN.N` segment is rejected rather than rewritten.

Q: A `sf-conn` request returns 403. Will it be retried after an auth refresh?
A: No. Only a definite expired session triggers the shared authentication refresh. An ordinary permission 403 is not replayed — it is a permissions problem, not an auth problem.

Q: What does `bypassUser` control, and which value belongs to an employee agent?
A: Which identity the agent session runs under. `bypassUser: false` for employee agents (`AgentforceEmployeeAgent`), which run as the authenticated Salesforce user; `true` for customer-facing agents, which run with no user identity. Sharing, FLS, `UserInfo` and record ownership follow from it.

Q: `sf agent preview start --api-name <employee agent>` returns `400 Invalid user ID`. What is wrong?
A: Not authentication. Before `@salesforce/agents` 2.0.1 the `--api-name` path hard-coded `bypassUser: true` for every agent type, so the Agent API rejected employee-agent sessions. The `--authoring-bundle` path already branched correctly, which is why the same agent previewed fine locally.

Q: Why can a team on stable `sf` 2.146.3 not get the `@salesforce/agents` 2.0.1 fix?
A: `latest` 2.146.3 ships `@salesforce/plugin-agent` 1.45.0, which pins `@salesforce/agents ^1.11.1` — a range capping at 1.11.7 that no 2.x build satisfies. The fix needs `latest-rc` 2.147.7 or `nightly` 2.148.1 (plugin-agent 2.0.0, `^2.0.0`), which also raise the Node floor to 22.

Q: `@salesforce/agents` 2.0.1 shipped on 2026-08-10. What had to happen before it could reach anyone through the CLI, and had it by 2026-08-12?
A: Two more publishes. `@salesforce/plugin-agent` 2.0.1 (2026-08-11 15:32 UTC) had to pin `@salesforce/agents ^2.0.1`, then `@salesforce/cli` 2.148.3 (2026-08-12 03:13 UTC) had to pin that plugin. Both happened — but 2.148.3 is on `nightly`. `latest` was still 2.146.3 for a sixth day.

Q: What are the two ways to consume `forcedotcom/sf-skills`, and what do you get from each?
A: `npx skills add forcedotcom/sf-skills` takes the **catalogue** — SKILL.md instructions only. `/plugin marketplace add forcedotcom/sf-skills` then `/plugin install salesforce-development@salesforce` takes the **runtime** — 41 skills plus five agents, three MCP servers, ten slash commands and hooks on eight events.

Q: In what order does the `salesforce-development` plugin resolve a capability, and what does the order say about Salesforce's own MCP servers?
A: Skills (primary) → Salesforce CLI (secondary) → Salesforce MCP (last resort). Salesforce ranks deterministic instructions above its own CLI, and its own CLI above its own hosted MCP servers — MCP is the fallback, not the front door.

Q: The `salesforce-development` plugin declares `"dependencies": []`. What do you actually have to install?
A: Claude Code ≥ 2.1.222, the Salesforce CLI, Node LTS (the bundled Apex and SOQL language servers run under `node`) and Python 3.8+ (the org-detection, deploy-safety and `agent-validator.py` hooks are Python). The empty array is the plugin's *plugin* dependencies, not its prerequisites.

Q: Which agents does the `salesforce-development` plugin ship for the ADLC, and how do they divide the work?
A: `adlc-orchestrator` is a plan-mode lifecycle coordinator delegating to `adlc-author` (writes `.agent` files), `adlc-engineer` (scaffolds Flow/Apex and deploys bundles) and `adlc-qa` (tests, optimizes and security-assesses). Alongside them: `salesforce-dev` and the read-only `architecture-review`.

Q: Why is the "Test" stage of the plugin's discovery journey different after 1.10.0?
A: It only completes after a real, successful Apex test run. Previously the journey could mark progress that had not actually happened. Inspect or clear it with `/salesforce-development:discovery journey inspect` / `journey reset`.

Q: What is the security change in `salesforce-development` 1.10.0?
A: Capability discovery no longer discloses descriptions of skills you have not installed. Only skills verified as installed **and unmodified** reveal their descriptions.

Q: You edit a file under `force-app/` in a session with the `salesforce-development` plugin installed. What runs?
A: A `PostToolUse` hook invokes `sf-deploy-gate auto-deploy` on `Edit`/`Write`/`MultiEdit` matching `force-app/**`, plus the `.agent` syntax validator on any `Write`/`Edit`. Metadata edits are not inert in that session.

Q: Are the eleven `data360_*` tools eleven endpoints?
A: No. Per sf-pi ADR 0027 (2026-06-01) they are **family tools over one shared action registry and dispatcher**, each called with an action string (`stream.create_ingest_api`, `sql.verify_rows`, `ingest_csv.plan`) plus `params`, `target_org`, `dry_run`, `allow_confirmed` and `output_mode`. The flat-facade shape was the legacy `d360` surface they replaced.

Q: Where do you look up a valid `data360_*` action name, and why not the tool schemas?
A: The generated-but-committed action map at `extensions/sf-data360/registry/v2/actions.json`, or the meta actions `actions.search` / `action.describe` / `examples.get`. Tool schemas stay deliberately small — catalogues load only after intent, to keep the prompt footprint bounded.

Q: What does sf-pi require before it will run a headless destructive Data 360 action (ADR 0106)?
A: All four: an authenticated **non-production** target, `--mutate`, an 8–32-character alphanumeric run ID, and both env gates `SF_PI_D360_V2_SWEEP_MUTATION_TARGET_ORG` and `D360_V2_SWEEP_ALLOW_DESTRUCTIVE`. Only the DLO name derived from that run ID may be deleted.

Q: After ADR 0106, how many destructive-safety rules does `sf-data360` have?
A: Two. The legacy facade keeps its dedicated-target rule for legacy callers; v2 **interactive** destructive calls need a non-production authenticated target plus explicit acknowledgement plus human confirmation. Production, unresolved and mismatched targets are blocked on both paths.

Q: What API version is Winter '27, and where was it confirmed?
A: **68.0**. Confirmed from the `## Next Release (v68)` section of `METADATA_SUPPORT.md` in `forcedotcom/source-deploy-retrieve` — a generated coverage report in a repo, not an org endpoint or a release note. It lists 59 new v68 metadata types: 21 DX-supported, 37 not, 1 partial.

Q: Name the three metadata layers of an Agentforce agent after v68.
A: **Authoring** — `AiAuthoringBundle` (API 65+, `aiAuthoringBundles/<name>/`, XML plus an `.agent` Agent Script file). **Runtime** — `AiAgentDefinition` and `AiAgentDefinitionVersion` (new in v68), with `Bot`/`BotVersion` as the legacy runtime. **Reasoning** — `GenAiPlannerBundle`, `GenAiPlugin`, `GenAiFunction`, `GenAiPromptTemplate`.

Q: What is odd about `AiAgentDefinitionVersion`'s registry entry?
A: It has **no `suffix`**. It uses the `bundle` adapter with `strictDirectoryName: true`, so it is a directory under `aiAgentDefinitionVersions/` whose folder name *is* the API name — renaming the folder renames the component. Its sibling `AiAgentDefinition` is a single file (`aiAgents/`, suffix `aiAgentDefinition`) with `strictDirectoryName: false`.

Q: What are the only two legal values of `rootTypesWithDependencies`, and why does the pair matter?
A: `Bot` and `AiAgentDefinitionVersion`. Both are roots from which a whole agent's dependent metadata is retrieved — which is the clearest evidence that the v68 pair is the successor to `Bot`/`BotVersion` rather than a side feature.

Q: Which agent-adjacent v68 metadata types can DX *not* deploy or retrieve?
A: `AiAgentDefinitionPlanner`, `BotEmailDefinition`, all four telephony-provider types (`TelephonyProvider`, `SecondaryTelephonyProvider`, `TrustedTelephonyProvider`, `ScndTelephPrvdOtbdDtl`) and three security types (`SecurityCustomBaseline`, `ScopedAccess`, `SensitiveDataRuleElmntGrp`). `AiAgentScorerDefinition` is partial — deploy/retrieve works, **source tracking does not**.

Q: `sf` `latest` sat at one version for six days. Stall or schedule?
A: Schedule. The CLI release notes state that stable ships **on Wednesdays**, with that week's release candidate published the same day, so an RC soaks about a week before promotion. 2.147.7 published to npm on 2026-08-05 and was promoted on 2026-08-12. Check whether a project publishes its cadence before calling a static tag a stall.

Q: `## 2.148.3 (August 19, 2026)` appears in the CLI release notes. What date is that?
A: The **planned stable-promotion date**, not the publish date — that build reached npm on 2026-08-12 03:13 UTC. Reading the heading as a publish date puts every CLI fact about a week into the future.

Q: `sf` 2.147.7 pins `@salesforce/plugin-agent` 2.0.0, which predates the employee-agent preview fix. Why does a fresh install still get the fix?
A: plugin-agent 2.0.0 **ranges** `@salesforce/agents` at `^2.0.0`, which resolves forward to 2.0.1 at install time. The fix comes from range resolution, not the pin — so an existing `node_modules` or a committed lockfile can hold you on the broken build while a colleague's fresh install is clean.

Q: What breaks when `sf` `latest` moves to 2.147.7?
A: `engines.node` goes from `>=18.6.0` to `>=22.0.0`. A `npm install -g @salesforce/cli` on a Node 18 or 20 CI image now emits only an `EBADENGINE` **warning** at install time and fails later in ways that read as metadata errors. Installer and tarball users are insulated — `sf update stable` moves a bundled Node 24 runtime and never consults system Node.

Q: SDR 13.0.1 fixed the zip-slip. What did 13.1.1 fix, and why in the same file?
A: A **TOCTOU symlink escape** in the same class, `StaticResourceMetadataTransformer`. 13.0.1 validated the *resolved destination path*; 13.1.1 adds `findSymlinkOnPath`, which walks **every path segment** between the extraction root and the destination, because a symlink already on disk could redirect an in-bounds write outside the extraction directory. New error key: `error_static_resource_symlink`.

Q: For the SDR TOCTOU fix, what is the malicious input?
A: **Your own working tree** — a symlink committed to a repository you cloned — not only an untrusted org. `sf project retrieve` unzips any `StaticResource` of content type `application/zip` or `application/jar` during metadata→source conversion, so cloning a repo is enough to expose the path.

Q: Why does the SDR TOCTOU fix reach stable `sf` immediately when the `--root-type-with-dependencies` flag does not?
A: A pinning asymmetry. `sf` pins each **plugin** to an exact version (`= 4.0.1`), but a plugin **ranges** its libraries (`^13.0.0`). So a library security patch resolves forward on a fresh install, while a plugin feature needs a new `sf` release. Verify with `npm ls @salesforce/source-deploy-retrieve`.

Q: What are the only two legal values of `sf project retrieve start --root-type-with-dependencies`?
A: **`Bot`** and **`AiAgentDefinitionVersion`** — a closed oclif enum, repeatable. Naming `Bot` also retrieves its dependent `GenAiPlannerBundle`, `GenAiPlugin` and `GenAiFunction` components. Two traps: the changelog calls it `--root-with-dependencies` (wrong), and the shipped help example writes a single dash.

Q: Is `--root-type-with-dependencies` a CLI convenience or a platform capability?
A: A platform capability. It maps to `rootTypesWithDependencies` on the SOAP Metadata API `RetrieveRequest` body, so any Metadata API caller — Ant, a custom client, a CI script — can send it, regardless of which `sf` version is installed.

Q: What does `mcpTools` declare in an Agent Skill, and what completes it?
A: The **MCP servers and tool names** a skill needs, with an optional `semver` range, nested under `metadata:`. It is the fourth field in the skill dependency contract: `cliTools` (local binaries), `accessCheck` (org permission), `relatedSkills` (sibling graph), `mcpTools` (MCP servers). Added across `forcedotcom/sf-skills` in 1.37.0, 2026-08-13.

Q: How does the `salesforce-development` plugin know a skill has not been tampered with?
A: `catalog/discovery.json` carries a per-skill `skillMdSha256` and `treeSha256`. That is the mechanism behind the 1.10.0 fix that limits capability discovery to skills **verified installed and unmodified** — edit a `SKILL.md` locally and it drops out of discovery.

Q: The hosted `headless-360` MCP server exposes how many tools, and what are they?
A: **Four meta-tools**, not a per-operation catalogue: `discover` (semantic search over an indexed operation catalog), `describe` (input schema and canonical route for one operation), `dispatch_readonly` (GET) and `dispatch` (POST/PATCH/DELETE). This corrects the "~100 admin-facing skills" framing.

Q: What does `mcp__headless-360__dispatch` actually take as arguments?
A: **Raw HTTP** — `{url, method, body?, queryParams?}` — not `{operation_id, arguments}`. `queryParams` must be camelCase; the tool rejects `query_params`. The response envelope is `{"status_code": …, "body": {…}}`.

Q: Which org does a `headless-360` dispatch call hit, and why does that matter?
A: The org bound to the **OAuth JWT of the current MCP session**. No org id, alias or credential appears in the call — which is why the same skill works against production and sandbox, and why the only thing separating a sandbox write from a production write is which session you are connected to.

Q: `mcp__headless-360__discover` returns nothing for a route you need. What does that prove?
A: Nothing. Documented Setup and Connect routes are not all indexed in the discovery corpus. Dispatch the exact path directly; only a real `404` from the call itself proves the route is unavailable on that org.

Q: `sf-skills` is Apache-2.0 — so is the npm package safe for client work?
A: Not unambiguously. `@salesforce/afv-skills` declares `"license": "CC-BY-NC-4.0"` in `package.json` on every published version, while the same tarball ships a byte-identical Apache-2.0 `LICENSE.txt`. SBOM and licence scanners read the manifest, so they will flag NonCommercial. The GitHub copy — what `npx skills add` fetches — is the defensible one.

Q: Two `@salesforce/agents` patches in five days hit the same code path. What is the shared root cause?
A: `sf agent preview --api-name` builds a preview session that is initialised differently from `--authoring-bundle`. 2.0.1 sent the wrong `bypassUser` (breaking employee agents); 2.0.2 sent no context variables. Both fail **silently** — the agent reasons without the values rather than erroring.

Q: A CI script runs `sf org generate password --length 12`. What does the org actually get, and what happens on 2026-08-19?
A: Not a 12-character password — the CLI **silently raised** it. From `sf` 2.148.3 (stable 2026-08-19, `@salesforce/plugin-user` 5.0.0) the command **errors** instead: `--length` must be ≥ 20 and `--complexity` ≥ 3. The break makes an old lie audible; it changes nothing the org ever received.

Q: You read the April 2026 deprecation notice for `sf org generate password` and fixed your scripts. Why might they still break?
A: The notice warned about **`--complexity` only** — "Starting in Summer '26, the command will fail if you specify a complexity value less than 3". The **`--length` ≥ 20** floor was never announced; it exists only in the `plugin-user` CHANGELOG (`30a97ff`, `feat!`) and the 2.148.3 release notes. Grep for both flags.

Q: Could a lockfile, a stale cache or a fresh install change *when* the `org generate password` break reaches you?
A: No. `sf` **pins** `@salesforce/plugin-user` to an exact version, so nothing pulls 5.0.0 early and nothing dodges it once 2.148.3 is `latest`. That is the opposite of a library fix like the SDR zip-slip, which `plugin-deploy-retrieve` **ranges** and which therefore arrives by resolution. Ask which layer a change lives in.

Q: How do you create a Lead via the CLI without triggering assignment rules?
A: `sf data create record --sobject Lead --values "..." --skip-assignment-rules`, new in `sf` 2.148.3 and also on `sf data update record`. It is **opt-out only and per-command** — omit it and Account/Case/Lead assignment rules still fire, including on API writes.

Q: `npm install @salesforce/react-native-agentforce` — what version do you get, and what is wrong with it?
A: **0.5.0**, which is the package's only dist-tag (`latest`) and is simultaneously marked **Pre-release** on GitHub, titled *262.1.3-RC4*. There is no `rc` or `next` tag to avoid it and no RC marker in the version string. The last non-RC build is **0.4.0**; GitHub's "Latest" badge still sits there.

Q: Why is npm a bad source for the React Native Agentforce bridge's release history?
A: The registry holds only `0.0.0`, `0.3.0`, `0.4.0`, `0.5.0` — GitHub releases `0.1.0` (260.4) and `0.2.0` (260.5) never published. Combined with marketing names that diverge entirely from npm versions (`0.5.0` = *262.1.3-RC4*), neither number predicts the other. Read the releases page.

Q: `sf agent preview --api-name <ApiName>` shows no reasoning trace. Is the agent not reasoning?
A: Probably not — before `@salesforce/agents` **2.0.4** (2026-08-18) `ProductionAgent.getTrace()` returned `undefined` unconditionally, so the `--api-name` path never asked for a trace. It now GETs `v1.1/preview/sessions/{sessionId}/plans/{planId}`. Trace fetches are also swallowed (`.catch(() => undefined)`), so a missing trace can equally be a permission or endpoint failure.

Q: Why do `sf agent preview --api-name` and `--authoring-bundle` keep behaving differently?
A: They are two client classes. `--authoring-bundle` runs `ScriptAgent` against local `.agent` source; `--api-name` runs `ProductionAgent` against the published agent. Four behaviours were implemented in the first and missing from the second in nine days — identity (`bypassUser`, 2.0.1), context variables (2.0.2), the `x-attributed-client: no-builder` header (2.0.3) and reasoning traces (2.0.4). The path that matches production is the less complete one.

Q: Stable `sf` 2.147.7 pins `@salesforce/plugin-agent` 2.0.0. Do you get the 2.0.4 agent fixes?
A: On a **fresh install, yes** — plugin-agent 2.0.0 *ranges* `@salesforce/agents` `^2.0.0`, which resolves 2.0.4. An existing `node_modules` or a lockfile does not. `^2.0.0` **permits** the fix; only `plugin-agent` 2.0.3's `^2.0.4` **compels** it, and that ships on `nightly` only.

Q: The `salesforce-development` plugin offers to add a skill. What decides which version you get?
A: `publicRelease.releaseRef` in the plugin's generated `discovery.json` — it becomes the `#<ref>` in `npx skills@1.5.20 add forcedotcom/sf-skills#<ref> …`. The catalogue is a snapshot on its own refresh schedule: it sat at **1.32.0** while the repo shipped 1.36.0, 1.37.0 and 1.38.0, and was refreshed to 1.38.0 only at 1.39.0. Read the ref before trusting the counts.

Q: You want every Agent Skill tagged "Data 360". Which field do you search, and with what value?
A: Two answers, and they differ. `SKILL.md` frontmatter carries `metadata.domains: ["Data 360"]` (Title Case, 1–3 per skill, added in 1.40.0). The catalogue and its `sf-context discovery domain` command carry a singular lowercase `domain: "data360"` derived from the name prefix. `domains` appears **zero** times in `discovery.json`, so the new field is invisible to the search command.

Q: Your delivery plan automates Data 360 with the `data360-*` Agent Skills. What is the supportability risk?
A: Every command they emit runs on `sf data360`, which is **`Jaganpro/sf-cli-plugin-data360`** — MIT, 3 stars, *"NOT an official Salesforce product… unsupported, experimental"*, absent from npm, installed by `sf plugins link` from a source clone with **no version to pin**. The Apache-2.0, `forcedotcom`-published skills do not make the runtime first-party. `sf-skills` 1.39.0 deleted the `compatibility:` line that declared this.

Q: The `salesforce-development` plugin resolves capabilities Skills → CLI → MCP. Does that mean Salesforce prefers its CLI over its own hosted MCP servers?
A: No — the precedence orders **instruction** sources, not execution. In `sf-skills` 1.41.0 the skills naming `headless-360` went **4 → 14**, and `experience-portal-create` forbids the CLI outright: *"`dispatch`/`dispatch_readonly` is the only way this skill talks to the org."* Where the hosted dispatcher covers the surface, it is the execution path.

Q: You quote "Winter '27 adds 59 new metadata types" from SDR's `METADATA_SUPPORT.md`. What is wrong with that citation?
A: It has no timestamp. The file is regenerated by a nightly bot (`chore: auto-update metadata coverage… [no ci]`), so the v68 section is a moving artifact — 59 types on 2026-08-13, **71** by 2026-08-20. Its `git log` also misleads in the other direction: the 08-21 commit is a 915-line Prettier reflow that changes no type. Diff type names, not lines.

Q: `platform-trial-org-create` provisions a trial org. Which endpoint does it call?
A: None — there is no signup endpoint. A trial org is an **insert of a `SignupRequest` sObject** (key prefix `0SR`) against an authenticated, entitled host org, read back on a second call for the assigned org id. An unentitled org fails with `NOT_FOUND` or `INVALID_TYPE` ("sObject type 'SignupRequest' is not supported") — an entitlement error wearing a schema error's clothes.

Q: You install `@salesforce/cli@latest` today. `@salesforce/plugin-deploy-retrieve` ranges SDR `^13.0.0` and 13.2.3 is published. Which SDR do you get?
A: Whatever `sf`'s **`npm-shrinkwrap.json`** says — **13.0.1** for `latest` 2.148.3. A published shrinkwrap is honoured by npm and pins every transitive dependency exactly, so caret ranges never resolve forward. `npm view … dependencies` shows the ranges and is the wrong check; read the shrinkwrap or run `npm ls @salesforce/source-deploy-retrieve` inside the install.

Q: Which two install paths escape the `sf` shrinkwrap?
A: **JIT plugins** (`oclif.jitPlugins` — 10 packages, pinned by version but installed on first use into the user plugins directory, where their own transitive deps resolve at that moment) and **`sf plugins install`**. Everything in the 28 core plugins and their libraries is fixed at CLI build time.

Q: Is `sf` `latest` patched for both SDR path escapes as of 2026-08-25?
A: No. It pins SDR **13.0.1**, which carries the **zip-slip** fix (13.0.1) and **not** the **TOCTOU symlink** fix (13.1.1). 13.1.1 is on `latest-rc` 2.149.9 and lands on stable at the 2026-08-26 Wednesday promotion at the earliest.

Q: The SDR CHANGELOG documents 13.2.1 with a compare link and a `chore(release)` commit. Can you install it?
A: No — `registry.npmjs.org/@salesforce/source-deploy-retrieve/13.2.1` returns `version not found`. The publish did not complete; `13.2.2` (`fix: linting post-fork-merge`) is the build that actually shipped #1817. **A version in a repo's changelog is not a version on npm — check the registry.**

Q: After upgrading `sf-pi` past v0.272.0, the `agentforce-*` skills stop being offered automatically. What happened and how do you undo it?
A: ADR 0108 made managed-library skills **`manual-only`** — Pi now loads a stamped `effective/` copy and `disable-model-invocation: true` keeps them out of `<available_skills>`. They still run via `/skill:<name>`. Undo by setting `sfPi.skillInvocation.packs.agentforce` (or `.default`) to `agent-invocable` in global settings, then re-stamping with `/sf-skills toggle`.
