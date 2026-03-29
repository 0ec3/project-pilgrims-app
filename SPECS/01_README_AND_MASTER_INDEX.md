# 01 — README AND MASTER INDEX

## Document status
- **Type:** Normative root document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, backend engineer, Flutter engineer, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** This is the root entry point for the full documentation system. Every human contributor and every AI agent must begin here before reading or editing any other spec file.
- **Last-updated-by:** AI-assisted hardening pass (validated 2026-03-22)
- **Related files:** All files in this spec system

---

# 1. What this project is

Pilgrims Mobile App is a mobile companion app for Muslim pilgrims, designed to help them perform rituals correctly, stay oriented in complex holy-site environments, coordinate with their family or group, and access practical assistance under stressful, low-connectivity, and high-fatigue conditions.

The product is intentionally focused. It is **not** trying to become a general travel super-app, a package-booking marketplace, a visa-processing platform, or an official government services replacement. Its primary value is calm, trustworthy, offline-capable support during pilgrimage.

The product is **Umrah-first by default**, with strong boundaries around seasonality and scope. Hajj-related expansion must follow documented release and approval rules.

The app must be designed so that:
- religious correctness is never treated casually,
- safety-critical help is never hidden behind dark patterns,
- offline functionality is treated as a core capability,
- UI remains legible and calm under stress,
- the codebase remains maintainable as complexity grows,
- AI coding agents can build and maintain the app with minimal ambiguity.

---

# 2. Why this documentation system exists

This documentation system exists to make the app buildable and maintainable by both humans and AI coding agents.

It is specifically designed to reduce the risks we identified in prior planning discussions:
- AI agents hallucinating requirements or architecture,
- AI agents misreading feature scope,
- AI agents changing code to satisfy tests while breaking real behavior,
- AI agents losing track after many tasks and large code generation,
- AI agents misunderstanding data relationships,
- AI agents implementing the wrong flow because context is spread across too many places,
- AI agents failing to update documentation after implementation,
- AI agents introducing refactor debt because they do not understand module boundaries,
- AI agents hardcoding UI and style values across many files, making future visual changes expensive.

This spec system is therefore built around five principles:
1. **Contract-first** — Core truths must be documented before implementation.
2. **Single source of truth** — Every major concern has one canonical home.
3. **Controlled modularity** — The docs are compact, but hard contracts remain separated.
4. **AI-agent recoverability** — A new agent must be able to resume safely with minimal confusion.
5. **Implementation readiness** — The docs must be precise enough to build from, not just discuss from.

---

# 3. Core product direction

## 3.1 Product mission
Help Muslim pilgrims complete their journey with more confidence, correctness, calm, and coordination.

## 3.2 Primary jobs to be done
The app exists to help users:
- understand what to do during pilgrimage,
- recover when they make a mistake or become uncertain,
- navigate and re-orient themselves in crowded or unfamiliar environments,
- stay coordinated with their family or group,
- access practical assistance in moments of stress, confusion, or urgency,
- prepare, remember, and organize key items before and during the journey.

## 3.3 Product positioning
This app is a **pilgrimage companion**, not a generalized Islamic lifestyle app and not a general mapping app.

## 3.4 Product philosophy
The app must feel:
- calm,
- trustworthy,
- respectful,
- practical,
- low-friction,
- resilient under poor connectivity,
- easy to use even when the user is tired, anxious, elderly, distracted, or unfamiliar with smartphones.

---

# 4. Key decisions already established

The following decisions have been established from earlier planning and discussion and should be treated as active direction unless later changed through documented decision control.

## 4.1 Documentation strategy decision
The final spec system uses **30 files**, not dozens of fragmented files and not an over-compressed minimal set. This is the intended balance between coverage and navigability.

## 4.2 AI-agent-first maintainability decision
The documentation architecture is intentionally optimized for AI coding agents.

That means:
- files must state their purpose clearly,
- hard contracts must stay separate,
- related feature concerns may be grouped into feature-family files,
- update responsibilities must be explicit,
- progress tracking and change tracking must be preserved,
- Flutter architecture and UI design rules must be centralized.

## 4.3 Flutter maintainability decision
The Flutter codebase must be structured for long-term maintainability.

This includes:
- modular folder structure,
- centralized themes,
- centralized design tokens,
- centralized typography,
- centralized spacing and sizing rules,
- centralized effect and animation rules,
- reusable shared components,
- no hardcoded style values scattered across many widgets,
- no inline business copy for reusable UI strings,
- clear dependency direction between modules.

