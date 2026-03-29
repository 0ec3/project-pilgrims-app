# 15 — OFFLINE, PACKS, SYNC, ASSET DELIVERY, AND CACHE POLICY

## Document status
- **Type:** Normative runtime and delivery contract document
- **Priority:** Highest
- **Audience:** Flutter engineers, backend engineers, mobile tech lead, QA, release engineers, AI coding agents, reviewer agents
- **Purpose:** Define the canonical offline-first behavior of the app, the lifecycle of downloadable packs, the sync model for local and server-backed data, asset delivery abstractions, caching rules, storage policy, failure handling, and verification requirements.
- **Authority level:** This file is the canonical source of truth for offline behavior, pack lifecycle, sync semantics, asset-delivery abstraction, and cache policy. Feature modules, API clients, pack managers, and tests must not contradict this file.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`
- **Related files:** `10`, `11`, `12`, `16`, `17`, `18`–`25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This product is not merely “network tolerant.” It is intentionally designed so that core pilgrimage help remains usable when connectivity is poor, intermittent, or absent.

That requirement creates architectural complexity in five areas:
- what data must be available locally,
- what data may be stale but usable,
- what data must remain server-backed,
- how large assets are discovered, downloaded, verified, stored, and purged,
- how the app reconciles local state with remote truth when connectivity returns.

This file exists to prevent drift between mobile implementation, backend contracts, pack distribution, caching behavior, and feature expectations.

It defines:
- offline-first behavior categories,
- canonical pack types and lifecycle,
- sync policies for reads and writes,
- asset delivery abstraction,
- cache categories and expiration rules,
- storage rules,
- user-visible failure and recovery behavior,
- release and QA requirements for offline correctness.

---

# 2. Offline-first principles

## 2.1 Essential value must survive network loss
The user must still be able to access the app’s essential pilgrimage value when the network is unavailable.

## 2.2 Local operational truth drives runtime UX
For offline-capable features, the device-local store is the operational source of truth during runtime.

## 2.3 Server truth still exists for protected domains
Entitlements, group membership, and other trusted shared state remain server-governed, even if the client caches snapshots for continuity.

## 2.4 Staleness must be safe, not invisible
If the app uses cached or stale data, it must do so in ways that do not mislead the user about protected, time-sensitive, or safety-sensitive state.

## 2.5 Asset delivery must be abstracted
The app’s contract is manifest-driven packs with integrity verification and local inventory state. Platform-specific download mechanisms are implementation details beneath that abstraction.

## 2.6 Fallback behavior is part of success
A feature is not truly complete if it only works under ideal network and storage conditions.

---

# 3. Offline capability tiers

Every feature or data domain must be classified into one of these tiers.

## 3.1 Tier A — Fully offline-capable essential
Must work meaningfully with no network if the app has been opened at least once and required local data exists.

Examples:
- ritual guidance using cached/published content
- RIC / resolver using local rule content
- phrasebook and emergency tools
- saved anchors / Save My Gate recall
- previously downloaded map packs and audio packs
- local planner, reminders, notes, bookmarks
- medical profile and emergency information

## 3.2 Tier B — Offline-capable with cached snapshot
Can remain useful offline using last-good cached data, but freshness may degrade.

Examples:
- flags and season configuration
- pack manifest snapshot
- cached entitlement snapshot for UX continuity only
- last seen group live-board summary if product later surfaces it as stale data

## 3.3 Tier C — Online-required trusted operation
Requires network and trusted backend interaction for correctness.

Examples:
- joining a group
- sending server-backed group check-ins
- purchase validation and restore
- refreshing authoritative entitlement state
- subscribing to private realtime channels

## 3.4 Tier D — Rich enhancement, optional when online
Improves the experience but must not be required for baseline value.

Examples:
- live board realtime updates
- recommended pack suggestions from server-backed context
- high-fidelity map assets not yet downloaded

---

# 4. Canonical offline behavior matrix

## 4.1 Rituals and RIC
- Must work offline using local content and rules.
- Must not require live network for core correctness guidance.
- May show freshness metadata for content version if relevant.

