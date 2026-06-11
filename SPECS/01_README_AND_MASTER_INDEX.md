# 01 — README AND MASTER INDEX

## Document status
- **Type:** Normative root document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, design lead, backend engineer, Flutter engineer, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** This is the root entry point for the full documentation system. Every human contributor and every AI agent must begin here before reading or editing any other spec file.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
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

Quality-first amendments in file `31` add one more operational requirement: implementation speed must not outrank mature product quality, religious correctness, safety, accessibility, privacy-light behavior, offline honesty, and release evidence.

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

# 4. Normative spec map

The documentation system is now organized as 31 normative markdown specs plus machine-readable contract artifacts under `SPECS/CONTRACTS/`.

## 4.1 Core and governance
- `01_README_AND_MASTER_INDEX.md` — root entry point and master index.
- `02_AI_AGENT_RULES_AND_WORKFLOW.md` — rules for AI coding, reviewer, and debugging agents.
- `03_PRODUCT_CHARTER_AND_SCOPE.md` — product identity, ethical rules, non-goals, release scope.
- `04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md` — canonical terms, ADRs, and controlled change process.
- `05_ROADMAP_PROGRESS_AND_CHANGELOG.md` — roadmap, progress, blockers, changelog, handoff notes.

## 4.2 Architecture and engineering
- `06_SYSTEM_ARCHITECTURE.md` — runtime zones, system boundaries, failure domains.
- `07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md` — package/layer rules and forbidden patterns.
- `08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md` — visual system, tokens, components, glass rules.
- `09_PLATFORM_SPEC_IOS_LIQUID_GLASS_ANDROID_ADAPTATION_AND_NATIVE_BRIDGES.md` — platform expression and native bridge rules.

## 4.3 Product, UX, and accessibility
- `10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md` — personas, IA, journeys, task flows.
- `11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md` — screen inventory, states, navigation contracts.
- `12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md` — copy, localization, RTL, accessibility.

## 4.4 Data, APIs, and systems
- `13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md` — server schema, local schema, RLS, invariants.
- `14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md` — API, realtime, privacy endpoints, integration contracts.
- `15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md` — offline tiers, packs, sync, cache, signed trust-chain, and last-known-good behavior.
- `16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md` — map stack, positioning, routing, offline wayfinding.
- `17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md` — telemetry, observability, performance budgets.

## 4.5 Feature families
- `18_FEATURE_RITUALS_RIC_AND_RELIGIOUS_CONTENT.md` — rituals, RIC, religious content behavior.
- `19_FEATURE_MAPS_SAVE_MY_GATE_AND_3_D_WAYFINDING.md` — maps, Save My Gate, 3D/2D/text degradation.
- `20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md` — group creation, join, check-ins, regroup, live board, coordination.
- `21_FEATURE_PLANNER_REMINDERS_WALLET_NOTES_AND_BOOKMARKS.md` — local planner, reminders, wallet, notes, bookmarks.
- `22_FEATURE_PHRASEBOOK_EMERGENCY_SAFETY_AND_ASSISTIVE_TOOLS.md` — phrasebook, emergency, medical, safety, assistive tools.
- `23_FEATURE_OFFLINE_PACKS_AUDIO_AND_CONTENT_DISTRIBUTION.md` — pack catalog, install, purge, audio distribution.
- `24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md` — account, subscriptions, entitlements, settings, privacy/data flow.
- `25_FEATURE_ONBOARDING_HOME_AND_SIMPLE_MODE.md` — startup, onboarding, Home, Simple Mode.

## 4.6 Quality, security, delivery, and amendments
- `26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md` — content governance, scholar review, publishing.
- `27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md` — testing strategy and device lab requirements.
- `28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md` — release gates, verification, evidence.
- `29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md` — security, privacy, compliance, risk register.
- `30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md` — delivery, incident response, rollback, operations.
- `31_QUALITY_FIRST_HARDENING_AMENDMENTS.md` — normative quality-first amendments and cross-spec hardening layer.

## 4.7 Machine-readable contract artifacts
The following contract artifacts are normative implementation aids. They mirror critical truths from the markdown specs and must stay synchronized with prose changes:

- `CONTRACTS/entitlement_capability_policy.yaml`
- `CONTRACTS/group_presence_privacy_contract.yaml`
- `CONTRACTS/content_pack_trust_chain_contract.yaml`
- `CONTRACTS/advisory_source_registry.schema.yaml`
- `CONTRACTS/release_gate_taxonomy.yaml`
- `CONTRACTS/screen_feature_traceability.yaml`

Validation helper:
- `tools/specs/validate_spec_contracts.py`

---

# 5. Reading order

## 5.1 Everyone starts here
Every contributor and AI agent must begin with this file.

## 5.2 Minimum reading set by task type
### Product or scope task
Read: `01`, `03`, `04`, relevant feature file, and `31`.

### UI or navigation task
Read: `01`, `08`, `10`, `11`, `12`, `25`, relevant feature file, `31`, and `CONTRACTS/screen_feature_traceability.yaml`.

### API, backend, or data task
Read: `01`, `06`, `13`, `14`, relevant feature file, `29`, `31`, and affected files in `CONTRACTS/`.

### Offline, packs, content, or publishing task
Read: `01`, `15`, `23`, `26`, `29`, `30`, `31`, and `CONTRACTS/content_pack_trust_chain_contract.yaml`.

### Group, location, or coordination task
Read: `01`, `13`, `14`, `16`, `19`, `20`, `24`, `29`, `31`, and `CONTRACTS/group_presence_privacy_contract.yaml`.

### Entitlement or monetization task
Read: `01`, `03`, `14`, `24`, relevant feature files, `29`, `31`, and `CONTRACTS/entitlement_capability_policy.yaml`.

### Release, QA, or operations task
Read: `01`, `17`, `27`, `28`, `29`, `30`, `31`, and `CONTRACTS/release_gate_taxonomy.yaml`.

---

# 6. Conflict and precedence rules

## 6.1 File precedence
When two files conflict:
1. file `31` controls for issues it explicitly supersedes,
2. the most specific feature/system file controls local behavior,
3. file `03` controls product ethics and scope,
4. file `29` controls privacy/security boundaries,
5. file `28` controls release go/no-go gates,
6. file `04` controls glossary and change process.

## 6.2 Markdown and contract artifact sync
Markdown specs are the human-readable authority. Contract artifacts are implementation aids and must not drift.

If a contract artifact and markdown spec conflict, stop implementation and update both through change control.

## 6.3 No silent implementation rule
No agent may silently implement behavior that changes:
- entitlement truth,
- API contracts,
- data ownership,
- content governance,
- privacy posture,
- release gates,
- group/location semantics,
- screen inventory.

---

# 7. Current quality-first hardening decisions

The following decisions are now active:

1. The project is quality-first, not MVP-speed-first.
2. In-app group creation is a governed authenticated leader flow when group creation ships.
3. Entitlement behavior must validate against the capability policy contract.
4. Group freshness, presence, and location behavior must validate against the privacy contract.
5. Pack and governed-content activation require signed trust-chain semantics for mature release quality.
6. Advisory/safety content requires source freshness metadata.
7. File `28` owns release gate authority; file `27` owns verification mechanics; file `30` owns rollout/incident execution.
8. Screen-to-feature traceability is mandatory for implementation and release evidence.

---

End of file.