# Agentforce Voice & Contact Center

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · Product status: **GA** — Voice since the Winter '26 cycle, Contact Center since 2026-02-23 · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Scope:** autonomous voice agents — how a call reaches one, the telephony options behind it, escalation to a human, what voice costs per minute versus per action, and the failure modes that only exist when the channel is a phone line.

> **Why this folder exists.** Voice had exactly one passing line in this study base before 2026-07-28, and "Contact Center" appeared nowhere outside the radar — despite Agentforce Contact Center being **GA since February 2026** and voice being where the commercial weight of Agentforce sits. A voice agent is not a text agent with a speaker attached: it has different economics (30 credits vs 20), different failure modes (latency, barge-in, mid-call handoff) and a hard geographic constraint that can end a client conversation before it starts.

## What is it?

Two products that get conflated, so separate them first:

- **Agentforce Voice** — the *capability*. An Agentforce Service Agent that handles autonomous inbound and outbound calls over **PSTN or SIP trunking**. Salesforce's own framing is blunt: it replaces the IVR.
- **Agentforce Contact Center** — the *product*. Salesforce's native CCaaS offering, **GA February 23, 2026**, launched at Enterprise Connect 2026, described as "the only contact center solution that unifies voice, digital channels, CRM data, and AI agents natively in a single system."

You can run Voice without buying Contact Center — pointed at a partner telephony provider. Contact Center is the bet that you'd rather not have a partner at all.

### Status and dates

| Thing | Status | Date |
|---|---|---|
| Agentforce Voice | **GA** | Winter '26 cycle — announced **October 21, 2025** with native CCaaS partners *(see caveat)* |
| Agentforce Contact Center | **GA** | **February 23, 2026**, launched at Enterprise Connect 2026 |
| Voice for Digital Channels | GA | Q2 2026 — web chat, mobile apps, WhatsApp, messaging |
| SIP routing · Mobile SDK | GA | Summer '26 |
| Global languages | **Beta** | per the [2026-07-27 scan](../../05-release-radar/01-agentforce/2026-07-27.md) |
| First customer go-live on Contact Center | — | TTEC Digital / Compass Working Capital, **July 23 2026** — see the field notes in [agentforce-platform.md](../../05-release-radar/agentforce-platform.md) |

