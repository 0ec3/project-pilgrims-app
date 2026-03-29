# 14 — API, REALTIME, AND INTEGRATION CONTRACTS

## Document status
- **Type:** Normative service contract document
- **Priority:** Highest
- **Audience:** Backend engineers, Flutter engineers, tech lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical online contract surface for Pilgrims Mobile App, including HTTP APIs, authentication and authorization rules, request/response schemas, error envelopes, rate limits, idempotency rules, caching behavior, realtime channels, external integration boundaries, versioning, and contract-change discipline.
- **Authority level:** This file is the canonical source of truth for API and realtime behavior. Handlers, clients, mocks, tests, and feature implementations must not diverge from this file.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`
- **Related files:** `10`, `11`, `12`, `15`, `16`, `17`, `18`–`26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists to prevent contract drift between:
- Flutter clients,
- Cloudflare Workers handlers,
- Supabase-backed data access,
- store validation flows,
- realtime channel behavior,
- tests, mocks, and fixtures.

This project is especially sensitive to API drift because:
- the online surface is intentionally small and must remain stable,
- offline-first behavior depends on predictable caching and safe fallbacks,
- group coordination relies on trusted authorization,
- entitlements must be server-validated,
- AI agents are prone to changing handlers without updating clients or docs,
- realtime access must not bypass the app’s privacy and authorization model.

This file defines:
- the canonical online surface,
- the request and response shapes,
- headers and status behavior,
- realtime channel contracts,
- store validation boundaries,
- change and versioning rules.

---

# 2. Contract design principles

## 2.1 Tiny online surface
Only the smallest set of features that truly require server coordination should be online.

## 2.2 Predictable contracts
Requests and responses must be explicit, versioned, and additive by default.

## 2.3 HTTP first, realtime selectively
Most online interactions should use standard HTTP. Realtime should be used only where a meaningful shared live experience exists.

## 2.4 Cache aggressively where safe
Read-heavy public configuration endpoints should support strong client and edge caching behavior.

## 2.5 Trust the server, not the client
The client may cache and render state, but entitlements, group membership, and protected writes must be validated in trusted layers.

## 2.6 Error handling must be standardized
Every non-success response must use a consistent machine-readable envelope.

## 2.7 Additive evolution over breakage
New optional fields and new endpoints are preferred over changing the meaning of existing fields.

---

# 3. Contract surface overview

## 3.1 Canonical HTTP surface
The app’s core online surface consists of:
- public control-plane reads
- authenticated entitlement reads
- authenticated group coordination writes/reads
- receipt validation / restore flows
- optional official-service handoff resolution if later approved

## 3.2 Canonical realtime surface
Realtime is limited to selected group-coordination experiences where live updates improve value.

## 3.3 Explicitly not part of the default online surface
The API is **not** intended to become:
- a generic content-delivery API for all ritual logic,
- a generalized notes/planner sync API,
- a background tracking channel,
- a giant map backend that every interaction depends on,
- a substitute for pack asset hosting,
- a substitute for official authority-managed services.

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

## 4.5 Optional future endpoints (not active by default)
These must not be implemented unless approved and documented.
- `POST /v1/groups`
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
Clients must ignore unknown response fields.
Servers must reject unexpected critical request fields only where validation rules require it.

---

# 6. Authentication and authorization rules

## 6.1 Public endpoints
No authentication required:
- `GET /v1/flags`
- `GET /v1/packs/manifest`

These endpoints must not return user-specific or sensitive data.

## 6.2 Authenticated endpoints
Require a valid user JWT issued by Supabase Auth:
- `GET /v1/entitlements`
- all group read/write endpoints
- all purchase endpoints

## 6.3 JWT rule
The edge layer must validate JWT authenticity and expiration before protected operations.

## 6.4 Authorization rule
Authentication is not sufficient for group actions. Group membership and role checks must also pass.

## 6.5 Client rule
The client may hide UI based on cached membership or entitlements, but the server remains authoritative.

---

# 7. Standard headers

## 7.1 Authenticated requests
- `Authorization: Bearer <jwt>`

