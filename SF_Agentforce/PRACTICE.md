# PRACTICE — SF_Agentforce

> The file you open when the goal is **do something**. Reading lives in [INDEX.md](INDEX.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**38 labs · ~13 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

The queue is **unblocked-first**, not INDEX order:

- **#1–18** need only Prompt Builder. Two of them want a second test user.
- **#19–22** add **Agentforce** itself. (#23–24 drop back to Prompt Builder only.)
- **#25–34** are the first to need **Data 360**.
- **#37–38** are the only ones needing a **second org**.

That split is deliberate. Prompt Builder and Data 360 were only ever coupled by accident, and coupling them is what makes practice feel like it needs a spare weekend.

---

## ▶ Next

**AF-PB-01 · 20 min · [Prompt Builder & Prompt Templates](prompt-builder-and-prompt-templates.md)**

Build a record-grounded template on Account, then run it against a fully populated record and an almost-empty one. Everything else assumes you have done this once.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | AF-PB-01 | [Prompt Builder](prompt-builder-and-prompt-templates.md) | 20 min | Empty grounding reads as hallucination | — |
| 2 | AF-PB-02 | [Prompt Builder](prompt-builder-and-prompt-templates.md) | 15 min | Renaming breaks callers silently | — |
| 3 | AF-PB-03 | [Prompt Builder](prompt-builder-and-prompt-templates.md) | 25 min | The ceiling counts the *resolved* prompt | — |
| 4 | AF-TYPE-01 | [Types](prompt-template-types.md) | 20 min | Type fixes object and context at creation | — |
| 5 | AF-TYPE-02 | [Types](prompt-template-types.md) | 10 min | Type cannot be changed later | — |
| 6 | AF-TYPE-03 | [Types](prompt-template-types.md) | 20 min | Prioritization sees only your own records | — |
| 7 | AF-TYPE-04 | [Types](prompt-template-types.md) | 15 min | Whether Knowledge Answers is agent-only | — |
| 8 | AF-VER-01 | [Versions & Access](prompt-template-versions-and-access.md) | 15 min | An active version is immutable | — |
| 9 | AF-VER-02 | [Versions & Access](prompt-template-versions-and-access.md) | 10 min | Deactivating leaves *nothing* active | — |
| 10 | AF-VER-04 | [Versions & Access](prompt-template-versions-and-access.md) | 15 min | Rollback is "activate an earlier one" | — |
| 11 | AF-VER-03 | [Versions & Access](prompt-template-versions-and-access.md) | 20 min | Whether Manager confers run rights | test user |
| 12 | AF-FLEX-01 | [Flex Templates](flex-prompt-templates.md) | 25 min | Flex has no surface — you supply the caller | — |
| 13 | AF-FLEX-02 | [Flex Templates](flex-prompt-templates.md) | 10 min | Activation is what publishes the action | — |
| 14 | AF-FLEX-03 | [Flex Templates](flex-prompt-templates.md) | 15 min | The 5-resource cap is real | — |
| 15 | AF-FLOW-01 | [Prompt Flows](template-triggered-prompt-flows.md) | 30 min | Add Prompt Instructions is additive | — |
| 16 | AF-FLOW-02 | [Prompt Flows](template-triggered-prompt-flows.md) | 10 min | A draft flow is invisible, silently | — |
| 17 | AF-FLOW-03 | [Prompt Flows](template-triggered-prompt-flows.md) | 20 min | What a mid-run fault does to the prompt | — |
| 18 | AF-FLOW-04 | [Prompt Flows](template-triggered-prompt-flows.md) | 20 min | Running user or system mode | test user |
| 19 | AF-ACT-01 | [Agent Actions](prompt-templates-as-agent-actions.md) | 30 min | The two-step wiring: action, then topic | Agentforce |
| 20 | AF-ACT-02 | [Agent Actions](prompt-templates-as-agent-actions.md) | 25 min | The instruction *is* the specification | Agentforce |
| 21 | AF-ACT-04 | [Agent Actions](prompt-templates-as-agent-actions.md) | 15 min | Whether any type but Flex works | Agentforce |
| 22 | AF-ACT-03 | [Agent Actions](prompt-templates-as-agent-actions.md) | 20 min | Nothing is pinned — behaviour shifts under you | Agentforce |
| 23 | AF-GRND-03 | [Grounding](grounding-a-prompt-template.md) | 20 min | The six sources combine, not compete | — |
| 24 | AF-TRUST-03 | [Trust Layer](einstein-trust-layer.md) | 20 min | Masking pushes you over the token limit | — |
| 25 | AF-GRND-01 | [Grounding](grounding-a-prompt-template.md) | 40 min | Relevance tuning lives on the retriever | Data 360 |
| 26 | AF-GRND-02 | [Grounding](grounding-a-prompt-template.md) | 15 min | The 20-result default eats the budget | Data 360 |
| 27 | AF-GRND-04 | [Grounding](grounding-a-prompt-template.md) | 20 min | Whether the Contact/Lead limit has lifted | Data 360 |
| 28 | AF-TRUST-01 | [Trust Layer](einstein-trust-layer.md) | 25 min | The model saw `PERSON_0`, not the name | Data 360 |
| 29 | AF-TRUST-02 | [Trust Layer](einstein-trust-layer.md) | 15 min | The masking toggle really is per entity | Data 360 |
| 30 | AF-TRUST-04 | [Trust Layer](einstein-trust-layer.md) | 20 min | How long audit data survives | Data 360 |
| 31 | AF-ATLAS-01 | [Atlas](atlas-reasoning-engine.md) | 30 min | Reasoning is visible after the fact | Data 360 |
| 32 | AF-ATLAS-02 | [Atlas](atlas-reasoning-engine.md) | 30 min | How it breaks a tie between two actions | Data 360 |
| 33 | AF-ATLAS-03 | [Atlas](atlas-reasoning-engine.md) | 20 min | Where the chain broke, and what it cost | Data 360 |
| 34 | AF-ATLAS-04 | [Atlas](atlas-reasoning-engine.md) | 25 min | The loop is bounded — count it yourself | Data 360 |
| 35 | AF-META-01 | [Metadata & Deployment](prompt-template-metadata-and-deployment.md) | 20 min | Every version travels, plus the pointer | — |
| 36 | AF-META-03 | [Metadata & Deployment](prompt-template-metadata-and-deployment.md) | 20 min | Whether a version cap exists | — |
| 37 | AF-META-04 | [Metadata & Deployment](prompt-template-metadata-and-deployment.md) | 30 min | Whether the Flow+Apex deploy bug is live | 2nd org |
| 38 | AF-META-02 | [Metadata & Deployment](prompt-template-metadata-and-deployment.md) | 30 min | Retriever IDs are org-specific | 2nd org · needs #25 |

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
