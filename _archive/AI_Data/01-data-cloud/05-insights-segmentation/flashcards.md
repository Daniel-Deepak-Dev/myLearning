# Calculated Insights & Segmentation — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What is a calculated insight?
A: A metric (e.g. lifetime value, engagement score) computed over Data 360 data on a schedule with a SQL-like definition.

Q: What is RFM, and how does it differ structurally from LTV?
A: Recency, Frequency, Monetary — each axis ranked (conventionally into quintiles) and combined into a tier such as champion, loyal, at risk or lapsed. LTV emits one number per profile, so a segment filters it by threshold; RFM emits a classification, so a segment filters it by label and the meaning travels with the value.

Q: What is the trap with RFM ranks?
A: They are relative, not absolute. Quintiles re-cut on every run, so a profile's tier can change because the population moved rather than because its behaviour did.

Q: What is a segment?
A: A defined audience slice built from profiles, attributes, and insights — the unit you activate to other systems.

Q: What is activation?
A: Publishing a segment or data to a target — Marketing Cloud, ad platforms, CRM — where action happens.

Q: What is the semantic layer, and what does Salesforce call its implementation?
A: A governed layer of business definitions sitting between raw data and consumers. Salesforce's implementation is Tableau Semantics — it standardizes metric definitions and translates data into business language.

Q: Why does an agent need a semantic layer more than a human does?
A: A human reading an ambiguous metric brings context or asks. An agent doesn't ask — it produces a confident number from whichever definition it found or inferred.

Q: What is OSI?
A: A vendor-neutral, YAML-based open-source standard for interoperable semantic models, metrics and relationships. Core spec finalized February 2026.

Q: What is the difference between a calculated insight and a semantic-layer definition?
A: The insight defines HOW a number is computed. The semantic layer defines WHAT the number means and makes that meaning machine-readable. Agents need both.

Q: Name the three legs of enterprise grounding.
A: Intelligent Context (unstructured content), the semantic layer (agreed meaning), and zero-copy federation (reach without copying). An agent answer is only as trustworthy as the weakest of the three.

Q: When should you ground an agent on an insight rather than on raw records?
A: For analytical questions. An insight is pre-aggregated, governed and cheap in tokens — and it removes the chance the model computes its own aggregate wrongly.

Q: An insight produces the wrong number for a customer. Where is the likely root cause?
A: Upstream in identity resolution — insights compute per unified profile, so a fragmented profile yields a wrong metric.

Q: How should you set segment refresh cadence?
A: Match it to the activation cadence, not to "as often as possible". Over-refreshing and over-publishing cost without benefit.

Q: What did Summer '26 add for computing metrics live?
A: Running SQL from Apex against Data 360, so an Apex-backed agent action can compute a rolling aggregate or multi-table join inline rather than depending on a scheduled insight. The dataspace trap still applies.
