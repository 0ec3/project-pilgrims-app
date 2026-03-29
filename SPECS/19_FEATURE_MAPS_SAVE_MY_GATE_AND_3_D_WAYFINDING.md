# 19 — FEATURE: MAPS, SAVE MY GATE, AND 3D WAYFINDING

## Document status
- **Type:** Normative feature-family specification
- **Priority:** Highest
- **Audience:** Founder, product lead, design lead, map engineers, Flutter engineers, backend engineers, QA, AI coding agents, reviewer agents, release agents
- **Purpose:** Define the canonical feature contract for the Maps feature family, including Map Root behavior, Save My Gate and saved-anchor flows, destination search, route preview, active wayfinding, 2D and 3D interaction rules, regroup/map handoffs, offline behavior, monetization boundaries, analytics hooks, and release-readiness expectations.
- **Authority level:** This file is the canonical source of truth for the Maps feature family. If implementation, UI, or tests diverge from this file, this file wins unless a higher-level normative contract or approved decision record explicitly changes it.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `04-DECISIONS-GLOSSARY-AND-CHANGE-CONTROL.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `09-PLATFORM-SPEC-IOS-LIQUID-GLASS-ANDROID-ADAPTATION-AND-NATIVE-BRIDGES.md`, `10-PERSONAS-IA-USER-JOURNEYS-AND-TASK-FLOWS.md`, `11-SCREENS-STATES-NAVIGATION-AND-UI-BLUEPRINTS.md`, `12-COPY-LOCALIZATION-RTL-AND-ACCESSIBILITY.md`, `13-DATA-MODEL-RLS-INVARIANTS-AND-MIGRATIONS.md`, `14-API-REALTIME-AND-INTEGRATION-CONTRACTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`, `17-ANALYTICS-OBSERVABILITY-AND-PERFORMANCE-BUDGETS.md`
- **Related files:** `20`, `23`, `24`, `25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file exists because maps are one of the easiest areas for a product team or AI agent to overpromise visually while underdelivering operationally.

For this project, the map feature family is unusually sensitive because:
- many users are tired, stressed, elderly, distracted, or low-confidence with smartphones,
- indoor and multi-level navigation is meaningfully harder than normal outdoor consumer-map use,
- the product explicitly wants Al-Maqsad-like utility in spirit, not merely a decorative campus map,
- weak positioning confidence can be more dangerous than no position at all,
- offline usefulness is a product promise rather than a nice-to-have,
- Save My Gate is not a convenience bookmark but a recovery primitive,
- 3D visuals can help comprehension in some cases and harm it in others,
- AI coding agents often overfocus on rendering and underdefine anchor recovery, fallback guidance, and degraded states.

This file prevents those failures by defining:
- what this feature family is responsible for,
- what users can and cannot expect,
- how Save My Gate and saved anchors work,
- how destination search and route guidance work,
- how 2D and 3D modes behave at the feature level,
- how map flows degrade when packs, permissions, positioning, or confidence are weak,
- how regroup pins and other shared map references interact with the feature,
- what must be tested and evidenced before release.

---

# 2. Feature purpose and user value

## 2.1 Feature family purpose
The Maps feature family exists to help pilgrims:
- orient themselves in complex or crowded environments,
- remember meaningful anchors such as entry/exit gates,
- recover when confused or disoriented,
- search for a destination or landmark quickly,
- preview and follow understandable routes where supported,
- regroup using text-first or anchor-aware flows,
- continue getting useful navigation help even when connectivity or positioning is degraded.

## 2.2 Main user value statement
A pilgrim should be able to open the Maps experience and quickly get help with one of these questions:
- Where am I relative to a gate, level, or landmark?
- How do I save this place so I can find it again later?
- How do I get back to my saved gate or anchor?
- How do I get to a destination or regroup point?
- How do I continue when the map cannot confidently place me?

## 2.3 Feature-level promise
This feature family must feel:
- calm,
- clear,
- confidence-aware,
- orientation-first,
- offline-capable,
- privacy-light,
- visually helpful but not visually theatrical.

---

# 3. Scope and boundaries

## 3.1 In scope
This feature family includes:
- Map Root as the main orientation and route-launch surface,
- Save My Gate and generalized saved-anchor behavior,
- destination search and picker flows,
- route preview behavior,
- active route-follow behavior,
- 2D and 3D map mode behavior,
- floor or level understanding in supported environments,
- anchor recall and anchor-to-route handoff,
- regroup pin visualization and route launch where applicable,
- manual orientation fallbacks such as landmark guidance and text guidance,
- offline-capable micro-basemap behavior,
- pack-aware richer map behavior,
- permission-aware and confidence-aware UX.

