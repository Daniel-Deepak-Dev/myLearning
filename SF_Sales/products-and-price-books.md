---
vault: SF_Sales
format: light
level: basic
status: open
gaps: 3
org_checks: 1
labs: 4
created: 2026-09-24
updated: 2026-09-24
currency: "Summer '26 (API 67.0)"
---
# Products & Price Books

**One line:** How a product gets a price. `Product2` is the item, `PricebookEntry` is its price in one price book and one currency, and `OpportunityLineItem` is that price sold on a deal.

**Reach for it when:** a product won't add to an opportunity, a price change didn't reach existing deals, or an Apex test fails on a missing standard price.

## Key points

- **Four objects.** `Product2` is the item; `Product2.Family` (label **Product Family**) is a picklist for grouping. `Pricebook2` is a list. `PricebookEntry` joins the two with a `UnitPrice` (label **List Price**). `OpportunityLineItem` (label *Opportunity Product*) points at the entry through `PricebookEntryId`.
- **One standard price book per org**, flagged `Pricebook2.IsStandard = true`. Its name is read-only, and the API can update it but not create or delete it. Every other price book is custom.
- **Standard price first.** A product needs an entry in the standard price book, in that currency, before it can get one in a custom price book. Skip it and you get *"No standard price defined for this product."*
- **`UseStandardPrice = true`** makes a custom entry copy the standard entry's `UnitPrice`, which then becomes read-only. Entries in the standard price book must have it set to `true`.
- **List Price vs Sales Price.** List Price (`OpportunityLineItem.ListPrice`) is copied from the entry. Sales Price (`UnitPrice`) is what the rep sold for; editing it needs **Edit Opportunity Product Sales Price**. Prices are copied, not linked: a later price book change never moves an existing deal's Amount.
- **One price book per opportunity** (`Opportunity.Pricebook2Id`), and every line item must come from it. Once lines exist, `Amount` is read-only and is the sum of their `TotalPrice`.
- **Multi-currency: one entry per currency.** A product has one price per currency in a price book, so each currency is its own `PricebookEntry`. Line items always take the opportunity's `CurrencyIsoCode`.
- **Product schedules:** Setup → **Product Schedules** → *Enable quantity scheduling*, *Enable revenue scheduling*, or both. Each product then opts in with `CanUseQuantitySchedule` / `CanUseRevenueSchedule`. A default schedule is Divide or Repeat, Daily to Yearly, 1–150 installments, and becomes `OpportunityLineItemSchedule` rows.
- **In Apex tests**, data-silo tests (API 24.0+) can't see org data, so get the ID from `Test.getStandardPricebookId()` and insert a standard entry before any custom one. `@IsTest(IsParallel=true)` tests can't call it.

## Gotchas

- **You can't swap the price book under existing lines.** The API rejects a `Pricebook2Id` or `CurrencyIsoCode` update on an opportunity with line items. Delete the lines first, then re-add from the new book.
- **Silent ignores, not errors.** An `Amount` update on an opportunity with products is ignored. So is `Quantity` on a line with any schedule, and `TotalPrice` on a line with a revenue schedule.
- **Deleted line items skip the Recycle Bin.** A directly deleted `OpportunityLineItem` can't be undeleted.
- **A product on an opportunity can't be deleted through the API.** The UI offers to archive it instead. Deactivate products and price books (`IsActive = false`) to keep history.
- **Schedule edits don't reach existing deals.** Changing a product's default schedule leaves opportunities that already carry it unchanged.
- **`ListPrice`, `Name` and `ProductCode` are empty in a before-insert trigger** on `OpportunityLineItem` in Lightning. Read them after insert.
- **Price book access isn't Apex sharing.** SOQL on `Pricebook2` ignores `with sharing` and returns every price book. In the UI, the Price Book org-wide default (`View Only` vs `Use`) decides who can add from a book.

## Gaps to close

- [ ] In Lightning, what does the opportunity's **Choose Price Book** action do when products already exist — warn and delete them, or refuse?
- [ ] What does the setting that auto-enters List Price as Sales Price change, and where does it sit in Setup?
- [ ] What do the Price Book sharing levels (`No Access`, `View Only`, `Use`) do to an API insert of `OpportunityLineItem`, not just the Add Products picker?

## Confirm in org

- 🚩 In a data-silo test, does `[SELECT Id FROM Pricebook2 WHERE IsStandard = true]` return a row, or only `Test.getStandardPricebookId()`? — run both in one test class.

## Hands-on

