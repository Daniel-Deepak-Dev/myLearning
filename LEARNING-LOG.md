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

### 2026-09-20 · Multilingual sites — three translation surfaces, and the URL question with no public answer

You fed: site language settings, language selector, per-language URLs, CMS content variants by locale, Translation Workbench for site content.

- **Multilingual Sites & Site Translation** → [SF_Experience_Cloud/21-multilingual-sites-and-translation.md](SF_Experience_Cloud/21-multilingual-sites-and-translation.md) · `new` · Level: deep
  - The spine: **three translation surfaces, three owners, three deploy routes.** Builder-authored strings translate inline in the component property editor; org metadata goes through **Translation Workbench**; CMS content becomes a **variant** in the workspace. Merging the three is what makes a translation estimate wrong.
  - Concrete: **40 languages including the default**, set in Experience Builder → Settings → Languages. Bulk route is export → translate → import — `.xlf` XLIFF for the site, zipped XLIFF per CMS workspace, STF also offered by the Workbench.
  - **Corrected your note: “per-language URLs” is not a documented Experience Cloud feature.** No reachable first-party page says a language gets its own URL, path or subdomain. Every documented switch is a runtime selection — the Language Selector, the profile language, or LWR's automatic detection. Carried as **gap 1** rather than asserted either way.
  - The sharpest gotcha is documented, not folklore: **editing default-language content while it is out for translation loses the edit**, because the import overwrites the default too. That is lab `EC-I18N-02`.
  - Left open, and both point at **16**: whether the auto-generated LWR sitemap emits per-language URLs or any `hreflang`, and whether a public page is cached **once** at the edge or **once per language** — the question a build-and-serve runtime forces and no source answers.

- **[SF_core/01-admin · 10 Custom labels & Translation Workbench](SF_core/01-admin-and-declarative-platform/10-custom-labels-and-translation-workbench.md)** · `updated` — its *“stops at Experience Cloud site localisation”* forward reference finally has a target. The bullet had been aimed at the vault INDEX because no note existed to receive it.
- **[SF_core/08-data · 22 Multi-currency, multi-language & locale](SF_core/08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md)** · `updated` — the cross-vault return link; it keeps language-vs-locale, **21** takes the site.

**Also touched:** [14](SF_Experience_Cloud/14-enhanced-cms-and-content-delivery.md), [16](SF_Experience_Cloud/16-site-performance-caching-and-seo.md) and [18](SF_Experience_Cloud/18-experience-cloud-devops.md) each gained one gotcha and a `## Related` line — variants are mostly a translation mechanism, 16's sitemap claim is untested on a multilingual site, and translations do **not** travel inside the site bundle. `SF_Experience_Cloud/PRACTICE.md` created — this vault's first — with `EC-I18N-01..04` as #1–4. 4 new `GLOSSARY.md` rows; one line in [PHASES.md](SF_Experience_Cloud/PHASES.md) recording that the area closed at 20 and fed topics append beyond it.

**Research conditions, because they affect every citation here.** `developer.salesforce.com` and `help.salesforce.com` both return **HTTP 403** to automated fetching from this machine — the same block [RELEASE-RADAR/01-agentforce/2026-07-28.md](RELEASE-RADAR/01-agentforce/2026-07-28.md) already records. Every first-party page was read through search extracts, so every source line says `via search` rather than `read`. Three facts rest on a single third-party source and carry 🚩.

---

### 2026-09-20 · Site accessibility — who actually owes WCAG conformance

You flagged that `03-lwc · 17` covered component-level a11y and **nothing owned the site-level obligation**. Researched and filed, EU and US.

- **Site Accessibility & Conformance** → [SF_Experience_Cloud/22-site-accessibility-and-conformance.md](SF_Experience_Cloud/22-site-accessibility-and-conformance.md) · `new` · Level: working
  - The spine: **a Salesforce ACR describes Salesforce's components, not your configured site.** The EAA obliges the *service provider* — your client — so an ACR is evidence about one input, never the site's conformance claim.
  - **Two ACRs, split by runtime**, and the split follows the template decision in **01**: *Experience Cloud – LWR* covers Build Your Own (LWR) and Microsite (LWR); *Experience Cloud – Aura* covers Customer Service, Customer Account Portal and Partner Central. Both Spring '25.
  - **The version mismatch is the live trap.** Salesforce targets WCAG **2.2** AA; the EAA binds to **EN 301 549 v3.2.1 = WCAG 2.1 AA**. **v4.1.1 shipped 2 September 2026** with WCAG 2.2 and an EAA-mapping annex, but is **not yet cited in the Official Journal**, so it confers no presumption of conformity.
  - Corrected two things the internet repeats: **"fines up to €100,000 or 4% of turnover"** is not in the directive (Art. 30 leaves penalties to Member States), and **Accessibility Mode is Salesforce Classic only** — it does nothing for a site's public pages.
  - Left open: which criteria the LWR ACR marks *Partially Supports* (the PDF would not extract), whether Enhanced Chat and Mobile Publisher carry their own ACRs, and three org checks including whether a published LWR page emits a correct `<html lang>`.

