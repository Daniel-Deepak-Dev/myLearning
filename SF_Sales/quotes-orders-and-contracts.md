---
vault: SF_Sales
format: light
level: working
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Quotes, Orders & Contracts

**One line:** The standard post-opportunity records. A quote proposes prices and can sync lines with its opportunity; a contract is the agreement; an order is what the customer bought, locked once activated.

**Reach for it when:** a quote won't sync, an order won't activate or accept products, or someone asks whether an order needs a contract.

## Key points

- **Enable Quotes:** Setup → **Quote Settings** → *Enable Quotes*, then pick the opportunity layouts that get the Quotes related list. *Create Quotes Without a Related Opportunity* is a separate, optional checkbox.
- **A quote normally belongs to an opportunity** and has its own `QuoteLineItem` rows. Its `CurrencyIsoCode` is copied from the opportunity and can't be changed.
- **One synced quote per opportunity.** `Opportunity.SyncedQuoteId` points at it and `Quote.IsSyncing` flags it. Use **Start Sync** / **Stop Sync** on the quote, or set or null `SyncedQuoteId` through the API.
- **Sync is two-way on line items.** Add or remove a line on either record and the other follows; sort order syncs too. Syncing a second quote replaces the opportunity's lines with that quote's lines. Stop Sync only breaks the link.
- **Quote PDFs:** build and activate a template under Setup → **Quote Templates**. The rep clicks **Create PDF**, picks a template and **Save to Quote**. Each save is a `QuoteDocument` named quote name plus a version (`AcmeQuote_V1`), and **Email PDF** sends it.
- **Orders:** Setup → **Order Settings** → *Enable Orders*. `Order.AccountId` and `Order.Pricebook2Id` are required, `ContractId` is optional. Every `OrderItem` must come from the order's price book, and that price book can never be changed or removed.
- **Whether an order needs a contract** is a page-layout choice. Untick *Required* on the Order layout's Contract Number field to create orders straight from an account. With a contract, the order's start date must fall inside the contract's dates.
- **Contracts:** `StatusCode` is Draft, InApproval or Activated, and `Status` ships with Draft, In Approval Process and Activated only. Nothing sets Expired automatically. **Contract Settings** holds *Auto-calculate Contract End Date* (`StartDate` + `ContractTerm`) and *Send Contract Expiration Notice Emails to Account and Contract Owners*.
- **Activation through the API:** create the record in a Draft status. Then activate it with an update that sets `Status` to an Activated value and changes nothing else. An activated contract can't be deleted or moved back. An activated order can return to Draft only if it has no reduction order products.

## Gotchas

- **An order won't activate** without the *Activate Orders* permission, at least one order product, and — if it has a contract — an active contract.
- **Activated orders are locked.** You can edit their order products but not add or remove any. Deactivating needs *Edit Activated Orders*, and any reduction orders must be deactivated and deleted first.
- **Reduction orders can't be created in Lightning Experience** — only in Classic. They need *Enable Reduction Orders* plus *Create Reduction Orders*, and one reduction order reduces one order.
- **Inactive things block sync.** An inactive or archived product, price book or list price, or an inactive currency, stops Start Sync: *"This quote can't be synced because it has inactive or archived products."*
- **You can't disable Quotes** while any quote is synced, or while formulas, triggers, workflow or approvals reference quote objects. Disabling Orders hides order data; it isn't deleted.
- **Quote PDFs drop what the user can't see.** Fields hidden by field-level security vanish silently, related-list text is cut to under 256 characters, and right-to-left languages render left-aligned. Advanced Currency Management isn't supported with quotes.
- **Expiration notices need an activated contract** and the standard `EndDate`. `OwnerExpirationNotice` (15–120 days) sets the lead time, and a daily job sends them around midnight.
- **CPQ is out of scope.** Salesforce CPQ and Revenue Cloud extend these objects. CPQ is end of sale and Revenue Cloud Advanced is its successor — see the backlog.

## Gaps to close

- [ ] Do custom fields on `QuoteLineItem` and `OpportunityLineItem` sync in standard quote sync, or does that take Apex or Flow?
- [ ] Which quote `Status` values allow **Email Quote**, and where is that controlled?
- [ ] On an activated order, which `OrderItem` fields can still change — `Quantity`, `UnitPrice`, dates — and what does *Enable Negative Quantity* allow on top?

## Confirm in org

- 🚩 Does the Order layout's Contract Number field ship as Required in a Summer '26 Developer Edition org? — Object Manager → Order → Page Layouts.

## Hands-on

- [ ] **SLS-QUOTE-01** · 20 min · Create two quotes on one opportunity with different lines. Sync the first, add a product on the opportunity, then sync the second. **Proves:** the new product lands on quote 1, and syncing quote 2 replaces the opportunity's lines — watch `SyncedQuoteId`. **Needs:** Quotes enabled.
- [ ] **SLS-QUOTE-02** · 15 min · Deactivate a product used on an unsynced quote, then click **Start Sync**. **Proves:** sync is refused for inactive products — copy the exact message. **Needs:** SLS-QUOTE-01 data.
- [ ] **SLS-QUOTE-03** · 25 min · Create a Draft contract and an order on it with one product, and activate the order. Then activate the contract, activate the order, and add a second product. **Proves:** an inactive contract blocks activation, and an activated order refuses new products — copy both errors. **Needs:** Orders enabled.
- [ ] **SLS-QUOTE-04** · 20 min · Enable Reduction Orders and look for **Reduce Order** on the activated order in Lightning. Switch to Classic, reduce one unit, then try to deactivate the original. **Proves:** reduction orders are Classic-only to create, and a live one blocks deactivation. **Needs:** SLS-QUOTE-03 order.

