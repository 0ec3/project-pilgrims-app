# 22 — FEATURE: PHRASEBOOK, EMERGENCY, SAFETY, AND ASSISTIVE TOOLS

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, content lead, design lead, Flutter engineers, backend engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for the assistance-tools feature family, including Phrasebook behavior, big-text phrase cards, audio and TTS fallback posture, Emergency cards, medical profile handling, safety alerts and contextual advisories, urgent assistive shortcuts, local data behavior, monetization boundaries, analytics hooks, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the Phrasebook, Emergency, Safety, and assistive-tools feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01_README_AND_MASTER_INDEX.md`, `03_PRODUCT_CHARTER_AND_SCOPE.md`, `04_DECISIONS_GLOSSARY_AND_CHANGE_CONTROL.md`, `07_FLUTTER_APP_ARCHITECTURE_AND_MODULE_BOUNDARIES.md`, `08_DESIGN_SYSTEM_THEMES_TOKENS_AND_COMPONENTS.md`, `09_PLATFORM_ADAPTATION_IOS_ANDROID_AND_NATIVE_BRIDGES.md`, `10_PERSONAS_IA_USER_JOURNEYS_AND_TASK_FLOWS.md`, `11_SCREENS_STATES_NAVIGATION_AND_UI_BLUEPRINTS.md`, `12_COPY_LOCALIZATION_RTL_AND_ACCESSIBILITY.md`, `13_DATA_MODEL_RLS_INVARIANTS_AND_MIGRATIONS.md`, `14_API_REALTIME_AND_INTEGRATION_CONTRACTS.md`, `15_OFFLINE_PACKS_SYNC_ASSET_DELIVERY_AND_CACHE_POLICY.md`, `17_ANALYTICS_OBSERVABILITY_AND_PERFORMANCE_BUDGETS.md`, `20_FEATURE_GROUP_HUB_CHECKINS_REGROUP_AND_SHARED_COORDINATION.md`, `21_FEATURE_PLANNER_REMINDERS_WALLET_NOTES_AND_BOOKMARKS.md`
- **Related files:** `23`, `24`, `25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because assistance features are often treated as “small utilities” even though they carry some of the app’s most important real-world trust burden.

For this project, this feature family is especially sensitive because:
- users may need help when stressed, tired, lost, or unable to communicate clearly,
- these tools must remain useful offline,
- AI agents often overfocus on visual polish and underdefine practical recovery behavior,
- medical and urgent-help flows require a stricter privacy posture than ordinary content,
- Safety Alerts must remain non-blocking and calm rather than becoming noisy or alarmist,
- Phrasebook, Emergency, and assistive shortcuts overlap in the user’s mind even if their runtime contracts differ,
- audio packs, text display, and fallback behaviors can easily drift into conflicting rules if not governed centrally.

This file prevents those failures by defining:
- what this assistance-tools family is responsible for,
- what users can and cannot expect,
- how Phrasebook behaves,
- how Emergency cards and medical profile flows behave,
- how safety alerts are layered into the experience,
- what assistive shortcuts exist and how they relate to other feature families,
- how audio, big-text, and fallback behavior should work,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
This feature family exists to help pilgrims:
- communicate basic needs quickly,
- show large readable phrases or help cards under stress,
- access emergency or urgent assistance tools immediately,
- preserve and present a private medical profile when necessary,
- receive calm non-blocking safety advisories,
- reach key recovery shortcuts such as saved gate recall or group safety actions without hunting through the app.

## 2.2 Main user value statement
A pilgrim should be able to open these assistance tools and quickly get help with one of these questions:
- How do I say this clearly to staff or another pilgrim?
- How do I show a big readable emergency card right now?
- How do I access my medical information safely?
- What safety advisory do I need to know right now?
- How do I reach my gate, my group, or another urgent support shortcut quickly?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- immediate,
- readable,
- offline-capable,
- respectful,
- high-clarity,
- dignity-preserving,
- privacy-light but privacy-serious where medical data is involved.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- Phrasebook categories, search, and phrase cards,
- big-text phrase presentation,
- offline and pack-aware phrase audio behavior,
- optional OS TTS fallback posture where approved,
- Emergency root and emergency card behavior,
- emergency numbers and SMS/share template flows,
- on-device medical profile storage, viewing, and explicit export,
- safety banners and safety tips surfaces,
- context-specific non-blocking safety ribbons on approved surfaces,
- urgent assistive shortcuts such as saved gate recall and “I’m Safe” handoff when relevant,
- favorites and assistive display preferences relevant to this family.

## 3.2 Out of scope
This feature family does **not** include:
- live translation,
- cloud backup of medical data,
- automatic emergency dispatch,
- auto-dialing or auto-sending emergency messages without user confirmation,
- medical advice beyond curated guidance and communication support,
- broad crowd prediction or enforcement logic,
- background location or surveillance behavior,
- generalized accessibility settings for the entire operating system.

## 3.3 Boundary with file `14`
File `14` defines the canonical online surface. This feature family only relies on:
- `GET /v1/flags` for safety advisories and simple feature toggles,
- `GET /v1/packs/manifest` and `GET /v1/entitlements` for audio/content pack and entitlement context where needed.