## 3.2 Out of scope
This feature family does **not** include:
- passive background location tracking,
- generalized crowd prediction claims,
- official authority routing ownership,
- guaranteed turn-by-turn precision in every indoor condition,
- live member tracking as a default coordination model,
- a server-first navigation product that breaks offline,
- a photorealistic 3D showcase built mainly for visual impressiveness.

## 3.3 Boundary with file `16`
File `16` is the canonical subsystem architecture for positioning, routing, rendering, graph design, and offline map layers.

This file does **not** re-decide those architectural truths.
Instead, it defines:
- the user-facing feature behavior,
- feature-level data contracts and UX rules,
- feature entry points and flows,
- entitlement and pack-facing behavior,
- what this feature must expose to QA and release gates.

## 3.4 Boundary with file `20`
Group coordination owns join/check-in/live-board semantics.
This file only defines the map-side behavior of regroup references, regroup visualization, and route launch into map flows.

## 3.5 Boundary with file `23`
Pack lifecycle, asset delivery, storage, and cache policy belong to file `23` and the pack/runtime contracts.
This file only defines how the map feature behaves when packs are installed, missing, stale, corrupted, or unavailable.

---

# 4. Product rules that govern this feature family

## 4.1 Orientation-first rule
This feature family exists to help people not get lost, recover calmly, and regroup.
If a behavior improves visual novelty but harms orientation clarity, it must be rejected.

## 4.2 Save My Gate is first-class
Save My Gate and other saved anchors are core orientation primitives, not secondary extras.
They must remain easy to access from both Home and Map flows.

## 4.3 3D is assistive, not sovereign
3D mode may be used where it genuinely improves route understanding, floor transition comprehension, or structural clarity.
It must never become the only acceptable mode or the default for every map interaction.

## 4.4 Confidence honesty rule
When location or floor confidence is weak, the UI must say so.
The app must not render a highly confident route or marker presentation that suggests precision the system does not have.

## 4.5 Offline usefulness rule
This feature family must remain meaningfully useful with no internet.
At minimum, the user must still be able to:
- open the micro-basemap or a clear fallback surface,
- recall saved anchors,
- search supported local gate/landmark data,
- view saved regroup references or text-based guidance where available,
- use text/landmark fallback when full routing is unavailable.

## 4.6 Privacy-light map rule
The feature must not become a passive tracking system.
Manual sharing, explicit route launch, optional foreground location, and optional BLE support are acceptable. Hidden continuous tracking is not.

## 4.7 Stress-safe UX rule
Walking, crowding, fatigue, and urgency must be assumed.
The feature must privilege large actions, obvious labels, short instructions, and reliable fallback paths.

## 4.8 Platform adaptation rule
The feature must inherit platform adaptation from the design system and platform spec.
Map controls, overlays, and modal behavior may adapt by platform, but map semantics, states, and feature truth must remain consistent.

---

# 5. Canonical terminology for this feature family

## 5.1 Map Root
The section-root screen for map and orientation tasks.

## 5.2 Saved anchor
A locally stored user reference point such as a gate, landmark, or manual pin, used for later recovery and routing.

## 5.3 Save My Gate
The user-facing anchor-saving flow centered on memorable gate-based recovery.

## 5.4 Destination
A route target such as a gate, landmark, facility, saved anchor, or regroup point.

## 5.5 Route preview
The pre-navigation state where the user sees the route summary, floor changes, and text guidance before actively following it.

## 5.6 Route follow
The in-motion or active wayfinding state focused on the current instruction and route progress.

## 5.7 2D mode
The default clarity-first representation of the map and route.

## 5.8 3D mode
A selective structural comprehension mode used when it improves floor, corridor, or entrance understanding.

## 5.9 Position confidence
The system’s confidence classification for current position or inferred navigational context.

## 5.10 Regroup pin
A group-coordination reference point that may be visualized or routed to in the map subsystem when available.

---

# 6. User stories

## 6.1 Save My Gate
- **As a pilgrim**, I can save the gate or anchor I want to remember so I can get back later.
- **As a pilgrim**, I can save it even if positioning is weak, by choosing or confirming it manually.
- **As a pilgrim**, I can later open the saved anchor offline and orient myself again.

## 6.2 Destination and route guidance
- **As a pilgrim**, I can search for a gate, landmark, or facility quickly.
- **As a pilgrim**, I can preview a route before I start moving.
- **As a pilgrim**, I can switch between overview and follow guidance without losing context.
- **As a pilgrim**, if the system is unsure of my location, it shows that honestly and gives me a fallback.

## 6.3 3D comprehension
- **As a pilgrim**, I can use 3D only when it helps me understand the structure or level changes better.
- **As a pilgrim**, I can return to 2D easily if 3D feels confusing, heavy, or visually crowded.

## 6.4 Regroup and shared coordination
- **As a group member**, I can open a regroup point inside the map and get orientation help to it.
- **As a leader**, I can rely on text-first regroup semantics even if members do not have strong positioning or rich map assets.

