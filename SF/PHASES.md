# Build plan — 19 phases

Each phase is **one AI run** producing 8–12 topic files plus that area's `INDEX.md` link updates. Phase 00 (this skeleton) is done.

Mark a phase ✅ when its files exist and its INDEX rows are live links.

| # | Status | Title | Area | Files | Notable |
|---|---|---|---|---|---|
| 00 | ✅ | Skeleton | — | 23 | tree, README, CURRENCY, template, inventory, 9 INDEX + 9 PHASES |
| 01 | ✅ | Declarative bedrock | 01 Admin | 11 | objects, relationships, formulas, CMDT ⚠️, order of execution |
| 02 | ✅ | Modern admin surface & org ops | 01 Admin | 8 | Dynamic Forms 🆕⚠️, Approval Orchestration 🆕⚠️, Foundations 🆕 |
| 03 | ✅ | Apex core, querying & triggers | 02 Apex | 9 | limits, SOQL/SOSL, DML, handler framework, order of execution ⚠️ |
| 04 | ✅ | Apex security defaults, async & events | 02 Apex | 10 | **user mode default** 🆕⚠️, `with sharing` default 🆕⚠️, queueable ⚠️, finalizers, `Database.Cursor` 🆕 |
| 05 | ✅ | Apex closeout + LWC entry | 02 → 03 | 10 | testing ⚠️, Stub API, `@InvocableMethod` 🆕, UDT 🆕 → LWC lifecycle, `lwc:if` ⚠️ |
| 06 | ✅ | LWC data, security & navigation | 03 LWC | 9 | LDS, GraphQL wire 🆕, **LWS is the default, Locker not retired** 🆕⚠️, SLDS 2 GA Winter '26 🆕⚠️ |
| 07 | ✅ | LWC quality, modern tooling & reach | 03 LWC | 10 | Jest ⚠️, a11y ⚠️, toasts ⚠️, custom Lightning types 🆕, `sf lightning dev` 🆕⚠️, LWC OSS, **+ static resources, State Managers 🆕** |
| 08 | ✅ | Flow fundamentals → Apex interop | 04 Flow | 12 | **WF/PB end of support, not retired** ⚠️, **fault paths don't roll back** ⚠️, reactive screens + Screen Actions 🆕, Transform 🆕, **+ HTTP callout** 🆕 |
| 09 | ✅ | Flow at scale | 04 Flow | 13 | **2,000-element cap removed at API 57.0** ⚠️, Flow Tests are record-triggered only ⚠️, Orchestrator, Migrate to Flow 🆕⚠️, agent actions 🆕, **+ run context, + Pause/Wait** |
| 10 | ✅ | Access model & record sharing | 07 Security | 15 | **profile-permissions retirement CANCELLED 2026-06-06** 🆕⚠️, restriction rules subtract ⚠️, **queue hierarchy default flip** 🆕⚠️, **+ licences, + grantee model, + access auditing** |
| 11 | ✅ | Identity, encryption & monitoring | 07 Security | 11 | **MFA enforced, phishing-resistant for admins** 🆕⚠️, **async sharing recalc RU** 🆕⚠️, **domain redirections ended** ⚠️, step-up 🆕, **Security Center Essentials free** 🆕, **+ session/login policies, + Field Audit Trail** |
| 12 | ✅ | APIs: REST → legacy streaming | 06 Integration | 14 | API retirement treadmill 🆕⚠️ (**410 GONE**), composite, Bulk 2.0 ⚠️, GraphQL 🆕, **Pub/Sub is recommended, it replaced nothing** 🆕⚠️, **+ endpoints/instanced-URL deadline, + Metadata/Tooling/Connect** |
| 13 | ✅ | Auth, external apps & agent-facing integration | 06 Integration | 12 | OAuth ⚠️, **External Client Apps** 🆕⚠️ (**device flow blocked since Sept 2025**), named credentials ⚠️ (**deprecated, no date**), API Catalog 🆕, Event Relay 🆕, MCP servers 🆕 (**no M2M flow**), **+ certificates & the PKI clock** 🆕⚠️ |
| 14 | ✅ | Data modeling & LDV performance | 08 Data | 14 | **Async SOQL retired Summer '23** ⚠️ (the plan named a dead feature), selectivity thresholds, Query Plan, skew, skinny tables, **+ record locking, + deletes/Recycle Bin, + storage model, + Person Accounts** |
| 15 | ⬜ | Retention, federation & data operations | 08 Data | 10 | big objects, archiving 🆕, zero-copy Data 360 🆕, backup ⚠️, Hyperforce 🆕 |
| 16 | ⬜ | Source-driven dev & 2GP packaging | 09 DevOps | 11 | **`sf` v2 replaces `sfdx`** 🆕⚠️, scratch orgs, unlocked 2GP 🆕⚠️, DevOps Center 🆕⚠️ |
| 17 | ⬜ | CI/CD, code quality & release ops | 09 DevOps | 11 | GitHub Actions, Code Analyzer v5 🆕⚠️, ApexGuru 🆕, Agentforce DX 🆕 |
| 18 | ⬜ | LWR sites: architecture → auth | 05 Experience | 10 | **LWR default, Aura legacy** 🆕⚠️, SSR/CDN, guest hardening ⚠️, licences, SSO |
| 19 | ⬜ | Site content, headless, performance & agents | 05 Experience | 8 | Enhanced CMS 🆕, headless 🆕, SEO 🆕, ExperienceBundle ⚠️, embedded agents 🆕 |

