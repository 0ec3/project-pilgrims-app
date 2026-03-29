# 23 — FEATURE: OFFLINE PACKS, AUDIO, AND CONTENT DISTRIBUTION

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, backend engineers, infra/release engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for Pack Catalog, Pack Detail / Install Flow, offline pack discovery, downloadable audio and content pack behavior, recommendation logic, entitlement-aware pack access, install/verify/purge UX, content-distribution policy, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the user-facing packs and downloadable-asset feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `18-FEATURE-RITUALS-RIC-AND-RELIGIOUS-CONTENT.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`, `20-FEATURE-GROUP-HUB-CHECKINS-REGROUP-AND-SHARED-COORDINATION.md`, `21-FEATURE-PLANNER-REMINDERS-WALLET-NOTES-AND-BOOKMARKS.md`, `22-FEATURE-PHRASEBOOK-EMERGENCY-SAFETY-AND-ASSISTIVE-TOOLS.md`, `24-FEATURE-ACCOUNT-SUBSCRIPTIONS-ENTITLEMENTS-AND-SETTINGS.md`, `25-FEATURE-ONBOARDING-HOME-AND-SIMPLE-MODE.md`
- **Related files:** `26`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because downloadable packs are one of the easiest places for teams and AI agents to confuse runtime architecture with user-facing product behavior.

For this project, that confusion is risky because:
- the base app must stay lean,
- the product promise depends on offline usefulness,
- packs carry both ethical monetization and operational risk,
- audio and map assets behave differently from governed ritual content,
- poor pack UX can make the app feel broken even when core free value still works,
- integrity, purge, storage pressure, and stale-manifest cases must be handled explicitly,
- season-aware recommendations matter because Umrah-first behavior must not quietly reintroduce Hajj complexity.

This file prevents those failures by defining:
- what the packs feature family is responsible for,
- what kinds of packs exist,
- how users discover and install them,
- how pack lock states and recommendation states behave,
- how audio/content packs are surfaced to user-facing features,
- how purge and storage pressure behavior work,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
This feature family exists to help pilgrims:
- keep the base app small,
- add richer offline value only when useful,
- understand what downloadable assets will help them,
- install those assets safely and transparently,
- recover gracefully when assets are missing, stale, corrupted, or purged,
- manage storage without losing essential free value.

## 2.2 Main user value statement
A pilgrim should be able to open the packs experience and quickly answer questions like:
- What offline packs are available for my journey?
- Which pack should I download first?
- Is this pack required, optional, or supporter-only?
- How much space will it use?
- What happens if the download fails or my storage is low?
- Can I safely remove it later?

## 2.3 Feature-level promise
This feature family must feel:
- clear,
- trustworthy,
- honest about readiness,
- respectful of storage and network constraints,
- season-aware,
- ethically monetized,
- useful even when no pack is installed.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- Pack Catalog behavior,
- Pack Detail / Install Flow behavior,
- pack recommendation logic,
- pack classes and user-facing descriptions,
- pack install, verify, fail, retry, repair, and purge UX,
- Wi‑Fi/mobile-data preference interaction,
- auto-download consent behavior where entitled,
- season-aware and context-aware pack suggestions,
- pack lock states and upgrade messaging rules,
- user-facing audio/content distribution semantics,
- feature handoff rules from packs into Maps, Rituals, Phrasebook, and Home.

## 3.2 Out of scope
This feature family does **not** include:
- deep pack lifecycle engine implementation details already owned by file `15`,
- store subscription truth or purchase validation,
- feature-specific audio player behavior,
- map rendering internals,
- scholar-review workflow for governed religious content,
- generalized file sync or cloud document delivery,
- ads or unrelated promotional surfaces.

## 3.3 Boundary with file `15`
File `15` is the canonical runtime and delivery contract for:
- offline-first policy,
- pack lifecycle states,
- asset delivery abstraction,
- storage categories,
- cache semantics,
- integrity rules,
- queueing and sync policy.

This file does **not** re-decide those technical truths.
Instead, it defines the user-facing feature behavior built on top of them.

