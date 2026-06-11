# 23 — FEATURE: OFFLINE PACKS, AUDIO, AND CONTENT DISTRIBUTION

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, backend engineers, infra/release engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for Pack Catalog, Pack Detail / Install Flow, offline pack discovery, downloadable audio and content pack behavior, recommendation logic, entitlement-aware pack access, install/verify/purge UX, content-distribution policy, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the user-facing packs and downloadable-asset feature family. File `15` owns technical pack lifecycle and trust-chain rules. File `26` owns governed content publishing. File `31` hardens quality-first requirements.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `06`, `07`, `08`, `09`, `11`, `12`, `13`, `14`, `15`, `17`, `18`, `19`, `20`, `21`, `22`, `24`, `25`, `26`, `27`, `28`, `29`, `30`, `31`, `CONTRACTS/content_pack_trust_chain_contract.yaml`, `CONTRACTS/entitlement_capability_policy.yaml`

---

# 1. Purpose

Downloadable packs let the base app stay lean while providing richer offline value.

This feature family defines user-facing behavior for:
- Pack Catalog,
- Pack Detail / Install Flow,
- recommendations,
- entitlement-aware lock states,
- install/verify/fail/retry/purge UX,
- audio and content pack surfacing,
- pack handoffs into Maps, Rituals, Phrasebook, Home, and Group.

---

# 2. Product promise

A pilgrim should be able to answer:
- What offline packs are available?
- Which one should I download first?
- Is this optional, recommended, or gated by Supporter?
- How much storage will it use?
- Is it ready yet?
- What happened if verification failed?
- Can I safely remove it later?

The experience must feel clear, trustworthy, storage-aware, season-aware, ethically monetized, and useful even when no pack is installed.

---

# 3. Scope and boundaries

## 3.1 In scope
- Pack Catalog behavior,
- Pack Detail / Install Flow behavior,
- recommendation logic,
- pack classes and user-facing descriptions,
- download/verify/fail/retry/purge UX,
- Wi-Fi/mobile-data preference interaction,
- auto-download consent behavior where entitled,
- season-aware/context-aware pack suggestions,
- pack lock states and upgrade messaging,
- user-facing audio/content distribution semantics.

## 3.2 Out of scope
- low-level download engine internals,
- store subscription truth,
- feature-specific audio player behavior,
- map rendering internals,
- scholar-review workflow,
- generalized file sync,
- ads or promotional surfaces.

## 3.3 Boundary with file `15`
File `15` owns offline tiers, pack lifecycle states, manifest caching, storage, trust-chain verification, last-known-good behavior, and sync policy.
This file turns those contracts into user-facing UX.

## 3.4 Boundary with file `26`
If governed content is distributed as a pack, file `26` governs review, provenance, signing, activation, emergency correction, and rollback.

## 3.5 Boundary with file `24`
File `24` owns Supporter truth and entitlement semantics. This file reacts to gates such as `PACK_AUTO_DOWNLOAD` and `AUDIO_OFFLINE`.

---

# 4. Product rules

## 4.1 Base-app-light rule
Heavy map/audio/media assets should live in packs where feasible.

## 4.2 No-pack usefulness rule
The app must remain meaningfully useful when no downloadable pack is installed.

## 4.3 Trust-chain-before-ready rule
A pack is not ready until all required verification succeeds.
User-facing “ready” or “installed” state requires the applicable checks from file `15`, including manifest signature, artifact checksum, artifact signature, signing-key validity, compatibility, and storage-completeness checks.

## 4.4 Ethical pack-gating rule
Supporter may gate convenience and richer offline assets, but packs must never become a hidden paywall on ritual correctness, baseline safety, phrase text, or core orientation recovery.

## 4.5 Season-aware recommendation rule
Recommendations remain Umrah-first by default and must not surface Hajj-oriented assets as primary recommendations outside approved season/scope.

## 4.6 User-consent rule
Large downloads and auto-download behavior require understandable user consent and must respect network/storage preferences.

## 4.7 Purge-with-dignity rule
Users may remove packs without fear of damaging the app. The app must explain what remains available after purge.

## 4.8 No executable-code rule
Packs contain data/media/content artifacts, not executable feature logic or a covert plugin system.

