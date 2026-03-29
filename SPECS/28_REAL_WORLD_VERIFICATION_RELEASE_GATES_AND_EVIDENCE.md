# 28 — REAL-WORLD VERIFICATION, RELEASE GATES, AND EVIDENCE

## Document status
- **Type:** Normative release-readiness, real-world verification, and evidence specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, QA lead, release owner, Flutter engineers, backend engineers, content/governance contributors, operations contributors, reviewer agents, release agents
- **Purpose:** Define the canonical real-world verification model, release-candidate evidence requirements, feature-family manual verification expectations, go/no-go gates, known-issue handling, sign-off responsibilities, and release-proof package required before Pilgrims Mobile App can be treated as ready to ship.
- **Authority level:** This file is the canonical source of truth for release-readiness proof. If dashboards, QA notes, beta feedback, CI status, or release habits conflict with this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`, `21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`, `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`, `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`, `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`
- **Related files:** `05`, `29`, `30`

---

# 1. Purpose of this file

This file exists because a release can look healthy long before it is actually safe for real pilgrims.

For this project, fake success is especially dangerous because:
- the app is often used while the user is tired, stressed, rushed, elderly, low-confidence with smartphones, or under social pressure,
- offline and degraded-state behavior is part of the core product promise rather than an optional enhancement,
- route-following, saved-anchor recovery, emergency access, and phrase support can fail in ways that only appear on real devices and real networks,
- purchase, restore, entitlement, notification, and asset-delivery flows often behave differently after reinstall, reboot, backgrounding, or low-storage pressure,
- governed religious content can be structurally valid yet still fail runtime readability, locale safety, or trust expectations,
- AI-assisted implementation can produce green tests and polished demos that do not prove real-world readiness.

This file prevents those failures by defining:
- what counts as real release evidence,
- how a release candidate must be manually and operationally verified,
- which feature families require on-device or field proof,
- how evidence depth scales with release risk,
- which conditions block release,
- who must sign off,
- and what must be recorded when known issues remain.

---

# 2. Release purpose and user value

## 2.1 Module purpose
This module exists to ensure that release decisions are based on trustworthy proof rather than intuition, optimism, or demo success.

## 2.2 User value statement
A pilgrim should not need to think about release gates directly.

The value to the pilgrim is that:
- first launch and Home feel understandable,
- urgent help remains reachable,
- ritual guidance stays trustworthy,
- maps and saved anchors remain useful under pressure,
- the app remains usable offline,
- platform adaptation does not make critical screens harder to read,
- subscription and restore behavior do not surprise users,
- release quality does not collapse when real conditions differ from the lab.

## 2.3 Operational value statement
The team should be able to answer questions like:
- What proof do we have that this release candidate works in real conditions?
- Which checks were done on physical devices?
- Which checks were done on weak or absent network?
- Which features were field-validated rather than only lab-tested?
- What evidence exists for maps, packs, purchases, and accessibility?
- What known issues remain, who owns them, and why are they acceptable or unacceptable?

---

# 3. Scope and boundaries

## 3.1 In scope
This file includes:
- release-candidate verification posture,
- manual verification structure,
- on-device proof requirements,
- real-network and offline verification rules,
- feature-family real-world checks,
- evidence packaging rules,
- sign-off responsibilities,
- go/no-go gates,
- known-issue and waiver policy as applied to release approval,
- seasonal and high-risk release-evidence escalation.

## 3.2 Out of scope
This file does **not** replace:
- automated testing strategy,
- device-lab composition rules,
- incident response runbooks,
- security/privacy policy,
- deployment steps,
- the underlying feature contracts.

Those are owned by related files. This file defines how release readiness is proven across them.

## 3.3 Boundary with file `27`
File `27` defines how the product is tested across layers, environments, devices, and matrices.

This file defines:
- what proof must exist at release-candidate time,
- which manual/field checks are still required after automation,
- how evidence is packaged and reviewed,
- who can approve or block release.

## 3.4 Boundary with file `26`
File `26` defines governed-content workflow, scholar review, content validation, and emergency correction.

This file defines the release evidence required when governed content changes affect what ships in the app runtime.

## 3.5 Boundary with file `30`
File `30` should define release operations, rollback procedure, hotfix workflow, and ongoing incident handling.

This file defines the proof required before something is considered ready to ship, not the operational steps after approval.

## 3.6 Boundary with feature-family files
Feature files `18` through `25` define what each feature family must prove before release.

This file converts those requirements into:
- one unified release-candidate checklist,
- one evidence bundle shape,
- one sign-off system.

---

# 4. Product rules that govern release verification

## 4.1 No-demo-as-proof rule
A successful happy-path demo is not release evidence.

## 4.2 Real-conditions rule
If the product claims offline usefulness, stress readability, degraded-state honesty, or low-confidence fallback, those claims must be proven under representative conditions before release.

## 4.3 Physical-device rule
A release candidate is not ship-ready unless required high-risk flows have been validated on physical devices, not only simulators, emulators, or mocks.

## 4.4 Critical-flows-first rule
Release proof must prioritize critical pilgrim outcomes before lower-priority polish.

Critical outcomes include at minimum:
- startup and first usable state,
- Home recovery behavior,
- ritual guidance and RIC,
- phrasebook and emergency access,
- Save My Gate and map fallback,
- group safety/regroup flows,
- pack install and recovery flows,
- account, restore, and entitlement continuity where relevant.

## 4.5 Honest-evidence rule
Evidence must reflect what was truly verified.
The team must not represent:
- simulator checks as device proof,
- lab Wi-Fi checks as real weak-network proof,
- visual inspection as accessibility proof,
- structured content validation as scholar sign-off,
- screenshots alone as behavioral proof.

## 4.6 Change-aware rule
Evidence depth must scale with release risk.
Map, native-bridge, entitlement, migration, offline-pack, and governed-content releases require stricter proof than small internal copy changes.

## 4.7 No hidden blocker rule
Known blocker-class issues must not be buried inside chat threads, memory, or informal comments.

## 4.8 No ethical shortcut rule
Release pressure must not override correctness, accessibility, privacy-light behavior, or emergency/ritual trust requirements.

## 4.9 Umrah-first release rule
Unless scope explicitly expands, release verification must prove the Umrah-first experience before any broader seasonal or optional complexity is treated as release-complete.

## 4.10 Field-proof rule
Where a feature’s value depends on movement, stress, or environmental reality, at least some representative field proof is mandatory before claiming release confidence.

---

# 5. Canonical terminology for this module

## 5.1 Release candidate
A build and configuration state being evaluated for possible shipment.

## 5.2 Real-world verification
Verification performed under representative device, network, environment, movement, readability, and interruption conditions rather than only deterministic lab conditions.

## 5.3 Evidence bundle
The compact, auditable package of results that explains why a release candidate should or should not ship.

## 5.4 Gate
A required release decision point with explicit pass/fail criteria.

## 5.5 Blocker
A defect, missing proof item, or unresolved risk that prevents release unless a waiver is explicitly approved.

## 5.6 Conditional blocker
An issue that may or may not block release depending on user impact, affected scope, mitigation, and release context.

## 5.7 Waiver
An explicit decision to proceed despite a known issue, with documented owner, rationale, mitigation, and expiration.

## 5.8 Field validation
Representative real-environment validation, such as movement-based testing, real network variation, glare/readability checks, or stress-oriented usability verification.

## 5.9 Evidence owner
The accountable human role responsible for making sure a given piece of release proof exists and is trustworthy.

## 5.10 Sign-off
The explicit accountable approval from a required role stating that the release candidate has met the defined gate for that role’s domain.

---

# 6. Release-candidate verification model

## 6.1 Canonical verification stages
Every release candidate should move through these stages in order:
1. automated gate pass,
2. device-lab certification complete,
3. release-candidate manual verification complete,
4. field or real-network validation complete where required,
5. evidence bundle assembled,
6. sign-off review and go/no-go decision.

## 6.2 Stage-separation rule
Passing an earlier stage never removes the need for later stages when those later stages are required by risk level.

## 6.3 Certification posture
The team should treat certification as proving release safety, not merely searching for extra bugs after code is “done.”

## 6.4 Time-of-proof rule
Evidence must correspond to the actual release candidate or clearly explain why shared evidence from an unchanged area remains valid.

---

# 7. Release-risk classification and evidence depth

## 7.1 Purpose
Not all releases require the same depth of proof.
This section defines how evidence scales.

## 7.2 Risk class A — low-risk content or copy release
Typical examples:
- non-critical copy cleanup,
- non-meaning-changing translation fix,
- low-risk settings copy adjustment,
- static help clarification.

### Required evidence depth
- automated regression summary,
- impacted-screen manual verification,
- locale/RTL check if applicable,
- updated known-issues section,
- lightweight sign-off.

## 7.3 Risk class B — standard feature/UI release
Typical examples:
- onboarding/Home layout changes,
- planner workflow changes,
- phrasebook UI changes,
- routine non-native feature logic changes.

### Required evidence depth
- full affected-area automation summary,
- physical-device checks on representative buckets,
- offline/degraded checks where relevant,
- accessibility checks on impacted surfaces,
- concise video or screenshot proof for key flows,
- full sign-off from QA plus feature owner.

## 7.4 Risk class C — high-risk platform or runtime release
Typical examples:
- map/rendering changes,
- pack install pipeline changes,
- purchase/restore changes,
- deep-link or startup resolver changes,
- state migration changes,
- notification behavior changes.

### Required evidence depth
- all class B evidence,
- multi-device physical proof,
- interruption/restart verification,
- weak-network or offline proof,
- field validation where relevant,
- performance evidence,
- release-owner review.

## 7.5 Risk class D — governed-content or trust-critical release
Typical examples:
- ritual content changes,
- RIC/remedy logic changes,
- scholar-sensitive translation changes,
- emergency-card or official-handoff changes.

### Required evidence depth
- all relevant class B/C evidence,
- governed-content validation summary,
- scholar/content approval evidence where required,
- runtime compatibility proof,
- last-known-good fallback proof where relevant,
- content/governance sign-off.

## 7.6 Risk class E — seasonal or multi-risk release
Typical examples:
- combined map + packs + content + onboarding release,
- pre-season release for high-traffic use,
- major scope or architecture milestone.

### Required evidence depth
- all required evidence from affected classes,
- widened device and locale coverage,
- expanded field validation,
- expanded blocker review,
- explicit founder or accountable release-owner go/no-go.

---

# 8. Ownership and sign-off responsibilities

## 8.1 Shared responsibility rule
Release readiness is a shared accountability system, not the job of QA alone.

## 8.2 Engineering sign-off responsibility
Engineering must confirm:
- code changes are complete for scope,
- automated gates passed or are honestly waived,
- crashers and high-severity regressions are resolved or explicitly documented,
- logs and diagnostics are available for unresolved issues.

## 8.3 QA sign-off responsibility
QA must confirm:
- required manual verification is complete,
- required device and environment coverage was met,
- evidence bundle is coherent,
- known issues and waivers are accurately represented.

## 8.4 Product sign-off responsibility
Product must confirm:
- critical flows still feel calm and understandable,
- the user promise remains intact,
- the release does not regress core trust outcomes,
- tradeoffs in any waiver are acceptable from a user-value perspective.

## 8.5 Content/governance sign-off responsibility
When governed content changed, content/governance must confirm:
- the correct content version is shipping,
- required approvals exist,
- the runtime presentation still matches approved meaning,
- emergency correction or fallback risks are understood.

## 8.6 Release owner responsibility
The release owner must confirm:
- required sign-offs exist,
- blockers are resolved or explicitly waived,
- no unowned risk remains,
- the release candidate is eligible for shipment according to this file.

## 8.7 AI-agent boundary
AI agents may help assemble summaries, checklist drafts, or issue clustering, but they must not self-approve release or silently reduce the evidence bar.

---

# 9. Evidence principles and quality rules

## 9.1 Concise-but-auditable rule
Evidence should be compact enough to review quickly and detailed enough to audit later.

## 9.2 Reproducibility rule
Where a failure or known issue exists, the evidence bundle should include enough context to reproduce it.

## 9.3 Source-truth rule
Structured test reports, device notes, logs, or captured outputs are stronger evidence than memory or chat summaries.

## 9.4 Media-evidence rule
Screenshots and videos are useful supporting proof, especially for UI, map, accessibility, and degraded-state behavior, but they do not replace structured result summaries.

## 9.5 Environment-truth rule
Evidence must record enough environment detail to interpret results correctly, including where relevant:
- platform,
- OS tier,
- device bucket,
- app build identifier,
- network condition,
- locale,
- accessibility state,
- account/entitlement state,
- content/pack version.

## 9.6 Privacy-light evidence rule
Evidence collection must not include unnecessary personal data, precise private location history, private medical data, or real user-authored content.

## 9.7 Evidence-expiry rule
Old evidence can support unchanged areas, but it must not be treated as fresh proof once affected flows, dependencies, or device assumptions have changed.

---

# 10. Canonical release evidence bundle

## 10.1 Required top-level sections
Every release candidate evidence bundle should contain at minimum:
- release summary,
- change-risk classification,
- build identifiers,
- automated verification summary,
- device-lab certification summary,
- manual verification summary,
- field/real-network validation summary where required,
- performance summary,
- accessibility/RTL/localization summary,
- governed-content summary when content changed,
- monetization/purchase summary when relevant,
- store/privacy/compliance summary where relevant,
- known issues and waivers,
- sign-off section,
- final recommendation.

## 10.2 Minimum release summary fields
The release summary should include:
- release candidate identifier,
- intended platform(s),
- intended scope,
- change synopsis,
- risk class,
- release owner,
- date of evidence review.

## 10.3 Minimum environment fields
The evidence bundle should capture where relevant:
- app version/build number,
- backend or config environment,
- content artifact version(s),
- pack manifest version,
- locale set used,
- entitlement test state,
- device bucket coverage,
- OS version coverage.

## 10.4 Evidence-location rule
Artifacts such as logs, screenshots, videos, dashboards, and test reports should be referenced consistently so future contributors can find them.

## 10.5 Missing-evidence rule
If a required evidence section is missing, that is itself a release issue, not a formatting nit.

## 10.6 Store and compliance evidence rule
Where relevant, the evidence bundle must include:
- current App Store / Google Play disclosure review against actual build behavior,
- privacy manifest / required-reason API / third-party SDK signature review status for iOS submissions where applicable,
- Data safety and account/data-deletion review status for Google Play submissions where applicable,
- verification that any user-facing deletion links or support pages actually load and match the shipped account behavior,
- any sensitive-permission, health, or medical declarations required by the release scope.

---

# 11. Manual verification posture

## 11.1 Purpose
Manual verification exists to prove usability, clarity, degraded-state honesty, and cross-feature behavior that automation alone cannot fully prove.

## 11.2 Manual verification rule
Manual verification must use representative scenarios rather than random tapping.

## 11.3 Scenario-based posture
Each manual verification slice should identify:
- the user situation,
- preconditions,
- device/environment,
- expected result,
- evidence captured,
- pass/fail outcome,
- issue reference if failed.

## 11.4 Non-expert-user rule
Where possible, at least some manual verification should reflect non-expert use rather than only internal power users who already understand the system.

## 11.5 Stress-clarity rule
Manual verification must explicitly examine:
- action discoverability,
- copy clarity,
- error recoverability,
- whether the screen stays calm and understandable under stress.

---

# 12. On-device verification requirements

## 12.1 Purpose
On-device verification proves behaviors that differ materially from lab-only runs.

## 12.2 Required platform coverage
At minimum, the release candidate should be verified on:
- one minimum-supported or low-end representative physical device per platform,
- one representative mid-tier physical device per platform,
- one current-platform representative when platform-specific changes or regressions justify it.

## 12.3 Required on-device categories
On-device proof is required for at minimum:
- cold and warm launch,
- startup routing,
- first-run behavior when relevant,
- Home and primary navigation,
- degraded/offline critical paths,
- permission interactions,
- notification behavior where relevant,
- purchase/restore where relevant,
- map and saved-anchor flows,
- pack install/resume/purge where relevant,
- screen-reader and large-text checks,
- thermal/performance sanity on critical flows.

## 12.4 Reboot/relaunch rule
If the release touches state persistence, downloads, notifications, entitlements, or packs, verification must include app kill/relaunch and device restart scenarios where relevant.

---

# 13. Real-network verification requirements

## 13.1 Purpose
Wi‑Fi lab success does not prove behavior under real mobile or unstable conditions.

## 13.2 Required real-network states
Where relevant, release verification must cover:
- stable online,
- slow backend response,
- weak or intermittent connectivity,
- network transition from offline to online,
- stale-cached-state presentation.

## 13.3 Required real-network flows
At minimum, real-network verification should cover affected flows such as:
- startup refresh behavior,
- group updates or regroup flows,
- pack browsing or manifest refresh,
- purchase receipt validation and restore,
- any flow that claims graceful retry or stale-state honesty.

## 13.4 Honesty rule
Real-network evidence must prove that the UI represents stale, partial, delayed, or failed network state honestly.

---

# 14. Offline and airplane-mode verification requirements

## 14.1 Purpose
Offline behavior is a product promise and requires explicit proof.

## 14.2 Required offline checks
At minimum, release verification must prove as applicable:
- first launch without network when supported by scope,
- returning launch without network,
- Home usefulness offline,
- ritual runtime offline,
- emergency and phrasebook offline,
- saved anchor recall offline,
- planner/note retrieval offline,
- local pack and audio availability offline,
- stale-but-usable protected summaries where allowed,
- honest communication when live data is unavailable.

## 14.3 Airplane-mode rule
Where offline support is claimed, true airplane-mode verification is preferred over simulated API stubbing alone.

## 14.4 Recovery-from-offline rule
Verification must include transition from offline back to online where the affected feature family claims recovery or refresh behavior.

---

# 15. Interruption, recovery, and lifecycle verification

## 15.1 Purpose
Many real failures appear only after interruption.

## 15.2 Required interruption scenarios
Depending on affected scope, verification should include:
- app background then foreground,
- app kill and relaunch,
- device rotation or orientation changes where relevant,
- permission denied then later granted,
- device reboot for reminders/download continuity where relevant,
- partial download then resume,
- sign-in/out state transitions,
- expired entitlement after cached state existed.

## 15.3 Recovery-proof rule
A release candidate cannot claim resilience unless recovery behavior itself was validated.

---

# 16. Navigation, routing, and deep-link verification

## 16.1 Purpose
The app must stay navigationally trustworthy under real usage.

## 16.2 Required navigation checks
As applicable, verify:
- first-launch routing,
- startup resolver outcomes,
- return-to-Home behavior,
- tab or root navigation integrity,
- back behavior on Android,
- modal/bottom-sheet dismissal safety,
- deep link to supported destinations,
- deep-link failure fallback,
- routing between Home and critical feature families.

## 16.3 No-dead-end rule
Manual verification must confirm there are no confusing dead ends in critical flows.

---

# 17. Feature-family verification — onboarding, Home, and Simple Mode

## 17.1 Required release checks
When onboarding/Home/Simple Mode changed, verify at minimum:
- first launch with network,
- first launch without network,
- continue with essentials path,
- language selection and persistence,
- Simple Mode selection and persistence,
- returning launch into standard Home,
- returning launch into Simple Home,
- urgent shortcut discoverability,
- ritual resume from Home,
- saved gate entry from Home,
- accessibility and readability on large text,
- platform adaptation clarity on iOS and Android.

## 17.2 Required real-world proof
At least one real-user or representative scenario should confirm:
- first-time users understand where to begin,
- stressed users can reach urgent help quickly,
- low-confidence users can complete key Simple Mode tasks,
- Home remains calm rather than crowded.

---

# 18. Feature-family verification — rituals, RIC, and governed content

## 18.1 Required release checks
When ritual flow, resolver logic, remedies, or governed content changed, verify at minimum:
- start and resume ritual flow,
- representative RIC scenarios,
- remedy surfacing and explanation,
- supported locale rendering,
- offline runtime behavior,
- content artifact compatibility,
- last-known-good fallback where applicable,
- no unsupported seasonal leakage,
- no entitlement drift on correctness-critical guidance.

## 18.2 Governed-content evidence
Evidence must include where relevant:
- content artifact version,
- publication candidate or artifact reference,
- required validation summary,
- scholar/content approval references when required,
- runtime screen proof for impacted locales or render modes.

## 18.3 Trust-critical blocker rule
A ritual-correctness mismatch or scholar-sensitive approval gap is a release blocker unless explicitly approved at the highest accountable level.

---

# 19. Feature-family verification — maps, Save My Gate, and route correctness

## 19.1 Required release checks
When map-related behavior changed, verify at minimum:
- Save My Gate create/edit/recall,
- offline anchor recall,
- route preview with and without required packs,
- degraded behavior for missing pack or low confidence,
- floor-change comprehension where supported,
- 2D fallback on weaker or lower-confidence conditions,
- regroup-pin handoff into map routing where relevant,
- map control accessibility basics,
- no fake-live or fake-precision implication.

## 19.2 Route-correctness meaning
Route-correctness verification means proving that the route starts from the intended context, targets the intended destination, communicates floor/transition meaning honestly, and degrades safely when confidence or data is insufficient.
It does **not** claim laboratory-grade physical precision beyond supported capabilities.

## 19.3 Required field validation
At least one representative movement-oriented validation should confirm:
- saved-anchor usefulness,
- route preview comprehension,
- route-follow clarity or fallback usefulness,
- readability under movement or stress,
- permission/confidence degradation honesty.

## 19.4 Map-proof rule
A single impressive internal demo on one flagship phone is not sufficient evidence.

---

# 20. Feature-family verification — group coordination and shared safety

## 20.1 Required release checks
When group features changed, verify at minimum:
- join flow,
- check-in / I’m Safe flow,
- stale-board labeling,
- regroup pin create/update/consume flow where relevant,
- signed-out or permission-limited fallback,
- weak-network behavior,
- route handoff to map when applicable.

## 20.2 Privacy-light proof rule
Evidence must prove functional usefulness without normalizing hidden passive tracking or misleading live-presence assumptions.

---

# 21. Feature-family verification — phrasebook, emergency, safety, and assistive tools

## 21.1 Required release checks
When phrasebook/emergency behavior changed, verify at minimum:
- emergency shortcut from Home and Simple Mode,
- emergency root open speed,
- phrase retrieval offline,
- big-text readability,
- audio installed vs missing fallback,
- local medical-profile or assistive flow where relevant,
- safety banner visibility rules,
- screen-reader clarity of critical actions.

## 21.2 Required urgency proof
Manual verification must confirm that an anxious user can reach help quickly without reading dense instructions or navigating deep menus.

## 21.3 Emergency honesty rule
Emergency surfaces must never imply official support, current verification, or network-backed certainty that the system does not actually possess.

---

# 22. Feature-family verification — planner, wallet, notes, and bookmarks

## 22.1 Required release checks
When personal organization flows changed, verify at minimum:
- planner CRUD offline,
- reminder create/update/delete,
- denied notification permission then later grant,
- reboot or relaunch survival where relevant,
- wallet capture and export,
- note/bookmark capture from supported sources,
- large-text and RTL sanity,
- downgrade-safe behavior where entitlements apply.

## 22.2 Stress-utility rule
Evidence should confirm that these tools still reduce stress rather than create more configuration burden.

---

# 23. Feature-family verification — packs, offline content, and audio

## 23.1 Required release checks
When pack or offline-content behavior changed, verify at minimum:
- recommended pack discovery,
- install and ready state,
- checksum or corruption failure,
- low-storage handling,
- download pause/resume,
- purge and recover,
- cached manifest behavior offline,
- feature handoff after install,
- audio availability after install and after relaunch.

## 23.2 Runtime-truth rule
Release verification must confirm that the app never claims a pack or audio asset is ready until it is actually usable locally.

## 23.3 Recovery-proof rule
Corruption or purge recovery must be verified where affected by scope.

---

# 24. Feature-family verification — account, subscriptions, entitlements, and settings

## 24.1 Required release checks
When account or monetization behavior changed, verify at minimum:
- guest and signed-in paths as relevant,
- account gate only when required,
- purchase in each platform’s approved test environment,
- restore on reinstall or new-device style path where relevant,
- expired/downgraded entitlement handling,
- offline cached entitlement behavior,
- settings persistence,
- subscription-management handoff.

## 24.2 Platform-store rule
Store-related release proof must come from approved platform test paths, not only mocked success responses.

## 24.3 Monetization ethics rule
Evidence must confirm that monetization surfaces do not block emergency, ritual correctness, or first-use value in ways forbidden by product policy.

---

# 25. Accessibility, localization, and RTL release checks

## 25.1 Required accessibility checks
Every release candidate affecting user-visible surfaces should verify at minimum on impacted flows:
- larger text,
- screen-reader basics,
- focus order and action labeling,
- tap-target clarity,
- non-color-only meaning,
- reduced transparency / increased contrast behavior where relevant,
- motion/transparency sanity where platform settings affect comprehension.

## 25.2 Required localization checks
Where affected, verify:
- missing-key absence,
- supported locale fallback,
- text overflow/clipping,
- mixed Arabic and Latin content,
- date/time/number formatting on impacted screens,
- consistent terminology on critical surfaces.

## 25.3 Required RTL checks
RTL checks should cover impacted shells and critical flows, especially:
- Home and onboarding,
- Rituals,
- emergency and phrasebook,
- group join and regroup,
- map instructions/labels where supported,
- packs and account flows.

## 25.4 Assistive-tech rule
Automated accessibility audits help, but at least some real assistive-technology interaction is still required for critical release confidence.

---

# 26. Performance, stability, battery, and thermal release proof

## 26.1 Required performance proof
Release evidence should include, for impacted high-risk flows:
- startup timing,
- first usable Home timing,
- critical screen open timing,
- emergency-root open timing,
- map route-preview responsiveness,
- pack install progress responsiveness,
- jank observations on critical screens.

## 26.2 Stability proof
Where relevant, the release bundle should summarize:
- crash-free certification runs,
- major non-fatal issue counts or notable regressions,
- ANR/freeze concerns where observed,
- blocker-class stability issues still open.

## 26.3 Battery and thermal sanity proof
For map, audio, or repeated active-use flows, representative sanity checks should note whether behavior shows concerning battery or thermal degradation.

## 26.4 Performance-on-low-end rule
A critical flow that performs well only on flagship devices is not release-ready for a wider supported target.

---

# 27. Beta, staged exposure, and external feedback posture

## 27.1 Beta rule
Beta testing is a confidence amplifier, not a substitute for structured verification.

## 27.2 Recommended beta channels
Where applicable, near-production builds should use appropriate beta channels such as:
- Google Play internal or closed testing,
- Google Play pre-launch reporting,
- Apple TestFlight,
- controlled internal tester groups.

## 27.3 Beta evidence rule
Relevant beta feedback should be summarized in the release bundle when it materially affects release confidence.

## 27.4 Pre-launch-report rule
Automated platform reports are useful signal but do not replace the project’s own real-world release gates.

## 27.5 Representative tester rule
When possible, beta and real-world validation should include:
- internal contributors,
- accessibility-aware testers,
- cross-language reviewers,
- low-confidence or non-expert users,
- testers using realistic travel or degraded-network conditions.

---

# 28. Go / no-go gates

## 28.1 Gate A — automated and certification gate
Must pass:
- required automated suites,
- required device-lab certification from file `27`,
- no unresolved blocker-class automation failures.

## 28.2 Gate B — manual critical-flow gate
Must pass:
- manual verification for all impacted critical flows,
- on-device proof for required physical-device areas,
- no unresolved critical usability or routing failures.

## 28.3 Gate C — offline and degraded-state gate
Must pass where relevant:
- offline claims are proven,
- stale/degraded states are communicated honestly,
- recovery behavior is verified.

## 28.4 Gate D — trust and correctness gate
Must pass where relevant:
- ritual correctness and governed-content proof,
- emergency/assistive trust requirements,
- no blocker-class misleading UX or ethical boundary violation.

## 28.5 Gate E — release evidence completeness gate
Must pass:
- evidence bundle is complete,
- store/compliance evidence is attached where relevant,
- known issues are documented,
- waivers are explicit and owned,
- required sign-offs exist.

## 28.6 No-go default rule
If a required gate is not passed and no explicit waiver exists, the default decision is **do not ship**.

---

# 29. Blockers, known issues, and waiver policy

## 29.1 Automatic release blockers
The following are automatic blockers unless explicitly overruled at the highest accountable level:
- startup failure or crash in critical flows,
- broken first usable state,
- ritual-correctness or governed-content mismatch,
- emergency or phrase critical-path failure,
- broken Save My Gate or required map fallback behavior,
- broken purchase or restore behavior in affected scope,
- corrupted or dishonest pack-ready state,
- severe accessibility breakage in critical flows,
- severe offline regression in promised core paths,
- missing required evidence or sign-off,
- misleading stale/live-state communication in critical flows.

## 29.2 Conditional blockers
These may block release depending on severity and scope:
- secondary-flow friction,
- non-critical visual regressions,
- minor translation problems outside critical paths,
- performance warnings above comfort but below hard fail,
- platform-specific issues isolated to explicitly unsupported or rarely affected combinations.

## 29.3 Known-issue recording rule
Known issues must state at minimum:
- issue id or reference,
- summary,
- severity,
- affected flow or matrix slice,
- user impact,
- workaround if any,
- owner,
- disposition: blocker / waived / accepted follow-up.

## 29.4 Waiver requirements
A waiver must state at minimum:
- why release is still acceptable,
- what user risk remains,
- which users or flows are affected,
- what mitigation exists,
- who approved the waiver,
- when the waiver expires or must be revisited.

## 29.5 No silent waiver rule
Informal acceptance in chat, meetings, or memory is not a waiver.

---

# 30. Evidence templates, update triggers, anti-patterns, and summary

## 30.1 Recommended evidence template sections
A practical evidence template should include:
- header and build id,
- change summary,
- risk classification,
- required checks matrix,
- executed checks and outcomes,
- attached media/log links,
- open issues and waivers,
- sign-offs,
- final recommendation.

## 30.2 When this file must be updated
This file must be updated whenever any of the following changes:
- release-candidate approval model,
- sign-off responsibilities,
- blocker criteria,
- required evidence categories,
- manual verification expectations,
- offline or accessibility release bar,
- governed-content release proof requirements,
- purchase/restore verification posture,
- map real-world validation posture,
- seasonal or high-risk release escalation rules.

If these truths change but this file is not updated, release decisions will drift quickly and become inconsistent.

## 30.3 Anti-patterns forbidden by this document
The following are forbidden unless explicitly approved:
- treating one demo video as ship proof,
- relying on simulator-only proof for maps, purchases, notifications, or accessibility,
- shipping without explicit blocker review,
- claiming offline readiness without airplane-mode proof where relevant,
- using screenshots as a substitute for structured results,
- hiding known issues because they are inconvenient to explain,
- reducing evidence depth ad hoc to hit a date,
- calling a release “ready” when required sign-offs are missing,
- treating beta feedback as the only real-world validation,
- allowing AI-generated summaries to replace accountable human release judgment.

## 30.4 Summary
This file defines the canonical release-readiness proof system for Pilgrims Mobile App.

It establishes:
- how release candidates move from testing to real-world verification,
- how evidence depth scales with risk,
- what on-device, offline, network, accessibility, and feature-family proof must exist,
- how evidence bundles are structured,
- which gates must pass before shipping,
- how blockers, known issues, and waivers are handled,
- and who must sign off.

Its purpose is to ensure that Pilgrims Mobile App ships only when there is real proof that the app remains:
- trustworthy,
- offline-capable,
- accessible,
- calm under stress,
- and safe to rely on in real pilgrimage conditions.

