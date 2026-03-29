# 30 — DELIVERY RUNBOOK, INCIDENTS, ROLLBACK, AND OPERATIONS

## Document status
- **Type:** Normative delivery, release-operations, incident-response, rollback, and operational runbook specification
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, release owner, Flutter engineers, backend engineers, QA lead, content/governance contributors, operations contributors, support contributors, reviewer agents, release agents
- **Purpose:** Define the canonical operational workflow for preparing, shipping, monitoring, supporting, hotfixing, rolling back, and recovering Pilgrims Mobile App across mobile builds, server-backed contracts, governed content, packs, flags, and trust-critical incidents.
- **Authority level:** This file is the canonical source of truth for release execution and operational recovery. If ad hoc release habits, chat decisions, dashboards, or pressure-driven shortcuts conflict with this file, this file wins unless a higher-authority document or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `05-ROADMAP-PROGRESS-AND-CHANGELOG.md`, `06-SYSTEM-ARCHITECTURE.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`, `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`, `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`, `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`, `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`, `29-SECURITY-PRIVACY-COMPLIANCE-AND-RISK-REGISTER.md`
- **Related files:** `11`, `18`, `19`, `20`, `21`, `22`

---

# 1. Purpose of this file

This file exists because a release can satisfy the proof bar in file `28` and still fail if the team does not know exactly how to ship, observe, react, and recover.

For this project, delivery and operations mistakes are especially dangerous because:
- the product has a deliberately small but trust-critical online surface,
- many user flows are used under stress, low confidence, fatigue, or weak connectivity,
- governed content, packs, and entitlements can change independently of app binaries,
- map, group, and emergency behavior can fail in ways that require different containment paths,
- app-store release mechanics are slower and less reversible than backend or flag operations,
- AI-assisted implementation can create release artifacts quickly but still miss the operational meaning of a safe rollout,
- a weak handoff between release, support, and incident response can turn a contained defect into a trust crisis.

This file prevents those failures by defining:
- the canonical environment strategy,
- the release execution workflow,
- the deployment and staging model,
- feature-flag and runtime-selection rules,
- operational dashboards and health checks,
- rollback paths by failure domain,
- hotfix rules,
- incident command and escalation rules,
- support handoff expectations,
- post-incident learning and disaster-recovery posture.

---

# 2. Operational purpose and user value

## 2.1 Module purpose
This module exists to ensure that Pilgrims Mobile App can be delivered and operated safely after it has already met the testing and release-evidence bar.

## 2.2 User value statement
A pilgrim should never have to think about the delivery runbook directly.

The value to the pilgrim is that:
- releases are gradual and controlled,
- critical regressions are detected quickly,
- misleading or broken behavior is contained fast,
- offline and last-known-good behavior continues protecting them,
- support responses are calm and informed,
- hotfixes do not create secondary damage,
- trust-critical issues are handled honestly.

## 2.3 Operational value statement
The team should be able to answer questions like:
- What exact steps are required to ship a release candidate?
- Which rollout control should we use first: flag, content pointer, pack manifest, or hotfix?
- Who owns the incident if a ritual-content issue appears after release?
- What does “rollback” mean for binary, server, pack, content, or entitlement failures?
- Which dashboards must be green before rollout percentage increases?
- What do support and product need to know during a live incident?

---

# 3. Scope and boundaries

## 3.1 In scope
This file includes:
- environment strategy,
- build promotion and release workflow,
- staged rollout expectations,
- feature-flag and runtime-activation rules,
- post-release monitoring rules,
- rollback decision framework,
- hotfix process,
- incident response workflow,
- operational ownership and escalation,
- support handoff rules,
- disaster-recovery summary,
- postmortem template and follow-up expectations.

## 3.2 Out of scope
This file does **not** replace:
- the product scope and ethics rules in file `03`,
- architecture truth in files `06`, `14`, and `15`,
- governed-content review and publication rules in file `26`,
- test strategy and device coverage in file `27`,
- release-proof and sign-off requirements in file `28`,
- security/privacy policy and risk posture in file `29`.

This file defines how the team operates once those files have already set the policy and proof bar.

## 3.3 Boundary with file `28`
File `28` answers: “Do we have enough evidence to ship this candidate?”

This file answers:
- how the release is actually executed,
- what sequence of operational checks is required,
- how staged rollout is managed,
- how rollback and hotfix decisions are made after shipment begins.

## 3.4 Boundary with file `29`
File `29` defines the security/privacy posture, risk register, and incident severity model.

This file defines:
- how operational responders use that severity model,
- who must be paged,
- what immediate containment actions are expected,
- how evidence is preserved during execution.

## 3.5 Boundary with file `26`
File `26` defines governed-content publication, emergency correction, and rollback semantics for content.

