# Permission Set Groups & Muting

> Area: 07-security-and-sharing · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 10

**Scope:** Composing permission sets into role-shaped bundles, and the one mechanism in the permission layer that subtracts. What you may grant at all is [02](02-licences-and-what-they-gate.md); automating the assignment is [05](05-user-access-policies-and-lifecycle.md).

## Core idea

Permission sets solve the profile-forking problem and immediately create a new one: a salesperson needs eleven of them, and assigning eleven things to every new hire is the same maintenance burden wearing a different hat. A **permission set group** is the fix — a named bundle that models a *persona* (`Sales_Manager`) composed of *capabilities* (`Convert_Leads`, `Manage_Forecasts`, `Export_Reports`). You assign the group; the platform recalculates the union. The genuinely interesting part is the **muting permission set**, which is the only construct in the entire permission layer that removes something. It does not remove it globally — it removes it *within that group*, so the same capability permission set can be reused elsewhere at full strength.

## How it works

- **A group's effective access is the union of its permission sets, minus anything muted.** Muting is scoped to the group and never touches the underlying permission set.
- **A muting permission set belongs to exactly one group.** It is created from the group itself, not from the Permission Sets list, which is why people fail to find it.
- **Muting cannot subtract below the profile.** If the profile grants `Export Reports`, muting it in a group changes nothing — the union still includes the profile. This is the commonest reason muting "doesn't work". → [03](03-profiles-and-the-permission-set-led-model.md)
- **Groups have a status.** After an edit they show *Updating* while the platform recalculates; access is not live until *Updated*. Deployments that assume immediacy race this.
- **A permission set can belong to many groups**, which is what makes capability-shaped sets worth the discipline. Design sets around one capability, groups around one job.
- **Session-based permission sets** activate only inside a session that met a condition — a specific auth method, a Flow, an IP range — and are assignable individually or through a group. They are the right tool for a standing privilege you do not want standing.
- **A group can carry a permission set licence requirement** through its members; the PSL still has to be assigned to the user separately. → [02](02-licences-and-what-they-gate.md)

## 2026 currency

Nothing in Summer '26 changes group or muting mechanics, but two things change how you use them. The **profile-permissions retirement was cancelled** ([03](03-profiles-and-the-permission-set-led-model.md)), so groups are now chosen on maintainability rather than deadline — which makes the "mute below the profile" limitation more important, not less, because inherited orgs will keep fat profiles for longer. And the **enhanced profile view's new indirect-change preview** has no equivalent here: permission dependencies still resolve silently inside a group, so a group can acquire a dependent permission nobody assigned. Audit groups by their *effective* view, not their member list. → [15](15-auditing-and-troubleshooting-access.md)

## Gotchas

- **Muting cannot go below the profile.** Mute all you like; the profile's grant survives the union. Fix the profile.
- **The muting permission set is created from inside the group.** It does not appear in the ordinary Permission Sets list and cannot be shared between groups.
- **A group in *Updating* status is not yet enforcing.** Automated tests and post-deployment smoke checks hit this and report a flaky permission bug.
- **Muting a permission does not mute its dependencies.** The dependent permission may still arrive via another member set, and the group's effective view is the only place that shows it.
- **Groups do not nest.** A group cannot contain another group; only permission sets.
- **Deleting a permission set that a group uses is blocked**, but removing it from the group silently changes every assignee's access with no warning.
- **Session-based permission sets are invisible in a normal access review** — the user's summary shows the assignment, not whether the session ever activates it.

## Recall

Q: What is the only mechanism in the permission layer that subtracts access?
A: A muting permission set inside a permission set group — and it subtracts only within that group.

Q: Why does muting a permission sometimes have no effect?
A: Because the profile grants it too. Muting cannot reduce access below what the profile provides.

Q: Where do you create a muting permission set?
A: From inside the permission set group it belongs to. It is scoped to that one group and never appears in the general Permission Sets list.

Q: How should permission sets and groups be shaped?
A: Permission sets around a single capability, groups around a single job or persona — so sets stay reusable across groups.

Q: What does a group's *Updating* status mean for a deployment?
A: The union is still being recalculated and access is not yet live. Do not assert on permissions until it reads *Updated*.

## Related

- [03 · Profiles & the permission-set-led model](03-profiles-and-the-permission-set-led-model.md) — the floor that muting cannot go below
- [05 · User Access Policies & lifecycle](05-user-access-policies-and-lifecycle.md) — assigning groups automatically on joiner, mover and leaver events
- [15 · Auditing & troubleshooting access](15-auditing-and-troubleshooting-access.md) — reading a group's effective access rather than its member list
