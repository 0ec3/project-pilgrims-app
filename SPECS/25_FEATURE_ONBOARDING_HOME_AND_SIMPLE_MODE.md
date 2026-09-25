# 25 — FEATURE: ONBOARDING, HOME, AND SIMPLE MODE

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for first launch, startup resolution, onboarding, language/preference setup, Home Root behavior, urgent shortcut architecture, Simple Mode behavior, first-use pack awareness, and the visual/platform rules that govern the app’s calm entry experience.
- **Authority level:** This file is the canonical source of truth for onboarding, Home, and Simple Mode behavior. File `11` owns the screen inventory. File `24` owns account/settings/privacy-data behavior. File `20` owns group behavior. File `31` supersedes quality-first hardening decisions.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `17`, `18`, `19`, `20`, `21`, `22`, `23`, `24`, `27`, `28`, `29`, `30`, `31`, `CONTRACTS/screen_feature_traceability.yaml`

---

# 1. Purpose

Onboarding, Home, and Simple Mode are the user’s first and most repeated contact with the product.

They must help pilgrims:
- enter the app without confusion,
- reach local-first value before account creation,
- recover into the right section when stressed,
- access urgent help quickly,
- simplify the interface when needed,
- understand stale/offline/protected-state limitations calmly.

---

# 2. Product rules

## 2.1 Home is a recovery surface
Home helps the user resume, recover, and reach urgent help. It is not a feature dump.

## 2.2 Onboarding is short and task-oriented
Onboarding must not become a marketing carousel, permission gauntlet, account funnel, or full settings wizard.

## 2.3 No forced account before value
The user must not be forced through account creation before local-first value is clear.

## 2.4 No permission wall
Permissions are requested only in context, when their value is clear.

## 2.5 Simple Mode is strategic
Simple Mode materially reduces cognitive load without becoming a disconnected second app.

## 2.6 Urgent shortcut rule
Emergency, phrase support, saved gate/map recovery, and group safe/regroup actions remain fast to reach.

## 2.7 Umrah-first rule
Onboarding and Home defaults remain Umrah-first unless season/scope explicitly permit otherwise.

## 2.8 Ethical monetization placement
Upgrade or Support this App messaging must never dominate first-use value or interrupt ritual-critical, emergency, medical, group-recovery, or urgent map-recovery tasks.

---

# 3. Scope and boundaries

## 3.1 In scope
- startup resolution,
- first-launch detection,
- onboarding welcome,
- language/preference setup,
- Home Root behavior,
- first-use and early-use states,
- urgent shortcut cluster,
- group create/join entry points from Home and Simple Mode,
- pack-readiness summary,
- Privacy & Data entry path from Settings/More,
- Simple Mode activation, persistence, and shortcut behavior.

## 3.2 Out of scope
- deep ritual logic,
- map routing or saved-anchor storage,
- group creation/join/check-in implementation,
- subscription or entitlement truth,
- pack installation lifecycle,
- emergency-card content governance,
- phrasebook content governance,
- account deletion/export implementation.

---

# 4. Startup Resolver behavior

Startup Resolver should resolve, in order:
1. app integrity and local migrations,
2. safe deep-link/direct task intent,
3. first-launch/onboarding state,
4. Simple Mode versus standard Home,
5. non-blocking protected-state refresh where safe.

It must not wait on non-essential online calls before routing the user to a usable state.

Offline launch must still route to onboarding, Simple Home, or Home Root using local state and cached data.

---

# 5. Onboarding behavior

Default onboarding should be:
1. welcome/value screen,
2. language/preferences setup,
3. Home or Simple Home.

It may offer Simple Mode as a simple preference, but must not require account, broad permissions, or monetization before value.

---

# 6. Home Root behavior

## 6.1 Required content blocks
Home Root may include:
- ritual status/start card,
- urgent shortcut cluster,
- saved gate/recent map card,
- active group summary or create/join group entry where relevant,
- planner/reminder summary,
- pack-readiness summary,
- optional non-blocking safety banner strip,
- low-priority Settings/Tools path.

## 6.2 Priority order
1. Current ritual or start ritual.
2. Urgent shortcuts: Emergency, Phrasebook, Save My Gate/Map, I’m Safe/Group.
3. Saved gate/recent map recovery.
4. Active group summary or low-pressure create/join prompt.
5. Planner/reminder summary.
6. Pack readiness.
7. Settings/Tools.

## 6.3 First-use state
If no ritual, saved gate, group, or planner context exists, Home should emphasize:
- Start Umrah,
- emergency/phrase support,
- lightweight Save My Gate education,
- calm explanation that more context appears after use.