This file defines:
- how those content operations are executed in a live incident,
- how content rollback fits into overall release operations,
- how app/content compatibility is protected during response.

## 3.6 Boundary with file `15`
File `15` defines pack states, trust, verification, and cache behavior.

This file defines:
- how pack incidents are triaged,
- when manifest-level containment is preferred,
- when pack delivery should be paused,
- how pack rollback interacts with release operations.

---

# 4. Product rules that govern delivery and operations

## 4.1 Safety-over-speed rule
When a release tradeoff exists between speed and trust, trust wins.

## 4.2 Smallest-safe-change rule
Contain incidents using the smallest operational change that safely protects users:
- disable risky exposure before shipping a new binary when possible,
- repoint to a known-good artifact before inventing live patches,
- prefer scoped rollback over broad panic reversions.

## 4.3 No “ship and pray” rule
A release is not complete when the store submission is done.
It remains active operational work until monitoring confirms expected stability.

## 4.4 Binary-rollback realism rule
Do not design the operations model around an assumption of instant binary rollback.
Store-mediated binaries are slower to reverse than flags, config selection, content pointers, and manifest controls.

## 4.5 Last-known-good rule
For content, packs, entitlements, and other runtime-dependent surfaces, the system must always preserve a last-known-good fallback path where architecture allows.

## 4.6 No silent-risk acceptance rule
If a risk remains after release, it must be named, owned, monitored, and either time-bounded or fixed.

## 4.7 One incident commander rule
During a live incident, one accountable human must own coordination.
Discussion is shared; command is not.

## 4.8 Honest-user-communication rule
If a problem materially affects trust, correctness, or access, user-facing communication must be accurate, calm, and not falsely reassuring.

## 4.9 No undocumented production change rule
Operational changes to flags, manifests, rollout percentages, or content activation must be auditable.

## 4.10 Umrah-first operational rule
Release and incident decisions must not quietly widen scope into Hajj or broader seasonality without approved product and operational readiness.

---

# 5. Canonical terminology for this module

## 5.1 Build promotion
The controlled movement of a build from development/testing toward beta and production readiness.

## 5.2 Release candidate
A build and configuration state that has passed verification and is eligible for controlled rollout.

## 5.3 Rollout
The staged exposure of a release candidate to real users through store distribution, flags, manifests, content activation, or equivalent operational mechanisms.

## 5.4 Rollback
Any controlled action that restores a safer previous state.

Rollback may refer to:
- binary rollout halt,
- flag rollback,
- manifest pointer rollback,
- governed-content rollback,
- pack exposure rollback,
- entitlement/config rollback,
- or a replacement hotfix that restores safe behavior.

## 5.5 Containment
The fastest safe action that limits user harm while fuller diagnosis or a lasting fix is still in progress.

## 5.6 Hotfix
A targeted corrective release or operational change made outside the normal larger release cadence because user impact is time-sensitive.

## 5.7 Operational freeze
A temporary rule that blocks non-essential production changes while release or incident work is ongoing.

## 5.8 Incident commander
The accountable responder coordinating a live incident across engineering, product, support, and governance.

## 5.9 Last-known-good build
The most recent previously trusted build/configuration state that remains safe to reference operationally.

## 5.10 Recovery point
The exact state the team intends to restore, such as a prior binary rollout percentage, prior content activation pointer, prior manifest version, or prior flag set.

---

# 6. Operational roles and ownership

## 6.1 Founder / accountable product owner
Owns high-level release risk acceptance for major milestones and the final acceptance of critical operational waivers where required.

## 6.2 Release owner
Owns the release checklist, go-live execution, rollout pacing, and coordination with QA, engineering, product, and support.

## 6.3 Mobile owner
Owns mobile binary build integrity, store submission readiness, platform-specific rollout actions, and app-side diagnostics.

## 6.4 Backend owner
Owns backend contract readiness, production service health, config/flag service health, auditability, and server-side rollback actions.

## 6.5 Content/governance owner
Owns governed-content activation, content emergency correction, content rollback, and review traceability during incidents that affect trust-critical content.

## 6.6 QA owner
Owns release evidence traceability, confirmation of the shipped candidate identity, and post-release verification on exposed tracks.

## 6.7 Support owner
Owns support briefings, issue intake triage, known-issue communication, and escalation of user-reported signals into the incident process.

## 6.8 Incident commander
May be the release owner or another designated accountable role during live incidents. Owns cross-function coordination and time-stamped decision logging.

## 6.9 Communications owner
Owns outward-facing update text, internal status summaries, and support-ready messaging when user communication is required.

## 6.10 AI-agent boundary
AI agents may help:
- assemble release notes,
- summarize telemetry and issue clusters,
- draft rollback checklists,
- generate postmortem skeletons.

