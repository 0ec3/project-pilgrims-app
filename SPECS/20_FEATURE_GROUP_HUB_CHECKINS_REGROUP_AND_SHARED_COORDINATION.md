# 20 — FEATURE: GROUP HUB, CHECK-INS, REGROUP, AND SHARED COORDINATION

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, backend engineers, Flutter engineers, design lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for the Group feature family, including group join behavior, Group Root behavior, quick check-ins, SMS/share fallback, Supporter live board behavior, regroup pin behavior, itinerary visibility, map handoffs, offline and degraded behavior, monetization boundaries, analytics hooks, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the Group feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`, `19-FEATURE-MAPS-SAVE-MY-GATE-AND-3D-WAYFINDING.md`
- **Related files:** `21`, `23`, `24`, `25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because group coordination is one of the easiest areas for a product team or AI agent to accidentally make more invasive, more confusing, or more fragile than the product intends.

For this project, the Group feature family is especially sensitive because:
- pilgrims often separate in crowded environments and need fast recovery, not complex social features,
- the product promise is explicitly privacy-light,
- users may be tired, anxious, elderly, or low-confidence with smartphones,
- connectivity may be weak or missing exactly when regrouping matters,
- AI agents often drift toward hidden tracking, chat-style sprawl, or overbuilt live presence models,
- map coordination and group coordination overlap but must not collapse into one confusing subsystem,
- group features involve trusted authorization and must not be invented purely in client code,
- monetization boundaries can easily become unethical if basic coordination becomes paywalled.

This file prevents those failures by defining:
- what the Group feature family is responsible for,
- what users can and cannot expect,
- how joining works,
- how “I’m Safe” and check-ins work,
- how regroup pins work,
- what Live Board means and what it does not mean,
- how coordination behaves when network or realtime is unavailable,
- how map handoffs work,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
The Group feature family exists to help pilgrims:
- join a known group quickly,
- communicate simple status updates with minimal friction,
- read regroup instructions clearly,
- recover from separation using explicit shared references,
- coordinate around leader-posted anchors and itinerary information,
- continue using a meaningful coordination fallback when live connectivity is weak or absent.

## 2.2 Main user value statement
A pilgrim should be able to open the Group experience and quickly get help with one of these questions:
- How do I join my family, leader, or agency group?
- How do I tell the group I am safe?
- Where are we regrouping?
- How do I route to the regroup point?
- What is the latest trusted group status?
- What can I still do if live updates are unavailable?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- privacy-light,
- low-friction,
- trustworthy,
- text-first when necessary,
- helpful without hidden tracking,
- useful even under degraded connectivity.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- Group Root behavior,
- join-by-code behavior,
- active group summary behavior,
- quick check-in behavior,
- manual SMS/share fallback behavior,
- optional Supporter Live Board behavior,
- leader-posted regroup pin behavior,
- itinerary visibility where available,
- pack recommendation surfaces tied to group/trip context,
- map handoffs for regroup references,
- stale-state and degraded-state handling for shared coordination.

## 3.2 Out of scope
This feature family does **not** include:
- hidden continuous location tracking,
- passive background pings,
- generic chat or social feed behavior,
- rich person-to-person messaging infrastructure,
- generalized friend graph features,
- official permit or travel-document workflows,
- direct store-billing ownership,
- speculative crowd prediction features,
- mandatory realtime dependence for baseline group usefulness.

## 3.3 Boundary with file `14`
File `14` defines the canonical HTTP and realtime contract surface for groups.
This file does **not** redefine endpoint behavior or schema authority.
Instead, it defines how those contracts become user-facing feature behavior.

## 3.4 Boundary with file `13`
File `13` is the canonical source of truth for `groups`, `group_members`, `group_checkins`, `group_regroup_pins`, and `group_itineraries`.
This file may describe their feature meaning and required invariants, but it must not contradict the data model.

## 3.5 Boundary with file `19`
Maps owns route preview, route follow, and map rendering behavior.
This file only defines how regroup references and group coordination hand off into the map feature family.

## 3.6 Boundary with file `23`
Pack lifecycle and offline asset delivery are owned elsewhere.
This file only defines how group-linked pack suggestions appear and how group coordination behaves when packs are missing or installed.

## 3.7 Boundary with file `24`
Account, entitlement, and settings truth live in file `24`.
This file only defines how group behavior reacts to authentication state or entitlement state.

---

# 4. Product rules that govern this feature family

## 4.1 Coordination without surveillance rule
This feature family exists to help people stay together, not to normalize hidden tracking.
If a behavior increases surveillance posture without strong product and ethical justification, it must be rejected.

## 4.2 Free-path-first rule
Every pilgrim must be able to:
- join a group,
- read regroup instructions,
- use “I’m Safe” intent,
- fall back to user-initiated SMS/share coordination,