## 6.4 Group entry behavior
If the user has no active group, Home may show a low-priority Group prompt that routes to Group Root, where the user can choose Create Group or Join Group.
Home should not force a choice between create/join in the top priority area unless onboarding context clearly indicates a leader flow.

If an active group snapshot exists, Home may surface latest regroup context, safe-status relevance, and quick Group entry, but must not imply live tracking.

## 6.5 Stale/protected-state honesty
If group, entitlement, pack, or other remote/supportive data is stale, unavailable, or unverified, Home must reflect that honestly where it matters.

## 6.6 Approved Home visual anatomy
The supplied approved Home visual reference establishes the current standard Home anatomy without changing feature ownership:

1. profile/greeting header,
2. prayer/context hero,
3. compact quick-action row,
4. Umrah progress,
5. Saved Gate + Jama’ah Group summaries,
6. Plan & Schedule,
7. persistent bottom navigation with a centered floating action slot.

The prayer/context hero is contextual/ambient information, not a replacement for ritual recovery priority. Current ritual actions and urgent recovery must remain immediately discoverable even when the prayer hero is visually dominant.

### Prayer/context hero
The visual reference shows:
- location context,
- current prayer name,
- countdown/current time context,
- optional weather/context tile,
- compact daily prayer-time chips.

The design does not establish prayer-time calculation authority, weather provider, freshness rules, or online/offline truth. No current normative feature/API spec owns those runtime capabilities. Until approved change control establishes ownership and defines calculation/provider, timezone/location context, freshness, offline/stale behavior, privacy, analytics, and test/release evidence, Home must omit those data-driven subfields or treat them strictly as non-runtime visual reference content; implementation must not guess or synthesize values.

### Quick-action row
The visual reference demonstrates five labeled tiles: `Bacaan`, `Save Gate`, `Tata Cara`, `Emergency`, and `Lainnya`.

These are visual examples only. Final localized labels and destinations must map to canonical feature routes and terminology; agents must not create new top-level features solely to preserve screenshot text.

### Ritual progress
The visual reference demonstrates a percentage-complete summary, a compact time indicator, a progress bar, and named milestones such as Ihram, Thawaf, Sa’i, Tahallul, and completion. Ritual truth and milestone ordering remain owned by file `18`.

### Saved Gate and Jama’ah Group summaries
The visual reference demonstrates paired compact cards. Their status text must use real freshness/state truth from map/group domains and must not imply live tracking.

### Plan & Schedule
The visual reference demonstrates a date strip, vertical timeline, completed/upcoming state distinction, time range, and explicit stateful action button. Planner behavior remains owned by file `21`.

### Bottom navigation
The visual reference demonstrates Home, Ibadah, Group, and Map as visible labels plus one centered floating action slot. This does not change the canonical five-section shell in files `10` and `11`: Home, Rituals, Map, Group, and Tools. The slot must not replace or silently hide Tools, and its iconography does not define behavior. It must not become QR/scanner/camera or another new action by inference. Before it is functional, it must map to an already-approved canonical route/action and be reflected in file `11` and traceability where applicable.

---

# 7. Urgent shortcut architecture

Canonical urgent shortcuts may include:
- Phrasebook,
- Emergency,
- Save My Gate / open Map,
- I’m Safe / open Group.

Shortcut labels may adapt, for example:
- `Map` vs `My Gate`,
- `Group` vs `I’m Safe`,
- `Join Group` or `Create Group` only when context makes it clear and not crowded.

The cluster must remain small and accessible at large text.

---

# 8. Simple Mode behavior

Simple Mode is a supported operating mode of the same app.

It may change visible complexity, card density, action sizing, copy brevity, navigation emphasis, and visual treatment.

It must not change:
- core feature ownership,
- data truth,
- entitlement meaning,
- offline guarantees,
- privacy boundaries.

## 8.1 Simple Mode priority order
1. Start/Resume Ritual.
2. Save My Gate / Map.
3. I’m Safe / Group.
4. Phrasebook / Emergency.
5. More / Help / Settings.

## 8.2 Simple Home required content
Simple Home should contain:
- Start / Resume Ritual,
- Save My Gate / Map,
- I’m Safe / Group,
- Phrasebook / Emergency,
- optional one or two context cards,
- low-priority More / Settings path.

## 8.3 Simple Group shortcut behavior
If active group exists, the shortcut may emphasize `I’m Safe` or Group.
If no group exists, it routes to Group Root where Create Group and Join Group are available.
It must not imply hidden membership or live tracking.

---

# 9. Settings, More, and Privacy & Data entry

Home and Simple Mode may expose a low-priority Settings/More path.

