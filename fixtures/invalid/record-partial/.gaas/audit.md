---
gaas_spec: "0.1"
org: acme
record:
  every_decision: false
  include_shadow: true
retention:
  minimum_days: 365
  export_before_expiry: true
signing:
  mode: provider_only
export:
  cadence: monthly
  destination_hint: s3-worm
---

We keep a year, export monthly to WORM storage, and let the runtime sign.
