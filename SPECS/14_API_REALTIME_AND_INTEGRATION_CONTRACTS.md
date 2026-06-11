# 14 — API, REALTIME, AND INTEGRATION CONTRACTS

## Document status
- **Type:** Normative service contract specification
- **Priority:** Highest
- **Audience:** Backend engineer, Flutter engineer, QA, AI agents, release/ops
- **Purpose:** Define HTTP API endpoints, realtime contracts, integration boundaries, request/response shapes, caching, auth, errors, and contract-testing expectations.
- **Last-updated-by:** AI-assisted hardening pass (validated 2026-03-22)
- **Related files:** 06, 07, 13, 15, 17, 20, 23, 24, 26, 27, 28, 29, 30

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
The online API should stay small.

The app must not become dependent on a large server backend for core local-first value.

## 2.2 Local-first default
The API supports:
- entitlements,
- group coordination,
- pack manifest discovery,
- safety/config flags,
- purchase validation,
- selected publishing/control-plane functions.

It should not become the default home for:
- notes,
- medical profile,
- ritual progress,
- saved anchors,
- local planner data,
- private user-authored content.

## 2.3 Explicit trust boundary rule
If a feature needs trusted server authority, the API must clearly define that trust boundary.

Examples:
- entitlement state,
- group membership,
- group leader permissions,
- purchase validation,
- release flags.

## 2.4 No hidden generic content API
Governed content should not be served by an undefined generic live API.

Governed content distribution must follow files `15`, `23`, and `26`.

## 2.5 Contract-first rule
Mobile code, backend handlers, and tests must agree on the contract.

Do not silently change:
- endpoint paths,
- enums,
- error codes,
- field names,
- auth rules,
- cache behavior,
- realtime event payloads.

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
The database remains the source of truth for server-backed domain data.

The API must not bypass RLS assumptions casually.

## 3.3 External integrations
External integrations may include:
- Apple / Google purchase validation,
- CDN/R2 pack delivery,
- crash/analytics service ingestion,
- platform notification APIs for local behavior only where applicable.

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
Join a group by join code.

### `POST /v1/groups/{group_id}/checkins`
Create a group check-in.

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

### `GET /v1/account/deletion-status`
Return the current status of an authenticated deletion request.

### `POST /v1/privacy/export-request`
Request an explicit, scoped export of server-backed personal data where applicable.

### `GET /v1/privacy/retention-summary`
Return a user-readable summary of server-backed data categories, default retention posture, and local-only data boundaries.

## 4.6 Optional future endpoints (not active by default)
These must not be implemented unless approved and documented.
- `PATCH /v1/groups/{group_id}`
- `POST /v1/groups/{group_id}/itinerary`
- `PATCH /v1/groups/{group_id}/itinerary/{day}`
- `GET /v1/groups/{group_id}/presence`
- `POST /v1/official-handoff/resolve`

---

# 5. Base protocol rules

## 5.1 Transport
- HTTPS only
- JSON request and response bodies unless explicitly documented otherwise
- UTF-8 encoding

## 5.2 Path versioning
All HTTP endpoints must be version-prefixed.

Current version:
- `/v1/...`

## 5.3 Content types
### Requests
- `Content-Type: application/json`

### Responses
- `Content-Type: application/json; charset=utf-8`

## 5.4 Timestamp format
All server timestamps must use RFC 3339 / ISO 8601 UTC timestamps.

## 5.5 JSON naming convention
JSON field names use `snake_case`.

## 5.6 Unknown field rule
Clients must ignore unknown response fields unless the endpoint contract explicitly forbids it.

Servers must reject unknown dangerous request fields where accepting them would create privilege, privacy, or integrity ambiguity.

---

# 6. Authentication and authorization

## 6.1 Auth mechanism
Authenticated endpoints require a valid user identity token.

The API layer validates:
- token presence,
- token signature / provider validity,
- expiry,
- user identity binding.

## 6.2 Public endpoints
Public endpoints:
- `GET /v1/flags`
- `GET /v1/packs/manifest`

Public endpoints must not expose user-private data.

## 6.3 Authenticated endpoints
Authenticated endpoints include:
- entitlements,
- group reads/writes,
- purchase validation/restore,
- account/privacy data requests.

## 6.4 Authorization rules
Authorization must validate:
- user can read the requested group,
- user can write to the requested group,
- user is leader where leader-only action is required,
- user can access the requested entitlement state,
- user can request deletion/export only for their own account context.

