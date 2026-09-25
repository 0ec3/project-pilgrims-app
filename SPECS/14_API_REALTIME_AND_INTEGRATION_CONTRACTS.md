# 14 — API, REALTIME, AND INTEGRATION CONTRACTS

## Document status
- **Type:** Normative service contract specification
- **Priority:** Highest
- **Audience:** Backend engineer, Flutter engineer, QA, AI agents, release/ops
- **Purpose:** Define HTTP API endpoints, realtime contracts, integration boundaries, request/response shapes, caching, auth, errors, and contract-testing expectations.
- **Last-updated-by:** AI-assisted governance/contract hardening pass (2026-06-12)
- **Related files:** `06`, `07`, `13`, `15`, `17`, `20`, `23`, `24`, `26`, `27`, `28`, `29`, `30`, `31`, `SPECS/CONTRACTS/*`

---

# 1. Scope

This file governs the online service surface used by the mobile app.

It defines:
- endpoint catalog,
- auth requirements,
- request/response shapes,
- caching and ETag behavior,
- realtime channels,
- idempotency,
- retry behavior,
- error envelopes,
- integration boundaries,
- contract-testing expectations.

This file does **not** define:
- full database schema (file `13`),
- app architecture (file `07`),
- offline cache rules in full detail (file `15`),
- observability dashboards (file `17`),
- operational rollout and incidents (file `30`).

---

# 2. API design principles

## 2.1 Tiny online surface rule
The online API should stay small. The app must not become dependent on a large server backend for core local-first value.

## 2.2 Local-first default
The API supports entitlements, group coordination, pack manifest discovery, safety/config flags, purchase validation, selected privacy/account actions, and selected publishing/control-plane functions.

It should not become the default home for notes, medical profile, ritual progress, saved anchors, local planner data, or private user-authored content.

## 2.3 Explicit trust boundary rule
If a feature needs trusted server authority, the API must clearly define that trust boundary.

Examples:
- entitlement state,
- group membership,
- group leader permissions,
- purchase validation,
- deletion/export request status,
- release flags.

## 2.4 No hidden generic content API
Governed content should not be served by an undefined generic live API. Governed content distribution must follow files `15`, `23`, and `26`.

## 2.5 Contract-first rule
Mobile code, backend handlers, and tests must agree on the contract.

Do not silently change endpoint paths, enums, error codes, field names, auth rules, cache behavior, realtime event payloads, or contract artifact semantics.

---

# 3. Runtime zones and API ownership

## 3.1 Edge API
The primary public service boundary is an Edge API layer, conceptually represented by Cloudflare Workers or equivalent.

Responsibilities:
- validate JWTs where required,
- enforce API-level authorization,
- normalize request/response shape,
- apply rate limits,
- proxy or coordinate with database and store validation services,
- expose tiny control-plane endpoints.

## 3.2 Supabase / database boundary
The database remains the source of truth for server-backed domain data. The API must not bypass RLS assumptions casually.

## 3.3 External integrations
External integrations may include Apple / Google purchase validation, CDN/R2 pack delivery, crash/analytics ingestion, and platform notification APIs for local behavior only where applicable.

---

# 4. Canonical endpoint catalog

## 4.1 Public read endpoints
### `GET /v1/flags`
Returns current lightweight control-plane config.

### `GET /v1/packs/manifest`
Returns the current manifest of downloadable packs and pack metadata.

## 4.2 Authenticated read endpoints
### `GET /v1/entitlements`
Returns the current trusted entitlement snapshot for the authenticated user.

### `GET /v1/groups/{group_id}/live-board`
Optional authenticated read for current group live-board snapshot when feature and entitlement permit it.

### `GET /v1/groups/{group_id}/regroup-pins`
Returns current active regroup pins for a group the user belongs to.

### `GET /v1/groups/{group_id}/itinerary`
Returns current itinerary payloads for a group the user belongs to.

## 4.3 Authenticated write endpoints
### `POST /v1/groups`
Create a governed group and assign the requester as the initial active `LEADER`.

