# Python for Data Work — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: pandas: Series vs DataFrame?
A: Series = one labeled column of values; DataFrame = a table of Series sharing an index.

Q: How do you turn a nested JSON API response into a DataFrame?
A: resp = requests.get(url); df = pd.json_normalize(resp.json()) — json_normalize flattens nested JSON.

Q: What does df.groupby('col').agg(...) return?
A: A new DataFrame aggregated per group — pandas' equivalent of SQL GROUP BY.
