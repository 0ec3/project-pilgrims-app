# 28 — REAL-WORLD VERIFICATION, RELEASE GATES, AND EVIDENCE

## Document status
- **Type:** Normative release-readiness, real-world verification, and evidence specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, QA lead, release owner, Flutter engineers, backend engineers, content/governance contributors, operations contributors, reviewer agents, release agents
- **Purpose:** Define the canonical real-world verification model, release-candidate evidence requirements, feature-family manual verification expectations, go/no-go gates, known-issue handling, waiver authority, and release-proof package required before Pilgrims Mobile App can be treated as ready to ship.
- **Authority level:** This file is the canonical source of truth for release-readiness proof and go/no-go decisions. File `27` owns testing mechanics. File `30` owns rollout and incident execution after release approval. If dashboards, QA notes, beta feedback, CI status, or release habits conflict with this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `09`, `10`, `11`, `12`, `14`, `15`, `16`, `17`, `18`–`27`, `29`, `30`, `31`, `CONTRACTS/release_gate_taxonomy.yaml`
- **Related contract artifacts:** `CONTRACTS/entitlement_capability_policy.yaml`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`, `CONTRACTS/screen_feature_traceability.yaml`

---

# 1. Purpose of this file

This file exists because a release can look healthy long before it is safe for real pilgrims.

For this project, fake success is especially dangerous because:
- the app is often used while the user is tired, stressed, rushed, elderly, low-confidence with smartphones, or under social pressure,
- offline and degraded-state behavior is part of the core product promise rather than an optional enhancement,
- route-following, saved-anchor recovery, emergency access, group coordination, and phrase support can fail in ways that only appear on real devices and real networks,
- purchase, restore, entitlement, deletion/export, and asset-delivery flows cross trust boundaries,
- governed religious content and safety advisories can be structurally valid yet still fail runtime readability, freshness, signing, locale safety, or trust expectations,
- AI-assisted implementation can produce green tests and polished demos that do not prove real-world readiness.

This file defines:
- what counts as real release evidence,
- how a release candidate must be manually and operationally verified,
- which feature families require on-device or field proof,
- how evidence depth scales with release risk,
- which contract artifacts must be validated,
- which conditions block release,
- who must sign off,
- what must be recorded when known issues remain.

---

# 2. Scope and boundaries

## 2.1 In scope
This file includes:
- release-candidate verification posture,
- release-risk classification and evidence depth,
- contract-artifact evidence requirements,
- manual and physical-device verification expectations,
- real-network and offline verification rules,
- feature-family real-world checks,
- evidence bundle rules,
- sign-off responsibilities,
- go/no-go gates,
- known-issue and waiver policy,
- no-waiver zones,
- seasonal and high-risk release-evidence escalation.

## 2.2 Out of scope
This file does not replace:
- automated testing strategy and test matrices in file `27`,
- incident response and rollback execution in file `30`,
- security/privacy policy and risk posture in file `29`,
- governed-content authoring and approval workflow in file `26`,
- the underlying feature contracts.

## 2.3 Boundary with file `27`
File `27` defines how the product is tested across layers, environments, devices, and matrices.
This file defines what proof must exist at release-candidate time and who can approve or block release.

## 2.4 Boundary with file `30`
File `30` defines release operations, rollback procedure, hotfix workflow, and ongoing incident handling.
This file defines the proof required before something is considered ready to ship.

## 2.5 Boundary with machine-readable release taxonomy
`CONTRACTS/release_gate_taxonomy.yaml` is the machine-readable companion for risk classes, blocker levels, waiver object fields, and no-waiver expectations.
If the taxonomy and this file drift, stop release work and update both.

---

# 3. Product rules that govern release verification

## 3.1 No-demo-as-proof rule
A successful happy-path demo is not release evidence.

## 3.2 Real-conditions rule
If the product claims offline usefulness, stress readability, degraded-state honesty, privacy-light behavior, or low-confidence fallback, those claims must be proven under representative conditions before release.

## 3.3 Physical-device rule
A release candidate is not ship-ready unless required high-risk flows have been validated on physical devices, not only simulators, emulators, or mocks.

## 3.4 Critical-flows-first rule
Release proof must prioritize critical pilgrim outcomes before lower-priority polish.

Critical outcomes include at minimum:
- startup and first usable state,
- Home and Simple Mode recovery behavior,
- ritual guidance and RIC,
- phrasebook, medical, and emergency access,
- Save My Gate and map fallback,
- group creation, join, safe-check-in, regroup, and stale/live honesty,
- pack install, trust-chain verification, and recovery flows,
- account, restore, entitlement, deletion/export, and privacy-data continuity where relevant.

## 3.5 Honest-evidence rule
Evidence must reflect what was truly verified.
The team must not represent:
- simulator checks as device proof,
- lab Wi-Fi checks as real weak-network proof,
- visual inspection as accessibility proof,
- structured content validation as scholar sign-off,
- checksum success as publisher-authenticity proof,
- screenshots alone as behavioral proof,
- contract YAML existence as runtime enforcement proof.

## 3.6 Change-aware rule
Evidence depth must scale with release risk. Map, native-bridge, entitlement, privacy, migration, group, offline-pack, signed-content, and governed-content releases require stricter proof than small internal copy changes.

## 3.7 No hidden blocker rule
Known blocker-class issues must not be buried inside chat threads, memory, informal comments, or undocumented exceptions.

## 3.8 No ethical shortcut rule
Release pressure must not override religious correctness, accessibility, privacy-light behavior, emergency access, artifact authenticity, or ritual trust requirements.

## 3.9 Umrah-first release rule
Unless scope explicitly expands, release verification must prove the Umrah-first experience before any broader seasonal or optional complexity is treated as release-complete.

---

# 4. Canonical terminology

## 4.1 Release candidate
A build and configuration state being evaluated for possible shipment.

## 4.2 Real-world verification
Verification performed under representative device, network, environment, movement, readability, and interruption conditions rather than only deterministic lab conditions.

## 4.3 Evidence bundle
The compact, auditable package of results that explains why a release candidate should or should not ship.

## 4.4 Gate
A required release decision point with explicit pass/fail criteria.

## 4.5 Blocker
A defect, missing proof item, or unresolved risk that prevents release unless a waiver is explicitly approved.

## 4.6 Waiver
An explicit decision to proceed despite a known issue, with documented owner, rationale, mitigation, expiration, and approval reference.

## 4.7 No-waiver zone
A domain where release cannot proceed with a known unresolved failure.

---

# 5. Release-risk classification

Risk classification must align with `CONTRACTS/release_gate_taxonomy.yaml`.

## 5.1 RC0 — documentation-only or non-runtime change
Examples:
- internal documentation wording,
- comments with no runtime, policy, content, contract, or legal effect.

Evidence:
- lightweight review,
- changed-files summary.

## 5.2 RC1 — low-risk UI or non-critical feature refinement
Examples:
- non-critical layout refinement,
- low-risk settings copy,
- non-sensitive help clarification.

Evidence:
- automated regression summary,
- impacted-screen check,
- locale/RTL check where applicable.

## 5.3 RC2 — user-visible feature, navigation, entitlement, or offline behavior change
Examples:
- Home/Simple Mode layout changes,
- planner workflow changes,
- screen inventory changes,
- lock-state copy changes,
- entitlement gate mapping changes,
- standard offline-state behavior.

Evidence:
- affected automation,
- representative physical-device checks,
- offline/degraded checks where relevant,
- accessibility checks,
- QA and feature-owner sign-off.

## 5.4 RC3 — trust-critical change
Examples:
- ritual/RIC/remedy changes,
- emergency/medical/safety behavior,
- group creation/join/check-in/regroup/privacy semantics,
- privacy/deletion/export behavior,
- purchase/restore/entitlement truth,
- migrations/RLS changes,
- pack manifest/signing/activation changes,
- governed-content publishing/activation,
- security/privacy controls.

Evidence:
- all relevant RC2 evidence,
- full contract-artifact validation where applicable,
- physical-device proof,
- weak-network/offline proof,
- privacy/security review evidence,
- content/scholar/safety approval where applicable,
- release-owner review.

## 5.5 RC4 — known correctness, safety, privacy, authenticity, or trust regression
Examples:
- known religious correctness defect,
- emergency access failure,
- hidden tracking regression,
- unauthenticated group data exposure,
- artifact signature bypass,
- deletion/export false claim,
- misleading live-state presentation.

Evidence:
- must fix or remove scope before release.

Waiver:
- not allowed.

---

# 6. Contract-artifact release evidence

## 6.1 Contract validation rule
Any release affecting a machine-readable contract must include validation output and runtime/implementation evidence, not only YAML parse success.

## 6.2 Entitlement capability policy
Required when release affects subscriptions, gates, lock states, offline entitlement continuity, or feature access.

Evidence must prove:
- no `never_gate` capability is locked,
- Supporter enrichments do not interrupt urgent/sacred/recovery flows,
- stale entitlement state is honestly represented,
- downgrade/refund behavior preserves ethical free access.

## 6.3 Group presence privacy contract
Required when release affects group creation, join, check-in, regroup, Live Board, map handoff, freshness, TTL, revocation, retention, or analytics.

Evidence must prove:
- no hidden tracking,
- ordinary check-ins do not carry precise location,
- stale/expired/revoked states render correctly,
- active trusted writes fail honestly offline,
- analytics exclude raw precise location, join codes, and private text.

## 6.4 Content/pack trust-chain contract
Required when release affects pack manifest, artifact download, verification, activation, rollback, key rotation, or governed-content distribution.

Evidence must prove:
- manifest signature validation,
- artifact checksum validation,
- artifact signature validation,
- revoked-key failure behavior,
- compatibility failure behavior,
- last-known-good preservation,
- signed rollback behavior where applicable.

## 6.5 Advisory source registry
Required when release affects safety banners, emergency numbers, official handoff notes, safety tips, or seasonal notices.

Evidence must prove:
- source metadata present,
- verification timestamp present,
- expiry behavior correct,
- stale/fallback behavior correct,
- expired publish-blocking advisory cannot activate.

## 6.6 Screen-feature traceability
Required when release adds/removes/changes screens, states, navigation, or critical-flow surfaces.

Evidence must prove:
- screen owner and feature owner match,
- offline/stale/error/locked states exist,
- accessibility and localization checks are complete,
- release-evidence owner is assigned.

---

# 7. Required gate checklist

A release candidate cannot proceed to production rollout unless the evidence bundle includes:

1. release candidate identity: build, commit, config, manifest, content activation pointer, and flags;
2. risk class and impacted specs/contracts;
3. automated test summary from file `27`;
4. physical-device proof for affected critical flows;
5. offline/degraded proof for affected offline or trusted-write flows;
6. accessibility proof for affected user-facing screens;
7. security/privacy review proof for affected protected data or trust boundaries;
8. governed-content and scholar/safety approval proof where applicable;
9. pack/content trust-chain proof where applicable;
10. known issues with blocker classification;
11. waiver objects for eligible non-blocking gaps;
12. sign-offs from required owners;
13. rollback/containment plan from file `30` for RC2+ releases.

---

# 8. No-waiver zones

Release may not proceed with known unresolved failures in:
- ritual correctness,
- RIC/remedy correctness,
- emergency access or emergency-card baseline,
- medical profile local privacy protection,
- hidden tracking or misleading location/presence behavior,
- server-side authorization/RLS for group/account data,
- account deletion/export false claims,
- artifact signature/trust-chain bypass,
- paywall on correctness or essential safety,
- legal/store privacy disclosure mismatch,
- critical accessibility blocker on essential flows.

---

# 9. Evidence bundle structure

The evidence bundle should be a compact Markdown or structured record with:

```yaml
release_candidate:
  build_id:
  commit_sha:
  config_snapshot:
  manifest_id:
  content_activation_pointer:
  flags_snapshot:
risk:
  risk_class:
  impacted_specs: []
  impacted_contracts: []
evidence:
  automated_tests:
  device_lab:
  field_or_weak_network:
  accessibility:
  privacy_security:
  content_governance:
  pack_trust_chain:
  advisory_freshness:
known_issues:
  blockers: []
  waived_gaps: []
signoffs:
  product:
  engineering:
  qa:
  release:
  security_privacy:
  content_governance:
rollback:
  containment_plan:
  last_known_good:
```

---

# 10. Sign-off responsibilities

## 10.1 Product owner
Confirms product scope, ethical boundaries, user impact, and no-waiver zones.

## 10.2 Engineering owner
Confirms implementation, migration, integration, performance, and rollback readiness.

## 10.3 QA owner
Confirms test evidence, device proof, field proof, accessibility proof, and known-issue classification.

## 10.4 Security/privacy owner
Confirms protected data, privacy-light behavior, disclosures, risk posture, and incident readiness.

## 10.5 Content/governance owner
Confirms governed-content approval, advisory freshness, artifact metadata, and rollback candidate validity.

## 10.6 Release owner
Confirms final evidence bundle completeness and go/no-go decision.

---

# 11. Definition of done

A release candidate is ready for controlled rollout only when:
- risk class is assigned,
- impacted specs and contracts are listed,
- automated tests pass or gaps are explicitly classified,
- required device/field/degraded/accessibility evidence exists,
- affected contract artifacts have validation and runtime proof,
- no no-waiver zone failure exists,
- known issues are classified and owned,
- required sign-offs exist,
- rollback/containment plan is ready.

---

# 12. AI-agent checklist

Before preparing or reviewing release evidence, an AI agent must:
1. Read files `27`, `28`, `29`, `30`, and `31`.
2. Read `CONTRACTS/release_gate_taxonomy.yaml`.
3. Check impacted contract artifacts.
4. Distinguish test mechanics from release approval.
5. Never classify screenshots, happy-path demos, or YAML parse success as complete release proof.
6. Never waive a no-waiver-zone failure.

---

End of file.