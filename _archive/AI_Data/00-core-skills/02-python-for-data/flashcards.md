# Python for Data Work — Flashcards

<!-- Strict format: one "Q:" line, then "A:" line(s), blank line between cards.
     Keep it strict — this file is scriptable into Anki (Q/A = front/back).
     Cover the A, answer out loud, then check. Add cards as you learn. -->

Q: pandas: Series vs DataFrame?
A: Series = one labeled column of values; DataFrame = a table of Series sharing an index.

Q: How do you turn a nested JSON API response into a DataFrame?
A: resp = requests.get(url); df = pd.json_normalize(resp.json()) — json_normalize flattens nested JSON. It flattens one level by default; pass record_path or max_level for deeper structures.

Q: What does df.groupby('col').agg(...) return?
A: A new DataFrame aggregated per group — pandas' equivalent of SQL GROUP BY.

Q: Why did Python become a platform skill for Salesforce work in 2026?
A: Code Extension deploys custom Python to isolated containers inside Data 360 — for batch data transformations and, most importantly, custom chunking logic on search index creation.

Q: Which SDK scaffolds a Code Extension project?
A: The Data Custom Code Python SDK, salesforce-data-customcode, used with the Salesforce CLI Code Extension plugin for sandbox validation and deployment.

Q: Why must you always set a timeout on requests calls?
A: Without one the call can hang indefinitely. In an agent context that means a retry, and a retry against a non-idempotent endpoint can mean a duplicate write.

Q: Why call raise_for_status()?
A: A 4xx or 5xx still returns a perfectly valid response object. Without raise_for_status() you silently parse an error body and get confusing downstream failures.

Q: What is the SettingWithCopyWarning about?
A: Chained pandas assignment may operate on a copy and silently fail to assign. Use .loc for assignment.

Q: What is the highest-value Python script in this whole roadmap?
A: The evaluation harness — run a fixed question set through the system, grade the answers, print the mean. Run it before and after a change; the delta is what turns a demo into a measured result.

Q: What is the permission split around Code Extension?
A: Developers author the code; users with the Data Cloud Architect permission set run and monitor it.
