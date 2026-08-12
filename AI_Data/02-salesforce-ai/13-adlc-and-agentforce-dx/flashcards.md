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
