# 05 — ROADMAP, PROGRESS, AND CHANGELOG

## Document status
- **Type:** Normative delivery-tracking and continuity document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, QA, content/governance contributors, operations contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define how the project is phased, how progress is tracked, how current work is summarized, how blockers are recorded, how handoff context is preserved, and how product/technical changes are logged over time.
- **Authority level:** This file is the canonical operational record of planned phases, current implementation status, active risks, milestone state, and change history.
- **Primary dependencies:** `SPECS/01_README_AND_MASTER_INDEX.md`, `SPECS/02_AI_AGENT_RULES_AND_WORKFLOW.md`, `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`, `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`
- **Related files:** All files, with strongest linkage to `06`–`17`, `18`–`26`, `27`, `28`, `29`, `30`, `31`, `SPECS/CONTRACTS/*`, `tools/specs/validate_spec_contracts.py`, and `.github/workflows/spec-contracts.yml`

---

# 1. Purpose of this file

This file exists because AI-agent-driven development easily loses continuity unless project state is made explicit.

For this project, continuity failures are especially costly because:
- the spec system is large enough that contributors can easily lose track of what is canonical,
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

This file does **not** replace detailed architecture contracts, feature specs, testing strategy, release-gate evidence, incident runbooks, or machine-readable contract artifacts. It connects those materials into one continuity layer.

---

# 4. Delivery model

## 4.1 Release philosophy
The project should ship in controlled layers rather than attempt a fully maximal pilgrimage platform in one pass.

The roadmap should prefer dependable foundations before breadth, offline utility before advanced polish, maintainable architecture before feature sprawl, and validated flows before aggressive expansion.

## 4.2 Phase model
The project is organized into delivery phases.

### Phase 0 — Foundations and control plane
Purpose:
- establish the 31 normative Markdown spec system,
- establish machine-readable contract artifacts and validator coverage,
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

Expansion candidates must come from a healthy, evidenced base rather than unresolved debt.

---

# 5. Current milestone map

| Milestone ID | Milestone | Status | Summary | Next concrete step |
|---|---|---|---|---|
| M-00 | Historical compact 30-file draft archived | Done | The previous compact 30-file draft is retained only as non-normative historical context. | Do not use archived drafts for implementation or review. |
| M-01 | 31-spec normative system established | Done | Files `01` through `31` exist as the current normative Markdown spec system. | Keep file names and cross-file dependencies stable. |
| M-02 | Machine-readable contract baseline established | Done | Contract artifacts exist under `SPECS/CONTRACTS/` and are treated as normative implementation policy where applicable. | Keep Markdown specs, contract artifacts, validator checks, and CI workflow synchronized. |
| M-03 | Contract hardening checkpoint | Done / monitor | Validator passes for all 6 required contract files, `.github/workflows/spec-contracts.yml` runs contract validation for relevant pushes and pull requests, and file `13` now mirrors group-presence mapping rules. | Monitor CI on contract-affecting changes and keep expanding checks as contracts evolve. |
| M-04 | Implementation bootstrap | Planned | Repository structure, shared packages, environments, tokens, schemas, APIs, and build scaffolding must be created under the spec contracts. | Begin repo/bootstrap work using files `01`–`17`, `24`–`31`, and `SPECS/CONTRACTS/*`. |
| M-05 | Core MVP vertical slices | Planned | Home, Rituals/RIC, Phrasebook/Emergency, Save My Gate, Offline Essentials, and Account baseline should be built as the first end-to-end flows. | Select the first two vertical slices and wire them through real app architecture. |
| M-06 | Integration hardening and governed-content tooling | Planned | Packs, content workflow, coordination depth, analytics, and release-quality integration must be established. | Instantiate content schemas/tooling and CI-quality lanes. |
| M-07 | Verification, device lab, and release-evidence readiness | Planned | Files `27`, `28`, `29`, and `30` must become operational execution, not just documentation. | Stand up device buckets, evidence templates, dashboards, and operational owners. |
| M-08 | Beta / pilot release candidate | Planned | A release candidate should exist only after MVP implementation and real verification are both in place. | Produce the first evidence bundle and staged rollout plan. |
| M-09 | V1 production release | Planned | Controlled production release with staged rollout, monitoring, rollback readiness, and support handoff. | Complete beta proof and release sign-off. |

