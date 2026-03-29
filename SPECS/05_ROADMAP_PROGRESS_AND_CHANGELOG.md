# 05 — ROADMAP, PROGRESS, AND CHANGELOG

## Document status
- **Type:** Normative delivery-tracking and continuity document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, QA, content/governance contributors, operations contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define how the project is phased, how progress is tracked, how current work is summarized, how blockers are recorded, how handoff context is preserved, and how product/technical changes are logged over time.
- **Authority level:** This file is the canonical operational record of planned phases, current implementation status, active risks, milestone state, and change history.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `02-AI-AGENT-RULES-AND-WORKFLOW.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`
- **Related files:** All files, with strongest linkage to `06`–`17`, `18`–`26`, `27`, `28`, `29`, and `30`

---

# 1. Purpose of this file

This file exists because AI-agent-driven development easily loses continuity unless project state is made explicit.

For this project, continuity failures are especially costly because:
- the spec system is now large enough that contributors can easily lose track of what is canonical,
- spec completion and implementation completion are different truths and must not be conflated,
- the product has several trust-critical domains such as ritual correctness, offline packs, map fallback, entitlement truth, privacy, and emergency access,
- AI agents may otherwise reopen settled questions, ignore unresolved operational constraints, or begin coding from the wrong phase assumptions,
- release readiness can look closer than it really is if documentation maturity is mistaken for shipped-product maturity.

This file reduces those risks by providing:
- a release-phased roadmap,
- milestone and release-plan continuity,
- a module-by-module progress tracker,
- a current-focus and blocker summary,
- a handoff context section for new humans or AI agents,
- a structured changelog,
- a release-evidence reference section.

---

# 2. Core principles for roadmap and progress tracking

## 2.1 Progress must be visible
If work is underway, blocked, partially complete, or ready for verification, that state should be clearly visible.

## 2.2 “Done” must mean something real
A task or module is not “done” merely because code was written or a test passed.

## 2.3 Continuity beats memory
No contributor or AI agent should rely on memory to understand project status.

## 2.4 Roadmap is directional, progress is factual
The roadmap describes the intended sequence and release layering. The progress tracker describes what is actually true now.

## 2.5 Spec maturity and implementation maturity are different dimensions
A completed specification is not the same thing as a completed module implementation.
This file must keep those truths separate.

## 2.6 Change history must preserve meaning
The changelog should explain real changes in a way that a future contributor can understand, not merely list file edits.

## 2.7 Delivery tracking must reflect risk
Blocked, fragile, partial, or verification-pending work must not be hidden inside optimistic status labels.

---

# 3. Scope of this file

This file covers:
- product and technical delivery phases,
- milestones and release-plan continuity,
- module status tracking,
- current active work focus,
- blockers and risks affecting delivery,
- handoff context between contributors and AI agents,
- user-visible and system-level changelog entries,
- release-evidence references.

This file does **not** replace:
- detailed architecture contracts,
- detailed feature specs,
- detailed testing strategy,
- release-gate evidence,
- incident runbooks.

Instead, it connects those materials into one continuity layer.

---

# 4. Delivery model

## 4.1 Release philosophy
The project should ship in controlled layers rather than attempt a fully maximal pilgrimage platform in one pass.

The roadmap should prefer:
- dependable foundations before breadth,
- offline utility before advanced polish,
- maintainable architecture before feature sprawl,
- validated flows before aggressive expansion.

## 4.2 Phase model
The project is organized into delivery phases.

### Phase 0 — Foundations and control plane
Purpose:
- establish the 30-file documentation backbone,
- establish Flutter, data, API, offline, map, content, testing, release, privacy, and operations contracts,
- establish AI-agent-safe governance and change-control discipline.

Success condition:
- the project becomes safe to build incrementally without uncontrolled drift.

### Phase 1 — Implementation bootstrap and MVP vertical slices
Purpose:
- convert the spec system into a real implementation baseline and first vertical slices.

Target capability areas:
- repository and environment bootstrap,
- centralized design tokens and shared components,
- baseline data and API scaffolding,
- baseline auth/entitlement foundation,
- Home and onboarding root,
- ritual/RIC baseline,
- phrasebook and emergency baseline,
- Save My Gate baseline,
- offline essentials and first pack strategy.

Success condition:
- the project has a working implementation baseline aligned to the spec system and can demonstrate early end-to-end MVP value.

### Phase 2 — Integration hardening and coordination depth
Purpose:
- deepen feature integration and operational realism without destabilizing the foundations.

Target capability areas:
- group coordination,
- richer offline packs and audio,
- stronger planner/notes/bookmarks depth,
- governed-content tooling and publication path,
- stronger observability,
- device-lab and release-evidence foundation.