---

# 5. Canonical terminology

- **Pack:** versioned downloadable asset bundle that expands offline value.
- **Pack Catalog:** browse/manage surface for packs.
- **Pack Detail / Install Flow:** single-pack explanation and management flow.
- **Installed pack:** pack that passed trust-chain verification and is locally registered.
- **Failed pack:** candidate that failed download, trust-chain, compatibility, or storage checks.
- **Purged pack:** previously installed pack removed from local storage.
- **Last-known-good pack:** currently trusted installed pack retained when a candidate update fails.
- **Voice pack:** phrasebook/assistance audio bundle.
- **Guided audio pack:** guided ritual or structured audio bundle.

---

# 6. Canonical pack categories

Aligned with file `15`:
- `MAP`
- `AUDIO`
- `CONTENT`
- `MEDIA`

`CONTENT` packs are allowed only where larger structured offline bundles are justified and governed. They must not bypass file `26`.

---

# 7. Discovery and recommendations

## 7.1 Discovery source
The pack manifest is the canonical discovery surface. The client must not hardcode downloadable asset lists or artifact locations.

## 7.2 Recommendation inputs
Recommendation ordering may consider:
- current season,
- locale/language,
- installed inventory,
- entitlement snapshot,
- active group or joined-group suggestion context,
- map/ritual/phrasebook entry point,
- area-of-interest context.

## 7.3 Umrah-first recommendation
When `season=umrah`, prioritize:
1. Haram high-resolution map pack,
2. relevant app-language audio or voice pack,
3. other appropriate general-purpose packs.

## 7.4 Hajj-capable recommendation
Hajj-oriented packs may be prioritized only when season/scope explicitly permits it.

## 7.5 Stale manifest rule
A cached manifest may be used for last-known browsing, but UI must not imply it is definitely current.

---

# 8. Entitlement behavior

## 8.1 Free baseline
The following must not require Supporter:
- core ritual text/RIC correctness,
- basic phrase text,
- emergency cards,
- Save My Gate recall,
- basic map/orientation fallback,
- installed free baseline packs where offered.

## 8.2 Supporter convenience
Supporter may unlock:
- `PACK_AUTO_DOWNLOAD`,
- `AUDIO_OFFLINE`,
- richer large offline assets,
- other convenience approved by file `24` and the entitlement capability contract.

## 8.3 Lock-state rule
Lock states must explain convenience/enrichment value without implying correctness or safety is withheld.

---

# 9. Install state model

User-facing states:
- not installed,
- queued,
- downloading,
- verifying,
- installed,
- failed,
- purged,
- locked,
- stale manifest,
- unavailable due to network/storage/compatibility.

## 9.1 Verify state
Verification must clearly communicate that the pack is still being prepared and is not ready yet.

## 9.2 Failure states
Failures must distinguish where possible:
- network/download failed,
- low storage,
- checksum failed,
- manifest signature failed,
- artifact signature failed,
- signing key revoked or unavailable,
- app version incompatible,
- manifest stale/unavailable,
- entitlement unavailable,
- user cancelled.

Use calm user copy. Technical details may exist in diagnostics but should not be the primary user-facing message.

## 9.3 Last-known-good rule
A failed candidate must not replace a previously installed trusted pack. UI should preserve and explain the current safe installed state when available.

---

# 10. Pack Catalog behavior

Pack Catalog must include:
- recommended packs,
- installed packs,
- browse/filter path,
- install state badges,
- size metadata,
- entitlement/lock indicators,
- storage/network preference awareness,
- stale manifest state.

Pack Catalog should help decision-making quickly and must not resemble a technical asset dashboard.

---

# 11. Pack Detail / Install Flow behavior

Pack Detail must include:
- pack title,
- what it improves,
- area/language relevance,
- pack type,
- size,
- install state,
- Supporter requirement if applicable,
- install/pause/resume/retry/purge actions,
- storage/network note,
- verification/failure explanation when relevant.

Required states:
- not installed,
- queued/downloading,
- verifying,
- installed,
- failed with retry,
- failed but last-known-good preserved,
- locked by entitlement,
- unavailable due to storage/network/compatibility,
- purged with re-download option,
- stale manifest info.

