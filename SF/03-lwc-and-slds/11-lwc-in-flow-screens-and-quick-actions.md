# LWC in Flow Screens & Quick Actions

> Area: 03-lwc-and-slds · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 06

**Scope:** The **component-authoring** contract for the two places a component is launched by something other than a Lightning page — a Flow screen and a record action. The Flow-designer side (building the flow, reactive screens, when to use a component at all) is [04-flow](../04-flow-and-automation/INDEX.md).

## Core idea

Both surfaces work the same way and it is worth seeing it once: the **`.js-meta.xml` file is the contract**, and the JavaScript only implements it. `targets` declares where the component may be placed; `targetConfigs` declares, per target, which `@api` properties the host may set and read. Everything awkward about these two hosts follows from one asymmetry — the host writes to your `@api` properties directly, but you cannot write back by assigning to them. Flow needs a `FlowAttributeChangeEvent`; a record action needs an event or a navigation. Assigning `this.myOutput = x` and expecting Flow to see it is the single most common failure here, and it fails quietly: the component is right, the flow variable is empty. The other thing to internalise is that a quick action comes in two shapes, and **headless** means the component renders nothing and exists only to have `invoke()` called.

## How it works

| Target | Host |
|---|---|
| `lightning__FlowScreen` | a screen flow, with `targetConfig` properties as inputs/outputs |
| `lightning__RecordAction` | a quick action — `<actionType>ScreenAction</actionType>` or `Action` (headless) |
| `lightning__RecordPage` / `AppPage` / `HomePage` | Lightning App Builder |
| `lightningCommunity__Page` / `Default` | Experience Builder — `Default` is required for a *property* editor |

- **`role` decides direction in Flow.** `<property name="total" type="Integer" role="outputOnly"/>` cannot be set by the flow; `inputOnly` cannot be read back; omitting `role` makes it both.
- **Writing back to Flow is an event.** `dispatchEvent(new FlowAttributeChangeEvent('total', value))` from `lightning/flowSupport` — the property name is a **string** and a typo is silent.
- **Flow navigation is also events.** `FlowNavigationNextEvent`, `FlowNavigationBackEvent`, `FlowNavigationFinishEvent` and `FlowNavigationPauseEvent`, all from `lightning/flowSupport`. `Next` only works if the screen allows it.
- **`@api validate()` gates the Next button.** Return `{ isValid: true }` or `{ isValid: false, errorMessage: '…' }`. It must carry `@api`, and it is called by the runtime — never by you.
- **Headless actions need an empty template and `@api invoke()`.** The runtime calls `invoke()` and renders nothing; a screen action instead renders in a modal and closes itself by dispatching `CloseActionScreenEvent` from `lightning/actions`.

```xml
<targetConfigs>
  <targetConfig targets="lightning__FlowScreen">
    <property name="accountId" type="String" role="inputOnly" label="Account"/>
    <property name="selectedIds" type="String" role="outputOnly" label="Selected"/>
  </targetConfig>
  <targetConfig targets="lightning__RecordAction" actionType="ScreenAction">
    <objects><object>Case</object></objects>          <!-- omit and it offers on everything -->
  </targetConfig>
</targetConfigs>
```

## 2026 currency

The component-authoring contract is stable; what has moved is how much of it you still need. **Reactive screen components** mean a flow can respond to a component's output *while the screen is open* rather than on Next, which removes a whole category of "wrap it in a component so the screen can react" work — that is a Flow-side capability and belongs to [04-flow](../04-flow-and-automation/INDEX.md), but it changes the *decision* to write one of these at all, so it is worth knowing before you start. The other 2026 note is that a headless quick action is now a common way to give an agent or a button a single scripted behaviour without a modal; where that behaviour should be an invocable Apex action instead, the comparison lives in [02-apex · 22](../02-apex-and-triggers/INDEX.md). → [AI_Data/05-release-radar/developer-tooling-and-apis.md](../../AI_Data/05-release-radar/developer-tooling-and-apis.md)

## Gotchas

- **Assigning to an `@api` property does not send it to Flow.** Without `FlowAttributeChangeEvent` the flow variable stays at its old value and nothing warns you.
- **The attribute name in `FlowAttributeChangeEvent` is an unchecked string.** Misspell it and the event dispatches successfully into nowhere.
- **`validate()` without `@api` is never called**, and the screen advances with invalid data.
- **A headless action that renders markup breaks.** The template must be empty; anything in it produces an unwanted flash of UI.
- **`CloseActionScreenEvent` only applies to screen actions.** In a headless action it does nothing.
- **Omitting `<objects>` on a `lightning__RecordAction` config offers the action on every object**, which is rarely what anyone wants.
- **A quick action still has to be added to the layout.** Deploying the component and its metadata is not enough — it must go into the Salesforce Mobile and Lightning Experience Actions section. → [01-admin](../01-admin-and-declarative-platform/INDEX.md)
- **`targetConfig` properties are design-time only.** They are set by an admin or a flow author, not at runtime by another component.

## Recall

Q: What actually declares where a component can be used and what the host can set?
A: The `.js-meta.xml` file — `targets` for placement, `targetConfigs` for the per-target property contract.

Q: How does a component return a value to a screen flow?
A: By dispatching `FlowAttributeChangeEvent(propertyName, value)` from `lightning/flowSupport`. Assigning to the `@api` property is not enough.

Q: What does `role="outputOnly"` mean?
A: The flow can read the property but cannot set it. `inputOnly` is the reverse; omitting `role` allows both.

Q: What are the two quick action shapes, and what does each require?
A: A screen action renders in a modal and closes with `CloseActionScreenEvent`; a headless action has an empty template and an `@api invoke()` method the runtime calls.

Q: How does a component block the flow's Next button?
A: An `@api validate()` method returning `{ isValid: false, errorMessage }`.

## Related

- [10 · Navigation & page references](10-navigation-and-page-references.md) — sending the user elsewhere once the action finishes
- [04-flow · screen flows](../04-flow-and-automation/INDEX.md) — the designer side, reactive screens, and whether a component is warranted
- [01 · Component model & lifecycle](01-component-model-and-lifecycle.md) — `.js-meta.xml`, `isExposed` and where `@api` values become readable