without requiring Supporter entitlement.

## 4.3 Realtime is enhancement, not baseline
Live Board and realtime freshness improvements may enrich the feature family, but the feature must remain useful when realtime is missing, unavailable, disabled, or unsupported.

## 4.4 Regroup is explicit, not inferred
The product should rely on explicit regroup pins, explicit check-ins, explicit text references, and explicit map launches rather than trying to infer hidden live location.

## 4.5 Group coordination must stay calm
The feature must avoid turning coordination into an alarmist or high-pressure experience. It should help users recover, not shame them.

## 4.6 Protected writes require trusted validation
Join, check-in, regroup pin creation, and protected group reads must remain server-validated. The client must not invent membership or leader permissions locally.

## 4.7 Map handoff must stay coherent
When group coordination launches into Maps, the user must land in a stable map task context and still understand that they came from Group.

## 4.8 Season-aware recommendation rule
Group-linked pack suggestions must remain season-aware and safe-by-default. When season is uncertain, recommendations must fall back to the safer Umrah-first baseline.

---

# 5. Canonical terminology for this feature family

## 5.1 Group
A user-associated coordination unit for family, travel companions, or organized parties.

## 5.2 Group leader
A privileged group role with additional coordination permissions.

## 5.3 Member
A standard group participant.

## 5.4 Check-in
A lightweight user action or system event representing a status or coordination update inside the group context.

## 5.5 “I’m Safe” intent
The user-facing quick action that expresses a safe-status update. It is an intent, not a single transport. Depending on context, it may create a server-backed group check-in, open a fallback share flow, or both.

## 5.6 Live Board
The shared coordination surface showing recent group-relevant status or activity updates.

## 5.7 Regroup pin
A leader-posted coordination anchor used to help members regroup.

## 5.8 Shared coordination
The broader feature behavior that includes join, safe-status updates, regroup references, live freshness where available, and group-visible itinerary context.

## 5.9 Freshness
How recent or trustworthy a live or shared status item is.

---

# 6. User stories

## 6.1 Join and setup
- **As a pilgrim**, I can join my group quickly using a leader-provided code.
- **As a pilgrim**, if I am not signed in yet, the app helps me complete the minimum auth state needed for trusted group actions.
- **As a pilgrim**, after joining, I can see the latest relevant regroup and trip information without needing to understand backend concepts.

## 6.2 Quick status update
- **As a pilgrim**, I can tap one clear action to communicate that I am safe.
- **As a pilgrim**, if network is weak, I can still send a user-initiated message with the key regroup text.
- **As a leader**, I can benefit from server-backed check-ins and optional live freshness without forcing members into hidden tracking.

## 6.3 Regroup and recovery
- **As a leader**, I can post a regroup reference clearly.
- **As a member**, I can read the latest regroup instruction quickly.
- **As a member**, I can launch to Maps when a map anchor exists, or copy text if map capability is limited.

## 6.4 Shared status and itinerary
- **As a Supporter or entitled user**, I can view a richer Live Board when the product policy allows.
- **As a member**, I can read leader-provided itinerary information when available.
- **As a pilgrim**, if live/shared data is stale, the app tells me honestly.

---

# 7. Free vs supporter boundaries

## 7.1 Free capability baseline
The following must remain available in the free path:
- join by code,
- Group Root access,
- read current group summary and regroup text if available,
- “I’m Safe” intent,
- user-initiated SMS/share fallback,
- map handoff into regroup detail where the reference exists,
- basic itinerary visibility if the group exposes it,
- season-aware pack suggestion visibility.

## 7.2 Supporter-linked advantages
Supporter-linked value may include:
- richer Live Board access,
- stronger realtime freshness,
- auto-download Trip Pack prompt behavior when `PACK_AUTO_DOWNLOAD` is enabled,
- other convenience surfaces explicitly approved elsewhere.

## 7.3 No paywall on baseline coordination
A user must never be blocked from joining a group or reading explicit regroup instructions because they are not a Supporter.

## 7.4 Ethical gating rule
Any lock-state messaging in Group must preserve the ethical boundary: Supporter may unlock richer coordination convenience, but not basic safety or basic regroup usefulness.

## 7.5 Never interrupt urgent coordination with upsell
Pack or Live Board upgrade prompts may appear in appropriate Group surfaces, but must not interrupt an urgent check-in or regroup flow.

---

# 8. Feature architecture overlay

## 8.1 Runtime responsibilities at the feature level
The Group feature family is responsible for coordinating:
- group-root state,
- join flow state,
- active group summary state,
- check-in intent and fallback selection,
- live board screen state,
- regroup pin detail and map-launch state,
- itinerary read surfaces,
- entitlement-aware lock or upgrade presentation,
- stale/freshness messaging,
- feature-family telemetry.

