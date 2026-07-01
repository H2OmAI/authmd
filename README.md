# auth.md — Governance You Can Read

**An open convention for declaring how an AI agent is governed: in files, in your repo, readable by people and enforced by machines.**

Spec version: **0.1-draft** · Status: **public draft, comments welcome** · License: [CC BY 4.0](LICENSE) (text), [Apache-2.0](LICENSE-CODE) (schemas & fixtures)

---

## The idea

The agent ecosystem already standardized on plain-text convention files: `agents.md` for instructions, `llms.txt` for guidance, `SKILL.md` for skills, MCP for tools. There is no agreed file for **governance** — who an agent may act as, what it may do, what must be recorded, and when it must stop and ask a human.

This convention fills that gap with a `.gaas/` directory at the governed project's root:

```
.gaas/
├── auth.md          # who or what the agent may act as
├── policy.md        # the rules it operates under
├── audit.md         # what must be recorded, and for how long
├── escalation.md    # when the agent stops and asks a person
└── attestation.sig  # detached signature over all of the above
```

Each `.md` file is **YAML frontmatter + Markdown body**:

- The **frontmatter** is the machine contract — validated against the JSON Schemas in [`schemas/`](schemas/).
- The **body** is the human rationale — included in the signed hash, never machine-interpreted.

Governance you can diff in a pull request, sign like a release, and enforce at runtime.

## A taste

```markdown
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
---

## Why this rule exists

A single bulk export of the customer table ended up in a partner's
Slack in 2025. Never again. Anything touching customer records at
scale gets blocked and a human decides.
```

**Conditions are declarative, never code.** A governance file that can execute arbitrary code is a supply-chain attack surface, not a governance layer. The v0.1 grammar is a structured matcher tree (`all`/`any` over `{field, op, value}` triples) — see [SPEC-policy.md](SPEC-policy.md).

## The spec

| Document | Declares |
| --- | --- |
| [SPEC-conventions.md](SPEC-conventions.md) | Shared file format: frontmatter, versioning, field paths, the matcher grammar |
| [SPEC-auth.md](SPEC-auth.md) | Agent identities, trust tiers, delegation limits, actions requiring a human's yes |
| [SPEC-policy.md](SPEC-policy.md) | Rules: scope, severity, verdict, declarative conditions |
| [SPEC-audit.md](SPEC-audit.md) | Record expectations: retention, signing mode, export cadence |
| [SPEC-escalation.md](SPEC-escalation.md) | Escalation routes: approvers, channels, timeouts |
| [SPEC-attestation.md](SPEC-attestation.md) | `attestation.sig`: the detached, signed manifest of the bundle |

## Conformance

[`fixtures/`](fixtures/) contains valid and invalid example bundles. An implementation conforms to spec 0.1 if it accepts every bundle in `fixtures/valid/` and rejects every bundle in `fixtures/invalid/` for the documented reason. Implementations are encouraged to run the fixtures in CI.

## Reference runtime

[GaaS](https://gaas.is) (Governance as a Service) is the reference runtime: it validates these files, compiles them into enforced runtime policy, countersigns applied bundles, and anchors the applied-bundle hash in a tamper-evident audit chain. The audit record itself is [free forever](PLEDGE.md).

The reference validator ships as `gaas-spec` on PyPI with a CLI (`gaas validate`, `gaas sign`, `gaas verify`) and a GitHub Action — no API key, no network, validation runs entirely local.

## Status & governance

This is a **0.1 draft**. The change process, versioning rules, and how to propose amendments are in [GOVERNANCE.md](GOVERNANCE.md). Issues and PRs are open to everyone; breaking changes only land in a new minor version with fixtures for both.
