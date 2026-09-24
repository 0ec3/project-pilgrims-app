# 02 — AI AGENT RULES AND WORKFLOW

## Document status
- **Type:** Normative operating manual
- **Priority:** Highest
- **Audience:** AI coding agents, AI reviewer agents, AI debugging agents, migration agents, release agents, technical leads, product owner
- **Purpose:** Define exactly how AI agents must behave before, during, and after any task in this project.
- **Authority level:** This file governs AI-agent execution behavior across the entire repository.
- **Primary dependency:** `SPECS/01_README_AND_MASTER_INDEX.md`
- **Related files:** All files, with strongest linkage to `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`, `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`, `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`, `SPECS/13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`, `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`, `SPECS/30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md`, `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`, `SPECS/CONTRACTS/*`, and `tools/specs/validate_spec_contracts.py`.

---

# 1. Why this file exists

This project is intended to be buildable and maintainable by AI agents, but AI agents have predictable failure modes.

This file exists to prevent:
- hallucinated requirements,
- stale-file or stale-contract drift,
- code changes that pass tests while breaking real user behavior,
- undocumented schema/API/entitlement/screen changes,
- broad refactors hidden inside small tasks,
- inconsistent handling of privacy-light, safety, religious correctness, accessibility, offline, and release-evidence requirements.

---

# 2. Core operating principles

## 2.1 Read before changing
No task may begin with code changes. The agent must first read the required documentation and inspect the relevant code, data structures, interfaces, tests, and contracts.

## 2.2 Contracts over guesses
If a machine-readable contract exists, the agent must follow it. The agent must not invent alternative behavior because it seems cleaner, easier, or more modern.

## 2.3 Real correctness over fake success
A passing test suite is not proof that the implementation is correct. Real behavior, user flows, architecture, accessibility, offline behavior, data integrity, contract validation, and release evidence matter more than test greenness alone.

## 2.4 Ask when ambiguity is critical
If the task contains critical ambiguity that cannot be safely resolved from the spec set or codebase, the agent must ask for clarification instead of inventing behavior.

## 2.5 Preserve maintainability
The agent must avoid changes that make the system harder to maintain later, even if those changes appear faster in the short term.

## 2.6 Update docs when truth changes
If implementation changes canonical truth, the related markdown spec, contract artifact, validator expectation, test fixture, and progress/changelog entry must be updated in the same task where applicable.

## 2.7 Minimize refactor blast radius
Change the smallest safe surface needed to solve the task unless a broader refactor is explicitly approved and documented.

---

# 3. Agent roles covered by this file

- **Coding agent:** implements features, fixes bugs, writes tests, updates docs.
- **Reviewer agent:** checks spec alignment, architecture, maintainability, and real behavior expectations.
- **Debugging agent:** diagnoses issues, identifies root cause, applies minimal safe fixes.
- **Migration agent:** handles schema changes, data movement, and contract evolution.
- **Release agent:** verifies readiness, release gates, rollback safety, and evidence completeness.

All roles must follow this file.

---

# 4. Mandatory pre-task workflow

Before making any change, the agent must complete the following sequence.

## 4.1 Read root and governance documents first
Read, in order:
1. `SPECS/01_README_AND_MASTER_INDEX.md`
2. this file: `SPECS/02_AI_AGENT_RULES_AND_WORKFLOW.md`
3. `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`
4. `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`
5. `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md` when the task touches quality-first decisions, contracts, release gates, privacy, group coordination, entitlements, packs, advisory content, screen inventory, or safety/correctness boundaries.

## 4.2 Read task-specific canonical documents
The agent must identify the task type and read the relevant canonical documents.

### Flutter UI, navigation, or copy work
Read:
- `SPECS/07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`
- `SPECS/08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md`
- `SPECS/09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md`
- `SPECS/10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md`
- `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`
- `SPECS/12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md`
- the approved Figma visual reference when the task changes current visual styling, tokens, shared components, or screen composition
- relevant feature-family file
- `SPECS/CONTRACTS/screen_feature_traceability.yaml` when screens, navigation, analytics, accessibility evidence, or entitlement dependencies are touched.

### Backend, API, data, or realtime work
Read:
- `SPECS/06_SYSTEM_ARCHITECTURE.md`
- `SPECS/13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`
- `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`
- `SPECS/15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md`
- relevant feature-family file
- affected contract artifacts under `SPECS/CONTRACTS/`.