## 3.4 Boundary with file `14`
File `14` owns:
- `GET /v1/packs/manifest`,
- flags and ETag behavior,
- purchase/restore contracts,
- pack manifest schema.

This file defines how those contracts become product behavior in the packs feature family.

## 3.5 Boundary with file `24`
File `24` owns:
- Supporter truth,
- `PACK_AUTO_DOWNLOAD`,
- `AUDIO_OFFLINE`,
- restore and purchase behavior,
- Settings ownership for Wi‑Fi-only and related preference surfaces.

This file reacts to those settings and gates but does not redefine them.

## 3.6 Boundary with file `18`
Rituals owns ritual audio semantics, ritual content runtime, and whether a specific ritual surface offers audio controls.
This file only defines how ritual-related audio or content packs are distributed and surfaced as downloadable assets.

## 3.7 Boundary with file `19`
Maps owns route and map behavior.
This file only defines how downloadable map packs are discovered, installed, represented, and handed off into map contexts.

## 3.8 Boundary with file `22`
Phrasebook/Emergency owns phrase-card, big-text, and emergency-audio behavior.
This file only defines how phrase audio or voice packs are packaged, installed, and made available to that feature family.

## 3.9 Boundary with file `26`
If governed ritual or phrase content evolves into larger structured downloadable bundles, governance and publishing rules must be updated in file `26` as well. This file alone cannot redefine governed content release workflow.

---

# 4. Product rules that govern this feature family

## 4.1 Base-app-light rule
The base app must stay lean. Heavy map and audio assets belong in packs rather than the default install whenever feasible.

## 4.2 No-pack usefulness rule
The app must remain meaningfully useful when no downloadable pack is installed.
Pack UX must never imply the app is broken simply because richer assets are absent.

## 4.3 Verify-before-ready rule
A pack is not ready until verification succeeds.
The UI must never present a partially downloaded or unverified artifact as installed truth.

## 4.4 Ethical pack-gating rule
Supporter may gate convenience and richer offline assets, but packs must never become a hidden paywall on ritual correctness, baseline safety, phrase text, or core orientation recovery.

## 4.5 Season-aware recommendation rule
Pack recommendations must remain Umrah-first by default and must not surface Hajj-oriented assets as primary recommendations outside approved season/scope.

## 4.6 User-consent rule
Large downloads and auto-download behavior require understandable user consent and must respect network/storage preferences.

## 4.7 Purge-with-dignity rule
Users must be able to remove packs later without fear that they are damaging the app.
The app should explain clearly what will remain available after purge.

## 4.8 Platform-honesty rule
The product may use different underlying asset-delivery mechanisms on iOS and Android, but the user-facing meaning of download, verify, install, and purge must stay consistent.

---

# 5. Canonical terminology for this feature family

## 5.1 Pack
A versioned downloadable asset bundle that expands offline value beyond the lean base app.

## 5.2 Pack Catalog
The browse/discovery surface listing available downloadable packs.

## 5.3 Pack Detail / Install Flow
The screen or flow where a user understands one pack’s purpose, eligibility, size, and install state, then installs or manages it.

## 5.4 Installed pack
A pack that has completed integrity verification and is registered as usable locally.

## 5.5 Purged pack
A pack that was previously installed but has been removed from local storage.

## 5.6 Required-for-best-experience
A helpful but non-essential recommendation label for packs that materially improve a feature but are not required for baseline use.

## 5.7 Auto-download consent
User consent allowing the app to begin eligible pack downloads automatically under defined conditions.

## 5.8 Pack stub
A retained local record indicating a previously known or previously installed pack without claiming the artifact is still present.

## 5.9 Voice pack
An audio pack for phrasebook or similar assistance playback.

## 5.10 Guided audio pack
An audio pack for guided ritual or other structured app experiences.

---

# 6. User stories

## 6.1 Discovery and install
- **As a pilgrim**, I can browse available offline packs and understand what each one helps with.
- **As a pilgrim**, I can install a pack with clear progress and honest failure handling.
- **As a pilgrim**, I can see whether a pack is optional, recommended, or locked by Supporter.