Success condition:
- the product supports richer real-world use while staying coherent and testable.

### Phase 3 — Verification, release hardening, and pilot readiness
Purpose:
- convert a working product into a verifiably releasable one.

Target capability areas:
- device and environment coverage,
- real-world verification,
- accessibility and RTL hardening,
- security/privacy execution,
- staged rollout and rollback readiness,
- support and incident operations.

Success condition:
- the product can enter beta or pilot release with explicit evidence rather than assumption.

### Phase 4 — V1 production release and post-V1 expansion decisions
Purpose:
- ship the first stable release and only then decide whether broader scope expansion is justified.

Examples of later candidates:
- broader pilgrimage-path expansion,
- deeper official-service handoff patterns,
- higher-fidelity operational integrations,
- richer premium convenience layers,
- deeper map refinement after real usage proves the value.

Success condition:
- expansion occurs from a healthy, evidenced base rather than from unresolved debt.

---

# 5. Delivery principles by phase

## 5.1 Phase 0 must reduce ambiguity
If Phase 0 does not leave the system easier for AI agents and humans to work in, it is incomplete.

## 5.2 Phase 1 must convert contracts into reality without violating the contracts
The first implementation phase should prove the architecture and shared components, not just produce isolated demos.

## 5.3 Phase 2 must deepen, not destabilize
New coordination and offline depth should build on working architecture rather than force large rewrites.

## 5.4 Phase 3 must treat “ready” as a proof claim
Verification, release evidence, and operations readiness are part of product quality, not optional polish.

## 5.5 Phase 4 must be decision-driven
Later expansion must not happen by drift. It requires explicit decision control.

---

# 6. Status model

This section defines the allowed status labels and how to read them.

## 6.1 Spec maturity labels
### Not started
The canonical spec is not yet meaningfully written.

### Drafting
The spec is actively being written or materially revised.

### Done
The canonical spec exists and is stable enough to guide implementation.

### Needs refresh
The canonical spec exists but is no longer aligned with newer project truth.

## 6.2 Implementation maturity labels
### Not started
No meaningful implementation aligned to the canonical spec exists yet.

### Planned
Implementation is understood and sequenced, but active coding has not started.

### In progress
Meaningful implementation work is underway.

### Partial
Some implementation exists, but it is not yet release-credible.

### Ready for review
Implementation is complete enough for structured review against specs.

### Ready for verification
Implementation and review are acceptable, but required testing, device checks, or release evidence are not yet complete.

### Done
Implementation meets its definition of done for the intended release layer.

### Blocked
Meaningful progress cannot continue because a dependency, decision, environment, or operational prerequisite is missing.

### Deferred
The module or enhancement has been intentionally postponed.

## 6.3 Validation labels
### Not started
No meaningful verification has been performed.

### Planned
Verification expectations are understood but not yet executed.

### In progress
Testing or review is underway.

### Pending real-world proof
Lab or local work exists, but device, field, or release evidence is still missing.

### Verified
The relevant verification bar for the intended release layer has been met.

## 6.4 Status honesty rule
Status must reflect actual state, not desired state.

Examples:
- If the spec is complete but no code exists, the module is **Spec: Done** and **Implementation: Not started**.
- If code exists but offline behavior is still broken, the module is not **Done**.
- If implementation exists but device-lab checks or real-world validation are still pending, validation must not be shown as **Verified**.

---

# 7. Priority framework

Every tracked module should also carry a delivery priority.

## 7.1 Priority levels
- **P0:** critical foundation or critical user value
- **P1:** highly important for target release
- **P2:** important but can follow after foundations
- **P3:** optional or later enhancement

## 7.2 Priority honesty rule
Priority should reflect release importance, not contributor enthusiasm.

---

# 8. Module tracker structure

Every tracked module entry should include the following fields.

## 8.1 Required fields
- Module name
- Related spec file(s)
- Phase target
- Priority
- Spec status
- Implementation status
- Validation status
- Current summary
- Next required action
- Last updated

## 8.2 Optional but recommended fields
- Owner or responsible role
- Notes on architectural risk
- Release target
- Linked decision IDs
- Linked issue/task IDs if external tracking exists

---

# 9. Milestones and release plan

## 9.1 Milestone status legend
- **Done:** completed and reflected in the canonical docs
- **Planned:** sequenced next or later, but not yet started
- **Blocked:** cannot progress meaningfully until prerequisites are resolved
- **In progress:** active work is underway

## 9.2 Current milestone map