### Group, location, coordination, or map handoff work
Read:
- `SPECS/06_SYSTEM_ARCHITECTURE.md`
- `SPECS/07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`
- `SPECS/09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md`
- `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`
- `SPECS/13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`
- `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`
- `SPECS/15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md`
- `SPECS/16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md`
- `SPECS/19_FEATURE_MAPS_SAVE_MY_GATE_AND_3_D_WAYFINDING.md`
- `SPECS/20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md`
- `SPECS/24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md`
- `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`
- `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`
- `SPECS/CONTRACTS/entitlement_capability_policy.yaml` when access or Supporter behavior is touched.

### Ritual, RIC, content, phrasebook, advisory, or safety-assistive work
Read:
- `SPECS/12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md`
- `SPECS/18_FEATURE_RITUALS_RIC_AND_RELIGIOUS_CONTENT.md` where ritual correctness applies
- `SPECS/22_FEATURE_PHRASEBOOK_EMERGENCY_SAFETY_AND_ASSISTIVE_TOOLS.md` where assistance/advisory surfaces apply
- `SPECS/26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md`
- `SPECS/CONTRACTS/advisory_source_registry.schema.yaml` where advisory freshness/source metadata applies.

### Offline packs, audio, publishing, or content delivery work
Read:
- `SPECS/15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md`
- `SPECS/23_FEATURE_OFFLINE_PACKS_AUDIO_AND_CONTENT_DISTRIBUTION.md`
- `SPECS/26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md`
- `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`
- `SPECS/30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md`
- `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`.

### Account, settings, entitlement, subscription, or privacy/data work
Read:
- `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`
- `SPECS/13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`
- `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`
- `SPECS/24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md`
- `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`
- `SPECS/CONTRACTS/entitlement_capability_policy.yaml`
- `SPECS/CONTRACTS/screen_feature_traceability.yaml` where settings/privacy screens are touched.

### Testing, release, operations, or evidence work
Read:
- `SPECS/17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md`
- `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`
- `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`
- `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`
- `SPECS/30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md`
- `SPECS/CONTRACTS/release_gate_taxonomy.yaml`.

## 4.3 Review contract artifacts before editing contract-shaped behavior
If the task touches entitlement gates, group presence/freshness, pack trust, advisory source metadata, release gates, or screen traceability, the agent must read the relevant YAML contract before changing code or prose.

Current contract artifacts:
- `SPECS/CONTRACTS/entitlement_capability_policy.yaml`
- `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`
- `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`
- `SPECS/CONTRACTS/advisory_source_registry.schema.yaml`
- `SPECS/CONTRACTS/release_gate_taxonomy.yaml`
- `SPECS/CONTRACTS/screen_feature_traceability.yaml`

When a contract artifact changes, the agent must run or request validation with:

```bash
python tools/specs/validate_spec_contracts.py
```

Passing this validator proves only contract-file consistency. It does not prove runtime correctness, UX quality, legal compliance, field readiness, or release approval.

## 4.4 Inspect the real codebase before editing
The agent must inspect the actual implementation before proposing or applying code changes.

This includes, where relevant:
- existing module/folder layout,
- public interfaces,
- repositories/services,
- widgets/components,
- route definitions,
- theme/token sources,
- localization files,
- schema/migration files,
- API handlers,
- tests,
- feature flags,
- native bridge code,
- map providers and wrappers.

The agent must not assume the codebase matches the docs.

## 4.5 Identify impacted files before touching anything
Before editing, identify:
- source files likely to change,
- tests likely to change,
- docs that must be updated,
- migration or contract risks,
- screens or flows that could regress.

## 4.6 Restate the task internally in project terms
Convert the request into a project-aware task statement that includes:
- feature area,
- in-scope behavior,
- out-of-scope behavior,
- canonical docs that govern it,
- validation expectations.

---

# 5. Required clarification rules

AI agents must not improvise through critical ambiguity.

## 5.1 Ask clarification when any of the following is true
- The user request conflicts with documented product scope.
- The requested behavior contradicts a canonical contract file.
- A schema change is implied but the target structure is unclear.
- A new user flow is required but screen ownership is unclear.
- An entitlement/paywall rule is unclear.
- A map behavior requires provider-specific assumptions not documented.
- A religious correctness issue cannot be safely inferred.
- A platform-specific behavior is materially different on iOS vs Android and the intended behavior is unclear.
- The request could be solved in multiple ways with different architectural consequences.

## 5.2 Proceed without clarification only when
- canonical docs clearly resolve the ambiguity,
- the codebase clearly resolves the ambiguity,
- the user has already provided the necessary preference,
- the change is small, local, reversible, and does not alter contracts.

