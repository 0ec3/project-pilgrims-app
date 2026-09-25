# 20 — FEATURE: GROUP HUB, CHECK-INS, REGROUP, AND SHARED COORDINATION

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, backend engineers, Flutter engineers, design lead, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for Group creation, group join behavior, Group Root behavior, quick check-ins, SMS/share fallback, Supporter Live Board behavior, regroup pin behavior, itinerary visibility, map handoffs, offline and degraded behavior, monetization boundaries, analytics hooks, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the Group feature family. File `31` supersedes earlier out-of-scope assumptions for group creation. File `14` owns HTTP/realtime contracts. File `13` owns schema/RLS truth. File `29` owns privacy/security boundaries.
- **Last-updated-by:** AI-assisted quality-first hardening pass (validated 2026-06-11)
- **Primary dependencies:** `01`, `03`, `04`, `07`, `08`, `09`, `10`, `11`, `12`, `13`, `14`, `15`, `17`, `19`, `24`, `29`, `31`, `CONTRACTS/group_presence_privacy_contract.yaml`, `CONTRACTS/entitlement_capability_policy.yaml`, `CONTRACTS/screen_feature_traceability.yaml`
- **Related files:** `21`, `22`, `23`, `25`, `27`, `28`, `30`

---

# 1. Purpose of this file

This file exists because group coordination is one of the easiest areas for a product team or AI agent to accidentally make more invasive, confusing, or fragile than the product intends.

For this project, the Group feature family is sensitive because:
- pilgrims often separate in crowded environments and need fast recovery, not complex social features,
- the product promise is explicitly privacy-light,
- users may be tired, anxious, elderly, or low-confidence with smartphones,
- connectivity may be weak or missing exactly when regrouping matters,
- AI agents often drift toward hidden tracking, chat-style sprawl, or overbuilt live presence models,
- map coordination and group coordination overlap but must not collapse into one confusing subsystem,
- group features involve trusted authorization and must not be invented purely in client code,
- monetization boundaries can easily become unethical if basic coordination becomes paywalled.

This file defines:
- governed group creation,
- join-by-code behavior,
- Group Root behavior,
- “I’m Safe” and check-ins,
- regroup pins,
- Live Board meaning and limits,
- itinerary visibility,
- stale/offline behavior,
- map handoff behavior,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
The Group feature family exists to help pilgrims:
- create a trusted coordination group when they are a leader,
- join a known group quickly,
- communicate simple status updates with minimal friction,
- read regroup instructions clearly,
- recover from separation using explicit shared references,
- coordinate around leader-posted anchors and itinerary information,
- continue using a meaningful coordination fallback when live connectivity is weak or absent.

## 2.2 Main user value statement
A pilgrim should be able to open Group and quickly answer:
- How do I create a group for my family or party?
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
- governed in-app group creation,
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
- contact import or automatic member discovery,
- official permit or travel-document workflows,
- direct store-billing ownership,
- speculative crowd prediction features,
- mandatory realtime dependence for baseline group usefulness.

## 3.3 Boundary with file `14`
File `14` defines the canonical HTTP and realtime contract surface for groups.
This file defines how those contracts become user-facing behavior.

## 3.4 Boundary with file `13`
File `13` is the canonical source of truth for `groups`, `group_members`, `group_checkins`, `group_regroup_pins`, `group_itineraries`, and any normalized group presence/event model.
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

## 3.8 Boundary with machine-readable contracts
Implementation must validate Group behavior against:
- `CONTRACTS/group_presence_privacy_contract.yaml`,
- `CONTRACTS/entitlement_capability_policy.yaml`,
- `CONTRACTS/screen_feature_traceability.yaml`.

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

## 4.3 Governed creation rule
Group creation is in quality-first scope as a governed authenticated leader flow.
It is not a generic social-group feature.
It exists to let a family leader, trip leader, or organizer create a simple coordination context safely.

