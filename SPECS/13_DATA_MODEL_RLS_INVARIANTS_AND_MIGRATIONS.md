# 13 — DATA MODEL, RLS, INVARIANTS, AND MIGRATIONS

## Document status
- **Type:** Normative data architecture and database contract document
- **Priority:** Highest
- **Audience:** Backend engineers, Flutter engineers, tech lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical server-side and device-local data model for the app, including entity ownership, relationships, row-level security, invariants, migration rules, seeds, fixtures, and data-retention boundaries.
- **Authority level:** This file is the canonical source of truth for relational schema, local persistence shape, authorization boundaries at the data layer, and migration discipline. If code, APIs, or feature docs diverge from this file, this file wins unless superseded through documented change control.
- **Primary dependencies:** `SPECS/01_README_AND_MASTER_INDEX.md`, `SPECS/02_AI_AGENT_RULES_AND_WORKFLOW.md`, `SPECS/03_PRODUCT_CHARTER_AND_SCOPE.md`, `SPECS/04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, `SPECS/06_SYSTEM_ARCHITECTURE.md`, `SPECS/07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`
- **Related files:** `10`, `11`, `12`, `14`, `15`, `16`, `17`, `18`–`26`, `27`, `28`, `29`, `30`, `31`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/entitlement_capability_policy.yaml`

---

# 1. Purpose of this file

This file exists to stop one of the most expensive forms of project drift: data-model confusion.

For this product, data-model mistakes are especially dangerous because:
- AI agents can easily invent new fields or duplicate concepts,
- group authorization depends on correct relational boundaries,
- entitlements must be trusted and not inferred locally,
- local-first behavior requires a clean boundary between server data and device-only data,
- map, packs, notes, planner, and medical data do not all belong in the same persistence layer,
- migrations can silently break clients if they are treated casually,
- RLS mistakes can expose group data or enable unauthorized writes.

This file defines:
- what data lives on the server,
- what data lives only on device,
- which relationships are authoritative,
- what must always be true,
- which tables require RLS and how that RLS is shaped,
- how schema changes must be rolled out safely.

---

# 2. Data architecture principles

## 2.1 Separate identity from app profile
Supabase Auth is the identity source. App-specific profile data belongs in an app table that references the authenticated user, not in a duplicate credentials table.

## 2.2 Keep server scope intentionally small
Only data that truly needs shared, trusted, or server-backed behavior should live on the server.

## 2.3 Keep private and local-first data on device by default
Notes, bookmarks, saved anchors, ritual progress, planner items, emergency profile, and similar private support data should stay on device unless a future approved feature requires otherwise.

## 2.4 Use explicit ownership everywhere
Every row must have a clear ownership rule: self-owned, group-scoped, leader-scoped, or service-managed.

## 2.5 Enforce invariants at the lowest reasonable layer
If a rule can be enforced by constraints, indexes, foreign keys, or RLS, prefer that over relying only on application code.

## 2.6 Prefer additive migrations
Schema evolution should favor additive, reversible, low-risk changes and staged cleanup rather than destructive edits.

## 2.7 RLS is mandatory for user-scoped and group-scoped tables
Application logic may help the UX, but server-side access must still be enforced by policy.

---

# 3. Canonical persistence split

## 3.1 Server-side relational data
The server database stores only shared or trusted data.

Canonical server domains:
- account profile metadata,
- entitlement state,
- group records,
- group membership,
- group check-ins,
- group presence/freshness events where normalized state is required,
- regroup pins,
- optional group itinerary content,
- server-side purchase validation records,
- minimal audit fields required for correctness and operations,
- Guide Marketplace provider, credential, listing, contact-channel, verification-audit, and report state where file `32` requires shared/server-trusted behavior.

## 3.2 Device-local persistent data
The device stores local-first support data:
- ritual sessions and RIC findings,
- saved gates / saved anchors,
- planner items and local reminders,
- notes and bookmarks,
- local wallet artifacts; V1 remains device-local unless a later approved sync/export contract explicitly changes this,
- emergency / medical profile,
- pack inventory and installation state,
- local settings and UX dismissals,
- cached flags / manifest snapshots,
- lightweight map/local search indexes where needed.