That path must allow users to reach:
- Settings Root,
- Simple Mode toggle,
- language/preferences,
- Support this App/restore,
- Privacy & Data.

Privacy & Data itself is owned by file `24`, but Home/Simple Mode must not make it undiscoverable.

---

# 10. Pack-awareness behavior

Home may show pack-preparation or pack-readiness context when:
- it has genuine journey value,
- a pack is missing for a relevant upcoming journey,
- a verification/failure state needs user attention,
- it does not crowd out urgent tasks.

Home must not imply the app is unusable without a pack.
If a pack candidate fails verification, Home may show calm recovery status only when useful and must preserve last-known-good meaning.

---

# 11. Platform and visual adaptation

Onboarding, Home, and Simple Mode share the same product behavior and the same **Pilgrims Soft Surface** visual identity on iOS and Android.

Both Light and Dark are mandatory. System follows OS appearance.

Platform adaptation may change native navigation, sheet/modal mechanics, haptics, system chrome, transitions, or permission handoffs, but must not fork the Home/Simple Mode identity.

Simple Mode may reduce decorative depth, glow, and layered effects when that improves clarity or performance. It must preserve semantic hierarchy, touch targets, feature truth, and appearance contrast.

Home and urgent shortcuts must remain readable and discoverable in both themes. Emergency, saved-gate recovery, group recovery, and ritual-start surfaces prioritize explicit contrast over decorative depth.

# 12. Data and local preferences

Local preference authority lives in file `24`, and device-local persistence categories live in file `13`.

Representative local values:
- onboarding completion state,
- Appearance mode (`system | light | dark`),
- onboarding version seen,
- selected language/locale override,
- Simple Mode enabled state,
- support prompt dismissal state,
- selected Home presentation preferences if later approved.

Startup routing must not depend on network to read these values.

---

# 13. Screen ownership

This feature family owns or strongly depends on:
- `startup_resolver`,
- `onboarding_welcome`,
- `language_preferences_setup`,
- `home_root`,
- `simple_home`,
- `simple_ritual_shortcut`,
- `simple_map_shortcut`,
- `simple_group_shortcut`,
- `simple_emergency_shortcut`.

It routes into, but does not own:
- `group_creation_flow`,
- `join_group_flow`,
- `privacy_data_flow`,
- `pack_detail_install_flow`.

---

# 14. Analytics and evidence

Required analytics must align with file `17`, including screen events for Home/Simple Mode and relevant entry events for group, pack, settings, and privacy paths.

Release evidence must prove:
- first launch without account,
- offline startup,
- Home first-use and personalized states,
- Simple Mode persistence,
- urgent shortcut reachability,
- group no-active-group routing to create/join options,
- Privacy & Data discoverability through Settings/More,
- pack readiness/failure state does not crowd urgent tasks,
- large text and screen-reader behavior.

---

# 15. Definition of done

This feature family is ready when:
- startup routes quickly to usable state,
- onboarding is short and non-coercive,
- Home stays a recovery surface,
- urgent shortcuts remain visible,
- Simple Mode reduces cognitive load without forking logic,
- group create/join entry is available without crowding Home,
- Privacy & Data remains discoverable,
- pack readiness is useful but not dominant,
- offline/stale/protected-state behavior is honest,
- accessibility is tested.

---

# 16. AI-agent checklist

Before editing onboarding/Home/Simple Mode code, an AI agent must:
1. Read files `10`, `11`, `12`, `20`, `23`, `24`, `25`, and `31`.
2. Check `CONTRACTS/screen_feature_traceability.yaml`.
3. Confirm Home priority order.
4. Confirm Simple Mode does not fork logic.
5. Confirm group create/join and Privacy & Data routing remain discoverable.
6. Confirm urgent flows are not crowded by upsell or pack prompts.

# Guide Marketplace entry-point amendment

Hire a Guide is a Tools-owned discovery task, not an onboarding requirement or urgent recovery primitive.

## Default entry
**Tools → Hire a Guide**

## Home
Home may surface a low-priority contextual Hire a Guide entry when it is relevant to the user's pilgrimage context.

It must remain lower priority than:
1. current ritual/start or recovery,
2. Emergency/Phrase support,
3. Save My Gate/map recovery,
4. urgent Group safe/regroup actions.

Home must not become a marketplace dashboard and must not show provider advertising in ritual-critical or urgent-recovery priority areas.

## Onboarding
Do not ask new users to create an account, apply as a provider, choose a guide, or grant unrelated permissions during default onboarding.

## Simple Mode
Hire a Guide is not included in the default Simple Mode urgent shortcut set.

If a future accessibility study demonstrates a need for an entry, that requires explicit Simple Mode design/release evidence rather than silently adding density.

---

End of file.