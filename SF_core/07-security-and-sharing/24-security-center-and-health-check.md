# Security Center & Health Check

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 11

**Scope:** Posture — measuring how an org is configured against a standard, and watching it drift. Owns **Who Sees What Explorer as a product**; its five lenses as an access tool are already [15](15-auditing-and-troubleshooting-access.md).

> **What changed.** *"Posture tooling is a paid add-on, so a single-org customer has nothing but Health Check"* stopped being true in **July 2026**, when **Security Center Essentials** became available in every org at no cost. The full Security Center remains a paid add-on, and **Who Sees What Explorer still sits behind it** — so the correction is real but narrower than the headlines suggest.

## Core idea

Every other note in this area describes a control. This one describes the **measurement** of those controls: whether they are set the way you think, and whether they still are. That second half is the harder problem — orgs do not fail an audit because nobody knew the right setting, they fail because someone changed it eleven months ago in a sandbox that got deployed. Health Check answers *how is this org configured right now, against a standard*. Security Center answers *how are all my orgs configured, and what moved*. Neither grants or denies anything; both are read-only, which is exactly why they get skipped and exactly why they matter.

## How it works

| Tier | Cost | What it gives you |
|---|---|---|
| **Health Check** | free, every org | one page scoring the org's security settings against a baseline, with in-place fixes |
| **Security Center Essentials** | **free, every org (Jul 2026)** | configuration metrics — Health Check score and baselines, connected apps, managed and unmanaged packages, trusted IP ranges, login IP ranges |
| **Security Center** | paid add-on, priced as a share of net spend | multi-org view, metric history and drift over time, the full metric set |
| **Security Center Extension Package** | managed package, for Security Center customers | **Who Sees What Explorer** and its five lenses |

- **Health Check groups settings as High-Risk, Medium-Risk, Low-Risk and Informational** and scores against the **Salesforce Baseline Standard** by default. You can upload **up to five custom baselines** — your own standard, or a regulator's — and score against those instead.
- **A custom baseline is the feature that makes the score meaningful.** Against the stock baseline the number is a comparison to Salesforce's opinion; against yours it is a comparison to your commitment.
- **Security Center's real product is history.** A point-in-time metric is available free; *this setting changed on 14 May and here is who* is what the licence buys.
- **Who Sees What Explorer needs the paid licence and the extension package.** Check entitlement before designing an access-review process around it — the free surfaces in [15](15-auditing-and-troubleshooting-access.md) are the fallback, and they are good.
- **It reads the same settings as the rest of this area** — session timeout ([18](18-session-security-login-policies-and-step-up.md)), Trusted URL wildcards ([20](20-my-domain-enhanced-domains-and-trusted-urls.md)), password policies, sharing settings — so a poor score is a pointer to another note, never a finding in itself.

## 2026 currency

Two changes, both about making posture unavoidable. **Security Center Essentials** landed in July 2026 across all orgs, which removes the "we were never licensed for it" answer to a baseline question. And **weekly Health Check notifications are now on by default for new production orgs**, turning a page nobody visited into an email somebody receives — a small change that alters behaviour more than most features do. Both belong to the same 2026 hardening wave as the MFA and step-up enforcement in [17](17-authentication-and-mfa.md) and [18](18-session-security-login-policies-and-step-up.md); the dated list is in [../CURRENCY.md](../CURRENCY.md).

## Gotchas

- **The score is a proxy, not a goal.** Health Check weights settings by its own model, not by your threat model — an org at 90% with a wide guest profile is worse off than one at 70% without.
- **Essentials is metrics, not management.** It shows connected apps, packages and IP ranges; it does not give you the drift history or the multi-org rollup that the paid tier exists for.
- **"We have Security Center" does not mean you have Who Sees What Explorer** — the extension package is a separate install.
- **A new org's weekly email goes to whoever is listed**, which after a few years is often someone who has left. Check the recipient, not just the setting.
- **Health Check cannot see anything outside Setup settings.** Sharing model design, code that runs in system mode and over-broad permission sets are all invisible to it. → [14](14-code-execution-context-and-security.md)
- **Fixing from the Health Check page changes production immediately.** The one-click *Fix Risks* control is convenient and is a change with no approval step attached.
- **Baselines are per org, not per pipeline.** Sandboxes drift from production by design, so compare like with like or the signal is noise. → [09-devops · INDEX](../09-devops-sfdx-and-release-management/INDEX.md)

## Recall

Q: What became free in July 2026, and what did not?
A: Security Center Essentials — configuration metrics in every org. The full Security Center, its drift history and Who Sees What Explorer remain paid.

Q: How many custom Health Check baselines can an org upload, and why bother?
A: Up to five. The stock score measures you against Salesforce's opinion; a custom baseline measures you against your own commitment.

Q: What does the paid Security Center buy that Essentials does not?
A: Multi-org rollup and metric history — drift over time, rather than a point-in-time reading.

Q: Where does Who Sees What Explorer actually live?
A: In the Security Center Extension Package, a managed package available to Security Center customers — not in Essentials.

Q: Why is a high Health Check score not a security conclusion?
A: It scores only Setup settings, against Salesforce's weighting. Sharing design, guest access and system-mode code are outside its view entirely.

## Related

- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — the free access-answering surfaces, and the five lenses as a tool
- [18 · Session security, login policies & step-up](18-session-security-login-policies-and-step-up.md) — the settings a low score most often points at
- [26 · Secure coding checklist](26-secure-coding-checklist.md) — the half of posture no Setup page can measure
- [01-admin · 17 Setup Audit Trail, monitoring & usage](../01-admin-and-declarative-platform/17-setup-audit-trail-monitoring-and-usage.md) — the durable record of who changed a setting