## 6.2 Audio and content use
- **As a pilgrim**, I can install offline audio for phrasebook or rituals when it is supported and entitled.
- **As a pilgrim**, if audio is unavailable, I still retain meaningful text guidance.

## 6.3 Storage and purge
- **As a pilgrim**, I can remove packs later to free storage and understand what functionality will degrade.
- **As a pilgrim**, I can recover from failed or corrupted downloads without complicated repair steps.

## 6.4 Recommendations and journey context
- **As an Umrah user**, I see Haram-first offline pack suggestions rather than Hajj-oriented recommendations.
- **As a group member or supporter**, I may get a helpful Trip Pack prompt after join or map entry when it genuinely improves the journey.

---

# 7. Canonical pack classes and user-facing meaning

## 7.1 Canonical pack categories
This feature family aligns with the pack categories already defined in file `15`:
- `MAP`
- `AUDIO`
- `CONTENT`
- `MEDIA`

## 7.2 Current product use of `MAP`
`MAP` packs may include:
- high-resolution Haram map assets,
- holy-sites tile sets,
- richer indoor or area-of-interest structures,
- other map-side offline bundles approved by architecture.

## 7.3 Current product use of `AUDIO`
`AUDIO` packs may include:
- phrasebook voice packs,
- offline phrase playback bundles,
- guided ritual audio bundles,
- other reviewed spoken guidance assets.

## 7.4 Controlled use of `CONTENT`
`CONTENT` packs are allowed only where larger structured offline bundles are justified and governed.
They must not become an informal way to bypass content governance or to ship arbitrary product logic in asset form.

## 7.5 Controlled use of `MEDIA`
`MEDIA` packs are optional future-use bundles for richer non-audio assets where justified.
They must remain subordinate to the same manifest, verification, and storage rules.

## 7.6 No executable-code rule
Packs contain data and media, not executable feature logic or arbitrary code.

---

# 8. Pack discovery and recommendation behavior

## 8.1 Discovery source rule
The pack manifest is the canonical discovery surface for downloadable packs.
The client must not hardcode downloadable asset lists or assume artifact URLs outside the manifest contract.

## 8.2 Pack Catalog purpose
Pack Catalog exists to help users understand what richer offline value is available and manage it calmly.

## 8.3 Recommendation inputs
Recommendation ordering may consider:
- current `season` from flags,
- app language or locale,
- current installed pack inventory,
- entitlement snapshot,
- active group or joined-group suggestion context,
- current feature entry point,
- area-of-interest or map context.

## 8.4 Umrah-first recommendation rule
When `season=umrah`, Pack Catalog and related prompts should prioritize:
1. Haram high-resolution map pack,
2. relevant app-language audio or voice packs,
3. other appropriate general-purpose packs.

Holy Sites / Hajj-focused packs must not be the primary recommendation by default.

## 8.5 Hajj-capable recommendation rule
When `season=hajj` and scope explicitly permits Hajj-oriented suggestions, recommendation order may prioritize:
1. Holy Sites or Hajj map pack,
2. Haram high-resolution pack,
3. relevant audio packs,
4. additional approved packs.

## 8.6 Browse-all rule
Even when a pack is suppressed from primary recommendation, the user may still discover it through a deliberate browse-all path if product scope allows.

## 8.7 Group-suggested packs rule
If `group_join_response.suggested_packs` or other trusted context offers suggested pack IDs, Pack Catalog may promote them, but must still apply season, entitlement, and ethical-priority rules.

## 8.8 Home and onboarding relationship rule
Pack suggestions may appear on Home or after onboarding, but should remain secondary to ritual start, urgent help, and recovery shortcuts.

---

# 9. Pack eligibility, lock states, and entitlement behavior

## 9.1 Canonical pack lock reasons
A pack may be unavailable because it is:
- not installed yet,
- downloading or verifying,
- locked by entitlement,
- unavailable on current device/platform,
- unavailable because the manifest or artifact cannot currently be reached,
- suppressed by season recommendation but still optionally discoverable.

## 9.2 Supporter-linked pack gates
Current entitlement gates relevant to this feature family include:
- `PACK_AUTO_DOWNLOAD`
- `AUDIO_OFFLINE`