## 4.4 Realtime is enhancement, not baseline
Live Board and realtime freshness improvements may enrich the feature family, but the feature must remain useful when realtime is missing, unavailable, disabled, unsupported, or not entitled.

## 4.5 Regroup is explicit, not inferred
The product should rely on explicit regroup pins, explicit check-ins, explicit text references, and explicit map launches rather than trying to infer hidden live location.

## 4.6 Group coordination must stay calm
The feature must avoid turning coordination into an alarmist or high-pressure experience. It should help users recover, not shame them.

## 4.7 Protected writes require trusted validation
Create, join, check-in, regroup pin creation, and protected group reads must remain server-validated. The client must not invent membership, leader permissions, group codes, or entitlement truth locally.

## 4.8 Map handoff must stay coherent
When group coordination launches into Maps, the user must land in a stable map task context and still understand that they came from Group.

## 4.9 Season-aware recommendation rule
Group-linked pack suggestions must remain season-aware and safe-by-default. When season is uncertain, recommendations must fall back to the safer Umrah-first baseline.

## 4.10 No contact graph rule
The feature must not import contacts, infer social relationships, auto-add people, or create a hidden social graph.
Invitations are explicit share-code or SMS/share handoffs initiated by the user.

---

# 5. Canonical terminology

## 5.1 Group
A user-associated coordination unit for family, travel companions, or organized parties.

## 5.2 Group leader
A privileged group role with additional coordination permissions.

## 5.3 Member
A standard group participant.

## 5.4 Group creation
The authenticated leader flow that creates a server-backed group, assigns the requester as initial leader, and returns a server-generated join code.

## 5.5 Join code
A 6-character uppercase alphanumeric code generated by the server and used by members to join a group.

## 5.6 Check-in
A lightweight user action representing a status or coordination update inside the group context.

## 5.7 “I’m Safe” intent
The user-facing quick action that expresses a safe-status update. It is an intent, not a single transport. Depending on context, it may create a server-backed group check-in, open a fallback share flow, or both.

## 5.8 Live Board
The shared coordination surface showing recent group-relevant status or activity updates.
Live Board must not imply continuous location tracking.

## 5.9 Regroup pin
A leader-posted coordination anchor used to help members regroup.

## 5.10 Shared coordination
The broader feature behavior that includes create, join, safe-status updates, regroup references, live freshness where available, and group-visible itinerary context.

## 5.11 Freshness
How recent or trustworthy a live or shared status item is.

---

# 6. User stories

## 6.1 Group creation and setup
- **As a leader**, I can create a group with a clear name and receive a shareable join code.
- **As a leader**, I can share the code through a user-initiated system share/SMS flow without the app auto-sending messages.
- **As a leader**, I understand when group creation cannot happen because I am offline, unauthenticated, rate-limited, or blocked by a trusted validation failure.

## 6.2 Join and setup
- **As a pilgrim**, I can join my group quickly using a leader-provided code.
- **As a pilgrim**, if I am not signed in yet, the app helps me complete the minimum auth state needed for trusted group actions.
- **As a pilgrim**, after joining, I can see the latest relevant regroup and trip information without needing to understand backend concepts.

## 6.3 Quick status update
- **As a pilgrim**, I can tap one clear action to communicate that I am safe.
- **As a pilgrim**, if network is weak, I can still send a user-initiated message with the key regroup text.
- **As a leader**, I can benefit from server-backed check-ins and optional live freshness without forcing members into hidden tracking.

## 6.4 Regroup and recovery
- **As a leader**, I can post a regroup reference clearly.
- **As a member**, I can read the latest regroup instruction quickly.
- **As a member**, I can launch to Maps when a map anchor exists, or copy text if map capability is limited.

## 6.5 Shared status and itinerary
- **As a Supporter or entitled user**, I can view a richer Live Board when product policy allows.
- **As a member**, I can read leader-provided itinerary information when available.
- **As a pilgrim**, if live/shared data is stale, the app tells me honestly.