## 8.2 What this feature must not own
This feature must not directly own:
- raw auth/session truth,
- store entitlement validation,
- raw realtime provider specifics throughout UI widgets,
- map rendering or route logic,
- pack installation lifecycle,
- server authorization policy.

## 8.3 Required stable interfaces
Feature implementation should depend on stable roles such as:
- `GroupRepository`
- `GroupJoinCoordinator`
- `GroupCheckinCoordinator`
- `LiveBoardRepository`
- `RegroupPinRepository`
- `GroupItineraryRepository`
- `GroupToMapHandoffAdapter`

These are representative interface roles, not a locked naming requirement.

## 8.4 One current-group UX assumption
V1 UX should optimize around one clear current active group context presented in Group Root.
If future product direction introduces richer multi-group switching, this file and the screen/navigation contracts must be updated explicitly.

---

# 9. Canonical server-backed data responsibilities

## 9.1 Groups table meaning
The `groups` entity represents a pilgrim coordination group with a stable join code, a leader, and a season scope.

## 9.2 Membership model meaning
The `group_members` relation is the trusted source of group membership, role, and membership status.

## 9.3 Check-in model meaning
The `group_checkins` relation represents lightweight, text-based coordination events. These must never be interpreted as hidden GPS tracking.

## 9.4 Regroup pin model meaning
The `group_regroup_pins` relation represents leader-posted regroup anchors and exists separately from check-ins on purpose.

### Why this separation matters
Regroup pins are lifecycle-managed shared anchors, while check-ins are lightweight status events. Treating them as the same concept causes ambiguity in:
- analytics,
- permission rules,
- map integration,
- UI state,
- AI-agent implementation safety.

## 9.5 Itinerary model meaning
`group_itineraries` represent optional shared itinerary content that is leader-managed or service-managed and member-readable.

---

# 10. Local cache and device-local state

## 10.1 Local persistence posture
The Group feature family is not fully local-first in the same way Rituals or saved anchors are. However, it may keep local cached state for continuity and degraded usability.

## 10.2 Allowed local caches
The client may maintain local cached state such as:
- last joined group summary,
- last known membership snapshot,
- last known active regroup pins,
- last known live board snapshot or summary,
- last seen itinerary snapshot,
- dismissed pack prompt state,
- recent check-in draft text or last-used text pin,
- last successful share template.

## 10.3 Staleness requirement
Any locally cached shared state that is shown after network loss must be visually and semantically marked as stale when freshness is uncertain.

## 10.4 No misleading offline writes rule
The client must not pretend a join, protected check-in, or regroup creation succeeded if the trusted write path did not complete.

---

# 11. Join flow behavior

## 11.1 Purpose
Join Group exists to connect a user to a trusted group context quickly and safely.

## 11.2 Group creation is out of scope by default
V1 user-facing behavior should assume groups are provisioned by a leader, organizer, or another approved flow outside this feature family.
In-app group creation remains out of scope unless the API and scope files explicitly change.

## 11.3 Join code contract
The canonical join input is a **6-character uppercase alphanumeric code**.

### Validation rules
- exactly 6 characters,
- A–Z or 0–9 only,
- client-side validation should prevent obviously invalid network calls,
- server remains authoritative.

## 11.4 Auth requirement
Trusted join requires authenticated user context.
If the user is not authenticated when they enter Group Join, the flow must route through the minimum acceptable account/auth gate before calling the protected endpoint.

## 11.5 Join request rule
Join must use the canonical join endpoint and an `Idempotency-Key`.
Repeated join attempts with the same intent should not create inconsistent membership state.

## 11.6 Join success behavior
On success, the user must land in a coherent Group Root context showing:
- group name,
- membership status,
- role,
- latest regroup summary if available,
- optional itinerary summary,
- optional season-aware suggested packs.

## 11.7 Join failure behavior
Friendly, user-readable failures must exist for:
- bad format,
- no matching code,
- unauthorized / expired auth,
- already joined or conflict semantics,
- rate limiting,
- network failure.

## 11.8 Join-copy rule
User-facing copy should say **“6-character code”** rather than imply a numeric-only code.

---

# 12. Group Root behavior

## 12.1 Purpose
Group Root is the main coordination hub for current group status, fast check-in, regroup visibility, and related group actions.

## 12.2 Required content blocks
Group Root must include, where relevant:
- group name and current role summary,
- fast “I’m Safe” action,
- latest regroup pin or regroup summary card,
- recent coordination freshness summary,
- itinerary summary or shortcut if available,
- optional live board entry or teaser when entitlement permits,
- optional season-aware suggested pack card.

## 12.3 Required states
Group Root must support:
- not joined yet,
- joined with current content,
- joined with stale cached state,
- loading / refreshing,
- offline degraded state,
- entitlement-limited live features,
- group unavailable / removed / no longer active,
- auth required state if protected data cannot be refreshed.