## 9.3 `PACK_AUTO_DOWNLOAD` meaning
This gate enables Supporter convenience for auto-download flows where the user has also given the necessary consent and network/storage conditions permit it.
It must not be treated as a blanket permission to download without user understanding.

## 9.4 `AUDIO_OFFLINE` meaning
This gate allows offline audio pack access where the pack exists, the user is entitled, and the runtime support is present.
Text usefulness must remain intact without it.

## 9.5 Lock-state copy rule
If a pack is locked, the UI must explain whether it is:
- a richer offline convenience,
- not required for core correctness or safety,
- unlockable through Supporter if appropriate.

## 9.6 Offline entitlement continuity rule
If entitlement is temporarily unverifiable offline, the pack feature must follow file `24`’s protected-state honesty rules.
Do not overclaim paid pack access after expiry or unknown protected-state freshness.

---

# 10. Install, verify, fail, retry, repair, and purge behavior

## 10.1 Purpose
The install flow exists to make pack lifecycle understandable and trustworthy at the user level.

## 10.2 Canonical user-visible states
The packs feature family must be able to render at least these user-visible states:
- not installed,
- queued,
- downloading,
- verifying,
- installed,
- failed,
- purged,
- locked.

## 10.3 Download-start rule
When the user initiates install, the app should first validate:
- current entitlement when relevant,
- network policy (such as Wi‑Fi-only preference),
- storage availability,
- pack compatibility or min-app-version constraints where relevant.

## 10.4 Download-progress rule
If progress information is available, the UI should show it clearly and should support pause/resume behavior where implementation allows.

## 10.5 Verify rule
Verification must be visible enough that users understand the app is still preparing the pack and that it is not ready yet.

## 10.6 Fail rule
If install fails, the UI must retain enough context to support:
- retry,
- possibly repair/restart,
- user understanding of the likely reason,
- leaving the screen without feeling that the app is stuck.

## 10.7 Repair behavior
If the runtime supports repair or resume, the user-facing flow may describe this as repair, retry, or continue download. It must not expose low-level chunk or checksum jargon unnecessarily.

## 10.8 Purge behavior
Purging a pack must:
- require explicit user intent,
- explain what space will be freed,
- explain that the pack can be downloaded again later,
- preserve a usable stub/inventory record when appropriate.

## 10.9 Post-purge rule
After purge, the feature should present a clean re-download path rather than treating the pack as unknown.

## 10.10 No-destructive-side-effect rule
Purging a pack must not silently remove unrelated user data or local-first feature state.

---

# 11. Auto-download and consent behavior

## 11.1 Auto-download is convenience, not baseline
Auto-download exists to reduce friction for Supporters and prepared users. It is not required for baseline pack usefulness.

## 11.2 Consent rule
The app may only auto-download packs when all of the following are true:
- the relevant entitlement permits it,
- the user has granted clear consent,
- network/storage/device conditions meet local policy,
- the app is recommending a genuinely useful pack.

## 11.3 Recommended auto-download contexts
Auto-download consent prompts may appear in contexts such as:
- after a successful group join,
- after entering a map context where a missing offline pack would materially help,
- inside Pack Catalog or Settings.

## 11.4 Never-auto-download rule
The app must not auto-download large packs during sacred, emergency, or time-critical flows where the prompt or transfer would increase cognitive load.

## 11.5 Wi‑Fi and user-preference rule
When Wi‑Fi-only or similar preference is enabled, the feature must honor it and wait or ask clearly before using mobile data.

---

# 12. Audio and content distribution behavior

## 12.1 Audio distribution purpose
Audio packs exist to expand offline playback for guided ritual or phrase/emergency surfaces where product policy allows.

## 12.2 Audio source relationship rule
This file governs offline audio-pack availability and install state.
The owning feature family governs playback priority and fallback semantics once the pack is or is not available.

## 12.3 Phrasebook audio relationship
Phrasebook/Emergency may use installed voice or audio packs when:
- the relevant audio pack is installed,
- `AUDIO_OFFLINE` is active when required,
- the owning runtime deems the clip usable.