> ⚠️ **Conflicting GA dates.** Most sources put Voice GA at **October 21, 2025** (Winter '26 cycle); others describe it moving "from pilot to GA" in **Spring '26** with Atlas-powered autonomous reasoning. The likely reconciliation is progressive GA — the channel first, the fully reasoning autonomous agent later — but that is inference. If a date matters to a client commitment, verify it; don't take either number from these notes.

## Why it matters (for the AI-Salesforce architect role)

**Voice is where the money is, and where the credits go.** A voice action costs **30 Flex Credits** against a standard action's 20 — 50% more per action, before you consider that voice conversations involve more turns than chat. Any ROI model that treats voice as "chat, but spoken" is wrong by a wide margin.

**The geographic constraint is a deal-qualifier, not a footnote.** Voice was **US and Canada only** as of early 2026, with global languages still Beta as of this scan. At Geeksoft, working from Europe, **this is the first thing to check** — before the demo, before the discovery call, before anyone gets attached to the idea. It is the single most likely reason a voice project doesn't happen.

**It changes what "the agent failed" means.** Text agents fail by saying something wrong. Voice agents also fail by taking too long to say anything, by talking over the customer, or by dropping context when a human takes the call. Those are latency and protocol problems, not prompt problems, and no amount of Agent Script tuning fixes them. See the failure modes below.

**Contact Center is a competitive posture as much as a product.** Salesforce shipping native CCaaS puts it opposite Genesys, Five9 and NICE — the same companies listed as its Voice partners. Know both facts at once: they are partners at the Voice layer and competitors at the Contact Center layer. Clients notice.

## How it works

```
   inbound call (PSTN or SIP trunk)
        │
        ▼
   telephony layer ── one of:
        ├── Amazon Connect ......... native, Salesforce manages provisioning
        ├── Partner Telephony ...... Genesys · Five9 · NiCE · Vonage
        └── SIP trunk .............. Summer '26; rides your existing internet,
        │                            no dedicated carrier number
        ▼
   Agentforce Service Agent  ── Atlas Reasoning Engine
        │   • barge-in: customer can interrupt mid-sentence
        │   • autonomous inbound AND outbound
        │   • automatic conversation logging
        ▼
   escalation to a human ── context transferred, live transcription into
        │                   Salesforce Voice so the rep can take over mid-call
        ▼
   full auditability through Data 360
```

### Setup — the shape of it

The simple path: point **a phone number** — or, since Summer '26, **a SIP trunk** — at an Agentforce Service Agent, then configure the connection from the **Agentforce Voice setup page**. Salesforce's release notes position SIP as the cheaper and more flexible option precisely because it rides your existing internet connection rather than a dedicated carrier number.

**Escalation is the part with prerequisites.** To hand a call to a human you need all three:

1. **Partner Telephony Setup** configured
2. **Service Cloud Voice** enabled
3. **Contact Center setup** completed

That is why a voice agent that answers calls fine can still fail its first escalation — the agent side works and the telephony side was never finished. Test escalation separately from conversation.

### Economics — read this before quoting anything

| Unit | Cost |
|---|---|
| Standard action | **20 Flex Credits** ≈ $0.10 |
| **Voice action** | **30 Flex Credits** ≈ $0.15 |
| Alternative **per-minute** voice model | **60 credits/min** ≈ $0.30 production, $0.24 sandbox |
| Flex Credits | $500 per 100,000 |

> ⚠️ These figures come from **secondary sources**, not a first-party pricing page. The per-minute model in particular changes the arithmetic completely — a five-minute call at 60 credits/min is 300 credits regardless of how many actions ran. **Verify against the client's actual contract before it reaches a proposal.** See [pricing-and-certification.md](../../05-release-radar/pricing-and-certification.md).

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] **Do this first:** check whether Agentforce Voice is even provisionable in an EU dev org. Record the answer — it determines whether the rest of this list is theoretical.
- [ ] Build one Service Agent, point a number at it, and call it. Then call it again and **interrupt it mid-sentence** — barge-in is the behaviour that most obviously separates voice from chat.
- [ ] Configure escalation end to end (Partner Telephony → Service Cloud Voice → Contact Center) and confirm the transcript and context actually arrive with the human. Time how long the handoff takes.
- [ ] Run the same conversation as text and as voice; compare credits consumed. That number is your ROI model's input.
- [ ] Model the same 5-minute call under per-action and per-minute billing. Know which model a client is on before promising a cost.
- [ ] Compare a voice agent authored in [Agent Script](../07-agent-script/notes.md) against the legacy setup — voice-specific constructs (`VoiceCallId`, connection blocks) were added to the ADLC skills in July 2026, see [13-adlc-and-agentforce-dx](../13-adlc-and-agentforce-dx/notes.md).

## Gotchas & sharp edges

- **US and Canada only** as of early 2026; global languages **Beta**. Check availability in the target region *first*. From Europe this is the qualifier that matters most.
- **Two billing models, wildly different arithmetic.** Per-action (30 credits) and per-minute (60 credits/min) are not close to equivalent. A long call with few actions is cheap under one and expensive under the other. Ask which applies.
- **Escalation has three prerequisites that live outside Agentforce.** Partner Telephony, Service Cloud Voice, Contact Center setup. The agent working is not evidence that escalation works.
- **Salesforce is both partner and competitor to Genesys, Five9 and NiCE.** Partner at the Voice layer, competitor at the Contact Center layer. Don't be surprised by the room's reaction.
- **Latency is a design constraint, not an implementation detail.** Every extra grounding hop, every extra action, is dead air on a phone call. The retrieval budget that feels fine in chat can be unusable in voice.
- **Barge-in changes the conversation model.** The customer can interrupt mid-sentence, so an agent that plans a long answer will rarely finish it. Write for short turns.
- **Voice agents log everything.** Automatic conversation logging plus full auditability through Data 360 is a feature — and a data-retention and consent question in the EU. Raise it before the client does.
- **The Mobile SDK and SIP routing are Summer '26 GA** — anything written before that describes a narrower product.
- **"Agentforce Voice" and "Salesforce Voice" are different things.** The former is the AI agent; the latter is the Service Cloud telephony surface the transcript lands in.

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — Service Agent vs Employee Agent; voice agents are Service Agents
- [Agent Script](../07-agent-script/notes.md) — where voice behaviour is authored, including model pinning for latency
- [Observability & Testing](../09-observability-and-testing/notes.md) — Refined Agent Analytics, Custom Scorers; voice sessions score differently
- [ADLC & Agentforce DX](../13-adlc-and-agentforce-dx/notes.md) — voice modality in the ADLC skills, `VoiceCallId`, adversarial voice testing
- [Prebuilt agents & buy vs build](../14-prebuilt-agents-and-buy-vs-build/notes.md) — Contact Center as a packaged product decision
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — masking and audit, which apply to transcripts too
