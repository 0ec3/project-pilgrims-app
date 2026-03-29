# 10 — PERSONAS, IA, USER JOURNEYS, AND TASK FLOWS

## Document status
- **Type:** Normative product behavior and UX structure document
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, Flutter engineers, QA, AI coding agents, reviewer agents, content/religious governance contributors
- **Purpose:** Define the canonical user personas, information architecture, core user journeys, key task flows, failure and recovery flows, offline behaviors, accessibility-sensitive behavior, and navigation intent of the app so that product, design, and implementation stay aligned.
- **Authority level:** This file is the canonical source of truth for how users move through the product and how the product should be structured around their needs. Screen-level details may be refined in file `11`, but must not contradict this document.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- **Related files:** `11`, `12`, `17`, `18`–`25`, `27`, `28`

---

# 1. Purpose of this file

This file exists because architecture alone does not tell the team what the app must feel like in real use.

For this product, user journeys are unusually important because:
- the app serves stressed, tired, distracted, and often first-time users,
- many flows happen while walking, waiting, searching, or coordinating in crowds,
- the app must remain useful under poor connectivity,
- the product includes both planned tasks and urgent “help me now” tasks,
- AI coding agents can easily build screens in isolation and miss the actual journey logic,
- a complex feature set can become overwhelming without a strong information architecture.

This file therefore defines:
- who the most important users are,
- what they are trying to achieve,
- how the product is organized for them,
- what the canonical task flows are,
- what happens when things go wrong,
- what the app must optimize for in both calm and stressful moments.

---

# 2. UX foundations from current platform guidance