## 5.3 Invalid strategies
The agent must never:
- guess the product owner’s preference,
- copy patterns from unrelated code without checking whether they are canonical,
- change contracts because implementation is inconvenient,
- assume missing fields or states probably exist.

---

# 6. Scope control rules

## 6.1 Stay within the requested change surface
Do not add extra features, screens, entities, roles, settings, or monetization logic unless the task explicitly requires them.

## 6.2 Do not silently broaden product scope
Do not quietly reintroduce Hajj complexity into Umrah-first flows, add always-on location sharing, add passive location polling, add social features, or introduce official-service responsibilities unless explicitly approved.

## 6.3 Avoid speculative architecture expansion
Do not add abstractions, wrappers, or service layers “for future flexibility” unless there is a documented near-term reason.

## 6.4 Prefer minimal, durable solutions
The right solution is the smallest one that satisfies documented requirements, preserves architecture health, keeps future evolution possible, and avoids style or logic duplication.

---

# 7. Codebase inspection rules

## 7.1 Before changing Flutter UI code, inspect
- theme and token definitions,
- shared UI components,
- localization resources,
- navigation and route setup,
- relevant feature module,
- state management entry points,
- tests for the screen or component.

## 7.2 Before changing backend or data code, inspect
- schema definitions,
- migrations,
- RLS rules,
- repository/service boundaries,
- API request/response shapes,
- contract tests if present,
- downstream consumers.

## 7.3 Before changing map code, inspect
- provider wrapper layer,
- route generation logic,
- positioning code,
- cached/offline map data logic,
- feature flags,
- performance-sensitive rendering paths,
- test and device-lab coverage.

## 7.4 Before changing entitlements or account logic, inspect
- store integration paths,
- entitlement keys,
- gating helpers,
- purchase restoration flow,
- subscription copy,
- settings surfaces,
- analytics events.

---

# 8. Flutter-specific implementation rules

## 8.1 Centralize styling
Repeated visual values must come from centralized sources: colors, typography, spacing, radii, shadows, blur/material values, opacity presets, icon sizing, animation timing, transitions, and surface treatment rules.

## 8.2 Centralize reusable copy
Reusable UI strings must come from localization resources, not inline widget strings.

## 8.3 Reuse shared components
If a UI pattern already exists as a shared component, reuse it unless there is a documented reason not to.

## 8.4 Respect module boundaries
Feature widgets must not directly depend on low-level infrastructure or unrelated feature modules.

## 8.5 Do not create one-off styling debt
Do not solve urgent UI problems with one-off hardcoded fixes that bypass the design system.

For visual work, agents must inspect the current canonical design-system contract and the approved Figma reference before inventing new surface, depth, color, typography, or appearance patterns. Figma is visual evidence only; it must not override product scope, IA, screen IDs, localization, or feature semantics owned by the normative specs.

## 8.6 Respect platform adaptation rules
If a style or interaction differs on iOS and Android, follow the platform spec rather than improvising.

---

# 9. Data-model and migration safety rules

## 9.1 No schema guessing
Never infer new columns, relations, or invariants without confirming them in the canonical data model.

## 9.2 Schema changes require full impact review
Before any schema change, review related tables, foreign keys, ownership model, RLS implications, API contract implications, sync/offline implications, fixtures, migration plan, rollback plan, and affected contracts.

## 9.3 Additive-first migration strategy
Prefer additive migrations and staged rollouts over destructive changes.

## 9.4 Do not break historical data casually
Any data migration must consider existing rows, nullability, defaults, backfill, and rollback.

## 9.5 Document every contract-relevant schema change
If schema changes, update the data model doc and dependent contract docs in the same task.

---

# 10. API and contract safety rules

## 10.1 API contracts are authoritative
Do not change request/response shape without updating the canonical API contract, impacted consumers, affected contracts, tests, and release evidence.

## 10.2 Be explicit about failure modes
If an endpoint or realtime event can fail, timeout, retry, dedupe, or conflict, those behaviors must be respected and documented.

## 10.3 Preserve backward compatibility when possible
Prefer additive evolution and explicit deprecation.

## 10.4 Do not hide breaking changes inside implementation
A breaking contract change is a planning event, not just a code change.

---

# 11. Map and wayfinding rules

## 11.1 Treat map functionality as four layers
Distinguish positioning, routing/wayfinding logic, visual rendering including 3D, and offline fallback guidance.