## 6.5 Client trust rule
The client must not be trusted for:
- membership,
- leader role,
- entitlement tier,
- purchase validity,
- server-side deletion/export status.

---

# 7. Standard response envelopes

## 7.1 Success envelope rule
Small endpoints may return direct JSON objects.

For list-like endpoints, prefer:
```json
{
  "data": [],
  "meta": {
    "server_time": "2026-03-22T00:00:00Z"
  }
}
```

## 7.2 Error envelope
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

## 7.3 Error message rule
Error messages should be safe for user-facing display only when the endpoint marks them as such.

Avoid exposing:
- database internals,
- provider raw messages,
- secrets,
- receipt payloads,
- raw auth failures,
- sensitive operational detail.

---

# 8. Canonical error codes

Use these stable error codes unless file `04` approves changes:

- `VALIDATION_ERROR`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `NOT_FOUND`
- `CONFLICT`
- `RATE_LIMITED`
- `PRECONDITION_FAILED`
- `INTEGRATION_ERROR`
- `INTERNAL_ERROR`

## 8.1 Feature-specific examples
### Group join
- bad code format → `VALIDATION_ERROR`
- code not found → `NOT_FOUND`
- already joined → `CONFLICT` or successful idempotent response depending on request identity
- unauthenticated → `UNAUTHORIZED`
- not allowed → `FORBIDDEN`

### Purchase validation
- invalid payload → `VALIDATION_ERROR`
- store unavailable → `INTEGRATION_ERROR`
- duplicate known transaction → idempotent success where safe

### Pack manifest
- unavailable backend → stale local fallback on client if available

---

# 9. Request IDs and traceability

## 9.1 Request ID rule
Every API response should include or be associated with a request ID.

The request ID may be:
- response header,
- body field in error envelope,
- structured log correlation value.

## 9.2 Client logging rule
Clients may log request IDs for diagnostics.

Clients must not log:
- raw tokens,
- raw receipts,
- medical profile content,
- exact private location,
- personal notes,
- ritual-sensitive private user notes.

---

# 10. Rate limiting rules

## 10.1 Goals
Rate limiting exists to protect:
- edge capacity,
- abuse-sensitive flows,
- store-validation endpoints,
- join-code brute forcing,
- accidental client retry storms.

## 10.2 Baseline limits
These are initial contract-level defaults and may be tuned with documented change control.

- `GET /v1/flags` → 60 requests/minute/IP
- `GET /v1/packs/manifest` → 30 requests/minute/IP
- `GET /v1/entitlements` → 30 requests/minute/user
- `POST /v1/groups` → 3 requests/hour/user and stricter abuse detection where needed
- `POST /v1/groups/join` → 10 requests/minute/user
- `POST /v1/groups/{group_id}/checkins` → 30 requests/minute/user
- `POST /v1/groups/{group_id}/regroup-pins` → 15 requests/minute/user
- `PATCH /v1/groups/{group_id}/regroup-pins/{pin_id}` → 30 requests/minute/user
- `POST /v1/purchases/*` → 15 requests/minute/user

## 10.3 Rate-limit contract rule
429 responses must include a retry hint and must not return HTML or provider-native error blobs.

---

# 11. Idempotency rules

## 11.1 Purpose
Idempotency is required where retries are likely and duplicate side effects would be harmful or confusing.

## 11.2 Required behavior
When the same authenticated principal sends the same idempotency key to the same endpoint within the retention window, the server must return the original logical result or a consistent duplicate-safe response.

## 11.3 Retention window
Default idempotency-key retention window:
- 24 hours for group creation, join, and purchase endpoints

## 11.4 Endpoint rules
### `POST /v1/groups`
Must be idempotent. Retried group creation must not create duplicate groups for the same creation intent.

### `POST /v1/groups/join`
Must be idempotent.

### `POST /v1/purchases/validate`
Must be idempotent by store transaction identity and idempotency key where applicable.

### `POST /v1/purchases/restore`
Must be retry-safe.

---

# 12. Caching and ETag rules

## 12.1 Goals
Caching is used to reduce latency, save battery and bandwidth, and support offline continuity.

## 12.2 Public cacheable endpoints
### `GET /v1/flags`
Recommended:
- `Cache-Control: public, max-age=300`
- ETag support
- client may use last-good cached snapshot offline

### `GET /v1/packs/manifest`
Recommended:
- `Cache-Control: public, max-age=1800`
- ETag support
- client may browse last-known manifest offline but must not imply latest certainty