---

# 7. Free vs supporter boundaries

## 7.1 Free capability baseline
The following map value remains free:
- Map Root access,
- micro-basemap access,
- Save My Gate / saved-anchor flows,
- saved-anchor recall,
- short-code and gate/landmark search against local supported data,
- text-first shareable pin generation,
- regroup pin visualization where shared state or text reference is available,
- basic route preview and route-follow behavior using available local data and supported graph layers,
- 2D clarity mode and fallback guidance.

## 7.2 Supporter-linked map advantages
Supporter value comes primarily through downloadable packs and richer offline assets, not by paywalling essential recovery.
This may include:
- access to richer offline map packs when entitlement permits,
- improved floor/landmark clarity when a high-fidelity pack is installed,
- smoother pack-driven route experience under offline conditions,
- optional auto-download prompts subject to pack/entitlement policy.

## 7.3 No direct paywall on anchor recovery
The user must never be blocked from opening or recalling their saved anchor because they are not a supporter.

## 7.4 No monetization intrusion in critical route moments
Supporter prompts may appear in Pack Catalog or map pack suggestion surfaces.
They must not interrupt active wayfinding or a time-sensitive recovery flow.

---

# 8. Feature architecture overlay

## 8.1 Runtime responsibilities at the feature level
The Maps feature family is responsible for coordinating:
- map screen state,
- destination and anchor flows,
- route preview and follow flows,
- mode controls such as 2D/3D and floor selection,
- feature-visible permission states,
- pack-aware presentation states,
- cross-feature handoffs from Home and Group,
- telemetry emission defined for this feature family.

## 8.2 What this feature must not own
This feature must not directly own:
- provider-native rendering truth,
- BLE stack implementation details,
- route graph authoring workflows,
- pack installation lifecycle implementation,
- group authorization truth,
- entitlement truth.

## 8.3 Required stable interfaces
Feature implementation should depend on stable map-domain interfaces such as:
- `MapSceneAdapter`
- `MapViewportController`
- `PositioningProvider`
- `RoutePlanner`
- `SavedAnchorRepository`
- `MapPackResolver`
- `RegroupPinMapAdapter`

These are representative interface roles, not a locked exact naming requirement.

---

# 9. Data contracts and local persistence

## 9.1 Persistence posture
Saved anchors are device-local by default.
They are not synced to the server by default and must remain usable offline.

## 9.2 Canonical local entity — SavedAnchor
The feature must operate against a local saved-anchor model aligned with the data architecture.

### Required fields
- `anchor_id`
- `kind` (`GATE`, `LANDMARK`, `PIN`)
- `display_title`
- `short_code` or recognizable short label where possible
- `logical_ref`
- optional `floor_or_level`
- optional `zone`
- optional `note`
- optional `photo_uri`
- `created_at`
- optional `last_used_at`
- optional `is_current_primary`

## 9.3 Required invariants
- every saved anchor must have a stable local id,
- every saved anchor must have enough data to remain useful without network,
- `display_title` must be user-readable,
- `logical_ref` must resolve to a meaningful local map or fallback reference when supported,
- photo or note are optional enhancements and must never be required for a valid save.

## 9.4 Primary-anchor rule
The runtime should support one clearly marked primary current anchor for quick access while still allowing a small recent history.

## 9.5 Recent destination memory
The feature may persist recent destinations and recent route launches locally to accelerate repeat behavior.
These remain local-only by default.

## 9.6 Route session state
The runtime may keep ephemeral route session state such as:
- current destination reference,
- current route id,
- current floor target,
- current guidance mode,
- current degradation reason,
- last known confidence state.

This state is operational and may be cleared or recreated as needed.

---

# 10. Map content and destination taxonomy

## 10.1 Minimum destination classes
The feature must support route targeting or at least orientation targeting for:
- gates,
- landmarks,
- supported facilities,
- saved anchors,
- regroup points,
- relevant pack-supported categories if later expanded.

## 10.2 User-facing naming rule
Destination naming must stay human-readable.
The UI should say “Gate,” “Landmark,” “Restroom,” “Elevator,” or another clear term instead of exposing internal routing or POI jargon.

## 10.3 Landmark usefulness rule
Landmarks must be treated as comprehension aids, not decorative clutter.
They should be used in search ranking, route instruction generation, anchor titles, and fallback guidance where useful.

## 10.4 Mixed-language and code formatting rule
Gate codes, short codes, floor labels, and other alphanumeric references must remain bidi-safe and localization-safe in Arabic and other RTL contexts.

---

# 11. Save My Gate and saved-anchor behavior

## 11.1 Purpose
Save My Gate exists to let a user preserve a memorable recovery point quickly and reopen it later without friction.