## 4.2 Maps and Save My Gate
- Saved anchors must work offline.
- Micro-basemap or lightweight fallback orientation must remain available without downloaded heavy packs.
- Richer map layers may depend on downloaded packs.
- Route requests may degrade to text guidance or anchor guidance if full map resources are absent.

## 4.3 Group coordination
- Group snapshots may be viewed from last-known state if the UX explicitly marks them as stale and only if this does not create dangerous misunderstanding.
- Active writes such as join/check-in require online trusted paths.
- Manual fallback paths such as text-based regrouping and SMS-friendly copy remain available.

## 4.4 Planner, notes, bookmarks, wallet
- Must remain fully usable offline because they are local-first features.

## 4.5 Entitlements
- The app may use last-known entitlement snapshots for short-lived UX continuity.
- Protected purchase truth remains server authoritative.
- Expired or unverifiable entitlements must fail safe rather than drift into indefinite optimistic access.

## 4.6 Packs and downloadable content
- Previously installed packs must remain usable offline.
- New pack discovery may rely on cached manifest if offline.
- New downloads require connectivity.

---

# 5. Canonical pack model

## 5.1 Purpose of packs
Packs allow the app to stay lean while offering richer offline value.

## 5.2 Supported pack categories
### `MAP`
Geographic, structural, or wayfinding-related asset bundles.

### `AUDIO`
Offline audio guidance or phrase/audio support bundles.

### `CONTENT`
Optional future category for larger structured content bundles if justified.

### `MEDIA`
Optional future category for non-audio rich assets if justified.

## 5.3 Pack identity rules
Every pack must have:
- stable `pack_id`
- type
- version
- checksum
- artifact location
- size metadata
- entitlement requirement flag
- optional language or area-of-interest metadata

## 5.4 Pack immutability rule
A published pack version is immutable. If content changes, publish a new version rather than mutating the existing artifact in place.

---

# 6. Pack lifecycle

## 6.1 Canonical states
- `NOT_INSTALLED`
- `DOWNLOADING`
- `VERIFYING`
- `INSTALLED`
- `FAILED`
- `PURGED`

## 6.2 State meanings
### `NOT_INSTALLED`
Pack exists in the manifest but is not present locally.

### `DOWNLOADING`
Bytes are being fetched or resumed.

### `VERIFYING`
The artifact is fully present but is not yet trusted until integrity checks pass.

### `INSTALLED`
The pack is verified, locally registered, and available for runtime use.

### `FAILED`
Download or verification failed. The pack must not be used.

### `PURGED`
The pack was previously installed but has been removed from local storage.

## 6.3 State transition rules
Allowed transitions:
- `NOT_INSTALLED -> DOWNLOADING`
- `DOWNLOADING -> VERIFYING`
- `VERIFYING -> INSTALLED`
- `DOWNLOADING -> FAILED`
- `VERIFYING -> FAILED`
- `INSTALLED -> PURGED`
- `FAILED -> DOWNLOADING`
- `PURGED -> DOWNLOADING`

## 6.4 Forbidden transitions
- `DOWNLOADING -> INSTALLED` without verification
- `FAILED -> INSTALLED` without successful retry + verification
- `PURGED -> INSTALLED` without re-download or validated local recovery

---

# 7. Pack discovery and manifest contract

## 7.1 Manifest as source of pack availability
The pack manifest is the canonical discovery surface for downloadable packs.

## 7.2 Client rule
The client must not hardcode pack URLs or assume artifact availability outside the manifest contract.

## 7.3 Manifest cache behavior
- last-good manifest may be reused offline
- manifest freshness comes from ETag/cache validation via `/v1/packs/manifest`
- missing network must not erase previously known pack catalog state

## 7.4 Safe stale-manifest rule
Using a cached manifest offline is allowed for browsing previously known packs, but the app must not falsely imply it knows the latest available versions.

---

# 8. Asset delivery abstraction

## 8.1 Core rule
The app’s contract is built around:
- manifest discovery,
- authenticated or public artifact retrieval as documented,
- checksum verification,
- local inventory state,
- runtime availability checks.

## 8.2 Platform-specific delivery rule
Platform-specific asset delivery mechanisms must live beneath the pack manager abstraction.