## 12.3 Non-public user-specific endpoints
User-specific endpoints must not be publicly cached.

Examples:
- entitlements,
- group state,
- purchase responses,
- account/privacy data responses.

## 12.4 Stale client behavior
If the client uses stale cached data, UI must distinguish:
- fresh,
- cached but acceptable,
- stale / needs refresh,
- unavailable.

---

# 13. Flags endpoint contract

## 13.1 Purpose
`GET /v1/flags` provides lightweight control-plane state.

It may include:
- season configuration,
- feature flags,
- safety banner pointers,
- content activation pointers,
- minimum app version hints,
- kill-switch flags for unsafe optional features.

## 13.2 Constraints
Flags must not contain:
- user-private data,
- large content payloads,
- scholar-sensitive live ritual rules,
- executable logic,
- raw secrets.

## 13.3 Example response
```json
{
  "server_time": "2026-03-22T00:00:00Z",
  "season": "umrah",
  "features": {
    "group_live_board": true,
    "offline_audio": true
  },
  "safety": {
    "banner_id": "safety_general_001",
    "level": "info"
  },
  "minimum_supported_app_version": "1.0.0"
}
```

## 13.4 Flag safety rule
Flags may hide or disable unsafe optional features.

Flags must not be used to remove baseline safety or correctness content.

---

# 14. Pack manifest contract

## 14.1 Purpose
`GET /v1/packs/manifest` returns available downloadable packs.

## 14.2 Manifest fields
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

## 14.3 Signed trust-chain fields
For mature release quality, manifest and artifact entries must also align with `SPECS/CONTRACTS/content_pack_trust_chain_contract.yaml`.

Required trust-chain fields include:
- `manifest_signature`,
- `artifact_signature`,
- `signing_key_id`,
- `signed_at`,
- `signing_algorithm`,
- revoked-key metadata where applicable.

## 14.4 Manifest rule
The client must not hardcode pack URLs.

## 14.5 Entitlement rule
If `entitlement_required` is present, the client must verify against trusted entitlement state before enabling gated convenience behavior.

Baseline safety/correctness packs must not be wrongly gated.

---

# 15. Entitlements endpoint contract

## 15.1 Purpose
`GET /v1/entitlements` returns trusted entitlement state.

## 15.2 Example response
```json
{
  "user_id": "uuid",
  "tier": "SUPPORTER",
  "source": "APPLE",
  "active_until": "2026-04-22T00:00:00Z",
  "gates": {
    "PACK_AUTO_DOWNLOAD": true,
    "AUDIO_OFFLINE": true,
    "GROUP_LIVE_BOARD": true,
    "SMART_PLANNER": true,
    "NOTES_BOOKMARKS_EXTENDED": true
  },
  "verified_at": "2026-03-22T00:00:00Z"
}
```

## 15.3 Rule
The client must not invent gates.

## 15.4 Stale state rule
If entitlement state is stale, UI must avoid implying verified current paid access where verification matters.

## 15.5 Capability policy rule
Implementation must validate entitlement use against `SPECS/CONTRACTS/entitlement_capability_policy.yaml`. Supporter must never gate capabilities marked `never_gate`.

---

# 16. Group endpoint contracts

## 16.1 Live-board response
A group live-board response should include:
- group summary,
- viewer role,
- members list or summary,
- latest check-ins,
- active regroup pins,
- freshness metadata,
- entitlement availability if live board is gated.

## 16.2 Check-in request
Fields:
- `kind`
- `text_pin`
- `client_event_id?`

Check-ins must not imply GPS tracking.

## 16.3 Regroup pin request
Fields:
- `label`
- `text_pin`
- `map_anchor_ref?`
- `expires_at?`

Leader-only.

## 16.4 Group creation request
Fields:
- `name`
- `season_scope?`
- `client_event_id?`

The server returns:
- group id,
- group name,
- viewer role,
- generated join code,
- share-code copy fields.

The server must not import contacts, auto-invite members, or create hidden social graph data.

## 16.5 Freshness rule
Group responses must expose enough timestamp/freshness information for the client to avoid fake-live presentation.

## 16.6 Group presence privacy rule
Any future normalized presence state must follow `SPECS/CONTRACTS/group_presence_privacy_contract.yaml`.

---

# 17. Purchase endpoints

## 17.1 Purchase validation input
The API may accept:
- store platform,
- receipt/transaction reference,
- app account token where applicable,
- product identifier,
- idempotency key.

## 17.2 Security rule
Raw receipt payloads must be treated as sensitive operational data.