## 4.4 Platform design decision
The UI direction should support an iOS-specific visual adaptation inspired by Apple’s Liquid Glass design direction where appropriate, while preserving readability and not overusing decorative translucency.

The app must not sacrifice ritual text readability, safety messages, or map clarity for style.

## 4.5 Map strategy decision
The mapping experience should aim toward an Al-Maqsad-like feel in utility and spatial guidance, but the spec must treat map functionality as a system composed of:
- positioning,
- routing graph and wayfinding logic,
- 3D scene rendering,
- offline fallback guidance.

The map system must not be specified as “just a pretty 3D map.”

## 4.6 Product scope decision
The app remains Umrah-first unless later release planning explicitly broadens scope. The docs must not quietly reintroduce Hajj complexity into default flows without approval.

## 4.7 Official-services boundary decision
The app may guide users to official services or hand off to official service ecosystems when needed, but must not assume responsibility for ministry-controlled, permit-controlled, or government-managed processes unless explicitly planned.

## 4.8 Simplicity under stress decision
The product should include a simplified operating path for stressed, elderly, low-literacy, or low-confidence users. This principle should influence onboarding, home screen, phrasebook, emergency presentation, and high-priority actions.

---

# 5. Recommendations and improvements incorporated into the new spec system

The new compact spec structure already includes several improvements based on earlier analysis and research.

## 5.1 Centralized UI system improvement
A dedicated design-system and theme file is included so that visual updates can be made from centralized theme and token sources rather than requiring edits across many Flutter widgets.

This improves:
- maintainability,
- design consistency,
- speed of visual iteration,
- AI-agent reliability.

## 5.2 Dedicated map architecture improvement
A dedicated map architecture spec is included because 3D pilgrimage wayfinding is too complex to bury inside a generic feature file.

This reduces confusion between:
- map provider choice,
- 3D rendering,
- indoor positioning,
- routing logic,
- offline text fallback.

## 5.3 Emergency and simple-mode improvement
The feature-family structure explicitly protects emergency tools, phrasebook, safety flows, and simplified operation as first-class product concerns rather than optional extras.

## 5.4 Release-proofing improvement
Real-world verification and release evidence are preserved as standalone spec areas so that automated tests cannot be mistaken for product correctness.

## 5.5 AI-agent continuity improvement
Progress, changelog, decisions, and handoff context are consolidated so future AI agents can recover project context quickly.

## 5.6 Official-services handoff improvement
The new structure leaves room for a documented handoff strategy to official service ecosystems when needed, reducing legal, operational, and trust risk.

---

# 6. Non-negotiable implementation principles

The following rules apply across the entire project.

## 6.1 No uncontrolled scope growth
No contributor or AI agent may add new features, new entities, new roles, new subscription logic, or new user flows simply because they “seem useful” unless the change is documented and approved.

## 6.2 No undocumented refactor
No broad refactor may be performed without first verifying module boundaries and documenting the reason, expected benefit, and impacted files.

## 6.3 No fake-green success
Passing automated tests is not sufficient proof of correctness.
A task is not complete if:
- real device behavior is broken,
- navigation is wrong,
- data relationships are broken,
- offline behavior regressed,
- accessibility regressed,
- UI became inconsistent,
- performance became unacceptable.

## 6.4 No duplicate source of truth
If a rule is already canonical in one file, another file must reference it instead of silently redefining it.

## 6.5 No hardcoded visual system values in feature widgets
Feature widgets must not hardcode repeated colors, spacing, typography, blur, animation timings, radii, or elevation values. These must come from centralized theme/token infrastructure.

## 6.6 No hidden contract changes
Any change to:
- API shape,
- data model,
- entitlement logic,
- routing rules,
- map behavior,
- feature state machine,
- localization model,
- offline sync behavior,
must be reflected in the relevant canonical docs.

## 6.7 Ask when critical ambiguity exists
If an AI agent does not understand a critical requirement and cannot safely infer it from the documented sources, it must ask for clarification rather than inventing behavior.

---

# 7. How to use this documentation system

## 7.1 For humans
1. Start with this file.
2. Read the product charter and scope.
3. Read architecture, Flutter structure, design system, data model, API contracts, and map architecture.
4. Read the relevant feature-family file.
5. Read testing and release verification requirements before implementation.

