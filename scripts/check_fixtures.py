#!/usr/bin/env python3
"""Check conformance fixtures against the spec schemas.

Primitive checker for this repo's CI: schema validation + the semantic
checks the spec requires beyond JSON Schema. The full reference validator
ships separately as `gaas-spec` (PyPI).

Exit 0 when every fixture behaves as fixtures/expected.json declares.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
SCHEMAS = {
    name: json.loads((REPO / "schemas" / f"{name.removesuffix('.md')}.schema.json").read_text())
    for name in ("auth.md", "policy.md", "audit.md", "escalation.md")
}


def frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.index("\n---", 4)
    return yaml.safe_load(text[4:end])


def semantic_errors(fname: str, data: dict) -> list[str]:
    """Semantic checks the spec requires beyond JSON Schema."""
    errors: list[str] = []
    if fname == "escalation.md":
        routes = {r["id"]: r for r in data.get("routes", [])}
        if "default" not in routes:
            errors.append("missing-default-route")
        # escalate_up chains must terminate in a block route, without cycles
        for rid, route in routes.items():
            seen, cur = set(), rid
            while True:
                if cur in seen:
                    errors.append(f"escalation-cycle:{rid}")
                    break
                seen.add(cur)
                r = routes.get(cur)
                if r is None:
                    errors.append(f"dangling-escalate-to:{cur}")
                    break
                if r["on_timeout"] == "block":
                    break
                cur = r.get("escalate_to")
    return errors


def check_bundle(bundle_dir: Path) -> list[str]:
    errors: list[str] = []
    for f in sorted((bundle_dir / ".gaas").glob("*.md")):
        try:
            data = frontmatter(f.read_text())
        except Exception as exc:
            errors.append(f"{f.name}: unparseable ({exc})")
            continue
        for err in Draft202012Validator(SCHEMAS[f.name]).iter_errors(data):
            errors.append(f"{f.name}: {err.message[:100]}")
        errors.extend(f"{f.name}: {e}" for e in semantic_errors(f.name, data))
    return errors


def main() -> int:
    expected = json.loads((REPO / "fixtures" / "expected.json").read_text())
    failures: list[str] = []
    for name, expect in expected.items():
        errors = check_bundle(REPO / "fixtures" / name)
        if expect["valid"] and errors:
            failures.append(f"{name}: expected VALID, got errors: {errors[:3]}")
        if not expect["valid"] and not errors:
            failures.append(f"{name}: expected INVALID ({expect.get('reason')}), but passed")
        print(f"{'OK  ' if not (expect['valid'] and errors or not expect['valid'] and not errors) else 'FAIL'} {name}")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print(" -", f)
        return 1
    print(f"\nAll {len(expected)} fixtures behave as declared.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
