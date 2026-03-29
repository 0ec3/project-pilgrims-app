# 27 — TESTING STRATEGY, TEST MATRIX, AND DEVICE LAB

## Document status
- **Type:** Normative quality-engineering, verification, and device-validation specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, QA lead, Flutter engineers, backend engineers, content/governance contributors, release engineers, operations contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical testing strategy, layered test model, quality gates, canonical test matrix dimensions, device-lab strategy, environment rules, automation expectations, evidence requirements, and release-blocking criteria for Pilgrims Mobile App.
- **Authority level:** This file is the canonical source of truth for how the product is verified before release. If CI pipelines, test plans, dashboards, manual QA, or device-lab behavior diverge from this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`, `21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`, `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`, `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`
- **Related files:** `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because Pilgrims Mobile App can look successful long before it is actually safe to release.

For this project, false confidence is unusually dangerous because:
- many flows are used when the pilgrim is stressed, tired, elderly, low-confidence with smartphones, or under time pressure,
- several critical journeys must still work offline or under weak connectivity,
- map and positioning behavior can degrade silently,
- governed ritual content can be structurally valid yet still fail the real user experience,
- accessibility, localization, and RTL issues often appear only on real devices and real settings,
- platform-adapted UI can regress differently on iOS and Android,
- entitlement and purchase flows can look correct on one path while failing on reinstall, restore, expiry, or downgrade,
- AI coding agents can easily produce passing tests that cover the wrong thing.

This file prevents those failures by defining:
- what quality means for this product,
- which test layers are required,
- how the canonical test matrix is structured,
- what environments and devices must be covered,
- when cloud device testing is enough and when physical-device testing is mandatory,
- what evidence is required before release,
- what conditions block release even when many tests are green.

---

# 2. Quality purpose and user value

## 2.1 Module purpose
This quality module exists to ensure that the app remains:
- trustworthy,
- calm under stress,
- offline-capable,
- accessible,
- performance-safe on supported devices,
- and honest about degraded states.

## 2.2 User value statement
A pilgrim should never have to think about the testing system directly.

The value to the pilgrim is that:
- the app opens quickly,
- the right screen appears when needed,
- critical flows still function on bad networks,
- emergency and phrase support remain reachable,
- ritual guidance behaves consistently,
- map and group features degrade honestly,
- platform differences do not create confusing behavior,
- large text, RTL, and assistive technologies remain usable.

## 2.3 Operational value statement
The team should be able to answer questions like:
- What exactly was tested for this release candidate?
- Which feature families have automated coverage versus only manual evidence?
- Which devices represent the minimum supported experience?
- Which failures are release blockers?
- Which issues only require monitoring or waiver review?
- Is a successful simulator run enough for this behavior, or is physical-device proof required?

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
- required release evidence,
- defect severity posture as it affects release readiness,
- field and stress validation requirements,
- quality anti-patterns and waiver expectations.

## 3.2 Out of scope
This file does **not** replace:
- feature-specific behavioral rules,
- telemetry taxonomy itself,
- security/privacy policy itself,
- incident response procedures,
- app-store release operations,
- deep backend SRE runbooks.

Those are owned by related files. This file describes how their quality expectations are verified.

## 3.3 Boundary with file `17`
File `17` defines:
- telemetry taxonomy,
- observability boundaries,
- alert thresholds,
- performance budgets.

This file defines how those budgets and telemetry contracts are tested and evidenced before release.

## 3.4 Boundary with file `26`
File `26` defines governed content workflow, scholar review, publication, and rollback safety.

This file defines how that content workflow is validated at schema, runtime, offline, regression, and release-evidence levels.

## 3.5 Boundary with file `30`
File `30` should define operations, rollback, incident behavior, and delivery runbooks.

This file defines pre-release and release-candidate quality verification, not the full operational incident response model.

## 3.6 Boundary with feature files
Feature files `18` through `25` define feature-specific testing expectations.
This file turns those expectations into one coherent strategy, one device-lab posture, and one release-evidence system.

---

# 4. Product rules that govern testing

## 4.1 Fake-green warning rule
A large passing test suite is not evidence of release readiness if the suite misses offline behavior, degraded states, accessibility, real-device validation, or stress-critical flows.

## 4.2 Critical-flow-first rule
Testing must prioritize critical pilgrim outcomes before secondary convenience features.

Critical outcomes include at minimum:
- startup and first usable state,
- ritual guidance and RIC,
- emergency and phrase support,
- Home recovery flows,
- Save My Gate and map fallback,
- group regroup and safe-update flows,
- pack install/recovery/purge behavior,
- account/restore/entitlement continuity where relevant.

## 4.3 Minimum-supported-device rule
Quality is judged on the supported minimum and representative mid-tier device range, not only on high-end developer hardware.