Do not expose raw provider payloads to logs or analytics.

## 17.3 Store abstraction rule
The mobile app should receive normalized entitlement state, not provider-native payloads as product truth.

---

# 18. Realtime contracts

## 18.1 Realtime scope
Realtime is approved only for group coordination enhancement.

## 18.2 Channel authorization
Realtime channels must validate:
- authenticated user,
- active group membership,
- role where needed.

## 18.3 Event types
Allowed group realtime event families:
- `group_checkin_created`
- `group_regroup_pin_created`
- `group_regroup_pin_updated`
- `group_member_updated`

## 18.4 Realtime degradation rule
Realtime must never be the only path to correctness.

If realtime fails, the app should use:
- manual refresh,
- cached snapshot with stale state,
- SMS/share fallback where relevant.

---

# 19. Retry behavior

## 19.1 Safe retries
Clients may retry:
- idempotent GETs,
- idempotent POSTs with idempotency key,
- transient network failures.

## 19.2 Retry backoff
Use exponential backoff or bounded retry policy for transient failures.

## 19.3 No retry storm rule
The app must not retry aggressively in crowded weak-network contexts.

Respect:
- rate-limit hints,
- network state,
- battery/performance concerns,
- user stress.

---

# 20. Offline and degraded behavior

## 20.1 Offline endpoint behavior
When offline:
- public cached data may fall back to last-good snapshots,
- entitlements may show cached continuity but not verified certainty,
- group protected writes must not pretend success,
- purchases/restores must show unavailable or pending explanation,
- account deletion/export requests must show unavailable until trusted server write is possible.

## 20.2 User-copy rule
Offline errors should explain:
- what still works,
- what needs network,
- whether data was saved locally,
- whether trusted server action happened.

---

# 21. Contract testing

## 21.1 Required contract tests
Contract tests must cover:
- schema fields,
- required/optional fields,
- auth requirements,
- error envelopes,
- canonical error codes,
- cache headers,
- idempotency behavior,
- rate-limit responses,
- stale/offline behavior.

## 21.2 Client fixture rule
Mobile test fixtures must be generated from or checked against the canonical contract.

Do not hand-maintain divergent mocks.

## 21.3 Breaking-change rule
Breaking API changes require synchronized updates to:
- this file,
- backend handlers,
- Flutter client models,
- fixtures,
- tests,
- analytics/dashboard expectations where relevant,
- release notes and migration plan where user-visible.

---

# 22. Privacy and security rules

## 22.1 Data minimization
Endpoints must request and return only what the feature needs.

## 22.2 No sensitive data in URL rule
Do not put tokens, receipts, medical data, private notes, or exact private coordinates in URLs or query strings.

## 22.3 Log redaction rule
API logs must redact:
- auth tokens,
- receipts,
- personal contact info where not needed,
- medical values,
- raw private text,
- precise location.

## 22.4 Account/privacy endpoint rule
Deletion, status, export, and retention endpoints must align with file `24` UX and file `29` retention/disclosure rules.

---

# 23. Observability requirements

## 23.1 Required API metrics
Track:
- request count,
- latency,
- error rate,
- rate-limit count,
- auth failure count,
- integration failure count,
- stale fallback usage where client reports it.

## 23.2 Critical endpoint alerts
Alert on abnormal failure for:
- `GET /v1/flags`,
- `GET /v1/packs/manifest`,
- `GET /v1/entitlements`,
- `POST /v1/groups`,
- `POST /v1/groups/join`,
- `POST /v1/groups/{group_id}/checkins`,
- `POST /v1/purchases/validate`,
- `POST /v1/purchases/restore`,
- `POST /v1/account/deletion-request`.

## 23.3 Privacy rule
No telemetry payload should include raw receipts, raw JWTs, medical profile contents, or exact hidden personal location.

---

# 24. Definition of done for this API system

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
- pack/content trust-chain fields are supported where applicable,
- observability is in place,
- release evidence links to file `28`.

---

# 25. AI-agent checklist

Before editing API-related code, an AI agent must:
1. Read files `13`, `14`, `24`, and `29`.
2. Read relevant feature-family file(s).
3. Check `SPECS/CONTRACTS/*` for affected machine-readable contracts.
4. Verify whether endpoint is public or authenticated.
5. Verify RLS and authorization assumptions.
6. Update contract tests and fixtures.
7. Avoid adding new endpoints without spec approval.
8. Document any breaking contract change.

---

End of file.