---

# 7. Free vs Supporter boundaries

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

## 7.2 Group creation entitlement rule
Group creation requires authentication and trusted server validation, but is not a Supporter-only upsell by default.
Any future quota or organizer-tier policy requires file `03`, file `14`, file `20`, file `24`, file `29`, and the entitlement contract to be updated together.

## 7.3 Supporter-linked advantages
Supporter-linked value may include:
- richer Live Board access,
- stronger realtime freshness,
- auto-download Trip Pack prompt behavior when `PACK_AUTO_DOWNLOAD` is enabled,
- other convenience surfaces explicitly approved elsewhere.

## 7.4 No paywall on baseline coordination
A user must never be blocked from joining a group or reading explicit regroup instructions because they are not a Supporter.

## 7.5 Ethical gating rule
Any lock-state messaging in Group must preserve the ethical boundary: Supporter may unlock richer coordination convenience, but not basic safety or basic regroup usefulness.

## 7.6 Never interrupt urgent coordination with upsell
Pack or Live Board upgrade prompts may appear in appropriate Group surfaces, but must not interrupt urgent check-in or regroup flows.

---

# 8. Feature architecture overlay

## 8.1 Runtime responsibilities at the feature level
The Group feature family is responsible for coordinating:
- group creation flow state,
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
- `GroupRepository`,
- `GroupCreationCoordinator`,
- `GroupJoinCoordinator`,
- `GroupCheckinCoordinator`,
- `LiveBoardRepository`,
- `RegroupPinRepository`,
- `GroupItineraryRepository`,
- `GroupToMapHandoffAdapter`.

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

## 9.3 Group creation model meaning
Group creation must create the `groups` row and the initial `group_members` leader row transactionally.
The generated code belongs to the server, not the client.

## 9.4 Check-in model meaning
The `group_checkins` relation represents lightweight, text-based coordination events. These must never be interpreted as hidden GPS tracking.

## 9.5 Regroup pin model meaning
The `group_regroup_pins` relation represents leader-posted regroup anchors and exists separately from check-ins on purpose.

## 9.6 Why regroup/check-in separation matters
Regroup pins are lifecycle-managed shared anchors, while check-ins are lightweight status events. Treating them as the same concept causes ambiguity in:
- analytics,
- permission rules,
- map integration,
- UI state,
- AI-agent implementation safety.

## 9.7 Itinerary model meaning
`group_itineraries` represent optional shared itinerary content that is leader-managed or service-managed and member-readable.

## 9.8 Presence/freshness model meaning
If normalized presence or freshness state is added beyond check-ins/regroup pins, it must follow `CONTRACTS/group_presence_privacy_contract.yaml` and file `13`.

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
The client must not pretend group creation, join, protected check-in, or regroup creation succeeded if the trusted write path did not complete.

## 10.5 No hidden offline queue rule
Group creation, join, check-in, and regroup writes must not be silently queued in a way that later surprises the user. If a retry/pending pattern is ever approved, the UI must clearly say what is pending and what has not happened.

---

# 11. Group creation flow behavior

## 11.1 Purpose
Group Creation exists to let a leader create a trusted coordination context quickly and safely.

## 11.2 Entry points
Approved entry points:
- Group Root when the user has no active group,
- setup prompt after onboarding if explicitly selected by a leader-type user,
- deep link or organizer handoff only if file `14` and security review approve the flow.

## 11.3 Auth requirement
Trusted group creation requires authenticated user context.
If the user is not authenticated, the flow must route through the minimum acceptable account/auth gate before calling `POST /v1/groups`.

## 11.4 Required inputs
Minimum user-facing inputs:
- group name,
- optional season scope if approved by scope rules,
- optional display alias if needed.

The client must not let the user manually choose the canonical join code unless file `14` and abuse review explicitly approve that change.