## 4.4 Degraded-state truth rule
Every feature that claims graceful degradation must be tested in degraded conditions, not only described in specs.

## 4.5 Real-device rule
Certain capabilities require physical-device evidence, not only emulator/simulator or mock proof.

These include at minimum:
- map positioning and orientation behavior,
- install/restart/purge/download flows,
- OS notification behavior,
- billing/restore flows,
- system accessibility interactions,
- performance and thermals,
- real-world readability and stress behavior.

## 4.6 Accessibility-is-release-quality rule
Large text, RTL, screen-reader usability, reduced-transparency or contrast behavior, and other accessibility-related requirements are release quality, not optional polish.

## 4.7 No private-production-data rule
Testing must not depend on live user private data, medical details, or sensitive production artifacts.

## 4.8 No scholar-sensitive-shortcut rule
No automation, fixture, or mock may bypass required governed-content publication and review constraints in a way that hides real risk.

## 4.9 Honest-waiver rule
If a release proceeds with a known quality gap, that gap must be explicitly documented with owner, risk, mitigation, and expiration. Silent acceptance is forbidden.

## 4.10 Cross-platform honesty rule
Shared Flutter logic is allowed, but platform-specific behavior must still be verified on its real platform.

---

# 5. Canonical terminology for this module

## 5.1 Test pyramid
The layered testing model where fast low-level tests are numerous, targeted higher-level tests are fewer, and broad real-device or field tests are selective but high value.

## 5.2 Quality gate
A required condition that must pass before the next delivery stage or release stage.

## 5.3 Release blocker
A defect or missing evidence item that prevents release unless formally waived by the accountable release owner under an approved process.

## 5.4 Device lab
The maintained set of physical devices, emulators/simulators, and cloud-device capacity used to validate supported device behavior.

## 5.5 Matrix dimension
A test variable used to select coverage combinations, such as platform, OS tier, locale, network state, or entitlement state.

## 5.6 Representative scenario
A realistic user flow chosen because it reflects real stress, not merely technical coverage.

## 5.7 Synthetic test data
Controlled non-production data created for repeatable tests, fixtures, screenshots, demos, or automation.

## 5.8 Canary suite
A small, fast, high-signal set of tests that runs frequently and must remain extremely stable.

## 5.9 Certification run
A broader pre-release execution across required layers, devices, and scenarios used to certify a release candidate.

## 5.10 Field validation
Representative real-world use outside purely lab conditions, especially for movement, readability, and stress.

---

# 6. Quality philosophy and test pyramid posture

## 6.1 Canonical posture
The product should use a strong test pyramid:
- many unit and repository/domain tests,
- many targeted widget tests,
- selected golden tests for high-risk visual surfaces,
- selected integration tests for critical flows,
- focused platform-native tests for bridges,
- selective but mandatory real-device and field validation for the highest-risk behaviors.

## 6.2 Why this posture is required
This project cannot rely only on end-to-end tests because:
- full E2E suites are slower and flakier,
- many failures are easier to catch at domain or widget level,
- most feature contracts are easier to stabilize in lower layers,
- device and field time is scarce and should be spent on the risks only physical reality can expose.

## 6.3 What this posture rejects
This file rejects two bad extremes:
- **only-unit-test culture** where complex flows are never validated end to end,
- **only-E2E-demo culture** where a few happy-path tests hide structural drift.

## 6.4 Risk-based allocation rule
Test effort should scale with real user risk, operational risk, and regression frequency.
The highest intensity goes to:
- Home/startup,
- ritual correctness surfaces,
- emergency and phrasebook flows,
- map recovery,
- packs/offline distribution,
- account/restore/entitlements,
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
- dependency or build-health validation,
- manifest and artifact integrity checks.

## 7.2 Layer 2 — Unit and domain tests
Includes:
- pure business logic,
- reducers/notifiers/controllers where isolated,
- repository rules with fakes,
- rule evaluators,
- sorting/ranking logic,
- entitlement mapping,
- migration logic,
- serialization/deserialization.

## 7.3 Layer 3 — Widget and screen-state tests
Includes:
- major state rendering,
- interaction wiring,
- accessibility labels or semantics where inspectable,
- edge-state rendering,
- copy/layout regressions that do not require native device proof.

## 7.4 Layer 4 — Golden and visual-regression tests
Includes selected high-risk surfaces only, such as:
- Home and Simple Home shells,
- emergency big-text cards,
- phrasebook cards with Arabic + translated text,
- paywall or lock states where honesty matters,
- degraded pack/install states,
- selected map fallback states where deterministic visuals are possible.

## 7.5 Layer 5 — Integration tests
Includes:
- startup routing,
- cross-feature handoffs,
- state persistence across flows,
- manifest and entitlement fetch integration,
- pack state transitions using controlled backends/fakes,
- content publication/runtime compatibility checks where app runtime is involved.

