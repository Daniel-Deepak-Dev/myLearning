# Mobile app, Notification Builder & Briefcase

> Area: 01-admin-and-declarative-platform · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 02

**Scope:** Configuring the Salesforce mobile app, sending custom notifications, and priming records for offline use. Mobile field composition is [05 · Dynamic Forms](05-dynamic-forms-and-lightning-app-builder.md); mobile action bars are [06](06-dynamic-actions-and-list-views.md).

## Core idea

Mobile is not a separate app to build — it is the same metadata rendered on a smaller form factor, with three admin surfaces of its own. **Navigation and branding** are org-level settings (the *Mobile Only* app supplies the nav menu; branding covers the loading screen and header). **Notification Builder** is how the platform pushes something a user did not go looking for. **Briefcase Builder** decides which records exist on the device when the network does not, which is the only part of mobile that is genuinely a data-modelling problem rather than a layout one.

## How it works

- **Navigation:** the **Mobile Only** app's navigation menu holds Lightning pages, Visualforce pages, Lightning components and productivity items. Ordering here is the mobile menu order.
- **Branding:** loading-page background colour, loading logo and header background colour. That is the extent of it — deeper skinning needs Mobile Publisher.
- **Compact layouts** decide the key fields shown in the mobile highlights area and in Lightning Experience hovers. Separate from page layouts, easy to forget.
- **Preview before shipping:** App Builder previews phone and tablet form factors, so form-factor visibility rules can be checked without a device.
- **Notification Builder** (Setup → Notification Builder) defines **custom notification types**; you then send one from a Flow *Send Custom Notification* action, from Apex via `Messaging.CustomNotification`, or through the invocable action API.

| Notification limit | Value |
|---|---|
| Custom notification types per org | **500** |
| Recipients per notification (after expanding groups/queues/teams) | **10,000** |
| Notification actions per org per hour | **10,000** — excess notifications are **lost**, not queued |
| Notifications retained for the tray | most recent **1 million** (trimmed when it hits 1.2 million) |

- **Push delivery is conditional.** It depends on the device's OS-level settings, the app's own settings, and the org's *Enable push notifications*. Without **full content push notifications**, only the notification title is delivered — the body stays inside the app.
- **Briefcase Builder** builds a briefcase of filtered records for offline priming, including custom objects and **related objects up to three levels deep**. The offline app primes from the briefcase; no briefcase, no offline records.

## 2026 currency

Dynamic Forms on Mobile is on by default in new orgs, so mobile record detail is now designed in App Builder rather than inherited from the layout — see [05](05-dynamic-forms-and-lightning-app-builder.md). Nothing else here shifted in Summer '26; treat mobile config as stable platform and spend the attention on Briefcase scoping instead.

## Gotchas

- **The 10,000-per-hour ceiling loses notifications silently.** A batch job or a record-triggered flow firing on a data load will blow through it and nobody is told; notifications resume next hour with the misses gone for good.
- Recipient counts are measured **after** expanding groups, queues and teams — "notify the Sales queue" can exceed 10,000 without anyone typing a big number. Split across multiple actions in the same flow.
- Custom notifications are not email. If the user's device suppresses push, the only trace is the in-app tray.
- **Compact layout ≠ page layout.** A field missing from the mobile highlights panel is a compact-layout fix.
- Briefcase filters run against real data volumes — a filter that looks small in a sandbox can prime an unusable amount on a device.
- Three levels of related objects is the ceiling; a fourth-level lookup a field references will simply be absent offline, which shows up as blank fields rather than an error.
- The *Mobile Only* navigation menu is separate from every Lightning app's nav — updating an app's tabs does not update mobile.
- Notification types are metadata but the **recipients are not**; deploying a type does not carry who receives it.

## Recall

Q: What are the three ways to send a custom notification?
A: The *Send Custom Notification* action in Flow, `Messaging.CustomNotification` in Apex, or the invocable action API.

Q: What happens when an org exceeds 10,000 notification actions in an hour?
A: Nothing more sends for that hour and the unsent notifications are lost; sending resumes in the next hour.

Q: How deep can a briefcase follow relationships, and what is a briefcase for?
A: Three levels of related objects; it defines which records are primed onto the device for offline use.

Q: A user sees a notification title but no body on their phone. Why?
A: Full content push notifications are not enabled, so only the title is pushed.

Q: Which layout controls the key fields in the mobile highlights area?
A: The compact layout, not the page layout.

## Related

- [05 · Dynamic Forms & Lightning App Builder](05-dynamic-forms-and-lightning-app-builder.md) — mobile record detail and form-factor visibility rules
- [06 · Dynamic Actions & list views](06-dynamic-actions-and-list-views.md) — the mobile action bar and the org switch that gates it
- [08-data · INDEX](../08-data-modeling-and-large-data-volumes/INDEX.md) — why briefcase filters are a data-volume decision