## 7.2 For AI coding agents
Every AI coding agent must begin by reading, in order:
1. `01-README-AND-MASTER-INDEX.md`
2. `02-AI-AGENT-RULES-AND-WORKFLOW.md`
3. `03-PRODUCT-CHARTER-AND-SCOPE.md`
4. The most relevant contract files for the task
5. The relevant feature-family file
6. Testing and release verification files if code is being changed

## 7.3 For reviewer agents
Reviewer agents must verify:
- implementation matches product scope,
- code respects architectural boundaries,
- data changes match the canonical schema,
- UI changes respect centralized design rules,
- real-world behavior has not been sacrificed for test pass rate,
- docs were updated where required.

---

# 8. Document types and authority model

This section explains how to interpret the spec system.

## 8.1 Normative documents
Normative documents define canonical truth. If implementation disagrees with a normative doc, the implementation is wrong unless a documented decision changes the doc.

## 8.2 Informative documents
Informative documents explain, summarize, support, or provide examples, but they do not override canonical rules.

## 8.3 Contract files
Contract files are the most critical normative files because they define structures and behaviors that AI agents are likely to misinterpret if left vague.

---

# 9. Final compact 30-file spec map

Below is the approved compact file system.

## Governance and control
1. `01-README-AND-MASTER-INDEX.md`
2. `02-AI-AGENT-RULES-AND-WORKFLOW.md`
3. `03-PRODUCT-CHARTER-AND-SCOPE.md`
4. `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`
5. `05-ROADMAP-PROGRESS-AND-CHANGELOG.md`