AI agents must not:
- perform privileged production actions autonomously,
- self-approve rollout increases,
- silently expire incidents,
- downgrade severity without human approval,
- alter manifests, rollout settings, or live content pointers without accountable human execution.

---

# 7. Canonical operational environments

## 7.1 Required environment tiers
The system should maintain at minimum:
1. local development
2. shared integration / test environment
3. staging / release-candidate environment
4. production
5. beta-distribution layer for mobile store testing
6. governed-content publication environment(s) consistent with file `26`

## 7.2 Local development environment
Purpose:
- individual engineer iteration,
- non-production secrets,
- disposable data,
- rapid debugging.

Rule:
- must never be treated as evidence of production readiness by itself.

## 7.3 Shared integration/test environment
Purpose:
- API and contract integration,
- pack/content/flag integration validation,
- collaborative QA,
- repeatable fixture-backed tests.

Rule:
- should remain stable enough for automated and manual integration work.

## 7.4 Staging / release-candidate environment
Purpose:
- final contract-compatible validation using release-candidate app builds,
- final config and manifest sanity,
- end-to-end operational rehearsals,
- release notes and release bundle reconciliation.

Rule:
- must be close enough to production to reveal operational issues early, while still protecting production data and users.

## 7.5 Production environment
Purpose:
- real user traffic,
- real operational truth,
- auditable release history.

Rule:
- non-essential production changes should be minimized during active rollout and incident response.

## 7.6 Beta-distribution layer
Purpose:
- App Store Connect / TestFlight exposure on Apple platforms,
- Play internal / closed / open testing on Android,
- last-mile store and device validation before full production rollout.

Rule:
- beta success is signal, not authorization to skip the rest of the release runbook.

## 7.7 Environment-separation rule
Secrets, service accounts, webhook endpoints, logging sinks, and operational dashboards must stay properly separated by environment.

---

# 8. Configuration, flags, manifests, and activation surfaces

## 8.1 Operational control surfaces
The system should recognize these main operational control surfaces:
- mobile binary version and track exposure,
- server flags and safe config values,
- pack manifest version or availability,
- governed-content activation pointer,
- entitlement/config service behavior,
- backend route or service availability,
- support and status communication surfaces.

## 8.2 Safe-default rule
Every operational control surface must fail toward user safety and truthfulness rather than optimistic exposure.

## 8.3 Config layering rule
The runtime should conceptually resolve configuration in this order:
1. app-bundled safe defaults,
2. validated last-known-good local state,
3. trusted remote config / manifest / content activation state when available and compatible.

## 8.4 No mixed-truth rule
Operational controls must not create contradictory user states across binary, config, content, and pack layers.

## 8.5 Auditability rule
Changes to live flags, manifest pointers, or content activation states must be logged with:
- actor,
- timestamp,
- changed values,
- reason,
- associated release or incident reference.

---

# 9. Feature-flag strategy

## 9.1 Purpose
Feature flags exist to:
- reduce blast radius,
- enable staged exposure,
- support safe containment,
- decouple some operational response paths from binary submission cycles.

## 9.2 Allowed flag categories
Representative allowed categories include:
- visibility flags for optional UI surfaces,
- safe rollout percentage or audience gating,
- capability enablement for non-core enrichments,
- operational fallback flags,
- maintenance-mode or degraded-path switches,
- selection flags between already-published safe artifacts.

## 9.3 Forbidden flag categories
Flags must not:
- invent new product scope outside approved docs,
- silently redefine entitlement truth,
- bypass scholar review or governed-content approval,
- change religious meaning in place,
- hide critical safety communication without accountable review.

## 9.4 Flag lifecycle rule
Every production flag should have:
- owner,
- purpose,
- default value,
- safe fallback value,
- cleanup expectation,
- removal target when temporary.

## 9.5 Release flag rule
Temporary rollout flags should be removed after stability is proven.
A permanent graveyard of stale flags is forbidden.

## 9.6 Kill-switch rule
For selected risky capabilities, a server-side or config-side kill switch is encouraged where architecture supports it, especially for:
- optional live group enrichments,
- non-essential advanced map layers,
- optional pack conveniences,
- non-core enrichments that can safely disappear without breaking core value.

## 9.7 No “flags as architecture” rule
Flags are operational tools, not a substitute for clean product contracts.

---

# 10. Release artifact model

## 10.1 Release package components
A releasable operational package may involve multiple coordinated artifacts:
- mobile binary build(s),
- release notes and metadata,
- config/flag snapshot,
- pack manifest state,
- governed-content activation state,
- release evidence bundle from file `28`,
- support handoff summary,
- rollback plan.

