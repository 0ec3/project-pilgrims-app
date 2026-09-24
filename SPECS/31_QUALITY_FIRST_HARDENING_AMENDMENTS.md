# 31 — QUALITY-FIRST HARDENING AMENDMENTS

## Document status
- **Type:** Normative amendment and cross-spec hardening patch
- **Priority:** Highest for conflicts listed here
- **Audience:** Founder, product lead, engineering lead, design lead, backend engineer, Flutter engineer, QA, AI coding agents, release agents
- **Purpose:** Convert audit findings into implementation-safe amendments while keeping the current 01–31 normative spec system and machine-readable contracts coherent.
- **Related files:** 03, 11, 13, 14, 15, 18–30, `SPECS/CONTRACTS/*`

---

# 1. Quality-first operating posture

This project optimizes for mature, trustworthy product quality rather than MVP speed.

Scope may still be staged for evidence, safety, operations, and implementation control, but shipped capabilities must feel complete, calm, accessible, privacy-light, coherent, and suitable for pilgrims under stress.

Quality-first does **not** mean feature sprawl. It means:
- richer features must have sharper contracts,
- UI must remain calm and recoverable,
- offline and degraded behavior must be real,
- religious correctness and safety must remain protected,
- privacy promises must be enforceable in data/API contracts,
- release evidence must prove the behavior users rely on.

---

# 2. Machine-readable contract artifacts

The following files are now part of the normative specification system:

- `SPECS/CONTRACTS/entitlement_capability_policy.yaml`
- `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`
- `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`
- `SPECS/CONTRACTS/advisory_source_registry.schema.yaml`
- `SPECS/CONTRACTS/release_gate_taxonomy.yaml`
- `SPECS/CONTRACTS/screen_feature_traceability.yaml`

Markdown specs remain the human-readable authority. The contract artifacts exist so implementation, tests, release checks, and AI agents can validate critical truths without reinterpreting prose.

Any product, API, data, entitlement, safety, content, release, or privacy change that affects a contract artifact must update the markdown spec and the artifact in the same change.

---

# 3. Superseding decision: group creation is governed in-app scope

## 3.1 Decision
Quality-first V1 supports in-app group creation as a governed, authenticated leader flow.

This supersedes any wording that treats in-app group creation as undefined external provisioning or out of scope by default.

## 3.2 Reason
The README and persona-level flows identify group creation as part of the group leader journey. Treating group provisioning as undefined creates product ambiguity and implementation drift.

A mature app should not leave pilgrims or group leaders dependent on an unspecified external provisioning path unless that path is explicitly designed, operated, and supported. Therefore, group creation must either be fully implemented with controls or explicitly disabled by release policy with honest UI copy.

## 3.3 Required behavior
In-app group creation must:
- require authenticated user context,
- create the authenticated user as initial active `LEADER`,
- generate a server-authoritative 6-character uppercase alphanumeric code,
- apply rate limits and abuse controls,
- return clear sharing copy,
- avoid importing contacts or creating hidden social graphs,
- provide SMS/share-code fallback without auto-sending,
- create auditable server state,
- degrade honestly when offline or unavailable.

## 3.4 API impact
File `14` must treat `POST /v1/groups` as an active authenticated write endpoint, not optional future scope, when group creation ships.

Minimum endpoint:

```text
POST /v1/groups
Auth: Required
Purpose: Create a governed group and assign the requester as initial leader.
Idempotency-Key: Required
Rate limit: strict, abuse-sensitive, lower than check-ins
```

## 3.5 Data impact
File `13` must support leader-created groups using the existing `groups` and `group_members` model. The server must enforce exactly one active logical leader and must not trust client-created leader state.

## 3.6 UI impact
File `11` must include `group_creation_flow` as a governed flow screen when this capability is enabled.

File `20` owns the group-creation business behavior.

File `24` owns the account gate copy and auth requirement.

