# 02 — AI AGENT RULES AND WORKFLOW

## Document status
- **Type:** Normative operating manual
- **Priority:** Highest
- **Audience:** AI coding agents, AI reviewer agents, AI debugging agents, technical leads, product owner
- **Purpose:** Define exactly how AI agents must behave before, during, and after any task in this project.
- **Authority level:** This file governs AI-agent execution behavior across the entire repository.
- **Primary dependency:** `01-README-AND-MASTER-INDEX.md`
- **Related files:** All files, with strongest linkage to `03`, `05`, `07`, `08`, `13`, `14`, `16`, `27`, `28`, and `30`

---

# 1. Why this file exists

This project is intended to be buildable and maintainable by AI agents, but AI agents have predictable failure modes.

In earlier project discussions, the following risks were explicitly identified:
- AI coding agents hallucinate missing requirements.
- AI agents misread instructions and drift away from the main plan.
- AI agents discover errors or complexity mid-task and silently improvise the wrong solution.
- AI agents often optimize for passing automatic tests even when the real app becomes worse.
- AI agents lose context after many tasks or large code generation sessions.
- AI agents frequently implement the wrong code because they did not inspect the real codebase, database relations, or related docs first.
- AI agents sometimes do not know how to implement a complex module or flow, but still proceed without asking clarification.
- AI agents get confused about development progress if progress tracking is missing or stale.
- AI agents get confused when there are many docs and no clear rule for which doc to read, trust, or update.
- AI agents create refactor debt when they do not understand module behavior, design-system boundaries, or data relationships.

This file exists to prevent those failures.

---

# 2. Core operating principles

Every AI agent working on this project must follow these principles.

## 2.1 Read before changing
No task may begin with code changes. The agent must first read the required documentation and inspect the relevant code, data structures, and interfaces.

## 2.2 Contracts over guesses
If a contract file exists, the agent must follow it. The agent must not invent alternative behavior because it seems cleaner, easier, or more modern.

## 2.3 Real correctness over fake success
A passing test suite is not proof that the implementation is correct. Real behavior, user flows, architecture, accessibility, offline behavior, and data integrity matter more than test greenness alone.

## 2.4 Ask when ambiguity is critical
If the task contains critical ambiguity that cannot be safely resolved from the spec set or codebase, the agent must ask for clarification instead of inventing behavior.

## 2.5 Preserve maintainability
The agent must avoid changes that make the system harder to maintain later, even if those changes appear faster in the short term.

## 2.6 Update the docs when the truth changes
If the implementation changes canonical truth, the related documentation must be updated in the same task.

## 2.7 Minimize refactor blast radius
The agent must change the smallest safe surface needed to solve the task unless a broader refactor is explicitly approved and documented.

---

# 3. Agent roles covered by this file

## 3.1 Coding agent
Implements features, fixes bugs, writes tests, updates docs.

## 3.2 Reviewer agent
Checks alignment with specs, architecture, maintainability, and real behavior expectations.

## 3.3 Debugging agent
Diagnoses issues, identifies root cause, proposes and applies minimal safe fixes.

## 3.4 Migration agent
Handles schema changes, data movement, or contract evolution.

## 3.5 Release agent
Verifies readiness, release gates, rollback safety, and evidence completeness.

All roles must follow this file.

---

# 4. Mandatory pre-task workflow

Before making any change, the agent must complete the following sequence.

## 4.1 Read the root documents first
The agent must read, in order:
1. `01-README-AND-MASTER-INDEX.md`
2. this file: `02-AI-AGENT-RULES-AND-WORKFLOW.md`
3. `03-PRODUCT-CHARTER-AND-SCOPE.md`

## 4.2 Read task-specific canonical documents
The agent must identify the task type and read the relevant canonical documents.

### For Flutter UI work
Read:
- `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
- `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`
- `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`
- `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`
- `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`
- `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`
- relevant feature-family file

### For backend/API/data work
Read:
- `06-SYSTEM-ARCHITECTURE.md`
- `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`
- `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
- `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`
- relevant feature-family file