| Milestone ID | Milestone | Status | Summary | Next concrete step |
|---|---|---|---|---|
| M-00 | Compact 30-file architecture agreed | Done | The project converged on the final compact 30-file spec system. | Keep file names and cross-file dependencies stable. |
| M-01 | Canonical 30-file spec set generated | Done | Files `01` through `30` now exist in draft-ready canonical form. | Keep continuity and change control accurate during implementation. |
| M-02 | Roadmap continuity refresh after full spec completion | Done | File `05` refreshed to reflect full-spec completion and the pre-implementation state. | Use this updated continuity layer as the project checkpoint. |
| M-03 | Implementation bootstrap | Planned | Repository structure, shared packages, environments, tokens, schemas, APIs, and build scaffolding must be created under the spec contracts. | Begin repo/bootstrap work using files `01`–`09`, `13`–`17`, and `24`–`30`. |
| M-04 | Core MVP vertical slices | Planned | Home, Rituals/RIC, Phrasebook/Emergency, Save My Gate, Offline Essentials, and Account baseline should be built as the first end-to-end flows. | Select the first two vertical slices and wire them through real app architecture. |
| M-05 | Integration hardening and governed-content tooling | Planned | Packs, content workflow, coordination depth, analytics, and release-quality integration must be established. | Instantiate content schemas/tooling and CI-quality lanes. |
| M-06 | Verification, device lab, and release-evidence readiness | Planned | Files `27`, `28`, `29`, and `30` must become operational execution, not just documentation. | Stand up device buckets, evidence templates, dashboards, and operational owners. |
| M-07 | Beta / pilot release candidate | Planned | A release candidate should exist only after MVP implementation and real verification are both in place. | Produce the first evidence bundle and staged rollout plan. |
| M-08 | V1 production release | Planned | Controlled production release with staged rollout, monitoring, rollback readiness, and support handoff. | Complete beta proof and release sign-off. |

---

# 10. Current project snapshot

## 10.1 Snapshot fields
- Current phase
- Overall delivery confidence
- Active focus areas
- Most critical blockers
- Recently completed milestones
- Modules approaching review or verification
- Highest operational risks
- Immediate next priority

## 10.2 Current snapshot (after full 30-file spec completion)
- **Current phase:** Phase 0 complete; transition checkpoint between Phase 0 and Phase 1
- **Overall delivery confidence:** high for documentation maturity; medium for implementation readiness because no aligned codebase, environments, or release evidence exist yet
- **Active focus areas:** implementation bootstrap planning, decision closure for provider/tooling choices, repo and environment setup planning, final spec hardening and compliance clarification
- **Most critical blockers:** no implementation baseline yet; no finalized production tooling stack; no operationalized content-review tooling; no device-lab or release-evidence execution lane yet
- **Recently completed milestones:** files `25` through `30` completed; full compact `01`–`30` spec stack complete; continuity refresh of file `05`; validated hardening across documentation integrity and release-compliance contracts
- **Modules approaching review or verification:** none in implementation yet; next review boundary is implementation bootstrap and first vertical-slice planning
- **Highest operational risks:** spec drift during implementation kickoff, map/provider complexity, entitlements and restore correctness, governed-content operationalization, privacy/compliance drift between docs and actual SDK choices
- **Immediate next priority:** begin implementation bootstrap under the canonical contracts rather than writing more net-new scope

---

# 11. Active work summary

## 11.1 Required fields for active work entries
- Work item title
- Category (spec / engineering / design / data / QA / release / operations)
- Status
- Why it matters now
- Dependencies
- Risks if delayed
- Expected next concrete step

## 11.2 Current active work entries

### Active item A — Implementation bootstrap plan
- **Category:** engineering / architecture
- **Status:** planned
- **Why it matters now:** the project now has enough specification maturity to begin real implementation, but only if the initial codebase and environments are shaped correctly
- **Dependencies:** files `01`–`09`, `13`–`17`, `24`–`30`
- **Risks if delayed:** the spec system remains theoretical and contributors may start coding ad hoc outside the intended module boundaries
- **Expected next concrete step:** define the initial repository structure, package boundaries, environment strategy, CI scaffolding, and first implementation slice order

### Active item B — Decision closure for implementation-critical vendor choices
- **Category:** spec / architecture / operations
- **Status:** planned
- **Why it matters now:** some implementation details remain intentionally constrained by the docs but not fully instantiated, especially for maps, purchases, observability, and production tooling
- **Dependencies:** files `09`, `14`, `16`, `17`, `24`, `29`, `30`
- **Risks if delayed:** teams may implement the right architecture with the wrong concrete services, permissions, cost profile, or disclosure posture
- **Expected next concrete step:** capture implementation-level ADRs for concrete provider selections and environment/tooling choices

