# Ingestion — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is a data stream?
A: A configured ingestion feed bringing data into Data 360 from a connector, on a batch or streaming schedule. It lands data as a DLO.

Q: Batch vs streaming ingestion — when do you use each?
A: Batch for scheduled bulk loads (e.g. nightly CRM sync); streaming for near-real-time events (web/mobile SDK, engagement data).

Q: Name four common Data 360 connectors.
A: CRM (core org), Marketing Cloud, Amazon S3, Web/Mobile SDK.

Q: What is Accelerated Data Ingest and what is its status?
A: Real-time CRM data into Data 360 with no pipeline lag. GA in Summer '26.

Q: Why does Accelerated Data Ingest matter more than it sounds?
A: Scheduled ingestion meant Data 360's copy of a Case or Opportunity always lagged the live record. That's fine for analytics but fatal for agents, which then answer confidently from stale state — the most common cause of a "the agent was wrong" ticket that isn't a model problem at all.

Q: What workaround did Accelerated Data Ingest eliminate, and why was that workaround bad?
A: Bypassing Data 360 to call CRM directly from an action. It cost you the unified profile and its governance, and reintroduced the sharing problems Data 360 was solving.

Q: What are the three ways data gets into Data 360?
A: Ingestion via data streams (copies the data), zero-copy federation (queries it where it lives), and Accelerated Data Ingest (real-time CRM).

Q: What is the rule for choosing a refresh schedule?
A: If an agent grounds on it, real-time. If a segment activates it, match the activation cadence. If only a dashboard reads it, scheduled is fine. Decide per stream, not per project.

Q: Where does ingestion's job end?
A: At the DLO. Mapping the DLO to a DMO is data modeling, not ingestion.

Q: Does ingesting data create unified profiles?
A: No. Two records for the same person remain two profiles until identity resolution runs with match and reconciliation rules.

Q: You are billed per unified profile. Why does ingestion still affect the bill?
A: Sloppy ingestion of duplicate-heavy sources inflates the profile count that identity resolution produces downstream.
