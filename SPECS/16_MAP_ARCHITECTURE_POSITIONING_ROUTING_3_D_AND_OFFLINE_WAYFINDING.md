# 16 — MAP ARCHITECTURE, POSITIONING, ROUTING, 3D, AND OFFLINE WAYFINDING

## Document status
- **Type:** Normative map subsystem architecture document
- **Priority:** Highest
- **Audience:** Founder, mobile tech lead, Flutter engineers, backend engineers, map engineers, QA, AI coding agents, reviewer agents
- **Purpose:** Define the canonical architecture of the map and wayfinding subsystem, including provider strategy, positioning model, routing graph, indoor/outdoor behavior, 2D and 3D rendering rules, offline fallback, saved-anchor behavior, map data ownership, performance budgets, legal constraints, and release verification requirements.
- **Authority level:** This file is the canonical source of truth for all map and wayfinding system behavior. Feature files, provider integrations, Flutter modules, tests, and UI designs must not contradict this file.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`
- **Related files:** `09`, `10`, `11`, `17`, `19`, `20`, `23`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because map work is one of the highest-risk areas in the project.

Map systems for this product are unusually difficult because:
- the product wants an Al-Maqsad-like sense of indoor utility and guidance, not just a decorative map,
- GPS is often weak or unavailable indoors,
- the environment includes multiple floors, entrances, corridors, facilities, and dense crowds,
- offline behavior is essential,
- the user may be stressed, tired, or disoriented,
- 3D visuals can easily create false confidence if routing and positioning are weak,
- AI coding agents are highly likely to overfocus on visual map rendering and under-specify routing, confidence, and fallback behavior.

This file prevents those failures by defining:
- the architecture of the map subsystem,
- the difference between positioning, routing, rendering, and offline fallback,
- what kind of provider strategy is acceptable,
- how saved anchors and regroup links work,
- how map data is modeled,
- how the app must behave when positioning is weak or unavailable,
- what “good enough” means for real-world map usefulness.

---

# 2. Design intent and product alignment

## 2.1 Product-level map goal
The map system exists to help pilgrims orient themselves, find destinations, remember anchors, regroup, and recover when confused.

## 2.2 The product does not want “just a 3D map”
This system must deliver:
- understandable orientation,
- route guidance,
- saved anchor recall,
- indoor/outdoor continuity where possible,
- fallback guidance when high-fidelity mapping is unavailable,
- 3D rendering only when it improves actual wayfinding.

## 2.3 Al-Maqsad-inspired direction
Public descriptions of Al‑Maqsad describe it as an indoor navigation system for the Grand Mosque, using Bluetooth/BLE support and working without internet, which is important because it validates the need for a separate indoor positioning and offline architecture rather than a generic consumer map stack assumption. The new map subsystem should aim for similar utility in spirit while remaining implementation-realistic for this product.

## 2.4 Product constraints that shape the map subsystem
- Umrah-first scope
- calm and readable UX
- no invasive hidden tracking
- offline-first essential value
- maintainability for AI-assisted development
- practical device performance budgets

---

# 3. Map architecture principles

## 3.1 Separate the map subsystem into four layers
The map subsystem consists of:
1. positioning
2. routing / wayfinding logic
3. scene/rendering
4. offline fallback and saved-anchor guidance

## 3.2 Position confidence matters as much as position itself
A route drawn from a low-confidence position may be worse than explicit “position uncertain” guidance.

## 3.3 Routing correctness matters more than visual impressiveness
If the app has 3D visuals but poor path logic, the map subsystem is failing.

## 3.4 Offline fallback is mandatory
The map system must remain helpful even when precise positioning, high-fidelity packs, or connectivity are missing.

## 3.5 Provider lock-in must be contained
Feature modules must not depend directly on provider-specific map APIs across the whole app.

## 3.6 Saved anchors are first-class navigation primitives
Save My Gate and related anchors are not secondary conveniences. They are part of the map system’s recovery model.

## 3.7 Manual orientation support remains valid
The system must support explicit text-based or anchor-based guidance when automated positioning is weak.

---

# 4. Canonical subsystem decomposition

## 4.1 Positioning layer
Determines or estimates where the user is and how confident the system is in that estimate.

### Responsibilities
- fuse location/position signals
- manage permission state
- expose confidence score/state
- handle indoor vs outdoor transitions
- surface unavailable/uncertain states clearly

## 4.2 Routing and wayfinding layer
Computes paths and guidance recommendations within the supported graph.

### Responsibilities
- path search across graph nodes and edges
- floor-aware path calculation
- route instruction generation
- anchor-based route assistance
- degraded guidance when full routing is unavailable

## 4.3 Scene/rendering layer
Renders 2D and/or 3D map views, overlays, anchors, routes, controls, and map camera behavior.

### Responsibilities
- map rendering
- indoor floor rendering
- 2D and 3D visual modes
- route overlay rendering
- landmark/highlight rendering
- camera transitions and focus states

## 4.4 Offline fallback layer
Preserves useful navigation help when richer mapping is unavailable.

### Responsibilities
- micro-basemap fallback
- saved anchor recall
- text directions and reference guidance
- “closest known landmark” guidance
- manual “I am here / I think I’m near X” support if designed later

---

# 5. Provider strategy

## 5.1 Provider strategy goals
The provider strategy must support:
- high-quality mobile rendering,
- customizable indoor data representation,
- 2D and 3D scene support,
- offline pack support,
- custom route overlays,
- practical Flutter integration,
- strong abstraction boundaries.

## 5.2 Canonical provider recommendation
The architecture should assume a **custom-data-first rendering strategy** layered on top of a mobile map rendering SDK with strong offline and 3D support, instead of assuming a consumer public map provider alone can solve the whole problem.

## 5.3 Why a custom-data-first strategy is preferred
This product needs:
- indoor/floor data the app can model directly,
- custom route graph control,
- custom saved-anchor semantics,
- selective offline packaging,
- precise styling and camera control,
- future flexibility for sacred-site-specific wayfinding rules.

## 5.4 Acceptable provider posture
The rendering provider should be treated as a scene engine and basemap layer, not the sole owner of:
- route graph truth,
- indoor topology truth,
- saved-anchor semantics,
- product-specific destination logic.

## 5.5 Provider abstraction rule
All provider-specific objects must be wrapped behind map-domain interfaces.

Examples:
- `MapViewportController`
- `MapSceneAdapter`
- `PositioningProvider`
- `MapPackResolver`
- `RouteOverlayRenderer`

## 5.6 Forbidden provider pattern
Do not spread provider-native types, styling primitives, or query logic throughout unrelated feature code.

---

# 6. 2D vs 3D strategy

## 6.1 2D mode role
2D mode is the default clarity-first view.

### Best uses
- initial orientation
- facility browsing
- low-end devices
- small-screen clarity
- fallback mode when 3D is too heavy or confusing

## 6.2 3D mode role
3D mode is a selective wayfinding aid, not a universal default for every task.

### Best uses
- understanding vertical or multi-level structure
- indoor corridor and gate relation clarity
- route-following where level transitions matter
- visually relating landmarks and entrances in complex environments

## 6.3 3D activation policy
3D should be used when one or more of the following is true:
- the route crosses floors/levels,
- the location is structurally confusing in 2D,
- the user explicitly opens 3D mode,
- the product decides that specific indoor navigation flows default to 3D after validation.

## 6.4 3D fallback rule
If device capability, performance, battery, or asset availability is insufficient, the map must fall back to 2D or text guidance without breaking the flow.

## 6.5 Forbidden 3D behavior
Forbidden:
- forcing 3D when it reduces readability,
- treating 3D as proof of route correctness,
- requiring 3D assets for baseline orientation.

---

# 7. Indoor vs outdoor strategy

## 7.1 Indoor-first complexity focus
The most distinctive value of this subsystem is indoor and dense-campus navigation where commodity GPS mapping is weakest.

## 7.2 Outdoor strategy
Outdoor map behavior may rely more heavily on standard location services and broader basemap context.

## 7.3 Indoor strategy
Indoor behavior must support:
- floor/level selection or detection
- entrance/gate understanding
- corridor/path awareness
- facility and landmark discovery
- confidence-aware positioning

## 7.4 Indoor/outdoor continuity rule
The system should support transition states instead of pretending indoor and outdoor are separate unrelated worlds.

Examples:
- entering a gate from an external plaza
- moving from outer area to internal corridor
- transitioning from outdoor GPS confidence to indoor BLE/other positioning confidence

---

# 8. Positioning architecture

## 8.1 Positioning goal
The app should estimate the user’s location or navigational context well enough to support useful orientation, not pretend to offer impossible precision under all conditions.

## 8.2 Positioning sources
The architecture should support a layered positioning model.

### Source A — OS location services
Used primarily for outdoor context and coarse orientation.

### Source B — BLE / beacon-assisted indoor positioning
Used where supported to improve indoor location estimation or indoor zone detection.

### Source C — user-selected or anchor-assisted context
Used when precise automated positioning is unavailable.

### Source D — route and landmark inference
Used to refine guidance after user selects destination or confirms reference points.

## 8.3 Confidence model
Every position estimate must carry a confidence classification.

### Canonical confidence states
- `HIGH`
- `MEDIUM`
- `LOW`
- `UNKNOWN`
- `UNAVAILABLE`

## 8.4 UI rule for low confidence
When confidence is low or unknown, the app should:
- avoid overclaiming exact location,
- show softer position indicators if needed,
- suggest manual confirmation or nearby landmarks,
- continue offering saved anchors and text guidance.

## 8.5 No-hidden-tracking rule
Positioning must respect the product’s privacy posture. No passive always-on tracking by default.

## 8.6 BLE architecture rule
BLE support must be optional at system level.

The map subsystem should function meaningfully even if:
- BLE hardware is not available,
- permissions are denied,
- beacon infrastructure is missing,
- BLE data is too noisy.

---

# 9. Positioning model details

## 9.1 Position object contract
The internal map-domain position model should include at minimum:
- source type
- timestamp
- confidence state
- coordinate or logical location reference
- floor/level reference if known
- accuracy radius if available
- freshness

## 9.2 Logical location reference
The map system should support logical positions even when continuous coordinates are weak.

Examples:
- `gate:79:l2`
- `corridor:west-2`
- `facility:wudu-north`

## 9.3 Floor determination rule
The system should not assume floor is always known. Floor must be an explicit nullable field or inference state.

## 9.4 Freshness rule
Positioning state must include freshness and should not remain visually “live” forever when updates stop.

---

# 10. Routing architecture

## 10.1 Routing goal
Compute understandable paths between origin and destination using a product-owned graph model rather than only provider-native consumer routing assumptions.

## 10.2 Routing graph model
The routing graph must model:
- nodes
- edges
- floors/levels
- vertical connectors
- constraints
- landmarks
- destination categories

## 10.3 Node types
Examples:
- gate node
- corridor node
- plaza node
- facility node
- entrance node
- staircase node
- escalator/elevator node
- prayer area node
- regroup anchor node

## 10.4 Edge types
Examples:
- walkable corridor edge
- open plaza edge
- stairs edge
- ramp edge
- escalator edge
- lift/elevator edge
- restricted edge
- temporary closure edge if supported later

## 10.5 Edge attributes
At minimum:
- `from_node`
- `to_node`
- `distance_m`
- `estimated_seconds`
- `edge_type`
- `is_accessible`
- `is_bidirectional`
- `floor_from`
- `floor_to`
- `availability_state`

## 10.6 Routing algorithm rule
The algorithm may evolve, but the architecture must support:
- shortest path and/or weighted best path
- accessibility-aware path variants
- floor transition handling
- dynamic exclusion of blocked edges when available

## 10.7 Route output contract
A route result should include:
- route id
- start reference
- end reference
- ordered path segments
- floor transitions
- summary metrics
- text guidance steps
- confidence / guidance quality flag if relevant

---

# 11. Multi-level wayfinding rules

## 11.1 Multi-level navigation is a first-class requirement
The graph and UI must treat floors/levels as explicit structure, not as decorative metadata.

## 11.2 Level transition model
Vertical connectors must be modeled explicitly.

Examples:
- stairs
- escalators
- elevators/lifts
- ramps

## 11.3 Multi-level route presentation rules
The route UI should help the user understand:
- current level
- destination level
- where the next level change happens
- what connector type to use
- when they have reached the correct floor

## 11.4 Level uncertainty rule
If the user’s current floor is uncertain, the system must surface that uncertainty and may prompt them to confirm a nearby reference rather than drawing an overconfident path.

---

# 12. Landmark and POI model

## 12.1 Landmark role
Landmarks are not decorative. They improve orientation and route comprehension.

## 12.2 Landmark model
A landmark should include:
- `landmark_id`
- `title`
- `kind`
- `logical_ref`
- `coordinate or geometry ref`
- `floor/level`
- `priority`
- `visibility_hint`

## 12.3 POI/facility categories
Examples:
- gates
- restrooms
- wudu facilities
- prayer areas
- exits
- escalators/elevators
- regroup points
- medical/help points if supported

## 12.4 User-facing naming rule
Use user-friendly names in UI. `POI` may exist internally, but should not dominate user-facing copy.

---

# 13. Save My Gate and anchor architecture

## 13.1 Save My Gate is a map-domain primitive
It is not just a bookmark. It is part of the orientation and recovery system.

## 13.2 Anchor model
A saved anchor should include:
- anchor id
- kind (`GATE`, `LANDMARK`, `PIN`)
- display title
- short code or recognizable label
- optional floor/zone
- optional photo or note
- logical ref
- created timestamp

## 13.3 Anchor usability rules
A saved anchor must remain useful even when:
- live positioning is unavailable,
- high-resolution map packs are absent,
- the user reopens the app later offline.

## 13.4 Anchor-route dependency rule
The route system must be able to use a saved anchor as destination input even if the origin is approximate.

---

# 14. Group-location and regroup dependencies

## 14.1 Privacy-light principle
The map system should support group coordination without becoming a passive tracking product.

## 14.2 Group map dependencies
The group subsystem may depend on the map subsystem for:
- regroup pin references
- destination previews
- saved anchor cross-links
- route launch to regroup point

## 14.3 Forbidden dependency
Do not define the map subsystem so that it assumes continuous member location streams are always present.

## 14.4 Regroup pin map behavior
If a regroup pin includes a `map_anchor_ref`, the map subsystem should be able to:
- visualize it
- open route guidance to it
- fall back to text pin guidance if map assets are missing

---

# 15. Scene and rendering architecture

## 15.1 Rendering responsibilities
The scene/rendering layer must support:
- basemap rendering
- route overlays
- anchor markers
- landmark emphasis
- floor visualization
- camera control
- simple mode / clarity mode fallbacks

## 15.2 Rendering must not own business truth
Rendering is not the source of routing truth or entitlement truth.

## 15.3 Scene layers
Recommended layer concepts:
- basemap layer
- indoor structure layer
- route layer
- anchor/user marker layer
- landmark label layer
- temporary interaction/highlight layer
- regroup/shared pin layer

## 15.4 Render abstraction rule
The rest of the app should issue semantic requests such as “show route to anchor” or “highlight regroup pin,” not raw provider drawing calls.

---

# 16. Camera behavior

## 16.1 Camera goals
The camera should support orientation, comprehension, and step-following without disorienting the user.

## 16.2 Camera modes
Recommended modes:
- overview
- follow-position
- route-preview
- floor-focus
- anchor-focus

## 16.3 Camera rules
- route preview should show the path clearly before turn-by-turn or step-following starts
- follow mode should not rotate or tilt so aggressively that the user loses context
- floor-focus mode should clearly indicate the active level
- camera transitions must use centralized motion rules from the design system

## 16.4 Camera fallback rule
If device performance is poor, reduce animation intensity before degrading the core map utility.

---

# 17. Route instruction generation

## 17.1 Route guidance output types
The system should support:
- visual route line
- step list
- floor transition instructions
- landmark-based hints
- text fallback instructions

## 17.2 Text instruction goals
Text instructions should be:
- short
- unambiguous
- floor-aware
- landmark-aware where useful
- readable under stress

## 17.3 Instruction examples
- “Head toward Gate 79 on Level 2.”
- “Continue straight along the west corridor.”
- “Go up one level using the escalator ahead.”
- “Your saved gate is on your right after the next staircase.”

## 17.4 Localization rule
Instruction templates must be compatible with localization and RTL.

---

# 18. Offline map architecture

## 18.1 Offline goal
The map subsystem must remain useful when network access is absent.

## 18.2 Offline layers of value
### Layer 1 — no downloaded pack, no network
Must still support:
- saved anchor recall
- micro-basemap or minimal fallback map if bundled
- text-guidance and landmark guidance
- route launch failure explanation when high-fidelity routing is unavailable

### Layer 2 — downloaded map packs, no network
Should support:
- full local rendering of supported map area
- anchor display
- route guidance using local graph and map pack data
- 2D and selected 3D scenes where assets are installed

### Layer 3 — online and downloaded packs
Best available behavior with fresh control-plane and optional shared coordination enhancements.

## 18.3 Map pack categories
The architecture should support at least:
- lightweight fallback map assets bundled or preloaded
- high-resolution indoor map pack(s)
- optional 3D scene or enhanced layer pack(s)

## 18.4 Offline routing rule
If the local routing graph and required pack assets are installed, route calculation should work fully offline for supported areas.

## 18.5 Offline fallback rule
If full route calculation cannot run offline, the app must still offer:
- saved anchor location details
- route-unavailable explanation
- nearby landmark text guidance
- regroup pin text guidance where applicable

---

# 19. Map data model ownership

## 19.1 Product-owned map data domains
The product should own canonical representations of:
- routing graph
- level/floor structure
- anchor references
- landmark references
- destination category mapping
- pack metadata for map assets

## 19.2 Provider-owned vs product-owned boundary
A rendering provider may own tile/style/render internals, but the product should own the semantic navigation model.

## 19.3 Versioning rule
Map graph and map pack data must be versioned so route logic, pack assets, and app runtime remain compatible.

## 19.4 Compatibility rule
A map pack version must declare compatibility with:
- routing graph version
- minimum app version
- optional 3D scene schema version if applicable

---

# 20. Permissions and privacy

## 20.1 Location permission policy
The map subsystem may request location permission when it helps orientation or route-following, but must continue offering useful manual and anchor-based flows if permission is denied.

## 20.2 Bluetooth permission policy
BLE-related permissions may be requested only where indoor positioning support justifies them. The app must not become useless when the user declines.

## 20.3 Privacy rule
The map subsystem must not silently collect or transmit continuous location traces for analytics or group tracking by default.

## 20.4 Analytics rule
Map analytics should be privacy-light and focused on quality signals rather than detailed hidden movement histories.

---

# 21. Performance budgets and constraints

## 21.1 Performance goals
The map system must be practical on the supported target device range.

## 21.2 Minimum runtime goals
These are initial targets and may be tuned in file `17`:
- route preview render after request: under 1.5 seconds on supported devices with local data
- basic map pan/zoom interaction: visually responsive without persistent severe frame drops
- installed offline pack opening: under 2 seconds to usable first frame for a previously warmed context where possible

## 21.3 Memory rule
3D scenes and rich layers must not assume unlimited memory.

## 21.4 Degradation rule
If performance budgets are threatened:
1. reduce non-essential visual effects
2. reduce 3D fidelity
3. fall back to 2D or text guidance

Never keep the feature in a flashy but unusable state.

---

# 22. Legal, attribution, and data-rights rules

## 22.1 Provider attribution rule
Any third-party map or scene provider must be used according to its attribution and license requirements.

## 22.2 Data-rights rule
The product must have clear rights to any custom indoor geometry, route graph, landmark data, or 3D scene data it ships.

## 22.3 Offline licensing rule
Do not assume every provider or region permits the same offline capabilities. Legal and contractual limits must be checked during provider selection and rollout.

## 22.4 Holy-site sensitivity rule
Map naming, labeling, and guidance text must remain respectful and operationally accurate.

---

# 23. API and realtime dependencies

## 23.1 API dependencies
The map subsystem depends on the API layer for:
- pack manifest discovery
- optional destination suggestions if later approved
- regroup pin retrieval through group endpoints
- feature flags affecting map behavior

## 23.2 Realtime dependencies
Realtime is optional and may be used for:
- regroup pin updates
- live board-linked coordination signals

## 23.3 Offline independence rule
Core map wayfinding must not depend on live API or realtime connectivity when required local data is installed.

---

# 24. Flutter and native boundary rules

## 24.1 Flutter responsibility
Flutter feature layers should consume map-domain abstractions and shared map widgets, not provider-native internals.

## 24.2 Native bridge responsibility
Use native bridges only where platform or provider performance requires them.

Examples:
- advanced map rendering hooks
- BLE scanning or ranging APIs
- low-level positioning services

## 24.3 Boundary rule
Native code must remain behind stable map-platform interfaces so provider or platform changes do not leak through the whole codebase.

---

# 25. QA and release validation requirements

## 25.1 Required map validation categories
- no-network map use
- no-permission map use
- low-confidence position handling
- floor transition routing
- saved anchor recall
- regroup pin route launch
- 2D fallback when 3D unavailable
- checksum/pack mismatch handling
- route instruction readability
- low-end device performance behavior

## 25.2 Required real-world validation
Before release, the map subsystem should be tested in real representative environments where possible, especially for:
- indoor orientation clarity
- saved anchor usefulness
- route-following comprehension
- BLE/permission degradation behavior
- stress readability

## 25.3 Fake-success warning
A map demo that works on one device with ideal assets and perfect connectivity is not proof of a production-ready map subsystem.

---

# 26. Recommendations adopted into this architecture

## 26.1 Recommendation — treat Al-Maqsad as a utility benchmark, not a cloning instruction
The architecture takes inspiration from the publicly described utility of Al‑Maqsad—indoor navigation, BLE-assisted positioning, and offline usefulness—without assuming identical infrastructure or public API access.

## 26.2 Recommendation — separate positioning, routing, rendering, and fallback
This is now a hard architectural rule to prevent 3D rendering from swallowing the whole map conversation.

## 26.3 Recommendation — product-owned graph and anchor semantics
The product now owns route-graph, anchor, and landmark semantics even if rendering is outsourced to a provider SDK.

## 26.4 Recommendation — offline value in layers
The architecture now explicitly defines what the user still gets with no pack, with installed packs, and with full online context.

## 26.5 Recommendation — confidence-aware guidance
The system now treats low-confidence location as a first-class state instead of pretending exact accuracy indoors.

---

# 27. Anti-patterns forbidden by this map architecture

The following are forbidden unless explicitly approved.

## 27.1 Treating 3D map rendering as the whole map subsystem
Forbidden.

## 27.2 Relying only on GPS for indoor navigation
Forbidden.

## 27.3 Spreading provider-native map types across feature modules
Forbidden.

## 27.4 Requiring high-fidelity map packs for baseline anchor recall
Forbidden.

## 27.5 Presenting low-confidence indoor position as precise truth
Forbidden.

## 27.6 Making group coordination depend on passive live tracking
Forbidden.

## 27.7 Shipping route logic that cannot explain floor transitions clearly
Forbidden.

## 27.8 Using map visuals that reduce readability in critical guidance contexts
Forbidden.

---

# 28. When this file must be updated

This file must be updated whenever any of the following changes:
- provider strategy
- positioning sources or confidence model
- routing graph model
- node or edge semantics
- floor/level handling
- 2D vs 3D activation policy
- offline map pack strategy
- map data ownership boundaries
- camera behavior model
- route instruction contract
- group/regroup map dependencies
- legal/attribution posture
- performance budgets or fallback rules

If any of these change but this file is not updated, feature behavior, Flutter implementation, map data, and QA expectations will drift quickly.

---

# 29. Summary

This file defines the canonical map and wayfinding architecture for Pilgrims Mobile App.

It establishes:
- the four-layer subsystem model
- the provider strategy and abstraction rules
- the positioning and confidence model
- the routing graph and multi-level wayfinding rules
- the scene/rendering and camera behavior model
- the saved-anchor and regroup dependencies
- the offline map value layers
- the privacy, performance, legal, and QA requirements

Its purpose is to ensure that the map system becomes:
- actually useful,
- offline-capable,
- confidence-aware,
- respectful of user stress and privacy,
- and maintainable for long-term AI-assisted development.