## 11.2 Entry points
The Save My Gate or save-anchor flow must be reachable from:
- Home shortcut,
- Map Root,
- Route Preview where relevant,
- selected map marker or search result,
- regroup detail or other contextual surfaces when it makes sense.

## 11.3 Allowed anchor sources
A saved anchor may originate from:
- tapped gate on map,
- searched gate result,
- selected landmark,
- manually placed pin,
- regroup pin handoff converted into a local anchor if explicitly saved by the user.

## 11.4 Save flow requirements
The save flow must allow:
- clear title or generated label,
- gate/landmark confirmation,
- optional floor/zone confirmation,
- optional note,
- optional photo,
- explicit save confirmation.

## 11.5 Save flow design rule
The flow must remain short enough to complete under stress.
Advanced customization must never slow down the core save path.

## 11.6 Manual-save fallback
If positioning is weak or the map is not reliable enough to prefill an exact anchor, the user must still be able to save a text-confirmed or search-confirmed anchor manually.

## 11.7 Saved-anchor detail requirements
Saved Anchor Detail must expose:
- anchor title,
- gate/floor/zone or landmark summary,
- note/photo if present,
- route to anchor action,
- copy/share action,
- edit or delete action,
- confidence-aware language if the anchor is approximate.

## 11.8 Delete behavior
Deletion must require explicit confirmation and must not silently remove the current primary anchor without telling the user.

## 11.9 Empty state
When the user has no saved anchors, the empty state must explain:
- why saved anchors matter,
- how to create one quickly,
- that the feature works offline.

---

# 12. Shareable pin and short-code contract

## 12.1 Purpose
Shareable map references must work in ordinary messaging channels without requiring the recipient to open the app.

## 12.2 Text-first rule
Human-readable text is the canonical transport format.
Any future deep link is additive and must never replace the text-first share format.

## 12.3 Canonical shared-reference content
A shared reference should include, where available:
- user-friendly anchor title,
- gate number or landmark title,
- level/floor,
- zone,
- short human instruction for how to find it inside the app,
- optional compact short code.

## 12.4 Short-code rule
Short codes may exist for power users and fast re-entry but must not become the only recognizable identifier.

## 12.5 Receiving and parsing rule
The feature should support parsing supported short-code patterns locally when they appear in:
- search input,
- pasted text where feasible,
- selected app-internal share references.

## 12.6 Privacy rule
Sharing is always user-initiated. The system must never auto-broadcast live location or saved anchors.

---

# 13. Destination search and picker behavior

## 13.1 Primary goal
Destination Search / Picker exists to get the user to a meaningful destination with minimal typing and minimal cognitive load.

## 13.2 Search inputs
The picker should support:
- gate number search,
- localized gate or landmark text search,
- short-code search where supported,
- recent destinations,
- saved anchors,
- regroup suggestions when available.

## 13.3 Ranking priorities
Search ranking should prefer:
1. exact gate-code matches,
2. exact short-code matches,
3. exact saved-anchor matches,
4. strong localized title matches,
5. relevant landmark or facility matches,
6. recent relevant choices.

## 13.4 Offline search rule
Core search behavior must work fully against on-device data for supported gate and landmark datasets.
No web search or internet dependence is allowed for basic local map discovery.

## 13.5 Search-result presentation rule
Results must remain easy to scan while walking.
Each result should clearly show:
- title,
- gate/landmark label,
- floor/level if relevant,
- zone if relevant,
- saved or regroup badge where relevant.

## 13.6 Empty-result rule
The empty state must suggest practical alternatives such as:
- search by gate number,
- use a saved anchor,
- browse a category,
- use a regroup text reference.

---

# 14. Route preview behavior

## 14.1 Purpose
Route Preview exists to help the user understand where they are going before active guidance begins.

## 14.2 Required content blocks
Route Preview must include:
- destination summary,
- route map preview,
- floor transition summary where relevant,
- route length or relative effort summary where available,
- text instruction preview,
- route-quality or confidence message where relevant,
- start guidance action.

## 14.3 Route preview honesty rule
If the origin is approximate or floor confidence is weak, Route Preview must say so clearly and must not present the route as if it were exact.

## 14.4 Fallback route-preview state
If a full route cannot be computed, Route Preview should degrade to one of the following when possible:
- anchor-focus map view,
- destination highlight with nearest useful landmark,
- floor-aware text guidance,
- simple “how to search and orient” instructions.

## 14.5 Missing-pack rule
When richer preview depends on a missing pack, the screen may offer a pack suggestion but must still try to provide useful fallback guidance.

## 14.6 Start/exit behavior
From Route Preview, the user must be able to:
- start route follow,
- switch mode when supported,
- save the destination as an anchor,
- back out to Map Root without losing context unnecessarily.

---

# 15. Active wayfinding behavior

