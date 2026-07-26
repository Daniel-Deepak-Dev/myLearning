# 05-release-radar — Salesforce AI / Agentforce / Data 360 updates

**What this is:** a running log of Salesforce technical updates worth knowing as an AI-Salesforce architect. Fed by the `daily-agentforce-updates` scheduled task.

**How it's organized — two layers.**

- **Dated scan notes** live in three **area folders** — [`01-agentforce/`](01-agentforce/), [`02-data-cloud/`](02-data-cloud/), [`03-salesforce-ai-research/`](03-salesforce-ai-research/). One `YYYY-MM-DD.md` per area per scan: table of contents, entries ordered most-consequential-first, a `**Status:**` line and per-entry `**Sources:**` on each. When a scan finds nothing, the note says so explicitly — a quiet day should read as a quiet day, not as a missed scan.
- **Topic files** sit at the root of this folder and hold the *running story* — dated entries newest-first, so a topic reads as a narrative over time. They stay at the root deliberately: most of them cut across areas (developer tooling covers both Agentforce and Data 360; pricing covers both), so filing them under one area would lose information.

**How to read it:** skim this README for the current state of play → open the newest dated note in the area you care about → drop into the topic file when you want the history. Every entry carries a **Why it matters** line; that's the part to remember.

## Areas — dated scan notes

| Folder | Covers | Latest |
|---|---|---|
| [01-agentforce/](01-agentforce/) | Agentforce platform, builder and Agent Script, developer tooling, governance, pricing | [2026-07-26](01-agentforce/2026-07-26.md) |
| [02-data-cloud/](02-data-cloud/) | Data 360 (ex-Data Cloud): ingestion, modeling, grounding, zero-copy, semantic layer | [2026-07-26](02-data-cloud/2026-07-26.md) |
| [03-salesforce-ai-research/](03-salesforce-ai-research/) | Salesforce AI Research: benchmarks (CRMArena, SCUBA, GIFT-Eval), open models, agent-lifecycle tooling | [2026-07-26](03-salesforce-ai-research/2026-07-26.md) |

## Topic files — the running story

| File | Covers |
|---|---|
| [agentforce-platform.md](agentforce-platform.md) | Agentforce Builder, Agent Script, Multi-Agent Orchestration, Voice, mobile SDK, observability |
| [data-360.md](data-360.md) | Data 360 (ex-Data Cloud): SOQL changes, Code Extension, Intelligent Context, semantic layer, zero-copy |
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | Hosted MCP servers, Headless 360, Apex/LWC changes, CLI, Agentforce Vibes, Agent Skills |
| [trust-security-and-governance.md](trust-security-and-governance.md) | Einstein Trust Layer, user-mode defaults, SOAP login retirement, secrets handling |
| [pricing-and-certification.md](pricing-and-certification.md) | Flex Credits, pay-per-resolution, Agentforce Specialist exam changes |

## State of play — as of 2026-07-26

Five things define the current Salesforce AI landscape. If you only retain five, retain these.

1. **Headless 360 is the organizing theme of Summer '26.** Every major Salesforce capability is now reachable as an API, an MCP tool, or a CLI command — by a human, an app, or an autonomous agent. Salesforce-hosted MCP servers are GA.
2. **Agent Script + the new Agentforce Builder are GA**, and from the week of **July 13, 2026** the *New Agent* button no longer opens the legacy builder. Agent Script is also **open source** (Apache 2.0). Learning it is no longer optional.
3. **Data Cloud is now Data 360** — a real rename (SKUs, release notes and the consultant cert all use it), and a reframing from CDP/warehouse into the *context engine* that grounds agents. Its developer surface grew a lot: `SET OPTIONS` in SOQL, Python Code Extensions, a Data 360 MCP server.
4. **Security defaults flipped.** At API 67.0, Apex DML/SOQL run in **user mode** by default and classes default to **`with sharing`**. `WITH SECURITY_ENFORCED` no longer compiles. Expect real migration work in older codebases.
5. **Commercials moved to consumption.** Flex Credits ($500 / 100k credits, ~$0.10 per action) is the recommended model, and the new Help Agent introduced **pay-per-resolution** at $2 per autonomous resolution — billed on outcomes, with consumption unmetered during the interaction.

**Newest additions (scan of 2026-07-26):** Salesforce AI Research is shipping [`agentforce-adlc`](https://github.com/SalesforceAIResearch/agentforce-adlc) — Claude Code skills covering the whole agent lifecycle in Agent Script, with voice support merged July 23 — and the **Headless 360 MCP Server** hit Beta with ~100 admin-facing *skills* rather than thousands of flat tools. On July 24 the VA awarded Salesforce a **$1.6B "Agentic Enterprise License Agreement"**, a third commercial model alongside Flex Credits and pay-per-resolution.

## Open questions to chase

- **Winter '27** release notes aren't public yet; Release Update *enforcement* starts September 2026. Watch what gets enforced.
- **Agent Script in the Agentforce Specialist exam** — it became the default authoring model in July 2026 but isn't named in the exam guide. Assume implicit scope; re-check before booking.
- **Exact Agentforce Builder / Agent Script GA date** — no first-party announcement located; secondary sources conflict between February 2026 and the Summer '26 cadence. The July 13, 2026 legacy-builder cutoff is confirmed.
- **Fin acquisition** — Salesforce signed a definitive agreement to acquire Fin (announced June 15, 2026; expected to close Q4 FY27), an SMB-focused autonomous service agent platform used by 30,000+ companies. Watch how it lands relative to the Help Agent.

---

_Last updated: 2026-07-26 · Sources are linked inline in each topic file._
