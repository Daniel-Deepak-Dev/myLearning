# SQL Fluency — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What's the difference between an INNER JOIN and a LEFT JOIN?
A: INNER returns only rows with matches in both tables; LEFT returns all rows from the left table, with NULLs where the right side has no match.

Q: What is a CTE and why use one?
A: A Common Table Expression (WITH name AS (...)) — a named subquery that makes multi-step logic readable and reusable within one statement. A nested subquery reads inside-out; a CTE reads top-down.

Q: What can a window function do that GROUP BY can't?
A: Compute aggregates/rankings across related rows while keeping every individual row in the output, e.g. ROW_NUMBER() OVER (PARTITION BY account ORDER BY date).

Q: WHERE vs HAVING?
A: WHERE filters rows before aggregation; HAVING filters groups after aggregation. Aggregates can't appear in WHERE.

Q: What are the three parts of a window function specification?
A: PARTITION BY (the group), ORDER BY (the sequence within the group), and the frame (ROWS BETWEEN …, which rows count).

Q: Why does a LEFT JOIN sometimes silently behave like an INNER JOIN?
A: Because filtering the right-hand table in the WHERE clause drops the unmatched rows the LEFT JOIN preserved. Filter in the ON clause instead. The result looks plausible with rows quietly missing.

Q: Why is SQL fluency more relevant to a Salesforce developer in 2026 than before?
A: Summer '26 added running SQL from Apex against Data 360. SOQL can't express the joins, aggregations and window functions lakehouse work needs, and the previous alternative was HTTP callouts to the Direct API.

Q: COUNT(*) vs COUNT(column)?
A: COUNT(*) counts rows; COUNT(column) skips NULLs.

Q: Why can't you write WHERE col = NULL?
A: NULL = NULL is not true — NULL comparisons yield unknown. Use IS NULL.

Q: What's the risk with default window frames?
A: With ORDER BY and no explicit frame you usually get RANGE UNBOUNDED PRECEDING rather than the whole partition. Be explicit about the frame.

Q: Where does SQL show up in Data 360 specifically?
A: Calculated insight definitions, ELT transformations, and SQL run from Apex — the last being new in Summer '26.
