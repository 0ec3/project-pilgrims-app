# Pilgrims Mobile App

> A calm, offline-first, quality-first mobile companion for Muslim pilgrims — built for reliability under stress, religious correctness by design, privacy-light coordination, and dignity in every interaction.

---

## Current documentation status

This repository is currently a **specification and governance repository** for Pilgrims Mobile App.

The normative source of truth lives in:

- [`SPECS/01_README_AND_MASTER_INDEX.md`](./SPECS/01_README_AND_MASTER_INDEX.md)
- [`SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`](./SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md)
- [`SPECS/CONTRACTS/`](./SPECS/CONTRACTS/)

The visible repository surface should be treated as product, architecture, UX, data, API, content, security, testing, release, and operations specifications unless or until implementation packages are added.

---

## Product vision

Pilgrims Mobile App exists to make pilgrimage clearer, calmer, and safer for pilgrims who may be tired, stressed, elderly, separated from their group, unfamiliar with smartphones, or operating with weak connectivity.

The app helps pilgrims:

- perform rituals correctly,
- recover when they are uncertain or make a mistake,
- save and recall gates or landmarks,
- navigate with graceful 3D → 2D → text degradation,
- coordinate with family or group without hidden tracking,
- access phrasebook, emergency, and medical-support tools,
- prepare, remember, and organize lightweight personal items,
- use essential value offline.

The default product scope is **Umrah-first**. Hajj complexity must not bleed into default flows unless season, scope, content governance, release evidence, and operations readiness explicitly permit it.

---

## Quality-first posture

The project now explicitly optimizes for **mature app quality rather than MVP speed**.

That means shipped capabilities must be:

- calm and highly legible,
- accessible at large text and with assistive technologies,
- privacy-light by design,
- honest about stale/offline/degraded state,
- governed by clear data/API contracts,
- release-evidenced on real devices where risk requires it,
- safe for pilgrims under stress.

Quality-first does **not** mean feature sprawl. Richer features require sharper scope, stronger contracts, stronger tests, and clearer release evidence.

See [`SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`](./SPECS/31_QUALITY_FIRST_HARDENING_AMENDMENTS.md).

---

## Non-negotiable product promises

| Promise | Meaning |
|---|---|
| **Offline-first** | Essential pilgrimage guidance remains useful without constant connectivity. |
| **Religious correctness** | Ritual/RIC/remedy content is governed and reviewed, not improvised in widget code. |
| **Calm under stress** | UI prioritizes readability, recovery, and action clarity over feature density. |
| **Privacy-light** | Private support data stays local by default and shared/group data is minimized. |
| **No hidden tracking** | Group and map features must not become passive surveillance. |
| **Ethical monetization** | Supporter unlocks convenience/enrichment, never correctness or essential safety. |
| **Last-known-good safety** | Packs, content, and config changes must preserve safe fallback paths. |

---

## Runtime zones

The system is specified across five runtime zones:

| Zone | Responsibilities |
|---|---|
| **Flutter App** | UI, local-first data, offline logic, feature modules, pack manager. |
| **Edge API** | Auth validation, group coordination, privacy/account requests, entitlement validation, control plane. |
| **Identity/Data** | Supabase Auth, PostgreSQL, RLS, server-backed group/account/entitlement data. |
| **Asset Delivery** | R2/CDN-backed immutable pack and content artifact delivery. |
| **Observability** | Privacy-safe analytics, crash reporting, performance traces, structured logs. |

Architecture details live in files `06`, `07`, `13`, `14`, `15`, `17`, and `30`.

---

## Offline and pack trust model

The app uses four offline tiers:

| Tier | Meaning | Examples |
|---|---|---|
| **A** | Fully offline-capable essential | Ritual guidance, RIC, phrasebook, emergency cards, Save My Gate recall, local planner/notes/bookmarks/medical profile. |
| **B** | Offline with cached snapshot | Flags, pack manifest snapshot, cached entitlement continuity, stale group summary. |
| **C** | Online-required trusted operation | Group creation, group join, server-backed check-ins, purchase/restore, deletion/export requests. |
| **D** | Rich optional enhancement | Realtime live board, high-fidelity undownloaded map assets, server-backed recommendations. |

Pack lifecycle remains:

```text
NOT_INSTALLED -> DOWNLOADING -> VERIFYING -> INSTALLED
                         \-> FAILED
INSTALLED -> PURGED
FAILED/PURGED -> DOWNLOADING
```

A pack may enter `INSTALLED` only after the required trust-chain checks succeed:

1. manifest signature verification,
2. artifact checksum verification,
3. artifact signature verification,
4. signing-key validity / revocation check,
5. schema/app compatibility check,
6. storage-completeness check.

