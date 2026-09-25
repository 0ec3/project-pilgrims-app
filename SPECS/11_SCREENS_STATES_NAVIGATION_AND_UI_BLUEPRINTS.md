# 11 — SCREENS, STATES, NAVIGATION, AND UI BLUEPRINTS

## Document status
- **Type:** Normative screen contract and navigation blueprint document
- **Priority:** Highest
- **Audience:** Product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents
- **Purpose:** Define the canonical screen inventory, screen purposes, navigation structure, state coverage, modal and sheet rules, empty/loading/error/offline behavior, and UI blueprint requirements so the app is implemented consistently and evaluated against the same screen-level contract.
- **Authority level:** This file is the canonical source of truth for screen-level behavior and screen-to-screen navigation. Design mockups, Flutter screens, and tests must not contradict this document. Feature-family files own business behavior; this file owns screen/state/navigation truth.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `07`, `08`, `09`, `10`, `12`, `15`, `16`, `18`–`25`, `27`, `28`, `31`, `CONTRACTS/screen_feature_traceability.yaml`
- **Related files:** `13`, `14`, `17`, `29`, `30`

---

# 1. Purpose of this file

This file exists because strong architecture and good journeys are still not enough if screen contracts remain vague.

Without a screen-level contract, teams and AI agents often create problems such as:
- inconsistent state handling across screens,
- hidden or duplicated entry points,
- screens that technically exist but do not fit the real user journey,
- pretty layouts with missing offline or error states,
- unpredictable back behavior,
- duplicated sheets and modals with slightly different meanings,
- inconsistent loading, empty, retry, stale, and permission behavior,
- different features inventing their own UI conventions.

This file defines:
- the canonical screen inventory,
- what each screen is for,
- where users can enter it from,
- what states it must support,
- where it can navigate next,
- what UI blueprint information must exist before implementation.

---

# 2. Screen blueprint principles

## 2.1 Every screen must have one clear job
A screen may support several related actions, but it must have a primary purpose.

## 2.2 Every important screen must define all meaningful states
At minimum, a screen must specify:
- default/content state,
- loading state,
- empty state if relevant,
- error state if relevant,
- offline or degraded state if relevant,
- unavailable, stale, locked, or permission-denied state if relevant.

## 2.3 Critical actions must be easy to find
Actions like Start Ritual, Save My Gate, Route to Destination, Create Group, Join Group, I’m Safe, Privacy & Data, and Emergency help must never be buried or hidden behind low-priority UI.

## 2.4 Navigation must be predictable
Users should be able to understand how they got to a screen, what it is for, and how to go back or finish.

## 2.5 A modal is not a substitute for proper information architecture
Use modals and sheets only when they are a better interaction pattern than a full screen.

## 2.6 State honesty matters
If data is stale, permission is missing, route confidence is low, a pack is not installed, a trusted write did not complete, or a privacy/deletion/export operation needs network, the UI must reflect that honestly.

## 2.7 Screen-feature traceability is mandatory
Every implemented screen must map to an owning feature file and critical flow list in `CONTRACTS/screen_feature_traceability.yaml`.

## 2.8 Visual source-of-truth and appearance rule
Screen behavior, IDs, navigation, and feature meaning come from this spec and owning feature specs. Figma mockups are visual references and must not silently add, remove, rename, or reassign canonical product behavior.

Every implemented screen must support complete Light and Dark appearances through the file `08` design system. System appearance is an app-level preference that selects the OS-matched Light/Dark theme; it does not create a third visual contract.

Where the current Figma reference has no verified Dark variant, screen blueprints must use the semantic Dark mappings from file `08` and must not invent or label unverified dark values as Figma-derived.

---

# 3. Canonical navigation model

## 3.1 App shell navigation
The canonical app shell exposes five primary sections:
- Home
- Rituals
- Map
- Group
- Tools

Settings may be reached from Home, Tools, Account Gate, or contextual surfaces, but it is not a sixth primary tab unless file `10` and this file are updated.

## 3.2 Navigation layers
### Layer 1 — Shell destination
Top-level destination selected in app shell.

### Layer 2 — Section root
The root screen for each top-level section.

