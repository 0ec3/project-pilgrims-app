# 09 — PLATFORM ADAPTATION, IOS, ANDROID, AND NATIVE BRIDGES

## Document status
- **Type:** Normative platform adaptation and native-boundary document
- **Priority:** Highest
- **Audience:** Flutter engineers, iOS engineers, Android engineers, design lead, QA, AI coding agents, reviewer agents
- **Purpose:** Define how the shared product and Pilgrims Soft Surface design system adapt to iOS and Android while preserving one visual identity, and how native capabilities are exposed through controlled bridge interfaces.
- **Authority level:** This file is the canonical source of truth for platform-specific UX adaptation, native-bridge boundaries, permission behavior, asset-delivery platform differences, store platform differences, and when platform divergence is allowed or required.
- **Primary dependencies:** `01-README-AND-MASTER-INDEX.md`, `03-PRODUCT-CHARTER-AND-SCOPE.md`, `06-SYSTEM-ARCHITECTURE.md`, `07-FLUTTER-APP-ARCHITECTURE-AND-MODULE-BOUNDARIES.md`, `08-DESIGN-SYSTEM-THEMES-TOKENS-AND-COMPONENTS.md`, `15-OFFLINE-PACKS-SYNC-ASSET-DELIVERY-AND-CACHE-POLICY.md`, `16-MAP-ARCHITECTURE-POSITIONING-ROUTING-3D-AND-OFFLINE-WAYFINDING.md`
- **Related files:** `10`, `11`, `12`, `14`, `17`, `18`–`25`, `27`, `28`, `29`, `30`

---

# 1. Purpose of this file

This file defines platform adaptation and native-boundary behavior for Pilgrims Mobile App.

File `08` owns the canonical visual language, Pilgrims Soft Surface, including Light/Dark theme semantics, surface/depth roles, tokens, and shared component styling.

This file owns:
- platform-specific interaction and presentation adaptation,
- native navigation and system behavior differences,
- native permission and settings handoffs,
- store, notification, location, Bluetooth, map, asset-delivery, and system-capability bridges,
- platform-specific testing and support expectations.

The app must feel like PILGRIMS on both platforms. Platform adaptation may be behaviorally native without creating separate iOS and Android visual identities.

# 2. Platform philosophy

## 2.1 One product, two platform expressions
The app has one product logic, one information architecture, one ethical boundary, one feature set where possible, and one canonical Pilgrims Soft Surface visual identity.

## 2.2 Shared product core
These remain aligned across iOS and Android unless an approved decision changes them:
- product scope,
- feature families,
- data semantics,
- API contracts,
- entitlement rules,
- offline-first behavior,
- map-domain behavior,
- accessibility intent,
- terminology,
- semantic visual roles,
- mandatory Light/Dark appearance support.

## 2.3 Platform-appropriate behavior
These may adapt by platform:
- navigation mechanics and native chrome behavior,
- modal/sheet presentation,
- haptics,
- transition feel,
- system bars,
- permission/settings handoffs,
- store APIs,
- notifications,
- location/BLE,
- asset delivery,
- map/native capability integration.

## 2.4 Shared visual-identity rule
Platform adaptation must not split the visual product identity into an iOS-only doctrine and an Android fallback. Both platforms consume the same Pilgrims Soft Surface semantic/component system from file `08`.

## 2.5 Appearance rule
System, Light, and Dark are supported on both platforms. Platform-specific system behavior may differ, but Light/Dark completeness and semantic meaning must not.

# 3. Platform scope categories

Every cross-platform behavior should be classified into one of the following categories.

## 3.1 Category A — Shared invariant
Must behave the same conceptually on all platforms.

Examples:
- who can join a group
- what a supporter entitlement means
- what Save My Gate does
- what counts as a regroup pin
- what content is offline-capable

## 3.2 Category B — Shared semantics, different presentation
Same meaning, different native expression.

Examples:
- top bar treatment
- bottom navigation/tab chrome
- modal sheet presentation
- map overlay controls
- list row density or interaction feel

## 3.3 Category C — Platform-specific technical implementation
Same product behavior, different native plumbing.

Examples:
- store purchase bridges
- local notifications implementation
- BLE APIs
- asset delivery mechanisms
- map SDK/native integration

