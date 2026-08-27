# Agent Script — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

A human-readable language for defining agents that **compiles to portable JSON** — making agent behaviour diffable, lintable in CI without an org, and deployable like any other source.

## Key terms
| Term | Definition |
|---|---|
| Hybrid Reasoning | The dial: how much is deterministic business logic vs. left to the model, per decision point. |
| Compile-to-JSON | The portability mechanism — what makes agents reviewable and CI-testable. |
| Model pinning | Declaring the model inside the script, versioned with the logic. |
| `knowledge:` block | Where a Data Library is wired in for grounding. |

## Rules of thumb

- **Subagent descriptions are executable config** — Atlas 3.0 routes on them. Highest-value thing to get right.
- Compiling clean ≠ behaving well. The compiler validates **structure**; scorers and evaluations validate **judgement**.
- Migrating? One-click upgrade, then **diff behaviours in preview** — the optimize step can change behaviour.
- Build the CI pipeline early: lint → compile → evaluate → deploy. It's a portfolio artifact in its own right.

## Exam traps / common confusions

- Legacy builder stopped **creating** agents week of **July 13, 2026** — editing/activation/versioning still work.
- **Not named in the Agentforce Specialist exam guide** despite being default. Assume implicit scope; re-check before booking.
- GA date is genuinely unclear (Feb '26 vs Summer '26 cadence, no first-party announcement). The July 13 cutoff is the confirmed fact.
- **Portability has limits:** the JSON travels; the Apex and Flows it invokes stay org-bound.

## Minimal example

Why it beat prose instructions:

```
LEGACY                          AGENT SCRIPT
prose in topic fields     →     compiled artifact
contradictions = silent   →     compiler catches structure
no diff                   →     PR review
org-only testing          →     plain CI job, no org
org-wide model            →     pinned per agent
```
