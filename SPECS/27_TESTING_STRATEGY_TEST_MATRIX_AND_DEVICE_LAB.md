# 27 — TESTING STRATEGY, TEST MATRIX, AND DEVICE LAB

## Document status
- **Type:** Normative quality-engineering, verification, and device-validation specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, QA lead, Flutter engineers, backend engineers, content/governance contributors, release engineers, operations contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical testing strategy, layered test model, quality gates, canonical test matrix dimensions, device-lab strategy, environment rules, automation expectations, evidence requirements, and release-blocking criteria for Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for how the product is tested and verified. File `28` owns release go/no-go gates and waiver authority. File `30` owns rollout and incident execution. If CI pipelines, test plans, dashboards, manual QA, or device-lab behavior diverge from this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `09`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`–`26`, `28`, `29`, `30`, `31`, `CONTRACTS/release_gate_taxonomy.yaml`
- **Related contract artifacts:** `CONTRACTS/entitlement_capability_policy.yaml`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`, `CONTRACTS/screen_feature_traceability.yaml`

---

# 1. Purpose of this file

This file exists because Pilgrims Mobile App can look successful long before it is actually safe to release.

False confidence is unusually dangerous because:
- many flows are used when the pilgrim is stressed, tired, elderly, low-confidence with smartphones, or under time pressure,
- several critical journeys must still work offline or under weak connectivity,
- map and positioning behavior can degrade silently,
- group creation, check-ins, and stale/live coordination can appear to work while violating privacy or trust boundaries,
- governed ritual/safety content can be structurally valid yet fail review, signing, freshness, or runtime behavior,
- accessibility, localization, and RTL issues often appear only on real devices and real settings,
- entitlement, purchase, deletion/export, and restore flows can look correct on one path while failing on reinstall, restore, expiry, downgrade, or offline state,
- AI coding agents can produce passing tests that cover the wrong thing.

This file defines:
- what quality means for this product,
- which test layers are required,
- how canonical test matrices are structured,
- what environments and devices must be covered,
- when cloud device testing is enough and when physical-device testing is mandatory,
- how machine-readable contract artifacts are validated,
- what evidence is required before release,
- what conditions block release even when many tests are green.

---

# 2. Quality purpose and user value

## 2.1 Module purpose
This quality module ensures the app remains:
- trustworthy,
- calm under stress,
- offline-capable,
- accessible,
- performance-safe on supported devices,
- privacy-light,
- honest about degraded states,
- protected by machine-readable contracts where safety/trust depends on consistency.

## 2.2 User value statement
A pilgrim should never have to think about the testing system directly.

The value to the pilgrim is that:
- the app opens quickly,
- the right screen appears when needed,
- critical flows still function on bad networks,
- emergency and phrase support remain reachable,
- ritual guidance behaves consistently,
- map and group features degrade honestly,
- subscription and privacy-data actions do not mislead them,
- platform differences do not create confusing behavior,
- large text, RTL, and assistive technologies remain usable.

---

# 3. Scope and boundaries

## 3.1 In scope
This file includes:
- quality philosophy,
- layered test strategy,
- canonical test suites and responsibilities,
- environment definitions,
- CI posture,
- device-lab strategy,
- cloud-vs-physical test allocation,
- matrix dimensions,
- contract-artifact validation,
- required release evidence inputs,
- defect severity posture as it affects release readiness,
- field and stress validation requirements,
- quality anti-patterns and waiver expectations.

## 3.2 Out of scope
This file does not replace:
- feature-specific behavioral rules,
- telemetry taxonomy itself,
- security/privacy policy itself,
- incident response procedures,
- app-store release operations,
- release go/no-go authority.

## 3.3 Boundary with file `28`
File `28` owns release gates, evidence sufficiency, no-waiver zones, and go/no-go approval. This file owns how testing and verification produce that evidence.

## 3.4 Boundary with file `29`
File `29` owns security/privacy policy and risk posture. This file verifies that security/privacy expectations are tested.

## 3.5 Boundary with file `30`
File `30` owns operations and incident execution. This file verifies readiness before rollout and may provide incident-reproduction evidence.

---

# 4. Product rules that govern testing

