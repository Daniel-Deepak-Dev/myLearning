# SQL Fluency — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: What's the difference between an INNER JOIN and a LEFT JOIN?
A: INNER returns only rows with matches in both tables; LEFT returns all rows from the left table, with NULLs where the right side has no match.

Q: What is a CTE and why use one?
A: A Common Table Expression (WITH name AS (...)) — a named subquery that makes multi-step logic readable and reusable within one statement.

Q: What can a window function do that GROUP BY can't?
A: Compute aggregates/rankings across related rows while keeping every individual row in the output, e.g. ROW_NUMBER() OVER (PARTITION BY account ORDER BY date).

Q: WHERE vs HAVING?
A: WHERE filters rows before aggregation; HAVING filters groups after aggregation.
