# SPEC — audit.md · spec 0.1

Declares the org's **record expectations**: what must be recorded, how long it is kept, how it is signed, and how it leaves the system. Frontmatter validates against [`schemas/audit.schema.json`](schemas/audit.schema.json).

`audit.md` is a **declaration the runtime validates against its actual configuration** — it does not configure the runtime. If the runtime's reality drifts from the declaration (e.g. the file declares co-signing but the org's signing mode is provider-only), a conforming runtime MUST surface the drift rather than silently proceed. Declared expectations the runtime cannot check are reported as unverifiable.

## 1. Frontmatter

```yaml
gaas_spec: "0.1"
org: acme
record:
  every_decision: true            # required to be true in 0.1 — partial recording is not a thing
  include_shadow: true            # optional, default true — shadow/would-be decisions recorded too
retention:
  minimum_days: 365               # declared minimum the org commits to
  export_before_expiry: true      # org's own promise to export before window closes
signing:
  mode: cosigned                  # provider_only | segregated | cosigned
  org_public_key: |               # required for segregated/cosigned — PEM, P-256
    -----BEGIN PUBLIC KEY-----
    ...
    -----END PUBLIC KEY-----
export:
  cadence: monthly                # none | monthly | quarterly — org's own export rhythm
  destination_hint: s3-worm       # free-form; informative only
```

## 2. Field semantics

- **`record.every_decision`** — MUST be `true`. The convention exists because partial records are worthless; a future version may define scoped exceptions, 0.1 does not.
- **`retention.minimum_days`** — the org's declared floor. The runtime compares this against the org's actual plan/config retention: actual ≥ declared passes; actual < declared is drift and MUST be surfaced.
- **`signing.mode`** —
  - `provider_only`: the runtime's key signs records.
  - `segregated`: only the org's key signs (the provider never holds it).
  - `cosigned`: both. For `segregated`/`cosigned`, `org_public_key` is required and MUST match the key registered with the runtime; mismatch is drift.
- **`export.cadence`** — the org's own operational promise; runtimes MAY check the last export timestamp against it and report drift, and MUST NOT block anything because of it.

## 3. What this file is not

It is not a retention configuration API, not a billing selector, and not a substitute for the runtime's immutability guarantees (hash chains, signatures, anchoring), which apply regardless of what this file says. Its value is that the org's *stated* record posture is versioned, signed, reviewable — and checkable against reality.
