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
| 11 | ⬜ | Identity, encryption & monitoring | 07 Security | 9 | MFA ⚠️, SSO, enhanced domains ⚠️, Shield, Event Monitoring, secure-coding checklist ⚠️ |
| 12 | ⬜ | APIs: REST → legacy streaming | 06 Integration | 12 | API retirement treadmill 🆕⚠️, composite, Bulk 2.0 ⚠️, GraphQL 🆕, **Pub/Sub replaces CometD** 🆕⚠️ |
| 13 | ⬜ | Auth, external apps & agent-facing integration | 06 Integration | 11 | OAuth ⚠️, **External Client Apps** 🆕⚠️, named credentials ⚠️, Event Relay 🆕, MCP servers 🆕 |
| 14 | ⬜ | Data modeling & LDV performance | 08 Data | 10 | relationships, external IDs, selectivity, Query Plan, skew, skinny tables |
| 15 | ⬜ | Retention, federation & data operations | 08 Data | 10 | big objects, archiving 🆕, zero-copy Data 360 🆕, backup ⚠️, Hyperforce 🆕 |
| 16 | ⬜ | Source-driven dev & 2GP packaging | 09 DevOps | 11 | **`sf` v2 replaces `sfdx`** 🆕⚠️, scratch orgs, unlocked 2GP 🆕⚠️, DevOps Center 🆕⚠️ |
| 17 | ⬜ | CI/CD, code quality & release ops | 09 DevOps | 11 | GitHub Actions, Code Analyzer v5 🆕⚠️, ApexGuru 🆕, Agentforce DX 🆕 |
| 18 | ⬜ | LWR sites: architecture → auth | 05 Experience | 10 | **LWR default, Aura legacy** 🆕⚠️, SSR/CDN, guest hardening ⚠️, licences, SSO |
| 19 | ⬜ | Site content, headless, performance & agents | 05 Experience | 8 | Enhanced CMS 🆕, headless 🆕, SEO 🆕, ExperienceBundle ⚠️, embedded agents 🆕 |

**199 topic files.** Exact file lists live in each area's `PHASES.md`. *(Phase 07 added two beyond plan — see [03-lwc/PHASES.md](03-lwc-and-slds/PHASES.md). Phase 08 added two and renumbered phase 09; **phase 09 added two more and renumbered again**, this time with live inbound links — see [04-flow/PHASES.md](04-flow-and-automation/PHASES.md). **Phase 10 added three and renumbered area 07 into learning order** — free, because no file in the area existed yet and only three inbound links named it by number; see [07-security/PHASES.md](07-security-and-sharing/PHASES.md).)*

## Sequencing

- **03–07 before 08–09** — Flow notes reference governor limits and invocable Apex signatures.
- **10–11 before 12–13 and 18–19** — OAuth, named credentials and guest hardening all rest on the access model.
- **16–17 before 18–19** — Experience Cloud deployment assumes 2GP and pipeline vocabulary.
- **Movable:** 14–15 (data modeling) can run any time after 02 if you want the data layer early. Nothing downstream depends on it.

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