---

# 6. Current project snapshot

## 6.1 Current snapshot
- **Current phase:** Phase 0 specification and contract hardening is materially complete; narrow Phase 1 bootstrap may begin. The contract-validation workflow has an observed green run on the current PR branch; remaining implementation-readiness gaps are operational/product decisions, not missing baseline contract validation.
- **Overall delivery confidence:** high for documentation maturity, contract-file coherence, and baseline CI enforcement; medium for implementation readiness because no aligned codebase, environments, runtime tests, or release evidence exist yet.
- **Active focus areas:** implementation bootstrap planning, release-evidence template planning, minimal governed ritual/RIC fixtures, and explicit resolution of Home runtime decisions that the approved visual reference does not own.
- **Most critical blockers:** no implementation baseline yet; no finalized production tooling stack; no operationalized content-review tooling; no device-lab or release-evidence execution lane yet.
- **Recently completed milestones:** specs `01`–`31`, contract artifact baseline, quality-first hardening amendments, archived 30-file draft marker, file `02` agent-workflow normalization, validator pass for 6 contract files, GitHub Actions workflow for contract validation, file `13` group-presence data-model alignment.
- **Immediate next priority:** begin narrow Phase 1 bootstrap with contract-aware implementation tasks while keeping unresolved Home runtime decisions non-functional until product ownership is approved.

## 6.2 Phase transition rule
Broad Phase 1 feature development must not begin until:
- the validator passes against all contract artifacts,
- CI runs the contract validator on relevant pushes and pull requests,
- screen traceability covers every canonical screen in file `11`,
- entitlement and privacy/account server-write rules are explicit,
- obsolete 30-file and hyphenated filename references are removed or clearly marked historical,
- implementation tasks reference the current 31-spec + contracts authority model.

Current status:
- validator pass: complete,
- CI contract workflow: complete; green run observed on the current PR branch,
- 47-screen traceability: complete in contract artifact,
- entitlement and privacy/account server-write rules: complete in contract/API specs,
- file `02` obsolete filename references: complete,
- file `13` group-presence prose alignment: complete,
- remaining known prose cleanup: file `31` carry-forward checklist should eventually be converted to a status table.

---

# 7. Module tracker status

| Module | Related specs/contracts | Phase target | Priority | Spec status | Implementation status | Validation status | Next required action |
|---|---|---:|---:|---|---|---|---|
| Governance/source of truth | `01`, `02`, `04`, `05`, `31`, `CONTRACTS/README` | 0 | P0 | Done / monitor | Not started | Validator and CI wired where contract-backed | Keep outdated historical references archived and current references normalized. |
| Contract validator | `tools/specs/validate_spec_contracts.py`, `CONTRACTS/*`, `.github/workflows/spec-contracts.yml` | 0 | P0 | Done / monitor | Script and workflow exist | GitHub Actions green observed; validator also checks canonical spec filenames/design migration | Keep validation green and expand checks only when new machine-checkable invariants are introduced. |
| Screen traceability | `11`, `screen_feature_traceability.yaml` | 0 | P0 | Done / monitor | Not started | Validator passed | Keep all 47 canonical screens mapped and evidence-owned. |
| Entitlements/account | `24`, `entitlement_capability_policy.yaml` | 1 | P0 | Done / hardening | Not started | Validator passed | Implement free/auth/Supporter capability gates exactly from contract. |
| API/privacy endpoints | `14`, `24`, `29`, `31` | 1 | P0 | Done / hardening | Not started | Spec-reviewed | Implement idempotency, rate-limit, audit, alert, and evidence rules from file `14`. |
| Group coordination | `20`, `13`, `14`, `group_presence_privacy_contract.yaml` | 2 | P1 | Done / monitor | Not started | Validator passed; file `13` aligned | Implement create/join/check-in as server-trusted writes with contract-backed fixtures. |
| Ritual/RIC content | `18`, `26` | 1 | P0 | Done | Not started | Planned | Add minimal governed fixture before implementation claims correctness. |
| Offline packs | `15`, `23`, `content_pack_trust_chain_contract.yaml` | 1 | P0 | Done / contract-backed | Not started | Validator passed | Reflect signed manifest verification and LKG activation path in implementation and tests. |
| Design system | `08`, `09`, `11`, `12` | 1 | P0 | Done / needs implementation tokens | Not started | Planned | Implement Figma-aligned Pilgrims Soft Surface semantic tokens, mandatory Light/Dark themes, and System/Light/Dark appearance handling in the Flutter design-system baseline. |
| Release evidence | `27`, `28`, `29`, `30`, `release_gate_taxonomy.yaml` | 3 | P0 | Done / contract-backed | Not started | Validator passed | Create evidence templates and CI/device-lab lanes. |