This feature family must not assume a dedicated phrasebook or emergency backend API in V1.

## 3.4 Boundary with file `13`
File `13` is the canonical source of truth for device-local medical profile and other local persistence categories.
This file may define feature-facing local contracts and runtime behavior, but must not contradict file `13`.

## 3.5 Boundary with file `20`
Group owns “I’m Safe” intent and shared coordination truth.
This file only defines how emergency or assistive surfaces may hand off into that action when relevant.

## 3.6 Boundary with file `21`
Notes and Bookmarks own personal capture and library behavior.
This file only defines where phrasebook/emergency/safety surfaces offer capture hooks.

## 3.7 Boundary with file `23`
Pack lifecycle, pack delivery, and asset integrity are owned by file `23`.
This file only defines how phrase audio and related assistance content behave when packs are present, missing, stale, or unavailable.

## 3.8 Boundary with file `24`
Account, subscriptions, entitlements, and settings own entitlement truth and persistent settings authority.
This feature family only reacts to entitlement snapshots and local preferences relevant to its behavior.

## 3.9 Boundary with file `25`
Home, onboarding, and Simple Mode own the global shortcut architecture.
This feature family only defines the destination behavior and assistive meaning of those shortcuts.

---

# 4. Product rules that govern this feature family

## 4.1 Urgent-help-first rule
If a user opens this feature family, they are often under stress or trying to avoid stress.
The design must optimize for action speed, readability, and clarity before feature richness.

## 4.2 Big-text is first-class
Big readable cards are not a decorative mode. They are a primary interaction model for this family.

## 4.3 Offline usefulness rule
Phrasebook, emergency cards, medical profile viewing, and safety fallback must remain meaningfully useful without network.

## 4.4 Safety alerts are advisory, not controlling
Safety Alerts should inform and nudge. They must not block ritual, route, or recovery tasks.

## 4.5 Medical privacy rule
Medical profile data is more sensitive than ordinary app content and must remain local by default with stronger local protection expectations.

## 4.6 User-confirmed communication rule
The app may prefill message or share content, but it must not silently send messages, auto-dial numbers, or pretend official dispatch occurred.

## 4.7 Assistive shortcuts are task shortcuts, not feature duplication
Saved gate, group safe-status, and other urgent shortcuts may appear in this family, but they must hand off to the canonical feature family that owns the deeper behavior.

## 4.8 Calm tone rule
Copy must remain calm, plain, and dignified. No alarmist phrasing, theatrical warning language, or false urgency unless the advisory is genuinely critical.

## 4.9 Ethical monetization rule
Basic communication, emergency cards, medical profile access, and safety advisories must not be paywalled.

---

# 5. Canonical terminology for this feature family

## 5.1 Phrasebook
The feature area for practical bilingual or multilingual communication cards and related phrase search.

## 5.2 Phrase card
A user-visible phrase presentation surface with Arabic and one or more user-language lines, optimized for fast display and optionally audio playback.

## 5.3 Big-text card
A high-clarity presentation mode with very large text and reduced visual clutter, intended for quick showing to another person.

## 5.4 Emergency root
The main urgent-assistance hub for emergency cards, medical profile shortcuts, safety tips, and other assistive shortcuts.

## 5.5 Emergency card
A prepared large-text help card for scenarios such as lost person, medical help, lost documents, police, embassy, or agency desk.

## 5.6 Medical profile
A device-local record of medical and emergency information stored with stronger local protection measures.

## 5.7 Safety alert
A remote-config advisory banner or ribbon delivered through the flags/control-plane path.

## 5.8 Safety tips sheet
A local/helpful explanatory sheet opened from safety alerts or emergency surfaces.

## 5.9 Assistive shortcut
A fast action that helps the user recover practically, such as saved gate recall, “I’m Safe” handoff, medical profile view, or urgent phrase entry.

## 5.10 Voice pack
An offline audio pack containing recorded phrase or guidance audio referenced by content metadata.

---

# 6. User stories

## 6.1 Phrasebook
- **As a pilgrim**, I can open Phrasebook offline and quickly find a phrase I need.
- **As a pilgrim**, I can show a large Arabic + translation card to someone with minimal taps.
- **As a pilgrim**, I can play phrase audio when available, but the card remains useful without audio.

## 6.2 Emergency and medical profile
- **As a pilgrim**, I can open emergency tools from Home, Tools, or Simple Mode and get immediate help.
- **As a pilgrim**, I can view my medical profile locally even without network.
- **As a pilgrim**, I can export my medical profile explicitly when I decide to.

## 6.3 Safety alerts
- **As a pilgrim**, I can see calm short advisories such as heat or crowd warnings without them interrupting key tasks.
- **As a pilgrim**, if I am offline, I still see the last safe known alert state or a local fallback.

## 6.4 Assistive shortcuts
- **As a pilgrim**, I can quickly reach saved gate recall, a group safe-status action, or an urgent phrase card from assistive surfaces.
- **As a low-confidence or elderly user**, I can rely on big-text, obvious actions, and minimal clutter.

---

# 7. Free vs supporter boundaries

