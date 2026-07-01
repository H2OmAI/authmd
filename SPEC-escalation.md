# SPEC — escalation.md · spec 0.1

Declares **where escalations go and what happens when nobody answers**. Frontmatter validates against [`schemas/escalation.schema.json`](schemas/escalation.schema.json).

Escalation *triggers* live in `auth.md` (`requires_human`) and `policy.md` (`verdict: escalate`); this file declares the **routes**.

## 1. Frontmatter

```yaml
gaas_spec: "0.1"
org: acme
routes:
  - id: default                          # required — [a-z0-9-]; "default" route is required
    approvers:                           # at least one channel required per route
      emails: [governance@acme.com]
    webhook:                             # optional — HMAC-signed POST per escalation
      url: https://hooks.acme.com/gaas-escalations
    timeout_minutes: 240                 # required — 5..10080
    on_timeout: block                    # required — block | escalate_up
    escalate_to: null                    # route id, required when on_timeout: escalate_up
  - id: high-value
    match:                               # optional — matcher tree selecting this route
      all:
        - { field: action.payload.estimated_impact.financial_exposure_usd, op: gt, value: 10000 }
    approvers:
      emails: [cfo@acme.com, governance@acme.com]
    timeout_minutes: 60
    on_timeout: escalate_up
    escalate_to: default
```

## 2. Field semantics

- **`routes[].id`** — a route named `default` MUST exist; it handles any escalation no other route matches.
- **`match`** — matcher tree (conventions §4) selecting the route. Routes are evaluated in file order; first match wins; `default` needs no `match`.
- **`approvers.emails`** — people who can decide. Runtimes MAY additionally support their own channel types via `x_` extensions (e.g. Slack, Teams, ServiceNow) — email is the portable baseline in 0.1.
- **`webhook.url`** — MUST be HTTPS. Runtimes MUST apply SSRF protections (no private, loopback, link-local, or metadata addresses; no redirects) and SHOULD sign deliveries (HMAC) with a key exchanged out of band.
- **`timeout_minutes` / `on_timeout`** — what happens when no human decides in time: `block` (fail-safe deny) or `escalate_up` to `escalate_to`. Timeout chains MUST terminate in a route whose `on_timeout` is `block` — validators MUST reject cycles.

## 3. Fail-safe rule

There is no `on_timeout: approve`. An unanswered escalation never becomes a yes. This is deliberate and non-negotiable in 0.1.

## 4. Limits

| Limit | Value |
| --- | --- |
| routes per file | 32 |
| emails per route | 16 |
| escalate_up chain length | 4 |
