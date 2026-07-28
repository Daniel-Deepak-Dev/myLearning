# Model Builder & BYOM — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Register which LLMs the org can use — Salesforce-hosted or your own endpoint — and select them at three levels: org default, **per agent in Agent Script**, per prompt template.

## Key terms
| Term | Definition |
|---|---|
| BYOM | External model via your endpoint and your provider contract (Bedrock, Vertex, Azure, self-hosted). |
| Model pinning | Setting the model for one agent inside its Agent Script, overriding the org default. |
| Atlas model support | Anthropic (Claude on Bedrock), OpenAI, **and Google Gemini** — all first-party. |

## Rules of thumb

- Reach for BYOM only for a nameable reason: **existing contract, data residency, a fine-tuned model, or a regulatory audit path.** "More control" alone buys operational burden.
- Claude is available **first-party via Bedrock** — don't build a BYOM integration to get it.
- Cheap fast model for high-volume triage; stronger model for the reasoning-heavy subagent. Per-action billing makes this a real cost lever.
- Hallucinating about a customer? That's **grounding**, not the model. Fine-tuning won't fix it.

## Exam traps / common confusions

- **BYOM changes Trust Layer guarantees** — zero retention then rides on *your* provider contract, not Salesforce's. Verify end-to-end; don't assume it transfers.
- **Three places set the model.** When two paths behave differently, check which model each used before debugging the prompt.
- Payload request/response mapping is the real work, and mismatches fail at **runtime**, not on save.

## Minimal example

Model selection precedence:

```
org default (Setup)
   └── overridden by → agent's Agent Script pin
         └── overridden by → prompt template setting

Design intent:
  triage subagent    → fast + cheap
  reasoning subagent → strong
  (billed per action, so depth multiplies cost)
```