## 7.6 Layer 6 — Platform-native or bridge tests
Includes:
- purchase bridge behavior,
- notification scheduling and permission flows,
- asset-delivery bridges,
- map SDK/native wrapper boundaries,
- lifecycle-specific platform behavior that pure Flutter tests cannot prove.

## 7.7 Layer 7 — Device and field validation
Includes:
- performance on supported devices,
- accessibility on system settings,
- map orientation and movement use,
- emergency usage speed,
- restore/reinstall behavior,
- weak-network or no-network recovery,
- real-world comprehension under stress.

---

# 8. Quality ownership model

## 8.1 Shared responsibility rule
Quality is shared across product, engineering, QA, content/governance, and release roles.
It must not be delegated to one person or one phase.

## 8.2 Engineering responsibility
Engineers own:
- automated tests for their modules,
- feature-level regression prevention,
- fixture quality,
- CI reliability for their areas,
- bug reproduction support.

## 8.3 QA responsibility
QA owns:
- matrix planning,
- certification runs,
- device-lab coordination,
- exploratory coverage,
- evidence collection,
- release-candidate quality summaries.

## 8.4 Product responsibility
Product owns:
- scenario prioritization,
- real-world acceptance interpretation,
- user-meaning validation,
- signoff on whether flows remain calm and understandable.

## 8.5 Content/governance responsibility
Content and scholar/governance roles own:
- validation of governed content publication outputs,
- correctness of content-driven fixtures,
- signoff for content changes that affect ritual meaning.

## 8.6 Release owner responsibility
The release owner owns final release gating decisions, including whether a waiver can be accepted.

## 8.7 AI-agent responsibility boundary
AI agents may help generate tests, fixtures, matrix drafts, and failure summaries, but they must not silently redefine the release bar or delete necessary coverage to make pipelines green.

---

# 9. Required testability architecture

## 9.1 Testability is an architecture requirement
Modules must remain testable by design, not made testable only after regressions occur.

## 9.2 Shared testkit rule
The Flutter repo should use centralized test utilities such as `pilgrims_testkit` or the internal equivalent for:
- stable fixtures,
- fake repositories,
- clock/environment control,
- golden harnesses,
- integration helpers,
- semantic finder helpers,
- route/bootstrap helpers.

## 9.3 Dependency-injection rule
Important dependencies such as repositories, time, network state providers, telemetry emitters, and entitlement providers must be injectable or swappable in tests.

## 9.4 Deterministic-state rule
Tests should not depend on real time, random ordering, uncontrolled remote flags, or live network responses unless the explicit purpose is to validate those live integrations in a controlled stage.

## 9.5 Stable-semantic-hook rule
Critical interactive elements should expose stable keys, route names, IDs, or semantics hooks where needed so automation remains reliable.

## 9.6 No test-only product forks rule
Do not create alternative hidden feature logic only for tests. Use controllable seams, not a fake second app.

---

# 10. Test environments and environment tiers

## 10.1 Canonical environment tiers
Testing should use these canonical tiers:
1. local developer
2. CI fast lane
3. CI extended lane
4. device-lab certification
5. field validation
6. beta distribution validation

## 10.2 Local developer tier
Purpose:
- fast confidence during development,
- unit/widget/integration subset,
- quick regression checks before pull request.

## 10.3 CI fast lane
Purpose:
- block obviously unsafe merges quickly.

Recommended contents:
- formatting/lint,
- generation checks,
- fast unit tests,
- selected widget tests,
- small canary integration suite.

## 10.4 CI extended lane
Purpose:
- broader automated confidence on mainline or release branches.

Recommended contents:
- fuller unit and widget suites,
- golden tests,
- broader integration tests,
- schema/content validation,
- contract tests,
- package or module build checks.

## 10.5 Device-lab certification tier
Purpose:
- release-candidate proof on required devices and settings.

## 10.6 Field-validation tier
Purpose:
- verify behavior that lab conditions cannot fully simulate, especially movement, readability, stress, and network variation.

## 10.7 Beta-distribution tier
Purpose:
- validate near-production builds through controlled internal/external testing channels before final release.

---

# 11. Test data, fixtures, and synthetic environments

## 11.1 Synthetic-data rule
Use synthetic or curated non-production data for all automated and most manual testing.

## 11.2 Required fixture families
The repo should maintain reusable fixtures for at minimum:
- locales and mixed-language strings,
- ritual sessions and RIC scenarios,
- citation and remedy bundles,
- pack manifests and inventory states,
- map anchors, routes, and low-confidence states,
- group boards and regroup pins,
- planner/wallet/note examples,
- entitlement snapshots,
- onboarding completion states,
- stale-content and stale-cache cases.

## 11.3 Sensitive-data rule
Never use real pilgrim medical data, real production receipts, private group data, or real personal notes in tests or screenshots.