## 10.2 Identity rule
Every release must have a unique release identifier or release record tying together:
- app build numbers,
- intended platform tracks,
- content/manifest/config versions,
- evidence bundle reference,
- sign-offs,
- rollout status.

## 10.3 Reproducibility rule
The team should be able to reconstruct exactly what was shipped and activated.

## 10.4 Multi-surface release rule
If the release changes binary, content, flags, or pack distribution together, the runbook must identify which surfaces are coordinated and which can be rolled back independently.

---

# 11. Deployment workflow

## 11.1 Canonical high-level workflow
The normal release execution workflow should be:

1. release candidate selected  
2. evidence and sign-offs confirmed from file `28`  
3. operational freeze begins for non-essential changes  
4. release record created  
5. store metadata and track setup verified  
6. config/flag snapshot reviewed  
7. pack/content activation compatibility verified  
8. beta / final pre-prod checks confirmed  
9. production rollout starts in a controlled stage  
10. monitoring window begins  
11. rollout pace decisions made from observed health  
12. release completed, paused, or contained based on evidence  

## 11.2 Operational freeze rule
Once a release candidate enters go-live preparation, unrelated config, content, or flag changes should be frozen unless explicitly approved and logged.

## 11.3 Checklist-before-start rule
The release owner must confirm at minimum:
- candidate identity is correct,
- no unresolved blocker without explicit waiver,
- rollout plan exists,
- rollback and containment plan exists,
- monitoring dashboard links are ready,
- support handoff draft is ready,
- on-call availability is confirmed for the monitoring window.

## 11.4 No “simultaneous chaos” rule
Do not combine unrelated high-risk production changes just because they are ready on the same day.

---

# 12. Build promotion and store-track strategy

## 12.1 Promotion posture
Builds should promote from internal confidence to broader confidence in deliberate steps, not jump from developer machine to global exposure.

## 12.2 Apple track posture
Apple releases should use:
- internal testing as needed,
- TestFlight for controlled beta validation,
- phased production release when appropriate for updates,
- ability to stop testing or expire builds when beta exposure is no longer safe.

## 12.3 Android track posture
Android releases should use:
- internal testing,
- closed or open testing as appropriate,
- staged rollout for production updates,
- halt/resume/update-rollout controls as part of operational response.

## 12.4 First-production caution
A first public production release is higher risk than a later incremental update and should not rely on assumed store rollback behavior.

## 12.5 Store-metadata readiness rule
Store copy, screenshots, privacy disclosures, and listing metadata must already be aligned before a release begins exposure.

## 12.6 Track hygiene rule
Old beta tracks, stale candidate builds, or misleading internal labels must be cleaned up so operations teams do not act on the wrong artifact.

---

# 13. Canonical release procedure

## 13.1 Pre-release preparation
Before starting any production exposure:
- confirm evidence bundle completion,
- confirm version numbers and build numbers,
- confirm config and content compatibility,
- confirm support briefing package,
- confirm monitoring dashboards and alerts,
- confirm designated incident commander for the monitoring window.

## 13.2 Initial exposure stage
Begin with a limited exposure stage whenever platform mechanics and risk class support it.

Typical examples:
- limited TestFlight / beta group completion,
- staged rollout percentage on Google Play,
- phased release on Apple updates,
- limited activation of non-core flags,
- limited manifest/content exposure where architecture allows.

## 13.3 Early-monitoring gate
Do not increase exposure until the early-monitoring window shows acceptable health.

## 13.4 Mid-rollout gate
Do not continue increasing rollout if:
- blocker-class incidents appear,
- crash or ANR/freeze trends spike beyond acceptable thresholds,
- purchase/restore failure trends appear,
- pack integrity failures rise materially,
- Home/startup critical-path failures appear,
- trust-critical complaints emerge.

## 13.5 Completion gate
A release is only “completed” when:
- rollout exposure is intentionally finished,
- post-rollout monitoring stabilizes,
- known issues are documented and owned,
- release record is finalized.

## 13.6 Post-release verification rule
At least one human operational check must confirm the real store-exposed release behaves as expected on live builds and real distribution paths.

---

# 14. Rollout pacing and decision rules

## 14.1 Risk-based pacing rule
Higher-risk releases require slower pacing and longer observation windows.

## 14.2 Suggested pacing categories
### Low-risk release
May move faster after early checks remain healthy.

### Standard release
Should include at least one explicit hold point after initial exposure.

### High-risk / trust-critical release
Should include multiple deliberate hold points and explicit cross-functional approval before each major increase.

## 14.3 Observation-window rule
Each rollout stage must have a named observation window and owner.
Do not increase exposure purely because time passed if the data is still unclear.

## 14.4 No optimism-only progression rule
Rollout progression requires evidence, not confidence vibes.