### Active item C — Governed-content tooling and schema bootstrap
- **Category:** content / engineering / governance
- **Status:** planned
- **Why it matters now:** files `18`, `23`, and `26` define strict content truth, but the actual schema repo, validation tooling, and publication mechanics do not exist yet
- **Dependencies:** files `13`, `15`, `18`, `23`, `26`, `27`, `28`, `30`
- **Risks if delayed:** religious and assistive content may drift back into hardcoded UI or informal documents during implementation
- **Expected next concrete step:** create the structured content source layout, validation rules, provenance model, and publication candidate flow

### Active item D — Quality and release foundation bootstrap
- **Category:** QA / release / operations
- **Status:** planned
- **Why it matters now:** files `27`–`30` define a strong quality and release model, but those controls only become real once the project has device buckets, evidence templates, dashboards, and operational roles
- **Dependencies:** files `17`, `27`, `28`, `29`, `30`
- **Risks if delayed:** implementation may look successful long before the team can actually verify or release it safely
- **Expected next concrete step:** stand up the initial CI quality lanes, device-bucket strategy, evidence-bundle template, and release-owner/on-call expectations

---

# 12. Blockers and preconditions

## 12.1 What counts as a blocker
A blocker is something that prevents meaningful progress or introduces unacceptable risk if ignored.

Examples:
- missing architectural decision,
- unresolved vendor or platform choice,
- missing environment or secret-management baseline,
- dependency on unfinished canonical file,
- uncertainty about product boundary that affects implementation,
- inability to validate a critical subsystem,
- store/provider/legal constraint preventing safe implementation.

## 12.2 Blocker entry format
Each blocker entry should include:
- Blocker ID
- Title
- Affected module(s)
- Severity
- Description
- Why it blocks progress
- Required resolution
- Owner
- Date identified
- Status

## 12.3 Current blockers / gating preconditions

### B-001 — Implementation baseline does not exist yet
- **Affected modules:** nearly all implementation modules
- **Severity:** high
- **Description:** the project now has complete specifications, but there is no aligned repository, package structure, CI lane, or environment bootstrap recorded as implemented
- **Why it blocks progress:** meaningful implementation should not start as scattered files or experiments detached from the canonical module boundaries
- **Required resolution:** begin implementation bootstrap using files `06`, `07`, `08`, `09`, `13`, `14`, `15`, `16`, and `17` as the control plane
- **Owner:** founder / engineering architecture
- **Date identified:** 2026-03-11
- **Status:** open

### B-002 — Concrete provider and tooling choices still need explicit decisions
- **Affected modules:** maps, observability, purchases, runtime delivery, release tooling, support tooling
- **Severity:** high
- **Description:** the spec set intentionally defines constraints and boundaries, but some production choices still require explicit ADRs or implementation decisions
- **Why it blocks progress:** the team can accidentally stay within the abstract architecture while still choosing tools or providers that break cost, policy, privacy, or performance assumptions
- **Required resolution:** capture concrete implementation decisions for provider/tooling choices before or during bootstrap
- **Owner:** founder / architecture / operations
- **Date identified:** 2026-03-11
- **Status:** open

### B-003 — Governed-content operations are specified but not operationalized
- **Affected modules:** rituals, phrasebook/emergency content, packs, content workflow, testing, release evidence, operations
- **Severity:** high
- **Description:** scholar review, provenance, validation, publish/rollback, and content integrity are now well specified, but the actual tooling and workflow are not yet instantiated
- **Why it blocks progress:** implementation could drift into hardcoded or weakly governed content handling if this is not built early
- **Required resolution:** create the content source-of-truth layout, validation pipeline, publication metadata model, and accountable review workflow
- **Owner:** content/governance + engineering
- **Date identified:** 2026-03-11
- **Status:** open

### B-004 — Quality and release operations exist only as documentation
- **Affected modules:** testing, verification, security/privacy execution, delivery operations
- **Severity:** medium-high
- **Description:** files `27`, `28`, `29`, and `30` now define the quality and release bar, but there is no device lab, evidence template library, release dashboard baseline, or operational owner map yet
- **Why it blocks progress:** implementation may move quickly while verification and release readiness remain theoretical
- **Required resolution:** turn the quality and operations files into active project infrastructure before later-stage implementation
- **Owner:** QA / release / operations
- **Date identified:** 2026-03-11
- **Status:** open

### B-005 — Legal/store disclosure execution has not yet been instantiated
- **Affected modules:** account, purchases, location, group, medical/emergency, privacy, release operations
- **Severity:** medium-high
- **Description:** the privacy/compliance posture is now documented, but legal copy ownership, store disclosure drafts, SDK inventory, and deletion/retention execution are not yet set up operationally
- **Why it blocks progress:** later implementation could quietly diverge from the required disclosure and compliance posture
- **Required resolution:** establish disclosure ownership, SDK inventory, store privacy review checklist, and deletion/retention execution planning before release-facing work
- **Owner:** founder / legal-compliance / engineering
- **Date identified:** 2026-03-11
- **Status:** open