- **[SF_core/03-lwc-and-slds/17](SF_core/03-lwc-and-slds/17-accessibility-and-internationalization.md)** · `updated` — the cross-vault return link. It keeps the component half; **22** takes the obligation.

**Also touched:** [RELEASE-RADAR/trust-security-and-governance.md](RELEASE-RADAR/trust-security-and-governance.md) — the *"accessibility enhancements, no obtainable per-component detail"* gap is **closed**. It is **two** Release Updates, both for **WCAG 2.2 *Resize and Reflow***, both **postponed twice** into Winter '27. The governance point is that a vendor's conformance target is dated and the date moves. 4 new `GLOSSARY.md` rows; first `## Hands-on` labs in this vault queued in `SF_Experience_Cloud/PRACTICE.md` as #5–8.

**Note for the record:** this note landed in parallel with the multilingual-sites feed from another session. Both were briefly numbered 21; settled by creation order — multilingual **21**, accessibility **22**.

---

### 2026-09-20 · Experience Cloud verification pass — the vault's own correction was wrong

**No notes fed — a verification run over the 20 `SF_Experience_Cloud/` notes.**

`scripts/vault.py check` was clean before and after; every finding here was a **factual** one, invisible to the mechanical rules.

**The headline: phase 19 overcorrected, and the overcorrection was load-bearing.** Experience Delivery *is* discontinued as of Winter '27 — phase 19 had that right. But it was the **Cloudflare-backed hosting tier**, and phase 19 recorded its withdrawal as *"an LWR site has no server-side rendering."* **Islands SSR is a standard LWR Experience Cloud capability**, on by default on Build Your Own (LWR) standard pages, gated per page by `lightning__ServerRenderable` on the theme layout, with `lightning__ServerRenderableWithHydration` for components that stay interactive. The false claim had reached five notes, `INDEX.md`, `GLOSSARY.md`, `SF_core/CURRENCY.md`, `SF_core/PHASES.md`' grading rules and the vault's own `AGENTS.md` trap list.

- **[02 LWR architecture & build model](SF_Experience_Cloud/02-lwr-architecture-and-build-model.md)** · `updated` — Experience Delivery reframed as the hosting tier; SSR capabilities added; `lwr:hydrate` replaced with the Experience Cloud capability tags; the unsourced "October 2026" runway replaced with the documented behaviour (republishing migrates the site to standard LWR infrastructure).
- **[16 Site performance, caching & SEO](SF_Experience_Cloud/16-site-performance-caching-and-seo.md)** · `updated` — the heaviest rewrite: correction blockquote, core idea, caching table, SEO bullets, currency and 3 recall pairs. A crawler on a default LWR page gets real HTML, not an empty shell.
- **[15 Headless sites & Connect APIs](SF_Experience_Cloud/15-headless-sites-and-connect-apis.md)** · `updated` — the trade flipped back: "we lose SSR by going headless" is a **live** argument again, not a dead one.
- **[01](SF_Experience_Cloud/01-template-choice-and-site-landscape.md)**, **[03](SF_Experience_Cloud/03-site-setup-domains-and-publishing.md)**, **[06](SF_Experience_Cloud/06-custom-lwc-in-lwr-sites.md)** · `updated` — same correction, smaller surface.
- **[04 Experience Builder layouts & theme layouts](SF_Experience_Cloud/04-experience-builder-layouts-and-theme-layouts.md)** · `updated` — **new fact, not a correction:** the theme layout is the SSR gate. A hand-written theme layout that omits `lightning__ServerRenderable` turns SSR off for every page using it, silently.

**Second correction — `lightningCommunity__RelaxedCSP`** (notes [01](SF_Experience_Cloud/01-template-choice-and-site-landscape.md) and [06](SF_Experience_Cloud/06-custom-lwc-in-lwr-sites.md)). Both stated that a managed-package LWC is hidden in Experience Builder unless it declares this. Two errors in one line: it is a **capability**, not a target, and it only applies to sites running with **Lightning Locker / LWS off** — the relaxed-CSP case, which is where the B2B and D2C store LWR templates sit. On an ordinary Locker-on LWR site a packaged component needs no such declaration.

**Verified and correct, left alone:** legacy Chat / Live Agent end of support **14 February 2026** and the **Enhanced Chat** rename of June 2025 — note 19's dates and naming both check out against Salesforce Help.

**Also touched:** `SF_Experience_Cloud/AGENTS.md` currency trap #3 rewritten to flag *both* failure modes; `INDEX.md` banner; `GLOSSARY.md` LWR row; `SF_core/CURRENCY.md` (3 rows + a dated maintenance correction); `SF_core/PHASES.md` grading rule; both `PHASES.md` build records annotated; two cross-vault links mislabelled `SF_Agentforce · …` while pointing at `RELEASE-RADAR/` fixed in [15](SF_Experience_Cloud/15-headless-sites-and-connect-apis.md) and [18](SF_Experience_Cloud/18-experience-cloud-devops.md).

**The lesson, logged in `CURRENCY.md`:** a withdrawal names a **product**, not a capability class. Phase 19 read "Experience Delivery is discontinued" as "SSR is gone" — and a correction written as a sweeping negative (*"there is no X"*) propagates faster, and is harder to dislodge, than the error it replaced.

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
