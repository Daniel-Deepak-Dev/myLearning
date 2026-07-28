# Agentforce Coworker — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

An AI teammate in the search bar that you **turn on rather than author** — it inherits the org's sharing model, searches CRM + Data 360 + Slack, and routes to specialized agents to act. **Beta, no GA date.**

## Key terms
| Term | Definition |
|---|---|
| Agentforce Coworker | Zero-config agent in the search bar. Announced 2026-05-21, Beta. Inherits org setup, sharing rules, permissions. |
| Search Agent | The component behind it. Rate limit **100 RPM**. |
| Federation vs ingestion | **Slack federates** (live, needs Slack Auth). **Drive/SharePoint ingest** (1 hr incremental, stale between crawls). |
| `Access_Ai_Search` | Permission set group granting user access — but assign via **Manage Users** instead (Salesforce's recommendation). |
| Data Services Credits | Covers data queries + unstructured/intelligent processing. Distinct from **Flex Credits** (prompts). |

## Rules of thumb

- **Seat-based license → searching CRM or Slack is free.** Zero Flex Credits, zero Data Services Credits. Get users on the right license.
- **Three sources in Beta, not 270+.** CRM, Data 360 objects, Slack. Drive/SharePoint/Jira are **pilot-only**.
- **Enabling Coworker enables Einstein.** Check what that means for the org first.
- **Coworker ≠ Employee Agent.** Employee Agent is purpose-built and authored; Coworker is zero-config and org-wide.
- Configure **user-based AI permissions** at rollout or seat-licensed users burn credits anyway.

## Exam traps / common confusions

- **Not on Government Cloud Plus.** Don't activate.
- **Beta consumption is non-refundable** — Non-GA services give rise to no refund or credit rights.
- **Guest / unauthenticated / portal users are always usage-based**, whatever the org's model.
- Slack is **not ingested into Data 360** — it's federated, so Slack Authentication is a prerequisite, not an option.
- Editions: **Enterprise, Unlimited, Agentforce 1**. Admin needs the **Agentforce Coworker Admin** permission set.

## Minimal example

```
Setup → Quick Find "Agentforce Coworker"
  → (optional) Set Up Data Space
  → Get Started with Agentforce Coworker → Turn On
  → Turn on End User Experience → tick disclaimer consent → Turn On
  → Manage Users → select users → Assign → Done

limits to remember: Slack 180 q/min sustained (1000 burst) · Search Agent 100 RPM
                    Drive & SharePoint 5,000 files, 1 hr incremental
                    PDFs ≤ 100 MB · other files ≤ 4 MB
```
