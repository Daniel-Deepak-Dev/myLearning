# Observability & Testing — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Turns "is the agent good?" into a versioned, deployable definition — Custom Scorers as `aiAgentScorerDefinitions` metadata, evaluations in CI, trace files for diagnosis.

## Key terms
| Term | Definition |
|---|---|
| Custom Scorer (Beta) | Your own KPI graded against live sessions. Deployable as metadata. |
| `aiAgentScorerDefinitions` | The Metadata API type — **the tell that evaluation is now infrastructure**. |
| Trace file | Post-preview record of how the agent routed and which actions ran. |
| `@IntegrationTest` | Apex tests with live callouts + `commitTestOnly()`. **Scratch orgs only.** |

## Rules of thumb

- Deploy scorers via **Metadata API, not the UI** — that's what puts evaluation in source control.
- Trace files are the primary diagnostic for mis-routing: they show *which subagent description won*.
- Pick 3 metrics from Refined Agent Analytics' 40+ for any given client conversation. The rest is decoration.
- Layer the tests: unit → `@IntegrationTest` → preview/trace → evaluations → live scorers. Each catches what the one below can't.

## Exam traps / common confusions

- **`@IntegrationTest` is scratch-org only**, async, one at a time — not yet CI-ready. Say so honestly.
- **Custom Scorers are Beta** and need the *Agentforce Scorer Beta* permission set.
- Scorers grade **live sessions** = real customer conversations. Consider what's logged and who reads it.
- Testing Center actions cost **16 credits (~$0.08)** each — a big evaluation suite has a real bill.
- A clean Agent Script compile proves **structure**, not behaviour.

## Minimal example

```
sf agent preview start
sf agent preview send  "my order is late and I want to cancel"
sf agent preview end
   → read trace: which subagent description won? which actions ran?

then: deploy aiAgentScorerDefinitions → activate in Scorer Hub
   → grade live sessions on "cited a policy document"
```
