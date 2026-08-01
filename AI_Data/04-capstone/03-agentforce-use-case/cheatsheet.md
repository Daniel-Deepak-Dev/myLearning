# Capstone: End-to-End Agentforce Use Case — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

One narrow measurable outcome, authored in **Agent Script**, grounded in Data 360, actioned by 67.0-compliant Apex — with a baseline, a measured result, unit economics and an honest failure analysis.

## Key terms
| Term | Definition |
|---|---|
| Flex Credits | $500 / 100k credits. Standard action = 20 credits (~$0.10). |
| Pay-per-resolution | $2 per autonomous resolution (Help Agent). Escalations free. Doesn't stack with Flex Credits. |
| Custom Scorer | Your KPI graded against live sessions; deployable as metadata. |

## Rules of thumb

- **Baseline the metric for two weeks before building.** No baseline, no result.
- **Cost per resolution = actions × $0.10.** Compare against $5–$15+ for a human ticket.
- Scope so it's measurable: "deflects password-reset cases on the EMEA queue", not "handles support".
- Three things make it architect-level: a **measured outcome**, **unit economics**, and an **honest failure analysis**.

## Exam traps / common confusions

- **Author in Agent Script** — the legacy builder can't create agents since July 13, 2026.
- **You pay per action, not per conversation.** Real resolutions run 5–15 actions; orchestration multiplies.
- **API 66.0 breaks invocable actions** without a visible no-arg constructor on input classes; Summer '26 is the enforcement date.
- Make actions **idempotent** — agents retry after timeouts.
- Benchmarks are **ceilings**: Salesforce's own help site hit 70% resolution of 4.3M inquiries; Oviva deflected ~50%.

## Minimal example

The arithmetic that wins the room:

```
actions per resolution   :  8
cost per action          :  $0.10
  → cost per resolution  :  $0.80

human ticket (loaded)    :  $5–$15
  → saving per deflection:  $4.20–$14.20

with 3-subagent orchestration → 2.4× actions → $1.92
  "worth it because <state the reason>"
```