## 12.4 Primary actions
- Join Group
- I’m Safe
- Open Regroup Detail
- Open Map Route to Regroup when available
- Open Live Board if available
- Open Group Itinerary if available

## 12.5 Group Root rule
The user should not need to understand realtime, channels, or backend state in order to use the Group section.

---

# 13. “I’m Safe” and check-in behavior

## 13.1 Purpose
“I’m Safe” is the canonical quick coordination action for telling the group that the user is okay and giving a simple location or regroup reference context.

## 13.2 Intent over transport rule
“I’m Safe” is a user-facing intent, not a single hardcoded transport.
The feature may use:
- server-backed group check-in,
- user-initiated share sheet fallback,
- or a sensible combination,

depending on availability and context.

## 13.3 Preferred behavior in online trusted conditions
When the user is an active member and the trusted write path is available:
- create a group check-in through the canonical protected endpoint,
- use text-based pin content as the primary payload,
- optionally offer immediate follow-up share action if useful,
- update Group Root and Live Board freshness accordingly.

## 13.4 Fallback behavior in degraded conditions
If network is unavailable, group membership cannot be refreshed, or the protected check-in write fails:
- the app must not fake server success,
- it should offer the user-initiated share sheet fallback immediately,
- the fallback message should include the best available regroup or location text,
- the UI should communicate that this was a messaging fallback rather than a trusted server-backed update.

## 13.5 Primary input rule
The primary check-in input is **text-based pin content**, not precise GPS coordinates.

## 13.6 Check-in kinds
The server-backed check-in model may support lightweight kinds such as:
- `SAFE`
- `CHECKIN`
- `STATUS`

V1 UI should keep the user-facing quick action simple rather than expose too many status types.

## 13.7 Duplicate protection rule
The client should send `client_event_id` where supported and tolerate idempotent or coalesced server handling of rapid duplicate safe-intent submissions.

## 13.8 User privacy rule
The feature must never imply that the app is automatically tracking the user’s position when the user taps “I’m Safe.”

---

# 14. Share-sheet fallback behavior

## 14.1 Purpose
Manual messaging fallback exists because group coordination must still work when network or realtime is weak.

## 14.2 Canonical fallback posture
The app should rely on the platform share sheet or message-compose surface and let the user decide whether to send via SMS, WhatsApp, Messages, or another supported app.

## 14.3 User confirmation rule
The app must not silently send messages on the user’s behalf.
User initiation and confirmation remain required.

## 14.4 Required fallback message ingredients
A fallback message should include, where available:
- safe-status statement,
- latest regroup text if relevant,
- user-readable location text if user intentionally provided it,
- calm product signature only if approved copy still wants it.

## 14.5 Copy quality rule
Fallback text must be short, readable, and useful without requiring the recipient to open the app.

## 14.6 Channel-agnostic rule
The shared text should remain useful whether the user picks SMS, WhatsApp, or another supported share destination.

---

# 15. Live Board behavior

## 15.1 Purpose
Live Board exists to provide richer shared coordination freshness, not to turn the app into a surveillance dashboard.

## 15.2 Product meaning
Live Board is the shared coordination surface showing recent group-relevant status or activity updates such as check-ins and regroup pin freshness.

## 15.3 Supporter-linked behavior
Live Board may be hidden, reduced, or locked according to product entitlement policy.
Entitlement gating is layered on top of authorization, not a substitute for authorization.

## 15.4 Required content blocks
Live Board must include, where relevant:
- recent check-in activity,
- relative freshness or timestamp,
- leader or member identity in privacy-safe form,
- latest regroup pin summary,
- stale or reconnecting indicators when realtime is absent,
- optional leader emphasis for who has not checked in recently if the product explicitly supports it.

## 15.5 Privacy-light display rule
Live Board should display minimal user representation such as display alias or masked phone rather than broad personal data.

## 15.6 Not a hidden tracking board
Live Board must not imply precise current location or passive continuous presence.

## 15.7 Realtime optionality rule
If realtime is unavailable, Live Board should degrade to:
- HTTP snapshot when available,
- stale cached summary when safe,
- or a clear unavailable state,

without making the whole Group feature feel broken.

## 15.8 Presence-event caution
Optional presence events may exist, but they must remain privacy-light and must not imply hidden location tracking.
Presence semantics are not required for baseline V1 usefulness.

---

# 16. Regroup pin behavior

## 16.1 Purpose
Regroup Pin exists to give the leader an explicit coordination anchor that members can read, copy, and route to.

## 16.2 Creation permissions
Only an active leader may create or update active regroup pins for the group.

## 16.3 Required regroup fields at the feature level
A regroup pin should expose at least:
- `label`
- `text_pin`
- optional `map_anchor_ref`
- optional `expires_at`
- freshness metadata
- active/inactive state

