# 11 — SCREENS, STATES, NAVIGATION, AND UI BLUEPRINTS

## Document status
- **Type:** Normative screen contract and navigation blueprint document
- **Priority:** Highest
- **Audience:** Product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents
- **Purpose:** Define the canonical screen inventory, screen purposes, navigation structure, state coverage, modal and sheet rules, empty/loading/error/offline behavior, and UI blueprint requirements so the app is implemented consistently and evaluated against the same screen-level contract.
- **Authority level:** This file is the canonical source of truth for screen-level behavior and screen-to-screen navigation. Design mockups, Flutter screens, and tests must not contradict this document.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- **Related files:** `12`, `17`, `18`–`25`, `27`, `28`

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
- inconsistent loading, empty, and retry behavior,
- different features inventing their own UI conventions.

This file prevents those failures by defining:
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
- default/content state
- loading state
- empty state if relevant
- error state if relevant
- offline or degraded state if relevant
- unavailable or permission-denied state if relevant

## 2.3 Critical actions must be easy to find
Actions like Start Ritual, Save My Gate, Route to Destination, Join Group, I’m Safe, and Emergency help must never be buried or hidden behind low-priority UI.

## 2.4 Navigation must be predictable
Users should be able to understand how they got to a screen, what it is for, and how to go back or finish.

## 2.5 A modal is not a substitute for proper information architecture
Use modals and sheets only when they are a better interaction pattern than a full screen.

## 2.6 State honesty matters
If the data is stale, permission is missing, route confidence is low, or a pack is not installed, the UI must reflect that honestly.

---

# 3. Canonical navigation model

## 3.1 App shell navigation
The canonical app shell exposes five primary sections:
- Home
- Rituals
- Map
- Group
- Tools

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
- detail -> parent screen
- modal/sheet -> dismiss to underlying context
- deep linked screen -> return to sensible section root if history is shallow

## 3.4 Cross-section shortcut rule
The app may offer shortcuts from Home or contextual screens into another section’s task flow, but the user should still land in a coherent section context.

---

# 4. Screen taxonomy

## 4.1 Screen categories
The app uses these screen categories:
- root screens
- hub screens
- detail screens
- flow screens
- modal/sheet surfaces
- utility overlays

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
- JoinGroupFlow
- StartRitualFlow
- RoutePreviewFlow
- PackInstallFlow

## 4.4 Detail screens
Focused content or entity views such as:
- RitualStepDetail
- RICResultDetail
- SavedAnchorDetail
- RegroupPinDetail
- NoteEditor

## 4.5 Modal/sheet surfaces
Short-lived focused surfaces such as:
- quick action sheet
- destination picker sheet
- pack status sheet
- filter sheet
- permission explanation sheet
- confirm delete dialog
- account deletion / data deletion explanation sheet

---

# 5. Canonical screen inventory

This inventory defines the required screen set for MVP/V1 scope.

## 5.1 Shell and entry screens
1. Launch / Startup Resolver
2. Onboarding Welcome
3. Language / Preferences Setup
4. Optional Sign-In / Account Gate
5. Home Root

## 5.2 Rituals screens
6. Rituals Root
7. Start / Resume Ritual Screen
8. Ritual Session Overview
9. Ritual Step Detail
10. RIC Entry
11. RIC Result
12. Ritual Bookmarks / Saved Guidance

## 5.3 Map screens
13. Map Root
14. Destination Search / Picker
15. Route Preview
16. Active Wayfinding / Route Follow
17. Save Anchor / Save Gate Flow
18. Saved Anchor Detail
19. Floor / Level Selector Surface

## 5.4 Group screens
20. Group Root
21. Join Group Flow
22. Group Live Board
23. Check-In Quick Flow
24. Regroup Pin Detail / Route Launch
25. Group Itinerary