## 4.1 Fake-green warning rule
A large passing test suite is not evidence of release readiness if the suite misses offline behavior, degraded states, accessibility, privacy, contract artifacts, real-device validation, or stress-critical flows.

## 4.2 Critical-flow-first rule
Testing must prioritize critical pilgrim outcomes before secondary convenience features.

Critical outcomes include at minimum:
- startup and first usable state,
- ritual guidance and RIC,
- emergency, medical, and phrase support,
- Home and Simple Mode recovery flows,
- Save My Gate and map fallback,
- group creation, join, regroup, safe-update, and stale/live honesty,
- pack install/recovery/purge/trust-chain behavior,
- account/restore/entitlement/deletion/export continuity where relevant.

## 4.3 Minimum-supported-device rule
Quality is judged on the supported minimum and representative mid-tier device range, not only on high-end developer hardware.

## 4.4 Degraded-state truth rule
Every feature that claims graceful degradation must be tested in degraded conditions, not only described in specs.

## 4.5 Real-device rule
Certain capabilities require physical-device evidence, including:
- map positioning and orientation behavior,
- install/restart/purge/download flows,
- OS notification behavior,
- billing/restore flows,
- account/deletion/export flows where platform/browser handoff is involved,
- system accessibility interactions,
- performance and thermals,
- real-world readability and stress behavior.

## 4.6 Accessibility-is-release-quality rule
Large text, RTL, screen-reader usability, reduced-transparency or contrast behavior, and other accessibility-related requirements are release quality, not optional polish.

## 4.7 No private-production-data rule
Testing must not depend on live user private data, medical details, real join codes, private groups, or sensitive production artifacts.

## 4.8 No scholar-sensitive-shortcut rule
No automation, fixture, or mock may bypass required governed-content publication and review constraints in a way that hides real risk.

## 4.9 Honest-waiver rule
If a release proceeds with a known quality gap, that gap must be explicitly documented with owner, risk, mitigation, and expiration under file `28`. Silent acceptance is forbidden.

## 4.10 Contract-enforcement rule
Machine-readable contract files must be parseable and must have tests proving relevant runtime behavior, not merely file existence.

---

# 5. Canonical terminology

## 5.1 Quality gate
A required condition that must pass before the next delivery stage or release stage.

## 5.2 Release blocker
A defect or missing evidence item that prevents release unless formally waived by file `28` and only outside no-waiver zones.

## 5.3 Device lab
The maintained set of physical devices, emulators/simulators, and cloud-device capacity used to validate supported device behavior.

## 5.4 Matrix dimension
A test variable used to select coverage combinations, such as platform, OS tier, locale, network state, or entitlement state.

## 5.5 Representative scenario
A realistic user flow chosen because it reflects real stress, not merely technical coverage.

## 5.6 Synthetic test data
Controlled non-production data created for repeatable tests, fixtures, screenshots, demos, or automation.

## 5.7 Certification run
A broader pre-release execution across required layers, devices, and scenarios used to certify a release candidate.

---

# 6. Quality philosophy and test pyramid posture

The product should use a strong test pyramid:
- many unit and repository/domain tests,
- many targeted widget tests,
- selected golden tests for high-risk visual surfaces,
- selected integration tests for critical flows,
- focused platform-native tests for bridges,
- selective but mandatory real-device and field validation for highest-risk behaviors.

Risk-based allocation gives highest intensity to:
- Home/startup,
- ritual correctness surfaces,
- emergency/medical/phrasebook flows,
- map recovery,
- group creation/join/regroup/check-in/privacy,
- packs/offline distribution/trust-chain,
- account/restore/entitlements/deletion/export,
- localization/accessibility shells.

---

# 7. Required quality layers

## 7.1 Layer 1 — Static and generated-artifact verification
Includes:
- linting,
- formatting,
- code generation verification,
- schema validation,
- localization-key validation,
- dependency/build-health validation,
- YAML contract parsing,
- manifest and artifact signature/checksum validation,
- advisory source metadata validation.

## 7.2 Layer 2 — Unit and domain tests
Includes:
- pure business logic,
- reducers/notifiers/controllers where isolated,
- repository rules with fakes,
- rule evaluators,
- sorting/ranking logic,
- entitlement mapping,
- migration logic,
- serialization/deserialization,
- freshness/TTL state transitions,
- pack state machine transitions.

