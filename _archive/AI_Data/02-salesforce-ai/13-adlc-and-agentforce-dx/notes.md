# ADLC & Agentforce DX

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · Product status: **CLI GA · Agentforce Vibes 2.0 Developer Preview · evaluations Beta** · sources in [05-release-radar/developer-tooling-and-apis.md](../../05-release-radar/developer-tooling-and-apis.md)

**Scope:** the lifecycle an agent goes through from idea to production and back — and the toolchain that automates each stage: Agent Skills, the `sf agent` commands, Agentforce Vibes, and the ADLC skill set.

> **Why this folder exists.** ADLC was referenced in passing in three files and taught in none. That's the wrong shape for the topic that **decides how you actually work**: it's the difference between building an agent and operating one, and it's the exact seam where this track meets the [Claude CCA track](../../03-claude-cca/) — the same Agent Skills format runs in Claude Code.
>
> **Scope discipline:** this folder owns the *lifecycle and the workflow*. [Observability & Testing](../09-observability-and-testing/notes.md) owns the *testing and observability tools* — scorers, the testing pyramid, `@IntegrationTest`, reading traces. Cross-link, don't restate.

## What is it?

The **Agent Development Lifecycle (ADLC)** is Salesforce's answer to "what does the SDLC look like when the artifact is an agent?" Salesforce publishes it as an architect-level framework with five phases and, separately, as a concrete developer workflow driven by Agent Skills.

### The five phases

| Phase | What happens |
|---|---|
| **Ideation & Design** | Define purpose, persona, tools and decision logic; produce a blueprint — agent architecture, user flows, technical specs |
| **Development — the inner loop** | Build reasoning logic, connect data sources, wire the tools |
| **Testing & Validation** | Rapid prompt-test-evaluate cycles in a harness. **Token economics are analysed here** — so cost failures are caught before production, not after |
| **Deployment** | Release to production |
| **Monitoring & Tuning — the outer loop** | Continuous monitoring, learning and improvement |

**Inner loop** = the tight build-and-try cycle a developer runs many times a day. **Outer loop** = the slow cycle of watching production and feeding what you learn back into the agent. The vocabulary matters because Salesforce's tooling is explicitly organised around it.

### Why it isn't just SDLC with new words

ADLC is a **closed-loop learning system** — testing, monitoring, calibration and refinement managing the inherent drift of a system whose behaviour isn't fully specified by its source. Three consequences:

- **Deployment is day one, not the finish line.** In SDLC, shipping ends the project. In ADLC, shipping starts the measurement.
- **Drift is expected, not a defect.** The model changes, the data changes, user phrasing changes. An agent that was good in March can be mediocre in July with no commit in between.
- **Cost is a test result.** Token economics belong in the test phase. This is the discipline that stops a working agent from being an unaffordable one.

## Why it matters (for the AI-Salesforce architect role)

**It's the deliverable clients don't know to ask for.** Anyone can demo an agent. The question that decides whether a Geeksoft engagement renews is "how do we know it's still working in six months" — and ADLC is the structured answer, with tooling behind it rather than a promise.

**It's the strongest overlap between your two tracks.** Agent Skills use the same open format Claude Code uses. A single exercise — driving an Agentforce agent through the full loop from Claude Code — advances the Agentforce Specialist prep *and* the CCA-F prep at once. That's the highest-leverage lab in this study base.

**It may be examinable weight, not trivia.** Multiple 2026 sources report a **Development Lifecycle and Observability** domain on the Agentforce Specialist exam at **15–20%** — a domain the study base didn't have a topic for until now. The weighting is unconfirmed; see the caveats in [the exam guide](../_cert-agentforce-specialist/exam-guide.md).

## How it works

### The skill-driven workflow

Install once, then work in plain language:

```bash
npx skills add forcedotcom/sf-skills     # prerequisites: Node.js + Salesforce CLI
```

Three skills carry the lifecycle: **`developing-agentforce`**, **`testing-agentforce`**, **`observing-agentforce`**.

| Phase | Skill | Commands |
|---|---|---|
| **Design** | `developing-agentforce` | plan mode (Shift+Tab in Claude Code); design interview; map the agent as a graph — router node plus domain subagents |
| **Build & deploy** | `developing-agentforce` | `sf agent generate authoring-bundle` → validate Agent Script compiles locally → `sf project deploy start` for backing Flow/Apex → deploy the bundle. Failures drive automated fix-and-retry loops |
| **Test & validate** | `testing-agentforce` | `sf agent preview start` / `send` / `end` for smoke tests; `sf agent test create` / `run` for YAML batch regression |
| **Publish** | `developing-agentforce` | `sf agent publish authoring-bundle` → `sf agent activate` |
| **Debug & observe** | `observing-agentforce` | local traces in `.sfdx/agents/[name]/sessions/…/traces/`; production via the **Session Trace Data Model**; **AgentLens** visualizer to walk the graph |