## 11.4 Deterministic-content-version rule
Governed content fixtures must declare explicit content versions and schema versions so regression triage remains traceable.

## 11.5 Fault-injection fixture rule
Maintain fixtures for deliberate failure states such as:
- corrupt pack checksum,
- missing localization key,
- stale entitlement snapshot,
- unsupported content version,
- missing route graph,
- denied permission,
- offline startup,
- pack purge while feature still references the pack.

---

# 12. Unit, domain, and repository test strategy

## 12.1 Purpose
Unit and domain tests should prove business rules at the fastest reliable layer.

## 12.2 Required coverage categories
At minimum, unit/domain tests should cover:
- startup resolver branching,
- season and recommendation logic,
- ritual step progression and counter logic,
- RIC/resolver evaluation rules,
- remedy lookup and fallback behavior,
- phrase search/ranking,
- emergency-card field interpolation,
- pack state machines,
- entitlement gate mapping,
- local migration logic,
- stale-state labeling,
- offline queue policies,
- sorting and priority logic on Home.

## 12.3 Repository-level verification
Repository tests must verify:
- local-first read behavior,
- stale cache handling,
- merge semantics,
- idempotency,
- serialization integrity,
- corruption rejection,
- downgrade-safe reads where relevant.

## 12.4 No-widget-logic-leak rule
Logic that must be stable under test should live outside widgets where practical so domain tests can prove it cheaply and clearly.

---

# 13. Widget, screen-state, and semantics test strategy

## 13.1 Purpose
Widget tests prove that high-risk states render and interact correctly without waiting for broad E2E runs.

## 13.2 Required widget-test categories
At minimum, widget tests should cover:
- empty/loading/error/degraded/success states,
- key button and route wiring,
- card priority and visibility rules,
- lock-state and restore-state messaging,
- safety-banner placement rules,
- phrase card layouts,
- Simple Mode shell differences,
- offline status communication,
- stale-state labels,
- selected semantic labels and focus order where deterministic.

## 13.3 Semantics verification rule
High-risk accessibility semantics should be asserted where Flutter test tooling can reliably do so, especially for:
- emergency shortcuts,
- Join / I’m Safe / Route / Copy actions,
- key Home cards,
- pack install controls,
- phrasebook big-text actions.

## 13.4 Widget-flake rule
Widget tests must remain deterministic. Do not rely on uncontrolled animations, real timers, or external services.

---

# 14. Golden and visual regression strategy

## 14.1 Purpose
Golden tests catch high-signal visual regressions in carefully selected surfaces.
They are not a substitute for accessibility or real-device proof.

## 14.2 Golden-test selection rule
Use golden tests only for surfaces where visual structure matters and deterministic rendering is feasible.

## 14.3 Recommended golden targets
Recommended baseline targets include:
- onboarding welcome,
- Home Root standard,
- Home Root simple mode,
- emergency card big text,
- phrase card Arabic + translation + transliteration layout,
- pack install states,
- subscription lock state,
- stale/live group board states,
- selected ritual step surfaces,
- selected map fallback or saved-anchor states that do not depend on live rendering engines.

## 14.4 Golden-variant dimensions
Where practical, golden coverage should include:
- light/dark theme as supported,
- standard and large text,
- LTR and RTL,
- selected narrow and tall aspect ratios.

## 14.5 Golden-limit rule
Do not create a massive brittle screenshot suite. Prefer a small set of high-risk, high-signal golden cases.

---

# 15. Integration and end-to-end strategy

## 15.1 Purpose
Integration tests should validate critical flows across modules and persistence boundaries.

## 15.2 Canonical integration suite groups
The integration suite should be organized around high-value journey groups.

### A. Startup and Home
- first launch online,
- first launch offline,
- onboarding completion,
- Simple Mode persistence,
- deep-link fallback,
- return to correct Home state.

### B. Ritual and governed content
- start Umrah session,
- resume session from Home,
- open step detail,
- run offline RIC scenario,
- show remedy,
- load correct content version or last-known-good fallback.

### C. Maps and saved anchors
- save anchor,
- recall anchor offline,
- route preview with pack present,
- pack missing fallback,
- route launch from regroup pin.

### D. Group and shared coordination
- join flow,
- check-in or I’m Safe flow,
- fallback share path when network weak,
- stale-state communication.

### E. Packs and offline assets
- browse cached manifest,
- install pack,
- verify ready state,
- fail checksum,
- purge and recover,
- audio availability after install.

### F. Account and entitlements
- account gate only when required,
- purchase/restore happy path in test environments,
- cached entitlement continuity offline,
- downgrade-safe behavior.

### G. Assistive and emergency
- emergency shortcut from Home,
- phrasebook retrieval offline,
- big-text display,
- medical-profile local flow,
- text-only fallback when audio unavailable.