For V1, wallet artifacts remain device-local by default. Do not add a server-backed wallet domain unless product, privacy, data-model, and API contracts are explicitly revised together.

## 3.3 Derived or ephemeral data
This data may exist temporarily or be regenerated, such as in-memory live board lists, transient route results, temporary upload/download states, and analytics event queues before flush.

---

# 4. Canonical server-side entity model

## 4.1 Identity source
### `auth.users`
This is the canonical authentication identity table managed by Supabase Auth.

Rule: do not duplicate email/phone/password identity ownership in a separate custom table unless a future documented reason requires it.

## 4.2 App profile table
### `profiles`
Stores app-specific user metadata linked 1:1 with `auth.users`.

Purpose:
- display name,
- locale preferences if server-backed,
- support metadata for group display,
- optional phone display/masking metadata if needed,
- account lifecycle timestamps.

Minimum columns:
- `id uuid primary key references auth.users(id) on delete cascade`
- `display_name text null`
- `phone_display text null`
- `avatar_url text null` (optional; not required for MVP)
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Indexes:
- primary key on `id`
- optional index on `created_at`

## 4.3 Entitlements table
### `user_entitlements`
Stores trusted, server-validated entitlement state.

Purpose:
- replace fragile client-side assumptions,
- support tier, active cutoff, source, restore/debug metadata, and server-computed gates.

Minimum columns:
- `user_id uuid primary key references auth.users(id) on delete cascade`
- `tier text not null default 'FREE'`
- `active_until timestamptz null`
- `source text not null default 'NONE'`
- `family_group_id text null`
- `last_validated_at timestamptz null`
- `gates jsonb not null default '{}'::jsonb`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Notes:
- `tier` is the human-readable entitlement tier.
- `active_until` is the current trusted paid-access cutoff where applicable.
- `gates` is a server-computed snapshot for client convenience, not the conceptual source of business policy.
- Feature docs and API docs may expose a simplified representation, but this table is the persistence truth.

Indexes:
- primary key on `user_id`
- index on `(tier)` if needed for admin/reporting only
- optional partial index on `(active_until)` for active subscription operations

## 4.4 Purchase validation records
### `purchase_receipts`
Stores server-side receipt validation history.

Purpose:
- audit successful and failed validation attempts,
- reconcile store events and restore flows,
- support entitlement debugging and fraud handling.

Minimum columns:
- `id uuid primary key default gen_random_uuid()`
- `user_id uuid not null references auth.users(id) on delete cascade`
- `platform text not null`
- `product_id text not null`
- `transaction_id text not null`
- `original_transaction_id text null`
- `status text not null`
- `validated_at timestamptz not null default now()`
- `expires_at timestamptz null`
- `raw_ref text null`
- `metadata jsonb not null default '{}'::jsonb`

Constraints:
- unique `(platform, transaction_id)`

Rule: do not store raw sensitive store payloads casually if a reference or normalized summary is sufficient.

## 4.5 Groups table
### `groups`
Represents a pilgrim coordination group.

Minimum columns:
- `id uuid primary key default gen_random_uuid()`
- `code text not null unique`
- `name text not null`
- `leader_user_id uuid not null references auth.users(id)`
- `season_scope text not null default 'UMRAH'`
- `created_by_client_event_id uuid null`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

Constraints:
- `check (length(code) = 6 and code ~ '^[A-Z0-9]+$')`
- `check (season_scope in ('UMRAH','HAJJ','MIXED'))`

Indexes:
- unique index on `(code)`
- index on `(leader_user_id)`
- optional index on `(created_by_client_event_id)` where not null

Group creation rule: group creation is a governed server-backed action. The server must generate `code`, create the `groups` row, and create the initial active leader row in `group_members` transactionally. The client must not choose the canonical join code or invent leader state locally.

## 4.6 Group membership table
### `group_members`
Represents membership and role of users inside groups.

