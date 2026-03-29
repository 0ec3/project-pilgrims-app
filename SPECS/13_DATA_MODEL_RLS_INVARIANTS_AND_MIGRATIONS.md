# 13 — DATA MODEL, RLS, INVARIANTS, AND MIGRATIONS

## Document status
- **Type:** Normative data architecture and database contract document
- **Priority:** Highest
- **Audience:** Backend engineers, Flutter engineers, tech lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical server-side and device-local data model for the app, including entity ownership, relationships, row-level security, invariants, migration rules, seeds, fixtures, and data-retention boundaries.
- **Authority level:** This file is the canonical source of truth for relational schema, local persistence shape, authorization boundaries at the data layer, and migration discipline. If code, APIs, or feature docs diverge from this file, this file wins unless superseded through documented change control.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `02-AI-AGENT-RULES-AND-WORKFLOW.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`
- **Related files:** `10`, `11`, `12`, `14`, `15`, `16`, `17`, `18`–`26`, `27`, `28`, `29`, `30`

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

### Canonical server domains
- account profile metadata
- entitlement state
- group records
- group membership
- group check-ins
- regroup pins
- optional group itinerary content
- server-side purchase validation records
- minimal audit fields required for correctness and operations

## 3.2 Device-local persistent data
The device stores local-first support data.

### Canonical device-local domains
- ritual sessions and RIC findings
- saved gates / saved anchors
- planner items and local reminders
- notes and bookmarks
- local wallet artifacts; V1 remains device-local unless a later approved sync/export contract explicitly changes this
- emergency / medical profile
- pack inventory and installation state
- local settings and UX dismissals
- cached flags / manifest snapshots
- lightweight map/local search indexes where needed

For V1, wallet artifacts remain device-local by default.
Do not add a server-backed wallet domain unless product, privacy, data-model, and API contracts are explicitly revised together.

## 3.3 Derived or ephemeral data
This data may exist temporarily or be regenerated.

Examples:
- in-memory live board lists
- transient route results
- temporary upload/download states
- analytics event queues before flush

---

# 4. Canonical server-side entity model

## 4.1 Identity source
### `auth.users`
This is the canonical authentication identity table managed by Supabase Auth.

### Rule
Do not duplicate email/phone/password identity ownership in a separate custom table unless a future documented reason requires it.

## 4.2 App profile table
### `profiles`
Stores app-specific user metadata linked 1:1 with `auth.users`.

### Purpose
- display name
- locale preferences if server-backed
- support metadata for group display
- optional phone display/masking metadata if needed
- account lifecycle timestamps

### Minimum columns
- `id uuid primary key references auth.users(id) on delete cascade`
- `display_name text null`
- `phone_display text null`
- `avatar_url text null` (optional; not required for MVP)
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Indexes
- primary key on `id`
- optional index on `created_at`

## 4.3 Entitlements table
### `user_entitlements`
Stores trusted, server-validated entitlement state.

### Purpose
This replaces fragile client-side assumptions and is more future-safe than hiding everything in one `premium_until` column.

### Minimum columns
- `user_id uuid primary key references auth.users(id) on delete cascade`
- `tier text not null default 'FREE'`
- `active_until timestamptz null`
- `source text not null default 'NONE'`
- `family_group_id text null`
- `last_validated_at timestamptz null`
- `gates jsonb not null default '{}'::jsonb`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Notes
- `tier` is the human-readable entitlement tier.
- `active_until` is the current trusted paid-access cutoff where applicable.
- `gates` is a server-computed snapshot for client convenience, not the conceptual source of business policy.
- Feature docs and API docs may expose a simplified representation, but this table is the persistence truth.

### Indexes
- primary key on `user_id`
- index on `(tier)` if needed for admin/reporting only
- optional partial index on `(active_until)` for active subscription operations

## 4.4 Purchase validation records
### `purchase_receipts`
Stores server-side receipt validation history.

### Purpose
- audit successful and failed validation attempts
- reconcile store events and restore flows
- support entitlement debugging and fraud handling

### Minimum columns
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