## 15.3 Integration-test restraint rule
Not every permutation belongs in full integration. The suite should target critical cross-boundary proof, not exhaustive combinatorics.

## 15.4 Physical-device promotion rule
Any integration scenario involving notifications, purchases, asset delivery, device restart, performance, map positioning, or OS accessibility must be promoted to physical-device validation if emulator/simulator proof is insufficient.

---

# 16. Platform-native and bridge test strategy

## 16.1 Purpose
Flutter does not remove the need to test platform-native bridges where product behavior depends on them.

## 16.2 iOS-specific required areas
At minimum, iOS-specific verification should cover:
- controlled glass/material behavior under reduced transparency or contrast settings,
- notification permission and scheduling behavior,
- purchase and restore bridging,
- asset/background-delivery behavior if used,
- map-native wrapper behavior on supported iOS versions,
- platform-specific subscription management handoffs.

## 16.3 Android-specific required areas
At minimum, Android-specific verification should cover:
- platform-adapted surface and navigation behavior,
- Play purchase bridge behavior,
- asset-delivery/download integration,
- notification channels and scheduling behavior,
- low-memory/background relaunch behavior where critical,
- back navigation and external-intent handoffs.

## 16.4 Recommended tool posture
Use platform-native or bridge-appropriate automation where needed, such as:
- Flutter integration tests for cross-platform flows,
- platform-native test layers for native plugins or wrappers,
- Espresso or UI Automator on Android where system-level interactions matter,
- XCTest UI/performance testing on Apple platforms where native visibility is required.

## 16.5 Bridge-contract rule
Every non-trivial native bridge should have:
- contract tests at the Flutter boundary,
- at least one platform-specific verification path,
- error-path verification,
- version compatibility notes where platform behavior differs.

---

# 17. Content, schema, and governed-publication validation strategy

## 17.1 Purpose
Governed content is part of runtime correctness and must be tested like code.

## 17.2 Required validation layers
For governed content and publication candidates, verify at minimum:
- schema correctness,
- referential integrity,
- locale completeness,
- bidi safety where applicable,
- transliteration structure,
- citation reference validity,
- artifact metadata completeness,
- required review-record presence,
- runtime compatibility with the app build,
- last-known-good fallback behavior.

## 17.3 Ritual-specific regression suites
Maintain stable regression suites for:
- supported Umrah paths,
- representative RIC scenarios,
- remedy rendering,
- season gating,
- Hajj leakage prevention,
- content-version mismatch behavior.

## 17.4 Publication candidate certification rule
A governed content publication candidate is not release-ready unless both content-level validation and app-runtime compatibility checks pass.

## 17.5 No screenshot-only governance rule
A visual review of rendered religious content is not enough evidence without structured validation and version traceability.

---

# 18. API contract, backend, and sync verification strategy

## 18.1 Purpose
The product has a deliberately limited online surface. That surface must remain stable and predictable.

## 18.2 Required API verification categories
At minimum, verify:
- request/response schema compatibility,
- auth and authorization expectations,
- idempotency where required,
- stale cache behavior,
- ETag/manifest refresh behavior,
- protected-route failures,
- normalized error-shape expectations,
- receipt validation flows,
- flags and pack manifest compatibility.

## 18.3 Contract-test rule
The backend surface should expose contract verification that runs before release candidates are certified, especially for:
- `/v1/flags`,
- `/v1/packs/manifest`,
- `/v1/entitlements`,
- group/protected coordination endpoints,
- purchase validation or restore support endpoints.

## 18.4 Client-backend compatibility rule
The release candidate app must be validated against the intended backend contract version and against compatible degraded or stale-cache behavior when the backend is unavailable.

---

# 19. Offline, weak-network, and recovery testing strategy

## 19.1 Purpose
Offline-first claims are meaningless unless offline and weak-network behavior are first-class test dimensions.

## 19.2 Required network states in the matrix
The canonical matrix must include at minimum:
- fully offline,
- weak/intermittent network,
- online with stale local state,
- online with slow backend response,
- transition from offline to online.

## 19.3 Required offline validation categories
At minimum, verify:
- startup routing offline,
- Home usefulness offline,
- ritual runtime offline,
- phrasebook and emergency offline,
- saved anchor recall offline,
- cached group or pack states with honest freshness messaging,
- queued telemetry/event handling,
- no false “live” implication when data is stale.

## 19.4 Interruption-and-recovery rule
The matrix should explicitly include interruptions such as:
- app kill and relaunch,
- device restart,
- background/foreground transition,
- permission denial then later grant,
- partial download then resume,
- account state change after cached local use.

## 19.5 Recovery evidence rule
A feature claiming graceful recovery must show evidence of recovery, not only of initial success.

---

# 20. Localization, RTL, and accessibility testing strategy

## 20.1 Purpose
Localization and accessibility are core product quality dimensions, not translation polish workstreams.

