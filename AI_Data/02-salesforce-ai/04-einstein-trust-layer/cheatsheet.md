# Einstein Trust Layer — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

The mandatory layer between Salesforce and the LLM: secure retrieval, masking and injection defence going out; demasking, toxicity scoring, zero retention and audit coming back.

## Key terms
| Term | Definition |
|---|---|
| Secure data retrieval | Grounding runs under the running user's permissions — the model sees only what they could. |
| Data masking | PII → placeholder tokens before leaving Salesforce; real values restored in the response. |
| Zero data retention | Provider commitment: no storage, no training. **Not** an encryption feature. |
| Prompt-injection defence | Blocks "ignore your instructions and…" before the model sees it. |

## Rules of thumb

- Recite the five to a client: **masking · secure retrieval · zero retention · toxicity scoring · audit trail.**
- It governs the **model interaction only**. Platform security governs record access; agent design governs what the agent may *do*.
- It matters more in 2026 than 2025 because Headless 360, hosted MCP and triggered agents multiplied the paths in — **several with no human in the loop**.
- Under user mode, the **running user's permissions are the access control**. Pick that user deliberately.

## Exam traps / common confusions

- Zero retention ≠ "data never leaves Salesforce." It leaves; it isn't stored or trained on.
- The Trust Layer will not save you from an over-permissioned running user or a destructive action wired into an agent.
- **BYOM changes the guarantees** — verify which protections still apply end-to-end on your own endpoint.
- Audit trail is a compliance artifact; know its retention period before promising anything.

## Minimal example

The three-layer answer to "is this secure?":

```
Platform security  → who can see which records   (user mode @ 67.0)
Trust Layer        → what reaches the model      (masking, retention)
Agent design       → what the agent may DO       (actions, guardrails)

Weakest layer wins. Usually it's the running user.
```
