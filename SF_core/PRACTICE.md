# PRACTICE — SF_core

> The file you open when the goal is **do something**. Reading lives in [README.md](README.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**3 labs · ~1 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

Most of `SF_core` is dense-format notes written before `## Hands-on` existed, so this queue is short and will stay short until those notes are refed. It is not a measure of the area.

All three currently need only **Prompt Builder** and a flow — no Agentforce licence, no Data 360, no second org.

---

## ▶ Next

**SF-PTFLOW-01 · 20 min · [04-flow · 28 Calling a prompt template from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md)**

Activate a Flex template, then call it from a screen flow and display the generation on a screen. The other two assume you have done this once.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | SF-PTFLOW-01 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 20 min | Activation alone publishes the action | — |
| 2 | SF-PTFLOW-02 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 15 min | The dependency is a string, not a reference | — |
| 3 | SF-PTFLOW-03 | [Prompt templates from Flow](04-flow-and-automation/28-calling-prompt-templates-from-flow.md) | 20 min | Two features that share a noun | — |

---

## Done

**Generated from the ticked labs — do not add rows by hand.** Tick `- [x]` in the
note and run `python scripts/vault.py fix`; the row appears here. The `What broke`
cell is yours: fill it in and it is preserved on every rebuild.

| Lab | Date | What broke — verbatim |
|---|---|---|
| — | — | — |

---

## Parked

Nothing yet. Park a lab here rather than leaving it in the queue when it is blocked on something outside your control — a licence, a Beta, a region restriction — and say what would unblock it.