**Design-first is the load-bearing idea.** The recommended flow starts in plan mode with the assistant interviewing you about architecture *before* anything is generated. Same instinct as writing the subagent description before the subagent — specification first, because the specification is what the model actually executes.

### Five workflow rules from the first-party guide

1. Keep each project in its own folder.
2. **Build only in scratch orgs or sandboxes — never production.**
3. Commit Agent Script to Git. It's source code; treat it that way.
4. Use `--json` on every command so output is machine-readable.
5. **Scope deployments explicitly** so you don't accidentally ship unrelated metadata.

### The tooling map

- **Agentforce Vibes 2.0** *(Developer Preview)* — agentic IDE that plans before acting, with multi-tab chat, Plan Mode, MCP integration, built-in Skills and Rules, live LWC previews, and current Claude and GPT models in one picker. Every Developer Edition org has included it free since April 2026.
- **Agentforce DX** — the CLI surface: agent project scaffolding (the `agent` template generates a runnable Local Info Agent), one-command agent user creation, `agent preview` GA, trace files, YAML/JSON evaluations *(Beta)*.
- **Agent Skills** — the open format at [agentskills.io](https://agentskills.io/home). Salesforce's library is [`forcedotcom/sf-skills`](https://github.com/forcedotcom/sf-skills), prepackaged with Vibes and working in Claude Code, Codex and others.
- **`SalesforceAIResearch/agentforce-adlc`** — the research toolkit: `/agentforce-generate`, `/agentforce-test`, `/agentforce-observe`, `/agentforce-secure` (an OWASP LLM Top 10 assessment). Voice modality merged July 2026, including `VoiceCallId` and connection blocks. **Licensed CC BY-NC 4.0 — see the warning below.**

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] **The high-leverage one:** `npx skills add forcedotcom/sf-skills` into Claude Code, then drive one agent from design interview → generate → deploy → preview → publish → activate without leaving the terminal. Counts for both certs.
- [ ] Run the design phase in plan mode *before* generating anything, and keep the interview transcript. Compare that agent against one you scaffolded straight away.
- [ ] Write one YAML test spec, run `sf agent test run`, then deliberately break a subagent description and watch which test catches it.
- [ ] Read a local trace from `.sfdx/agents/…/traces/` and the same session through the Session Trace Data Model. Note what production gives you that local doesn't.
- [ ] Do one full outer-loop pass: pull production traces, find a failure pattern, fix, redeploy. That loop is the actual deliverable.
- [ ] Compare `agentforce-adlc` against `sf-skills` — overlapping scope, different licences. Decide now which is safe for client work.

## Gotchas & sharp edges

- **Licences differ and it matters commercially.** `sf-skills` is Salesforce's supported library. **`agentforce-adlc` is CC BY-NC 4.0 — non-commercial, so it cannot be used on Geeksoft client work.** Agent Script itself is Apache 2.0. Three artifacts, three licences; read before you build on any of them.
- **`agentforce-adlc` is research-grade, not a supported product.** No GA/Beta designation, no support path. Its `main` has had no commits since **July 24, 2026** and **no published releases** — and note the trap the radar recorded: the GitHub listing showed "updated July 28" from repository metadata, not code. Check `commits/main.atom` before believing an Updated column.
- **Agentforce Vibes 2.0 is Developer Preview.** Fine to learn on; don't put it in a delivery plan.
- **Agent evaluations are Beta**; `agent preview` is GA. Different maturity, adjacent commands.
- **Never build in production.** The guide says it explicitly, and the fix-and-retry loops make an unscoped deployment genuinely dangerous — an automated retry against a production org will keep trying.
- **`--json` isn't optional in an agent-driven workflow.** Without it the assistant parses human-formatted output and gets it subtly wrong.
- **Compiling clean is not behaving well.** Local Agent Script validation checks structure only — see [Observability & Testing](../09-observability-and-testing/notes.md) for what actually verifies behaviour.
- **"ADLC" names two things.** The lifecycle framework, and the `agentforce-adlc` repo that implements a version of it. Say which you mean.
- **Drift has no commit.** Nothing in Git changes when an agent degrades. Only the outer loop catches it — which is why monitoring is a phase, not an afterthought.

## Related topics

- [Observability & Testing](../09-observability-and-testing/notes.md) — the testing pyramid, Custom Scorers, trace interpretation
- [Agent Script](../07-agent-script/notes.md) — the artifact this lifecycle versions and deploys
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — the router-plus-subagents graph the design phase produces
- [Voice & Contact Center](../12-voice-and-contact-center/notes.md) — voice modality in the ADLC skills
- [Agent Fabric](../11-agent-fabric-and-interop/notes.md) — where a finished agent gets registered and governed
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) and [Capstone: MCP server](../../04-capstone/01-mcp-server-salesforce/notes.md) — the same skills format, the other side of the seam
