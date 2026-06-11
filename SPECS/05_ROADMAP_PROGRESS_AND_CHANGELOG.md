# 05 — ROADMAP, PROGRESS, AND CHANGELOG

## Document status
- **Type:** Normative delivery-tracking and continuity document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, QA, content/governance contributors, operations contributors, AI coding agents, reviewer agents, release agents
- **Purpose:** Define how the project is phased, how progress is tracked, how current work is summarized, how blockers are recorded, how handoff context is preserved, and how product/technical changes are logged over time.
- **Authority level:** This file is the canonical operational record of planned phases, current implementation status, active risks, milestone state, and change history.
- **Primary dependencies:** `SPECS/01_README_AND_MASTER_INDEX.md`, `SPECS/02_AI_AGENT_RULES_AND_WORKFLOW.md`, `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`, `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`
- **Related files:** All files, with strongest linkage to `06`–`17`, `18`–`26`, `27`, `28`, `29`, `30`, `31`, `SPECS/CONTRACTS/*`, and `tools/specs/validate_spec_contracts.py`

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

This file does **not** replace:
- detailed architecture contracts,
- detailed feature specs,
- detailed testing strategy,
- release-gate evidence,
- incident runbooks,
- machine-readable contract artifacts.

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

Examples of later candidates:
- broader pilgrimage-path expansion,
- deeper official-service handoff patterns,
- higher-fidelity operational integrations,
- richer premium convenience layers,
- deeper map refinement after real usage proves the value.

Success condition:
- expansion occurs from a healthy, evidenced base rather than from unresolved debt.

---

# 5. Current milestone map

| Milestone ID | Milestone | Status | Summary | Next concrete step |
|---|---|---|---|---|
| M-00 | Historical compact 30-file draft archived | Done | The previous compact 30-file draft is retained only as non-normative historical context. | Do not use archived drafts for implementation or review. |
| M-01 | 31-spec normative system established | Done | Files `01` through `31` exist as the current normative Markdown spec system. | Keep file names and cross-file dependencies stable. |
| M-02 | Machine-readable contract baseline established | Done | Contract artifacts exist under `SPECS/CONTRACTS/` and are treated as normative implementation policy where applicable. | Keep Markdown specs, contract artifacts, and validator checks synchronized. |
| M-03 | Contract hardening checkpoint | In progress | Screen traceability, entitlements, group presence privacy, and validator coverage are being tightened before broad Phase 1 work. | Finish validator-backed checks and API/privacy endpoint alignment. |
| M-04 | Implementation bootstrap | Planned | Repository structure, shared packages, environments, tokens, schemas, APIs, and build scaffolding must be created under the spec contracts. | Begin repo/bootstrap work using files `01`–`17`, `24`–`31`, and `SPECS/CONTRACTS/*`. |
| M-05 | Core MVP vertical slices | Planned | Home, Rituals/RIC, Phrasebook/Emergency, Save My Gate, Offline Essentials, and Account baseline should be built as the first end-to-end flows. | Select the first two vertical slices and wire them through real app architecture. |
| M-06 | Integration hardening and governed-content tooling | Planned | Packs, content workflow, coordination depth, analytics, and release-quality integration must be established. | Instantiate content schemas/tooling and CI-quality lanes. |
| M-07 | Verification, device lab, and release-evidence readiness | Planned | Files `27`, `28`, `29`, and `30` must become operational execution, not just documentation. | Stand up device buckets, evidence templates, dashboards, and operational owners. |
| M-08 | Beta / pilot release candidate | Planned | A release candidate should exist only after MVP implementation and real verification are both in place. | Produce the first evidence bundle and staged rollout plan. |
| M-09 | V1 production release | Planned | Controlled production release with staged rollout, monitoring, rollback readiness, and support handoff. | Complete beta proof and release sign-off. |

---

# 6. Current project snapshot

## 6.1 Current snapshot
- **Current phase:** Phase 0 complete with active hardening checkpoint before unrestricted Phase 1 implementation.
- **Overall delivery confidence:** high for documentation maturity; medium for implementation readiness because no aligned codebase, environments, or release evidence exist yet.
- **Active focus areas:** contract hardening, validator enforcement, API/privacy endpoint alignment, screen traceability, implementation bootstrap planning.
- **Most critical blockers:** no implementation baseline yet; no finalized production tooling stack; no operationalized content-review tooling; no device-lab or release-evidence execution lane yet.
- **Recently completed milestones:** specs `01`–`31`, contract artifact baseline, quality-first hardening amendments, archived 30-file draft marker.
- **Immediate next priority:** complete validator-backed spec/contract alignment, then begin narrow Phase 1 bootstrap.