## 15.1 Purpose
Route Follow exists to help the user move with confidence using current instruction, map context, and fallback cues.

## 15.2 Required content blocks
Active Wayfinding / Route Follow must include:
- current instruction,
- route map or route context,
- destination summary,
- floor indicator,
- overview toggle,
- exit guidance action,
- visible degraded-state message when confidence or assets are weak.

## 15.3 Instruction style rules
Instructions must be:
- short,
- stress-readable,
- floor-aware,
- landmark-aware where useful,
- free of internal jargon,
- available in text form even when the map view is visually complex.

## 15.4 Route-follow state changes
The route-follow screen must explicitly handle:
- high-confidence guidance,
- medium-confidence guidance,
- low-confidence / uncertain origin,
- floor uncertainty,
- missing pack degraded mode,
- permission denied fallback,
- route no longer reliable,
- route exited by user.

## 15.5 Degradation behavior
If the feature can no longer maintain rich route-follow quality, it must degrade in a stable order such as:
1. reduce visual complexity,
2. prefer 2D over 3D,
3. retain route line if still useful,
4. switch to anchor/destination focus with text guidance,
5. switch to text/landmark recovery guidance.

## 15.6 Exit behavior
Exiting active wayfinding should route back to:
- Route Preview,
- Saved Anchor Detail,
- Regroup Pin Detail,
- or Map Root,

according to the most sensible task context.

---

# 16. 2D and 3D mode behavior

## 16.1 Default mode rule
2D is the default clarity-first map mode.

## 16.2 Role of 3D
3D exists to improve comprehension when:
- floor changes matter,
- vertical connectors matter,
- the surrounding structure is more understandable in 3D,
- route-follow comprehension is improved rather than degraded.

## 16.3 3D must not be universal default
3D must not become the default for all map entry states, all search states, or all anchor recall states.

## 16.4 Allowed 3D entry points
3D may be entered from:
- explicit user toggle,
- route preview for multi-level paths,
- route follow where the system validates a clear benefit,
- specific supported indoor scenes after real-world validation.

## 16.5 3D fallback rule
If device capability, performance, battery, or asset support is insufficient, the feature must fall back to 2D or text guidance without breaking the task.

## 16.6 3D interaction rule
3D interactions must remain simple and task-focused.
The user must not need expert map-manipulation skill to understand a route.

## 16.7 Visual clarity rule
3D shading, extrusion, labels, and camera angle must preserve route clarity and control readability.
Decorative rendering must not crowd out the instruction layer.

## 16.8 Accessibility and transparency rule
3D overlays, glass-like map controls, and floating chrome must degrade safely when contrast, reduced transparency, or reduced motion settings require it.

---

# 17. Floor and multi-level wayfinding rules

## 17.1 Multi-level handling is first-class
The feature must treat floors and levels as explicit task-relevant information, not hidden metadata.

## 17.2 Required level information in route surfaces
Where supported, route surfaces must clearly indicate:
- current level if known,
- destination level,
- next level transition,
- connector type,
- arrival on correct level.

## 17.3 Level selector behavior
The floor selector may be presented as a sheet or a lightweight overlay, but it must remain easy to use and easy to dismiss.

## 17.4 Level uncertainty rule
If the user’s current floor is uncertain, the feature should say so and may prompt them to confirm a nearby landmark or floor reference before drawing a highly specific path.

## 17.5 Accessibility-aware path support
Where the routing graph supports it, route preview and route follow should allow or derive accessibility-aware variants.
The UI must not imply accessible guarantees beyond what the graph and environment can actually support.

---

# 18. Positioning, permission, and confidence behavior

## 18.1 Positioning posture
Positioning is helpful but not guaranteed.
The feature must remain usable without live high-confidence positioning.

## 18.2 Source-aware user experience
The feature may benefit from:
- OS location,
- optional BLE/beacon-assisted context,
- user-selected anchors,
- landmark inference,

but the user-facing layer must remain centered on confidence and usability, not on exposing source complexity.

## 18.3 Permission request rule
Location and BLE permissions must be asked for in context and explained by user value.
The user must still have fallback map value even if permissions are denied.

## 18.4 No-permission fallback
If location permission is denied:
- the map remains openable,
- saved anchors remain usable,
- destination search remains usable,
- route launch may still work from approximate or manual origin where supported,
- the UI explains what richer positioning would improve.

## 18.5 Low-confidence behavior
When confidence is low or unknown, the feature should:
- soften or reduce exact-position emphasis,
- show low-confidence messaging,
- suggest nearby landmark confirmation,
- preserve saved-anchor and text-guidance paths,
- avoid exaggerated follow-mode certainty.

## 18.6 Freshness rule
Position indicators must not appear live forever after updates stop.
If position freshness decays, the feature must reflect that clearly.

