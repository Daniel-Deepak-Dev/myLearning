# MuleSoft Agent Fabric — Resources

> **Source note.** `salesforce.com`, `salesforceben.com` and `architect.salesforce.com` return HTTP 403 to automated fetching, so several pages below were read via search extracts rather than directly — the same constraint the radar records in [01-agentforce/2026-07-28.md](../../05-release-radar/01-agentforce/2026-07-28.md). **`docs.mulesoft.com` fetched cleanly and is the authority here.** Where launch-era articles and the current docs disagree on component names, prefer the docs — that is exactly how the Flex Gateway → Omni Gateway rename surfaced.

## Official docs / Trailhead

**First-party MuleSoft — the authoritative set:**
- **MuleSoft Agent Fabric Overview** — the four pillars, registration methods, Agent Networks — https://docs.mulesoft.com/general/agent-fabric-overview
- Omni Gateway release notes — where the Flex Gateway rename is documented — https://docs.mulesoft.com/release-notes/flex-gateway/flex-gateway-release-notes
- Deploy a Managed Omni Gateway — https://docs.mulesoft.com/gateway/latest/flex-gateway-managed-set-up
- MuleSoft Agent Fabric product page — https://www.mulesoft.com/ai/agent-fabric
- MuleSoft Omni Gateway — https://www.mulesoft.com/platform/omni-api-gateway
- AI Agent Governance — https://www.mulesoft.com/platform/ai/ai-agent-governance

**Salesforce architect guides (403 to automated fetch — open in a browser):**
- MuleSoft Agent Fabric Deep Dive — https://architect.salesforce.com/docs/architect/fundamentals/guide/mulesoft-agent-fabric-deep-dive.html
- Architecting the Agentic Enterprise with MuleSoft — https://architect.salesforce.com/docs/architect/fundamentals/guide/mulesoft-architecting-agentic-enterprise.html

**Announcements (secondary — treat claims as aspirational):**
- Salesforce Launches MuleSoft Agent Fabric — the September 2025 launch — https://www.salesforce.com/news/stories/mulesoft-agent-fabric-announcement/
- Salesforce Advances Agent Fabric: Guided Determinism and Governance Controls — **April 15, 2026** — https://www.salesforce.com/news/stories/agent-fabric-control-plane-announcement/
- Salesforce Expands MuleSoft Agent Fabric with Automated Discovery — https://www.salesforce.com/news/stories/mulesoft-agent-fabric-automated-agent-discovery/
- Trusted Agents at Scale: How Open Discovery Is Unifying the Agentic Enterprise — the federated-registry rationale — https://www.salesforce.com/blog/open-discovery-agentic-enterprise/

## Courses & videos
<!-- No Trailhead module located as of 2026-07-28. Worth re-checking — this is a MuleSoft product, so any module may live under the MuleSoft rather than the Agentforce catalog. -->

## Articles & repos
- Salesforce Launches MuleSoft Agent Fabric: A Complete Breakdown (Salesforce Ben) — component-by-component with the launch dates — https://www.salesforceben.com/salesforce-launches-mulesoft-agent-fabric-a-complete-breakdown/
- Meet the New MuleSoft Agent Fabric: Salesforce's Solution to Rogue Agents (Salesforce Ben) — the agent-sprawl framing — https://www.salesforceben.com/meet-the-new-mulesoft-agent-fabric-salesforces-solution-to-rogue-agents/
- MuleSoft Omni Gateway: As Close to an Agent Control Plane as It Gets (Futurum) — https://futurumgroup.com/insights/mulesoft-omni-gateway-as-close-to-an-agent-control-plane-as-it-gets/
- Salesforce Stakes Out Multi-Vendor Agent Control Plane — Determinism, Governance, Enforcement Remains the Test (Futurum) — the sceptical read, worth having — https://futurumgroup.com/insights/salesforce-stakes-out-multi-vendor-agent-control-plane-determinism-governance-enforcement-remains-the-test/
- MuleSoft Omni Gateway — A New Era for API Management — the rename explained by a practitioner — https://medium.com/another-integration-blog/mulesoft-omni-gateway-a-new-era-for-api-management-6df1970d281b
- Publishing and Securing MCP Servers with Managed Omni Gateway — https://medium.com/another-integration-blog/publishing-and-securing-mcp-servers-with-managed-omni-gateway-56d529c9814e

## In this repo
- [Multi-Agent Orchestration](../08-multi-agent-orchestration/notes.md) — the in-org layer this sits above
- [MCP (Claude track)](../../03-claude-cca/05-mcp/notes.md) — the protocol being governed
- [Release radar: developer tooling & APIs](../../05-release-radar/developer-tooling-and-apis.md) — dated entry, hosted MCP servers
- [Agentforce Specialist exam guide](../_cert-agentforce-specialist/exam-guide.md) — the Multi-Agent Interoperability domain

## My own artifacts
<!-- labs, gists, dev orgs, scripts you built for this topic -->
<!-- Put the two-layer client diagram here once drawn — in-org orchestration inside, Fabric registry across. It's the reusable Geeksoft artifact. -->
<!-- Also record the answer when you establish what Agent Fabric actually costs. -->