Minimum columns:
- `group_id uuid not null references groups(id) on delete cascade`
- `user_id uuid not null references auth.users(id) on delete cascade`
- `role text not null`
- `joined_at timestamptz not null default now()`
- `status text not null default 'ACTIVE'`
- `display_alias text null`
- primary key `(group_id, user_id)`

Constraints:
- `check (role in ('LEADER','MEMBER'))`
- `check (status in ('ACTIVE','LEFT','REMOVED'))`

Indexes:
- index on `(user_id)`
- index on `(group_id, role)`
- index on `(group_id, status)`

Rule: there must always be exactly one active logical leader for a group, enforced by group/role consistency rules.

## 4.7 Group check-ins table
### `group_checkins`
Represents lightweight group-presence or “I’m Safe” activity.

Minimum columns:
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `user_id uuid not null references auth.users(id) on delete cascade`
- `kind text not null default 'SAFE'`
- `text_pin text not null`
- `client_event_id uuid null`
- `created_at timestamptz not null default now()`
- `metadata jsonb not null default '{}'::jsonb`

Constraints:
- `check (kind in ('SAFE','CHECKIN','STATUS'))`

Indexes:
- index on `(group_id, created_at desc)`
- index on `(group_id, user_id, created_at desc)`
- index on `(client_event_id)` where not null

Rule: check-ins are text-based coordination events. They do not imply GPS tracking.

## 4.8 Group presence events table
### `group_presence_events`
Represents normalized, time-bounded group freshness or presence state where a feature needs explicit TTL, revocation, retention, or map handoff semantics beyond plain check-ins.

### Why this table exists
Most group coordination remains text-first through `group_checkins` and `group_regroup_pins`. This table exists only to make privacy-sensitive freshness state explicit and testable when normalized state is required. It must not become a passive tracking table.

### Identifier mapping
`id` is the persisted database primary key. API payloads may expose this same value as `event_id`.

Do not add a separate persisted `event_id` column unless this file, file `14`, file `20`, and `CONTRACTS/group_presence_privacy_contract.yaml` are updated together.

### Minimum columns
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `actor_user_id uuid not null references auth.users(id) on delete cascade`
- `event_type text not null`
- `text_pin text null`
- `map_anchor_ref text null`
- `precision_level text not null default 'none'`
- `shared_at timestamptz not null default now()`
- `ttl_expires_at timestamptz not null`
- `freshness_status text not null default 'fresh'`
- `share_reason text not null default 'explicit_user_action'`
- `consent_token_id uuid null`
- `revoked_at timestamptz null`
- `retention_expires_at timestamptz null`
- `client_event_id uuid null`
- `metadata jsonb not null default '{}'::jsonb`

### Conditional field rules
- `text_pin` is required for `text_checkin` and `regroup_pin`.
- `text_pin` is optional for `safe_checkin` and `route_handoff`.
- `map_anchor_ref` is required for `regroup_pin` and `route_handoff`.
- `map_anchor_ref` is optional for `safe_checkin` and `text_checkin`.

These rules mirror `CONTRACTS/group_presence_privacy_contract.yaml` and should be enforced through application validation and database constraints where practical.

### Constraints
- `check (event_type in ('safe_checkin','text_checkin','regroup_pin','route_handoff'))`
- `check (precision_level in ('none','coarse','precise'))`
- `check (freshness_status in ('fresh','stale','expired','revoked'))`
- `check (share_reason = 'explicit_user_action')`
- conditional constraint: `text_pin is not null` when `event_type in ('text_checkin','regroup_pin')`
- conditional constraint: `map_anchor_ref is not null` when `event_type in ('regroup_pin','route_handoff')`

### Indexes
- index on `(group_id, shared_at desc)`
- index on `(group_id, freshness_status)`
- index on `(actor_user_id, shared_at desc)`
- index on `(ttl_expires_at)`
- index on `(retention_expires_at)` where not null
- index on `(client_event_id)` where not null

