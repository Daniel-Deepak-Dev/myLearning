# Record Types & Picklist Architecture (UI only restriction)

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 01
Human UI: Record Types strictly enforce which picklist values a user can select.

Agent API: The API bypasses these UI restrictions.

Agent Context: Agents use Record Types simply as a blueprint to guide which picklist values are appropriate for a specific process, as the system will not block them from inserting mismatched values.

**Scope:** Record types as a process-differentiation mechanism, and the picklist machinery they filter — global value sets, dependent picklists, restricted picklists.

## Core idea

A record type lets one object serve several business processes without splitting the schema. It does three jobs: it subsets which picklist values are available, it selects which page layout a user sees, and it links to a business process (sales stages, case statuses, lead statuses). Because layout assignment is *per profile per record type*, record types are also the point where the configuration matrix starts multiplying — two record types across ten profiles is twenty assignments to keep coherent. Picklists are the thing record types most often filter, so the two topics are one subject in practice.

## How it works

- **Record type is metadata**, not data: a `RecordTypeId` on the record points at it. Reference it by `DeveloperName`, never by hardcoded ID — IDs differ across every org.
- **Master record type** is the implicit default that exists before you create any. Records created by the API without an explicit `RecordTypeId` land on the user's default.
- **Availability vs default** are separate settings on the profile or permission set: a record type can be available to a user without being their default.
- **Global value sets** define picklist values once and share them across many fields — the only way to avoid drift between "Country" on five objects. Local value sets are per-field.
- **Restricted picklists** reject any value not in the set, including from the API and Data Loader. Unrestricted picklists silently accept anything.
- **Dependent picklists** filter a dependent field's values by a controlling field. The controlling field must be a picklist of **300 values or fewer**, or a checkbox. Multi-select picklists cannot control.
- **Business processes** must exist before a record type can be created on `Opportunity`, `Case`, `Lead` and `Solution` — the record type form asks for one.

## 2026 currency

The layout half of a record type's job is being displaced. Field visibility and section arrangement now belong to **Dynamic Forms**, and button/action visibility to **Dynamic Actions** — both driven by visibility rules rather than by layout-per-record-type assignment. Record types remain the right tool for picklist subsetting and process differentiation. See [05 · Dynamic Forms](INDEX.md) and [06 · Dynamic Actions](INDEX.md), phase 02.

## For AI and headless users

An agent never renders a layout, so that half of a record type is dead weight to it. The picklist half is worth *more* than it is to a human: a model asked to set a field sees the union of every value across every process unless something narrows it, and it will pick a plausible wrong one. The record type is that narrowing — a machine-readable enum per process.

- **Read the scoped set, never hardcode it.** UI API returns exactly the values legal for one record type, plus the `validFor` bitmaps encoding the dependent-picklist rules:
  - `GET /services/data/v67.0/ui-api/object-info/Case/picklist-values/{recordTypeId}/Reason`
  - `GET /services/data/v67.0/ui-api/record-defaults/create/Case?recordTypeId={id}` — defaults *and* scoped picklists in one call; the usual agent-side "what may I write?" probe.
- **Record type filtering is a UI rule, not a DML rule.** A plain REST/SOAP insert can set a value the record type does not offer and the platform accepts it. `Restricted` validates against the *field's* value set, never the record-type subset. Headless, a record type is guidance — not a guardrail.
- **Enforcement is added deliberately:** a validation rule pairing `RecordType.DeveloperName` with the value, an invocable Apex/Flow the agent calls instead of doing raw DML, or writing through UI API, which does honour record-type constraints.
- **The agent is a real user.** Agentforce runs its actions as an assigned agent user, so record type availability and defaults come from that user's permission sets. Granting an agent only the record types it should touch is real blast-radius control and makes intent auditable.
- **Record type as a routing key.** Agentforce actions and prompt templates branch on `RecordTypeId` exactly as UI automation does — one "log a case" action resolves the record type and serves several processes, instead of shipping one action per process.
- **Server-side automation is unaffected.** Validation rules, assignment rules, criteria-based sharing and record-triggered flows all read `RecordTypeId` regardless of write path, so an agent-created record still lands in the right process.

### Example — `Case` with `Billing` and `Technical`