## 7.2 Idempotent write protection
For retry-prone writes:
- `Idempotency-Key: <uuid-v4>`

Required on:
- `POST /v1/groups/join`
- `POST /v1/purchases/validate`
- `POST /v1/purchases/restore`

Optional but recommended on:
- `POST /v1/groups/{group_id}/checkins`
- `POST /v1/groups/{group_id}/regroup-pins`

## 7.3 Cache validation
For ETagged reads:
- `If-None-Match: <etag>`

Supported on:
- `GET /v1/flags`
- `GET /v1/packs/manifest`
- optionally `GET /v1/entitlements` if a strong snapshot contract is later justified

## 7.4 Request tracing
Server responses should include:
- `X-Request-Id`

## 7.5 Rate limit hints
When rate limiting is enforced, responses may include:
- `Retry-After`
- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset`

---

# 8. Standard response envelope rules

## 8.1 Success responses
Success responses return either:
- a JSON object,
- a JSON array,
- or `204 No Content` where documented.

## 8.2 Error envelope
All non-2xx responses must use this JSON structure:

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

## 8.3 Error codes
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

## 8.4 Error-message rules
- `message` must be safe for logs and safe for user-facing fallback copy.
- Do not leak secrets, SQL details, or store-provider internals.
- `fields` must be present only when field-level validation applies.

---

# 9. Status code rules

## 9.1 Common success codes
- `200 OK`
- `201 Created`
- `204 No Content`
- `304 Not Modified`

## 9.2 Common client error codes
- `400 Bad Request` → `VALIDATION_ERROR`
- `401 Unauthorized` → `UNAUTHORIZED`
- `403 Forbidden` → `FORBIDDEN`
- `404 Not Found` → `NOT_FOUND`
- `409 Conflict` → `CONFLICT`
- `412 Precondition Failed` → `PRECONDITION_FAILED`
- `429 Too Many Requests` → `RATE_LIMITED`

## 9.3 Common server error codes
- `500 Internal Server Error` → `INTERNAL_ERROR`
- `502/503/504` may be used where upstream or provider failure needs transport distinction

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
- 24 hours for join and purchase endpoints

## 11.4 Endpoint rules
### `POST /v1/groups/join`
Must be idempotent.

### `POST /v1/purchases/validate`
Must be idempotent relative to the same purchase reference.

### `POST /v1/purchases/restore`
Must be idempotent.

### `POST /v1/groups/{group_id}/checkins`
Should tolerate duplicates safely. If `client_event_id` is supplied, the server may coalesce duplicates.

---

# 12. Caching and ETag rules

## 12.1 Goals
Caching is used to reduce latency, save battery and bandwidth, and support offline-first control-plane behavior.

## 12.2 ETagged endpoints
Required ETag behavior on:
- `GET /v1/flags`
- `GET /v1/packs/manifest`

## 12.3 Cache-Control defaults
### `GET /v1/flags`
- `Cache-Control: public, max-age=300`

### `GET /v1/packs/manifest`
- `Cache-Control: public, max-age=1800`

## 12.4 304 behavior
If `If-None-Match` matches the current representation, return `304 Not Modified` with no response body.

## 12.5 Client rule
Clients must store the last-good payload and ETag and use them for offline continuity.

## 12.6 Cache safety rule
Only endpoints with no user-specific private data may be treated as public-cacheable.

---

# 13. Canonical schema fragments

These schemas describe the primary JSON contract shapes. The machine-readable OpenAPI file may express them in JSON Schema/OpenAPI syntax, but these definitions are normative.

## 13.1 `flags_response`
```json
{
  "season": "umrah",
  "banners": [
    {
      "id": "safety_global",
      "kind": "info",
      "text": "Follow on-ground staff and signage.",
      "starts_at": null,
      "ends_at": null
    }
  ],
  "toggles": {
    "group_live_board": true,
    "smart_planner": true,
    "ios_glass_chrome": true
  },
  "updated_at": "2026-03-09T00:00:00Z"
}
```

### Required fields
- `season`
- `banners`
- `toggles`
- `updated_at`

### Rules
- `season` ∈ `umrah | hajj`
- `banners` may be empty
- `toggles` must only contain documented keys

## 13.2 `packs_manifest_response`
```json
{
  "version": 3,
  "generated_at": "2026-03-09T00:00:00Z",
  "packs": [
    {
      "id": "haram_hires_ar_v3",
      "type": "MAP",
      "title": "Haram High-Resolution Pack",
      "languages": ["ar", "en", "id"],
      "size_bytes": 73400320,
      "checksum_sha256": "...",
      "artifact_url": "https://cdn.example/packs/haram_hires_ar_v3.pack",
      "requires_supporter": true,
      "aoi": "haram",
      "min_app_version": "1.0.0"
    }
  ]
}
```

### Required fields
- `version`
- `generated_at`
- `packs`

### Pack fields
Required per pack:
- `id`
- `type`
- `title`
- `size_bytes`
- `checksum_sha256`
- `artifact_url`
- `requires_supporter`

Optional:
- `languages`
- `aoi`
- `min_app_version`
- `description`
- `recommended_when`

## 13.3 `entitlements_response`
```json
{
  "tier": "SUPPORTER",
  "active_until": "2026-05-01T00:00:00Z",
  "source": "APPLE",
  "gates": {
    "PACK_AUTO_DOWNLOAD": true,
    "AUDIO_OFFLINE": true,
    "SMART_PLANNER": true,
    "GROUP_LIVE_BOARD": true,
    "NOTES_BOOKMARKS_EXTENDED": true
  },
  "last_validated_at": "2026-03-09T00:00:00Z"
}
```

### Required fields
- `tier`
- `gates`

### Rules
- `tier` ∈ `FREE | SUPPORTER`
- `gates` must reflect trusted server-side state

## 13.4 `group_join_request`
```json
{
  "code": "AB12CD"
}
```

### Required fields
- `code`

### Validation
- exactly 6 uppercase alphanumeric characters

## 13.5 `group_join_response`
```json
{
  "group": {
    "id": "uuid",
    "code": "AB12CD",
    "name": "Family Group",
    "leader_user_id": "uuid",
    "season_scope": "UMRAH"
  },
  "membership": {
    "role": "MEMBER",
    "status": "ACTIVE",
    "joined_at": "2026-03-09T00:00:00Z"
  },
  "suggested_packs": [
    {
      "id": "haram_hires_ar_v3",
      "reason": "group_destination_match"
    }
  ]
}
```

### Required fields
- `group`
- `membership`
- `suggested_packs`

## 13.6 `group_checkin_request`
```json
{
  "text_pin": "Gate 72, Level 1, near Umbrella B",
  "kind": "SAFE",
  "client_event_id": "uuid"
}
```

### Required fields
- `text_pin`

### Optional fields
- `kind`
- `client_event_id`
- `metadata`

### Rules
- `text_pin` length: 3–120 characters
- `kind` defaults to `SAFE`

## 13.7 `group_checkin_response`
Default response:
- `204 No Content`

Optional future additive response:
- may return normalized server echo metadata if needed, but not in v1 by default

## 13.8 `regroup_pin_create_request`
```json
{
  "label": "Meet here after tawaf",
  "text_pin": "Gate 79, Level 2",
  "map_anchor_ref": "gate:79:l2",
  "expires_at": "2026-03-09T06:00:00Z"
}
```

### Required fields
- `label`
- `text_pin`

### Rules
- leader-only
- `expires_at` optional

## 13.9 `regroup_pin_response`
```json
{
  "id": "uuid",
  "group_id": "uuid",
  "label": "Meet here after tawaf",
  "text_pin": "Gate 79, Level 2",
  "map_anchor_ref": "gate:79:l2",
  "is_active": true,
  "created_at": "2026-03-09T00:00:00Z",
  "expires_at": "2026-03-09T06:00:00Z"
}
```

## 13.10 `live_board_response`
```json
{
  "group_id": "uuid",
  "generated_at": "2026-03-09T00:00:00Z",
  "members": [
    {
      "user_id": "uuid",
      "display_name": "Aisha",
      "last_checkin_at": "2026-03-09T00:00:00Z",
      "last_text_pin": "Gate 72, Level 1",
      "freshness": "RECENT"
    }
  ],
  "active_regroup_pins": []
}
```

### Rules
- visible only to active group members
- may be gated by supporter entitlement in product policy, but must still obey membership authorization

## 13.11 `purchase_validate_request`
```json
{
  "platform": "ios",
  "product_id": "supporter_monthly",
  "receipt": "opaque receipt or signed transaction payload",
  "transaction_id": "optional-client-known-ref"
}
```

### Required fields
- `platform`
- `product_id`
- at least one purchase proof field required by the platform contract

## 13.12 `purchase_restore_request`
```json
{
  "platform": "android"
}
```

## 13.13 `purchase_response`
```json
{
  "entitlements": {
    "tier": "SUPPORTER",
    "active_until": "2026-05-01T00:00:00Z",
    "source": "GOOGLE",
    "gates": {
      "PACK_AUTO_DOWNLOAD": true,
      "AUDIO_OFFLINE": true,
      "SMART_PLANNER": true,
      "GROUP_LIVE_BOARD": true,
      "NOTES_BOOKMARKS_EXTENDED": true
    },
    "last_validated_at": "2026-03-09T00:00:00Z"
  }
}
```

---

# 14. Endpoint contracts

## 14.1 `GET /v1/flags`
### Purpose
Returns small control-plane state such as season, banners, and simple feature toggles.

### Auth
Public

### Caching
ETag + `Cache-Control: public, max-age=300`

### Response
- `200` → `flags_response`
- `304` → no body

### Notes
- must never return PII
- must remain lightweight and safe for offline cache reuse

## 14.2 `GET /v1/packs/manifest`
### Purpose
Returns metadata for downloadable packs.

### Auth
Public

### Caching
ETag + `Cache-Control: public, max-age=1800`

### Response
- `200` → `packs_manifest_response`
- `304` → no body

### Notes
- artifact URLs may point to CDN/R2
- pack metadata is immutable by version

## 14.3 `GET /v1/entitlements`
### Purpose
Return current trusted entitlement snapshot.

### Auth
Required

### Response
- `200` → `entitlements_response`
- `401` / `403`

### Notes
- client must treat server response as authoritative
- response must not overexpose internal billing provider details

## 14.4 `POST /v1/groups/join`
### Purpose
Join a group using its join code.

### Auth
Required

### Headers
- `Authorization`
- `Idempotency-Key` required

### Request body
`group_join_request`

### Response
- `200` → `group_join_response`
- `400` validation
- `401` unauthorized
- `404` if no matching active code exists
- `409` if already joined and business logic chooses conflict instead of idempotent success
- `429` rate-limited

### Notes
- idempotent replay should return same logical membership outcome
- join flow must enforce membership semantics consistent with RLS/data model

## 14.5 `POST /v1/groups/{group_id}/checkins`
### Purpose
Create a group check-in.

### Auth
Required

### Headers
- `Authorization`
- `Idempotency-Key` optional but recommended

### Request body
`group_checkin_request`

### Response
- `204 No Content`
- `400` validation
- `401` unauthorized
- `403` not an active member
- `404` group not found
- `429` rate-limited

### Notes
- no precise GPS required
- text-based pin is the primary input
- server may coalesce duplicate `client_event_id` values safely

## 14.6 `GET /v1/groups/{group_id}/live-board`
### Purpose
Return current group coordination snapshot.

### Auth
Required

### Response
- `200` → `live_board_response`
- `401` unauthorized
- `403` not an active member
- `404` group not found

### Notes
- entitlement gating, if any, is product policy layered on top of authorization
- if product policy hides live board for free users, return a product-appropriate contract such as `403` with explanatory code or a reduced response only if explicitly documented

## 14.7 `GET /v1/groups/{group_id}/regroup-pins`
### Purpose
Return active regroup pins for the group.

### Auth
Required

### Response
- `200` → array of `regroup_pin_response`
- `401` / `403` / `404`

## 14.8 `POST /v1/groups/{group_id}/regroup-pins`
### Purpose
Create a regroup pin.

### Auth
Required

### Request body
`regroup_pin_create_request`

### Response
- `201 Created` → `regroup_pin_response`
- `401` unauthorized
- `403` not an active leader
- `404` group not found
- `429` rate-limited

## 14.9 `PATCH /v1/groups/{group_id}/regroup-pins/{pin_id}`
### Purpose
Update or deactivate a regroup pin.

### Auth
Required

### Response
- `200` → updated `regroup_pin_response`
- `401` / `403` / `404`

### Notes
- patch semantics must be explicit in the machine-readable contract
- leader-only

## 14.10 `GET /v1/groups/{group_id}/itinerary`
### Purpose
Return group itinerary data.

### Auth
Required

### Response
- `200` → array or object keyed by day, as defined in OpenAPI
- `401` / `403` / `404`

### Notes
- active members can read

## 14.11 `POST /v1/purchases/validate`
### Purpose
Validate a purchase and refresh entitlement state.

### Auth
Required

### Headers
- `Authorization`
- `Idempotency-Key` required

### Request body
`purchase_validate_request`

### Response
- `200` → `purchase_response`
- `400` validation
- `401` unauthorized
- `403` invalid purchase or forbidden state
- `409` conflicting purchase state where applicable
- `429` rate-limited
- `502/503` provider integration failure if surfaced at transport level

### Notes
- server must not trust client-side purchase success without validation
- provider-native payload details should not leak directly to app clients

## 14.12 `POST /v1/purchases/restore`
### Purpose
Restore trusted entitlement state from store/back-end records.

### Auth
Required

### Headers
- `Authorization`
- `Idempotency-Key` required

### Request body
`purchase_restore_request`

### Response
- `200` → `purchase_response`
- `400` / `401` / `403` / `429`

---

# 15. Realtime architecture contract

## 15.1 Realtime design goals
Realtime is used only where it improves group coordination meaningfully without becoming mandatory for basic group usefulness.

## 15.2 Canonical realtime use cases
Allowed v1/v1.1 use cases:
- live board freshness updates
- regroup pin broadcast/update events
- presence or broadcast events scoped to private group channels

## 15.3 Realtime transport rule
Private Supabase Realtime channels are the preferred contract surface for group live coordination, not public channels.

## 15.4 Realtime authorization rule
Realtime access must be gated by authorization rules consistent with group membership and role constraints.

## 15.5 Realtime is optional, not required for feature baseline
If realtime is unavailable, the app must degrade to HTTP snapshot + manual coordination fallback.

---

# 16. Realtime channel contracts

## 16.1 Channel naming rule
Channel names must be stable, private, and derivable from canonical domain identifiers.

### Canonical examples
- `private:group:{group_id}`
- `private:group:{group_id}:presence`
- `private:group:{group_id}:pins`

## 16.2 Public channels forbidden for protected group data
Protected group data must never rely on public channel subscription.

## 16.3 Channel membership rule
A client may join a private group channel only if it is an active member of that group.

## 16.4 Leader write rule
Leader-only broadcast/update actions must be enforced for leader-scoped events such as regroup pin creation or pin-state updates.

---

# 17. Realtime event catalog

## 17.1 `group.live_board.snapshot`
### Purpose
Optional initial snapshot event for live-board subscribers.

### Payload
```json
{
  "type": "group.live_board.snapshot",
  "group_id": "uuid",
  "generated_at": "2026-03-09T00:00:00Z",
  "members": []
}
```

## 17.2 `group.checkin.created`
### Purpose
Notify group members that a new check-in has been recorded.

### Payload
```json
{
  "type": "group.checkin.created",
  "group_id": "uuid",
  "checkin": {
    "id": "uuid",
    "user_id": "uuid",
    "kind": "SAFE",
    "text_pin": "Gate 72, Level 1",
    "created_at": "2026-03-09T00:00:00Z"
  }
}
```

## 17.3 `group.regroup_pin.created`
### Payload
```json
{
  "type": "group.regroup_pin.created",
  "group_id": "uuid",
  "pin": {
    "id": "uuid",
    "label": "Meet here after tawaf",
    "text_pin": "Gate 79, Level 2",
    "map_anchor_ref": "gate:79:l2",
    "is_active": true,
    "created_at": "2026-03-09T00:00:00Z"
  }
}
```

## 17.4 `group.regroup_pin.updated`
### Payload
Same shape as created event with updated fields.

## 17.5 `group.presence.changed`
Optional if presence semantics are enabled.

### Rule
Presence events must remain privacy-light and must not imply hidden continuous location tracking.

---

# 18. Realtime delivery semantics

## 18.1 Ordering rule
Realtime delivery should be treated as best-effort near-real-time, not as the sole canonical ordering source for critical business truth.

## 18.2 Recovery rule
Clients must be able to recover from disconnect by reloading snapshot data over HTTP.

## 18.3 Deduplication rule
Clients should deduplicate events by stable IDs or timestamps when the same logical event can arrive via snapshot + stream.

## 18.4 Replay rule
If replay is later enabled, replay access must still obey private-channel authorization.

---

# 19. External integration boundaries

## 19.1 Store integrations
External store integrations are used for:
- iOS purchase validation / restore
- Android purchase validation / restore

### Rule
Store-provider-specific logic must terminate at the trusted backend boundary and return normalized entitlement responses to the app.

## 19.2 Official-service handoff integrations
If later implemented, official-service handoffs must:
- remain explicitly bounded,
- avoid pretending the app owns the official workflow,
- use link or metadata resolution contracts rather than scraping or unofficial assumptions.

## 19.3 Map/provider integrations
Provider-specific map SDK usage must not leak into API contracts unless a future server-side map feature explicitly requires it.

---

# 20. Purchase integration contract rules

## 20.1 iOS purchase rule
The backend must treat App Store purchase state as trusted only after server-side validation/normalization.

## 20.2 Android purchase rule
The backend should verify Android purchases using secure server-side flows and should acknowledge purchases through backend-capable mechanisms where applicable.

## 20.3 Restore rule
Restore endpoints return current trusted entitlements, not raw historical purchase dumps.

## 20.4 Family sharing rule
Platform-specific family sharing behaviors may differ. The backend contract should return normalized entitlement state and source, not assume identical semantics across stores.

---

# 21. OpenAPI contract generation rule

## 21.1 Canonical machine-readable source
The machine-readable OpenAPI contract should be maintained as an OpenAPI 3.1 document.

## 21.2 Why OpenAPI 3.1
OpenAPI 3.1 aligns with modern JSON Schema and provides a strong interoperable contract basis for generated mocks, validation, and tooling.

## 21.3 Generated artifacts
From the OpenAPI contract, the project may generate:
- mock servers
- request validators
- client stubs
- schema docs

## 21.4 Rule
Generated artifacts do not replace this document or the machine-readable contract as sources of truth.

---

# 22. Validation rules

## 22.1 General validation
- reject malformed JSON
- reject wrong enum values
- reject unknown critical path parameters
- reject invalid join code formats
- reject overlong text pins and labels
- reject missing required fields

## 22.2 Path-parameter rule
Path parameters must be validated before trusted operations are attempted.

## 22.3 Authorization-before-work rule
Protected write operations should check authorization before expensive downstream operations when possible.

---

# 23. Observability and telemetry contract hooks

## 23.1 Required server metrics/events
The server should emit at least:
- `api_flags_200{etag_hit}`
- `api_manifest_200{etag_hit}`
- `api_entitlements_200{tier}`
- `api_group_join_200{role}`
- `api_group_checkin_204{kind}`
- `api_regroup_pin_201{}`
- `api_purchase_validate_200{platform}`
- `api_4xx{code}`
- `api_5xx{}`

## 23.2 Privacy rule
No telemetry payload should include raw receipts, raw JWTs, medical profile contents, or exact hidden personal data.

## 23.3 Request correlation rule
Error logs must be traceable using request IDs without requiring sensitive payload logging.

---

# 24. Security and abuse-prevention rules

## 24.1 Join-code abuse prevention
- validate format strictly
- rate-limit aggressively
- avoid disclosing whether a code exists beyond safe contract semantics

## 24.2 Group-write protection
- membership required for check-ins
- leader membership required for regroup pin writes
- all protected writes audited through request logs and DB policies

## 24.3 Purchase abuse prevention
- do not trust client-declared purchase success
- deduplicate transaction references
- retain enough normalized purchase history for entitlement debugging and fraud review

## 24.4 Realtime abuse prevention
- private channels only for protected group data
- authorization on join and send actions
- no public broadcast of protected coordination events

---

# 25. Versioning and deprecation policy

## 25.1 Additive changes
Additive changes include:
- new optional response fields
- new optional request fields where safely ignored
- new endpoints
- new event types

### Rule
These should not require a new major API version.

## 25.2 Breaking changes
Breaking changes include:
- removing or renaming fields
- changing required fields
- changing endpoint semantics incompatibly
- changing event payload semantics incompatibly

### Rule
Breaking changes require:
- `/v2` or equivalent version strategy
- migration plan
- deprecation window
- coordinated client rollout plan

## 25.3 Minimum deprecation window
Unless a security issue requires otherwise, old breaking contracts should remain supported for at least 90 days after new-client readiness.

---

# 26. Change-control workflow for API changes

## 26.1 Any handler change that alters contract shape requires
- this file updated
- machine-readable OpenAPI updated
- impacted feature docs updated
- tests and fixtures updated
- `13` updated if data shape changed
- `05` updated if status or release impact changed

## 26.2 CI rule
Contract validation, schema generation, or snapshot checks should fail CI when handlers drift from the documented contract.

---

# 27. Recommendations adopted into this contract design

## 27.1 Recommendation — stabilize around `/v1` and OpenAPI 3.1
The contract now formalizes versioned paths and an OpenAPI 3.1 machine-readable source instead of informal “OpenAPI-like” documentation.

## 27.2 Recommendation — dedicated regroup-pin endpoints
Because regroup pins are now a first-class entity in the data model, they are now first-class API resources as well.

## 27.3 Recommendation — realtime as enhancement, not dependency
The contract explicitly makes realtime optional for usefulness and preserves HTTP snapshot + manual fallback.

## 27.4 Recommendation — normalized purchase responses
Store-specific validation now resolves into one normalized entitlement response shape rather than leaking platform-specific complexity into the app.

## 27.5 Recommendation — control-plane reads remain tiny and cacheable
Flags and pack manifest remain the most aggressively cacheable surfaces to support local-first behavior.

---

# 28. Anti-patterns forbidden by this contract system

The following are forbidden unless explicitly approved.

## 28.1 Unversioned breaking endpoint changes
Forbidden.

## 28.2 Client-derived entitlement truth
Forbidden.

## 28.3 Public realtime channels for protected group data
Forbidden.

## 28.4 Endpoint-specific custom error formats
Forbidden.

## 28.5 Returning raw provider payloads directly to mobile clients
Forbidden.

## 28.6 Contract changes without corresponding data/doc/test updates
Forbidden.

## 28.7 Using realtime as the only way to recover group truth
Forbidden.

## 28.8 Turning the API into a generic sync surface for all local-first data
Forbidden.

---

# 29. When this file must be updated

This file must be updated whenever any of the following changes:
- endpoint list
- request or response fields
- status code semantics
- auth requirements
- rate limits
- idempotency rules
- caching rules
- realtime channel names or payloads
- purchase integration shapes
- versioning or deprecation policy
- machine-readable OpenAPI strategy

If any of these evolve but this file is not updated, mobile, backend, tests, and release safety will drift quickly.

---

# 30. Summary

This file defines the canonical service contracts for Pilgrims Mobile App.

It establishes:
- the small online API surface
- the authentication and authorization rules
- the standard headers, errors, status codes, rate limits, and idempotency rules
- the primary request and response schemas
- the realtime channel and event contracts
- the store integration boundaries
- the OpenAPI, versioning, and deprecation discipline
- the anti-patterns that must be prevented

Its purpose is to make backend and Flutter implementation:
- stable
- secure
- cache-friendly
- offline-compatible
- and safe for AI-assisted development without contract drift.