Files `27` and `28` must test group creation under success, offline, duplicate/retry, abuse/rate-limit, and authorization failure states.

---

# 4. Entitlement capability policy

File `24` owns entitlement truth. File `03` owns ethical monetization boundaries. Feature files own feature-specific behavior.

The machine-readable implementation checklist is `SPECS/CONTRACTS/entitlement_capability_policy.yaml`.

## 4.1 Non-negotiable rule
Supporter may unlock convenience, enrichment, automation, and richer offline assets. It must never gate:
- ritual correctness,
- RIC access,
- baseline recovery/navigation,
- phrase text,
- emergency cards,
- medical profile basics,
- basic group coordination,
- local-first basic planner/notes/bookmarks capability.

## 4.2 Implementation rule
Client code must not invent entitlement keys or treat Supporter as a generic unlock-all flag.

Any capability marked `never_gate` must have release tests proving access is preserved for the relevant guest/free/offline states.

---

# 5. Group presence and privacy contract

The machine-readable privacy contract is `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`.

## 5.1 Reason
Existing specs correctly reject surveillance and misleading live-state behavior, but quality-first implementation requires normalized TTL, freshness, precision, revocation, and retention semantics.

## 5.2 Canonical object
When shared presence, freshness, regroup handoff, or route handoff needs normalized state, use `group_presence_event` semantics:

```text
group_presence_event
- event_id
- group_id
- actor_user_id
- event_type: safe_checkin | text_checkin | regroup_pin | route_handoff
- text_pin
- map_anchor_ref?
- precision_level: none | coarse | precise
- shared_at
- ttl_expires_at
- freshness_status: fresh | stale | expired | revoked
- share_reason: explicit_user_action
- consent_token_id?
- revoked_at?
- retention_expires_at?
- client_event_id?
```

## 5.3 Enforcement rules
- Ordinary safe/text check-ins must not contain precise GPS coordinates.
- Precise location is not default and requires explicit task-linked user action.
- Cached state must show freshness age or stale/expired status where it matters.
- Realtime is an enhancement, not the source of truth.
- No raw precise location may enter ordinary product analytics.
- Expired or revoked state must not appear as live board certainty.

---

# 6. Signed content and pack trust chain

The machine-readable trust-chain contract is `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`.

## 6.1 Strengthened rule
Checksum verification remains mandatory but is not sufficient for mature release quality.

Downloadable packs, governed content artifacts, manifest files, and activation pointers require publisher authenticity controls.

## 6.2 Activation requirements
A downloaded pack or governed artifact may move to `INSTALLED` only after:
1. manifest signature verification succeeds,
2. artifact checksum verification succeeds,
3. artifact signature verification succeeds,
4. schema/app compatibility checks pass,
5. storage completeness checks pass.

Failure at any step must preserve last-known-good runtime behavior and must not expose the candidate artifact to feature runtime.

## 6.3 Operational requirements
Signing-key rotation, revoked-key handling, anti-rollback policy, compromise response, and emergency rollback override must be documented in release and operations scope before ship.

---

# 7. Advisory source registry

The machine-readable advisory source schema is `SPECS/CONTRACTS/advisory_source_registry.schema.yaml`.

## 7.1 Scope
This applies to:
- safety banners,
- emergency numbers,
- official handoff notes,
- region-sensitive safety tips,
- seasonal notices.

## 7.2 Required behavior
Each governed advisory source must define:
- jurisdiction,
- locale,
- authority/source type,
- verification timestamp,
- expiry timestamp,
- owner,
- severity,
- offline fallback copy,
- stale behavior,
- whether expiry blocks publication.

Expired source metadata must fail publication when `publish_blocking_if_expired=true`.

Safety advisories must remain non-blocking for ritual and recovery tasks.

---

# 8. Privacy & Data flow

File `24` must expose a first-class Privacy & Data flow.

