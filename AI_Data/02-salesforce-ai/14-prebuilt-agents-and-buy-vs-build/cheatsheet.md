# Prebuilt agents & buy vs build — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Salesforce now ships **finished** agents — Help Agent, Commerce, IT Service, Contact Center, industry packs — so the architect's question moved from "can you build one" to **"should you"**. Deployment is minutes; **grounding it well is the project**, and that's the billable part.

## Key terms
| Term | Definition |
|---|---|
| Help Agent | Prebuilt self-service support agent. **GA July 2026**, "six clicks or less", web/text/voice from one screen. Portal is now a single conversation bar. |
| Shopper / Buyer / Merchant | Agentforce Commerce trio. **GA July 6 2026.** B2C storefront · B2B via WhatsApp+SMS · back-office catalogue in natural language. |
| Pay-per-resolution | **$2** per autonomous end-to-end resolution; consumption unmetered *during* the interaction. Help Agent, July 2026. |
| AELA | Agentic Enterprise License Agreement — negotiated, enterprise-wide. The VA's **$1.6B / 3yr**, July 24 2026. |
| IT Service Domain Pack | 50+ prebuilt agents into Slack, Teams, IT Service Desk. |
| Missionforce | The public-sector/health vertical estate behind the VA deal. |

## Rules of thumb

- **The deciding question: is the differentiation in the CONVERSATION or in the DATA?** Conversation → build. Data → buy, and spend the budget on Data 360 grounding.
- **Price the maintenance, not the build.** A custom agent commits somebody to the outer loop forever; a prebuilt one moves that to Salesforce.
- **Know the commercial model before modelling anything.** Discrete countable outcomes favour pay-per-resolution; long exploratory sessions may favour Flex Credits.
- **Benchmarks to quote:** `help.salesforce.com` — **4.3M inquiries, 70% resolved** (first-party). Oviva — **300k msgs/month**, half deflected, 40% resolved autonomously.

## Exam traps / common confusions

- **"Deployable in minutes" is true and misleading** — deployment is minutes, grounding is the project. Both get quoted in the same meeting.
- **Pay-per-resolution needs "resolution" defined** — who adjudicates, what a partial counts as. Commercial question, not technical.
- **Commerce sells natively inside ChatGPT** — catalogue synced from Business Manager, no middleware — but **checkout stays on the merchant's own site**. Don't assume that of competitors.
- **Prebuilt ≠ exempt from platform limits.** Flex Credits, voice rates and Trust Layer behaviour are unchanged.
- The 70% figure is **Salesforce's own** — cite it as theirs.

## Minimal example

```
buy-vs-build, in order — first clear answer usually decides it

 1. prebuilt covers the use case?          no → build
 2. differentiation in conversation/data?  conversation → build | data → buy + ground
 3. commercial model fits the outcome?     discrete resolutions → pay-per-resolution
 4. who owns it through drift?             prebuilt → Salesforce | custom → you, forever
 5. extensible at the seam that matters?   yes → buy then extend

models: Flex Credits ~$0.10/action ($500/100k) · pay-per-resolution $2 · AELA negotiated
```