## 11.2 Do not equate 3D visuals with navigation correctness
A beautiful 3D view is not a successful navigation implementation if location confidence, route logic, or fallback text directions are wrong.

## 11.3 Respect provider abstraction boundaries
Do not leak provider-specific assumptions through the whole codebase unless architecture explicitly allows it.

## 11.4 Test failure states seriously
Map changes must consider no GPS, low signal, provider render failure, partial offline pack availability, unknown floor, ambiguous user position, route not found, and stale map data.

---

# 12. Testing rules

## 12.1 Tests are necessary but not sufficient
Write or update tests where appropriate, but do not treat tests as the only proof of correctness.

## 12.2 Never change tests just to bless broken behavior
If a test fails because implementation regressed, fix implementation or explicitly document a valid behavior change.

## 12.3 Choose the right test layer
Use unit tests, widget tests, integration tests, end-to-end/manual checks, and device-specific validation according to the risk and behavior being changed.

## 12.4 Validate edge states
Consider loading, empty, offline, retry, partial sync, expired entitlement, localization/RTL, accessibility modes, poor network, interrupted downloads, and stale cache.

## 12.5 Respect the real-world verification layer
If a task affects user-critical behavior, release-evidence and manual-verification requirements must be considered, not skipped.

## 12.6 Validate contracts where applicable
If a task changes a machine-readable contract, run `python tools/specs/validate_spec_contracts.py` and record the result in the handoff.

---

# 13. Definition of done for AI agents

A task is only done when all of the following are true:
- the implementation matches the intended task and does not introduce unrelated scope,
- module boundaries, centralized theming, shared components, and documented contracts are respected,
- the feature works correctly in realistic scenarios,
- no relation, invariant, ownership rule, migration expectation, or contract artifact is violated,
- relevant tests and validators pass or any inability to run them is honestly documented,
- required docs are updated,
- future contributors can understand what changed and why.

---

# 14. Mandatory post-task workflow

After implementing a change, the agent must:
1. determine whether the task changed canonical truth,
2. update docs in the same task when contracts, flows, architecture, or behavior changed,
3. update contract artifacts and validators when contract truth changed,
4. record progress/changelog if the project workflow requires it,
5. run or verify the right test and validation layers,
6. check adjacent flows and related modules for unintended regressions,
7. summarize what changed, why, which files were updated, and any remaining risk.

---

# 15. Required document update rules

## 15.1 If Flutter module structure changes
Update `SPECS/07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`, `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`, and possibly feature-family files and test docs.

## 15.2 If themes, tokens, or components change
Update `SPECS/08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md`, `SPECS/09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md` if platform behavior changes, `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md` if screen blueprints change, impacted feature-family docs, and `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`.

## 15.3 If data model changes
Update `SPECS/13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`, `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`, impacted feature-family docs, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`, and affected files in `SPECS/CONTRACTS/`.

## 15.4 If API or realtime contracts change
Update `SPECS/14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`, impacted feature docs, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`, and affected files in `SPECS/CONTRACTS/`.

## 15.5 If map behavior changes
Update `SPECS/16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md`, `SPECS/19_FEATURE_MAPS_SAVE_MY_GATE_AND_3_D_WAYFINDING.md`, `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`, `SPECS/17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md`, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, and `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`.

## 15.6 If onboarding, Home, or Simple Mode changes
Update `SPECS/10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md`, `SPECS/11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`, `SPECS/12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md` if copy/accessibility changes, `SPECS/25_FEATURE_ONBOARDING_HOME_AND_SIMPLE_MODE.md`, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, and `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`.