## 5.5 Tools screens
26. Tools Root
27. Planner List
28. Planner Item Editor
29. Reminder Editor / Reminder Settings Surface
30. Wallet List
31. Wallet Item Detail
32. Notes List
33. Note Editor
34. Bookmarks List
35. Phrasebook Root
36. Emergency / Assistance Root
37. Emergency Card Detail
38. Pack Catalog
39. Pack Detail / Install Flow
40. Settings Root

## 5.6 Simple Mode screens
41. Simple Mode Home
42. Simple Mode Ritual Shortcut
43. Simple Mode Map Shortcut
44. Simple Mode Group Shortcut
45. Simple Mode Emergency Shortcut

---

# 6. Shared screen blueprint template

Every screen blueprint in this file follows this template.

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

## 6.2 State checklist
For each screen, explicitly consider:
- loading
- loaded/content
- empty
- error
- offline/degraded
- permission missing
- unavailable/locked

---

# 7. Shell and startup screens

## 7.1 Screen: Launch / Startup Resolver
### Screen ID
`startup_resolver`

### Category
Entry / system screen

### Primary purpose
Resolve initial app state and send the user to the correct next screen quickly.

### Entry points
- app launch
- cold start
- deep link open

### Preconditions
None.

### Primary content blocks
- launch branding / minimal startup surface
- no dense content

### Primary actions
None; automatic resolution.

### Navigation exits
- Onboarding Welcome
- Home Root
- deep linked destination
- re-auth or account-related gate if absolutely required

### States
- initializing
- startup error (rare)

### Offline behavior
Must still resolve to local-capable Home or other local-first screen when possible.

### Rule
Do not turn this into a slow loading dashboard.

---

## 7.2 Screen: Onboarding Welcome
### Screen ID
`onboarding_welcome`

### Category
Flow screen

### Primary purpose
Introduce the app’s value and get the user to a usable state with minimal friction.

### Entry points
- first launch
- explicit onboarding reset

### Primary content blocks
- short value intro
- continue action
- optional skip / continue with essentials

### Primary actions
- continue
- choose language if inline

### Navigation exits
- language/preferences setup
- Home Root

### States
- default
- locale fallback state if necessary

### Offline behavior
Must still allow forward progress.

### Accessibility notes
Large text and screen-reader clarity are required.

---

## 7.3 Screen: Optional Sign-In / Account Gate
### Screen ID
`account_gate`

### Category
Flow screen / gate screen

### Primary purpose
Request authentication only when a trusted online feature actually requires it.

### Entry points
- Group join
- purchase restore/validation
- protected account settings

### Rule
Do not force this at first launch unless product direction changes.

### States
- sign-in choice
- loading
- auth failure
- offline unavailable for auth-required action

---

# 8. Home screen blueprints

## 8.1 Screen: Home Root
### Screen ID
`home_root`

### Category
Root screen

### Primary purpose
Act as the calm control surface for resume, recovery, and quick access to high-priority tasks.

### Entry points
- app shell Home tab
- post-onboarding
- post-flow completion

### Primary content blocks
- current ritual status card or start ritual card
- urgent shortcut cluster
- saved anchor / recent map action card
- group summary card if user has an active group
- planner/reminder summary
- pack readiness/preparation summary if useful

### Primary actions
- Start / Resume Ritual
- Save My Gate / open Map
- I’m Safe / open Group
- Phrasebook / Emergency

### Secondary actions
- open planner
- open pack catalog
- open settings or more tools

### Navigation exits
- Rituals Root / active ritual detail
- Map Root
- Group Root
- Emergency Root
- Tools Root

### States
- first-use empty / onboarding-oriented state
- normal personalized state
- offline local-only state
- stale remote summary state where applicable

### Data dependencies
- local ritual session
- saved anchor summary
- local planner summary
- group snapshot if available
- cached flags

### Offline behavior
Must remain meaningful offline.

### Accessibility notes
Urgent actions must remain above the fold where possible.

---

# 9. Rituals screen blueprints

## 9.1 Screen: Rituals Root
### Screen ID
`rituals_root`

### Category
Root / hub screen

### Primary purpose
Provide entry to active ritual guidance, start flow, history or saved guidance access if available, and RIC.