---

# 8. Current blocker register

| Blocker ID | Severity | Area | Description | Required resolution |
|---|---|---|---|---|
| B-001 | P0 | Implementation | No aligned Flutter/backend implementation baseline exists yet. | Bootstrap repo structure, packages, tokens, routes, schemas, and tests from specs. |
| B-003 | P0 | Content correctness | Ritual/RIC implementation needs minimal governed fixture before correctness claims. | Add schema/fixture/review metadata under content governance. |
| B-004 | P1 | Operations | Device-lab and release-evidence lane not operationalized. | Create release evidence templates, owner model, and device bucket execution path. |
| B-005 | P1 | Home context/product ownership | The approved Home visual shows prayer-time/current-prayer/countdown/location/weather subcontent, but no normative runtime owner currently defines calculation/provider, timezone/location dependency, freshness, stale/offline behavior, privacy, analytics, or release evidence. | Product owner must either (a) explicitly add the capability with a named owning spec and end-to-end contract, or (b) keep those data-driven subfields omitted/non-runtime. Do not infer implementation from Figma. |
| B-006 | P1 | Home shell/product ownership | The centered floating Home action slot has no canonical behavior. | Product owner must map it to an already-approved canonical route/action and update file `11` plus traceability if screen/navigation semantics change, or keep the slot non-functional/absent. Do not infer QR/scanner/camera behavior from iconography. |

---

# 9. Changelog

## 2026-09-24 — Final audit status correction and unresolved Home decisions
- Corrected roadmap language that still said the contract-validation workflow was awaiting an observed green run; the current PR head has a completed successful workflow run.
- Recorded the prayer/weather Home context runtime ownership gap as an explicit product decision instead of allowing implementation agents to infer calculation/provider behavior from the visual reference.
- Recorded the centered floating Home action as an explicit unresolved product decision; it must not silently become QR/scanner/camera or displace the canonical Tools section.
- No machine-readable contract changed because these items remain unresolved product ownership decisions rather than approved runtime semantics.

## 2026-09-24 — Final cross-spec quality audit hardening
- Normalized remaining broken hyphenated spec filename references to canonical underscore filenames.
- Removed residual active glass-specific platform/architecture wording so D-006 consistently governs one Pilgrims Soft Surface identity across iOS and Android.
- Clarified that prayer-time/weather data and the centered Home floating slot are visual evidence only until an approved runtime owner/action exists; the mockup does not replace the canonical Tools section or authorize QR/scanner/camera behavior.
- Made script-aware font fallback an explicit design-system/localization contract for Arabic, English, Indonesian, mixed-script, and large-text coverage.
- Reconciled Notes/Bookmarks entitlement prose with file `24` and `CONTRACTS/entitlement_capability_policy.yaml`; `NOTES_BOOKMARKS_EXTENDED` is canonical.
- Converted file `31` carry-forward items into truthful status, leaving implementation tests pending because Flutter/backend implementation has not started.
- Expanded the validator to catch canonical filename/design-migration drift and made the CI workflow run for all `SPECS/**` changes.
- Machine-readable product contracts were not changed because this audit found prose/reference drift rather than contract-semantic drift.

