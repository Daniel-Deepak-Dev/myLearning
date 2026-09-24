# PRACTICE — SF_Service

> The file you open when the goal is **do something**. Reading lives in [INDEX.md](INDEX.md).
>
> **Three rules.** One item under ▶ Next · max 3 in flight · every lab has a time box.
>
> If you catch yourself reading instead of running, you are in the wrong file.

**51 labs · ~18 h total.** Nothing here runs over 45 minutes. If one overruns it was too big — split it into `NNa` / `NNb` rather than letting it become the lab you never start.

Each lab's full wording lives in its own note, as a `- [ ]` line under `## Hands-on`. **Tick it there when it is done** — labs are ticked, not deleted, because work you actually did is a record. That tick is the whole record: [Done](#done) is rebuilt from it.

## A lab is not finished until you have written down what broke

That is the point of the **Done** table's last column. Copy the error string **verbatim** — not paraphrased, not summarised. In six months the notes will have been rewritten and the release will have moved, but an exact error string is still what you type into a search box. It is the part that keeps earning.

If a lab produced no failure at all, say so — `no failure; worked first time` is a real result and tells you the lab was too gentle.

## Order

The queue is **unblocked-first**, not INDEX order:

- **#1–12** need only Omni-Channel and a **rep user** — a second user you log in as, so the push, the decline and the supervisor view have someone on the other end. #1 builds the channel, queue, statuses and presence configuration that #2–12 reuse.
- **#13–16** need only Lightning Knowledge and, for two of them, a test user. They are independent of chat and Omni-Channel.
- **#17** needs nothing. **#18** builds the Enhanced Chat chain end to end and needs **a web page on a domain you control**. **#19–39** reuse that channel; **#40** also wants the chat on an **Experience Cloud site**.
- **#41–43** need a **Custom Client** deployment and curl — no web page.
- **#44–50** are the first to need **Agentforce**: an active Service Agent, and for #49–50 a deployed Custom Lightning Type.
- **#51** is the only one needing **Xcode or Android Studio**.

That split is deliberate. Omni-Channel is the engine every chat runs through, so it comes first and needs nothing a Developer Edition org lacks. Agentforce was only ever coupled to chat by the handoff, and coupling them earlier would make practice feel like it needs a licence you may not have.

---

## ▶ Next

**SVC-OMNI-01 · 30 min · [Omni-Channel Fundamentals](omni-channel-fundamentals.md)**

Build a Case service channel, a queue with a routing configuration, a presence status and a presence configuration, then assign a case to the queue while the rep is Online. Watch `PendingServiceRouting` turn into `AgentWork`. Every other Omni lab assumes this setup exists.

---

## In flight — max 3

| Lab | Box | Started | Blocked on |
|---|---|---|---|
| — | — | — | — |

---

## Queue

