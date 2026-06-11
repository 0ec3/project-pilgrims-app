# 04 — DECISIONS, GLOSSARY, AND CHANGE CONTROL

## Document status
- **Type:** Normative governance document
- **Priority:** Highest
- **Audience:** Product owner, engineering lead, design lead, QA lead, content/governance contributors, AI agents, release reviewers
- **Purpose:** Define how decisions are recorded, how terms are used consistently, how conflicts are resolved, and how project-wide changes are controlled.
- **Authority level:** This file is the canonical governance reference for decisions, terminology, and change-control process.
- **Primary dependency:** `SPECS/01_README_AND_MASTER_INDEX.md`
- **Related files:** All normative specs, `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`, `SPECS/CONTRACTS/*`, and `tools/specs/validate_spec_contracts.py`

---

# 1. Purpose of this file

This file exists because the project depends on stable shared meaning.

It governs:
- accepted and superseded decisions,
- canonical terminology,
- forbidden ambiguous aliases,
- conflict-resolution behavior,
- change-control requirements,
- naming conventions,
- decision-record expectations.

If a contributor or AI agent is uncertain whether a change alters project truth, they must treat it as a change-control event.

---

# 2. Governance principles

## 2.1 Canonical truth must be explicit
Do not rely on memory, prior chat context, or implementation convenience when deciding product or architecture truth.

## 2.2 Decisions must remain traceable
Material choices must be recorded with enough context that a future contributor can understand what was chosen and why.

## 2.3 Terminology must be stable
One concept should not have multiple casual names in implementation, docs, analytics, or UI copy.

## 2.4 Contracts and specs must move together
If a Markdown spec and a machine-readable contract both govern an area, changes must update both in the same task.

## 2.5 Superseded history must be visible
Old decisions and artifacts may remain for historical context, but they must be clearly marked superseded or non-normative.

---

# 3. Authority hierarchy

When conflicts arise, resolve them in this order:
1. `README.md` and `SPECS/01_README_AND_MASTER_INDEX.md` for source-of-truth structure.
2. `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md` for quality-first hardening decisions introduced after the original 30-spec set.
3. Machine-readable contracts in `SPECS/CONTRACTS/*` for structured implementation policy.
4. Feature and architecture specs `03`–`30` for domain detail.
5. This file for glossary, decision, naming, and change-control procedure.
6. Implementation code, tests, fixtures, and generated artifacts.

If a lower-priority source conflicts with a higher-priority source, stop and patch the conflict rather than silently choosing one.

---

# 4. Canonical terminology rules

## 4.1 Product terms
Use these terms consistently:

| Term | Meaning | Notes |
|---|---|---|
| Pilgrim | The primary user of the app. | Avoid tourist/traveler when discussing core flows. |
| Companion app | The product category. | Avoid positioning as an official authority. |
| Umrah-first | Early release scope prioritizes Umrah journeys. | Hajj complexity requires explicit expansion decision. |
| RIC | Ritual Issue Checker. | Do not rename casually. |
| Simple Mode | Reduced-density recovery-focused mode. | Do not call it elder mode or panic mode. |
| Save My Gate | First-class recovery feature for recalling a saved gate/anchor. | Preserve name in UX and docs unless formally changed. |
| Pack | Offline content/data/audio bundle. | Must not imply executable code. |
| Supporter | Paid tier name. | Paid tier must not imply correctness/safety is withheld from free users. |
| Group | Small pilgrim coordination group. | Not a social network or tracking circle. |
| Regroup pin | Explicit group meeting point/instruction. | Not passive live tracking. |
| Live board | Optional richer group status board. | Must preserve stale-state honesty and privacy. |

## 4.2 Forbidden aliases
Do not introduce these terms as canonical names:
- panic mode,
- elder mode,
- tracking group,
- live tracking,
- official permit management,
- AI fatwa,
- religious ruling generator,
- always-on location,
- premium safety,
- premium correctness.

They may appear only when explicitly documenting forbidden behavior.

---

# 5. Decision records

## 5.1 D-001 — Compact 30-file spec architecture
- **Status:** superseded
- **Area:** documentation governance
- **Decision:** The earlier compact 30-file draft is historical only. Current normative governance uses 31 Markdown specs plus machine-readable contract artifacts and validator enforcement.
- **Superseded by:** D-005

