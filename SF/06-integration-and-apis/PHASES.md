# Phases for 06 · Integration & APIs

26 topics across 2 runs. Master plan: [../PHASES.md](../PHASES.md) · standing rules there apply to every phase.

> **Runs after security (phases 10–11).** OAuth, named credentials and API access control all rest on the access model.
> Currency anchor for this area: [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md).

> **The area grew from 23 to 25 at phase-12 plan time, and was renumbered in learning order.** Two topics were inserted — **03** (endpoints and hostnames) and **09** (Metadata/Tooling/Connect) — pushing the old 03–07 to 04–08, the old 08–12 to 10–14, and the whole phase-13 block from 13–23 to **15–25**. **The renumber was nearly free and will never be this cheap again:** not one file in the area existed, and the grep found **13 inbound lines** in the vault naming an area-06 topic by number — every one of them a link whose *href* was `INDEX.md`, so nothing broke, only the visible number went stale. All 13 were fixed in the same commit. **Phase 13 must append only. Do not renumber 01–14 now that they exist**, and repeat that grep before touching numbering again.

---

## Phase 12 — APIs: REST → legacy streaming · 14 files ✅

```
01-integration-patterns-and-selection.md
02-api-versions-and-the-retirement-treadmill.md    🆕⚠️
03-api-endpoints-hostnames-and-edge-network.md     🆕⚠️  ← ADDED at plan time
04-rest-api-fundamentals.md                              (was 03)
05-soap-api-and-where-it-persists.md                     (was 04)
06-composite-batch-and-graph-apis.md                     (was 05)
07-bulk-api-2.md                                   ⚠️    (was 06)
08-ui-api-and-metadata-aware-clients.md                  (was 07)
09-metadata-tooling-and-connect-apis.md            🆕    ← ADDED at plan time
10-graphql-api.md                                  🆕    (was 08)
11-pub-sub-api.md                                  🆕⚠️  (was 09)
12-platform-event-design.md                              (was 10)
13-change-data-capture.md                                (was 11)
14-legacy-streaming-and-outbound-messaging.md      ⚠️    (was 12)
```

**Two files added before the run.** Each closed a hole another note had already promised someone would fill:

- **03** — three orphans, one topic. [07-security · 26](../07-security-and-sharing/26-secure-coding-checklist.md) lists hardcoded `na139`-style hostnames as review finding 16 and points here to explain them; [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md) says *"CSP trusted sites belong to 06-integration"*; and `Salesforce Edge Network` (2023) was the **only seed page in the area with no target topic**.
- **09** — nothing in 23 topics owned the APIs that move *configuration* rather than records. **01's "which API for which job" table could not name the API you deploy with**, phases 16–17 assume the vocabulary, and it is the honest answer to **05**'s "where does SOAP persist": here.

### Retro

**⚠️ — the plan's headline correction was itself wrong, for the third phase running — and this time the wrong sentence was already published**