### Constraints
- unique `(platform, transaction_id)`

### Rule
Do not store raw sensitive store payloads casually if a reference or normalized summary is sufficient.

## 4.5 Groups table
### `groups`
Represents a pilgrim coordination group.

### Minimum columns
- `id uuid primary key default gen_random_uuid()`
- `code text not null unique`
- `name text not null`
- `leader_user_id uuid not null references auth.users(id)`
- `season_scope text not null default 'UMRAH'`
- `created_at timestamptz not null default now()`
- `updated_at timestamptz not null default now()`

### Constraints
- `check (length(code) = 6 and code ~ '^[A-Z0-9]+$')`
- `check (season_scope in ('UMRAH','HAJJ','MIXED'))`

### Indexes
- unique index on `(code)`
- index on `(leader_user_id)`

## 4.6 Group membership table
### `group_members`
Represents membership and role of users inside groups.

### Minimum columns
- `group_id uuid not null references groups(id) on delete cascade`
- `user_id uuid not null references auth.users(id) on delete cascade`
- `role text not null`
- `joined_at timestamptz not null default now()`
- `status text not null default 'ACTIVE'`
- `display_alias text null`
- primary key `(group_id, user_id)`

### Constraints
- `check (role in ('LEADER','MEMBER'))`
- `check (status in ('ACTIVE','LEFT','REMOVED'))`

### Indexes
- index on `(user_id)`
- index on `(group_id, role)`
- index on `(group_id, status)`

### Rule
There must always be exactly one active logical leader for a group, enforced by group/role consistency rules.

## 4.7 Group check-ins table
### `group_checkins`
Represents lightweight group-presence or “I’m Safe” activity.

### Minimum columns
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `user_id uuid not null references auth.users(id) on delete cascade`
- `kind text not null default 'SAFE'`
- `text_pin text not null`
- `client_event_id uuid null`
- `created_at timestamptz not null default now()`
- `metadata jsonb not null default '{}'::jsonb`

### Constraints
- `check (kind in ('SAFE','CHECKIN','STATUS'))`

### Indexes
- index on `(group_id, created_at desc)`
- index on `(group_id, user_id, created_at desc)`
- index on `(client_event_id)` where not null

### Rule
Check-ins are text-based coordination events. They do not imply GPS tracking.

## 4.8 Regroup pins table
### `group_regroup_pins`
Represents leader-posted regroup anchors.

### Why this table exists
Earlier specs allowed regroup pins to be encoded as special check-ins. That is too ambiguous for long-term analytics, lifecycle rules, map integration, and AI-agent implementation safety.

### Minimum columns
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

### Indexes
- index on `(group_id, created_at desc)`
- index on `(group_id, is_active)`

### Rule
Only leaders may create active regroup pins for their group.

## 4.9 Group itineraries table
### `group_itineraries`
Represents optional shared itinerary content for a group.

### Minimum columns
- `id uuid primary key default gen_random_uuid()`
- `group_id uuid not null references groups(id) on delete cascade`
- `day date not null`
- `body jsonb not null`
- `updated_at timestamptz not null default now()`
- `updated_by_user_id uuid null references auth.users(id)`

### Constraints
- unique `(group_id, day)`

### Indexes
- index on `(group_id, day)`

### Rule
Itinerary content is leader-managed or service-managed and read-only to regular members unless a future approved feature changes that.

---

# 5. Canonical device-local entity model

The server schema is intentionally small. The following data is canonical on device.

## 5.1 Ritual sessions
### `ritual_sessions`
Represents local ritual progress state.

### Minimum fields
- `id uuid`
- `mode text`  
- `path text`
- `madhhab text`
- `current_step_id text`
- `started_at datetime`
- `updated_at datetime`
- `completed_at datetime?`
- `status text`

### Constraints
- `mode in ('umrah','hajj')`
- `status in ('ACTIVE','PAUSED','COMPLETED','ABANDONED')`

## 5.2 RIC findings
### `ric_findings`
Represents local results produced by the ritual integrity checker.

### Minimum fields
- `id uuid`
- `ritual_session_id uuid`
- `status text`
- `finding_code text`
- `remedies_json text/json`
- `created_at datetime`

