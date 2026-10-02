---
vault: SF_Data_360
format: light
level: basic
status: open
gaps: 2
labs: 3
created: 2026-10-02
updated: 2026-10-02
currency: "Summer '26 (API 67.0)"
---
# Data 360 DevOps

**One line:** Moving Data 360 configuration from sandbox to production with **data kits**, and running custom Python inside Data 360 with **Code Extension**.

**Reach for it when:** someone asks "how do we promote this?" in a Data 360 design review, or a sandbox shows production numbers with no data behind them.

## Key points

- **Two kinds of data kit.** A **DevOps data kit** migrates metadata from sandbox to production; it can be created from any data space and deploys to the **same** data space in the target. A **standard data kit** packages a solution to share; it is created from the **default** data space and deploys to **any** data space.
- **A DevOps kit carries** data streams, data lake objects, calculated insights and data graphs, among others. Retrieve it with `sf project retrieve start --manifest`, then deploy with `sf project deploy start`.
- **A Data 360 sandbox holds metadata only.** No data is copied, not even in Partial Copy or Full Copy sandboxes.
- **Connections arrive Inactive.** They are replicated without their authorization data, so each one must be activated and re-authorized before data flows.
- **Code Extension** runs custom **Python** inside Data 360: batch data transforms, and custom chunking for search indexes → [Vector search](vector-search-and-rag.md). You build it with the Data Custom Code Python SDK and the Salesforce CLI Code Extension plugin.
- **Author is not operator.** Developers write the code; users with the **Data Cloud Architect** permission set run, monitor and migrate it.

## Gotchas

- **Sandbox components show production record counts and dates** until data is ingested in the sandbox. A data stream can look populated and hold nothing.
- **A DevOps kit is pinned to one data space.** It doesn't quietly become a distributable package later. Decide early whether you are promoting or packaging.
- **An older sandbox needs a refresh** before Data 360 can be provisioned in it, if it predates sandbox GA.
- **Check what a kit pulled in.** Adding a transform brings its code extension along automatically.

## Gaps to close

- [ ] Re-read Data Kits, Data 360 in a Sandbox and the CLI deployment guide in full once the doc domains are reachable. This note was built from search extracts.
- [ ] Which Data 360 components can't be carried in a data kit at API 67.0, and so stay manual steps in a runbook?

## Hands-on

- [ ] **D360-OPS-01** · 30 min · In a Data 360 sandbox, build a DevOps data kit with one data stream and one calculated insight, then retrieve it with the CLI. **Proves:** what comes back as metadata, and what doesn't; that gap is your runbook's manual section. **Needs:** a Data 360 sandbox.
- [ ] **D360-OPS-02** · 15 min · Open a freshly created Data 360 sandbox's connections and data streams before activating anything. **Proves:** connections are Inactive and stream counts show production values with no data. **Needs:** #1.
- [ ] **D360-OPS-03** · 30 min · Scaffold a code extension with the Python SDK, run it locally, then deploy it. **Proves:** the author/operator split; check who can run it.

## Related

- [Lab Environment](lab-environment.md) — where you can practise this without a client sandbox
- [Vector Search & RAG](vector-search-and-rag.md) — the custom-chunking use of Code Extension
- [Data Model: DSO, DLO & DMO](data-model-dso-dlo-dmo.md) — the data spaces a kit is pinned to
- [RELEASE-RADAR · Data 360](../RELEASE-RADAR/data-360.md) — the Code Extension and data-kit entries

## Sources

- [Data Kits](https://help.salesforce.com/s/articleView?id=sf.c360_a_data_package_kits.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · standard vs DevOps data kits and their data-space rules
- [Use CLI to Deploy Changes from a Sandbox to Data 360](https://developer.salesforce.com/docs/data/data-cloud-dev/guide/dc-deploy_data_kit_using_cli.html) — Salesforce Developers · via search 2026-10-02 · retrieve and deploy commands; kit contents
- [Considerations for Sandbox in Data 360](https://help.salesforce.com/s/articleView?id=data.c360_a_data_cloud_sandbox_consideration.htm&language=en_US&type=5) — Salesforce Help · via search 2026-10-02 · metadata only; production values shown; connections Inactive
- [Code Extension in Data 360](https://developer.salesforce.com/docs/data/data-cloud-code-ext/guide/use-custom-code.html) — Salesforce Developers · via search 2026-10-02 · Python, the SDK and CLI plugin, Data Cloud Architect permission set

## History

- 2026-10-02 · created — facts carried over from the archived roadmap notes and confirmed against Salesforce search extracts
