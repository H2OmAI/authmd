---
gaas_spec: "0.1"
org: acme
policies:
  - id: warn-everything-in-scope
    description: Warn on every delete action while we calibrate
    severity: advisory
    verdict: warn
    scope:
      action_types: [delete]
    when: always
---
Calibration guard.
