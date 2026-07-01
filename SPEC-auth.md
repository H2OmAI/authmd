# SPEC — auth.md · spec 0.1

Declares **who or what may act**: the agents an org recognizes, their trust tiers, their delegation limits, and the actions that always require a human's yes. Frontmatter validates against [`schemas/auth.schema.json`](schemas/auth.schema.json).

## 1. Frontmatter

```yaml
gaas_spec: "0.1"
org: acme
agents:
  - id: support-triage-bot               # required — the agent id it declares at runtime
    name: Support Triage Bot             # optional — display name
    framework: langchain                 # optional — free-form hint (langchain, crewai, custom, …)
    trust_tier: standard                 # optional — untrusted | limited | standard | elevated
    delegation_limit_usd: 500            # optional — max financial exposure per action
    allowed_action_types: [access, communicate]   # optional — omitted = runtime default
    denied_action_types: [delete]        # optional — always wins over allowed
requires_human:
  - description: Any irreversible action over $1,000
    when:
      all:
        - { field: action.payload.estimated_impact.reversible, op: eq, value: false }
        - { field: action.payload.estimated_impact.financial_exposure_usd, op: gt, value: 1000 }
  - description: Anything touching regulated data categories
    when:
      any:
        - { field: action.payload.estimated_impact.data_categories, op: contains, value: PHI }
        - { field: action.payload.estimated_impact.data_categories, op: contains, value: PCI }
```

## 2. Field semantics

- **`agents[].id`** — matches the `agent.id` an intent declares at runtime. An intent from an agent id not listed here is subject to the runtime's default posture; `auth.md` narrows, it does not create identity. Identity *verification* (that the caller really is that agent) is the runtime's job — this file declares intent-level authority, not authentication.
- **`trust_tier`** — a floor/ceiling hint to the runtime's trust model: `untrusted` < `limited` < `standard` < `elevated`. A file MUST NOT raise an agent above the tier the runtime has independently established; it MAY lower it.
- **`delegation_limit_usd`** — compiles to a rule: financial exposure above the limit triggers `escalate`.
- **`allowed_action_types` / `denied_action_types`** — action-type allow/deny lists. `denied` always wins. Compiles to `block` rules for denied types and for types outside `allowed` when `allowed` is present.
- **`requires_human`** — matcher trees (conventions §4) that compile to `escalate` rules. Each entry MUST carry a `description`.

## 3. Compilation model (informative)

A runtime compiles `auth.md` into the same rule structure as `policy.md`: per-agent scope (`agent.id eq <id>`) plus the declared constraint. The two files differ in *audience* — `auth.md` answers "who may act, and up to what authority"; `policy.md` answers "what conduct is acceptable" — not in mechanism.

## 4. Interaction with the runtime

- Suspension/quarantine registries, behavioral anomaly detection, and session trust budgets live in the runtime and are not expressible here; `auth.md` cannot re-enable a suspended agent.
- Where both `auth.md` and `policy.md` produce a verdict for the same intent, normal severity/verdict resolution applies (SPEC-policy.md §3).

## 5. Limits

| Limit | Value |
| --- | --- |
| agents per file | 512 |
| requires_human entries | 64 |