## Related

- [Products & Price Books](products-and-price-books.md) — the price book entries every quote line and order product must come from
- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the opportunity a quote syncs to, and whose Amount its lines drive
- [SF_core · 08-data-modeling · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) — the post-sale row: `Quote`, `Order` and `Contract`, each with its own line-item child

## Sources

- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `Quote` (`IsSyncing`, `Status` values, currency *"copied from the related Opportunity and can't be changed"*); `QuoteDocument`; `Opportunity.SyncedQuoteId` (*"Read only in an Apex trigger"*, set or null to start or stop sync); `Order` (`AccountId` and `Pricebook2Id` required, create as Draft, *"the Status field is the only field you can update when activating"*, back to Draft only without reduction order products); `OrderItem` (must match the order's price book); `Contract` (`StatusCode` values, `EndDate` from `ContractTerm`, `OwnerExpirationNotice` 15–120 days, activated contracts can't change status or be deleted)
- [How Quote Syncing Works](https://help.salesforce.com/s/articleView?id=sf.quotes_synch_overview.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"it can sync with only one quote at a time"*; line items and sorting sync both ways; replacing the synced quote replaces opportunity lines
- [Sync Quotes and Opportunities](https://help.salesforce.com/s/articleView?id=sales.quotes_synch.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Start Sync, Stop Sync; the old quote stops syncing when a new one starts
- [Troubleshooting Quote Syncing](https://help.salesforce.com/s/articleView?id=sales.quotes_sync_troubleshooting.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · the inactive product, price book, list price and currency errors
- [Set Up Quotes](https://help.salesforce.com/apex/HTViewHelpDoc?id=quotes_enable.htm) — Salesforce Help · read 2026-09-24 · Quote Settings; *Create Quotes Without a Related Opportunity*; can't disable while synced or referenced
- [Create and Email Quote PDFs](https://help.salesforce.com/s/articleView?id=sales.quotes_create_pdf.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Create PDF, Save to Quote, `AcmeQuote_V1`, Email PDF
- [Considerations for Creating Quote Templates](https://help.salesforce.com/s/articleView?id=sales.quotes_template_considerations.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · FLS-hidden fields don't appear; *"Advanced Currency Management isn't supported with quotes"*; PDFs in Quote PDFs and Notes & Attachments
- [Considerations for Creating Quote PDFs](https://help.salesforce.com/s/articleView?id=sales.quotes_considerations_for_creating_pdfs.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · right-to-left languages; related-list text *"truncated to fewer than 256 characters"*
- [Generate Quotes and Sync Them Easily](https://trailhead.salesforce.com/content/learn/projects/manage-products-prices-quotes-orders/create-multiple-quotes) — Trailhead · read 2026-09-24 · the Start Sync flow and the Save to Quote step
- [Enable Orders](https://help.salesforce.com/s/articleView?id=customize_order_enable.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Order Settings; *"If you disable orders, your order-related data is hidden"*
- [Guidelines for Creating Orders](https://help.salesforce.com/s/articleView?id=sales.order_create.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · start date inside the contract dates; contract optional by admin setting
- [Create a Salesforce Order without a Contract](https://help.salesforce.com/s/articleView?id=000387771&language=en_US&type=1) — Salesforce Help KB 000387771 · read 2026-09-24 · deselect *Required* on the Contract Number field of the Order layout
- [Considerations for Activation Limitations](https://help.salesforce.com/s/articleView?id=sales.order_activate.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"You can activate orders for active contracts but not for inactive contracts"*; needs order products; *"You can't add or remove them"*; Activate Orders and Edit Activated Orders
- [Editing and Deletion Limitations for Orders and Reduction Orders](https://help.salesforce.com/s/articleView?id=sf.order_edit.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · price book can't be changed or removed; deleting a contract deletes its orders
- [Reduction Orders](https://help.salesforce.com/s/articleView?id=sf.orderreduction_overview.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"If you're using Lightning Experience, you can't create reduction orders"*; one reduction order per order
- [Enable Reduction Orders](https://help.salesforce.com/s/articleView?id=sales.customize_order_enable_ro.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · the setting and the *Create Reduction Orders* permission
- [Set Up Contracts](https://help.salesforce.com/s/articleView?id=sales.customize_contract.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Contract Settings checkboxes
- [Did Not Receive Notice for Salesforce Contract Expiration](https://help.salesforce.com/s/articleView?id=000385179&language=en_US&type=1) — Salesforce Help KB 000385179 · read 2026-09-24 · activated contracts only; standard End Date; daily job around midnight
- [Set Contract Status to 'Expired' or 'Discontinued' once End Date passes](https://help.salesforce.com/s/articleView?id=000380733&language=en_US&type=1) — Salesforce Help KB 000380733 · read 2026-09-24 · *"By default, Contract has only three statuses"*
- [Salesforce CPQ Not End of Life: What End of Sales Means](https://www.salesforce.com/sales/cpq/end-of-life/) — Salesforce, page dated 10 July 2026 · read 2026-09-24 · *"no longer selling new Salesforce CPQ licenses to new customers"*; Revenue Cloud Advanced is *"the successor to Salesforce CPQ"*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
