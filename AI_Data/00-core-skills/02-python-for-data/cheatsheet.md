# Python for Data Work — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

pandas for tables, `requests` for APIs, `json` for payloads — and since Summer '26 Python is a first-class **Data 360 runtime** via Code Extension.

## Key terms
| Term | Definition |
|---|---|
| Code Extension | Custom Python in isolated Data 360 containers. Headline use: **custom chunking**. |
| `salesforce-data-customcode` | The Python SDK that scaffolds a Code Extension project for local authoring. |
| `pd.json_normalize` | Flattens a nested API response into a DataFrame in one call. |

## Rules of thumb

- **Always set `timeout=` on `requests`** and call `raise_for_status()`. A hang means a retry; a retry can mean a duplicate write.
- Use `.loc` for assignment — chained assignment can silently not assign.
- Secrets in environment variables, never literals.
- The highest-value script you'll write is the **evaluation harness**: run it before and after a change; the delta is your claim.

## Exam traps / common confusions

- **Code Extension is Python only** so far, and has an **author ≠ operator** split (running/monitoring needs the Data Cloud Architect perm set).
- `json_normalize` flattens one level by default — pass `record_path` / `max_level` for deeper nesting.
- A 4xx returns a valid response object; without `raise_for_status()` you parse an error body.

## Minimal example

```python
import pandas as pd, requests

r = requests.post(url, headers={"Authorization": f"Bearer {tok}"},
                  json={"query": "SELECT Id FROM Account"}, timeout=30)
r.raise_for_status()
df = pd.json_normalize(r.json()["records"])

# the eval harness — turns a demo into a measured result
qs = pd.read_csv("eval_set.csv")            # question, expected
qs["actual"]  = qs.question.apply(ask)
qs["correct"] = qs.apply(grade, axis=1)
print(qs.correct.mean())                     # run before AND after
```
