# Data Engineering & Pipeline Patterns — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

ETL vs ELT, idempotency, orchestration and quality checks — with two of them sharpened by agents: **freshness became correctness**, and **idempotency moved from pipelines into actions**.

## Key terms
| Term | Definition |
|---|---|
| ELT | Load raw, transform in the warehouse. Modern default; what a lakehouse assumes. |
| Idempotency | Re-running produces the same result. What makes retries safe. |
| Data lineage | Where data came from and how it was transformed. Also answers "what produced this agent's answer?" |
| Freshness check | When did this last update? The most-often-missing quality assertion. |

## Rules of thumb

- **If an agent reads it, it needs to be current. If a dashboard reads it, scheduled is fine.** Decide per stream.
- **Every write an agent can trigger must be idempotent** — agents retry after timeouts with no human deciding to.
- A check that logs a warning nobody reads is not a check. **Fail the run.**
- Keep the raw layer: a transformation bug should be re-runnable, not lost.

## Exam traps / common confusions

- **Freshness is a correctness property for agents**, not a cost trade-off. Four hours stale = a confidently wrong answer.
- Over-refreshing everything is invisible waste — and duplicate-heavy loads inflate a profile-priced bill.
- **Don't bypass the platform for freshness** — calling a source directly from an action loses the unified profile and its governance.
- Backfills aren't reruns: changed business logic can rewrite history downstream consumers didn't expect.

## Minimal example

Making an agent action idempotent — four options:

```
natural key, not auto-increment
upsert, not insert
explicit idempotency key on the write endpoint
check-then-act guarded by a unique constraint

"Issue refund" without one of these can issue two.
```