| # | Lab | Topic | Box | Proves | Needs |
|---|---|---|---|---|---|
| 1 | SVC-OMNI-01 | [Omni Fundamentals](omni-channel-fundamentals.md) | 30 min | Queue assignment triggers the push | rep user |
| 2 | SVC-OMNI-02 | [Omni Fundamentals](omni-channel-fundamentals.md) | 10 min | One presence configuration per user | rep user · needs #1 |
| 3 | SVC-OMNI-03 | [Omni Fundamentals](omni-channel-fundamentals.md) | 15 min | No status access, no work | rep user · needs #1 |
| 4 | SVC-OMNI-04 | [Omni Fundamentals](omni-channel-fundamentals.md) | 15 min | Declines live on `AgentWork` | rep user · needs #1 |
| 5 | SVC-ROUTE-01 | [Routing & Capacity](omni-channel-routing-and-capacity.md) | 20 min | Capacity blocks, not availability | rep user · needs #1 |
| 6 | SVC-ROUTE-02 | [Routing & Capacity](omni-channel-routing-and-capacity.md) | 20 min | The Status field frees capacity, not the tab | rep user · needs #1 |
| 7 | SVC-ROUTE-03 | [Routing & Capacity](omni-channel-routing-and-capacity.md) | 15 min | A push timeout is final for that rep | rep user · needs #1 |
| 8 | SVC-ROUTE-04 | [Routing & Capacity](omni-channel-routing-and-capacity.md) | 30 min | Additional skills drop after the time-out | rep user · needs #1 |
| 9 | SVC-OFLOW-04 | [Omni-Channel Flows](omni-channel-flows.md) | 25 min | Records reach a routing flow only as a subflow | rep user · needs #1 |
| 10 | SVC-SUPV-01 | [Omni Supervisor](omni-supervisor.md) | 20 min | A configuration filters the view, not access | rep user · needs #1 |
| 11 | SVC-SUPV-02 | [Omni Supervisor](omni-supervisor.md) | 15 min | Membership through a role is ignored | rep user · needs #1 |
| 12 | SVC-SUPV-04 | [Omni Supervisor](omni-supervisor.md) | 15 min | Offline stops tracking live work | rep user · needs #1 |
| 13 | SVC-KNOW-01 | [Knowledge](knowledge.md) | 15 min | One article is many version rows | — |
| 14 | SVC-KNOW-03 | [Knowledge](knowledge.md) | 10 min | No Knowledge User licence, read-only | test user |
| 15 | SVC-KNOW-02 | [Knowledge](knowledge.md) | 25 min | Category visibility hides categorised articles | test user |
| 16 | SVC-KNOW-04 | [Knowledge](knowledge.md) | 30 min | Scheduled publishing lands on 15-minute slots | — |
| 17 | SVC-CHAT-04 | [Enhanced Chat](enhanced-chat.md) | 10 min | Which name Setup shows for the channel type | — |
| 18 | SVC-CHSET-01 | [Setup Chain](enhanced-chat-setup-chain.md) | 45 min | Nothing reaches the page before Publish | web page on your own domain · needs #1 |
| 19 | SVC-CHAT-01 | [Enhanced Chat](enhanced-chat.md) | 20 min | A conversation survives a closed tab | needs #18 |
| 20 | SVC-CHAT-02 | [Enhanced Chat](enhanced-chat.md) | 15 min | The standard permission set is not rep access | rep user · needs #18 |
| 21 | SVC-CHAT-03 | [Enhanced Chat](enhanced-chat.md) | 15 min | Channel, customer and session are three records | needs #18 |
| 22 | SVC-CHSET-02 | [Setup Chain](enhanced-chat-setup-chain.md) | 20 min | Pre-chat values arrive as strings | needs #18 |
| 23 | SVC-CHSET-03 | [Setup Chain](enhanced-chat-setup-chain.md) | 20 min | Business hours hide the button — minutes later | needs #18 |
| 24 | SVC-CHSET-04 | [Setup Chain](enhanced-chat-setup-chain.md) | 15 min | What pre-chat does without Omni-Flow | needs #18 |
| 25 | SVC-ESD-02 | [Deployments](embedded-service-deployments.md) | 10 min | Type and channel are fixed at creation | needs #18 |
| 26 | SVC-ESD-01 | [Deployments](embedded-service-deployments.md) | 25 min | One channel, many deployments | a second domain · needs #18 |
| 27 | SVC-CONV-01 | [Enhanced Conversation](enhanced-conversation-component.md) | 20 min | Org Default is not required | rep user · needs #18 |
| 28 | SVC-CONV-02 | [Enhanced Conversation](enhanced-conversation-component.md) | 15 min | What a rep gets with no component | rep user · needs #18 |
| 29 | SVC-CONV-03 | [Enhanced Conversation](enhanced-conversation-component.md) | 15 min | Earlier sessions show by default | rep user · needs #18 |
| 30 | SVC-CONV-04 | [Enhanced Conversation](enhanced-conversation-component.md) | 15 min | Properties strip the toolbar for everyone | rep user · needs #18 |
| 31 | SVC-OFLOW-01 | [Omni-Channel Flows](omni-channel-flows.md) | 30 min | The channel launches the flow | rep user · needs #18 |
| 32 | SVC-OFLOW-02 | [Omni-Channel Flows](omni-channel-flows.md) | 20 min | What a mapping-name mismatch does | needs #31 |
| 33 | SVC-OFLOW-03 | [Omni-Channel Flows](omni-channel-flows.md) | 20 min | A flow fault lands in the fallback queue | needs #31 |
| 34 | SVC-SUPV-03 | [Omni Supervisor](omni-supervisor.md) | 20 min | Whispers are stored in the transcript | rep user · needs #18 |
| 35 | SVC-CHVER-01 | [Sessions & Verification](enhanced-chat-sessions-and-user-verification.md) | 15 min | Unverified history stays in one browser | needs #18 |
| 36 | SVC-CHVER-04 | [Sessions & Verification](enhanced-chat-sessions-and-user-verification.md) | 15 min | Automation can block a session ending | needs #18 |
| 37 | SVC-CHVER-02 | [Sessions & Verification](enhanced-chat-sessions-and-user-verification.md) | 45 min | One `sub`, one history everywhere | Node or OpenSSL · needs #18 |
| 38 | SVC-CHVER-03 | [Sessions & Verification](enhanced-chat-sessions-and-user-verification.md) | 20 min | Only RS256/RS512 with 2048-bit keys verify | needs #37 |
| 39 | SVC-CHV2-01 | [v1 vs v2](enhanced-chat-v1-vs-v2.md) | 30 min | One channel serves both clients | a second domain · needs #18 |
| 40 | SVC-ESD-03 | [Deployments](embedded-service-deployments.md) | 15 min | Why `scrt2URL` needs a Trusted URL | Experience Cloud site with the chat · needs #18 |
| 41 | SVC-CHAPI-01 | [Custom Client & SDK](enhanced-chat-custom-client-and-mobile-sdk.md) | 30 min | The whole client is four calls | Custom Client deployment, curl · needs #1 |
| 42 | SVC-CHAPI-02 | [Custom Client & SDK](enhanced-chat-custom-client-and-mobile-sdk.md) | 20 min | `Last-Event-ID` brings back missed events | needs #41 |
| 43 | SVC-CHAPI-03 | [Custom Client & SDK](enhanced-chat-custom-client-and-mobile-sdk.md) | 15 min | Whether an upper-case UUID is rejected | needs #41 |
| 44 | SVC-HAND-01 | [Handoff](bot-and-agent-to-human-handoff.md) | 30 min | The rep gets the same session | Agentforce · rep user · needs #31 |
| 45 | SVC-HAND-02 | [Handoff](bot-and-agent-to-human-handoff.md) | 20 min | A failed transfer leaves the agent in charge | Agentforce · needs #44 |
| 46 | SVC-HAND-03 | [Handoff](bot-and-agent-to-human-handoff.md) | 15 min | What an unwired escalation says | Agentforce · needs #44 |
| 47 | SVC-HAND-04 | [Handoff](bot-and-agent-to-human-handoff.md) | 25 min | The flow, not the agent, decides the handoff | Agentforce · rep user · needs #44 |
| 48 | SVC-CHV2-04 | [v1 vs v2](enhanced-chat-v1-vs-v2.md) | 15 min | Context reaches the agent only after ready | Agentforce · needs #39 |
| 49 | SVC-CHV2-02 | [v1 vs v2](enhanced-chat-v1-vs-v2.md) | 20 min | Mixed versions break the v1 window | Agentforce, Custom Lightning Type · needs #39 |
| 50 | SVC-CHV2-03 | [v1 vs v2](enhanced-chat-v1-vs-v2.md) | 20 min | Renderers are per channel folder, and silent | Agentforce, Custom Lightning Type, DX project · needs #39 |
| 51 | SVC-CHAPI-04 | [Custom Client & SDK](enhanced-chat-custom-client-and-mobile-sdk.md) | 45 min | Two SDKs on one channel | Xcode or Android Studio, Agentforce |

---

## Done

**Generated from the ticked labs — do not add rows by hand.** Tick `- [x]` in the
note and run `python scripts/vault.py fix`; the row appears here. The `What broke`
cell is yours: fill it in and it is preserved on every rebuild.

| Lab | Date | What broke — verbatim |
|---|---|---|
| — | — | — |

---

## Parked

Nothing yet. Park a lab here rather than leaving it in the queue when it is blocked on something outside your control — a licence, a Beta, a region restriction — and say what would unblock it.
