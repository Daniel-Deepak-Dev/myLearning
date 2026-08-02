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
| 08 | ⬜ | Flow fundamentals → Apex interop | 04 Flow | 11 | **WF/Process Builder retired** ⚠️, record-triggered, reactive screens 🆕, Transform 🆕 |
| 09 | ⬜ | Flow at scale | 04 Flow | 10 | limits ⚠️, Flow Tests, Orchestrator, Migrate to Flow 🆕⚠️, flows as agent actions 🆕 |
| 10 | ⬜ | Access model & record sharing | 07 Security | 12 | permission-set-led model 🆕⚠️, PSG muting, restriction ⚠️ + scoping rules |
| 11 | ⬜ | Identity, encryption & monitoring | 07 Security | 9 | MFA ⚠️, SSO, enhanced domains ⚠️, Shield, Event Monitoring, secure-coding checklist ⚠️ |
| 12 | ⬜ | APIs: REST → legacy streaming | 06 Integration | 12 | API retirement treadmill 🆕⚠️, composite, Bulk 2.0 ⚠️, GraphQL 🆕, **Pub/Sub replaces CometD** 🆕⚠️ |
| 13 | ⬜ | Auth, external apps & agent-facing integration | 06 Integration | 11 | OAuth ⚠️, **External Client Apps** 🆕⚠️, named credentials ⚠️, Event Relay 🆕, MCP servers 🆕 |
| 14 | ⬜ | Data modeling & LDV performance | 08 Data | 10 | relationships, external IDs, selectivity, Query Plan, skew, skinny tables |
| 15 | ⬜ | Retention, federation & data operations | 08 Data | 10 | big objects, archiving 🆕, zero-copy Data 360 🆕, backup ⚠️, Hyperforce 🆕 |
| 16 | ⬜ | Source-driven dev & 2GP packaging | 09 DevOps | 11 | **`sf` v2 replaces `sfdx`** 🆕⚠️, scratch orgs, unlocked 2GP 🆕⚠️, DevOps Center 🆕⚠️ |
| 17 | ⬜ | CI/CD, code quality & release ops | 09 DevOps | 11 | GitHub Actions, Code Analyzer v5 🆕⚠️, ApexGuru 🆕, Agentforce DX 🆕 |
| 18 | ⬜ | LWR sites: architecture → auth | 05 Experience | 10 | **LWR default, Aura legacy** 🆕⚠️, SSR/CDN, guest hardening ⚠️, licences, SSO |
| 19 | ⬜ | Site content, headless, performance & agents | 05 Experience | 8 | Enhanced CMS 🆕, headless 🆕, SEO 🆕, ExperienceBundle ⚠️, embedded agents 🆕 |

**192 topic files.** Exact file lists live in each area's `PHASES.md`. *(Phase 07 added two beyond plan — see [03-lwc/PHASES.md](03-lwc-and-slds/PHASES.md).)*

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
# no file over the cap
Get-ChildItem SF -Recurse -Filter *.md | ForEach-Object {
  $n = (Get-Content $_.FullName | Measure-Object -Line).Lines
  if ($n -gt 85) { "$($_.Name): $n lines" }
}
```

Then grep the phase output for `WITH SECURITY_ENFORCED`, `sfdx force:`, `if:true`, `Locker`, `CometD` — each may appear **only** inside a ⚠️ correction, never as current guidance.