- [ ] **SLS-PROD-01** · 15 min · Create a product, skip the standard price, then add it to a custom price book in the UI and with `sf data create record`. **Proves:** *No standard price defined for this product* — the standard entry is a hard prerequisite. **Needs:** nothing.
- [ ] **SLS-PROD-02** · 20 min · Add two products to an opportunity, then change its `Pricebook2Id` with `sf data update record`. **Proves:** the API refuses a price book change while lines exist — copy the error. **Needs:** a second active custom price book.
- [ ] **SLS-PROD-03** · 20 min · Enable quantity scheduling, give a product a default schedule (Divide, Monthly, 3), add it to a deal, then update the line's `Quantity` through the API. **Proves:** the call succeeds but the value doesn't change — ignored, not rejected. **Needs:** nothing.
- [ ] **SLS-PROD-04** · 15 min · Write an Apex test that inserts a custom `PricebookEntry` without a standard one, then with one via `Test.getStandardPricebookId()`, then mark the class `IsParallel=true`. **Proves:** the standard entry is required in tests too, and parallel tests can't call the method. **Needs:** nothing.

## Related

- [Opportunities, Sales Process & Path](opportunities-sales-process-and-path.md) — the opportunity whose Amount the line items take over
- [Quotes, Orders & Contracts](quotes-orders-and-contracts.md) — where the same price book entries become quote lines and order products
- [SF_core · 08-data-modeling · 04 Standard CRM object map](../SF_core/08-data-modeling-and-large-data-volumes/04-standard-crm-object-map.md) — the four-hop pricing chain, and why "the product won't add" is nearly always a missing or inactive entry
- [SF_core · 08-data-modeling · 22 Multi-currency, multi-language & locale](../SF_core/08-data-modeling-and-large-data-volumes/22-multi-currency-multi-language-and-locale.md) — `CurrencyIsoCode`, the corporate currency and dated rates behind one entry per currency

## Sources

- [Object Reference for the Salesforce Platform (PDF, v68.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/object_reference.pdf) — Salesforce Developers · read 2026-09-24 · `Pricebook2`: *"Every org has one standard price book"*, name read-only, *"can only update the standard price book"*, define a standard price per currency first; `PricebookEntry`: `UseStandardPrice`, `UnitPrice` label List Price, *"You must load the standard price for a product before you're permitted to load its custom prices"*; `Product2`: `Family`, `CanUseQuantitySchedule`, installments 1–150, *"one price for a given currency within the same price book"*, API delete fails when an opportunity uses it; `OpportunityLineItem`: *Effects on Opportunities* (Amount read-only, Pricebook2Id and CurrencyIsoCode updates rejected, no Recycle Bin, ListPrice empty before insert); `OpportunityLineItemSchedule`
- [Error "No Standard Price Defined for This Product"](https://help.salesforce.com/s/articleView?id=000385004&language=en_US&type=1) — Salesforce Help KB 000385004 · read 2026-09-24 · the error string and fix
- [Change the Pricebook on your Opportunities](https://help.salesforce.com/s/articleView?id=000387649&language=en_US&type=1) — Salesforce Help KB 000387649 · read 2026-09-24 · *"you must delete all products from those Opportunities first"*
- [Difference Between Sales Price and List Price](https://help.salesforce.com/s/articleView?id=000382583&language=en_US&type=1) — Salesforce Help KB 000382583 · read 2026-09-24 · *Edit Opportunity Product Sales Price*
- [Impact to Opportunities and Orders when Price is updated on a Product](https://help.salesforce.com/s/articleView?id=000383411&language=en_US&type=1) — Salesforce Help KB 000383411 · read 2026-09-24 · *"will not affect the Amount on an Opportunity, or an Order"*
- [Product, Price Book, Price Book Entry, and Product Schedule Fields](https://help.salesforce.com/s/articleView?id=sales.products_fields.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · Use Standard Price, Is Standard Price Book, Product Family
- [Enable Product Schedules in Salesforce Classic](https://help.salesforce.com/s/articleView?id=sales.enabling_schedules.htm&language=en_US&type=5) — Salesforce Help · via search 2026-09-24 · Setup → Product Schedules, the two enable checkboxes
- [Considerations for Using Product Schedules](https://help.salesforce.com/s/articleView?id=sales.products_considerations_for_using_schedules.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · *"opportunities with that product aren't updated"*
- [Considerations for Removing Products and Price Books](https://help.salesforce.com/s/articleView?id=sf.products_del.htm&language=en_US&type=5) — Salesforce Help · read 2026-09-24 · deactivate rather than delete
- [Apex Developer Guide (PDF, v67.0)](https://resources.docs.salesforce.com/latest/latest/en-us/sfdc/pdf/salesforce_apex_developer_guide.pdf) — Salesforce Developers · read 2026-09-24 · IsParallel tests *"can't call the Test.getStandardPricebookId() method"*; *"queries that use Pricebook2 ignore the with sharing keyword"*; data-silo tests from API 24.0
- [Test.getStandardPricebookId() thread](https://trailhead.salesforce.com/trailblazer-community/feed/0D54V00007T4UoeSAF) — Trailblazer Community, not documentation 🚩 · via search 2026-09-24 · the ID is available without `SeeAllData`
- [Control Access to Price Books and Products](https://trailhead.salesforce.com/content/learn/projects/manage-products-prices-quotes-orders/control-access-price-books-products) — Trailhead · read 2026-09-24 · Price Book default access *View Only*, share a book with *Use*

## History

- 2026-09-24 · created — research pass for the new SF_Sales vault
