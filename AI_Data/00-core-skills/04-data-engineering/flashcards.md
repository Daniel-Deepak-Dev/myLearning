# Data Engineering & Pipeline Patterns — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: ETL vs ELT?
A: Transform before loading (ETL) vs load raw then transform inside the warehouse (ELT — the modern default).

Q: What makes a pipeline idempotent, and why does it matter?
A: Re-running it produces the same result — essential for safe retries after failures.

Q: What is data lineage?
A: Tracking where data came from and how it was transformed — key for trust, debugging, and compliance. In an agentic context it also answers "which data produced this agent's answer?"

Q: What is a semantic layer?
A: A governed layer of business definitions (what counts as "revenue") sitting between raw data and consumers, human or AI.

Q: Why did ELT become the default?
A: Storage got cheap and warehouse compute got fast. It also keeps the raw data, so a transformation bug is re-runnable rather than lost — which is why lakehouses assume it.

Q: How did agents change the batch-vs-real-time decision?
A: It became a correctness decision rather than a cost one. Four hours stale is invisible on a dashboard; for an agent it means answering confidently from a case that closed twenty minutes ago.

Q: How did agents extend the idempotency requirement?
A: An agent may retry an action after a timeout with no human deciding to. A non-idempotent "issue refund" action can issue two — so idempotency moved from pipelines into every agent action.

Q: Name four ways to make an operation idempotent.
A: Natural keys instead of auto-increment, upserts instead of inserts, an explicit idempotency key on write endpoints, or check-then-act guarded by a unique constraint.

Q: What is the rule about data quality checks?
A: A check that logs a warning nobody reads is not a check — fail the run.

Q: Which quality assertion is most often missing, and why does it matter now?
A: The freshness check — when did this last update. It's what catches the agent-grounding failure before a customer does.

Q: Why shouldn't you bypass the platform to get fresher data into an agent?
A: Calling a source system directly from an agent action loses the unified profile and its governance.

Q: Why is a backfill not just a rerun?
A: A backfill over changed business logic can rewrite history in ways downstream consumers don't expect.