## 3.4 Category D — Platform-only behavior by necessity
Rare. Allowed only where platform APIs or store rules force it.

Examples:
- family-sharing nuance surfaced differently per store/platform
- iOS-specific material adaptation details
- Android-specific permission granularity or device settings affordances

---

# 4. Shared platform invariants

The following are non-negotiable across iOS and Android.

## 4.1 Product invariants
- Umrah-first scope
- core rituals and RIC behavior
- ethical monetization boundary
- offline-first essential value
- privacy-light posture
- no passive hidden tracking
- Simple Mode as a supported product capability

## 4.2 Data and contract invariants
- same canonical entity meanings
- same API contract shapes
- same pack lifecycle semantics
- same route graph semantics
- same entitlement gate meanings
- same group-role meanings

## 4.3 UX invariants
- critical flows remain reachable
- important actions remain obvious
- readability takes priority over style
- emergency and safety content remains strong-contrast and low-friction
- the app must still degrade clearly under offline or low-confidence map conditions

---

# 5. Platform adaptation categories in detail

## 5.1 Navigation chrome
Navigation meaning is shared. Native behavior, system bar treatment, transition mechanics, and modal conventions may adapt by platform while consuming the same semantic Soft Surface roles.

## 5.2 Control surfaces
Buttons, chips, overlays, sheets, and bars may adapt interaction feel and native presentation details while preserving component meaning and appearance semantics.

## 5.3 Modal and sheet presentation
Information hierarchy stays shared. Presentation mechanics may follow iOS- or Android-appropriate conventions.

## 5.4 Map overlays
Map controls use the shared Pilgrims Soft Surface map-overlay roles in both Light and Dark. Platform differences must never reduce route clarity, confidence honesty, label readability, or tap reliability.

## 5.5 Permission prompts and settings handoff
Native permission models and system-settings affordances are platform-specific. Product copy and explanation remain consistent with files `11` and `12`.

---

# 6. iOS adaptation strategy

## 6.1 iOS design goals
On iOS, the app should feel refined, calm, modern, and natural within Apple platform conventions while remaining recognizably PILGRIMS.

## 6.2 iOS expression rule
Use the shared Pilgrims Soft Surface semantic system. iOS may use native translucent/system material where platform conventions make it appropriate, but transparency is not the product identity and must not replace the semantic surface hierarchy.

## 6.3 iOS structural behavior
iOS may favor native-feeling navigation transitions, sheets, haptics, system-bar behavior, and platform control conventions where they do not conflict with product truth.

## 6.4 iOS appearance behavior
System appearance follows iOS system appearance. Explicit Light or Dark user override must apply immediately and persist locally.

## 6.5 Accessibility rule on iOS
Reduced motion, reduced transparency, increased contrast, text-size, and assistive-technology settings must simplify decorative depth/material and strengthen boundaries without changing semantics.

---

# 7. Android adaptation strategy

## 7.1 Android design goals
On Android, the app should feel refined, calm, modern, and natural within Android conventions while remaining recognizably PILGRIMS.

## 7.2 Android expression rule
Android uses the same Pilgrims Soft Surface semantic system and must not be treated as a secondary solid-surface fallback. Native behavior may adapt where Android conventions require it.

## 7.3 Android structural behavior
Android may favor platform-appropriate navigation transitions, predictive/back behavior where applicable, sheets/dialogs, haptics, system bars, and permission/settings patterns.

## 7.4 Android appearance behavior
System appearance follows Android system appearance. Explicit Light or Dark user override must apply immediately and persist locally.

## 7.5 Accessibility rule on Android
Contrast, large text, reduced-motion equivalents, accessibility services, and system capabilities must be respected. Decorative depth cannot become the only boundary or state cue.

# 8. Shared design system vs platform adaptation boundary

## 8.1 Shared design system owns
- semantic color roles
- text roles
- spacing roles
- shape/radius families
- motion token families
- component meanings
- content hierarchy
- accessibility requirements

## 8.2 Platform adaptation layer owns
- how those semantics are rendered per platform
- which material treatment variant is used
- bar and overlay presentation differences
- transition selection by platform
- native integration-specific visual affordances

## 8.3 Feature module rule
Feature modules must consume platform-adapted shared components or theme extensions, not hand-roll platform differences per screen.

