---
gaas_spec: "0.1"
org: acme
agents:
  - id: support-triage-bot
    name: Support Triage Bot
    framework: langchain
    trust_tier: standard
    delegation_limit_usd: 500
    allowed_action_types: [access, communicate]
    denied_action_types: [delete]
requires_human:
  - description: Any irreversible action over $1,000
    when:
      all:
        - { field: action.payload.estimated_impact.reversible, op: eq, value: false }
        - { field: action.payload.estimated_impact.financial_exposure_usd, op: gt, value: 1000 }
---

The triage bot reads tickets and drafts replies. It never deletes,
and big irreversible things are a human's call.
