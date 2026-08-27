# Platform Cache

> Area: 02-apex-and-triggers · Currency: **Summer '26 (API 67.0)** · Status: 🌱 learning · Phase: 20

**Scope:** The org and session caches an Apex transaction can read and write — capacity, TTL, `CacheBuilder`, and why a cache miss is the normal path. The limits cache exists to relieve are [01](01-apex-language-core-and-governor-limits.md) and [24](24-apex-performance-and-profiling.md).

## Core idea

Platform Cache is a tenant-scoped, in-memory key-value store that outlives the transaction that wrote it — the only such thing Apex has. Everything else is either per-transaction (a static variable, gone when the request ends) or durable and expensive (a record, costing a query to read and a DML to write). Cache sits between them: fast, shared across users, and **allowed to disappear at any moment**.

That last property is the whole design constraint, and it is the one people get wrong. **Cache is not storage.** Salesforce evicts keys by **least recently used** whenever a partition reaches capacity, so an entry can vanish long before its TTL expires, for reasons that have nothing to do with your code. A read returning `null` is therefore not an error — it is the ordinary case you must write for. Anything you cannot cheaply recompute does not belong here.

## How it works

| | Session cache | Org cache |
|---|---|---|
| Scope | one user's session | all users, all requests |
| Class | `Cache.Session` | `Cache.Org` |
| TTL range | 300 s – **28,800 s (8 h)** | 300 s – **172,800 s (48 h)** |
| Default TTL | 8 hours | **86,400 s (24 h)** |
| Local cache per request | 500 KB | 1,000 KB |
| Also ends when | the session ends — whichever comes first | TTL or eviction only |

- **Capacity is per org and smaller than people expect.** Enterprise **10 MB**; Unlimited and Performance **30 MB**; Developer **0** until you request a **10 MB** trial. **Professional Edition has none at all.** More is bought in **10 MB** blocks.
- **One cached item caps at 100 KB**, a key at **50 characters**, and the minimum partition is **1 MB**.
- **Partitions divide the org's capacity**, each splitting its allocation between org and session cache. Naming one explicitly (`local.MyPartition.myKey`) is what stops one feature evicting another's entries.
- **`Cache.CacheBuilder` handles the miss for you.** Implement `doLoad(String key)`; the platform calls it only when the value is absent, which removes the check-then-populate boilerplate everyone writes wrong once.
- **Cache writes are transactional.** If the transaction fails, every cache operation in it rolls back with the rest.

```apex
public class ConfigCache implements Cache.CacheBuilder {
    public Object doLoad(String key) {          // runs only on a miss
        return [SELECT DeveloperName, Threshold__c FROM App_Config__mdt
                WHERE DeveloperName = :key LIMIT 1];
    }
}
// call site — no null check, no populate branch
App_Config__mdt cfg = (App_Config__mdt) Cache.Org.get(ConfigCache.class, 'Billing');
```

## Gotchas

- **A miss is normal, not exceptional.** LRU eviction runs whenever a partition fills, so `get()` returns `null` at moments unrelated to TTL. Code treating a miss as an error fails in production and never in a quiet sandbox.
- **Cache enforces neither FLS nor sharing on the way out.** Whatever went in comes back to whoever asks. Cache the *computed answer*, not raw record data the next caller should not see. → [10](10-apex-security-user-mode-and-fls.md)
- **Session cache dies with the session even with TTL remaining.** Eight hours is a ceiling, not a promise.
- **Breaching the per-request local cache limit causes evictions mid-request** — unexpected misses and wasted serialization inside a single transaction.
- **100 KB per item is easy to exceed** with a serialized list of sObjects, and it fails on write.
- **Nothing tells you a partition is undersized.** The symptom is a hit rate quietly collapsing, invisible unless you instrument it.
- **Developer Edition has no cache until trial capacity is requested**, so a scratch org proves nothing about cache-dependent code by default.
- **Custom settings and custom metadata are already in an application cache** and do not cost a query. Reach for Platform Cache when the data is *not* config — a callout response, an expensive aggregate. → [01-admin · 09](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md)

## Recall

Q: Why must a cache miss be a normal code path rather than an error?
A: Platform Cache evicts by least recently used whenever a partition hits capacity, so an entry can disappear well before its TTL, independently of your code.

Q: What are the maximum TTLs for session and org cache?
A: Session **8 hours** (28,800 s), org **48 hours** (172,800 s). Org cache defaults to 24 hours; session cache also ends when the session does.

Q: What does `Cache.CacheBuilder` give you over `Cache.Org.get()`?
A: It detects the miss itself and calls your `doLoad(String key)` only when the value is absent, removing the check-then-populate branch.

Q: Which editions get Platform Cache, and how much?
A: Enterprise 10 MB, Unlimited and Performance 30 MB, Developer 0 (10 MB on trial request). Professional Edition has none. Extra capacity comes in 10 MB blocks.

Q: Does reading from Platform Cache apply field-level security?
A: No. Cached values are returned to any caller, which is why you cache a computed answer rather than raw record data.

## Related

- [24 · Apex performance & profiling](24-apex-performance-and-profiling.md) — the CPU and query pressure cache is meant to relieve
- [19 · Callouts, Named Credentials & HTTP](19-callouts-named-credentials-and-http-in-apex.md) — caching an access token is the canonical org-cache use
- [01-admin · 09 Custom metadata vs custom settings](../01-admin-and-declarative-platform/09-custom-metadata-vs-custom-settings.md) — config is already cached; this note is for what is not
- [08-data · 06 Storage model & schema limits](../08-data-modeling-and-large-data-volumes/06-storage-model-and-schema-limits.md) — the durable tiers, for anything that must survive