## 14.5 Cross-surface progression rule
If binary, content, and manifest changes are coordinated, progression should consider the slowest or riskiest surface, not the fastest one.

---

# 15. Operational dashboards and live checks

## 15.1 Purpose
Dashboards exist to make release and incident judgment faster, not noisier.

## 15.2 Minimum operational views
Operations should maintain at minimum views for:
- release status and rollout stage,
- crash and stability trends,
- startup/Home health,
- entitlement and restore health,
- pack/asset delivery health,
- governed-content activation and rollback history,
- map/navigation critical-path health,
- support issue intake volume,
- security/privacy incident queue where relevant.

## 15.3 Recommended release-health signals
Representative signals include:
- crash-free session or equivalent stability trend,
- ANR/freeze trend where relevant,
- startup failure rate,
- first-usable-state failure rate,
- failed restore or purchase validation rate,
- pack install failure or checksum failure rate,
- content compatibility failures,
- stale-fallback or last-known-good activation spikes,
- map route-preview failure spikes,
- emergency-root open failures,
- major support-ticket spike by category.

## 15.4 Alert-noise rule
Only alert on signals that are actionable enough to influence rollout or incident handling.

## 15.5 Release dashboard truth rule
Dashboards must separate:
- beta vs production,
- current release vs historical baseline,
- platform differences,
- low-volume uncertainty vs real regressions.

---

# 16. Operational readiness checklist

## 16.1 Before production exposure
Confirm:
- release record created,
- evidence bundle attached,
- sign-offs complete,
- rollout plan documented,
- rollback plan documented,
- on-call roles confirmed,
- support handoff prepared,
- feature flags and manifest pointers reviewed,
- store disclosures, privacy manifests, and any required account-deletion resources reviewed against the shipped candidate where applicable,
- known issues and waivers documented.

## 16.2 During rollout
Confirm repeatedly:
- rollout stage and timestamp,
- current health snapshot,
- open issues and owner,
- whether escalation threshold is crossed,
- next decision time.

## 16.3 After rollout completion
Confirm:
- rollout finished or intentionally paused,
- release record finalized,
- support summary updated,
- post-release follow-up tasks recorded,
- roadmap/changelog update queued for file `05` after the 30-file set is complete.

---

# 17. Rollback philosophy and recovery-point model

## 17.1 Purpose
Rollback must restore safety, not merely revert activity.

## 17.2 Recovery-point types
A rollback may target one of several recovery points:
- prior flag/config state,
- prior content activation pointer,
- prior pack manifest exposure,
- prior rollout percentage or halted rollout state,
- prior server behavior or safe degraded mode,
- prior binary version exposure if platform mechanics and operational timing allow,
- replacement hotfix release.

## 17.3 Smallest-safe-recovery rule
Choose the smallest recovery point that:
- stops user harm,
- preserves data integrity,
- avoids new confusion,
- can be executed quickly and auditably.

## 17.4 Binary-last-resort rule
Because store-distributed binaries are slower to reverse, binary rollback should not be the only planned containment path for trust-critical risks.

## 17.5 Rollback evidence rule
Every rollback must record:
- trigger,
- scope,
- chosen recovery point,
- actor,
- timestamp,
- user impact note,
- validation result after rollback.

---

# 18. Rollback procedures by failure domain

## 18.1 Binary/UI regression
Examples:
- severe startup failure,
- broken Home routing,
- major accessibility regression,
- restore flow unusable.

Preferred operational sequence:
1. halt or pause rollout where platform supports it,
2. verify whether a safe config/flag containment exists,
3. confirm blast radius,
4. ship targeted hotfix if needed,
5. do not increase exposure until recovery evidence exists.

## 18.2 Governed-content incident
Examples:
- ritual meaning mismatch,
- incorrect remedy guidance,
- broken content artifact compatibility.

Preferred operational sequence:
1. stop risky activation path,
2. repoint to last-known-good governed artifact if available,
3. coordinate with content/governance owner,
4. preserve review and publication evidence,
5. publish corrected artifact or safe binary/config follow-up if required,
6. document cross-link to content incident record.

## 18.3 Pack/asset incident
Examples:
- bad checksum wave,
- corrupted ready state,
- manifest references broken artifacts,
- audio pack falsely marked ready.

Preferred operational sequence:
1. stop exposing broken manifest state,
2. revert to last-good manifest or disable affected pack entries,
3. preserve installed last-good local packs on device when safe,
4. investigate CDN/manifests/checksum lineage,
5. only re-enable after verification.

## 18.4 Backend/config incident
Examples:
- auth refresh failure,
- entitlement service outage,
- group endpoint instability,
- stale-state mislabeling caused by config.