### Entry points
- shell tab
- Home shortcut
- deep link

### Primary content blocks
- active session card or start ritual card
- progress summary
- RIC quick entry
- saved guidance / bookmarks section

### Primary actions
- start or resume ritual
- open RIC
- open step detail

### States
- no session yet
- active session
- paused/completed session summary
- offline local session only

---

## 9.2 Screen: Start / Resume Ritual Screen
### Screen ID
`ritual_start_resume`

### Category
Flow screen

### Primary purpose
Start a new ritual session or resume a prior one.

### Entry points
- Home
- Rituals Root

### Primary content blocks
- session choice / current status
- start action
- resume action if applicable

### States
- no prior session
- resumable session available
- corrupted/local state recovery option

### Offline behavior
Fully supported using local content.

---

## 9.3 Screen: Ritual Session Overview
### Screen ID
`ritual_session_overview`

### Category
Flow / overview screen

### Primary purpose
Show current step, progress, and next action.

### Primary content blocks
- current step highlight
- next action card
- progress structure / step list
- shortcut to RIC

### States
- active session
- paused session
- completed session
- missing content fallback

### Navigation exits
- Ritual Step Detail
- RIC Entry

---

## 9.4 Screen: Ritual Step Detail
### Screen ID
`ritual_step_detail`

### Category
Detail screen

### Primary purpose
Explain the current or selected ritual step clearly.

### Primary content blocks
- step title
- concise action summary
- expandable detail
- related do/don’t / reminder blocks
- bookmark or note action

### States
- default content
- expanded detail
- offline content loaded
- missing content fallback

### Rule
This screen must favor readability over decorative material styling.

---

## 9.5 Screen: RIC Entry
### Screen ID
`ric_entry`

### Category
Flow screen

### Primary purpose
Collect focused information needed for ritual uncertainty resolution.

### Primary content blocks
- short step-by-step prompts
- answer controls
- current context summary if available

### States
- fresh start
- partially answered
- missing context warning

### Rule
Avoid intimidating or overly dense phrasing.

---

## 9.6 Screen: RIC Result
### Screen ID
`ric_result`

### Category
Result screen

### Primary purpose
Present outcome and recommended next action.

### Primary content blocks
- result status banner
- next action summary
- remedy card(s)
- optional expandable explanation
- save note / bookmark action

### States
- valid
- remedy required
- uncertainty not fully resolved
- offline local result

### Rule
The result must be calming and clear, not legalistic by default.

---

# 10. Map screen blueprints

## 10.1 Screen: Map Root
### Screen ID
`map_root`

### Category
Root screen

### Primary purpose
Provide a map-first hub for orientation, anchor recall, and route launch.

### Entry points
- shell tab
- Home shortcut
- regroup pin route launch
- saved anchor route launch

### Primary content blocks
- map viewport
- destination entry / search trigger
- current anchor shortcut
- recenter / focus controls
- optional mode controls (2D/3D, floor)

### States
- map ready
- no permission but map usable in fallback mode
- low-confidence position
- no pack / fallback mode
- offline with local assets
- map unavailable error

### Primary actions
- search destination
- save anchor
- open route preview
- focus saved gate

### Rule
This screen must prioritize utility over generic exploration.

---

## 10.2 Screen: Destination Search / Picker
### Screen ID
`map_destination_picker`

### Category
Flow screen or bottom sheet

### Primary purpose
Let the user choose a destination quickly.

### Primary content blocks
- search field
- category shortcuts
- recent / saved anchors
- regroup pin suggestions where relevant

### States
- default
- search results
- empty search result
- offline limited search

---

## 10.3 Screen: Route Preview
### Screen ID
`route_preview`

### Category
Flow screen

### Primary purpose
Show the user the chosen route before they begin following it.

### Primary content blocks
- route summary
- map preview
- floor changes summary
- text direction preview
- start guidance action

### States
- route ready
- low-confidence origin
- route unavailable fallback
- missing pack / degraded preview

