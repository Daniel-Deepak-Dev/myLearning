# Learning log

What you fed, when, and where it landed.

Your memory works by date. The vault works by topic. This file joins the two.

Each `INDEX.md` also carries `Created` and `Updated` columns, so you can go the other way — from a topic back to the day.

Newest first.

## Format

```
### YYYY-MM-DD · <short title>

<one line of framing, or **No notes fed — a structural change.**>

- **<Topic>** → [path](path) · `new` or `updated` · Level: basic
  - <what was learnt, or what changed>

**Also touched:** <reciprocal links, index fixes, glossary rows>
```

---

### 2026-09-20 · Metadata moved to frontmatter; the vault became usable for studying

**No notes fed — a structural change, and the largest one so far.**

The trigger was a maintenance question: every small change cost edits in many files. The last commit before this was 25 files for 9 notes' worth of knowledge — **64% bookkeeping**. Auditing that turned up something worse: **every study tracker in the vault read zero.** 0 ticked labs, 0 `Done` rows, 0 sessions logged, 0 weak answers, 0 `Last reviewed` dates. The vault had been comprehensively *written* and never *used*, while every authoring tracker was accurate. `_archive/AI_Data/REVIEW.md` had predicted exactly that and said the fix was to change the shape of the file, not the discipline.

- **Metadata is now YAML frontmatter** — 260 files, eight legacy shapes, one schema. The `>` blockquote is retired, not duplicated. Obsidian reads frontmatter as Properties, which is what makes Bases, property search and sorting possible; it could never read a blockquote.
  - Only **11 of 249 notes carried dates**, so anything time-based worked on 4% of the vault. `git log --follow` backfilled the rest — but an authored date always won, so nothing hand-written was lost. All 249 carry both now.
  - **Staleness is derived, not stamped.** The `⏳ N months old` line is gone entirely — a whole class of drift deleted rather than automated.
- **Recording a study action now costs one click.** Tick `- [x]` in the note; `PRACTICE.md`'s `Done` table is rebuilt from it. The "what broke" cell stays yours and survives every rebuild.
- **1,194 `## Recall` pairs exported** two ways from one source — a tagged Anki TSV and a per-vault `_cards.md` for the Obsidian spaced-repetition plugin, with scheduling preserved across regenerations.
- **[HOME.md](HOME.md) answers "what do I study next"** and is generated, so it cannot rot the way the archived `REVIEW.md` did. It surfaces *one* unblocked lab, not a list of 41 — a list of 41 is what produced 0 ticks.
- **Reciprocity relaxed to cross-vault links only.** The universal rule sat at 50% compliance, broken even in notes written the same week it was restated. Obsidian's Backlinks panel covers same-vault links for free. **447 findings became 31**, all real seams.
- **`scripts/vault.py`** grew to 23 check rules and 6 fixers, plus `migrate`, `cards` and `home`. Verified by corrupting four derived values across three files and requiring `fix` to restore a byte-identical tree.

**Also touched:** the contract collapsed — "Never YAML frontmatter" was stated in **7 files** and every one had to be reversed, which is the clearest argument yet for one normative source. [NOTES-SYSTEM.md](NOTES-SYSTEM.md) is now it; `_note-template.md` is a pointer to [templates/note.md](templates/note.md) and its 43-line rule comment is deleted; the `study-notes` skill shed the 12 mechanical steps `fix` now performs. Two live bugs fixed in the same pass: `SF_core/_template.md` and `Interview/_template.md` would have recreated the retired format, and `/human-vs-agent` was refusing all 20 Experience Cloud notes.

**Still open:** 31 cross-vault seams need a hand-written reason clause — listed in [HOME.md](HOME.md). The Obsidian spaced-repetition plugin is not installed yet, so in-Obsidian review does not work; the Anki half does.

---

### 2026-09-19 · Experience Cloud promoted to its own vault

**No notes fed — a structural change.**

`SF_core/05-experience-cloud-lwr/` became the root-level vault **[SF_Experience_Cloud/](SF_Experience_Cloud/INDEX.md)**, a peer of `SF_core/`, `SF_Agentforce/` and `SF_Data_360/`. All 20 topic files moved unchanged, numbering intact.

