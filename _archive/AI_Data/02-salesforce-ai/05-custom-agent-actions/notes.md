# Custom Agent Actions

> Track: Salesforce AI · Roadmap: Phase 03 · Weeks 9–14 · Status: 🌱 learning
> Currency: **Summer '26 (API 67.0)** · sources in [05-release-radar/trust-security-and-governance.md](../../05-release-radar/trust-security-and-governance.md)

**Roadmap scope:** Invocable Apex and autolaunched Flows as agent actions. Input/output descriptions become the agent's understanding of the tool — write them like prompts. Your Apex/Flow home turf.

> ⚠️ **API 67.0 contains breaking changes that affect existing agent actions.** Read "What breaks at 67.0" before writing new ones or bumping an old class.

## What is it?

An **action** is what an agent can actually do. Everything else — reasoning, grounding, guardrails — exists to decide *which* action runs and *with what inputs*.

### What can be an action

| Building block | Notes |
|---|---|
| **Autolaunched Flow** | Declarative. The default choice for admin-maintainable logic. |
| **Invocable Apex** (`@InvocableMethod`) | Code. For anything Flow can't express. |
| **Prompt template** | A Flex template invoked as an action. |
| **Apex REST endpoint** | Added Spring '26 — existing custom APIs become agent-callable without duplication. |
| **`@AuraEnabled` method** | Added Spring '26 — same idea for existing controller methods. |
| **External API call** | Via named credentials / External Services. |

Spring '26's addition of **Apex REST and `@AuraEnabled`** is quietly significant: a large amount of logic already written for LWC and integrations became agent-callable without a rewrite. When scoping a project, inventory what's already exposed before building new invocables.

## Why it matters (for the AI-Salesforce architect role)

**This is where a Salesforce developer's existing skill converts directly into AI work** — and where the biggest quality lever sits, in a place most developers don't expect.

### The descriptions ARE the interface

The reasoning engine never reads your Apex. It reads:

- the **action description** — to decide whether this action is relevant
- the **input descriptions** — to decide what to pass
- the **output descriptions** — to decide what the result means

So the description field is not documentation. It's **executable specification**, in exactly the same way a subagent description is (see [multi-agent orchestration](../08-multi-agent-orchestration/notes.md)). The most common cause of "the agent picked the wrong action" is a vague description, not a model limitation.

**Write them like prompts, not like field labels:**

| Weak | Strong |
|---|---|
| `Account ID` | `The 18-character Salesforce ID of the Account to credit. Must be an existing Account the running user can edit.` |
| `Processes refund` | `Issues a refund against a closed Order. Use only when the customer has explicitly asked for money back and the order status is Delivered. Do not use for exchanges.` |

The "do not use for…" clause matters as much as the positive description. Negative boundaries are how you stop mis-selection between two similar actions.

### Return typed structures, not prose

If an action returns a structured type rather than a string, a **Custom Lightning Type** can attach a purpose-built UI to it — defined once, rendering idiomatically on desktop LWC *and* natively in the mobile app. Designing action outputs as typed structures gets you cross-surface UI for free. Prose output cannot be rendered specially anywhere.

## How it works

### What breaks at 67.0

Four changes, in rough order of how likely they are to bite:

**1. Invocable input classes need a visible no-arg constructor.** Any custom Apex type used as an invocable action input must expose a no-argument constructor — `public`, or `global` for packaged classes. **The requirement starts at API 66.0**; Summer '26 is when the Release Update auto-activates, which is why it is so often dated to 67.0. **This breaks existing Agentforce Apex actions**, and the mechanism is ordinary OO behaviour: declaring any constructor with arguments removes the compiler-generated default one. It's the first thing to check when an action stops working after an API bump. Apex-side detail: [SF_core/02-apex · 22](../../../SF_core/02-apex-and-triggers/22-invocable-apex-and-agentforce-actions.md).

**2. Database operations default to user mode.** SOQL, SOSL, DML and `Database` methods now enforce the running user's object permissions, FLS and sharing rules. Elevated access is opt-in:

```apex
// 67.0 default — user mode, no keyword needed
List<Account> a = [SELECT Id, Name FROM Account];

// explicit opt-out where genuinely required, with a reason
List<Account> all = [SELECT Id, Name FROM Account WITH SYSTEM_MODE];
```

**3. Keyword-less classes default to `with sharing`.** Previously a class with no sharing keyword *inherited the caller's* sharing context — which meant sharing simply went unenforced when that class was the entry point. Bypassing is now a deliberate `without sharing` declaration.

**4. `WITH SECURITY_ENFORCED` no longer compiles.** Replace with `WITH USER_MODE`, which is materially better, not just renamed:

- handles polymorphic fields (`Owner`, `Task.whatId`)
- checks the **`WHERE` clause**, not just the `SELECT` list
- reports **every** FLS violation instead of only the first — read them off the `QueryException`

### The migration trap

These apply to classes **compiled at 67.0**. Existing classes on older API versions keep their old behaviour, so nothing breaks on upgrade day. **The risk is asymmetric:** the moment someone bumps a class's API version — for an unrelated reason — its data access semantics change underneath them. This deserves a written team convention, not a verbal one.

### Triggers changed too

Apex triggers now **always run in system mode** and can no longer declare sharing or access modes. That removes ambiguity, but it also means a trigger is the wrong place for security-sensitive logic. Push it into a handler class where you control the access mode explicitly.

### Actions as MCP tools

Under Headless 360, an `@InvocableMethod` can be exposed through a **custom hosted MCP server** as an MCP tool — and those servers **respect the org's full sharing and security model**. The same method serves an Agentforce agent and an external Claude client, with the same enforcement. That is the cleanest bridge between this track and the Claude track; see [the capstone MCP project](../../04-capstone/01-mcp-server-salesforce/notes.md).

## Hands-on / labs
<!-- create ./labs/ when you build something; link the files here -->

- [ ] Build one `@InvocableMethod` action, wire it into an agent, and confirm it runs.
- [ ] **The description experiment:** deliberately write a vague description, observe mis-selection in preview, then tighten it and re-run. Nothing teaches this faster.
- [ ] Bump an existing class to 67.0 and see what breaks. Better in a scratch org than in a client's sandbox.
- [ ] Return a typed structure from an action and attach a Custom Lightning Type.
- [ ] Expose the same `@InvocableMethod` as a tool on a custom hosted MCP server and call it from Claude.

## Gotchas & sharp edges

- **Vague descriptions cause mis-selection.** Include negative boundaries ("do not use for exchanges"), not just positive ones.
- **Check for the no-arg constructor first** when an action breaks after an API bump. It's the most common casualty, and it bites from **66.0** — not 67.0, as most write-ups claim.
- **`WITH SECURITY_ENFORCED` won't compile** — grep for it before upgrading anything.
- **User mode may make an action legitimately return less.** That's the feature working, not a bug. If the agent genuinely needs elevated access, opt in explicitly and document why.
- **Every action invocation costs ~20 credits (~$0.10).** An action that internally loops or chains is a recurring cost multiplier.
- **Don't put security-sensitive logic in triggers** — they're system mode with no way to declare otherwise.
- **Idempotency matters more for agents than for UI.** An agent may retry after a timeout. A non-idempotent "issue refund" action can issue two.

## Related topics

- [Agentforce Anatomy](../02-agentforce-anatomy/notes.md) — where actions sit in the runtime
- [Agent Script](../07-agent-script/notes.md) — how actions are invoked in the current authoring model
- [Einstein Trust Layer](../04-einstein-trust-layer/notes.md) — the layer above access mode
- [Multi-agent orchestration](../08-multi-agent-orchestration/notes.md) — descriptions as routing contracts, same principle
- [Capstone: MCP server](../../04-capstone/01-mcp-server-salesforce/notes.md) — actions as MCP tools
- [Release radar: trust, security and governance](../../05-release-radar/trust-security-and-governance.md) — the migration checklist