## 12.4 Ritual audio relationship
Rituals may use installed guided-audio packs when content, entitlement, and runtime support align.
Ritual correctness and step usability must remain meaningful without them.

## 12.5 Content-bundle relationship
If larger structured content bundles are later distributed as packs, they must still preserve:
- governed content provenance,
- explicit versioning,
- compatibility validation,
- offline fallback rules.

## 12.6 Stream-versus-pack honesty rule
If audio can stream online but is not installed offline, the UI should distinguish between:
- streaming available now,
- offline pack available for download,
- no audio currently available.

---

# 13. Storage, quotas, and purge strategy at the feature level

## 13.1 Storage-awareness rule
Pack flows must help users understand storage consequences without forcing them into technical detail.

## 13.2 Pre-download storage checks
Before starting a large download, the flow should check for sufficient space and offer a clear recovery path if storage is low.

## 13.3 Low-storage recovery options
Recovery options may include:
- purging previously installed packs,
- delaying the download,
- changing network/power/storage conditions,
- visiting Settings or device storage guidance.

## 13.4 Suggested purge timing
The feature may suggest purging old or low-priority packs after the relevant journey phase has ended or when device storage is tight.

## 13.5 No-hidden-purge rule
The app must not silently purge installed user-expected packs without explicit documented policy and clear user understanding.

## 13.6 App-private storage rule
Pack artifacts remain app-private by default and are not treated like casual user files.

---

# 14. Pack Catalog behavior

## 14.1 Purpose
Pack Catalog is the main browse and management surface for downloadable offline packs.

## 14.2 Required content blocks
Pack Catalog must support:
- recommended packs section,
- installed packs section,
- discoverable browse-all catalog or filter path,
- install state badges,
- size metadata,
- entitlement or lock-state indicators where relevant,
- storage/network preference awareness where useful.

## 14.3 Sorting priorities
Default sorting should typically favor:
1. recommended current-journey packs,
2. currently downloading or verifying packs,
3. already installed packs,
4. other available packs.

## 14.4 Catalog honesty rule
If the manifest is cached/stale, Pack Catalog may still browse last-known packs but should not imply that the catalog is definitely current.

## 14.5 No-crowding rule
Pack Catalog should not overwhelm the user with too many subtle pack classes or technical columns.
It should help them decide, not perform storage administration like a desktop file manager.

---

# 15. Pack Detail / Install Flow behavior

## 15.1 Purpose
Pack Detail / Install Flow helps the user understand one pack deeply enough to install or manage it.

## 15.2 Required content blocks
Pack Detail should show, where relevant:
- pack title,
- what it improves,
- area or language relevance,
- pack type,
- size,
- install state,
- supporter requirement if applicable,
- primary install/purge action,
- brief storage/network note when needed.

## 15.3 Recommended explanatory content
Use concise sections such as:
- “What you get”
- “Works offline after install”
- “Recommended for Umrah” or equivalent
- “Requires Supporter” where applicable

## 15.4 Detail-state handling
Pack Detail must support:
- not installed,
- downloading,
- verifying,
- installed,
- failed with retry,
- purged,
- locked,
- stale manifest info.

## 15.5 No-overpromise rule
Pack Detail must not promise capabilities the downstream feature cannot actually provide.
Example: a map pack should not imply precise indoor guidance if the map subsystem still needs additional positioning support.

---

# 16. Screen and UX contract for this feature family

## 16.1 Canonical screens
This feature family owns or strongly depends on:
- `pack_catalog`
- `pack_detail_install_flow`

It may also appear through cards or prompts from Home, Group, Maps, Rituals, Phrasebook, and Settings.

## 16.2 Pack Catalog UX contract
### Required content blocks
- recommended pack list,
- installed pack list,
- browse-all / filter entry,
- state badge per pack,
- size metadata,
- optional Wi‑Fi/download preference summary.

### Required states
- content ready,
- first-use empty/no installed packs,
- stale manifest browse state,
- offline browse from cached manifest,
- manifest unavailable fallback,
- low-storage hint state.