## 7.3 Layer 3 — Widget and screen-state tests
Includes:
- major state rendering,
- interaction wiring,
- accessibility labels/semantics where inspectable,
- stale/offline/locked/error states,
- deletion/export status states,
- group creation/join failure states,
- pack verification failure states.

## 7.4 Layer 4 — Golden and visual-regression tests
Selected high-risk surfaces only:
- Home and Simple Home shells,
- emergency big-text cards,
- phrasebook cards with Arabic + translated text,
- group stale/live and trusted-write failure cards,
- paywall/lock states where honesty matters,
- degraded pack/install states,
- Privacy & Data flow states,
- selected map fallback states where deterministic visuals are possible.

## 7.5 Layer 5 — Integration tests
Includes:
- startup routing,
- cross-feature handoffs,
- state persistence across flows,
- manifest and entitlement fetch integration,
- group creation/join/check-in with controlled backend,
- account deletion/export request/status with controlled backend,
- pack state transitions using controlled backends/fakes,
- content publication/runtime compatibility checks.

## 7.6 Layer 6 — Platform-native or bridge tests
Includes:
- purchase bridge behavior,
- notification scheduling and permission flows,
- asset-delivery bridges,
- map SDK/native wrapper boundaries,
- browser/system-settings handoffs,
- lifecycle-specific platform behavior that pure Flutter tests cannot prove.

## 7.7 Layer 7 — Device and field validation
Includes:
- performance on supported devices,
- accessibility on system settings,
- map orientation and movement use,
- emergency usage speed,
- restore/reinstall behavior,
- weak-network or no-network recovery,
- pack download/verify/restart/purge behavior,
- group creation/join/check-in under weak network,
- readability under glare/stress where feasible.

---

# 8. Contract-artifact validation suites

## 8.1 Baseline parser validation
`tools/specs/validate_spec_contracts.py` must pass whenever files in `SPECS/CONTRACTS/` change.

## 8.2 Entitlement capability policy tests
Must verify:
- `never_gate` capabilities remain accessible in appropriate guest/free/offline states,
- Supporter gates match API/client fixtures,
- downgrade/refund behavior preserves ethical free access,
- lock-state copy does not imply correctness or safety is withheld.

## 8.3 Group presence privacy tests
Must verify:
- ordinary check-ins do not include precise location,
- stale/expired/revoked status renders correctly,
- TTL expiration changes live-board behavior,
- revoked/expired events do not appear as live certainty,
- analytics exclude raw precise location, join codes, and private text.

## 8.4 Content/pack trust-chain tests
Must verify:
- manifest signature success/failure,
- artifact checksum success/failure,
- artifact signature success/failure,
- revoked-key failure,
- compatibility failure,
- last-known-good preservation,
- signed rollback pointer behavior.

## 8.5 Advisory source registry tests
Must verify:
- required advisory metadata exists,
- expired publish-blocking advisories fail activation,
- stale/fallback behavior displays correctly,
- emergency/safety content remains non-blocking for ritual/recovery flows.

## 8.6 Screen-feature traceability tests
Must verify:
- all canonical screens have feature owners,
- critical flows have screen coverage,
- `group_creation_flow` and `privacy_data_flow` exist,
- offline/stale/error/locked states are represented.

---

# 9. Canonical test matrix dimensions

Test planning must consider:
- platform: iOS, Android,
- device class: minimum supported, mid-tier, large-screen where supported,
- OS version: minimum supported, current stable, recent prior,
- locale: English, Arabic/RTL, Indonesian where supported,
- text scale: normal, large, extra large,
- contrast/transparency settings,
- network: online, weak, intermittent, offline,
- storage: normal, low storage,
- auth: guest, signed-in, expired session,
- entitlement: free, Supporter, expired/downgraded,
- group role: none, leader, member, removed,
- pack state: not installed, downloading, verifying, installed, failed, purged,
- content/advisory state: current, stale, expired, rollback candidate,
- permission state: granted, denied, limited, not determined.

---

# 10. Critical scenario matrix