---

# 12. Auto-download and consent

Auto-download is convenience, not baseline.

It may occur only when:
- entitlement permits it,
- user has granted clear consent,
- network/storage/device conditions meet policy,
- the recommended pack is genuinely useful.

Auto-download prompts must not appear during sacred, emergency, or time-critical flows where they increase cognitive load.

---

# 13. Audio and content distribution

## 13.1 Audio packs
Audio packs expand offline playback for guided ritual or phrase/emergency surfaces. If audio is unavailable, text remains meaningful.

## 13.2 Phrasebook audio
Phrasebook/Emergency may use installed voice/audio packs when installed, entitled where required, and runtime-compatible.

## 13.3 Ritual audio
Rituals may use installed guided-audio packs when content, entitlement, and runtime support align. Ritual correctness and step usability remain meaningful without audio.

## 13.4 Content bundles
Larger content bundles must preserve governed content provenance, explicit versioning, signed artifact metadata, compatibility validation, and offline fallback rules.

---

# 14. Storage and purge

Pack flows must help users understand storage consequences without forcing technical detail.

Purging a pack must:
- require explicit user intent,
- explain what space will be freed,
- explain what will remain available,
- preserve unrelated local-first user data,
- provide a re-download path where possible.

The app must not silently purge user-expected packs without explicit documented policy and clear user understanding.

---

# 15. Copy, localization, RTL, and accessibility

Copy must be practical, calm, honest, storage-aware, and ethically clear.

Preferred copy patterns:
- “Download for offline use”
- “Works offline after install”
- “Verifying pack”
- “Couldn’t verify this pack”
- “Current installed pack is still available”
- “Waiting for Wi-Fi”
- “Need more storage”
- “You can remove this later”

Avoid exposing low-level technical terms as primary copy unless diagnostics/support context requires it.

Accessibility requirements:
- large text,
- progress communication not color-only,
- screen-reader clarity for install and failure states,
- accessible pause/retry/purge controls,
- reduced-motion-safe state transitions.

---

# 16. Analytics and observability

This feature family must emit canonical events from file `17`, including:
- `pack_catalog_view`,
- `pack_detail_view`,
- `pack_download_start`,
- `pack_download_fail`,
- `pack_verify_start`,
- `pack_checksum_fail`,
- `pack_manifest_signature_fail`,
- `pack_artifact_signature_fail`,
- `pack_signing_key_revoked_fail`,
- `pack_compatibility_fail`,
- `pack_last_known_good_preserved`,
- `pack_install_complete`,
- `pack_purge_complete`.

Analytics must not include sensitive artifact secrets, private user content, or unnecessary identifiers.

---

# 17. Testing and release evidence

Tests must cover:
- catalog ready/stale/offline states,
- install success,
- download interruption/resume,
- low storage,
- checksum failure,
- manifest signature failure,
- artifact signature failure,
- revoked signing key,
- compatibility failure,
- last-known-good preservation,
- purge and re-download,
- entitlement lock states,
- large text and screen reader behavior.

Release evidence must include validation against `CONTRACTS/content_pack_trust_chain_contract.yaml` where pack/content delivery behavior changes.

---

# 18. Definition of done

This feature family is ready when:
- Pack Catalog and Pack Detail support required states,
- no pack appears installed before required verification succeeds,
- last-known-good is preserved on candidate failure,
- entitlement behavior follows file `24` and capability policy,
- pack failures are understandable without technical overload,
- purge behavior preserves user data,
- analytics and release evidence match files `17`, `27`, and `28`.

---

# 19. AI-agent checklist

Before editing packs/audio/content-distribution code, an AI agent must:
1. Read files `15`, `17`, `23`, `24`, `26`, `28`, `29`, `30`, and `31`.
2. Read `CONTRACTS/content_pack_trust_chain_contract.yaml` and `CONTRACTS/entitlement_capability_policy.yaml`.
3. Confirm pack lifecycle state.
4. Confirm entitlement behavior.
5. Confirm trust-chain verification and last-known-good behavior.
6. Never mark a pack installed before verification succeeds.
7. Never ship executable logic inside a pack.

---

End of file.