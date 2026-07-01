---
gaas_spec: "0.1"
org: acme
routes:
  - id: high-value
    match:
      all:
        - { field: action.payload.estimated_impact.financial_exposure_usd, op: gt, value: 10000 }
    approvers:
      emails: [cfo@acme.com, governance@acme.com]
    timeout_minutes: 60
    on_timeout: escalate_up
    escalate_to: default
  - id: default
    approvers:
      emails: [governance@acme.com]
    webhook:
      url: https://hooks.acme.com/gaas-escalations
    timeout_minutes: 240
    on_timeout: block
---

Big-ticket items go to the CFO first; everything else to the governance
inbox. Nothing auto-approves on timeout.