### For map and wayfinding work
Read:
- `06`
- `07`
- `09`
- `11`
- `13`
- `14`
- `15`
- `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`
- `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`

### For ritual/content correctness work
Read:
- `12`
- `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`
- `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`

### For release or validation work
Read:
- `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`
- `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`
- `29-SECURITY-PRIVACY-COMPLIANCE-AND-RISK-REGISTER.md`
- `30-DELIVERY-RUNBOOK-INCIDENTS-ROLLBACK-AND-OPERATIONS.md`

## 4.3 Inspect the real codebase before editing
The agent must inspect the actual implementation before proposing or applying changes.

This includes, where relevant:
- existing module/folder layout,
- existing public interfaces,
- existing repositories/services,
- existing widgets/components,
- route definitions,
- theme/token sources,
- localization files,
- schema/migration files,
- API handlers,
- test files,
- feature flags,
- native bridge code,
- map providers and wrappers.

The agent must not assume the codebase matches the docs. It must verify.

## 4.4 Identify impacted files before touching anything
Before editing, the agent must identify:
- source files likely to change,
- tests likely to change,
- docs that must be updated,
- migration or contract risks,
- screens or flows that could regress.

## 4.5 Restate the task internally in project terms
The agent must convert the request into a project-aware task statement that includes:
- feature area,
- in-scope behavior,
- out-of-scope behavior,
- canonical docs that govern it,
- validation expectations.

---

# 5. Required clarification rules

AI agents must not improvise through critical ambiguity.

## 5.1 The agent must ask clarification when any of the following is true
- The user request conflicts with the documented product scope.
- The requested behavior contradicts a canonical contract file.
- A schema change is implied but the target structure is unclear.
- A new user flow is required but screen ownership is unclear.
- An entitlement/paywall rule is unclear.
- A map behavior requires provider-specific assumptions not documented.
- A religious correctness issue cannot be safely inferred.
- A platform-specific behavior is materially different on iOS vs Android and the intended behavior is unclear.
- The request could be solved in multiple ways with different architectural consequences.

## 5.2 The agent may proceed without clarification only when
- the canonical docs clearly resolve the ambiguity,
- the codebase clearly resolves the ambiguity,
- the user has already provided the necessary preference,
- the change is small, local, reversible, and does not alter contracts.

## 5.3 The agent must never use these invalid strategies
- guessing the product owner’s preference,
- copying patterns from unrelated parts of the codebase without checking if they are still canonical,
- changing contracts because implementation is inconvenient,
- assuming missing fields or states “probably exist.”

---

# 6. Scope control rules

## 6.1 Stay within the requested change surface
The agent must not add extra features, extra screens, extra entities, extra roles, extra settings, or extra monetization logic unless the task explicitly requires them.

## 6.2 Do not silently broaden product scope
The agent must not quietly reintroduce Hajj complexity into Umrah-first flows, add always-on location sharing, add background tracking, add social features, or introduce official-service responsibilities unless those changes are explicitly approved.

## 6.3 Avoid speculative architecture expansion
Do not add abstractions, wrappers, or service layers “for future flexibility” unless there is a documented near-term reason.

## 6.4 Prefer minimal, durable solutions
The right solution is the smallest one that:
- satisfies the documented requirements,
- preserves architecture health,
- keeps future evolution possible,
- does not create style or logic duplication.

---

# 7. Codebase inspection rules

## 7.1 Before changing Flutter UI code, the agent must inspect
- theme and token definitions,
- shared UI components,
- localization resources,
- navigation and route setup,
- the relevant feature module,
- state management entry points,
- test coverage for the screen or component.

## 7.2 Before changing backend or data code, the agent must inspect
- schema definitions,
- migrations,
- RLS rules,
- repository/service boundaries,
- API request/response shapes,
- contract tests if present,
- any downstream consumers.

## 7.3 Before changing map code, the agent must inspect
- provider wrapper layer,
- route generation logic,
- positioning code,
- cached/offline map data logic,
- feature flags,
- performance-sensitive rendering paths,
- test and device-lab coverage.

## 7.4 Before changing entitlements or account logic, the agent must inspect
- store integration paths,
- entitlement keys,
- gating helpers,
- purchase restoration flow,
- subscription copy,
- settings surfaces,
- analytics events.