## 10.1 Startup and Home
- first launch without account,
- offline launch with last-good content,
- Home recovery card under stale group/map/pack state,
- Simple Mode urgent shortcuts.

## 10.2 Rituals and RIC
- start/resume ritual offline,
- RIC result correctness fixtures,
- remedy/citation rendering,
- scholar-reviewed content artifact runtime compatibility.

## 10.3 Emergency, medical, phrasebook
- emergency root speed,
- big-text phrase rendering,
- medical profile reveal/edit local-only,
- offline phrasebook access,
- safety/advisory stale/fallback state.

## 10.4 Maps and Save My Gate
- save gate,
- recall offline,
- route preview degradation,
- low-confidence positioning copy,
- map handoff from regroup pin.

## 10.5 Group
- create group success,
- create group unauthenticated → account gate → return,
- create group offline failure,
- create group rate limit,
- create group idempotent retry,
- join success/invalid/not-found/rate-limit,
- check-in success/offline fallback,
- regroup pin leader-only behavior,
- stale/expired/revoked live-board state,
- no hidden contact import/social graph.

## 10.6 Packs/content
- manifest fetch/cache/stale state,
- download interruption/resume,
- verifying state,
- checksum failure,
- artifact signature failure,
- manifest signature failure,
- revoked signing key,
- app compatibility failure,
- last-known-good preservation,
- purge/reinstall.

## 10.7 Account, entitlement, Privacy & Data
- guest core use without account,
- entitlement refresh success/failure/stale,
- restore success/failure/offline,
- downgrade/refund state,
- Privacy & Data local-only explanation,
- deletion request success/failure/offline,
- deletion status states,
- export request success/failure/offline,
- retention summary copy.

---

# 11. Device-lab posture

## 11.1 Minimum device proof
Each release candidate affecting critical flows must include at least:
- one representative iOS physical device,
- one representative Android physical device,
- minimum-supported or lower-mid-tier hardware where available,
- accessibility settings verification on at least one platform for affected surfaces.

## 11.2 Physical proof required
Physical proof is required for:
- map/location/orientation,
- pack download/verify/restart/purge,
- purchase/restore,
- notifications,
- browser/system-settings handoff,
- accessibility settings,
- performance/thermal/battery-sensitive flows.

## 11.3 Cloud-device use
Cloud devices may supplement coverage but must not replace physical proof for the above categories.

---

# 12. Blocker posture

Release-blocking conditions include:
- app cannot reach first usable state,
- ritual correctness/RIC critical defect,
- emergency/phrase baseline unavailable,
- Save My Gate recall failure in expected offline state,
- group RLS/auth/privacy failure,
- hidden tracking/contact import regression,
- entitlement never-gate violation,
- deletion/export false claim or data leak,
- pack/content trust-chain bypass,
- expired publish-blocking advisory activation,
- critical accessibility failure on essential flow,
- unsupported private production data in tests.

Waivers are controlled by file `28`; no-waiver zones cannot be waived.

---

# 13. Evidence output requirements

Test evidence must record:
- release candidate identity,
- impacted specs/contracts,
- environments used,
- devices used,
- network/storage/accessibility states,
- automated test summary,
- manual/device proof summary,
- failed tests and classification,
- known gaps and owners,
- screenshots/videos only as supporting artifacts, not proof by themselves.

---

# 14. Definition of done

Testing strategy is ready when:
- layered test suites exist,
- contract-artifact validation is wired into CI or equivalent checks,
- critical scenario matrix is covered,
- physical-device requirements are planned,
- degraded/offline/stale states are tested,
- accessibility is treated as release quality,
- security/privacy and trust-chain failures block release where required,
- evidence outputs feed file `28` directly.

---

# 15. AI-agent checklist

Before editing tests or verification plans, an AI agent must:
1. Read files `11`, `13`, `14`, `15`, `20`, `24`, `26`, `27`, `28`, `29`, `30`, and `31` where relevant.
2. Read affected contract artifacts.
3. Identify critical flows and matrix dimensions.
4. Confirm whether physical-device proof is required.
5. Do not treat YAML parsing, screenshots, or happy-path demos as sufficient proof.
6. Update evidence and release-gate references with test changes.

---

End of file.