The structure of this file follows several principles reinforced by current platform guidance:
- apps should use familiar navigation structures to reduce confusion rather than inventing unnecessary complexity, which Apple explicitly emphasizes in navigation guidance ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2022/10001/))
- adaptive design is not just about resizing UI, but about making the interface usable in the available space, which Flutter highlights in its adaptive design docs ([docs.flutter.dev](https://docs.flutter.dev/ui/adaptive-responsive))
- offline-first apps should present local data immediately and remain useful without reliable network, which Android’s offline-first guidance explicitly recommends ([developer.android.com](https://developer.android.com/topic/architecture/data-layer/offline-first))
- accessibility and larger-text support must be treated as normal product requirements, not late add-ons, which Flutter’s accessibility guidance reinforces.([docs.flutter.dev](https://docs.flutter.dev/ui/accessibility))

These principles are applied here as product rules, not just technical suggestions.

---

# 3. UX strategy summary

## 3.1 What the app must optimize for
The product must optimize for these four usage modes:
1. **Guided pilgrimage mode** — “What do I do now?”
2. **Recovery mode** — “I’m unsure / I made a mistake / I’m lost.”
3. **Coordination mode** — “Where is my group / how do we regroup?”
4. **Urgent assistance mode** — “I need help now.”

## 3.2 What the app must avoid
The app must avoid:
- overwhelming first-time users with too many entry points,
- burying urgent features behind secondary menus,
- making online-only assumptions during critical flows,
- requiring users to understand system architecture in order to get help,
- turning every feature into a dense power-user tool.

## 3.3 Navigation principle
The app should feel simple at the top level and richer only when the user drills into a relevant feature family.

---

# 4. Primary personas

The personas below are canonical product anchors. They are not marketing segments; they are behavior and design anchors.

## 4.1 Persona A — First-time Umrah pilgrim
### Summary
A first-time pilgrim with low confidence in the process and limited mental bandwidth during the journey.

### Goals
- understand what to do step by step
- avoid making a serious mistake
- know what to do next without reading too much
- feel reassured and not embarrassed by uncertainty

### Typical constraints
- limited familiarity with pilgrimage sequence
- may be tired or stressed
- may have weak connectivity
- may not be comfortable switching between several app sections

### High-priority product needs
- clear “start here” path
- strong rituals and RIC support
- clear next step and recovery guidance
- low cognitive load
- offline support

## 4.2 Persona B — Elderly pilgrim / low-confidence smartphone user
### Summary
A pilgrim who may understand the journey spiritually but struggles with modern smartphone complexity, dense UI, or fast-changing app states.

### Goals
- complete essential tasks with minimal confusion
- quickly access help, gate recall, and phrase support
- avoid complicated configuration and small controls

### Typical constraints
- large text needs
- slower reading or interaction pace
- one-handed use or motor limitations
- low tolerance for nested menus or hidden states

### High-priority product needs
- Simple Mode
- large touch targets
- large text options
- emergency shortcuts
- obvious navigation
- reduced visual clutter

## 4.3 Persona C — Group member traveling with family or a guided group
### Summary
A pilgrim relying on group coordination more than solo exploration.

### Goals
- know where the group is meeting
- send quick “I’m safe” updates
- follow regroup instructions without needing continuous tracking
- see shared itinerary context when available

### Typical constraints
- may be moving quickly between rituals and regrouping
- may not want complex map interactions
- may not want invasive location sharing

### High-priority product needs
- easy join flow
- obvious group entry point
- quick check-in
- regroup pins
- route-to-regroup support
- SMS/manual fallback language

## 4.4 Persona D — Group leader or organizer
### Summary
A user responsible for helping several pilgrims stay coordinated.

### Goals
- guide the group efficiently
- create clear regroup instructions
- reduce member confusion
- avoid repeated manual coordination in chaotic conditions

### Typical constraints
- time pressure
- repeated member questions
- mixed user skill levels in the group
- shared responsibility for safety and clarity

### High-priority product needs
- easy group creation/join management
- clear leader actions
- regroup pin posting
- itinerary visibility
- fast awareness of recent member check-ins

## 4.5 Persona E — Stress-response user
### Summary
A pilgrim who is disoriented, anxious, separated, or facing an urgent practical problem.

### Goals
- get immediate help
- communicate quickly
- recall a saved anchor or group regroup point
- avoid reading lots of explanatory text

### Typical constraints
- high emotional load
- little patience for setup or multi-step flows
- possibly offline or low battery

### High-priority product needs
- emergency mode
- big-text phrase support
- saved gate recall
- “I’m Safe” / regroup quick actions
- obvious back-to-home recovery path

## 4.6 Persona F — Quiet planner and note-keeper
### Summary
A pilgrim who uses the app before and during the journey for organization and reminders.

### Goals
- remember items and tasks
- keep small notes or bookmarks
- download the right packs before travel
- have things ready before entering stressful environments

### Typical constraints
- may use the app more calmly before travel, but still needs continuity on the journey

### High-priority product needs
- planner and reminders
- pack browsing and download clarity
- notes/bookmarks
- settings and preparation surfaces

---

# 5. Cross-persona stress factors

These are not separate personas, but conditions the app must handle well.

## 5.1 Low connectivity
The user may have weak, slow, or no network.

## 5.2 Fatigue
The user may be tired, dehydrated, rushed, or cognitively overloaded.

## 5.3 High-density environment
The user may be in a crowded, noisy, visually busy space.

## 5.4 Mixed language confidence
The user may rely on Arabic, English, Indonesian, transliteration, or phrase support.

## 5.5 Accessibility adjustments
The user may need larger text, simpler navigation, reduced transparency, reduced motion, or clearer contrast.

---

# 6. Information architecture goals

## 6.1 IA principles
The information architecture must:
- expose the most important tasks immediately,
- keep urgent tasks fast to reach,
- avoid burying core actions in deep navigation,
- separate planned tasks from urgent tasks clearly,
- keep the app understandable even for low-confidence users.

## 6.2 IA strategy
The app uses a **task-oriented top-level IA** rather than a purely technical or content-library-first IA.

## 6.3 Primary navigation rule
Top-level navigation should reflect what users need to do, not how the system is engineered.

---

# 7. Canonical top-level information architecture

## 7.1 Proposed top-level sections
The app should be structured around these primary sections:

1. **Home**
2. **Rituals**
3. **Map**
4. **Group**
5. **Tools**

This can be implemented through bottom navigation, adaptive side navigation, or another platform-appropriate structure, but these conceptual top-level sections remain canonical.

## 7.2 Section meanings
### Home
The dashboard and recovery surface. Entry point for most users.

### Rituals
Ritual steps, RIC, guidance, and next-step help.

### Map
Wayfinding, Save My Gate, anchors, route guidance, 2D/3D map modes.

### Group
Join, check-ins, live board, regroup, shared coordination.

### Tools
Planner, reminders, wallet, notes, bookmarks, phrasebook, emergency, settings entry points where appropriate.

## 7.3 Emergency shortcut rule
Emergency and high-priority assistive functions must be reachable without requiring a deep trip through the IA.

## 7.4 Simple Mode IA rule
Simple Mode may reduce visible complexity and expose only a smaller set of high-priority destinations, but it must still map back to the same canonical feature families.

---

# 8. Home architecture

## 8.1 Home purpose
Home is the calm control surface for the product.

## 8.2 Home must answer these questions quickly
- What should I do next?
- Where do I go for rituals?
- Where do I go for maps?
- How do I reach my group?
- Where is emergency help or phrase support?

## 8.3 Home content priorities
Recommended order of importance:
1. current journey guidance / quick start
2. urgent shortcuts
3. saved gate / recent map action
4. group status shortcut if applicable
5. planner/reminder summary
6. preparation/offline pack summary where useful

## 8.4 Home must avoid
- becoming a cluttered dashboard with every feature shown equally
- requiring horizontal exploration to discover core flows
- showing stale online data as if it were live truth

---

# 9. Rituals IA

## 9.1 Rituals entry role
The Rituals section is the canonical destination for pilgrimage guidance and RIC.

## 9.2 Rituals section should include
- active ritual session or start flow
- current step and next step
- RIC / mistake-resolution entry
- step list or progress structure
- bookmarks or saved guidance references where relevant

## 9.3 Rituals hierarchy rule
The user should always be able to answer:
- where am I in the process,
- what is next,
- what if I am unsure.

---

# 10. Map IA

## 10.1 Map entry role
The Map section is the canonical destination for orientation, wayfinding, anchors, and route guidance.

## 10.2 Map section should include
- current map view
- saved gate/anchor shortcut
- destination search or category selection
- route preview / route-following entry
- floor/level context if relevant
- map mode controls where appropriate

## 10.3 Map IA rule
Saved anchors and route guidance should be easier to access than broad exploratory map browsing.

---

# 11. Group IA

## 11.1 Group entry role
The Group section is the canonical destination for coordination.

## 11.2 Group section should include
- join/create or active-group summary
- recent member statuses/check-ins
- regroup pin visibility
- quick “I’m Safe” action
- itinerary shortcut if available

## 11.3 Group IA rule
The user should not need to understand realtime concepts to use the Group section.

---

# 12. Tools IA

## 12.1 Tools entry role
The Tools section contains supporting utilities and personal organization features.

## 12.2 Tools section should include
- planner
- reminders
- wallet
- notes
- bookmarks
- phrasebook
- emergency tools
- settings shortcut if not globally available elsewhere

## 12.3 Tools IA rule
Urgent support tools should still be accessible quickly even if they also live under Tools.

---

# 13. Canonical navigation model

## 13.1 Navigation goals
The navigation model should:
- make high-priority destinations discoverable,
- reduce deep nested navigation,
- preserve easy return paths,
- support both exploratory and urgent use.

## 13.2 Canonical navigation levels
### Level 1 — App shell navigation
Top-level sections: Home / Rituals / Map / Group / Tools

### Level 2 — Section hub and primary flows
Each section exposes its major tasks.

### Level 3 — Detail views and task-specific screens
Example: route details, note editor, RIC result, pack details.

## 13.3 Navigation recovery rule
The user must always have a clear way back to:
- Home
- current section root
- current urgent task context

## 13.4 Deep-link rule
Deep links may open directly into a relevant task, but the app must still make it clear where the user is within the overall structure.

---

# 14. Canonical user journey inventory

This section lists the primary journeys the product must support.

## 14.1 Onboarding and first-use journeys
- first launch
- language and permission setup
- first ritual session start
- first pack awareness
- first anchor save

## 14.2 Guided pilgrimage journeys
- start Umrah guidance
- resume active ritual session
- open current step
- resolve a mistake using RIC

## 14.3 Wayfinding journeys
- open map from Home
- save a gate
- route to a destination
- navigate to regroup pin
- recover using saved anchor offline

## 14.4 Group journeys
- join group
- send “I’m Safe” check-in
- read regroup instructions
- open live board or latest group state

## 14.5 Personal organization journeys
- add planner item
- enable reminder
- create note
- bookmark content
- browse/download packs

## 14.6 Assistance journeys
- open phrasebook
- use big-text emergency phrase
- open emergency card
- reach urgent shortcut from Home

## 14.7 Failure and recovery journeys
- no network at launch
- denied permission during map flow
- missing pack during map flow
- low-confidence map position
- entitlement refresh unavailable
- group live feature unavailable

---

# 15. Journey template

Every major journey in this document follows this structure:
- goal
- trigger
- preconditions
- primary path
- edge cases
- failure handling
- success outcome

---

# 16. Journey A — First launch and first-time setup

## Goal
Get a new user into a usable state quickly without overwhelming them.

## Trigger
User opens the app for the first time.

## Preconditions
Fresh install.

## Primary path
1. Launch screen resolves quickly.
2. User selects language or confirms default locale.
3. User sees concise onboarding focused on value, not feature dump.
4. User is offered the option to continue with simple setup.
5. User lands on Home with clear next actions.

## Key product rules
- Do not force account creation before the user can understand the app’s value unless a feature truly requires it.
- Do not ask for all permissions up front without context.
- Keep onboarding short and task-oriented.

## Edge cases
- no network
- unsupported locale fallback
- user skips onboarding

## Failure handling
- app still lands in a usable offline-capable Home state
- permission-reliant features explain later when needed

## Success outcome
User understands where to begin and sees at least one clear next action.

---

# 17. Journey B — Start Umrah guidance

## Goal
Help the user begin a guided Umrah flow with minimal confusion.

## Trigger
User taps “Start Umrah” or equivalent from Home or Rituals.

## Preconditions
None, beyond app open.

## Primary path
1. User enters Rituals.
2. User selects or confirms relevant context if needed.
3. App creates or resumes a ritual session.
4. App shows the current step, next step, and progress structure.
5. User continues through guidance.

## Key product rules
- The default scope is Umrah-first.
- The user should not be confronted with unnecessary Hajj-path complexity in the default Umrah flow.
- The app should explain “what next” more clearly than “what everything is.”

## Edge cases
- offline at start
- partially completed prior ritual session
- user changes language mid-session

## Failure handling
- use local ritual content and progress state
- allow reset/restart flow if session is corrupt or abandoned

## Success outcome
User enters a guided ritual session and knows what to do next.

---

# 18. Journey C — Resolve uncertainty or mistake with RIC

## Goal
Help the user recover from uncertainty, interruption, or a mistake.

## Trigger
User taps a “Not sure?”, “Check”, or RIC entry point.

## Preconditions
May occur inside or outside an active ritual session.

## Primary path
1. User opens RIC.
2. App asks focused questions or uses current ritual context.
3. App evaluates local rule content.
4. App returns a result with clear status and recommended next action.
5. If relevant, the user can save or note the remedy.

## Key product rules
- Keep the flow focused and calming.
- Do not overload the user with legalistic or overly dense explanation in the primary result.
- Provide expandable detail only when useful.

## Edge cases
- user has incomplete ritual context
- user is offline
- rule result requires a more careful explanation

## Failure handling
- if the app cannot confidently resolve, direct the user to a safer fallback explanation rather than pretending certainty

## Success outcome
User leaves the flow knowing what to do next or what uncertainty remains.

---

# 19. Journey D — Save My Gate

## Goal
Allow the user to save a memorable anchor for later recovery.

## Trigger
User taps “Save My Gate” from Home, Map, or a relevant quick action.

## Preconditions
User is in a context where a gate or anchor can be chosen or confirmed.

## Primary path
1. User opens save-anchor flow.
2. App proposes a gate/anchor or lets user enter/confirm it.
3. User saves it with optional note or photo.
4. Saved anchor becomes accessible from Home and Map.

## Key product rules
- This must work offline.
- The saved anchor must remain useful even without full map packs.
- The flow should be short and obvious.

## Edge cases
- no live position
- user saves non-gate anchor
- multiple saved anchors

## Failure handling
- allow manual text-based save if map precision is weak

## Success outcome
User can later open the saved anchor and orient themselves.

---

# 20. Journey E — Route to destination / wayfinding

## Goal
Help the user navigate to a destination or anchor.

## Trigger
User selects a destination, regroup pin, or saved anchor.

## Preconditions
Map subsystem available at least in fallback mode.

## Primary path
1. User opens Map or route action.
2. User chooses destination.
3. App assesses position confidence.
4. App computes route if possible.
5. App presents route visually and textually.
6. User can switch between overview and follow modes if supported.

## Key product rules
- low-confidence location must be shown honestly
- 2D must remain a clarity-first option
- 3D is supportive, not mandatory
- fallback text guidance must exist when richer map guidance is unavailable

## Edge cases
- offline with full pack
- offline without full pack
- floor unknown
- route unavailable
- location permission denied

## Failure handling
- switch to saved anchor guidance, landmark guidance, or text route hints

## Success outcome
User can move toward the destination with confidence appropriate to the available data.

---

# 21. Journey F — Join a group

## Goal
Allow a user to join a group safely and clearly.

## Trigger
User chooses to join a group from Group section or Home shortcut.

## Preconditions
Authenticated online session required.

## Primary path
1. User opens Group.
2. User taps Join Group.
3. User enters or pastes 6-character code.
4. App validates code via trusted backend.
5. App confirms joined state and shows group summary.

## Key product rules
- join requires trusted online confirmation
- code format should be easy to understand and validate locally before request
- the user should immediately understand they are now in a group context

## Edge cases
- already in the group
- invalid code
- offline
- auth expired

## Failure handling
- clear validation error or offline requirement explanation

## Success outcome
User becomes an active group member and sees group coordination tools.

---

# 22. Journey G — Send “I’m Safe” check-in

## Goal
Allow a group member to send a fast reassuring status update.

## Trigger
User taps “I’m Safe” or equivalent quick action.

## Preconditions
Authenticated active group membership and online trusted path.

## Primary path
1. User opens quick check-in action.
2. App suggests current text pin or allows manual pin text.
3. User confirms.
4. App posts check-in.
5. Group state updates.

## Key product rules
- this is text-based coordination, not hidden tracking
- the flow must be very short
- manual text input must remain possible if position inference is weak

## Edge cases
- offline
- low-confidence location
- no active group

## Failure handling
- provide manual fallback copy path or prompt to retry when online

## Success outcome
User’s group receives a trusted check-in update.

---

# 23. Journey H — Follow a regroup pin

## Goal
Allow a user to regroup with the group using a shared regroup point.

## Trigger
User opens active regroup pin from Group or map-related entry point.

## Preconditions
Group membership.

## Primary path
1. User sees active regroup pin.
2. User opens details.
3. User launches map route or text guidance.
4. App guides the user using map, anchor, or text fallback.

## Key product rules
- regroup pins must be understandable even if the user never opens full map exploration
- text-based guidance must remain available

## Edge cases
- offline with no full map pack
- low-confidence position
- regroup pin expired or removed

## Failure handling
- show text pin and nearest landmark guidance if route cannot be rendered

## Success outcome
User can head toward the regroup point with minimal confusion.

---

# 24. Journey I — Emergency / assistance shortcut

## Goal
Let the user reach urgent practical help immediately.

## Trigger
User taps emergency shortcut from Home, Tools, or Simple Mode.

## Preconditions
None.

## Primary path
1. User opens emergency or assistance mode.
2. App shows big-text, high-clarity urgent actions.
3. User accesses phrase card, medical profile, saved gate, or “I’m Safe” related action.

## Key product rules
- this must work offline
- this must not depend on account, group, or entitlement for basic access
- the interface must prioritize clarity over visual polish

## Edge cases
- no medical profile stored
- no saved gate
- no group joined
- low battery / no network

## Failure handling
- show available emergency tools even if some supporting data is missing

## Success outcome
User gets actionable help immediately.

---

# 25. Journey J — Browse and install offline packs

## Goal
Help the user prepare richer offline capability before or during the journey.

## Trigger
User opens pack catalog or is prompted contextually.

## Preconditions
Manifest available now or from cached snapshot.

## Primary path
1. User opens pack catalog.
2. User sees recommended or available packs.
3. User chooses a pack.
4. App shows size, purpose, entitlement requirement, and install state.
5. User downloads, verifies, and installs the pack.

## Key product rules
- use clear install states
- do not overcomplicate with technical jargon
- do not imply a pack is ready before verification completes
- support purge and retry flows

## Edge cases
- offline with cached manifest only
- low storage
- checksum failure
- entitlement required but missing

## Failure handling
- clear retry or storage resolution path

## Success outcome
Pack becomes installed and available for runtime use.

---

# 26. Journey K — Add planner item or reminder

## Goal
Allow the user to save a practical journey task or reminder.

## Trigger
User opens planner/reminders from Tools or contextual flow.

## Preconditions
None.

## Primary path
1. User opens planner.
2. User adds item.
3. User optionally enables reminder.
4. App stores item locally and schedules reminder if requested.

## Key product rules
- this is a local-first feature
- the flow should be lightweight, not like a full productivity suite
- reminder success should not depend on network

## Edge cases
- notification permission denied
- item created offline
- user in Simple Mode

## Failure handling
- item can still exist even if reminder cannot be scheduled yet

## Success outcome
User has a saved task and optional reminder.

---

# 27. Journey L — Create note or bookmark

## Goal
Allow the user to save information for later reference.

## Trigger
User bookmarks content or opens note creation.

## Preconditions
None.

## Primary path
1. User chooses to bookmark or create note.
2. App saves locally.
3. User can return later through Tools or contextual surfaces.

## Key product rules
- local-first by default
- quick enough to use during real travel context
- premium enhancement rules must remain ethically bounded

## Edge cases
- supporter/free feature limits
- attachment failure or storage limit if attachments are allowed

## Failure handling
- preserve core note/bookmark behavior even if richer attachment capability fails

## Success outcome
User can later retrieve saved content quickly.

---

# 28. Failure and recovery journeys

This product requires explicit recovery flows, not just error banners.

## 28.1 No network at launch
### Desired behavior
- app opens using local data
- Home remains meaningful
- stale or unavailable online sections degrade clearly

## 28.2 No permission during map flow
### Desired behavior
- map remains useful through anchors, destination browsing, and manual/fallback guidance
- app explains why live location would help without blocking use

## 28.3 Missing pack during map flow
### Desired behavior
- app offers fallback orientation or text guidance
- app may suggest pack download when online, but does not dead-end the user without explanation

## 28.4 Low-confidence map position
### Desired behavior
- app indicates uncertainty
- app suggests anchors or nearby landmarks
- app avoids overclaiming exact precision

## 28.5 Auth expired during group or purchase flow
### Desired behavior
- local-only features remain usable
- protected action pauses safely
- re-auth flow is clear

## 28.6 Entitlement refresh unavailable
### Desired behavior
- app uses safe local snapshot for continuity where appropriate
- does not promise newly granted access without server confirmation

---

# 29. Simple Mode behavior model

## 29.1 Purpose
Simple Mode exists to reduce cognitive load and expose only the highest-value actions.

## 29.2 Canonical Simple Mode destinations
Recommended visible actions:
- Start / Resume Rituals
- Save My Gate / Map
- I’m Safe / Group
- Phrasebook / Emergency

## 29.3 Simple Mode rule
Simple Mode removes visible complexity but does not create a second product architecture.

## 29.4 Exit and recovery rule
The user must always be able to return to the regular structure safely.

---

# 30. Accessibility-sensitive task-flow rules

## 30.1 Large text users
Flows must remain usable when text is significantly larger.

## 30.2 Low-vision users
Critical tasks must not depend on subtle translucency, weak contrast, or tiny map controls.

## 30.3 Screen-reader users
Key flows such as onboarding, rituals, emergency, group join, and basic pack installation must remain understandable with assistive technologies.

## 30.4 Motor/accessibility users
Primary tasks must avoid requiring overly precise gestures or tiny control targets.

---

# 31. Information architecture anti-patterns

The following are forbidden unless explicitly approved.

## 31.1 Hiding emergency or urgent assistance deep inside secondary navigation
Forbidden.

## 31.2 Treating Tools as a dumping ground for unrelated features
Forbidden.

## 31.3 Exposing too many equal-priority actions on Home
Forbidden.

## 31.4 Building screen flows around implementation boundaries instead of user tasks
Forbidden.

## 31.5 Making online-only assumptions inside core pilgrimage flows
Forbidden.

## 31.6 Creating Simple Mode as a disconnected second app
Forbidden.

---

# 32. Recommendations adopted into this UX structure

## 32.1 Recommendation — Home as recovery surface, not just dashboard
Home is now explicitly defined as the calm control surface that helps the user resume, recover, and reach urgent tasks quickly.

## 32.2 Recommendation — map utility before map exploration
The IA now prioritizes saved anchors, destination routing, and regroup actions over generic map browsing.

## 32.3 Recommendation — Simple Mode is strategic
Simple Mode is now structurally reflected in journeys and IA instead of treated as a later visual tweak.

## 32.4 Recommendation — explicit failure journeys
Offline, permission denial, stale state, and route-confidence problems are now first-class product journeys.

## 32.5 Recommendation — group coordination without hidden tracking
Group journeys now center around codes, check-ins, regroup pins, and clear map links instead of default continuous tracking.

---

# 33. When this file must be updated

This file must be updated whenever any of the following changes:
- canonical personas
- top-level section structure
- Home priorities
- Simple Mode scope
- major journey steps or their success criteria
- recovery flow expectations
- navigation hierarchy
- emergency shortcut behavior
- major accessibility-sensitive flow requirements

If these change but this file is not updated, screen design, feature implementation, and QA will drift quickly.

---

# 34. Summary

This file defines the behavioral and structural UX backbone of Pilgrims Mobile App.

It establishes:
- the primary personas
- the top-level information architecture
- the canonical navigation model
- the core user journeys
- the failure and recovery flows
- the role of Home, Rituals, Map, Group, and Tools
- the Simple Mode behavior model
- the accessibility-sensitive flow rules

Its purpose is to ensure that the product remains:
- understandable
- calm under stress
- task-oriented
- offline-capable
- and safe for long-term AI-assisted implementation without UX drift.

