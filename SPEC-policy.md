# SPEC — policy.md · spec 0.1

Declares the rules an agent operates under. Frontmatter validates against [`schemas/policy.schema.json`](schemas/policy.schema.json); shared conventions (file format, field paths, matcher grammar) are in [SPEC-conventions.md](SPEC-conventions.md).

## 1. Frontmatter

```yaml
gaas_spec: "0.1"
org: acme
policies:
  - id: no-bulk-customer-export          # required — [a-z0-9-], unique in file
    description: >-                       # required — one plain-English sentence
      Block bulk exports of customer records
    severity: mandatory                   # required — advisory | mandatory | critical
    verdict: block                        # required — warn | approve_modified | escalate | block
    scope:                                # optional — empty/omitted = universal
      action_types: [access, transact]    #   OR within a dimension,
      target_types: [record]              #   AND across dimensions
      sensitivities: [confidential, regulated]
    when:                                 # required — matcher tree (conventions §4)
      all:
        - { field: action.target.identifier, op: contains, value: customer }
        - { field: action.payload.estimated_impact.audience_size, op: gte, value: 1000 }
    suggest: >-                           # optional — remediation shown on trigger
      Export a filtered subset under 1,000 records, or request operator sign-off.
```

## 2. Field semantics

- **`id`** — stable identifier; renaming is a breaking change to the bundle's history. 1–64 chars of `[a-z0-9-]`.
- **`description`** — what a reviewer reads in a diff. MUST be non-empty.
- **`severity`**
  - `advisory` — informational; a triggered advisory rule SHOULD downgrade to a warning.
  - `mandatory` — a triggered rule applies its verdict.
  - `critical` — a triggered rule applies its verdict and runtimes SHOULD treat it as non-overridable within the org.
- **`verdict`** — what happens when `when` matches: `warn`, `approve_modified` (approve with the suggested modification), `escalate` (stop and ask a human), `block`.
- **`scope`** — index-style pre-filter. Dimensions: `action_types`, `target_types`, `sensitivities`, `data_categories`, `regulatory_domains`, `trust_tiers`. Empty list or omitted dimension = matches all. Values within a dimension OR together; dimensions AND together.
- **`when`** — the matcher tree. `when: always` is permitted as shorthand for a rule that triggers on everything in scope.
- **`suggest`** — remediation text surfaced to the agent/operator when the rule triggers.

## 3. Evaluation model

1. A rule is **applicable** to an intent when every scope dimension matches.
2. An applicable rule **triggers** when its `when` tree matches.
3. Multiple triggered rules resolve by severity then verdict strength (`block` > `escalate` > `approve_modified` > `warn`); the runtime's own tier system MAY sit above org rules.
4. Org rules declared in `policy.md` MUST only ever apply to intents belonging to `org` — a bundle can never affect another tenant.
5. Rules MUST NOT weaken the runtime's universal floor: a bundle cannot approve what the runtime's own critical policies block. Files add constraints; they do not subtract them.

## 4. Limits

| Limit | Value |
| --- | --- |
| policies per file | 256 |
| matcher tree depth | 8 |
| leaves per tree | 64 |
| `matches` pattern length | 512 chars |

## 5. Portability note

A conforming validator checks structure, whitelisted field paths, and matcher well-formedness. Whether a given verdict is *enforced* (blocked before execution) or *advisory* (recorded and reported) is a property of the runtime and its deployment mode — see the reference runtime's documentation. The file's meaning is identical either way.