### Rule
RIC findings are local operational data unless a future server-backed feature explicitly requires sync.

## 5.3 Saved anchors
### `saved_anchors`
Represents Save My Gate and other user-saved orientation anchors.

### Minimum fields
- `id uuid`
- `kind text`
- `short_code text`
- `title text`
- `level text null`
- `zone text null`
- `landmark_text text null`
- `photo_uri text null`
- `created_at datetime`
- `updated_at datetime`

### Constraints
- `kind in ('GATE','LANDMARK','PIN')`

## 5.4 Planner items
### `planner_items`
Represents local planning and reminder objects.

### Minimum fields
- `id uuid`
- `date_key text`
- `time_local text null`
- `type text`
- `title text`
- `note text null`
- `notification_enabled bool`
- `source text`
- `created_at datetime`
- `updated_at datetime`

## 5.5 Notes
### `notes`
Represents local notes.

### Minimum fields
- `id uuid`
- `title text`
- `body_md text`
- `source_kind text null`
- `source_ref text null`
- `created_at datetime`
- `updated_at datetime null`
- `supporter_features_used bool`

## 5.6 Note attachments
### `note_attachments`
Represents local attachment metadata for notes.

### Minimum fields
- `id uuid`
- `note_id uuid`
- `mime text`
- `uri text`
- `size_bytes int`
- `created_at datetime`

## 5.7 Bookmarks
### `bookmarks`
Represents local bookmarks.

### Minimum fields
- `id uuid`
- `kind text`
- `ref text`
- `title text`
- `created_at datetime`

## 5.8 Medical profile
### `medical_profile`
Represents device-only emergency/medical information.

### Minimum fields
- `id int/singleton`
- `ciphertext blob/text`
- `updated_at datetime`

### Rule
Medical profile data never syncs by default.

## 5.9 Pack inventory
### `pack_inventory`
Represents local pack installation state.

### Minimum fields
- `pack_id text`
- `type text`
- `version int`
- `checksum text`
- `state text`
- `installed_at datetime null`
- `size_bytes int`
- `purgeable bool`
- `last_error_code text null`

### Constraints
- `state in ('NOT_INSTALLED','DOWNLOADING','VERIFYING','INSTALLED','FAILED','PURGED')`

## 5.10 Cached flags and manifest snapshots
### `remote_cache_snapshots`
Represents last-good local cache for flags/manifest/config.

### Minimum fields
- `key text primary key`
- `etag text null`
- `payload text`
- `fetched_at datetime`
- `expires_at datetime null`

---

# 6. Canonical enums and dictionaries

These values are authoritative. Any change here requires synchronized updates in schema, API, Flutter models, fixtures, tests, and analytics.

## 6.1 Server enums
- `entitlement_tier`: `FREE`, `SUPPORTER`
- `entitlement_source`: `NONE`, `APPLE`, `GOOGLE`, `PROMO`, `FAMILY`
- `group_member_role`: `LEADER`, `MEMBER`
- `group_member_status`: `ACTIVE`, `LEFT`, `REMOVED`
- `group_season_scope`: `UMRAH`, `HAJJ`, `MIXED`
- `checkin_kind`: `SAFE`, `CHECKIN`, `STATUS`

## 6.2 Local enums
- `mode`: `umrah`, `hajj`
- `path`: `Umrah`, `Tamattu`, `Qiran`, `Ifrad`
- `madhhab`: `Hanafi`, `Shafii`, `Maliki`, `Hanbali`
- `ric_status`: `VALID`, `MISSING_PILLAR`, `MISSING_WAJIB`, `REMEDY_REQUIRED`
- `anchor_kind`: `GATE`, `LANDMARK`, `PIN`
- `pack_state`: `NOT_INSTALLED`, `DOWNLOADING`, `VERIFYING`, `INSTALLED`, `FAILED`, `PURGED`

## 6.3 Enum rule
Do not create ad hoc string literals in code. Centralize shared enum definitions and serializers.

---

# 7. Relationship model