## 11.5 Server creation rule
Creation must use `POST /v1/groups` and an `Idempotency-Key`.
The server must:
- generate the join code,
- create the group,
- assign the requester as active leader,
- enforce rate limits and abuse controls,
- return a safe share-code payload.

## 11.6 Success behavior
On success, the leader lands in Group Root showing:
- group name,
- leader role,
- join code/share code card,
- clear copy for inviting members,
- “I’m Safe” and regroup actions where applicable,
- optional itinerary and pack suggestion surfaces.

## 11.7 Failure behavior
Friendly failures must exist for:
- unauthenticated,
- offline / network unavailable,
- rate limited,
- validation failure,
- duplicate idempotent result,
- server unavailable,
- authorization or account state invalid.

## 11.8 Share-code rule
The app may prefill a system share/SMS body, but must never auto-send, auto-invite contacts, or scrape the address book.

---

# 12. Join flow behavior

## 12.1 Purpose
Join Group exists to connect a user to a trusted group context quickly and safely.

## 12.2 Join code contract
The canonical join input is a **6-character uppercase alphanumeric code**.

Validation rules:
- exactly 6 characters,
- A–Z or 0–9 only,
- client-side validation should prevent obviously invalid network calls,
- server remains authoritative.

## 12.3 Auth requirement
Trusted join requires authenticated user context.
If the user is not authenticated when they enter Group Join, the flow must route through the minimum acceptable account/auth gate before calling the protected endpoint.

## 12.4 Join request rule
Join must use the canonical join endpoint and an `Idempotency-Key`.
Repeated join attempts with the same intent should not create inconsistent membership state.

## 12.5 Join success behavior
On success, the user must land in a coherent Group Root context showing:
- group name,
- membership status,
- role,
- latest regroup summary if available,
- optional itinerary summary,
- optional season-aware suggested packs.

## 12.6 Join failure behavior
Friendly, user-readable failures must exist for:
- bad format,
- no matching code,
- unauthorized / expired auth,
- already joined or conflict semantics,
- rate limiting,
- network failure.

## 12.7 Join-copy rule
User-facing copy should say **“6-character code”** rather than imply a numeric-only code.

---

# 13. Group Root behavior

## 13.1 Purpose
Group Root is the main coordination hub for current group status, fast check-in, regroup visibility, group creation/join entry, and related group actions.

## 13.2 Required content blocks
Group Root must include, where relevant:
- no-group state with Create Group and Join Group choices,
- group name and current role summary,
- fast “I’m Safe” action,
- latest regroup pin or regroup summary card,
- recent coordination freshness summary,
- join code/share card for leaders where appropriate,
- itinerary summary or shortcut if available,
- optional live board entry or teaser when entitlement permits,
- optional season-aware suggested pack card.

## 13.3 Required states
Group Root must support:
- no group yet,
- creating group,
- create group failed,
- not joined yet,
- joined with current content,
- joined with stale cached state,
- loading / refreshing,
- offline degraded state,
- entitlement-limited live features,
- group unavailable / removed / no longer active,
- auth required state if protected data cannot be refreshed.

## 13.4 Primary actions
- Create Group
- Join Group
- Share Join Code where leader and policy permit
- I’m Safe
- Open Regroup Detail
- Open Map Route to Regroup when available
- Open Live Board if available
- Open Group Itinerary if available

---

# 14. Check-in and “I’m Safe” behavior

## 14.1 Purpose
“I’m Safe” gives a pilgrim a fast, calm way to communicate status without exposing more information than needed.

## 14.2 Check-in content
Check-ins are text-first.
They may include:
- kind,
- text pin / short status,
- timestamp,
- client event id,
- freshness metadata.

They must not include precise GPS coordinates unless a future approved map/location handoff explicitly changes the contract.

## 14.3 Success behavior
On trusted server success, the UI may show confirmation and update Group Root/Live Board according to freshness state.

## 14.4 Offline behavior
If trusted server write cannot complete:
- do not pretend success,
- offer user-initiated SMS/share fallback if useful,
- preserve typed text only locally if the user intentionally keeps it,
- explain that group board was not updated.

