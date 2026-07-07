# Data Modeling: DSO → DLO → DMO — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: DSO vs DLO vs DMO?
A: DSO = raw data exactly as it arrives from the source; DLO = the stored, source-shaped table in the data lake; DMO = the standardized canonical object DLOs are mapped into.

Q: What is harmonization?
A: Mapping disparate source fields into the standard data model so "email" from five systems becomes one consistent attribute.

Q: Why does DLO→DMO mapping matter so much?
A: Cross-source consistency (and everything downstream: identity resolution, insights, segments) depends on it — it's the heart of the Consultant exam.
