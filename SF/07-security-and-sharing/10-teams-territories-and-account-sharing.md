# Teams, Territories & Account Sharing

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** The record-sharing mechanisms that are configured on the record rather than in Setup — account and opportunity teams — and the second hierarchy that Enterprise Territory Management adds. Ordinary rules are [09](09-sharing-rules-and-manual-sharing.md).

## Core idea

Sharing rules answer *which population sees which records* and they answer it centrally. Some businesses cannot express access that way, because the answer is per-deal: this opportunity has a solution engineer, that one does not. **Teams** push the grant onto the record itself, where the owner maintains it. **Enterprise Territory Management** goes the other way and adds a *whole second hierarchy* alongside roles, so an account can be shared by territory membership rather than by ownership. Both are legitimate; both are also the two mechanisms most likely to make an access model unexplainable, because they scatter grants across thousands of records and across a hierarchy that most people forget exists.

## How it works

- **Account and opportunity teams are per-record member lists** with a role and an access level per member. Enabling them adds `AccountTeamMember` / `OpportunityTeamMember` and the corresponding share rows.
- **Team-derived shares have their own `RowCause`** (`Team`), so they survive independently of manual shares and are rebuilt from the team membership, not from a rule. → [09](09-sharing-rules-and-manual-sharing.md)
- **Account team membership does not automatically extend to child records.** Access to the account's opportunities and cases depends on those objects' OWDs and on account team *default* access settings, which are configured separately per object.
- **A default account team** attached to a user is copied onto records they own — a template, not a live link. Changing the default does not retrofit existing accounts.
- **Enterprise Territory Management (ETM)** models territories in a hierarchy, assigns accounts to territories by rule or manually, and assigns users to territories. Access flows up the *territory* hierarchy exactly as it flows up the role hierarchy.
- **ETM's `Territory2` model has a state** — territory model versions are activated, and only one model is active at a time, which makes territory redesign a versioned deployment rather than an edit.
- **Both hierarchies apply simultaneously.** A user can reach a record by role, by territory, or by both, and the effective access is the most permissive path.

> **From my notes.** The "assistant agent" scenario in my 2025 prep is the cleanest statement of where teams stop. *A field names a helper on the opportunity; changing it must revoke the old helper and grant the new one.* No sharing rule expresses that — criteria-based rules cannot key off a user lookup this way — and a share group is the wrong family entirely. The answer is **an opportunity team plus Apex that maintains the membership**, which is the general shape worth remembering: **teams give you the grant structure, code gives you the trigger for changing it.** → [02-apex · 11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)

## 2026 currency

No change to teams or ETM in Summer '26. The change that reaches them is elsewhere and is worth noting because it compounds: **restriction rules subtract from the union** ([11](11-restriction-rules.md)), and a restriction rule on an object that is also shared by team and by territory produces an answer no single mechanism explains. Where an org runs teams, ETM and restriction rules together, **`15` stops being a convenience and becomes the only reliable way to answer an access question** → [15](15-auditing-and-troubleshooting-access.md).

## Gotchas

- **Teams scatter grants across records**, so there is no central place to read them. Auditing means querying `AccountTeamMember` and `OpportunityTeamMember`, not reading Setup.
- **A default team is a template applied at record creation.** Editing it later changes nothing that already exists.
- **Account team access does not imply opportunity access.** The child object's own default access setting decides, and it defaults to none.
- **Territory hierarchy is a second upward-inheritance path** that most access reviews forget, and it can silently grant what the role hierarchy was carefully designed to withhold.
- **Only one territory model is active.** Building the new one is safe; activating it re-derives every account assignment and every share in one operation.
- **Removing a team member removes their share immediately**, including on records where they were the only reason anyone downstream had access.
- **Teams and ETM both multiply share rows.** On a large account object this is where sharing recalculation time actually goes. → [16](INDEX.md) *(phase 11)*

## Recall

Q: How do teams differ from sharing rules as a grant mechanism?
A: Teams are configured per record by the owner; sharing rules are configured centrally in Setup for a whole population.

Q: Does adding a user to an account team give them access to that account's opportunities?
A: Only if the account team's default access for Opportunity is set to grant it. It is a separate, per-object setting.

Q: What is a default account team?
A: A template copied onto records when they are created. Changing it does not update existing records.

Q: How many territory models can be active at once?
A: One. Others exist as versions, and activating a different model re-derives every assignment and share.

Q: If a user can reach a record by both role and territory, which wins?
A: The most permissive path. Both hierarchies apply at the same time and access is the union.

## Related

- [09 · Sharing rules & manual sharing](09-sharing-rules-and-manual-sharing.md) — the central mechanism these two supplement
- [07 · Role hierarchy & ownership](07-role-hierarchy-and-ownership.md) — the first hierarchy, which ETM runs alongside
- [11 · Restriction rules](11-restriction-rules.md) — the subtraction that makes multi-mechanism models unreadable without tooling
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — how to answer an access question when four mechanisms are in play