## 7.1 Free capability baseline
The following must remain available in the free path:
- phrasebook text and big-text cards,
- local phrase search,
- emergency cards,
- safety alerts and safety tips,
- local medical profile create/view/update/export,
- user-confirmed SMS/share templates,
- emergency numbers visibility and copy/open-in-dialer handoff where supported,
- favorites if this family enables them,
- urgent assistive shortcuts.

## 7.2 Supporter-linked enrichments
Supporter-linked value may include:
- offline phrase audio playback when `AUDIO_OFFLINE` is active,
- richer voice pack access and pace control,
- extended language packs where content distribution policy uses optional packs,
- convenience enhancements that do not reduce baseline safety or communication access.

## 7.3 No paywall on safety or communication basics
A user must never be blocked from accessing phrase text, big-text cards, emergency cards, medical profile, or safety advisories because they are not a Supporter.

## 7.4 Audio entitlement rule
Offline audio is an enrichment. Text and big-text card usefulness must never depend on audio entitlement.

## 7.5 Ethical upgrade placement rule
Upgrade or pack prompts may appear in Phrasebook pack or audio contexts, but must not interrupt urgent emergency or medical-profile use.

---

# 8. Feature architecture overlay

## 8.1 Runtime responsibilities at the feature level
This feature family is responsible for coordinating:
- phrasebook root state,
- category and search state,
- phrase-card presentation state,
- audio availability and playback selection,
- emergency root state,
- emergency card detail state,
- medical profile local access state,
- safety-banner rendering and dismissal state,
- assistive shortcut routing and handoff state,
- feature-family telemetry.

## 8.2 What this feature must not own
This feature must not directly own:
- global entitlement truth,
- pack installation lifecycle,
- group membership or group write truth,
- map route generation or saved-anchor storage truth,
- global accessibility settings for the whole app,
- phone or SMS delivery success as if the app were the transport.

## 8.3 Required stable interfaces
Feature implementation should depend on stable roles such as:
- `PhrasebookRepository`
- `PhraseAudioResolver`
- `EmergencyCardRepository`
- `MedicalProfileRepository`
- `SafetyBannerRepository`
- `SafetyDismissalStore`
- `AssistiveShortcutCoordinator`

These are representative interface roles, not a locked naming requirement.

---

# 9. Content and asset model

## 9.1 Content-source posture
Phrasebook, emergency cards, emergency numbers, and related templates are content assets, not hardcoded widget text.
They ship as bundled content and/or pack-resolved content according to content governance and pack policy.

## 9.2 Canonical content directories
Representative source layout:

```text
content/
  phrasebook/
    categories.json
    phrases_base.json
    phrases_ar.json
    phrases_en.json
    phrases_id.json
    ranking_rules.json
  emergency/
    cards.json
    numbers.json
    sms_templates.json
  safety/
    fallback_strings.json
```

Actual directory names may vary, but the contracts below remain canonical.

## 9.3 Phrase record shape
Each phrase record should expose at minimum:
- `id`
- `category_id`
- `text` map keyed by locale
- optional `variants`
- optional `audio` mapping by locale
- optional `flags`
- optional `keywords`

### Representative shape
```json
{
  "id": "need_wheelchair",
  "category_id": "assistance",
  "text": {
    "ar": "أحتاج إلى كرسي متحرك",
    "en": "I need a wheelchair",
    "id": "Saya perlu kursi roda"
  },
  "variants": [
    {
      "id": "need_wheelchair_urgent",
      "text": {
        "ar": "بشكل عاجل",
        "en": "Urgently"
      }
    }
  ],
  "audio": {
    "ar": {
      "pack_id": "voice_ar_v1",
      "track_id": "need_wheelchair"
    }
  },
  "flags": {
    "hajj_only": false
  },
  "keywords": ["wheelchair", "chair", "help"]
}
```

## 9.4 Category record shape
Each category should expose at minimum:
- `id`
- `title_key` or localized title payload
- `icon`
- optional `sort_order`

## 9.5 Emergency card shape
Each emergency card should expose at minimum:
- `id`
- `title_key` or localized title payload
- `lines`
- optional `cta`
- optional `tags`
- optional `flags`

### Representative shape
```json
{
  "id": "lost_person",
  "title_key": "em.lost_person.title",
  "lines": [
    {"lang": "ar", "text": "فقدت شخصًا من مجموعتي"},
    {"lang": "en", "text": "I lost someone in my group"}
  ],
  "cta": {"type": "sms", "template_id": "lost_person_sms"}
}
```

## 9.6 SMS template shape
Each SMS/share template should expose at minimum:
- `id`
- `text`
- optional `required_fields`

### Representative shape
```json
{
  "id": "lost_person_sms",
  "text": "We lost a member near Gate {{gate}} ({{level}}). Description: {{desc}}."
}
```

## 9.7 Emergency numbers shape
Emergency numbers should expose informational contact entries such as:
- `id`
- `title`
- `number`
- optional `region_scope`
- optional `notes`

### Rule
These numbers are informational or handoff helpers. The app must not claim official verification beyond what governance and content-review processes support.

