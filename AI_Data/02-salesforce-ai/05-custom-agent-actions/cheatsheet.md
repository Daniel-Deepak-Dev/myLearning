# Custom Agent Actions — Cheatsheet

> Half a page max. If it doesn't fit here, it belongs in notes.md.

## In one sentence

Flows, `@InvocableMethod` Apex, prompt templates, Apex REST and `@AuraEnabled` methods become agent actions — and their **descriptions**, not their code, are what the reasoning engine actually reads.

## Key terms
| Term | Definition |
|---|---|
| Action description | Executable specification, not documentation. Drives selection and input filling. |
| `WITH USER_MODE` | Replaces the retired `WITH SECURITY_ENFORCED`. Checks the `WHERE` clause and reports *all* FLS violations. |
| Custom Lightning Type | UI attached to a typed action output; renders on desktop and native mobile from one definition. |
| No-arg constructor rule | Invocable input classes need a visible one from **API 66.0**; the Release Update enforces it in Summer '26. Breaks existing actions. |

## Rules of thumb

- Write descriptions like prompts, with **negative boundaries** — "do not use for exchanges" prevents more mis-selection than any positive phrasing.
- Return **typed structures**, not prose — prose can't be rendered specially anywhere.
- Inventory existing **Apex REST / `@AuraEnabled`** methods before building new invocables (Spring '26 made them agent-callable).
- Make actions **idempotent**: an agent may retry after a timeout, and "issue refund" twice is a real incident.

## Exam traps / common confusions

- **Breaking change #1 — and it's 66.0, not 67.0:** invocable input classes need a visible no-arg constructor (public, or global if packaged). Summer '26 is the *enforcement* date, not the start.
- **67.0 defaults:** SOQL/DML in user mode; keyword-less classes are `with sharing`; `WITH SECURITY_ENFORCED` **won't compile**.
- Old classes keep old behaviour until **recompiled at 67.0** — the risk arrives on an unrelated version bump.
- **Triggers always run in system mode** now and can't declare sharing — so don't put security-sensitive logic there.

## Minimal example

```apex
public with sharing class RefundAction {          // 67.0: 'with sharing' is the default anyway
    public class Input {
        public Input() {}                          // REQUIRED from 66.0 — visible no-arg constructor
        @InvocableVariable(label='Order ID'
            description='18-char ID of a Delivered Order to refund.')
        public Id orderId;
    }
    @InvocableMethod(label='Issue Refund'
        description='Refunds a Delivered order. Do NOT use for exchanges or partial credits.')
    public static void run(List<Input> inputs) {
        List<Order> o = [SELECT Id FROM Order WHERE Id = :inputs[0].orderId];  // user mode
    }
}
```