Preferred operational sequence:
1. shift to safe degraded mode,
2. disable risky optional surfaces if needed,
3. restore backend service or safe config,
4. confirm client behavior against stale/local fallback,
5. continue or restart rollout only after stability is proven.

## 18.5 Purchase/restore incident
Examples:
- restore failures spike,
- validation endpoint fails,
- store-bridge regression on one platform.

Preferred operational sequence:
1. halt rollout increase,
2. confirm whether issue is platform, backend, or configuration specific,
3. communicate restore/purchase known issue to support,
4. contain via temporary CTA changes or messaging if ethical and allowed,
5. hotfix or backend fix as required.

## 18.6 Security/privacy incident
Examples:
- sensitive logging leak,
- broken authorization,
- token handling defect,
- hidden tracking behavior.

Preferred operational sequence:
1. classify severity per file `29`,
2. contain access or collection immediately,
3. preserve evidence,
4. involve legal/compliance if required,
5. do not resume rollout until security/privacy owner clears the issue.

---

# 19. Hotfix process

## 19.1 Purpose
Hotfixes exist for issues that materially affect user trust, access, correctness, privacy, or stability and cannot wait for the next normal cycle.

## 19.2 Hotfix triggers
Typical hotfix triggers include:
- blocker-class startup/Home failures,
- ritual-correctness or governed-content runtime mismatch,
- severe accessibility regression in critical flows,
- severe purchase/restore failure,
- widespread pack or manifest breakage,
- severe map recovery regression,
- SEV-1 / SEV-2 security or privacy issue.

## 19.3 Hotfix constraints
A hotfix must:
- stay tightly scoped,
- avoid opportunistic unrelated changes,
- reuse the existing evidence and incident context,
- still meet a proportionate verification and sign-off bar.

## 19.4 Hotfix evidence rule
Hotfixes may use a narrower evidence bundle than a full feature release, but it must still include:
- exact issue being fixed,
- impacted scope,
- regression checks for the fix,
- rollback plan,
- sign-offs appropriate to the risk.

## 19.5 Hotfix communication rule
Support, product, QA, and operations must know:
- what the hotfix addresses,
- what remains broken until it ships,
- what workaround exists if any,
- what metrics confirm recovery.

## 19.6 No stealth hotfix rule
Even urgent config-only or content-only hotfixes must be logged as release or incident actions.

---

# 20. Incident response workflow

## 20.1 Canonical workflow
The incident workflow should be:

1. detect  
2. acknowledge  
3. classify severity  
4. appoint incident commander  
5. stabilize communications  
6. contain harm  
7. diagnose  
8. execute recovery or rollback  
9. verify recovery  
10. communicate status and next steps  
11. close operationally  
12. run postmortem  

## 20.2 Detection sources
Incidents may begin from:
- dashboards or alerts,
- support spike,
- beta tester escalation,
- product/governance review,
- QA verification after rollout,
- external partner/store signals,
- security/privacy reports.

## 20.3 Acknowledgment rule
Potential SEV-1 or SEV-2 incidents should be acknowledged quickly by a named human owner.
Silence is not triage.

## 20.4 Triage packet
Every new incident should quickly capture:
- summary,
- time first observed,
- affected platform(s),
- affected feature family,
- severity hypothesis,
- suspected rollback/containment options,
- current incident commander,
- next update time.

## 20.5 Communication cadence rule
During active incidents, maintain explicit next-update times even if there is no full fix yet.

---

# 21. Severity handling and escalation

## 21.1 Severity source
Use the security/privacy severity model in file `29` and the release-blocker logic in file `28` together with operational judgment.

## 21.2 SEV-1 posture
Examples:
- trust-critical ritual or safety failure,
- broad startup crash,
- material sensitive-data exposure,
- severe authorization failure,
- broken emergency-root access on released builds.

Expected response:
- immediate incident commander,
- immediate containment attempt,
- executive/product awareness,
- no rollout increases,
- likely rollout halt or rollback.

## 21.3 SEV-2 posture
Examples:
- significant but narrower critical-path regression,
- serious restore failure,
- severe map recovery failure,
- corrupted content/pack activation affecting a meaningful cohort.

Expected response:
- rapid cross-functional coordination,
- explicit containment plan,
- rollout pause or scoped rollback likely.

## 21.4 SEV-3 posture
Examples:
- limited-scope but meaningful production issue,
- non-critical yet high-friction regression,
- contained SDK/disclosure issue requiring timely fix.

Expected response:
- owned mitigation,
- monitoring,
- scheduled fix or hotfix depending on trajectory.

## 21.5 SEV-4 posture
Examples:
- low-impact ops issue,
- documentation or tooling friction,
- minor non-critical production defect.

Expected response:
- track, own, fix in normal cadence unless trend changes.