## 9.8 Ranking rules
Phrase search and category emphasis may use local ranking rules that consider:
- default ranking,
- season,
- locale relevance,
- urgency categories,
- user favorites or recent use.

### Season rule
Hajj-only phrase content must not be promoted in Umrah-first contexts.

## 9.9 Audio-content referential integrity rule
Every referenced `audio.pack_id` must correspond to a valid manifest-discoverable pack when offline audio is expected.

---

# 10. Local data and persistence posture

## 10.1 Canonical persistence posture
This feature family is local-first.
Phrasebook favorites, medical profile data, emergency drafts, safety dismissals, and related preferences remain on device by default.

## 10.2 PhraseFavorite local entity
The runtime may persist:
- `phrase_id`
- `saved_at`

## 10.3 MedicalProfile local entity
This feature family must align with the device-local `medical_profile` contract from file `13`.

### Canonical rule
Medical profile is a single protected local record, not a synced profile table.

## 10.4 Recommended medical-profile runtime fields
At the feature level, medical profile editing and display should support fields such as:
- blood type,
- conditions,
- medications,
- allergies,
- emergency contacts,
- optional freeform notes.

### Rule
The exact storage format may remain encrypted JSON in a single protected local payload as long as editing and export rules remain stable.

## 10.5 EmergencyDraft local entity
The runtime may persist emergency template drafts locally with fields such as:
- `template_id`
- `fields`
- `last_edited_at`

## 10.6 Safety-banner dismissals local entity
The runtime may persist local dismissal state such as:
- `banner_id`
- `dismissed_at`
- optional `banner_version`

## 10.7 Stronger local protection rule
Medical profile and similar sensitive records should use stronger local protection measures than ordinary local content, in line with system architecture and privacy/security policy.

---

# 11. Phrasebook behavior

## 11.1 Purpose
Phrasebook exists to help the user communicate practical needs quickly through large readable multilingual cards.

## 11.2 Core capabilities
Phrasebook must support:
- category browsing,
- on-device search,
- phrase-card detail view,
- favorites where supported,
- big-text display,
- optional audio playback,
- copy/share actions where helpful.

## 11.3 Search rule
Search must be on-device and usable offline.
It should match across Arabic, the active user language, and relevant keywords or metadata.

## 11.4 Search ranking priorities
Search ranking should prefer:
1. exact phrase text matches,
2. exact localized title or keyword matches,
3. current-season relevant phrases,
4. recent or favorite phrases,
5. category-relevant fuzzy matches.

## 11.5 Season-aware ranking rule
In Umrah-first behavior, phrases marked `hajj_only` or strongly Hajj-specific must not be promoted as primary results.
They may remain suppressed or secondary according to approved content policy.

## 11.6 Phrase-card presentation rule
Phrase Card Detail must prioritize:
- Arabic line prominence where relevant,
- readable user-language translation,
- very large text,
- simple audio/favorite/copy actions,
- minimal clutter.

## 11.7 Big-text card behavior
Big-text mode should:
- fill most of the screen,
- minimize chrome,
- maintain strong contrast,
- support quick previous/next where it improves flow,
- allow easy dismiss or back behavior.

## 11.8 Phrase favorites rule
Favorites should be lightweight and local.
They are a retrieval aid, not a separate social or synced list.

## 11.9 Copy/share rule
Phrase copy/share may be offered where useful, but the primary experience remains showing the phrase card directly.

---

# 12. Phrase audio and TTS behavior

## 12.1 Purpose
Audio is a supportive aid for pronunciation and comprehension. It is not required for phrase usefulness.

## 12.2 Audio source priority
When the user requests phrase playback, the runtime should prefer:
1. verified installed offline voice-pack clip,
2. online stream if supported and network is available,
3. optional system TTS fallback only where explicitly allowed and platform/language quality is acceptable,
4. text-only fallback if no acceptable audio source exists.

## 12.3 Offline-audio entitlement rule
Offline audio requires:
- an installed audio pack,
- `AUDIO_OFFLINE` entitlement when that gate is active,
- runtime support.

## 12.4 No-audio fallback rule
If phrase audio is unavailable, the feature must remain fully usable through text and big-text presentation.
The UI should say audio is unavailable rather than silently failing.

## 12.5 Pace control rule
If audio playback is supported, pace control may be offered as a convenience enhancement, but it must remain simple and not crowd the phrase card.

## 12.6 TTS caution rule
System TTS must not be treated as guaranteed content parity with reviewed recorded audio.
If TTS fallback is used, the UI should not imply it is the same as a curated voice-pack recording.

## 12.7 Phrasebook audio versus ritual audio rule
This file governs phrasebook/emergency audio behavior only.
It must not be used to weaken ritual-audio boundaries defined elsewhere.

---

# 13. Emergency root and emergency-card behavior

## 13.1 Purpose
Emergency Root exists to provide immediate high-clarity access to urgent practical help.

## 13.2 Core emergency capabilities
Emergency Root must support:
- urgent card shortcuts,
- medical profile shortcut,
- saved gate shortcut where available,
- “I’m Safe” / group handoff where available,
- urgent phrasebook shortcut,
- safety tips or active advisory visibility where relevant.