## 7.1 Core server relationships
- `auth.users 1—1 profiles`
- `auth.users 1—1 user_entitlements`
- `auth.users 1—* purchase_receipts`
- `auth.users 1—* groups` via `groups.leader_user_id`
- `groups *—* auth.users` via `group_members`
- `groups 1—* group_checkins`
- `groups 1—* group_regroup_pins`
- `groups 1—* group_itineraries`

## 7.2 Local relationship examples
- `ritual_sessions 1—* ric_findings`
- `notes 1—* note_attachments`
- bookmarks and saved anchors may point to cross-module refs by value, not by foreign key

## 7.3 Reference rule for local models
Local feature models may reference source objects by stable `source_kind` + `source_ref` rather than requiring hard relational coupling across all local tables.

---

# 8. Hard invariants

These are rules that must always remain true.

## 8.1 Identity and ownership
- **I-001:** Every `profiles` row belongs to exactly one `auth.users` identity.
- **I-002:** Every `user_entitlements` row belongs to exactly one `auth.users` identity.

## 8.2 Group membership and leadership
- **I-010:** A user cannot read or write group-scoped data for a group they are not a member of.
- **I-011:** A check-in requires active membership in the target group.
- **I-012:** A regroup pin requires active leader membership in the target group.
- **I-013:** `groups.code` must be exactly 6 uppercase alphanumeric characters and unique.
- **I-014:** A group’s `leader_user_id` must correspond to an active `group_members` row with role `LEADER`.

## 8.3 Entitlements
- **I-020:** Trusted server-side entitlement state is authoritative.
- **I-021:** The client may cache entitlement snapshots but may not invent or extend them.
- **I-022:** Free-vs-paid policy decisions are product-governed; the database only stores current trusted access state.

## 8.4 Packs and offline assets
- **I-030:** A pack must not be marked installed until checksum verification succeeds.
- **I-031:** Purged packs must not remain discoverable as installed in local inventory state.

## 8.5 Ritual and RIC
- **I-040:** `ric_status=VALID` is impossible when a required pillar is missing.
- **I-041:** When `mode=umrah`, Hajj-only planning or content fixtures must not leak into the session.

## 8.6 Privacy and locality
- **I-050:** Medical profile remains local-only by default.
- **I-051:** Notes, bookmarks, saved anchors, and local planner data remain local unless a future approved feature explicitly changes the contract.

---

# 9. Row-level security architecture

## 9.1 RLS policy goals
RLS must guarantee that:
- users can only see their own profile and entitlement rows,
- group data is only visible to active members,
- leader actions are only available to active leaders,
- service-only tables are not exposed directly to end users,
- policy logic remains testable and performant.

## 9.2 Tables that must have RLS enabled
- `profiles`
- `user_entitlements`
- `groups`
- `group_members`
- `group_checkins`
- `group_regroup_pins`
- `group_itineraries`
- `purchase_receipts`

## 9.3 General RLS implementation rules
- Enable RLS explicitly on every user-facing table.
- Avoid granting direct broad access to `anon` or `authenticated` roles outside policy design.
- Keep policy logic as simple and index-friendly as possible.
- Use explicit helper functions only when they improve clarity and are audited.
- Treat service-role access as privileged and outside normal user policy paths.

## 9.4 Performance rule for RLS
Columns referenced in RLS predicates must be indexed when they are not already covered by primary or unique keys.

## 9.5 Owner-bypass rule
Be aware that table owners can bypass RLS unless the table is configured to force row security where appropriate. This must be considered in admin/service-role design.

## 9.6 BYPASSRLS rule
Application roles must not use BYPASSRLS. Only tightly controlled administrative/service contexts may bypass row security when absolutely necessary.

---

# 10. RLS policy matrix

## 10.1 `profiles`
### Read
User may read only own row.

### Update
User may update only own row, subject to field restrictions if implemented.

### Insert
Usually service-managed at signup/profile bootstrap.

## 10.2 `user_entitlements`
### Read
User may read only own row.

### Update/insert/delete
Only trusted backend/service role may write.

