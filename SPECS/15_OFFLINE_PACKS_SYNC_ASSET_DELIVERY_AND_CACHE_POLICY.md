# 15 — OFFLINE, PACKS, SYNC, ASSET DELIVERY, AND CACHE POLICY

## Document status
- **Type:** Normative runtime and delivery contract document
- **Priority:** Highest
- **Audience:** Flutter engineers, backend engineers, mobile tech lead, QA, release engineers, AI coding agents, reviewer agents
- **Purpose:** Define canonical offline-first behavior, downloadable pack lifecycle, sync model, asset delivery abstraction, caching rules, storage policy, failure handling, verification requirements, and signed trust-chain expectations.
- **Authority level:** This file is the canonical source of truth for offline behavior, pack lifecycle, sync semantics, asset-delivery abstraction, and cache policy. Feature modules, API clients, pack managers, and tests must not contradict this file.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `06`, `07`, `13`, `14`, `23`, `26`, `29`, `30`, `31`, `CONTRACTS/content_pack_trust_chain_contract.yaml`
- **Related files:** `10`, `11`, `12`, `16`, `17`, `18`–`25`, `27`, `28`

---

# 1. Purpose of this file

This product is not merely “network tolerant.” It is intentionally designed so that core pilgrimage help remains usable when connectivity is poor, intermittent, or absent.

That requirement creates architectural complexity in five areas:
- what data must be available locally,
- what data may be stale but usable,
- what data must remain server-backed,
- how large assets are discovered, downloaded, authenticated, verified, stored, activated, and purged,
- how the app reconciles local state with remote truth when connectivity returns.

This file prevents drift between mobile implementation, backend contracts, pack distribution, caching behavior, and feature expectations.

---

# 2. Offline-first principles

## 2.1 Essential value must survive network loss
The user must still be able to access essential pilgrimage value when the network is unavailable.

## 2.2 Local operational truth drives runtime UX
For offline-capable features, the device-local store is the operational source of truth during runtime.

## 2.3 Server truth still exists for protected domains
Entitlements, group membership, group creation/join/check-in writes, account deletion/export requests, and other trusted shared state remain server-governed even if the client caches snapshots for continuity.

## 2.4 Staleness must be safe, not invisible
If the app uses cached or stale data, it must do so in ways that do not mislead the user about protected, time-sensitive, safety-sensitive, or trust-sensitive state.

## 2.5 Asset delivery must be abstracted
The app’s contract is manifest-driven packs with authenticated manifest/artifact trust-chain verification and local inventory state. Platform-specific download mechanisms are implementation details beneath that abstraction.

## 2.6 Fallback behavior is part of success
A feature is not truly complete if it only works under ideal network and storage conditions.

---

# 3. Offline capability tiers

Every feature or data domain must be classified into one of these tiers.

## 3.1 Tier A — Fully offline-capable essential
Must work meaningfully with no network if the app has been opened at least once and required local data exists.

Examples:
- ritual guidance using cached/published content,
- RIC/resolver using local rule content,
- phrasebook and emergency tools,
- saved anchors / Save My Gate recall,
- previously installed map packs and audio packs,
- local planner, reminders, notes, bookmarks,
- medical profile and emergency information.

## 3.2 Tier B — Offline-capable with cached snapshot
Can remain useful offline using last-good cached data, but freshness may degrade.

Examples:
- flags and season configuration,
- pack manifest snapshot,
- cached entitlement snapshot for UX continuity only,
- last seen group summary if product surfaces it as stale data,
- deletion/export request status if clearly marked stale.

## 3.3 Tier C — Online-required trusted operation
Requires network and trusted backend interaction for correctness.

Examples:
- creating a group,
- joining a group,
- sending server-backed group check-ins,
- creating regroup pins,
- purchase validation and restore,
- refreshing authoritative entitlement state,
- account deletion/export requests,
- subscribing to private realtime channels.

## 3.4 Tier D — Rich enhancement, optional when online
Improves the experience but must not be required for baseline value.