## 6.2 Phase transition rule
Broad Phase 1 feature development must not begin until:
- the validator passes against all contract artifacts,
- screen traceability covers every canonical screen in file `11`,
- entitlement and privacy/account server-write rules are explicit,
- obsolete 30-file and hyphenated filename references are removed or clearly marked historical,
- implementation tasks reference the current 31-spec + contracts authority model.

---

# 7. Module tracker status

| Module | Related specs/contracts | Phase target | Priority | Spec status | Implementation status | Validation status | Next required action |
|---|---|---:|---:|---|---|---|---|
| Governance/source of truth | `01`, `02`, `04`, `05`, `31`, `CONTRACTS/README` | 0 | P0 | Done / hardening | Not started | Planned | Keep outdated historical references archived and current references normalized. |
| Contract validator | `tools/specs/validate_spec_contracts.py`, `CONTRACTS/*` | 0 | P0 | In progress | In progress | In progress | Run validator in CI and expand checks as contracts evolve. |
| Screen traceability | `11`, `screen_feature_traceability.yaml` | 0 | P0 | In progress | Not started | Planned | Keep all 47 canonical screens mapped and evidence-owned. |
| Entitlements/account | `24`, `entitlement_capability_policy.yaml` | 1 | P0 | Done / hardening | Not started | Planned | Implement free/auth/Supporter capability gates exactly from contract. |
| API/privacy endpoints | `14`, `24`, `29`, `31` | 1 | P0 | Needs hardening | Not started | Planned | Add idempotency, rate-limit, audit, alert, and evidence rules for deletion/export endpoints. |
| Group coordination | `20`, `13`, `14`, `group_presence_privacy_contract.yaml` | 2 | P1 | Done / hardening | Not started | Planned | Implement group create/join/check-in as server-trusted writes with no hidden offline queue. |
| Ritual/RIC content | `18`, `26` | 1 | P0 | Done | Not started | Planned | Add minimal governed fixture before implementation claims correctness. |
| Offline packs | `15`, `23`, `content_pack_trust_chain_contract.yaml` | 1 | P0 | Done | Not started | Planned | Implement signed manifest verification and LKG activation path. |
| Design system | `08`, `09`, `11`, `12` | 1 | P0 | Done / needs implementation tokens | Not started | Planned | Convert tokens and components into concrete Flutter package baseline. |
| Release evidence | `27`, `28`, `29`, `30`, `release_gate_taxonomy.yaml` | 3 | P0 | Done | Not started | Planned | Create evidence templates and CI/device-lab lanes. |

---

# 8. Current blocker register

| Blocker ID | Severity | Area | Description | Required resolution |
|---|---|---|---|---|
| B-001 | P0 | Implementation | No aligned Flutter/backend implementation baseline exists yet. | Bootstrap repo structure, packages, tokens, routes, schemas, and tests from specs. |
| B-002 | P0 | Validation | Contract validator must be run and wired into CI before relying on contracts during implementation. | Add CI command and evidence record after validator passes. |
| B-003 | P0 | Content correctness | Ritual/RIC implementation needs minimal governed fixture before correctness claims. | Add schema/fixture/review metadata under content governance. |
| B-004 | P1 | Operations | Device-lab and release-evidence lane not operationalized. | Create release evidence templates, owner model, and device bucket execution path. |
| B-005 | P1 | API/security | Privacy/account endpoints need complete idempotency, rate-limit, audit, alert, and user-visible status rules. | Harden file `14` and dependent tests before endpoint implementation. |

---

# 9. Changelog

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
3. Run `python tools/specs/validate_spec_contracts.py`.
4. For the target feature area, read the relevant Markdown specs and contract artifact.
5. Do not implement from archived 30-file draft material or obsolete hyphenated filename references.
6. Do not call a module done until implementation, tests, accessibility/offline behavior, and release evidence match the governing specs.

---

# 11. Definition of done for this file

This file is healthy when:
- current phase status is accurate,
- milestone language reflects current governance rather than archived history,
- blockers are explicit,
- module statuses distinguish spec maturity from implementation maturity,
- changelog entries preserve why changes happened,
- next contributors can safely resume without relying on chat memory.