## 20.2 Required localization checks
At minimum, verify:
- missing-key detection,
- locale fallback behavior,
- text overflow and clipping,
- mixed Arabic and Latin rendering,
- numerals/date/time formatting,
- translated lock/error/support copy consistency,
- supported-language startup/onboarding flows.

## 20.3 Required RTL checks
RTL validation must include at minimum:
- shell navigation,
- Home and Simple Home,
- Rituals,
- emergency and phrasebook,
- group join and regroup,
- pack catalog/detail,
- map instructions and overlays where supported,
- settings and account flows.

## 20.4 Required accessibility settings checks
At minimum, device validation should cover:
- larger text sizes,
- bold text where supported,
- reduced transparency / increased contrast on iOS where relevant,
- screen readers,
- focus order and labels,
- touch-target clarity,
- motion/transparency combinations where platform settings affect legibility.

## 20.5 Assistive-technology rule
Critical flows must be tested with real assistive technologies, not only visual inspection.

## 20.6 Accessibility-audit rule
The process should use platform and framework accessibility tooling where useful, but passing automated audits is not enough without scenario-based usability checks.

---

# 21. Performance, battery, memory, and rendering verification

## 21.1 Purpose
Performance budgets from file `17` are release contracts and must be proven on supported devices.

## 21.2 Required measured areas
At minimum, certification must verify:
- cold/warm/hot startup,
- first meaningful frame and home-ready duration,
- critical screen open latency,
- emergency-root open speed,
- ritual-step open speed,
- map render and route-preview responsiveness,
- pack install feedback responsiveness,
- scroll smoothness on high-risk screens,
- memory pressure and low-memory recovery behavior where possible.

## 21.3 Supported-device performance rule
Performance evidence must include at least:
- one minimum-supported or low-end representative device per platform,
- one representative mid-tier device per platform,
- optionally one higher-tier sanity device for diagnosis, not for quality signoff.

## 21.4 Jank and frozen-state rule
A screen that is logically correct but visibly janky in critical use remains a release-quality issue.

## 21.5 Battery and thermal sanity rule
For map, audio, and repeated active-use sessions, perform sanity checks for excessive battery or thermal behavior on representative devices even if exhaustive lab instrumentation is deferred.

---

# 22. Canonical device-lab strategy

## 22.1 Device-lab purpose
The device lab exists to validate the supported product truth, not to collect a vanity museum of phones.

## 22.2 Device-lab composition
The canonical lab should combine:
- local emulators/simulators for fast iteration,
- cloud devices for broad automated coverage,
- physical Android phones,
- physical iPhones,
- optionally one or more tablets only if product scope requires meaningful tablet verification.

## 22.3 Required device buckets per platform
Maintain at minimum these buckets:
- **minimum-supported bucket** — slowest/oldest supported profile that still represents the release bar,
- **representative mid-tier bucket** — the main confidence device class,
- **current-platform bucket** — recent OS/device coverage for adaptation changes,
- **special-condition bucket** — device(s) used for storage pressure, low-memory, accessibility, or field-validation tasks.

## 22.4 Bucket-over-model rule
This spec intentionally prioritizes buckets over fixed device model names so the lab can evolve without rewriting the whole quality contract every time the market changes.

## 22.5 OS coverage rule
Each release candidate must be validated on:
- the minimum supported OS range actually promised by the product,
- at least one current major OS release per platform,
- any additional OS version where platform-specific regressions are known or suspected.

## 22.6 Cloud-device rule
Cloud device infrastructure is appropriate for scalable regression checks, but it does not replace physical-device validation for the highest-risk behaviors.

## 22.7 Physical-device mandatory areas
Physical-device proof is mandatory for at minimum:
- purchases and restore,
- push/notification permission flows,
- pack install/purge/restart behavior,
- map and movement-oriented validation,
- real screen-reader checks,
- reduced-transparency/increased-contrast behavior,
- performance certification,
- field and stress validation.

---

# 23. Canonical test matrix dimensions

## 23.1 Matrix purpose
The matrix exists to prevent accidental blind spots.
It is not a command to run every possible combination.

## 23.2 Required dimensions
The canonical matrix should include at minimum these dimensions:
- platform,
- OS tier,
- device bucket,
- network state,
- locale and text direction,
- accessibility settings state,
- entitlement/account state,
- season/scope state,
- pack/content availability state,
- permission state,
- app lifecycle/interruption state,
- data freshness state.

## 23.3 Canonical value sets
### Platform
- iOS
- Android

### OS tier
- minimum supported
- representative stable
- current release

### Device bucket
- minimum-supported / low-end representative
- mid-tier representative
- current-platform representative

### Network state
- offline
- weak/intermittent
- normal online
- slow backend / stale data

### Locale and direction
- English/LTR baseline
- Arabic/RTL baseline
- Indonesian/LTR baseline
- mixed Arabic + user-language display cases

