# Code Execution Context & Security

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** Which contexts enforce the access model of [01](01-security-model-layers-overview.md)–[13](13-field-level-security-and-visibility-layers.md) and which bypass it. The Apex keywords themselves are [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)–[11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md); this note is the map of contexts.

> **What changed.** *"Automation runs as an administrator, so the access model is a UI concern"* is wrong in both directions at 67.0. **Apex now defaults to user mode and `with sharing`** — it enforces the model unless told not to. **Flow's triggered types did not move** and still run in system context without sharing. The safe-by-default assumption has swapped sides: the same logic is now more permissive built in Flow than built in Apex.

## Core idea

Everything in this area describes what a *user* may do. Almost nothing on the platform runs as a plain user in a browser. Code, flows, guest sessions, integration users and agents each execute in a context that decides whether the model is consulted at all, and those contexts do not agree with each other. The one question worth asking of any component is therefore not *what can this user see* but **whose access is being enforced here, and is it being enforced at all**. Ownership of the answer is split deliberately: the Apex mechanics live in area 02, and this note owns the comparison across contexts — because the mistakes happen at the boundaries, where a screen flow calls an Apex class that queries on behalf of a guest.

## How it works

| Context | Object & field permissions | Sharing | Changeable? |
|---|---|---|---|
| **Apex, class compiled at 67.0** | enforced (user mode) | enforced (`with sharing`) | yes — `AccessLevel.SYSTEM_MODE`, `without sharing` |
| **Apex, class on an older API version** | bypassed | inherits the caller | yes |
| **Apex trigger body** | bypassed — always system mode | bypassed | **no** |
| **Record/schedule/event-triggered flow** | bypassed | bypassed | **no** |
| **Screen & autolaunched flow** | bypassed | depends on *How to Run the Flow* | yes |
| **Guest user session** | enforced, on a hardened profile | guest sharing rules only, read-only | no |
| **Integration / API user** | enforced as that user | enforced as that user | via its permission sets |

- **"System Context With Sharing" in Flow means sharing only.** Object permissions and FLS are still bypassed — it is not Apex's `with sharing` and not user mode. → [04-flow · 19](../04-flow-and-automation/19-flow-run-context-and-sharing.md)
- **The API version that decides Apex behaviour is the one on the class containing the query**, not the caller's. A 67.0 service calling a 55.0 selector gets system-mode SOQL from the selector.
- **User mode enforces restriction rules too**, so a 67.0 class returns the filtered set where an older one returned everything. → [11](11-restriction-rules.md)
- **An agent action is ordinary Apex or Flow under an agent's running user.** The context rules above apply unchanged — the agent adds no boundary of its own. → [02-apex · 22](../02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md)
- **An integration user's permission sets are the entire control surface** for anything arriving over the API, and they are the thing least often reviewed.

> **From my notes, and now wrong.** My 2025 prep asks how to fix an Apex class that updates fields a user has read-only via FLS. Its three plausible answers were `WITH SECURITY_ENFORCED`, `with sharing`, and checking `isUpdateable()` per field — and it marks **`isUpdateable()`** correct. At 67.0 that is superseded and one of the distractors no longer even compiles. **`WITH SECURITY_ENFORCED` was retired**; **`with sharing` was never the answer**, because it governs records rather than fields; and a class compiled at **67.0 enforces FLS by default**, so the bug in the question cannot occur unless someone opted out. Describe checks are now for deciding what to *render*, not for guarding the write. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)

## 2026 currency

The 67.0 flip is documented in [../CURRENCY.md](../CURRENCY.md) and sourced in [AI_Data/05-release-radar/trust-security-and-governance.md](../../AI_Data/05-release-radar/trust-security-and-governance.md). Its stated reasoning is what makes this note a security-area concern rather than an Apex one: the platform stopped assuming the surface in front of it had already filtered the data, because that caller may now be an **autonomous agent**. An Agentforce agent inherits the access of the user it runs as and can reach anything that user can, but it composes and aggregates far faster than a person browsing — so the access model, not the prompt, is the control that has to hold. The Trust Layer's own guardrails are described in [AI_Data/](../../AI_Data/05-release-radar/trust-security-and-governance.md); do not restate them here.

## Gotchas

- **Flow did not follow Apex.** A record-triggered flow at 67.0 has exactly the reach it had in 2019, and no setting changes it. → [04-flow · 19](../04-flow-and-automation/19-flow-run-context-and-sharing.md)
- **Bumping an old class's API version changes its data-access semantics** without changing a line of its code. That is the real migration risk, and it arrives long after upgrade day.
- **Triggers can no longer declare an access mode at all.** Security-sensitive logic belongs in the handler. → [02-apex · 06](../02-apex-and-triggers/06-triggers-and-the-handler-framework.md)
- **A Get Records in system context returns rows the user will never be shown**, and putting them on a screen leaks them through the DOM.
- **Every `@AuraEnabled` method is an endpoint** for anyone who can load the component. Its own checks are the boundary; the component is not. → [03-lwc · 08](../03-lwc-and-slds/08-apex-in-lwc-wire-vs-imperative.md)
- **Guest users cannot own records and cannot be granted edit by a sharing rule.** Any recipe that does either predates 2021. → [04-flow · 21](../04-flow-and-automation/21-flow-for-external-and-guest-users.md)
- **An unexplained `AccessLevel.SYSTEM_MODE` is where a permission bypass hides.** It is a question in review, not automatically a defect.

## Recall

Q: Which is more permissive at 67.0 for the same logic — Apex or Flow?
A: Flow. Apex defaults to user mode and `with sharing`; Flow's triggered types still run in system context without sharing and cannot be changed.

Q: What does Flow's "System Context With Sharing" actually enforce?
A: Record-level sharing only. Object permissions and field-level security are still bypassed.

Q: Which class's API version decides whether a query runs in user mode?
A: The one containing the query, not the caller's.

Q: Does an Agentforce agent have its own access boundary?
A: No. It runs as a user and inherits that user's access exactly — the access model is the control surface.

Q: What is the migration risk created by the 67.0 defaults being version-gated?
A: Nothing breaks on upgrade day, but bumping an old class's API version silently changes its data access under unchanged code.

## Related

- [02-apex · 10 Apex security: user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the keywords and mechanics this note maps
- [04-flow · 19 Flow run context & sharing](../04-flow-and-automation/19-flow-run-context-and-sharing.md) — the Flow half in full, including why the default is not a context
- [11 · Restriction rules](11-restriction-rules.md) — the subtraction user-mode code inherits and system-mode code does not
- [AI_Data · trust, security & governance](../../AI_Data/05-release-radar/trust-security-and-governance.md) — the sourced record of the 67.0 flip and the agentic reasoning behind it