## 8.1 Required user-facing capabilities
The flow must include:
- account deletion request,
- deletion request status,
- local-only data deletion explanation,
- personal data export request where applicable,
- retention summary for purchase/accounting/security/support categories,
- backup/legal-hold delay explanation where applicable.

## 8.2 Required API surface
File `14` must include, or explicitly document an approved equivalent for:

```text
POST /v1/account/deletion-request
GET  /v1/account/deletion-status
POST /v1/privacy/export-request
GET  /v1/privacy/retention-summary
```

## 8.3 Boundary rule
The UI must distinguish local-only data from server-backed account data. It must not imply that local medical profile, notes, planner items, ritual progress, saved anchors, or bookmarks were uploaded when they remain device-local.

---

# 9. Unified release gate taxonomy

File `28` owns go/no-go gates, blocker classification, risk-class mapping, and waiver authority.

File `27` owns verification mechanics.

File `30` owns rollout, incident response, rollback, and operational execution after gate decisions.

The machine-readable taxonomy is `SPECS/CONTRACTS/release_gate_taxonomy.yaml`.

## 9.1 Contract evidence requirement
Release evidence must explicitly state whether changed behavior affects:
- entitlement capability policy,
- group presence privacy,
- content/pack trust chain,
- advisory freshness,
- screen-feature traceability,
- account deletion/privacy behavior.

Any affected contract must have corresponding proof before release approval.

## 9.2 No-waiver zones
No waiver may override:
- religious correctness,
- essential safety access,
- privacy-light behavior,
- store/legal non-compliance,
- known artifact authenticity failure,
- misleading live/group state.

---

# 10. Screen-feature traceability

File `11` owns screen/state/navigation contracts. Feature files own business behavior.

The machine-readable traceability checklist is `SPECS/CONTRACTS/screen_feature_traceability.yaml`.

## 10.1 Required additional screen concepts
The screen inventory must include these quality-critical concepts when the feature is enabled:
- `group_creation_flow`,
- `privacy_data_flow`.

## 10.2 Implementation rule
Every screen implementation must reference:
- feature owner,
- critical flows,
- offline behavior,
- permission dependencies,
- entitlement dependencies,
- accessibility notes,
- analytics events,
- release-evidence owner.

If a screen contract and feature-family contract diverge, implementation must stop and both specs must be updated through change control before code proceeds.

---

# 11. Audit carry-forward status

| Item | Status | Current truth |
|---|---|---|
| Activate governed group creation and privacy endpoints in file `14` | Done | `POST /v1/groups` and the account/privacy request/status endpoints are active normative contracts. |
| Align file `20` with governed in-app group creation | Done | Group creation is an authenticated, server-trusted leader flow. |
| Define normalized `group_presence_events` where needed | Done | File `13`, file `14`, file `20`, and `CONTRACTS/group_presence_privacy_contract.yaml` agree on identifier mapping, TTL/freshness, privacy, and RLS expectations. |
| Add signed manifest/artifact trust metadata | Done | Files `15`, `23`, `26`, `29`, `30`, and `CONTRACTS/content_pack_trust_chain_contract.yaml` define signed activation and last-known-good behavior. |
| Define Privacy & Data and entitlement ownership | Done | File `24` owns the user-facing flow and entitlement truth; file `14` owns the HTTP contracts. |
| Align testing/release/operations with release-gate taxonomy | Done | Files `27`, `28`, and `30` reference the machine-readable taxonomy and evidence boundaries. |
| Add `group_creation_flow` and `privacy_data_flow` traceability | Done | File `11` and `CONTRACTS/screen_feature_traceability.yaml` contain the canonical screen IDs. |
| Build implementation tests from contract artifacts | Pending implementation | Validator/test requirements are specified, but Flutter/backend implementation and runtime fixtures remain not started per file `05`. |

This amendment is now a cross-spec hardening record, not a substitute for older prose sections. Current domain specs and contracts must remain synchronized directly through normal change control.