### Accessibility state
- default
- large text
- screen reader on
- reduced transparency / increased contrast where applicable

### Entitlement/account state
- signed out, free
- signed in, free
- supporter active
- supporter expired or downgraded
- cached entitlement offline

### Season/scope state
- Umrah default
- Hajj-enabled or seasonal scope only when explicitly supported

### Pack/content state
- no pack installed
- relevant pack installed
- pack installed but stale metadata
- pack missing/corrupt/purged
- governed content current
- governed content last-known-good fallback

### Permission state
- location allowed / denied / limited where relevant
- notifications allowed / denied
- media/file/camera permissions as feature-relevant

### Lifecycle/interruption state
- cold start
- warm start
- hot resume
- app kill and relaunch
- reboot/restart where relevant

## 23.4 Risk-based matrix selection rule
Each feature or release candidate should select a tractable set of combinations from the matrix based on risk. The matrix is a decision framework, not a brute-force obligation.

---

# 24. Canonical scenario matrix by feature family

## 24.1 Startup, Home, and Simple Mode
Required scenario families:
- first launch online,
- first launch offline,
- return launch with active ritual,
- return launch with saved anchor,
- Simple Mode enabled,
- large text Home,
- emergency shortcut from Home,
- deep-link failure fallback.

## 24.2 Rituals and governed content
Required scenario families:
- begin Umrah session,
- resume from active step,
- offline RIC answer flow,
- remedy display,
- governed content current version,
- governed content fallback to last-known-good,
- Arabic + localized content readability,
- season-gating safety.

## 24.3 Maps and Save My Gate
Required scenario families:
- save current anchor,
- recall anchor offline,
- route preview with pack,
- route fallback without pack,
- low-confidence positioning,
- floor-change comprehension,
- weak device 2D fallback,
- route launch from regroup pin.

## 24.4 Group coordination
Required scenario families:
- join by code,
- signed-out gate then recover,
- I’m Safe / check-in under weak network,
- stale live-board messaging,
- leader regroup pin create/update,
- route handoff to Maps.

## 24.5 Phrasebook, emergency, assistive
Required scenario families:
- phrase retrieval offline,
- big-text phrase display,
- audio installed vs missing,
- emergency root with sparse data,
- medical-profile local flow,
- safety-banner presence and non-presence rules,
- Home/Simple Mode emergency shortcut reachability.

## 24.6 Packs and offline assets
Required scenario families:
- discover recommended pack,
- install, verify, and ready state,
- checksum failure,
- low storage preflight,
- purge and recovery,
- offline browse from cached manifest,
- post-install feature handoff.

## 24.7 Account, subscriptions, settings
Required scenario families:
- first use without account,
- account gate only when required,
- purchase on each platform test path,
- restore on reinstall/new device path,
- expiry/downgrade reflection,
- offline use with cached entitlement snapshot,
- subscription management handoff.

---

# 25. Automation lane design

## 25.1 PR / merge lane
The pull-request lane should remain fast and include at minimum:
- lint/format/generation checks,
- selected unit tests,
- selected widget tests,
- fast canary integration suite,
- changed-area or impacted-package checks where supported.

## 25.2 Mainline lane
The mainline lane should include a broader regression set, including:
- wider unit and widget coverage,
- golden checks,
- key integration suites,
- governed-content validation,
- contract checks,
- selected cloud-device runs if budget allows.

## 25.3 Release-candidate lane
The release lane should include:
- all gating automated suites,
- required cloud-device coverage,
- required physical-device certification checklist,
- performance budget evidence,
- release evidence bundle.

## 25.4 Flake-handling rule
Flaky tests are a quality bug.
They must be triaged, stabilized, quarantined with owner and expiry, or removed and replaced with a stronger signal.

## 25.5 Retry restraint rule
Retries may reduce infrastructure noise, but they must not be used to hide real regressions.

---

# 26. Beta, pre-launch, and external validation posture

## 26.1 Internal beta requirement
Before general release, release candidates should go through internal beta testing on real devices.

## 26.2 Platform beta-channel posture
Recommended platform channels include:
- internal or closed testing tracks on Google Play,
- TestFlight groups on Apple platforms,
- cloud-device and pre-launch style automation where appropriate.

## 26.3 Beta-purpose rule
Beta is not a substitute for structured QA. It is a final confidence and reality-check layer after disciplined verification, not before.

## 26.4 Pre-launch-report posture
Android pre-launch style automated device scanning can add useful signal, but it must supplement rather than replace the project’s own matrix and critical-flow validation.

## 26.5 Tester-cohort rule
Beta testers should include at least:
- internal product/engineering contributors,
- cross-language reviewers,
- accessibility-aware testers,
- low-confidence or non-expert users where possible,
- scenario-relevant testers for travel and stress conditions.