---

# 19. Regroup, group, and shared-reference behavior

## 19.1 Privacy-light regroup rule
Map support for group coordination must rely on explicit regroup references, route launch, and text-first communication rather than passive member tracking.

## 19.2 Map-side regroup capabilities
When a regroup pin or map anchor reference is available, the feature should be able to:
- visualize it,
- open its detail,
- launch route preview to it,
- start route follow when supported,
- fall back to text guidance if richer map assets are unavailable.

## 19.3 Regroup pin visualization rules
Regroup references should be visually distinct from ordinary saved anchors while still remaining calm and readable.
The map must not become cluttered with stale or ambiguous regroup markers.

## 19.4 Cross-feature entry rule
When the user launches a regroup route from Group, they must land in a stable map screen context such as Route Preview or Map Root, not in an obscure provider-internal surface.

## 19.5 Regroup text fallback rule
If map assets, route computation, or confidence are insufficient, regroup text must still remain copyable and usable without pretending the map can do more than it can.

---

# 20. Offline behavior and degraded states

## 20.1 Offline tier
This feature family is a mixed offline feature family:
- essential orientation and anchor recovery are treated as Tier A or Tier B local-first capability,
- richer route fidelity and live shared state may degrade depending on local assets and recent snapshots.

## 20.2 Offline guarantees
Once the app has required local map data and local persistence available, the following must work meaningfully offline:
- open Map Root in fallback/local mode,
- open and recall saved anchors,
- search supported local gates and landmarks,
- view a saved regroup reference if already available locally or textually,
- preview a route where the supported local graph and assets allow it,
- fall back to text guidance when richer route guidance is unavailable.

## 20.3 No-pack behavior
When no high-fidelity pack is installed, the feature must still provide:
- micro-basemap or minimal structural view,
- gate/landmark orientation,
- saved-anchor recall,
- supported local search,
- text/landmark guidance.

## 20.4 Missing-data rule
If a user requests a capability that genuinely cannot work because local data is missing, the feature must say so plainly and offer the best next action.

## 20.5 Corrupted-pack rule
If a required pack is corrupted or incomplete, the feature must not crash or render nonsense.
It should surface a pack problem state and degrade to the best available fallback.

## 20.6 Stale shared-state rule
If group-linked or control-plane state shown in map context is stale, the UI must say so where it matters.

---

# 21. Screen and UX contract for this feature family

## 21.1 Canonical screens
This feature family owns or strongly depends on the following canonical screens:
- `map_root`
- `map_destination_picker`
- `route_preview`
- `route_follow`
- `save_anchor_flow`
- `saved_anchor_detail`
- `floor_selector_surface`

## 21.2 Map Root UX contract
### Required content blocks
- map viewport,
- destination search trigger,
- current anchor shortcut,
- recenter/focus controls,
- mode controls where appropriate,
- pack/degraded state messaging where relevant.

### Required states
- map ready,
- offline local mode,
- no permission but usable fallback,
- low-confidence position,
- no pack / fallback mode,
- map unavailable error.

### Primary actions
- search destination,
- save anchor,
- open route preview,
- focus saved gate.

### Rule
Map Root must prioritize utility over broad exploration.

## 21.3 Destination Picker UX contract
### Required content blocks
- search field,
- category shortcuts where available,
- recent and saved anchors,
- regroup suggestions when relevant,
- clearly ranked results.

### Required states
- default,
- search results,
- empty results,
- offline limited search.

### Rule
The picker should be fast and readable enough for walking or quick-stop use.

## 21.4 Route Preview UX contract
### Required content blocks
- route summary,
- map preview,
- floor changes summary,
- text direction preview,
- start guidance action,
- degradation explanation where needed.

### Required states
- route ready,
- low-confidence origin,
- route unavailable fallback,
- missing pack / degraded preview,
- offline route from local graph if available.

### Rule
Do not overstate precision when confidence is low.

## 21.5 Route Follow UX contract
### Required content blocks
- current instruction,
- route map or route context,
- floor indicator,
- anchor or destination summary,
- overview toggle,
- exit guidance action.

### Required states
- normal follow,
- low-confidence follow,
- floor uncertainty,
- degraded text mode,
- route lost or route unavailable,
- user-exited state.

### Rule
Active wayfinding must keep the current instruction and next useful action easy to find.

## 21.6 Save Anchor / Save Gate Flow UX contract
### Required content blocks
- proposed gate/anchor summary,
- manual search or confirm action,
- optional note/photo controls,
- save action,
- post-save confirmation.

### Required states
- prefilled candidate,
- manual entry/selection,
- weak-confidence manual save,
- validation error,
- save complete.

### Rule
This flow should remain short and not depend on perfect live positioning.

