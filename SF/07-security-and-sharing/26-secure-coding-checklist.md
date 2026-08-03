# Secure Coding Checklist

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** The area's capstone — a review checklist, not an essay. Every line names the exact thing to search for. Mechanics live in [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md)–[11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md), [03-lwc · 09](../03-lwc-and-slds/09-lightning-web-security.md) and [14](14-code-execution-context-and-security.md); this is what you run against a diff.

> **What changed.** The 2019-era checklist — *"call `isAccessible()` before every query, `isUpdateable()` before every write, and wrap SOQL in `WITH SECURITY_ENFORCED`"* — is superseded. At **API 67.0 Apex defaults to user mode and `with sharing`**, so those checks are no longer the guard; `WITH SECURITY_ENFORCED` **no longer compiles**. The review question inverted: you are not looking for missing checks any more, you are looking for **deliberate opt-outs**. Likewise XSS advice written for **Lightning Locker** describes a different product from **LWS**.

## Core idea

A secure-by-default platform does not remove the review, it moves it. When enforcement was opt-in, the defect was omission and the reviewer's job was to find the missing call. Now enforcement is the default, so the defect is **escalation** — a `SYSTEM_MODE`, a `without sharing`, an old API version on a class — and each one is a question rather than an automatic finding, because plenty of them are legitimate. The checklist below is ordered the way a review actually runs: what the code can reach, what it does with input, what it exposes, and what it leaves behind.

## How it works

| # | Check | Search the diff for | Why it matters |
|---|---|---|---|
| 1 | escalated data access | `AccessLevel.SYSTEM_MODE`, `USER_MODE` absent on `Database.query…` | the modern bypass, and it is invisible at compile time |
| 2 | sharing bypass | `without sharing`, `inherited sharing` | legitimate in a service class, a defect in a controller |
| 3 | stale API version | `<apiVersion>` below `67.0` in `*.cls-meta.xml` | an old class still runs in system mode under unchanged code |
| 4 | retired syntax | `WITH SECURITY_ENFORCED` | does not compile — its presence dates the whole file |
| 5 | SOQL injection | `Database.query(` with `+` or string interpolation | use `queryWithBinds` and a bind map |
| 6 | SOSL / dynamic input | `String.escapeSingleQuotes` missing around user input | the only sanitiser for a query fragment you must concatenate |
| 7 | exposed endpoints | `@AuraEnabled`, `@RestResource`, `@InvocableMethod` | each is callable by anyone who can reach it; the component is not the boundary |
| 8 | agent-callable surface | `@InvocableMethod` with broad scope | an agent action inherits its running user and composes far faster than a person |
| 9 | trigger-body logic | security decisions inside `trigger` | triggers are always system mode and cannot declare otherwise |
| 10 | Flow run context | record-, schedule- or event-triggered flows | they still bypass object, field **and** sharing, with no setting |
| 11 | guest exposure | site guest profile, `@AuraEnabled` reachable from a public page | guest users cannot own records and read-only sharing is the only grant |
| 12 | XSS sinks | `innerHTML`, `lwc:dom="manual"`, `unescape`, `{!$…}` in VF | LWS sanitises much and is **not** a firewall |
| 13 | external hosts | new script or `fetch` targets | a CDN block is **CSP / Trusted URLs**, not LWS |
| 14 | secrets | hardcoded keys, tokens, endpoints, `String` constants that look like credentials | named credentials or protected custom metadata, never a class constant |
| 15 | legacy auth | `login()`, `grant_type=password`, new Connected Apps | password-only session minting; being retired for that reason |
| 16 | hardcoded URLs | `.my.salesforce.com` literals, instance hostnames like `na139` | legacy redirections ended, instanced URLs unsupported in Winter '27 |

## 2026 currency

Three lines above are new this year and worth stating as rules rather than checks. **The OAuth username-password flow and SOAP `login()` are on retirement paths** (Winter '27 and Spring '27), so any remaining use is an authentication finding — see [17](17-authentication-and-mfa.md). **New Connected Apps cannot be created** without a Salesforce Support exception; External Client Apps are the model, which makes "add a connected app" an outdated instruction in any runbook → [06-integration · 14](../06-integration-and-apis/INDEX.md). And **anonymous Apex execution from managed packages is being blocked** from Summer '27, which retires a small category of installed-package behaviour. Sourcing for all three: [../CURRENCY.md](../CURRENCY.md).

## Gotchas

- **An escalation is a question, not a verdict.** `without sharing` on a deliberately org-wide service is correct; the defect is the one nobody can explain.
- **Bumping a class's API version changes its data access with no code change** — the riskiest one-line diff in a Salesforce repo. → [14](14-code-execution-context-and-security.md)
- **Test coverage proves nothing about security.** Tests run as an admin unless you use `System.runAs`, and after the async sharing update even that lags. → [16](16-sharing-recalculation-and-performance.md)
- **A `catch` that returns the raw exception message leaks schema and row data** to the client. Log the detail, return a generic message.
- **`Schema.describe` calls are for deciding what to render**, not for guarding a write — the platform guards the write now.
- **Code Analyzer catches some of this and not the interesting parts.** Escalation intent, guest reachability and agent scope are human review. → [09-devops · 14](../09-devops-sfdx-and-release-management/INDEX.md)
- **The same logic is more permissive built in Flow than in Apex at 67.0.** "Clicks are safer than code" is backwards, and a Flow diff deserves this checklist too. → [04-flow · 19](../04-flow-and-automation/19-flow-run-context-and-sharing.md)

## Recall

Q: How did the review question change at API 67.0?
A: From "where is the missing permission check" to "where is the deliberate opt-out" — user mode and `with sharing` are now the defaults.

Q: What does finding `WITH SECURITY_ENFORCED` in a file tell you?
A: That the file predates its retirement and no longer compiles at 67.0 — treat the whole file as unreviewed since then.

Q: Which construct still cannot declare an access mode at all?
A: A trigger body. It is always system mode, which is why security-sensitive logic belongs in the handler class.

Q: A component cannot load a script from an external CDN. Which control, and which note?
A: Trusted URLs / CSP — not LWS. See [20](20-my-domain-enhanced-domains-and-trusted-urls.md).

Q: Name the one-line diff that silently changes a class's data access.
A: Raising `<apiVersion>` in the `.cls-meta.xml` to 67.0 — the code is untouched, the enforcement is not.

## Related

- [14 · Code execution context & security](14-code-execution-context-and-security.md) — the context map this checklist operationalises
- [02-apex · 10 Apex security: user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the keywords and their exact semantics
- [03-lwc · 09 Lightning Web Security](../03-lwc-and-slds/09-lightning-web-security.md) — what LWS actually blocks, and the three things wrongly blamed on it
- [24 · Security Center & Health Check](24-security-center-and-health-check.md) — the configuration half of posture, which no code review reaches
