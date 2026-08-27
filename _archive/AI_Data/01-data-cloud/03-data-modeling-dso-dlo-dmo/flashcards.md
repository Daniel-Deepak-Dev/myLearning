# Data Modeling: DSO → DLO → DMO — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: DSO vs DLO vs DMO?
A: DSO = raw data exactly as it arrives from the source; DLO = the stored, source-shaped table in the data lake; DMO = the standardized canonical object DLOs are mapped into.

Q: What is harmonization?
A: Mapping disparate source fields into the standard data model so "email" from five systems becomes one consistent attribute.

Q: Why does DLO→DMO mapping matter so much?
A: Everything downstream inherits it — identity resolution matches on DMO fields, insights compute over DMOs, segments filter them, and agents ground on them. A mapping mistake propagates into every agent answer.

Q: What is the SET OPTIONS clause?
A: A SOQL clause added in Summer '26 that specifies a Data 360 dataspace and controls NULL / empty-string handling. It goes at the very end of the query.

Q: What happens if you query a DLO without specifying a dataspace?
A: The query silently returns zero records — not an error, not a warning. Zero rows looks identical to "no matching data", which is why this costs people an afternoon.

Q: What does honorEmptyStrings = true do?
A: Makes Data 360 treat NULL and '' as distinct values. The default (false) collapses them the way Salesforce Platform objects do.

Q: Why does the NULL / empty-string default matter?
A: DLOs are lake tables and don't share Platform object semantics. The collapsing default is a classic source of wrong-but-plausible results — queries that return rows, just not the right ones.

Q: What can you now do from Apex against Data 360, and why does it matter?
A: Run SQL (Summer '26). SOQL can't express the joins, aggregations and window functions lakehouse work needs, and the previous alternative was HTTP callouts to the Direct API. An Apex-backed agent action can now compute a rolling aggregate or multi-table join in one query.

Q: Should you map to a standard DMO or create a custom one?
A: Prefer standard. Cross-source consistency is the entire point, and a custom DMO per source recreates the silos you were removing.

Q: Why not ingest and map every field "just in case"?
A: Unmapped DLO fields still cost storage but add no downstream value.

Q: Which modeling decision is most painful to change later?
A: The primary key — identity resolution consumes it, so changing it means reworking matching and everything built on the resulting profiles.

Q: Which Apex namespace runs Data 360 SQL, and what are its five classes?
A: `sfsqlquery` — `SqlStatement` (execute), `SqlRowIterator` (iterate), `Row` (typed accessors like `getString`/`getInteger`), `QueryHandle` (re-fetch an earlier query's results) and `SqlQueueable` (async for large sets). Added in the Winter '27 release notes.

Q: What are the three `sfsqlquery` workflows and when do you pick each?
A: `SqlStatement` → `SqlRowIterator` → `Row` when the query is small and the caller waits; `QueryHandle` → `SqlRowIterator` → `Row` to re-fetch results of a query that already ran; `SqlQueueable` → `SqlRowIterator` → `Row` for large sets or anything outliving the transaction.

Q: What limit bites a polling loop built on `SqlQueueable`?
A: The queueable chain ceiling — stack depth caps at 50 in production. A poll-until-complete loop is a chain, so budget the polls.

Q: Does the dataspace trap apply to `sfsqlquery`?
A: Yes. Omit the dataspace on a DLO query and you get zero rows, silently, with no error — exactly as with `SET OPTIONS` in SOQL.

Q: Why does `sfsqlquery` matter for agent grounding specifically?
A: An Apex-backed agent action can compute a rolling aggregate or multi-table join at the moment the agent asks, instead of reading an insight refreshed on someone else's schedule. Grounding moves from "recently true" to "true now".