## 14.5 Copy tone
Copy must be calm and precise:
- “Shared with your group” only after server success,
- “Message ready to send” for share/SMS drafts,
- “Not updated yet” for offline failure.

---

# 15. Live Board behavior

## 15.1 Purpose
Live Board gives a richer group status surface where permitted by entitlement and realtime availability.

## 15.2 Non-surveillance rule
Live Board is not live tracking.
It must not show hidden continuous location, movement trails, or passive pings.

## 15.3 Freshness rule
Every Live Board item must have enough timestamp/freshness metadata to avoid fake-live presentation.

## 15.4 Entitlement rule
`GROUP_LIVE_BOARD` may gate richer Live Board behavior, but baseline group coordination remains free.

## 15.5 Realtime degradation
If realtime fails:
- show last refreshed state with stale marker,
- offer manual refresh when online,
- preserve baseline regroup and safe-action access.

---

# 16. Regroup pin behavior

## 16.1 Purpose
A regroup pin lets a leader give members a clear meeting reference.

## 16.2 Leader-only rule
Only active leaders may create or update active regroup pins.
Server remains authoritative.

## 16.3 Required fields
A regroup pin should include:
- label,
- text pin,
- optional map anchor reference,
- created timestamp,
- optional expiry,
- active/inactive state.

## 16.4 Member behavior
Members should be able to:
- read regroup text clearly,
- copy text,
- launch map route when a map anchor exists,
- understand stale/expired state.

## 16.5 Offline behavior
Cached regroup pins may remain useful offline, but must show stale/last-updated context.
New regroup pin creation must not pretend success offline.

---

# 17. Itinerary behavior

## 17.1 Purpose
Group itinerary gives members lightweight shared plan visibility.

## 17.2 Scope rule
Itinerary is a simple coordination aid, not a complete tour-operator management system.

## 17.3 Write ownership
Itinerary writes are leader-managed, service-managed, or future-approved according to file `14`.

## 17.4 Offline behavior
Cached itinerary may be shown offline with stale markings.

---

# 18. Map handoff behavior

## 18.1 Handoff rule
When Group launches Maps, the destination context must remain understandable.

Examples:
- “Route to regroup point”
- “Open saved anchor from group”
- “Copy text instead” when map route is unavailable

## 18.2 Privacy rule
Map handoff does not grant ongoing location sharing.
It is a task-linked action.

## 18.3 Degradation rule
Route handoff should degrade:
- route preview,
- 2D route,
- text instructions,
- copyable regroup reference.

---

# 19. Privacy, freshness, and retention

## 19.1 Contract rule
Group presence, freshness, and any location-related handoff must follow `CONTRACTS/group_presence_privacy_contract.yaml`.

## 19.2 Foreground-first rule
Default group behavior is foreground and user-initiated.

## 19.3 No historical trail rule
The product must not create a general movement or location history of pilgrims.

## 19.4 Freshness states
Group surfaces should distinguish:
- fresh,
- stale,
- expired,
- unavailable,
- revoked where applicable.

## 19.5 Analytics privacy
Group analytics must not contain raw precise location, private text values, medical values, or hidden social graph data.

---

# 20. Accessibility and copy

## 20.1 Stress-safe copy rule
Copy should be short, calm, and explicit about state.

## 20.2 Large text rule
Group Root, join code, share code, regroup instructions, and “I’m Safe” actions must remain usable at large text sizes.

## 20.3 Screen reader rule
Freshness, role, and critical action states must be available to assistive technologies.

## 20.4 Color-independent rule
Live/stale/expired status must not rely on color alone.

---

# 21. Analytics and observability

