# Spec Governance

## Status

Spec **0.1 — final** (declared 2 July 2026, tag `v0.1.0`). The declaration criteria were: the reference implementation ([`gaas-spec`](https://pypi.org/project/gaas-spec/) 0.1.0) passes every conformance fixture, and at least one non-reference consumer exists (the standalone CLI and the [validate CI Action](validate/action.yml)). The reference runtime is [GaaS](https://gaas.is). Changes from here follow the process below; 0.1 documents remain valid for all of 0.x per the versioning rules.

## Change process

1. **Anyone** may open an issue or PR against the spec text, schemas, or fixtures.
2. Substantive changes (grammar, semantics, schema shape) require: a written rationale, updated fixtures demonstrating the change (valid and invalid cases), and no breakage of existing `fixtures/valid/` under the same minor version.
3. Editorial changes (typos, clarifications that don't alter conformance) merge freely.
4. Final decision rests with the maintainer (H2Om.AI) while the spec is pre-1.0 — a deliberately boring BDFL model, stated openly rather than performed as neutrality. If adoption broadens, governance graduates with it (editors group, then a lightweight WG).

## Versioning

- Versions are `major.minor` (`gaas_spec: "0.1"`).
- **Minor** versions are additive: every bundle valid under `X.Y` is valid under `X.Y+1`.
- **Breaking** changes require a new major version, a migration note, and fixtures for both versions maintained side by side.
- Validators declare which versions they implement and MUST reject files targeting versions they don't.

## Conformance

An implementation conforms if it accepts every bundle in `fixtures/valid/` and rejects every bundle in `fixtures/invalid/` with the documented reason code. Fixtures are the spec's ground truth; where prose and fixtures disagree, fixtures win and a spec erratum is filed.

## Licensing

Spec text: [CC BY 4.0](LICENSE). Schemas, fixtures, and any code in this repo: [Apache-2.0](LICENSE-CODE). Implementations owe nothing beyond attribution of the spec text.