---

# 8. Flutter-specific implementation rules

This section is mandatory for any agent touching Flutter code.

## 8.1 Centralize styling
The agent must never spread repeated visual values across feature widgets.

The following must come from centralized sources:
- colors,
- typography,
- spacing,
- radii,
- shadows,
- blur/material values,
- opacity presets,
- icon sizing rules,
- animation durations,
- animation curves,
- page transitions,
- surface treatment rules.

## 8.2 Centralize reusable copy
Reusable UI strings must come from localization resources, not inline widget strings.

## 8.3 Reuse shared components
If a UI pattern already exists as a shared component, the agent must reuse it unless there is a documented reason not to.

## 8.4 Respect module boundaries
Feature widgets must not directly depend on low-level infrastructure or unrelated feature modules.

## 8.5 Do not create one-off styling debt
The agent must not solve urgent UI problems with one-off hardcoded fixes that bypass the design system.

## 8.6 Respect platform adaptation rules
If a style or interaction differs on iOS and Android, the agent must follow the platform spec rather than improvising.

---

# 9. Data-model and migration safety rules

## 9.1 No schema guessing
The agent must never infer new columns, relations, or invariants without confirming them in the canonical data model.

## 9.2 Schema changes require full impact review
Before any schema change, the agent must review:
- related tables,
- foreign keys,
- ownership model,
- RLS implications,
- API contract implications,
- sync/offline implications,
- test fixture implications,
- migration/rollback implications.

## 9.3 Additive-first migration strategy
Prefer additive migrations and staged rollouts over destructive changes.

## 9.4 Do not break historical data casually
Any data migration must consider existing rows, nullability, defaults, backfill, and rollback.

## 9.5 Document every contract-relevant schema change
If the schema changes, the data model doc and any dependent contract docs must be updated in the same task.

---

# 10. API and contract safety rules

## 10.1 API contracts are authoritative
The agent must not change request or response shape without updating the canonical contract doc and all impacted consumers.

## 10.2 Be explicit about failure modes
If an endpoint or realtime event can fail, timeout, retry, dedupe, or conflict, those behaviors must be respected and documented.

## 10.3 Preserve backward compatibility when possible
If a contract must evolve, prefer additive evolution and explicit deprecation.

## 10.4 Do not hide breaking changes inside implementation
A breaking contract change is a planning event, not just a code change.

---

# 11. Map and wayfinding rules

Because the map subsystem is complex, AI agents must follow stricter rules here.

## 11.1 Treat map functionality as four layers
The agent must distinguish between:
- positioning,
- routing/wayfinding logic,
- visual rendering including 3D,
- offline fallback guidance.

## 11.2 Do not equate 3D visuals with navigation correctness
A beautiful 3D view is not a successful navigation implementation if location confidence, route logic, or fallback text directions are wrong.

## 11.3 Respect provider abstraction boundaries
Do not leak provider-specific assumptions through the whole codebase unless the architecture explicitly allows it.

## 11.4 Test failure states seriously
Map changes must consider:
- no GPS,
- low signal,
- provider render failure,
- partial offline pack availability,
- unknown floor,
- ambiguous user position,
- route not found,
- stale map data.

---

# 12. Testing rules

## 12.1 Tests are necessary but not sufficient
The agent must write or update tests where appropriate, but must not treat tests as the only proof of correctness.

## 12.2 Never change tests just to bless broken behavior
If a test fails because the implementation regressed, the agent must fix the implementation or explicitly document a valid behavior change.

## 12.3 The agent must choose the right test layer
Use:
- unit tests for logic,
- widget tests for UI states,
- integration tests for flow boundaries,
- end-to-end or manual checks for real user behavior,
- device-specific validation for maps, native bridges, and performance-sensitive features.

## 12.4 Validate edge states
The agent must consider:
- loading,
- empty,
- offline,
- retry,
- partial sync,
- expired entitlement,
- localization/RTL,
- accessibility modes,
- poor network,
- interrupted downloads,
- stale cache.