## 10.3 `purchase_receipts`
### Read
User may read own receipt history only if product needs it; otherwise keep service-only.

### Write
Only trusted backend/service role writes.

## 10.4 `groups`
### Read
Active members may read their groups.

### Insert
Group creation may be allowed to authenticated users through trusted flows.

### Update
Only active leaders may update editable group fields.

## 10.5 `group_members`
### Read
Active members of a group may read membership rows for their group.

### Insert
Join flow writes must be controlled by trusted backend logic or tightly controlled policies.

### Update/delete
Only trusted backend or leader-authorized flows where explicitly allowed.

## 10.6 `group_checkins`
### Read
Active members of the same group may read check-ins for their group.

### Insert
Only active members of the same group may insert their own check-ins.

### Update/delete
Generally disallowed for end users after insert.

## 10.7 `group_regroup_pins`
### Read
Active members of the same group may read active regroup pins.

### Insert/update
Only active leaders of the same group may create or manage regroup pins.

## 10.8 `group_itineraries`
### Read
Active members of the same group may read itineraries.

### Write
Only active leaders or trusted service paths may write.

---

# 11. Example RLS implementation outline

This section is illustrative and should be kept aligned with actual migration SQL.

```sql
alter table public.profiles enable row level security;
alter table public.user_entitlements enable row level security;
alter table public.groups enable row level security;
alter table public.group_members enable row level security;
alter table public.group_checkins enable row level security;
alter table public.group_regroup_pins enable row level security;
alter table public.group_itineraries enable row level security;
alter table public.purchase_receipts enable row level security;

create policy profiles_self_select on public.profiles
for select using (id = auth.uid());

create policy profiles_self_update on public.profiles
for update using (id = auth.uid());

create policy entitlements_self_select on public.user_entitlements
for select using (user_id = auth.uid());

create policy groups_member_select on public.groups
for select using (
  exists (
    select 1 from public.group_members gm
    where gm.group_id = groups.id
      and gm.user_id = auth.uid()
      and gm.status = 'ACTIVE'
  )
);

create policy groups_leader_update on public.groups
for update using (
  exists (
    select 1 from public.group_members gm
    where gm.group_id = groups.id
      and gm.user_id = auth.uid()
      and gm.role = 'LEADER'
      and gm.status = 'ACTIVE'
  )
);

create policy members_group_select on public.group_members
for select using (
  exists (
    select 1 from public.group_members gm
    where gm.group_id = group_members.group_id
      and gm.user_id = auth.uid()
      and gm.status = 'ACTIVE'
  )
);

create policy checkins_group_select on public.group_checkins
for select using (
  exists (
    select 1 from public.group_members gm
    where gm.group_id = group_checkins.group_id
      and gm.user_id = auth.uid()
      and gm.status = 'ACTIVE'
  )
);

create policy checkins_member_insert on public.group_checkins
for insert with check (
  user_id = auth.uid()
  and exists (
    select 1 from public.group_members gm
    where gm.group_id = group_checkins.group_id
      and gm.user_id = auth.uid()
      and gm.status = 'ACTIVE'
  )
);

create policy regroup_member_select on public.group_regroup_pins
for select using (
  exists (
    select 1 from public.group_members gm
    where gm.group_id = group_regroup_pins.group_id
      and gm.user_id = auth.uid()
      and gm.status = 'ACTIVE'
  )
);

create policy regroup_leader_write on public.group_regroup_pins
for insert with check (
  posted_by_user_id = auth.uid()
  and exists (
    select 1 from public.group_members gm
    where gm.group_id = group_regroup_pins.group_id
      and gm.user_id = auth.uid()
      and gm.role = 'LEADER'
      and gm.status = 'ACTIVE'
  )
);
```

---

# 12. Indexing and performance rules

## 12.1 Required server indexes
At minimum:
- `groups(code)` unique
- `groups(leader_user_id)`
- `group_members(user_id)`
- `group_members(group_id, role)`
- `group_members(group_id, status)`
- `group_checkins(group_id, created_at desc)`
- `group_checkins(group_id, user_id, created_at desc)`
- `group_regroup_pins(group_id, is_active)`
- `group_itineraries(group_id, day)` unique
- `purchase_receipts(platform, transaction_id)` unique