## 13.3 Emergency card purpose
An Emergency Card exists to communicate one urgent need clearly in a large readable form.

## 13.4 Core emergency-card categories
Representative categories may include:
- lost person,
- medical help,
- police/security,
- lost documents,
- embassy/consulate,
- agency desk,
- wheelchair or mobility help.

## 13.5 Emergency-card CTA rule
Where relevant, an Emergency Card may offer one or more of:
- copy message,
- open SMS/share template,
- open dialer with number prefilled,
- open related urgent phrase.

## 13.6 No auto-dispatch rule
Even when a CTA exists, the app must not auto-send or auto-dial without the user’s explicit action.

## 13.7 Emergency-root sparse-data rule
Emergency Root must remain useful even when:
- no medical profile exists,
- no saved gate exists,
- no group is joined,
- no network exists.

## 13.8 Assistive shortcut rule
Emergency Root may expose quick actions into:
- saved gate recall,
- group safe-status flow,
- urgent phrasebook categories,
- medical profile,

but must not own the deeper logic those other feature families govern.

---

# 14. Medical profile behavior

## 14.1 Purpose
Medical profile allows the user to keep essential medical and emergency information accessible on-device and presentable when needed.

## 14.2 Core profile capabilities
Medical profile must support:
- create or update local record,
- read-only presentation mode,
- explicit export,
- local deletion or clear action.

## 14.3 Local-only rule
Medical profile remains local by default.
No hidden sync, upload, analytics collection, or backend dependency is allowed for normal use.

## 14.4 Local protection rule
Viewing or exporting the medical profile may require an extra local-protection step such as app passcode or biometric confirmation if the security/privacy configuration requires it.

## 14.5 Presentation rule
Medical profile presentation must be:
- readable,
- low-clutter,
- easy to hand over physically,
- usable in large text mode,
- understandable without the edit form being visible.

## 14.6 Export rule
Export is explicit and user-initiated.
The app may export a human-readable card or PDF summary stored or shared only through explicit user choice.

## 14.7 No overbuilt medical scope rule
The profile is an emergency communication aid, not a medical-records platform.

---

# 15. Safety alerts and safety tips behavior

## 15.1 Purpose
Safety Alerts exist to deliver calm, concise, remote-config advisories without interrupting the user’s core tasks.

## 15.2 Control-plane rule
Safety alerts are delivered through the lightweight flags/control-plane path, not a separate alert backend and not push notification infrastructure.

## 15.3 Banner model
A safety banner should expose at minimum:
- `id`
- `kind` or `level`
- user-facing text
- optional start/end time
- optional `aoi` or context hint
- optional version or update marker.

## 15.4 Safety levels
The canonical levels are:
- `info`
- `warn`
- `critical`

## 15.5 UI rule
Safety banners must be:
- calm,
- short,
- dismissible where appropriate,
- visually prioritized by level,
- limited in number to avoid alert fatigue.

## 15.6 Non-blocking rule
Safety alerts must not interrupt ritual step flows or force deep modal handling.

## 15.7 Surface rules
Approved safety surfaces include:
- Home banner strip,
- Safety Tips sheet,
- subtle context ribbons on selected surfaces such as Maps or Group,
- visibility inside Emergency Root when relevant.

## 15.8 Ritual non-interruption rule
Ritual step/detail screens remain banner-free.

## 15.9 Dismissal rule
Dismissals persist locally until expiration or material content/version change.

## 15.10 Offline fallback rule
When offline, the feature should use:
- last-good cached flags/banner state,
- local fallback safety strings when no safe cached state exists,
- clear stale handling where it matters.

## 15.11 Safety Tips sheet rule
Safety Tips sheet is primarily local/offline-help content and should remain available even if fresh flags are unavailable.

---

# 16. Assistive shortcuts behavior

## 16.1 Purpose
Assistive shortcuts exist to reduce the number of steps required to reach high-value recovery actions under stress.

## 16.2 Canonical shortcut examples
This feature family may expose shortcuts such as:
- open urgent phrase category,
- open saved gate recall,
- open “I’m Safe” handoff,
- open medical profile,
- open current critical safety advisory.

## 16.3 Shortcut ownership rule
The shortcut surface may live here, but the destination behavior remains owned by the canonical destination feature.

## 16.4 Simple Mode relationship rule
Simple Mode may reuse these assistance surfaces or shortcuts with reduced framing, but it must not duplicate or fork their core logic.

## 16.5 Offline rule
Shortcuts that point to local-first destinations must remain usable offline.
If a shortcut points to a degraded or online-required destination, the app must explain that state clearly.

---

# 17. Screen and UX contract for this feature family

## 17.1 Canonical screens
This feature family owns or strongly depends on the following canonical screens and surfaces:
- `phrasebook_root`
- `phrase_card_detail`
- `emergency_root`
- `emergency_card_detail`
- `medical_profile_view_edit`
- `safety_tips_sheet`

## 17.2 Phrasebook Root UX contract
### Required content blocks
- category shortcuts or grouped list,
- local search,
- recent/favorite phrases where relevant,
- phrase rows with readable preview,
- audio availability cues where relevant.