## 15.7 If ritual, RIC, or governed content changes
Update `SPECS/18_FEATURE_RITUALS_RIC_AND_RELIGIOUS_CONTENT.md`, `SPECS/26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md`, `SPECS/12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md` if user-facing wording changes, `SPECS/27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`, `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, and `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`.

## 15.8 If release or operational behavior changes
Update `SPECS/28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`, `SPECS/29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`, `SPECS/30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md`, `SPECS/05_ROADMAP_PROGRESS_AND_CHANGELOG.md`, and `SPECS/CONTRACTS/release_gate_taxonomy.yaml` where release taxonomy changes.

## 15.9 If entitlement, group presence, pack trust, advisory source, release gate, or screen traceability contracts change
Update the owning markdown spec, affected feature/system specs, affected tests, `tools/specs/validate_spec_contracts.py` if validation semantics changed, and run the validator.

## 15.10 If canonical documentation files are edited directly
Preserve document-status metadata, remove obsolete drafting residue, preserve canonical file-number references, use current underscore filenames for concrete paths, and run a consistency scan for affected endpoints, file numbers, metadata, and contract references.

---

# 16. Reviewer-agent checklist

A reviewer agent must verify:
- scope and intent,
- architecture and module boundaries,
- data relations, API contracts, and invariants,
- contract artifacts and validator status where relevant,
- UX readability, offline behavior, localization/RTL, and accessibility,
- testing/validation sufficiency,
- maintainability and absence of speculative abstractions.

---

# 17. Recovery workflow when the agent is confused

If confused, the agent must:
1. identify whether confusion is about product scope, architecture, data relations, contract shape, feature flow, platform behavior, map provider assumptions, test expectations, or existing code behavior,
2. re-read canonical docs,
3. re-inspect the codebase,
4. ask for clarification if critical ambiguity remains,
5. avoid papering over confusion with broad refactor or abstraction.

---

# 18. Recovery workflow when codebase and docs disagree

The agent must determine whether docs are ahead of implementation, code evolved without docs, or a previous task introduced drift. Existing code is not automatically authoritative, and documentation may also lag. Resolve by canonical file authority, decision records, recent changelog entries, task history, and explicit user direction. Critical truth conflicts must be escalated rather than guessed.

---

# 19. Anti-patterns explicitly forbidden in this project

Forbidden behaviors include:
- hardcoding repeated style values in widgets,
- copy-paste implementation across feature modules when shared boundaries exist,
- silent schema/API/contract changes,
- broad refactor hidden inside a bug fix,
- rewriting tests to accept a regression without explicit justification,
- adding fields, enums, states, screens, or flows “just in case,”
- skipping documentation updates because code is “self-explanatory,”
- treating visual polish as more important than readability,
- treating 3D maps as purely visual,
- assuming AI memory is enough to preserve context,
- bypassing contract artifacts or validators for convenience.

---

# 20. Task templates for AI agents

## 20.1 Feature implementation template
- What exact user problem is being solved?
- Which feature-family file owns this?
- Which screens are affected?
- Which data/API/contracts are affected?
- Which edge cases matter?
- Which tests and docs must be updated?

## 20.2 Bug-fix template
- What is the real root cause?
- Is it local or systemic?
- Which contract or invariant is being violated?
- Can it be fixed with a minimal change?
- What adjacent regressions must be checked?

## 20.3 Refactor template
- Why is refactor needed?
- What exact pain does it solve?
- What boundaries will it touch?
- Is it approved and documented?
- What must prove it reduced risk rather than increased it?

## 20.4 Data migration template
- What invariant is changing?
- What is the rollout strategy?
- How is historical data handled?
- How is rollback handled?
- Which consumers and contracts need updating?

---

# 21. Evidence expectations for sensitive areas

## 21.1 Ritual correctness
Changes affecting ritual guidance, RIC, or remedies require careful review against ritual and content-governance docs.

## 21.2 Emergency and safety flows
Changes affecting emergency cards, phrasebook emergency mode, or safety alerts must preserve immediacy, legibility, offline access, and low-friction interaction.

## 21.3 Map and wayfinding
Changes affecting wayfinding must preserve correctness under uncertainty and degraded conditions.

## 21.4 Subscription and entitlement logic
Changes affecting entitlements must preserve ethical boundaries and avoid accidental paywall expansion into correctness or safety-critical content.

## 21.5 Group coordination and shared freshness
Changes affecting group creation, check-ins, regroup, route handoff, or live board state must preserve explicit user action, bounded freshness, authorization, and honest stale/offline representation.

---

# 22. Handoff requirements between agents

When one AI agent hands off to another, the handoff must include:
- task goal,
- current status,
- files changed,
- files still needing changes,
- unresolved questions,
- known risks,
- required validation still pending.

The handoff must not assume the next agent has reliable memory of prior context.

---

# 23. Minimum quality standard for agent-generated output

Every agent-generated change should aim for:
- clear structure,
- minimal unnecessary complexity,
- consistency with the spec system,
- strong naming,
- maintainable abstractions,
- centralized style usage,
- thoughtful edge-state handling,
- honest handling of uncertainty,
- documented follow-up if incomplete.

---

# 24. Summary

This file defines how AI agents must operate in this project.

Its purpose is to protect the project from hallucination, context loss, stale file references, bad assumptions, contract drift, fake-green test success, scattered styling, refactor debt, and undocumented changes.

Any AI agent that works on this project must follow this file together with the root index, file `31` where applicable, relevant canonical specs, and affected contract artifacts before making changes.
