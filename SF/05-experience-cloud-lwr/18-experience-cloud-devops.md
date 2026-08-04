# Experience Cloud DevOps ⚠️

> Area: 05-experience-cloud-lwr · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 19

**Scope:** Deploying and source-controlling a site in a pipeline — the metadata-type trap and the gotchas that break CI/CD. The bundle *distinction* is owned by [02](02-lwr-architecture-and-build-model.md); this note owns what it does to a pipeline. Rests on [09-devops · 05 Metadata API](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md).

> **What changed.** The old "deploy a community via **`SiteDotCom`**" advice is a source-control dead end — it ships a binary blob that regenerates differently on every retrieve, so diffs are meaningless. And the newer fix is subtler than tutorials admit: **`ExperienceBundle` does not identify the runtime** — Aura *and* non-enhanced LWR sites both use it. **Enhanced LWR sites (the default) use `DigitalExperienceBundle` + `DigitalExperienceConfig`** and are **not** retrievable under `ExperienceBundle` at all.

## Core idea

The metadata type behind a site is decided by its **template + runtime**, and the wrong choice fails silently. **`SiteDotCom`** is the legacy binary type — opaque, non-diffable, a dead end. **`ExperienceBundle`** is plain-text JSON, diffable, used by Aura and *non-enhanced* LWR — so seeing it tells you the site is diffable but **not** which runtime it is. **`DigitalExperienceBundle`** (with `DigitalExperienceConfig`) is what **enhanced** LWR sites use, and enhanced is the default for new sites. Practical rule: a modern site is a `DigitalExperienceBundle`, it is diffable, and it will not appear if your retrieve manifest only names `ExperienceBundle`.

## How it works

| Metadata type | Used by | Identifies runtime? | Source control |
|---|---|---|---|
| `SiteDotCom` | legacy / Aura origins | no | binary blob, non-diffable |
| `ExperienceBundle` | Aura **and** non-enhanced LWR | **no** | plain-text JSON, diffable |
| `DigitalExperienceBundle` + `DigitalExperienceConfig` | **enhanced LWR (default)** | yes | plain-text, diffable |

- **Retrieve by the right type.** `sf project retrieve` must name `DigitalExperienceBundle` for enhanced LWR — it is *not* found under `ExperienceBundle`.
- **Sites carry dependencies.** A deploy usually needs the Network/CustomSite, the guest profile/permission sets, CMS content and any custom LWC — a bundle alone often won't activate.
- **Publish is separate from deploy.** Deploying metadata updates the definition; the site must still be **published** for changes to reach visitors.

## 2026 currency

Enhanced sites being the default means `DigitalExperienceBundle` is the type you'll meet most, and the one stale tutorials get wrong by reaching for `ExperienceBundle` or `SiteDotCom`. Pipeline tooling (DevOps Center, Gearset-style tools) supports it — only if the manifest is right. Detail: [AI_Data/05-release-radar/README.md](../../AI_Data/05-release-radar/README.md).

## Gotchas

- **Wrong metadata type = silent no-op.** Naming `ExperienceBundle` for an enhanced LWR site retrieves and deploys nothing — no error, just an absent site.
- **`ExperienceBundle` ≠ a runtime signal.** Don't infer "LWR" from it; Aura sites use it too — check the site definition, [02](02-lwr-architecture-and-build-model.md).
- **`SiteDotCom` diffs are noise.** Every retrieve is a different blob; never gate a review on its diff.
- **Deploy ≠ publish.** Metadata can be live in the org while the site serves the last published build.
- **Guest profile is a dependency, not an afterthought** — omit it and the site deploys but guests see nothing, [07](07-guest-user-security-model.md).
- **Cross-org site/network IDs differ** — hard-coded references break between sandbox and prod; parameterize them.

## Recall

Q: Which metadata type does a modern (enhanced) LWR site use?
A: `DigitalExperienceBundle` (with `DigitalExperienceConfig`) — plain-text and diffable, and *not* retrievable under `ExperienceBundle`.

Q: Does `ExperienceBundle` tell you the site's runtime?
A: No — Aura and non-enhanced LWR sites both use it, so it identifies diffability, not the runtime.

Q: Why is `SiteDotCom` a source-control dead end?
A: It's a binary blob Salesforce regenerates differently on every retrieve, so diffs never show meaningful changes.

Q: What's the silent failure when your manifest names the wrong site metadata type?
A: The retrieve/deploy finds nothing for that site — no error, the site simply doesn't come across.

Q: Does deploying a site's metadata make changes visible to visitors?
A: No — the site must still be published; deploy updates the definition, publish serves it.

## Related

- [02 · LWR architecture & build model](02-lwr-architecture-and-build-model.md) — owns the LWR / enhanced-LWR / bundle-type distinction
- [09-devops · 05 Metadata API](../09-devops-sfdx-and-release-management/05-metadata-api-and-deployment-mechanics.md) — the retrieve/deploy mechanics this rides on
- [14 · Enhanced CMS & content delivery](14-enhanced-cms-and-content-delivery.md) — the content half of a site deploy