### Required states
- content ready,
- filtered empty,
- offline fully available,
- audio pack unavailable,
- content missing/corrupt fallback.

### Primary actions
- open phrase card,
- search,
- favorite phrase,
- play audio if available.

### Rule
Phrasebook Root must prioritize retrieval speed and clarity over browsing ornament.

## 17.3 Phrase Card Detail UX contract
### Required content blocks
- Arabic line,
- user-language translation,
- optional transliteration if approved by copy/content policy,
- audio action where available,
- favorite action,
- copy/share action where relevant,
- big-text emphasis.

### Required states
- content ready,
- audio available,
- audio unavailable,
- offline text-only,
- missing translation fallback if needed.

### Rule
The card must be showable to another person immediately without the user doing extra setup.

## 17.4 Emergency Root UX contract
### Required content blocks
- urgent-card shortcuts,
- medical profile shortcut,
- saved gate shortcut if available,
- group safe-status shortcut if relevant,
- urgent phrasebook section,
- active advisory/safety tip entry where relevant.

### Required states
- standard emergency hub,
- sparse-data state,
- offline fully available,
- medical profile protected/locked state.

### Rule
No decorative clutter and no weak contrast.

## 17.5 Emergency Card Detail UX contract
### Required content blocks
- large readable lines,
- clear title,
- optional user-language mirror,
- CTA actions such as copy, SMS/share, or dialer handoff.

### Required states
- card ready,
- missing template field assistance,
- related local data unavailable,
- offline text-only.

### Rule
The card must remain useful even if supporting integration data is absent.

## 17.6 Medical Profile View/Edit UX contract
### Required content blocks
- readable summary view,
- edit path,
- explicit export action,
- delete/clear action,
- local-protection explanation where relevant.

### Required states
- no profile yet,
- profile ready,
- locked/protected,
- export in progress,
- export failure.

### Rule
View mode should be easier to use under stress than edit mode.

## 17.7 Safety Tips Sheet UX contract
### Required content blocks
- grouped tips sections,
- links or shortcuts into Phrasebook/Emergency when relevant,
- active-banner context if present,
- dismiss or close action.

### Required states
- local content ready,
- banner-context enriched,
- offline local-only,
- stale banner context.

### Rule
This sheet is informative and calm, not a dense article reader.

---

# 18. Copy, localization, RTL, and accessibility rules

## 18.1 Copy tone
Copy in this feature family must be:
- direct,
- calm,
- respectful,
- practical,
- non-technical,
- non-alarmist.

## 18.2 Phrasebook copy style
Phrasebook cards should avoid clutter and unnecessary explanation.
Short clear text is more important than long contextual prose.

## 18.3 Safety copy style
Safety alerts must stay short and actionable.
Examples:
- “High temperature today. Hydrate and seek shade.”
- “Crowds expected after prayers. Move with care and stay with your group.”
- “Follow on-ground staff and signage.”

## 18.4 Emergency copy style
Emergency text must support showing a message to another person quickly.
It should not assume the user can explain the situation in detail verbally.

## 18.5 Mixed-language and RTL rule
Arabic and user-language text, numbers, gate references, and mixed-language phrases must remain bidi-safe and readable in RTL contexts.

## 18.6 Big-text accessibility rule
Phrase and emergency cards must support very large readable text, strong contrast, and minimal chrome.

## 18.7 Screen-reader rule
Core actions such as play, copy, export, and urgent-card selection must have strong semantic labels and must remain understandable with assistive technologies.

## 18.8 Reduced-transparency, contrast, and appearance rule
If reduced transparency, high contrast, or similar accessibility settings are active, cards and urgent surfaces must prefer clarity over decorative material effects.

Emergency, medical, big-text, and assistive surfaces must remain explicitly high-contrast and low-decoration in both Light and Dark. Soft Surface depth or glow must never become the only indicator of urgency, selection, error, or disabled state.

## 18.9 No map-only emergency dependency rule
Emergency or assistive flows must not depend on map visibility, subtle color-only state, or small controls.

---

# 19. Offline behavior and degraded states

## 19.1 Offline tier
This feature family is strongly local-first.

## 19.2 Offline guarantees
The following must work meaningfully offline:
- phrasebook browse and search over installed text assets,
- phrase-card display,
- emergency-card display,
- medical profile view/edit using local data,
- safety tips sheet local content,
- last-known safety banner state or local fallback,
- assistive shortcuts into other local-first surfaces.

## 19.3 Online-support degradation rule
If fresh flags, entitlements, or pack metadata are unavailable:
- the family should continue from local state,
- audio affordances may degrade honestly,
- safety advisories should use last-good or local fallback content.

## 19.4 Pack-missing rule
If a voice pack is missing, text and big-text functionality remain fully usable and the UI may optionally offer a pack prompt when appropriate.

## 19.5 Corrupt-content rule
If phrase or emergency content assets are partially missing or corrupt, the feature must degrade to the best safe subset and surface observability signals rather than crashing.

---

# 20. Security and privacy rules for this feature family

## 20.1 No hidden upload rule
Medical profile, emergency drafts, phrase favorites, and similar local data must not be uploaded automatically.

