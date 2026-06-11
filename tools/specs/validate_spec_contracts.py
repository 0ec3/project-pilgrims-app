#!/usr/bin/env python3
"""Validate machine-readable Pilgrims spec contract files.

This script intentionally performs structural checks only. Product truth still lives in the
normative markdown specs, but these YAML files must remain parseable and internally sane
so implementation, QA, and release tooling can consume them safely.
"""

from __future__ import annotations

from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required. Install with: python -m pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[2]
CONTRACT_DIR = ROOT / "SPECS" / "CONTRACTS"
REQUIRED = [
    "entitlement_capability_policy.yaml",
    "group_presence_privacy_contract.yaml",
    "content_pack_trust_chain_contract.yaml",
    "advisory_source_registry.schema.yaml",
    "release_gate_taxonomy.yaml",
    "screen_feature_traceability.yaml",
]


def load_yaml(path: Path) -> dict:
    if not path.exists():
        raise AssertionError(f"Missing required contract file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError(f"Contract must parse as mapping: {path.relative_to(ROOT)}")
    if "version" not in data and "schema_version" not in data:
        raise AssertionError(f"Contract missing version/schema_version: {path.relative_to(ROOT)}")
    return data


def validate_entitlements(data: dict) -> None:
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, dict) or not capabilities:
        raise AssertionError("entitlement_capability_policy.yaml must define capabilities")

    for key, value in capabilities.items():
        if not isinstance(value, dict):
            raise AssertionError(f"Capability {key} must be a mapping")
        criticality = value.get("criticality")
        if criticality in {"correctness", "emergency"} and value.get("supporter_allowed") is False and value.get("supporter") is False:
            raise AssertionError(f"Critical capability cannot exclude Supporter access: {key}")
        if criticality in {"correctness", "emergency"} and value.get("never_gate") is not True:
            raise AssertionError(f"Critical capability must be never_gate=true: {key}")


def validate_group_presence(data: dict) -> None:
    text = yaml.safe_dump(data)
    forbidden_terms = ["background tracking", "passive surveillance"]
    # The contract may name forbidden behaviors, but it must also clearly carry freshness semantics.
    for required in ["fresh", "stale", "expired", "revoked"]:
        if required not in text.lower():
            raise AssertionError(f"group_presence_privacy_contract.yaml missing freshness term: {required}")


def validate_trust_chain(data: dict) -> None:
    text = yaml.safe_dump(data)
    for required in ["manifest_signature", "artifact_signature", "signing_key_id"]:
        if required not in text:
            raise AssertionError(f"content_pack_trust_chain_contract.yaml missing {required}")


def main() -> int:
    loaded = {name: load_yaml(CONTRACT_DIR / name) for name in REQUIRED}
    validate_entitlements(loaded["entitlement_capability_policy.yaml"])
    validate_group_presence(loaded["group_presence_privacy_contract.yaml"])
    validate_trust_chain(loaded["content_pack_trust_chain_contract.yaml"])
    print(f"Validated {len(loaded)} spec contract files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