**208 topic files.** Exact file lists live in each area's `PHASES.md`. *(Phase 07 added two beyond plan — see [03-lwc/PHASES.md](03-lwc-and-slds/PHASES.md). Phase 08 added two and renumbered phase 09; **phase 09 added two more and renumbered again**, this time with live inbound links — see [04-flow/PHASES.md](04-flow-and-automation/PHASES.md). **Phase 10 added three and renumbered area 07 into learning order** — free, because no file in the area existed yet and only three inbound links named it by number. **Phase 11 added two more**, appending and shifting only 16–26 so the 15 existing files never moved; see [07-security/PHASES.md](07-security-and-sharing/PHASES.md). **Phase 12 added two and renumbered area 06 into learning order** — again free, no file in the area existed, and all 13 inbound numeric references were link *text* over an `INDEX.md` href, so nothing broke; see [06-integration/PHASES.md](06-integration-and-apis/PHASES.md). **Phase 13 added one and appended it**, honouring phase 12's own warning — 15–25 were already named by number from areas 02 and 07, so certificates went on the end as **26** and nothing moved. **Phase 14 added four and renumbered area 08 into learning order** — free for the third time, because no file in the area existed and all ~25 inbound links pointed at `INDEX.md`; the five that named a number did so in link *text*, and the phase's own link sweep was touching those files anyway. Phase 15 shifted to **15–24**; see [08-data/PHASES.md](08-data-modeling-and-large-data-volumes/PHASES.md).)*

## Sequencing

- **03–07 before 08–09** — Flow notes reference governor limits and invocable Apex signatures.
- **10–11 before 12–13 and 18–19** — OAuth, named credentials and guest hardening all rest on the access model.
- **16–17 before 18–19** — Experience Cloud deployment assumes 2GP and pipeline vocabulary.
- **Movable:** 15 (retention & data operations) can run any time. Nothing downstream depends on it. *(14 ran here, out of numeric order with 16–19 still open — that was the point of calling the block movable.)*

## Standing rules for every phase

1. Write **only** the listed files plus that area's `INDEX.md` row updates. Never let a phase sprawl.
2. **Hard cap ~80 lines per file.** If a topic won't fit, split the taxonomy rather than writing long.
3. Every 🆕 topic is researched against Summer '26 release notes **before** writing.
4. Every ⚠️ topic **opens with a one-line "What changed"** correction, before `## Core idea`.
5. Cross-link into `AI_Data/` rather than duplicating Agentforce/Data 360 content; link to `AI_Data/05-release-radar/` for currency detail.
6. Where [_notion-seed/INVENTORY.md](_notion-seed/INVENTORY.md) maps an old note to the topic, harvest the genuine gotcha into a `> **From my notes.**` callout — **and correct it if stale.** Never copy verbatim.
7. New platform jargon → [AI_Data/GLOSSARY.md](../AI_Data/GLOSSARY.md).
8. One commit per phase: `SF: phase NN — <title>`. Flip the ⬜ to ✅ in this table in the same commit.

## Post-phase check

```powershell
# no topic file over the cap
Get-ChildItem SF -Recurse -Filter *.md |
  Where-Object { $_.Name -notin @('INDEX.md','PHASES.md','CURRENCY.md','README.md','INVENTORY.md','_template.md') } |
  ForEach-Object {
    $n = @(Get-Content $_.FullName).Count
    if ($n -gt 85) { "$($_.Name): $n lines" }
  }
```

> **Fixed in phase 08, two bugs.** It used `(Get-Content … | Measure-Object -Line).Lines`, which **does not count blank lines** — an 81-line file reported as 59, ~27% low, so the `-gt 85` gate was really at ~117 real lines and had never fired. It also scanned `INDEX.md`, `PHASES.md`, `CURRENCY.md` and `INVENTORY.md`, none of which the cap applies to; with the count fixed those became permanent false positives.

Then grep the phase output for `WITH SECURITY_ENFORCED`, `sfdx force:`, `if:true`, `Locker`, `CometD` — each may appear **only** inside a ⚠️ correction, never as current guidance. Since phase 08, add **`retired`** near *Workflow* or *Process Builder*: end of support is not retirement. Since phase 10, add **`retire`/`retirement`/`deprecat` near *profile***, and any sentence implying a profile **end-of-life date** — the retirement of permissions in profiles was **cancelled on 2026-06-06** and there is no date to state.