## 5.2 D-002 — Umrah-first product scope
- **Status:** accepted
- **Area:** product scope
- **Decision:** Default product and early release scope are Umrah-first; Hajj complexity must not be silently reintroduced.

## 5.3 D-003 — Centralized Flutter theme and token architecture
- **Status:** accepted
- **Area:** engineering/design system
- **Decision:** Repeated style values must be centralized rather than hardcoded across feature widgets.

## 5.4 D-004 — Controlled iOS Liquid Glass adaptation
- **Status:** accepted
- **Area:** design/platform
- **Decision:** Use controlled iOS-specific glass/material adaptation where appropriate without compromising readability.

## 5.5 D-005 — 31-spec plus machine-readable contract governance
- **Status:** accepted
- **Area:** documentation governance
- **Decision:** Treat `README.md`, `SPECS/01_README_AND_MASTER_INDEX.md`, specs `01`–`31`, `SPECS/CONTRACTS/*`, and `tools/specs/validate_spec_contracts.py` as the current normative specification system.
- **Consequences:** Archived 30-file drafts are non-normative. AI agents must not use them to infer current filenames, authority hierarchy, scope, dependencies, or release gates.

---

# 6. Change-control triggers

A change must update this file or a related decision record if it materially affects:
- product scope,
- monetization boundary,
- architecture direction,
- map/provider strategy,
- content-governance policy,
- data model or invariant behavior,
- platform adaptation,
- feature boundary,
- release strategy,
- privacy/safety posture,
- AI-agent workflow rules,
- contract artifact semantics.

---

# 7. Conflict-resolution workflow

When a conflict is found:
1. Identify every affected Markdown spec, contract artifact, validator, test fixture, and implementation file.
2. Determine which source has authority using the hierarchy above.
3. Patch all affected sources in the same change.
4. Add or update validator coverage when the conflict can recur structurally.
5. Record a decision if the resolution changes project truth.
6. Do not continue implementation until the conflict is resolved.

---

# 8. Naming conventions across the project

## 8.1 General naming goals
Names should be:
- clear,
- stable,
- scoped,
- searchable,
- consistent across docs and code where practical.

## 8.2 Documentation file naming convention
Current normative Markdown spec filenames use:
- two-digit numeric ordering prefix,
- uppercase descriptive words separated by underscores,
- descriptive scope,
- no unnecessary abbreviations unless already canonical.

Examples:
- `SPECS/16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md`
- `SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`

Machine-readable contracts use lowercase snake_case filenames under `SPECS/CONTRACTS/`.

Example:
- `SPECS/CONTRACTS/screen_feature_traceability.yaml`

Historical hyphenated spec references are obsolete and must not be used for new work.

## 8.3 Flutter/Dart naming convention guidance
Detailed code conventions may be refined in the Flutter architecture file, but the following rules apply at a high level:
- packages/modules should use stable descriptive names,
- widgets should be named by purpose, not visual coincidence,
- repositories/services should reflect domain meaning,
- avoid abbreviations unless widely understood and already canonical,
- public API names should align with canonical glossary terms where possible.

## 8.4 API naming convention guidance
- Resource naming should be explicit and domain-consistent.
- Event names should reflect user-meaningful actions or system events, not implementation trivia.
- Avoid multiple names for the same entity across endpoints.

## 8.5 Analytics naming convention guidance
- Event families should be predictable.
- Event names should use stable domain language.
- Avoid renaming analytics casually because historical analysis continuity matters.

---

# 9. Decision record template

Each material decision entry should include:
- **Decision ID**
- **Date**
- **Status**: proposed / accepted / superseded / deprecated
- **Owner**
- **Area**
- **Context**
- **Decision**
- **Alternatives considered**
- **Why this decision was chosen**
- **Consequences**
- **Files impacted**
- **Supersedes / superseded by** if relevant

---

# 10. Definition of done for governance changes

A governance change is complete only when:
- impacted Markdown specs are updated,
- impacted contract artifacts are updated,
- validator coverage is updated where structural drift can recur,
- obsolete artifacts are explicitly marked archived/non-normative or removed,
- changelog/roadmap continuity is updated where needed,
- AI-agent workflow rules point to current filenames and authority sources.