### Rule
Do not overstate precision when confidence is low.

---

## 10.4 Screen: Active Wayfinding / Route Follow
### Screen ID
`route_follow`

### Category
Flow screen

### Primary purpose
Help the user follow the route in motion.

### Primary content blocks
- current instruction
- route map
- floor indicator
- anchor/destination summary
- quick switch to overview

### States
- active guidance
- low-confidence guidance
- route off-course or unclear
- guidance degraded to text/anchor mode

### Rule
This screen must remain readable in stressful walking contexts.

---

## 10.5 Screen: Save Anchor / Save Gate Flow
### Screen ID
`save_anchor_flow`

### Category
Flow screen or modal sheet

### Primary purpose
Save a gate or meaningful anchor.

### Primary content blocks
- suggested or selected anchor
- editable title/label
- optional note/photo
- confirm save action

### States
- suggested anchor
- manual entry fallback
- save success
- storage failure

### Offline behavior
Fully supported.

---

## 10.6 Screen: Saved Anchor Detail
### Screen ID
`saved_anchor_detail`

### Category
Detail screen

### Primary purpose
Show the saved anchor and support route launch or recall.

### Primary content blocks
- anchor title
- text location details
- optional image/note
- route action
- delete/edit action

### States
- full detail
- anchor only with no map pack
- route unavailable fallback

---

# 11. Group screen blueprints

## 11.1 Screen: Group Root
### Screen ID
`group_root`

### Category
Root screen

### Primary purpose
Act as the group coordination hub.

### States
- no group joined
- active group summary
- offline stale summary
- auth required gate

### Primary content blocks
- join group CTA or active group card
- quick I’m Safe action
- regroup summary
- recent check-ins or live board shortcut
- itinerary shortcut

---

## 11.2 Screen: Join Group Flow
### Screen ID
`group_join_flow`

### Category
Flow screen

### Primary purpose
Allow the user to join a group by code.

### Primary content blocks
- code input
- join CTA
- guidance text

### States
- empty form
- validating
- invalid code
- already joined
- offline unavailable
- auth required

### Rule
This must feel short and trustworthy.

---

## 11.3 Screen: Group Live Board
### Screen ID
`group_live_board`

### Category
Hub/detail screen

### Primary purpose
Show recent group status and coordination context.

### Primary content blocks
- member status list
- freshness indicators
- active regroup pins
- itinerary snippet if useful

### States
- active live data
- cached stale data
- unavailable by entitlement or feature flag
- no recent activity
- offline with stale snapshot

### Rule
Do not imply continuous tracking.

---

## 11.4 Screen: Check-In Quick Flow
### Screen ID
`group_checkin_quick`

### Category
Flow sheet or compact full screen

### Primary purpose
Let the user send a fast “I’m Safe” or status check-in.

### Primary content blocks
- suggested text pin
- editable text field
- send action

### States
- ready
- low-confidence location fallback
- sending
- success
- offline unavailable

---

## 11.5 Screen: Regroup Pin Detail / Route Launch
### Screen ID
`group_regroup_pin_detail`

### Category
Detail screen

### Primary purpose
Explain the regroup point and launch route or fallback guidance.

### Primary content blocks
- regroup label
- text pin details
- map anchor summary if present
- route action
- text fallback guidance

### States
- active regroup pin
- expired pin
- route available
- text fallback only

---

## 11.6 Screen: Group Itinerary
### Screen ID
`group_itinerary`

### Category
Detail screen

### Primary purpose
Show shared day-by-day itinerary information.

### States
- has itinerary
- empty/no itinerary
- offline cached itinerary
- unavailable

---

# 12. Tools and assistance screen blueprints

## 12.1 Screen: Tools Root
### Screen ID
`tools_root`

### Category
Root screen

### Primary purpose
Provide structured access to supporting utilities.

### Primary content blocks
- planner
- notes/bookmarks
- phrasebook
- emergency
- packs
- settings

### Rule
This must not become a cluttered junk drawer.