### Primary actions
- open Pack Detail,
- start install,
- retry failed pack,
- purge installed pack,
- open relevant settings/download preferences.

### Rule
Pack Catalog should help decision-making quickly. It must not resemble a technical asset dashboard.

## 16.3 Pack Detail / Install Flow UX contract
### Required content blocks
- pack summary,
- what it improves,
- size,
- install status,
- install/pause/resume/retry/purge actions as applicable,
- entitlement/lock explanation where relevant.

### Required states
- not installed,
- queued/downloading,
- verifying,
- installed,
- failed,
- locked by entitlement,
- unavailable due to storage/network policy,
- purged with re-download option.

### Rule
This screen must make state transitions understandable and must never imply completion before verification.

---

# 17. Copy, localization, RTL, and accessibility rules

## 17.1 Copy tone
Packs copy must be:
- practical,
- calm,
- honest,
- storage-aware without sounding technical or alarming,
- ethically clear about free versus Supporter.

## 17.2 Recommended copy patterns
Prefer language such as:
- “Download for offline use”
- “Works offline after install”
- “Waiting for Wi‑Fi”
- “Need more storage”
- “You can remove this later”
- “Requires Supporter for offline audio”

Avoid jargon like:
- “checksum mismatch” as primary user copy,
- “artifact registry” or “payload,”
- dense billing language inside pack flows.

## 17.3 Season recommendation copy rule
Recommendation text must remain season-aware and simple.
Examples:
- “Recommended for Umrah”
- “Recommended for Hajj routes”
- “Useful for Arabic phrase audio offline”

## 17.4 RTL and mixed-content rule
Pack IDs, language tags, storage sizes, app versions, and mixed-language titles must remain bidi-safe and readable in RTL contexts.

## 17.5 Accessibility requirements
This feature family must support:
- large text,
- progress communication that is not color-only,
- screen-reader clarity for install state and progress,
- accessible pause/retry/purge controls,
- honest lock-state explanations,
- reduced-motion-safe state transitions.

---

# 18. Offline behavior and degraded states

## 18.1 Offline tier
This feature family itself is mixed-mode:
- browsing known packs is possible from cached manifest,
- installed packs remain usable offline,
- new downloads require network,
- lock-state truth may depend on cached entitlement continuity rules.

## 18.2 Offline guarantees
When offline, the user should still be able to:
- browse last-known pack metadata if cached,
- see installed pack states,
- use installed packs in their owning feature families,
- understand which packs are absent or purged.

## 18.3 Offline browsing rule
The UI must distinguish between:
- installed and ready,
- known from stale manifest,
- not downloadable right now because network is missing.

## 18.4 Manifest-missing rule
If no manifest has ever been cached and network is unavailable, Pack Catalog should show a clear unavailable state rather than an empty misleading catalog.

## 18.5 Protected-state degradation rule
If entitlement freshness is unknown, the app should preserve free and locally-installed free-capable value, but must follow file `24` for supporter-gated pack continuity.

---

# 19. Security and privacy rules for this feature family

## 19.1 Integrity-first rule
A pack must pass integrity verification before the feature layer treats it as ready.

## 19.2 Transport rule
Downloads must use secure transport and must not expose users to unsafe unsigned or casually mutable asset assumptions.

## 19.3 No sensitive-logging rule
Do not log raw signed store payloads, user-specific private identifiers, or security-sensitive artifact references recklessly in pack analytics or diagnostics.

## 19.4 App-private asset rule
Pack artifacts remain app-private and are not exported casually to shared storage.

## 19.5 No-hidden-executable rule
Packs may not act as a covert plugin system or executable logic channel.

---

# 20. Architecture and implementation boundaries

## 20.1 Feature-family module rule
The packs feature family should own:
- presentation and state for Pack Catalog and Pack Detail,
- recommendation logic orchestration,
- user-facing install/purge flows,
- pack-to-feature handoff messaging.

## 20.2 Stable interface examples
Feature implementation should depend on stable roles such as:
- `PackCatalogRepository`
- `PackInstallCoordinator`
- `PackInventoryRepository`
- `PackRecommendationEngine`
- `PackAccessPolicyResolver`
- `PackToFeatureHandoffAdapter`