Since phase 11, five more — the mid-2026 enforcement wave turned a lot of advice into fact:

- **MFA described as `recommended`, `optional` or `best practice`.** It is enforced, and phishing-resistant for privileged users.
- **`Salesforce Authenticator`, `TOTP` or `SMS` offered as sufficient MFA** without the carve-out that they no longer qualify for admin-grade access.
- **`Transaction Security` unqualified** where the current framework is meant — the legacy one is retired, *Enhanced* is the name.
- **`Security Center` near `paid`** without the **Essentials** qualifier: Essentials has been free in every org since July 2026.
- **Any claim a legacy My Domain URL `redirect`s.** Redirections ended in Spring '26; it 404s.

Since phase 12, four more — and one **amendment to the rule above**:

- **`CometD` is no longer a banned-as-current term.** The old rule said it may appear only inside a ⚠️ correction. That was built on the belief that Pub/Sub replaced it, which is wrong: `lightning/empApi` is supported, current, and CometD-based. **Grep instead for `CometD` or `Streaming API` within a line of `retired`, `dead`, `replaced`, `superseded` or `deprecated`** — those are the false claims. *(`superseded` added in phase 13: it was missing from this list, and a line in [04-flow · 07](04-flow-and-automation/07-platform-event-and-async-path-flows.md) reading "CometD is superseded by the Pub/Sub API" survived the phase-12 sweep because of it. Fixed.)*
- **`lightning/empApi` described as legacy.** It is the supported in-org LWC subscriber. Only *PushTopic* and *generic* events carry the docs' *(Legacy)* label.
- **Any asserted retirement date for an API version above 30.0.** 21.0–30.0 retired Summer '25; **no next wave is announced.** Also flag any sentence that turns the SOAP `login()` retirement (API 31.0–64.0, **Summer '27**) into a *version* retirement — it withdraws one call, not those versions.
- **`SOAP` near `retired` or `dead`.** `login()` is retiring; the API is not, and it *gained* JWT support at 67.0.
- **`Sforce-Enable-PKChunking` presented as Bulk API 2.0.** It is a **v1** header and does nothing in 2.0.

Since phase 13, seven more — and note that the phase-13 defect was a **wrong date on a correct retirement**, not another "old ≠ dead". Both failure modes now have rules:

- **`login()` near `Spring '27`.** The date is **Summer '27** (Help article 005132110). It was wrong in seven lines across five files for two phases. **Verify a date against the Help article, never against another note in this vault.**
- **`Connected App` presented as the way to set up a new integration**, or any runbook step reading *"create a connected app"*. Creation is Support-gated since Spring '26. Equally flag **`Connected App` near `retired`** — existing ones are not.
- **username-password flow described as blocked `by default`** without the **new-orgs-only** carve-out. Blocked by default from Summer '23 for orgs created then or later; an older org may still be running it.
- **`legacy named credential` near any date.** Deprecated, **no retirement date published**.
- **`Event Relay` near `Azure`, `GCP` or `Google`.** Amazon EventBridge is the only destination.
- **`MCP` near `service account`, `client credentials` or `machine-to-machine`.** Authorization code only — there is no M2M flow.
- **`certificate pinning` presented as good practice.** Salesforce's guidance is to stop; validity reaches 47 days in 2029.

Since phase 14, six more — **and the direction of the check changes here.** Every rule above this line guards against calling a live thing dead. Phase 14's defect was the opposite: the plan named **Async SOQL**, retired since Summer '23, as a topic to write about. **Both directions now need checking, and a plan's own file list is not evidence a feature exists.**

- **`Async SOQL` presented as available.** Retired **Summer '23** (Help 000394892); the answer is **Bulk API query or Batch Apex**. May appear **only** inside a ⚠️ correction. Note that Async SOQL was the *headline* feature at big-object GA, so nearly every pre-2023 tutorial leads with it.
- **`Big Object` near `retired`.** Big objects are current at 67.0 — only the query mechanism went. The inverse error to the one above, in the same sentence's neighbourhood.
- **`semi-join` or `anti-join` near `Summer '26`, `new` or `now available`.** The Summer '26 item by that name is **Data Pipelines / recipes**, not SOQL. SOQL semi-joins are ancient — the seed corpus has a 2019 note on them.
- **A selectivity threshold quoted with only one tier or without the cap.** Standard is **30% / 15%, cap 1,000,000**; custom is **10% / 5%, cap 333,333**. Half-quoting is the usual form of this error.
- **`skinny table` described as self-service**, or as something you can view in Setup. It is a Support request, invisible to you, and re-requested every time the field set changes.
- **`delete` described as freeing storage or restoring performance immediately.** Soft-deleted rows keep costing both until physically purged. Equally flag **`formula field` + `never indexed`** stated flatly — a **deterministic, single-object** formula can be indexed by Support; a cross-object one never can.