---

## 12.2 Screen: Planner List
### Screen ID
`planner_list`

### Category
Hub/list screen

### States
- empty planner
- populated planner
- offline (normal)

## 12.3 Screen: Planner Item Editor
### Screen ID
`planner_editor`

### Category
Editor screen or sheet

### States
- create
- edit
- reminder unavailable because permission denied

## 12.4 Screen: Notes List
### Screen ID
`notes_list`

### Category
List screen

### States
- empty
- populated
- supporter limit reached if applicable

## 12.5 Screen: Note Editor
### Screen ID
`note_editor`

### Category
Editor screen

### States
- create
- edit
- attachment issue
- storage error

## 12.6 Screen: Bookmarks List
### Screen ID
`bookmarks_list`

### Category
List screen

### States
- empty
- populated

## 12.7 Screen: Phrasebook Root
### Screen ID
`phrasebook_root`

### Category
Hub screen

### Primary purpose
Provide quick access to phrase cards and phrase categories.

### States
- category view
- search/filter state
- offline fully available

## 12.8 Screen: Emergency / Assistance Root
### Screen ID
`emergency_root`

### Category
Hub screen

### Primary purpose
Provide urgent help actions in a high-clarity layout.

### Primary content blocks
- big-text urgent actions
- medical profile shortcut
- saved gate shortcut
- I’m Safe / group action shortcut if relevant
- phrasebook urgent section

### States
- standard emergency hub
- sparse-data state (no medical profile, no saved gate, no group)
- offline fully available

### Rule
No decorative clutter and no weak contrast.

## 12.9 Screen: Emergency Card Detail
### Screen ID
`emergency_card_detail`

### Category
Detail screen

### Primary purpose
Show a large readable emergency or practical card.

### States
- card ready
- missing local profile data

## 12.10 Screen: Pack Catalog
### Screen ID
`pack_catalog`

### Category
List/hub screen

### Primary purpose
Show available downloadable packs.

### States
- loading cached manifest
- manifest available
- offline cached manifest
- no manifest yet
- all installed / mixed states

## 12.11 Screen: Pack Detail / Install Flow
### Screen ID
`pack_detail_install`

### Category
Detail/flow screen

### Primary purpose
Explain a pack and manage its install state.

### States
- not installed
- downloading
- verifying
- installed
- failed
- purged
- locked by entitlement
- low storage

## 12.12 Screen: Settings Root
### Screen ID
`settings_root`

### Category
Root/detail screen

### Primary purpose
Expose account, preferences, pack settings, notifications, privacy, account/data management, and app options.

### Primary content blocks
- account summary card or sign-in prompt
- Support this App / subscription entry
- language and local preferences section
- packs/download preferences section
- notifications and permissions summary section
- privacy and data section
- account/data management section with delete-account or deletion-request entry when authenticated
- help/about section

### Primary actions
- sign in or manage account
- restore purchase or manage subscription where appropriate
- edit local preferences
- open system settings for permissions when needed
- open delete-account / data-deletion flow or trusted web handoff when applicable

### States
- default
- auth-linked settings available/unavailable
- permissions summary states
- account/data-management available/unavailable state where auth or connectivity affects the path

---

# 13. Simple Mode screen blueprints

## 13.1 Screen: Simple Mode Home
### Screen ID
`simple_home`

### Category
Root screen

### Primary purpose
Expose only the highest-priority actions in a reduced-complexity layout.

### Primary content blocks
- Start / Resume Ritual
- Save My Gate / Map
- I’m Safe / Group
- Phrasebook / Emergency

### States
- default
- offline local-only
- active ritual shortcut state

### Rule
This is not a separate product. It is a simplified lens onto the same core architecture.

## 13.2 Simple Mode shortcut screens
These may reuse canonical screens with simplified entry framing rather than duplicating product logic.

Examples:
- `simple_ritual_shortcut`
- `simple_map_shortcut`
- `simple_group_shortcut`
- `simple_emergency_shortcut`

---