Rules:
- Auth required.
- `Idempotency-Key` required.
- Server generates the canonical 6-character uppercase alphanumeric join code.
- Server writes both `groups` and initial `group_members` state transactionally.
- The client must not invent leader state locally.
- Rate limiting and abuse checks are mandatory.
- Offline clients must show honest unavailable state and must not queue hidden group creation.

### `POST /v1/groups/join`
Join a group by join code. Must be authenticated, idempotent, rate-limited, and server-authoritative.

### `POST /v1/groups/{group_id}/checkins`
Create a group check-in. Must follow `SPECS/CONTRACTS/group_presence_privacy_contract.yaml` where presence semantics apply.

### `POST /v1/groups/{group_id}/regroup-pins`
Create a regroup pin. Leader-only.

### `PATCH /v1/groups/{group_id}/regroup-pins/{pin_id}`
Update or deactivate a regroup pin. Leader-only.

## 4.4 Purchase endpoints
### `POST /v1/purchases/validate`
Validate a purchase payload or transaction reference from the client and return updated entitlement state.

### `POST /v1/purchases/restore`
Trigger restore lookup and return current trusted entitlement state.

## 4.5 Privacy and account data endpoints
### `POST /v1/account/deletion-request`
Request deletion of server-backed account data, subject to lawful retention, purchase/accounting needs, fraud-prevention needs, backup delay, and legal hold constraints.

Rules:
- Auth required.
- `Idempotency-Key` required.
- Rate limit: 3 requests/day/user.
- Must return a deletion request identifier and status.
- Must not claim immediate deletion when backup delay, fraud/accounting retention, or legal hold applies.
- Must not delete local-only data; the client must offer separate local data deletion.

### `GET /v1/account/deletion-status`
Return the current status of an authenticated deletion request.

Rules:
- Auth required.
- Rate limit: 30 requests/hour/user.
- Must expose user-readable status and any lawful retention caveat.
- Must not expose internal legal, abuse, or operational details beyond user-safe explanation.

### `POST /v1/privacy/export-request`
Request an explicit, scoped export of server-backed personal data where applicable.

Rules:
- Auth required.
- `Idempotency-Key` required.
- Rate limit: 5 requests/day/user.
- Must return an export request identifier and status.
- Must clearly distinguish server-backed export from local-only data that never left the device.

### `GET /v1/privacy/retention-summary`
Return a user-readable summary of server-backed data categories, default retention posture, and local-only data boundaries.

Rules:
- Auth required when returning account-specific summary.
- Rate limit: 30 requests/hour/user.
- Must be safe for direct display in the Privacy & Data flow.

## 4.6 Optional future endpoints (not active by default)
These must not be implemented unless approved and documented.
- `PATCH /v1/groups/{group_id}`
- `POST /v1/groups/{group_id}/itinerary`
- `PATCH /v1/groups/{group_id}/itinerary/{day}`
- `GET /v1/groups/{group_id}/presence`
- `POST /v1/official-handoff/resolve`

---

# 5. Base protocol rules

- HTTPS only.
- JSON request and response bodies unless explicitly documented otherwise.
- UTF-8 encoding.
- All endpoints must be version-prefixed with `/v1/...`.
- Requests use `Content-Type: application/json`.
- Responses use `Content-Type: application/json; charset=utf-8`.
- All server timestamps must use RFC 3339 / ISO 8601 UTC timestamps.
- JSON field names use `snake_case`.
- Clients must ignore unknown response fields unless the endpoint contract explicitly forbids it.
- Servers must reject unknown dangerous request fields where accepting them would create privilege, privacy, or integrity ambiguity.

---

# 6. Authentication and authorization

Authenticated endpoints require a valid user identity token.

The API layer validates:
- token presence,
- token signature / provider validity,
- expiry,
- user identity binding.

Public endpoints:
- `GET /v1/flags`
- `GET /v1/packs/manifest`

Authenticated endpoints include:
- entitlements,
- group reads/writes,
- purchase validation/restore,
- account/privacy data requests.

