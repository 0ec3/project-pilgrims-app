# 17 — ANALYTICS, OBSERVABILITY, AND PERFORMANCE BUDGETS

## Document status
- **Type:** Normative quality, telemetry, and runtime-budget document
- **Priority:** Highest
- **Audience:** Founder, product lead, engineering lead, backend engineers, Flutter engineers, QA, release engineers, data/analytics contributors, AI coding agents, reviewer agents, operations contributors
- **Purpose:** Define how Pilgrims Mobile App measures real usage, detects regressions, observes failures across mobile and backend runtimes, enforces privacy-safe analytics, and maintains strict performance budgets so the product remains calm, fast, trustworthy, and maintainable under real pilgrimage conditions.
- **Authority level:** This file is the canonical source of truth for analytics taxonomy, telemetry naming, privacy-safe measurement rules, logging boundaries, crash/error observability, alert thresholds, and performance budgets. Feature files, dashboards, alerts, instrumentation code, and release gates must not contradict this file.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- **Related files:** `18`, `19`, `20`, `21`, `22`, `23`, `24`, `25`, `26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This product cannot rely on opinions, passing tests, or polished mockups to determine whether it is truly working well.

Pilgrims Mobile App operates in conditions where hidden quality failures are especially dangerous:
- users may be stressed, tired, elderly, or low-confidence with smartphones,
- connectivity can be weak or absent,
- maps and packs can fail in ways that are not obvious from happy-path testing,
- ritual and emergency flows must remain reliable even under degraded conditions,
- AI coding agents can easily add instrumentation inconsistently or over-collect data,
- performance decay can slowly damage user trust long before the app is considered “broken.”

This file exists to prevent those failures by defining:
- what must be measured,
- what must never be measured,
- how analytics events are named and governed,
- how mobile and backend observability fit together,
- what runtime budgets are considered acceptable,
- which thresholds require alerts,
- what evidence is required before release.

---

# 2. Core principles

## 2.1 Measure real user value, not vanity
Instrumentation must prioritize whether pilgrims can complete important tasks safely and calmly, not whether teams can generate large numbers of events.

## 2.2 Privacy-light by design
Telemetry must respect the product’s privacy posture. No hidden continuous location tracking, no medical detail leakage, no raw purchase artifacts, and no ritual-sensitive personal data collection beyond what is strictly necessary for product quality.

## 2.3 Observability is a product capability
Crash reporting, alerting, tracing, and performance monitoring are not optional engineering decorations. They are part of how the product remains trustworthy in the field.

## 2.4 Budgets are contracts, not suggestions
Startup time, rendering smoothness, memory, asset size, network usage, and backend latency must all have explicit budgets. Regressions against these budgets are release risks.

## 2.5 Local-first still needs measurement
Offline-first behavior does not remove the need for telemetry. It changes how telemetry must be queued, sampled, flushed, and interpreted.

## 2.6 Graceful degradation must be observable
If richer behavior degrades to fallback behavior, the system must expose that clearly through telemetry so the team can detect hidden decay.

## 2.7 Instrument once, reuse everywhere
Analytics naming, parameter semantics, correlation IDs, and error taxonomy must be centralized so feature modules do not invent their own incompatible conventions.

## 2.8 Safety-critical and ritual-critical surfaces need stronger discipline
Flows related to ritual correctness, emergency help, group coordination, or wayfinding must receive higher observability priority than cosmetic or purely convenience surfaces.

---

# 3. Scope of this file

This file covers:
- product analytics taxonomy,
- event naming rules,
- event parameter rules,
- user-property rules,
- funnel and journey measurement,
- client logging,
- backend metrics and logging,
- crash/error reporting,
- tracing and correlation,
- alert thresholds and escalation triggers,
- performance budgets for mobile and backend,
- battery, memory, startup, rendering, network, pack, and map budgets,
- release-evidence expectations related to telemetry and performance.

This file does **not** replace:
- detailed API contracts,
- detailed data-model contracts,
- feature-specific behavior specs,
- security/privacy policy,
- testing-matrix details,
- incident runbooks.

Instead, it provides the measurement and operational-quality layer that those files depend on.

---

# 4. Canonical telemetry architecture

## 4.1 Runtime telemetry zones
The telemetry architecture has four major zones:
1. **Client analytics and product telemetry**
2. **Client error and performance telemetry**
3. **Backend service observability**
4. **Release and operational dashboards**

## 4.2 Client telemetry layers
The mobile app must separate telemetry concerns into:
- **product analytics events** for journeys, funnels, feature usage, and degradation signals,
- **diagnostic logs** for developer troubleshooting and low-level debugging,
- **crash and non-fatal exception reporting**,
- **performance traces and runtime metrics**.

## 4.3 Backend telemetry layers
The backend surface must expose:
- structured request logs,
- endpoint success/failure counters,
- latency histograms,
- rate-limit and abuse counters,
- dependency health metrics,
- purchase-validation diagnostics,
- flag/manifest cache behavior metrics.

## 4.4 Correlation model
Every protected API request and every queued telemetry batch should support request or trace correlation without requiring sensitive payload logging.

### Required correlation identifiers
- `request_id` for edge/backend requests,
- `session_id` for app session grouping,
- `install_id` or equivalent app-instance identifier,
- optional `trace_id` for cross-layer troubleshooting,
- `release_version` and `build_number` for every event and diagnostic envelope.

## 4.5 Offline queue model
Client analytics and diagnostic events may be queued locally and flushed later when connectivity is available.

### Queue rules
- essential user flows must never block on analytics upload,
- event delivery is best-effort unless an explicit compliance or financial requirement states otherwise,
- queued events must be time-stamped at occurrence time, not upload time,
- stale queued events older than the retention window may be dropped,
- queue backpressure must prefer dropping lower-priority diagnostics before core product analytics.

---

# 5. Recommended implementation stack and boundaries

## 5.1 Canonical tool categories
The project should implement the following categories of tooling:
- **product analytics platform**,
- **crash/error reporting platform**,
- **client performance instrumentation**,
- **backend metrics/logging/tracing platform**,
- **dashboard and alerting layer**.

## 5.2 Tooling boundary rule
This file defines the **contract** and the **required capabilities**, not a permanently locked vendor choice.

Any chosen implementation must support at minimum:
- event logging with schema discipline,
- privacy-safe parameter control,
- queued/offline client delivery,
- non-fatal and fatal error capture,
- release tagging,
- request correlation,
- backend latency and error metrics,
- alert threshold configuration,
- export or query capability for release evidence.

## 5.3 Current recommended reference architecture
Unless later changed through governance:
- product analytics may use a mobile analytics platform that supports app events, funnels, and user properties,
- mobile crashes and non-fatals should flow into a dedicated crash/error service,
- mobile performance traces may be captured through a dedicated performance SDK and/or platform-native diagnostics,
- edge/backend observability should use structured logs plus metrics counters/histograms and trace-friendly correlation IDs,
- dashboards should aggregate mobile and backend signals into one release-readiness view.

## 5.4 Platform-native diagnostics rule
The implementation should preserve platform-native visibility where possible:
- iOS diagnostics such as launches, hangs, memory, disk writes, and scroll hitches,
- Android vitals such as crash rate, ANR rate, rendering issues, launch time, and low-memory kills.

## 5.5 Flutter boundary rule
Flutter feature modules must emit analytics and traces through shared telemetry interfaces or helpers, not by calling vendor SDKs ad hoc from arbitrary widgets.

---

# 6. Event taxonomy model

## 6.1 Event families
All product analytics events must belong to one of these canonical families:
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
- `pack_*`
- `entitlement_*`
- `settings_*`
- `sync_*`
- `error_*`
- `perf_*`
- `experiment_*` (only if experimentation is later approved)

## 6.2 Event types
Events should describe one of the following behaviors:
- view,
- impression,
- start,
- complete,
- fail,
- retry,
- dismiss,
- degrade,
- recover,
- opt_in,
- opt_out,
- choose,
- save,
- share,
- restore,
- upgrade,
- expire.

## 6.3 Canonical naming rule
Event names use lowercase `snake_case` and should follow:

`<family>_<object>_<action>`

Examples:
- `screen_home_view`
- `ritual_session_start`
- `ric_result_view`
- `map_route_preview_start`
- `map_route_preview_fail`
- `group_join_complete`
- `pack_download_degrade`
- `entitlement_restore_fail`

## 6.4 Naming stability rule
Once an event name is used in production, it must not be silently renamed. Changes require:
- versioned change note,
- dashboard migration,
- downstream query update,
- release note in roadmap/changelog if materially relevant.

## 6.5 No overloaded events
One event must describe one conceptual occurrence. Do not use one generic event like `button_clicked` or `action_taken` across the product.

## 6.6 User-facing language rule
Internal event names must use canonical product terms from the glossary even if user-facing copy differs.

---

# 7. Event envelope contract

## 7.1 Required common fields
Every product analytics event must include:
- `event_name`
- `occurred_at`
- `session_id`
- `install_id`
- `app_version`
- `build_number`
- `platform`
- `os_version`
- `locale`
- `text_direction`
- `network_state`
- `season`
- `simple_mode_enabled`

## 7.2 Strongly recommended common fields
Where relevant, also include:
- `screen_id`
- `journey_id`
- `entry_point`
- `result`
- `failure_code`
- `degradation_state`
- `latency_ms`
- `content_version`
- `pack_version`
- `map_graph_version`
- `entitlement_tier_snapshot`

## 7.3 Field typing rule
All event parameters must have stable declared types.

Examples:
- booleans stay booleans,
- enumerations stay strings from a documented enum set,
- durations use integer milliseconds,
- counts use integers,
- sizes use integer bytes or integer kilobytes/megabytes according to the documented field.

## 7.4 No freeform unbounded text by default
Freeform user-entered text must not be sent in analytics payloads unless a later explicit privacy and governance review approves a narrowly scoped exception.

## 7.5 Cardinality control rule
Avoid high-cardinality fields that damage analytics quality or platform limits.

Forbidden or restricted examples:
- raw join codes,
- exact anchor names entered by users if not normalized,
- full destination labels if not dictionary-backed,
- precise coordinates,
- raw receipt IDs,
- full exception messages as analytics parameters.

---

# 8. User properties and cohort properties

## 8.1 Purpose
User properties exist only to support stable segmentation and product understanding, not to accumulate personal dossiers.

## 8.2 Allowed user-property categories
The app may maintain privacy-safe user properties such as:
- `preferred_language`
- `text_direction`
- `simple_mode_enabled`
- `last_known_season`
- `last_known_entitlement_tier`
- `primary_persona_hint` (derived, coarse, optional)
- `download_preference_wifi_only`
- `large_text_enabled`
- `screen_reader_enabled`

## 8.3 Forbidden user-property categories
Do not store as analytics user properties:
- exact current location,
- continuous movement history,
- medical conditions or profile content,
- specific ritual mistakes made by an identifiable user,
- raw purchase references,
- precise group membership identifiers unless later approved and heavily constrained,
- phone numbers, email addresses, or names.

## 8.4 Cohort-property rule
Where journey analysis needs richer segmentation, prefer coarse cohort flags or temporary analysis joins rather than permanent sensitive user properties.

---

# 9. Privacy-safe analytics rules

## 9.1 Non-negotiable privacy constraints
The telemetry system must not collect:
- continuous background location traces,
- exact foreground route replay by default,
- raw medical profile contents,
- raw notes or journal entries,
- raw phrasebook user input,
- raw JWTs or auth tokens,
- raw store receipts,
- exact hidden personal identifiers unless required for a trusted operational reason and covered by a separate governed security document.

## 9.2 Map privacy rule
Map analytics must focus on product quality signals such as:
- route requested,
- route success/fail,
- positioning confidence state,
- floor selection frequency,
- fallback guidance activation,
- pack installed or missing,
- route completion coarse outcome if later supported.

It must not silently record detailed path traces by default.

## 9.3 Group privacy rule
Group instrumentation must describe coordination outcomes without exposing unnecessary relational detail.

Examples allowed:
- join success/fail,
- live board opened,
- check-in method used,
- regroup pin created/viewed/launched.

Examples forbidden by default:
- contact lists,
- exact recipient phone numbers,
- hidden member presence history exported into analytics,
- exact message bodies.

## 9.4 Ritual privacy rule
Ritual measurement may track progress and recovery patterns in aggregate, but care must be taken not to create humiliating or overly intrusive histories tied to identifiable users.

## 9.5 Retention rule
Raw event retention and detailed diagnostics retention must follow the project’s privacy and operational-retention policy. If retention changes, this file and the security/privacy file must both be updated.

---

# 10. Event priority tiers

## 10.1 Tier A — Must-have product truth
These events are mandatory for release-worthy instrumentation because they verify core user value.

Includes:
- app launch/session start
- screen root views for critical sections
- ritual start/resume/complete
- RIC start/result/action taken
- route preview start/result
- save anchor / recall anchor
- group join/check-in/regroup flows
- phrasebook/emergency usage
- pack discovery/download/install/failure
- entitlement restore/validate/upgrade outcomes

## 10.2 Tier B — Strongly recommended quality signals
These help diagnose friction and degradation.

Includes:
- offline fallback entry
- cache stale usage
- retry usage
- permission-denied states
- pack repair flows
- map confidence degradation
- screen render budget breaches

## 10.3 Tier C — Nice-to-have optimization signals
These are lower priority and may be sampled more aggressively.

Includes:
- secondary settings exploration
- component-level micro-interactions
- non-critical content impressions

## 10.4 Sampling rule
Tier A events should be unsampled except where platform costs force a governed exception.
Tier B may be lightly sampled if event volume becomes problematic.
Tier C may be more aggressively sampled.

---

# 11. Canonical feature event map

## 11.1 App and session events
- `app_launch_start`
- `app_launch_complete`
- `app_launch_fail`
- `session_start`
- `session_end`
- `session_restore_from_background`
- `session_offline_start`

## 11.2 Screen events
Each critical screen root should emit:
- `screen_<screen_id>_view`
- `screen_<screen_id>_empty`
- `screen_<screen_id>_error`
- `screen_<screen_id>_offline`
- `screen_<screen_id>_degrade`

At minimum for:
- home
- rituals_root
- ritual_step_detail
- ric_result
- map_root
- route_preview
- active_wayfinding
- group_root
- join_group
- pack_catalog
- settings_root
- phrasebook_root
- emergency_root

## 11.3 Rituals and RIC events
- `ritual_session_start`
- `ritual_session_resume`
- `ritual_step_view`
- `ritual_step_complete`
- `ritual_bookmark_save`
- `ritual_audio_play`
- `ritual_audio_unavailable`
- `ric_start`
- `ric_question_answered`
- `ric_result_view`
- `ric_result_classified`
- `ric_remedy_open`
- `ric_remedy_saved_to_wallet`

### Required ritual parameters where relevant
- `mode`
- `path`
- `madhhab`
- `step_id`
- `result_status`
- `offline_capable`
- `content_version`

## 11.4 Map and wayfinding events
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

### Required map parameters where relevant
- `position_confidence_state`
- `pack_state`
- `route_mode`
- `graph_version`
- `fallback_type`
- `permission_state_location`
- `permission_state_bluetooth`

## 11.5 Group events
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

### Required group parameters where relevant
- `role`
- `checkin_method`
- `live_board_enabled`
- `regroup_pin_state`
- `network_state`

## 11.6 Planner, notes, bookmarks, wallet events
- `planner_item_create`
- `planner_item_complete`
- `planner_item_delete`
- `planner_suggestion_view`
- `wallet_item_create`
- `wallet_item_open`
- `wallet_export_start`
- `notes_item_create`
- `bookmark_create`

## 11.7 Phrasebook and emergency events
- `phrasebook_root_view`
- `phrasebook_phrase_view`
- `phrasebook_audio_play`
- `phrasebook_big_text_open`
- `emergency_root_view`
- `emergency_card_open`
- `emergency_sms_template_use`
- `medical_profile_view_local`
- `medical_profile_export`

## 11.8 Packs and offline-distribution events
- `pack_catalog_view`
- `pack_detail_view`
- `pack_download_queue`
- `pack_download_start`
- `pack_download_progress_checkpoint`
- `pack_download_pause`
- `pack_download_resume`
- `pack_download_fail`
- `pack_download_repair`
- `pack_install_complete`
- `pack_purge_complete`
- `pack_auto_download_opt_in`

### Required pack parameters where relevant
- `pack_id`
- `pack_type`
- `pack_version`
- `download_network_type`
- `wifi_only_enabled`
- `failure_code`
- `bytes_downloaded`
- `duration_ms`

## 11.9 Entitlement and settings events
- `entitlement_snapshot_refresh`
- `entitlement_restore_start`
- `entitlement_restore_complete`
- `entitlement_restore_fail`
- `entitlement_upgrade_view`
- `entitlement_upgrade_start`
- `entitlement_upgrade_complete`
- `entitlement_upgrade_fail`
- `settings_preference_change`

---

# 12. Journey and funnel definitions

## 12.1 Principle
Funnels must reflect meaningful user outcomes, not just screen-to-screen clicks.

## 12.2 Core funnel A — First successful ritual guidance use
Stages:
1. `screen_home_view`
2. `ritual_session_start`
3. `ritual_step_view`
4. `ritual_step_complete`
5. `ritual_session_complete` or stable continuation milestone

## 12.3 Core funnel B — Recovery using RIC
Stages:
1. `ric_start`
2. `ric_question_answered`
3. `ric_result_view`
4. `ric_remedy_open`
5. optional `ric_remedy_saved_to_wallet`

## 12.4 Core funnel C — Orientation and map recovery
Stages:
1. `map_root_view`
2. `map_destination_select`
3. `map_route_preview_complete`
4. `map_route_follow_start`
5. success or fallback outcome marker

## 12.5 Core funnel D — Save My Gate / anchor recovery
Stages:
1. `map_anchor_save`
2. later `map_anchor_recall`
3. optional `map_route_follow_start`

## 12.6 Core funnel E — Group join and check-in
Stages:
1. `group_join_start`
2. `group_join_complete`
3. `group_checkin_start`
4. `group_checkin_complete` or `group_checkin_fallback_sms`

## 12.7 Core funnel F — Supporter pack adoption
Stages:
1. `pack_catalog_view`
2. `pack_detail_view`
3. `entitlement_upgrade_view` or existing supporter state
4. `pack_download_start`
5. `pack_install_complete`

## 12.8 Funnel segmentation rules
Funnels should be segmentable by:
- season,
- online vs offline context,
- simple mode enabled,
- locale,
- platform,
- entitlement tier,
- first-time vs returning usage where available,
- pack installed vs not installed.

---

# 13. Error taxonomy

## 13.1 Purpose
Every important failure should map to a canonical error taxonomy so dashboards, alerts, QA evidence, and support investigation stay consistent.

## 13.2 Top-level error classes
- `NETWORK`
- `AUTH`
- `AUTHORIZATION`
- `VALIDATION`
- `RATE_LIMIT`
- `SERVER`
- `CACHE`
- `STORAGE`
- `PACK_INTEGRITY`
- `PACK_SPACE`
- `PACK_DELIVERY`
- `LOCATION_PERMISSION`
- `BLUETOOTH_PERMISSION`
- `POSITIONING_UNAVAILABLE`
- `ROUTING_UNAVAILABLE`
- `CONTENT_MISSING`
- `CONTENT_VERSION_MISMATCH`
- `ENTITLEMENT_STALE`
- `PURCHASE_VALIDATION`
- `UI_RENDER`
- `UNKNOWN`

## 13.3 Failure-code rule
Analytics events may include `failure_code`, but this must use a documented enum or code set, not raw exception messages.

## 13.4 Cross-layer mapping rule
Where possible, client and backend errors should map into the same canonical taxonomy even if the native platform or vendor SDK uses different source terminology.

---

# 14. Logging strategy

## 14.1 Log classes
The system uses three different log classes:
- **product analytics events**,
- **structured diagnostic logs**,
- **security/audit logs** where required by trusted operations.

## 14.2 Structured logging rule
All backend logs and important client diagnostic logs must be structured, machine-readable, and field-based.

## 14.3 Log levels
Use canonical levels:
- `DEBUG`
- `INFO`
- `WARN`
- `ERROR`
- `FATAL`

## 14.4 Client logging rule
Client logs must be useful in development and controlled in production.

Production rules:
- avoid verbose noisy logs,
- redact sensitive content,
- preserve request IDs and compact failure metadata,
- never require logs for core UX to function.

## 14.5 Backend logging rule
Backend logs must always include:
- `timestamp`
- `request_id`
- `path`
- `method`
- `status_code`
- `latency_ms`
- `release_version`
- `environment`

Where relevant also include:
- `etag_hit`
- `auth_state`
- `rate_limited`
- `error_code`
- `upstream_dependency`

## 14.6 Redaction rule
The following must be redacted or excluded from logs by default:
- auth tokens,
- raw receipt payloads,
- medical profile content,
- exact user-entered notes,
- precise hidden locations,
- full phone numbers or emails.

---

# 15. Crash and non-fatal reporting strategy

## 15.1 Fatal crash capture
The mobile app must capture fatal crashes with:
- app version,
- build number,
- platform and OS version,
- device class,
- last known screen,
- session ID,
- correlation context where available.

## 15.2 Non-fatal capture
Capture non-fatal errors for:
- repeated network failures in critical flows,
- pack verification failures,
- unexpected parsing failures,
- map runtime exceptions,
- entitlement restore anomalies,
- screen render or state-machine failures that do not crash immediately.

## 15.3 Priority rule
Critical non-fatal issues in ritual, map recovery, group coordination, pack installation, and emergency flows must be surfaced with higher alerting priority than cosmetic non-fatals.

## 15.4 Deduplication rule
Crash and non-fatal tools must support fingerprinting or grouping so the team is not overwhelmed by repeated identical reports.

## 15.5 Release association rule
Every crash and non-fatal report must be attributable to a release and environment.

---

# 16. Tracing and cross-system diagnostics

## 16.1 Purpose
Tracing exists to connect user-visible slowness or failure with the backend or runtime path that caused it.

## 16.2 When tracing is required
Tracing or equivalent correlation is required for:
- app startup spans,
- flags fetch,
- pack manifest fetch,
- group join,
- group check-in,
- purchase validate/restore,
- pack install flow,
- route preview generation if backend or pack lookup is involved.

## 16.3 Span naming rule
Spans use `snake_case` and describe the operation, for example:
- `startup_bootstrap`
- `flags_fetch`
- `manifest_fetch`
- `group_join_request`
- `purchase_restore_request`
- `pack_checksum_verify`

## 16.4 Sampling rule
Tracing may be sampled, but critical failures and slow traces above the threshold should be retained preferentially.

---

# 17. Backend observability requirements

## 17.1 Minimum metrics by endpoint family
### Control-plane reads
For `/flags` and `/packs/manifest`, record:
- request count,
- 2xx/3xx/4xx/5xx counts,
- p50/p95/p99 latency,
- cache hit ratio or `etag_hit` ratio,
- upstream error rate.

### Authenticated reads/writes
For entitlements, join, check-in, regroup, and purchases, record:
- success count,
- failure count by canonical error code,
- auth failures,
- rate-limit hits,
- p50/p95/p99 latency,
- idempotency replay count where applicable.

## 17.2 Required backend event hooks
The server must emit or derive at minimum:
- `api_flags_200`
- `api_manifest_200`
- `api_entitlements_200`
- `api_group_join_200`
- `api_group_checkin_204`
- `api_regroup_pin_201`
- `api_purchase_validate_200`
- `api_4xx`
- `api_5xx`

## 17.3 Dependency health metrics
The system must surface dependency health for:
- edge runtime availability,
- database connectivity and latency,
- realtime health if enabled,
- pack storage or CDN errors,
- store validation provider failures where applicable.

## 17.4 Abuse and safety metrics
Track at minimum:
- join-code invalid attempts,
- rate-limit hit volume,
- repeated purchase-restore failures,
- repeated manifest or checksum failures,
- unusual spikes in 401/403/429/5xx responses.

---

# 18. Alerting model

## 18.1 Alert philosophy
Alerts must be meaningful, actionable, and few enough that people trust them.

## 18.2 P0 immediate alerts
Trigger immediate operational alerting for:
- crash-free sessions below release threshold,
- backend 5xx spike beyond threshold,
- purchase validate/restore widespread failure,
- pack checksum failure spike,
- group join failure spike,
- emergency-root crash or severe broken flow detection,
- map route-preview failure spike in supported areas.

## 18.3 P1 urgent but not paging-level alerts
Trigger urgent review for:
- startup p95 budget breach,
- route preview latency budget breach,
- manifest fetch error-rate increase,
- pack install success-rate drop,
- ANR/hang trend regression,
- frozen-frame trend regression,
- LMK or memory termination spike.

## 18.4 P2 monitoring alerts
Trigger review during working hours for:
- degraded fallback usage increase,
- entitlement snapshot staleness increase,
- copy or content version mismatch warnings,
- non-critical screen render budget drift.

## 18.5 Alert ownership rule
Every alert must have:
- an owner role,
- a severity,
- a runbook link,
- a threshold definition,
- a suppression/escalation rule,
- a known dashboard or query source.

---

# 19. Mobile performance budget philosophy

## 19.1 Goal
The app must feel calm, responsive, and trustworthy on the supported device range, especially during stressed, crowded, and low-connectivity usage.

## 19.2 Budget tiers
Performance budgets are expressed in three layers:
- **release target** — expected for general release readiness,
- **warning threshold** — triggers investigation,
- **fail threshold** — blocks release unless explicitly waived.

## 19.3 Supported-device rule
Budgets must be evaluated on the supported minimum and representative mid-tier devices, not only on high-end development hardware.

## 19.4 Feature-priority rule
Critical tasks such as startup, rituals, map recovery, emergency access, and pack install feedback must receive stronger budget enforcement than secondary surfaces.

---

# 20. App startup and first-frame budgets

## 20.1 Startup definitions
- **cold start:** app launched from a not-running state.
- **warm start:** app resumed after partial process retention.
- **hot resume:** app returned from background with process intact.

## 20.2 Release targets
### Cold start
- p50 ≤ **1.8 s**
- p95 ≤ **2.8 s**
- fail threshold: p95 > **3.5 s**

### Warm start
- p50 ≤ **1.0 s**
- p95 ≤ **1.8 s**
- fail threshold: p95 > **2.3 s**

### Hot resume
- p50 ≤ **450 ms**
- p95 ≤ **900 ms**
- fail threshold: p95 > **1.2 s**

## 20.3 Startup rule
The first meaningful frame for critical surfaces must not wait on non-essential network calls.

## 20.4 Startup instrumentation
Track at minimum:
- app bootstrap duration,
- first frame duration,
- home-ready duration,
- flags fetch overlap,
- local cache readiness,
- expensive startup work categories.

---

# 21. Screen rendering and interaction budgets

## 21.1 General screen transition targets
For critical screens:
- screen data-ready p50 ≤ **500 ms** from local-first sources where data is already available,
- screen data-ready p95 ≤ **900 ms**,
- fail threshold: p95 > **1.4 s** except where documented pack or network dependencies legitimately apply.

## 21.2 Scroll and interaction targets
The app should avoid persistent visible jank in core flows.

Operational targets:
- no repeated frozen frames in normal critical-path usage,
- severe jank on critical screens must be treated as a release-quality failure,
- interaction-to-visible-response for simple local actions should generally remain ≤ **100 ms** and not exceed **200 ms** in p95 conditions.

## 21.3 Ritual screen budgets
- Ritual step detail open p50 ≤ **350 ms**
- Ritual step detail open p95 ≤ **700 ms**
- fail threshold: p95 > **1.0 s**

## 21.4 Phrasebook and emergency budgets
- emergency root open p95 ≤ **500 ms**
- emergency card open p95 ≤ **350 ms**
- fail threshold for emergency root: p95 > **800 ms**

## 21.5 Group screen budgets
- group root open p95 ≤ **900 ms** with cached state
- check-in button feedback ≤ **150 ms** locally
- fallback SMS/action sheet presentation p95 ≤ **300 ms**

---

# 22. Map and wayfinding performance budgets

## 22.1 Relationship to file 16
File `16` defines the map architecture and the initial expectations. This file turns those expectations into enforceable quality budgets.

## 22.2 Route preview targets
- route preview render after request p50 ≤ **900 ms** with local data ready
- route preview render after request p95 ≤ **1.5 s**
- fail threshold: p95 > **2.2 s** on supported devices

## 22.3 Active map usability targets
- basic pan/zoom must remain visually responsive without persistent severe frame drops,
- map control tap response p95 ≤ **150 ms**,
- floor-switch response p95 ≤ **400 ms**,
- fail threshold: repeated visible frozen interactions during supported map usage.

## 22.4 Pack-open targets
- installed offline map pack to usable first frame p95 ≤ **2.0 s** in previously warmed contexts,
- fail threshold: p95 > **3.0 s**.

## 22.5 Degradation rule
If map budgets are threatened, the system must prefer:
1. reducing visual effects,
2. reducing 3D fidelity,
3. falling back to 2D,
4. falling back to text and anchor guidance.

## 22.6 Map memory rule
The map runtime must not assume unlimited memory. Repeated map usage must be monitored for memory growth and low-memory kill risk.

---

# 23. Network budgets

## 23.1 General principle
The app must remain useful under weak connectivity, so network usage should be efficient, cache-aware, and never block essential offline value.

## 23.2 Read endpoint targets
### `/flags`
- p95 edge latency target ≤ **200 ms**
- fail threshold: p95 > **350 ms** for sustained periods

### `/packs/manifest`
- p95 edge latency target ≤ **350 ms**
- fail threshold: p95 > **600 ms** for sustained periods

## 23.3 Authenticated endpoint targets
### group join
- p95 ≤ **800 ms**
- fail threshold: p95 > **1.5 s**

### check-in
- p95 ≤ **600 ms**
- fail threshold: p95 > **1.2 s**

### entitlement refresh
- p95 ≤ **700 ms**
- fail threshold: p95 > **1.3 s**

### purchase validate/restore
- p95 ≤ **1.8 s**
- fail threshold: p95 > **3.0 s**

## 23.4 Request-size rule
Telemetry and API payloads should remain compact. Avoid oversized request bodies for ordinary user actions.

## 23.5 Retry rule
Critical network flows may retry according to API-contract rules, but retries must be observable and must not create hidden repeated writes or silent UI stalls.

---

# 24. Memory, battery, and storage budgets

## 24.1 Memory philosophy
Memory regressions matter even when they do not crash immediately. They can cause low-memory kills, bad multitasking behavior, and degraded map performance.

## 24.2 Memory targets
### General app runtime
- no sustained unexplained memory growth during repeated navigation of critical flows,
- release review required if memory footprint regresses by more than **15%** on representative scenarios without an approved reason,
- fail threshold if repeated low-memory termination evidence appears on supported devices for normal core journeys.

### Map-heavy scenarios
- memory profiling is mandatory for route preview, active wayfinding, floor switching, and 3D scene use,
- fail threshold if supported mid-tier devices cannot complete supported map journeys without frequent recoverable or unrecoverable memory pressure.

## 24.3 Battery rule
The app must avoid hidden continuous background activity, abusive wake usage, or unnecessary sensor usage.

### Battery alert triggers
Investigate when there is evidence of:
- excessive wake usage,
- repeated background work without user value,
- map or sensor flows that remain active after exit,
- significant battery regressions between releases on comparable scenarios.

## 24.4 Storage rule
The base app and installed packs must remain within documented size budgets and avoid uncontrolled cache growth.

---

# 25. Asset size budgets

## 25.1 Base app size budget
The base mobile app remains subject to the project-level target of **≤ 60 MB** for the core app footprint.

## 25.2 Pack budgets
Packs remain governed by the pack-policy file, but telemetry must monitor:
- download size,
- install size,
- repair frequency,
- purge frequency,
- failure rate by pack type and version.

## 25.3 Regression rule
Any size increase in the base app or a major pack class must be called out in release evidence and investigated if it materially harms startup, storage pressure, or install success.

---

# 26. Offline and sync observability

## 26.1 Why it matters
Offline-first products can appear healthy in cloud dashboards while failing users locally. Therefore degraded local behavior must be explicitly observable.

## 26.2 Required offline/degradation signals
Track when relevant:
- cached flags used,
- cached manifest used,
- offline queue length buckets,
- sync flush success/fail,
- stale entitlement snapshot shown,
- pack unavailable but fallback used,
- route unavailable but text guidance used,
- group live board unavailable but SMS/manual path used.

## 26.3 Queue health metrics
The client should surface aggregate signals for:
- queued event count buckets,
- oldest queued event age buckets,
- flush success rate,
- flush retry rate,
- dropped event count by priority tier.

## 26.4 Staleness rule
The UI and telemetry should both reflect when cached or stale data is being used in a meaningful user flow.

---

# 27. Release dashboards

## 27.1 Minimum release-readiness dashboard
A release-readiness dashboard must combine at minimum:
- crash-free sessions,
- non-fatal trend for critical flows,
- startup p50/p95,
- frozen-frame or hang trend,
- low-memory termination trend where available,
- flags and manifest latency/error rate,
- group join success rate,
- group check-in success rate,
- route preview success rate,
- pack install success rate,
- purchase validate/restore success rate,
- fallback/degradation trend for critical journeys.

## 27.2 Feature dashboards
The project should maintain dedicated dashboards for:
- rituals and RIC,
- maps and wayfinding,
- group coordination,
- packs and asset delivery,
- entitlements and purchases,
- emergency and phrasebook usage,
- accessibility and simple-mode adoption.

## 27.3 Accessibility visibility rule
Dashboards should make it possible to compare quality outcomes for cohorts such as large text, screen reader usage, and simple mode without exposing sensitive personal data.

---

# 28. Alert thresholds and service-level targets

## 28.1 Mobile quality targets
- crash-free sessions target: **≥ 99.7%**
- warning threshold: **< 99.5%**
- fail threshold: **< 99.3%**

## 28.2 Critical journey success targets
### group join success
- target: **≥ 99.0%** excluding explicit validation/user-input mistakes
- warning threshold: **< 98.0%**
- fail threshold: **< 97.0%**

### pack install completion after download start
- target: **≥ 98.0%** on supported storage/network conditions
- warning threshold: **< 96.0%**
- fail threshold: **< 94.0%**

### route preview success in supported conditions
- target: **≥ 98.0%**
- warning threshold: **< 96.0%**
- fail threshold: **< 94.0%**

### entitlement restore success
- target: **≥ 98.5%** excluding invalid account/store states
- warning threshold: **< 97.0%**
- fail threshold: **< 95.0%**

## 28.3 Backend availability targets
For the app’s core public and authenticated control-plane endpoints, the operational target should remain high enough that users rarely notice service degradation. Exact SLO reporting may be maintained in operations tooling, but release review must treat sustained spikes in 5xxs or latency breaches as quality failures.

---

# 29. Instrumentation governance rules

## 29.1 Shared schema registry rule
Analytics events, parameters, enums, and dashboards must be defined in a shared registry or equivalent governed source, not scattered across feature files and code comments.

## 29.2 Change discipline
When adding or changing instrumentation:
- update this file if the taxonomy or common contract changes,
- update affected feature file(s),
- update dashboards/queries,
- update test fixtures or validation where relevant,
- record material changes in the roadmap/changelog file.

## 29.3 No speculative instrumentation
Do not add broad event spam “just in case it helps later.” Every event should answer a product, quality, or operational question.

## 29.4 Review requirement
New Tier A instrumentation, new sensitive fields, or new cohort properties require review by product and engineering ownership, and privacy/security review where appropriate.

---

# 30. Testing and validation requirements for telemetry

## 30.1 Required automated checks
Instrumentation code should be validated for:
- event name correctness,
- parameter presence and typing,
- forbidden-field absence,
- queue behavior,
- retry behavior,
- dedupe or idempotency where expected,
- log redaction,
- trace correlation propagation.

## 30.2 Required manual checks
Before a release candidate is approved, verify on device:
- startup metrics are captured,
- crash and non-fatal tagging include release metadata,
- core funnels fire once and with correct parameters,
- offline events queue and flush later,
- fallback events appear when degradation paths are used,
- no sensitive payload leakage appears in logs or dashboards,
- map and pack instrumentation reflect real behavior under degraded conditions.

## 30.3 QA evidence rule
Release evidence should include representative dashboard snapshots or exported metrics for:
- startup,
- crash quality,
- core journey success,
- pack flows,
- route preview,
- offline/fallback behavior.

---

# 31. Cross-file dependency rules

## 31.1 If a new feature file introduces a major journey
Update:
- this file’s feature event map,
- the relevant feature-family spec,
- testing and release-evidence files.

## 31.2 If a data enum used in telemetry changes
Update:
- this file,
- data model doc,
- API doc if exposed,
- dashboards and queries,
- fixtures and tests.

## 31.3 If a performance budget changes
Update:
- this file,
- any feature file that references the budget,
- testing and release-gate files,
- operations dashboard thresholds if applicable.

## 31.4 If a privacy boundary changes
Update:
- this file,
- security/privacy file,
- affected feature files,
- instrumentation code and redaction tests.

---

# 32. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved:

## 32.1 Logging raw sensitive payloads
Forbidden.

## 32.2 Continuous hidden location analytics by default
Forbidden.

## 32.3 Vendor SDK calls scattered across feature widgets
Forbidden.

## 32.4 Using analytics events as a substitute for proper error handling
Forbidden.

## 32.5 Shipping budget regressions without documented acknowledgement
Forbidden.

## 32.6 Measuring vanity interactions while missing core journey truth
Forbidden.

## 32.7 Silent event renames or schema drift
Forbidden.

## 32.8 Requiring network success before recording locally knowable telemetry
Forbidden.

## 32.9 Treating crash-free rate alone as sufficient proof of quality
Forbidden.

## 32.10 Capturing freeform user text in analytics without explicit approval
Forbidden.

---

# 33. Implementation priorities

## 33.1 Phase 1 priorities
Implement first:
- shared telemetry interfaces,
- app/session/screen events,
- startup performance instrumentation,
- crash and non-fatal reporting,
- Tier A rituals/RIC/map/group/pack events,
- backend request metrics for existing endpoints,
- release-readiness dashboard skeleton.

## 33.2 Phase 2 priorities
Then add:
- degradation/fallback signals,
- richer pack diagnostics,
- route-preview and active-wayfinding performance traces,
- entitlement and restore funnel analysis,
- alerting automation.

## 33.3 Phase 3 priorities
Then refine:
- map 3D-specific performance signals,
- deeper battery and memory analysis,
- cohort-based quality views,
- targeted performance experiments if later approved.

---

# 34. When this file must be updated

This file must be updated whenever any of the following changes:
- analytics taxonomy,
- event naming rules,
- common telemetry envelope,
- user-property policy,
- privacy-safe measurement boundaries,
- crash/error reporting strategy,
- backend observability strategy,
- alert thresholds,
- startup or rendering budgets,
- map or pack performance budgets,
- release evidence expectations tied to telemetry.

If those truths change but this file is not updated, dashboards, instrumentation, QA, and release decisions will drift quickly.

---

# 35. Summary

This file defines how Pilgrims Mobile App measures reality.

It establishes:
- a governed analytics taxonomy,
- privacy-safe telemetry boundaries,
- shared event and parameter contracts,
- crash and non-fatal reporting expectations,
- backend observability requirements,
- alerting thresholds,
- startup, rendering, network, memory, battery, map, and asset-size budgets,
- the cross-file update rules needed to keep quality measurement coherent.

The goal is not to collect more data than necessary.
The goal is to ensure the app remains calm, reliable, ethical, and fast in the real conditions pilgrims actually face.