These are representative interface roles, not locked names.

## 20.3 No-widget-download-manager rule
Screen widgets must not implement low-level download or checksum logic directly.
That behavior belongs behind repositories/coordinators consistent with files `07` and `15`.

## 20.4 Platform mechanism abstraction rule
Whether a pack arrives through app-managed CDN download, iOS-native background asset support, or another approved platform path must remain hidden beneath stable platform/data abstractions.

---

# 21. Analytics and observability requirements

## 21.1 Required analytics events
This feature family must emit the canonical packs/content-distribution events from file `17` and the pack-policy contract, including at minimum:
- `pack_list_view`
- `pack_download_start`
- `pack_download_progress` (sampled)
- `pack_download_done`
- `pack_download_failed`
- `pack_verify_failed`
- `pack_repair_attempt`
- `pack_purged`
- `pack_autodownload_prompt`

## 21.2 Recommended parameters where relevant
- `pack_id`
- `pack_type`
- `pack_version`
- `size_bytes`
- `season`
- `network_state`
- `is_supporter_required`
- `lock_reason`
- `verify_ms`
- `freed_bytes`

## 21.3 Privacy-light analytics rule
Do not send private note content, medical data, or store receipt payloads through this feature family’s telemetry.

## 21.4 Observability priorities
High-signal issues include:
- manifest fetch failures,
- stale-manifest overuse,
- checksum/verify failures,
- repair frequency spikes,
- pack install completion regressions,
- purge-regret patterns where users immediately need to reinstall,
- incorrect season recommendation ordering.

---

# 22. Performance and operational rules for this feature family

## 22.1 Performance authority
Global performance, storage, and size budgets are defined normatively in file `17`.
This feature family must obey them.

## 22.2 Feature-level operational targets
Recommended targets:
- Pack Catalog open from cached manifest ≤ **500 ms** on representative mid-tier devices,
- state badge updates should feel immediate after inventory changes,
- download resume after relaunch should re-enter a live progress state quickly when the runtime supports it,
- install/verify completion must not freeze UI or pretend readiness early.

## 22.3 Size and storage discipline
Base app footprint must remain within project budgets, and pack recommendations must not encourage uncontrolled storage growth.

## 22.4 Operational honesty rule
If a platform or asset path only partially supports background or resume behavior, the UI must remain honest rather than promising seamless background completion it cannot guarantee.

---

# 23. Testing and validation requirements

## 23.1 Required automated coverage
Automated tests must cover at minimum:
- recommendation ordering by season and locale,
- manifest-cache fallback behavior,
- pack state badge mapping,
- install-state transition handling,
- failed verification behavior,
- purge and re-download state behavior,
- entitlement lock-state behavior,
- stale versus current manifest rendering,
- pack-to-feature handoff rules,
- RTL rendering of size/version/language metadata.

## 23.2 Required manual/device validation
Manual or device validation must cover at minimum:
- first install of a recommended pack,
- pause/resume or restart-safe download behavior where supported,
- checksum/verify failure messaging,
- low-storage preflight behavior,
- purge and re-download flow,
- Umrah-season recommendation ordering,
- Hajj-season recommendation ordering when scope is enabled,
- offline browse of cached manifest,
- map layer and audio behavior after install and after purge,
- large-text and screen-reader behavior of install-state and progress controls.

## 23.3 Real-world validation requirement
Before release, representative field validation should confirm:
- users understand which pack to install first,
- the app still feels useful before any pack install,
- downloads/retries remain understandable under weak connectivity,
- purge behavior feels safe rather than destructive,
- Supporter gating remains ethically clear.

## 23.4 Fake-success warning
A successful happy-path download on strong Wi‑Fi is not enough evidence.
Release confidence requires resume, verification failure, offline browsing, storage pressure, and purge behavior on real devices.

---

