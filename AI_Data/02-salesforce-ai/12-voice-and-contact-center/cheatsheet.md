# Agentforce Voice & Contact Center — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

**Voice** = an Agentforce Service Agent answering PSTN/SIP calls autonomously, replacing the IVR (GA, Winter '26 cycle). **Contact Center** = Salesforce's own native CCaaS built around it (**GA 2026-02-23**). Voice costs more per action, fails in ways text never does, and was **US/Canada only** as of early 2026.

## Key terms
| Term | Definition |
|---|---|
| Agentforce Voice | The capability — autonomous inbound *and* outbound calls over PSTN or SIP trunking. |
| Agentforce Contact Center | The product — native CCaaS unifying voice, digital channels, CRM data and AI agents. GA Feb 23 2026, Enterprise Connect. |
| Partner Telephony | The integration path for Genesys, Five9, NiCE, Vonage. **Amazon Connect is native** — Salesforce manages provisioning. |
| SIP trunking | Summer '26. Rides your existing internet instead of a dedicated carrier number — cheaper and more flexible. |
| Barge-in | The customer interrupting mid-sentence. Supported — and it means long agent answers rarely land. |
| Voice for Digital Channels | GA Q2 2026 — same capability on web chat, mobile, WhatsApp, messaging. |
| Salesforce Voice | ≠ Agentforce Voice. The Service Cloud telephony surface the live transcript lands in. |

## Rules of thumb

- **Check regional availability before anything else.** US + Canada only as of early 2026; global languages Beta. From Europe this qualifies or kills the project.
- **Voice action = 30 Flex Credits (~$0.15)** vs standard 20 (~$0.10). Never model voice as "chat but spoken."
- **Escalation needs three things outside Agentforce:** Partner Telephony Setup → Service Cloud Voice enabled → Contact Center setup complete.
- **Latency is a design constraint.** Every grounding hop is dead air. Write short turns.
- Salesforce is **partner and competitor** to Genesys/Five9/NiCE — Voice layer vs Contact Center layer.

## Exam traps / common confusions

- **Two billing models, not one:** per-action **30 credits**, or per-minute **60 credits/min** (~$0.30 prod, $0.24 sandbox). A long call with few actions prices completely differently under each. *(Secondary-source figures — verify.)*
- **Voice GA date is disputed:** Oct 21 2025 (Winter '26 cycle) vs "pilot → GA in Spring '26". Likely progressive GA. Don't quote either without checking.
- **A working voice agent is not evidence that escalation works** — the telephony prerequisites are separate.
- **Amazon Connect is the native option**; the other four are Partner Telephony.
- Contact Center is **GA, not Beta** — since February 2026.

## Minimal example

```
call → telephony (Amazon Connect native | Partner Telephony | SIP trunk)
     → Agentforce Service Agent (Atlas)  ── barge-in · autonomous in/outbound · auto-logging
     → escalate → human, with context + live transcription into Salesforce Voice
     → audit trail in Data 360

partners: Amazon Connect · Five9 · Genesys · NiCE · Vonage
credits:  standard 20  |  voice 30  |  per-minute alt. 60/min   ($500 / 100k credits)
```
