#!/usr/bin/env python3
"""Validate machine-readable Pilgrims spec contract files."""

from __future__ import annotations

from pathlib import Path
import re

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install with: python -m pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[2]
SPEC_DIR = ROOT / "SPECS"
CONTRACT_DIR = SPEC_DIR / "CONTRACTS"
SCREEN_SPEC = SPEC_DIR / "11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md"

EXPECTED_NORMATIVE_SPECS = [
    "01_README_AND_MASTER_INDEX.md",
    "02_AI_AGENT_RULES_AND_WORKFLOW.md",
    "03_PRODUCT_CHARTER_AND_SCOPE.md",
    "04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md",
    "05_ROADMAP_PROGRESS_AND_CHANGELOG.md",
    "06_SYSTEM_ARCHITECTURE.md",
    "07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md",
    "08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md",
    "09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md",
    "10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md",
    "11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md",
    "12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md",
    "13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md",
    "14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md",
    "15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md",
    "16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md",
    "17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md",
    "18_FEATURE_RITUALS_RIC_AND_RELIGIOUS_CONTENT.md",
    "19_FEATURE_MAPS_SAVE_MY_GATE_AND_3_D_WAYFINDING.md",
    "20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md",
    "21_FEATURE_PLANNER_REMINDERS_WALLET_NOTES_AND_BOOKMARKS.md",
    "22_FEATURE_PHRASEBOOK_EMERGENCY_SAFETY_AND_ASSISTIVE_TOOLS.md",
    "23_FEATURE_OFFLINE_PACKS_AUDIO_AND_CONTENT_DISTRIBUTION.md",
    "24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md",
    "25_FEATURE_ONBOARDING_HOME_AND_SIMPLE_MODE.md",
    "26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md",
    "27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md",
    "28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md",
    "29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md",
    "30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md",
    "31_QUALITY_FIRST_HARDENING_AMENDMENTS.md",
    "32_FEATURE_GUIDE_MARKETPLACE_MUTAWEF_DISCOVERY_AND_TRUST.md",
]

OLD_FILE_09 = "09_PLATFORM_SPEC_IOS_LIQUID_GLASS_ANDROID_ADAPTATION_AND_NATIVE_BRIDGES.md"
FORBIDDEN_ACTIVE_DESIGN_TERMS = (
    "liquid glass",
    "effect.glass",
    "surfaceglass",
    "glass card",
    "glass-heavy",
    "glass-like",
    "dark theme if supported",
    "light/dark modes if used",
)

REQUIRED = [
    "entitlement_capability_policy.yaml",
    "group_presence_privacy_contract.yaml",
    "content_pack_trust_chain_contract.yaml",
    "advisory_source_registry.schema.yaml",
    "release_gate_taxonomy.yaml",
    "screen_feature_traceability.yaml",
    "guide_marketplace_trust_contract.yaml",
]

BASELINE_SCREEN_IDS = {
    "startup_resolver", "onboarding_welcome", "language_preferences_setup", "account_gate",
    "home_root", "rituals_root", "start_resume_ritual", "ritual_session_overview",
    "ritual_step_detail", "ric_entry", "ric_result", "ritual_bookmarks_saved_guidance",
    "map_root", "destination_search_picker", "route_preview", "active_wayfinding",
    "save_anchor_flow", "saved_anchor_detail", "floor_level_selector", "group_root",
    "group_creation_flow", "join_group_flow", "group_live_board", "checkin_quick_flow",
    "regroup_pin_detail", "group_itinerary", "tools_root", "planner_list",
    "planner_item_editor", "reminder_editor", "wallet_list", "wallet_item_detail",
    "notes_list", "note_editor", "bookmarks_list", "phrasebook_root", "emergency_root",
    "emergency_card_detail", "pack_catalog", "pack_detail_install_flow", "settings_root",
    "privacy_data_flow", "simple_home", "simple_ritual_shortcut", "simple_map_shortcut",
    "simple_group_shortcut", "simple_emergency_shortcut",
    "guide_marketplace_root", "guide_profile_detail", "guide_registration_flow",
    "guide_verification_status", "guide_listing_editor",
}

MUST_STAY_FREE = {"correctness", "emergency", "emergency_assistive", "recovery", "offline_recovery"}


def fail(message: str) -> None:
    raise AssertionError(message)


