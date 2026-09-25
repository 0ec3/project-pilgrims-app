# 17 — ANALYTICS, OBSERVABILITY, AND PERFORMANCE BUDGETS

## Document status
- **Type:** Normative quality, telemetry, and runtime-budget document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, backend engineers, Flutter engineers, QA, release engineers, data/analytics contributors, AI coding agents, reviewer agents, operations contributors
- **Purpose:** Define how Pilgrims Mobile App measures real usage, detects regressions, observes failures across mobile, backend, content, and pack runtimes, enforces privacy-safe analytics, and maintains performance budgets.
- **Authority level:** This file is the canonical source of truth for analytics taxonomy, telemetry naming, privacy-safe measurement rules, logging boundaries, crash/error observability, alert thresholds, and performance budgets.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `20`, `24`, `26`, `27`, `28`, `29`, `30`, `31`
- **Related contract artifacts:** `CONTRACTS/entitlement_capability_policy.yaml`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/advisory_source_registry.schema.yaml`, `CONTRACTS/screen_feature_traceability.yaml`

---

# 1. Purpose

This file defines the measurement layer required to know whether the app is working safely, calmly, and reliably in real pilgrimage conditions.

It covers:
- event taxonomy,
- event naming,
- allowed and forbidden telemetry payload classes,
- mobile and backend observability,
- content/pack/advisory activation observability,
- performance budgets,
- release-evidence expectations.

---

# 2. Core principles

## 2.1 Measure real user value, not vanity
Instrumentation must prioritize whether pilgrims can complete important tasks safely and calmly.

## 2.2 Privacy-light by design
Telemetry must avoid sensitive payloads and unnecessary personal detail. The app measures feature health and degraded states, not private user stories.

## 2.3 Observability is a product capability
Crash reporting, alerting, tracing, and performance monitoring are part of how the product remains trustworthy in the field.

## 2.4 Budgets are contracts
Startup time, rendering smoothness, memory, asset size, network usage, backend latency, pack verification, and critical-flow latency must have explicit budgets.

## 2.5 Local-first still needs measurement
Offline-first behavior changes how telemetry is queued, sampled, flushed, and interpreted. It does not remove the need for observability.

## 2.6 Graceful degradation must be observable
Fallbacks such as stale group state, text-only maps, trust-chain failure, or offline account requests must be visible to QA and release dashboards without exposing sensitive contents.

## 2.7 Contract artifacts need telemetry hooks
Machine-readable contracts must have corresponding observability signals where runtime behavior can fail.

---

# 3. Telemetry architecture

Telemetry zones:
1. client product analytics,
2. client crash/error/performance telemetry,
3. backend service observability,
4. pack/content/advisory activation observability,
5. release and operational dashboards.

## 3.1 Correlation model
Every protected API request and telemetry batch should support correlation without including sensitive payload contents.

Required common correlation fields:
- `request_id` where server-backed,
- `session_id`,
- `install_id`,
- `release_version`,
- `build_number`,
- `platform`,
- `environment`.

## 3.2 Offline queue rules
- Essential user flows never block on analytics upload.
- Events are timestamped at occurrence time, not upload time.
- Stale queued events may be dropped after the retention window.
- Queue pressure drops lower-priority diagnostics before critical product-quality events.

---

# 4. Event taxonomy model

## 4.1 Canonical event families
Allowed event families:
- `app_*`
- `session_*`
- `screen_*`
- `journey_*`
- `ritual_*`
- `ric_*`
- `map_*`
- `group_*`
- `planner_*`
- `notes_*`
- `bookmark_*`
- `wallet_*`
- `phrasebook_*`
- `emergency_*`
- `medical_*`
- `pack_*`
- `content_*`
- `advisory_*`
- `entitlement_*`
- `privacy_*`
- `account_*`
- `settings_*`
- `sync_*`
- `error_*`
- `perf_*`

`experiment_*` remains disallowed unless experimentation is later approved.

## 4.2 Naming rule
Event names use lowercase `snake_case` and follow `<family>_<object>_<action>`.

Examples:
- `screen_home_root_view`
- `group_create_complete`
- `pack_artifact_signature_fail`
- `privacy_export_request_complete`

## 4.3 Naming stability rule
Production event names must not be silently renamed. Changes require a versioned change note, dashboard migration, downstream query update, and release note where material.

---

# 5. Event envelope contract

Every product analytics event must include:
- `event_name`,
- `occurred_at`,
- `session_id`,
- `install_id`,
- `app_version`,
- `build_number`,
- `platform`,
- `os_version`,
- `locale`,
- `text_direction`,
- `network_state`,
- `season`,
- `simple_mode_enabled`.

Where relevant, include:
- `screen_id`,
- `journey_id`,
- `entry_point`,
- `result`,
- `failure_code`,
- `degradation_state`,
- `latency_ms`,
- `content_version`,
- `pack_version`,
- `manifest_id`,
- `entitlement_tier_snapshot`,
- `freshness_status`.

Freeform user-entered text is forbidden by default.

---

# 6. Privacy-safe analytics rules

Telemetry must not include sensitive content classes such as account secrets, store proof payloads, medical details, private note/planner contents, exact hidden location, group invitation codes, group names, check-in text, contact-list data, or deletion/export payload contents.

## 6.1 Map privacy
Map analytics may record coarse quality signals such as route success/failure, position-confidence state, fallback activation, pack state, and permission state. Detailed path reconstruction is not allowed by default.

## 6.2 Group privacy
Allowed group signals:
- create/join/check-in/regroup success or failure,
- role as a coarse enum,
- freshness status,
- fallback method,
- Live Board viewed.

Disallowed by default:
- contact-list data,
- recipient contact details,
- member presence history as analytics payload,
- message body content,
- group invitation code values,
- precise coordinate payloads.

## 6.3 Privacy & Data telemetry
Deletion/export telemetry may record lifecycle state and failure class. It must not include exported content, deletion payload details, legal notes, or unnecessary identifiers.

---

# 7. Event priority tiers

## 7.1 Tier A — Must-have product truth
Mandatory for release-worthy instrumentation:
- app launch/session start,
- critical screen views,
- ritual start/resume/RIC result,
- emergency/phrase/medical baseline use,
- Save My Gate / map fallback,
- group create/join/check-in/regroup flows,
- pack download/verify/install/failure,
- entitlement restore/validate/upgrade outcomes,
- Privacy & Data deletion/export request outcomes,
- content/advisory activation failures.

## 7.2 Tier B — Strong quality signals
- offline fallback entry,
- stale cache use,
- retry usage,
- permission-denied states,
- pack repair flows,
- map confidence degradation,
- screen render budget breach,
- trust-chain degraded/failure state.

## 7.3 Tier C — Optimization signals
- secondary settings exploration,
- component-level micro-interactions,
- non-critical content impressions.

Tier A events should be unsampled except under governed exception.

---

# 8. Canonical feature event map

## 8.1 App/session/screen events
- `app_launch_start`
- `app_launch_complete`
- `app_launch_fail`
- `session_start`
- `session_end`
- `session_restore_from_background`
- `session_offline_start`
- `screen_<screen_id>_view`
- `screen_<screen_id>_empty`
- `screen_<screen_id>_error`
- `screen_<screen_id>_offline`
- `screen_<screen_id>_degrade`

Critical screen IDs include `home_root`, `simple_home`, `group_creation_flow`, `join_group_flow`, `privacy_data_flow`, `pack_detail_install_flow`, `emergency_root`, `phrasebook_root`, `map_root`, `rituals_root`, and `ric_result`.

## 8.2 Rituals and RIC events
- `ritual_session_start`
- `ritual_session_resume`
- `ritual_step_view`
- `ritual_step_complete`
- `ritual_audio_play`
- `ritual_audio_unavailable`
- `ric_start`
- `ric_question_answered`
- `ric_result_view`
- `ric_result_classified`
- `ric_remedy_open`
- `ric_remedy_saved_to_wallet`

## 8.3 Map and wayfinding events
- `map_root_view`
- `map_pack_missing`
- `map_position_state_change`
- `map_floor_change`
- `map_destination_select`
- `map_route_preview_start`
- `map_route_preview_complete`
- `map_route_preview_fail`
- `map_route_follow_start`
- `map_route_follow_degrade`
- `map_route_follow_exit`
- `map_anchor_save`
- `map_anchor_recall`
- `map_anchor_share`

## 8.4 Group events
- `group_create_start`
- `group_create_complete`
- `group_create_fail`
- `group_join_start`
- `group_join_complete`
- `group_join_fail`
- `group_live_board_view`
- `group_checkin_start`
- `group_checkin_complete`
- `group_checkin_fail`
- `group_checkin_fallback_sms`
- `group_regroup_pin_view`
- `group_regroup_pin_create`
- `group_regroup_pin_route_launch`
- `group_presence_freshness_change`

Allowed parameters include coarse role, check-in method, live-board enabled state, regroup-pin state, freshness status, network state, and failure code.

## 8.5 Packs and offline-distribution events
- `pack_catalog_view`
- `pack_detail_view`
- `pack_download_queue`
- `pack_download_start`
- `pack_download_progress_checkpoint`
- `pack_download_pause`
- `pack_download_resume`
- `pack_download_fail`
- `pack_verify_start`
- `pack_checksum_fail`
- `pack_manifest_signature_fail`
- `pack_artifact_signature_fail`
- `pack_signing_key_revoked_fail`
- `pack_compatibility_fail`
- `pack_last_known_good_preserved`
- `pack_install_complete`
- `pack_purge_complete`
- `pack_auto_download_opt_in`

## 8.6 Content and advisory events
- `content_artifact_activate_start`
- `content_artifact_activate_complete`
- `content_artifact_activate_fail`
- `content_rollback_pointer_activate`
- `advisory_registry_validate_complete`
- `advisory_registry_validate_fail`
- `advisory_expired_blocked`
- `advisory_stale_fallback_view`

## 8.7 Entitlement, account, and privacy events
- `entitlement_snapshot_refresh`
- `entitlement_restore_start`
- `entitlement_restore_complete`
- `entitlement_restore_fail`
- `entitlement_upgrade_view`
- `entitlement_upgrade_start`
- `entitlement_upgrade_complete`
- `entitlement_upgrade_fail`
- `settings_preference_change`
- `privacy_data_view`
- `account_deletion_request_start`
- `account_deletion_request_complete`
- `account_deletion_request_fail`
- `account_deletion_status_view`
- `privacy_export_request_start`
- `privacy_export_request_complete`
- `privacy_export_request_fail`
- `privacy_retention_summary_view`


### Appearance preference
Appearance changes should use the existing `settings_preference_change` event rather than introducing a new appearance-specific event. Allowed safe value: `appearance_mode` with enum `system | light | dark`. Do not log theme-derived user content or sensitive context.
---

# 9. Core funnels

## 9.1 First successful ritual guidance use
`screen_home_root_view` → `ritual_session_start` → `ritual_step_view` → `ritual_step_complete` → stable continuation/completion milestone.

## 9.2 Recovery using RIC
`ric_start` → `ric_question_answered` → `ric_result_view` → `ric_remedy_open` → optional `ric_remedy_saved_to_wallet`.

## 9.3 Orientation and map recovery
`map_root_view` → `map_destination_select` → `map_route_preview_complete` → `map_route_follow_start` or fallback outcome marker.

## 9.4 Group creation / join / check-in
Leader funnel: `group_create_start` → `group_create_complete` → safe share-code handoff where tracked without code values.
Member funnel: `group_join_start` → `group_join_complete` → `group_checkin_start` → `group_checkin_complete` or `group_checkin_fallback_sms`.

## 9.5 Supporter pack adoption
`pack_catalog_view` → `pack_detail_view` → supporter state or `entitlement_upgrade_view` → `pack_download_start` → verification events → `pack_install_complete`.

## 9.6 Privacy & Data action
`privacy_data_view` → deletion/export/retention action → completion/failure/status view.

---

# 10. Error taxonomy

Canonical top-level error classes:
- `NETWORK`
- `AUTH`
- `AUTHORIZATION`
- `VALIDATION`
- `RATE_LIMIT`
- `SERVER`
- `CACHE`
- `STORAGE`
- `PACK_CHECKSUM`
- `PACK_SIGNATURE`
- `PACK_KEY_REVOKED`
- `PACK_COMPATIBILITY`
- `PACK_SPACE`
- `PACK_DELIVERY`
- `CONTENT_SIGNATURE`
- `CONTENT_VERSION_MISMATCH`
- `ADVISORY_EXPIRED`
- `LOCATION_PERMISSION`
- `BLUETOOTH_PERMISSION`
- `POSITIONING_UNAVAILABLE`
- `ROUTING_UNAVAILABLE`
- `ENTITLEMENT_STALE`
- `PURCHASE_VALIDATION`
- `PRIVACY_REQUEST_UNAVAILABLE`
- `DELETION_REQUEST_FAILED`
- `EXPORT_REQUEST_FAILED`
- `UI_RENDER`
- `UNKNOWN`

Events may include `failure_code`, but it must use documented enums and not raw exception messages.

---

# 11. Backend observability

Backend metrics must include:
- request count,
- latency,
- error rate,
- rate-limit count,
- auth failure count,
- authorization failure count,
- integration failure count,
- group create/join/check-in failures,
- purchase/restore failures,
- deletion/export request failures,
- pack manifest failures,
- trust-chain verification failures where server-observable,
- stale fallback usage where client reports it.

Critical endpoint alerts include:
- `GET /v1/flags`,
- `GET /v1/packs/manifest`,
- `GET /v1/entitlements`,
- `POST /v1/groups`,
- `POST /v1/groups/join`,
- `POST /v1/groups/{group_id}/checkins`,
- `POST /v1/groups/{group_id}/regroup-pins`,
- `POST /v1/purchases/validate`,
- `POST /v1/purchases/restore`,
- `POST /v1/account/deletion-request`,
- `GET /v1/account/deletion-status`,
- `POST /v1/privacy/export-request`,
- `GET /v1/privacy/retention-summary`.

---

# 12. Logging strategy

Production logs must redact or omit sensitive content classes described in file `29`, including protected account/session material, store proof payloads, medical/private-support contents, group code values, precise private location, and deletion/export payload contents.

Backend logs should include structured operational fields:
- `timestamp`,
- `request_id`,
- `path`,
- `method`,
- `status_code`,
- `latency_ms`,
- `release_version`,
- `environment`,
- `failure_code` where applicable.

---

# 13. Performance budgets

Pilgrims Soft Surface rendering must stay within the existing runtime budgets. Layered outer/inset shadows, highlights, ambient glow, scrims, or blur must use shared effect tiers and low-cost variants for dense/repeated surfaces. Decorative effects must simplify before they are allowed to cause scrolling, animation, startup, or map-control jank.

Light/Dark appearance switching must not trigger unnecessary domain reloads or navigation reconstruction.

Initial budgets:
- cold start to first meaningful Home: p95 ≤ 2.5s on representative devices,
- emergency root open from Home: p95 ≤ 300ms after app ready,
- phrase big-text open: p95 ≤ 300ms,
- Save My Gate recall: p95 ≤ 400ms,
- group creation response under normal service: p95 ≤ 1000ms,
- group join response: p95 ≤ 800ms,
- check-in response: p95 ≤ 600ms,
- pack detail open: p95 ≤ 500ms,
- pack verification progress UI responsive during verification,
- Privacy & Data screen open: p95 ≤ 500ms,
- deletion/export request submit under normal service: p95 ≤ 1200ms.

Budgets are release risks when exceeded on affected critical flows.

---

# 14. Release evidence expectations

Telemetry/performance evidence must show:
- critical events are emitted with safe parameters,
- forbidden fields are absent,
- critical backend endpoints have metrics/alerts,
- degraded/stale/offline states are observable,
- trust-chain failure signals exist,
- Privacy & Data actions are observable without exposing contents,
- performance budgets are measured on representative devices where required,
- dashboards support file `28` evidence bundles.

---

# 15. Definition of done

Analytics and observability are ready when:
- event taxonomy covers critical flows,
- forbidden fields are blocked or reviewed,
- group creation/privacy/pack trust-chain/advisory events exist,
- backend endpoints emit safe operational metrics,
- performance budgets are testable,
- release dashboards support files `27` and `28`,
- incident signals support file `30`.

---

# 16. AI-agent checklist

Before adding or changing telemetry, an AI agent must:
1. Read files `17`, `27`, `28`, `29`, `30`, and relevant feature specs.
2. Check affected contract artifacts.
3. Confirm event name stability.
4. Confirm forbidden payload fields.
5. Confirm release/incident dashboards are not broken.
6. Never add sensitive user or protected operational payloads to analytics.

# Guide Marketplace analytics and observability amendment

Guide Marketplace uses the privacy-safe `guide_*` event family.

Approved candidate event names:
- `guide_marketplace_view`
- `guide_search`
- `guide_profile_view`
- `guide_contact_intent`
- `guide_application_start`
- `guide_application_submit`
- `guide_application_result`
- `guide_listing_publish`
- `guide_report_submit`
- `guide_verification_state_change`

Allowed properties must remain low-cardinality, non-sensitive operational dimensions such as normalized service type, normalized verification state/type, result class, broad locale, and broad feature state where justified.

Ordinary analytics, logs, traces, crash breadcrumbs, and experiment payloads must not contain:
- government identity values,
- raw licence/credential numbers,
- credential-document contents,
- phone/WhatsApp/email,
- private conversation content,
- report body,
- precise private location,
- religious question/advice content.

Operational monitoring should measure:
- public-listing eligibility/filtering failures,
- stale-data fallback rate,
- contact-resolution errors,
- application/listing write errors,
- credential-expiry/revocation propagation latency,
- report/moderation queue health,
- rate-limit/abuse signals,
- unexpected public visibility after ineligibility.

No analytics signal may be treated as credential verification or legal eligibility truth.

---

End of file.