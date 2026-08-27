# Model Builder & BYOM

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/agentforce-platform.md](../../05-release-radar/agentforce-platform.md)

**Roadmap scope:** Registering external models — including Claude via Amazon Bedrock — for use in Prompt Builder and beyond. The bridge between your two worlds.

## What is it?

**Model Builder** is where you register and configure which LLMs the org can use. Two categories:

- **Salesforce-hosted models** — provisioned for you, governed by Salesforce's provider agreements. The default.
- **Bring Your Own Model (BYOM)** — an external foundation model reached through *your* endpoint and *your* provider contract: Claude on Amazon Bedrock, models on Google Vertex, Azure OpenAI, or a self-hosted endpoint.

Registered models become selectable in Prompt Builder templates and in agents.

## Why it matters (for the AI-Salesforce architect role)

**Model choice became an architecture decision you own, at three levels — and this is new.**

| Level | Where set | Scope |
|---|---|---|
| Org default | Setup | Everything not overridden |
| **Per agent** | **Pinned in Agent Script** | That agent |
| Per template | Prompt Builder | That template |

Until Agent Script, "which model runs this agent" was effectively one org-wide setting. Now it's a per-agent decision with real cost and latency consequences — a cheap fast model for high-volume triage, a stronger model for the reasoning-heavy subagent. That's a genuine design lever, and it interacts directly with Flex Credits economics.

**The Atlas Reasoning Engine now supports Google Gemini** alongside OpenAI and Anthropic on Amazon Bedrock. Three first-party options before you reach for BYOM at all.

**For the dual-credential angle specifically:** this is the concrete place where the Claude track and the Salesforce track meet in production. Registering Claude via Bedrock and grounding it in Data 360 is a demonstrable skill very few people have on both sides.

## How it works

### Registering a BYOM endpoint (shape of the task)

1. Stand up the model endpoint — e.g. enable a Claude model in **Amazon Bedrock** in your AWS account.
2. Create the connection in Model Builder with the endpoint URL and authentication.
3. Configure request/response mapping so Salesforce's payload shape matches the provider's API.
4. Test with a prompt template.
5. Reference the model from templates and agents.

The step that consumes the time is **3** — payload shapes differ between providers, and mismatches surface as unhelpful runtime errors rather than validation failures.

### When BYOM is actually justified

| Reason | Verdict |
|---|---|
| Existing enterprise agreement / negotiated rate with a provider | **Strong** |
| Data residency requires a specific region or account | **Strong** |
| A fine-tuned or domain-specific model you already run | **Strong** |
| Regulatory need for your own provider contract and audit path | **Strong** |
| "We want Claude" — when Claude via Bedrock is already available first-party | **Weak** — use the supported path |
| "More control" with nothing specific behind it | **Weak** — you're buying operational burden |

BYOM adds an endpoint you own, monitor, patch and pay for. Take it for a reason you can name.

### What changes about the Trust Layer

This is the important architectural caveat and it's frequently glossed over. With a Salesforce-hosted model, the full Trust Layer chain applies and the zero-retention commitment rides on Salesforce's agreement with the provider.

With BYOM, **verify which protections still apply end-to-end** — particularly zero retention, which now depends on *your* contract with *your* provider, not Salesforce's. Don't assume the guarantee transfers. Confirm it against current documentation for your specific configuration before repeating any of it to a client's security team.

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Register Claude via Amazon Bedrock in Model Builder and call it from a prompt template.
- [ ] Pin a different model on one agent in Agent Script and compare latency and output against the org default.
- [ ] Run the same grounded prompt across three models and record cost, latency and quality. That table is a genuinely useful client artifact.
- [ ] Read the Trust Layer audit trail for a BYOM call and compare it against a Salesforce-hosted call — note what differs.

## Gotchas & sharp edges

- **BYOM ≠ better.** It's more control *and* more responsibility: an endpoint you own, monitor and pay for.
- **Verify Trust Layer coverage end-to-end.** Zero retention under BYOM depends on your provider contract, not Salesforce's.
- **Three places set the model** — org default, agent (Agent Script), template. When two paths behave differently, check which model each actually used before debugging the prompt.
- **Payload mapping is the time sink.** Provider API shapes differ; mismatches fail at runtime, not at save time.
- **Claude is available first-party via Bedrock.** Don't build a BYOM integration to get something the supported path already gives you.
- **Model choice is a cost lever.** Combined with per-action billing, a stronger model on a high-volume triage agent is a recurring expense with no proportionate benefit.
- **Fine-tuning is not the answer to hallucination — grounding is.** If the agent invents facts about a customer, that's a retrieval problem. Fix it in [RAG on platform](../../01-data-cloud/08-rag-on-platform/notes.md).

## Related topics

- [Agent Script](../07-agent-script/notes.md) — where per-agent model pinning happens
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — what BYOM changes about the guarantees
- [Prompt Builder](../03-prompt-builder/notes.md) — per-template model selection
- [Claude API](../../03-claude-cca/01-claude-api/notes.md) — the other side of the bridge
- [Salesforce AI Landscape](../01-landscape/notes.md) — where Model Builder sits