Examples:
- live board realtime updates,
- recommended pack suggestions from server-backed context,
- high-fidelity map assets not yet downloaded.

---

# 4. Canonical offline behavior matrix

## 4.1 Rituals and RIC
- Must work offline using local content and rules.
- Must not require live network for core correctness guidance.
- May show freshness/content-version metadata.

## 4.2 Maps and Save My Gate
- Saved anchors must work offline.
- Micro-basemap or lightweight fallback orientation must remain available without downloaded heavy packs.
- Richer map layers may depend on downloaded packs.
- Route requests may degrade to text guidance or anchor guidance if full map resources are absent.

## 4.3 Group coordination
- Group snapshots may be viewed from last-known state if the UX explicitly marks them as stale and only if this does not create dangerous misunderstanding.
- Active trusted writes such as create, join, check-in, regroup creation, or deletion/export requests require online trusted paths.
- Manual fallback paths such as text-based regrouping and SMS-friendly copy remain available.
- The client must not silently queue trusted group writes in a way that later surprises the user.

## 4.4 Planner, notes, bookmarks, wallet
- Must remain fully usable offline because they are local-first features.
- No hidden sync or upload is allowed by default.

## 4.5 Entitlements
- The app may use last-known entitlement snapshots for short-lived UX continuity.
- Protected purchase truth remains server-authoritative.
- Expired or unverifiable entitlements must fail safe rather than drift into indefinite optimistic access.

## 4.6 Packs and downloadable content
- Previously installed packs must remain usable offline if their local trust state remains valid.
- New pack discovery may rely on cached manifest if offline.
- New downloads require connectivity.
- Activation requires manifest/artifact trust-chain checks, not checksum alone.

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
Structured content bundles where approved by content governance.

### `MEDIA`
Optional future category for non-audio rich assets if justified.

## 5.3 Pack identity rules
Every pack must have:
- stable `pack_id`,
- type/category,
- version,
- checksum,
- artifact location/delivery reference,
- size metadata,
- entitlement requirement flag where applicable,
- optional language or area-of-interest metadata,
- trust-chain fields required by `CONTRACTS/content_pack_trust_chain_contract.yaml`.

## 5.4 Pack immutability rule
A published pack version is immutable. If content changes, publish a new version rather than mutating the existing artifact in place.

## 5.5 No executable-code rule
Pack artifacts must never contain executable code or runtime logic that bypasses app review, content governance, or release controls.

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
The artifact is fully present but is not yet trusted until integrity, authenticity, compatibility, and storage-completeness checks pass.

### `INSTALLED`
The pack is verified, trusted, locally registered, and available for runtime use.

### `FAILED`
Download, trust-chain verification, compatibility check, or storage check failed. The pack must not be used.

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
- any transition to `INSTALLED` without signature, checksum, compatibility, and storage-completeness success where trust-chain metadata is required

---

# 7. Pack discovery and manifest contract

## 7.1 Manifest as source of pack availability
The pack manifest is the canonical discovery surface for downloadable packs.

## 7.2 Client rule
The client must not hardcode pack URLs or assume artifact availability outside the manifest contract.

## 7.3 Manifest cache behavior
- last-good manifest may be reused offline,
- manifest freshness comes from ETag/cache validation via `/v1/packs/manifest`,
- missing network must not erase previously known pack catalog state.

## 7.4 Safe stale-manifest rule
Using a cached manifest offline is allowed for browsing previously known packs, but the app must not falsely imply it knows the latest available versions.

## 7.5 Required manifest trust fields
Manifest metadata must align with file `14` and `CONTRACTS/content_pack_trust_chain_contract.yaml`.

Required fields include:
- `manifest_id`,
- `manifest_version`,
- `generated_at`,
- `signing_key_id`,
- `signing_algorithm`,
- `manifest_signature`,
- `revoked_key_ids`,
- `min_app_version`,
- pack entries with artifact signatures and checksums.

## 7.6 Manifest verification rule
The client must verify the manifest signature before trusting pack entries for new activation.
If signature verification fails, the client must preserve last-known-good local state and show safe failure or stale state.