## 21.6 Escalation rule
Severity can be escalated upward when:
- blast radius grows,
- mitigation fails,
- user trust damage is larger than expected,
- support or telemetry signal shows broader impact,
- legal/compliance implications appear.

---

# 22. Support handoff rules

## 22.1 Purpose
Support must receive operationally useful information, not vague engineering fragments.

## 22.2 Required support handoff for releases
For every significant release, provide support with:
- release summary,
- user-visible changes,
- known issues and workarounds,
- likely confusion points,
- support-safe explanations,
- escalation triggers.

## 22.3 Required support handoff for incidents
During incidents, support must receive:
- current issue summary,
- affected user segment if known,
- whether new users should be advised to wait, retry, or use a fallback,
- what not to promise,
- next update time,
- escalation path for unusual cases.

## 22.4 Support privacy rule
Do not ask support to collect unnecessary personal, medical, or precise-location details while triaging routine problems.

## 22.5 Support evidence rule
If support escalates a case, the minimum useful handoff should include:
- platform,
- app version/build,
- locale,
- network state if known,
- exact user-visible failure,
- reproduction hints,
- screenshots only when safe and non-sensitive.

---

# 23. User communication rules during incidents and release issues

## 23.1 Calm-truth rule
Communication must be calm, plain-language, and truthful.

## 23.2 No fake certainty rule
Do not say the issue is fixed until recovery has been verified on the affected surface.

## 23.3 No blame rule
User-facing communication must not blame users, testers, devices, or connectivity in a dismissive way.

## 23.4 Scope honesty rule
If the issue affects only a platform, locale, track, or feature, say so clearly.

## 23.5 Trust-critical communication rule
When ritual correctness, emergency access, or privacy is affected, communication should be reviewed with the relevant owner before publication.

---

# 24. Operational checklists by feature family

## 24.1 Onboarding / Home / Simple Mode
Operational checks should confirm:
- correct startup routing,
- Home remains usable,
- urgent shortcuts still work,
- offline landing is safe,
- Simple Mode preference persists,
- no early release regression in first-use comprehension.

## 24.2 Rituals / governed content
Operational checks should confirm:
- correct content artifact active,
- no invalid fallback activation,
- last-known-good recovery available,
- no unsupported seasonal leakage,
- emergency content rollback path known.

## 24.3 Maps / Save My Gate
Operational checks should confirm:
- anchors still recall safely,
- route preview availability is truthful,
- missing-pack fallback remains honest,
- no false precision or misleading live-state implication after rollout.

## 24.4 Group
Operational checks should confirm:
- join and safe-status actions work,
- stale-state communication remains honest,
- no hidden tracking implication introduced by config or rollout.

## 24.5 Packs / audio
Operational checks should confirm:
- manifest state correct,
- install/verify/ready transitions healthy,
- no corrupted ready state,
- purge/recover behavior unchanged for exposed cohort.

## 24.6 Account / entitlements
Operational checks should confirm:
- account gate still appears only when needed,
- purchase/restore paths healthy,
- cached entitlement communication honest,
- no forced sign-in drift.

## 24.7 Emergency / phrasebook / medical profile
Operational checks should confirm:
- emergency entry fast and visible,
- phrase retrieval works offline,
- no sensitive logging or export surprises,
- support and privacy copy remain aligned.

---

# 25. Observability, logs, and evidence preservation during incidents

## 25.1 Evidence-preservation rule
Incident responders must preserve enough evidence to understand cause and validate recovery without widely spreading sensitive data.

## 25.2 Minimum preserved items
Where relevant preserve:
- timestamps,
- release/build identifiers,
- config/flag snapshots,
- manifest/content pointers,
- error rates or dashboard snapshots,
- representative logs/traces,
- affected issue links,
- decision timeline.

## 25.3 Redaction rule
Evidence collected during incidents must still obey file `29`.
Do not casually paste restricted data into broad channels or general-purpose docs.

## 25.4 Recovery-validation rule
Once a containment or rollback is executed, capture proof that it actually changed the live state as intended.

---

# 26. Disaster recovery summary

## 26.1 Purpose
Disaster recovery is the posture for low-probability but high-impact operational failure, not only ordinary rollback.

## 26.2 Representative disaster scenarios
The team should be prepared for at minimum:
- config/flag service outage,
- pack manifest corruption or CDN delivery outage,
- backend auth or entitlement outage,
- governed-content activation incident,
- analytics/monitoring partial blindness during live rollout,
- store-track or beta-distribution confusion,
- accidental release of wrong build/config combination.

## 26.3 Minimum disaster-recovery posture
For each major scenario, the team should know:
- primary containment action,
- fallback operational mode,
- minimum product promise that remains,
- required owners,
- what must be restored first.