Authorization must validate:
- user can read the requested group,
- user can write to the requested group,
- user is leader where leader-only action is required,
- user can access the requested entitlement state,
- user can request deletion/export only for their own account context.

The client must not be trusted for membership, leader role, entitlement tier, purchase validity, or server-side deletion/export status.

---

# 7. Standard response envelopes and error codes

Small endpoints may return direct JSON objects. List-like endpoints should use:

```json
{
  "data": [],
  "meta": {
    "server_time": "2026-06-12T00:00:00Z"
  }
}
```

All API errors should follow:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-friendly summary",
    "fields": [
      {"path": "field_name", "issue": "explanation"}
    ],
    "request_id": "req_..."
  }
}
```

Canonical error codes:
- `VALIDATION_ERROR`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `NOT_FOUND`
- `CONFLICT`
- `RATE_LIMITED`
- `PRECONDITION_FAILED`
- `INTEGRATION_ERROR`
- `INTERNAL_ERROR`

Error messages should avoid exposing database internals, provider raw messages, secrets, receipt payloads, raw auth failures, or sensitive operational detail.

---

# 8. Request IDs and traceability

Every API response should include or be associated with a request ID through a response header, body error field, or structured log correlation value.

Clients may log request IDs for diagnostics.

Clients must not log raw tokens, raw receipts, medical profile content, exact private location, personal notes, or ritual-sensitive private user notes.

---

# 9. Rate limiting rules

## 9.1 Goals
Rate limiting protects edge capacity, abuse-sensitive flows, store-validation endpoints, join-code brute forcing, privacy/account actions, and accidental client retry storms.

## 9.2 Baseline limits
Initial contract-level defaults:
- `GET /v1/flags` → 60 requests/minute/IP
- `GET /v1/packs/manifest` → 30 requests/minute/IP
- `GET /v1/entitlements` → 30 requests/minute/user
- `POST /v1/groups` → 3 requests/hour/user and stricter abuse detection where needed
- `POST /v1/groups/join` → 10 requests/minute/user
- `POST /v1/groups/{group_id}/checkins` → 30 requests/minute/user
- `POST /v1/groups/{group_id}/regroup-pins` → 15 requests/minute/user
- `PATCH /v1/groups/{group_id}/regroup-pins/{pin_id}` → 30 requests/minute/user
- `POST /v1/purchases/*` → 15 requests/minute/user
- `POST /v1/account/deletion-request` → 3 requests/day/user
- `GET /v1/account/deletion-status` → 30 requests/hour/user
- `POST /v1/privacy/export-request` → 5 requests/day/user
- `GET /v1/privacy/retention-summary` → 30 requests/hour/user

429 responses must include a retry hint and must not return HTML or provider-native error blobs.

---

# 10. Idempotency rules

## 10.1 Purpose
Idempotency is required where retries are likely and duplicate side effects would be harmful or confusing.

## 10.2 Required behavior
When the same authenticated principal sends the same idempotency key to the same endpoint within the retention window, the server must return the original logical result or a consistent duplicate-safe response.

## 10.3 Retention window
Default idempotency-key retention window:
- 24 hours for group creation, group join, group check-in where `client_event_id` is supplied, and purchase endpoints.
- 30 days for account deletion requests and privacy export requests.

## 10.4 Endpoint rules
- `POST /v1/groups` must be idempotent.
- `POST /v1/groups/join` must be idempotent.
- `POST /v1/groups/{group_id}/checkins` must be idempotent when `client_event_id` is supplied.
- `POST /v1/purchases/validate` must be idempotent by store transaction identity and idempotency key where applicable.
- `POST /v1/purchases/restore` must be retry-safe.
- `POST /v1/account/deletion-request` must be idempotent and return the existing active deletion request if one exists.
- `POST /v1/privacy/export-request` must be idempotent and return the existing compatible export request if one exists.

---

# 11. Caching and ETag rules

Public cacheable endpoints:
- `GET /v1/flags` → recommended `Cache-Control: public, max-age=300`, ETag support, last-good cached snapshot offline.
- `GET /v1/packs/manifest` → recommended `Cache-Control: public, max-age=1800`, ETag support, last-known manifest offline with stale honesty.

User-specific endpoints must not be publicly cached. Examples include entitlements, group state, purchase responses, and account/privacy data responses.

If the client uses stale cached data, UI must distinguish fresh, cached but acceptable, stale/needs refresh, and unavailable.

---

# 12. Flags endpoint contract

`GET /v1/flags` provides lightweight control-plane state.

It may include season configuration, feature flags, safety banner pointers, content activation pointers, minimum app version hints, and kill-switch flags for unsafe optional features.

Flags must not contain user-private data, large content payloads, scholar-sensitive live ritual rules, executable logic, or raw secrets.

Flags may hide or disable unsafe optional features. Flags must not be used to remove baseline safety or correctness content.

---

# 13. Pack manifest contract

`GET /v1/packs/manifest` returns available downloadable packs.

Each pack entry should include:
- `pack_id`
- `version`
- `category`
- `locale`
- `season_scope`
- `title`
- `description`
- `size_bytes`
- `checksum_sha256`
- `artifact_url` or delivery reference
- `min_app_version`
- `entitlement_required?`
- `dependencies[]`

For mature release quality, manifest and artifact entries must align with `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`, including `manifest_signature`, `artifact_signature`, `signing_key_id`, `signed_at`, `signing_algorithm`, and revoked-key metadata where applicable.

The client must not hardcode pack URLs. Baseline safety/correctness packs must not be wrongly gated.

---

# 14. Entitlements endpoint contract

`GET /v1/entitlements` returns trusted entitlement state.

Example response:

```json
{
  "user_id": "uuid",
  "tier": "SUPPORTER",
  "source": "APPLE",
  "active_until": "2026-06-12T00:00:00Z",
  "gates": {
    "PACK_AUTO_DOWNLOAD": true,
    "AUDIO_OFFLINE": true,
    "GROUP_LIVE_BOARD": true,
    "SMART_PLANNER": true,
    "NOTES_BOOKMARKS_EXTENDED": true
  },
  "verified_at": "2026-06-12T00:00:00Z"
}
```

The client must not invent gates. Implementation must validate entitlement use against `SPECS/CONTRACTS/entitlement_capability_policy.yaml`. Supporter must never gate capabilities marked `never_gate`.

---

# 15. Group endpoint contracts

## 15.1 Live-board response
A group live-board response should include group summary, viewer role, members list or summary, latest check-ins, active regroup pins, freshness metadata, and entitlement availability if live board is gated.

## 15.2 Check-in request
Fields:
- `kind`
- `text_pin?` according to the group presence contract
- `client_event_id?`

Check-ins must not imply GPS tracking.

## 15.3 Regroup pin request
Fields:
- `label`
- `text_pin`
- `map_anchor_ref?`
- `expires_at?`

Leader-only.

## 15.4 Group creation request
Fields:
- `name`
- `season_scope?`
- `client_event_id?`

The server returns group id, group name, viewer role, generated join code, and share-code copy fields.

The server must not import contacts, auto-invite members, or create hidden social graph data.

## 15.5 Presence identifier mapping
When group presence events are represented through API payloads, `event_id` maps to the database primary key `id` in `group_presence_events` unless files `13`, `14`, and `SPECS/CONTRACTS/group_presence_privacy_contract.yaml` are updated together.

## 15.6 Freshness rule
Group responses must expose enough timestamp/freshness information for the client to avoid fake-live presentation.

## 15.7 Group presence privacy rule
Any normalized presence state must follow `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`.

---

# 16. Purchase endpoints

Purchase validation input may accept store platform, receipt/transaction reference, app account token where applicable, product identifier, and idempotency key.

Raw receipt payloads must be treated as sensitive operational data and must not be exposed to logs or analytics.

The mobile app should receive normalized entitlement state, not provider-native payloads as product truth.

---

# 17. Realtime contracts

Realtime is approved only for group coordination enhancement.

Realtime channels must validate authenticated user, active group membership, and role where needed.

Allowed group realtime event families:
- `group_checkin_created`
- `group_regroup_pin_created`
- `group_regroup_pin_updated`
- `group_member_updated`

Realtime must never be the only path to correctness. If realtime fails, the app should use manual refresh, cached snapshot with stale state, and SMS/share fallback where relevant.

---

# 18. Retry behavior

Clients may retry idempotent GETs, idempotent POSTs with idempotency key, and transient network failures.

Use exponential backoff or bounded retry policy for transient failures. The app must not retry aggressively in crowded weak-network contexts.

Respect rate-limit hints, network state, battery/performance concerns, and user stress.

---

# 19. Offline and degraded behavior

When offline:
- public cached data may fall back to last-good snapshots,
- entitlements may show cached continuity but not verified certainty,
- group protected writes must not pretend success,
- purchases/restores must show unavailable or pending explanation,
- account deletion/export requests must show unavailable until trusted server write is possible.

Offline errors should explain what still works, what needs network, whether data was saved locally, and whether trusted server action happened.

---

# 20. Contract testing

Contract tests must cover:
- schema fields,
- required/optional fields,
- auth requirements,
- authorization requirements,
- error envelopes,
- canonical error codes,
- cache headers,
- idempotency behavior,
- rate-limit responses,
- stale/offline behavior,
- privacy endpoint deletion/export semantics,
- group presence identifier mapping.

Mobile test fixtures must be generated from or checked against the canonical contract. Do not hand-maintain divergent mocks.

Breaking API changes require synchronized updates to this file, backend handlers, Flutter client models, fixtures, tests, analytics/dashboard expectations where relevant, release notes, and migration plan where user-visible.

---

# 21. Privacy and security rules

## 21.1 Data minimization
Endpoints must request and return only what the feature needs.

## 21.2 No sensitive data in URL rule
Do not put tokens, receipts, medical data, private notes, exact private coordinates, deletion request IDs, or export download tokens in URLs or query strings.

## 21.3 Log redaction rule
API logs must redact auth tokens, receipts, personal contact info where not needed, medical values, raw private text, precise location, deletion/export request details, and provider-native account identifiers beyond what is operationally necessary.

## 21.4 Account/privacy endpoint rule
Deletion, status, export, and retention endpoints must align with file `24` UX and file `29` retention/disclosure rules.

## 21.5 Audit trail rule
Deletion and export requests must record an internal audit event containing request id, authenticated user id, request class, server timestamp, result state, and request idempotency key hash. Audit events must not contain exported data payloads or raw user-private fields.

---

# 22. Observability requirements

Required API metrics:
- request count,
- latency,
- error rate,
- rate-limit count,
- auth failure count,
- integration failure count,
- stale fallback usage where client reports it,
- privacy/account request status distribution.

Critical endpoint alerts must cover abnormal failure for:
- `GET /v1/flags`
- `GET /v1/packs/manifest`
- `GET /v1/entitlements`
- `POST /v1/groups`
- `POST /v1/groups/join`
- `POST /v1/groups/{group_id}/checkins`
- `POST /v1/purchases/validate`
- `POST /v1/purchases/restore`
- `POST /v1/account/deletion-request`
- `GET /v1/account/deletion-status`
- `POST /v1/privacy/export-request`
- `GET /v1/privacy/retention-summary`

No telemetry payload should include raw receipts, raw JWTs, medical profile contents, exact hidden personal location, deletion/export payload details, or raw private notes.

---

# 23. Definition of done for this API system

This API system is ready when:
- endpoint catalog matches implementation,
- request/response schemas are documented,
- auth/authorization tests pass,
- RLS assumptions align with file `13`,
- contract fixtures exist for Flutter,
- error envelopes are stable,
- rate limits are implemented,
- idempotency works for required endpoints,
- stale/offline behavior is tested,
- entitlement capability policy is enforced,
- group presence privacy contract is honored,
- account/privacy endpoints match files `24` and `29`,
- deletion/export endpoints have idempotency, rate-limit, audit, and alert evidence,
- pack/content trust-chain fields are supported where applicable,
- observability is in place,
- release evidence links to file `28`.

---

# 24. AI-agent checklist

Before editing API-related code, an AI agent must:
1. Read files `13`, `14`, `24`, and `29`.
2. Read relevant feature-family file(s).
3. Check `SPECS/CONTRACTS/*` for affected machine-readable contracts.
4. Verify whether endpoint is public or authenticated.
5. Verify RLS and authorization assumptions.
6. Update contract tests and fixtures.
7. Avoid adding new endpoints without spec approval.
8. Document any breaking contract change.

# 18. Guide Marketplace API contract amendment

File `32` introduces a small online surface for a server-trusted optional feature. It does not change the local-first rule for essential pilgrimage value.

## 18.1 Public/current reads

### `GET /v1/guides`
Purpose: return only currently public-eligible guide/listing summaries, with approved fact-specific trust metadata.

Rules:
- public/guest access is allowed only if final legal/security review permits;
- response must not expose raw private contact targets or restricted credential evidence;
- cache policy must carry freshness sufficient to prevent stale "currently verified" claims;
- filters may cover approved language, service area, group-size, price, and precise trust types.

### `GET /v1/guides/{guide_id}`
Purpose: return current public profile/listing detail and approved trust/disclosure metadata.

Rules:
- ineligible/removed providers must not return as active due to stale application cache;
- no restricted credential/report/moderation fields;
- price/disclosure shape must support applicable Saudi requirements.

## 18.2 Provider application/profile/listing endpoints

### `POST /v1/guides/applications`
- Auth required.
- Network required.
- `Idempotency-Key` required.
- Strict abuse/rate limits.
- Server creates trusted application state; client cannot choose verification outcome.

### `GET /v1/guides/me/application`
- Auth required.
- Returns the caller's current trusted application/provider status with explicit freshness.

### `PATCH /v1/guides/me/profile`
- Auth required.
- Updates only provider self-service fields.
- Must reject attempts to write verification/moderation/public-eligibility fields.

### `POST /v1/guides/me/listings`
- Auth required.
- `Idempotency-Key` required.
- Creates a draft/reviewable listing only for approved service types.

### `PATCH /v1/guides/me/listings/{listing_id}`
- Auth required.
- Provider must own the listing.
- Must not bypass required re-review or reactivate an ineligible provider.

## 18.3 Contact and report endpoints

### `POST /v1/guides/{guide_id}/contact-intent`
Purpose: resolve an explicit user-selected contact handoff without creating a booking.

Rules:
- rate-limited and abuse-sensitive;
- auth policy must be finalized by privacy/abuse review;
- must re-check current provider/listing eligibility at request time;
- returns only an approved current channel/target or safe handoff payload;
- does not auto-message, disclose pilgrim contact data, create a booking, or retain conversation content.

### `POST /v1/guides/{guide_id}/reports`
- Auth required unless an approved abuse-safe alternative is defined.
- `Idempotency-Key` required where retry duplication matters.
- Rate-limited.
- Report body is restricted trust-and-safety data and must not enter ordinary analytics.

## 18.4 Privileged verification/moderation
Provider verification, credential approval/revocation, suspension, urgent delisting, and public-eligibility override are privileged service/admin operations.

They must **not** be exposed as ordinary mobile-provider actions that allow self-verification.

## 18.5 Error semantics
Guide endpoints must distinguish at least:
- `AUTH_REQUIRED`,
- `NETWORK_REQUIRED`,
- `RATE_LIMITED`,
- `PROVIDER_NOT_ELIGIBLE`,
- `CREDENTIAL_EXPIRED_OR_INVALID`,
- `LISTING_NOT_PUBLIC`,
- `SERVICE_TYPE_UNAVAILABLE`,
- `FEATURE_LEGALLY_UNAVAILABLE`,
- `CONTACT_CHANNEL_UNAVAILABLE`,
- validation/conflict failures.

Errors must not leak restricted moderation or credential evidence.

## 18.6 Audit and legal gate
No guide endpoint family may be enabled for public production while the applicable legal release gates in file `32` remain unresolved.

---

End of file.