## 8.3 iOS rule
The architecture must support modern iOS asset-delivery paths, including Background Assets or app-managed CDN downloads beneath the pack abstraction.

## 8.4 Android rule
Android asset delivery may use app-managed downloads or platform-supported asset-delivery mechanisms beneath the same abstraction.

## 8.5 CDN rule
Large immutable artifacts should be served from CDN-backed storage with resumable and cache-friendly behavior where possible.

## 8.6 Runtime independence rule
Feature modules must not care whether a pack arrived via one platform mechanism or another. They should only care whether the required pack is installed and usable.

---

# 9. Integrity and trust model for packs

## 9.1 Verification requirement
A pack must not be marked installed until integrity verification succeeds.

## 9.2 Minimum verification data
- expected `pack_id`
- expected `version`
- expected `checksum_sha256`
- expected artifact size if supplied

## 9.3 Verification outcomes
### Success
Mark pack `INSTALLED`, update local inventory, expose to runtime.

### Failure
Mark `FAILED`, preserve error code, do not expose pack as usable.

## 9.4 Partial download rule
Partially downloaded files must not be treated as installed or visible to feature runtime except through explicit in-progress UI.

## 9.5 Recovery rule
Failed or partial artifacts must be recoverable through retry/resume or clean restart.

---

# 10. Storage policy

## 10.1 Storage categories
The app uses these local storage categories:
- local structured database
- app preferences / small key-value state
- secure local storage for sensitive items
- app-private file storage for pack artifacts
- temporary cache storage

## 10.2 App-private storage rule
Downloaded packs and offline assets must live in app-private storage, not casual shared storage by default.

## 10.3 Sensitive-data rule
Emergency/medical data must use stronger local protection and must not be stored in broad shared file paths.

## 10.4 Cache-vs-persistent rule
- packs and user-private data are persistent
- temporary transport/cache artifacts may be purgeable
- app must distinguish between “installed asset” and “transport cache file”

## 10.5 Storage-pressure rule
The app must handle low-storage conditions gracefully by:
- warning before large downloads when possible
- refusing downloads safely when capacity is insufficient
- allowing explicit purge of non-essential packs

## 10.6 Backup rule
Local data types must be intentionally classified for backup behavior.
Sensitive or bulky transient artifacts should not be accidentally backed up if that creates privacy or restore problems.

---

# 11. Device-local source-of-truth rules

## 11.1 Local database
The local structured store is the runtime source of truth for:
- planner items
- notes and bookmarks
- saved anchors
- ritual sessions
- RIC findings
- pack inventory records
- last-good control-plane cache

## 11.2 Preferences / key-value store
Use for:
- small UI settings
- dismissals
- last selected filters or local UI preferences
- non-relational lightweight state

## 11.3 Secure local storage
Use for:
- encryption keys or protected secrets
- sensitive medical-profile encryption references
- minimal secure session-related metadata when needed

## 11.4 File storage
Use for:
- installed packs
- downloaded media bundles
- optional exported artifacts if supported later

---

# 12. Sync model overview

## 12.1 Sync philosophy
Not all data syncs.

The system distinguishes between:
- local-only data
- cached remote snapshots
- remote-authoritative data with local cache
- write-through or queued online actions

## 12.2 Sync categories
### Category A — No sync
Examples:
- notes
- bookmarks
- saved anchors
- planner items
- medical profile
- local ritual sessions

### Category B — Snapshot refresh
Examples:
- flags
- pack manifest
- entitlement snapshot
- optional group snapshot views

### Category C — Online write with optional local queueing
Examples:
- check-ins
- join requests
- purchase validate/restore requests

### Category D — Realtime enhancement
Examples:
- live board updates
- regroup pin updates

---

# 13. Read policies

## 13.1 Local-first read policy
For offline-capable features, the UI should read local state first and refresh from network only where necessary or available.

## 13.2 Snapshot refresh policy
For control-plane reads such as flags and manifest:
- use local cached snapshot immediately
- revalidate using ETag when connectivity exists
- replace local snapshot only when the server representation changes

