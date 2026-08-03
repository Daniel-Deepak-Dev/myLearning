# Flow Run Context & Sharing

> Area: 04-flow-and-automation · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 09

**Scope:** What a flow is *allowed* to see and write, which is a different question from who it runs as. Guest and external specifics are [21](21-flow-for-external-and-guest-users.md); the org's access model is [07-security](../07-security-and-sharing/INDEX.md).

> **What changed.** *"A record-triggered flow runs as the user who saved the record, so it respects their access"* — the first half is right and the second half is wrong. **Running user and execution context are two independent things.** A record-triggered flow's running user is the saver, but its execution context is **system context without sharing**, it cannot be changed, and the flow can therefore read and write records that user cannot see. The `How to Run the Flow` setting people cite as the fix **does not exist on record-triggered flows at all**.

## Core idea

Every flow answers two separate questions. *Who is the running user?* decides what `$User` returns, who owns records the flow creates, and whose name appears in audit fields. *What context does it execute in?* decides whether object permissions, field-level security and sharing rules are enforced at all. Confusing them is the most consequential mistake in this area, because a flow can run **as** a user with almost no permissions and still do anything, or run as an administrator and still be blocked. The rule that actually holds: **the triggered flow types are system context without sharing and you cannot change it**; screen and autolaunched flows are the only ones that expose a choice, and their default is not a context but a deferral — the option is literally named *Depends on How Flow is Launched*.

## How it works

| Flow type | Execution context | Configurable? |
|---|---|---|
| **Record-triggered** | system context **without sharing** | **no** |
| **Schedule-triggered** | system context **without sharing** | no |
| **Platform event-triggered** | system context **without sharing** | no |
| **Screen flow** | *Depends on How Flow is Launched* — user context when launched from a page, button or action | **yes** |
| **Autolaunched** | *Depends on How Flow is Launched* — inherits its caller | **yes** |

- **`How to Run the Flow`** sits in Flow Properties on screen and autolaunched flows, with three values: *Depends on How Flow is Launched*, **System Context With Sharing—Enforces Record-Level Access**, and **System Context Without Sharing—Access All Data**.
- **"With Sharing" here means sharing only.** Object permissions and FLS are still bypassed — it is not user mode, and it is not what `with sharing` means in Apex. → [02-apex · 10](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md), [11](../02-apex-and-triggers/11-sharing-keywords-and-apex-managed-sharing.md)
- **The default being conditional is why published guidance disagrees** about what an autolaunched flow's default is. It has no fixed answer; read the caller.
- **A subflow inherits the parent's context**, so elevating one screen flow elevates everything it calls.
- **The elevated-subflow pattern is the recommended shape**: leave the outer flow in user context and put the one privileged operation in a small subflow set to system context — the Flow equivalent of a narrow `without sharing` helper class.

## 2026 currency

The platform moved in the opposite direction everywhere else, which is what makes this note worth reading twice. **Apex flipped to user mode by default at API 67.0** and keyword-less classes now default to `with sharing` → [../CURRENCY.md](../CURRENCY.md). Flow did not flip. A record-triggered flow at 67.0 has exactly the reach it had in 2019, so **the same logic is now more permissive in Flow than in Apex** — which inverts the old assumption that clicks are the safe option and code is the risky one. Nothing in the Summer '26 notes changes flow run context; the change is in the contrast. Treat "should this be Flow or Apex?" as a security question as well as a limits question. → [01](01-automation-landscape-and-tool-selection.md), [07-security](../07-security-and-sharing/INDEX.md)

## Gotchas

- **A record-triggered flow bypasses sharing, FLS and object permissions**, whatever the running user can do. There is no setting to change this.
- **"System Context With Sharing" enforces record access only.** FLS and object permissions are still bypassed — the name oversells it.
- **The screen-flow default is a deferral, not a context.** *Depends on How Flow is Launched* means the answer changes with the launch surface, including the site a guest hits. → [21](21-flow-for-external-and-guest-users.md)
- **Elevating a parent elevates every subflow it calls.** Grant privilege at the leaf, not the root.
- **`$User` tells you nothing about permissions being enforced.** It is the running user, not the context.
- **A Get Records in system context returns rows the user will never be shown**, and putting them on a screen leaks them — through the DOM, not just the UI. → [04](04-screen-flows-and-ux-design.md)
- **Debugging as another user does not reproduce context**, because the triggered types' context is fixed regardless of who runs them. → [15](15-flow-testing-and-debugging.md)
- **An in-flight approval locks the record**, and a flow in any context will fail to update it. → [17](17-approval-orchestration.md)

## Recall

Q: What are the two independent questions every flow answers about access?
A: Who the running user is, and what execution context it runs in. They are unrelated.

Q: Can you make a record-triggered flow respect the running user's sharing?
A: No. It runs in system context without sharing and exposes no setting to change that.

Q: What does *System Context With Sharing—Enforces Record-Level Access* actually enforce?
A: Record-level sharing only. Object permissions and field-level security are still bypassed.

Q: What is the default value of *How to Run the Flow*, and why is it confusing?
A: *Depends on How Flow is Launched* — it is a deferral rather than a context, so the effective answer changes with the caller.

Q: Why is Flow now more permissive than Apex for the same logic?
A: Apex defaulted to user mode at API 67.0 and `with sharing`; Flow's triggered types did not move.

## Related

- [21 · Flow for external & guest users](21-flow-for-external-and-guest-users.md) — where a permissive context becomes a public exposure
- [02-apex · 10 Apex security, user mode & FLS](../02-apex-and-triggers/10-apex-security-user-mode-and-fls.md) — the same distinction in code, and the 67.0 default that Flow did not follow
- [07-security](../07-security-and-sharing/INDEX.md) — the permissions and sharing model these contexts bypass