## 20.2 Minimal permission rule
This family should request only permissions directly relevant to the user’s chosen action, such as media/file access for import or local notifications if future feature behavior genuinely needs them.

## 20.3 Medical data logging rule
Do not log medical profile content, emergency contact details, or sensitive user-entered emergency descriptions recklessly in analytics or diagnostics.

## 20.4 Sharing rule
All SMS/share and export flows remain explicitly user-initiated.

## 20.5 Numbers/dialer rule
If the app offers a dialer handoff, it must remain explicit and user-confirmed. The app is not an emergency dispatch service.

---

# 21. API, flags, and integration behavior

## 21.1 Flags dependency
Safety Alerts rely on `GET /v1/flags` and must obey ETag and last-good-cache behavior.

## 21.2 Flags surface rule
Flags may influence:
- season,
- safety banners,
- light assistance toggle behavior,
- copy ordering,

but must not be used to redefine this feature family’s core contracts ad hoc.

## 21.3 Entitlement dependency
Audio/offline enrichments should use the trusted entitlement snapshot from `GET /v1/entitlements`.

## 21.4 Pack dependency
Voice-pack availability must be derived from manifest and local pack state, not from hardcoded assumptions.

## 21.5 Group handoff dependency
Emergency or assistive “I’m Safe” handoffs must call into Group-owned flows and respect Group’s privacy-light rules.

---

# 22. Performance and operational rules for this feature family

## 22.1 Performance authority
Global budgets are defined normatively in file `17`.
This feature family must obey them.

## 22.2 Feature-level operational targets
Recommended feature-level targets:
- Phrasebook Root open to usable state ≤ **400 ms** with installed local content,
- phrase-card open p95 ≤ **250 ms**,
- emergency root open p95 ≤ **500 ms**,
- emergency card open p95 ≤ **350 ms**,
- safety tips sheet open p95 ≤ **200 ms**,
- cached flags safety-banner render remains lightweight enough to avoid visible frame jank on supported devices.

## 22.3 Reliability priorities
This feature family must optimize for:
- near-instant big-text presentation,
- offline readability,
- honest audio availability,
- stable safety-banner caching and dismissal,
- graceful degradation before failure.

---

# 23. Analytics and observability requirements

## 23.1 Required analytics events from file `17`
This feature family must emit at minimum:
- `phrasebook_root_view`
- `phrasebook_phrase_view`
- `phrasebook_audio_play`
- `phrasebook_big_text_open`
- `emergency_root_view`
- `emergency_card_open`
- `emergency_sms_template_use`
- `medical_profile_view_local`
- `medical_profile_export`

## 23.2 Safety-alert telemetry naming rule
Because file `17` currently defines no dedicated `safety_*` family, safety-alert interactions in this feature family should use canonically governed temporary names under `journey_*` or `screen_*` patterns until file `17` is extended explicitly.

Recommended examples:
- `journey_safety_banner_view`
- `journey_safety_banner_dismiss`
- `journey_safety_tips_open`
- `journey_safety_context_ribbon_view`

## 23.3 Required parameters where relevant
- `season`
- `phrase_category`
- `audio_source`
- `offline_capable`
- `banner_level`
- `banner_id`
- `shortcut_kind`
- `network_state`
- `pack_state`

## 23.4 Privacy-light analytics rule
Do not capture medical-profile content, message-body freeform user text, emergency contact numbers, or sensitive draft fields as analytics parameters.

## 23.5 Observability priorities
High-signal issues include:
- missing or corrupt content assets,
- phrase search index failures,
- pack-audio lookup failures,
- safety-banner parse/cache regressions,
- medical-profile local-protection or export failures,
- emergency template field-resolution failures.

---

# 24. Testing and validation requirements

## 24.1 Required automated coverage
Automated tests must cover at minimum:
- phrase search ranking and season filtering,
- phrase-card rendering with Arabic + user-language lines,
- big-text presentation state,
- audio source selection and fallback order,
- voice-pack missing behavior,
- emergency-card template field filling,
- medical-profile local encryption/decryption boundaries at repository level,
- explicit export behavior,
- safety-banner sorting, expiry, and dismissal persistence,
- stale cached flags handling,
- assistive shortcut routing/handoff behavior.

## 24.2 Required manual/device validation
Manual or device validation must cover at minimum:
- phrasebook fully offline,
- big-text phrase use under large text and RTL,
- emergency root with no medical profile/saved gate/group joined,
- medical-profile create/view/export on real device,
- SMS/share template flow with user confirmation,
- voice-pack playback offline when installed,
- text-only fallback when audio is unavailable,
- safety banner behavior on Home and context ribbons on approved screens,
- Ritual screens remain banner-free,
- screen-reader usability for core assistance actions.

## 24.3 Real-world validation requirement
Before release, representative field testing should validate:
- phrase retrieval speed under stress,
- readability of big-text cards outdoors or in crowded conditions,
- emergency shortcut usefulness from Home or Simple Mode,
- medical-profile handover clarity,
- calmness and usefulness of safety alerts without alert fatigue.