---

# 13. Risk-aware progress rules

## 13.1 Partial work must be called partial
Do not mark a module done when only the happy path works.

## 13.2 A reviewed spec is not the same as an implemented module
Spec maturity and implementation maturity are separate dimensions and should stay separate here.

## 13.3 Architecture-health risk must be visible
If a module technically works but has known maintainability debt, that should be recorded.

## 13.4 Verification debt must be visible
If implementation exists but device-lab checks or real-world validation are still pending, status should reflect that.

## 13.5 Operationalization debt must be visible
If a process file exists but no real tooling, owners, or dashboards implement it yet, that gap should be called out.

---

# 14. Current module tracker

## 14.1 Governance and control modules

| # | Module | File | Phase | Priority | Spec | Implementation | Validation | Current summary | Next required action | Last updated |
|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Documentation system and master index | `01` | 0 | P0 | Done | Ready to apply | Not started | Canonical reading order and dependency map are complete. | Use as the root entry point for all implementation work. | 2026-03-11 |
| 02 | AI-agent workflow enforcement | `02` | 0–1 | P0 | Done | Ready to apply | Not started | AI-agent operating rules exist and should govern future code work. | Enforce in every implementation task. | 2026-03-11 |
| 03 | Product scope and charter | `03` | 0–4 | P0 | Done | Ready to apply | Not started | Product identity, ethical boundaries, and Umrah-first scope are stable. | Use as the guardrail for scope decisions during implementation. | 2026-03-11 |
| 04 | Decisions, glossary, and change control | `04` | 0–4 | P0 | Done | Ready to apply | Not started | Canonical naming and change-control system exists. | Record concrete implementation ADRs next. | 2026-03-11 |
| 05 | Roadmap, progress, and changelog | `05` | 0–4 | P0 | Done | Active continuity layer | Not started | Continuity file refreshed for the full 30-file system and pre-implementation state. | Keep updated after major implementation or milestone changes. | 2026-03-11 |

## 14.2 Architecture, UX, and platform modules

| # | Module | File | Phase | Priority | Spec | Implementation | Validation | Current summary | Next required action | Last updated |
|---|---|---|---|---|---|---|---|---|---|---|
| 06 | System architecture | `06` | 0–1 | P0 | Done | Not started | Not started | Full system boundary contract exists. | Translate into repo/services/environment bootstrap. | 2026-03-11 |
| 07 | Flutter app architecture and module boundaries | `07` | 0–1 | P0 | Done | Not started | Not started | Canonical Flutter structure exists. | Create actual package/folder/module baseline. | 2026-03-11 |
| 08 | Design system, themes, tokens, and components | `08` | 0–1 | P0 | Done | Not started | Not started | Centralized visual rules exist. | Implement token/theme/component foundation before feature widgets. | 2026-03-11 |
| 09 | Platform adaptation, native bridges, and iOS/Android rules | `09` | 0–3 | P0 | Done | Not started | Not started | Platform boundaries and native-bridge policy are defined. | Finalize concrete bridge/provider choices and wrapper strategy. | 2026-03-11 |
| 10 | Personas, IA, user journeys, and task flows | `10` | 0–3 | P1 | Done | Ready to apply | Not started | Real-user scenarios and stress/failure flows are documented. | Use to select first MVP vertical slices and acceptance criteria. | 2026-03-11 |
| 11 | Screens, states, navigation, and UI blueprints | `11` | 0–3 | P1 | Done | Not started | Not started | Screen-level contracts and state inventory exist. | Convert to route map and screen implementation backlog. | 2026-03-11 |
| 12 | Copy, localization, RTL, and accessibility | `12` | 0–3 | P0 | Done | Not started | Not started | Copy and locale/accessibility rules are stable. | Set up localization structure and accessibility QA baseline early. | 2026-03-11 |
| 13 | Data model, RLS, invariants, and migrations | `13` | 0–2 | P0 | Done | Not started | Not started | Canonical data truth exists. | Build schemas, migrations, and access control implementation. | 2026-03-11 |
| 14 | API, realtime, and integration contracts | `14` | 0–2 | P0 | Done | Not started | Not started | Service contracts are specified. | Implement endpoint and transport skeletons with auth and error discipline. | 2026-03-11 |
| 15 | Offline packs, sync, asset delivery, and cache policy | `15` | 0–3 | P0 | Done | Not started | Not started | Offline and artifact trust posture is specified. | Build manifest, local inventory, and last-known-good handling. | 2026-03-11 |
| 16 | Map architecture, positioning, routing, 3D, and offline wayfinding | `16` | 0–3 | P0 | Done | Not started | Not started | The map subsystem contract is strong but operationally complex. | Finalize concrete provider/path decisions before deep map coding. | 2026-03-11 |
| 17 | Analytics, observability, and performance budgets | `17` | 0–3 | P0 | Done | Not started | Not started | Telemetry, alerts, and budgets are documented. | Stand up privacy-safe instrumentation and release-health dashboards. | 2026-03-11 |