## Core architecture and contracts
6. `06-SYSTEM-ARCHITECTURE.md`
7. `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
8. `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`
9. `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`
10. `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`
11. `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`
12. `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`
13. `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`
14. `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
15. `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`
16. `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
17. `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`

## Feature families
18. `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`
19. `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`
20. `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`
21. `21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md`
22. `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`
23. `23-FEATURE-OFFLINE-PACKS-AUDIO-AND-CONTENT-DISTRIBUTION.md`
24. `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`
25. `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`
26. `26-CONTENT-MODEL-SCHOLAR-REVIEW-AND-PUBLISHING-WORKFLOW.md`

## Quality, release, and operations
27. `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`
28. `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`
29. `29-SECURITY-PRIVACY-COMPLIANCE-AND-RISK-REGISTER.md`
30. `30-DELIVERY-RUNBOOK-INCIDENTS-ROLLBACK-AND-OPERATIONS.md`

---

# 10. File purpose matrix

## 10.1 Governance and control

### 01 — README AND MASTER INDEX
Root document, reading order, file map, update matrix, authority model.

### 02 — AI AGENT RULES AND WORKFLOW
How AI agents must behave before, during, and after tasks.

### 03 — PRODUCT CHARTER AND SCOPE
Defines what the product is, who it serves, what is included, and what is explicitly out of scope.

### 04 — DECISIONS, GLOSSARY, AND CHANGE CONTROL
Defines terms, preserves decisions, and governs controlled change.

### 05 — ROADMAP, PROGRESS, AND CHANGELOG
Tracks delivery phases, active progress, blockers, and historical change.

## 10.2 Core architecture and contracts

### 06 — SYSTEM ARCHITECTURE
Full system overview and service boundaries.

### 07 — FLUTTER APP ARCHITECTURE AND MODULE BOUNDARIES
Canonical Flutter project structure and module rules.

### 08 — DESIGN SYSTEM, THEMES, TOKENS, AND COMPONENTS
Centralized visual system and component rules.

### 09 — PLATFORM SPEC, IOS LIQUID GLASS, AND NATIVE BRIDGES
Platform behavior rules and native boundaries.

### 10 — PERSONAS, IA, USER JOURNEYS, AND TASK FLOWS
Real-user flows and app structure.

### 11 — SCREENS, STATES, NAVIGATION, AND UI BLUEPRINTS
Screen-level contracts.

### 12 — COPY, LOCALIZATION, RTL, AND ACCESSIBILITY
Language, translation, respectfulness, and inclusion rules.

### 13 — DATA MODEL, RLS, INVARIANTS, AND MIGRATIONS
Canonical data and security model.

### 14 — API, REALTIME, AND INTEGRATION CONTRACTS
Canonical service contract rules.

### 15 — OFFLINE, PACKS, SYNC, ASSET DELIVERY, AND CACHE POLICY
Offline-first, sync, packs, and caching behavior.

### 16 — MAP ARCHITECTURE, POSITIONING, ROUTING, 3D, AND OFFLINE WAYFINDING
Canonical map subsystem rules.

### 17 — ANALYTICS, OBSERVABILITY, AND PERFORMANCE BUDGETS
Measurement, diagnostics, and performance constraints.

## 10.3 Feature families

### 18 — RITUALS, RIC, AND RELIGIOUS CONTENT
Ritual flows and mistake-resolution behavior.

### 19 — MAPS, SAVE MY GATE, AND 3D WAYFINDING
User-facing mapping and navigation features.

### 20 — GROUP HUB, CHECK-INS, REGROUP, AND SHARED COORDINATION
Group coordination and regrouping features.

### 21 — PLANNER, REMINDERS, WALLET, NOTES, AND BOOKMARKS
Personal organization features.

### 22 — PHRASEBOOK, EMERGENCY, SAFETY, AND ASSISTIVE TOOLS
Stress and assistance tooling.

### 23 — OFFLINE PACKS, AUDIO, AND CONTENT DISTRIBUTION
Pack UX and downloadable assets.

### 24 — ACCOUNT, SUBSCRIPTIONS, ENTITLEMENTS, AND SETTINGS
Identity, subscriptions, and preferences.

### 25 — ONBOARDING, HOME, AND SIMPLE MODE
First-run experience and simplified operation.

### 26 — CONTENT MODEL, SCHOLAR REVIEW, AND PUBLISHING WORKFLOW
Structured content lifecycle and review controls.

## 10.4 Quality, release, and operations

### 27 — TESTING STRATEGY, TEST MATRIX, AND DEVICE LAB
Automated and manual testing plan.

### 28 — REAL-WORLD VERIFICATION, RELEASE GATES, AND EVIDENCE
Proof of real correctness before release.

### 29 — SECURITY, PRIVACY, COMPLIANCE, AND RISK REGISTER
Data protection and risk management.

### 30 — DELIVERY RUNBOOK, INCIDENTS, ROLLBACK, AND OPERATIONS
Release operations and incident recovery.

---

# 11. Reading matrix by task type

## 11.1 If the task is Flutter UI work
Read:
1. `01`
2. `02`
3. `03`
4. `07`
5. `08`
6. `09`
7. `10`
8. `11`
9. `12`
10. relevant feature-family file
11. `27`
12. `28`

## 11.2 If the task is backend or API work
Read:
1. `01`
2. `02`
3. `03`
4. `06`
5. `13`
6. `14`
7. `15`
8. relevant feature-family file
9. `27`
10. `28`
11. `29`
12. `30`

## 11.3 If the task is map or 3D wayfinding work
Read:
1. `01`
2. `02`
3. `03`
4. `06`
5. `07`
6. `09`
7. `11`
8. `13`
9. `14`
10. `15`
11. `16`
12. `19`
13. `17`
14. `27`
15. `28`

## 11.4 If the task is content or ritual correctness work
Read:
1. `01`
2. `02`
3. `03`
4. `12`
5. `18`
6. `26`
7. `27`
8. `28`

## 11.5 If the task is subscription or entitlement work
Read:
1. `01`
2. `02`
3. `03`
4. `09`
5. `13`
6. `14`
7. `24`
8. `27`
9. `28`
10. `29`

---

# 12. Update matrix

This section tells contributors which files must be updated when changes are made.

## 12.1 If product scope changes
Update:
- `03`
- relevant feature-family files
- `05`
- possibly `10`, `11`, `27`, `28`

## 12.2 If Flutter structure or folder/module boundaries change
Update:
- `07`
- `05`
- any impacted feature-family files
- `27` if test strategy changes

## 12.3 If theme, tokens, components, or UI styling rules change
Update:
- `08`
- `09` if platform behavior changes
- `11` if screen blueprints change
- impacted feature-family files
- `05`

## 12.4 If map behavior changes
Update:
- `16`
- `19`
- `11`
- `17` if performance or analytics changes
- `27`
- `28`
- `05`

## 12.5 If data model or relationships change
Update:
- `13`
- `14`
- impacted feature-family files
- `27`
- `28`
- `29` if privacy/security changes
- `05`

## 12.6 If API contracts or realtime events change
Update:
- `14`
- impacted feature-family files
- `27`
- `28`
- `05`

## 12.7 If offline, packs, or caching rules change
Update:
- `15`
- `23`
- impacted feature-family files
- `27`
- `28`
- `05`

## 12.8 If onboarding or simple mode changes
Update:
- `10`
- `11`
- `12` if copy/accessibility changes
- `25`
- `27`
- `28`
- `05`

## 12.9 If release process or incident handling changes
Update:
- `28`
- `29`
- `30`
- `05`

---

# 13. Repository and folder expectations

This section sets the high-level expectation for how the repo should feel before file `07` defines the detailed Flutter structure.

## 13.1 The codebase must be easy to navigate
The repository should make it easy for both humans and AI agents to answer these questions quickly:
- where does a feature live,
- where do shared components live,
- where do design tokens live,
- where do strings and localization live,
- where do platform bridges live,
- where do repositories and data sources live,
- where do tests live,
- where do downloaded assets live,
- where do pack manifests and offline data rules live.

## 13.2 Visual values must be centralized
Colors, fonts, animation timings, transitions, effects, spacing, radius values, and semantic UI roles must live in centralized theme/token files.

## 13.3 Assets must be categorized intentionally
Assets should be structured by type and purpose, such as:
- icons,
- illustrations,
- bundled audio,
- downloaded audio,
- map assets,
- language resources,
- emergency visuals,
- design-system assets.

## 13.4 Shared logic must be reusable and discoverable
Repeated business logic or repeated widget patterns should not be reimplemented in multiple feature folders.

---

# 14. What “implementation ready” means in this project

A spec file is implementation ready when it:
- clearly states purpose,
- clearly states what is in and out,
- references its dependencies,
- defines any relevant data or behavioral contract,
- includes edge cases where needed,
- can be followed by a competent engineer or AI agent without inventing major missing behavior.

A spec file is **not** implementation ready if it:
- uses vague language like “something like,”
- mixes multiple sources of truth,
- hides important rules in examples,
- does not say what happens in failure states,
- omits update requirements,
- assumes the implementer will “just know” the right behavior.

---

# 15. Anti-failure guidance for AI-agent execution

This project is particularly sensitive to common AI-agent failure modes. The documentation system is designed to prevent them, but this file also states them explicitly.

## 15.1 Common failure mode: making assumptions from partial context
**Prevention:** Always read the required files listed in the reading matrix before editing.

## 15.2 Common failure mode: breaking data relations to fix an error
**Prevention:** Data and API changes must always reference the canonical schema and invariant definitions.

## 15.3 Common failure mode: passing tests while breaking reality
**Prevention:** Real-world verification and release evidence are separate required steps.

## 15.4 Common failure mode: adding extra features mid-task
**Prevention:** Product scope is controlled in file `03`, and every task must stay within the approved surface.

## 15.5 Common failure mode: scattered UI styling and hardcoded values
**Prevention:** Centralized design system and Flutter architecture files explicitly forbid this.

## 15.6 Common failure mode: getting lost after many tasks
**Prevention:** Progress, changelog, decisions, and update rules exist to preserve context continuity.

---

# 16. Expected quality bar for every future file

Every future file in this system should aim to be:
- clear,
- consistent,
- cross-referenced,
- structured,
- specific,
- implementation ready,
- AI-agent friendly,
- maintainable over time.

That means every file should generally include:
- purpose,
- audience,
- dependencies,
- authoritative scope,
- required sections,
- update rules where relevant,
- related files,
- implementation notes where useful.

---

# 17. Implementation bootstrap reading order

The compact 30-file documentation system now exists as a working set.

After this root file, the default implementation bootstrap reading order is:
1. file `02` for AI-agent workflow and change discipline,
2. file `03` for product scope and ethical boundaries,
3. file `04` for glossary, decisions, and change control,
4. file `05` for current phase, blockers, and continuity,
5. files `06` through `09` for system, Flutter, design-system, and platform architecture,
6. files `13` through `17` for data, API, offline/packs, maps, and telemetry contracts,
7. the directly relevant feature files `18` through `25`,
8. file `27` for testing strategy,
9. file `28` for release evidence,
10. file `29` for security, privacy, and compliance,
11. file `30` for delivery operations and rollback.

Humans and AI agents may prune this order for narrow tasks, but they must still read every higher-authority canonical file that governs the requested change.

---

# 18. Summary

This file is the root control document for the Pilgrims Mobile App spec system.

It defines:
- what the project is,
- why the documentation system exists,
- the final compact 30-file structure,
- how the files relate to one another,
- how humans and AI agents should read them,
- how changes must be reflected across the system,
- the non-negotiable rules that protect maintainability, correctness, and clarity.

All future work should begin from this file.

