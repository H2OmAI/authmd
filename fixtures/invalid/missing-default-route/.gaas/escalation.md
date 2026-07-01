---
gaas_spec: "0.1"
org: acme
routes:
  - id: only-route
    match:
      all:
        - { field: action.type, op: eq, value: transact }
    approvers:
      emails: [governance@acme.com]
    timeout_minutes: 60
    on_timeout: block
---