def load_yaml(path: Path) -> dict:
    if not path.exists():
        fail(f"Missing required contract file: {path.relative_to(ROOT)}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"Contract must parse as mapping: {path.relative_to(ROOT)}")
    if "version" not in data and "schema_version" not in data:
        fail(f"Contract missing version/schema_version: {path.relative_to(ROOT)}")
    return data


def mapping(data: dict, key: str, source: str) -> dict:
    value = data.get(key)
    if not isinstance(value, dict) or not value:
        fail(f"{source} must define non-empty mapping: {key}")
    return value


def validate_repository_spec_references() -> None:
    expected_paths = [SPEC_DIR / name for name in EXPECTED_NORMATIVE_SPECS]
    for path in expected_paths:
        if not path.exists():
            fail(f"Missing normative spec: {path.relative_to(ROOT)}")

    old_path = SPEC_DIR / OLD_FILE_09
    if old_path.exists():
        fail(f"Superseded file 09 still exists: {old_path.relative_to(ROOT)}")

    scan_paths = [ROOT / "README.md", *expected_paths]
    legacy_filename_pattern = re.compile(r"`(?:SPECS/)?\d{2}-[A-Z0-9][A-Z0-9_-]*\.md`")

    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        if OLD_FILE_09 in text:
            fail(f"Stale old file 09 reference in {path.relative_to(ROOT)}")
        legacy_match = legacy_filename_pattern.search(text)
        if legacy_match:
            fail(
                f"Stale hyphenated spec filename reference in {path.relative_to(ROOT)}: "
                f"{legacy_match.group(0)}"
            )

        # D-004 and changelog history may retain the phrase Liquid Glass only in files 04 and 05.
        allow_historical_liquid_glass = path.name in {
            "04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md",
            "05_ROADMAP_PROGRESS_AND_CHANGELOG.md",
        }
        lower = text.lower()
        for term in FORBIDDEN_ACTIVE_DESIGN_TERMS:
            if term == "liquid glass" and allow_historical_liquid_glass:
                continue
            if term in lower:
                fail(
                    f"Active superseded design terminology in {path.relative_to(ROOT)}: {term}"
                )


def validate_entitlements(data: dict) -> None:
    capabilities = mapping(data, "capabilities", "entitlement_capability_policy.yaml")
    for key, value in capabilities.items():
        if not isinstance(value, dict):
            fail(f"Capability {key} must be a mapping")
        for field in ("criticality", "guest_allowed", "free_allowed", "supporter_allowed"):
            if field not in value:
                fail(f"Capability {key} missing required field: {field}")
        if value.get("criticality") in MUST_STAY_FREE:
            if value.get("never_gate") is not True:
                fail(f"Baseline capability must be never_gate=true: {key}")
            if value.get("free_allowed") is not True or value.get("supporter_allowed") is not True:
                fail(f"Baseline capability must allow free and supporter access: {key}")
        paid_only = value.get("free_allowed") is False and value.get("supporter_allowed") is True
        if paid_only and not value.get("entitlement_key"):
            fail(f"Paid-only capability must define entitlement_key: {key}")
        if value.get("auth_required") is True:
            if "server_trust_required" not in value:
                fail(f"Auth-required capability must state server_trust_required: {key}")
            if value.get("server_trust_required") is True and "network_required" not in value:
                fail(f"Server-trusted capability must state network_required: {key}")
        if value.get("local_only") is True and value.get("server_trust_required") is True:
            fail(f"Local-only capability cannot require server trust: {key}")

    required = {
        "ritual.guidance.text", "ritual.ric.basic", "maps.save_my_gate",
        "group.create_basic", "group.join_and_manual_coordination", "group.safe_checkin_manual",
        "phrasebook.text_and_big_text_cards", "emergency.cards_and_safety_basics",
        "medical_profile.local_basic", "packs.manual_download_and_verify",
    }
    missing = sorted(required - set(capabilities))
    if missing:
        fail(f"Missing baseline capabilities: {', '.join(missing)}")


def validate_group_presence(data: dict) -> None:
    text = yaml.safe_dump(data).lower()
    for term in ("fresh", "stale", "expired", "revoked"):
        if term not in text:
            fail(f"group_presence_privacy_contract.yaml missing freshness term: {term}")
    object_mappings = mapping(data, "object_mappings", "group_presence_privacy_contract.yaml")
    if object_mappings.get("database_primary_key") != "id":
        fail("Group presence database_primary_key must be id")
    if object_mappings.get("api_identifier") != "event_id":
        fail("Group presence api_identifier must be event_id")
    objects = mapping(data, "objects", "group_presence_privacy_contract.yaml")
    event = mapping(objects, "group_presence_event", "group_presence_privacy_contract.yaml")
    required_fields = mapping(event, "required_fields", "group_presence_event")
    for field in ("event_id", "group_id", "actor_user_id", "event_type", "shared_at", "ttl_expires_at", "freshness_status", "share_reason"):
        if field not in required_fields:
            fail(f"group_presence_event missing required field: {field}")
    conditional = mapping(event, "conditional_fields", "group_presence_event")
    text_pin = mapping(conditional, "text_pin", "group_presence_event.conditional_fields")
    if "regroup_pin" not in text_pin.get("required_for", []):
        fail("text_pin must be required for regroup_pin")


def validate_trust_chain(data: dict) -> None:
    text = yaml.safe_dump(data).lower()
    for term in ("manifest_signature", "artifact_signature", "signing_key_id", "anti-rollback", "last-known-good", "activation"):
        if term not in text:
            fail(f"content_pack_trust_chain_contract.yaml missing term: {term}")


def validate_advisory_source_registry(data: dict) -> None:
    text = yaml.safe_dump(data).lower()
    for term in ("source_type", "jurisdiction", "review_status", "last_verified_at"):
        if term not in text:
            fail(f"advisory_source_registry.schema.yaml missing term: {term}")


def validate_release_gate_taxonomy(data: dict) -> None:
    text = yaml.safe_dump(data)
    for rc in ("RC0", "RC1", "RC2", "RC3", "RC4"):
        if rc not in text:
            fail(f"release_gate_taxonomy.yaml missing release class: {rc}")
    lower = text.lower()
    for term in ("waiver", "evidence"):
        if term not in lower:
            fail(f"release_gate_taxonomy.yaml missing term: {term}")



def validate_guide_marketplace_trust(data: dict) -> None:
    legal = mapping(data, "legal_release_gates", "guide_marketplace_trust_contract.yaml")
    if legal.get("public_release_when_unresolved") is not False:
        fail("Guide Marketplace public release must remain blocked while legal gates are unresolved")
    blockers = mapping(legal, "blockers", "guide_marketplace_trust_contract.yaml")
    for blocker in ("LEGAL-GUIDE-001", "LEGAL-GUIDE-002", "LEGAL-GUIDE-003"):
        if blocker not in blockers:
            fail(f"guide_marketplace_trust_contract.yaml missing blocker: {blocker}")
        entry = blockers[blocker]
        if not isinstance(entry, dict) or entry.get("required_resolution_before_public_release") is not True:
            fail(f"Guide legal blocker must require resolution before release: {blocker}")

    states = mapping(data, "provider_states", "guide_marketplace_trust_contract.yaml")
    if states.get("client_may_set_trusted_states") is not False:
        fail("Provider client must not be able to set trusted provider states")
    values = set(states.get("values", []))
    required_states = {"DRAFT", "SUBMITTED", "UNDER_REVIEW", "VERIFIED", "REJECTED", "SUSPENDED", "EXPIRED", "REVOKED"}
    if not required_states.issubset(values):
        fail("Guide Marketplace provider lifecycle is missing required states")

    trust = mapping(data, "trust_model", "guide_marketplace_trust_contract.yaml")
    if trust.get("generic_is_verified_boolean_sufficient") is not False:
        fail("Generic is_verified boolean must not be sufficient for Guide Marketplace trust")
    if trust.get("public_badges_must_be_fact_specific") is not True:
        fail("Guide Marketplace public trust badges must be fact-specific")

    eligibility = mapping(data, "public_eligibility", "guide_marketplace_trust_contract.yaml")
    if eligibility.get("server_trust_required") is not True:
        fail("Guide Marketplace public eligibility must be server-trusted")
    if eligibility.get("provider_client_may_override") is not False:
        fail("Provider client must not override public eligibility")
    if eligibility.get("stale_cache_may_keep_publicly_current") is not False:
        fail("Stale guide cache must not preserve current eligibility claims")

    contact = mapping(data, "contact_handoff", "guide_marketplace_trust_contract.yaml")
    if contact.get("explicit_user_action_required") is not True:
        fail("Guide contact handoff must require explicit user action")
    if contact.get("server_recheck_current_eligibility_before_resolution") is not True:
        fail("Guide contact resolution must re-check current eligibility")
    if contact.get("auto_message_allowed") is not False:
        fail("Guide contact handoff must not auto-message")

    religious = mapping(data, "religious_boundary", "guide_marketplace_trust_contract.yaml")
    if religious.get("guide_advice_is_governed_ric_truth") is not False:
        fail("Guide advice must not become governed RIC truth")
    if religious.get("tourism_licence_implies_scholar_authority") is not False:
        fail("Tourism licence must not imply scholar authority")

    offline = mapping(data, "offline_behavior", "guide_marketplace_trust_contract.yaml")
    if offline.get("hidden_trusted_write_queue_allowed") is not False:
        fail("Guide Marketplace must not silently queue trusted writes offline")


def validate_screen_traceability(data: dict, entitlements: dict) -> None:
    traceability = mapping(data, "traceability", "screen_feature_traceability.yaml")
    missing = sorted(BASELINE_SCREEN_IDS - set(traceability))
    extra = sorted(set(traceability) - BASELINE_SCREEN_IDS)
    if missing:
        fail(f"screen_feature_traceability.yaml missing screens: {', '.join(missing)}")
    if extra:
        fail(f"screen_feature_traceability.yaml contains unknown screens: {', '.join(extra)}")

    capabilities = set(mapping(entitlements, "capabilities", "entitlement_capability_policy.yaml"))
    allowed_markers = {"GROUP_LIVE_BOARD", "PACK_AUTO_DOWNLOAD_optional", "AUDIO_OFFLINE_optional", "notes_bookmarks_extended_optional", "NOTES_BOOKMARKS_EXTENDED"}
    for screen_id, entry in traceability.items():
        if not isinstance(entry, dict):
            fail(f"Screen {screen_id} traceability entry must be a mapping")
        for field in ("feature_owner", "critical_flows", "offline_behavior", "analytics_events"):
            if field not in entry:
                fail(f"Screen {screen_id} missing field: {field}")
        if not isinstance(entry["critical_flows"], list) or not entry["critical_flows"]:
            fail(f"Screen {screen_id} must define critical_flows")
        if not isinstance(entry["analytics_events"], list) or not entry["analytics_events"]:
            fail(f"Screen {screen_id} must define analytics_events")
        for dep in entry.get("entitlement_dependencies", []) or []:
            dep = str(dep)
            if dep not in allowed_markers and dep not in capabilities and not dep.endswith("_optional"):
                fail(f"Screen {screen_id} references unknown entitlement/capability: {dep}")

    if SCREEN_SPEC.exists():
        spec_text = SCREEN_SPEC.read_text(encoding="utf-8")
        spec_screen_ids = set(re.findall(r"—\s*`([a-z0-9_]+)`", spec_text))
        if spec_screen_ids:
            missing_from_contract = sorted(spec_screen_ids - set(traceability))
            extra_in_contract = sorted(set(traceability) - spec_screen_ids)
            if missing_from_contract:
                fail(
                    "screen_feature_traceability.yaml missing file 11 screens: "
                    + ", ".join(missing_from_contract)
                )
            if extra_in_contract:
                fail(
                    "screen_feature_traceability.yaml contains screens absent from file 11: "
                    + ", ".join(extra_in_contract)
                )
        match = re.search(r"currently contains (\d+) canonical screens", spec_text)
        if match and int(match.group(1)) != len(traceability):
            fail(f"File 11 screen count mismatch: {match.group(1)} != {len(traceability)}")


def main() -> int:
    validate_repository_spec_references()
    loaded = {name: load_yaml(CONTRACT_DIR / name) for name in REQUIRED}
    validate_entitlements(loaded["entitlement_capability_policy.yaml"])
    validate_group_presence(loaded["group_presence_privacy_contract.yaml"])
    validate_trust_chain(loaded["content_pack_trust_chain_contract.yaml"])
    validate_advisory_source_registry(loaded["advisory_source_registry.schema.yaml"])
    validate_release_gate_taxonomy(loaded["release_gate_taxonomy.yaml"])
    validate_guide_marketplace_trust(loaded["guide_marketplace_trust_contract.yaml"])
    validate_screen_traceability(loaded["screen_feature_traceability.yaml"], loaded["entitlement_capability_policy.yaml"])
    print(f"Validated {len(loaded)} spec contract files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
