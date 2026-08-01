# Agentforce in Setup & AI-assisted admin

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** The AI surface inside Setup and the discipline for using it. What Agentforce *is*, how agents are built and grounded, lives in [AI_Data/02-salesforce-ai](../../AI_Data/02-salesforce-ai/INDEX.md) — this note stays on the admin's side of the line.

## Core idea

**Setup with Agentforce is GA**: an agent that works inside Setup, taking a described intent ("give the support team read access to this object") and doing the configuration. Setup Home is now a command center with a prompt bar rather than a landing page. Two design decisions make it safe enough to use for real work: it **acts only on your approval**, and it **operates strictly within your own permissions** — it cannot become a privilege escalation path. The third is what makes it auditable: every change it makes lands in the **Setup Audit Trail** like any admin's.

## How it works

- **Where:** the prompt bar in Setup Home, and in the flow of work on Setup pages.
- **What it covers today** — the common admin surface, not all of Setup:
  - users and **troubleshooting user access**
  - permission sets, permission set groups, org-wide defaults, sharing rules
  - custom objects and fields — including suggesting an **existing** object or field that already fits
  - flows, Lightning pages, custom report types
  - formulas: create, modify and **explain**
  - answers from Salesforce Help, and navigation to the right Setup page
- **Cost:** Setup actions are **non-billable and consume no Agentforce Flex credits.** Experimenting here does not draw down the org's balance.
- **Permissions, in two layers:**

| To | Needs |
|---|---|
| Enable it | **Customize Application** + **Data Cloud User** |
| Use it | **Use Setup with Agentforce** + **Execute Prompt Template**, plus access to the **Data 360 default data space** |

- **Elsewhere in the platform:** **Ask Agentforce (Beta)** in Flow debug details returns a root-cause analysis of a failed interview — the same assistive pattern applied to debugging rather than configuration.
- **The review loop that makes it work:** describe intent → read the proposed change → approve → verify in [Setup Audit Trail](17-setup-audit-trail-monitoring-and-usage.md) → capture it in source control.

## 2026 currency

This surface moves fast and the note reflects what is GA now: Setup with Agentforce itself, with capability breadth explicitly described as growing. Two things to unlearn: it is no longer a pilot or beta, and Setup usage is not metered. Track changes in [AI_Data/05-release-radar/agentforce-platform.md](../../AI_Data/05-release-radar/agentforce-platform.md) rather than re-deriving them here; anything in this note that contradicts the radar loses.

## Gotchas

- **It inherits your permissions, which is the point and the risk.** A System Administrator's agent can do anything a System Administrator can — including deleting a field. Least privilege applies to the human, and therefore to the agent.
- **Approval is not review.** Reading "created 3 permission sets" and clicking approve is not the same as checking what is in them. The audit trail is the backstop, not the review.
- **Org-made changes are not in git.** Prompt-driven config in a sandbox still has to be retrieved and committed, or the next deployment overwrites it. → [09-devops](../09-devops-sfdx-and-release-management/INDEX.md)
- The **Data 360 default data space** requirement surprises people: an org without Data 360 set up cannot use it, even with the permissions granted.
- Non-billable applies to **Setup** actions. The same org's runtime agents still consume Flex credits — do not generalise the pricing.
- Coverage is "common tasks first", so a request outside it fails vaguely rather than explicitly; treat a confusing answer as out-of-scope and do it by hand.
- Never let it configure straight in production because it is fast. The speed argument is exactly why the sandbox-first rule matters more, not less.
- Formula *explanation* is the highest-value, lowest-risk use — it reads existing config rather than changing it, and it is the best way to build trust in the tool.

## Recall

Q: What is the status of Setup with Agentforce, and does it consume credits?
A: GA, and no — Setup actions are non-billable and do not draw Agentforce Flex credits.

Q: What permissions does a user need to *use* it?
A: *Use Setup with Agentforce* and *Execute Prompt Template*, plus access to the Data 360 default data space. Enabling it needs Customize Application and Data Cloud User.

Q: Can the Setup agent do something the admin driving it cannot?
A: No. It acts only within the running user's permissions, and only after that user approves the action.

Q: Where do you verify what the agent actually changed?
A: The Setup Audit Trail, which records its changes like any other admin change.

Q: Name three things it can configure today.
A: Any three of: users and access troubleshooting, permission sets and sharing rules, custom objects and fields, flows, Lightning pages, custom report types, formulas.

## Related

- [17 · Setup Audit Trail, monitoring & usage](17-setup-audit-trail-monitoring-and-usage.md) — the control that makes agent-made config reviewable
- [18 · Salesforce Foundations & org strategy](18-salesforce-foundations-and-org-strategy.md) — how Agentforce arrives in an ordinary Enterprise org
- [AI_Data/02-salesforce-ai · INDEX](../../AI_Data/02-salesforce-ai/INDEX.md) — the agent platform itself: topics, actions, grounding, Trust Layer
