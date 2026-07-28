# Capstone: End-to-End Agentforce Use Case

> Track: Capstone · Roadmap: Phase 05 · Weeks 21–26 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/](../../05-release-radar/README.md)

**Roadmap scope:** Pick one measurable outcome — case deflection or lead scoring — and build it: data in via Data 360, reasoning via agent, action via custom Apex.

> **Two things changed since the roadmap was written.** Author in **Agent Script**, not topics — the legacy builder stopped creating agents the week of July 13, 2026. And **unit economics are now part of the design**: you pay per action, so architecture has a visible price.

## What is it?

One narrow, measurable outcome, built end to end and evidenced with numbers.

**Pick something with a metric that already exists.** Case deflection rate, first-response time, lead qualification throughput. If you have to invent the metric, the result won't be persuasive.

## Why it matters (for the AI-Salesforce architect role)

This is the project that proves the whole roadmap. It touches every track: Data 360 grounding, Agent Script authoring, Apex actions under the new security model, evaluation, and cost.

**Three things make it read as architect-level rather than developer-level:**

1. **A measured outcome**, not a demo — "deflection went from 12% to 31% on this queue over four weeks."
2. **Unit economics** — you can state what a resolution costs and why.
3. **An honest failure analysis** — what it gets wrong, and what you'd fix next. This is what separates a real project from a rehearsed demo, and it's what an experienced interviewer probes for.

### Benchmarks for the business case

Useful reference points, all first-party or named:

| Source | Result |
|---|---|
| Salesforce's own `help.salesforce.com` | **4.3M inquiries, 70% resolved** by Agentforce |
| Oviva (European digital health) | 300,000+ inbound messages/month; **half** of inquiries deflected, **40%** of operational support resolved without a human |

**Use these as ceilings, not forecasts** — deflection is heavily domain-dependent.

## How it works

### The unit economics section — do not skip this

| Item | Cost |
|---|---|
| Flex Credits | $500 per 100,000 credits |
| Standard action | 20 credits (~**$0.10**) |
| Voice action | 30 credits (~$0.15) |
| Sandbox / Testing Center action | 16 credits (~$0.08) |

**You pay per action, not per conversation.** That's the modelling trap: a demo conversation is one action; a real resolution is often **five to fifteen**. And an orchestrator routing through three subagents multiplies that again.

So compute, for your use case: *actions per resolution × $0.10 = cost per resolution.* Then compare against the fully-loaded cost of a human ticket (typically $5–$15+). That arithmetic is the first thing a CFO asks for and the last thing most demos can supply.

Worth knowing as contrast: the prepackaged Help Agent uses **pay-per-resolution** — $2 per autonomous end-to-end resolution, escalations and negative-feedback sessions free, consumption unmetered during the interaction. It does **not** stack on Flex Credits.

### Build order

1. **Pick the outcome and baseline it.** Measure the current metric for two weeks before you build.
2. **Ground it** — Data 360, with real-time ingest if the agent reads live records. Stale grounding is the top failure cause.
3. **Author in Agent Script.** Pin the model deliberately.
4. **Build the action** — invocable Apex under 67.0 rules: user mode, `with sharing`, and a visible **no-arg constructor** on any invocable input class. Make it **idempotent**.
5. **Test:** `agent preview` + trace files, then YAML/JSON evaluations in CI.
6. **Deploy via Metadata API** so the whole thing is source-controlled.
7. **Measure with Custom Scorers** against live sessions.
8. **Compute unit economics** and write the failure analysis.

### Consider orchestration — and price it

If the use case spans two domains, build two narrow subagents and an orchestrator. Give each subagent a description that states its **exclusions** — Atlas 3.0 routes on those descriptions, and a vague one causes intermittent mis-routing that looks like a model failure.

Then note the cost: three subagents ≈ three times the actions. Being able to say *"orchestration cost us 2.4× per resolution and here's why it was worth it"* is exactly the analysis this project should produce.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Baseline the metric for two weeks **before** building.
- [ ] Author the agent in Agent Script; lint and compile it in CI with no org connected.
- [ ] Build one idempotent Apex action, 67.0-compliant.
- [ ] Run `agent preview`, read the trace, confirm routing.
- [ ] Deploy a Custom Scorer and grade live sessions.
- [ ] Count actions per resolution and compute cost per resolution.
- [ ] Write the failure analysis: what it gets wrong, and why.

## Gotchas & sharp edges

- **Don't author in topics.** The legacy builder can't create new agents since July 13, 2026.
- **No baseline, no result.** Measure before you build or you have a demo, not a project.
- **Per-action billing surprises people.** Five to fifteen actions per real resolution; orchestration multiplies.
- **The 67.0 no-arg constructor rule breaks invocable actions.** Check it first when something stops working.
- **Make the action idempotent** — agents retry after timeouts, and a duplicated write is a real incident.
- **Stale grounding is the top failure cause**, and it presents as a model problem.
- **Subagent descriptions are executable config**, not labels. Include exclusions.
- **A vague scope kills the evaluation.** "Handles support" can't be measured; "deflects password-reset cases on the EMEA queue" can.
- **Deflection benchmarks are ceilings.** 70% is Salesforce's own domain, heavily tuned.

## Related topics

- [Agent Script](../../02-salesforce-ai/07-agent-script/notes.md) — how to author it
- [Multi-agent orchestration](../../02-salesforce-ai/08-multi-agent-orchestration/notes.md) — if it spans domains
- [Custom agent actions](../../02-salesforce-ai/05-custom-agent-actions/notes.md) — the 67.0 rules
- [Observability & testing](../../02-salesforce-ai/09-observability-and-testing/notes.md) — how you measure
- [Ingestion](../../01-data-cloud/02-ingestion/notes.md) — freshness for grounding
- [Write-up & pitch](../04-writeup/notes.md) — where the numbers and failure analysis land
- [Release radar: pricing and certification](../../05-release-radar/pricing-and-certification.md) — Flex Credits and benchmarks