## 12.5 Respect the real-world verification layer
If a task affects user-critical behavior, the release-evidence and manual-verification requirements must be considered, not skipped.

---

# 13. Definition of done for AI agents

A task is only done when all of the following are true.

## 13.1 Scope correctness
The implementation matches the intended task and does not introduce unrelated scope.

## 13.2 Architectural correctness
The implementation respects module boundaries, centralized theming, shared components, and documented contracts.

## 13.3 Behavioral correctness
The feature works correctly in realistic scenarios, not just ideal ones.

## 13.4 Data correctness
No relation, invariant, ownership rule, or migration expectation is violated.

## 13.5 Test correctness
Relevant tests pass and still reflect intended behavior.

## 13.6 Documentation correctness
All required docs are updated.

## 13.7 Reviewability
A future contributor or AI agent can understand what changed and why.

---

# 14. Mandatory post-task workflow

After implementing a change, the agent must complete this workflow.

## 14.1 Re-check impacted docs
The agent must determine whether the task changed any canonical truth.

## 14.2 Update docs in the same task
If the task changed contracts, flows, architecture, or behavior, the relevant docs must be updated immediately.

## 14.3 Record progress
The task status and change summary must be reflected in the progress/changelog file if the project workflow requires it.

## 14.4 Re-run or verify relevant tests
The agent must verify the right test layers, not just the fastest ones.

## 14.5 Re-check for unintended regressions
The agent must consider adjacent flows and related modules.

## 14.6 Summarize the change clearly
The final handoff should state:
- what changed,
- why it changed,
- which files were updated,
- any remaining risk or follow-up.

---

# 15. Required document update rules

The following update rules are mandatory.

## 15.1 If Flutter module structure changes
Update:
- `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
- `05-ROADMAP-PROGRESS-AND-CHANGELOG.md`
- possibly feature-family files and test docs

## 15.2 If themes, tokens, or components change
Update:
- `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`
- `09` if platform-specific behavior changes
- `11` if screen blueprints change
- impacted feature-family docs
- `05`

## 15.3 If data model changes
Update:
- `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`
- `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
- impacted feature-family docs
- `27`
- `28`
- `05`

## 15.4 If API or realtime contracts change
Update:
- `14`
- impacted feature docs
- `27`
- `28`
- `05`

## 15.5 If map behavior changes
Update:
- `16`
- `19`
- `11`
- `17`
- `27`
- `28`
- `05`

## 15.6 If onboarding, home, or simple mode changes
Update:
- `10`
- `11`
- `12` if copy or accessibility changes
- `25`
- `27`
- `28`
- `05`

## 15.7 If content workflow or ritual behavior changes
Update:
- `18`
- `26`
- `12` if user-facing wording changes
- `27`
- `28`
- `05`

## 15.8 If release or operational behavior changes
Update:
- `28`
- `29`
- `30`
- `05`

## 15.9 If canonical documentation files are edited directly
The agent must preserve document hygiene:
- keep the document-status block complete and syntactically intact,
- do not leave unresolved placeholder metadata, draft scaffolding, or obsolete drafting residue in canonical docs once the file set exists,
- preserve or update canonical file-number references when boundaries move,
- remove unnecessary tracking query parameters from embedded reference links,
- re-run a quick consistency scan for affected endpoints, file numbers, and metadata after editing.

---

# 16. Reviewer-agent checklist

A reviewer agent must verify all of the following.

## 16.1 Scope and intent
- Does the change stay within requested scope?
- Did the coding agent invent anything not requested?

## 16.2 Architecture
- Does the change respect module boundaries?
- Does it preserve centralized design and shared patterns?

## 16.3 Data and contracts
- Are data relations, API contracts, and invariants preserved?
- Were docs updated if truth changed?

## 16.4 UX and accessibility
- Does the change preserve readability, offline behavior, and accessibility?
- Does it respect platform adaptation rules?

## 16.5 Testing and validation
- Were the right tests updated?
- Is there any sign that tests were modified to approve broken behavior?

## 16.6 Maintainability
- Did the agent add duplication, hardcoded styling, hidden coupling, or speculative abstractions?

---

# 17. Recovery workflow when the agent is confused