`Reason` holds the union of both processes: `Invoice_Dispute`, `Refund`, `Hardware_Failure`, `Installation`. An agent handed the raw field describe sees all four and may file a `Refund` on a `Technical` case — and the API will write it.

Ground the model on the scoped list, passing only those values into the tool schema:

```
GET /services/data/v67.0/ui-api/object-info/Case/picklist-values/012.../Reason
→ { "values": [ { "value": "Hardware_Failure" }, { "value": "Installation" } ] }
```

Then enforce it, because the read above is only advisory:

```
AND(
  RecordType.DeveloperName = "Technical",
  OR(ISPICKVAL(Reason, "Invoice_Dispute"), ISPICKVAL(Reason, "Refund"))
)
```

## Gotchas

- Hardcoded record type IDs are the classic deployment failure: they are org-specific, so they break on every promotion. Query by `DeveloperName`.
- **Deactivating** a picklist value leaves existing records holding it; **deleting** it forces a replace-or-blank decision. Reports and filters treat the two very differently.
- Deleting a record type requires reassigning every record that uses it — on a large object that is a data job, not a config click.
- Validation rules do not know about record types unless you say so; a rule written for one process fires on all of them until it checks `RecordTypeId`.
- A restricted picklist will fail an integration or data load that was working fine against the unrestricted version.
- Dependent picklist rules are stored on the *dependent* field, so exporting the controlling field alone loses the dependency.
- The controlling field's 300-value ceiling is on the **controlling** side only — the dependent field can be larger.
- Record type availability is granted by profile *or* permission set; auditing only profiles gives an incomplete answer. See [07-security](../07-security-and-sharing/INDEX.md).
- The record-type picklist subset is not enforced on DML — the inverse of the restricted-picklist trap above. An agent or integration writing raw REST/SOAP can set an out-of-process value and succeed silently.
- Deriving an agent's allowed values from `getPicklistValues()` in Apex returns the whole field value set, not the record-type subset. Record-type-aware reads come from UI API.

## Recall

Q: What three jobs does a record type do?
A: Subsets available picklist values, selects the page layout per profile, and links the record to a business process.

Q: Why should Apex and Flow never hardcode a record type ID?
A: Record type IDs are org-specific, so hardcoded values break on deployment to any other org. Reference `DeveloperName` instead.

Q: What is the value limit on a controlling picklist in a dependency?
A: 300 values or fewer; a checkbox may also control. Multi-select picklists cannot control.

Q: What is the difference between deactivating and deleting a picklist value?
A: Deactivating leaves the value on existing records but removes it from new selections; deleting forces you to replace or blank it.

Q: Does a restricted picklist enforce against the API?
A: Yes — restricted picklists reject out-of-set values from every write path including Data Loader, which is why they break tolerant integrations.

Q: Does a record type stop an agent from writing an out-of-process picklist value?
A: No. The subset is a UI-side filter; REST/SOAP DML accepts it. Enforce with a record-type-aware validation rule, an invocable service, or by writing through UI API.

Q: How does a headless client fetch only the values valid for one record type?
A: UI API — `ui-api/object-info/{object}/picklist-values/{recordTypeId}/{field}`, or `ui-api/record-defaults/create/{object}?recordTypeId=` for defaults and scoped picklists together. Both include `validFor` for dependencies.

Q: Why still bother with record types when AI users never see a layout?
A: The layout job is dead weight to them, but the value-set subsetting becomes the enum that keeps a model from choosing across processes — plus routing for Agentforce actions and availability control on the agent user.

## Related

- [03 · Objects, fields & relationships](03-objects-fields-and-relationships.md) — the schema record types sit on
- [08 · Validation rules & duplicate management](08-validation-rules-and-duplicate-management.md) — where record-type-aware enforcement is written
- [07-security · INDEX](../07-security-and-sharing/INDEX.md) — how record type availability is granted
- [19 · Agentforce in Setup & AI-assisted admin](19-agentforce-in-setup-and-ai-assisted-admin.md) — the agent user whose permission sets grant record types
- [06-integration · 25 · MCP servers & agent-facing APIs](../06-integration-and-apis/25-mcp-servers-and-agent-facing-apis.md) — UI API as the record-type-aware read path
- [04-flow · 23 · Flows as Agentforce actions](../04-flow-and-automation/23-flows-as-agentforce-actions.md) — the invocable write path that can enforce the subset