### Layer 3 — Task screen
A more focused task or detail screen inside a section.

### Layer 4 — Modal/sheet/dialog
Used for focused confirmation, filters, quick actions, short forms, or high-priority interruptions.

## 3.3 Back behavior rule
Back should follow the user’s mental model:
- detail → parent screen,
- modal/sheet → dismiss to underlying context,
- deep linked screen → return to sensible section root if history is shallow.

## 3.4 Cross-section shortcut rule
The app may offer shortcuts from Home or contextual screens into another section’s task flow, but the user should still land in a coherent section context.

---

# 4. Screen taxonomy

## 4.1 Screen categories
The app uses these screen categories:
- root screens,
- hub screens,
- detail screens,
- flow screens,
- modal/sheet surfaces,
- utility overlays.

## 4.2 Root screens
Top-level section roots:
- HomeRoot
- RitualsRoot
- MapRoot
- GroupRoot
- ToolsRoot

## 4.3 Flow screens
Task-oriented full screens such as:
- OnboardingFlow
- GroupCreationFlow
- JoinGroupFlow
- StartRitualFlow
- RoutePreviewFlow
- PackInstallFlow
- PrivacyDataFlow

## 4.4 Detail screens
Focused content or entity views such as:
- RitualStepDetail
- RICResultDetail
- SavedAnchorDetail
- RegroupPinDetail
- WalletItemDetail
- NoteEditor

## 4.5 Modal/sheet surfaces
Short-lived focused surfaces such as:
- quick action sheet,
- destination picker sheet,
- pack status sheet,
- filter sheet,
- permission explanation sheet,
- confirm delete dialog,
- account deletion / data deletion explanation sheet,
- deletion/export status sheet.

---

# 5. Canonical screen inventory

This inventory defines the required screen set for quality-first V1 scope. The app remains calm and progressive even with a rich screen set; Home and Simple Mode must not surface everything at once.

## 5.1 Shell and entry screens
1. Launch / Startup Resolver — `startup_resolver`
2. Onboarding Welcome — `onboarding_welcome`
3. Language / Preferences Setup — `language_preferences_setup`
4. Optional Sign-In / Account Gate — `account_gate`
5. Home Root — `home_root`

## 5.2 Rituals screens
6. Rituals Root — `rituals_root`
7. Start / Resume Ritual Screen — `start_resume_ritual`
8. Ritual Session Overview — `ritual_session_overview`
9. Ritual Step Detail — `ritual_step_detail`
10. RIC Entry — `ric_entry`
11. RIC Result — `ric_result`
12. Ritual Bookmarks / Saved Guidance — `ritual_bookmarks_saved_guidance`

## 5.3 Map screens
13. Map Root — `map_root`
14. Destination Search / Picker — `destination_search_picker`
15. Route Preview — `route_preview`
16. Active Wayfinding / Route Follow — `active_wayfinding`
17. Save Anchor / Save Gate Flow — `save_anchor_flow`
18. Saved Anchor Detail — `saved_anchor_detail`
19. Floor / Level Selector Surface — `floor_level_selector`

## 5.4 Group screens
20. Group Root — `group_root`
21. Group Creation Flow — `group_creation_flow`
22. Join Group Flow — `join_group_flow`
23. Group Live Board — `group_live_board`
24. Check-In Quick Flow — `checkin_quick_flow`
25. Regroup Pin Detail / Route Launch — `regroup_pin_detail`
26. Group Itinerary — `group_itinerary`

## 5.5 Tools screens
27. Tools Root — `tools_root`
28. Planner List — `planner_list`
29. Planner Item Editor — `planner_item_editor`
30. Reminder Editor / Reminder Settings Surface — `reminder_editor`
31. Wallet List — `wallet_list`
32. Wallet Item Detail — `wallet_item_detail`
33. Notes List — `notes_list`
34. Note Editor — `note_editor`
35. Bookmarks List — `bookmarks_list`
36. Phrasebook Root — `phrasebook_root`
37. Emergency / Assistance Root — `emergency_root`
38. Emergency Card Detail — `emergency_card_detail`
39. Pack Catalog — `pack_catalog`
40. Pack Detail / Install Flow — `pack_detail_install_flow`
41. Settings Root — `settings_root`
42. Privacy & Data Flow — `privacy_data_flow`