## 13.3 Protected read policy
For server-governed reads such as entitlements or group live board:
- cached snapshot may be shown for continuity if explicitly safe
- freshness must be handled carefully
- fresh server read should replace stale state when connectivity and auth permit

## 13.4 Missing-local-data rule
If required local data does not exist, the app must present a clear unavailable/offline message rather than pretending data is present.

---

# 14. Write policies

## 14.1 Write categories
### Local write only
Write directly to local store and succeed immediately.

Examples:
- notes
- bookmarks
- planner items
- ritual progress
- saved gate/anchor

### Online trusted write
Requires network and trusted server response.

Examples:
- group join
- group check-in
- regroup pin creation
- purchase validation/restore

## 14.2 Queueing policy
Not every online-required write should be silently queued.

### Queue allowed only when
- duplicate/retry semantics are well-defined
- delayed execution does not create dangerous misunderstanding
- the UI can clearly represent “pending” vs “confirmed” state

### Queue discouraged or forbidden when
- the user expects immediate trusted confirmation
- membership or entitlement truth is the purpose of the write
- replay risk is high and confusing

## 14.3 Current queueing decision
### Allowed local queueing
- analytics event buffering
- optional retry bookkeeping for failed pack metadata fetches

### Do not silently queue for later send in v1
- group join
- purchase validate
- purchase restore

### Optional future queued retry with explicit UX
- group check-ins, only if the product later wants explicit pending-send behavior and the UX makes it obvious

---

# 15. Conflict and reconciliation policy

## 15.1 Local-only data
No server reconciliation needed.

## 15.2 Cached remote snapshots
Newest trusted server snapshot replaces old snapshot.

## 15.3 Remote-authoritative data
Server state wins. Client cache is updated to match server truth.

## 15.4 Protected stale-state rule
If a cached entitlement or group state conflicts with the fresh server state, the fresh server state wins immediately.

## 15.5 UI reconciliation rule
When protected state changes, the UI must update gracefully and not leave dangling access illusions.

---

# 16. Cache categories

## 16.1 Control-plane cache
Examples:
- flags
- pack manifest

Characteristics:
- ETag-driven
- last-good snapshot usable offline
- small payloads

## 16.2 Runtime data cache
Examples:
- cached entitlement snapshot
- cached group live-board snapshot if used
- local map search indexes if available

Characteristics:
- app-private
- purpose-specific freshness rules
- not always safe for long-term stale reuse

## 16.3 Artifact cache / installed assets
Examples:
- pack files
- downloaded audio
- optional offline map layers

Characteristics:
- large
- versioned
- integrity-verified
- purgeable

## 16.4 Temporary transport cache
Examples:
- partial downloads
- resumable chunk metadata
- temporary extraction directories

Characteristics:
- internal-only
- not a source of truth
- safe to clear when necessary

---

# 17. Cache policy rules

## 17.1 Last-good cache rule
For flags and manifest, the last successful payload plus ETag should be stored and reused until replaced or purged.

## 17.2 Explicit freshness metadata rule
Cached snapshots should carry timestamps or freshness metadata so the app can reason about age.

## 17.3 Cache invalidation rule
Immutable or versioned artifacts should be replaced by new versions rather than mutated in place.

## 17.4 Sensitive-state rule
Cached protected state must not be displayed in a way that implies current trusted validity when the app cannot verify freshness and the distinction matters.

## 17.5 Manual refresh rule
Where meaningful, the app may allow the user to explicitly retry or refresh server-backed state.

---

# 18. Recommended cache TTL guidance

These values are initial defaults and may be tuned with controlled change.

## 18.1 `flags`
- local cache usable immediately
- HTTP `max-age`: 5 minutes
- stale snapshot acceptable for offline continuity until replaced

## 18.2 `packs_manifest`
- local cache usable immediately
- HTTP `max-age`: 30 minutes
- stale snapshot acceptable for browsing known packs offline

## 18.3 `entitlements_snapshot`
- no public-cache semantics
- local snapshot for UX continuity only
- should be refreshed on app start, restore flow, or purchase-related transitions when online

## 18.4 `group_live_board_snapshot`
- product-specific short freshness window
- display stale indicators if offline or delayed