Checksum alone is not sufficient for quality-first release.

See files `15`, `23`, `26`, `29`, `30`, and [`SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`](./SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml).

---

## Feature families

| Spec | Feature family |
|---|---|
| `18` | Rituals, RIC, and religious content. |
| `19` | Maps, Save My Gate, 3D/2D/text wayfinding degradation. |
| `20` | Group creation, group join, check-ins, regroup, Live Board, shared coordination. |
| `21` | Planner, reminders, wallet, notes, bookmarks. |
| `22` | Phrasebook, emergency, safety, medical, assistive tools. |
| `23` | Offline packs, audio, and content distribution. |
| `24` | Account, subscriptions, entitlements, Settings, Privacy & Data. |
| `25` | Onboarding, Home, Simple Mode. |

---

## Group coordination posture

Group coordination is designed for recovery and regrouping, not surveillance.

Current quality-first decision:

- In-app group creation is a governed authenticated leader flow.
- The server generates the canonical 6-character uppercase alphanumeric join code.
- Group creation, join, check-ins, and regroup writes are trusted online operations.
- Baseline group coordination is not Supporter-only.
- Live Board may be a Supporter enrichment, but it is not the baseline group promise.
- No contact import, automatic invites, hidden social graph, passive background pings, or continuous tracking.
- Ordinary check-ins are text-first and do not carry precise GPS coordinates.
- Freshness must be represented honestly as fresh, stale, expired, unavailable, or revoked where applicable.

See files `13`, `14`, `20`, `24`, `29`, and [`SPECS/CONTRACTS/group_presence_privacy_contract.yaml`](./SPECS/CONTRACTS/group_presence_privacy_contract.yaml).

---

## Account, entitlement, and Privacy & Data

Account is optional until a trusted online feature requires it.

Trusted account-gated operations include:

- group creation,
- group join,
- purchase validation/restore,
- account deletion request/status,
- privacy export request,
- protected account settings.

Supporter may unlock convenience and enrichment such as offline audio, pack auto-download, richer Live Board, smart planner suggestions, or extended notes/bookmarks. It must never gate ritual correctness, RIC, baseline recovery/navigation, phrase text, emergency cards, medical profile basics, or basic group coordination.

Privacy & Data is a first-class Settings flow. It must explain local-only versus server-backed data, deletion request/status, export request, retention summary, and public deletion/help handoff where required.

See files `14`, `24`, `29`, and [`SPECS/CONTRACTS/entitlement_capability_policy.yaml`](./SPECS/CONTRACTS/entitlement_capability_policy.yaml).

---

## Canonical screens

The canonical screen inventory is currently **47 screens**.

The screen system includes first-class flows for:

- `group_creation_flow`,
- `join_group_flow`,
- `privacy_data_flow`,
- `pack_detail_install_flow`,
- Home and Simple Mode recovery surfaces,
- ritual/RIC flows,
- map/Save My Gate flows,
- emergency/phrase/medical flows,
- account/entitlement/restore flows.

Every screen must define entry points, preconditions, offline/degraded behavior, accessibility notes, entitlement dependencies, analytics events, and release-evidence ownership.

See file `11` and [`SPECS/CONTRACTS/screen_feature_traceability.yaml`](./SPECS/CONTRACTS/screen_feature_traceability.yaml).

---

## API surface

The canonical API catalog lives in file `14`.

