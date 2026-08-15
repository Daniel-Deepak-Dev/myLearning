# Scan log — one line per scan

**Why this file exists.** The radar scans three areas daily, and most days most areas have nothing. A
quiet day must read as a quiet day rather than as a missed scan — but that costs one row here, not a file
per area. **A dated note is created only when that area routed at least one item to a topic file.**
Everything else is a `—`.

Substance lives in the [topic files](README.md#topic-files--the-running-story). Unchanged artifact state
lives in [watchlist.md](watchlist.md). This file answers one question: *did a scan run, and did it find
anything?*

| Scan (UTC) | Agentforce | Data 360 | AI Research |
|---|---|---|---|
| 2026-08-15 03:37 | [`@salesforce/agents` 2.0.2 · `sf-skills` 1.38.0](01-agentforce/2026-08-15.md) | — | — |
| 2026-08-14 03:41 | [SDR 13.1.1 TOCTOU · `mcpTools` · `--root-type-with-dependencies`](01-agentforce/2026-08-14.md) | — | — |
| 2026-08-13 03:37 | [`sf` 2.147.7 → `latest` · Winter '27 = API 68.0](01-agentforce/2026-08-13.md) | — | — |
| 2026-08-12 03:37 | [Claude Code plugin 1.10.0 · Data 360 v2 dispatcher](01-agentforce/2026-08-12.md) | [cross-link](02-data-cloud/2026-08-12.md) | — |
| 2026-08-11 03:38 | [`sf-pi` v0.263.0 drops the 50.0 fallback · `@salesforce/agents` 2.0.1](01-agentforce/2026-08-11.md) | [cross-link](02-data-cloud/2026-08-11.md) | — |
| 2026-08-10 03:36 | [Instanced-URL Release Update · `sf-pi` v0.262.1 provenance](01-agentforce/2026-08-10.md) | — | — |
| 2026-08-09 03:55 | [OAuth username-password retirement · `sf-pi` guardrail](01-agentforce/2026-08-09.md) · *weekly* | [`sfsqlquery` · `sf-data360`](02-data-cloud/2026-08-09.md) | — |
| 2026-08-08 03:20 | [IL5 · zip-slip dist-tag move · `sf-skills` 1.34/1.35](01-agentforce/2026-08-08.md) | [gap check — Data Cloud One](02-data-cloud/2026-08-08.md) | [GIFT-Eval reimplementation](03-salesforce-ai-research/2026-08-08.md) |
| 2026-08-07 03:30 | [IL5 first record · `sf-pi` model catalogue deleted](01-agentforce/2026-08-07.md) *(recovered 08-08)* | [semi-joins are CRM Analytics](02-data-cloud/2026-08-07.md) | [SCUBA](03-salesforce-ai-research/2026-08-07.md) |
| 2026-08-06 03:08 | [dist-tag roll caught live · Army HRC](01-agentforce/2026-08-06.md) *(recovered 08-08)* | [cross-link](02-data-cloud/2026-08-06.md) | [SCUBA](03-salesforce-ai-research/2026-08-06.md) |
| 2026-08-05 03:15 | [`sf-pi` eval gating · React Native 0.4.0](01-agentforce/2026-08-05.md) | — | [GIFT-Eval backlog](03-salesforce-ai-research/2026-08-05.md) |
| 2026-08-03 03:06 | [CLI 2.147.0 correction](01-agentforce/2026-08-03.md) *(recovered 08-08)* | — | [SCUBA · GIFT-Eval `org` correction](03-salesforce-ai-research/2026-08-03.md) |
| 2026-08-02 03:10 | [SDR zip-slip · Mobile SDK 18.26.8](01-agentforce/2026-08-02.md) · *weekly* | [reference app rename](02-data-cloud/2026-08-02.md) | [topic file created](03-salesforce-ai-research/2026-08-02.md) |
| 2026-08-01 03:19 + 12:18 | [`sf-skills` 1.33.0 · licence correction](01-agentforce/2026-08-01.md) | [observability backend](02-data-cloud/2026-08-01.md) | — |
| 2026-07-31 | [long-form note](01-agentforce/2026-07-31.md) | [long-form note](02-data-cloud/2026-07-31.md) | [long-form note](03-salesforce-ai-research/2026-07-31.md) |
| 2026-07-30 | [long-form note](01-agentforce/2026-07-30.md) | [long-form note](02-data-cloud/2026-07-30.md) | [long-form note](03-salesforce-ai-research/2026-07-30.md) |
| 2026-07-29 | [long-form note](01-agentforce/2026-07-29.md) | [long-form note](02-data-cloud/2026-07-29.md) | [long-form note](03-salesforce-ai-research/2026-07-29.md) |
| 2026-07-28 | [long-form note + structural pass](01-agentforce/2026-07-28.md) | [long-form note](02-data-cloud/2026-07-28.md) | [long-form note](03-salesforce-ai-research/2026-07-28.md) |
| 2026-07-27 | [long-form note](01-agentforce/2026-07-27.md) | [long-form note](02-data-cloud/2026-07-27.md) | [long-form note](03-salesforce-ai-research/2026-07-27.md) |
| 2026-07-26 | [long-form note](01-agentforce/2026-07-26.md) | [long-form note](02-data-cloud/2026-07-26.md) | [long-form note](03-salesforce-ai-research/2026-07-26.md) |

**No scan on 2026-08-04.** Notes dated 2026-07-26 → 2026-07-31 predate the writing contract and are full
write-ups; they are left as-is.

## Quiet streaks — the trigger for a gap check

An area quiet for **5 consecutive scans** stops being re-scanned the same way. The next run spends that
area's budget on a gap check instead and records what it checked. Reporting *"sixth consecutive scan with
no movement"* is not an output.

| Area | Quiet since | Consecutive quiet scans | Next action |
|---|---|---|---|
| Data 360 | 2026-08-12 (last cross-link) | 3 | Gap check due at 5 — target the `sf-pi` siblings and `help.salesforce.com` release notes |
| AI Research | 2026-08-08 | 6 | **Gap check owed.** `agentforce-adlc` 16 days idle; the post-ICML lull has run six weeks |
