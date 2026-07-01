# Shared Conventions — spec 0.1

Normative for all files in the family. The key words MUST, MUST NOT, SHOULD, and MAY are to be interpreted as described in RFC 2119.

## 1. Bundle layout

A **governance bundle** is a directory named `.gaas/` at the root of the governed project, containing one or more of:

| File | Required | Purpose |
| --- | --- | --- |
| `auth.md` | no | agent identities & authority boundaries |
| `policy.md` | no | operating rules |
| `audit.md` | no | record expectations |
| `escalation.md` | no | human-escalation routes |
| `attestation.sig` | no | detached signature over the other files |

A bundle with any one file is valid. Adopting `policy.md` alone is a supported on-ramp.

## 2. File format

Every `.md` file in the bundle MUST be UTF-8 text consisting of:

1. A single YAML frontmatter block delimited by `---` lines, starting at byte 0.
2. An optional Markdown body after the closing delimiter.

The frontmatter is the **machine contract**: it MUST validate against the corresponding JSON Schema in `schemas/`. The body is **human rationale**: implementations MUST include it when hashing the file (§5) and MUST NOT interpret it.

### 2.1 Required frontmatter keys (every file)

```yaml
gaas_spec: "0.1"     # spec version this file targets (string, exactly "0.1")
org: acme            # org slug — lowercase, [a-z0-9_-], 1–64 chars
```

Implementations MUST reject a file whose `gaas_spec` major.minor they do not implement. Unknown **top-level** frontmatter keys MUST be rejected (strict mode keeps the contract honest); unknown keys nested inside `x_` extensions (§6) are permitted.

## 3. Field paths

Conditions and constraints reference intent data by **dotted field path** into the governed intent's canonical namespace:

```
agent.id                    agent.trust_tier
action.type                 action.verb
action.target.type          action.target.identifier      action.target.sensitivity
action.payload.summary
action.payload.estimated_impact.reversible
action.payload.estimated_impact.financial_exposure_usd
action.payload.estimated_impact.audience_size
action.payload.estimated_impact.data_categories
action.payload.estimated_impact.regulatory_domains
context.session_id          context.conversation_id
enrichment.contradiction_count
enrichment.context_confidence
```

The full whitelist is `schemas/fieldpaths-0.1.json`. Implementations MUST reject paths not on the whitelist — arbitrary attribute traversal is forbidden by design. Runtimes MAY expose additional paths under `x_` (§6), which portable bundles SHOULD avoid.

## 4. The matcher grammar (`when`)

Conditions are **declarative, never code**. A `when` clause is a matcher tree:

```yaml
when:
  all:                      # AND — every child must match
    - { field: action.type, op: eq, value: communicate }
    - any:                  # OR — at least one child must match
        - { field: action.target.sensitivity, op: eq, value: regulated }
        - { field: action.payload.estimated_impact.financial_exposure_usd, op: gt, value: 5000 }
```

### 4.1 Leaf matchers

A leaf is `{ field, op, value }`:

| `op` | Applies to | Matches when |
| --- | --- | --- |
| `eq` / `ne` | any scalar | field equals / does not equal `value` |
| `gt` / `gte` / `lt` / `lte` | numbers | numeric comparison |
| `in` / `not_in` | scalar vs list `value` | field is / is not one of `value` |
| `contains` | string or list field | string field contains substring `value` (case-insensitive), or list field contains element `value` |
| `matches` | strings | field matches the RE2-compatible regular expression `value` |
| `exists` | any | field is present and non-null (`value` MUST be `true` or `false`) |

### 4.2 Composite matchers

`all: [...]` and `any: [...]` take one or more children (leaf or composite), nesting to a maximum depth of **8**. `not:` takes exactly one child and negates it.

### 4.3 Semantics

- A **missing field** fails every leaf op except `exists: false`. Absence never satisfies a comparison — the fail-safe direction is "absence of data = the rule does not silently pass".
- `matches` MUST be evaluated with a linear-time engine (RE2 class). Backreferences and lookaround are not part of 0.1.
- Numeric comparison against a non-numeric field value is a validation-time error where detectable, else a non-match at runtime.
- Matching is deterministic: the same intent and the same bundle always produce the same result. No clock access, no randomness, no I/O.

### 4.4 Why not an expression language

Strings of code — even sandboxed — make governance files a supply-chain risk, non-portable across runtimes, and unreviewable by non-programmers. The matcher tree covers the overwhelming majority of real rules; a string expression language can arrive in a later spec version without breaking 0.1 documents. Rules inexpressible in 0.1 SHOULD live in the runtime (as vetted, versioned policy) and be referenced from the body text.

## 5. Hashing & canonical form

The **file hash** is SHA-256 over the file's raw bytes (frontmatter + body, exactly as committed). The **manifest** maps filename → hash for every `.md` file present; `attestation.sig` signs the manifest (see SPEC-attestation.md). Line endings are significant — bundles SHOULD be committed with LF and a `.gitattributes` guard.

## 6. Extensions

Runtimes MAY define extension keys prefixed `x_` (e.g. `x_gaas_membrane`). Portable bundles SHOULD NOT rely on them; validators MUST ignore unknown `x_` keys and MUST NOT reject a bundle because of them.

## 7. Versioning

Spec versions are `major.minor`. Within a minor version, only additive, backward-compatible clarifications occur. Files declare the version they target; validators declare the versions they implement. See GOVERNANCE.md for the change process.