## 12.2 RLS index rule
Any column used in frequent RLS predicates must have an appropriate index unless already covered by a strong existing key.

## 12.3 Local index guidance
Local stores should index:
- notes by `created_at`
- bookmarks by `(kind, ref)`
- planner items by `date_key`
- saved anchors by `short_code`
- pack inventory by `state`

---

# 13. Data retention and deletion rules

## 13.1 Server retention
- group check-ins: short retention window by default, such as 60 days
- regroup pins: expired and inactive pins may be purged on a shorter retention schedule
- purchase receipts: retain as needed for entitlement audit and compliance
- itineraries: retain according to product policy or leader archival settings if later introduced

## 13.2 Local retention
- local notes, bookmarks, planner items, and saved anchors remain until user deletes them
- packs are purgeable
- medical profile remains until explicit deletion

## 13.3 Deletion rule
Deletion behavior must be explicit. Do not silently purge user-private local data without user action unless a documented storage-recovery policy clearly allows it.

---

# 14. Migration architecture

## 14.1 Migration goals
Migrations must be:
- version-controlled
- reviewable
- reproducible
- testable
- rollback-aware
- safe for AI-agent execution

## 14.2 Migration source of truth
Database schema changes must be introduced through migration files committed to source control.

## 14.3 Migration environments
Schema changes must be tested through at least:
- local/dev database
- staging/preview branch database
- production deployment pipeline

## 14.4 Branching rule
Use isolated preview/branch environments for schema experiments and PR validation before production rollout.

## 14.5 CI/CD rule
Production migrations should be deployed through CI/CD, not hand-applied from a contributor laptop.

---

# 15. Migration playbook

## 15.1 General migration rule
Never edit production tables ad hoc. Every schema change must have a migration and related doc updates.

## 15.2 Additive-first migration sequence
Preferred order:
1. add new nullable column / table / index
2. deploy code that can read both old and new states if needed
3. backfill data where necessary
4. switch writes to new shape
5. remove old shape only after validation and deprecation window if applicable

## 15.3 Migration PR must include
- migration SQL file(s)
- this doc updated
- API doc updates if payloads change
- affected feature doc updates
- fixture updates
- tests updated
- rollback or mitigation notes

## 15.4 Dangerous migrations requiring extra review
- dropping columns or tables
- enum/value changes used by clients
- RLS policy changes
- changing ownership or foreign-key rules
- changing entitlement persistence model
- changing group membership semantics

## 15.5 Local-store migration rule
Local DB migrations must also be versioned and tested. Local model changes must not silently corrupt or orphan on-device user data.

---

# 16. Migration examples

## 16.1 Safe additive server change example
Add `location_hint text null` to `group_checkins`.

Required steps:
- migration adds column
- API contract updated if request/response shape changes
- Flutter model updated
- tests updated
- no RLS change if permissions unchanged

## 16.2 Safe local change example
Add `note` to `planner_items`.

Required steps:
- local DB migration
- feature doc update
- migration test with existing rows
- no server impact

## 16.3 Breaking server change example
Replace `group_regroup_pins.text_pin` with structured map anchor object.

Required steps:
- additive new columns first
- backfill/compat adapter
- API versioning or additive compatibility
- map and group feature updates
- migration/release plan documented
- removal delayed until clients are migrated

---

# 17. Seed data and fixtures

## 17.1 Dev seed minimums
- 3 authenticated users
- 1 group with 1 leader + multiple members
- sample entitlement states: free + supporter
- 10 recent check-ins across a short window
- 1 active regroup pin
- 1 itinerary day
- flags snapshot with `season=umrah`
- packs manifest snapshot

## 17.2 Test fixtures
### Server fixtures
- active member
- non-member
- leader
- free entitlement
- supporter entitlement
- expired entitlement
- duplicate join/check-in scenarios

### Local fixtures
- active ritual session
- valid and invalid RIC findings
- installed and failed packs
- free-cap and supporter notes scenarios
- emergency profile present/absent