If the agent becomes confused mid-task, it must not continue blindly.

## 17.1 Pause and identify confusion type
The agent must determine whether the confusion is about:
- product scope,
- architecture,
- data relations,
- contract shape,
- feature flow,
- platform behavior,
- map provider assumptions,
- test expectations,
- existing code behavior.

## 17.2 Re-read canonical docs
The agent must re-read the most relevant canonical files before making further changes.

## 17.3 Re-inspect the codebase
The agent must verify whether the confusion comes from stale assumptions or real code divergence.

## 17.4 Ask for clarification if still unresolved
If critical ambiguity remains, the agent must ask.

## 17.5 Do not paper over confusion with refactor or abstraction
Confusion is not a valid reason to widen the change surface.

---

# 18. Recovery workflow when the codebase and docs disagree

Sometimes the codebase may not match the documented design.

## 18.1 Determine which is intended truth
The agent must evaluate whether:
- the docs are ahead of implementation,
- the code evolved without docs,
- a previous task introduced drift.

## 18.2 Do not assume code is automatically correct
Existing code is not authoritative just because it exists.

## 18.3 Do not assume docs are automatically current
Documentation may also lag.

## 18.4 Resolve by evidence
Use:
- canonical file authority,
- decision records,
- recent changelog entries,
- task history,
- explicit user direction.

## 18.5 If still unclear, ask
Critical truth conflicts must be escalated rather than guessed.

---

# 19. Anti-patterns explicitly forbidden in this project

The following behaviors are forbidden.

## 19.1 Hardcoding repeated style values in widgets
Forbidden unless explicitly documented as a temporary exception.

## 19.2 Copy-paste implementation across feature modules
Forbidden when shared component or shared logic boundaries exist.

## 19.3 Silent schema or API changes
Forbidden.

## 19.4 Broad refactor hidden inside a bug fix
Forbidden.

## 19.5 Rewriting tests to accept a regression without explicit justification
Forbidden.

## 19.6 Adding fields, enums, states, or flows “just in case”
Forbidden.

## 19.7 Skipping documentation updates because the code “is self-explanatory”
Forbidden.

## 19.8 Treating visual polish as more important than readability
Forbidden, especially for ritual text, emergency flows, and wayfinding.

## 19.9 Treating 3D maps as purely visual
Forbidden.

## 19.10 Assuming AI memory is enough to preserve context
Forbidden. The documentation system is the memory backbone.

---

# 20. Task templates for AI agents

These are mandatory mental templates for common work types.

## 20.1 Feature implementation template
- What exact user problem is being solved?
- Which feature-family file owns this?
- Which screens are affected?
- Which data/contracts are affected?
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
- What must be proven to show it reduced risk rather than increased it?

## 20.4 Data migration template
- What invariant is changing?
- What is the rollout strategy?
- How is historical data handled?
- How is rollback handled?
- Which consumers need updating?

---

# 21. Evidence expectations for sensitive areas

Certain parts of this app require extra caution.

## 21.1 Ritual correctness
Changes affecting ritual guidance, RIC, or remedies require especially careful review against the ritual and content-governance docs.

## 21.2 Emergency and safety flows
Changes affecting emergency cards, phrasebook emergency mode, or safety alerts must preserve immediacy, legibility, offline access, and low-friction interaction.

## 21.3 Map and wayfinding
Changes affecting wayfinding must preserve correctness under uncertainty and degraded conditions.

## 21.4 Subscription and entitlement logic
Changes affecting entitlements must preserve ethical boundaries and avoid accidental paywall expansion into correctness or safety-critical content.

---

# 22. Handoff requirements between agents

When one AI agent hands off to another, the handoff must include:
- task goal,
- current status,
- files changed,
- files that still need changes,
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

Its purpose is not just to improve code quality, but to protect the project from the exact failure modes that AI-assisted development commonly introduces:
- hallucination,
- context loss,
- bad assumptions,
- contract drift,
- fake-green test success,
- scattered styling,
- refactor debt,
- undocumented changes.

Any AI agent that works on this project must follow this file together with the root index and the relevant canonical spec files before making changes.