## 16.4 Text-first rule
`text_pin` is mandatory because regroup must remain useful even when map anchoring is unavailable.

## 16.5 Map-anchor optionality rule
`map_anchor_ref` is optional and exists only to improve map launch and route behavior when supported.
It must never become required for a valid regroup pin.

## 16.6 Expiration rule
If `expires_at` passes or the leader deactivates the pin:
- the UI must stop implying it is current,
- Maps must not over-highlight it as the active regroup target,
- older pins may still remain visible in controlled historical contexts only if that behavior is explicitly approved later.

## 16.7 Multiple pins rule
The product may keep more than one regroup pin historically, but the Group Root and map-integrated surfaces should emphasize the latest active relevant one and avoid clutter.

## 16.8 Regroup pin detail requirements
Regroup Pin Detail / Route Launch must show:
- label,
- text_pin,
- freshness state,
- expiry or inactive state if relevant,
- copy action,
- route/open in map action when available,
- fallback instructions when route launch is unavailable.

---

# 17. Group itinerary behavior

## 17.1 Purpose
Group Itinerary exists to provide shared, leader-managed planning context without turning the app into a full collaborative calendar.

## 17.2 Product scope
In V1, itinerary is optional, read-focused, and leader-managed or service-managed.
Regular members read it; they do not edit it.

## 17.3 Required content blocks
Where itinerary exists, the feature should expose:
- next itinerary item summary in Group Root,
- full itinerary screen if relevant,
- clear day/date grouping,
- local freshness indicator if data is cached or stale.

## 17.4 No cloud-planner scope creep
Do not let itinerary behavior drift into generalized calendar sync, personal planning sync, or collaborative editing without an approved change.

---

# 18. Shared coordination state model

## 18.1 Conceptual feature states
At the feature-family level, the Group feature family should handle these broad states:
- not joined,
- joined and current,
- joined but stale,
- joined with live enhancement active,
- joined but live enhancement unavailable,
- auth required,
- group inaccessible or removed.

## 18.2 Freshness communication
Freshness should be visible where it materially affects user trust, especially for:
- Live Board,
- regroup pins,
- itinerary summaries,
- last seen shared coordination state.

## 18.3 No fake live-state rule
When the app is showing stale last-known data, the UI must not style it as if it were unquestionably current.

---

# 19. Map handoff behavior

## 19.1 Purpose
Group-to-map handoff exists to turn a regroup reference into a practical recovery action.

## 19.2 Launch conditions
When a regroup pin exposes sufficient map anchor or routeable context, the feature should allow:
- open regroup detail,
- route preview launch,
- route follow start when supported by Maps.

## 19.3 Stable context rule
When launched from Group, the user must land in a stable map task context such as Route Preview or Map Root rather than a provider-internal or ambiguous screen.

## 19.4 Text fallback rule
If map routing, pack availability, or location confidence is insufficient, the Group feature must still preserve text-based regroup usefulness through copy/share and readable instructions.

## 19.5 Cross-feature consistency rule
The Group feature must treat regroup pins as distinct from saved anchors while allowing map-side rendering and route launch behavior to remain coherent.

---

# 20. Packs and season-aware recommendation behavior

## 20.1 Why Group surfaces may suggest packs
After a successful join, the app may infer that certain offline assets would improve group coordination or regroup usefulness.

## 20.2 Recommendation inputs
Pack suggestions may consider:
- current season flag,
- group `season_scope`,
- device locale/language,
- currently installed packs,
- entitlement state.

## 20.3 Safe season-default rule
When season or scope information is unclear, Group-linked suggestions must default to the safer Umrah-first recommendation posture.

## 20.4 Umrah recommendation posture
During Umrah-first behavior, Group-linked suggestions should prioritize:
- Haram high-resolution map pack,
- relevant device-language audio/voice pack where appropriate.

## 20.5 Hajj-capable recommendation posture
If season and scope explicitly allow Hajj-oriented suggestions, the feature may prioritize Holy Sites packs before Haram high-resolution follow-up suggestions.

## 20.6 Recommendation presentation rule
Pack suggestions should feel like optional helpful follow-up, not a blocker to basic coordination.

## 20.7 Auto-download rule
Auto-download prompts or toggles are only relevant when entitlement and pack policy allow them.

---

# 21. Offline behavior and degraded states

## 21.1 Offline tier
The Group feature family is mixed-tier:
- join and protected write coordination are online-required trusted operations,
- last-known shared state may be shown as stale cached state where safe,
- manual SMS/share fallback remains a critical degraded path.

## 21.2 Online-required operations
The following require trusted online interaction:
- group join,
- protected server-backed check-ins,
- live board refresh,
- leader regroup pin create/update,
- authoritative itinerary refresh.

