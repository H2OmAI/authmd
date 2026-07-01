# Conformance Fixtures — spec 0.1

Ground truth for implementations. **Where the spec prose and these fixtures disagree, the fixtures win** (see GOVERNANCE.md).

- `valid/` — bundles a conforming validator MUST accept.
- `invalid/` — bundles a conforming validator MUST reject, with the reason code in [`expected.json`](expected.json).

Some invalid fixtures are rejectable by JSON Schema alone; others carry a `note` in `expected.json` marking them as **semantic checks** a validator must implement beyond schema validation (e.g. `missing-default-route`). A schema-only checker is not a conforming validator.

| Fixture | Expected | Reason code |
| --- | --- | --- |
| `valid/full-bundle` | accept | — |
| `valid/policy-only` | accept | — |
| `valid/when-always` | accept | — |
| `invalid/unknown-top-key` | reject | `unknown-frontmatter-key` |
| `invalid/bad-op` | reject | `unknown-operator` |
| `invalid/bad-field-path` | reject | `field-path-not-whitelisted` |
| `invalid/timeout-approve` | reject | `unsafe-timeout-action` |
| `invalid/missing-default-route` | reject | `missing-default-route` (semantic) |
| `invalid/record-partial` | reject | `partial-recording-forbidden` |
| `invalid/wrong-spec-version` | reject | `unsupported-spec-version` |