- **65 inbound links across 27 files** repointed, and **~100 outbound links** from the moved notes rewritten back into `SF_core/`.
- **63 link labels** normalised from `05-experience ·` to `SF_Experience_Cloud ·`, matching the `SF_Agentforce ·` convention.
- New in the vault: `AGENTS.md` (scope, routing test, the four live currency traps) and `_inbox.md`.
- **Currency and the build record stayed in `SF_core/`** — [CURRENCY.md](SF_core/CURRENCY.md) is one ledger for the whole platform.
- Routing updated in [AGENTS.md](AGENTS.md), [NOTES-SYSTEM.md](NOTES-SYSTEM.md) and the `study-notes` skill: the test is now **strip the product out of the sentence — is it still true?**

**Also this day:** reasoning recorded in [NOTES-SYSTEM.md](NOTES-SYSTEM.md#decisions-log).

---


### 2026-08-30

Fed: Flex prompt template · template-triggered prompt flow · Add Prompt Instructions. The open question was **where a Flex template is actually used**.

- **Flex Prompt Templates** → [SF_Agentforce/flex-prompt-templates.md](SF_Agentforce/flex-prompt-templates.md) · `new` · Level: working
  - The answer: the other five types own a surface, Flex owns none. **If you can point at the button Salesforce already built for it, use that type — if not, it is Flex.** Four callers: agent action, Flow, Apex/LWC, REST.
  - Also touched: [prompt-template-types.md](SF_Agentforce/prompt-template-types.md) — the Flex row said *"anywhere"*, which was a shrug; now it says *no entry point of its own*.
- **Calling a prompt template from Flow** → [SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md](SF_core/04-flow-and-automation/28-calling-prompt-templates-from-flow.md) · `new` · Level: working
  - The missing fact behind the confusion: an **activated** template is automatically an invocable action, under the **Prompt Template** category in the Actions element.
  - **Flow and prompt templates point two ways.** A template-triggered prompt flow feeds the template while it resolves; an ordinary flow calls the template and reads the text back. Both get called "prompt flows".
  - Also touched: [template-triggered-prompt-flows.md](SF_Agentforce/template-triggered-prompt-flows.md), [23-flows-as-agentforce-actions.md](SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md), [32-invoking-prompt-templates-from-apex.md](SF_core/02-apex-and-triggers/32-invoking-prompt-templates-from-apex.md), [01-automation-landscape-and-tool-selection.md](SF_core/04-flow-and-automation/01-automation-landscape-and-tool-selection.md).
- **6 labs added** — `AF-FLEX-01..03` queued at [PRACTICE.md](SF_Agentforce/PRACTICE.md) #12–14, and `SF-PTFLOW-01..03` which sit in their note only, because `SF_core` has no `PRACTICE.md` yet.

---

### 2026-08-28 · hands-on labs for SF_Agentforce

Not a feed either — the notes now say what to *do*, not just what is true.

- **35 labs** added as `## Hands-on` sections across all 9 notes, 3–4 each, one line apiece. Every lab carries an ID (`AF-TRUST-01`), a time box and a **`Proves:`** — a lab without a *Proves* is a chore, not a lab.
- **Roughly a third break something on purpose**, mined straight from each note's `## Gotchas`: deactivate the active version and watch the template stop working, leave a prompt flow as a draft and hunt for it, write a vague action instruction and watch the agent not call it, push a masked prompt past 65,536 tokens.
- **Labs are ticked, not deleted** — the opposite of the gap rule. A settled question is clutter; work you did is a record. They never count towards `Status`.
- **11 labs settle an open 🚩** in their note's `## Confirm in org`, and say which.
- New **[SF_Agentforce/PRACTICE.md](SF_Agentforce/PRACTICE.md)** — ▶ Next, In flight (max 3), a Queue and a Done table. The queue is **unblocked-first**, not INDEX order: nothing needs Data 360 until #22, nothing needs a second org until #34.
- **A lab is not finished until you have written down what broke, verbatim.** That is the Done table's last column, and the reason it exists — an exact error string is still what you search for in six months.

Shape reused from the retired `_archive/AI_Data/` vault, which had solved this and took the solution with it. Quarried, not linked.

**System changes.** `## Hands-on` added to [_note-template.md](_note-template.md), [NOTES-SYSTEM.md](NOTES-SYSTEM.md) (with the three-way split: gaps are a reading list, org checks are questions an org settles, labs are skills you build), the `study-notes` skill (new **§5a Lab pass**, plus a PRACTICE.md queue row in §8), and both `AGENTS.md` files.

---

### 2026-08-28 · drained every open gap in SF_Agentforce

Not a feed — a closing pass. All **30** open gaps were either answered or reclassified. **No new note was spawned**, which is why the count fell this time instead of moving sideways.

- [Einstein Trust Layer](SF_Agentforce/einstein-trust-layer.md) · `updated` — default masked entities (**Name, Email, Phone, Credit Card, US SSN**), per-entity toggle, `PERSON_0` token shape, **masking caps the context window at 65,536 tokens**, checksum validation. **Toxicity is scored 0–1 and returned *with* the response — it does not block.** Audit trail lives in Data 360 DMOs.
- [Atlas Reasoning Engine](SF_Agentforce/atlas-reasoning-engine.md) · `updated` — Atlas itself is not configurable; you author the agent around it. Loop bounded at **seven reasoning loops**, ~last six turns (🚩 from a search snippet). Reasoning is visible afterwards through **Agentforce Session Tracing**, over `ssot__TelemetryTraceSpan__dlm` and `ssot__AiAgentInteraction__dlm`.
- [Template-Triggered Prompt Flows](SF_Agentforce/template-triggered-prompt-flows.md) · `updated` — the four **capability bindings**, the additive **Add Prompt Instructions** element, and the reuse rule: a type binding serves every template of that type, `FlexTemplate://` serves one.
- [Grounding a Prompt Template](SF_Agentforce/grounding-a-prompt-template.md) · `updated` — index vs retriever, where each is built, what the retriever exposes, and the **20-result default**. Sources combine rather than compete.
- [Prompt Templates as Agent Actions](SF_Agentforce/prompt-templates-as-agent-actions.md) · `updated` — `GenAiFunction` / `GenAiPlugin` shape. **`GenAiFunction` has no version field**, so an action always resolves to the active version. 20 credits (~$0.10) per standard action.
- [Prompt Template Metadata & Deployment](SF_Agentforce/prompt-template-metadata-and-deployment.md) · `updated` — why the active-version pointer cannot arrive orphaned, and that retrieve never pulls a dependent Data 360 retriever.

**Two duplicates removed** — the Flex-only-agent-action question was open in two notes, the version-cap question in two more. Each now has one owner and a cross-link.

**System changes.** Org-only questions moved to a new `## Confirm in org` section and no longer count towards `Status`; **14** of them remain. The `study-notes` skill gained a **§5b Close pass** so feeding notes drains gaps instead of only adding them. The 50-line ceiling now counts to `## Related` — the footer of links, sources and history is exempt.

**Also touched:** `GLOSSARY.md` gained Agentforce Session Tracing, `GenAiFunction`, `GenAiPlugin`; `SF_Agentforce/INDEX.md` gained an **Org ✓** column.

---

### 2026-08-28 · answered the open questions on Versions & Access

- **Prompt Template Metadata & Deployment** → [SF_Agentforce/prompt-template-metadata-and-deployment.md](SF_Agentforce/prompt-template-metadata-and-deployment.md) · `new` · Level: working
  - `GenAiPromptTemplate` carries **every version** plus `activeVersionIdentifier`. Deployment moves the whole history and the choice of which is live.
  - **Published versions cannot be edited by UI *or* Metadata API** — the immutability rule is platform-wide.
  - `GenAiPromptTemplateActv` is a different type: Salesforce-provided templates only, and it just sets Allowed/Blocked.
- [Prompt Template Versions & Access](SF_Agentforce/prompt-template-versions-and-access.md) · `updated` — the two permission sets are **alternatives, not a hierarchy**.
- Two questions survive as 🚩: whether there is a version cap (none documented anywhere I could reach), and whether Manager also confers User's run rights.

---

### 2026-08-28 · answered the open questions on Prompt Template Types

- **Prompt Templates as Agent Actions** → [SF_Agentforce/prompt-templates-as-agent-actions.md](SF_Agentforce/prompt-templates-as-agent-actions.md) · `new` · Level: working
  - **Flex** is the type you expose. Wiring is Agent Assets → New Agent Action → reference type *Prompt Template*, then add it to a topic.
  - The action's instructions are the specification Atlas reads — not documentation.
- [Prompt Template Types](SF_Agentforce/prompt-template-types.md) · `updated` — added a **Surfaces in** column; Sales Email's recipient turns out to be a **picker set at creation**, not a fixed object.
- Three questions survive as 🚩: whether the recipient picker offers Lead, whether Knowledge Answers works outside an agent, and whether any type but Flex can be an agent action. None is documented either way.

---

### 2026-08-28 · answered the open questions on Prompt Builder

Researched the four open questions on [Prompt Builder & Prompt Templates](SF_Agentforce/prompt-builder-and-prompt-templates.md). Three answered outright, one flagged.

- **Prompt Template Versions & Access** → [SF_Agentforce/prompt-template-versions-and-access.md](SF_Agentforce/prompt-template-versions-and-access.md) · `new` · Level: basic
  - Setup → Einstein Setup; **Prompt Template Manager** builds, **Prompt Template User** runs.
  - An activated version is **immutable** — rollback means activating an earlier version. Deactivate the active one and *nothing* is active.
- **Grounding a Prompt Template** → [SF_Agentforce/grounding-a-prompt-template.md](SF_Agentforce/grounding-a-prompt-template.md) · `new` · Level: working
  - Six sources: record merge fields, related lists, Flow, Apex, retrievers, Data 360 enrichment.
  - 🚩 The Contact/Lead restriction on Data 360 enrichment comes from an **April 2024** blog. Likely lifted by Summer '26 — confirm in org.
- [Prompt Builder & Prompt Templates](SF_Agentforce/prompt-builder-and-prompt-templates.md) · `updated` — ceilings confirmed (128,000 chars, 50 merge fields). Now **✅ complete**, the first note to get there.
- [Prompt Template Types](SF_Agentforce/prompt-template-types.md) · `updated` — the Flex-inputs-capped-at-5 question confirmed, and it generalises: 5 each for Flow, Apex and related lists too.

**Also touched:** `SF_core/02-apex · 31` and `01-admin · 19` gained return links; `SF_Data_360/INDEX.md`'s dead "grounding on Data 360" link now has a real target; 3 new `GLOSSARY.md` rows.

---

### 2026-08-27 · first feed

Prompt Builder, template types, Trust Layer, Atlas, Apex in templates, template-triggered flows.

- **Prompt Builder & Prompt Templates** → [SF_Agentforce/prompt-builder-and-prompt-templates.md](SF_Agentforce/prompt-builder-and-prompt-templates.md) · `new` · Level: basic
- **Prompt Template Types** → [SF_Agentforce/prompt-template-types.md](SF_Agentforce/prompt-template-types.md) · `new` · Level: basic
  - Answered your Q: **Record Prioritization** is the sixth type. It was in your `capabilityType` table but not your list.
- **Template-Triggered Prompt Flows** → [SF_Agentforce/template-triggered-prompt-flows.md](SF_Agentforce/template-triggered-prompt-flows.md) · `new` · Level: working
  - Your Manual/Automatic scenarios kept as the worked examples.
  - Your second question is partly open — 🚩 which template types accept a flow.
- **Einstein Trust Layer** → [SF_Agentforce/einstein-trust-layer.md](SF_Agentforce/einstein-trust-layer.md) · `new` · Level: basic
  - Corrected: masking stops PII leaving; **zero retention** is what stops the model learning.
- **Atlas Reasoning Engine** → [SF_Agentforce/atlas-reasoning-engine.md](SF_Agentforce/atlas-reasoning-engine.md) · `new` · Level: basic
  - Sharpened from "orchestration framework" to plan → retrieve → reason → act → refine.

**Routed to SF_core** (the Apex half of your notes):

- [02-apex · 31 Apex-grounded prompt templates](SF_core/02-apex-and-triggers/31-apex-grounded-prompt-templates.md) · `updated` — added the `recordPrioritization` capabilityType row; corrected `CapabilityType` → lowercase `capabilityType`.
- [04-flow · 23 Flows as Agentforce actions](SF_core/04-flow-and-automation/23-flows-as-agentforce-actions.md) · `updated` — disambiguated its "autolaunched only" rule from template-triggered prompt flows.

**Also this day:** `AI_Data/` retired to `_archive/`; its glossary and release radar promoted to the root. See [NOTES-SYSTEM.md](NOTES-SYSTEM.md#decisions-log).
