# Zero Copy & BYOL Federation — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is zero copy / BYOL?
A: Federation pattern: query data in Snowflake, BigQuery, or Databricks in place — bring your own lake — without copying it into Data Cloud.

Q: When does zero copy beat ingestion, and vice versa?
A: Zero copy when the data is large, already governed elsewhere, and freshness matters; ingest when you need Data Cloud features on it (identity resolution, segmentation performance) or the source can't serve queries.