## 21.3 Degraded but still useful operations
The following may still be meaningfully available offline or in degraded conditions:
- read cached group summary if previously fetched,
- read last-known regroup text if available,
- open previously cached itinerary summary marked stale,
- copy and share fallback message,
- launch to Maps if previously cached regroup/map reference is still usable locally.

## 21.4 Stale snapshot rule
A cached group snapshot may be shown only if it is clearly labeled stale and cannot dangerously mislead the user.

## 21.5 No-network check-in rule
If a server-backed check-in cannot be sent due to no network, the feature should offer fallback messaging rather than pretending the group received an update.

## 21.6 No-realtime rule
If realtime is unavailable but HTTP still works, the feature should fall back to snapshot refresh.
If both are unavailable, the feature should preserve manual coordination paths.

## 21.7 Removed or inactive group handling
If the server indicates the user is no longer an active member or the group is not available:
- Group Root must explain that state clearly,
- stale cached content must not be presented as active shared truth,
- user should still be able to copy their last local fallback text if that helps practical recovery.

---

# 22. Screen and UX contract for this feature family

## 22.1 Canonical screens
This feature family owns or strongly depends on the following canonical screens:
- `group_root`
- `join_group_flow`
- `group_live_board`
- `checkin_quick_flow`
- `regroup_pin_detail_route_launch`
- `group_itinerary`

## 22.2 Group Root UX contract
### Required content blocks
- group summary,
- I’m Safe CTA,
- regroup summary card,
- optional itinerary summary,
- optional live-board entry,
- optional pack suggestion card.

### Required states
- not joined,
- joined/current,
- joined/stale,
- offline degraded,
- locked live enhancement,
- group unavailable.

### Primary actions
- Join Group
- I’m Safe
- Open Regroup Detail
- Open Live Board
- Open Itinerary

### Rule
The root must prioritize immediate coordination value over broad feature browsing.

## 22.3 Join Group Flow UX contract
### Required content blocks
- join code entry,
- help text,
- continue action,
- auth handoff messaging if needed.

### Required states
- empty entry,
- locally invalid format,
- submitting,
- success,
- not found,
- conflict or already joined,
- rate-limited,
- network failure,
- auth required.

### Rule
This flow must be short and error-tolerant.

## 22.4 Check-In Quick Flow UX contract
### Required content blocks
- simple confirmation or text entry surface,
- current regroup summary if available,
- primary update action,
- fallback share action when relevant,
- success or failure confirmation.

### Required states
- ready,
- sending,
- sent,
- failed with retry,
- offline fallback,
- not an active member.

### Rule
The user should be able to complete a coordination update in seconds.

## 22.5 Group Live Board UX contract
### Required content blocks
- recent activity list or strip,
- freshness indicator,
- regroup pin summary,
- stale or reconnecting indicator when needed.

### Required states
- live/current,
- snapshot only,
- stale cached,
- unavailable/locked,
- empty/no recent activity.

### Rule
This screen must remain easy to scan. It must not become a noisy admin console.

## 22.6 Regroup Pin Detail / Route Launch UX contract
### Required content blocks
- pin label,
- text pin,
- freshness/expiry state,
- copy action,
- map route/open action if supported.

### Required states
- active/current,
- stale/aged,
- expired/inactive,
- map launch unavailable,
- offline text-only use.

### Rule
Text usefulness must remain strong even when map behavior degrades.

## 22.7 Group Itinerary UX contract
### Required content blocks
- grouped itinerary items,
- next item emphasis,
- freshness/stale state,
- simple empty state if no itinerary exists.

### Required states
- current content,
- no itinerary,
- stale cached,
- unavailable.

### Rule
Itinerary must feel like supporting context, not a dense scheduling product.

---

# 23. Copy, localization, RTL, and accessibility rules for group coordination

## 23.1 Copy tone
Group copy must be:
- direct,
- calm,
- practical,
- socially neutral,
- not blaming,
- not creepy.

## 23.2 User-facing copy examples
Preferred patterns include:
- “Join your group”
- “Enter the 6-character code from your leader.”
- “I’m Safe”
- “Recent check-ins. No background tracking.”
- “Regroup at Gate 79, Level 2.”
- “Live updates unavailable. You can still copy the regroup point.”

## 23.3 Bidi and mixed-content rule
Join codes, gate codes, level labels, short references, and mixed-language status strings must remain bidi-safe and readable in RTL interfaces.

## 23.4 Accessibility requirements
Group flows must support:
- large enough entry targets for code input,
- screen-reader labels for quick actions,
- clear semantic labeling for stale vs current shared state,
- no color-only meaning for safe/fresh/stale status,
- readable relative-time or timestamp presentation,
- large text without breaking join, regroup, and live board layouts.

## 23.5 Privacy wording rule
Copy must never imply hidden location monitoring.
If live freshness exists, it should be described as recent activity or check-ins, not automatic tracking.