Key endpoint families include:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/v1/flags` | Public lightweight config/control-plane snapshot. |
| `GET` | `/v1/packs/manifest` | Public manifest discovery for packs/artifacts. |
| `GET` | `/v1/entitlements` | Trusted user entitlement snapshot. |
| `POST` | `/v1/groups` | Governed group creation. |
| `POST` | `/v1/groups/join` | Join group by code. |
| `POST` | `/v1/groups/{group_id}/checkins` | Server-backed group check-in. |
| `POST` | `/v1/groups/{group_id}/regroup-pins` | Leader-only regroup pin creation. |
| `POST` | `/v1/purchases/validate` | Store purchase validation. |
| `POST` | `/v1/purchases/restore` | Purchase restore. |
| `POST` | `/v1/account/deletion-request` | Server-backed account deletion request. |
| `GET` | `/v1/account/deletion-status` | Deletion request status. |
| `POST` | `/v1/privacy/export-request` | Scoped server-backed data export request. |
| `GET` | `/v1/privacy/retention-summary` | User-readable retention summary. |

Group creation, group join, purchase validation/restore, and other retry-sensitive writes require idempotency where file `14` specifies it.

---

## Machine-readable contract artifacts

The `SPECS/CONTRACTS/` directory contains implementation-facing contracts that mirror critical markdown spec truth:

| Contract | Purpose |
|---|---|
| `entitlement_capability_policy.yaml` | Defines never-gate and Supporter capability rules. |
| `group_presence_privacy_contract.yaml` | Defines freshness, TTL, precision, consent, and privacy behavior for group presence. |
| `content_pack_trust_chain_contract.yaml` | Defines signed manifest/artifact activation and rollback requirements. |
| `advisory_source_registry.schema.yaml` | Defines freshness/source metadata for safety advisories and emergency/official handoff content. |
| `release_gate_taxonomy.yaml` | Defines release risk classes, blocker levels, no-waiver expectations, and waiver object fields. |
| `screen_feature_traceability.yaml` | Maps critical screens to feature owners and release-evidence expectations. |

Validation helper:

```bash
python tools/specs/validate_spec_contracts.py
```

---

## Release, testing, and operations spine

| File | Owns |
|---|---|
| `27` | Testing strategy, matrix, device-lab mechanics, contract validation tests. |
| `28` | Release go/no-go gates, evidence sufficiency, waiver authority, no-waiver zones. |
| `29` | Security, privacy, compliance, data classification, risk register. |
| `30` | Delivery runbook, rollout, containment, rollback, incidents, support handoff. |

No release may override religious correctness, emergency baseline access, privacy-light behavior, RLS/auth boundaries, deletion/export truth, artifact authenticity, or critical accessibility requirements.

---

## AI agent operational rules

All AI agents must:

1. Start with [`SPECS/01_README_AND_MASTER_INDEX.md`](./SPECS/01_README_AND_MASTER_INDEX.md).
2. Read file `31` when a change touches quality-first hardening decisions.
3. Read affected files in `SPECS/CONTRACTS/`.
4. Never invent API endpoints, entitlement keys, schema fields, screens, content rules, or release gates.
5. Never weaken privacy, RLS, signing, local-only data boundaries, accessibility, or religious content governance for implementation convenience.
6. Update markdown specs and contract artifacts together when contract truth changes.
7. Treat passing tests as insufficient unless the relevant release evidence also exists.

---

## Spec file index

All normative specifications reside in [`SPECS/`](./SPECS/).
The detailed master index is [`SPECS/01_README_AND_MASTER_INDEX.md`](./SPECS/01_README_AND_MASTER_INDEX.md).

Current normative set:

- `01_README_AND_MASTER_INDEX.md`
- `02_AI_AGENT_RULES_AND_WORKFLOW.md`
- `03_PRODUCT_CHARTER_AND_SCOPE.md`
- `04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`
- `05_ROADMAP_PROGRESS_AND_CHANGELOG.md`
- `06_SYSTEM_ARCHITECTURE.md`
- `07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`
- `08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md`
- `09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md`
- `10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md`
- `11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`
- `12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md`
- `13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`
- `14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`
- `15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md`
- `16_MAP_ARCHITECTURE_POSITIONING_ROUTING_3_D_AND_OFFLINE_WAYFINDING.md`
- `17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md`
- `18_FEATURE_RITUALS_RIC_AND_RELIGIOUS_CONTENT.md`
- `19_FEATURE_MAPS_SAVE_MY_GATE_AND_3_D_WAYFINDING.md`
- `20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md`
- `21_FEATURE_PLANNER_REMINDERS_WALLET_NOTES_AND_BOOKMARKS.md`
- `22_FEATURE_PHRASEBOOK_EMERGENCY_SAFETY_AND_ASSISTIVE_TOOLS.md`
- `23_FEATURE_OFFLINE_PACKS_AUDIO_AND_CONTENT_DISTRIBUTION.md`
- `24_FEATURE_ACCOUNT_SUBSCRIPTIONS_ENTITLEMENTS_AND_SETTINGS.md`
- `25_FEATURE_ONBOARDING_HOME_AND_SIMPLE_MODE.md`
- `26_CONTENT_MODEL_SCHOLAR_REVIEW_AND_PUBLISHING_WORKFLOW.md`
- `27_TESTING_STRATEGY_TEST_MATRIX_AND_DEVICE_LAB.md`
- `28_REAL_WORLD_VERIFICATION_RELEASE_GATES_AND_EVIDENCE.md`
- `29_SECURITY_PRIVACY_COMPLIANCE_AND_RISK_REGISTER.md`
- `30_DELIVERY_RUNBOOK_INCIDENTS_ROLLBACK_AND_OPERATIONS.md`
- `31_QUALITY_FIRST_HARDENING_AMENDMENTS.md`

Contract artifacts live under [`SPECS/CONTRACTS/`](./SPECS/CONTRACTS/).

---

End of file.