---

# 8. Asset delivery abstraction

## 8.1 Core rule
The app’s contract is built around:
- manifest discovery,
- authenticated or public artifact retrieval as documented,
- checksum verification,
- signature verification,
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

# 9. Integrity, authenticity, and trust model for packs

## 9.1 Verification requirement
A pack must not be marked installed until trust-chain verification succeeds.

## 9.2 Minimum verification data
- expected `pack_id`,
- expected `version`,
- expected `checksum_sha256`,
- expected artifact size if supplied,
- `artifact_signature`,
- `signing_key_id`,
- `signed_at`,
- `signing_algorithm`,
- compatibility fields.

## 9.3 Verification checks
Verification must include:
1. manifest signature check,
2. artifact checksum check,
3. artifact signature check,
4. signing-key validity/revocation check,
5. schema/app compatibility check,
6. storage-completeness check.

## 9.4 Verification outcomes
### Success
Mark pack `INSTALLED`, update local inventory, expose to runtime.

### Failure
Mark `FAILED`, preserve error code, do not expose pack as usable.

## 9.5 Partial download rule
Partially downloaded files must not be treated as installed or visible to feature runtime except through explicit in-progress UI.

## 9.6 Recovery rule
Failed or partial artifacts must be recoverable through retry/resume or clean restart.

## 9.7 Last-known-good rule
A failed candidate pack must not replace the current last-known-good installed pack.

## 9.8 Anti-rollback rule
Activation pointers may move backward only through an explicit signed rollback action with reason and release/incident reference.

## 9.9 Key rotation rule
Signing-key rotation must have documented overlap, revoked-key handling, and release evidence before production activation.

---

# 10. Storage policy

## 10.1 Storage categories
The app uses these local storage categories:
- local structured database,
- app preferences / small key-value state,
- secure local storage for sensitive items,
- app-private file storage for pack artifacts,
- temporary cache storage.

## 10.2 App-private storage rule
Downloaded packs and offline assets must live in app-private storage, not casual shared storage by default.

## 10.3 Sensitive-data rule
Emergency/medical data must use stronger local protection and must not be stored in broad shared file paths.

## 10.4 Cache-vs-persistent rule
- packs and user-private data are persistent,
- temporary transport/cache artifacts may be purgeable,
- app must distinguish between “installed asset” and “transport cache file.”

## 10.5 Storage-pressure rule
The app must handle low-storage conditions gracefully by:
- warning before large downloads when possible,
- refusing downloads safely when capacity is insufficient,
- allowing explicit purge of non-essential packs.

## 10.6 Backup rule
Local data types must be intentionally classified for backup behavior.
Sensitive or bulky transient artifacts should not be accidentally backed up if that creates privacy or restore problems.

---

# 11. Device-local source-of-truth rules

## 11.1 Local database
The local structured store is the runtime source of truth for:
- planner items,
- notes and bookmarks,
- saved anchors,
- ritual sessions,
- RIC findings,
- pack inventory records,
- last-good control-plane cache.

## 11.2 Preferences / key-value store
Use for:
- small UI settings,
- dismissals,
- last selected filters or local UI preferences.

## 11.3 Secure storage
Use for:
- tokens/session material as approved by file `29`,
- sensitive local protection keys where needed.

## 11.4 App-private file storage
Use for:
- downloaded packs,
- media/audio/map artifacts,
- local files not intended for broad shared storage.

---

# 12. Sync and refresh rules

## 12.1 Pull refresh
The app may refresh:
- flags,
- pack manifest,
- entitlements,
- group summaries,
- deletion/export status where applicable.

## 12.2 Push/write behavior
Trusted writes require online server acknowledgement:
- group creation,
- group join,
- group check-in,
- regroup pin creation,
- purchase validation/restore,
- account deletion/export requests.

## 12.3 No fake-success rule
The client must not pretend a trusted server write succeeded if it did not complete.