- **11/14 — Pub/Sub API did not replace CometD.** This plan called *"Pub/Sub API (gRPC) replaced CometD"* **the single biggest change in the area**. Salesforce's Streaming API Developer Guide says something materially weaker: *"we **recommend** you use Pub/Sub API instead of Streaming API."* **No end-of-life is published for Streaming API, CometD or Bayeux.** Only **PushTopic events** and **generic events** carry the docs' *(Legacy)* label. The checkable disproof was inside the vault the whole time: **`lightning/empApi` is supported, current, and CometD-based** — a note asserting CometD's retirement cannot explain why that module exists. This is the **eighth instance of "old ≠ dead" in this build**, after Lightning Locker, `if:true`, `System.assertEquals`, page layouts, classic approvals, Workflow Rules/Process Builder and the cancelled profile-permissions retirement — and the second where the error was live in an area INDEX rather than only in a plan. Phase 11's rule (*re-verify the correction itself*) is what caught it, at plan time rather than at write time.
- **02 — one wave complete, no next wave announced.** Versions **21.0–30.0** were retired in **Summer '25** and now return **HTTP 410 GONE**; the floor is **31.0**. Projections that 31.0–39.0 follow in a named release circulate widely and **none is an announcement**. The adjacent dated item is easy to conflate and is a different thing: **SOAP `login()` retiring for API 31.0–64.0 in Summer '27** withdraws *one call* across a version range, not those versions. *(This line said **Spring '27** until phase 13 checked the Help article; see the phase-13 retro.)*

**🆕 the plan did not flag — one of them is weeks away, not a roadmap item**

- **03 — the instanced-URL withdrawal has a real date and it is now.** Winter '27 reaches **sandboxes from August 2026 and production from September 2026**, and shortly after an org takes it, API traffic on instanced hostnames is no longer supported. The opt-in *Block API traffic that uses an incorrect instanced URL* switch opened **19 June 2026**; a documented known issue made **SOAP login URLs called through Visualforce return 400 Bad Request**, fixed **16–18 June 2026**, so testing is only meaningful after that. Phase 11 recorded the Winter '27 date as a domain fact; nobody had converted it into an integration deadline.
- **09 — Connect REST API's limits loosened at 67.0.** Orgs moved **off** the per-user/per-app/per-hour throttle onto the org's **per-24-hour Platform API limit**; only Chatter-requiring requests keep an hourly cap, and **the same applies to Connect in Apex**. A relief, not a restriction — designs built around the old hourly ceiling can be simplified.
- **06 — the composite limits are worth stating as numbers.** 25 subrequests for batch and composite, **500 nodes per graph** (v50.0+), 200 records for sObject Tree. Composite's `allOrNone` is **opt-in**; Composite Graph's atomicity is **implicit and per graph**, so one request can carry several graphs that succeed or fail independently.
- **10 — 67.0 mutation chaining is a *larger* referencing model than composite's.** `@{ref.Record.FieldName.value}` references **any field** from an earlier operation; composite's `referenceId` only ever exposed the ID. And it landed in the **API**, not the wire adapter, which still has no mutations.

**Other corrections made while writing**

- **Bulk 2.0's PK chunking difference is sharper than "behaves differently".** `Sforce-Enable-PKChunking` is a **Bulk v1 header**. In 2.0 you set neither batch sizes nor that header — copying v1 advice into a 2.0 client does nothing at all.
- **SOAP gained capability in the same release as a retirement announcement.** 67.0 accepts **JWT access tokens in the `sessionId` header**. An API receiving new authentication support is being narrowed, not withdrawn — the cleanest available evidence against "SOAP is dead".
- **`/tooling/query` is the answer to a recurring question.** `SELECT Body FROM ApexClass` fails on the normal query endpoint and succeeds on the Tooling one, and the error says nothing useful.

**Seed harvest** · *six pages routed, five substantive*

- **01** — `SF - Integration Patterns and Practices` (**2026-02**). → *read first as instructed, and it earned the billing: the pattern taxonomy matches what was written. **One stale line** — it names outbound messaging as a first-choice fire-and-forget mechanism. Corrected inline against **14**.*
- **07** — `Bulk API`. → *v1-era throughout, as predicted: batch splitting, the 10,000-record batch ceiling and `Sforce-Enable-PKChunking`. All three are v1 mechanics and are corrected inline. Its durable lesson survives — **lock contention, not row count, makes a large load slow**.*
- **14** — `CometD` (**2025**). → *harvested. The long-polling mechanics are still correct; what it lacks is the framing this note exists to supply. It became the ⚠️ hook, though **in the opposite direction to the one the plan expected**.*
- **13** — `Change data capture` + `lightning/empApi - Change Data Capture` (2023). → *both still structurally correct — channel names, header shape, subscribe/unsubscribe pattern. Nothing to correct, one thing to add: `empApi` is the way to subscribe **inside a component**, not the way an external system should.*
- **05** — `SOAP API` (2019). → *structure only, as the inventory predicted. The enterprise/partner split and header model hold; its worked example authenticates with `login()` and it presents SOAP as the default for new work. Both noted rather than reproduced.*
- **03** — `Salesforce Edge Network` (2023). → ***previously unrouted***; *now has a home. Treats Edge purely as a latency switch, which is still true and now incomplete — hostname choice became a supportability question, not a performance one.*
- **12** — `Platform Event / Salesforce Events`. → *thin. Treats an event as fire-and-forget notification; the omission worth naming is that **an event is a published contract**. Harvested as one line.*
- **04** — `IN`, flagged *"unclear — inspect"*. → **inspected: it is SOQL, not REST.** *It belongs with the area-02 `IN`/semi-join cluster already covered in phase 03. Removed from this area's mapping.*

**Rule 1 exceeded deliberately, with approval** — two files added, and the correction sweep reached [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [../README.md](../README.md), [AI_Data/GLOSSARY.md](../../AI_Data/GLOSSARY.md), [../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md) and 13 stale numeric references across areas 02, 05, 07 and 08. **Fifth phase running to make the same call**, and the second where a published sentence was wrong rather than merely a planned one.

---

## Phase 13 — Auth, external apps & agent-facing integration · 12 files ✅

```
15-oauth-flows-and-authorization.md                      ⚠️
16-external-client-apps.md                               🆕⚠️
17-named-credentials-and-external-credentials.md         ⚠️
18-apex-rest-and-custom-endpoints.md
19-external-services-openapi-and-the-api-catalog.md            ← scope widened at plan time
20-salesforce-connect-and-external-objects.md
21-mulesoft-and-api-led-boundaries.md
22-event-relay-and-cloud-eventing.md                     🆕
23-idempotency-retries-and-error-handling.md
24-api-limits-monitoring-and-access-control.md
25-mcp-servers-and-agent-facing-apis.md                  🆕
26-certificates-mutual-tls-and-the-pki-changes.md        🆕⚠️  ← ADDED at plan time
```

**One file added, appended not inserted.** Phase 12's warning held: 01–14 existed and 15–25 were named by number from areas 02 and 07, so **26** went on the end and nothing moved. The renumber grep was repeated and confirmed no inbound reference shifted.

### Retro

**⚠️ — the planned corrections survived verification for the first time in four phases. A *date* did not.**

- **The failure mode changed.** Phases 10, 11 and 12 each had a headline ⚠️ that was itself stale, always the same way: something described as retired that was not. Phase 13's three ⚠️ items all verified as written. What broke instead was arithmetic on a date — **SOAP `login()` retires in Summer '27, not Spring '27** — and it was live in **seven lines across five files**, two of them published notes ([05](05-soap-api-and-where-it-persists.md), [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md)). Help article **005132110** is unambiguous. `AI_Data/05-release-radar/` had it right the whole time, and [../CURRENCY.md](../CURRENCY.md) contradicted itself — line 37 said Summer '27 while its own table said Spring '27. **A date is a citable fact and gets cited; verify it against the Help article, not against another note in the vault.**
- **17 was right to flag deprecation and would have been wrong to add a date.** Legacy named credentials are *"deprecated and will be discontinued in a future release"* with **no published date**. That is the ninth "old ≠ dead" in this build and the first the plan got right unprompted.

**🆕 the plan did not flag**

- **16 — a second connected-app enforcement, live since September 2025.** The **Connected App Usage Restrictions Change** blocks **uninstalled** connected apps for *new* users, blocks **OAuth 2.0 device flow outright even for prior users**, and adds an **`Approve Uninstalled Connected Apps`** permission as the bypass. Inventory tool: Setup → **Connected Apps OAuth Usage**. The plan and [../CURRENCY.md](../CURRENCY.md) both knew only about the *creation* gate.
- **19 — the API Catalog turned this note into the spine of the phase.** Deploying an Apex REST class adds its **OpenAPI document to the API Catalog** and makes its methods available as **agent actions**, with extension fields controlling the exposure. That makes `18 → 19 → 25` one pipeline instead of three adjacent topics, and it is why 19 was retitled at plan time.
- **25 — hosted MCP has no machine-to-machine flow.** Authorization code only. Also new and unrecorded: the **`mcp_api`** scope (deliberately narrower than `api`), servers **inactive by default**, a **30-minute** propagation delay on a new external client app, and `API_CLIENT_CATEGORY = SALESFORCE_HOSTED_MCP` for auditing → [24](24-api-limits-monitoring-and-access-control.md).
- **20 — Salesforce Connect's per-hour ceilings were removed on Hyperforce.** New-row and OData-callout limits are gone for the 2.0/4.0/4.01 adapters in EE/PE/UE/DE. That ceiling was the standard reason to replicate instead of federate, so pre-2026 assessments are worth reopening. Summer '26 also gave the **cross-org adapter** named credential support.
- **15 — "blocked by default" needed a carve-out.** Three events, routinely merged: org-wide block switch (Winter '22), blocked by default in **new orgs only** (Summer '23), retirement for connected apps (Winter '27). Also new: the **`Any API Auth`** permission gating SOAP `login()`.

**The added file — 26, certificates & the PKI changes**

The only genuinely homeless topic in the area, and dated: **dual-use public-CA roots are banned**, so mTLS built on them fails at reissue; **validity drops 200 days (15 Mar 2026) → 100 (15 Mar 2027) → 47 (15 Mar 2029)**; and Salesforce says **stop certificate pinning**. Nothing in the vault owned certificates — [07-security · 19](../07-security-and-sharing/19-sso-saml-oidc-and-identity.md) mentions SAML signing-cert expiry and stops. Placed in area 06 rather than 07 because the casualty is an integration, not a login.

**Seed harvest** · *two pages routed, both as predicted*

- **18** — `Apex REST Callouts` + `Apex Rest Web Services` (2021). → *structure only, exactly as the inventory predicted — annotations and a worked example, no prose. Two things they predate: the **user-mode default at 67.0** inverts their implicit system-mode assumption, and a published endpoint is now a candidate agent action. Harvested as one callout.*

**Rule 1 exceeded deliberately, with approval** — one file added, and the `login()` date sweep reached [../CURRENCY.md](../CURRENCY.md), [../PHASES.md](../PHASES.md), [../README.md](../README.md), [07-security · 17](../07-security-and-sharing/17-authentication-and-mfa.md), [07-security · 26](../07-security-and-sharing/26-secure-coding-checklist.md), [AI_Data/GLOSSARY.md](../../AI_Data/GLOSSARY.md) and [../_notion-seed/INVENTORY.md](../_notion-seed/INVENTORY.md). **Sixth phase running to make the same call** — and the third where a published sentence was wrong rather than merely a planned one.
