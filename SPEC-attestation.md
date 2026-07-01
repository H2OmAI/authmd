# SPEC — attestation.sig · spec 0.1

The **detached signature over the bundle**: portable, offline-verifiable proof of exactly which governance declarations were in force. Validates against [`schemas/attestation.schema.json`](schemas/attestation.schema.json).

Unlike its siblings, `attestation.sig` is **JSON, not Markdown** — it is written by tools, not people.

## 1. Format

```json
{
  "gaas_spec": "0.1",
  "org": "acme",
  "manifest": {
    "auth.md":       "sha256:9f2c…",
    "policy.md":     "sha256:1b7e…",
    "audit.md":      "sha256:44a0…",
    "escalation.md": "sha256:c3d9…"
  },
  "manifest_hash": "sha256:7a1f…",
  "algo": "ES256",
  "signatures": [
    {
      "key_id": "acme-governance-2026",
      "signer": "org",
      "sig": "base64url…",
      "signed_at": "2026-07-01T12:00:00Z"
    },
    {
      "key_id": "gaas-runtime-prod",
      "signer": "runtime",
      "sig": "base64url…",
      "signed_at": "2026-07-01T12:00:05Z"
    }
  ]
}
```

## 2. Semantics

- **`manifest`** — filename → `sha256:<hex>` of the file's raw bytes (conventions §5), for every `.md` bundle file present. Files present in the bundle but missing from the manifest (or vice versa) MUST fail verification.
- **`manifest_hash`** — SHA-256 over the manifest serialized as canonical JSON (RFC 8785 JCS). This is the signed payload.
- **`algo`** — `ES256` (ECDSA P-256 + SHA-256) is the only algorithm in 0.1.
- **`signatures[]`** — one or more detached signatures over `manifest_hash`. `signer` is `org` (the governed organization's key) or `runtime` (the enforcing runtime countersigning at apply time). Multiple signatures of either kind MAY appear (key rotation, multi-party).

## 3. Verification procedure

1. Recompute each file's SHA-256; compare to `manifest`. Any mismatch → **invalid**.
2. Recompute `manifest_hash` over the canonical-JSON manifest; compare. Mismatch → **invalid**.
3. For each signature, verify `sig` over `manifest_hash` with the public key identified by `key_id`. At least one valid signature → **verified (by that signer)**; report each signature's status individually.

Verification requires no network and no runtime account. Public keys travel out of band (the runtime's key-registration flow, a well-known URL, or the org's own key distribution).

## 4. Relationship to the runtime

A runtime that applies a bundle SHOULD countersign it (`signer: runtime`) and SHOULD record the `manifest_hash` in its tamper-evident audit chain, binding "what the rules said" to "what decisions were made" — the applied-bundle hash appearing in the audit record is what turns these files from documentation into evidence.

Where an org's signing posture is *segregated* or *cosigned* (see SPEC-audit.md), the runtime MUST require a valid `org` signature before applying a bundle. In *provider_only* posture the org signature is optional and the runtime signs at apply time.