# 14. Canonical state families

Every screen should consider these shared state families where relevant.

## 14.1 `loading`
Use when the user is waiting for meaningful content.

## 14.2 `content`
Normal ready state.

## 14.3 `empty`
Used when there is no data yet and the user can act to create or obtain it.

## 14.4 `error`
Used when a request or operation failed unexpectedly.

## 14.5 `offline`
Used when the feature is degraded or local-only due to lack of connectivity.

## 14.6 `stale`
Used when cached data is still useful but may not reflect the latest trusted server state.

## 14.7 `permission_missing`
Used when a feature would benefit from or require a denied/absent platform permission.

## 14.8 `locked_or_unavailable`
Used when a feature is unavailable because of entitlement, account, pack, flag, or unsupported capability.

---

# 15. Navigation contract rules

## 15.1 Screen entry-point rule
Every screen must have documented entry points. Screens must not become orphaned destinations or secret deep routes.

## 15.2 Task-completion exit rule
After completing a task, the app should route the user to the most sensible next context.

Examples:
- after saving a gate -> Saved Anchor Detail or Map Root with confirmation
- after joining a group -> Group Root summary
- after pack install -> Pack Detail or contextually return to requested feature
- after RIC result -> Ritual Session Overview or retained result screen

## 15.3 Deep-link safety rule
If the user opens a deep-linked screen with missing prerequisites, the app must either:
- resolve them safely,
- or redirect to a sensible fallback with explanation.

## 15.4 Cross-feature navigation rule
Cross-feature navigation should land on a stable public screen, not on another feature’s internal implementation detail.

---

# 16. Modal, sheet, and dialog rules

## 16.1 Full screen vs sheet decision rule
Use a full screen when:
- the task is multi-step,
- the user needs strong focus,
- the content is dense,
- accessibility or large text may require more space.

Use a sheet when:
- the task is short,
- the context should remain visible behind it,
- the input scope is limited,
- the user is making a fast contextual choice.

Use a dialog only when:
- the user must confirm a critical action,
- or a very short blocking decision is needed.

## 16.2 Canonical sheet use cases
- destination picker
- quick check-in
- filter/sort controls
- floor selector
- permission explanation
- delete confirmation

## 16.3 Modal anti-pattern
Do not hide multi-step important flows inside overly cramped sheets.

---

# 17. Loading, skeleton, and placeholder rules

## 17.1 Loading states must be meaningful
Screens with repeated list or card structures may use skeleton placeholders when it improves perceived continuity.

## 17.2 Avoid fake content loading
Do not animate elaborate placeholders when a simple progress or immediate local content is more honest.

## 17.3 Local-first loading rule
If local data exists, show it immediately and refresh in the background rather than blocking on remote fetch.

---

# 18. Empty-state rules

## 18.1 Empty states must be actionable
An empty state should explain:
- what is missing,
- why it matters,
- what the user can do next.

## 18.2 Canonical empty-state examples
- no ritual session yet
- no saved anchor yet
- no group joined yet
- no planner items yet
- no notes/bookmarks yet
- no pack installed yet

## 18.3 Empty-state anti-pattern
Do not use vague empty states like “Nothing here” without a next action.

---

# 19. Offline and stale-state rules

## 19.1 Offline state rule
When a screen is offline-capable, it must still be useful using local data.

## 19.2 Stale-state rule
If the screen shows cached server-backed data, it must indicate staleness where it matters.

## 19.3 Protected-state rule
Do not show stale protected state as if it were confirmed truth when freshness materially matters.

Examples:
- entitlement access
- active group live status

---

# 20. Permission and unavailable-state rules

## 20.1 Permission state rule
If a feature is missing a useful permission, the screen must:
- explain the value of the permission,
- preserve fallback use where possible,
- offer a path to retry or open system settings when appropriate.

## 20.2 Capability-unavailable rule
If a feature is unavailable because of pack absence, unsupported device capability, or disabled flag, the UI must present a truthful unavailable state instead of a broken screen.

---