## 26.4 Product-minimum-survival mode
If major online systems fail, the app should still preserve as much as possible of:
- local Home usefulness,
- bundled last-known-good ritual guidance,
- offline phrasebook and emergency tools,
- saved local anchors and planner data,
- honest degraded-state messaging.

## 26.5 Recovery-priority order
A practical recovery priority is:
1. protect user trust and correctness,
2. preserve core local-first usability,
3. restore auth/entitlement and pack discovery,
4. restore richer online convenience,
5. restore non-critical analytics and secondary tooling.

---

# 27. Postmortem and continuous-improvement rules

## 27.1 Required postmortem triggers
A postmortem is required after at minimum:
- SEV-1 incidents,
- major SEV-2 incidents,
- any rollback that materially affected users,
- any governed-content emergency correction,
- any release halted for blocker-class live regressions,
- recurring incident patterns that signal structural weakness.

## 27.2 Postmortem goals
A postmortem should explain:
- what happened,
- why it happened,
- how detection behaved,
- how containment behaved,
- what made recovery slower or riskier,
- what structural changes will prevent recurrence.

## 27.3 No-blame rule
Postmortems are for learning and accountability, not scapegoating.

## 27.4 Required follow-through rule
Action items from a postmortem must have owners and target dates.
A postmortem without tracked follow-through is incomplete.

## 27.5 Cross-file update rule
If an incident reveals a broken assumption in architecture, release evidence, security posture, content operations, or feature contracts, the relevant canonical files must be updated.

---

# 28. Recommended postmortem template

## 28.1 Header
- incident id
- title
- severity
- incident commander
- start time
- end time / stabilized time
- affected platforms and versions

## 28.2 Executive summary
- one-paragraph summary of what happened and user impact

## 28.3 Timeline
- detection
- acknowledgment
- key decisions
- containment action
- rollback or hotfix action
- recovery verification
- closure

## 28.4 Impact
- affected users or cohort estimate
- affected feature families
- trust / privacy / correctness / stability implications
- support volume impact

## 28.5 Root cause
- technical cause
- process cause
- missing guardrail if applicable

## 28.6 What worked
- useful alerts
- useful last-known-good paths
- effective communication
- successful containment actions

## 28.7 What failed or slowed response
- missing dashboard,
- confusing ownership,
- poor evidence packaging,
- slow store mechanics,
- unclear rollback path,
- stale docs.

## 28.8 Corrective actions
- immediate fix
- medium-term fix
- systemic prevention
- documentation updates required

## 28.9 Owner table
For each action:
- owner
- due date
- status

---

# 29. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 29.1 Shipping without a written rollback plan
Forbidden.

## 29.2 Increasing rollout because “it looks probably fine”
Forbidden.

## 29.3 Treating staged rollout as optional for high-risk releases
Forbidden.

## 29.4 Making emergency production changes with no audit trail
Forbidden.

## 29.5 Letting multiple people improvise conflicting incident commands
Forbidden.

## 29.6 Relying only on a new binary when a safer faster containment path exists
Forbidden.

## 29.7 Leaving stale rollout flags active indefinitely
Forbidden.

## 29.8 Using support as an unstructured debugging proxy for production
Forbidden.

## 29.9 Closing incidents because volume dropped without verifying recovery
Forbidden.

## 29.10 Treating content rollback, pack rollback, and binary rollback as the same thing
Forbidden.

## 29.11 Claiming a user-visible issue is fixed before live validation
Forbidden.

## 29.12 Failing to preserve evidence because response felt urgent
Forbidden.

---

# 30. Update triggers and summary

## 30.1 When this file must be updated
This file must be updated whenever any of the following changes:
- release workflow,
- environment strategy,
- rollout control surfaces,
- feature-flag posture,
- rollback procedure,
- hotfix process,
- incident severity execution model,
- support handoff process,
- required dashboards or health signals,
- disaster-recovery priorities,
- postmortem requirements,
- store-release assumptions or operational tooling choices.

If these truths change but this file is not updated, release execution and incident handling will drift quickly.

## 30.2 Summary
This file defines the canonical delivery and operational runbook for Pilgrims Mobile App.

It establishes:
- how release candidates are prepared and promoted,
- how production rollout is staged and monitored,
- how flags, manifests, governed content, and binaries are operated together,
- how rollback is chosen by failure domain,
- how hotfixes are executed,
- how incidents are classified, commanded, contained, and verified,
- how support receives trustworthy handoff information,
- how disaster recovery and postmortem learning are handled.

Its purpose is to ensure that Pilgrims Mobile App is not only buildable and releasable, but also operable under real conditions in a way that remains:
- trustworthy,
- calm,
- auditable,
- rollback-safe,
- privacy-respecting,
- and resilient for long-term AI-assisted development.

