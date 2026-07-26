# 05-release-radar — Salesforce AI / Agentforce / Data 360 updates

**What this is:** a running log of Salesforce technical updates worth knowing as an AI-Salesforce architect. Fed by the `daily-agentforce-updates` scheduled task.

**How it's organized.** **Topic files** are the knowledge — each one reads as a story about a subject, newest entry at top, revised when something supersedes it. [CHANGELOG.md](CHANGELOG.md) is the dated index: one line per finding, pointing at the entry. The date is metadata, not the filing system.

**Every entry carries:** what changed → **how you actually use it** (click path, endpoint, CLI command, metadata type, permission set) → **the trap** that would cost you an afternoon → why it matters → `**Status:**` → `**Study action:**` → `**Sources:**`. If an entry has no mechanism and no trap, it didn't clear the bar and shouldn't be here.

**How to read it:** skim this README for the current state of play → open the topic file that matters to what you're building. Scan [CHANGELOG.md](CHANGELOG.md) when you want to know what's new since you last looked.

## Topic files

| File | Covers |
|---|---|
| [agentforce-platform.md](agentforce-platform.md) | Agentforce Builder, Agent Script, Multi-Agent Orchestration, Voice, mobile SDK, observability |
| [data-360.md](data-360.md) | Data 360 (ex-Data Cloud): SOQL changes, Code Extension, ingestion monitoring, Intelligent Context, semantic layer, zero-copy |
| [developer-tooling-and-apis.md](developer-tooling-and-apis.md) | Hosted MCP servers, Headless 360, Agentforce ADLC skills, Apex/LWC changes, CLI, Agentforce Vibes |
| [trust-security-and-governance.md](trust-security-and-governance.md) | Einstein Trust Layer, user-mode defaults, SOAP login retirement, secrets handling |
| [pricing-and-certification.md](pricing-and-certification.md) | Flex Credits, pay-per-resolution, Agentic ELA, Agentforce Specialist exam changes |
| [ai-research-and-benchmarks.md](ai-research-and-benchmarks.md) | Salesforce AI Research: CRMArena-Pro, SCUBA, GIFT-Eval — what agents measurably can't do yet |

## State of play — as of 2026-07-26

Five things define the current Salesforce AI landscape. If you only retain five, retain these.

1. **Headless 360 is the organizing theme of Summer '26.** Every major Salesforce capability is now reachable as an API, an MCP tool, or a CLI command — by a human, an app, or an autonomous agent. Salesforce-hosted MCP servers are GA.
2. **Agent Script + the new Agentforce Builder are GA**, and from the week of **July 13, 2026** the *New Agent* button no longer opens the legacy builder. Agent Script is also **open source** (Apache 2.0). Learning it is no longer optional.
3. **Data Cloud is now Data 360** — a real rename (SKUs, release notes and the consultant cert all use it), and a reframing from CDP/warehouse into the *context engine* that grounds agents. Its developer surface grew a lot: `SET OPTIONS` in SOQL, Python Code Extensions, a Data 360 MCP server.
4. **Security defaults flipped.** At API 67.0, Apex DML/SOQL run in **user mode** by default and classes default to **`with sharing`**. `WITH SECURITY_ENFORCED` no longer compiles. Expect real migration work in older codebases.
5. **Commercials moved to consumption.** Flex Credits ($500 / 100k credits, ~$0.10 per action) is the recommended model, and the new Help Agent introduced **pay-per-resolution** at $2 per autonomous resolution — billed on outcomes, with consumption unmetered during the interaction.

Three things to add to that picture, from 2026-07-26: [`agentforce-adlc`](developer-tooling-and-apis.md) gives you Claude Code skills for the whole agent lifecycle, and it encodes Agent Script's real authoring rules (4-space indent, Python-style `True`/`False`, `developer_name` must match the bundle folder). The **Agentic ELA** is now a third commercial model alongside Flex Credits and pay-per-resolution, and it inverts what you optimize for. And [CRMArena-Pro](ai-research-and-benchmarks.md) puts a peer-reviewed number on the ceiling: ~83% on structured single-turn CRM tasks, sharply worse multi-turn, near-blind to confidentiality unless prompted.

## Open questions to chase

- **Winter '27** release notes aren't public yet; Release Update *enforcement* starts September 2026. Watch what gets enforced.
- **Agent Script in the Agentforce Specialist exam** — it became the default authoring model in July 2026 but isn't named in the exam guide. Assume implicit scope; re-check before booking.
- **Exact Agentforce Builder / Agent Script GA date** — no first-party announcement located; secondary sources conflict between February 2026 and the Summer '26 cadence. The July 13, 2026 legacy-builder cutoff is confirmed.
- **Fin acquisition** — Salesforce signed a definitive agreement to acquire Fin (announced June 15, 2026; expected to close Q4 FY27), an SMB-focused autonomous service agent platform used by 30,000+ companies. Watch how it lands relative to the Help Agent.

---

_Last updated: 2026-07-26 · Sources are linked inline in each topic file._