## 17.3 Golden data rule
Golden snapshots must be regenerated intentionally and explain semantic changes.

---

# 18. Data-quality and test hooks

## 18.1 Required DB-level tests
- RLS enabled on required tables
- non-member cannot read or insert group data
- leader-only actions enforce correctly
- unique code constraints hold
- foreign keys enforce ownership
- local-only invariants remain local-only in server schema

## 18.2 Required integration tests
- `POST /v1/groups/join` idempotency
- `POST /v1/groups/{group_id}/checkins` membership enforcement
- entitlement restore and refresh flows
- group live board backfill + stream authorization
- manifest/flags caching contract

## 18.3 Required local-store tests
- pack inventory state machine migrations
- ritual session + RIC integrity
- notes/bookmarks caps and downgrade behavior
- planner migration resilience
- medical profile encryption wrapper behavior

---

# 19. Data-change impact matrix

## 19.1 If a server table changes
Update:
- this file
- `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
- affected feature-family file(s)
- `27-TESTING-STRATEGY-TEST-MATRIX-AND-DEVICE-LAB.md`
- `28-REAL-WORLD-VERIFICATION-RELEASE-GATES-AND-EVIDENCE.md`
- `05-ROADMAP-PROGRESS-AND-CHANGELOG.md`

## 19.2 If a local model changes
Update:
- this file
- affected feature-family file(s)
- Flutter/local persistence contracts in implementation docs if impacted
- test docs and fixtures
- changelog/progress if materially relevant

## 19.3 If an enum changes
Update:
- this file
- API doc if surfaced externally
- local and server serializers
- fixtures
- analytics doc if event payloads use it
- tests and snapshots

---

# 20. Recommendations adopted into this data model

## 20.1 Recommendation — use `auth.users` + `profiles`
The model now uses Supabase Auth as the identity root and separates app profile data from auth credentials.

## 20.2 Recommendation — dedicated regroup pins table
Regroup pins are now a first-class entity rather than an overloaded special check-in.

## 20.3 Recommendation — explicit entitlement table
Entitlements now have a more future-safe persistence model than a single overloaded timestamp field.

## 20.4 Recommendation — preserve local-only privacy by design
Sensitive and personal support data remains local by default unless future scope explicitly changes it.

## 20.5 Recommendation — migration discipline as architecture, not cleanup
Schema evolution is treated as a governed process to protect AI-agent reliability and release safety.

---

# 21. Anti-patterns forbidden by this data architecture

The following are forbidden unless explicitly approved.

## 21.1 Duplicating auth identity in a second credentials table
Forbidden.

## 21.2 Syncing private local support data to the server by default
Forbidden.

## 21.3 Client-derived entitlement truth
Forbidden.

## 21.4 Group authorization enforced only in app code
Forbidden.

## 21.5 Overloading regroup pins into generic check-ins without a documented contract
Forbidden.

## 21.6 Ad hoc production schema edits without migration files
Forbidden.

## 21.7 Enum changes without synchronized cross-doc updates
Forbidden.

## 21.8 RLS policies without indexing the relevant predicate columns where needed
Forbidden.

---

# 22. When this file must be updated

This file must be updated whenever any of the following changes:
- server table shape
- local persistence shape
- ownership rules
- group membership semantics
- entitlement persistence model
- regroup pin model
- RLS policy logic
- enum values
- migration policy
- retention rules
- seed/fixture strategy

If any of those evolve but this file is not updated, backend, Flutter, tests, and release validation will drift quickly.

---

# 23. Summary

This file defines the canonical data architecture for Pilgrims Mobile App.

It establishes:
- the split between server and device-local data
- the authoritative server schema
- the authoritative local model families
- the key relationships and enums
- hard invariants
- the RLS security model
- migration rules and rollout discipline
- seed data and fixture expectations
- the cross-file updates required whenever data truth changes

Its purpose is to make the system safe for:
- trusted group coordination
- ethical entitlement handling
- private local-first user support
- maintainable schema evolution
- and reliable AI-assisted implementation over time.

