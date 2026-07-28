# Salesforce AI Landscape — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Four stacked generations — Einstein (predict) → Einstein GPT (draft) → Copilot (assist) → **Agentforce** (act) — sitting on Data 360 for grounding and the Trust Layer for control, all reachable headlessly as of Summer '26.

## Key terms
| Term | Definition |
|---|---|
| Agentforce 360 | The 2026 platform umbrella: agents + Data 360 + Tableau + Slack. Not a version number. |
| Atlas Reasoning Engine | The agent brain. **v3.0** routes to subagents by reading their descriptions. |
| Headless 360 | Every capability = API, MCP tool, or CLI command. The Summer '26 organizing idea. |
| Einstein Copilot | **Historical.** Folded into Agentforce. A source using it as current is out of date. |

## Rules of thumb

- Diagnose failures **bottom-up**: grounding → prompt → reasoning → access mode. Most "bad AI" is grounding or staleness.
- Model choice is yours (Claude / OpenAI / Gemini) and **pinnable per agent** in Agent Script — a cost/latency decision, not a default.
- Agentforce without Data 360 grounding is a polite chatbot. The grounding is the product.

## Exam traps / common confusions

- **Einstein ≠ generative.** Classic predictive Einstein still ships and still appears on exams.
- **Copilot is not current.** Neither is topic-and-instruction authoring (legacy since **July 13, 2026**).
- **The 16 cert renames are cosmetic** — *Agentforce Sales Consultant* etc.; no content or exam-code change.
- Agentforce Specialist now includes **Multi-Agent Interoperability (~5%)**: MCP, A2A, Agent API.

## Minimal example

Failure triage, in the order that resolves fastest:

```
"The agent gave a wrong answer about a customer."
  1. Was the data stale?      → Accelerated Data Ingest (GA)
  2. Was it grounded at all?  → retriever / Data Library wired up?
  3. Wrong action chosen?     → Agent Script routing
  4. Wrong subagent?          → the subagent *description* is the routing contract
  5. Only then                → suspect the model
```