### Rules
- Ordinary safe/text check-ins must not store precise coordinates.
- `precision_level='precise'` is allowed only for an explicitly approved task-linked map/location handoff.
- Expired or revoked events must not appear as live certainty in Group UI.
- Retention must remain bounded and aligned with file `29`.
- This table must follow `CONTRACTS/group_presence_privacy_contract.yaml`.

## 4.9 Regroup pins table
### `group_regroup_pins`
Represents leader-posted regroup anchors.

Earlier specs allowed regroup pins to be encoded as special check-ins. That is too ambiguous for long-term analytics, lifecycle rules, map integration, and AI-agent implementation safety.

Minimum columns:
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `posted_by_user_id uuid not null references auth.users(id)`
- `label text not null`
- `text_pin text not null`
- `map_anchor_ref text null`
- `is_active boolean not null default true`
- `created_at timestamptz not null default now()`
- `expires_at timestamptz null`
- `metadata jsonb not null default '{}'::jsonb`

Indexes:
- index on `(group_id, created_at desc)`
- index on `(group_id, is_active)`

Rule: only leaders may create active regroup pins for their group.

## 4.10 Group itineraries table
### `group_itineraries`
Represents optional shared itinerary content for a group.

Minimum columns:
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `day date not null`
- `body jsonb not null`
- `updated_at timestamptz not null default now()`
- `updated_by_user_id uuid null references auth.users(id)`

Constraints:
- unique `(group_id, day)`

Indexes:
- index on `(group_id, day)`

Rule: itinerary content is leader-managed or service-managed and read-only to regular members unless a future approved feature changes that.

---

# 5. Canonical device-local entity model

The server schema is intentionally small. The following data is canonical on device.

## 5.1 Ritual sessions
### `ritual_sessions`
Represents local ritual progress state.

Minimum fields:
- `id uuid`
- `mode text`
- `path text`
- `madhhab text`
- `current_step_id text`
- `started_at datetime`
- `updated_at datetime`
- `completed_at datetime?`
- `status text`

Constraints:
- `mode in ('umrah','hajj')`
- `status in ('ACTIVE','PAUSED','COMPLETED','ABANDONED')`

## 5.2 RIC findings
### `ric_findings`
Represents local results produced by the ritual integrity checker.

Minimum fields:
- `id uuid`
- `ritual_session_id uuid`
- `status text`
- `finding_code text`
- `remedies_json text/json`
- `created_at datetime`
- `content_version text`

Rule: RIC findings are local by default. They may reference governed content IDs but should not upload private ritual state to the server.

## 5.3 Saved anchors
### `saved_anchors`
Represents saved gates, landmarks, or pins.

Minimum fields:
- `id uuid`
- `kind text`
- `label text`
- `gate_number text?`
- `level text?`
- `zone text?`
- `lat double?`
- `lng double?`
- `created_at datetime`
- `updated_at datetime`
- `photo_ref text?`
- `notes text?`

Constraints:
- `kind in ('GATE','LANDMARK','PIN')`

Rule: saved anchors are device-local by default unless explicitly shared through a user-initiated action.

## 5.4 Planner items
### `planner_items`
Represents local planning tasks.

Minimum fields:
- `id uuid`
- `title text`
- `description text?`
- `date date?`
- `time time?`
- `status text`
- `source text?`
- `created_at datetime`
- `updated_at datetime`

## 5.5 Notes and bookmarks
### `notes`
User-authored local notes.

### `bookmarks`
References to app content or user-relevant items.

Rule: no hidden sync. No server-backed notes/bookmarks unless future specs explicitly revise product and privacy boundaries.

## 5.6 Medical profile
### `medical_profile`
Local restricted emergency-support data.

Rule: medical profile must remain local-only by default and use stronger local protection as described in files `22` and `29`.

## 5.7 Pack inventory
### `pack_inventory`
Local record of installed, failed, purged, or downloading packs.

Rule: a pack cannot be marked installed unless verification succeeds under file `15`.

---

# 6. RLS policy requirements

## 6.1 General rule
RLS must be enabled on all user-scoped and group-scoped server tables.

