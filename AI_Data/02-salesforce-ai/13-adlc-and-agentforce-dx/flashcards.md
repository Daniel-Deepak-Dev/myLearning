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
A: dist-tags are not ordered by version. As of 2026-08-02, `latest` is 2.145.6, `latest-rc` 2.146.3 and `nightly` 2.147.3. A plain `npm install -g @salesforce/cli` follows `latest`, so the newest published version and the version you get are different.

Q: What is the security lesson from the SDR zip-slip that outlives the specific bug?
A: `sf project retrieve` is an **inbound** trust boundary. It takes org-controlled bytes — which a packaging partner, a compromised sandbox or an agent with metadata write access can influence — and writes them onto a developer laptop or CI runner.

Q: Which sf CLI version first required Node 22, and what else came with it?
A: 2.147.3 (2026-08-01, `nightly` dist-tag): `engines.node >=22.0.0`, `@salesforce/core ^9.0.0`, `@salesforce/plugin-agent` 2.0.0 and `@salesforce/plugin-deploy-retrieve` 4.0.1. You cannot take the security patch without taking all of it.

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