# 21. Entitlement and lock-state rules

## 21.1 Lock-state rule
If a feature or richer variant is gated, the screen must:
- explain the value of the upgrade,
- preserve ethical free access boundaries,
- avoid suggesting that correctness or essential safety is being withheld.

## 21.2 Examples of lock-state screens
- extended notes feature state
- supporter-only pack state
- group live board if supporter-gated in product policy

---

# 22. Accessibility-specific blueprint rules

## 22.1 Large text rule
No screen is complete unless it still works in larger text sizes.

## 22.2 Touch target rule
Critical actions must remain easy to tap under stressed conditions.

## 22.3 Screen-reader rule
Key screen titles, action labels, and state changes must remain understandable with assistive technology.

## 22.4 Emergency readability rule
Emergency and assistance screens must use the clearest and most robust presentation variants.

---

# 23. Analytics binding rule

## 23.1 Every primary screen must define at least
- screen viewed event
- primary action tapped events
- critical failure state exposed event where relevant

## 23.2 Analytics must not leak sensitive content
Do not log raw note content, medical profile details, precise private text pins beyond approved analytics policy, or other sensitive payloads.

---

# 24. UI blueprint artifact requirements

Every screen implementation should eventually be supported by a blueprint artifact that includes:
- screen name
- layout sketch or wireframe
- content hierarchy
- component references
- state variants
- navigation exits
- platform adaptation notes
- accessibility notes
- linked analytics events
- linked test cases

## 24.1 Rule
Design mockups are helpful, but they are not sufficient unless the state and navigation behavior are also specified.

---

# 25. Screen anti-patterns

The following are forbidden unless explicitly approved.

## 25.1 Building screens with only the happy-path state
Forbidden.

## 25.2 Reusing a screen for multiple unrelated jobs without a clear primary purpose
Forbidden.

## 25.3 Hiding critical actions inside overflow menus or secondary tabs
Forbidden.

## 25.4 Creating modal-heavy flows where full screens are more accessible and clearer
Forbidden.

## 25.5 Showing stale protected data without clear state communication
Forbidden.

## 25.6 Building map screens around provider capabilities instead of user tasks
Forbidden.

## 25.7 Duplicating functionally identical screens with slightly different styling instead of using shared blueprint variants
Forbidden.

---

# 26. Recommendations adopted into this screen contract

## 26.1 Recommendation — Home as the calm command surface
Home is now defined screen-by-screen as the place for resume, recover, and reach urgent help quickly.

## 26.2 Recommendation — map and group screens emphasize task launch over exploration
Map and Group root screens are structured around saved anchors, routes, check-ins, and regrouping rather than generic browsing.

## 26.3 Recommendation — every important screen has explicit degraded states
Offline, stale, permission-missing, and unavailable states are now part of the blueprint contract.

## 26.4 Recommendation — Simple Mode reuses the same product architecture
Simple Mode screens are shortcuts and reduced-complexity views, not a second disconnected app.

## 26.5 Recommendation — modal discipline
Sheets and dialogs are now governed explicitly to prevent cramped or inaccessible flows.

---

# 27. When this file must be updated

This file must be updated whenever any of the following changes:
- screen inventory
- top-level section roots
- primary screen purposes
- navigation entry or exit rules
- state coverage expectations
- modal/sheet usage rules
- major task completion routing
- accessibility-sensitive screen behavior
- pack or map screen state semantics
- Simple Mode screen set

If these evolve but this file is not updated, UI implementation and QA will drift quickly.

---

# 28. Summary

This file defines the canonical screen-level contract for Pilgrims Mobile App.

It establishes:
- the full screen inventory
- what each screen is for
- how users enter and exit it
- which states it must support
- what content blocks and actions are primary
- how navigation, sheets, dialogs, and degraded states should behave
- how blueprints must be documented for implementation and testing

Its purpose is to make the UI:
- coherent
- predictable
- resilient under failure
- accessible
- and safe for long-term AI-assisted implementation without screen-level drift.