## 12.4 Offline queue caution
Offline queues may be used only for low-risk local telemetry or explicitly approved flows. Trusted group/account/purchase writes must not be silently queued by default.

---

# 13. User-visible failure behavior

## 13.1 Failure copy principles
Failure copy must tell the user:
- what happened,
- whether anything was saved locally,
- whether trusted server action completed,
- what they can still do.

## 13.2 Pack failure states
Pack failure states must distinguish:
- network failed,
- low storage,
- checksum failed,
- signature failed,
- revoked signing key,
- app version incompatible,
- manifest stale/unavailable,
- server unavailable,
- user cancelled.

## 13.3 Safety rule
A failed pack or manifest must never remove existing essential baseline value.

---

# 14. Testing and release evidence

## 14.1 Required test coverage
Tests must cover:
- no-network startup,
- offline ritual/RIC access,
- offline saved gate recall,
- stale group state display,
- group trusted write unavailable offline,
- entitlement stale state,
- pack install success,
- interrupted download recovery,
- low-storage failure,
- checksum failure,
- signature failure,
- revoked-key failure,
- incompatible version failure,
- purge behavior,
- last-known-good preservation.

## 14.2 Physical-device proof
Physical-device proof is required for:
- install/restart/purge/download flows,
- low storage behavior where practical,
- background/foreground download behavior where platform-specific,
- offline after app restart,
- pack activation and failure states.

## 14.3 Trust-chain evidence
Release evidence must show that contract validation against `CONTRACTS/content_pack_trust_chain_contract.yaml` passed for changed pack/content delivery behavior.

---

# 15. Definition of done

This offline/pack system is ready when:
- offline capability tiers are assigned,
- trusted writes degrade honestly offline,
- pack lifecycle follows the allowed state machine,
- manifest discovery is canonical,
- checksum and signature verification are implemented,
- candidate failures preserve last-known-good state,
- storage pressure and purge behavior are safe,
- stale states are visible and accessible,
- tests cover degraded states,
- release evidence satisfies file `28`.

---

# 16. AI-agent checklist

Before editing offline, sync, cache, or pack code, an AI agent must:
1. Read files `13`, `14`, `15`, `23`, `26`, `29`, `30`, and `31`.
2. Read `CONTRACTS/content_pack_trust_chain_contract.yaml`.
3. Confirm the offline tier and trusted-write behavior.
4. Confirm whether data is local-only, cached remote, or server truth.
5. Confirm pack lifecycle transitions.
6. Never mark a pack installed without all required trust-chain checks.
7. Update tests and release evidence for changed offline or pack behavior.

# 18. Guide Marketplace offline/cache classification

Guide Marketplace is optional server-trusted value and does not alter Tier A essential guarantees.

## 18.1 Tier B — optional cached browse
A last-good guide/listing snapshot may be cached for browsing only when:
- the UI clearly marks it stale when freshness is insufficient,
- cached credential/trust state is not presented as currently verified indefinitely,
- the cache excludes restricted credential evidence and unnecessary raw contact targets,
- public eligibility loss can invalidate/hide cached active treatment.

## 18.2 Tier C — online-required trusted operations
The following require network/server truth:
- provider application submission,
- authoritative application/verification status refresh,
- listing publication or trusted listing writes,
- credential verification/re-verification,
- report submission,
- contact-intent resolution,
- current public-eligibility confirmation before contact handoff.

## 18.3 No hidden queue
Do not silently queue Guide Marketplace trusted writes for later execution. Offline submission/update/report/contact attempts must fail honestly and preserve local form input only where privacy policy permits.

## 18.4 Stale-trust safety
If the app cannot establish current credential/public eligibility:
- cached profile information may remain readable only as stale context,
- "currently verified" semantics must be removed,
- Contact Guide must not resolve a new channel until current eligibility is re-checked.

## 18.5 Independence rule
Guide Marketplace unavailability must not degrade Rituals/RIC, Emergency, Phrasebook, Save My Gate, baseline map recovery, local personal tools, or baseline group coordination.

---

End of file.