---

# 19. User-visible offline and pack UX rules

## 19.1 Offline messaging rule
The app must clearly distinguish between:
- fully available offline value
- unavailable because not downloaded yet
- unavailable because server confirmation is required
- stale but viewable cached data

## 19.2 Pack UX rule
For every pack, the UI should be able to show:
- not installed
- downloading with progress if available
- verifying
- installed
- failed with retry path
- purged
- locked by entitlement if applicable

## 19.3 No false confidence rule
The app must not present a pack as ready before verification completes.

## 19.4 Upgrade-boundary rule
If a pack is gated by supporter entitlement, the lock state must remain ethically clear and must not suggest that free users lose essential pilgrimage correctness or safety.

---

# 20. Network-awareness policy

## 20.1 Connectivity as hint, not truth
Connectivity status may be used as a UX hint, but the app must still handle real request failure even when the OS thinks the network is available.

## 20.2 Battery and data-awareness policy
Where appropriate, large pack downloads may respect user/network conditions such as Wi-Fi preference or low battery mode if the product surfaces those settings.

## 20.3 Large-download recommendation rule
Large optional packs should encourage but not require more favorable network conditions.

---

# 21. Background behavior rules

## 21.1 Background download rule
Background download behavior should be platform-capable but abstracted. The product contract must not depend on identical platform mechanics.

## 21.2 Background sync rule
Do not assume unlimited background execution for freshness. The app should tolerate foreground refresh as the primary guaranteed path.

## 21.3 Reminder rule
Local reminders must work from local scheduled state and not depend on the app being online at trigger time.

---

# 22. Failure classes and required behavior

## 22.1 No network
- use local data where available
- show stale or offline state where appropriate
- do not attempt protected writes as if successful

## 22.2 Flaky network
- retry safe reads where reasonable
- preserve local UX continuity
- use idempotency for retry-prone protected writes

## 22.3 Pack download interrupted
- preserve partial state if resumable
- allow retry/resume
- never expose partially downloaded pack as installed

## 22.4 Checksum mismatch
- mark pack `FAILED`
- keep detailed error code
- require retry or redownload

## 22.5 Low storage
- refuse installation safely
- provide user-facing storage explanation
- offer purge path for optional packs

## 22.6 Auth expired
- stop protected reads/writes
- preserve local-only features
- prompt safe re-auth flow when needed

## 22.7 Manifest stale or unavailable
- use last-good snapshot if present
- show manifest freshness if needed for support/debug UX

## 22.8 Entitlement refresh unavailable
- use last-known local snapshot only for continuity
- avoid falsely confirming new access or post-expiry certainty without server verification

---

# 23. Sync and pack manager responsibilities

## 23.1 Pack manager responsibilities
- fetch manifest
- compare versions
- schedule downloads
- track progress
- verify checksums
- register install state
- expose purge and retry operations
- surface user-readable failure states

## 23.2 Sync coordinator responsibilities
- decide when to refresh cached snapshots
- coordinate online protected reads
- manage safe retries
- avoid duplicate writes
- reconcile local cache with server truth

## 23.3 Repository responsibilities
Feature repositories should consume sync and pack manager abstractions rather than implementing custom fetch/cache logic in feature modules.

---

# 24. Security and privacy rules

## 24.1 Pack security rule
Pack verification data must come from trusted manifest contracts. Do not trust file names or local paths as proof of integrity.

## 24.2 Private data rule
Local private support data must not be silently uploaded or mirrored to the server without an approved contract change.

## 24.3 Sensitive local storage rule
Medical or sensitive emergency data must remain protected locally and excluded from casual logging and analytics.

## 24.4 Cache logging rule
Logs and analytics must not leak sensitive local payloads, pack URLs with embedded secrets, or private content values.

---

# 25. Performance and efficiency rules

## 25.1 Lean base-app rule
Do not bundle rich offline assets that should be delivered as optional packs.

## 25.2 Local-read performance rule
Primary offline-capable screens should load from local data without waiting on network requests.

## 25.3 Download-efficiency rule
Prefer resumable and CDN-friendly transfer patterns for large assets.