## 21.1 Required analytics events
This feature family must emit canonical group events defined in file `17`, including at minimum:
- `group_create_start`,
- `group_create_complete`,
- `group_create_fail`,
- `group_join_start`,
- `group_join_complete`,
- `group_join_fail`,
- `group_live_board_view`,
- `group_checkin_start`,
- `group_checkin_complete`,
- `group_checkin_fail`,
- `group_checkin_fallback_sms`,
- `group_regroup_pin_view`,
- `group_regroup_pin_create`,
- `group_regroup_pin_route_launch`.

## 21.2 Required parameters where relevant
Allowed parameters include:
- `role`,
- `checkin_method`,
- `live_board_enabled`,
- `regroup_pin_state`,
- `network_state`,
- `season`,
- `freshness_status`,
- `failure_code`.

## 21.3 Forbidden analytics values
Do not send:
- join code,
- group name,
- raw check-in text,
- precise location,
- contact data,
- medical values.

---

# 22. Performance and reliability

## 22.1 Performance targets
Initial targets:
- fallback SMS/action sheet presentation p95 ≤ 300 ms,
- group creation endpoint p95 ≤ 1000 ms under normal service conditions,
- group join endpoint p95 ≤ 800 ms,
- check-in endpoint p95 ≤ 600 ms.

## 22.2 Reliability priorities
This feature family must optimize for:
- fast group creation feedback,
- fast join resolution,
- near-instant check-in acknowledgement at the UI layer,
- stable fallback messaging,
- honest stale/live indication,
- graceful degradation before coordination feels broken.

---

# 23. Testing and release evidence

## 23.1 Required test coverage
Tests must cover:
- group creation success,
- group creation offline failure,
- group creation idempotent retry,
- group creation rate-limit failure,
- group creation unauthenticated state,
- join success,
- join invalid code,
- join not found,
- join network failure,
- check-in success,
- check-in offline fallback,
- regroup pin leader-only writes,
- stale cached Group Root,
- Live Board gated/unavailable/degraded states,
- map handoff degradation,
- large text and screen reader behavior.

## 23.2 Release proof
Release evidence must include:
- physical-device proof for group creation/join/check-in flows,
- weak-network/degraded proof,
- stale-state UI proof,
- entitlement boundary proof,
- privacy proof that no hidden tracking or contact graph behavior exists,
- contract validation against `CONTRACTS/group_presence_privacy_contract.yaml` and `CONTRACTS/entitlement_capability_policy.yaml`.

---

# 24. Definition of done

The Group feature family is ready when:
- group creation is governed, authenticated, idempotent, and rate-limited,
- join-by-code is validated client-side and server-side,
- baseline coordination remains free,
- Live Board is clearly enhancement, not baseline,
- no hidden tracking or contact graph behavior exists,
- stale and offline states are honest,
- map handoffs are coherent and degraded-safe,
- analytics are privacy-safe,
- accessibility requirements are tested,
- release evidence satisfies file `28`.

---

# 25. AI-agent checklist

Before editing Group-related code, an AI agent must:
1. Read files `13`, `14`, `20`, `24`, `29`, and `31`.
2. Read `CONTRACTS/group_presence_privacy_contract.yaml`.
3. Read `CONTRACTS/entitlement_capability_policy.yaml`.
4. Confirm whether the change affects API, RLS, screen inventory, entitlement policy, or release gates.
5. Never add hidden tracking, contact import, generic chat, or automatic social graph behavior.
6. Update tests, fixtures, analytics, and docs together.

# Guide Marketplace boundary

Guide Marketplace is owned by file `32`, not Group.

A family or private party may use Hire a Guide, but V1 must not turn Group into:
- provider discovery,
- provider chat,
- provider presence tracking,
- provider booking,
- shared payment,
- provider review,
- automatic provider invitation.

Guide Marketplace must not reuse Group presence, join codes, Live Board, or regroup semantics as a hidden provider-location/social graph.

If a future approved flow lets a group leader share a guide profile or contact link with group members, that must remain an explicit lightweight share/handoff and must not change Group's privacy-light coordination contract without change control.

---

End of file.