## 24.4 Fake-success warning
A rendered phrase card in a simulator is not enough evidence.
Release confidence requires offline use, large-text readability, emergency shortcut testing, safety-banner caching, and audio fallback validation.

---

# 25. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- Phrasebook works offline with meaningful search and big-text display,
- emergency root remains useful with sparse data,
- medical profile remains local and explicitly exportable,
- safety alerts use cached flags or safe local fallback without interrupting rituals,
- assistive shortcuts hand off coherently to saved gate and group actions,
- offline audio enrichment works only when entitlement, pack, and runtime support align,
- text remains fully useful without audio,
- analytics hooks align with file `17`,
- real-device validation confirms the family reduces stress rather than adding friction.

---

# 26. Cross-file dependency rules

## 26.1 If phrase or emergency content schema changes
Update:
- this file,
- file `26` when content-governance or publishing rules are affected,
- file `23` if pack asset mapping changes,
- tests and fixtures.

## 26.2 If medical-profile storage or export behavior changes
Update:
- this file,
- file `13`,
- file `29` if privacy/security posture changes,
- release evidence expectations if materially affected.

## 26.3 If safety-banner contract changes
Update:
- this file,
- file `14`,
- file `17` if telemetry naming or analytics family changes,
- tests and cached payload fixtures.

## 26.4 If assistive shortcuts change
Update:
- this file,
- the owning destination feature file(s),
- file `11` if screen/state/navigation contracts change,
- file `25` if Home/Simple Mode shortcut behavior changes.

## 26.5 If audio entitlement or pack policy changes
Update:
- this file,
- file `23`,
- file `24`,
- file `17` if observability or event semantics change.

---

# 27. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 27.1 Treating phrasebook or emergency as online-only
Forbidden.

## 27.2 Hiding urgent assistance deep inside secondary navigation
Forbidden.

## 27.3 Auto-sending or auto-dialing emergency communication
Forbidden.

## 27.4 Uploading medical profile by default
Forbidden.

## 27.5 Making offline phrase audio a prerequisite for phrase usefulness
Forbidden.

## 27.6 Letting safety alerts interrupt ritual step flows
Forbidden.

## 27.7 Treating safety alerts as a real-time tracking system
Forbidden.

## 27.8 Replacing clear big-text cards with visually clever but low-legibility surfaces
Forbidden.

## 27.9 Logging medical or emergency freeform details into analytics
Forbidden.

## 27.10 Turning assistive shortcuts into duplicated feature logic that forks the product architecture
Forbidden.

---

# 28. Implementation priorities

## 28.1 Phase 1 priorities
Implement first:
- Phrasebook Root and Phrase Card Detail,
- Emergency Root and Emergency Card Detail,
- local medical profile storage and display,
- safety banner caching/rendering using flags,
- urgent assistive shortcuts from Home/Tools/Simple Mode,
- fully offline text/big-text support.

## 28.2 Phase 2 priorities
Then add:
- favorites and better phrase search ranking,
- voice-pack offline audio integration,
- explicit export/share polish,
- safety context ribbons on approved surfaces,
- stronger emergency template composition helpers.

## 28.3 Phase 3 priorities
Then refine:
- optional system TTS fallback where approved,
- richer locale coverage and pack-driven language expansion,
- field-tested ranking improvements,
- deeper assistive shortcut polish based on real use evidence.

---

# 29. When this file must be updated

This file must be updated whenever any of the following changes:
- phrase or emergency content structure,
- phrase audio or TTS policy,
- emergency card categories or CTA behavior,
- medical-profile storage or export posture,
- safety-banner surface behavior,
- assistive shortcut behavior,
- audio entitlement behavior,
- analytics hooks for this feature family,
- release-evidence expectations tied to phrasebook, emergency, safety, or assistive tools.

If these truths change but this file is not updated, implementation and QA will drift quickly.

---

# 30. Summary

This file defines the canonical feature-facing contract for Phrasebook, Emergency, Safety, and assistive tools in Pilgrims Mobile App.

It establishes:
- the purpose and boundaries of the assistance-tools family,
- phrasebook and big-text communication behavior,
- emergency-card and medical-profile behavior,
- safety-alert and safety-tip behavior,
- urgent assistive shortcuts and handoff rules,
- local-first privacy posture,
- audio and entitlement boundaries,
- screen contracts,
- required analytics, testing, and release-readiness expectations.

Its purpose is to ensure these urgent-support tools become:
- calm,
- readable,
- offline-capable,
- privacy-respecting,
- and maintainable for long-term AI-assisted implementation.



# Guide Marketplace safety boundary

Hire a Guide is not an emergency or safety-response substitute.

Emergency, phrase support, medical-profile basics, Save My Gate recovery, and Group safe/regroup actions remain higher-priority urgent support surfaces and must not be displaced by guide discovery/contact.

Guide profiles/listings must not:
- advertise automatic emergency dispatch,
- imply official emergency authority without verified legal basis,
- replace official emergency numbers or curated safety guidance,
- receive hidden access to the user's medical profile, precise location, or emergency data.

If a guide-related report concerns immediate safety, the report UX may direct the user toward appropriate emergency/official support, but report submission itself is not emergency dispatch.