## 5.6 Simple Mode screens
43. Simple Mode Home — `simple_home`
44. Simple Mode Ritual Shortcut — `simple_ritual_shortcut`
45. Simple Mode Map Shortcut — `simple_map_shortcut`
46. Simple Mode Group Shortcut — `simple_group_shortcut`
47. Simple Mode Emergency Shortcut — `simple_emergency_shortcut`

---

# 6. Shared screen blueprint template

Every screen blueprint or implementation task must answer these fields.

## 6.1 Required blueprint fields
- Screen ID
- Screen name
- Category
- Primary purpose
- Entry points
- Preconditions
- Primary content blocks
- Primary actions
- Secondary actions
- Navigation exits
- States
- Data dependencies
- Offline behavior
- Permission dependencies
- Entitlement dependencies
- Accessibility notes
- Analytics events
- Related feature-family file(s)
- Release-evidence owner

## 6.2 State checklist
For each screen, explicitly consider:
- loading,
- loaded/content,
- empty,
- error,
- offline/degraded,
- stale/cached,
- permission missing,
- unavailable/locked,
- trusted-write failed,
- destructive action pending/complete/failed where relevant.

---

# 7. Quality-critical screen contracts

## 7.1 Home Root
Home Root is a recovery surface, not a feature dump.

### Task priority
1. current ritual status / continue or start ritual,
2. urgent shortcut cluster: Emergency, Phrasebook, Save My Gate, I’m Safe,
3. saved gate / recent map action,
4. active group summary,
5. planner/reminder summary,
6. pack readiness summary,
7. Settings/Tools entry.

Task priority describes what must remain easiest to resume or reach; it does not require the first visible card to be the ritual card. Contextual ambient information such as prayer time may occupy a visual hero position as long as it does not obscure or slow access to higher-priority recovery actions.

### Approved visual composition reference
The supplied Home reference associated with Figma node `21:600` demonstrates this vertical composition:
1. profile/greeting header with notification and Settings actions,
2. prayer/context hero with current-prayer emphasis and prayer-time chips,
3. five compact quick-action tiles,
4. Umrah progress card with milestone stepper,
5. paired Saved Gate and Jama’ah Group compact cards,
6. Plan & Schedule section with date strip and timeline rows,
7. bottom navigation with a centered floating action slot.

The reference also demonstrates the current visual hierarchy:
- white/light canvas,
- dominant cyan/turquoise accent,
- very rounded cards,
- soft raised surfaces,
- compact icon tiles,
- restrained shadows,
- cyan active navigation and action treatment,
- orange secondary planner action treatment.

This visual composition does **not** authorize new feature semantics. Labels, group freshness, saved-gate truth, and planner actions remain governed by their owning feature/data/API specs.

Prayer-time calculation/source behavior and weather sourcing do not currently have an approved runtime owner in the normative feature/API system. Therefore the mockup establishes only visual anatomy for those subfields. Until change control assigns an owner and defines calculation/provider, timezone/location context, freshness, offline/stale behavior, privacy, analytics, and test/release evidence, implementation must omit those data-driven subfields or keep them as clearly non-runtime design reference content rather than guessing or synthesizing values.

The centered floating action is likewise unassigned by the mockup. It must not be inferred as QR/scanner/camera or any other new behavior. The canonical shell remains five primary sections — Home, Rituals, Map, Group, and Tools. The visual slot must not remove or replace Tools; it becomes functional only if mapped to an already-approved canonical route/action and synchronized with this file and `CONTRACTS/screen_feature_traceability.yaml`.

### Required responsive behavior
- Quick actions may wrap, scroll, or adapt to available width rather than shrinking below usable touch targets.
- The paired Saved Gate/Jama’ah Group cards may stack vertically when width or text scale requires it.
- Planner rows must preserve title/time/action legibility at large text and under localization expansion.
- Bottom navigation must preserve safe-area spacing and not allow the centered floating action to obscure labels or system gesture areas.
- RTL must mirror directional layout where appropriate without changing real-world map/direction semantics.
- Light and Dark must keep the same information hierarchy and component anatomy.

