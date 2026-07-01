---
gaas_spec: "0.1"
org: acme
policies:
  - id: no-bulk-customer-export
    description: Block bulk exports of customer records
    severity: mandatory
    verdict: block
    scope:
      action_types: [access]
    when:
      all:
        - { field: action.target.identifier, op: contains, value: customer }
        - { field: action.payload.estimated_impact.audience_size, op: gte, value: 1000 }
    suggest: Export a filtered subset under 1,000 records, or request operator sign-off.
  - id: escalate-regulated-comms
    description: Escalate outbound communication touching regulated data
    severity: critical
    verdict: escalate
    scope:
      action_types: [communicate]
    when:
      any:
        - { field: action.target.sensitivity, op: eq, value: regulated }
        - { field: action.payload.estimated_impact.regulatory_domains, op: contains, value: HIPAA }
---

## Why these rules exist

A single bulk export of the customer table ended up in a partner's Slack
in 2025. Never again. Regulated communications always get a human.