## 21.7 Saved Anchor Detail UX contract
### Required content blocks
- anchor title,
- gate/floor/zone or landmark summary,
- optional note/photo,
- route action,
- share/copy action,
- edit/delete controls.

### Required states
- content ready,
- missing underlying map asset but anchor still valid,
- approximate/manual anchor warning,
- deleted or missing anchor error.

### Rule
The detail screen should make later recovery feel easy, not archival.

## 21.8 Floor Selector UX contract
### Required content blocks
- available floors/levels,
- current active floor indicator,
- quick switch controls,
- contextual information about destination floor where relevant.

### Required states
- explicit floor list,
- limited known floors,
- floor uncertainty message if needed.

### Rule
The floor selector must not become a complex hidden menu system.

---

# 22. Copy, localization, RTL, and accessibility rules for maps

## 22.1 Copy tone
Map copy must be:
- direct,
- short,
- calm,
- confidence-aware,
- landmark-oriented when useful.

## 22.2 User-facing instruction style
Prefer language such as:
- “Head toward Gate 79 on Level 2.”
- “Continue along the west corridor.”
- “Go up one level using the escalator ahead.”
- “Location uncertain. Use your saved gate or nearby landmark to confirm.”

Avoid dense cartographic jargon or false certainty.

## 22.3 Mixed-content formatting
Gate codes, floor labels, and short codes must display correctly in RTL contexts using bidi-safe formatting practices.

## 22.4 Accessibility requirements
Map surfaces must support:
- large enough controls,
- strong control contrast,
- non-map text fallback for current instruction,
- understandable low-confidence communication,
- screen-reader labels for important controls,
- reduced-motion-safe transitions,
- reduced-transparency-safe control surfaces.

## 22.5 Map-only signal anti-pattern
Critical route information must never exist only as a visual line or subtle highlight on the map.
Text and state communication must remain available.

---

# 23. Performance and operational rules for this feature family

## 23.1 Performance authority
Performance budgets are defined normatively in file `17` and map architecture file `16`.
This feature must obey them.

## 23.2 Operational priorities
This feature must optimize for:
- startup into Map Root without heavy blocking,
- fast anchor recall,
- stable route preview,
- usable route-follow updates,
- responsive floor changes,
- graceful degradation before visual or runtime collapse.

## 23.3 Feature-level budget discipline
If a feature addition risks map clarity, device thermals, memory pressure, or route latency, the feature must prefer reduced visual richness over degraded core wayfinding.

---

# 24. Analytics and observability requirements

## 24.1 Required analytics events
This feature family must emit the canonical map events defined in file `17`, including at minimum:
- `map_root_view`
- `map_pack_missing`
- `map_position_state_change`
- `map_floor_change`
- `map_destination_select`
- `map_route_preview_start`
- `map_route_preview_complete`
- `map_route_preview_fail`
- `map_route_follow_start`
- `map_route_follow_degrade`
- `map_route_follow_exit`
- `map_anchor_save`
- `map_anchor_recall`
- `map_anchor_share`

## 24.2 Required analytics parameters where relevant
- `position_confidence_state`
- `pack_state`
- `route_mode`
- `graph_version`
- `fallback_type`
- `permission_state_location`
- `permission_state_bluetooth`

## 24.3 Map funnel expectations
This feature must support the map funnels defined in file `17`, especially:
- orientation and map recovery,
- Save My Gate / anchor recovery,
- regroup pin route launch where relevant.

## 24.4 Privacy analytics rule
Telemetry must not capture hidden continuous path traces or exact route replay by default.
Measurement should focus on success, failure, degradation, and fallback.

## 24.5 Non-fatal monitoring priorities
High-priority non-fatal map issues include:
- route preview failures,
- corrupted local map asset failures,
- repeated floor-switch failures,
- rendering failures that force fallback,
- pack-dependent route regressions,
- positioning-state errors that misrepresent confidence.

---

# 25. Testing and validation requirements

## 25.1 Required automated coverage
Automated tests must cover at minimum:
- saved-anchor creation, edit, recall, and deletion,
- short-code parse behavior,
- destination ranking behavior for gate vs landmark queries,
- route-preview state transitions,
- route-follow degraded-state transitions,
- no-permission fallback behavior,
- pack-present vs pack-missing behavior,
- 2D/3D mode toggling and fallback behavior,
- regroup pin map visualization and route-launch handoff,
- localization-safe instruction rendering.

## 25.2 Required manual/device validation
Manual or device validation must cover at minimum:
- Save My Gate flow under real movement/stress conditions,
- offline anchor recall,
- route preview comprehension,
- route-follow comprehension,
- low-confidence positioning presentation,
- floor change comprehension,
- 3D clarity versus 2D fallback on supported and weaker devices,
- pack-missing degraded states,
- RTL display of gate/floor/short-code content,
- screen-reader usability of core map controls.