Home must remain useful offline and must not request account or permissions before task-linked value is clear.

## 7.2 Group Creation Flow
### Purpose
Create a governed, authenticated group and return a server-generated shareable join code.

### Entry points
- Group Root no-group state,
- Simple Mode Group Shortcut where relevant,
- leader-oriented onboarding handoff only when explicitly selected.

### Preconditions
- authenticated user required before trusted create write,
- network required,
- server write path available.

### Required content blocks
- group name input,
- simple explanation of why sign-in/network is required,
- create action,
- share-code success card,
- safe SMS/share handoff,
- offline/unavailable/rate-limited failure copy.

### Required states
- unauthenticated → Account Gate,
- editing,
- submitting,
- created,
- offline unavailable,
- rate limited,
- validation failed,
- server unavailable,
- idempotent retry resolved.

### Rules
- Do not allow manual canonical code selection.
- Do not import contacts.
- Do not auto-send invitations.
- Do not pretend offline creation succeeded.

## 7.3 Join Group Flow
Join Group connects a user to an existing group by 6-character uppercase alphanumeric code. It must route through Account Gate if needed, validate obvious bad input locally, and rely on server truth for membership.

## 7.4 Group Root
Group Root must show no-group, creating/failed, joined/current, stale-cached, offline, entitlement-limited, unavailable, and auth-required states.
It must include Create Group and Join Group in the no-group state.

## 7.5 Privacy & Data Flow
### Purpose
Help users understand and manage local-only data, server-backed account data, deletion, export, retention, and privacy handoffs.

### Entry points
- Settings Root,
- Account/profile settings,
- deletion/export status deep link where applicable.

### Required content blocks
- local-only data explanation,
- server-backed data explanation,
- delete account / request deletion,
- deletion status,
- local-only data deletion explanation or links,
- export server-backed personal data request,
- retention summary,
- privacy policy / public deletion web handoff where applicable.

### Required states
- guest/no-account explanation,
- authenticated current state,
- offline unavailable for trusted request,
- deletion request submitted,
- deletion in progress,
- deletion complete,
- deletion blocked/failed,
- export requested,
- export unavailable/failed.

### Rules
- Do not imply local-only data was uploaded.
- Do not promise immediate deletion of legally retained records.
- Do not hide deletion/export behind undocumented support channels.

## 7.6 Pack Detail / Install Flow
Pack install must expose download, verifying, installed, failed, purged, low-storage, stale-manifest, signature/checksum failure, and compatibility-failure states.
A pack must never appear runtime-usable before verification and trust-chain checks succeed.

---

# 8. Navigation and modality rules

## 8.1 Account Gate return rule
After successful sign-in, Account Gate must return the user to the initiating task where safe:
- group creation,
- group join,
- purchase/restore,
- deletion/export/status request.

## 8.2 Destructive action rule
Deletion and purge flows require calm confirmation and clear distinction between local-only deletion and server-backed account deletion.

## 8.3 Emergency non-interruption rule
Emergency, medical, ritual-critical, and urgent recovery flows must not be interrupted by upgrade messaging.

## 8.4 Modal scope rule
Use a modal/sheet for short, reversible, focused decisions. Use a full flow for account deletion, export, group creation, pack install, ritual start, and other multi-state tasks.

---

# 9. Accessibility and localization requirements

## 9.1 Accessibility baseline
Every screen must support:
- large text,
- screen reader labels and focus order,
- non-color-only status meaning,
- touch targets appropriate for tired or low-confidence users,
- reduced-transparency / increased-contrast behavior from the design system,
- readable Light and Dark treatment with explicit boundaries for important states.

## 9.2 RTL and localization
Layouts and copy must support RTL and localization expansion. Critical status strings must not be embedded as unlocalized widget literals.

## 9.3 Stale/live accessibility rule
Freshness, stale, expired, locked, offline, and trusted-write failure states must be exposed to assistive technologies.

---

# 10. Analytics and evidence hooks

## 10.1 Screen analytics rule
Every screen must define screen-view and critical-action events through file `17` and feature-family specs.

