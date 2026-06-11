# Machine-readable contract artifacts

## Purpose

The files in this directory are **machine-readable companions** to the normative Markdown specs.

They mirror implementation-critical truths from the specs so implementation, tests, release checks, and AI agents can validate behavior without repeatedly re-interpreting long prose documents.

They are especially important for rules that must not drift during implementation, such as:
- entitlement and paywall boundaries,
- group presence and privacy semantics,
- pack/content signing and activation rules,
- advisory freshness requirements,
- release-risk classification,
- screen-to-feature ownership and evidence mapping.

---

## Authority model

Markdown specs remain the human-readable authority.

Contract artifacts are normative implementation aids.

If a Markdown spec and a YAML contract conflict:
1. stop implementation work for the affected behavior,
2. identify the owning spec and owning contract,
3. update both through the documented change-control process,
4. re-run contract validation,
5. update tests/release evidence if the truth changed.

Do **not** silently choose whichever source is easier to implement.

---

## Required treatment by humans and AI agents

Humans and AI agents must treat these files as follows:

- Do not delete them as documentation clutter.
- Do not treat them as optional examples.
- Do not create implementation behavior that contradicts them.
- Do not add new entitlement keys, screen IDs, release classes, freshness states, signing fields, or advisory fields without synchronizing the owning Markdown spec.
- Do not edit a YAML contract without also checking impacted tests, release evidence, and feature specs.
- Do not treat successful YAML parsing as proof of runtime correctness.
- Do use these files as fixtures or input contracts for tests, CI, release checks, and AI-agent review.

---

## Current artifacts

| File | Owner spec | How it must be used |
|---|---|---|
| `entitlement_capability_policy.yaml` | `SPECS/24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md` | Drives entitlement fixture generation, paywall/lock-state tests, never-gate checks, downgrade behavior checks, and release evidence for monetization changes. |
| `group_presence_privacy_contract.yaml` | `SPECS/20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md` | Drives group presence data tests, freshness/TTL UI tests, privacy tests, analytics-redaction tests, and no-hidden-tracking review. |
| `content_pack_trust_chain_contract.yaml` | `SPECS/15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md` and `SPECS/26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md` | Drives pack/content manifest tests, signature/checksum/key-revocation tests, last-known-good tests, rollback tests, and release evidence for pack/content activation. |
| `advisory_source_registry.schema.yaml` | `SPECS/22_FEATURE_PHRASEBOOK_EMERGENCY_SAFETY_AND_ASSISTIVE_TOOLS.md` | Drives safety/emergency advisory metadata checks, expiry checks, stale/fallback behavior tests, and content-governance release evidence. |
| `release_gate_taxonomy.yaml` | `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md` | Drives release-risk classification, waiver object shape, no-waiver checks, release evidence templates, and release-agent review behavior. |
| `screen_feature_traceability.yaml` | `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md` | Drives screen ownership checks, navigation coverage, critical-flow test mapping, and release evidence ownership. |

---

## Validator

The validator lives at:

```bash
python tools/specs/validate_spec_contracts.py
```

The validator must pass whenever files in this directory change.

Current validator scope:
- confirms required contract files exist,
- confirms YAML files parse as mappings,
- confirms each contract has version metadata,
- performs initial sanity checks for entitlement, group presence, and trust-chain contracts.

Validator limitations:
- it does not replace product review,
- it does not prove runtime behavior,
- it does not prove release readiness,
- it does not replace file `27` testing requirements or file `28` release evidence.

---

## Development workflow

When editing implementation code affected by these contracts:

1. Read the owning Markdown spec.
2. Read the affected YAML contract.
3. Use the YAML as a test fixture or validation input where practical.
4. Add or update runtime tests proving the implementation obeys the contract.
5. Run `python tools/specs/validate_spec_contracts.py` if contract files changed.
6. Update file `27` test evidence expectations or file `28` release evidence if the change affects verification or release gates.

---

End of file.