## 14.3 Feature-family modules

| # | Module | File | Phase | Priority | Spec | Implementation | Validation | Current summary | Next required action | Last updated |
|---|---|---|---|---|---|---|---|---|---|---|
| 18 | Rituals, RIC, and religious content | `18` | 1–3 | P0 | Done | Not started | Not started | Trust-critical ritual and remedy behavior is specified. | Build as one of the first MVP vertical slices with governed content support. | 2026-03-11 |
| 19 | Maps, Save My Gate, and 3D wayfinding | `19` | 1–3 | P0 | Done | Not started | Not started | Map feature contract exists, but depends on file `16` operational choices. | Start with Save My Gate and honest fallback before deeper 3D polish. | 2026-03-11 |
| 20 | Group Hub, check-ins, regroup, and shared coordination | `20` | 2–3 | P1 | Done | Not started | Not started | Coordination model is documented and privacy-light. | Implement only after core trust flows and privacy boundaries are in place. | 2026-03-11 |
| 21 | Planner, reminders, wallet, notes, and bookmarks | `21` | 1–2 | P1 | Done | Not started | Not started | Personal organization tools are specified as support features, not core identity drivers. | Implement after Home, Rituals, and emergency roots are stable. | 2026-03-11 |
| 22 | Phrasebook, emergency, safety, and assistive tools | `22` | 1–2 | P0 | Done | Not started | Not started | High-value offline support surfaces are specified. | Build early as part of the MVP trust and assistance layer. | 2026-03-11 |
| 23 | Offline packs, audio, and content distribution | `23` | 2–3 | P1 | Done | Not started | Not started | Richer pack/content delivery behavior is specified. | Build after baseline offline and manifest architecture exists. | 2026-03-11 |
| 24 | Account, subscriptions, entitlements, and settings | `24` | 1–3 | P0 | Done | Not started | Not started | Entitlement and settings behavior is documented with ethical guardrails. | Implement auth/account baseline and restore truth early enough to shape later premium surfaces. | 2026-03-11 |
| 25 | Onboarding, Home, and Simple Mode | `25` | 1–2 | P0 | Done | Not started | Not started | Calm first-use and repeat-entry contract is now complete. | Build as a first implementation slice because it is the product root. | 2026-03-11 |
| 26 | Content model, scholar review, and publishing workflow | `26` | 1–3 | P0 | Done | Not started | Not started | Governed-content and publication workflow is documented. | Instantiate schemas, provenance, review flow, and rollback-safe artifact logic. | 2026-03-11 |

## 14.4 Quality, release, security, and operations modules

| # | Module | File | Phase | Priority | Spec | Implementation | Validation | Current summary | Next required action | Last updated |
|---|---|---|---|---|---|---|---|---|---|---|
| 27 | Testing strategy, test matrix, and device lab | `27` | 1–3 | P0 | Done | Not started | Not started | Quality system is specified but not operationalized. | Create testkit, CI lanes, fixture strategy, and initial device buckets. | 2026-03-11 |
| 28 | Real-world verification, release gates, and evidence | `28` | 2–3 | P0 | Done | Not started | Not started | Release-proof requirements are specified. | Create evidence templates and manual verification execution model. | 2026-03-11 |
| 29 | Security, privacy, compliance, and risk register | `29` | 1–4 | P0 | Done | Not started | Not started | Security/privacy posture and risk register exist. | Instantiate SDK inventory, retention/deletion execution, and disclosure ownership. | 2026-03-11 |
| 30 | Delivery runbook, incidents, rollback, and operations | `30` | 2–4 | P0 | Done | Not started | Not started | Operational runbook exists but no real release infrastructure exists yet. | Create release records, rollout controls, dashboards, incident roles, and support handoff templates. | 2026-03-11 |

---

# 15. Handoff context

This section exists so a new AI agent or contributor can resume work safely.

## 15.1 Handoff summary fields
- Current phase
- Recently completed work
- Work currently in progress
- Highest-priority next step
- Critical unresolved questions
- Modules at risk of drift
- Known gaps between docs and implementation
- Validation still missing