## 25.3 Real-world validation requirement
Before release, representative real-environment testing should validate:
- indoor orientation clarity,
- saved anchor usefulness,
- route-following comprehension,
- BLE/permission degradation behavior,
- readability under stress and movement.

## 25.4 Fake-success warning
A visually impressive demo route on one device is not evidence that the feature is release-ready.
Release confidence requires degraded-state and offline validation.

---

# 26. Definition of done for this feature family

This feature family is not ready for release unless all of the following are true:
- Save My Gate works offline and remains useful later,
- Map Root supports meaningful no-pack and no-permission states,
- destination search works against supported local data,
- route preview and route-follow handle low-confidence and degraded states honestly,
- 3D mode is assistive and safely falls back,
- regroup pin handoffs work without requiring passive live tracking,
- analytics hooks are wired according to file `17`,
- device validation confirms clarity and recovery under stress,
- the feature respects the free/supporter and privacy boundaries.

---

# 27. Cross-file dependency rules

## 27.1 If saved-anchor model changes
Update:
- this file,
- file `13`,
- relevant tests and fixtures,
- file `11` if screen states or flows change.

## 27.2 If route preview or route-follow screen behavior changes
Update:
- this file,
- file `11`,
- file `16` if the change alters deeper map-system truth,
- file `17` if analytics, budgets, or event semantics change.

## 27.3 If regroup-pin map behavior changes
Update:
- this file,
- file `20`,
- file `14`,
- file `13` if the data shape changes.

## 27.4 If pack-dependent map behavior changes
Update:
- this file,
- file `23`,
- file `15`,
- file `17` if performance or degraded telemetry rules change.

## 27.5 If 2D/3D activation policy changes
Update:
- this file,
- file `16`,
- file `11` where route/map states change,
- release evidence expectations if materially affected.

---

# 28. Anti-patterns forbidden by this document

The following are forbidden unless explicitly approved.

## 28.1 Treating the map feature as a decorative 3D showcase
Forbidden.

## 28.2 Requiring high-fidelity packs for basic anchor recall
Forbidden.

## 28.3 Presenting low-confidence position as precise truth
Forbidden.

## 28.4 Making regroup depend on passive continuous tracking
Forbidden.

## 28.5 Hiding Save My Gate behind deep or secondary navigation
Forbidden.

## 28.6 Making map recovery depend on internet connectivity for baseline usefulness
Forbidden.

## 28.7 Exposing provider-native map concepts directly across feature code
Forbidden.

## 28.8 Using 3D when it materially harms readability or control clarity
Forbidden.

## 28.9 Relying on visual route lines without text fallback for important guidance
Forbidden.

## 28.10 Treating pack suggestions or monetization as more important than route recovery
Forbidden.

---

# 29. Implementation priorities

## 29.1 Phase 1 priorities
Implement first:
- Map Root with micro-basemap fallback,
- Save My Gate and saved-anchor recall,
- local search for gates/landmarks,
- text-first shareable pins,
- route preview and route-follow baseline in 2D,
- no-permission and no-pack degraded states,
- Home and Group handoffs into stable map screens.

## 29.2 Phase 2 priorities
Then add:
- richer pack-aware map clarity,
- better floor-aware routing surfaces,
- regroup pin visualization and route launch polish,
- stronger low-confidence recovery cues,
- better recent-destination and anchor workflows.

## 29.3 Phase 3 priorities
Then refine:
- selective 3D defaults for validated scenarios,
- stronger scene fidelity where it does not harm clarity,
- device- and capability-aware visual tuning,
- deeper real-world optimization based on evidence.

---

# 30. When this file must be updated

This file must be updated whenever any of the following changes:
- Save My Gate or saved-anchor behavior,
- destination types or search behavior,
- route preview or route-follow flows,
- 2D vs 3D activation rules,
- map screen states,
- regroup/map interaction behavior,
- pack-dependent map UX,
- permission or confidence handling at the feature layer,
- analytics hooks for map journeys,
- release-evidence expectations for map validation.

If these truths change but this file is not updated, implementation and QA will drift quickly.

---

# 31. Summary

This file defines the canonical feature-facing contract for Maps, Save My Gate, and 3D wayfinding in Pilgrims Mobile App.

It establishes:
- the user-facing purpose of the map feature family,
- the free/supporter and privacy boundaries,
- the behavior of Save My Gate and saved anchors,
- destination search, route preview, and active wayfinding rules,
- the proper role of 2D and 3D,
- confidence-aware and offline-aware degraded behavior,
- regroup/map handoffs,
- required analytics, testing, and release-readiness expectations.

Its purpose is to ensure the map feature becomes:
- practically useful,
- honest about uncertainty,
- resilient offline,
- calm under stress,
- and maintainable for long-term AI-assisted implementation.