## 6.2 Profiles
Users may read and update their own profile according to approved fields.

## 6.3 Entitlements
Users may read their own normalized entitlement state. Users may not directly write entitlement state. Entitlement writes happen through trusted backend/store validation flows.

## 6.4 Purchase receipts
Users may read limited normalized purchase/restore state where needed. Raw operational validation details should remain service-only.

## 6.5 Groups
Users may read groups where they have active membership. Leaders may update approved group metadata where feature scope allows. Group creation must be performed by a trusted endpoint that creates group and initial leader membership atomically.

## 6.6 Group members
Users may read membership rows for groups where they are active members. Leaders may perform approved membership management actions. Users may not escalate their own role.

## 6.7 Group check-ins
Active group members may read check-ins for their group. Active group members may create their own check-ins. Users may not create check-ins for other users.

## 6.8 Group presence events
Active group members may read presence events for their group where retention and visibility rules allow. Active group members may create only their own explicit-user-action events through trusted endpoints. Users may not create, revoke, or alter presence events for other users unless a future approved leader/admin workflow explicitly allows it. Expired or revoked events should not be returned in live-board queries as current state.

## 6.9 Regroup pins
Active group members may read regroup pins for their group. Only active leaders may create or update active regroup pins.

## 6.10 Group itineraries
Active group members may read group itinerary rows. Only active leaders or approved service roles may write itinerary rows.

---

# 7. Hard invariants

| ID | Invariant |
|---|---|
| **I-001** | Every `profiles` row belongs to exactly one `auth.users` identity |
| **I-010** | Users cannot read/write group data for groups they are not an active member of |
| **I-011** | Users cannot assign themselves leader role |
| **I-012** | Only active leaders may create regroup pins |
| **I-013** | Group codes are exactly 6 uppercase alphanumeric characters, globally unique, and server-generated |
| **I-014** | Group creation must create `groups` and initial active `LEADER` membership transactionally |
| **I-015** | Group presence events must be explicit-user-action, TTL-bound, and never treated as a hidden tracking trail |
| **I-016** | `group_presence_events.id` is the persisted primary key exposed as API `event_id` unless a synchronized contract migration changes it |
| **I-017** | `text_pin` presence for group presence events is conditional on `event_type` and must match `CONTRACTS/group_presence_privacy_contract.yaml` |
| **I-020** | Server-side entitlement state is authoritative; client may never invent or extend it |
| **I-030** | A pack must not be marked `INSTALLED` until verification succeeds |
| **I-040** | `ric_status=VALID` is impossible when a required pillar is missing |
| **I-050** | Medical profile is local-only by default — never synced |

---

# 8. Canonical enums

## 8.1 Server enums
```text
entitlement_tier:    FREE | SUPPORTER
entitlement_source:  NONE | APPLE | GOOGLE | PROMO | FAMILY
group_member_role:   LEADER | MEMBER
group_member_status: ACTIVE | LEFT | REMOVED
group_season_scope:  UMRAH | HAJJ | MIXED
checkin_kind:        SAFE | CHECKIN | STATUS
presence_event_type: safe_checkin | text_checkin | regroup_pin | route_handoff
presence_precision:  none | coarse | precise
freshness_status:    fresh | stale | expired | revoked
```

## 8.2 Local enums
```text
ritual_mode:   umrah | hajj
ritual_path:   Umrah | Tamattu | Qiran | Ifrad
madhhab:       Hanafi | Shafii | Maliki | Hanbali
ric_status:    VALID | MISSING_PILLAR | MISSING_WAJIB | REMEDY_REQUIRED
anchor_kind:   GATE | LANDMARK | PIN
pack_state:    NOT_INSTALLED | DOWNLOADING | VERIFYING | INSTALLED | FAILED | PURGED
```

---

# 9. Migration discipline

## 9.1 Additive-first rule
Prefer additive migrations:
- add nullable column,
- backfill safely,
- deploy code that reads both old/new where needed,
- tighten constraints later.

