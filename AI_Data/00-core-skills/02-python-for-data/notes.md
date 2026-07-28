# Python for Data Work

> Track: Core skills · Roadmap: Phase 01 · Weeks 1–4 · Status: 🌱 learning
> Vendor-neutral. Salesforce-specific application lives in [01-data-cloud/09-data-360-devops](../../01-data-cloud/09-data-360-devops/notes.md).

**Roadmap scope:** pandas basics, JSON handling, calling REST APIs. You don't need to be a Pythonista — you need to move data and call models comfortably.

## What is it?

Three capabilities, not a language course:

| Capability | Library | What you actually do with it |
|---|---|---|
| **Tabular manipulation** | `pandas` | Load, filter, group, join, reshape, export |
| **JSON handling** | `json`, dict/list idioms | Parse API responses, build request bodies |
| **HTTP** | `requests` | Call REST APIs — Salesforce, Claude, anything |

That's the working set. Depth beyond it is optional for this roadmap.

## Why it matters (for the AI-Salesforce architect role)

**Python became a first-class Data 360 runtime in Summer '26** — which changes this from a general-purpose skill into a platform skill.

**Code Extension** deploys custom Python to isolated containers inside Data 360, for batch data transformations and — the important one — **custom chunking logic on search index creation**. Chunking is usually the single biggest lever on RAG quality, and Python is how you control it.

The toolchain: the [Data Custom Code Python SDK](https://pypi.org/project/salesforce-data-customcode/) (`salesforce-data-customcode`) scaffolds a project you author and debug locally, then the Salesforce CLI Code Extension plugin validates against a sandbox and deploys.

**Two other places it pays off:**

- **Calling the Claude API** — the CCA-F track, and any prototype that isn't running inside an org
- **Evaluation harnesses** — scoring agent or RAG output against a fixed question set is a small pandas script, and it's the thing that turns a demo into a measured result

## How it works

### The three idioms worth having at your fingertips

```python
import pandas as pd, requests, json

# 1. tabular
df = pd.read_csv("orders.csv")
top = (df[df.amount > 100]
         .groupby("profile_id", as_index=False)["amount"]
         .sum()
         .sort_values("amount", ascending=False))

# 2. HTTP + JSON
r = requests.post(url,
                  headers={"Authorization": f"Bearer {token}"},
                  json={"query": "SELECT Id FROM Account"},
                  timeout=30)
r.raise_for_status()
records = r.json()["records"]

# 3. JSON → tabular
df2 = pd.json_normalize(records)
```

`pd.json_normalize` is the one people don't know about and should — it flattens nested API responses into a DataFrame in one call.

### Evaluation harness shape

The script that makes a RAG or agent project measurable:

```python
questions = pd.read_csv("eval_set.csv")        # question, expected
questions["actual"] = questions.question.apply(ask_the_system)
questions["correct"] = questions.apply(grade, axis=1)
print(questions.correct.mean())                 # the number you report
```

Run it before a change and after. The delta is the claim.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] pandas 10-minute intro, then load a real CSV and answer three questions about it.
- [ ] Call the Salesforce REST API with `requests` and `json_normalize` the result.
- [ ] Call the Claude API and parse a structured JSON response.
- [ ] Scaffold a Code Extension project with the Data Custom Code SDK and deploy a trivial function.
- [ ] Write the evaluation-harness script above for the [RAG capstone](../../04-capstone/02-rag-assistant-crm/notes.md).

## Gotchas & sharp edges

- **Always set a `timeout` on `requests`.** Without one it can hang indefinitely — which in an agent context means a retry, and a retry can mean a duplicate write.
- **Call `raise_for_status()`.** A 4xx returns a perfectly valid response object; silently parsing it produces confusing downstream errors.
- **Chained pandas assignment** triggers `SettingWithCopyWarning` and sometimes silently doesn't assign. Use `.loc`.
- **`json_normalize` flattens one level by default** — pass `record_path` / `max_level` for deeper structures.
- **Don't commit tokens.** Environment variables, not literals — and note the Salesforce CLI now redacts secrets from its own output by default for the same reason.
- **Code Extension is Python only** and runs in isolated containers; author ≠ operator (running and monitoring needs the Data Cloud Architect permission set).

## Related topics

- [Data 360 DevOps](../../01-data-cloud/09-data-360-devops/notes.md) — Code Extension workflow
- [Vector DB & unstructured](../../01-data-cloud/07-vector-db-unstructured/notes.md) — custom chunking, the main use case
- [Claude API](../../03-claude-cca/01-claude-api/notes.md) — calling models from Python
- [Data engineering patterns](../04-data-engineering/notes.md)
- [SQL fluency](../01-sql/notes.md) — the other data-manipulation tool
