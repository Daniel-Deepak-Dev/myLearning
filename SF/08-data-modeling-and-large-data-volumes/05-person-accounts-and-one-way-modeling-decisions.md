# Person Accounts & One-Way Modeling Decisions

> Area: 08-data-modeling-and-large-data-volumes · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 14

**Scope:** The B2C account model, and the wider class of platform switches that cannot be undone. The B2B graph it modifies is [04](04-standard-crm-object-map.md).

## Core idea

Salesforce's core model assumes a business buys from you: an Account is a company and a Contact is a person inside it. **Person Accounts** collapse that for B2C by storing one individual as an Account and a Contact **simultaneously** — one record to the user, two rows underneath, joined for life.

The reason this note exists is not the feature, it is the **switch**. Enabling Person Accounts cannot be undone. There is no disable button, no Support case, no migration path back; the org has a different data model from that moment on. That makes it the clearest member of a small family of decisions where the cost of being wrong is a new org, and it deserves to be treated as an architecture review item rather than a Setup task.

## How it works

- **One record, two rows.** A person account consumes storage on **both Account and Contact** — budget roughly double per individual → [06](06-storage-model-and-schema-limits.md).
- **`IsPersonAccount`** marks them; **`PersonContactId`** points at the shadow Contact; Contact fields surfaced on the account carry a **`__pc`** suffix instead of `__c`.
- **Prerequisites before the switch:** Account needs **at least one record type**, and the sharing model must have **Contact OWD = `Controlled by Parent`**, or Account and Contact both **Private**. Salesforce creates the person account record type for you.
- **A Lead with no Company converts to a Person Account**, which is how most orgs acquire them by accident during a pilot.
- **Sharing follows the Account.** The shadow Contact has no independent sharing, exactly as under `Controlled by Parent` → [07-security · 06](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md).

**The wider family of one-way doors:**

| Switch | Why it does not come back |
|---|---|
| **Person Accounts** | no disable path, at all |
| **Multiple Currencies** | reversal needs Support and is conditional in practice → [22](INDEX.md) *(phase 15)* |
| **State & Country picklists** | the conversion rewrites stored data |
| **Big object index** | fixed at deployment; changing it means a new big object → [14](14-big-objects-and-the-archive-tier.md) |
| **Field data type change** | can null existing values with no undo |
| **Master-detail direction** | conversion has preconditions a populated org rarely meets → [02](02-relationships-deep-dive.md) |

## Gotchas

- **Reporting splits down the middle.** Account-side children (Orders, Cases) and Contact-side children (Campaign Members, Emails) cannot be joined in a single standard report, because a report type traverses one path.
- **Packages and integrations assume business accounts.** Anything writing `Account.Name` or expecting a separate Contact insert needs testing — a person account's Name is derived from the person fields and is not directly writable.
- **The storage surprise arrives at migration time.** An org sized for 5M individuals needs storage for 10M rows.
- **`__pc` fields are invisible to code that walks `__c` conventions**, including a fair amount of home-grown metadata tooling.
- **You cannot pilot this in production.** A sandbox proves the feature works; it cannot prove you want it forever, because the sandbox is disposable and production is not.
- **Enabling it changes the sharing model first.** If the org runs Contact OWD as Public Read/Write today, tightening it is its own project with its own recalculation cost → [07-security · 16](../07-security-and-sharing/16-sharing-recalculation-and-performance.md).

## Recall

Q: How much storage does one person account consume?
A: Two records' worth — one Account row and one Contact row — so roughly double a business-account contact.

Q: What are the prerequisites for enabling Person Accounts?
A: At least one Account record type, and a sharing model where Contact OWD is `Controlled by Parent` or Account and Contact are both Private.

Q: How do most orgs acquire person accounts unintentionally?
A: Lead conversion — a Lead with no Company value converts into a Person Account.

Q: What suffix do Contact fields carry when surfaced on a person account?
A: `__pc`, not `__c`.

Q: Why can a report not show a person account's Orders and Campaign Memberships together?
A: They hang off opposite halves of the record — Account side and Contact side — and a report type traverses only one path.

## Related

- [04 · Standard CRM object map](04-standard-crm-object-map.md) — the B2B model this reshapes
- [06 · Storage model & schema limits](06-storage-model-and-schema-limits.md) — why doubling the row count matters
- [02 · Relationships deep dive](02-relationships-deep-dive.md) — the other conversions with preconditions
- [07-security · 06 Org-wide defaults & record access](../07-security-and-sharing/06-org-wide-defaults-and-record-access.md) — the sharing prerequisite, in context