---

# 9. Native bridge philosophy

## 9.1 Native code should be deliberate and bounded
Native bridges exist to expose platform capabilities that Flutter alone should not directly own or that require platform-specific performance and APIs.

## 9.2 Bridge goals
Native bridges must:
- expose stable APIs to Flutter
- isolate provider/platform details
- support testing and mocking
- keep product semantics in Dart/domain layers where possible
- reduce plugin sprawl and random direct platform channel usage

## 9.3 Bridge anti-goal
Do not put product business rules in native bridge code unless the rule is inherently platform-native and documented.

## 9.4 Preferred bridge style
Use typed, explicit bridge contracts. Flutter’s platform integration guidance and plugin/package guidance support typed platform-channel or generated-interface approaches instead of ad hoc channel strings scattered through the app. ([docs.flutter.dev](https://docs.flutter.dev/platform-integration/platform-channels))

---

# 10. Canonical native bridge catalog

The following bridge surfaces are considered canonical for this project.

## 10.1 `StoreBridge`
Purpose:
- initiate purchase
- retrieve platform purchase references
- restore transaction state when appropriate
- return normalized purchase data to trusted backend flows

### Rule
Bridge returns platform-native purchase references/status, but trusted entitlement truth still comes from backend validation.

## 10.2 `NotificationsBridge`
Purpose:
- request notification permissions
- schedule local reminders
- cancel/update local reminders
- inspect notification capability state where needed

### Rule
Reminder semantics remain shared; scheduling implementation is platform-specific.

## 10.3 `LocationBridge`
Purpose:
- request location permission
- retrieve coarse/fine location state as permitted
- surface service enabled/disabled state

### Rule
Location bridge does not define routing or navigation behavior; it only exposes platform location capability.

## 10.4 `BluetoothBridge`
Purpose:
- request BLE-related permissions
- scan or range beacons if supported
- surface BLE availability and permission state

### Rule
BLE support must be optional and confidence-aware.

## 10.5 `MapBridge`
Purpose:
- expose provider-native rendering and performance-sensitive map functionality
- surface camera operations if provider-specific optimizations are required
- host native map view wrappers when necessary

### Rule
Map domain truth stays in shared map architecture; bridge only provides platform/provider capabilities.

## 10.6 `AssetDeliveryBridge`
Purpose:
- expose any platform-specific asset-delivery services beneath the pack manager abstraction
- query download capability/state if needed
- surface lifecycle events when platform-managed delivery is used

### Rule
The Flutter pack manager should not care whether the platform uses app-managed downloads or system-backed asset delivery, only whether the pack is installed and verified.

## 10.7 `SystemCapabilitiesBridge`
Purpose:
- query reduced transparency / reduced motion / contrast preferences if needed
- query background task capability or other platform-specific capabilities
- query system adaptation flags used in platform rendering decisions

---

# 11. Bridge contract design rules

## 11.1 Shared Dart-facing API first
Each bridge must expose a stable Dart-facing interface owned by shared platform or app-core layers.

## 11.2 Typed payloads only
Bridge payloads must use typed models or generated typed interfaces, not loosely structured maps sprinkled across feature code.

## 11.3 One bridge, one responsibility family
Do not create giant “NativeBridge” or “SystemManager” interfaces that mix unrelated concerns.

## 11.4 No direct feature-widget channel access
Feature widgets and screens must not call platform channels directly.

## 11.5 Mockability rule
Every bridge must be mockable for tests.

---

# 12. Store and entitlement platform differences

## 12.1 Shared product meaning
The product-level meaning of `FREE` and `SUPPORTER` must remain shared across platforms.

## 12.2 Platform purchase differences
Purchase initiation, receipt shape, restoration details, and family-related behavior may differ between stores.

## 12.3 Bridge vs backend rule
- native bridge handles purchase initiation and local platform transaction access
- backend validates and normalizes purchase state
- Flutter receives normalized entitlement state

## 12.4 Family-sharing rule
Do not assume identical family-sharing behavior between Apple and Google. The platform UI may need different explanatory wording while the normalized entitlement contract stays consistent.

---

# 13. Asset-delivery platform differences

## 13.1 Shared product contract
The product contract remains:
- manifest discovery
- download/acquisition
- verification
- install state
- purgeability
- pack-manager ownership

## 13.2 iOS asset-delivery rule
Apple’s current direction introduces Background Assets and Apple-hosted background asset flows as the modern asset-distribution path. Therefore iOS architecture must not hardwire older On-Demand Resources assumptions into the app contract. ([developer.apple.com](https://developer.apple.com/documentation/BackgroundAssets))

## 13.3 Android asset-delivery rule
Android may use app-managed downloads or platform-assisted delivery beneath the same abstraction.

## 13.4 User-experience rule
Regardless of platform, the user should see the same semantic pack states:
- not installed
- downloading
- verifying
- installed
- failed
- purged

---

# 14. Notification and reminder platform differences

## 14.1 Shared product contract
Reminders are local and must work offline from local scheduled state.

## 14.2 Platform implementation differences
Permission flows, scheduling APIs, and edge-case delivery behavior differ by platform and must be handled in the bridge layer.

## 14.3 UX rule
The product should explain reminder availability in shared language while respecting platform-specific permission timing and settings affordances.

---

# 15. Location and BLE permission differences

## 15.1 Shared product contract
The map subsystem may use location or BLE to improve orientation, but the app must still provide useful fallback behavior if permissions are denied.

## 15.2 Platform variation rule
Permission prompts, rationale flows, and settings redirection may differ between iOS and Android.

## 15.3 UX rule
Do not create platform-inappropriate pre-prompt behavior. Permission education should remain short, respectful, and tied to real user value.

## 15.4 No-dependency rule
The product must not become unusable simply because location or BLE permission was denied.

---

# 16. Map rendering platform differences

## 16.1 Shared map semantics
Route graph, anchors, floors, regroup references, and confidence states remain shared.

## 16.2 Platform implementation differences
The rendering engine, native wrappers, and performance-sensitive hooks may differ by platform.

## 16.3 3D rule
3D behavior may be tuned per platform based on SDK capability, device performance, and rendering constraints, but route meaning and fallback behavior must remain aligned.

## 16.4 Feature rule
Feature modules must not care whether the map is implemented with one native view path or another.

---

# 17. Navigation, bars, and modal adaptation

## 17.1 Shared information architecture
The app uses one information architecture.

## 17.2 iOS chrome guidance
- tab and top chrome may lean into material/glass treatment
- modal and sheet hierarchy should feel native to iOS
- transitions should feel fluid and cohesive

## 17.3 Android chrome guidance
- bars and navigation should use stronger material/elevated surfaces
- transitions should feel Android-appropriate and efficient
- modal patterns should remain familiar to Android users

## 17.4 Shared semantics rule
A primary action is still primary, a destructive action is still destructive, and emergency surfaces remain high priority on both platforms.

---

# 18. Platform-specific accessibility rules

## 18.1 Shared accessibility contract
Both platforms must support:
- larger text
- high contrast
- reduced motion handling
- direction-aware layout
- screen-reader accessible semantics
- practical touch targets

## 18.2 iOS-specific accessibility adaptation
Respect platform accessibility states that materially affect material rendering, especially reduced transparency and increased contrast. Apple explicitly ties historical Liquid Glass behavior to these accessibility settings. ([developer.apple.com](https://developer.apple.com/documentation/technologyoverviews/adopting-historical Liquid Glass))

## 18.3 Android-specific accessibility adaptation
Respect platform text scaling, contrast, talkback/navigation, and input-mode differences without requiring separate product logic.

---

# 19. Testing strategy by platform

## 19.1 Shared tests
- product behavior tests
- shared repository/domain tests
- API contract tests
- local persistence tests
- pack state machine tests

## 19.2 iOS-specific tests
- historical Liquid Glass / material fallback behavior with accessibility settings
- Background Assets or iOS asset-delivery integration behavior if used
- store purchase bridge behavior
- map native wrapper behavior on supported iOS versions
- notification scheduling and permission flows

## 19.3 Android-specific tests
- Android surface adaptation behavior
- asset-delivery/download integration behavior
- Play purchase bridge behavior
- notification permission/scheduling differences by OS version
- map native wrapper behavior across representative devices

## 19.4 Bridge tests
Every bridge must have:
- interface-level Dart tests where possible
- mock/fake tests
- platform-specific integration tests for critical paths

---

# 20. Release and support matrix guidance

## 20.1 Supported OS matrix
The exact minimum supported versions must be defined in release planning and testing documents, but this file requires that platform adaptation and native bridge strategy be validated against the intended support matrix before locking implementation choices.

## 20.2 Capability variability rule
Not every supported device will have equal:
- BLE reliability
- 3D rendering capability
- storage performance
- notification behavior
- battery tolerance

The app must degrade by capability rather than failing unpredictably.

---

# 21. Platform QA scenarios

## 21.1 iOS QA must include
- material/glass fallback under Reduce Transparency
- high-contrast and larger-text checks
- map overlays with glass chrome and route readability
- asset download/install behavior through the chosen iOS asset path
- restore purchase and entitlement refresh

## 21.2 Android QA must include
- elevated/material adaptation consistency
- larger-text and talkback checks
- low-end device performance checks
- download/install behavior through the chosen Android asset path
- purchase and restore behavior via Android flows

## 21.3 Shared QA must include
- no-permission location/BLE behavior
- pack install/purge/reinstall behavior
- emergency and safety readability
- Simple Mode cross-platform usability
- map fallback when 3D or precise positioning is unavailable

---

# 22. Recommendations adopted into this platform spec

## 22.1 Recommendation — one Pilgrims visual identity
Both platforms use Pilgrims Soft Surface from file `08`; platform adaptation changes native behavior, not brand identity.

## 22.2 Recommendation — mandatory dual appearance
System, Light, and Dark must work on iOS and Android, including critical surfaces and platform chrome.

## 22.3 Recommendation — native bridges as typed interfaces, not scattered channels
Store, notifications, location, Bluetooth, map, asset-delivery, and system-capability integrations remain typed and mockable.

## 22.4 Recommendation — asset delivery remains abstracted from product contract
Platform delivery implementations may differ while pack/product semantics remain shared.

## 22.5 Recommendation — platform differences remain explicit categories
Shared invariant, shared semantics/different presentation, platform-specific implementation, and necessity-driven platform-only behavior remain the governing classification.

# 23. Anti-patterns forbidden by this platform spec

## 23.1 Forking visual identity by platform
Do not create separate iOS and Android design doctrines.

## 23.2 Treating native material as product identity
Native translucent/material effects may be used where appropriate, but they do not replace Pilgrims Soft Surface semantics.

## 23.3 Direct platform-channel usage inside feature widgets
Feature widgets must depend on platform abstractions.

## 23.4 Giant all-purpose native bridges
Keep bridge responsibilities bounded.

## 23.5 Letting platform-specific code define product business rules
Native code must not invent product truth.

## 23.6 Requiring platform-only capabilities for baseline product usefulness
Graceful fallback remains mandatory.

## 23.7 Platform divergence that changes feature meaning without an approved decision
Presentation may differ; product semantics may not drift.

## 23.8 Treating purchase success on device as trusted entitlement success
Server-trusted entitlement rules remain authoritative.

## 23.9 Partial appearance support
Do not ship a platform where Light or Dark is materially incomplete for required flows.

# 24. When this file must be updated

This file must be updated whenever any of the following changes:
- iOS adaptation rules
- Android adaptation rules
- historical Liquid Glass usage boundaries
- native bridge catalog
- store integration boundary
- asset-delivery platform implementation strategy
- map-native bridge strategy
- permission-flow strategy
- platform support matrix assumptions
- accessibility behaviors tied to system settings

If any of these evolve but this file is not updated, platform-specific behavior, QA, and Flutter implementation boundaries will drift quickly.

---

# 25. Summary

This file defines how Pilgrims Mobile App adapts to iOS and Android while preserving one product architecture.

It establishes:
- what remains shared across platforms
- what may adapt by platform
- how historical Liquid Glass is used on iOS
- how Android should express the product without imitation
- which native bridge families exist and what they own
- how platform-specific purchase, asset, notification, location, BLE, and map behaviors are isolated
- how platform QA and accessibility requirements should be enforced

Its purpose is to keep the app:
- native-feeling on both platforms
- visually coherent
- maintainable in Flutter
- and safe for long-term AI-assisted development without hidden platform drift.