# 24. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- Pack Catalog and Pack Detail accurately reflect manifest and inventory truth,
- no pack is presented as ready before verification succeeds,
- no-pack baseline app value remains clear and usable,
- season-aware recommendations respect Umrah-first defaults,
- pack gating follows file `24` and stays ethically bounded,
- installed packs remain usable offline in their owning feature families,
- purge behavior is clear and reversible through re-download,
- analytics hooks align with file `17`,
- real-device validation confirms storage/network failure handling is understandable.

---

# 25. Cross-file dependency rules

## 25.1 If pack manifest schema changes
Update:
- this file,
- file `14`,
- file `15`,
- file `13` if local inventory shape changes,
- fixtures and tests.

## 25.2 If pack lifecycle semantics change
Update:
- this file,
- file `15`,
- file `13` if local enum/state changes,
- release evidence requirements where affected.

## 25.3 If audio-pack policy changes
Update:
- this file,
- file `18` and/or `22`,
- file `24` if entitlement semantics change,
- file `17` if telemetry or dashboards change.

## 25.4 If map-pack behavior changes
Update:
- this file,
- file `19`,
- file `16` if subsystem assumptions change,
- file `11` if screen contracts or entry points change.

## 25.5 If recommendation strategy or season behavior changes
Update:
- this file,
- file `03` if product-scope consequences exist,
- file `20` and `25` if Home/Group prompts change,
- tests and release-check scenarios.

---

# 26. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 26.1 Treating packs as required for baseline core value
Forbidden.

## 26.2 Marking a pack installed before integrity verification succeeds
Forbidden.

## 26.3 Hardcoding pack lists or artifact URLs outside the manifest contract
Forbidden.

## 26.4 Turning packs into a hidden code/plugin system
Forbidden.

## 26.5 Overloading Pack Catalog with technical admin detail instead of user-centered guidance
Forbidden.

## 26.6 Suggesting Hajj-oriented packs as the primary default in Umrah-first contexts
Forbidden.

## 26.7 Silently purging packs without clear user understanding or documented recovery policy
Forbidden.

## 26.8 Hiding lock reasons or conflating entitlement lock with missing download state
Forbidden.

## 26.9 Using pack upsell copy that implies correctness or safety is for sale
Forbidden.

## 26.10 Letting widgets implement low-level download, checksum, or storage logic directly
Forbidden.

---

# 27. Implementation priorities

## 27.1 Phase 1 priorities
Implement first:
- manifest-driven Pack Catalog,
- Pack Detail / Install Flow baseline,
- local inventory state rendering,
- install/verify/fail/purge user flows,
- season-aware recommendation ordering,
- pack-to-map and pack-to-audio availability handoff.

## 27.2 Phase 2 priorities
Then add:
- auto-download consent behavior,
- richer recommendation context from Group/Home,
- stronger failure/repair UX polish,
- better storage-management assistance.

## 27.3 Phase 3 priorities
Then refine:
- post-launch recommendation tuning,
- better cross-platform asset-delivery optimizations under the same abstraction,
- smarter but still honest pre-download preparation prompts.

---

# 28. When this file must be updated

This file must be updated whenever any of the following changes:
- pack classes or product meaning,
- Pack Catalog or Pack Detail behavior,
- install/verify/purge UX,
- season-aware recommendation logic,
- auto-download consent behavior,
- audio/content pack policy,
- pack gating semantics visible to users,
- analytics hooks or performance expectations for packs,
- release-readiness expectations for downloadable assets.

If these truths change but this file is not updated, pack UX, entitlement handling, and offline experience will drift quickly.

---

# 29. Summary

This file defines the canonical feature-facing contract for Offline Packs, Audio, and Content Distribution in Pilgrims Mobile App.

It establishes:
- what packs are and what they are for,
- how pack discovery and recommendation work,
- how install/verify/fail/purge behavior is surfaced,
- how entitlement-aware pack access behaves,
- how audio and content packs relate to owning feature families,
- how Pack Catalog and Pack Detail must behave,
- what analytics, testing, and release-readiness expectations must be met.

Its purpose is to ensure the packs feature family becomes:
- trustworthy,
- ethically monetized,
- understandable under storage/network stress,
- and maintainable for long-term AI-assisted implementation without confusing runtime contracts with product behavior.