## 9.2 Destructive-change rule
Destructive changes require written rationale, rollback plan, fixture updates, release gate review, and migration evidence.

## 9.3 Enum-change rule
Enum changes require synchronized updates in file `13`, file `14`, Flutter models, fixtures, analytics, tests, relevant feature docs, and affected contract artifacts.

## 9.4 RLS migration rule
RLS changes are high-risk. They require explicit tests proving users cannot access unauthorized rows.

## 9.5 Group presence contract migration rule
Any change to `group_presence_events` identifiers, freshness state, precision, conditional text/map fields, TTL, retention, or visibility must update this file, file `14`, file `20`, `CONTRACTS/group_presence_privacy_contract.yaml`, fixtures, RLS tests, and release evidence together.

---

# 10. Seeds and fixtures

## 10.1 Seed data purpose
Seed data exists for development and tests, not production truth.

## 10.2 Required fixture families
Fixtures should cover:
- free user,
- Supporter user,
- expired Supporter user,
- group leader,
- group member,
- removed member,
- group with active regroup pin,
- stale group state,
- local-only ritual session,
- local-only medical profile,
- pack states,
- content version references.

## 10.3 Group presence fixture requirements
Group presence fixtures should include:
- `safe_checkin` without required freeform `text_pin`,
- `text_checkin` with `text_pin`,
- `regroup_pin` with `text_pin` and `map_anchor_ref`,
- `route_handoff` with `map_anchor_ref`,
- fresh, stale, expired, and revoked states,
- current API payload field `event_id` mapped from database `id`.

## 10.4 Privacy rule
Fixtures must not contain real private user data.

---

# 11. Retention and deletion posture

## 11.1 Server data
Server data retention is governed by file `29`.

## 11.2 Local data
Local data deletion is controlled by user actions and app uninstall semantics, subject to platform behavior.

## 11.3 Account deletion
If server account deletion is requested, server-backed data must follow file `29` and file `14` deletion/status endpoint contracts.

Do not promise immediate deletion of records that must be retained for purchase, accounting, fraud-prevention, security, backup, or legal reasons.

## 11.4 Group presence retention
Group presence events must be retained only as long as needed for coordination, safety, abuse prevention, or incident/legal requirements. Ordinary presence/freshness data must not quietly become long-term behavior history.

---

# 12. Definition of done

This data model is ready when:
- server/local ownership is clear,
- RLS policies exist and are tested,
- hard invariants are enforceable,
- migrations are additive or reviewed,
- fixtures cover key states,
- API contracts match the schema,
- feature specs match data truth,
- privacy boundaries match file `29`,
- release evidence exists for high-risk data changes.

---

# 13. AI-agent checklist

Before editing data-related code, an AI agent must:
1. Read files `01`, `13`, `14`, `20`, `24`, `29`, and `31` where relevant.
2. Check affected machine-readable contracts in `SPECS/CONTRACTS/`.
3. Identify server vs local ownership.
4. Check RLS implications.
5. Check migration safety.
6. Update fixtures and tests.
7. Update API and feature docs if schema truth changes.
8. Avoid adding server storage for local-private data without explicit approval.

---

# Quality-first amendment — group creation and presence model

This section records the direct data-model alignment required by file `31`, file `20`, and `CONTRACTS/group_presence_privacy_contract.yaml`.

## A. Governed group creation
Group creation is a server-backed transactional operation. A successful group creation must produce:
- one `groups` row,
- one active `group_members` row for the requester,
- requester role `LEADER`,
- a server-generated 6-character uppercase alphanumeric code,
- auditable timestamps and request correlation where available.

The client must not choose the canonical group code, invent membership, or assign leader privilege locally.

## B. Group presence privacy
Any normalized freshness or presence event must follow `CONTRACTS/group_presence_privacy_contract.yaml`.

The data layer must preserve these privacy properties:
- foreground-first, user-action-linked sharing,
- no passive location history,
- TTL-bound freshness,
- explicit stale/expired/revoked states,
- no raw precise location in ordinary check-ins,
- bounded retention.

