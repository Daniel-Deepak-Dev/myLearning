# Learning log

What you fed, when, and where it landed.

Your memory works by date. The vault works by topic. This file joins the two.

Each `INDEX.md` also carries `Created` and `Updated` columns, so you can go the other way — from a topic back to the day.

Newest first.

## Format

```
### YYYY-MM-DD

- **<Topic>** → [path](path) · `new` or `updated` · Level: basic
  - Also touched: <the reciprocal link that was added>
```

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