---

# 24. Security and privacy rules for this feature family

## 24.1 No hidden tracking
The Group feature family must not request, require, or imply continuous background location tracking for baseline coordination.

## 24.2 Minimal data display
Group UI should minimize unnecessary exposure of personal data.
Display alias or masked identifiers are preferred over broad personal profile data.

## 24.3 Authorization rule
Authentication alone is not sufficient. Membership and role checks must still gate group read/write behavior.

## 24.4 Protected realtime rule
Protected group data must never rely on public channels.
Private authorized channels are the canonical realtime surface.

## 24.5 User-initiated sharing rule
Any message or cross-app sharing behavior must remain explicitly user-initiated.

## 24.6 Logging and analytics redaction rule
Do not log full phone numbers, raw message recipients, or hidden personal identifiers in analytics or diagnostic logs.

---

# 25. Realtime behavior and delivery semantics

## 25.1 Realtime design goal
Realtime exists only where it meaningfully improves group coordination without becoming mandatory for baseline usefulness.

## 25.2 Allowed realtime use cases
Allowed group-family realtime uses include:
- live board freshness updates,
- regroup pin broadcast/update events,
- optional privacy-light presence events if explicitly enabled later.

## 25.3 Channel posture
Private authorized group channels are the canonical transport posture for protected group live coordination.

## 25.4 Realtime event families
The feature family should be compatible with canonical events such as:
- `group.live_board.snapshot`
- `group.checkin.created`
- `group.regroup_pin.created`
- `group.regroup_pin.updated`
- optional `group.presence.changed`

## 25.5 Ordering and truth rule
Realtime is best-effort near-real-time and must not become the sole source of critical business truth.
Protected writes and recoverable snapshots remain grounded in canonical server data.

---

# 26. Performance and operational rules for this feature family

## 26.1 Performance authority
Performance budgets are defined normatively in file `17`.
This feature family must obey them.

## 26.2 Critical budget posture
At minimum, this feature must respect:
- group root open with cached state p95 ≤ **900 ms**,
- check-in button feedback ≤ **150 ms** locally,
- fallback SMS/action sheet presentation p95 ≤ **300 ms**,
- group join endpoint p95 ≤ **800 ms** with fail threshold above that governed by file `17`,
- check-in endpoint p95 ≤ **600 ms** with fail threshold governed by file `17`.

## 26.3 Reliability priorities
This feature family must optimize for:
- fast join resolution,
- near-instant check-in acknowledgement at the UI layer,
- stable fallback messaging,
- honest stale/live indication,
- graceful degradation before coordination feels broken.

---

# 27. Analytics and observability requirements

## 27.1 Required analytics events
This feature family must emit the canonical group events defined in file `17`, including at minimum:
- `group_join_start`
- `group_join_complete`
- `group_join_fail`
- `group_live_board_view`
- `group_checkin_start`
- `group_checkin_complete`
- `group_checkin_fail`
- `group_checkin_fallback_sms`
- `group_regroup_pin_view`
- `group_regroup_pin_create`
- `group_regroup_pin_route_launch`

## 27.2 Required parameters where relevant
- `role`
- `checkin_method`
- `live_board_enabled`
- `regroup_pin_state`
- `network_state`
- `season`

## 27.3 Privacy-light analytics rule
Do not capture hidden continuous path traces, raw phone numbers, or raw message-recipient data. Measurement should focus on success, failure, fallback, freshness, and degradation.

## 27.4 Tracing requirements
Tracing or equivalent correlation should exist for:
- group join request,
- group check-in request,
- live board snapshot fetch where relevant,
- regroup pin create/update requests.

## 27.5 Operational alerting relevance
Group join failure spikes, protected check-in failure spikes, and regroup creation failures are high-signal issues and must surface meaningfully in observability tooling.

---

# 28. Testing and validation requirements

## 28.1 Required automated coverage
Automated tests must cover at minimum:
- join-code validation,
- idempotent join behavior,
- auth-gated join routing,
- member vs non-member check-in behavior,
- client_event_id duplicate tolerance,
- fallback share message composition,
- regroup pin create/update permission boundaries,
- stale-state rendering,
- live board entitlement gating,
- private-channel membership rules at integration level,
- map handoff from regroup detail,
- season-aware pack recommendation behavior.

## 28.2 Required manual/device validation
Manual or device validation must cover at minimum:
- join flow from signed-out and signed-in states,
- one-tap or near-one-tap safe update behavior,
- offline/no-network fallback to share sheet,
- leader regroup pin posting and member visibility,
- live board snapshot and realtime freshness when entitled,
- stale cached group state communication,
- route launch from regroup pin into Maps,
- large text and RTL usability for join/group/regroup surfaces,
- screen-reader labeling of I’m Safe, Join, Live Board, and Copy/Route actions.

