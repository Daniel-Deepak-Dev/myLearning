# Zero Copy & BYOL Federation — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is zero copy / BYOL?
A: Federation pattern: query data in Snowflake, BigQuery, Databricks or Redshift in place — bring your own lake — without copying it into Data 360.

Q: When does zero copy beat ingestion, and vice versa?
A: Zero copy when the data is large, already governed elsewhere, freshness matters, or compliance forbids copying. Ingest when you need Data 360 features on it (identity resolution, segmentation performance), predictable query latency, or real-time agent grounding.

Q: What is the Summer '26 status of AWS Glue Data Catalog federation?
A: GA — proposal-safe, you can commit to it in a delivery plan.

Q: What is the Summer '26 status of Microsoft Fabric OneLake federation?
A: Beta. Fine to prototype and demo, but it carries no support commitment and must not become load-bearing in a delivery plan.

Q: Why does the Databricks IdP authentication change matter?
A: It is a security-review unlock. "Can we govern this connection centrally?" is the question that stalls zero-copy projects — not the technology.

Q: With zero copy, what determines query performance?
A: The source system. If the warehouse is slow or under-provisioned, Data 360 is slow — and so is any agent grounded on it.

Q: Is federated data free?
A: No. You avoid Data 360 storage cost, but you pay source-side compute on every query.

Q: Does zero copy solve data freshness?
A: Only partly. It removes pipeline lag, but if the source itself is stale, so is the federated view.

Q: What is the trap in over-federating?
A: Teams federate everything to avoid duplication, then discover that identity resolution and segmentation need the data locally.

Q: Where does zero copy sit in the three legs of enterprise grounding?
A: It is the reach leg — reach without copying — alongside Intelligent Context (unstructured content) and the semantic layer (agreed meaning).
