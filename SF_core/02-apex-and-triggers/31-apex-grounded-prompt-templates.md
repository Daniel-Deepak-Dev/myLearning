# Apex-Grounded Prompt Templates

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 23

**Scope:** `@InvocableMethod(capabilityType=…)` — Apex invoked *while a prompt is being resolved*, to supply grounding data. The invocable signature rules are [22](22-invocable-apex-and-agentforce-actions.md) and are not repeated here; template authoring and grounding strategy are [AI_Data/02-salesforce-ai/03-prompt-builder/notes.md](../../AI_Data/02-salesforce-ai/03-prompt-builder/notes.md).

## Core idea

**This is the same annotation as [22](22-invocable-apex-and-agentforce-actions.md) doing an entirely different job**, and that inversion is the whole note. In 22 the platform calls your method *as an action* — a unit of work an agent or Flow chose to run, whose return value is a result. Add a `capabilityType` parameter and the platform calls the same method *during prompt resolution* instead, before any model has seen anything, and the return value is not a result at all: it is a `String` spliced into the prompt wherever the template's Apex merge field sits. The method is not doing the work; it is deciding what the model gets told. Everything sharp about the pattern follows from that — you are authoring model input, in Apex, under the running user's permissions.

## How it works

| Template type | `capabilityType` string |
|---|---|
| Sales Email | `PromptTemplateType://einstein_gpt__salesEmail` |
| Field Generation | `PromptTemplateType://einstein_gpt__fieldCompletion` |
| Record Summary | `PromptTemplateType://einstein_gpt__recordSummary` |
| Flex | `FlexTemplate://<template_API_Name>` — **the template's API name, not a type name** |

- **The parameter must be `List<Request>`**, and the `Request` inner class declares one `@InvocableVariable` per input the template type offers — `sender`, `recipient`, `relatedObject` for a sales email. You do not name these freely; the template type dictates them.
- **The `Response` class must expose `@InvocableVariable public String Prompt`.** That field name *is* the contract, capital P included. Whatever string it holds becomes prompt text.
- **Apex is the escape hatch for what merge fields cannot express** — a SOQL result rendered as readable lines, a filtered or ranked subset, well-formed JSON, or data from a callout Prompt Builder cannot reach.

```apex
public with sharing class PropertyInterestGrounding {
    @InvocableMethod(capabilityType='PromptTemplateType://einstein_gpt__salesEmail')
    public static List<Response> ground(List<Request> requests) {
        Request req = requests[0];                        // resolution is single-record
        Response r = new Response();
        r.Prompt = summarise(req.recipient, req.relatedObject);  // becomes prompt TEXT
        return new List<Response>{ r };
    }
    public class Request {
        public Request() {}                               // 66.0 rule applies here too
        @InvocableVariable public Contact recipient;
        @InvocableVariable public Property__c relatedObject;
    }
    public class Response { @InvocableVariable public String Prompt; }
}
```

## 2026 currency

**The API 66.0 no-argument-constructor Release Update reaches grounding classes too, and almost nobody writes it up that way.** Every published example frames that rule as an *agent action* concern, but a grounding `Request` is an invocable parameter class like any other — the platform instantiates it, so adding a parameterised constructor breaks prompt resolution at runtime with no compile error → [22](22-invocable-apex-and-agentforce-actions.md). The second 67.0 consequence is quieter and worse: grounding Apex now runs in **user mode** by default, so a SOQL query that fed the model ten rows for an admin can feed it three for a support agent. The model does not know rows are missing and will answer confidently from the subset. → [10](10-apex-security-user-mode-and-fls.md)

## Gotchas

- **`Response.Prompt` is a naked `String`, which makes this an injection surface.** Any record data you concatenate — a Contact description, a case comment — is untrusted text becoming model instructions. The Trust Layer scans it, but layout and framing are yours. → [AI_Data · Einstein Trust Layer](../../AI_Data/02-salesforce-ai/04-einstein-trust-layer/notes.md)
- **`FlexTemplate://` takes the template API name**, so renaming the template in Prompt Builder breaks the Apex at runtime — a string dependency with no compiler protection, exactly like `Type.forName()` → [28](28-dependency-injection-and-pluggable-apex.md).
- **One `@InvocableMethod` per class still applies**, so grounding three templates means three outer classes — the rule from 22 does not relax because the capability changed.
- **Resolution is not bulk.** Unlike an action, prompt resolution hands you one request; writing a loop over `requests` is harmless but the bulk-alignment discipline from 22 has nothing to align.
- **Returning an empty or null `Prompt` does not fail loudly.** The merge field resolves to nothing and the model improvises around the hole — the classic grounding failure, and it reads as a hallucination.
- **A callout inside grounding puts an HTTP round trip on the prompt's critical path**, inside the user's wait for a generation that is already slow.
- **Debug logs are the only real visibility** into what you handed the model; the resolved prompt is not stored on the record.

## Recall

Q: What single change turns an ordinary invocable method into a prompt-grounding provider?
A: The `capabilityType` parameter on `@InvocableMethod` — the signature rules are otherwise identical to an action.

Q: What must the `Response` inner class expose, and why is the exact name load-bearing?
A: `@InvocableVariable public String Prompt`. The platform reads that field by name to get the text it splices into the template.

Q: How does a Flex template's `capabilityType` differ from the other three?
A: It is `FlexTemplate://<template_API_Name>` — bound to one specific template, where the others (`einstein_gpt__salesEmail`, `__fieldCompletion`, `__recordSummary`) name a template *type*.

Q: Why can the same grounding class produce a good answer for an admin and a wrong one for an agent at 67.0?
A: Grounding SOQL runs in user mode, so it silently returns fewer rows; the model answers confidently from the smaller set.

Q: What breaks if someone adds a constructor with arguments to the `Request` class?
A: Prompt resolution fails at runtime — the compiler-generated no-arg constructor disappears and the platform can no longer instantiate the class (API 66.0 rule).

## Related

- [22 · Invocable Apex & Agentforce actions](22-invocable-apex-and-agentforce-actions.md) — the same annotation as an action, and the signature rules this note assumes
- [32 · Invoking prompt templates from Apex](32-invoking-prompt-templates-from-apex.md) — the inverse direction: Apex as the caller rather than the data provider
- [10 · Apex security: user mode & FLS](10-apex-security-user-mode-and-fls.md) — why grounding queries can under-return at 67.0
- [AI_Data · Prompt Builder](../../AI_Data/02-salesforce-ai/03-prompt-builder/notes.md) — template types, merge fields and grounding strategy
