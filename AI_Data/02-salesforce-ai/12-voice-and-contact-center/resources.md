# Agentforce Voice & Contact Center — Resources

> **Source note.** `salesforce.com`, `admin.salesforce.com` and `help.salesforce.com` return HTTP 403 to automated fetching, so those pages were read via search extracts — the constraint the radar records in [01-agentforce/2026-07-28.md](../../05-release-radar/01-agentforce/2026-07-28.md). `developer.salesforce.com` fetched cleanly but its partner-guide overview is thin. **Every pricing figure in this topic is secondary-sourced** — no first-party pricing page was reached. Treat credit rates as indicative until checked against a contract or an org.

## Official docs / Trailhead

- **Agentforce Voice overview** (Agentforce Partner Guide) — architecture and partner telephony — https://developer.salesforce.com/docs/ai/agentforce-partner/guide/agentforce-voice-overview.html
- **Meet Agentforce Voice** — Trailhead quick-look module — https://trailhead.salesforce.com/content/learn/modules/agentforce-voice-quick-look/meet-agentforce-voice
- From Chat to Calls: Introducing Agentforce Voice (Salesforce Admins) — https://admin.salesforce.com/blog/2026/introducing-agentforce-voice
- Salesforce Summer '26 Release Notes — SIP routing and Mobile SDK GA — https://help.salesforce.com/s/articleView?language=en_US&id=release-notes.salesforce_release_notes.htm

## Courses & videos
<!-- The Trailhead quick-look above is the only first-party module located as of 2026-07-28. Expect a fuller module once global languages leave Beta. -->

## Articles & repos

**Contact Center launch coverage — the GA date and positioning:**
- Enterprise Connect 2026: Salesforce Launches Agentforce Contact Center (UC Today) — https://www.uctoday.com/unified-communications/salesforce-agentforce-contact-center/
- Salesforce launches Agentforce Contact Center (No Jitter) — https://www.nojitter.com/ai-automation/salesforce-launches-agentforce-contact-center
- Agentforce Contact Center brings native CCaaS to Salesforce (TechTarget) — https://www.techtarget.com/searchCustomerExperience/news/366639947/Agentforce-Contact-Center-brings-native-CCaaS-to-Salesforce
- Agentforce Contact Center and the End of the Integration Era (SalesforceDevops.net) — the partner-vs-competitor read — https://salesforcedevops.net/index.php/2026/03/10/agentforce-contact-center-salesforce-ccaas-competition/

**Setup and capability detail:**
- Agentforce Voice Agent Setup: From Prerequisites to Talking with the Agent (ABSYZ) — the escalation prerequisites — https://www.absyz.com/agentforce-voice-agent-setup-in-salesforce-from-prerequisites-to-talking-with-the-agent/
- Agentforce Voice: The Complete 2026 Guide (Salesforce Dictionary) — PSTN/SIP, barge-in, logging — https://salesforcedictionary.com/blogs/agentforce-voice-complete-2026-guide
- An Update on Voice: What's Available and What's on the Roadmap (Performa) — https://performa-it.co.uk/resources/knowledge-hub/an-update-on-voice-whats-available-and-whats-on-the-roadmap/

**Pricing — all secondary, all to be verified:**
- Salesforce Agentforce Credits & Cost Model: Complete Guide 2026 (Jitendra Zaa) — the 30-credit and 60-credit/min figures — https://www.jitendrazaa.com/blog/salesforce/salesforce-agentforce-credits-cost-model-complete-guide-2026/
- Salesforce Agentforce: Features, Pricing & Limits (2026) — https://myaskai.com/blog/salesforce-agentforce-complete-guide-2026

**Ecosystem:**
- TTEC Digital deploys first live Salesforce customer on Agentforce Contact Center — https://www.globenewswire.com/news-release/2026/07/23/3332068/0/en/TTEC-Digital-Deploys-First-Live-Salesforce-Customer-on-Agentforce-Contact-Center.html
- Vonage Deepens Native Contact Center with Agentforce Voice Integrations — https://finviz.com/news/255045/vonage-deepens-native-contact-center-with-salesforces-agentforce-voice-integrations

## In this repo
- [Release radar: Agentforce platform](../../05-release-radar/agentforce-platform.md) — dated entries and the TTEC field note
- [Release radar: pricing & certification](../../05-release-radar/pricing-and-certification.md) — Flex Credits, pay-per-resolution, voice rates
- [Agent Script](../07-agent-script/notes.md) — where voice behaviour is authored
- [ADLC & Agentforce DX](../13-adlc-and-agentforce-dx/notes.md) — `VoiceCallId` and adversarial voice testing

## My own artifacts
<!-- labs, gists, dev orgs, scripts you built for this topic -->
<!-- Record here: (1) whether Voice is provisionable in an EU dev org — the answer that gates everything else;
     (2) measured credits for the same conversation as text vs voice;
     (3) how long the escalation handoff actually takes. -->