## 2026-09-24 — Figma-aligned Pilgrims Soft Surface and dual-appearance contract
- Superseded the former Liquid-Glass-led visual doctrine while preserving D-004 as historical decision record.
- Adopted D-006: the approved Figma direction is the visual reference and file `08` now owns the canonical **Pilgrims Soft Surface** design language.
- Made System / Light / Dark appearance a first-class product contract; Light and Dark are both mandatory.
- Renamed file `09` to `09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md` so platform adaptation and native bridges remain style-neutral.
- Preserved existing product behavior, IA, accessibility, offline, entitlement, privacy, religious-content, and native-bridge truth.
- Flutter implementation remains **not started**; this change updates specification truth and verification expectations only.


## 2026-06-12 — Group presence data-model prose aligned
- Updated file `13` to use current underscore dependencies in document metadata.
- Documented `group_presence_events.id` as the persisted database primary key exposed as API `event_id`.
- Changed `group_presence_events.text_pin` from unconditional required prose to conditional presence aligned with `CONTRACTS/group_presence_privacy_contract.yaml`.
- Added hard invariants, migration discipline, and fixture requirements for group presence identifier and conditional-field behavior.
- Updated this roadmap to clear file `13` as an open prose-drift blocker.

## 2026-06-12 — Contract CI workflow added
- Confirmed `.github/workflows/spec-contracts.yml` exists and runs `python tools/specs/validate_spec_contracts.py` for relevant pushes and pull requests.
- Updated roadmap status from CI validation missing to CI workflow present and pending first observed green run.

## 2026-06-12 — Validator pass and agent-workflow normalization
- Confirmed local validation output: `Validated 6 spec contract files.`
- Updated file `02` to use current underscore spec paths and require contract-artifact review before contract-shaped changes.
- Updated this roadmap snapshot to distinguish contract validation done from CI enforcement still pending.

## 2026-06-12 — Governance and contract hardening patch
- Marked the archived compact 30-file draft as non-normative historical context.
- Superseded the old compact 30-file governance decision in file `04`.
- Recorded current governance as 31 normative Markdown specs plus machine-readable contracts and validator enforcement.
- Expanded screen traceability expectations to cover every canonical screen in file `11`.
- Expanded entitlement capability policy to distinguish free baseline, authenticated trusted writes, Supporter convenience features, downgrade behavior, and entitlement keys.
- Aligned group presence contract terminology with the data model by documenting `id` as database primary key and `event_id` as API identifier.
- Hardened validator coverage for contract structure, screen count, entitlement axes, group-presence mapping, advisory registry, release taxonomy, and trust-chain terms.

---

# 10. Handoff context for next contributor or AI agent

Before starting Phase 1 implementation:
1. Read `README.md`, `SPECS/01_README_AND_MASTER_INDEX.md`, `SPECS/02_AI_AGENT_RULES_AND_WORKFLOW.md`, `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, and this file.
2. Read `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md` and `SPECS/CONTRACTS/README.md`.
3. Run `python tools/specs/validate_spec_contracts.py` locally and confirm GitHub Actions also runs on contract-affecting changes.
4. For the target feature area, read the relevant Markdown specs and contract artifact.
5. Do not implement from archived 30-file draft material or obsolete hyphenated filename references.
6. Do not call a module done until implementation, tests, accessibility/offline behavior, and release evidence match the governing specs.
7. Treat file `31` carry-forward table conversion as low-priority prose cleanup, not a blocker for narrow Phase 1 bootstrap.

---

# 11. Definition of done for this file

This file is healthy when:
- current phase status is accurate,
- milestone language reflects current governance rather than archived history,
- blockers are explicit,
- module statuses distinguish spec maturity from implementation maturity,
- changelog entries preserve why changes happened,
- next contributors can safely resume without relying on chat memory.

---

End of file.