## 25.4 Purgeability rule
Optional rich assets must be purgeable so device storage pressure does not trap the user.

---

# 26. Testing requirements

## 26.1 Required unit tests
- pack state machine transitions
- checksum verification logic
- stale snapshot selection rules
- protected-vs-local read routing
- retry and error translation logic

## 26.2 Required integration tests
- flags ETag 200/304 behavior
- manifest ETag 200/304 behavior
- pack install success and checksum failure
- local-first read on no network
- failed protected writes under offline conditions
- entitlement refresh fallback behavior

## 26.3 Required device tests
- airplane mode behavior
- interrupted downloads
- low-storage failure path
- app relaunch during download/verification
- installed pack persistence across restart
- local reminders firing offline

## 26.4 Required manual release checks
- fresh install with no network after initial sync
- stale manifest browsing
- using maps with only fallback assets
- opening emergency tools fully offline
- purging and reinstalling optional packs

---

# 27. Data and contract alignment rules

## 27.1 Alignment with file `13`
Pack inventory, local snapshots, ritual sessions, notes, planner items, and medical profile persistence must remain consistent with the canonical local model.

## 27.2 Alignment with file `14`
Flags and manifest fetch behavior, ETag use, idempotency, and protected online writes must remain consistent with the API contract.

## 27.3 Alignment with file `16`
Offline map packs and fallback wayfinding behavior must remain consistent with the map subsystem architecture.

## 27.4 Alignment with feature-family files
Feature files must not redefine offline or pack semantics independently.

---

# 28. Recommendations adopted into this policy

## 28.1 Recommendation — local-first source of truth for offline-capable reads
The app now formally treats local persistence as the operational source of truth for offline-capable runtime behavior.

## 28.2 Recommendation — manifest + integrity + pack-manager abstraction
The pack system is now formally defined around manifest discovery, checksum verification, and a platform-independent pack-manager abstraction.

## 28.3 Recommendation — do not over-queue trusted writes
Protected actions such as group join and purchase restore are intentionally not silently queued in v1 because delayed replay would create misleading states.

## 28.4 Recommendation — fallback behavior is a first-class product success metric
The app is considered correct only when it degrades clearly and safely under offline or low-resource conditions.

## 28.5 Recommendation — stale protected state must be handled conservatively
Entitlement and group states may be cached, but must not be presented as current truth when freshness matters and the server cannot be reached.

---

# 29. Anti-patterns forbidden by this policy

The following are forbidden unless explicitly approved.

## 29.1 Requiring network for essential ritual or emergency value
Forbidden.

## 29.2 Treating a partially downloaded pack as available
Forbidden.

## 29.3 Marking a pack installed without checksum verification
Forbidden.

## 29.4 Hardcoding pack URLs in feature modules
Forbidden.

## 29.5 Letting every feature invent its own cache logic
Forbidden.

## 29.6 Silently uploading local private support data to the server
Forbidden.

## 29.7 Treating stale protected state as guaranteed current truth
Forbidden.

## 29.8 Hiding offline limitations in misleading UI
Forbidden.

---

# 30. When this file must be updated

This file must be updated whenever any of the following changes:
- offline capability classification
- pack categories or pack lifecycle
- manifest semantics
- integrity verification rules
- storage paths or storage policy
- sync category or retry policy
- queueing policy for protected writes
- cache TTLs or cache invalidation rules
- background delivery assumptions
- offline UX state semantics
- alignment with map pack behavior or API cache behavior

If any of these evolve but this file is not updated, mobile behavior, backend contracts, QA, and release verification will drift quickly.

---

# 31. Summary

This file defines the canonical offline-first runtime policy for Pilgrims Mobile App.

It establishes:
- what must work offline
- what may work from cached snapshots
- what must remain server-backed
- how packs are discovered, downloaded, verified, installed, and purged
- how sync and cache behavior are categorized
- how stale state and failure modes must be handled
- how offline correctness is tested and released

Its purpose is to ensure that the app remains:
- useful under poor connectivity
- honest about freshness and trust
- efficient in asset delivery
- and safe for long-term AI-assisted development without offline behavior drifting across modules.