## 28.3 Real-world validation requirement
Before release, representative field testing should validate:
- group join speed and comprehension,
- safe-update completion under stress,
- message fallback usefulness,
- regroup clarity after separation,
- stale vs live-state honesty,
- leader/member mental model clarity.

## 28.4 Fake-success warning
A happy-path demo with strong connectivity is not enough evidence that group coordination is release-ready.
Degraded network and fallback messaging behavior are part of the required proof.

---

# 29. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- join by 6-character code works through the trusted online path,
- the feature never implies hidden tracking,
- “I’m Safe” is fast, understandable, and can degrade to user-initiated share fallback,
- regroup pins are distinct from ordinary check-ins at the data and feature level,
- Supporter Live Board is enhancement-only and degrades safely,
- map handoff from regroup references remains coherent,
- season-aware pack suggestions remain safe and non-intrusive,
- analytics hooks are wired according to file `17`,
- offline and stale-state behavior is honest,
- real-world validation confirms the feature helps groups recover rather than confusing them.

---

# 30. Cross-file dependency rules

## 30.1 If group or regroup schema changes
Update:
- this file,
- file `13`,
- file `14`,
- tests/fixtures and release evidence requirements.

## 30.2 If Group screen behavior changes
Update:
- this file,
- file `11`,
- file `10` if journey expectations change,
- file `12` if copy or accessibility expectations materially change.

## 30.3 If map handoff behavior changes
Update:
- this file,
- file `19`,
- file `16` if deeper map-system truth changes,
- file `14` if payload or endpoint semantics change.

## 30.4 If realtime policy changes
Update:
- this file,
- file `14`,
- file `17`,
- file `29` if privacy/security posture is materially affected.

## 30.5 If free/supporter boundary changes
Update:
- this file,
- file `24` or monetization authority file,
- file `17` if event semantics or dashboards change,
- paywall and copy rules where relevant.

---

# 31. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 31.1 Treating group coordination as live tracking by default
Forbidden.

## 31.2 Requiring realtime for baseline usefulness
Forbidden.

## 31.3 Auto-sending SMS or messages without user confirmation
Forbidden.

## 31.4 Encoding regroup pins as generic check-ins in new implementation work
Forbidden.

## 31.5 Exposing protected group data through public channels
Forbidden.

## 31.6 Blocking basic regroup usefulness behind Supporter entitlement
Forbidden.

## 31.7 Making users understand channels, subscriptions, or backend jargon to coordinate
Forbidden.

## 31.8 Showing stale group state as if it were unquestionably current
Forbidden.

## 31.9 Displaying unnecessary personal data in live/group surfaces
Forbidden.

## 31.10 Turning itinerary into an uncontrolled collaborative scheduling product
Forbidden.

---

# 32. Implementation priorities

## 32.1 Phase 1 priorities
Implement first:
- Join Group flow,
- Group Root baseline,
- I’m Safe intent with trusted check-in and fallback share path,
- regroup pin visibility and copy behavior,
- basic map handoff into regroup route launch,
- stale cached group summary behavior.

## 32.2 Phase 2 priorities
Then add:
- Supporter Live Board,
- leader regroup creation/update polish,
- itinerary read surfaces,
- stronger season-aware group pack suggestions,
- better stale/live freshness messaging.

## 32.3 Phase 3 priorities
Then refine:
- richer private-channel realtime polish,
- optional presence semantics only if still privacy-light,
- stronger leader operational summaries,
- deeper real-world tuning based on field evidence.

---

# 33. When this file must be updated

This file must be updated whenever any of the following changes:
- join flow behavior,
- join code semantics,
- I’m Safe/check-in behavior,
- fallback messaging posture,
- Live Board meaning or entitlement policy,
- regroup pin lifecycle or map handoff behavior,
- itinerary visibility rules,
- stale/shared-state behavior,
- group analytics hooks,
- release-evidence expectations tied to group coordination.

If these truths change but this file is not updated, implementation and QA will drift quickly.

---

# 34. Summary

This file defines the canonical feature-facing contract for Group Hub, check-ins, regroup, and shared coordination in Pilgrims Mobile App.

It establishes:
- the purpose and limits of group coordination,
- the free/supporter and privacy boundaries,
- join-by-code behavior,
- the meaning of “I’m Safe” and fallback sharing,
- the role of Live Board,
- the lifecycle and meaning of regroup pins,
- itinerary visibility rules,
- map handoff behavior,
- offline and stale-state expectations,
- required analytics, testing, and release-readiness requirements.

Its purpose is to ensure the Group feature family becomes:
- useful,
- calm,
- privacy-light,
- resilient under weak connectivity,
- and safe for long-term AI-assisted implementation without drifting into surveillance or coordination chaos.