---

# 27. Defect severity, release blockers, and waiver policy

## 27.1 Severity posture
Defect severity must be based on user harm, trust impact, and release risk, not only technical elegance.

## 27.2 Automatic release blockers
The following are release blockers unless an explicit exception is approved at the highest accountable level:
- crash or startup failure in critical flows on supported devices,
- ritual correctness or governed-content mismatch in supported scenarios,
- emergency/phrase critical path failure,
- Save My Gate or map fallback failure in supported baseline scenarios,
- broken restore or entitlement misrepresentation,
- corrupted or unsafe pack installation truth,
- severe RTL/accessibility breakage in critical flows,
- performance fail-threshold breach for critical flows on supported devices,
- dishonest stale/live-state communication,
- missing required release evidence.

## 27.3 Conditional blockers
The following may be blockers depending on scope and severity:
- non-critical visual regressions,
- secondary-flow friction,
- minor translation defects outside critical surfaces,
- high-but-not-fail performance warnings,
- issues isolated to explicitly unsupported combinations.

## 27.4 Waiver rule
A waiver must include at minimum:
- issue description,
- severity rationale,
- affected matrix slice,
- user impact,
- mitigation,
- owner,
- deadline or expiration,
- reason release is still acceptable.

## 27.5 No silent known-bug rule
Known release-relevant bugs must not remain tribal knowledge only.

---

# 28. Required release evidence bundle

## 28.1 Purpose
A release candidate is not truly reviewable without a compact evidence bundle.

## 28.2 Required evidence categories
The release evidence bundle should contain at minimum:
- automated suite summary,
- changed-area risk summary,
- unresolved known issues and waivers,
- device-lab certification checklist results,
- performance budget evidence,
- accessibility/RTL verification summary,
- offline/degraded-state verification summary,
- governed-content/publication compatibility evidence when content changed,
- purchase/restore evidence when monetization code changed,
- field-validation notes for features that require them.

## 28.3 Evidence format rule
Evidence should be concise, auditable, and easy to review.
Screenshots or videos may help, but they do not replace structured results.

## 28.4 Change-aware evidence rule
Evidence depth should scale with what changed.
A content-only change does not require the same evidence as a map-renderer change, but both still require explicit justification.

---

# 29. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 29.1 Treating one happy-path demo as release proof
Forbidden.

## 29.2 Testing only on high-end developer devices
Forbidden.

## 29.3 Shipping with known critical accessibility or offline regressions because “most users won’t hit them”
Forbidden.

## 29.4 Using live production user data as ordinary test data
Forbidden.

## 29.5 Letting AI-generated tests replace human scenario judgment for critical flows
Forbidden.

## 29.6 Marking flaky failures as passed without owner and cleanup plan
Forbidden.

## 29.7 Claiming graceful degradation without degraded-state verification
Forbidden.

## 29.8 Treating simulator-only map, purchase, notification, or accessibility checks as sufficient release evidence
Forbidden.

## 29.9 Ignoring low-end or minimum-supported device performance because flagship devices are smooth
Forbidden.

## 29.10 Mutating the test matrix ad hoc to avoid uncomfortable failures
Forbidden.

---

# 30. Implementation priorities, update triggers, and summary

## 30.1 Phase 1 priorities
Implement first:
- shared testkit utilities,
- fast PR lane,
- domain/widget coverage for critical modules,
- canonical integration canary suite,
- minimum device buckets and certification checklist,
- offline/degraded-state scenarios for critical flows.

## 30.2 Phase 2 priorities
Then add:
- broader golden coverage,
- richer cloud-device coverage,
- performance evidence automation,
- governed-content publication compatibility suites,
- stronger accessibility and RTL automation.

## 30.3 Phase 3 priorities
Then refine:
- more field-validation discipline,
- better flake diagnostics and quarantining workflows,
- smarter risk-based matrix selection tooling,
- improved release evidence packaging.

## 30.4 When this file must be updated
This file must be updated whenever any of the following changes:
- supported device or OS posture,
- critical feature risk priorities,
- required release evidence,
- matrix dimensions,
- CI lane structure,
- beta/pre-launch validation strategy,
- blocker or waiver policy,
- governed-content runtime validation posture,
- accessibility or offline release bar.

If these truths change but this file is not updated, release quality and testing effort will drift quickly.

## 30.5 Summary
This file defines the canonical testing strategy for Pilgrims Mobile App.

It establishes:
- the quality philosophy and pyramid posture,
- the required test layers,
- the environment and automation lanes,
- the device-lab and matrix strategy,
- the critical scenario families per feature area,
- the release-blocking criteria,
- the evidence required before release.

Its purpose is to ensure that Pilgrims Mobile App is verified not only for correctness in code, but for calmness, accessibility, offline resilience, platform honesty, and real-world trust under pilgrimage conditions.