## C. RLS posture
RLS policies for group data must enforce:
- members can read group rows only for active memberships,
- leaders can perform leader-only writes only for their active group,
- group creation assigns leader role transactionally,
- group presence/check-in/regroup records are readable only to active group members unless a future approved public handoff contract exists,
- deleted/left/removed members lose access according to membership status rules.

## D. Migration posture
Adding `group_presence_events` is additive. Existing `group_checkins` and `group_regroup_pins` remain valid and must not be collapsed into one overloaded table.

# 19. Guide Marketplace conceptual data and RLS amendment

This section defines canonical relational intent for file `32`. It does **not** create a migration in this specification task.

## 19.1 `guide_provider_profiles`
Server-backed provider domain linked to the existing authenticated identity.

Minimum conceptual ownership:
- `user_id` references the existing authenticated user;
- provider-editable public profile fields are self-owned;
- lifecycle, moderation, public-eligibility, and verification fields are service-managed.

A provider profile is not a second authentication identity and not a client-trusted role toggle.

## 19.2 `guide_credentials`
Stores normalized credential/authorization verification metadata.

Conceptual fields include:
- credential id and provider id,
- credential type,
- source authority,
- masked/public reference where legally required,
- verification method/state,
- verified-at timestamp,
- issue/expiry/re-check timestamp where applicable,
- evidence disposition/reference only when retention is necessary,
- suspension/revocation metadata.

Raw credential or identity evidence is **restricted** and must not be placed in public rows or ordinary app-profile fields. Prefer authoritative verification plus retained result metadata over permanent document storage.

## 19.3 `guide_listings`
Stores narrowly scoped guide-service listings.

Conceptual fields include:
- provider/listing ids,
- approved service type,
- localized title/description,
- service area,
- languages,
- group-size capability,
- structured price/currency/pricing unit/fees,
- inclusions/exclusions,
- availability summary,
- listing/moderation state,
- timestamps/revision metadata.

V1 must not model visa, hotel, transport, package, ticketing, or broad-tour inventory through this table.

## 19.4 `guide_contact_channels`
Stores approved provider contact-channel targets and visibility/resolution metadata.

Raw contact targets must not be included in broad public browse/search payloads by default. A server-resolved handoff may reveal only the minimum current approved target after eligibility re-check.

## 19.5 `guide_verification_events`
Append-oriented service-managed audit history for verification, suspension, revocation, expiry, re-verification, and other trust-state transitions.

Ordinary users/providers cannot mutate this history.

## 19.6 `guide_reports`
Restricted trust-and-safety reports.

Report bodies and internal moderation notes are not public and are not ordinary analytics. RLS must prevent reporters/providers/public users from reading unrelated restricted report content.

## 19.7 Optional `guide_contact_intents`
May record minimal explicit contact-intent/audit/anti-abuse metadata if legal/privacy review demonstrates a real purpose.

Do not create it merely to improve analytics, and never store external conversation bodies.

## 19.8 Explicitly absent from V1
Do not create guide-domain tables for:
- bookings,
- payments,
- transactions,
- escrow,
- disputes,
- chat messages,
- ratings/reviews.

## 19.9 Public eligibility invariant
A public guide/listing query must be enforceable from server-trusted state. Public discoverability requires all applicable conditions from `CONTRACTS/guide_marketplace_trust_contract.yaml`, including current mandatory credentials, active approved listing, no suspension/revocation/expiry, enabled service type, and resolved legal release gates.

Provider/client code cannot override public eligibility.

## 19.10 RLS invariants
RLS/authorization must prove:
- providers edit only their own allowed self-service fields;
- providers cannot self-set verification, credential validity, suspension/revocation, or public eligibility;
- public reads expose only eligible records and explicitly public trust metadata;
- restricted credential evidence is never public;
- verification events are service-managed;
- report details are restricted;
- ineligible provider/listing rows cannot leak through alternate public queries;
- service-role moderation/verification writes are auditable.

The app must never rely on Flutter visibility as the enforcement boundary.

---

End of file.