## 10.2 Privacy rule
Screen analytics must not include raw medical data, raw note text, join codes, precise hidden location, raw purchase payloads, or deletion/export payload details.

## 10.3 Release evidence rule
Every screen tied to a critical flow must have release evidence coverage under file `28`.

Critical screen families include:
- Home / Simple Mode,
- Rituals / RIC,
- Emergency / Phrasebook / Medical,
- Save My Gate / Map fallback,
- Group Creation / Join / Check-in / Regroup,
- Pack Install / Verification,
- Account / Entitlements / Restore,
- Privacy & Data,
- Guide Marketplace provider trust / contact / provider application.

---

# 11. Definition of done

This screen system is ready when:
- all 52 canonical screens have blueprint coverage or approved non-implementation rationale,
- every screen maps to a feature owner,
- critical screens define offline/degraded/stale/error states,
- account and privacy flows return correctly after auth,
- group creation and privacy data flows are implemented as first-class flows,
- design system tokens and copy/l10n rules are followed,
- accessibility requirements are tested,
- release evidence links exist for critical flows.

---

# 12. AI-agent checklist

Before editing UI or navigation code, an AI agent must:
1. Read files `08`, `10`, `11`, `12`, relevant feature files, and `31`.
2. Check `CONTRACTS/screen_feature_traceability.yaml`.
3. Confirm the screen owner and critical flows.
4. Confirm offline, stale, locked, and error states.
5. Confirm accessibility and localization requirements.
6. Avoid adding untracked screens or modals without updating this file and traceability.

# 13. Guide Marketplace canonical screen amendment

File `32` adds five canonical screens. These are task/detail flows reached through Tools or an approved contextual shortcut; none is a sixth shell destination.

48. Guide Marketplace Root — `guide_marketplace_root`
   - **Purpose:** browse/search/filter currently eligible guide listings and understand cached/legal-unavailable states.
   - **Entry:** Tools → Hire a Guide; approved low-priority contextual Home shortcut.
   - **States:** loading, current content, no results, filtered results, error, cached/stale, feature legally/operationally unavailable.
   - **Next:** guide profile detail; provider registration entry where appropriate.
   - **Offline:** optional cached browse only with explicit stale treatment; must not imply old credentials are current.

49. Guide Profile Detail — `guide_profile_detail`
   - **Purpose:** show provider/listing scope, structured pricing, languages/service area/group size, fact-specific current trust signals, Contact Guide, and report action.
   - **States:** current eligible, stale cached, ineligible/removed, contact unavailable/offline, trust-detail disclosure.
   - **Next:** explicit contact handoff or report surface.
   - **Offline:** cached reading may be allowed, but contact resolution requires an online eligibility re-check.

50. Guide Registration Flow — `guide_registration_flow`
   - **Purpose:** authenticated provider application using only required eligibility information.
   - **States:** auth gate, draft, validation failure, submit, online failure, legal/credential program unavailable.
   - **Next:** verification status.
   - **Offline:** trusted submission unavailable; no hidden write queue.

51. Guide Verification Status — `guide_verification_status`
   - **Purpose:** show the provider's trusted application/eligibility lifecycle and re-verification needs.
   - **States:** submitted, under review, verified, rejected, suspended, expired, revoked, re-verification required, stale/unavailable.
   - **Offline:** last-known status may be displayed only as stale/non-authoritative where safe.

52. Guide Listing Editor — `guide_listing_editor`
   - **Purpose:** authenticated provider creation/editing of allowed listing fields.
   - **States:** draft, validation failure, pending review, active, re-review required, suspended/unavailable, offline trusted-write failure.
   - **Offline:** no publish/update success may be invented or silently queued.

## 13.1 Shared Guide Marketplace screen rules
- File `32` owns business behavior.
- `CONTRACTS/screen_feature_traceability.yaml` must map all five IDs.
- Trust state must be text/semantics-first, not color-only.
- Large text, screen reader, Arabic RTL, Light/Dark, stale-state honesty, and legally unavailable state require release evidence.
- Contact/report sheets are subordinate surfaces and are not separate canonical screens in V1.

---

End of file.