# Lab 04 — Identity Resolution Across Three Sources

> Status: ⬜ not started · Date run: —

## Goal

Unify the home org's contacts, the external org's contacts and the API-pushed records into one profile set — and design the test data so that the ruleset can visibly *fail*. Most people run this lab, see the profile count drop and call it success. That's the trap.

## Prereqs

- Labs [01](lab-01-home-org-crm-connector.md), [02](lab-02-external-org-connection.md), [03](lab-03-ingestion-api-any-org.md) done, all mapped to the same Individual DMO.
- Baseline credit number from [lab-00](lab-00-tenant-baseline.md). **Check it before and after this lab** — identity resolution is billed on records *reviewed*, and it's the heaviest consumer in the tenant.

> **Keep the dataset in the hundreds.** This is the lab that can drain a free tenant.

## Design the test set first

Before touching the ruleset, hand-build these cases and record the expected outcome for each:

| Case | Example | Should it match? |
|---|---|---|
| Exact email, both orgs | `anna@x.com` in home + external | ✅ yes |
| Same person, email changed | `anna@x.com` / `anna@y.com`, same name + phone | 🤔 depends on your rules — decide *before* you run |
| Near-miss name | `Jon Smith` / `John Smyth`, different emails | ❌ no |
| **Household** | two different people, same surname, same address | ❌ **no — and this is the one that will trip** |
| Same email, different people | shared family/company mailbox | ❌ no, but exact-email matching will merge them |

You now have a test oracle. Without it you're not testing, you're admiring.

## Steps

1. **Ruleset v1: exact email only.** Run it. Record the resulting unified profile count and check each case against your table.
2. **Ruleset v2: add fuzzy name + address.** Re-run. Record the new count. **The delta is the money** — that's the line in a client conversation about match quality.
3. **Reconciliation rules.** Set different strategies per attribute (most recent vs. source priority) and verify *which value won* on a profile where the sources disagree. Craft that disagreement deliberately.
4. **Check every case in your table** against the actual unified profiles, not against the count.

## How you know it worked

Not "the count went down". You know it worked when **every row in your table matches the outcome you predicted** — including the ones that should *not* have merged.

## Break it on purpose

**Over-match deliberately.** Fuzzy name + address across your household pair. Open the merged profile and look at two real people wearing one identity.

This is worth doing once because of what it teaches about incentives: over-matching produces *fewer* profiles, which looks cleaner in the UI and is **cheaper** under profile-based pricing (~$240/1,000 unified profiles). The direction the platform rewards is the direction that causes a privacy incident. Never tune matching on cost alone — see [identity resolution](../../04-identity-resolution/notes.md).

## Credits spent

Before: — · After: — · Delta: —

## Notes from my run

—