## 15.2 Current handoff context
- **Current phase:** Phase 0 complete; project is now at the transition checkpoint into Phase 1
- **Recently completed work:** files `25`–`30` completed; the full compact `01`–`30` spec set now exists; file `05` refreshed to reflect the true project state; a validated hardening pass corrected source hygiene, contract drift, and release-compliance gaps
- **Work currently in progress:** no implementation work is active yet; the project is at a documentation-clean and compliance-hardened handoff point before implementation bootstrap
- **Highest-priority next step:** begin implementation bootstrap using the architecture, data, design system, offline, content, testing, security, and operations contracts already defined
- **Critical unresolved questions:** exact concrete provider/tooling choices for maps, purchases, observability, runtime delivery, and operational tooling; exact bootstrap ordering for the first MVP vertical slices; who owns legal/compliance execution and governed-content review operations in practice
- **Modules at risk of drift:** maps (`16`, `19`), governed content (`18`, `26`), entitlements/purchases (`24`), packs/offline delivery (`15`, `23`), release/security operations (`27`–`30`)
- **Known gaps between docs and implementation:** no aligned codebase, no instantiated schemas/migrations, no live API/service skeletons, no content tooling, no device-lab execution, no release dashboards, no release evidence packages
- **Validation still missing:** all implementation validation, device testing, real-world verification, security execution proof, and release evidence

---

# 16. Changelog policy

## 16.1 Purpose of the changelog
The changelog explains meaningful project change over time.

It should help future readers answer:
- what changed,
- why it changed,
- what user or system behavior is different now,
- whether the change is breaking, additive, corrective, or clarifying.

## 16.2 What belongs in the changelog
Include:
- meaningful spec changes,
- product-scope changes,
- new accepted decisions,
- architecture changes,
- feature behavior changes,
- data-contract changes,
- release-relevant fixes,
- quality, privacy, or compliance changes,
- continuity updates that change how the project should now be interpreted.

## 16.3 What does not belong in the changelog
Do not clutter the changelog with:
- trivial typo-only edits,
- formatting-only edits,
- minor internal wording cleanup unless it changes interpretation,
- repetitive entries with no operational meaning.

## 16.4 Changelog entry template
Each entry should include:
- Date
- Version or milestone label if applicable
- Type (added / changed / fixed / deprecated / removed / clarified)
- Area
- Summary
- Reason
- Impacted files or modules
- Whether any breaking behavior is involved

---

# 17. Changelog

## 2026-03-22 — Fixed — Spec hardening and release-compliance clarification
- **Area:** documentation integrity / contract alignment / store-compliance readiness
- **Summary:** corrected stale root guidance, repaired corrupted document-status metadata, sanitized embedded reference URLs, aligned data-model test hooks with canonical group endpoints, clarified V1 local-only wallet posture, added future-proof document-hygiene rules for AI edits, and added explicit account-deletion and disclosure-verification requirements across account UX, compliance, release evidence, and operations readiness.
- **Reason:** reduce ambiguity before implementation bootstrap and close a real release-policy gap for account-bearing builds.
- **Impacted modules:** files `01`, `02`, `05`, `06`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `16`, `24`, `27`, `28`, `29`, and `30`
- **Breaking behavior:** no product-scope or runtime-behavior change; documentation quality and release-governance hardening only

## 2026-03-09 — Added — Governance / Documentation milestone `M-00`
- **Area:** project foundation
- **Summary:** established the compact 30-file documentation architecture for AI-agent-driven delivery
- **Reason:** reduce documentation sprawl while preserving hard contracts and maintainability
- **Impacted modules:** entire spec system
- **Breaking behavior:** no runtime impact; governance impact yes

## 2026-03-09 — Added — Governance
- **Area:** AI-agent workflow
- **Summary:** established a dedicated AI-agent operating manual governing clarification rules, code inspection discipline, testing integrity, and documentation update rules
- **Reason:** directly address known AI-agent failure modes
- **Impacted modules:** all implementation workflows
- **Breaking behavior:** no runtime impact; process impact yes

## 2026-03-09 — Added — Product and control plane
- **Area:** product scope / change control / roadmap continuity
- **Summary:** established the product charter, canonical glossary, naming rules, change-control system, and initial roadmap/progress continuity layer
- **Reason:** prevent scope drift, terminology fragmentation, and project-status ambiguity
- **Impacted modules:** governance layer and all downstream files
- **Breaking behavior:** no runtime impact; governance impact yes

## 2026-03-09 to 2026-03-10 — Added — Architecture and platform baseline milestone `M-01A`
- **Area:** core technical contracts
- **Summary:** completed the system architecture, Flutter module boundaries, design system, platform adaptation, personas/IA, screen blueprints, copy/localization/accessibility, data model, API contracts, offline/cache policy, map architecture, and analytics/observability budget files
- **Reason:** create the full technical and UX control plane needed before implementation
- **Impacted modules:** files `06`–`17`
- **Breaking behavior:** no runtime impact; implementation-governance impact yes

## 2026-03-09 to 2026-03-10 — Added — Feature-family baseline milestone `M-01B`
- **Area:** user-facing capability contracts
- **Summary:** completed the feature-family specs for Rituals/RIC, Maps/Save My Gate, Group, Planner, Phrasebook/Emergency, Offline Packs/Audio, Account/Entitlements, and Onboarding/Home/Simple Mode
- **Reason:** define user-facing behavior before implementation begins and keep feature scope coherent with the architecture
- **Impacted modules:** files `18`–`25`
- **Breaking behavior:** no runtime impact; feature-contract impact yes

## 2026-03-11 — Added — Governed content and release-control stack milestone `M-01C`
- **Area:** content governance / testing / release / security / operations
- **Summary:** completed the final five control files covering content model and scholar review, testing strategy, real-world verification, security/privacy/compliance, and delivery/incident/rollback operations
- **Reason:** prevent the project from becoming implementation-capable without also becoming release-safe, privacy-safe, and rollback-safe
- **Impacted modules:** files `26`–`30`
- **Breaking behavior:** no runtime impact; release-governance impact yes

## 2026-03-11 — Changed — Roadmap continuity milestone `M-02`
- **Area:** project status interpretation
- **Summary:** updated file `05` to reflect that the 30-file canonical spec system is now complete, separated spec maturity from implementation maturity, refreshed blockers, and shifted the project state from “foundational docs still being written” to “ready for implementation bootstrap”
- **Reason:** the previous version of file `05` no longer reflected the real project state
- **Impacted modules:** file `05`, all implementation planning
- **Breaking behavior:** no runtime impact; continuity and sequencing impact yes

---

# 18. Release evidence references

## 18.1 Purpose
This section links project state to the evidence system that will later govern releases.

## 18.2 Current evidence state
No application release, beta evidence bundle, or production evidence package has yet been recorded under the compact 30-file spec system.

## 18.3 Canonical future evidence sources
When implementation reaches later phases, release evidence should reference at minimum:
- file `27` for test-matrix and device-lab execution,
- file `28` for release gates and evidence bundles,
- file `29` for security/privacy and incident severity posture,
- file `30` for delivery operations, rollback, and postmortems.

## 18.4 Suggested evidence-log fields
- Release label
- Date
- Included phases/modules
- Key user-visible changes
- Key technical changes
- Evidence bundle location
- Known limitations
- Rollout state
- Final decision

---

# 19. Operational use rules for AI agents and contributors

## 19.1 Before starting a task
Inspect this file to understand:
- current phase,
- active milestones,
- module status,
- blockers,
- current priorities,
- recently changed areas.

## 19.2 After completing meaningful work
Update this file if the task changed:
- module status,
- milestone status,
- active work focus,
- blocker state,
- handoff context,
- changelog-worthy project truth.

## 19.3 When confused about project context
Use this file as the first continuity checkpoint before assuming the project’s current state.

## 19.4 When handing off to another contributor or AI agent
The handoff summary should be reflected here or be consistent with the handoff sections here.

## 19.5 When starting implementation
Do not treat “all 30 specs exist” as permission to code ad hoc.
Implementation must still begin from the architecture, data, design, offline, testing, security, and operations control files in the intended order.

---

# 20. When this file must be updated

This file must be updated whenever:
- a milestone status changes materially,
- a module status changes materially,
- the current phase changes,
- a blocker appears, changes, or is resolved,
- a major decision affects sequencing or delivery,
- a changelog-worthy product or technical change occurs,
- active focus areas change,
- implementation meaningfully begins,
- a release milestone or evidence package is completed.

If meaningful work happens and this file is not updated, project continuity degrades.

---

# 21. Summary

This file is the project continuity backbone.

It defines:
- the delivery phases,
- the milestone and release-plan structure,
- the status model for specs, implementation, and validation,
- the module tracker,
- the current project snapshot,
- the active work structure,
- blocker tracking rules,
- the handoff context,
- the changelog,
- the release-evidence reference layer,
- and the rules for keeping project status visible over time.

Its purpose is to ensure that as the app grows, no human or AI agent has to guess:
- which phase the project is in,
- whether a module is merely specified or actually built,
- what is actively blocking progress,
- what changed recently,
- and what the correct next step is.
